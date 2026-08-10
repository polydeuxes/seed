"""Append-only in-memory event ledger."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
import sqlite3
from typing import Any, Iterable, Iterator

from seed_runtime.execution_status import (
    ExecutionStatusConsumer,
    ProgressCadence,
    emit_progress_if_due,
    emit_status,
)
from seed_runtime.ids import new_id, reserve_id_prefix
from seed_runtime.models import Actor, Event, _decode_screened_event_payload


# What a ledger can say about a stored occurrence's integrity.
#
# `06.Standing:16` names append-only records permissively, among projected
# material and context views. Nothing in active law requires append-only, and
# nothing here claims history cannot change: a `DROP TRIGGER` followed by a
# rewrite of both row and digest defeats this. The warranted claim is narrower
# — mutation is refused by default, and undetected corruption becomes
# detectable.
VERIFIED = "verified"
UNVERIFIABLE = "unverifiable"
CORRUPTED = "corrupted"


_PREFIX_DOMAIN = b"seed.event-ledger.append-prefix.v1\0"
_EMPTY_PREFIX_COMMITMENT = hashlib.sha256(_PREFIX_DOMAIN + b"empty").hexdigest()


@dataclass(frozen=True)
class EventLedgerBoundary:
    """An opaque commitment to one exact append prefix.

    Callers may retain and return the value, but only an EventLedger interprets
    it. Equal ordered prefixes produce equal boundaries; a boundary does not
    expose an append position.
    """

    commitment: str


class InvalidLedgerBoundary(ValueError):
    """A boundary does not denote a prefix of the ledger being read."""


class LedgerIntegrityError(Exception):
    """A durable store cannot supply the integrity its occurrences require."""

# Every persisted field, because an occurrence moved between sessions is as
# altered as one whose payload changed, and `session_id` is now the boundary
# keeping bounded exchanges apart.
_DIGESTED_FIELDS = (
    "id", "kind", "workspace_id", "actor", "timestamp", "payload",
    "session_id", "causation_id", "correlation_id",
)


def _content_digest(row: dict) -> str:
    """A stable digest over the whole recorded row."""
    return hashlib.sha256(
        json.dumps({f: row.get(f) for f in _DIGESTED_FIELDS},
                   sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _canonical_occurrence_bytes(event: Event) -> bytes:
    """Canonical bytes for the occurrence itself, excluding ledger mechanics."""
    represented = {
        "id": event.id,
        "kind": event.kind,
        "workspace_id": event.workspace_id,
        "actor": event.actor,
        "timestamp": event.timestamp.isoformat(),
        "payload": event.payload,
        "session_id": event.session_id,
        "causation_id": event.causation_id,
        "correlation_id": event.correlation_id,
    }
    return json.dumps(
        represented, sort_keys=True, separators=(",", ":")
    ).encode()


def _next_prefix_commitment(previous: str, event: Event) -> str:
    occurrence = _canonical_occurrence_bytes(event)
    return hashlib.sha256(
        _PREFIX_DOMAIN
        + bytes.fromhex(previous)
        + len(occurrence).to_bytes(8, "big")
        + occurrence
    ).hexdigest()


class EventLedger:
    """Process-local append-only ledger for recording Seed runtime events."""

    __seed_arch__ = {
        "owner": "event_history",
        "layer": "events",
        "summary": "Owns append-only runtime event history read by projection and owner services.",
        "edges": [
            {"to": "StateProjector", "label": "feeds projection"},
        ],
    }

    def __init__(self) -> None:
        self._events: list[Event] = []
        self._by_id: dict[str, Event] = {}
        self._by_workspace: dict[str, list[Event]] = defaultdict(list)
        self._by_id_position: dict[str, int] = {}
        self._latest_prefix_commitment = _EMPTY_PREFIX_COMMITMENT
        self._boundary_positions: dict[str, int] = {
            _EMPTY_PREFIX_COMMITMENT: 0
        }

    def append(
        self,
        kind: str,
        workspace_id: str = "default",
        payload: dict[str, Any] | None = None,
        *,
        actor: Actor = "system",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Event:
        """Record an event and return the stored event."""
        event = Event(
            id=new_id("evt"),
            kind=kind,
            workspace_id=workspace_id,
            actor=actor,
            payload=payload or {},
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        self._store(event)
        return event

    def append_many(
        self,
        events: Iterable[Event],
        *,
        status_consumer: ExecutionStatusConsumer | None = None,
    ) -> list[Event]:
        """Record pre-built events in order and return the stored events.

        Event granularity remains unchanged: each supplied Event is stored as its
        own ledger event. Implementations may batch the underlying persistence
        transaction for storage efficiency.
        """
        stored_events = [event.model_copy(deep=True) for event in events]
        self._validate_batch(stored_events)
        total = len(stored_events)
        emit_status(
            status_consumer,
            "event_persistence",
            "Writing events",
            current=0,
            total=total,
        )
        cadence = ProgressCadence()
        for index, event in enumerate(stored_events, start=1):
            self._store(event)
            emit_progress_if_due(
                status_consumer,
                cadence,
                "event_persistence",
                "Writing events",
                current=index,
                total=total,
            )
        return stored_events

    def get(self, event_id: str) -> Event | None:
        """Return an event by id, if it exists."""
        return self._by_id.get(event_id)

    def capture_boundary(self) -> EventLedgerBoundary:
        """Capture an opaque commitment to the current append prefix."""
        return EventLedgerBoundary(self._latest_prefix_commitment)

    def _position_through(self, through: EventLedgerBoundary | None) -> int:
        if through is None:
            return len(self._events)
        position = self._boundary_positions.get(through.commitment)
        if position is None:
            raise InvalidLedgerBoundary(
                "boundary does not denote an append prefix of this ledger"
            )
        return position

    def list(
        self,
        workspace_id: str | None = None,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        """Return events in append order, optionally scoped to a workspace."""
        position = self._position_through(through)
        if workspace_id is None:
            return list(self._events[:position])
        bounded = []
        for event in self._by_workspace.get(workspace_id, []):
            if self._by_id_position[event.id] > position:
                break
            bounded.append(event)
        return bounded

    def list_events(
        self,
        workspace_id: str | None = None,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        """Backward-compatible alias for :meth:`list`."""
        return self.list(workspace_id, through=through)

    def integrity_of(self, event_id: str) -> str:
        """What this ledger can say about a stored occurrence's integrity.

        An in-memory ledger holds objects, not stored bytes, so there is no
        recorded representation to have diverged from. It reports
        `UNVERIFIABLE` rather than `VERIFIED`: nothing was protected, and
        saying otherwise would manufacture the guarantee.
        """
        return UNVERIFIABLE

    def list_session(
        self,
        workspace_id: str,
        session_id: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        """Return one session's events in append order.

        A session projection reads a session. Reading the whole workspace and
        discarding the rest costs the whole workspace, which for a durable
        ledger grows without bound while the answer does not.
        """
        return [
            event
            for event in self.list(workspace_id, through=through)
            if event.session_id == session_id
        ]

    def has_session(
        self,
        workspace_id: str,
        session_id: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> bool:
        """Whether at least one occurrence establishes this session boundary."""
        position = self._position_through(through)
        for event in self._by_workspace.get(workspace_id, ()):
            if self._by_id_position[event.id] > position:
                break
            if event.session_id == session_id:
                return True
        return False

    def iter_session_kind(
        self,
        workspace_id: str,
        session_id: str,
        kind: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> Iterator[Event]:
        """Yield one kind from one session without collecting a result list."""
        position = self._position_through(through)
        for event in self._by_workspace.get(workspace_id, ()):
            if self._by_id_position[event.id] > position:
                break
            if event.session_id == session_id and event.kind == kind:
                yield event

    def extend(self, events: Iterable[Event]) -> None:
        """Append externally constructed events while preserving order and IDs."""
        self.append_many(events)

    def _store(self, event: Event) -> None:
        if event.id in self._by_id:
            raise ValueError(f"event id already exists: {event.id}")
        # Canonicalization may refuse a payload. Derive before making the
        # occurrence visible anywhere so a failed append cannot leave event
        # history ahead of its append-prefix mechanics.
        commitment = _next_prefix_commitment(self._latest_prefix_commitment, event)
        position = len(self._events) + 1
        self._events.append(event)
        self._by_id[event.id] = event
        self._by_workspace[event.workspace_id].append(event)
        self._latest_prefix_commitment = commitment
        self._boundary_positions[commitment] = position
        self._by_id_position[event.id] = position

    def _validate_batch(self, events: list[Event]) -> None:
        seen: set[str] = set()
        for event in events:
            if event.id in self._by_id or event.id in seen:
                raise ValueError(f"event id already exists: {event.id}")
            seen.add(event.id)


# Compatibility for older tests and callers; EventLedger itself remains in-memory.
class SQLiteEventLedger(EventLedger):
    """SQLite-backed ledger with the same public API as EventLedger."""

    # Every minted-id prefix this ledger stores and a later process may mint
    # again. A prefix missing here is a collision waiting for the second
    # process: `new_id` counts from 1 per process, so the second console
    # lifetime against a durable ledger reissues the first one's identifiers.
    #
    # The four operator-console prefixes were absent until `#2413` connected
    # the console to a durable ledger, at which point the second `seed --db`
    # invocation aborted on `duplicate presentation reference`. Nothing was
    # wrong with them before: no console had ever written durable history.
    _PERSISTED_ID_PREFIXES = (
        "obs",
        "obs_local_host",
        "evd",
        "evd_obs",
        "fact",
        "fact_obs",
        "need",
        "operator_presentation",
        "operator_ingress_attempt",
        "operator_material",
        "session",
    )

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self._connection = sqlite3.connect(database_path)
        self._connection.row_factory = sqlite3.Row
        # A durable prefix chain has to be extended by every writer. Older
        # writers do not register this connection-local function, so the
        # durable trigger installed below refuses their inserts instead of
        # admitting an occurrence outside the chain.
        self._connection.create_function(
            "seed_prefix_writer", 0, lambda: 1, deterministic=True
        )
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                workspace_id TEXT NOT NULL,
                actor TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                payload TEXT NOT NULL,
                session_id TEXT,
                causation_id TEXT,
                correlation_id TEXT,
                content_hash TEXT NOT NULL
            )
            """)
        # Minted identifier counters, kept durably instead of reconstructed.
        #
        # `#2414` measured the reconstruction: every payload of every event
        # deserialized and walked on every open, to recover the highest issued
        # suffix per prefix. That is a whole-history read for an answer of a few
        # integers, and it grows without bound — 36.9s at 100,000 events,
        # extrapolating to about 356s at a million.
        #
        # This table is not an occurrence. It records no claim and supports no
        # standing; it is ledger mechanics, and the `events` mutation refusal
        # deliberately does not cover it.
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS id_reservations (
                prefix TEXT PRIMARY KEY,
                max_suffix INTEGER NOT NULL
            )
            """)
        # A store either was born with integrity or is not this store. There is
        # no ALTER path: creating a new database by running a compatibility
        # migration over the shape we no longer support is backwards, and an
        # empty pre-digest schema is still a schema Seed does not keep.
        columns = {
            row["name"]: row
            for row in self._connection.execute("PRAGMA table_info(events)")
        }
        if "content_hash" not in columns:
            raise LedgerIntegrityError(
                f"{database_path} has an events table without content_hash. "
                "Seed does not migrate pre-integrity ledgers; a store either "
                "carries digests from birth or is not supported"
            )
        if not columns["content_hash"]["notnull"]:
            # The column being present is not the invariant. A store created
            # by the withdrawn ALTER path has a nullable digest column, and
            # could hold nothing but valid digests today while still admitting
            # an undigested occurrence tomorrow. Checking current rows would
            # accept it and leave the claim false.
            raise LedgerIntegrityError(
                f"{database_path} declares content_hash nullable, so it was not "
                "born with the current integrity schema. Holding no undigested "
                "occurrence now is not the same as being unable to hold one"
            )
        # Refuse the mutation the API never performs, so that code outside the
        # API cannot perform it either. A `DROP TRIGGER` removes this; that is
        # what keeps the claim at "refused by default" rather than "immutable".
        self._connection.execute("""
            CREATE TRIGGER IF NOT EXISTS events_refuse_update
            BEFORE UPDATE ON events
            BEGIN SELECT RAISE(ABORT, 'recorded occurrences do not change'); END
            """)
        self._connection.execute("""
            CREATE TRIGGER IF NOT EXISTS events_refuse_delete
            BEFORE DELETE ON events
            BEGIN SELECT RAISE(ABORT, 'recorded occurrences are not removed'); END
            """)
        # The boundary sessions are actually selected by. Without it the
        # session read returns one session after scanning every row, which is
        # bounded in what it answers and not in what it reads.
        self._connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_workspace_session
            ON events(workspace_id, session_id)
            """)
        self._connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_workspace_session_kind
            ON events(workspace_id, session_id, kind)
            """)
        self._ensure_prefix_commitments()
        self._connection.commit()
        max_event_suffix = self._max_event_id_suffix()
        self._next_event_number = max_event_suffix + 1
        reserve_id_prefix("evt", max_event_suffix)
        for prefix, max_suffix in self._connection.execute(
            "SELECT prefix, max_suffix FROM id_reservations"
        ):
            reserve_id_prefix(prefix, max_suffix)

    def append(
        self,
        kind: str,
        workspace_id: str = "default",
        payload: dict[str, Any] | None = None,
        *,
        actor: Actor = "system",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Event:
        event = Event(
            id=self._new_event_id(),
            kind=kind,
            workspace_id=workspace_id,
            actor=actor,
            payload=payload or {},
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        self._insert(event)
        return event

    def append_many(
        self,
        events: Iterable[Event],
        *,
        status_consumer: ExecutionStatusConsumer | None = None,
    ) -> list[Event]:
        """Persist pre-built events in order using a single SQLite transaction."""
        stored_events = [event.model_copy(deep=True) for event in events]
        self._validate_sqlite_batch(stored_events)
        total = len(stored_events)
        emit_status(
            status_consumer,
            "event_persistence",
            "Writing events",
            current=0,
            total=total,
        )
        cadence = ProgressCadence()
        # One transaction, occurrences and their identifier reservations
        # together. `#2428` stated that a reservation is written in the same
        # transaction as the occurrence that carried the identifier, and
        # `append` does that; this path did not. A failure between the two
        # commits left durable occurrences carrying identifiers whose counters
        # were stale on reopen, which is the collision `#2428` exists to
        # prevent. `evt` is partly shielded because open recovers the maximum
        # event id separately; the payload and session prefixes are not.
        with self._connection:
            for index, event in enumerate(stored_events, start=1):
                event_rowid = self._insert_without_commit(event)
                self._insert_prefix_commitment(event, event_rowid)
                self._persist_reservations(self._observed_suffixes(event))
                emit_progress_if_due(
                    status_consumer,
                    cadence,
                    "event_persistence",
                    "Writing events",
                    current=index,
                    total=total,
                )
        for event in stored_events:
            self._advance_event_counter(event.id)
        return stored_events

    def get(self, event_id: str) -> Event | None:
        row = self._connection.execute(
            "SELECT * FROM events WHERE id = ?",
            (event_id,),
        ).fetchone()
        return self._row_to_event(row) if row is not None else None

    def capture_boundary(self) -> EventLedgerBoundary:
        """Capture an opaque commitment to the current durable append prefix."""
        row = self._connection.execute(
            "SELECT commitment FROM event_prefix_commitments "
            "ORDER BY position DESC LIMIT 1"
        ).fetchone()
        return EventLedgerBoundary(
            row["commitment"] if row is not None else _EMPTY_PREFIX_COMMITMENT
        )

    def _rowid_through(self, through: EventLedgerBoundary | None) -> int | None:
        if through is None:
            return None
        if through.commitment == _EMPTY_PREFIX_COMMITMENT:
            return 0
        row = self._connection.execute(
            "SELECT event_rowid FROM event_prefix_commitments "
            "WHERE commitment = ?",
            (through.commitment,),
        ).fetchone()
        if row is None:
            raise InvalidLedgerBoundary(
                "boundary does not denote an append prefix of this ledger"
            )
        return int(row["event_rowid"])

    def list(
        self,
        workspace_id: str | None = None,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        rowid = self._rowid_through(through)
        boundary_sql = "" if rowid is None else " WHERE rowid <= ?"
        boundary_args: tuple[Any, ...] = () if rowid is None else (rowid,)
        if workspace_id is None:
            rows = self._connection.execute(
                f"SELECT * FROM events{boundary_sql} ORDER BY rowid",
                boundary_args,
            ).fetchall()
        else:
            qualifier = "WHERE" if rowid is None else "AND"
            rows = self._connection.execute(
                f"SELECT * FROM events{boundary_sql} {qualifier} "
                "workspace_id = ? ORDER BY rowid",
                (*boundary_args, workspace_id),
            ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def list_events(
        self,
        workspace_id: str | None = None,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        return self.list(workspace_id, through=through)

    def list_session(
        self,
        workspace_id: str,
        session_id: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> list[Event]:
        rowid = self._rowid_through(through)
        boundary = "" if rowid is None else "AND rowid <= ? "
        args: tuple[Any, ...] = (
            (workspace_id, session_id)
            if rowid is None
            else (workspace_id, session_id, rowid)
        )
        rows = self._connection.execute(
            "SELECT * FROM events WHERE workspace_id = ? AND session_id = ? "
            + boundary
            + "ORDER BY rowid",
            args,
        ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def has_session(
        self,
        workspace_id: str,
        session_id: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> bool:
        rowid = self._rowid_through(through)
        boundary = "" if rowid is None else "AND rowid <= ? "
        args: tuple[Any, ...] = (
            (workspace_id, session_id)
            if rowid is None
            else (workspace_id, session_id, rowid)
        )
        row = self._connection.execute(
            "SELECT 1 FROM events WHERE workspace_id = ? AND session_id = ? "
            + boundary
            + "LIMIT 1",
            args,
        ).fetchone()
        return row is not None

    def iter_session_kind(
        self,
        workspace_id: str,
        session_id: str,
        kind: str,
        *,
        through: EventLedgerBoundary | None = None,
    ) -> Iterator[Event]:
        rowid = self._rowid_through(through)
        boundary = "" if rowid is None else "AND rowid <= ? "
        args: tuple[Any, ...] = (
            (workspace_id, session_id, kind)
            if rowid is None
            else (workspace_id, session_id, kind, rowid)
        )
        rows = self._connection.execute(
            "SELECT * FROM events WHERE workspace_id = ? AND session_id = ? "
            "AND kind = ? " + boundary + "ORDER BY rowid",
            args,
        )
        for row in rows:
            yield self._row_to_event(row)

    def integrity_of(self, event_id: str) -> str:
        """Recompute the stored row's digest and compare it with the recorded one.

        Verification belongs where the guarantee is claimed. `#2416` made
        ordinary reads cheap, and putting a digest on `get` or `list_session`
        would charge every reader for an obligation only a consuming act
        carries.
        """
        row = self._connection.execute(
            "SELECT * FROM events WHERE id = ?", (event_id,)
        ).fetchone()
        if row is None:
            # Nothing is stored, so there is nothing to have diverged. This is
            # the absence of an occurrence, not a durable one lacking integrity.
            return UNVERIFIABLE
        # A durable occurrence always carries a digest: the store is refused
        # at open otherwise. So this answers VERIFIED or CORRUPTED, never
        # UNVERIFIABLE. Leaving a supported unverifiable path here would let it
        # be cited later as evidence that durable references need no integrity.
        return (
            VERIFIED
            if _content_digest(dict(row)) == row["content_hash"]
            else CORRUPTED
        )

    def extend(self, events: Iterable[Event]) -> None:
        self.append_many(events)

    def close(self) -> None:
        self._connection.close()

    def _insert(self, event: Event) -> None:
        with self._connection:
            event_rowid = self._insert_without_commit(event)
            self._insert_prefix_commitment(event, event_rowid)
            self._persist_reservations(self._observed_suffixes(event))
        self._advance_event_counter(event.id)

    def _ensure_prefix_commitments(self) -> None:
        """Create or validate the ledger-owned append-prefix mechanics.

        An existing store without the table receives one atomic derivation from
        the append sequence it currently represents. This does not alter or
        strengthen any occurrence's integrity result.
        """
        existed = self._connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' "
            "AND name = 'event_prefix_commitments'"
        ).fetchone() is not None
        self._connection.execute("BEGIN IMMEDIATE")
        try:
            self._connection.execute("""
                CREATE TABLE IF NOT EXISTS event_prefix_commitments (
                    position INTEGER PRIMARY KEY,
                    event_rowid INTEGER NOT NULL UNIQUE,
                    event_id TEXT NOT NULL UNIQUE,
                    commitment TEXT NOT NULL UNIQUE
                )
                """)
            self._connection.execute("""
                CREATE TRIGGER IF NOT EXISTS prefix_commitments_refuse_update
                BEFORE UPDATE ON event_prefix_commitments
                BEGIN SELECT RAISE(ABORT, 'append-prefix commitments do not change'); END
                """)
            self._connection.execute("""
                CREATE TRIGGER IF NOT EXISTS prefix_commitments_refuse_delete
                BEFORE DELETE ON event_prefix_commitments
                BEGIN SELECT RAISE(ABORT, 'append-prefix commitments are not removed'); END
                """)
            self._connection.execute("""
                CREATE TRIGGER IF NOT EXISTS events_require_prefix_writer
                BEFORE INSERT ON events
                WHEN seed_prefix_writer() != 1
                BEGIN SELECT RAISE(ABORT, 'writer cannot maintain append-prefix commitments'); END
                """)
            if not existed:
                previous = _EMPTY_PREFIX_COMMITMENT
                position = 0
                for row in self._connection.execute(
                    "SELECT rowid AS event_rowid, * FROM events ORDER BY rowid"
                ):
                    position += 1
                    event = self._row_to_event(row)
                    previous = _next_prefix_commitment(previous, event)
                    self._connection.execute(
                        "INSERT INTO event_prefix_commitments "
                        "(position, event_rowid, event_id, commitment) "
                        "VALUES (?, ?, ?, ?)",
                        (position, row["event_rowid"], event.id, previous),
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
            "COALESCE(MAX(event_rowid), 0) AS tail FROM event_prefix_commitments"
        ).fetchone()
        if (
            event_stats["n"] != prefix_stats["n"]
            or prefix_stats["position"] != prefix_stats["n"]
            or event_stats["tail"] != prefix_stats["tail"]
        ):
            raise LedgerIntegrityError(
                "append-prefix commitment mechanics are incomplete"
            )

    def _insert_prefix_commitment(
        self, event: Event, event_rowid: int
    ) -> None:
        position_row = self._connection.execute(
            "SELECT COALESCE(MAX(position), 0) + 1 AS position, "
            "(SELECT commitment FROM event_prefix_commitments "
            " ORDER BY position DESC LIMIT 1) AS previous "
            "FROM event_prefix_commitments"
        ).fetchone()
        previous = position_row["previous"] or _EMPTY_PREFIX_COMMITMENT
        commitment = _next_prefix_commitment(previous, event)
        self._connection.execute(
            "INSERT INTO event_prefix_commitments "
            "(position, event_rowid, event_id, commitment) VALUES (?, ?, ?, ?)",
            (position_row["position"], event_rowid, event.id, commitment),
        )

    def _insert_without_commit(self, event: Event) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO events (id, kind, workspace_id, actor, timestamp, payload, session_id, causation_id, correlation_id, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            self._row_values(event),
        )
        return int(cursor.lastrowid)

    @staticmethod
    def _row_values(event: Event) -> tuple:
        row = {
            "id": event.id,
            "kind": event.kind,
            "workspace_id": event.workspace_id,
            "actor": event.actor,
            "timestamp": event.timestamp.isoformat(),
            "payload": json.dumps(event.payload),
            "session_id": event.session_id,
            "causation_id": event.causation_id,
            "correlation_id": event.correlation_id,
        }
        return tuple(row[f] for f in _DIGESTED_FIELDS) + (_content_digest(row),)

    def _validate_sqlite_batch(self, events: list[Event]) -> None:
        seen: set[str] = set()
        for event in events:
            if event.id in seen:
                raise ValueError(f"event id already exists: {event.id}")
            seen.add(event.id)

    def _row_to_event(self, row: sqlite3.Row) -> Event:
        return Event(
            id=row["id"],
            kind=row["kind"],
            workspace_id=row["workspace_id"],
            actor=row["actor"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            payload=_decode_screened_event_payload(row["payload"]),
            session_id=row["session_id"],
            causation_id=row["causation_id"],
            correlation_id=row["correlation_id"],
        )

    def _new_event_id(self) -> str:
        event_id = f"evt_{self._next_event_number:06d}"
        self._next_event_number += 1
        reserve_id_prefix("evt", self._next_event_number - 1)
        return event_id

    def _advance_event_counter(self, event_id: str) -> None:
        suffix = _numeric_suffix(event_id, "evt")
        if suffix is None:
            return
        self._next_event_number = max(self._next_event_number, suffix + 1)
        reserve_id_prefix("evt", suffix)

    def _max_event_id_suffix(self) -> int:
        row = self._connection.execute("""
            SELECT MAX(CAST(SUBSTR(id, 5) AS INTEGER)) AS max_suffix
            FROM events
            WHERE id LIKE 'evt_%'
              AND SUBSTR(id, 5) GLOB '[0-9]*'
              AND SUBSTR(id, 5) NOT GLOB '*[^0-9]*'
            """).fetchone()
        return int(row["max_suffix"] or 0)

    def _reserve_persisted_payload_ids(self) -> None:
        rows = self._connection.execute(
            "SELECT payload FROM events ORDER BY rowid"
        ).fetchall()
        for row in rows:
            try:
                payload = json.loads(row["payload"])
            except (TypeError, json.JSONDecodeError):
                continue
            self._reserve_payload_ids(payload)

    def _observed_suffixes(self, event: Event) -> dict[str, int]:
        """Every reservable identifier this one occurrence carries."""
        found: dict[str, int] = {}
        values = list(_walk_values(event.payload))
        if event.session_id is not None:
            values.append(event.session_id)
        for value in values:
            if not isinstance(value, str):
                continue
            for prefix in (*self._PERSISTED_ID_PREFIXES, "session"):
                suffix = _numeric_suffix(value, prefix)
                if suffix is not None and suffix > found.get(prefix, 0):
                    found[prefix] = suffix
        return found

    def _persist_reservations(self, observed: dict[str, int]) -> None:
        for prefix, max_suffix in observed.items():
            self._connection.execute(
                "INSERT INTO id_reservations (prefix, max_suffix) VALUES (?, ?) "
                "ON CONFLICT(prefix) DO UPDATE SET max_suffix = MAX(max_suffix, ?)",
                (prefix, max_suffix, max_suffix),
            )
            reserve_id_prefix(prefix, max_suffix)

    def _reserve_persisted_session_ids(self) -> None:
        """Session ids live in their own column, not in any payload.

        A session id appears in `dimensions.scope` only as
        `workspace:...;session:...`, which is not an identifier string, so
        walking payloads never sees one.
        """
        rows = self._connection.execute(
            "SELECT DISTINCT session_id FROM events WHERE session_id IS NOT NULL"
        ).fetchall()
        max_suffix = 0
        for row in rows:
            suffix = _numeric_suffix(row["session_id"], "session")
            if suffix is not None:
                max_suffix = max(max_suffix, suffix)
        if max_suffix:
            reserve_id_prefix("session", max_suffix)

    def _reserve_payload_ids(self, payload: Any) -> None:
        max_suffixes = {prefix: 0 for prefix in self._PERSISTED_ID_PREFIXES}
        for value in _walk_values(payload):
            if not isinstance(value, str):
                continue
            for prefix in self._PERSISTED_ID_PREFIXES:
                suffix = _numeric_suffix(value, prefix)
                if suffix is not None:
                    max_suffixes[prefix] = max(max_suffixes[prefix], suffix)
        for prefix, max_suffix in max_suffixes.items():
            if max_suffix:
                reserve_id_prefix(prefix, max_suffix)


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


def _numeric_suffix(value: str, prefix: str) -> int | None:
    marker = f"{prefix}_"
    if not value.startswith(marker):
        return None
    suffix = value[len(marker) :]
    if not suffix.isdigit():
        return None
    return int(suffix)
