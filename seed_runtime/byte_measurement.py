"""Measure exact bytes across complete bounded ingest occurrences.

This is the first acquisition boundary that does not receive its measured
subjects from a caller.  The subjects are the literal byte values carried by
the exact raw material linked from every ingest occurrence in the declared
Localities through one recorded ledger boundary.

One byte value receives one count Assertion.  Recurrence is a separate
Assertion and exists only where the total count exceeds one.  The same byte
material establishes no character, word, position pair, grammar, or represented
relation.
"""

from __future__ import annotations


from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.event import Event
from seed_runtime.identities import new_identity
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
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
    "operator.measurement.byte_position_pair_counts_recorded"
)
BYTE_PAIR_MEASUREMENT_RESULT_KIND = "exact byte-position-pair count Measurement results"
RESPONSIBILITY_UNESTABLISHED = "unestablished"
BYTE_OCCURRENCE_PRESERVATION = (
    "byte Measurement results recorded after Yield"
)
BYTE_PAIR_OCCURRENCE_PRESERVATION = (
    "byte-position-pair Measurement results recorded after Yield"
)
BYTE_RESULT_COORDINATES = frozenset(
    {
        "result_identity",
        "dimensions",
        "exact_act",
        "downstream_act_identity",
        "act_occurrence_identity",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_reference",
        "measurement_rule",
        "source_localities",
        "completeness_boundary",
        "assertions",
    }
)
BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND = (
    "operator.measurement.byte_responsible_act_evidenced"
)
BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.measurement.byte_responsibility_assignment_recorded"
)
BYTE_PAIR_RESULT_COORDINATES = (
    BYTE_RESULT_COORDINATES - {"responsibility_assignment_reference"}
) | {
    "responsibility_assignment_evidence",
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
    "operator.measurement.byte_position_pair_responsible_act_evidenced"
)
BYTE_PAIR_APPLICABILITY_RECORDED_KIND = (
    "operator.measurement.byte_position_pair_input_applicability_recorded"
)
BYTE_PAIR_APPLICABILITY_RESULT_KIND = "byte-position-pair input Applicability result"
BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES = frozenset(
    {
        "result_identity",
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
    }
)
BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND = (
    "operator.measurement.byte_position_pair_applicability_act_evidenced"
)
ASSERTION_LOCALITY_MOVEMENT_KIND = "operator.assertion.locality_movement_recorded"
ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND = (
    "operator.assertion.locality_movement_responsibility_assignment_recorded"
)
ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND = (
    "operator.assertion.locality_movement_act_evidenced"
)
ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND = "Assertion Locality movement result"
EVENT_KIND_RESPONSIBILITIES = {
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: "01.Source.D",
    BYTE_MEASUREMENT_RECORDED_KIND: "01.Source.D",
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND: "01.Source.D",
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND: "02.Acts.A",
    BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND: "02.Acts.A",
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND: "01.Standing.E.1",
    BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND: "03.Movement.A",
    ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND: "02.Acts.A",
    ASSERTION_LOCALITY_MOVEMENT_KIND: "03.Movement.A",
}
ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY = (
    "make one exact preserved Assertion available in another Locality and "
    "preserve its identity, Standing, and carried limits"
)
BYTE_MEASUREMENT_RULE = (
    "each exact byte in exact recorded Ingest material with the same exact byte "
    "material"
)
BYTE_PAIR_MEASUREMENT_RULE = (
    "each exact byte-pair occurrence in source order within one exact recorded Ingest "
    "material occurrence with the same exact pair material and source order"
)
MEASUREMENT_EVIDENCE_SCOPE = (
    "exact byte-count Measurement Evidence; bounded byte Standing; source "
    "Standing not revised"
)
SOURCE_SET_EVIDENCE_SCOPE = (
    "exact bounded source-material Measurement Evidence"
)
PAIR_MEASUREMENT_EVIDENCE_SCOPE = (
    "declared exact-source ordered byte-position-pair Measurement Evidence; exact "
    "measured pair and order; bounded pair Standing; source Standing not revised"
)
BYTE_PAIR_RESULT_BOUNDARY = (
    "establish exact counts of byte-pair occurrences in source order within the exact "
    "bounded source material"
)
BYTE_PAIR_INPUT_ROLE = "exact bounded source material for position-byte Measurement"
SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY = "this Seed"
BYTE_MEASUREMENT_RESPONSIBILITY = (
    "perform the bounded exact-byte Measurement and Yield the findings "
    "established by its exact source occurrences, rule, Scope, Authority, and limits"
)
BYTE_PAIR_MEASUREMENT_RESPONSIBILITY = (
    "Yield exact byte-position-pair findings from an applicable exact bounded "
    "source material within its Scope, provenance, occurrence references, "
    "Authority, Unknown, and limits"
)
BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY = (
    "determine whether one exact source-material-set Assertion may participate "
    "in one exact byte-position-pair Measurement Act"
)
BYTE_PAIR_APPLICABILITY_AUTHORITY = (
    "determine Applicability of this exact proposed input to this exact downstream "
    "Act; establishes no Applicability for another Act; the resulting Standing, "
    "not this authority, determines participation"
)
BYTE_PAIR_UNKNOWN = (
    "what this ordered byte position pair participates in or represents remains Unknown",
)
BYTE_PAIR_LIMITS = (
    "an exact byte-position-pair count or recurrence bounded by the exact measured "
    "pair and order",
)
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve this measured Assertion's carried Standing coordinates"
)
ASSERTION_RESPONSIBILITIES = {
    MEASURED_ASSERTION_RESPONSIBILITY: "01.Standing.D.1",
}


class ByteMeasurementError(ValueError):
    """The exact byte Measurement could not be performed as declared."""


def _require_exact_result_yield(
    ledger: EventLedger,
    event: Any,
    evidence: Any,
    act_evidence: Any,
    *,
    result_name: str,
    occurrence_coordinate: str = "act_occurrence_identity",
) -> None:
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=evidence.identity,
        responsible_act_evidence_event_identity=act_evidence.identity,
        recorded_result_occurrence_coordinate=occurrence_coordinate,
        responsible_act_occurrence_coordinate=occurrence_coordinate,
    )
    if not all(requirements.values()):
        raise ByteMeasurementError(
            f"{event.identity} names no exact {result_name} yield Evidence"
        )


@dataclass(frozen=True)
class MeasuredByteCount:
    representation: int
    occurrences_carrying: int
    count: int


@dataclass(frozen=True)
class MeasuredByteInputs:
    source_localities: tuple[str, ...]
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
    source_localities: tuple[str, ...]
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


@dataclass(frozen=True)
class _RecordedBytePairFinding:
    assertion_identity: str
    recorded_occurrence_identity: str
    representation: tuple[int, int]
    result: str
    _content_coordinates: tuple[int, int, int] | bool
    _local_support_assertion_identities: tuple[str, ...]

    @property
    def content(self) -> dict[str, int | bool]:
        if self.result == "recurrence":
            return {"recurrence_established": self._content_coordinates}
        input_count, occurrences_carrying, count = self._content_coordinates
        return {
            "input_count": input_count,
            "occurrences_carrying": occurrences_carrying,
            "count": count,
        }

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


_BYTE_PAIR_MEASUREMENT_RULE_JSON = _canonical(BYTE_PAIR_MEASUREMENT_RULE)


def _identity(
    *, result: str, subject: dict[str, Any], scope: dict[str, Any], content: Any
) -> str:
    carried = {"result": result, "subject": subject, "scope": scope, "content": content}
    return "byte-measurement:" + hashlib.sha256(
        _canonical(carried).encode("utf-8")
    ).hexdigest()


def _pair_assertion_identity(
    *,
    result: str,
    representation: tuple[int, int],
    canonical_scope: str,
    content: dict[str, Any],
) -> str:
    """Hash the fixed pair-Assertion JSON shape without rebuilding that shape."""

    first, second = representation
    canonical_subject = (
        '{"measurement_rule":'
        + _BYTE_PAIR_MEASUREMENT_RULE_JSON
        + f',"representation":[{first},{second}]}}'
    )
    if result == "recurrence":
        canonical_content = '{"recurrence_established":true}'
        canonical_result = '"recurrence"'
    else:
        canonical_content = (
            f'{{"count":{content["count"]},'
            f'"input_count":{content["input_count"]},'
            f'"occurrences_carrying":{content["occurrences_carrying"]}}}'
        )
        canonical_result = '"count"'
    carried = (
        '{"content":'
        + canonical_content
        + ',"result":'
        + canonical_result
        + ',"scope":'
        + canonical_scope
        + ',"subject":'
        + canonical_subject
        + "}"
    )
    return "byte-measurement:" + hashlib.sha256(carried.encode("utf-8")).hexdigest()


def _seed_native_measurement_assignment(
    measured: MeasuredByteInputs | MeasuredBytePairInputs,
) -> dict[str, Any]:
    """Return why this exact preserved-material Measurement belongs here."""

    return {
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "standing": "assigned",
        "source_occurrence_references": [dict(item) for item in measured.source_material],
        "completeness_boundary": measured.completeness_boundary.identity,
        "determination": (
            "exact Ingest and material occurrences through the recorded boundary"
        ),
    }


def _recorded_input_assertion_standing(
    ledger: EventLedger,
    source: RecordedByteAssertion,
    *,
    measurement_locality_identity: str,
) -> tuple[RecordedByteAssertion, dict[str, str | None]]:
    """Resolve the exact result occurrence carrying one proposed input.

    The Assertion's detached material is not Standing.  Its intact Measurement
    result occurrence is the Standing carrier; an exact movement occurrence
    preserves that Standing when the downstream Act has another Locality.
    """

    if type(source) is not RecordedByteAssertion:
        raise ByteMeasurementError(
            "byte-position-pair Applicability requires one recorded byte Assertion"
        )
    if source.locality_movement_event_identity is None:
        source_event = ledger.get(source.recorded_occurrence_identity)
        readings = assertions_of_recorded_byte_measurement(
            ledger, source.recorded_occurrence_identity
        )
        exact = next(
            (
                reading
                for reading in readings or ()
                if reading.assertion_identity == source.assertion_identity
            ),
            None,
        )
        if (
            source_event is None
            or source_event.locality_identity != measurement_locality_identity
        ):
            exact = None
    else:
        exact = _validate_moved_byte_assertion(
            ledger, source.locality_movement_event_identity
        )
        movement = ledger.get(source.locality_movement_event_identity)
        if (
            movement is None
            or movement.locality_identity != measurement_locality_identity
        ):
            exact = None
    if (
        exact is None
        or exact.result != "exact_source_material_set"
        or exact.reference != source.reference
        or exact.locality_movement_event_identity
        != source.locality_movement_event_identity
    ):
        raise ByteMeasurementError(
            "byte-position-pair Applicability requires exact input Standing"
        )
    return exact, {
        "recorded_measurement_result_occurrence_identity": (
            exact.recorded_occurrence_identity
        ),
        "assertion_identity": exact.assertion_identity,
        "locality_movement_result_occurrence_identity": (
            exact.locality_movement_event_identity
        ),
    }


def _pair_input_applicability(
    ledger: EventLedger,
    source: RecordedByteAssertion,
    *,
    downstream_act_identity: str,
    applicability_act_identity: str,
    applicability_act_occurrence_identity: str,
    measurement_locality_identity: str,
) -> dict[str, Any]:
    """Determine this source Assertion's use by this exact pair Measurement."""

    source, input_standing = _recorded_input_assertion_standing(
        ledger,
        source,
        measurement_locality_identity=measurement_locality_identity,
    )
    material = source.material
    scope = material["assertion_scope"]
    content = {
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "downstream_act_identity": downstream_act_identity,
        "downstream_act": "declared byte-position-pair Measurement",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "assigned_by_responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "applicability_act_identity": applicability_act_identity,
        "applicability_act_occurrence_identity": applicability_act_occurrence_identity,
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
    }
    if (
        material["dimensions"].get("authority") != "unestablished"
        or material["dimensions"].get("evidence_scope")
        != SOURCE_SET_EVIDENCE_SCOPE
    ):
        standing = "Unknown"
        basis = "the input carries no recognized Evidence scope for this exact source-material use"
        applicability_scope = scope
        source_provenance = material["dimensions"]["source_provenance"]
        input_authority = material["dimensions"]["authority"]
        input_unknown = material["unknown"]
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
        input_authority = material["dimensions"]["authority"]
        input_unknown = material["unknown"]
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
        "downstream_act": "declared byte-position-pair Measurement",
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "measurement_locality": measurement_locality_identity,
        "scope_locality": applicability_scope,
        "input_standing": input_standing,
        "input_authority": input_authority,
        "input_unknown": input_unknown,
        "input_limits": input_limits,
        "conflicts": [basis] if standing == "conflicting" else [],
        "coordinate_treatment": {
            "support_relation_standing": {
                "carried": False,
                "treatment": "not established by Applicability",
            },
            "known_loss": {"carried": False, "treatment": "not represented by input"},
            "current_Standing": {
                "carried": False,
                "treatment": "not required for this historical bounded source material",
            },
            "negative_authority": negative_authority,
        },
        "unknown": [
            "what any byte or byte position pair represents remains Unknown",
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
    source_localities: Iterable[str],
) -> MeasuredByteInputs:
    """Count every exact byte in every declared Locality through one boundary."""

    localities = tuple(dict.fromkeys(source_localities))
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
            exact = _ingested_bytes(ledger, ingest)
            if ingest.identity in seen_material:
                raise ByteMeasurementError(
                    "one Ingest occurrence cannot enter a byte Measurement twice"
                )
            seen_material.add(ingest.identity)
            source_material.append({"ingest_occurrence_identity": ingest.identity})
            for value, count in Counter(exact).items():
                carrying[value] += 1
                totals[value] += count
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
        source_localities=localities,
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
            "byte-position-pair Measurement requires an exact Act Locality"
        )
    read = assertions_of_recorded_byte_measurement(
        ledger, source_measurement_event_identity
    )
    if read is None:
        raise ByteMeasurementError("byte-position-pair Measurement requires a source")
    source = next(
        (item for item in read if item.result == "exact_source_material_set"),
        None,
    )
    if source is None:
        raise ByteMeasurementError(
            "byte-position-pair Measurement requires an exact source-material-set Assertion"
        )
    source = _move_byte_assertion_to_locality(
        ledger,
        source=source,
        destination_locality=measurement_locality_identity,
    )
    material = source.material
    scope = material["assertion_scope"]
    content = material["dimensions"]["content"]
    downstream_act_identity = new_identity("byte_position_pair_measurement_act")
    return source, scope, content, downstream_act_identity


def _movement_assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
    }


def _source_assertion_from_reference(
    ledger: EventLedger, reference: Any
) -> tuple[RecordedByteAssertion, Event]:
    if type(reference) is not dict or set(reference) != {
        "recorded_occurrence_identity",
        "assertion_identity",
    }:
        raise ByteMeasurementError("Assertion movement carries no exact source")
    source_results = assertions_of_recorded_byte_measurement(
        ledger, reference["recorded_occurrence_identity"]
    )
    source = next(
        (
            item
            for item in source_results or ()
            if item.assertion_identity == reference["assertion_identity"]
        ),
        None,
    )
    source_event = ledger.get(reference["recorded_occurrence_identity"])
    if source is None or source_event is None or source_event.locality_identity is None:
        raise ByteMeasurementError("Assertion movement source cannot be read")
    return source, source_event


def _source_measurement_standing_coordinates(source_event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": source_event.identity,
        "result_identity": source_event.material["result_identity"],
        "act_occurrence_identity": source_event.material["act_occurrence_identity"],
        "responsible_act_evidence_identity": source_event.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": source_event.material[
            "evidence_of_yield_relation_identity"
        ],
    }


def _require_current_movement_source_standing(
    ledger: EventLedger,
    *,
    source_event: Event,
    locality_standing: dict[str, Any],
) -> str:
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    current = read_operator_locality_standing(
        ledger, locality_identity=source_event.locality_identity
    )
    boundary = locality_standing.get("through_event_occurrence_identity")
    if (
        locality_standing != current
        or type(boundary) is not str
        or not boundary
        or locality_standing.get("measurement_occurrences", {}).get(
            source_event.identity
        )
        != _source_measurement_standing_coordinates(source_event)
    ):
        raise ByteMeasurementError(
            "Assertion movement assignment requires exact current source Standing"
        )
    return boundary


def _require_current_movement_destination_standing(
    ledger: EventLedger,
    *,
    destination_locality: str,
    locality_standing: dict[str, Any],
    assignment_identity: str | None = None,
) -> str | None:
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    current = read_operator_locality_standing(
        ledger, locality_identity=destination_locality
    )
    boundary = locality_standing.get("through_event_occurrence_identity")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    if (
        locality_standing != current
        or locality_standing.get("locality_identity") != destination_locality
        or (boundary is not None and (type(boundary) is not str or not boundary))
        or (
            assignment_identity is not None
            and (
                type(assignments) is not dict
                or assignments.get(assignment_identity, object()) is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "Assertion movement requires exact current destination Standing"
        )
    return boundary


def _movement_assignment_material(
    *,
    source: RecordedByteAssertion,
    source_locality: str,
    destination_locality: str,
    source_standing_boundary_identity: str,
    destination_standing_boundary_identity: str | None,
    assignment_identity: str,
    assignment_subject_identity: str,
    movement_act_identity: str,
    movement_act_occurrence_identity: str,
    movement_result_identity: str,
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "movement_act_identity": movement_act_identity,
        "movement_act_occurrence_identity": movement_act_occurrence_identity,
        "movement_result_identity": movement_result_identity,
        "book_clause_identity": "03.Movement.A",
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "source_assertion_reference": source.reference,
        "source_locality": source_locality,
        "destination_locality": destination_locality,
        "source_standing_boundary_identity": source_standing_boundary_identity,
        "destination_standing_boundary_identity": (
            destination_standing_boundary_identity
        ),
        "determination": (
            "the exact preserved Assertion available in another Locality"
        ),
        "scope": {
            "source_assertion_reference": source.reference,
            "source_standing_boundary_identity": source_standing_boundary_identity,
            "destination_standing_boundary_identity": (
                destination_standing_boundary_identity
            ),
        },
        "authority": source.material["dimensions"]["authority"],
        "limits": [
            "assignment is bounded to the exact source Assertion and source and "
            "destination Standing boundaries"
        ],
        "unknown": ["what the exact Assertion represents remains Unknown"],
    }


def record_assertion_locality_movement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    destination_locality: str,
    source_locality_standing: dict[str, Any],
    destination_locality_standing: dict[str, Any],
) -> Event:
    """Record the exact Responsibility assignment for one Assertion movement."""

    if type(destination_locality) is not str or not destination_locality:
        raise ByteMeasurementError("Assertion movement requires a destination Locality")
    exact_source, source_event = _source_assertion_from_reference(
        ledger, source.reference
    )
    if exact_source != source:
        raise ByteMeasurementError("Assertion movement requires its exact source")
    if source_event.locality_identity == destination_locality:
        raise ByteMeasurementError("same-Locality Assertion requires no movement")
    source_boundary = _require_current_movement_source_standing(
        ledger,
        source_event=source_event,
        locality_standing=source_locality_standing,
    )
    destination_boundary = _require_current_movement_destination_standing(
        ledger,
        destination_locality=destination_locality,
        locality_standing=destination_locality_standing,
    )
    identities = {
        "assignment_identity": new_identity("assertion_locality_movement_assignment"),
        "assignment_subject_identity": new_identity(
            "assertion_locality_movement_assignment_subject"
        ),
        "movement_act_identity": new_identity("assertion_locality_movement_act"),
        "movement_act_occurrence_identity": new_identity(
            "assertion_locality_movement_occurrence"
        ),
        "movement_result_identity": new_identity(
            "assertion_locality_movement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError("Assertion movement lifecycle identities collapsed")
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND,
        _movement_assignment_material(
            source=source,
            source_locality=source_event.locality_identity,
            destination_locality=destination_locality,
            source_standing_boundary_identity=source_boundary,
            destination_standing_boundary_identity=destination_boundary,
            **identities,
        ),
        locality_identity=destination_locality,
    )


def _read_assertion_locality_movement_responsibility_assignment(
    ledger: EventLedger,
    assignment_event_identity: str,
    *,
    prior_destination_standing: dict[str, Any] | None = None,
) -> tuple[Event, RecordedByteAssertion, Event]:
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind
        != ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
        or assignment.locality_identity is None
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment is absent or corrupted"
        )
    material = assignment.material
    source, source_event = _source_assertion_from_reference(
        ledger, material.get("source_assertion_reference")
    )
    identities = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "assignment_identity",
            "assignment_subject_identity",
            "movement_act_identity",
            "movement_act_occurrence_identity",
            "movement_result_identity",
        )
    }
    source_boundary = material.get("source_standing_boundary_identity")
    destination_boundary = material.get("destination_standing_boundary_identity")
    if (
        any(type(identity) is not str or not identity for identity in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(source_boundary) is not str
        or not source_boundary
        or (
            destination_boundary is not None
            and (type(destination_boundary) is not str or not destination_boundary)
        )
    ):
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment carries malformed coordinates"
        )
    expected = _movement_assignment_material(
        source=source,
        source_locality=source_event.locality_identity,
        destination_locality=assignment.locality_identity,
        source_standing_boundary_identity=source_boundary,
        destination_standing_boundary_identity=destination_boundary,
        **identities,
    )
    if material != expected:
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment coordinates are not exact"
        )
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing_through,
    )

    try:
        source_standing = read_operator_locality_standing_through(
            ledger,
            locality_identity=source_event.locality_identity,
            through_event_occurrence_identity=source_boundary,
        )
        if prior_destination_standing is None:
            prior_destination_standing = read_operator_locality_standing_through(
                ledger,
                locality_identity=assignment.locality_identity,
                through_event_occurrence_identity=destination_boundary,
            )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment has no exact Standing"
        ) from error
    if source_standing.get("measurement_occurrences", {}).get(source_event.identity) != (
        _source_measurement_standing_coordinates(source_event)
    ):
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment has no exact source Standing"
        )
    prior_destination_boundary = prior_destination_standing.get(
        "through_event_occurrence_identity"
    )
    carried_assignments = prior_destination_standing.get(
        "responsibility_assignment_occurrences"
    )
    destination_boundary_is_exact = prior_destination_boundary == destination_boundary
    assignment_is_carried_later = bool(
        type(prior_destination_boundary) is str
        and prior_destination_boundary
        and type(carried_assignments) is dict
        and carried_assignments.get(assignment.identity, object()) is None
    )
    if (
        prior_destination_standing.get("locality_identity")
        != assignment.locality_identity
        or not (destination_boundary_is_exact or assignment_is_carried_later)
    ):
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment has no exact destination Standing"
        )
    order = (assignment.identity,)
    if destination_boundary is not None:
        order = (destination_boundary, assignment.identity)
    if assignment_is_carried_later and prior_destination_boundary != assignment.identity:
        order = (*order, prior_destination_boundary)
    try:
        ledger.occurrences_in_append_order(
            order, locality_identity=assignment.locality_identity
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment order is false"
        ) from error
    return assignment, source, source_event


def get_assertion_locality_movement_responsibility_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> Event:
    return _read_assertion_locality_movement_responsibility_assignment(
        ledger, assignment_event_identity
    )[0]


def _movement_act_material(assignment: Event) -> dict[str, Any]:
    return {
        "act": "Assertion Locality movement",
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": _movement_assignment_reference(
            assignment
        ),
        "movement_act_identity": assignment.material["movement_act_identity"],
        "movement_act_occurrence_identity": assignment.material[
            "movement_act_occurrence_identity"
        ],
        "source_assertion_reference": assignment.material[
            "source_assertion_reference"
        ],
        "source_locality": assignment.material["source_locality"],
        "destination_locality": assignment.locality_identity,
        "locality_relation": {
            "first_subject": assignment.material["source_assertion_reference"],
            "second_subject": assignment.locality_identity,
            "relation_occurrence_identity": assignment.material[
                "movement_act_occurrence_identity"
            ],
        },
        "authority": assignment.material["authority"],
        "evidence_scope": "Evidence for this exact Assertion Locality movement",
    }


def record_assertion_locality_movement_responsible_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    assignment, _source, _source_event = (
        _read_assertion_locality_movement_responsibility_assignment(
            ledger, responsibility_assignment_event_identity
        )
    )
    _require_current_movement_destination_standing(
        ledger,
        destination_locality=assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        assignment_identity=assignment.identity,
    )
    for prior in ledger.iter_locality_kind(
        assignment.locality_identity,
        ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND,
    ):
        if prior.material.get("responsibility_assignment_reference") == (
            _movement_assignment_reference(assignment)
        ):
            raise ByteMeasurementError(
                "Assertion movement Responsibility assignment already carries an Act"
            )
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND,
        _movement_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def _record_assertion_locality_movement_act_from_carried_standing(
    ledger: EventLedger,
    *,
    assignment: Event,
    destination_standing: dict[str, Any],
) -> Event:
    if (
        assignment.kind
        != ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
        or ledger.get(assignment.identity) != assignment
        or ledger.integrity_of(assignment.identity) == CORRUPTED
        or destination_standing.get("locality_identity")
        != assignment.locality_identity
        or destination_standing.get("through_event_occurrence_identity")
        != assignment.identity
        or destination_standing.get(
            "responsibility_assignment_occurrences", {}
        ).get(assignment.identity, object())
        is not None
        or ledger.append_boundary_through_occurrence(assignment.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "Assertion movement Act requires exact carried assignment Standing"
        )
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND,
        _movement_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def _read_assertion_locality_movement_act_evidence(
    ledger: EventLedger,
    act_evidence_event_identity: str,
    *,
    prior_destination_standing: dict[str, Any] | None = None,
) -> tuple[Event, Event, RecordedByteAssertion]:
    act = ledger.get(act_evidence_event_identity)
    if (
        act is None
        or act.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ByteMeasurementError("Assertion movement Act Evidence is absent or corrupted")
    reference = act.material.get("responsibility_assignment_reference")
    if type(reference) is not dict:
        raise ByteMeasurementError("Assertion movement Act carries no exact assignment")
    assignment, source, _source_event = (
        _read_assertion_locality_movement_responsibility_assignment(
            ledger,
            reference.get("recorded_occurrence_identity"),
            prior_destination_standing=prior_destination_standing,
        )
    )
    if (
        reference != _movement_assignment_reference(assignment)
        or act.locality_identity != assignment.locality_identity
        or act.material != _movement_act_material(assignment)
    ):
        raise ByteMeasurementError("Assertion movement Act Evidence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, act.identity),
            locality_identity=assignment.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError("Assertion movement Act order is false") from error
    return act, assignment, source


def _movement_result_material(
    assignment: Event,
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["movement_result_identity"],
        "movement_act_identity": assignment.material["movement_act_identity"],
        "movement_act_occurrence_identity": assignment.material[
            "movement_act_occurrence_identity"
        ],
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": _movement_assignment_reference(
            assignment
        ),
        "source_assertion_reference": assignment.material[
            "source_assertion_reference"
        ],
        "assertion_identity": assignment.material["source_assertion_reference"][
            "assertion_identity"
        ],
        "source_locality": assignment.material["source_locality"],
        "destination_locality": assignment.locality_identity,
        "locality_relation": {
            "first_subject": assignment.material["source_assertion_reference"],
            "second_subject": assignment.locality_identity,
            "relation_occurrence_identity": assignment.material[
                "movement_act_occurrence_identity"
            ],
        },
        "preserved_coordinates": [
            "Evidence",
            "Authority",
            "Scope",
            "Unknown",
            "limits",
            "Standing",
        ],
        "authority": assignment.material["authority"],
        "movement_scope": (
            "Locality movement bounded to this exact Assertion; establishes no "
            "different identity or Standing"
        ),
    }


def record_assertion_locality_movement_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act, assignment, _source = _read_assertion_locality_movement_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    for kind in (
        RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
        ASSERTION_LOCALITY_MOVEMENT_KIND,
    ):
        for prior in ledger.iter_locality_kind(assignment.locality_identity, kind):
            if prior.material.get("responsible_act_evidence_identity") == act.identity:
                raise ByteMeasurementError(
                    "Assertion movement Act already carries a Yield or result"
                )
    return _append_assertion_locality_movement_result(
        ledger, act=act, assignment=assignment
    )


def _append_assertion_locality_movement_result(
    ledger: EventLedger, *, act: Event, assignment: Event
) -> Event:
    result_material = _movement_result_material(assignment)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=assignment.locality_identity,
        exact_act="Assertion Locality movement",
        act_occurrence_identity=assignment.material[
            "movement_act_occurrence_identity"
        ],
        responsible_act_evidence_identity=act.identity,
        result_kind=ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND,
        result_identity=assignment.material["movement_result_identity"],
        result_content=result_material,
        responsibility=ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        occurrence_boundary="assertion_locality_movement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        responsible_act_occurrence_coordinate="movement_act_occurrence_identity",
        coordinates_of_recorded_result={key: (key,) for key in result_material},
    )
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_KIND,
        {
            **_movement_result_material(assignment),
            "responsible_act_evidence_identity": act.identity,
            "evidence_of_yield_relation_identity": evidence.identity,
        },
        locality_identity=assignment.locality_identity,
    )


def _record_assertion_locality_movement_result_from_carried_act(
    ledger: EventLedger, *, act: Event, assignment: Event
) -> Event:
    if (
        ledger.get(act.identity) != act
        or act.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND
        or ledger.integrity_of(act.identity) == CORRUPTED
        or act.locality_identity != assignment.locality_identity
        or act.material != _movement_act_material(assignment)
        or ledger.append_boundary_through_occurrence(act.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "Assertion movement result requires its exact carried Act at the append tip"
        )
    return _append_assertion_locality_movement_result(
        ledger, act=act, assignment=assignment
    )


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
    if source_event.locality_identity == destination_locality:
        return source
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    assignment = record_assertion_locality_movement_responsibility_assignment(
        ledger,
        source=source,
        destination_locality=destination_locality,
        source_locality_standing=read_operator_locality_standing(
            ledger, locality_identity=source_event.locality_identity
        ),
        destination_locality_standing=read_operator_locality_standing(
            ledger, locality_identity=destination_locality
        ),
    )
    act = record_assertion_locality_movement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=destination_locality
        ),
    )
    movement = record_assertion_locality_movement_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    exact = _validate_moved_byte_assertion(ledger, movement.identity)
    if exact is None:
        raise ByteMeasurementError("Assertion locality movement is absent")
    return exact


def move_recorded_byte_assertion_to_locality(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    destination_locality: str,
) -> RecordedByteAssertion:
    return _move_byte_assertion_to_locality(
        ledger,
        source=source,
        destination_locality=destination_locality,
    )


def _record_movement_assignment_from_carried_standings(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    source_event: Event,
    source_standing: dict[str, Any],
    destination_locality: str,
    destination_standing: dict[str, Any],
) -> Event:
    source_boundary = source_standing.get("through_event_occurrence_identity")
    destination_boundary = destination_standing.get(
        "through_event_occurrence_identity"
    )
    if (
        source_standing.get("locality_identity") != source_event.locality_identity
        or type(source_boundary) is not str
        or not source_boundary
        or source_standing.get("measurement_occurrences", {}).get(
            source_event.identity
        )
        != _source_measurement_standing_coordinates(source_event)
        or destination_standing.get("locality_identity") != destination_locality
        or (
            destination_boundary is not None
            and (
                type(destination_boundary) is not str
                or not destination_boundary
                or ledger.append_boundary_through_occurrence(destination_boundary)
                != ledger.append_boundary()
            )
        )
    ):
        raise ByteMeasurementError(
            "Assertion movement assignment requires exact carried source and destination Standing"
        )
    identities = {
        "assignment_identity": new_identity(
            "assertion_locality_movement_assignment"
        ),
        "assignment_subject_identity": new_identity(
            "assertion_locality_movement_assignment_subject"
        ),
        "movement_act_identity": new_identity("assertion_locality_movement_act"),
        "movement_act_occurrence_identity": new_identity(
            "assertion_locality_movement_occurrence"
        ),
        "movement_result_identity": new_identity(
            "assertion_locality_movement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError("Assertion movement lifecycle identities collapsed")
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND,
        _movement_assignment_material(
            source=source,
            source_locality=source_event.locality_identity,
            destination_locality=destination_locality,
            source_standing_boundary_identity=source_boundary,
            destination_standing_boundary_identity=destination_boundary,
            **identities,
        ),
        locality_identity=destination_locality,
    )


def move_recorded_byte_assertions_to_locality(
    ledger: EventLedger,
    *,
    sources: tuple[RecordedByteAssertion, ...],
    destination_locality: str,
) -> tuple[RecordedByteAssertion, ...]:
    """Move one exact result's Assertions in one bounded same-call lifecycle."""

    if not sources:
        return ()
    source_event_identity = sources[0].recorded_occurrence_identity
    if any(
        source.recorded_occurrence_identity != source_event_identity
        for source in sources
    ):
        raise ByteMeasurementError(
            "bounded Assertion movement requires one exact source result"
        )
    source_event = ledger.get(source_event_identity)
    if source_event is None or source_event.locality_identity is None:
        raise ByteMeasurementError("Assertion locality movement requires its source")
    if source_event.locality_identity == destination_locality:
        return sources
    exact_sources = {
        source.assertion_identity: source
        for source in assertions_of_recorded_byte_measurement(
            ledger, source_event_identity
        )
        or ()
    }
    if any(exact_sources.get(source.assertion_identity) != source for source in sources):
        raise ByteMeasurementError(
            "bounded Assertion movement requires each exact source Assertion"
        )
    from seed_runtime.operator_locality_standing import (
        advance_operator_locality_standing,
        read_operator_locality_standing,
    )

    source_standing = read_operator_locality_standing(
        ledger, locality_identity=source_event.locality_identity
    )
    _require_current_movement_source_standing(
        ledger, source_event=source_event, locality_standing=source_standing
    )
    destination_standing = read_operator_locality_standing(
        ledger, locality_identity=destination_locality
    )
    _require_current_movement_destination_standing(
        ledger,
        destination_locality=destination_locality,
        locality_standing=destination_standing,
    )
    moved = []
    for source in sources:
        assignment = _record_movement_assignment_from_carried_standings(
            ledger,
            source=source,
            source_event=source_event,
            source_standing=source_standing,
            destination_locality=destination_locality,
            destination_standing=destination_standing,
        )
        destination_standing = advance_operator_locality_standing(
            ledger,
            (assignment.identity,),
            locality_identity=destination_locality,
            prior=destination_standing,
        )
        act = _record_assertion_locality_movement_act_from_carried_standing(
            ledger,
            assignment=assignment,
            destination_standing=destination_standing,
        )
        destination_standing = advance_operator_locality_standing(
            ledger,
            (act.identity,),
            locality_identity=destination_locality,
            prior=destination_standing,
        )
        movement = _record_assertion_locality_movement_result_from_carried_act(
            ledger, act=act, assignment=assignment
        )
        destination_standing = advance_operator_locality_standing(
            ledger,
            (
                movement.material["evidence_of_yield_relation_identity"],
                movement.identity,
            ),
            locality_identity=destination_locality,
            prior=destination_standing,
        )
        exact = _validate_moved_byte_assertion(
            ledger,
            movement.identity,
            prior_destination_standing=destination_standing,
        )
        if exact is None:
            raise ByteMeasurementError("Assertion locality movement is absent")
        moved.append(exact)
    return tuple(moved)


def _validate_moved_byte_assertion(
    ledger: EventLedger,
    movement_event_identity: str,
    *,
    prior_destination_standing: dict[str, Any] | None = None,
) -> RecordedByteAssertion | None:
    movement = ledger.get(movement_event_identity)
    if movement is None or movement.kind != ASSERTION_LOCALITY_MOVEMENT_KIND:
        return None
    if ledger.integrity_of(movement.identity) == CORRUPTED:
        raise ByteMeasurementError("Assertion locality movement is corrupted")
    act_evidence, assignment, source = (
        _read_assertion_locality_movement_act_evidence(
            ledger,
            movement.material.get("responsible_act_evidence_identity"),
            prior_destination_standing=prior_destination_standing,
        )
    )
    if (
        movement.locality_identity != assignment.locality_identity
        or movement.material.get("responsibility_assignment_reference")
        != _movement_assignment_reference(assignment)
    ):
        raise ByteMeasurementError(
            "Assertion locality movement carries no exact assignment"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=movement.identity,
        evidence_of_yield_relation_event_identity=movement.material.get("evidence_of_yield_relation_identity"),
        responsible_act_evidence_event_identity=movement.material.get(
            "responsible_act_evidence_identity"
        ),
        recorded_result_occurrence_coordinate="movement_act_occurrence_identity",
        responsible_act_occurrence_coordinate="movement_act_occurrence_identity",
    )
    yield_evidence = ledger.get(
        movement.material.get("evidence_of_yield_relation_identity")
    )
    if (
        not all(requirements.values())
        or yield_evidence is None
        or yield_evidence.material.get("result_kind")
        != ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND
        or yield_evidence.material.get("occurrence_boundary")
        != "assertion_locality_movement"
    ):
        raise ByteMeasurementError("Assertion movement Evidence of Yield relation is not exact")
    expected = {
        **_movement_result_material(assignment),
        "responsible_act_evidence_identity": act_evidence.identity,
        "evidence_of_yield_relation_identity": movement.material.get(
            "evidence_of_yield_relation_identity"
        ),
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


def _measure_byte_position_pair_counts_through(
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
                    "corrupted ingest cannot participate in byte-position-pair Measurement"
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
        for pair in totals
    )
    return MeasuredBytePairInputs(
        source_localities=localities,
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
        "source_localities": list(measured.source_localities),
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
                "source_provenance": (
                    "complete declared Ingest through one boundary"
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
                "occurrence_references": [
                    item["ingest_occurrence_identity"]
                    for item in measured.source_material
                ],
                "local_assertion_references": [],
            },
            "conflicts": "Unknown",
            "unknown": ["what the exact source bytes represent remains Unknown"],
            "limits": [
                "exact source-material set bounded by source occurrences and "
                "completeness boundary"
            ],
        }
    ]

    def assertion(
        *,
        result: str,
        item: MeasuredByteCount,
        content: dict[str, Any],
        provenance: str,
        local_support_references: list[str],
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
                "occurrence_references": [],
                "local_assertion_references": local_support_references,
            },
            "conflicts": "Unknown",
            "unknown": ["what this byte participates in or represents remains Unknown"],
            "limits": [
                "exact byte count or recurrence bounded by source occurrences and "
                "Measurement rule"
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
            local_support_references=[source_identity],
        )
        results.append(count)
        if item.count > 1:
            results.append(
                assertion(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    provenance="the exact count Assertion carried here",
                    local_support_references=[count["dimensions"]["identity"]],
                )
            )
    return results


def _byte_measurement_source_material(
    ledger: EventLedger,
    *,
    localities: tuple[str, ...],
    boundary: EventLedgerBoundary,
) -> tuple[dict[str, str], ...]:
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
    source_material = []
    seen_material = set()
    for locality in localities:
        for ingest in ledger.iter_locality_kind(
            locality, INGEST_OCCURRED_KIND, through=boundary
        ):
            _ingested_bytes(ledger, ingest)
            if ingest.identity in seen_material:
                raise ByteMeasurementError(
                    "one Ingest occurrence cannot enter a byte Measurement twice"
                )
            seen_material.add(ingest.identity)
            source_material.append(
                {"ingest_occurrence_identity": ingest.identity}
            )
    if not source_material:
        raise ByteMeasurementError(
            "declared source Localities contain no ingest through the Measurement boundary"
        )
    return tuple(source_material)


def _byte_measurement_assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
    }


def _byte_measurement_assignment_material(
    *,
    source_localities: tuple[str, ...],
    source_material: tuple[dict[str, str], ...],
    completeness_boundary_identity: str,
    standing_boundary_identity: str | None,
    assignment_identity: str,
    assignment_subject_identity: str,
    measurement_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "measurement_act_identity": measurement_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "measurement_rule": BYTE_MEASUREMENT_RULE,
        "source_localities": list(source_localities),
        "source_occurrence_references": [
            dict(reference) for reference in source_material
        ],
        "completeness_boundary_identity": completeness_boundary_identity,
        "standing_boundary_identity": standing_boundary_identity,
        "scope": {
            "recording_standing_boundary_identity": standing_boundary_identity,
            "source_localities": list(source_localities),
            "completeness_boundary_identity": completeness_boundary_identity,
        },
        "authority": "unestablished",
        "limits": [
            "assignment is bounded to the exact declared source Localities, "
            "Ingest occurrences, and completeness boundary"
        ],
        "unknown": ["what the exact source material represents remains Unknown"],
    }


def _require_current_byte_measurement_standing(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    locality_standing: dict[str, Any],
    required_assignment_identity: str | None = None,
) -> str | None:
    if type(locality_standing) is not dict:
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality Standing"
        )
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    current = read_operator_locality_standing(
        ledger, locality_identity=recording_locality_identity
    )
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    boundary = locality_standing.get("through_event_occurrence_identity")
    if (
        locality_standing != current
        or locality_standing.get("locality_identity")
        != recording_locality_identity
        or (boundary is not None and (type(boundary) is not str or not boundary))
        or (
            required_assignment_identity is not None
            and (
                type(assignments) is not dict
                or assignments.get(required_assignment_identity, object())
                is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality Standing"
        )
    return boundary


def _require_carried_byte_measurement_standing_at_tip(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    locality_standing: dict[str, Any],
    required_assignment_identity: str | None = None,
) -> str:
    if type(locality_standing) is not dict:
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality Standing"
        )
    boundary = locality_standing.get("through_event_occurrence_identity")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    if (
        locality_standing.get("locality_identity")
        != recording_locality_identity
        or type(boundary) is not str
        or not boundary
        or (
            required_assignment_identity is not None
            and (
                type(assignments) is not dict
                or assignments.get(required_assignment_identity, object())
                is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality Standing"
        )
    event = ledger.get(boundary)
    if (
        event is None
        or event.locality_identity != recording_locality_identity
        or ledger.integrity_of(boundary) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality Standing"
        )
    return boundary


def _prepare_byte_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
    recording_locality_identity: str,
) -> tuple[tuple[str, ...], EventLedgerBoundary, tuple[dict[str, str], ...]]:
    if (
        type(recording_locality_identity) is not str
        or not recording_locality_identity
    ):
        raise ByteMeasurementError(
            "byte Measurement recording requires an exact Locality"
        )
    localities = tuple(dict.fromkeys(source_localities))
    if (
        not localities
        or any(type(locality) is not str or not locality for locality in localities)
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact declared source Localities"
        )
    boundary = ledger.append_boundary()
    source_material = _byte_measurement_source_material(
        ledger, localities=localities, boundary=boundary
    )
    return localities, boundary, source_material


def _append_byte_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_localities: tuple[str, ...],
    source_material: tuple[dict[str, str], ...],
    completeness_boundary_identity: str,
    standing_boundary_identity: str | None,
    recording_locality_identity: str,
) -> Event:
    identities = {
        "assignment_identity": new_identity("byte_measurement_assignment"),
        "assignment_subject_identity": new_identity(
            "byte_measurement_assignment_subject"
        ),
        "measurement_act_identity": new_identity("byte_measurement_act"),
        "act_occurrence_identity": new_identity("byte_measurement_occurrence"),
        "measurement_result_identity": new_identity("byte_measurement_result"),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError(
            "byte Measurement lifecycle identities collapsed"
        )
    return ledger.append(
        BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _byte_measurement_assignment_material(
            source_localities=source_localities,
            source_material=source_material,
            completeness_boundary_identity=completeness_boundary_identity,
            standing_boundary_identity=standing_boundary_identity,
            **identities,
        ),
        locality_identity=recording_locality_identity,
    )


def record_byte_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
    recording_locality_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Record one exact-byte Measurement Responsibility assignment."""

    localities, boundary, source_material = (
        _prepare_byte_measurement_responsibility_assignment(
            ledger,
            source_localities=source_localities,
            recording_locality_identity=recording_locality_identity,
        )
    )
    standing_boundary_identity = _require_current_byte_measurement_standing(
        ledger,
        recording_locality_identity=recording_locality_identity,
        locality_standing=locality_standing,
    )
    return _append_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=localities,
        source_material=source_material,
        completeness_boundary_identity=boundary.identity,
        standing_boundary_identity=standing_boundary_identity,
        recording_locality_identity=recording_locality_identity,
    )


def _record_byte_measurement_responsibility_assignment_from_carried_standing(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
    recording_locality_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    localities, boundary, source_material = (
        _prepare_byte_measurement_responsibility_assignment(
            ledger,
            source_localities=source_localities,
            recording_locality_identity=recording_locality_identity,
        )
    )
    standing_boundary_identity = (
        _require_carried_byte_measurement_standing_at_tip(
            ledger,
            recording_locality_identity=recording_locality_identity,
            locality_standing=locality_standing,
        )
    )
    return _append_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=localities,
        source_material=source_material,
        completeness_boundary_identity=boundary.identity,
        standing_boundary_identity=standing_boundary_identity,
        recording_locality_identity=recording_locality_identity,
    )


def _read_byte_measurement_responsibility_assignment(
    ledger: EventLedger,
    assignment_event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, tuple[str, ...], EventLedgerBoundary, tuple[dict[str, str], ...]]:
    if type(assignment_event_identity) is not str or not assignment_event_identity:
        raise ByteMeasurementError(
            "byte Measurement requires one exact Responsibility assignment"
        )
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind
        != BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or type(assignment.locality_identity) is not str
        or not assignment.locality_identity
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement Responsibility assignment is absent or corrupted"
        )
    material = assignment.material
    identities = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "assignment_identity",
            "assignment_subject_identity",
            "measurement_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    localities_value = material.get("source_localities")
    completeness_boundary_identity = material.get(
        "completeness_boundary_identity"
    )
    standing_boundary_identity = material.get("standing_boundary_identity")
    if (
        any(type(identity) is not str or not identity for identity in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(localities_value) is not list
        or not localities_value
        or any(type(locality) is not str or not locality for locality in localities_value)
        or len(set(localities_value)) != len(localities_value)
        or type(completeness_boundary_identity) is not str
        or not completeness_boundary_identity
        or (
            standing_boundary_identity is not None
            and (
                type(standing_boundary_identity) is not str
                or not standing_boundary_identity
            )
        )
    ):
        raise ByteMeasurementError(
            "byte Measurement Responsibility assignment carries malformed coordinates"
        )
    localities = tuple(localities_value)
    boundary = EventLedgerBoundary(completeness_boundary_identity)
    source_material = _byte_measurement_source_material(
        ledger, localities=localities, boundary=boundary
    )
    expected = _byte_measurement_assignment_material(
        source_localities=localities,
        source_material=source_material,
        completeness_boundary_identity=completeness_boundary_identity,
        standing_boundary_identity=standing_boundary_identity,
        **identities,
    )
    if material != expected:
        raise ByteMeasurementError(
            "byte Measurement Responsibility assignment coordinates are not exact"
        )
    if prior_standing is None:
        from seed_runtime.operator_locality_standing import (
            _operator_standing_validation_context,
            read_operator_locality_standing_through,
        )

        prior_standing = _operator_standing_validation_context(
            ledger, locality_identity=assignment.locality_identity
        )
        if prior_standing is None:
            try:
                prior_standing = read_operator_locality_standing_through(
                    ledger,
                    locality_identity=assignment.locality_identity,
                    through_event_occurrence_identity=standing_boundary_identity,
                )
            except (TypeError, ValueError) as error:
                raise ByteMeasurementError(
                    "byte Measurement Responsibility assignment has no exact prior Standing"
                ) from error
    carried_assignments = prior_standing.get(
        "responsibility_assignment_occurrences"
    )
    prior_boundary_identity = prior_standing.get(
        "through_event_occurrence_identity"
    )
    boundary_is_exact = prior_boundary_identity == standing_boundary_identity
    assignment_is_carried_later = bool(
        type(prior_boundary_identity) is str
        and prior_boundary_identity
        and type(carried_assignments) is dict
        and carried_assignments.get(assignment.identity, object()) is None
    )
    if (
        prior_standing.get("locality_identity") != assignment.locality_identity
        or not (boundary_is_exact or assignment_is_carried_later)
    ):
        raise ByteMeasurementError(
            "byte Measurement Responsibility assignment has no exact prior Standing"
        )
    if boundary_is_exact:
        order = (assignment.identity,)
        if standing_boundary_identity is not None:
            order = (standing_boundary_identity, assignment.identity)
    elif prior_boundary_identity == assignment.identity:
        order = (assignment.identity,)
    else:
        order = (assignment.identity, prior_boundary_identity)
        if standing_boundary_identity is not None:
            order = (
                standing_boundary_identity,
                assignment.identity,
                prior_boundary_identity,
            )
    try:
        ledger.occurrences_in_append_order(
            order, locality_identity=assignment.locality_identity
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "byte Measurement Responsibility assignment order is false"
        ) from error
    return assignment, localities, boundary, source_material


def get_byte_measurement_responsibility_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> Event:
    return _read_byte_measurement_responsibility_assignment(
        ledger, assignment_event_identity
    )[0]


def _byte_measurement_act_evidence_material(
    assignment: Event,
) -> dict[str, Any]:
    return {
        "downstream_act_identity": assignment.material[
            "measurement_act_identity"
        ],
        "act_occurrence_identity": assignment.material[
            "act_occurrence_identity"
        ],
        "act": "declared exact-byte Measurement",
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": (
            _byte_measurement_assignment_reference(assignment)
        ),
        "source_localities": list(assignment.material["source_localities"]),
        "authority": "unestablished",
        "evidence_scope": (
            "Evidence bounded to this exact responsible Measurement "
            "occurrence; establishes no responsibility"
        ),
    }


def _append_byte_measurement_responsible_act_evidence(
    ledger: EventLedger,
    *,
    assignment: Event,
) -> Event:
    for prior_act in ledger.iter_locality_kind(
        assignment.locality_identity,
        BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
    ):
        if (
            prior_act.material.get("responsibility_assignment_reference")
            == _byte_measurement_assignment_reference(assignment)
            or prior_act.material.get("act_occurrence_identity")
            == assignment.material["act_occurrence_identity"]
        ):
            raise ByteMeasurementError(
                "byte Measurement Responsibility assignment already carries an Act"
            )
    return ledger.append(
        BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
        _byte_measurement_act_evidence_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def record_byte_measurement_responsible_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    """Record Evidence for one exact assigned byte Measurement Act."""

    assignment, _localities, _boundary, _source_material = (
        _read_byte_measurement_responsibility_assignment(
            ledger, responsibility_assignment_event_identity
        )
    )
    _require_current_byte_measurement_standing(
        ledger,
        recording_locality_identity=assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        required_assignment_identity=assignment.identity,
    )
    return _append_byte_measurement_responsible_act_evidence(
        ledger,
        assignment=assignment,
    )


def _record_byte_measurement_responsible_act_evidence_from_carried_standing(
    ledger: EventLedger,
    *,
    responsibility_assignment: Event,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    if (
        type(responsibility_assignment) is not Event
        or responsibility_assignment.kind
        != BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or ledger.integrity_of(responsibility_assignment.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement requires its exact carried assignment"
        )
    exact_assignment, _localities, _boundary, _source_material = (
        _read_byte_measurement_responsibility_assignment(
            ledger,
            responsibility_assignment.identity,
            prior_standing=responsibility_assignment_standing,
        )
    )
    if exact_assignment != responsibility_assignment:
        raise ByteMeasurementError(
            "byte Measurement requires its exact carried assignment"
        )
    _require_carried_byte_measurement_standing_at_tip(
        ledger,
        recording_locality_identity=responsibility_assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        required_assignment_identity=responsibility_assignment.identity,
    )
    return _append_byte_measurement_responsible_act_evidence(
        ledger,
        assignment=responsibility_assignment,
    )


def _measurement_of_responsible_act_evidence(
    ledger: EventLedger,
    responsible_act_evidence_event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Any, Event, MeasuredByteInputs]:
    event = ledger.get(responsible_act_evidence_event_identity)
    if (
        event is None
        or event.kind != BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement Yield requires one exact responsible Act Evidence occurrence"
        )
    material = event.material
    assignment_reference = material.get("responsibility_assignment_reference")
    if (
        type(assignment_reference) is not dict
        or set(assignment_reference)
        != {
            "recorded_occurrence_identity",
            "assignment_identity",
            "assignment_subject_identity",
        }
        or type(event.locality_identity) is not str
        or not event.locality_identity
    ):
        raise ByteMeasurementError(
            "byte Measurement responsible Act Evidence carries malformed coordinates"
        )
    assignment, localities, boundary, _source_material = (
        _read_byte_measurement_responsibility_assignment(
            ledger,
            assignment_reference.get("recorded_occurrence_identity"),
            prior_standing=prior_standing,
        )
    )
    measured = _measure_byte_counts_through(
        ledger,
        localities=localities,
        boundary=boundary,
    )
    expected = _byte_measurement_act_evidence_material(assignment)
    if (
        assignment_reference
        != _byte_measurement_assignment_reference(assignment)
        or event.locality_identity != assignment.locality_identity
        or material != expected
    ):
        raise ByteMeasurementError(
            "byte Measurement responsible Act Evidence is not exact"
        )
    return event, assignment, measured


def _require_byte_measurement_act_without_result(
    ledger: EventLedger, act_evidence: Event
) -> None:
    for kind in (
        RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
        BYTE_MEASUREMENT_RECORDED_KIND,
    ):
        for event in ledger.iter_locality_kind(act_evidence.locality_identity, kind):
            if (
                event.material.get("responsible_act_evidence_identity")
                == act_evidence.identity
            ):
                raise ByteMeasurementError(
                    "byte Measurement responsible Act occurrence already has a Yield or result"
                )


def _record_byte_measurement_result_from_exact_inputs(
    ledger: EventLedger,
    *,
    responsible_act_evidence: Event,
    assignment: Event,
    measured: MeasuredByteInputs,
) -> Event:
    result_identity = assignment.material["measurement_result_identity"]
    result_material = {
        "result_identity": result_identity,
        "dimensions": {
                "identity": "byte-count-measurement-occurrence",
                "content": (
                    "exact source-material-set, byte count, and recurrence Assertions"
                ),
                "source_provenance": "complete declared Ingest through one boundary",
                "authority": "unestablished",
                "evidence_scope": MEASUREMENT_EVIDENCE_SCOPE,
        },
        "exact_act": "declared exact-byte Measurement",
        "downstream_act_identity": responsible_act_evidence.material[
            "downstream_act_identity"
        ],
        "act_occurrence_identity": responsible_act_evidence.material[
            "act_occurrence_identity"
        ],
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": (
            _byte_measurement_assignment_reference(assignment)
        ),
        "measurement_rule": BYTE_MEASUREMENT_RULE,
        "source_localities": list(measured.source_localities),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
        "assertions": _assertions(measured),
    }
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=responsible_act_evidence.locality_identity,
        exact_act="declared exact-byte Measurement",
        act_occurrence_identity=responsible_act_evidence.material[
            "act_occurrence_identity"
        ],
        responsible_act_evidence_identity=responsible_act_evidence.identity,
        result_kind=BYTE_MEASUREMENT_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=BYTE_MEASUREMENT_RESPONSIBILITY,
        occurrence_boundary="byte_measurement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        BYTE_MEASUREMENT_RECORDED_KIND,
        {
            **result_material,
            "evidence_of_yield_relation_identity": evidence.identity,
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "occurrence_preservation": BYTE_OCCURRENCE_PRESERVATION,
        },
        locality_identity=responsible_act_evidence.locality_identity,
    )


def record_byte_measurement_result(
    ledger: EventLedger,
    *,
    responsible_act_evidence_event_identity: str,
):
    """Record the Yield and result of one exact evidenced byte Measurement Act."""

    supplied = ledger.get(responsible_act_evidence_event_identity)
    if (
        supplied is None
        or supplied.kind != BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
        or ledger.integrity_of(supplied.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement Yield requires one exact responsible Act Evidence occurrence"
        )
    _require_byte_measurement_act_without_result(ledger, supplied)

    responsible_act_evidence, assignment, measured = (
        _measurement_of_responsible_act_evidence(
            ledger, supplied.identity
        )
    )

    return _record_byte_measurement_result_from_exact_inputs(
        ledger,
        responsible_act_evidence=responsible_act_evidence,
        assignment=assignment,
        measured=measured,
    )


def _record_byte_measurement_result_from_carried_act_evidence(
    ledger: EventLedger,
    *,
    responsible_act_evidence: Event,
    responsibility_assignment: Event,
    locality_standing: dict[str, Any],
) -> Event:
    if (
        type(responsible_act_evidence) is not Event
        or type(responsibility_assignment) is not Event
        or ledger.get(responsible_act_evidence.identity)
        != responsible_act_evidence
        or responsible_act_evidence.kind
        != BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
        or ledger.integrity_of(responsible_act_evidence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(
            responsible_act_evidence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires exact carried lifecycle occurrences"
        )
    exact_act, exact_assignment, measured = (
        _measurement_of_responsible_act_evidence(
            ledger,
            responsible_act_evidence.identity,
            prior_standing=locality_standing,
        )
    )
    if (
        exact_act != responsible_act_evidence
        or exact_assignment != responsibility_assignment
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires exact carried lifecycle occurrences"
        )
    if (
        ledger.get(responsible_act_evidence.identity) != responsible_act_evidence
        or ledger.integrity_of(responsible_act_evidence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(
            responsible_act_evidence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires its exact Act at the append tip"
        )
    return _record_byte_measurement_result_from_exact_inputs(
        ledger,
        responsible_act_evidence=responsible_act_evidence,
        assignment=responsibility_assignment,
        measured=measured,
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
        raise ByteMeasurementError("a corrupted occurrence cannot return byte results")
    material = event.material
    if set(material) != BYTE_RESULT_COORDINATES | {
        "evidence_of_yield_relation_identity",
        "responsible_act_evidence_identity",
        "occurrence_preservation",
    }:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact byte result and recording surfaces"
        )
    if (
        material.get("occurrence_preservation") != BYTE_OCCURRENCE_PRESERVATION
        or material.get("exact_act") != "declared exact-byte Measurement"
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
                    "exact source-material-set, byte count, and recurrence Assertions"
                ),
            "source_provenance": (
                "complete declared Ingest through one boundary"
            ),
            "authority": "unestablished",
            "evidence_scope": MEASUREMENT_EVIDENCE_SCOPE,
        }
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not preserve its exact Measurement and "
            "recording-occurrence Evidence"
        )
    evidence_identity = material.get("evidence_of_yield_relation_identity")
    evidence = ledger.get(evidence_identity) if isinstance(evidence_identity, str) else None
    if (
        evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind")
        != BYTE_MEASUREMENT_RESULT_KIND
        or evidence.material.get("coordinates_of_carried_result")
        != [coordinate for coordinate in material if coordinate in BYTE_RESULT_COORDINATES]
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
        "responsibility_assignment_reference": material[
            "responsibility_assignment_reference"
        ],
        "source_localities": material["source_localities"],
        "authority": "unestablished",
        "evidence_scope": (
            "Evidence bounded to this exact responsible Measurement "
            "occurrence; establishes no responsibility"
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
    _validated_act, assignment, measured = (
        _measurement_of_responsible_act_evidence(
            ledger, act_evidence.identity
        )
    )
    _require_exact_result_yield(
        ledger,
        event,
        evidence,
        act_evidence,
        result_name="byte Measurement",
    )
    boundary_value = material.get("completeness_boundary")
    localities_value = material.get("source_localities")
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
    if (
        material.get("responsibility_assignment_reference")
        != _byte_measurement_assignment_reference(assignment)
        or measured.completeness_boundary.identity != boundary_value["identity"]
        or list(measured.source_localities) != localities_value
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
        local_identities = assertion["input_support"]["local_assertion_references"]
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
        "source_localities": list(measured.source_localities),
    }
    results: list[dict[str, Any]] = []

    def assertion(
        *,
        result: str,
        item: MeasuredBytePairCount,
        content: dict[str, Any],
        provenance: str,
        local_support_references: list[str],
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
                "local_assertion_references": local_support_references,
            },
            "conflicts": "Unknown",
            "unknown": list(BYTE_PAIR_UNKNOWN),
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
            local_support_references=[],
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
                    local_support_references=[count["dimensions"]["identity"]],
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
            "act": "declared byte-position-pair Measurement",
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
                "Evidence bounded to this exact responsible Measurement "
                "occurrence; establishes no responsibility or authority "
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
    result_identity = new_identity("byte_pair_applicability_result")
    result_material = {
        "result_identity": result_identity,
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
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=recording_locality_identity,
        exact_act="input Applicability determination",
        act_occurrence_identity=applicability_assertion["applicability_act_occurrence_identity"],
        responsible_act_evidence_identity=applicability_act_evidence.identity,
        result_kind=BYTE_PAIR_APPLICABILITY_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        occurrence_boundary="byte_pair_applicability",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        responsible_act_occurrence_coordinate="applicability_act_occurrence_identity",
    )
    return ledger.append(
        BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
        {
            **result_material,
            "evidence_of_yield_relation_identity": evidence.identity,
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
    evidence_identity = material.get("evidence_of_yield_relation_identity")
    evidence = ledger.get(evidence_identity) if isinstance(evidence_identity, str) else None
    if set(material) != BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES | {
        "evidence_of_yield_relation_identity",
        "responsible_act_evidence_identity",
    }:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact Applicability result surface"
        )
    result_coordinates = {
        key: value
        for key, value in material.items()
        if key in BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES
    }
    if (
        evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind")
        != BYTE_PAIR_APPLICABILITY_RESULT_KIND
        or evidence.material.get("coordinates_of_carried_result") != list(result_coordinates)
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
    _require_exact_result_yield(
        ledger,
        event,
        evidence,
        act_evidence,
        result_name="Applicability",
        occurrence_coordinate="applicability_act_occurrence_identity",
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
        or applicability_assertion.get("downstream_act") != "declared byte-position-pair Measurement"
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
    ):
        raise ByteMeasurementError(f"{event_identity} carries incoherent Applicability")
    source_reference = material.get("input_assertion_reference")
    movement_event_identity = material.get("input_movement_event_identity")
    if (
        type(source_reference) is not dict
        or set(source_reference)
        != {"recorded_occurrence_identity", "assertion_identity"}
    ):
        raise ByteMeasurementError(
            f"{event_identity} carries no exact input Standing reference"
        )
    if movement_event_identity is None:
        readings = assertions_of_recorded_byte_measurement(
            ledger, source_reference.get("recorded_occurrence_identity")
        )
        source = next(
            (
                reading
                for reading in readings or ()
                if reading.assertion_identity
                == source_reference.get("assertion_identity")
            ),
            None,
        )
    elif type(movement_event_identity) is str and movement_event_identity:
        source = _validate_moved_byte_assertion(ledger, movement_event_identity)
    else:
        source = None
    if source is None or source.reference != source_reference:
        raise ByteMeasurementError(
            f"{event_identity} carries no exact input Standing occurrence"
        )
    _validate_recorded_pair_input_applicability(
        ledger,
        applicability_assertion,
        source=source,
        event=event,
        downstream_act_identity=material.get("downstream_act_identity"),
    )
    return json.loads(_canonical(applicability_assertion))


def record_byte_position_pair_count_layer(
    ledger: EventLedger,
    *,
    source_measurement_event_identity: str,
    recording_locality_identity: str,
):
    """Record exact byte-position-pair counts without crossing append boundaries."""

    if not isinstance(recording_locality_identity, str) or not recording_locality_identity:
        raise ByteMeasurementError(
            "byte-position-pair Measurement recording requires an exact Locality"
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
        ledger,
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
    act_occurrence_identity = new_identity("byte_position_pair_measurement_occurrence")
    measured = _measure_byte_position_pair_counts_through(
        ledger,
        localities=tuple(scope["source_localities"]),
        boundary=EventLedgerBoundary(content["completeness_boundary"]["identity"]),
        source_assertion_reference=source.reference,
        source_movement_event_identity=source.locality_movement_event_identity,
        input_applicability=applicability,
        downstream_act_identity=downstream_act_identity,
        act_occurrence_identity=act_occurrence_identity,
    )
    result_identity = new_identity("byte_position_pair_measurement_result")
    result_material = {
        "result_identity": result_identity,
        "dimensions": {
            "identity": "byte-position-pair-count-measurement-occurrence",
            "content": (
                "byte-position-pair count and recurrence Assertions"
            ),
            "source_provenance": "the recorded source-material-set Assertion",
            "authority": "unestablished",
            "evidence_scope": PAIR_MEASUREMENT_EVIDENCE_SCOPE,
        },
        "exact_act": "declared byte-position-pair Measurement",
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
        "source_localities": list(measured.source_localities),
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
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=recording_locality_identity,
        exact_act="declared byte-position-pair Measurement",
        act_occurrence_identity=measured.act_occurrence_identity,
        responsible_act_evidence_identity=responsible_act_evidence.identity,
        result_kind=BYTE_PAIR_MEASUREMENT_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        occurrence_boundary="byte_pair_measurement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        {
            **result_material,
            "evidence_of_yield_relation_identity": evidence.identity,
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "occurrence_preservation": BYTE_PAIR_OCCURRENCE_PRESERVATION,
        },
        locality_identity=recording_locality_identity,
    )


def _validate_recorded_pair_input_applicability(
    ledger: EventLedger,
    applicability_assertion: Any,
    *,
    source: RecordedByteAssertion,
    event,
    downstream_act_identity: str,
) -> None:
    """Validate historical Applicability without determining it again."""

    source, input_standing = _recorded_input_assertion_standing(
        ledger,
        source,
        measurement_locality_identity=event.locality_identity,
    )
    source_material = source.material
    scope = source_material["assertion_scope"]
    content = {
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "downstream_act_identity": downstream_act_identity,
        "downstream_act": "declared byte-position-pair Measurement",
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
        "downstream_act": "declared byte-position-pair Measurement",
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "measurement_locality": measurement_locality,
        "scope_locality": scope,
        "input_standing": input_standing,
        "input_authority": source_material["dimensions"]["authority"],
        "input_unknown": source_material["unknown"],
        "input_limits": source_material["limits"],
        "conflicts": [],
        "coordinate_treatment": {
            "support_relation_standing": {
                "carried": False,
                "treatment": "not established by Applicability",
            },
            "known_loss": {"carried": False, "treatment": "not represented by input"},
            "current_Standing": {
                "carried": False,
                "treatment": "not required for this historical bounded source material",
            },
            "negative_authority": {
                "carried": True,
                "value": source_material["limits"],
                "treatment": "preserved as limits on this exact use",
            },
        },
        "unknown": [
            "what any byte or byte position pair represents remains Unknown"
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


def _read_recorded_byte_position_pair_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    findings_only: bool,
) -> tuple[RecordedBytePairAssertion, ...] | tuple[_RecordedBytePairFinding, ...] | None:
    """Validate one exact pair result and return its requested reading surface."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(
            f"{event_identity} is not a byte-position-pair Measurement occurrence"
        )
    if ledger.integrity_of(event_identity) == CORRUPTED:
        raise ByteMeasurementError("a corrupted occurrence cannot return pair results")
    material = event.material
    exact_surface = BYTE_PAIR_RESULT_COORDINATES | {
        "evidence_of_yield_relation_identity",
        "responsible_act_evidence_identity",
        "occurrence_preservation",
    }
    if set(material) != exact_surface:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact pair result and recording surfaces"
        )
    expected_dimensions = {
        "identity": "byte-position-pair-count-measurement-occurrence",
        "content": (
            "byte-position-pair count and recurrence Assertions"
        ),
        "source_provenance": "the recorded source-material-set Assertion",
        "authority": "unestablished",
        "evidence_scope": PAIR_MEASUREMENT_EVIDENCE_SCOPE,
    }
    if (
        material.get("occurrence_preservation") != BYTE_PAIR_OCCURRENCE_PRESERVATION
        or material.get("exact_act") != "declared byte-position-pair Measurement"
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
    evidence_identity = material.get("evidence_of_yield_relation_identity")
    evidence = ledger.get(evidence_identity) if isinstance(evidence_identity, str) else None
    if (
        evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind")
        != BYTE_PAIR_MEASUREMENT_RESULT_KIND
        or evidence.material.get("coordinates_of_carried_result")
        != [
            coordinate
            for coordinate in material
            if coordinate in BYTE_PAIR_RESULT_COORDINATES
        ]
        or evidence.material.get("dimensions", {}).get("responsibility")
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or evidence.material.get("dimensions", {}).get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or evidence.material.get("dimensions", {}).get("act_occurrence_identity")
        != material["act_occurrence_identity"]
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact byte-position-pair yield Evidence"
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
        "act": "declared byte-position-pair Measurement",
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
            "Evidence bounded to this exact responsible Measurement "
            "occurrence; establishes no responsibility or authority "
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
    _require_exact_result_yield(
        ledger,
        event,
        evidence,
        act_evidence,
        result_name="byte-position-pair",
    )
    boundary_value = material.get("completeness_boundary")
    localities_value = material.get("source_localities")
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
            "exact Ingest and material occurrences through the recorded boundary"
        ),
    }
    if (
        localities_value != source_scope["source_localities"]
        or boundary_value != source_content["completeness_boundary"]
        or material.get("responsibility_assignment_evidence")
        != expected_assignment_evidence
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry its exact input source boundary"
        )
    _validate_recorded_pair_input_applicability(
        ledger,
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
        "source_localities": localities_value,
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
        "unknown",
        "limits",
    }
    canonical_scope = _canonical(expected_scope)
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
                    "source_provenance",
                    "responsibility",
                    "authority",
                    "evidence_scope",
                }
            or dimensions.get("responsibility") != MEASURED_ASSERTION_RESPONSIBILITY
            or dimensions.get("authority") != "unestablished"
            or dimensions.get("evidence_scope") != PAIR_MEASUREMENT_EVIDENCE_SCOPE
            or assertion.get("unknown") != list(BYTE_PAIR_UNKNOWN)
            or assertion.get("limits")
            != list(BYTE_PAIR_LIMITS)
        ):
            raise ByteMeasurementError(f"{event_identity} carries an unlawful pair Assertion")
        content = dimensions.get("content")
        fixed_content_shape = (
            result == "recurrence"
            and content == {"recurrence_established": True}
        ) or (
            result == "count"
            and type(content) is dict
            and set(content) == {"input_count", "occurrences_carrying", "count"}
            and all(type(value) is int for value in content.values())
        )
        expected_identity = (
            _pair_assertion_identity(
                result=result,
                representation=tuple(representation),
                canonical_scope=canonical_scope,
                content=content,
            )
            if fixed_content_shape
            else _identity(
                result=result,
                subject=subject,
                scope=expected_scope,
                content=content,
            )
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
            != {"assertion_references": [source_reference], "local_assertion_references": []}
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
                "local_assertion_references": [count["dimensions"]["identity"]],
            }
        ):
            raise ByteMeasurementError(f"{event_identity} carries unlawful recurrence support")
    validated_results = []
    for assertion in assertions:
        if findings_only:
            content = assertion["dimensions"]["content"]
            content_coordinates: tuple[int, int, int] | bool
            if assertion["result"] == "recurrence":
                content_coordinates = content["recurrence_established"]
            else:
                content_coordinates = (
                    content["input_count"],
                    content["occurrences_carrying"],
                    content["count"],
                )
            validated_results.append(
                _RecordedBytePairFinding(
                    assertion_identity=assertion["dimensions"]["identity"],
                    recorded_occurrence_identity=event.identity,
                    representation=tuple(
                        assertion["assertion_subject"]["representation"]
                    ),
                    result=assertion["result"],
                    _content_coordinates=content_coordinates,
                    _local_support_assertion_identities=tuple(
                        assertion["input_support"][
                            "local_assertion_references"
                        ]
                    ),
                )
            )
            continue
        support = assertion["input_support"]
        support_references = list(support["assertion_references"])
        support_references.extend(
            {
                "recorded_occurrence_identity": event.identity,
                "assertion_identity": local_identity,
            }
            for local_identity in support["local_assertion_references"]
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


def assertions_of_recorded_byte_position_pair_measurement(
    ledger: EventLedger, event_identity: str
) -> tuple[RecordedBytePairAssertion, ...] | None:
    """Read the exact pair result without performing Measurement again."""

    reading = _read_recorded_byte_position_pair_measurement(
        ledger, event_identity, findings_only=False
    )
    return reading


def _findings_of_recorded_byte_position_pair_measurement(
    ledger: EventLedger, event_identity: str
) -> tuple[_RecordedBytePairFinding, ...] | None:
    """Read only exact finding coordinates after the same full validation."""

    reading = _read_recorded_byte_position_pair_measurement(
        ledger, event_identity, findings_only=True
    )
    return reading


def byte_position_pair_measurement_occurrence_references(
    ledger: EventLedger, event_identity: str
) -> tuple[str, ...]:
    """Return the exact ordered Applicability and Measurement occurrences."""

    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, event_identity
    )
    if type(assertions) is not tuple:
        raise ByteMeasurementError("pair Measurement result is absent")
    result = ledger.get(event_identity)
    assert result is not None
    applicability_identity = result.material["input_applicability_event_identity"]
    applicability = ledger.get(applicability_identity)
    if applicability is None:
        raise ByteMeasurementError(
            "pair Measurement carries no exact Applicability result"
        )
    get_recorded_pair_input_applicability(ledger, applicability.identity)
    references = (
        applicability.material["responsible_act_evidence_identity"],
        applicability.material["evidence_of_yield_relation_identity"],
        applicability.identity,
        result.material["responsible_act_evidence_identity"],
        result.material["evidence_of_yield_relation_identity"],
        result.identity,
    )
    ordered = ledger.occurrences_in_append_order(
        references, locality_identity=result.locality_identity
    )
    if tuple(event.identity for event in ordered) != references:
        raise ByteMeasurementError(
            "pair Applicability and Measurement occurrences are not ordered"
        )
    return references


def input_applicability_of_recorded_byte_position_pair_measurement(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any] | None:
    """Validate the exact input-to-Act Applicability Assertion."""

    read = assertions_of_recorded_byte_position_pair_measurement(ledger, event_identity)
    if read is None:
        return None
    event = ledger.get(event_identity)
    return json.loads(_canonical(event.material["input_applicability"]))
