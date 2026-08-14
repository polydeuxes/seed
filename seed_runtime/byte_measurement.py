"""Measure exact bytes across complete bounded ingress occurrences.

This is the first acquisition boundary that does not receive its measured
subjects from a caller.  The subjects are the literal byte values carried by
the exact raw material linked from every ingress occurrence in the declared
sessions through one captured ledger boundary.

One byte value receives one count Assertion.  Recurrence is a separate
Assertion and exists only where the total count exceeds one.  Byte equality
establishes no character, word, language, position, adjacency, grammar,
represented relation, relation, or significance.
"""

from __future__ import annotations


from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.ids import new_id
from seed_runtime.yield_evidence import (
    YIELD_EVIDENCE_KIND,
    _record_yield_evidence,
    yield_commitment,
)


RAW_MATERIAL_CAPTURED_KIND = "operator.material.raw_captured"
INGRESS_OCCURRED_KIND = "operator.material.occurred"
BYTE_MEASUREMENT_RECORDED_KIND = "operator.measurement.byte_counts_recorded"
BYTE_MEASUREMENT_RESULT_KIND = "exact byte-count Measurement results"
BYTE_MEASUREMENT_CONVENTION = "exact_captured_byte_count_measurement"
BYTE_PAIR_MEASUREMENT_RECORDED_KIND = (
    "operator.measurement.adjacent_byte_pair_counts_recorded"
)
BYTE_PAIR_MEASUREMENT_RESULT_KIND = "exact adjacent-byte-pair count Measurement results"
BYTE_PAIR_MEASUREMENT_CONVENTION = "exact_adjacent_captured_byte_pair_count_v1"
RESPONSIBILITY_UNESTABLISHED = "unestablished"
BYTE_OCCURRENCE_PRESERVATION = (
    "byte Measurement results durably recorded after yield"
)
BYTE_PAIR_OCCURRENCE_PRESERVATION = (
    "adjacent-byte-pair Measurement results durably recorded after yield"
)
BYTE_RESULT_COORDINATES = frozenset(
    {
        "dimensions",
        "yielding_act",
        "downstream_act_id",
        "act_occurrence_id",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_evidence",
        "measurement_rule",
        "source_locality_ids",
        "completeness_boundary",
        "assertions",
    }
)
BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND = (
    "operator.measurement.byte_responsible_act_evidenced"
)
BYTE_PAIR_RESULT_COORDINATES = BYTE_RESULT_COORDINATES | {
    "downstream_act_id",
    "act_occurrence_id",
    "responsibility",
    "responsible_boundary",
    "source_assertion_ref",
    "source_movement_event_id",
    "input_applicability",
    "input_applicability_event_id",
    "input_role",
}
BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND = (
    "operator.measurement.adjacent_byte_pair_responsible_act_evidenced"
)
BYTE_PAIR_APPLICABILITY_RECORDED_KIND = (
    "operator.measurement.adjacent_byte_pair_input_applicability_recorded"
)
BYTE_PAIR_APPLICABILITY_CONVENTION = "adjacent_byte_pair_input_applicability_v1"
BYTE_PAIR_APPLICABILITY_RESULT_KIND = "adjacent-byte-pair input Applicability result"
BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES = frozenset(
    {
        "dimensions",
        "yielding_act",
        "responsibility",
        "responsible_boundary",
        "assigned_by_responsibility",
        "responsibility_basis",
        "applicability_act_id",
        "applicability_act_occurrence_id",
        "downstream_act_id",
        "input_assertion_ref",
        "input_movement_event_id",
        "input_role",
        "applicability",
        "downstream_act_outcome",
    }
)
BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND = (
    "operator.measurement.adjacent_byte_pair_applicability_act_evidenced"
)
ASSERTION_LOCALITY_MOVEMENT_KIND = "operator.assertion.locality_movement_recorded"
ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND = (
    "operator.assertion.locality_movement_act_evidenced"
)
ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY = (
    "make one exact preserved Assertion available in another locality of the "
    "same workspace without changing its identity, Standing, or carried limits"
)
BYTE_MEASUREMENT_RULE = (
    "each individual byte of exact captured ingress material; equal only when "
    "the byte values are identical"
)
BYTE_PAIR_MEASUREMENT_RULE = (
    "each ordered pair of consecutive bytes within one exact captured ingress "
    "material occurrence; equal only when both byte values are identical in order"
)
MEASUREMENT_AUTHORITY = (
    "literal byte-count Measurement Evidence only; establishes no character, "
    "word, language, position, adjacency, grammar, represented relation, or relation; it "
    "establishes new bounded byte Standing and does not revise source Standing"
)
SOURCE_SET_AUTHORITY = (
    "exact bounded source-material Measurement Evidence only; establishes no "
    "character, word, language, position, adjacency, grammar, represented relation, or relation"
)
PAIR_MEASUREMENT_AUTHORITY = (
    "declared exact-source and literal ordered adjacent-byte-pair Measurement "
    "Evidence only; establishes no character, word, language, grammar, represented relation, "
    "relation beyond the exact measured adjacency and order or significance; "
    "it establishes new bounded pair Standing and does not revise source Standing"
)
BYTE_PAIR_RESULT_BOUNDARY = (
    "establish exact counts of consecutive two-byte spans within the exact "
    "bounded source material"
)
BYTE_PAIR_INPUT_ROLE = "exact bounded source material for adjacent-byte Measurement"
SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY = "this Seed"
BYTE_MEASUREMENT_RESPONSIBILITY = (
    "perform the bounded exact-byte Measurement and yield only the findings "
    "established by its exact source occurrences, rule, Scope, Authority, and limits"
)
BYTE_PAIR_MEASUREMENT_RESPONSIBILITY = (
    "yield exact adjacent-byte-pair findings from an "
    "applicable exact bounded source material without exceeding the source's "
    "Scope, provenance, occurrence identities, Authority, Unknowns, or limits"
)
BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY = (
    "determine whether one exact source-material-set Assertion may participate "
    "in one exact adjacent-byte-pair Measurement Act"
)
BYTE_PAIR_RESPONSIBILITY_BASIS = (
    "see 01.Source.E, 01.Standing.E.1, and 02.Acts"
)
BYTE_PAIR_APPLICABILITY_AUTHORITY = (
    "determine Applicability of this exact proposed input to this exact downstream "
    "Act only; the resulting Standing, not this authority, determines participation"
)
BYTE_PAIR_UNKNOWNS = (
    "what this ordered adjacent byte pair participates in or represents remains Unknown",
)
BYTE_PAIR_FORBIDDEN_INFERENCES = (
    "an exact adjacent-byte-pair count or recurrence establishes no character, "
    "word, language, grammar, represented relation, relation beyond the exact measured "
    "adjacency and order, or significance",
)
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve this measured Assertion's carried Standing coordinates"
)


class ByteMeasurementError(ValueError):
    """The exact byte Measurement could not be performed as declared."""


@dataclass(frozen=True)
class MeasuredByteCount:
    byte_hex: str
    occurrences_examined: int
    occurrences_carrying: int
    total_count: int


@dataclass(frozen=True)
class MeasuredByteInputs:
    workspace_id: str
    source_locality_ids: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary
    source_material: tuple[dict[str, str], ...]
    counts: tuple[MeasuredByteCount, ...]


@dataclass(frozen=True)
class MeasuredBytePairCount:
    pair_hex: str
    occurrences_examined: int
    occurrences_carrying: int
    total_count: int


@dataclass(frozen=True)
class MeasuredBytePairInputs:
    workspace_id: str
    source_locality_ids: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary
    source_material: tuple[dict[str, str], ...]
    source_assertion_ref: dict[str, str]
    source_movement_event_id: str | None
    input_applicability: dict[str, Any]
    downstream_act_id: str
    act_occurrence_id: str
    counts: tuple[MeasuredBytePairCount, ...]


@dataclass(frozen=True)
class RecordedByteAssertion:
    assertion_id: str
    recorded_occurrence_id: str
    byte_hex: str | None
    result: str
    _payload_json: str
    _support_assertion_refs_json: str
    locality_movement_event_id: str | None = None

    @property
    def payload(self) -> dict[str, Any]:
        """Return one detached copy of the exact reconstructed JSON representation."""

        return json.loads(self._payload_json)

    @property
    def support_assertion_refs(self) -> tuple[dict[str, str], ...]:
        """Return detached occurrence-bound local support addresses."""

        return tuple(json.loads(self._support_assertion_refs_json))

    @property
    def reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_id": self.recorded_occurrence_id,
            "assertion_id": self.assertion_id,
        }


@dataclass(frozen=True)
class RecordedBytePairAssertion:
    assertion_id: str
    recorded_occurrence_id: str
    pair_hex: str | None
    result: str
    _payload_json: str
    _support_assertion_refs_json: str

    @property
    def payload(self) -> dict[str, Any]:
        return json.loads(self._payload_json)

    @property
    def support_assertion_refs(self) -> tuple[dict[str, str], ...]:
        return tuple(json.loads(self._support_assertion_refs_json))

    @property
    def reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_id": self.recorded_occurrence_id,
            "assertion_id": self.assertion_id,
        }


def _canonical(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def _movement_commitment(payload: dict[str, Any]) -> str:
    """Commit an Assertion under the locality-movement domain."""

    digest = hashlib.sha256(b"seed.assertion-locality-movement.v1\0")
    encoded = _canonical(payload).encode("utf-8")
    digest.update(len(encoded).to_bytes(8, "big"))
    digest.update(encoded)
    return digest.hexdigest()


def _identity(
    *, result: str, subject: dict[str, Any], scope: dict[str, Any], content: Any
) -> str:
    carried = {"result": result, "subject": subject, "scope": scope, "content": content}
    return "byte-measurement:" + hashlib.sha256(
        _canonical(carried).encode("utf-8")
    ).hexdigest()


def _seed_native_measurement_assignment(
    measured: MeasuredByteInputs | MeasuredBytePairInputs,
) -> dict[str, Any]:
    """Expose why this exact preserved-material Measurement belongs here."""

    return {
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "workspace_id": measured.workspace_id,
        "source_occurrence_refs": [dict(item) for item in measured.source_material],
        "completeness_boundary": measured.completeness_boundary.commitment,
        "determination": (
            "exact ingress and raw-material occurrences were read through the "
            "captured boundary in this workspace"
        ),
    }


def _pair_input_applicability(
    source: RecordedByteAssertion,
    *,
    downstream_act_id: str,
    applicability_act_id: str,
    applicability_act_occurrence_id: str,
    act_workspace_id: str,
    measurement_locality_id: str,
) -> dict[str, Any]:
    """Determine this source Assertion's use by this exact pair Measurement."""

    payload = source.payload
    scope = payload["assertion_scope"]
    content = {
        "input_assertion_ref": source.reference,
        "input_movement_event_id": source.locality_movement_event_id,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "downstream_act_id": downstream_act_id,
        "downstream_act": "declared adjacent-byte-pair Measurement",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "applicability_act_id": applicability_act_id,
        "applicability_act_occurrence_id": applicability_act_occurrence_id,
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
    }
    if act_workspace_id != scope["workspace_id"]:
        standing = "inapplicable"
        basis = "exact Act workspace differs from the input's bounded workspace"
        applicability_scope = {
            "act_workspace_id": act_workspace_id,
            "measurement_locality_id": measurement_locality_id,
        }
        source_provenance: Any = "not input across the workspace boundary"
        input_standing: Any = {"carried": False, "reason": basis}
        input_authority: Any = {"carried": False, "reason": basis}
        input_unknowns: Any = {"carried": False, "reason": basis}
        input_limits: Any = {"carried": False, "reason": basis}
        negative_authority = {
            "carried": False,
            "treatment": "source limits did not cross the workspace boundary",
        }
    elif payload["dimensions"]["standing"] != "measured":
        standing = "conflicting"
        basis = "the input does not carry the measured Standing required by this Act"
        applicability_scope = scope
        source_provenance = payload["dimensions"]["source_provenance"]
        input_standing = payload["dimensions"]["standing"]
        input_authority = payload["dimensions"]["authority"]
        input_unknowns = payload["unknowns"]
        input_limits = payload["forbidden_inferences"]
        negative_authority = {
            "carried": True,
            "value": input_limits,
            "treatment": "preserved as limits on this exact use",
        }
    elif payload["dimensions"]["authority"] != SOURCE_SET_AUTHORITY:
        standing = "Unknown"
        basis = "the input carries no recognized Authority for this exact source-material use"
        applicability_scope = scope
        source_provenance = payload["dimensions"]["source_provenance"]
        input_standing = payload["dimensions"]["standing"]
        input_authority = payload["dimensions"]["authority"]
        input_unknowns = payload["unknowns"]
        input_limits = payload["forbidden_inferences"]
        negative_authority = {
            "carried": True,
            "value": input_limits,
            "treatment": "preserved as limits on this exact use",
        }
    else:
        standing = "applicable"
        basis = "exact bounded source material matches this Act and result boundary"
        applicability_scope = scope
        source_provenance = payload["dimensions"]["source_provenance"]
        input_standing = payload["dimensions"]["standing"]
        input_authority = payload["dimensions"]["authority"]
        input_unknowns = payload["unknowns"]
        input_limits = payload["forbidden_inferences"]
        negative_authority = {
            "carried": True,
            "value": input_limits,
            "treatment": "preserved as limits on this exact use",
        }
    identity = "byte-pair-applicability:" + hashlib.sha256(
        _canonical(
            {
                "content": content,
                "scope": applicability_scope,
                "act_context": {
                    "workspace_id": act_workspace_id,
                    "measurement_locality_id": measurement_locality_id,
                },
                "standing": standing,
            }
        ).encode("utf-8")
    ).hexdigest()
    return {
        "dimensions": {
            "identity": identity,
            "content": content,
            "standing": standing,
            "source_provenance": source_provenance,
            "authority": BYTE_PAIR_APPLICABILITY_AUTHORITY,
        },
        "result": "input_applicability",
        "input_assertion_ref": source.reference,
        "input_movement_event_id": source.locality_movement_event_id,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "downstream_act_id": downstream_act_id,
        "downstream_act_occurrence_id": None,
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "responsibility_basis": BYTE_PAIR_RESPONSIBILITY_BASIS,
        "applicability_act_id": applicability_act_id,
        "applicability_act_occurrence_id": applicability_act_occurrence_id,
        "downstream_act": "declared adjacent-byte-pair Measurement",
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "act_context": {
            "workspace_id": act_workspace_id,
            "measurement_locality_id": measurement_locality_id,
        },
        "scope_locality": applicability_scope,
        "input_standing": input_standing,
        "input_authority": input_authority,
        "input_unknowns": input_unknowns,
        "input_limits": input_limits,
        "conflicts": [basis] if standing == "conflicting" else [],
        "determination_basis": basis,
        "coordinate_treatment": {
            "support_relation_standing": {
                "carried": False,
                "treatment": "not established by Applicability",
            },
            "known_loss": {"carried": False, "treatment": "not represented by input"},
            "currentness": {
                "carried": False,
                "treatment": "not required for this historical bounded source material",
            },
            "negative_authority": negative_authority,
        },
        "unknowns": [
            "what any byte or adjacent byte pair represents remains Unknown",
            *([basis] if standing == "Unknown" else []),
        ],
        "forbidden_inferences": [
            "Applicability to this Measurement is not downstream applicability, "
            "admission, represented relation, or authority for another use"
        ],
    }


def _raw_bytes(
    ledger: EventLedger,
    ingress,
    *,
    workspace_id: str,
    raw_through_boundary: dict[str, Any],
) -> tuple[str, bytes]:
    raw_id = ingress.payload.get("raw_material_event_id")
    if not isinstance(raw_id, str) or not raw_id:
        raise ByteMeasurementError(f"{ingress.id} names no exact raw material")
    raw = raw_through_boundary.get(raw_id)
    if (
        raw is None
        or raw.kind != RAW_MATERIAL_CAPTURED_KIND
        or raw.workspace_id != workspace_id
        or raw.locality_id != ingress.locality_id
        or ledger.integrity_of(raw_id) == CORRUPTED
    ):
        raise ByteMeasurementError(
            f"{raw_id} is not intact raw material for {ingress.id} in its boundary"
        )
    represented = raw.payload.get("exact_bytes_hex")
    if not isinstance(represented, str):
        raise ByteMeasurementError(f"{raw_id} carries no exact byte representation")
    try:
        exact = bytes.fromhex(represented)
    except ValueError as exc:
        raise ByteMeasurementError(f"{raw_id} carries malformed exact bytes") from exc
    if exact.hex() != represented or raw.payload.get("byte_count") != len(exact):
        raise ByteMeasurementError(f"{raw_id} carries incoherent exact bytes")
    return raw_id, exact


def measure_byte_counts(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_locality_ids: Iterable[str],
) -> MeasuredByteInputs:
    """Count every exact byte in every declared session through one boundary."""

    sessions = tuple(dict.fromkeys(source_locality_ids))
    if not sessions or any(not isinstance(item, str) or not item for item in sessions):
        raise ByteMeasurementError(
            "byte Measurement requires exact declared source sessions"
        )
    boundary = ledger.capture_boundary()
    return _measure_byte_counts_through(
        ledger,
        workspace_id=workspace_id,
        sessions=sessions,
        boundary=boundary,
    )


def _measure_byte_counts_through(
    ledger: EventLedger,
    *,
    workspace_id: str,
    sessions: tuple[str, ...],
    boundary: EventLedgerBoundary,
) -> MeasuredByteInputs:
    missing = [
        session
        for session in sessions
        if not ledger.has_locality(workspace_id, session, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source sessions are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    source_material: list[dict[str, str]] = []
    seen_raw_material: set[str] = set()
    carrying = [0] * 256
    totals = [0] * 256
    examined = 0
    for session in sessions:
        raw_through_boundary = {
            event.id: event
            for event in ledger.iter_locality_kind(
                workspace_id,
                session,
                RAW_MATERIAL_CAPTURED_KIND,
                through=boundary,
            )
        }
        for ingress in ledger.iter_locality_kind(
            workspace_id, session, INGRESS_OCCURRED_KIND, through=boundary
        ):
            if ledger.integrity_of(ingress.id) == CORRUPTED:
                raise ByteMeasurementError(
                    "corrupted ingress cannot participate in byte Measurement"
                )
            raw_id, exact = _raw_bytes(
                ledger,
                ingress,
                workspace_id=workspace_id,
                raw_through_boundary=raw_through_boundary,
            )
            if raw_id in seen_raw_material:
                raise ByteMeasurementError(
                    "one raw-material occurrence cannot enter a byte Measurement twice"
                )
            seen_raw_material.add(raw_id)
            source_material.append(
                {"ingress_occurrence_id": ingress.id, "raw_material_event_id": raw_id}
            )
            examined += 1
            seen = set(exact)
            for value in seen:
                carrying[value] += 1
            for value in exact:
                totals[value] += 1
    if not source_material:
        raise ByteMeasurementError(
            "declared source sessions contain no ingress through the Measurement boundary"
        )
    counts = tuple(
        MeasuredByteCount(
            byte_hex=f"{value:02x}",
            occurrences_examined=examined,
            occurrences_carrying=carrying[value],
            total_count=totals[value],
        )
        for value in range(256)
        if totals[value] > 0
    )
    return MeasuredByteInputs(
        workspace_id=workspace_id,
        source_locality_ids=sessions,
        completeness_boundary=boundary,
        source_material=tuple(source_material),
        counts=counts,
    )


def _prepare_pair_source(
    ledger: EventLedger,
    *,
    source_measurement_event_id: str,
    act_workspace_id: str,
    measurement_locality_id: str,
) -> tuple[RecordedByteAssertion, dict[str, Any], dict[str, Any], str]:
    """Reconstruct one source before its act-local Applicability determination."""

    if (
        not isinstance(act_workspace_id, str)
        or not act_workspace_id
        or not isinstance(measurement_locality_id, str)
        or not measurement_locality_id
    ):
        raise ByteMeasurementError(
            "adjacent-byte-pair Measurement requires an exact Act workspace and session"
        )
    reconstructed = assertions_of_recorded_byte_measurement(
        ledger, source_measurement_event_id
    )
    if reconstructed is None:
        raise ByteMeasurementError("adjacent-byte-pair Measurement requires a source")
    source = next(
        (item for item in reconstructed if item.result == "exact_source_material_set"),
        None,
    )
    if source is None:
        raise ByteMeasurementError(
            "adjacent-byte-pair Measurement requires an exact source-material-set Assertion"
        )
    source = _move_byte_assertion_to_locality(
        ledger,
        source=source,
        destination_workspace_id=act_workspace_id,
        destination_locality=measurement_locality_id,
    )
    payload = source.payload
    scope = payload["assertion_scope"]
    content = payload["dimensions"]["content"]
    downstream_act_id = new_id("adjacent_byte_pair_measurement_act")
    return source, scope, content, downstream_act_id


def _move_byte_assertion_to_locality(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    destination_workspace_id: str,
    destination_locality: str,
) -> RecordedByteAssertion:
    """Preserve one same-workspace Assertion movement without copying the Assertion."""

    source_event = ledger.get(source.recorded_occurrence_id)
    if source_event is None or source_event.workspace_id != destination_workspace_id:
        raise ByteMeasurementError(
            "Assertion locality movement does not authorize a workspace crossing"
        )
    source_locality = source_event.locality_id
    if source_locality == destination_locality:
        return source
    if source_locality is None:
        raise ByteMeasurementError("Assertion locality movement requires source locality")
    movement_act_id = new_id("assertion_locality_movement_act")
    movement_occurrence_id = new_id("assertion_locality_movement_occurrence")
    payload = source.payload
    assignment_evidence = {
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "workspace_id": destination_workspace_id,
        "source_assertion_ref": source.reference,
        "source_locality": source_locality,
        "destination_locality": destination_locality,
        "determination": (
            "the exact preserved Assertion moved between localities of this "
            "same workspace"
        ),
    }
    act_evidence = ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND,
        destination_workspace_id,
        {
            "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "responsibility_assignment_evidence": assignment_evidence,
            "movement_act_id": movement_act_id,
            "movement_act_occurrence_id": movement_occurrence_id,
            "source_assertion_ref": source.reference,
            "source_locality": source_locality,
            "destination_locality": destination_locality,
            "authority": (
                "evidences this exact same-workspace Assertion locality movement"
            ),
        },
        locality_id=destination_locality,
    )
    movement = ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_KIND,
        destination_workspace_id,
        {
            "movement_act_id": movement_act_id,
            "movement_act_occurrence_id": movement_occurrence_id,
            "movement_act_evidence_event_id": act_evidence.id,
            "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "responsibility_assignment_evidence": assignment_evidence,
            "source_assertion_ref": source.reference,
            "assertion_id": source.assertion_id,
            "source_locality": source_locality,
            "destination_locality": destination_locality,
            "assertion_commitment": _movement_commitment(payload),
            "surviving_coordinates": [
                "Evidence",
                "Authority",
                "Scope",
                "Unknowns",
                "limits",
                "Standing",
            ],
            "authority": (
                "same-workspace locality movement of this exact Assertion only; "
                "establishes no changed identity, Standing, or cross-workspace use"
            ),
        },
        locality_id=destination_locality,
    )
    return RecordedByteAssertion(
        assertion_id=source.assertion_id,
        recorded_occurrence_id=source.recorded_occurrence_id,
        byte_hex=source.byte_hex,
        result=source.result,
        _payload_json=_canonical(payload),
        _support_assertion_refs_json=_canonical(list(source.support_assertion_refs)),
        locality_movement_event_id=movement.id,
    )


def _validate_moved_byte_assertion(
    ledger: EventLedger, movement_event_id: str
) -> RecordedByteAssertion | None:
    movement = ledger.get(movement_event_id)
    if movement is None or movement.kind != ASSERTION_LOCALITY_MOVEMENT_KIND:
        return None
    if ledger.integrity_of(movement.id) == CORRUPTED:
        raise ByteMeasurementError("Assertion locality movement is corrupted")
    source_ref = movement.payload.get("source_assertion_ref")
    if not isinstance(source_ref, dict):
        raise ByteMeasurementError("Assertion movement carries no exact source")
    source_results = assertions_of_recorded_byte_measurement(
        ledger, source_ref.get("recorded_occurrence_id")
    )
    source = next(
        (
            item
            for item in source_results or ()
            if item.assertion_id == source_ref.get("assertion_id")
        ),
        None,
    )
    if source is None:
        raise ByteMeasurementError("Assertion movement source cannot be reconstructed")
    source_event = ledger.get(source.recorded_occurrence_id)
    if source_event is None:
        raise ByteMeasurementError("Assertion movement source occurrence is unavailable")
    act_evidence = ledger.get(movement.payload.get("movement_act_evidence_event_id"))
    expected_evidence = {
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": {
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "workspace_id": movement.workspace_id,
            "source_assertion_ref": source.reference,
            "source_locality": source_event.locality_id,
            "destination_locality": movement.locality_id,
            "determination": (
                "the exact preserved Assertion moved between localities of this "
                "same workspace"
            ),
        },
        "movement_act_id": movement.payload.get("movement_act_id"),
        "movement_act_occurrence_id": movement.payload.get(
            "movement_act_occurrence_id"
        ),
        "source_assertion_ref": source.reference,
        "source_locality": source_event.locality_id,
        "destination_locality": movement.locality_id,
        "authority": (
            "evidences this exact same-workspace Assertion locality movement"
        ),
    }
    if (
        act_evidence is None
        or act_evidence.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND
        or ledger.integrity_of(act_evidence.id) == CORRUPTED
        or act_evidence.payload != expected_evidence
    ):
        raise ByteMeasurementError("Assertion movement Act Evidence is not exact")
    expected = {
        "movement_act_id": movement.payload.get("movement_act_id"),
        "movement_act_occurrence_id": movement.payload.get(
            "movement_act_occurrence_id"
        ),
        "movement_act_evidence_event_id": act_evidence.id,
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": expected_evidence[
            "responsibility_assignment_evidence"
        ],
        "source_assertion_ref": source.reference,
        "assertion_id": source.assertion_id,
        "source_locality": source_event.locality_id,
        "destination_locality": movement.locality_id,
        "assertion_commitment": _movement_commitment(source.payload),
        "surviving_coordinates": [
            "Evidence",
            "Authority",
            "Scope",
            "Unknowns",
            "limits",
            "Standing",
        ],
        "authority": (
            "same-workspace locality movement of this exact Assertion only; "
            "establishes no changed identity, Standing, or cross-workspace use"
        ),
    }
    if movement.payload != expected:
        raise ByteMeasurementError("Assertion locality movement is not exact")
    return RecordedByteAssertion(
        assertion_id=source.assertion_id,
        recorded_occurrence_id=source.recorded_occurrence_id,
        byte_hex=source.byte_hex,
        result=source.result,
        _payload_json=_canonical(source.payload),
        _support_assertion_refs_json=_canonical(list(source.support_assertion_refs)),
        locality_movement_event_id=movement.id,
    )


def _measure_adjacent_byte_pair_counts_through(
    ledger: EventLedger,
    *,
    workspace_id: str,
    sessions: tuple[str, ...],
    boundary: EventLedgerBoundary,
    source_assertion_ref: dict[str, str],
    source_movement_event_id: str | None,
    input_applicability: dict[str, Any],
    downstream_act_id: str,
    act_occurrence_id: str,
) -> MeasuredBytePairInputs:
    missing = [
        session
        for session in sessions
        if not ledger.has_locality(workspace_id, session, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source sessions are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    source_material: list[dict[str, str]] = []
    seen_raw_material: set[str] = set()
    totals: dict[bytes, int] = {}
    carrying: dict[bytes, int] = {}
    examined = 0
    for session in sessions:
        raw_through_boundary = {
            event.id: event
            for event in ledger.iter_locality_kind(
                workspace_id,
                session,
                RAW_MATERIAL_CAPTURED_KIND,
                through=boundary,
            )
        }
        for ingress in ledger.iter_locality_kind(
            workspace_id, session, INGRESS_OCCURRED_KIND, through=boundary
        ):
            if ledger.integrity_of(ingress.id) == CORRUPTED:
                raise ByteMeasurementError(
                    "corrupted ingress cannot participate in adjacent-byte-pair Measurement"
                )
            raw_id, exact = _raw_bytes(
                ledger,
                ingress,
                workspace_id=workspace_id,
                raw_through_boundary=raw_through_boundary,
            )
            if raw_id in seen_raw_material:
                raise ByteMeasurementError(
                    "one raw-material occurrence cannot enter a pair Measurement twice"
                )
            seen_raw_material.add(raw_id)
            source_material.append(
                {"ingress_occurrence_id": ingress.id, "raw_material_event_id": raw_id}
            )
            examined += 1
            seen: set[bytes] = set()
            for index in range(len(exact) - 1):
                pair = exact[index : index + 2]
                totals[pair] = totals.get(pair, 0) + 1
                seen.add(pair)
            for pair in seen:
                carrying[pair] = carrying.get(pair, 0) + 1
    if not source_material:
        raise ByteMeasurementError(
            "declared source sessions contain no ingress through the Measurement boundary"
        )
    counts = tuple(
        MeasuredBytePairCount(
            pair_hex=pair.hex(),
            occurrences_examined=examined,
            occurrences_carrying=carrying[pair],
            total_count=totals[pair],
        )
        for pair in sorted(totals)
    )
    return MeasuredBytePairInputs(
        workspace_id=workspace_id,
        source_locality_ids=sessions,
        completeness_boundary=boundary,
        source_material=tuple(source_material),
        source_assertion_ref=source_assertion_ref,
        source_movement_event_id=source_movement_event_id,
        input_applicability=input_applicability,
        downstream_act_id=downstream_act_id,
        act_occurrence_id=act_occurrence_id,
        counts=counts,
    )


def _assertions(measured: MeasuredByteInputs) -> list[dict[str, Any]]:
    scope = {
        "workspace_id": measured.workspace_id,
        "source_locality_ids": list(measured.source_locality_ids),
    }
    source_subject = {"measurement_rule": BYTE_MEASUREMENT_RULE}
    source_content = {
        "source_material": list(measured.source_material),
        "completeness_boundary": {
            "commitment": measured.completeness_boundary.commitment
        },
    }
    source_id = _identity(
        result="exact_source_material_set",
        subject=source_subject,
        scope=scope,
        content=source_content,
    )
    results: list[dict[str, Any]] = [
        {
            "dimensions": {
                "identity": source_id,
                "content": source_content,
                "standing": "measured",
                "source_provenance": (
                    "complete declared ingress read through one boundary"
                ),
                "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                "authority": SOURCE_SET_AUTHORITY,
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": "exact_source_material_set",
            "assertion_subject": source_subject,
            "assertion_scope": scope,
            "support_basis": {
                "event_ids": [
                    event_id
                    for item in measured.source_material
                    for event_id in (
                        item["ingress_occurrence_id"],
                        item["raw_material_event_id"],
                    )
                ],
                "local_assertion_ids": [],
            },
            "conflicts": "Unknown",
            "unknowns": ["what the exact source bytes represent remains Unknown"],
            "forbidden_inferences": [
                "an exact source-material set establishes no character, word, "
                "language, position, adjacency, grammar, represented relation, or relation"
            ],
        }
    ]

    def assertion(
        *,
        result: str,
        item: MeasuredByteCount,
        content: dict[str, Any],
        provenance: str,
        local_support_ids: list[str],
    ):
        subject = {"byte_hex": item.byte_hex, "measurement_rule": BYTE_MEASUREMENT_RULE}
        identity = _identity(result=result, subject=subject, scope=scope, content=content)
        return {
            "dimensions": {
                "identity": identity,
                "content": content,
                "standing": "measured",
                "source_provenance": provenance,
                "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                "authority": MEASUREMENT_AUTHORITY,
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": result,
            "assertion_subject": subject,
            "assertion_scope": scope,
            "support_basis": {
                "event_ids": [],
                "local_assertion_ids": local_support_ids,
            },
            "conflicts": "Unknown",
            "unknowns": ["what this byte participates in or represents remains Unknown"],
            "forbidden_inferences": [
                "an exact byte count or recurrence establishes no character, word, "
                "language, position, adjacency, grammar, represented relation, or relation"
            ],
        }

    for item in measured.counts:
        count_content = {
            "occurrences_examined": item.occurrences_examined,
            "occurrences_carrying": item.occurrences_carrying,
            "total_count": item.total_count,
        }
        count = assertion(
            result="count",
            item=item,
            content=count_content,
            provenance="the exact source-material-set Assertion carried here",
            local_support_ids=[source_id],
        )
        results.append(count)
        if item.total_count > 1:
            results.append(
                assertion(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    provenance="the exact count Assertion carried here",
                    local_support_ids=[count["dimensions"]["identity"]],
                )
            )
    return results


def record_byte_count_layer(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_locality_ids: Iterable[str],
    recording_locality_id: str,
):
    """Record one bounded Measurement occurrence with distinct byte results."""

    if not isinstance(recording_locality_id, str) or not recording_locality_id:
        raise ByteMeasurementError(
            "byte Measurement recording requires an exact session"
        )
    downstream_act_id = new_id("byte_measurement_act")
    act_occurrence_id = new_id("byte_measurement_occurrence")
    measured = measure_byte_counts(
        ledger, workspace_id=workspace_id, source_locality_ids=source_locality_ids
    )
    result_payload = {
        "dimensions": {
                "identity": "byte-count-measurement-occurrence",
                "content": (
                    "exact source-material-set, byte count, and conditional "
                    "recurrence Assertions yielded"
                ),
                "standing": "measured",
                "source_provenance": "complete declared ingress read through one boundary",
                "authority": MEASUREMENT_AUTHORITY,
        },
        "yielding_act": "declared Measurement",
        "downstream_act_id": downstream_act_id,
        "act_occurrence_id": act_occurrence_id,
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": _seed_native_measurement_assignment(
            measured
        ),
        "measurement_rule": BYTE_MEASUREMENT_RULE,
        "source_locality_ids": list(measured.source_locality_ids),
        "completeness_boundary": {
            "commitment": measured.completeness_boundary.commitment
        },
        "assertions": _assertions(measured),
    }
    responsible_act_evidence = ledger.append(
        BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
        workspace_id,
        {
            "downstream_act_id": downstream_act_id,
            "act_occurrence_id": act_occurrence_id,
            "act": "declared exact-byte Measurement",
            "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "responsibility_assignment_evidence": result_payload[
                "responsibility_assignment_evidence"
            ],
            "result_commitment": yield_commitment(
                BYTE_MEASUREMENT_CONVENTION, result_payload
            ),
            "standing": "occurred",
            "authority": (
                "Evidence concerning this exact bounded responsible Measurement "
                "occurrence only; establishes no responsibility"
            ),
        },
        locality_id=recording_locality_id,
    )
    evidence = _record_yield_evidence(
        ledger,
        workspace_id=workspace_id,
        locality_id=recording_locality_id,
        convention=BYTE_MEASUREMENT_CONVENTION,
        yielding_act="declared Measurement",
        act_occurrence_id=act_occurrence_id,
        yielded_result_kind=BYTE_MEASUREMENT_RESULT_KIND,
        result_identity="byte-count-measurement-occurrence",
        yielded_content=result_payload,
        responsibility=BYTE_MEASUREMENT_RESPONSIBILITY,
        live_boundary="byte_measurement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        BYTE_MEASUREMENT_RECORDED_KIND,
        workspace_id,
        {
            **result_payload,
            "yield_evidence_id": evidence.id,
            "responsible_act_evidence_id": responsible_act_evidence.id,
            "occurrence_preservation": BYTE_OCCURRENCE_PRESERVATION,
        },
        locality_id=recording_locality_id,
    )


def assertions_of_recorded_byte_measurement(
    ledger: EventLedger, event_id: str
) -> tuple[RecordedByteAssertion, ...] | None:
    """Reconstruct the exact byte results after replaying their bounded source read."""

    event = ledger.get(event_id)
    if event is None:
        return None
    if event.kind != BYTE_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(f"{event_id} is not a byte Measurement occurrence")
    if ledger.integrity_of(event_id) == CORRUPTED:
        raise ByteMeasurementError("a corrupted occurrence cannot expose byte results")
    payload = event.payload
    if set(payload) != BYTE_RESULT_COORDINATES | {
        "yield_evidence_id",
        "responsible_act_evidence_id",
        "occurrence_preservation",
    }:
        raise ByteMeasurementError(
            f"{event_id} does not carry the exact byte result and recording surfaces"
        )
    if (
        payload.get("occurrence_preservation") != BYTE_OCCURRENCE_PRESERVATION
        or payload.get("yielding_act") != "declared Measurement"
        or payload.get("responsibility") != BYTE_MEASUREMENT_RESPONSIBILITY
        or payload.get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or not isinstance(payload.get("downstream_act_id"), str)
        or not payload["downstream_act_id"]
        or not isinstance(payload.get("act_occurrence_id"), str)
        or not payload["act_occurrence_id"]
        or payload["downstream_act_id"] == payload["act_occurrence_id"]
        or payload.get("dimensions")
        != {
            "identity": "byte-count-measurement-occurrence",
                "content": (
                    "exact source-material-set, byte count, and conditional "
                    "recurrence Assertions yielded"
                ),
            "standing": "measured",
            "source_provenance": (
                "complete declared ingress read through one boundary"
            ),
            "authority": MEASUREMENT_AUTHORITY,
        }
    ):
        raise ByteMeasurementError(
            f"{event_id} does not preserve its exact Measurement and "
            "recording-occurrence Evidence"
        )
    evidence_id = payload.get("yield_evidence_id")
    evidence = ledger.get(evidence_id) if isinstance(evidence_id, str) else None
    if (
        evidence is None
        or evidence.kind != YIELD_EVIDENCE_KIND
        or evidence.workspace_id != event.workspace_id
        or ledger.integrity_of(evidence.id) == CORRUPTED
        or evidence.payload.get("yield_convention")
        != BYTE_MEASUREMENT_CONVENTION
        or evidence.payload.get("yielded_result_kind")
        != BYTE_MEASUREMENT_RESULT_KIND
        or evidence.payload.get("yield_coordinates")
        != sorted(BYTE_RESULT_COORDINATES)
        or evidence.payload.get("dimensions", {}).get("responsibility")
        != BYTE_MEASUREMENT_RESPONSIBILITY
        or evidence.payload.get("dimensions", {}).get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or evidence.payload.get("dimensions", {}).get("act_occurrence_id")
        != payload["act_occurrence_id"]
    ):
        raise ByteMeasurementError(
            f"{event_id} names no exact byte Measurement yield Evidence"
        )
    yielded = {name: payload[name] for name in BYTE_RESULT_COORDINATES}
    if evidence.payload.get("yield_commitment") != yield_commitment(
        BYTE_MEASUREMENT_CONVENTION, yielded
    ):
        raise ByteMeasurementError(
            f"{event_id} does not carry the exact yielded byte Measurement result"
        )
    act_evidence_id = payload.get("responsible_act_evidence_id")
    act_evidence = ledger.get(act_evidence_id) if isinstance(act_evidence_id, str) else None
    expected_act_evidence = {
        "downstream_act_id": payload["downstream_act_id"],
        "act_occurrence_id": payload["act_occurrence_id"],
        "act": "declared exact-byte Measurement",
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": payload[
            "responsibility_assignment_evidence"
        ],
        "result_commitment": yield_commitment(
            BYTE_MEASUREMENT_CONVENTION, yielded
        ),
        "standing": "occurred",
        "authority": (
            "Evidence concerning this exact bounded responsible Measurement "
            "occurrence only; establishes no responsibility"
        ),
    }
    if (
        act_evidence is None
        or act_evidence.kind != BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
        or act_evidence.workspace_id != event.workspace_id
        or act_evidence.locality_id != event.locality_id
        or ledger.integrity_of(act_evidence.id) == CORRUPTED
        or act_evidence.payload != expected_act_evidence
    ):
        raise ByteMeasurementError(
            f"{event_id} names no exact responsible byte Measurement occurrence Evidence"
        )
    boundary_value = payload.get("completeness_boundary")
    localities_value = payload.get("source_locality_ids")
    if (
        payload.get("measurement_rule") != BYTE_MEASUREMENT_RULE
        or not isinstance(boundary_value, dict)
        or set(boundary_value) != {"commitment"}
        or not isinstance(boundary_value["commitment"], str)
        or not isinstance(localities_value, list)
        or not localities_value
        or any(not isinstance(item, str) or not item for item in localities_value)
        or len(set(localities_value)) != len(localities_value)
    ):
        raise ByteMeasurementError(
            f"{event_id} does not carry the exact byte Measurement boundary"
        )
    boundary = EventLedgerBoundary(boundary_value["commitment"])
    measured = _measure_byte_counts_through(
        ledger,
        workspace_id=event.workspace_id,
        sessions=tuple(localities_value),
        boundary=boundary,
    )
    if payload.get("responsibility_assignment_evidence") != (
        _seed_native_measurement_assignment(measured)
    ):
        raise ByteMeasurementError(
            f"{event_id} does not establish its Seed-native Measurement boundary"
        )
    expected = _assertions(measured)
    if payload.get("assertions") != expected:
        raise ByteMeasurementError(
            f"{event_id} does not carry the results of its complete bounded source read"
        )
    reconstructed = []
    for assertion in expected:
        local_ids = assertion["support_basis"]["local_assertion_ids"]
        reconstructed.append(
            RecordedByteAssertion(
                assertion_id=assertion["dimensions"]["identity"],
                recorded_occurrence_id=event.id,
                byte_hex=assertion["assertion_subject"].get("byte_hex"),
                result=assertion["result"],
                _payload_json=_canonical(assertion),
                _support_assertion_refs_json=_canonical(
                    [
                        {
                            "recorded_occurrence_id": event.id,
                            "assertion_id": local_id,
                        }
                        for local_id in local_ids
                    ]
                ),
            )
        )
    return tuple(reconstructed)


def _pair_assertions(measured: MeasuredBytePairInputs) -> list[dict[str, Any]]:
    scope = {
        "workspace_id": measured.workspace_id,
        "source_locality_ids": list(measured.source_locality_ids),
    }
    results: list[dict[str, Any]] = []

    def assertion(
        *,
        result: str,
        item: MeasuredBytePairCount,
        content: dict[str, Any],
        provenance: str,
        local_support_ids: list[str],
        external_support_refs: list[dict[str, str]],
    ) -> dict[str, Any]:
        subject = {
            "pair_hex": item.pair_hex,
            "measurement_rule": BYTE_PAIR_MEASUREMENT_RULE,
        }
        identity = _identity(result=result, subject=subject, scope=scope, content=content)
        return {
            "dimensions": {
                "identity": identity,
                "content": content,
                "standing": "measured",
                "source_provenance": provenance,
                "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                "authority": PAIR_MEASUREMENT_AUTHORITY,
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": result,
            "assertion_subject": subject,
            "assertion_scope": scope,
            "support_basis": {
                "assertion_refs": external_support_refs,
                "local_assertion_ids": local_support_ids,
            },
            "conflicts": "Unknown",
            "unknowns": list(BYTE_PAIR_UNKNOWNS),
            "forbidden_inferences": list(BYTE_PAIR_FORBIDDEN_INFERENCES),
        }

    for item in measured.counts:
        count = assertion(
            result="count",
            item=item,
            content={
                "occurrences_examined": item.occurrences_examined,
                "occurrences_carrying": item.occurrences_carrying,
                "total_count": item.total_count,
            },
            provenance="the exact source-material-set Assertion referenced here",
            local_support_ids=[],
            external_support_refs=[measured.source_assertion_ref],
        )
        results.append(count)
        if item.total_count > 1:
            results.append(
                assertion(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    provenance="the exact count Assertion carried here",
                    local_support_ids=[count["dimensions"]["identity"]],
                    external_support_refs=[],
                )
            )
    return results


def _record_pair_responsible_act_evidence(
    ledger: EventLedger,
    *,
    measured: MeasuredBytePairInputs,
    recording_locality_id: str,
    yielded_content: dict[str, Any],
):
    """Preserve Evidence concerning this exact bounded responsible Act."""

    return ledger.append(
        BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND,
        measured.workspace_id,
        {
            "downstream_act_id": measured.downstream_act_id,
            "act_occurrence_id": measured.act_occurrence_id,
            "act": "declared adjacent-byte-pair Measurement",
            "responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "responsibility_assignment_evidence": _seed_native_measurement_assignment(
                measured
            ),
            "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
            "input_applicability_identity": measured.input_applicability["dimensions"][
                "identity"
            ],
            "input_assertion_ref": measured.source_assertion_ref,
            "input_role": BYTE_PAIR_INPUT_ROLE,
            "result_commitment": yield_commitment(
                BYTE_PAIR_MEASUREMENT_CONVENTION, yielded_content
            ),
            "standing": "occurred",
            "authority": (
                "Evidence concerning this exact bounded responsible Measurement "
                "occurrence only; establishes no responsibility or authority "
                "for another Act"
            ),
        },
        locality_id=recording_locality_id,
    )


def _record_pair_input_applicability(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    applicability_assertion: dict[str, Any],
    workspace_id: str,
    recording_locality_id: str,
):
    """Preserve Applicability whether or not the downstream Measurement occurs."""

    standing = applicability_assertion["dimensions"]["standing"]
    result_payload = {
        "dimensions": {
            "identity": applicability_assertion["dimensions"]["identity"],
            "content": "exact source-Assertion to downstream-Act Applicability",
            "standing": standing,
            "source_provenance": applicability_assertion["dimensions"]["source_provenance"],
            "authority": BYTE_PAIR_APPLICABILITY_AUTHORITY,
        },
        "yielding_act": "input Applicability determination",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "responsibility_basis": BYTE_PAIR_RESPONSIBILITY_BASIS,
        "applicability_act_id": applicability_assertion["applicability_act_id"],
        "applicability_act_occurrence_id": applicability_assertion[
            "applicability_act_occurrence_id"
        ],
        "downstream_act_id": applicability_assertion["downstream_act_id"],
        "input_assertion_ref": source.reference,
        "input_movement_event_id": source.locality_movement_event_id,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "applicability": applicability_assertion,
        "downstream_act_outcome": "not established by this Applicability Assertion",
    }
    applicability_act_evidence = ledger.append(
        BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND,
        workspace_id,
        {
            "applicability_act_id": applicability_assertion["applicability_act_id"],
            "applicability_act_occurrence_id": applicability_assertion[
                "applicability_act_occurrence_id"
            ],
            "act": "input Applicability determination",
            "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
            "input_assertion_ref": source.reference,
            "input_movement_event_id": source.locality_movement_event_id,
            "input_role": BYTE_PAIR_INPUT_ROLE,
            "downstream_act_id": applicability_assertion["downstream_act_id"],
            "result_commitment": yield_commitment(
                BYTE_PAIR_APPLICABILITY_CONVENTION, result_payload
            ),
            "standing": "occurred",
        },
        locality_id=recording_locality_id,
    )
    evidence = _record_yield_evidence(
        ledger,
        workspace_id=workspace_id,
        locality_id=recording_locality_id,
        convention=BYTE_PAIR_APPLICABILITY_CONVENTION,
        yielding_act="input Applicability determination",
        act_occurrence_id=applicability_assertion["applicability_act_occurrence_id"],
        yielded_result_kind=BYTE_PAIR_APPLICABILITY_RESULT_KIND,
        result_identity=applicability_assertion["dimensions"]["identity"],
        yielded_content=result_payload,
        responsibility=BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        live_boundary="byte_pair_applicability",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
        workspace_id,
        {
            **result_payload,
            "yield_evidence_id": evidence.id,
            "responsible_act_evidence_id": applicability_act_evidence.id,
        },
        locality_id=recording_locality_id,
    )


def get_recorded_pair_input_applicability(
    ledger: EventLedger, event_id: str
) -> dict[str, Any] | None:
    """Reconstruct one historical input Applicability result without redetermining it."""

    event = ledger.get(event_id)
    if event is None:
        return None
    if event.kind != BYTE_PAIR_APPLICABILITY_RECORDED_KIND:
        raise ByteMeasurementError(f"{event_id} is not pair-input Applicability")
    if ledger.integrity_of(event.id) == CORRUPTED:
        raise ByteMeasurementError("corrupted Applicability cannot be reconstructed")
    payload = event.payload
    evidence_id = payload.get("yield_evidence_id")
    evidence = ledger.get(evidence_id) if isinstance(evidence_id, str) else None
    if set(payload) != BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES | {
        "yield_evidence_id",
        "responsible_act_evidence_id",
    }:
        raise ByteMeasurementError(
            f"{event_id} does not carry the exact Applicability result surface"
        )
    yielded = {
        key: payload[key] for key in BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES
    }
    if (
        evidence is None
        or evidence.kind != YIELD_EVIDENCE_KIND
        or evidence.workspace_id != event.workspace_id
        or evidence.locality_id != event.locality_id
        or ledger.integrity_of(evidence.id) == CORRUPTED
        or evidence.payload.get("yield_convention")
        != BYTE_PAIR_APPLICABILITY_CONVENTION
        or evidence.payload.get("yielded_result_kind")
        != BYTE_PAIR_APPLICABILITY_RESULT_KIND
        or evidence.payload.get("yield_coordinates") != sorted(yielded)
        or evidence.payload.get("dimensions", {}).get("responsibility")
        != BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY
        or evidence.payload.get("dimensions", {}).get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or evidence.payload.get("dimensions", {}).get("act_occurrence_id")
        != payload["applicability_act_occurrence_id"]
        or evidence.payload.get("yield_commitment")
        != yield_commitment(BYTE_PAIR_APPLICABILITY_CONVENTION, yielded)
    ):
        raise ByteMeasurementError(
            f"{event_id} names no exact Applicability yield Evidence"
        )
    act_evidence_id = payload.get("responsible_act_evidence_id")
    act_evidence = ledger.get(act_evidence_id) if isinstance(act_evidence_id, str) else None
    expected_act_evidence = {
        "applicability_act_id": payload["applicability_act_id"],
        "applicability_act_occurrence_id": payload[
            "applicability_act_occurrence_id"
        ],
        "act": "input Applicability determination",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "input_assertion_ref": payload["input_assertion_ref"],
        "input_movement_event_id": payload["input_movement_event_id"],
        "input_role": payload["input_role"],
        "downstream_act_id": payload["downstream_act_id"],
        "result_commitment": yield_commitment(
            BYTE_PAIR_APPLICABILITY_CONVENTION, yielded
        ),
        "standing": "occurred",
    }
    if (
        act_evidence is None
        or act_evidence.kind != BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND
        or act_evidence.workspace_id != event.workspace_id
        or act_evidence.locality_id != event.locality_id
        or ledger.integrity_of(act_evidence.id) == CORRUPTED
        or act_evidence.payload != expected_act_evidence
    ):
        raise ByteMeasurementError(
            f"{event_id} names no exact Applicability determination occurrence Evidence"
        )
    applicability_assertion = payload.get("applicability")
    dimensions = applicability_assertion.get("dimensions") if isinstance(applicability_assertion, dict) else None
    standing = dimensions.get("standing") if isinstance(dimensions, dict) else None
    content = dimensions.get("content") if isinstance(dimensions, dict) else None
    act_context = applicability_assertion.get("act_context") if isinstance(applicability_assertion, dict) else None
    scope = applicability_assertion.get("scope_locality") if isinstance(applicability_assertion, dict) else None
    expected_identity = (
        "byte-pair-applicability:"
        + hashlib.sha256(
            _canonical(
                {
                    "content": content,
                    "scope": scope,
                    "act_context": act_context,
                    "standing": standing,
                }
            ).encode("utf-8")
        ).hexdigest()
        if isinstance(content, dict)
        and isinstance(scope, dict)
        and isinstance(act_context, dict)
        else None
    )
    if (
        standing not in {"applicable", "inapplicable", "conflicting", "Unknown"}
        or dimensions.get("identity") != expected_identity
        or applicability_assertion.get("result") != "input_applicability"
        or applicability_assertion.get("downstream_act_occurrence_id") is not None
        or applicability_assertion.get("responsibility")
        != BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY
        or applicability_assertion.get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or applicability_assertion.get("assigned_by_responsibility")
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or applicability_assertion.get("responsibility_basis") != BYTE_PAIR_RESPONSIBILITY_BASIS
        or applicability_assertion.get("applicability_act_id") != payload.get("applicability_act_id")
        or applicability_assertion.get("applicability_act_occurrence_id")
        != payload.get("applicability_act_occurrence_id")
        or payload.get("applicability_act_id")
        == payload.get("applicability_act_occurrence_id")
        or applicability_assertion.get("downstream_act") != "declared adjacent-byte-pair Measurement"
        or applicability_assertion.get("result_boundary") != BYTE_PAIR_RESULT_BOUNDARY
        or payload.get("dimensions", {}).get("standing") != standing
        or payload.get("downstream_act_id") != applicability_assertion.get("downstream_act_id")
        or payload.get("input_assertion_ref") != applicability_assertion.get("input_assertion_ref")
        or payload.get("input_role") != BYTE_PAIR_INPUT_ROLE
        or applicability_assertion.get("input_role") != BYTE_PAIR_INPUT_ROLE
        or payload.get("responsibility")
        != BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY
        or payload.get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or payload.get("assigned_by_responsibility")
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or payload.get("responsibility_basis") != BYTE_PAIR_RESPONSIBILITY_BASIS
        or payload.get("downstream_act_outcome")
        != "not established by this Applicability Assertion"
    ):
        raise ByteMeasurementError(f"{event_id} carries incoherent Applicability")
    return json.loads(_canonical(applicability_assertion))


def record_adjacent_byte_pair_count_layer(
    ledger: EventLedger,
    *,
    source_measurement_event_id: str,
    workspace_id: str,
    recording_locality_id: str,
):
    """Record exact adjacent-byte-pair counts without crossing capture boundaries."""

    if not isinstance(recording_locality_id, str) or not recording_locality_id:
        raise ByteMeasurementError(
            "adjacent-byte-pair Measurement recording requires an exact session"
        )
    source, scope, content, downstream_act_id = _prepare_pair_source(
        ledger,
        source_measurement_event_id=source_measurement_event_id,
        act_workspace_id=workspace_id,
        measurement_locality_id=recording_locality_id,
    )
    applicability_act_id = new_id("byte_pair_applicability_act")
    applicability_act_occurrence_id = new_id(
        "byte_pair_applicability_occurrence"
    )
    applicability = _pair_input_applicability(
        source,
        downstream_act_id=downstream_act_id,
        applicability_act_id=applicability_act_id,
        applicability_act_occurrence_id=applicability_act_occurrence_id,
        act_workspace_id=workspace_id,
        measurement_locality_id=recording_locality_id,
    )
    applicability_event = _record_pair_input_applicability(
        ledger,
        source=source,
        applicability_assertion=applicability,
        workspace_id=workspace_id,
        recording_locality_id=recording_locality_id,
    )
    if applicability["dimensions"]["standing"] != "applicable":
        return applicability_event
    act_occurrence_id = new_id("adjacent_byte_pair_measurement_occurrence")
    measured = _measure_adjacent_byte_pair_counts_through(
        ledger,
        workspace_id=scope["workspace_id"],
        sessions=tuple(scope["source_locality_ids"]),
        boundary=EventLedgerBoundary(content["completeness_boundary"]["commitment"]),
        source_assertion_ref=source.reference,
        source_movement_event_id=source.locality_movement_event_id,
        input_applicability=applicability,
        downstream_act_id=downstream_act_id,
        act_occurrence_id=act_occurrence_id,
    )
    result_payload = {
        "dimensions": {
            "identity": "adjacent-byte-pair-count-measurement-occurrence",
            "content": (
                "adjacent-byte-pair count and conditional recurrence Assertions yielded"
            ),
            "standing": "measured",
            "source_provenance": "the exact reconstructed source-material-set Assertion",
            "authority": PAIR_MEASUREMENT_AUTHORITY,
        },
        "yielding_act": "declared Measurement",
        "downstream_act_id": measured.downstream_act_id,
        "act_occurrence_id": measured.act_occurrence_id,
        "responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": _seed_native_measurement_assignment(
            measured
        ),
        "measurement_rule": BYTE_PAIR_MEASUREMENT_RULE,
        "source_assertion_ref": measured.source_assertion_ref,
        "source_movement_event_id": measured.source_movement_event_id,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "input_applicability": measured.input_applicability,
        "input_applicability_event_id": applicability_event.id,
        "source_locality_ids": list(measured.source_locality_ids),
        "completeness_boundary": {
            "commitment": measured.completeness_boundary.commitment
        },
        "assertions": _pair_assertions(measured),
    }
    responsible_act_evidence = _record_pair_responsible_act_evidence(
        ledger,
        measured=measured,
        recording_locality_id=recording_locality_id,
        yielded_content=result_payload,
    )
    evidence = _record_yield_evidence(
        ledger,
        workspace_id=measured.workspace_id,
        locality_id=recording_locality_id,
        convention=BYTE_PAIR_MEASUREMENT_CONVENTION,
        yielding_act="declared Measurement",
        act_occurrence_id=measured.act_occurrence_id,
        yielded_result_kind=BYTE_PAIR_MEASUREMENT_RESULT_KIND,
        result_identity="adjacent-byte-pair-count-measurement-occurrence",
        yielded_content=result_payload,
        responsibility=BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        live_boundary="byte_pair_measurement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        measured.workspace_id,
        {
            **result_payload,
            "yield_evidence_id": evidence.id,
            "responsible_act_evidence_id": responsible_act_evidence.id,
            "occurrence_preservation": BYTE_PAIR_OCCURRENCE_PRESERVATION,
        },
        locality_id=recording_locality_id,
    )


def _validate_recorded_pair_input_applicability(
    applicability_assertion: Any,
    *,
    source: RecordedByteAssertion,
    event,
    downstream_act_id: str,
) -> None:
    """Validate historical Applicability without determining it again."""

    source_payload = source.payload
    scope = source_payload["assertion_scope"]
    content = {
        "input_assertion_ref": source.reference,
        "input_movement_event_id": source.locality_movement_event_id,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "downstream_act_id": downstream_act_id,
        "downstream_act": "declared adjacent-byte-pair Measurement",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "applicability_act_id": applicability_assertion.get("applicability_act_id"),
        "applicability_act_occurrence_id": applicability_assertion.get(
            "applicability_act_occurrence_id"
        ),
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
    }
    act_context = {
        "workspace_id": event.workspace_id,
        "measurement_locality_id": event.locality_id,
    }
    identity = "byte-pair-applicability:" + hashlib.sha256(
        _canonical(
            {
                "content": content,
                "scope": scope,
                "act_context": act_context,
                "standing": "applicable",
            }
        ).encode("utf-8")
    ).hexdigest()
    expected = {
        "dimensions": {
            "identity": identity,
            "content": content,
            "standing": "applicable",
            "source_provenance": source_payload["dimensions"]["source_provenance"],
            "authority": BYTE_PAIR_APPLICABILITY_AUTHORITY,
        },
        "result": "input_applicability",
        "input_assertion_ref": source.reference,
        "input_movement_event_id": source.locality_movement_event_id,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "downstream_act_id": downstream_act_id,
        "downstream_act_occurrence_id": None,
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "responsibility_basis": BYTE_PAIR_RESPONSIBILITY_BASIS,
        "applicability_act_id": applicability_assertion.get("applicability_act_id"),
        "applicability_act_occurrence_id": applicability_assertion.get(
            "applicability_act_occurrence_id"
        ),
        "downstream_act": "declared adjacent-byte-pair Measurement",
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "act_context": act_context,
        "scope_locality": scope,
        "input_standing": source_payload["dimensions"]["standing"],
        "input_authority": source_payload["dimensions"]["authority"],
        "input_unknowns": source_payload["unknowns"],
        "input_limits": source_payload["forbidden_inferences"],
        "conflicts": [],
        "determination_basis": (
            "exact bounded source material matches this Act and result boundary"
        ),
        "coordinate_treatment": {
            "support_relation_standing": {
                "carried": False,
                "treatment": "not established by Applicability",
            },
            "known_loss": {"carried": False, "treatment": "not represented by input"},
            "currentness": {
                "carried": False,
                "treatment": "not required for this historical bounded source material",
            },
            "negative_authority": {
                "carried": True,
                "value": source_payload["forbidden_inferences"],
                "treatment": "preserved as limits on this exact use",
            },
        },
        "unknowns": [
            "what any byte or adjacent byte pair represents remains Unknown"
        ],
        "forbidden_inferences": [
            "Applicability to this Measurement is not downstream applicability, "
            "admission, represented relation, or authority for another use"
        ],
    }
    if applicability_assertion != expected:
        raise ByteMeasurementError(
            f"{event.id} does not carry its exact historical input Applicability"
        )


def assertions_of_recorded_adjacent_byte_pair_measurement(
    ledger: EventLedger, event_id: str
) -> tuple[RecordedBytePairAssertion, ...] | None:
    """Reconstruct the yielded pair result without performing Measurement again."""

    event = ledger.get(event_id)
    if event is None:
        return None
    if event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(
            f"{event_id} is not an adjacent-byte-pair Measurement occurrence"
        )
    if ledger.integrity_of(event_id) == CORRUPTED:
        raise ByteMeasurementError("a corrupted occurrence cannot expose pair results")
    payload = event.payload
    exact_surface = BYTE_PAIR_RESULT_COORDINATES | {
        "yield_evidence_id",
        "responsible_act_evidence_id",
        "occurrence_preservation",
    }
    if set(payload) != exact_surface:
        raise ByteMeasurementError(
            f"{event_id} does not carry the exact pair result and recording surfaces"
        )
    expected_dimensions = {
        "identity": "adjacent-byte-pair-count-measurement-occurrence",
        "content": (
            "adjacent-byte-pair count and conditional recurrence Assertions yielded"
        ),
        "standing": "measured",
        "source_provenance": "the exact reconstructed source-material-set Assertion",
        "authority": PAIR_MEASUREMENT_AUTHORITY,
    }
    if (
        payload.get("occurrence_preservation") != BYTE_PAIR_OCCURRENCE_PRESERVATION
        or payload.get("yielding_act") != "declared Measurement"
        or payload.get("responsibility") != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or not isinstance(payload.get("downstream_act_id"), str)
        or not payload["downstream_act_id"]
        or not isinstance(payload.get("act_occurrence_id"), str)
        or not payload["act_occurrence_id"]
        or payload["downstream_act_id"] == payload["act_occurrence_id"]
        or payload.get("dimensions") != expected_dimensions
        or payload.get("measurement_rule") != BYTE_PAIR_MEASUREMENT_RULE
    ):
        raise ByteMeasurementError(
            f"{event_id} does not preserve its exact pair Measurement Assertion"
        )
    evidence_id = payload.get("yield_evidence_id")
    evidence = ledger.get(evidence_id) if isinstance(evidence_id, str) else None
    if (
        evidence is None
        or evidence.kind != YIELD_EVIDENCE_KIND
        or evidence.workspace_id != event.workspace_id
        or ledger.integrity_of(evidence.id) == CORRUPTED
        or evidence.payload.get("yield_convention")
        != BYTE_PAIR_MEASUREMENT_CONVENTION
        or evidence.payload.get("yielded_result_kind")
        != BYTE_PAIR_MEASUREMENT_RESULT_KIND
        or evidence.payload.get("yield_coordinates")
        != sorted(BYTE_PAIR_RESULT_COORDINATES)
        or evidence.payload.get("dimensions", {}).get("responsibility")
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or evidence.payload.get("dimensions", {}).get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or evidence.payload.get("dimensions", {}).get("act_occurrence_id")
        != payload["act_occurrence_id"]
    ):
        raise ByteMeasurementError(
            f"{event_id} names no exact adjacent-byte-pair yield Evidence"
        )
    yielded = {name: payload[name] for name in BYTE_PAIR_RESULT_COORDINATES}
    if evidence.payload.get("yield_commitment") != yield_commitment(
        BYTE_PAIR_MEASUREMENT_CONVENTION, yielded
    ):
        raise ByteMeasurementError(
            f"{event_id} does not carry the exact yielded pair Measurement result"
        )
    act_evidence_id = payload.get("responsible_act_evidence_id")
    act_evidence = ledger.get(act_evidence_id) if isinstance(act_evidence_id, str) else None
    carried_applicability = payload.get("input_applicability")
    applicability_dimensions = (
        carried_applicability.get("dimensions")
        if isinstance(carried_applicability, dict)
        else None
    )
    applicability_identity = (
        applicability_dimensions.get("identity")
        if isinstance(applicability_dimensions, dict)
        else None
    )
    if not isinstance(applicability_identity, str) or not applicability_identity:
        raise ByteMeasurementError(f"{event_id} carries no exact input Applicability")
    expected_act_evidence = {
        "downstream_act_id": payload["downstream_act_id"],
        "act_occurrence_id": payload["act_occurrence_id"],
        "act": "declared adjacent-byte-pair Measurement",
        "responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": payload[
            "responsibility_assignment_evidence"
        ],
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "input_applicability_identity": applicability_identity,
        "input_assertion_ref": payload["source_assertion_ref"],
        "input_role": payload["input_role"],
        "result_commitment": yield_commitment(
            BYTE_PAIR_MEASUREMENT_CONVENTION, yielded
        ),
        "standing": "occurred",
        "authority": (
            "Evidence concerning this exact bounded responsible Measurement "
            "occurrence only; establishes no responsibility or authority "
            "for another Act"
        ),
    }
    if (
        act_evidence is None
        or act_evidence.kind != BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND
        or act_evidence.workspace_id != event.workspace_id
        or act_evidence.locality_id != event.locality_id
        or ledger.integrity_of(act_evidence.id) == CORRUPTED
        or act_evidence.payload != expected_act_evidence
    ):
        raise ByteMeasurementError(
            f"{event_id} names no exact responsible pair Measurement occurrence Evidence"
        )
    boundary_value = payload.get("completeness_boundary")
    localities_value = payload.get("source_locality_ids")
    if (
        not isinstance(boundary_value, dict)
        or set(boundary_value) != {"commitment"}
        or not isinstance(boundary_value["commitment"], str)
        or not isinstance(localities_value, list)
        or not localities_value
        or any(not isinstance(item, str) or not item for item in localities_value)
        or len(set(localities_value)) != len(localities_value)
    ):
        raise ByteMeasurementError(
            f"{event_id} does not carry the exact pair Measurement boundary"
        )
    source_ref = payload.get("source_assertion_ref")
    if (
        not isinstance(source_ref, dict)
        or set(source_ref) != {"recorded_occurrence_id", "assertion_id"}
        or not all(isinstance(value, str) and value for value in source_ref.values())
    ):
        raise ByteMeasurementError(f"{event_id} carries no exact source Assertion")
    movement_event_id = payload.get("source_movement_event_id")
    if movement_event_id is None:
        source_results = assertions_of_recorded_byte_measurement(
            ledger, source_ref["recorded_occurrence_id"]
        )
        source = next(
            (
                item
                for item in source_results or ()
                if item.assertion_id == source_ref["assertion_id"]
            ),
            None,
        )
    elif isinstance(movement_event_id, str) and movement_event_id:
        source = _validate_moved_byte_assertion(ledger, movement_event_id)
    else:
        source = None
    if source is not None and source.assertion_id != source_ref["assertion_id"]:
        source = None
    if source is None or event.locality_id is None:
        raise ByteMeasurementError(
            f"{event_id} does not carry its exact input source Assertion"
        )
    source_payload = source.payload
    source_scope = source_payload["assertion_scope"]
    source_content = source_payload["dimensions"]["content"]
    expected_assignment_evidence = {
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "workspace_id": source_scope["workspace_id"],
        "source_occurrence_refs": source_content["source_material"],
        "completeness_boundary": source_content["completeness_boundary"][
            "commitment"
        ],
        "determination": (
            "exact ingress and raw-material occurrences were read through the "
            "captured boundary in this workspace"
        ),
    }
    if (
        event.workspace_id != source_scope["workspace_id"]
        or localities_value != source_scope["source_locality_ids"]
        or boundary_value != source_content["completeness_boundary"]
        or payload.get("responsibility_assignment_evidence")
        != expected_assignment_evidence
    ):
        raise ByteMeasurementError(
            f"{event_id} does not carry its exact input source boundary"
        )
    _validate_recorded_pair_input_applicability(
        payload.get("input_applicability"),
        source=source,
        event=event,
        downstream_act_id=payload["downstream_act_id"],
    )
    applicability_event_id = payload.get("input_applicability_event_id")
    recorded_applicability = (
        get_recorded_pair_input_applicability(ledger, applicability_event_id)
        if isinstance(applicability_event_id, str)
        else None
    )
    if recorded_applicability != payload.get("input_applicability"):
        raise ByteMeasurementError(
            f"{event_id} does not name its exact recorded input Applicability"
        )
    expected_scope = {
        "workspace_id": event.workspace_id,
        "source_locality_ids": localities_value,
    }
    assertions = payload.get("assertions")
    if not isinstance(assertions, list):
        raise ByteMeasurementError(f"{event_id} carries no pair result Assertions")
    by_pair: dict[str, dict[str, dict[str, Any]]] = {}
    exact_keys = {
        "dimensions",
        "subject_kind",
        "responsible_boundary",
        "result",
        "assertion_subject",
        "assertion_scope",
        "support_basis",
        "conflicts",
        "unknowns",
        "forbidden_inferences",
    }
    for assertion in assertions:
        if not isinstance(assertion, dict) or set(assertion) != exact_keys:
            raise ByteMeasurementError(f"{event_id} carries a malformed pair Assertion")
        subject = assertion.get("assertion_subject")
        result = assertion.get("result")
        dimensions = assertion.get("dimensions")
        pair_hex = subject.get("pair_hex") if isinstance(subject, dict) else None
        try:
            pair_bytes = bytes.fromhex(pair_hex) if isinstance(pair_hex, str) else b""
        except ValueError as exc:
            raise ByteMeasurementError(f"{event_id} carries a malformed pair subject") from exc
        if (
            len(pair_bytes) != 2
            or subject
            != {"pair_hex": pair_hex, "measurement_rule": BYTE_PAIR_MEASUREMENT_RULE}
            or result not in {"count", "recurrence"}
            or assertion.get("assertion_scope") != expected_scope
            or assertion.get("subject_kind") != "assertion"
            or assertion.get("responsible_boundary") != "this recorded assertion"
            or assertion.get("conflicts") != "Unknown"
            or not isinstance(dimensions, dict)
            or set(dimensions)
            != {
                "identity",
                "content",
                "standing",
                "source_provenance",
                "responsibility",
                "authority",
            }
            or dimensions.get("standing") != "measured"
            or dimensions.get("responsibility") != MEASURED_ASSERTION_RESPONSIBILITY
            or dimensions.get("authority") != PAIR_MEASUREMENT_AUTHORITY
            or assertion.get("unknowns") != list(BYTE_PAIR_UNKNOWNS)
            or assertion.get("forbidden_inferences")
            != list(BYTE_PAIR_FORBIDDEN_INFERENCES)
        ):
            raise ByteMeasurementError(f"{event_id} carries an unlawful pair Assertion")
        content = dimensions.get("content")
        expected_identity = _identity(
            result=result, subject=subject, scope=expected_scope, content=content
        )
        if dimensions.get("identity") != expected_identity:
            raise ByteMeasurementError(f"{event_id} carries a false pair Assertion identity")
        group = by_pair.setdefault(pair_hex, {})
        if result in group:
            raise ByteMeasurementError(f"{event_id} duplicates one pair result")
        group[result] = assertion
    for pair_hex, group in by_pair.items():
        count = group.get("count")
        if count is None:
            raise ByteMeasurementError(f"{event_id} carries recurrence without count")
        count_content = count["dimensions"]["content"]
        if (
            not isinstance(count_content, dict)
            or set(count_content)
            != {"occurrences_examined", "occurrences_carrying", "total_count"}
            or any(type(value) is not int or value <= 0 for value in count_content.values())
            or count_content["occurrences_carrying"] > count_content["occurrences_examined"]
            or count_content["occurrences_carrying"] > count_content["total_count"]
            or count["support_basis"]
            != {"assertion_refs": [source_ref], "local_assertion_ids": []}
            or count["dimensions"]["source_provenance"]
            != "the exact source-material-set Assertion referenced here"
        ):
            raise ByteMeasurementError(f"{event_id} carries an unlawful pair count")
        recurrence = group.get("recurrence")
        if (recurrence is not None) != (count_content["total_count"] > 1):
            raise ByteMeasurementError(f"{event_id} carries the wrong recurrence boundary")
        if recurrence is not None and (
            recurrence["dimensions"]["content"] != {"recurrence_established": True}
            or recurrence["dimensions"]["source_provenance"]
            != "the exact count Assertion carried here"
            or recurrence["support_basis"]
            != {
                "assertion_refs": [],
                "local_assertion_ids": [count["dimensions"]["identity"]],
            }
        ):
            raise ByteMeasurementError(f"{event_id} carries unlawful recurrence support")
    validated_results = []
    for assertion in assertions:
        support = assertion["support_basis"]
        support_refs = list(support["assertion_refs"])
        support_refs.extend(
            {
                "recorded_occurrence_id": event.id,
                "assertion_id": local_id,
            }
            for local_id in support["local_assertion_ids"]
        )
        validated_results.append(RecordedBytePairAssertion(
            assertion_id=assertion["dimensions"]["identity"],
            recorded_occurrence_id=event.id,
            pair_hex=assertion["assertion_subject"].get("pair_hex"),
            result=assertion["result"],
            _payload_json=_canonical(assertion),
            _support_assertion_refs_json=_canonical(support_refs),
        ))
    return tuple(validated_results)


def input_applicability_of_recorded_adjacent_byte_pair_measurement(
    ledger: EventLedger, event_id: str
) -> dict[str, Any] | None:
    """Validate the independent input-to-Act Applicability Assertion."""

    reconstructed = assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event_id)
    if reconstructed is None:
        return None
    event = ledger.get(event_id)
    return json.loads(_canonical(event.payload["input_applicability"]))
