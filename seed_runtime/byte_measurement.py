"""Measure exact bytes across complete bounded ingest occurrences.

This is the first acquisition boundary that does not receive its measured
subjects from a caller.  The subjects are the literal byte values carried by
the exact raw material linked from every ingest occurrence in the declared
Localities through one recorded ledger boundary.

One byte value receives one count Assertion.  Recurrence is a separate
Assertion and exists only where the total count exceeds one.  Byte equality
establishes no character, word, position, adjacency, grammar, or represented
relation.
"""

from __future__ import annotations


from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.identities import new_identity
from seed_runtime.yield_evidence import (
    YIELD_EVIDENCE_KIND,
    _record_yield_evidence,
    read_yield_edge_requirements,
)
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    MaterialIngestError,
    ingested_material_bytes,
)


INGEST_OCCURRED_KIND = MATERIAL_INGEST_OCCURRED_KIND
BYTE_MEASUREMENT_RECORDED_KIND = "operator.measurement.byte_counts_recorded"
BYTE_MEASUREMENT_RESULT_KIND = "exact byte-count Measurement results"
BYTE_PAIR_MEASUREMENT_RECORDED_KIND = (
    "operator.measurement.adjacent_byte_pair_counts_recorded"
)
BYTE_PAIR_MEASUREMENT_RESULT_KIND = "exact adjacent-byte-pair count Measurement results"
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
        "exact_act",
        "downstream_act_identity",
        "act_occurrence_identity",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_evidence",
        "measurement_rule",
        "source_locality_identities",
        "completeness_boundary",
        "assertions",
    }
)
BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND = (
    "operator.measurement.byte_responsible_act_evidenced"
)
BYTE_PAIR_RESULT_COORDINATES = BYTE_RESULT_COORDINATES | {
    "downstream_act_identity",
    "act_occurrence_identity",
    "responsibility",
    "responsible_boundary",
    "source_assertion_reference",
    "source_movement_event_identity",
    "input_applicability",
    "input_applicability_event_identity",
    "input_role",
}
BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND = (
    "operator.measurement.adjacent_byte_pair_responsible_act_evidenced"
)
BYTE_PAIR_APPLICABILITY_RECORDED_KIND = (
    "operator.measurement.adjacent_byte_pair_input_applicability_recorded"
)
BYTE_PAIR_APPLICABILITY_RESULT_KIND = "adjacent-byte-pair input Applicability result"
BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES = frozenset(
    {
        "dimensions",
        "exact_act",
        "responsibility",
        "responsible_boundary",
        "assigned_by_responsibility",
        "applicability_act_identity",
        "applicability_act_occurrence_identity",
        "downstream_act_identity",
        "input_assertion_reference",
        "input_movement_event_identity",
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
ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND = "Assertion Locality movement result"
EVENT_KIND_RESPONSIBILITIES = {
    BYTE_MEASUREMENT_RECORDED_KIND: "02.Acts.A",
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND: "02.Acts.A",
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND: "02.Acts.A",
    BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND: "02.Acts.A",
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND: "01.Standing.E.1",
    BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND: "02.Acts.A",
    ASSERTION_LOCALITY_MOVEMENT_KIND: "06.Standing.B",
}
ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY = (
    "make one exact preserved Assertion available in another Locality without "
    "changing its identity, Standing, or carried limits"
)
BYTE_MEASUREMENT_RULE = (
    "each individual byte of exact recorded ingest material; equal only when "
    "the byte values are identical"
)
BYTE_PAIR_MEASUREMENT_RULE = (
    "each ordered pair of consecutive bytes within one exact recorded ingest "
    "material occurrence; equal only when both byte values are identical in order"
)
MEASUREMENT_EVIDENCE_SCOPE = (
    "literal byte-count Measurement Evidence only; establishes no character, "
    "word, position, adjacency, grammar, represented relation, or relation; it "
    "establishes new bounded byte Standing and does not revise source Standing"
)
SOURCE_SET_EVIDENCE_SCOPE = (
    "exact bounded source-material Measurement Evidence only; establishes no "
    "character, word, position, adjacency, grammar, represented relation, or relation"
)
PAIR_MEASUREMENT_EVIDENCE_SCOPE = (
    "declared exact-source and literal ordered adjacent-byte-pair Measurement "
    "Evidence only; establishes no character, word, grammar, represented relation, "
    "relation beyond the exact measured adjacency and order; "
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
BYTE_PAIR_APPLICABILITY_AUTHORITY = (
    "determine Applicability of this exact proposed input to this exact downstream "
    "Act only; the resulting Standing, not this authority, determines participation"
)
BYTE_PAIR_UNKNOWNS = (
    "what this ordered adjacent byte pair participates in or represents remains Unknown",
)
BYTE_PAIR_LIMITS = (
    "an exact adjacent-byte-pair count or recurrence establishes no character, "
    "word, grammar, represented relation, relation beyond the exact measured "
    "adjacency and order",
)
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve this measured Assertion's carried Standing coordinates"
)


class ByteMeasurementError(ValueError):
    """The exact byte Measurement could not be performed as declared."""


@dataclass(frozen=True)
class MeasuredByteCount:
    representation: int
    occurrences_carrying: int
    count: int


@dataclass(frozen=True)
class MeasuredByteInputs:
    source_locality_identities: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary
    source_material: tuple[dict[str, str], ...]
    counts: tuple[MeasuredByteCount, ...]


@dataclass(frozen=True)
class MeasuredBytePairCount:
    representation: tuple[int, int]
    occurrences_carrying: int
    count: int


@dataclass(frozen=True)
class MeasuredBytePairInputs:
    source_locality_identities: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary
    source_material: tuple[dict[str, str], ...]
    source_assertion_reference: dict[str, str]
    source_movement_event_identity: str | None
    input_applicability: dict[str, Any]
    downstream_act_identity: str
    act_occurrence_identity: str
    counts: tuple[MeasuredBytePairCount, ...]


@dataclass(frozen=True)
class RecordedByteAssertion:
    assertion_identity: str
    recorded_occurrence_identity: str
    representation: int | None
    result: str
    _material_json: str
    _support_assertion_refs_json: str
    locality_movement_event_identity: str | None = None

    @property
    def material(self) -> dict[str, Any]:
        """Return one detached copy of the recorded JSON representation."""

        return json.loads(self._material_json)

    @property
    def support_assertion_references(self) -> tuple[dict[str, str], ...]:
        """Return detached occurrence-bound local support addresses."""

        return tuple(json.loads(self._support_assertion_refs_json))

    @property
    def reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.assertion_identity,
        }


@dataclass(frozen=True)
class RecordedBytePairAssertion:
    assertion_identity: str
    recorded_occurrence_identity: str
    representation: tuple[int, int] | None
    result: str
    _material_json: str
    _support_assertion_refs_json: str

    @property
    def material(self) -> dict[str, Any]:
        return json.loads(self._material_json)

    @property
    def support_assertion_references(self) -> tuple[dict[str, str], ...]:
        return tuple(json.loads(self._support_assertion_refs_json))

    @property
    def reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.assertion_identity,
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


def _seed_native_measurement_assignment(
    measured: MeasuredByteInputs | MeasuredBytePairInputs,
) -> dict[str, Any]:
    """Expose why this exact preserved-material Measurement belongs here."""

    return {
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "standing": "assigned",
        "source_occurrence_references": [dict(item) for item in measured.source_material],
        "completeness_boundary": measured.completeness_boundary.identity,
        "determination": (
            "exact ingest and raw-material occurrences were read through the "
            "recorded boundary"
        ),
    }


def _pair_input_applicability(
    source: RecordedByteAssertion,
    *,
    downstream_act_identity: str,
    applicability_act_identity: str,
    applicability_act_occurrence_identity: str,
    measurement_locality_identity: str,
) -> dict[str, Any]:
    """Determine this source Assertion's use by this exact pair Measurement."""

    material = source.material
    scope = material["assertion_scope"]
    content = {
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "downstream_act_identity": downstream_act_identity,
        "downstream_act": "declared adjacent-byte-pair Measurement",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "applicability_act_identity": applicability_act_identity,
        "applicability_act_occurrence_identity": applicability_act_occurrence_identity,
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
    }
    if material["dimensions"]["standing"] != "measured":
        standing = "conflicting"
        basis = "the input does not carry the measured Standing required by this Act"
        applicability_scope = scope
        source_provenance = material["dimensions"]["source_provenance"]
        input_standing = material["dimensions"]["standing"]
        input_authority = material["dimensions"]["authority"]
        input_unknowns = material["unknowns"]
        input_limits = material["limits"]
        negative_authority = {
            "carried": True,
            "value": input_limits,
            "treatment": "preserved as limits on this exact use",
        }
    elif (
        material["dimensions"].get("authority") != "unestablished"
        or material["dimensions"].get("evidence_scope")
        != SOURCE_SET_EVIDENCE_SCOPE
    ):
        standing = "Unknown"
        basis = "the input carries no recognized Evidence scope for this exact source-material use"
        applicability_scope = scope
        source_provenance = material["dimensions"]["source_provenance"]
        input_standing = material["dimensions"]["standing"]
        input_authority = material["dimensions"]["authority"]
        input_unknowns = material["unknowns"]
        input_limits = material["limits"]
        negative_authority = {
            "carried": True,
            "value": input_limits,
            "treatment": "preserved as limits on this exact use",
        }
    else:
        standing = "applicable"
        basis = "exact bounded source material matches this Act and result boundary"
        applicability_scope = scope
        source_provenance = material["dimensions"]["source_provenance"]
        input_standing = material["dimensions"]["standing"]
        input_authority = material["dimensions"]["authority"]
        input_unknowns = material["unknowns"]
        input_limits = material["limits"]
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
                "measurement_locality": measurement_locality_identity,
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
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "downstream_act_identity": downstream_act_identity,
        "downstream_act_occurrence_identity": None,
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "applicability_act_identity": applicability_act_identity,
        "applicability_act_occurrence_identity": applicability_act_occurrence_identity,
        "downstream_act": "declared adjacent-byte-pair Measurement",
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "measurement_locality": measurement_locality_identity,
        "scope_locality": applicability_scope,
        "input_standing": input_standing,
        "input_authority": input_authority,
        "input_unknowns": input_unknowns,
        "input_limits": input_limits,
        "conflicts": [basis] if standing == "conflicting" else [],
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
        "limits": [
            "Applicability to this Measurement is not downstream applicability, "
            "admission, represented relation, or authority for another use"
        ],
    }


def _ingested_bytes(ledger: EventLedger, occurrence) -> bytes:
    if ledger.integrity_of(occurrence.identity) == CORRUPTED:
        raise ByteMeasurementError(
            f"{occurrence.identity} is not an intact Ingest occurrence"
        )
    try:
        return ingested_material_bytes(occurrence)
    except MaterialIngestError as exc:
        raise ByteMeasurementError(str(exc)) from exc


def measure_byte_counts(
    ledger: EventLedger,
    *,
    source_locality_identities: Iterable[str],
) -> MeasuredByteInputs:
    """Count every exact byte in every declared Locality through one boundary."""

    localities = tuple(dict.fromkeys(source_locality_identities))
    if not localities or any(not isinstance(item, str) or not item for item in localities):
        raise ByteMeasurementError(
            "byte Measurement requires exact declared source Localities"
        )
    boundary = ledger.append_boundary()
    return _measure_byte_counts_through(
        ledger,
        localities=localities,
        boundary=boundary,
    )


def _measure_byte_counts_through(
    ledger: EventLedger,
    *,
    localities: tuple[str, ...],
    boundary: EventLedgerBoundary,
) -> MeasuredByteInputs:
    missing = [
        locality
        for locality in localities
        if not ledger.has_locality(locality, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source Localities are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    source_material: list[dict[str, str]] = []
    seen_material: set[str] = set()
    carrying = [0] * 256
    totals = [0] * 256
    for locality in localities:
        for ingest in ledger.iter_locality_kind(
            locality, INGEST_OCCURRED_KIND, through=boundary
        ):
            if ledger.integrity_of(ingest.identity) == CORRUPTED:
                raise ByteMeasurementError(
                    "corrupted ingest cannot participate in byte Measurement"
                )
            exact = _ingested_bytes(ledger, ingest)
            if ingest.identity in seen_material:
                raise ByteMeasurementError(
                    "one Ingest occurrence cannot enter a byte Measurement twice"
                )
            seen_material.add(ingest.identity)
            source_material.append({"ingest_occurrence_identity": ingest.identity})
            seen = set(exact)
            for value in seen:
                carrying[value] += 1
            for value in exact:
                totals[value] += 1
    if not source_material:
        raise ByteMeasurementError(
            "declared source Localities contain no ingest through the Measurement boundary"
        )
    counts = tuple(
        MeasuredByteCount(
            representation=value,
            occurrences_carrying=carrying[value],
            count=totals[value],
        )
        for value in range(256)
        if totals[value] > 0
    )
    return MeasuredByteInputs(
        source_locality_identities=localities,
        completeness_boundary=boundary,
        source_material=tuple(source_material),
        counts=counts,
    )


def _prepare_pair_source(
    ledger: EventLedger,
    *,
    source_measurement_event_identity: str,
    measurement_locality_identity: str,
) -> tuple[RecordedByteAssertion, dict[str, Any], dict[str, Any], str]:
    """Read one source before its act-local Applicability determination."""

    if (
        not isinstance(measurement_locality_identity, str)
        or not measurement_locality_identity
    ):
        raise ByteMeasurementError(
            "adjacent-byte-pair Measurement requires an exact Act Locality"
        )
    read = assertions_of_recorded_byte_measurement(
        ledger, source_measurement_event_identity
    )
    if read is None:
        raise ByteMeasurementError("adjacent-byte-pair Measurement requires a source")
    source = next(
        (item for item in read if item.result == "exact_source_material_set"),
        None,
    )
    if source is None:
        raise ByteMeasurementError(
            "adjacent-byte-pair Measurement requires an exact source-material-set Assertion"
        )
    source = _move_byte_assertion_to_locality(
        ledger,
        source=source,
        destination_locality=measurement_locality_identity,
    )
    material = source.material
    scope = material["assertion_scope"]
    content = material["dimensions"]["content"]
    downstream_act_identity = new_identity("adjacent_byte_pair_measurement_act")
    return source, scope, content, downstream_act_identity


def _move_byte_assertion_to_locality(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    destination_locality: str,
) -> RecordedByteAssertion:
    """Preserve one Assertion movement without copying the Assertion."""

    source_event = ledger.get(source.recorded_occurrence_identity)
    if source_event is None:
        raise ByteMeasurementError("Assertion locality movement requires its source")
    source_locality = source_event.locality_identity
    if source_locality == destination_locality:
        return source
    if source_locality is None:
        raise ByteMeasurementError("Assertion locality movement requires source locality")
    movement_act_identity = new_identity("assertion_locality_movement_act")
    movement_occurrence_identity = new_identity("assertion_locality_movement_occurrence")
    movement_result_identity = new_identity("assertion_locality_movement_result")
    material = source.material
    assignment_evidence = {
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "standing": "assigned",
        "source_assertion_reference": source.reference,
        "source_locality": source_locality,
        "destination_locality": destination_locality,
        "determination": "the exact preserved Assertion moved between Localities",
    }
    result_material = {
        "result_identity": movement_result_identity,
        "movement_act_identity": movement_act_identity,
        "movement_act_occurrence_identity": movement_occurrence_identity,
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": assignment_evidence,
        "source_assertion_reference": source.reference,
        "assertion_identity": source.assertion_identity,
        "source_locality": source_locality,
        "destination_locality": destination_locality,
        "locality_relation": {
            "first_subject": source.reference,
            "second_subject": destination_locality,
            "relation_occurrence_identity": movement_occurrence_identity,
        },
        "surviving_coordinates": [
            "Evidence",
            "Authority",
            "Scope",
            "Unknowns",
            "limits",
            "Standing",
        ],
        "authority": "unestablished",
        "movement_scope": (
            "Locality movement of this exact Assertion only; establishes no "
            "different identity or Standing"
        ),
    }
    act_evidence = ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND,
        {
            "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "responsibility_assignment_evidence": assignment_evidence,
            "movement_act_identity": movement_act_identity,
            "movement_act_occurrence_identity": movement_occurrence_identity,
            "source_assertion_reference": source.reference,
            "source_locality": source_locality,
            "destination_locality": destination_locality,
            "locality_relation": {
                "first_subject": source.reference,
                "second_subject": destination_locality,
                "relation_occurrence_identity": movement_occurrence_identity,
            },
            "authority": "unestablished",
            "evidence_scope": "evidences this exact Assertion Locality movement",
        },
        locality_identity=destination_locality,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=destination_locality,
        exact_act="Assertion Locality movement",
        act_occurrence_identity=movement_occurrence_identity,
        result_kind=ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND,
        result_identity=movement_result_identity,
        result_content=result_material,
        responsibility=ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        live_boundary="assertion_locality_movement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        recorded_result_coordinates={key: (key,) for key in result_material},
    )
    movement = ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_KIND,
        {
            **result_material,
            "responsible_act_evidence_identity": act_evidence.identity,
            "yield_evidence_identity": yield_evidence.identity,
        },
        locality_identity=destination_locality,
    )
    return RecordedByteAssertion(
        assertion_identity=source.assertion_identity,
        recorded_occurrence_identity=source.recorded_occurrence_identity,
        representation=source.representation,
        result=source.result,
        _material_json=_canonical(material),
        _support_assertion_refs_json=_canonical(list(source.support_assertion_references)),
        locality_movement_event_identity=movement.identity,
    )


def _validate_moved_byte_assertion(
    ledger: EventLedger, movement_event_identity: str
) -> RecordedByteAssertion | None:
    movement = ledger.get(movement_event_identity)
    if movement is None or movement.kind != ASSERTION_LOCALITY_MOVEMENT_KIND:
        return None
    if ledger.integrity_of(movement.identity) == CORRUPTED:
        raise ByteMeasurementError("Assertion locality movement is corrupted")
    source_reference = movement.material.get("source_assertion_reference")
    if not isinstance(source_reference, dict):
        raise ByteMeasurementError("Assertion movement carries no exact source")
    source_results = assertions_of_recorded_byte_measurement(
        ledger, source_reference.get("recorded_occurrence_identity")
    )
    source = next(
        (
            item
            for item in source_results or ()
            if item.assertion_identity == source_reference.get("assertion_identity")
        ),
        None,
    )
    if source is None:
        raise ByteMeasurementError("Assertion movement source cannot be read")
    source_event = ledger.get(source.recorded_occurrence_identity)
    if source_event is None:
        raise ByteMeasurementError("Assertion movement source occurrence is unavailable")
    act_evidence = ledger.get(movement.material.get("responsible_act_evidence_identity"))
    expected_result = {
        "result_identity": movement.material.get("result_identity"),
        "movement_act_identity": movement.material.get("movement_act_identity"),
        "movement_act_occurrence_identity": movement.material.get(
            "movement_act_occurrence_identity"
        ),
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": {
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "standing": "assigned",
            "source_assertion_reference": source.reference,
            "source_locality": source_event.locality_identity,
            "destination_locality": movement.locality_identity,
            "determination": "the exact preserved Assertion moved between Localities",
        },
        "source_assertion_reference": source.reference,
        "assertion_identity": source.assertion_identity,
        "source_locality": source_event.locality_identity,
        "destination_locality": movement.locality_identity,
        "locality_relation": {
            "first_subject": source.reference,
            "second_subject": movement.locality_identity,
            "relation_occurrence_identity": movement.material.get(
                "movement_act_occurrence_identity"
            ),
        },
        "surviving_coordinates": [
            "Evidence",
            "Authority",
            "Scope",
            "Unknowns",
            "limits",
            "Standing",
        ],
        "authority": "unestablished",
        "movement_scope": (
            "Locality movement of this exact Assertion only; establishes no "
            "different identity or Standing"
        ),
    }
    expected_evidence = {
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": {
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "standing": "assigned",
            "source_assertion_reference": source.reference,
            "source_locality": source_event.locality_identity,
            "destination_locality": movement.locality_identity,
            "determination": "the exact preserved Assertion moved between Localities",
        },
        "movement_act_identity": movement.material.get("movement_act_identity"),
        "movement_act_occurrence_identity": movement.material.get(
            "movement_act_occurrence_identity"
        ),
        "source_assertion_reference": source.reference,
        "source_locality": source_event.locality_identity,
        "destination_locality": movement.locality_identity,
        "locality_relation": {
            "first_subject": source.reference,
            "second_subject": movement.locality_identity,
            "relation_occurrence_identity": movement.material.get(
                "movement_act_occurrence_identity"
            ),
        },
        "authority": "unestablished",
        "evidence_scope": "evidences this exact Assertion Locality movement",
    }
    if (
        act_evidence is None
        or act_evidence.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
        or act_evidence.material != expected_evidence
    ):
        raise ByteMeasurementError("Assertion movement Act Evidence is not exact")
    requirements = read_yield_edge_requirements(
        ledger,
        recorded_result_event_identity=movement.identity,
        result_evidence_event_identity=movement.material.get("yield_evidence_identity"),
        responsible_act_evidence_event_identity=movement.material.get(
            "responsible_act_evidence_identity"
        ),
        recorded_result_occurrence_coordinate="movement_act_occurrence_identity",
        responsible_act_occurrence_coordinate="movement_act_occurrence_identity",
    )
    if not all(requirements.values()):
        raise ByteMeasurementError("Assertion movement Yield Evidence is not exact")
    expected = {
        **expected_result,
        "responsible_act_evidence_identity": act_evidence.identity,
        "yield_evidence_identity": movement.material.get("yield_evidence_identity"),
    }
    if movement.material != expected:
        raise ByteMeasurementError("Assertion locality movement is not exact")
    return RecordedByteAssertion(
        assertion_identity=source.assertion_identity,
        recorded_occurrence_identity=source.recorded_occurrence_identity,
        representation=source.representation,
        result=source.result,
        _material_json=_canonical(source.material),
        _support_assertion_refs_json=_canonical(list(source.support_assertion_references)),
        locality_movement_event_identity=movement.identity,
    )


def _measure_adjacent_byte_pair_counts_through(
    ledger: EventLedger,
    *,
    localities: tuple[str, ...],
    boundary: EventLedgerBoundary,
    source_assertion_reference: dict[str, str],
    source_movement_event_identity: str | None,
    input_applicability: dict[str, Any],
    downstream_act_identity: str,
    act_occurrence_identity: str,
) -> MeasuredBytePairInputs:
    missing = [
        locality
        for locality in localities
        if not ledger.has_locality(locality, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source Localities are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    source_material: list[dict[str, str]] = []
    seen_material: set[str] = set()
    totals: dict[bytes, int] = {}
    carrying: dict[bytes, int] = {}
    for locality in localities:
        for ingest in ledger.iter_locality_kind(
            locality, INGEST_OCCURRED_KIND, through=boundary
        ):
            if ledger.integrity_of(ingest.identity) == CORRUPTED:
                raise ByteMeasurementError(
                    "corrupted ingest cannot participate in adjacent-byte-pair Measurement"
                )
            exact = _ingested_bytes(ledger, ingest)
            if ingest.identity in seen_material:
                raise ByteMeasurementError(
                    "one Ingest occurrence cannot enter a pair Measurement twice"
                )
            seen_material.add(ingest.identity)
            source_material.append({"ingest_occurrence_identity": ingest.identity})
            seen: set[bytes] = set()
            for index in range(len(exact) - 1):
                pair = exact[index : index + 2]
                totals[pair] = totals.get(pair, 0) + 1
                seen.add(pair)
            for pair in seen:
                carrying[pair] = carrying.get(pair, 0) + 1
    if not source_material:
        raise ByteMeasurementError(
            "declared source Localities contain no ingest through the Measurement boundary"
        )
    counts = tuple(
        MeasuredBytePairCount(
            representation=(pair[0], pair[1]),
            occurrences_carrying=carrying[pair],
            count=totals[pair],
        )
        for pair in sorted(totals)
    )
    return MeasuredBytePairInputs(
        source_locality_identities=localities,
        completeness_boundary=boundary,
        source_material=tuple(source_material),
        source_assertion_reference=source_assertion_reference,
        source_movement_event_identity=source_movement_event_identity,
        input_applicability=input_applicability,
        downstream_act_identity=downstream_act_identity,
        act_occurrence_identity=act_occurrence_identity,
        counts=counts,
    )


def _assertions(measured: MeasuredByteInputs) -> list[dict[str, Any]]:
    scope = {
        "source_locality_identities": list(measured.source_locality_identities),
    }
    source_subject = {"measurement_rule": BYTE_MEASUREMENT_RULE}
    source_content = {
        "source_material": list(measured.source_material),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
    }
    source_identity = _identity(
        result="exact_source_material_set",
        subject=source_subject,
        scope=scope,
        content=source_content,
    )
    results: list[dict[str, Any]] = [
        {
            "dimensions": {
                "identity": source_identity,
                "content": source_content,
                "standing": "measured",
                "source_provenance": (
                    "complete declared ingest read through one boundary"
                ),
                "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                "authority": "unestablished",
                "evidence_scope": SOURCE_SET_EVIDENCE_SCOPE,
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": "exact_source_material_set",
            "assertion_subject": source_subject,
            "assertion_scope": scope,
            "input_support": {
                "event_identities": [
                    item["ingest_occurrence_identity"]
                    for item in measured.source_material
                ],
                "local_assertion_identities": [],
            },
            "conflicts": "Unknown",
            "unknowns": ["what the exact source bytes represent remains Unknown"],
            "limits": [
                "an exact source-material set establishes no character, word, "
                "position, adjacency, grammar, represented relation, or relation"
            ],
        }
    ]

    def assertion(
        *,
        result: str,
        item: MeasuredByteCount,
        content: dict[str, Any],
        provenance: str,
        local_support_identities: list[str],
    ):
        subject = {
            "representation": item.representation,
            "measurement_rule": BYTE_MEASUREMENT_RULE,
        }
        identity = _identity(result=result, subject=subject, scope=scope, content=content)
        return {
            "dimensions": {
                "identity": identity,
                "content": content,
                "standing": "measured",
                "source_provenance": provenance,
                "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                "authority": "unestablished",
                "evidence_scope": MEASUREMENT_EVIDENCE_SCOPE,
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": result,
            "assertion_subject": subject,
            "assertion_scope": scope,
            "input_support": {
                "event_identities": [],
                "local_assertion_identities": local_support_identities,
            },
            "conflicts": "Unknown",
            "unknowns": ["what this byte participates in or represents remains Unknown"],
            "limits": [
                "an exact byte count or recurrence establishes no character, word, "
                "position, adjacency, grammar, represented relation, or relation"
            ],
        }

    for item in measured.counts:
        count_content = {
            "input_count": len(measured.source_material),
            "occurrences_carrying": item.occurrences_carrying,
            "count": item.count,
        }
        count = assertion(
            result="count",
            item=item,
            content=count_content,
            provenance="the exact source-material-set Assertion carried here",
            local_support_identities=[source_identity],
        )
        results.append(count)
        if item.count > 1:
            results.append(
                assertion(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    provenance="the exact count Assertion carried here",
                    local_support_identities=[count["dimensions"]["identity"]],
                )
            )
    return results


def record_byte_count_layer(
    ledger: EventLedger,
    *,
    source_locality_identities: Iterable[str],
    recording_locality_identity: str,
):
    """Record one bounded Measurement occurrence with distinct byte results."""

    if not isinstance(recording_locality_identity, str) or not recording_locality_identity:
        raise ByteMeasurementError(
            "byte Measurement recording requires an exact Locality"
        )
    downstream_act_identity = new_identity("byte_measurement_act")
    act_occurrence_identity = new_identity("byte_measurement_occurrence")
    measured = measure_byte_counts(
        ledger, source_locality_identities=source_locality_identities
    )
    result_material = {
        "dimensions": {
                "identity": "byte-count-measurement-occurrence",
                "content": (
                    "exact source-material-set, byte count, and conditional "
                    "recurrence Assertions"
                ),
                "standing": "measured",
                "source_provenance": "complete declared ingest read through one boundary",
                "authority": "unestablished",
                "evidence_scope": MEASUREMENT_EVIDENCE_SCOPE,
        },
        "exact_act": "declared Measurement",
        "downstream_act_identity": downstream_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": _seed_native_measurement_assignment(
            measured
        ),
        "measurement_rule": BYTE_MEASUREMENT_RULE,
        "source_locality_identities": list(measured.source_locality_identities),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
        "assertions": _assertions(measured),
    }
    responsible_act_evidence = ledger.append(
        BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": downstream_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "declared exact-byte Measurement",
            "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "responsibility_assignment_evidence": result_material[
                "responsibility_assignment_evidence"
            ],
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence for this exact bounded responsible Measurement "
                "occurrence only; establishes no responsibility"
            ),
        },
        locality_identity=recording_locality_identity,
    )
    evidence = _record_yield_evidence(
        ledger,
        locality_identity=recording_locality_identity,
        exact_act="declared Measurement",
        act_occurrence_identity=act_occurrence_identity,
        result_kind=BYTE_MEASUREMENT_RESULT_KIND,
        result_identity="byte-count-measurement-occurrence",
        result_content=result_material,
        responsibility=BYTE_MEASUREMENT_RESPONSIBILITY,
        live_boundary="byte_measurement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        BYTE_MEASUREMENT_RECORDED_KIND,
        {
            **result_material,
            "yield_evidence_identity": evidence.identity,
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "occurrence_preservation": BYTE_OCCURRENCE_PRESERVATION,
        },
        locality_identity=recording_locality_identity,
    )


def assertions_of_recorded_byte_measurement(
    ledger: EventLedger, event_identity: str
) -> tuple[RecordedByteAssertion, ...] | None:
    """Read the exact byte results after replaying their bounded source read."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != BYTE_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(f"{event_identity} is not a byte Measurement occurrence")
    if ledger.integrity_of(event_identity) == CORRUPTED:
        raise ByteMeasurementError("a corrupted occurrence cannot expose byte results")
    material = event.material
    if set(material) != BYTE_RESULT_COORDINATES | {
        "yield_evidence_identity",
        "responsible_act_evidence_identity",
        "occurrence_preservation",
    }:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact byte result and recording surfaces"
        )
    if (
        material.get("occurrence_preservation") != BYTE_OCCURRENCE_PRESERVATION
        or material.get("exact_act") != "declared Measurement"
        or material.get("responsibility") != BYTE_MEASUREMENT_RESPONSIBILITY
        or material.get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or not isinstance(material.get("downstream_act_identity"), str)
        or not material["downstream_act_identity"]
        or not isinstance(material.get("act_occurrence_identity"), str)
        or not material["act_occurrence_identity"]
        or material["downstream_act_identity"] == material["act_occurrence_identity"]
        or material.get("dimensions")
        != {
            "identity": "byte-count-measurement-occurrence",
                "content": (
                    "exact source-material-set, byte count, and conditional "
                    "recurrence Assertions"
                ),
            "standing": "measured",
            "source_provenance": (
                "complete declared ingest read through one boundary"
            ),
            "authority": "unestablished",
            "evidence_scope": MEASUREMENT_EVIDENCE_SCOPE,
        }
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not preserve its exact Measurement and "
            "recording-occurrence Evidence"
        )
    evidence_identity = material.get("yield_evidence_identity")
    evidence = ledger.get(evidence_identity) if isinstance(evidence_identity, str) else None
    if (
        evidence is None
        or evidence.kind != YIELD_EVIDENCE_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind")
        != BYTE_MEASUREMENT_RESULT_KIND
        or evidence.material.get("yield_coordinates")
        != sorted(BYTE_RESULT_COORDINATES)
        or evidence.material.get("dimensions", {}).get("responsibility")
        != BYTE_MEASUREMENT_RESPONSIBILITY
        or evidence.material.get("dimensions", {}).get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or evidence.material.get("dimensions", {}).get("act_occurrence_identity")
        != material["act_occurrence_identity"]
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact byte Measurement yield Evidence"
        )
    act_evidence_identity = material.get("responsible_act_evidence_identity")
    act_evidence = ledger.get(act_evidence_identity) if isinstance(act_evidence_identity, str) else None
    expected_act_evidence = {
        "downstream_act_identity": material["downstream_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": "declared exact-byte Measurement",
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": material[
            "responsibility_assignment_evidence"
        ],
        "authority": "unestablished",
        "evidence_scope": (
            "Evidence for this exact bounded responsible Measurement "
            "occurrence only; establishes no responsibility"
        ),
    }
    if (
        act_evidence is None
        or act_evidence.kind != BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
        or act_evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
        or act_evidence.material != expected_act_evidence
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact responsible byte Measurement occurrence Evidence"
        )
    boundary_value = material.get("completeness_boundary")
    localities_value = material.get("source_locality_identities")
    if (
        material.get("measurement_rule") != BYTE_MEASUREMENT_RULE
        or not isinstance(boundary_value, dict)
        or set(boundary_value) != {"identity"}
        or not isinstance(boundary_value["identity"], str)
        or not isinstance(localities_value, list)
        or not localities_value
        or any(not isinstance(item, str) or not item for item in localities_value)
        or len(set(localities_value)) != len(localities_value)
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact byte Measurement boundary"
        )
    boundary = EventLedgerBoundary(boundary_value["identity"])
    measured = _measure_byte_counts_through(
        ledger,
        localities=tuple(localities_value),
        boundary=boundary,
    )
    if material.get("responsibility_assignment_evidence") != (
        _seed_native_measurement_assignment(measured)
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not establish its Seed-native Measurement boundary"
        )
    expected = _assertions(measured)
    if material.get("assertions") != expected:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the results of its complete bounded source read"
        )
    read = []
    for assertion in expected:
        local_identities = assertion["input_support"]["local_assertion_identities"]
        read.append(
            RecordedByteAssertion(
                assertion_identity=assertion["dimensions"]["identity"],
                recorded_occurrence_identity=event.identity,
                representation=assertion["assertion_subject"].get("representation"),
                result=assertion["result"],
                _material_json=_canonical(assertion),
                _support_assertion_refs_json=_canonical(
                    [
                        {
                            "recorded_occurrence_identity": event.identity,
                            "assertion_identity": local_identity,
                        }
                        for local_identity in local_identities
                    ]
                ),
            )
        )
    return tuple(read)


def _pair_assertions(measured: MeasuredBytePairInputs) -> list[dict[str, Any]]:
    scope = {
        "source_locality_identities": list(measured.source_locality_identities),
    }
    results: list[dict[str, Any]] = []

    def assertion(
        *,
        result: str,
        item: MeasuredBytePairCount,
        content: dict[str, Any],
        provenance: str,
        local_support_identities: list[str],
        source_support_references: list[dict[str, str]],
    ) -> dict[str, Any]:
        subject = {
            "representation": list(item.representation),
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
                "authority": "unestablished",
                "evidence_scope": PAIR_MEASUREMENT_EVIDENCE_SCOPE,
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": result,
            "assertion_subject": subject,
            "assertion_scope": scope,
            "input_support": {
                "assertion_references": source_support_references,
                "local_assertion_identities": local_support_identities,
            },
            "conflicts": "Unknown",
            "unknowns": list(BYTE_PAIR_UNKNOWNS),
            "limits": list(BYTE_PAIR_LIMITS),
        }

    for item in measured.counts:
        count = assertion(
            result="count",
            item=item,
            content={
                "input_count": len(measured.source_material),
                "occurrences_carrying": item.occurrences_carrying,
                "count": item.count,
            },
            provenance="the exact source-material-set Assertion referenced here",
            local_support_identities=[],
            source_support_references=[measured.source_assertion_reference],
        )
        results.append(count)
        if item.count > 1:
            results.append(
                assertion(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    provenance="the exact count Assertion carried here",
                    local_support_identities=[count["dimensions"]["identity"]],
                    source_support_references=[],
                )
            )
    return results


def _record_pair_responsible_act_evidence(
    ledger: EventLedger,
    *,
    measured: MeasuredBytePairInputs,
    recording_locality_identity: str,
    result_content: dict[str, Any],
):
    """Preserve Evidence for this exact bounded responsible Act."""

    return ledger.append(
        BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": measured.downstream_act_identity,
            "act_occurrence_identity": measured.act_occurrence_identity,
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
            "input_assertion_reference": measured.source_assertion_reference,
            "input_role": BYTE_PAIR_INPUT_ROLE,
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence for this exact bounded responsible Measurement "
                "occurrence only; establishes no responsibility or authority "
                "for another Act"
            ),
        },
        locality_identity=recording_locality_identity,
    )


def _record_pair_input_applicability(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    applicability_assertion: dict[str, Any],
    recording_locality_identity: str,
):
    """Preserve Applicability whether or not the downstream Measurement occurs."""

    standing = applicability_assertion["dimensions"]["standing"]
    result_material = {
        "dimensions": {
            "identity": applicability_assertion["dimensions"]["identity"],
            "content": "exact source-Assertion to downstream-Act Applicability",
            "standing": standing,
            "source_provenance": applicability_assertion["dimensions"]["source_provenance"],
            "authority": BYTE_PAIR_APPLICABILITY_AUTHORITY,
        },
        "exact_act": "input Applicability determination",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "applicability_act_identity": applicability_assertion["applicability_act_identity"],
        "applicability_act_occurrence_identity": applicability_assertion[
            "applicability_act_occurrence_identity"
        ],
        "downstream_act_identity": applicability_assertion["downstream_act_identity"],
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "applicability": applicability_assertion,
        "downstream_act_outcome": "not established by this Applicability Assertion",
    }
    applicability_act_evidence = ledger.append(
        BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND,
        {
            "applicability_act_identity": applicability_assertion["applicability_act_identity"],
            "applicability_act_occurrence_identity": applicability_assertion[
                "applicability_act_occurrence_identity"
            ],
            "act": "input Applicability determination",
            "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
            "input_assertion_reference": source.reference,
            "input_movement_event_identity": source.locality_movement_event_identity,
            "input_role": BYTE_PAIR_INPUT_ROLE,
            "downstream_act_identity": applicability_assertion["downstream_act_identity"],
            "authority": BYTE_PAIR_APPLICABILITY_AUTHORITY,
            "evidence_scope": (
                "Evidence for this exact input Applicability "
                "determination occurrence"
            ),
        },
        locality_identity=recording_locality_identity,
    )
    evidence = _record_yield_evidence(
        ledger,
        locality_identity=recording_locality_identity,
        exact_act="input Applicability determination",
        act_occurrence_identity=applicability_assertion["applicability_act_occurrence_identity"],
        result_kind=BYTE_PAIR_APPLICABILITY_RESULT_KIND,
        result_identity=applicability_assertion["dimensions"]["identity"],
        result_content=result_material,
        responsibility=BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        live_boundary="byte_pair_applicability",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
        {
            **result_material,
            "yield_evidence_identity": evidence.identity,
            "responsible_act_evidence_identity": applicability_act_evidence.identity,
        },
        locality_identity=recording_locality_identity,
    )


def get_recorded_pair_input_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any] | None:
    """Read one historical input Applicability result without redetermining it."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != BYTE_PAIR_APPLICABILITY_RECORDED_KIND:
        raise ByteMeasurementError(f"{event_identity} is not pair-input Applicability")
    if ledger.integrity_of(event.identity) == CORRUPTED:
        raise ByteMeasurementError("corrupted Applicability cannot be read")
    material = event.material
    evidence_identity = material.get("yield_evidence_identity")
    evidence = ledger.get(evidence_identity) if isinstance(evidence_identity, str) else None
    if set(material) != BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES | {
        "yield_evidence_identity",
        "responsible_act_evidence_identity",
    }:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact Applicability result surface"
        )
    result_coordinates = {
        key: material[key] for key in BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES
    }
    if (
        evidence is None
        or evidence.kind != YIELD_EVIDENCE_KIND
        or evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind")
        != BYTE_PAIR_APPLICABILITY_RESULT_KIND
        or evidence.material.get("yield_coordinates") != sorted(result_coordinates)
        or evidence.material.get("dimensions", {}).get("responsibility")
        != BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY
        or evidence.material.get("dimensions", {}).get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or evidence.material.get("dimensions", {}).get("act_occurrence_identity")
        != material["applicability_act_occurrence_identity"]
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact Applicability yield Evidence"
        )
    act_evidence_identity = material.get("responsible_act_evidence_identity")
    act_evidence = ledger.get(act_evidence_identity) if isinstance(act_evidence_identity, str) else None
    expected_act_evidence = {
        "applicability_act_identity": material["applicability_act_identity"],
        "applicability_act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "act": "input Applicability determination",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "input_assertion_reference": material["input_assertion_reference"],
        "input_movement_event_identity": material["input_movement_event_identity"],
        "input_role": material["input_role"],
        "downstream_act_identity": material["downstream_act_identity"],
        "authority": BYTE_PAIR_APPLICABILITY_AUTHORITY,
        "evidence_scope": (
            "Evidence for this exact input Applicability "
            "determination occurrence"
        ),
    }
    if (
        act_evidence is None
        or act_evidence.kind != BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND
        or act_evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
        or act_evidence.material != expected_act_evidence
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact Applicability determination occurrence Evidence"
        )
    applicability_assertion = material.get("applicability")
    dimensions = applicability_assertion.get("dimensions") if isinstance(applicability_assertion, dict) else None
    standing = dimensions.get("standing") if isinstance(dimensions, dict) else None
    content = dimensions.get("content") if isinstance(dimensions, dict) else None
    measurement_locality = applicability_assertion.get("measurement_locality") if isinstance(applicability_assertion, dict) else None
    scope = applicability_assertion.get("scope_locality") if isinstance(applicability_assertion, dict) else None
    expected_identity = (
        "byte-pair-applicability:"
        + hashlib.sha256(
            _canonical(
                {
                    "content": content,
                    "scope": scope,
                    "measurement_locality": measurement_locality,
                    "standing": standing,
                }
            ).encode("utf-8")
        ).hexdigest()
        if isinstance(content, dict)
        and isinstance(scope, dict)
        and isinstance(measurement_locality, str)
        else None
    )
    if (
        standing not in {"applicable", "inapplicable", "conflicting", "Unknown"}
        or dimensions.get("identity") != expected_identity
        or applicability_assertion.get("result") != "input_applicability"
        or applicability_assertion.get("downstream_act_occurrence_identity") is not None
        or applicability_assertion.get("responsibility")
        != BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY
        or applicability_assertion.get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or applicability_assertion.get("assigned_by_responsibility")
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or applicability_assertion.get("applicability_act_identity") != material.get("applicability_act_identity")
        or applicability_assertion.get("applicability_act_occurrence_identity")
        != material.get("applicability_act_occurrence_identity")
        or material.get("applicability_act_identity")
        == material.get("applicability_act_occurrence_identity")
        or applicability_assertion.get("downstream_act") != "declared adjacent-byte-pair Measurement"
        or applicability_assertion.get("result_boundary") != BYTE_PAIR_RESULT_BOUNDARY
        or material.get("dimensions", {}).get("standing") != standing
        or material.get("downstream_act_identity") != applicability_assertion.get("downstream_act_identity")
        or material.get("input_assertion_reference") != applicability_assertion.get("input_assertion_reference")
        or material.get("input_role") != BYTE_PAIR_INPUT_ROLE
        or applicability_assertion.get("input_role") != BYTE_PAIR_INPUT_ROLE
        or material.get("responsibility")
        != BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY
        or material.get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or material.get("assigned_by_responsibility")
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or material.get("downstream_act_outcome")
        != "not established by this Applicability Assertion"
    ):
        raise ByteMeasurementError(f"{event_identity} carries incoherent Applicability")
    return json.loads(_canonical(applicability_assertion))


def record_adjacent_byte_pair_count_layer(
    ledger: EventLedger,
    *,
    source_measurement_event_identity: str,
    recording_locality_identity: str,
):
    """Record exact adjacent-byte-pair counts without crossing append boundaries."""

    if not isinstance(recording_locality_identity, str) or not recording_locality_identity:
        raise ByteMeasurementError(
            "adjacent-byte-pair Measurement recording requires an exact Locality"
        )
    source, scope, content, downstream_act_identity = _prepare_pair_source(
        ledger,
        source_measurement_event_identity=source_measurement_event_identity,
        measurement_locality_identity=recording_locality_identity,
    )
    applicability_act_identity = new_identity("byte_pair_applicability_act")
    applicability_act_occurrence_identity = new_identity(
        "byte_pair_applicability_occurrence"
    )
    applicability = _pair_input_applicability(
        source,
        downstream_act_identity=downstream_act_identity,
        applicability_act_identity=applicability_act_identity,
        applicability_act_occurrence_identity=applicability_act_occurrence_identity,
        measurement_locality_identity=recording_locality_identity,
    )
    applicability_event = _record_pair_input_applicability(
        ledger,
        source=source,
        applicability_assertion=applicability,
        recording_locality_identity=recording_locality_identity,
    )
    if applicability["dimensions"]["standing"] != "applicable":
        return applicability_event
    act_occurrence_identity = new_identity("adjacent_byte_pair_measurement_occurrence")
    measured = _measure_adjacent_byte_pair_counts_through(
        ledger,
        localities=tuple(scope["source_locality_identities"]),
        boundary=EventLedgerBoundary(content["completeness_boundary"]["identity"]),
        source_assertion_reference=source.reference,
        source_movement_event_identity=source.locality_movement_event_identity,
        input_applicability=applicability,
        downstream_act_identity=downstream_act_identity,
        act_occurrence_identity=act_occurrence_identity,
    )
    result_material = {
        "dimensions": {
            "identity": "adjacent-byte-pair-count-measurement-occurrence",
            "content": (
                "adjacent-byte-pair count and conditional recurrence Assertions"
            ),
            "standing": "measured",
            "source_provenance": "the recorded source-material-set Assertion",
            "authority": "unestablished",
            "evidence_scope": PAIR_MEASUREMENT_EVIDENCE_SCOPE,
        },
        "exact_act": "declared Measurement",
        "downstream_act_identity": measured.downstream_act_identity,
        "act_occurrence_identity": measured.act_occurrence_identity,
        "responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": _seed_native_measurement_assignment(
            measured
        ),
        "measurement_rule": BYTE_PAIR_MEASUREMENT_RULE,
        "source_assertion_reference": measured.source_assertion_reference,
        "source_movement_event_identity": measured.source_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "input_applicability": measured.input_applicability,
        "input_applicability_event_identity": applicability_event.identity,
        "source_locality_identities": list(measured.source_locality_identities),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
        "assertions": _pair_assertions(measured),
    }
    responsible_act_evidence = _record_pair_responsible_act_evidence(
        ledger,
        measured=measured,
        recording_locality_identity=recording_locality_identity,
        result_content=result_material,
    )
    evidence = _record_yield_evidence(
        ledger,
        locality_identity=recording_locality_identity,
        exact_act="declared Measurement",
        act_occurrence_identity=measured.act_occurrence_identity,
        result_kind=BYTE_PAIR_MEASUREMENT_RESULT_KIND,
        result_identity="adjacent-byte-pair-count-measurement-occurrence",
        result_content=result_material,
        responsibility=BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        live_boundary="byte_pair_measurement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        {
            **result_material,
            "yield_evidence_identity": evidence.identity,
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "occurrence_preservation": BYTE_PAIR_OCCURRENCE_PRESERVATION,
        },
        locality_identity=recording_locality_identity,
    )


def _validate_recorded_pair_input_applicability(
    applicability_assertion: Any,
    *,
    source: RecordedByteAssertion,
    event,
    downstream_act_identity: str,
) -> None:
    """Validate historical Applicability without determining it again."""

    source_material = source.material
    scope = source_material["assertion_scope"]
    content = {
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "downstream_act_identity": downstream_act_identity,
        "downstream_act": "declared adjacent-byte-pair Measurement",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "applicability_act_identity": applicability_assertion.get("applicability_act_identity"),
        "applicability_act_occurrence_identity": applicability_assertion.get(
            "applicability_act_occurrence_identity"
        ),
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
    }
    measurement_locality = event.locality_identity
    identity = "byte-pair-applicability:" + hashlib.sha256(
        _canonical(
            {
                "content": content,
                "scope": scope,
                "measurement_locality": measurement_locality,
                "standing": "applicable",
            }
        ).encode("utf-8")
    ).hexdigest()
    expected = {
        "dimensions": {
            "identity": identity,
            "content": content,
            "standing": "applicable",
            "source_provenance": source_material["dimensions"]["source_provenance"],
            "authority": BYTE_PAIR_APPLICABILITY_AUTHORITY,
        },
        "result": "input_applicability",
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "downstream_act_identity": downstream_act_identity,
        "downstream_act_occurrence_identity": None,
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "applicability_act_identity": applicability_assertion.get("applicability_act_identity"),
        "applicability_act_occurrence_identity": applicability_assertion.get(
            "applicability_act_occurrence_identity"
        ),
        "downstream_act": "declared adjacent-byte-pair Measurement",
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "measurement_locality": measurement_locality,
        "scope_locality": scope,
        "input_standing": source_material["dimensions"]["standing"],
        "input_authority": source_material["dimensions"]["authority"],
        "input_unknowns": source_material["unknowns"],
        "input_limits": source_material["limits"],
        "conflicts": [],
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
                "value": source_material["limits"],
                "treatment": "preserved as limits on this exact use",
            },
        },
        "unknowns": [
            "what any byte or adjacent byte pair represents remains Unknown"
        ],
        "limits": [
            "Applicability to this Measurement is not downstream applicability, "
            "admission, represented relation, or authority for another use"
        ],
    }
    if applicability_assertion != expected:
        raise ByteMeasurementError(
            f"{event.identity} does not carry its exact historical input Applicability"
        )


def assertions_of_recorded_adjacent_byte_pair_measurement(
    ledger: EventLedger, event_identity: str
) -> tuple[RecordedBytePairAssertion, ...] | None:
    """Read the exact pair result without performing Measurement again."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(
            f"{event_identity} is not an adjacent-byte-pair Measurement occurrence"
        )
    if ledger.integrity_of(event_identity) == CORRUPTED:
        raise ByteMeasurementError("a corrupted occurrence cannot expose pair results")
    material = event.material
    exact_surface = BYTE_PAIR_RESULT_COORDINATES | {
        "yield_evidence_identity",
        "responsible_act_evidence_identity",
        "occurrence_preservation",
    }
    if set(material) != exact_surface:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact pair result and recording surfaces"
        )
    expected_dimensions = {
        "identity": "adjacent-byte-pair-count-measurement-occurrence",
        "content": (
            "adjacent-byte-pair count and conditional recurrence Assertions"
        ),
        "standing": "measured",
        "source_provenance": "the recorded source-material-set Assertion",
        "authority": "unestablished",
        "evidence_scope": PAIR_MEASUREMENT_EVIDENCE_SCOPE,
    }
    if (
        material.get("occurrence_preservation") != BYTE_PAIR_OCCURRENCE_PRESERVATION
        or material.get("exact_act") != "declared Measurement"
        or material.get("responsibility") != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or not isinstance(material.get("downstream_act_identity"), str)
        or not material["downstream_act_identity"]
        or not isinstance(material.get("act_occurrence_identity"), str)
        or not material["act_occurrence_identity"]
        or material["downstream_act_identity"] == material["act_occurrence_identity"]
        or material.get("dimensions") != expected_dimensions
        or material.get("measurement_rule") != BYTE_PAIR_MEASUREMENT_RULE
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not preserve its exact pair Measurement Assertion"
        )
    evidence_identity = material.get("yield_evidence_identity")
    evidence = ledger.get(evidence_identity) if isinstance(evidence_identity, str) else None
    if (
        evidence is None
        or evidence.kind != YIELD_EVIDENCE_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind")
        != BYTE_PAIR_MEASUREMENT_RESULT_KIND
        or evidence.material.get("yield_coordinates")
        != sorted(BYTE_PAIR_RESULT_COORDINATES)
        or evidence.material.get("dimensions", {}).get("responsibility")
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or evidence.material.get("dimensions", {}).get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or evidence.material.get("dimensions", {}).get("act_occurrence_identity")
        != material["act_occurrence_identity"]
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact adjacent-byte-pair yield Evidence"
        )
    act_evidence_identity = material.get("responsible_act_evidence_identity")
    act_evidence = ledger.get(act_evidence_identity) if isinstance(act_evidence_identity, str) else None
    carried_applicability = material.get("input_applicability")
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
        raise ByteMeasurementError(f"{event_identity} carries no exact input Applicability")
    expected_act_evidence = {
        "downstream_act_identity": material["downstream_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": "declared adjacent-byte-pair Measurement",
        "responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": material[
            "responsibility_assignment_evidence"
        ],
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "input_applicability_identity": applicability_identity,
        "input_assertion_reference": material["source_assertion_reference"],
        "input_role": material["input_role"],
        "authority": "unestablished",
        "evidence_scope": (
            "Evidence for this exact bounded responsible Measurement "
            "occurrence only; establishes no responsibility or authority "
            "for another Act"
        ),
    }
    if (
        act_evidence is None
        or act_evidence.kind != BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND
        or act_evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
        or act_evidence.material != expected_act_evidence
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact responsible pair Measurement occurrence Evidence"
        )
    boundary_value = material.get("completeness_boundary")
    localities_value = material.get("source_locality_identities")
    if (
        not isinstance(boundary_value, dict)
        or set(boundary_value) != {"identity"}
        or not isinstance(boundary_value["identity"], str)
        or not isinstance(localities_value, list)
        or not localities_value
        or any(not isinstance(item, str) or not item for item in localities_value)
        or len(set(localities_value)) != len(localities_value)
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact pair Measurement boundary"
        )
    source_reference = material.get("source_assertion_reference")
    if (
        not isinstance(source_reference, dict)
        or set(source_reference) != {"recorded_occurrence_identity", "assertion_identity"}
        or not all(isinstance(value, str) and value for value in source_reference.values())
    ):
        raise ByteMeasurementError(f"{event_identity} carries no exact source Assertion")
    movement_event_identity = material.get("source_movement_event_identity")
    if movement_event_identity is None:
        source_results = assertions_of_recorded_byte_measurement(
            ledger, source_reference["recorded_occurrence_identity"]
        )
        source = next(
            (
                item
                for item in source_results or ()
                if item.assertion_identity == source_reference["assertion_identity"]
            ),
            None,
        )
    elif isinstance(movement_event_identity, str) and movement_event_identity:
        source = _validate_moved_byte_assertion(ledger, movement_event_identity)
    else:
        source = None
    if source is not None and source.assertion_identity != source_reference["assertion_identity"]:
        source = None
    if source is None or event.locality_identity is None:
        raise ByteMeasurementError(
            f"{event_identity} does not carry its exact input source Assertion"
        )
    source_material = source.material
    source_scope = source_material["assertion_scope"]
    source_content = source_material["dimensions"]["content"]
    expected_assignment_evidence = {
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "standing": "assigned",
        "source_occurrence_references": source_content["source_material"],
            "completeness_boundary": source_content["completeness_boundary"][
                "identity"
            ],
        "determination": (
            "exact ingest and raw-material occurrences were read through the "
            "recorded boundary"
        ),
    }
    if (
        localities_value != source_scope["source_locality_identities"]
        or boundary_value != source_content["completeness_boundary"]
        or material.get("responsibility_assignment_evidence")
        != expected_assignment_evidence
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry its exact input source boundary"
        )
    _validate_recorded_pair_input_applicability(
        material.get("input_applicability"),
        source=source,
        event=event,
        downstream_act_identity=material["downstream_act_identity"],
    )
    applicability_event_identity = material.get("input_applicability_event_identity")
    recorded_applicability = (
        get_recorded_pair_input_applicability(ledger, applicability_event_identity)
        if isinstance(applicability_event_identity, str)
        else None
    )
    if recorded_applicability != material.get("input_applicability"):
        raise ByteMeasurementError(
            f"{event_identity} does not name its exact recorded input Applicability"
        )
    expected_scope = {
        "source_locality_identities": localities_value,
    }
    assertions = material.get("assertions")
    if not isinstance(assertions, list):
        raise ByteMeasurementError(f"{event_identity} carries no pair result Assertions")
    by_pair: dict[tuple[int, int], dict[str, dict[str, Any]]] = {}
    exact_keys = {
        "dimensions",
        "subject_kind",
        "responsible_boundary",
        "result",
        "assertion_subject",
        "assertion_scope",
        "input_support",
        "conflicts",
        "unknowns",
        "limits",
    }
    for assertion in assertions:
        if not isinstance(assertion, dict) or set(assertion) != exact_keys:
            raise ByteMeasurementError(f"{event_identity} carries a malformed pair Assertion")
        subject = assertion.get("assertion_subject")
        result = assertion.get("result")
        dimensions = assertion.get("dimensions")
        representation = (
            subject.get("representation") if isinstance(subject, dict) else None
        )
        if (
            type(representation) is not list
            or len(representation) != 2
            or any(
                type(value) is not int or not 0 <= value <= 255
                for value in representation
            )
            or subject
            != {
                "representation": representation,
                "measurement_rule": BYTE_PAIR_MEASUREMENT_RULE,
            }
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
                    "evidence_scope",
                }
            or dimensions.get("standing") != "measured"
            or dimensions.get("responsibility") != MEASURED_ASSERTION_RESPONSIBILITY
            or dimensions.get("authority") != "unestablished"
            or dimensions.get("evidence_scope") != PAIR_MEASUREMENT_EVIDENCE_SCOPE
            or assertion.get("unknowns") != list(BYTE_PAIR_UNKNOWNS)
            or assertion.get("limits")
            != list(BYTE_PAIR_LIMITS)
        ):
            raise ByteMeasurementError(f"{event_identity} carries an unlawful pair Assertion")
        content = dimensions.get("content")
        expected_identity = _identity(
            result=result, subject=subject, scope=expected_scope, content=content
        )
        if dimensions.get("identity") != expected_identity:
            raise ByteMeasurementError(f"{event_identity} carries a false pair Assertion identity")
        group = by_pair.setdefault(tuple(representation), {})
        if result in group:
            raise ByteMeasurementError(f"{event_identity} duplicates one pair result")
        group[result] = assertion
    for group in by_pair.values():
        count = group.get("count")
        if count is None:
            raise ByteMeasurementError(f"{event_identity} carries recurrence without count")
        count_content = count["dimensions"]["content"]
        if (
            not isinstance(count_content, dict)
            or set(count_content)
            != {"input_count", "occurrences_carrying", "count"}
            or any(type(value) is not int or value <= 0 for value in count_content.values())
            or count_content["occurrences_carrying"] > count_content["input_count"]
            or count_content["occurrences_carrying"] > count_content["count"]
            or count["input_support"]
            != {"assertion_references": [source_reference], "local_assertion_identities": []}
            or count["dimensions"]["source_provenance"]
            != "the exact source-material-set Assertion referenced here"
        ):
            raise ByteMeasurementError(f"{event_identity} carries an unlawful pair count")
        recurrence = group.get("recurrence")
        if (recurrence is not None) != (count_content["count"] > 1):
            raise ByteMeasurementError(f"{event_identity} carries the wrong recurrence boundary")
        if recurrence is not None and (
            recurrence["dimensions"]["content"] != {"recurrence_established": True}
            or recurrence["dimensions"]["source_provenance"]
            != "the exact count Assertion carried here"
            or recurrence["input_support"]
            != {
                "assertion_references": [],
                "local_assertion_identities": [count["dimensions"]["identity"]],
            }
        ):
            raise ByteMeasurementError(f"{event_identity} carries unlawful recurrence support")
    validated_results = []
    for assertion in assertions:
        support = assertion["input_support"]
        support_references = list(support["assertion_references"])
        support_references.extend(
            {
                "recorded_occurrence_identity": event.identity,
                "assertion_identity": local_identity,
            }
            for local_identity in support["local_assertion_identities"]
        )
        validated_results.append(RecordedBytePairAssertion(
            assertion_identity=assertion["dimensions"]["identity"],
            recorded_occurrence_identity=event.identity,
            representation=tuple(assertion["assertion_subject"]["representation"]),
            result=assertion["result"],
            _material_json=_canonical(assertion),
            _support_assertion_refs_json=_canonical(support_references),
        ))
    return tuple(validated_results)


def input_applicability_of_recorded_adjacent_byte_pair_measurement(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any] | None:
    """Validate the independent input-to-Act Applicability Assertion."""

    read = assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event_identity)
    if read is None:
        return None
    event = ledger.get(event_identity)
    return json.loads(_canonical(event.material["input_applicability"]))
