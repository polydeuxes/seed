"""Measure exact bytes across a complete bounded ingress population.

This is the first acquisition boundary that does not receive its measured
subjects from a caller.  The subjects are the literal byte values carried by
the exact raw material linked from every ingress occurrence in the declared
sessions through one captured ledger boundary.

One byte value receives one count Assertion.  Recurrence is a separate
Assertion and exists only where the total count exceeds one.  Byte equality
establishes no character, word, language, position, adjacency, grammar,
meaning, relation, or significance.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.production_evidence import (
    PRODUCTION_EVIDENCE_KIND,
    _record_production_evidence,
    production_commitment,
)


RAW_MATERIAL_CAPTURED_KIND = "operator.ingress.raw_material_captured"
INGRESS_OCCURRED_KIND = "operator.ingress.ingress_occurred"
BYTE_MEASUREMENT_RECORDED_KIND = "operator.measurement.byte_counts_recorded"
BYTE_MEASUREMENT_RESULT_KIND = "exact byte-count Measurement results"
BYTE_MEASUREMENT_CONVENTION = "exact_captured_byte_count_measurement_v1"
RESPONSIBILITY_UNRECOVERED = "unrecovered"
BYTE_OCCURRENCE_PRESERVATION = (
    "byte Measurement results durably recorded after production"
)
BYTE_RESULT_COORDINATES = frozenset(
    {
        "dimensions",
        "producing_act",
        "producer",
        "measurement_rule",
        "source_session_ids",
        "completeness_boundary",
        "assertions",
    }
)
BYTE_MEASUREMENT_RULE = (
    "each individual byte of exact captured ingress material; equal only when "
    "the byte values are identical"
)
MEASUREMENT_AUTHORITY = (
    "literal byte-count Measurement Evidence only; establishes no character, "
    "word, language, position, adjacency, grammar, meaning, relation, or "
    "Standing movement"
)
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve the fidelity of this measured Assertion's Standing to its "
    "carried coordinates"
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
class MeasuredBytePopulation:
    workspace_id: str
    source_session_ids: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary
    source_material: tuple[dict[str, str], ...]
    counts: tuple[MeasuredByteCount, ...]


@dataclass(frozen=True)
class RecordedByteAssertion:
    assertion_id: str
    recorded_occurrence_id: str
    byte_hex: str | None
    result: str

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


def _identity(
    *, result: str, subject: dict[str, Any], scope: dict[str, Any], content: Any
) -> str:
    carried = {"result": result, "subject": subject, "scope": scope, "content": content}
    return "byte-measurement:" + hashlib.sha256(
        _canonical(carried).encode("utf-8")
    ).hexdigest()


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
        or raw.session_id != ingress.session_id
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
    source_session_ids: Iterable[str],
) -> MeasuredBytePopulation:
    """Count every exact byte in every declared session through one boundary."""

    sessions = tuple(dict.fromkeys(source_session_ids))
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
) -> MeasuredBytePopulation:
    missing = [
        session
        for session in sessions
        if not ledger.has_session(workspace_id, session, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source sessions are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    source_material: list[dict[str, str]] = []
    carrying = [0] * 256
    totals = [0] * 256
    examined = 0
    for session in sessions:
        raw_through_boundary = {
            event.id: event
            for event in ledger.iter_session_kind(
                workspace_id,
                session,
                RAW_MATERIAL_CAPTURED_KIND,
                through=boundary,
            )
        }
        for ingress in ledger.iter_session_kind(
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
    return MeasuredBytePopulation(
        workspace_id=workspace_id,
        source_session_ids=sessions,
        completeness_boundary=boundary,
        source_material=tuple(source_material),
        counts=counts,
    )


def _assertions(measured: MeasuredBytePopulation) -> list[dict[str, Any]]:
    scope = {
        "workspace_id": measured.workspace_id,
        "source_session_ids": list(measured.source_session_ids),
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
                "authority_warrant": MEASUREMENT_AUTHORITY,
            },
            "subject_kind": "assertion",
            "responsibility_owner": "this recorded assertion",
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
            "unknowns": ["what the exact source bytes represent remains Unknown"],
            "forbidden_inferences": [
                "an exact source-material set establishes no character, word, "
                "language, position, adjacency, grammar, meaning, or relation"
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
                "authority_warrant": MEASUREMENT_AUTHORITY,
            },
            "subject_kind": "assertion",
            "responsibility_owner": "this recorded assertion",
            "result": result,
            "assertion_subject": subject,
            "assertion_scope": scope,
            "support_basis": {
                "event_ids": [],
                "local_assertion_ids": local_support_ids,
            },
            "unknowns": ["what this byte participates in or represents remains Unknown"],
            "forbidden_inferences": [
                "an exact byte count or recurrence establishes no character, word, "
                "language, position, adjacency, grammar, meaning, or relation"
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
    source_session_ids: Iterable[str],
    recording_session_id: str,
):
    """Record one bounded Measurement occurrence with distinct byte results."""

    if not isinstance(recording_session_id, str) or not recording_session_id:
        raise ByteMeasurementError(
            "byte Measurement recording requires an exact session"
        )
    measured = measure_byte_counts(
        ledger, workspace_id=workspace_id, source_session_ids=source_session_ids
    )
    result_payload = {
        "dimensions": {
                "identity": "byte-count-measurement-occurrence",
                "content": "distinct exact byte count and recurrence Assertions produced",
                "standing": "measured",
                "source_provenance": "complete declared ingress read through one boundary",
                "authority_warrant": MEASUREMENT_AUTHORITY,
        },
        "producing_act": "declared Measurement",
        "producer": RESPONSIBILITY_UNRECOVERED,
        "measurement_rule": BYTE_MEASUREMENT_RULE,
        "source_session_ids": list(measured.source_session_ids),
        "completeness_boundary": {
            "commitment": measured.completeness_boundary.commitment
        },
        "assertions": _assertions(measured),
    }
    evidence = _record_production_evidence(
        ledger,
        workspace_id=workspace_id,
        session_id=recording_session_id,
        convention=BYTE_MEASUREMENT_CONVENTION,
        producing_act="declared Measurement",
        produced_result_kind=BYTE_MEASUREMENT_RESULT_KIND,
        result_identity="byte-count-measurement-occurrence",
        produced_content=result_payload,
        producer=RESPONSIBILITY_UNRECOVERED,
        responsibility=RESPONSIBILITY_UNRECOVERED,
    )
    return ledger.append(
        BYTE_MEASUREMENT_RECORDED_KIND,
        workspace_id,
        {
            **result_payload,
            "production_evidence_id": evidence.id,
            "occurrence_preservation": BYTE_OCCURRENCE_PRESERVATION,
        },
        session_id=recording_session_id,
    )


def assertions_of_recorded_byte_measurement(
    ledger: EventLedger, event_id: str
) -> tuple[RecordedByteAssertion, ...] | None:
    """Recover the exact byte results after replaying their bounded source read."""

    event = ledger.get(event_id)
    if event is None:
        return None
    if event.kind != BYTE_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(f"{event_id} is not a byte Measurement occurrence")
    if ledger.integrity_of(event_id) == CORRUPTED:
        raise ByteMeasurementError("a corrupted occurrence cannot expose byte results")
    payload = event.payload
    if set(payload) != BYTE_RESULT_COORDINATES | {
        "production_evidence_id",
        "occurrence_preservation",
    }:
        raise ByteMeasurementError(
            f"{event_id} does not carry the exact byte result and recording surfaces"
        )
    if (
        payload.get("occurrence_preservation") != BYTE_OCCURRENCE_PRESERVATION
        or payload.get("producing_act") != "declared Measurement"
        or payload.get("producer") != RESPONSIBILITY_UNRECOVERED
        or payload.get("dimensions")
        != {
            "identity": "byte-count-measurement-occurrence",
            "content": (
                "distinct exact byte count and recurrence Assertions produced"
            ),
            "standing": "measured",
            "source_provenance": (
                "complete declared ingress read through one boundary"
            ),
            "authority_warrant": MEASUREMENT_AUTHORITY,
        }
    ):
        raise ByteMeasurementError(
            f"{event_id} does not preserve its exact Measurement and "
            "recording-occurrence testimony"
        )
    evidence_id = payload.get("production_evidence_id")
    evidence = ledger.get(evidence_id) if isinstance(evidence_id, str) else None
    if (
        evidence is None
        or evidence.kind != PRODUCTION_EVIDENCE_KIND
        or evidence.workspace_id != event.workspace_id
        or ledger.integrity_of(evidence.id) == CORRUPTED
        or evidence.payload.get("production_convention")
        != BYTE_MEASUREMENT_CONVENTION
        or evidence.payload.get("produced_result_kind")
        != BYTE_MEASUREMENT_RESULT_KIND
        or evidence.payload.get("production_coordinates")
        != sorted(BYTE_RESULT_COORDINATES)
        or evidence.payload.get("dimensions", {}).get("producer")
        != RESPONSIBILITY_UNRECOVERED
        or evidence.payload.get("dimensions", {}).get("responsibility")
        != RESPONSIBILITY_UNRECOVERED
    ):
        raise ByteMeasurementError(
            f"{event_id} names no exact byte Measurement production Evidence"
        )
    produced = {name: payload[name] for name in BYTE_RESULT_COORDINATES}
    if evidence.payload.get("production_commitment") != production_commitment(
        BYTE_MEASUREMENT_CONVENTION, produced
    ):
        raise ByteMeasurementError(
            f"{event_id} does not carry the exact produced byte Measurement result"
        )
    boundary_value = payload.get("completeness_boundary")
    sessions_value = payload.get("source_session_ids")
    if (
        payload.get("measurement_rule") != BYTE_MEASUREMENT_RULE
        or not isinstance(boundary_value, dict)
        or set(boundary_value) != {"commitment"}
        or not isinstance(boundary_value["commitment"], str)
        or not isinstance(sessions_value, list)
        or not sessions_value
        or any(not isinstance(item, str) or not item for item in sessions_value)
        or len(set(sessions_value)) != len(sessions_value)
    ):
        raise ByteMeasurementError(
            f"{event_id} does not carry the exact byte Measurement boundary"
        )
    boundary = EventLedgerBoundary(boundary_value["commitment"])
    measured = _measure_byte_counts_through(
        ledger,
        workspace_id=event.workspace_id,
        sessions=tuple(sessions_value),
        boundary=boundary,
    )
    expected = _assertions(measured)
    if payload.get("assertions") != expected:
        raise ByteMeasurementError(
            f"{event_id} does not carry the results of its complete bounded source read"
        )
    recovered = []
    for assertion in expected:
        recovered.append(
            RecordedByteAssertion(
                assertion_id=assertion["dimensions"]["identity"],
                recorded_occurrence_id=event.id,
                byte_hex=assertion["assertion_subject"].get("byte_hex"),
                result=assertion["result"],
            )
        )
    return tuple(recovered)
