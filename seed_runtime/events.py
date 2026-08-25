"""Append-only in-memory event ledger."""

from __future__ import annotations

from collections import defaultdict
from contextlib import contextmanager
from copy import deepcopy
from itertools import chain
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
import sqlite3
import zlib
from typing import Any, Iterable, Iterator

from seed_runtime.identities import new_identity, reserve_identity_prefix
from seed_runtime.event import Event, _decode_screened_event_material


# What a ledger can say about a stored occurrence's integrity.
#
# `06.Standing:16` names append-only records permissively, among material
# forms. Nothing in active law requires append-only, and
# nothing here asserts history cannot revision: a `DROP TRIGGER` followed by a
# rewrite of both row and material identity defeats this. The established Assertion is narrower
# — mutation is refused by default, and undetected corruption becomes
# detectable.
VERIFIED = "verified"
UNVERIFIABLE = "unverifiable"
CORRUPTED = "corrupted"


_PREFIX_DOMAIN = b"seed.event-ledger.append-prefix\0"
_EMPTY_PREFIX_IDENTITY = hashlib.sha256(_PREFIX_DOMAIN + b"empty").hexdigest()


@dataclass(frozen=True)
class EventLedgerBoundary:
    """The exact identity of one append prefix.

    Callers may retain and return the value, but only an EventLedger reads
    it. The same ordered prefix yields the same boundary; a boundary does not
    carry an append position.
    """

    identity: str


class InvalidLedgerBoundary(ValueError):
    """A boundary does not denote a prefix of the ledger being read."""


class LedgerIntegrityError(Exception):
    """A durable store cannot supply the integrity its occurrences require."""

# Every persisted field, because an occurrence moved between Localities is as
# altered as one whose material different, and `locality_identity` is now the
# boundary keeping bounded localities apart.
_OCCURRENCE_FIELDS = (
    "identity", "kind", "timestamp", "material", "exact_material",
    "locality_identity",
)
_STORED_OCCURRENCE_FIELDS = (
    "identity", "kind", "timestamp", "material", "exact_material_identity",
    "locality_identity",
)


# Material storage, below the integrity boundary.
#
# The material identity is computed over the exact JSON string, never over the stored
# bytes, so how a material was written down cannot revision what it commits to.
# `#2492` was the same lesson at the other end: two base64 encodings of one
# byte string had to read one account.
#
# Level 1 rather than 6 or 9. `#2494` measured 4.9x against 5.3x at less than
# half the compression cost, and decompression is flat across levels at roughly
# 50 microseconds per material — about one second across the 205,328 reads the
# count layer performs.
_MATERIAL_COMPRESSION_LEVEL = 1


_EVENT_ROW_COLUMNS = (
    "events.*, event_exact_materials.exact_material AS exact_material"
)
_EVENT_ROW_SOURCE = (
    "events LEFT JOIN event_exact_materials ON "
    "event_exact_materials.material_identity = events.exact_material_identity"
)


def _exact_material_identity(exact_material: bytes) -> str:
    """The storage identity of one exact immutable byte sequence."""

    if type(exact_material) is not bytes:
        raise LedgerIntegrityError("exact material identity requires exact bytes")
    return hashlib.sha256(exact_material).hexdigest()


def _stored_material(serialized: str) -> str | bytes:
    """The material as stored: compressed when that is smaller, else as written.

    A material that does not shrink is stored as text, because compressing it
    would cost bytes and reads for nothing. The two forms are told apart on read
    by their type, which SQLite preserves.
    """

    encoded = serialized.encode("utf-8")
    compressed = zlib.compress(encoded, _MATERIAL_COMPRESSION_LEVEL)
    return compressed if len(compressed) < len(encoded) else serialized


class InvalidStoredMaterial(LedgerIntegrityError):
    """A stored material cannot be returned to the string it was identified from."""


def _serialized_material(stored: str | bytes) -> str:
    """The exact JSON string a stored material carries.

    A store written before compression holds text, and reads preserved.

    **Failure to read the stored material is corruption, not a
    compressor error.** Damaged compressed bytes raise `zlib.error`, and bytes
    that decompress but are not UTF-8 raise `UnicodeDecodeError`; both mean the
    stored row no longer carries what it was identified from, which is the
    condition `integrity_of` exists to report. Letting either escape would make
    a corrupted store crash its reader instead of being told about it.
    """

    if isinstance(stored, bytes):
        try:
            return zlib.decompress(stored).decode("utf-8")
        except (zlib.error, UnicodeDecodeError) as exc:
            raise InvalidStoredMaterial(
                f"a stored material could not be read: {exc}"
            ) from exc
    if not isinstance(stored, str):
        raise InvalidStoredMaterial(
            f"a stored material is {type(stored).__name__}, not text or bytes"
        )
    return stored


def _identity_of_stored_occurrence_material(row: "sqlite3.Row") -> str | None:
    """The material identity of a stored row, or nothing when it cannot be read.

    A row whose material will not decompress cannot reproduce its material
    identity. `integrity_of` reports that result rather than raising it.
    """

    try:
        return _occurrence_material_identity(_stored_occurrence_material(row))
    except LedgerIntegrityError:
        return None


def _stored_occurrence_material(row: "sqlite3.Row") -> dict:
    """A stored row as the material identity was taken over it.

    The material is returned to its exact string because the identity is
    taken from what the occurrence carries, not its stored form.
    """

    values = dict(row)
    values["material"] = _serialized_material(values["material"])
    reference = values.get("exact_material_identity")
    exact_material = values.get("exact_material")
    if reference is None:
        if exact_material is not None:
            raise LedgerIntegrityError(
                "an absent exact-material reference carries exact bytes"
            )
    elif (
        type(reference) is not str
        or not reference
        or type(exact_material) is not bytes
        or _exact_material_identity(exact_material) != reference
    ):
        raise LedgerIntegrityError(
            "an exact-material reference does not carry its exact bytes"
        )
    return values


def _occurrence_material_identity(row: dict) -> str:
    """A stable material identity over the whole recorded row.

    Every occurrence field must be present. `row.get` returned `None` for an
    absent field and for a null one alike, so a row missing `locality_identity`
    produced the same identity as a row whose Locality was null. SQLite supplies
    every column; other callers are refused when a field is absent.
    """

    missing = [field for field in _OCCURRENCE_FIELDS if field not in row]
    if missing:
        raise LedgerIntegrityError(
            "a material identity requires every recorded field; absent: " + ", ".join(missing)
        )
    return hashlib.sha256(_identified_occurrence_bytes(row)).hexdigest()


def _identified_occurrence_bytes(row: dict) -> bytes:
    exact_material = row["exact_material"]
    if exact_material is not None and type(exact_material) is not bytes:
        raise LedgerIntegrityError("exact material must be stored as bytes or absent")
    represented = json.dumps(
        {
            field: row[field]
            for field in _OCCURRENCE_FIELDS
            if field != "exact_material"
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    exact = b"" if exact_material is None else exact_material
    presence = b"\x00" if exact_material is None else b"\x01"
    return (
        len(represented).to_bytes(8, "big")
        + represented
        + presence
        + len(exact).to_bytes(8, "big")
        + exact
    )


def _exact_occurrence_bytes(event: Event) -> bytes:
    """Exact bytes for the occurrence itself, excluding ledger mechanics."""
    represented = {
        "identity": event.identity,
        "kind": event.kind,
        "timestamp": event.timestamp.isoformat(),
        "material": event.material,
        "exact_material": event.exact_material,
        "locality_identity": event.locality_identity,
    }
    return _identified_occurrence_bytes(represented)


def _next_prefix_identity(previous: str, event: Event) -> str:
    occurrence = _exact_occurrence_bytes(event)
    return hashlib.sha256(
        _PREFIX_DOMAIN
        + bytes.fromhex(previous)
        + len(occurrence).to_bytes(8, "big")
        + occurrence
    ).hexdigest()


class EventLedger:
    """Process-local append-only ledger for recording Seed runtime events."""

    @contextmanager
    def batched(self) -> Iterator[None]:
        """The scope a durable ledger uses to commit once. Nothing here is durable."""

        yield

    def flush(self) -> None:
        """No durable store to commit to."""

    def __init__(self) -> None:
        self._events: list[Event] = []
        self._by_identity: dict[str, Event] = {}
        self._by_locality: dict[str | None, list[Event]] = defaultdict(list)
        self._by_identity_position: dict[str, int] = {}
        self._latest_prefix_identity = _EMPTY_PREFIX_IDENTITY
        self._prefix_identities_by_position: list[str] = [
            _EMPTY_PREFIX_IDENTITY
        ]
        self._boundary_positions: dict[str, int] = {
            _EMPTY_PREFIX_IDENTITY: 0
        }

    def append(
        self,
        kind: str,
        material: dict[str, Any] | None = None,
        *,
        exact_material: bytes | None = None,
        locality_identity: str | None = None,
    ) -> Event:
        """Record an event and return the stored event."""
        event = Event(
            identity=new_identity("evt"),
            kind=kind,
            material=material or {},
            exact_material=exact_material,
            locality_identity=locality_identity,
        )
        self._store(event)
        return event

    def allocate_event_identity(self) -> str:
        """Allocate an identity for material built before `append_many`."""

        return new_identity("evt")

    def mint_identity(self, prefix: str) -> str:
        """Mint one identity in this ledger's identity domain."""

        if type(prefix) is not str or not prefix:
            raise TypeError("one exact identity prefix is required")
        return new_identity(prefix)

    def append_many(
        self,
        events: Iterable[Event],
    ) -> list[Event]:
        """Record pre-built events in order and return the stored events.

        Event granularity remains preserved: each supplied Event is stored as its
        own ledger event. Implementations may batch the underlying persistence
        transaction for storage efficiency.
        """
        stored_events = [deepcopy(event) for event in events]
        self._validate_batch(stored_events)
        for event in stored_events:
            self._store(event)
        return stored_events

    def get(self, event_identity: str) -> Event | None:
        """Return an event by identity, if it exists."""
        return self._by_identity.get(event_identity)

    def occurrences_in_append_order(
        self,
        event_identities: Iterable[str],
        *,
        locality_identity: str,
    ) -> list[Event]:
        """Resolve exact occurrences and refuse a false append order."""

        events = []
        prior_position = 0
        seen = set()
        for event_identity in event_identities:
            if event_identity in seen:
                raise ValueError("one occurrence was supplied more than once")
            event = self.get(event_identity)
            position = self._by_identity_position.get(event_identity)
            if (
                event is None
                or position is None
                or event.locality_identity != locality_identity
            ):
                raise ValueError("the supplied occurrence is not in this Locality")
            if position <= prior_position:
                raise ValueError("the supplied occurrences are not in append order")
            events.append(event)
            seen.add(event_identity)
            prior_position = position
        return events

    def append_boundary(self) -> EventLedgerBoundary:
        """Capture the exact identity of the current append prefix."""
        return EventLedgerBoundary(self._latest_prefix_identity)

    def append_boundary_through_occurrence(
        self, event_identity: str
    ) -> EventLedgerBoundary:
        """Resolve the existing append boundary ending at one occurrence.

        The occurrence identity remains the caller's address.  This returns
        the ledger's already-derived prefix identity at that exact occurrence;
        it does not mint another boundary or consult the moving tip.
        """

        if type(event_identity) is not str or not event_identity:
            raise InvalidLedgerBoundary(
                "append boundary requires one exact occurrence identity"
            )
        position = self._by_identity_position.get(event_identity)
        if position is None:
            raise InvalidLedgerBoundary(
                "occurrence does not belong to this append sequence"
            )
        return EventLedgerBoundary(self._prefix_identities_by_position[position])

    def _position_through(self, through: EventLedgerBoundary | None) -> int:
        if through is None:
            return len(self._events)
        position = self._boundary_positions.get(through.identity)
        if position is None:
            raise InvalidLedgerBoundary(
                "boundary does not denote an append prefix of this ledger"
            )
        return position

    def list(
        self,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        """Return events in append order."""
        position = self._position_through(through)
        return list(self._events[:position])

    def list_events(
        self,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        return self.list(through=through)

    def _exact_material_reference(self, event_identity: str) -> str | None:
        """Address exact bytes without making the address occurrence material."""

        event = self.get(event_identity)
        if event is None or event.exact_material is None:
            return None
        return _exact_material_identity(event.exact_material)

    def integrity_of(self, event_identity: str) -> str:
        """What this ledger can say about a stored occurrence's integrity.

        An in-memory ledger holds objects, not stored bytes, so there is no
        recorded material to have diverged from. It reports
        `UNVERIFIABLE` rather than `VERIFIED`: nothing was protected, and
        saying otherwise would manufacture the guarantee.
        """
        return UNVERIFIABLE

    def list_locality(
        self,
        locality_identity: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        """Return one Locality's events in append order."""
        position = self._position_through(through)
        return [
            event
            for event in self._by_locality.get(locality_identity, ())
            if self._by_identity_position[event.identity] <= position
        ]

    def has_locality(
        self,
        locality_identity: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> bool:
        """Whether at least one occurrence establishes this Locality boundary."""
        position = self._position_through(through)
        for event in self._by_locality.get(locality_identity, ()):
            if self._by_identity_position[event.identity] > position:
                break
            return True
        return False

    def latest_locality_event(self, locality_identity: str) -> Event | None:
        """Return the latest exact occurrence in a Locality, if present."""

        events = self._by_locality.get(locality_identity, ())
        return events[-1] if events else None

    def prior_locality_event(
        self, event_identity: str, locality_identity: str
    ) -> Event | None:
        """Return the nearest earlier occurrence in the same Locality."""

        event = self.get(event_identity)
        position = self._by_identity_position.get(event_identity)
        if event is None or position is None or event.locality_identity != locality_identity:
            raise ValueError("the occurrence is not in this Locality")
        for earlier in reversed(self._events[: position - 1]):
            if earlier.locality_identity == locality_identity:
                return earlier
        return None

    def iter_locality_kind(
        self,
        locality_identity: str,
        kind: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> Iterator[Event]:
        """Yield one kind from one Locality without collecting a result list."""
        position = self._position_through(through)
        for event in self._by_locality.get(locality_identity, ()):
            if self._by_identity_position[event.identity] > position:
                break
            if event.kind == kind:
                yield event

    def iter_locality_kind_identities(
        self,
        locality_identity: str,
        kind: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> Iterator[str]:
        """Yield the identities of one kind from one Locality, in append order.

        The same bounded rows in the same order as `iter_locality_kind`, returning
        only their identities. It does not read or inspect occurrence
        materials. A caller requiring occurrence content must use the occurrence
        read; `integrity_of` remains the separate integrity boundary.
        """
        for event in self.iter_locality_kind(
            locality_identity, kind, through=through
        ):
            yield event.identity

    def extend(self, events: Iterable[Event]) -> None:
        """Append supplied events while preserving order and identities."""
        self.append_many(events)

    def _store(self, event: Event) -> None:
        if event.identity in self._by_identity:
            raise ValueError(f"event identity already exists: {event.identity}")
        # Canonicalization may refuse a material. Derive before making the
        # occurrence visible anywhere so a failed append cannot leave event
        # history ahead of its append-prefix mechanics.
        identity = _next_prefix_identity(self._latest_prefix_identity, event)
        position = len(self._events) + 1
        self._events.append(event)
        self._by_identity[event.identity] = event
        self._by_locality[event.locality_identity].append(event)
        self._latest_prefix_identity = identity
        self._prefix_identities_by_position.append(identity)
        self._boundary_positions[identity] = position
        self._by_identity_position[event.identity] = position

    def _validate_batch(self, events: list[Event]) -> None:
        seen: set[str] = set()
        for event in events:
            if event.identity in self._by_identity or event.identity in seen:
                raise ValueError(f"event identity already exists: {event.identity}")
            seen.add(event.identity)


class SQLiteEventLedger(EventLedger):
    """SQLite-backed ledger with the same public API as EventLedger."""

    # Every minted-identity prefix this ledger stores and a later process may mint
    # again. A prefix missing here is a collision waiting for the second
    # process: `new_identity` counts from 1 per process, so the second console
    # lifetime against a durable ledger reissues the first one's identities.
    #
    # The four operator-console prefixes were absent until `#2413` connected
    # the console to a durable ledger, at which point the second `seed --db`
    # invocation aborted on a duplicate minted identity. Nothing was
    # wrong with them before: no console had ever written durable history.
    # Every entry is minted by current runtime code and may be carried by a
    # durable occurrence.
    _RESERVABLE_PREFIXES = frozenset({
        "operator_material", "checkpoint_locality", "locality",
        "byte_position_pair_measurement_act",
        "byte_position_pair_measurement_assignment",
        "byte_position_pair_measurement_assignment_subject",
        "byte_position_pair_measurement_occurrence",
        "byte_position_pair_measurement_result", "byte_measurement_act",
        "byte_measurement_assignment", "byte_measurement_assignment_subject",
        "byte_measurement_occurrence", "byte_measurement_result",
        "candidate_responsibility_subject",
        "candidate_responsibility_scope",
        "candidate_applicability_act",
        "candidate_applicability_act_occurrence",
        "candidate_applicability_result",
        "candidate_act",
        "candidate_act_occurrence",
        "candidate_result",
        "byte_pair_applicability_act", "byte_pair_applicability_occurrence",
        "byte_pair_applicability_result",
        "recorded_pair_comparison_assignment",
        "recorded_pair_comparison_assignment_subject",
        "recorded_pair_comparison_applicability_act",
        "recorded_pair_comparison_applicability_occurrence",
        "recorded_pair_comparison_applicability_result",
        "recorded_pair_comparison_act",
        "recorded_pair_comparison_occurrence",
        "recorded_pair_comparison_result",
        "recorded_pair_comparison_earlier_input_relation",
        "recorded_pair_comparison_later_input_relation",
        "recorded_pair_comparison_earlier_participation",
        "recorded_pair_comparison_later_participation",
        "assertion_locality_movement",
        "assertion_locality_movement_assignment",
        "assertion_locality_movement_assignment_subject",
        "assertion_locality_movement_act",
        "assertion_locality_movement_occurrence",
        "assertion_locality_movement_result",
        "occurrence_position_measurement_act",
        "occurrence_position_measurement_assignment",
        "occurrence_position_measurement_assignment_subject",
        "occurrence_position_measurement_occurrence",
        "occurrence_position_measurement_result",
        "byte_pair_occurrence_position_assignment",
        "byte_pair_occurrence_position_assignment_subject",
        "byte_pair_occurrence_position_measurement_act",
        "byte_pair_occurrence_position_measurement_act_occurrence",
        "byte_pair_occurrence_position_measurement_result",
        "addressed_byte_occurrence_reference_assignment",
        "addressed_byte_occurrence_reference_assignment_subject",
        "addressed_byte_occurrence_reference_applicability_act",
        "addressed_byte_occurrence_reference_applicability_act_occurrence",
        "addressed_byte_occurrence_reference_applicability_result",
        "addressed_byte_occurrence_reference_determination_measurement_act",
        "addressed_byte_occurrence_reference_determination_measurement_act_occurrence",
        "addressed_byte_occurrence_reference_determination_measurement_result",
        "act_of_measurement_of_recurrent_byte_pair_occurrence_position",
        "act_occurrence_of_measurement_of_recurrent_byte_pair_occurrence_position",
        "result_of_measurement_of_recurrent_byte_pair_occurrence_position",
        "recurrent_pair_position_measurement_assignment",
        "recurrent_pair_position_measurement_assignment_subject",
        "shared_pair_position_assignment_identity",
        "shared_pair_position_assignment_subject_identity",
        "shared_pair_position_applicability_act_identity",
        "shared_pair_position_applicability_act_occurrence_identity",
        "shared_pair_position_applicability_result_identity",
        "shared_pair_position_measurement_act_identity",
        "shared_pair_position_measurement_act_occurrence_identity",
        "shared_pair_position_measurement_result_identity",
        "shared_pair_position_first_input_relation_identity",
        "shared_pair_position_second_input_relation_identity",
        "shared_pair_position_first_participation_relation_identity",
        "shared_pair_position_second_participation_relation_identity",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_assignment",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_assignment_subject",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_occurrence",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_compare_act",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_compare_occurrence",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_result",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_path_input_relation",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_comparison_input_relation",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_path_participation",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_comparison_participation",
        "ordered_path_source_position_material_applicability_act_identity",
        "ordered_path_source_position_material_applicability_act_occurrence_identity",
        "ordered_path_source_position_material_applicability_result_identity",
        "ordered_path_source_position_material_compare_act_identity",
        "ordered_path_source_position_material_compare_act_occurrence_identity",
        "ordered_path_source_position_material_compare_result_identity",
        "ordered_path_source_position_material_first_input_relation_identity",
        "ordered_path_source_position_material_second_input_relation_identity",
        "ordered_path_source_position_material_first_participation_relation_identity",
        "ordered_path_source_position_material_second_participation_relation_identity",
        "source_position_compare_applicability_act",
        "source_position_compare_applicability_act_occurrence",
        "source_position_compare_applicability_result",
        "source_position_compare_act",
        "source_position_compare_act_occurrence",
        "source_position_compare_result",
        "source_position_compare_first_participation",
        "source_position_compare_second_participation",
        "source_position_measurement_act",
        "source_position_measurement_act_occurrence",
        "source_position_measurement_result",
        "source_position_recurrence_measurement_act",
        "source_position_recurrence_measurement_act_occurrence",
        "source_position_recurrence_measurement_result",
        "recurrence_corresponding_source_position_material_measurement_act",
        "recurrence_corresponding_source_position_material_measurement_act_occurrence",
        "recurrence_corresponding_source_position_material_measurement_result",
        "source_position_responsibility",
        "source_position_responsibility_subject",
        "recurrent_result_exact_material_measurement_act",
        "recurrent_result_exact_material_measurement_act_occurrence",
        "recurrent_result_exact_material_measurement_result",
        "operator_invocation_locality",
        "operator_invocation_locality_act",
        "operator_invocation_locality_act_occurrence",
        "operator_invocation_locality_assignment",
        "operator_invocation_locality_assignment_subject",
        "operator_invocation_locality_relation_occurrence",
        "operator_invocation_locality_result",
        "operator_invocation_locality_scope",
        "recorded_standing_boundary_locality",
        "recorded_standing_boundary_locality_act",
        "recorded_standing_boundary_locality_act_occurrence",
        "recorded_standing_boundary_locality_assignment",
        "recorded_standing_boundary_locality_assignment_subject",
        "recorded_standing_boundary_locality_relation_occurrence",
        "recorded_standing_boundary_locality_result",
        "recorded_standing_boundary_locality_scope",
        "standing_boundary_reference_act_occurrence",
        "standing_boundary_reference_recording_act",
        "standing_boundary_reference_result",
        "standing_locality",
        "standing_locality_continuation_act",
        "standing_locality_continuation_occurrence",
        "standing_locality_continuation_relation_occurrence",
        "standing_locality_continuation_result_boundary",
        "standing_locality_continuation_responsibility_assignment",
        "standing_locality_continuation_responsibility_subject",
    })

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self._batch_depth = 0
        self._connection = sqlite3.connect(database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        # A durable prefix chain has to be extended by every writer. Older
        # writers do not register this connection-local function, so the
        # durable trigger installed below refuses their inserts instead of
        # admitting an occurrence outside the chain.
        self._connection.create_function(
            "seed_prefix_writer", 0, lambda: 1, deterministic=True
        )
        if self._connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' "
            "AND name = 'event_references'"
        ).fetchone() is not None:
            raise LedgerIntegrityError(
                f"{database_path} carries the withdrawn runtime occurrence-reference index"
            )
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS event_exact_materials (
                material_identity TEXT PRIMARY KEY,
                exact_material BLOB NOT NULL
            ) WITHOUT ROWID
            """)
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS events (
                identity TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                material TEXT NOT NULL,
                exact_material_identity TEXT,
                locality_identity TEXT,
                occurrence_material_identity TEXT NOT NULL,
                FOREIGN KEY (exact_material_identity)
                    REFERENCES event_exact_materials(material_identity)
            )
            """)
        # Minted identity counters, kept durably instead of read.
        #
        # `#2414` measured the read: every material of every event
        # deserialized and walked on every open, to read the highest issued
        # number per prefix. That is a whole-history read for a result of a few
        # integers, and it grows without bound — 36.9s at 100,000 events,
        # extrapolating to about 356s at a million.
        #
        # This table is not an occurrence. It records no Assertion and
        # supports no standing; it is ledger mechanics, and the `events`
        # mutation refusal deliberately does not cover it.
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS identity_reservations (
                prefix TEXT PRIMARY KEY,
                max_number INTEGER NOT NULL
            )
            """)
        # A store without the current occurrence fields is not this store.
        columns = {
            row["name"]: row
            for row in self._connection.execute("PRAGMA table_info(events)")
        }
        exact_columns = set(_STORED_OCCURRENCE_FIELDS) | {
            "occurrence_material_identity"
        }
        if set(columns) != exact_columns:
            raise LedgerIntegrityError(
                f"{database_path} does not carry the current occurrence fields"
            )
        if "occurrence_material_identity" not in columns:
            raise LedgerIntegrityError(
                f"{database_path} has an events table without occurrence_material_identity. "
                "Seed does not migrate pre-integrity ledgers; a store either "
                "carries material identities from birth or is not supported"
            )
        if not columns["occurrence_material_identity"]["notnull"]:
            # A nullable column permits an occurrence without this identity.
            raise LedgerIntegrityError(
                f"{database_path} declares occurrence_material_identity nullable, so it was not "
                "born with the current integrity schema"
            )
        exact_material_columns = {
            row["name"]: row
            for row in self._connection.execute(
                "PRAGMA table_info(event_exact_materials)"
            )
        }
        if set(exact_material_columns) != {
            "material_identity", "exact_material"
        } or not exact_material_columns["exact_material"]["notnull"]:
            raise LedgerIntegrityError(
                f"{database_path} does not carry the current exact-material store"
            )
        # Refuse the mutation the API never performs, so that code outside the
        # API cannot perform it either. A `DROP TRIGGER` removes this; that is
        # what keeps the Assertion at "refused by default" rather than "immutable".
        self._connection.execute("""
            CREATE TRIGGER IF NOT EXISTS events_refuse_update
            BEFORE UPDATE ON events
            BEGIN SELECT RAISE(ABORT, 'recorded occurrences do not revision'); END
            """)
        self._connection.execute("""
            CREATE TRIGGER IF NOT EXISTS events_refuse_delete
            BEFORE DELETE ON events
            BEGIN SELECT RAISE(ABORT, 'recorded occurrences are not removed'); END
            """)
        self._connection.execute("""
            CREATE TRIGGER IF NOT EXISTS event_exact_materials_refuse_update
            BEFORE UPDATE ON event_exact_materials
            BEGIN SELECT RAISE(ABORT, 'exact material does not revision'); END
            """)
        self._connection.execute("""
            CREATE TRIGGER IF NOT EXISTS event_exact_materials_refuse_delete
            BEFORE DELETE ON event_exact_materials
            BEGIN SELECT RAISE(ABORT, 'exact material is not removed'); END
            """)
        # The boundary Localities are actually selected by. Without it the
        # Locality read returns one Locality after scanning every row, which is
        # bounded in what it returns and not in what it reads.
        self._connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_locality
            ON events(locality_identity)
            """)
        self._connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_locality_kind
            ON events(locality_identity, kind)
            """)
        self._ensure_prefix_identities()
        self._connection.commit()
        max_event_number = self._max_event_identity_number()
        self._next_event_number = max_event_number + 1
        reserve_identity_prefix("evt", max_event_number)
        for prefix, max_number in self._connection.execute(
            "SELECT prefix, max_number FROM identity_reservations"
        ):
            reserve_identity_prefix(prefix, max_number)

    def append(
        self,
        kind: str,
        material: dict[str, Any] | None = None,
        *,
        exact_material: bytes | None = None,
        locality_identity: str | None = None,
    ) -> Event:
        event = Event(
            identity=self._new_event_identity(),
            kind=kind,
            material=material or {},
            exact_material=exact_material,
            locality_identity=locality_identity,
        )
        self._insert(event)
        return event

    def allocate_event_identity(self) -> str:
        """Allocate an identity for material built before `append_many`."""

        return self._new_event_identity()

    def mint_identity(self, prefix: str) -> str:
        """Mint one identity without interpreting occurrence material."""

        if type(prefix) is not str or not prefix:
            raise TypeError("one exact identity prefix is required")
        if self._batch_depth:
            return self._mint_identity_without_commit(prefix)
        with self._connection:
            return self._mint_identity_without_commit(prefix)

    def _mint_identity_without_commit(self, prefix: str) -> str:
        self._connection.execute(
            "INSERT INTO identity_reservations (prefix, max_number) "
            "VALUES (?, 0) ON CONFLICT(prefix) DO NOTHING",
            (prefix,),
        )
        row = self._connection.execute(
            "SELECT max_number FROM identity_reservations WHERE prefix = ?",
            (prefix,),
        ).fetchone()
        max_number = int(row["max_number"])
        reserve_identity_prefix(prefix, max_number)
        identity = new_identity(prefix)
        number = _numeric_number(identity, prefix)
        if number is None:
            raise LedgerIntegrityError("minted identity has no exact number")
        self._persist_reservations({prefix: number})
        return identity

    def append_many(
        self,
        events: Iterable[Event],
    ) -> list[Event]:
        """Persist pre-built events in order using a single SQLite transaction."""
        stored_events = [deepcopy(event) for event in events]
        self._validate_sqlite_batch(stored_events)
        # One transaction, occurrences and their identity reservations
        # together. `#2428` stated that a reservation is written in the same
        # transaction as the occurrence that carried the identity, and
        # `append` does that; this path did not. A failure between the two
        # commits left durable occurrences carrying identities whose counters
        # were stale on reopen, which is the collision `#2428` exists to
        # prevent. `evt` is partly shielded because open reads the maximum
        # event identity separately; the material and Locality prefixes are not.
        with self._connection:
            for event in stored_events:
                event_rowid = self._insert_without_commit(event)
                self._insert_prefix_identity(event, event_rowid)
                self._persist_reservations(self._reservable_identity_numbers(event))
        for event in stored_events:
            self._advance_event_counter(event.identity)
        return stored_events

    def get(self, event_identity: str) -> Event | None:
        row = self._connection.execute(
            f"SELECT {_EVENT_ROW_COLUMNS} FROM {_EVENT_ROW_SOURCE} "
            "WHERE events.identity = ?",
            (event_identity,),
        ).fetchone()
        return self._row_to_event(row) if row is not None else None

    def occurrences_in_append_order(
        self,
        event_identities: Iterable[str],
        *,
        locality_identity: str,
    ) -> list[Event]:
        """Resolve exact durable occurrences and refuse a false append order."""

        identities = list(event_identities)
        if len(set(identities)) != len(identities):
            raise ValueError("one occurrence was supplied more than once")
        events = []
        prior_rowid = 0
        for event_identity in identities:
            row = self._connection.execute(
                f"SELECT events.rowid, {_EVENT_ROW_COLUMNS} "
                f"FROM {_EVENT_ROW_SOURCE} WHERE events.identity = ?",
                (event_identity,),
            ).fetchone()
            if row is None or row["locality_identity"] != locality_identity:
                raise ValueError("the supplied occurrence is not in this Locality")
            rowid = int(row["rowid"])
            if rowid <= prior_rowid:
                raise ValueError("the supplied occurrences are not in append order")
            events.append(self._row_to_event(row))
            prior_rowid = rowid
        return events

    def append_boundary(self) -> EventLedgerBoundary:
        """Capture the exact identity of the current durable append prefix."""
        self._validate_prefix_identities_after_external_commit()
        row = self._connection.execute(
            "SELECT identity FROM event_prefix_identities "
            "ORDER BY position DESC LIMIT 1"
        ).fetchone()
        return EventLedgerBoundary(
            row["identity"] if row is not None else _EMPTY_PREFIX_IDENTITY
        )

    def append_boundary_through_occurrence(
        self, event_identity: str
    ) -> EventLedgerBoundary:
        """Resolve the existing append boundary ending at one occurrence."""

        if type(event_identity) is not str or not event_identity:
            raise InvalidLedgerBoundary(
                "append boundary requires one exact occurrence identity"
            )
        self._validate_prefix_identities_after_external_commit()
        row = self._connection.execute(
            "SELECT identity FROM event_prefix_identities "
            "WHERE event_identity = ?",
            (event_identity,),
        ).fetchone()
        if row is None:
            raise InvalidLedgerBoundary(
                "occurrence does not belong to this append sequence"
            )
        return EventLedgerBoundary(row["identity"])

    def _rowid_through(self, through: EventLedgerBoundary | None) -> int | None:
        if through is None:
            return None
        self._validate_prefix_identities_after_external_commit()
        if through.identity == _EMPTY_PREFIX_IDENTITY:
            return 0
        row = self._connection.execute(
            "SELECT event_rowid FROM event_prefix_identities "
            "WHERE identity = ?",
            (through.identity,),
        ).fetchone()
        if row is None:
            raise InvalidLedgerBoundary(
                "boundary does not denote an append prefix of this ledger"
            )
        return int(row["event_rowid"])

    def list(
        self,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        rowid = self._rowid_through(through)
        boundary_sql = "" if rowid is None else " WHERE events.rowid <= ?"
        boundary_args: tuple[Any, ...] = () if rowid is None else (rowid,)
        rows = self._connection.execute(
            f"SELECT {_EVENT_ROW_COLUMNS} FROM {_EVENT_ROW_SOURCE}"
            f"{boundary_sql} ORDER BY events.rowid",
            boundary_args,
        ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def list_events(
        self,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        return self.list(through=through)

    def list_locality(
        self,
        locality_identity: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        rowid = self._rowid_through(through)
        boundary = "" if rowid is None else "AND events.rowid <= ? "
        args: tuple[Any, ...] = (locality_identity,) if rowid is None else (locality_identity, rowid)
        rows = self._connection.execute(
            f"SELECT {_EVENT_ROW_COLUMNS} FROM {_EVENT_ROW_SOURCE} "
            "WHERE events.locality_identity = ? "
            + boundary
            + "ORDER BY events.rowid",
            args,
        ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def has_locality(
        self,
        locality_identity: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> bool:
        rowid = self._rowid_through(through)
        boundary = "" if rowid is None else "AND events.rowid <= ? "
        args: tuple[Any, ...] = (locality_identity,) if rowid is None else (locality_identity, rowid)
        row = self._connection.execute(
            "SELECT 1 FROM events WHERE locality_identity = ? "
            + boundary
            + "LIMIT 1",
            args,
        ).fetchone()
        return row is not None

    def latest_locality_event(self, locality_identity: str) -> Event | None:
        """Return the latest exact occurrence in a Locality, if present."""

        row = self._connection.execute(
            f"SELECT {_EVENT_ROW_COLUMNS} FROM {_EVENT_ROW_SOURCE} "
            "WHERE events.locality_identity = ? ORDER BY events.rowid DESC LIMIT 1",
            (locality_identity,),
        ).fetchone()
        return None if row is None else self._row_to_event(row)

    def prior_locality_event(
        self, event_identity: str, locality_identity: str
    ) -> Event | None:
        """Return the nearest earlier occurrence in the same Locality."""

        event_row = self._connection.execute(
            "SELECT rowid, locality_identity FROM events WHERE identity = ?",
            (event_identity,),
        ).fetchone()
        if event_row is None or event_row["locality_identity"] != locality_identity:
            raise ValueError("the occurrence is not in this Locality")
        row = self._connection.execute(
            f"SELECT {_EVENT_ROW_COLUMNS} FROM {_EVENT_ROW_SOURCE} "
            "WHERE events.locality_identity = ? AND events.rowid < ? "
            "ORDER BY events.rowid DESC LIMIT 1",
            (locality_identity, int(event_row["rowid"])),
        ).fetchone()
        return None if row is None else self._row_to_event(row)

    def iter_locality_kind(
        self,
        locality_identity: str,
        kind: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> Iterator[Event]:
        rowid = self._rowid_through(through)
        boundary = "" if rowid is None else "AND events.rowid <= ? "
        args: tuple[Any, ...] = (
            (locality_identity, kind) if rowid is None else (locality_identity, kind, rowid)
        )
        rows = self._connection.execute(
            f"SELECT {_EVENT_ROW_COLUMNS} FROM {_EVENT_ROW_SOURCE} "
            "WHERE events.locality_identity = ? "
            "AND events.kind = ? " + boundary + "ORDER BY events.rowid",
            args,
        )
        for row in rows:
            yield self._row_to_event(row)

    def iter_locality_kind_identities(
        self,
        locality_identity: str,
        kind: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> Iterator[str]:
        """Read one column of the same bounded rows `iter_locality_kind` reads.

        The same bounded rows and order, returning only identities.

        **This does not read or inspect occurrence materials**, and the
        difference is nameable rather than merely cheaper: the occurrence read
        decodes each material through `_decode_screened_event_material`, which
        refuses a durable material carrying a secret field name. An identity read
        performs no such screen, because it hands no material to its caller. A
        caller requiring occurrence content must use the occurrence read, and
        `integrity_of` remains the separate integrity boundary.

        The signature-count inputs run measured why this is worth its own
        read: one 300-occurrence material-acquisition result read costs 7.09 ms
        as Events and 0.25 ms as identities, because 902 bytes of JSON per
        occurrence are decoded and discarded by a caller that keeps only the
        identity.
        """
        rowid = self._rowid_through(through)
        boundary = "" if rowid is None else "AND rowid <= ? "
        args: tuple[Any, ...] = (
            (locality_identity, kind) if rowid is None else (locality_identity, kind, rowid)
        )
        rows = self._connection.execute(
            "SELECT identity FROM events WHERE locality_identity = ? "
            "AND kind = ? " + boundary + "ORDER BY rowid",
            args,
        )
        for row in rows:
            yield row[0]

    def integrity_of(self, event_identity: str) -> str:
        """Recompute the stored row's material identity and compare it with the recorded one.

        Verification belongs where the guarantee is asserted. `#2416` made
        ordinary reads cheap, and putting a material identity on `get` or `list_locality`
        would charge every reader for an obligation only an Act with participating inputs
        carries.
        """
        row = self._connection.execute(
            f"SELECT {_EVENT_ROW_COLUMNS} FROM {_EVENT_ROW_SOURCE} "
            "WHERE events.identity = ?",
            (event_identity,),
        ).fetchone()
        if row is None:
            # Nothing is stored, so there is nothing to have diverged. This is
            # the absence of an occurrence, not a durable one lacking integrity.
            return UNVERIFIABLE
        # A durable occurrence always carries a material identity: the store is refused
        # at open otherwise. So this returns VERIFIED or CORRUPTED, never
        # UNVERIFIABLE. Leaving a supported unverifiable path here would let it
        # be cited later as yield_relation that durable references need no integrity.
        return (
            VERIFIED
            if _identity_of_stored_occurrence_material(row) == row["occurrence_material_identity"]
            else CORRUPTED
        )

    def extend(self, events: Iterable[Event]) -> None:
        self.append_many(events)

    def close(self) -> None:
        self._connection.close()

    def _insert(self, event: Event) -> None:
        if self._batch_depth:
            self._write_without_commit(event)
        else:
            with self._connection:
                self._write_without_commit(event)
        self._advance_event_counter(event.identity)

    def _write_without_commit(self, event: Event) -> None:
        event_rowid = self._insert_without_commit(event)
        self._insert_prefix_identity(event, event_rowid)
        self._persist_reservations(self._reservable_identity_numbers(event))

    @contextmanager
    def batched(self) -> Iterator[None]:
        """Hold one transaction open across appends until this scope closes.

        What differences is how many times the store is committed, not what a
        commit contains: each occurrence still reaches the store paired with
        its prefix identity, because both are written before either is
        committed. A store that loses this scope loses whole occurrences and
        keeps a chain that accounts for exactly the ones it kept.

        Occurrences appended inside are not durable until the scope closes or
        :meth:`flush` is called. An act that must not proceed until an
        occurrence is durable calls `flush` itself; nothing here knows which
        acts those are.
        """

        self._batch_depth += 1
        try:
            yield
        except BaseException:
            if self._batch_depth == 1:
                self._connection.rollback()
            raise
        finally:
            self._batch_depth -= 1
        if not self._batch_depth:
            self._connection.commit()

    def flush(self) -> None:
        """Commit what this scope has appended so far, and stay open."""

        self._connection.commit()

    def _ensure_prefix_identities(self) -> None:
        """Create or validate the ledger-local append-prefix mechanics.

        An existing store without the table receives one atomic derivation from
        the append sequence it currently represents. This does not alter or
        strengthen any occurrence's integrity result.
        """
        existed = self._connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' "
            "AND name = 'event_prefix_identities'"
        ).fetchone() is not None
        self._connection.execute("BEGIN IMMEDIATE")
        try:
            self._connection.execute("""
                CREATE TABLE IF NOT EXISTS event_prefix_identities (
                    position INTEGER PRIMARY KEY,
                    event_rowid INTEGER NOT NULL UNIQUE,
                    event_identity TEXT NOT NULL UNIQUE,
                    identity TEXT NOT NULL UNIQUE
                )
                """)
            self._connection.execute("""
                CREATE TRIGGER IF NOT EXISTS prefix_identities_refuse_update
                BEFORE UPDATE ON event_prefix_identities
                BEGIN SELECT RAISE(ABORT, 'append-prefix identities do not revision'); END
                """)
            self._connection.execute("""
                CREATE TRIGGER IF NOT EXISTS prefix_identities_refuse_delete
                BEFORE DELETE ON event_prefix_identities
                BEGIN SELECT RAISE(ABORT, 'append-prefix identities are not removed'); END
                """)
            self._connection.execute("""
                CREATE TRIGGER IF NOT EXISTS events_require_prefix_writer
                BEFORE INSERT ON events
                WHEN seed_prefix_writer() != 1
                BEGIN SELECT RAISE(ABORT, 'writer cannot maintain append-prefix identities'); END
                """)
            if not existed:
                previous = _EMPTY_PREFIX_IDENTITY
                position = 0
                for row in self._connection.execute(
                    f"SELECT events.rowid AS event_rowid, {_EVENT_ROW_COLUMNS} "
                    f"FROM {_EVENT_ROW_SOURCE} ORDER BY events.rowid"
                ):
                    position += 1
                    event = self._row_to_event(row)
                    previous = _next_prefix_identity(previous, event)
                    self._connection.execute(
                        "INSERT INTO event_prefix_identities "
                        "(position, event_rowid, event_identity, identity) "
                        "VALUES (?, ?, ?, ?)",
                        (position, row["event_rowid"], event.identity, previous),
                    )
            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise

        event_stats = self._connection.execute(
            "SELECT COUNT(*) AS n, COALESCE(MAX(rowid), 0) AS tail FROM events"
        ).fetchone()
        prefix_stats = self._connection.execute(
            "SELECT COUNT(*) AS n, COALESCE(MAX(position), 0) AS position, "
            "COALESCE(MAX(event_rowid), 0) AS tail FROM event_prefix_identities"
        ).fetchone()
        if (
            event_stats["n"] != prefix_stats["n"]
            or prefix_stats["position"] != prefix_stats["n"]
            or event_stats["tail"] != prefix_stats["tail"]
        ):
            raise LedgerIntegrityError(
                "append-prefix identity mechanics are incomplete"
            )
        self._validate_prefix_identities()

    def _prefix_data_version(self) -> int:
        return int(self._connection.execute("PRAGMA data_version").fetchone()[0])

    def _validate_prefix_identities_after_external_commit(self) -> None:
        data_version = self._prefix_data_version()
        if getattr(self, "_validated_prefix_data_version", None) != data_version:
            self._validate_prefix_identities()

    def _validate_prefix_identities(self) -> None:
        while True:
            data_version = self._prefix_data_version()
            event_rows = iter(
                self._connection.execute(
                    f"SELECT events.rowid AS event_rowid, {_EVENT_ROW_COLUMNS} "
                    f"FROM {_EVENT_ROW_SOURCE} ORDER BY events.rowid"
                )
            )
            prefix_rows = iter(
                self._connection.execute(
                    "SELECT position, event_rowid, event_identity, identity "
                    "FROM event_prefix_identities ORDER BY position"
                )
            )
            previous = _EMPTY_PREFIX_IDENTITY
            position = 0
            while True:
                event_row = next(event_rows, None)
                prefix_row = next(prefix_rows, None)
                if event_row is None or prefix_row is None:
                    if event_row is not None or prefix_row is not None:
                        raise LedgerIntegrityError(
                            "append-prefix identity mechanics are incomplete"
                        )
                    break
                position += 1
                event = self._row_to_event(event_row)
                previous = _next_prefix_identity(previous, event)
                if (
                    prefix_row["position"] != position
                    or prefix_row["event_rowid"] != event_row["event_rowid"]
                    or prefix_row["event_identity"] != event.identity
                    or prefix_row["identity"] != previous
                ):
                    raise LedgerIntegrityError(
                        "append-prefix identity mechanics are incomplete"
                    )
            current_data_version = self._prefix_data_version()
            if current_data_version == data_version:
                self._validated_prefix_data_version = current_data_version
                return

    def _insert_prefix_identity(
        self, event: Event, event_rowid: int
    ) -> None:
        position_row = self._connection.execute(
            "SELECT COALESCE(MAX(position), 0) + 1 AS position, "
            "(SELECT identity FROM event_prefix_identities "
            " ORDER BY position DESC LIMIT 1) AS previous "
            "FROM event_prefix_identities"
        ).fetchone()
        previous = position_row["previous"] or _EMPTY_PREFIX_IDENTITY
        identity = _next_prefix_identity(previous, event)
        self._connection.execute(
            "INSERT INTO event_prefix_identities "
            "(position, event_rowid, event_identity, identity) VALUES (?, ?, ?, ?)",
            (position_row["position"], event_rowid, event.identity, identity),
        )

    def _insert_without_commit(self, event: Event) -> int:
        exact_material_identity = self._store_exact_material_without_commit(
            event.exact_material
        )
        cursor = self._connection.execute(
            """
            INSERT INTO events (
                identity, kind, timestamp, material, exact_material_identity,
                locality_identity, occurrence_material_identity
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            self._row_values(event, exact_material_identity),
        )
        return int(cursor.lastrowid)

    def _exact_material_reference(self, event_identity: str) -> str | None:
        """Read one durable storage reference without making it Event material."""

        row = self._connection.execute(
            "SELECT exact_material_identity FROM events WHERE identity = ?",
            (event_identity,),
        ).fetchone()
        return None if row is None else row["exact_material_identity"]

    def _read_exact_material_reference(
        self, material_identity: str
    ) -> bytes | None:
        """Read storage bytes addressed by a private exact-material reference."""

        row = self._connection.execute(
            "SELECT exact_material FROM event_exact_materials "
            "WHERE material_identity = ?",
            (material_identity,),
        ).fetchone()
        return None if row is None else row["exact_material"]

    def _store_exact_material_without_commit(
        self, exact_material: bytes | None
    ) -> str | None:
        if exact_material is None:
            return None
        material_identity = _exact_material_identity(exact_material)
        stored = self._connection.execute(
            "SELECT exact_material FROM event_exact_materials "
            "WHERE material_identity = ?",
            (material_identity,),
        ).fetchone()
        if stored is None:
            self._connection.execute(
                "INSERT INTO event_exact_materials "
                "(material_identity, exact_material) VALUES (?, ?)",
                (material_identity, exact_material),
            )
        elif type(stored["exact_material"]) is not bytes or (
            stored["exact_material"] != exact_material
        ):
            raise LedgerIntegrityError(
                "one exact-material identity cannot address different bytes"
            )
        return material_identity

    @staticmethod
    def _row_values(event: Event, exact_material_identity: str | None) -> tuple:
        row = {
            "identity": event.identity,
            "kind": event.kind,
            "timestamp": event.timestamp.isoformat(),
            "material": json.dumps(event.material),
            "exact_material": event.exact_material,
            "exact_material_identity": exact_material_identity,
            "locality_identity": event.locality_identity,
        }
        # Storage form does not participate in the occurrence material identity.
        material_identity = _occurrence_material_identity(row)
        row["material"] = _stored_material(row["material"])
        return tuple(row[f] for f in _STORED_OCCURRENCE_FIELDS) + (
            material_identity,
        )

    def _validate_sqlite_batch(self, events: list[Event]) -> None:
        seen: set[str] = set()
        for event in events:
            if event.identity in seen:
                raise ValueError(f"event identity already exists: {event.identity}")
            seen.add(event.identity)

    def _row_to_event(self, row: sqlite3.Row) -> Event:
        if (
            row["exact_material_identity"] is not None
            and row["exact_material"] is None
        ):
            raise InvalidStoredMaterial(
                "an event exact-material reference is not available"
            )
        try:
            material = _decode_screened_event_material(_serialized_material(row["material"]))
        except json.JSONDecodeError as exc:
            # Read as text and not as an occurrence. The same condition as
            # a material that will not decompress: the stored row no longer
            # carries what it was identified from, so it is refused as an
            # integrity failure rather than as the parser's error. This was
            # already reachable before compression, for a text material damaged
            # in place.
            raise InvalidStoredMaterial(
                f"a stored material is not an exact occurrence: {exc}"
            ) from exc
        return Event(
            identity=row["identity"],
            kind=row["kind"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            material=material,
            exact_material=row["exact_material"],
            locality_identity=row["locality_identity"],
        )

    def _new_event_identity(self) -> str:
        event_identity = f"evt_{self._next_event_number:06d}"
        self._next_event_number += 1
        reserve_identity_prefix("evt", self._next_event_number - 1)
        return event_identity

    def _advance_event_counter(self, event_identity: str) -> None:
        number = _numeric_number(event_identity, "evt")
        if number is None:
            return
        self._next_event_number = max(self._next_event_number, number + 1)
        reserve_identity_prefix("evt", number)

    def _max_event_identity_number(self) -> int:
        row = self._connection.execute("""
            SELECT MAX(CAST(SUBSTR(identity, 5) AS INTEGER)) AS max_number
            FROM events
            WHERE identity LIKE 'evt_%'
              AND SUBSTR(identity, 5) GLOB '[0-9]*'
              AND SUBSTR(identity, 5) NOT GLOB '*[^0-9]*'
            """).fetchone()
        return int(row["max_number"] or 0)

    def _reservable_identity_numbers(self, event: Event) -> dict[str, int]:
        """Every reservable identity this one occurrence carries.

        A reservable identity is a known prefix, an underscore, and digits.
        The digits therefore run to the end of the string and begin just after
        its **last** underscore, so one split locates the only candidate split
        place rather than testing the value against each prefix in turn.

        `#2483` measured why that matters on a Compare material: testing every
        walked value against every prefix cost 53.6 million calls over 3,984
        appended occurrences, and the materials grow with what the layer
        compares.
        """
        found: dict[str, int] = {}
        reservable = self._RESERVABLE_PREFIXES
        values = _walk_values(event.material)
        if event.locality_identity is not None:
            values = chain(values, (event.locality_identity,))
        for value in values:
            if not isinstance(value, str):
                continue
            divided = value.rsplit("_", 1)
            if len(divided) != 2:
                continue
            prefix, digits = divided
            if prefix not in reservable or not digits.isdigit():
                continue
            number = int(digits)
            if number > found.get(prefix, 0):
                found[prefix] = number
        return found

    def _persist_reservations(self, reservations: dict[str, int]) -> None:
        for prefix, max_number in reservations.items():
            self._connection.execute(
                "INSERT INTO identity_reservations (prefix, max_number) VALUES (?, ?) "
                "ON CONFLICT(prefix) DO UPDATE SET max_number = MAX(max_number, ?)",
                (prefix, max_number, max_number),
            )
            reserve_identity_prefix(prefix, max_number)

def _walk_values(value: Any) -> Iterable[Any]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _walk_values(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_values(nested)
    else:
        yield value


def _numeric_number(value: str, prefix: str) -> int | None:
    marker = f"{prefix}_"
    if not value.startswith(marker):
        return None
    number = value[len(marker) :]
    if not number.isdigit():
        return None
    return int(number)
