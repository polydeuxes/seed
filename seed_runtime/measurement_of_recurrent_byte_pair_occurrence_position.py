"""Measure where one yielded recurrent byte-pair subject occurs.

This is a declared Measurement result, not a Candidate, Admission, or Standing
movement.  Its inputs: two distinct occurrence references:

* the recurrence Assertion yielded by an earlier byte-pair Measurement; and
* one later exact material acquisition result in the same Locality.

Ordering and distance are views over the two measured positions.  The result
carries neither a caller-supplied sign nor a grammatical meaning.
"""

from __future__ import annotations

import hashlib
from typing import Any, NamedTuple

from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    _validated_recorded_byte_position_pair_measurement,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.identities import new_identity
from seed_runtime.material_acquisition import (
    acquired_material_bytes,
    read_exact_material_acquisition_result,
)
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)


RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND = (
    "operator.measurement_of_recurrent_byte_pair_occurrence_position."
    "recording_occurrence_of_result"
)
RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT = (
    "operator.measurement_of_recurrent_byte_pair_occurrence_position."
    "act_occurrence_recorded"
)
RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND = (
    "operator.measurement_of_recurrent_byte_pair_occurrence_position."
    "responsibility_assignment_recorded"
)
RESULT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KIND = (
    "result of exact Measurement of recurrent byte-pair occurrence position"
)
ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "declared Measurement of byte-pair occurrence position"
)
RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "Measurement of each exact ordered position for one exact byte pair "
    "in one exact material result"
)
RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "each ordered occurrence of the exact Yield-carried byte pair in one exact "
    "material acquisition result within one completeness boundary and occurrence count boundary"
)
SCOPE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "exact Yield-carried pair Assertion and exact later material acquisition result only"
)
MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_BOUNDARY = (
    "measurement_of_recurrent_byte_pair_occurrence_position"
)
RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_ASSERTION = (
    "preserve this measured Assertion's carried Standing coordinates"
)
RESULT_COORDINATES_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = frozenset(
    {
        "result_identity",
        "dimensions",
        "exact_act",
        "addressed_act_identity",
        "act_occurrence_identity",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_reference",
        "measurement_rule",
        "source_localities",
        "completeness_boundary",
        "pair_assertion_reference",
        "source_material_acquisition_occurrence_identity",
        "occurrence_count_boundary",
        "available_occurrence_count",
        "known_loss",
        "assertions",
    }
)
EVENT_KIND_RESPONSIBILITIES = {
    RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND: "01.Source.D",
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND: "01.Source.D",
    RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT: "02.Acts.A",
}


def _exact_measurement_occurrence_standing_coordinates(
    ledger: EventLedger, event_identity: str
) -> dict[str, str]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError(
            "pair occurrence assignment carries no intact pair Measurement"
        )
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
        "yield_relation_identity": event.material[
            "yield_relation_identity"
        ],
    }


def _exact_material_acquisition_result_availability_coordinates(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event = read_exact_material_acquisition_result(ledger, event_identity)
    dimensions = event.material["dimensions"]
    occurrence = {
        "subject_reference": dimensions["identity"],
        "result_occurrence_identity": event.identity,
        "source_role": event.material["source_role"],
    }
    return occurrence


class ReferenceToRecordedRecurrentBytePair(NamedTuple):
    """Exact address of one recurrence Assertion and its count support."""

    recorded_occurrence_identity: str
    recurrence_assertion_identity: str
    count_assertion_identity: str
    locality_identity: str
    source_occurrence_identities: tuple[str, ...]
    completeness_boundary_identity: str
    exact_material: bytes

    @property
    def assertion_reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.recurrence_assertion_identity,
        }


class FindingOfRecurrentBytePairOccurrencePositions(NamedTuple):
    """Bounded ordered position findings for one exact pair subject."""

    pair_reference: ReferenceToRecordedRecurrentBytePair
    source_material_acquisition_occurrence_identity: str
    source_locality_identity: str
    completeness_boundary: EventLedgerBoundary
    occurrence_count_boundary: int
    available_occurrence_count: int
    occurrences: tuple[tuple[int, int], ...]


class ReferenceToRecordedRecurrentBytePairOccurrencePosition(NamedTuple):
    """Immutable address of one exact yielded pair-position Assertion."""

    recorded_occurrence_identity: str
    assertion_identity: str
    pair_measurement_occurrence_identity: str
    recurrence_assertion_identity: str
    count_assertion_identity: str
    source_material_acquisition_occurrence_identity: str
    locality_identity: str
    completeness_boundary_identity: str
    exact_pair: bytes
    first_position: int
    second_position: int

    @property
    def assertion_reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.assertion_identity,
        }

def _validate_pair_reference(reference: ReferenceToRecordedRecurrentBytePair) -> None:
    if type(reference) is not ReferenceToRecordedRecurrentBytePair:
        raise TypeError("recurrent pair reference requires one exact reference")
    strings = (
        reference.recorded_occurrence_identity,
        reference.recurrence_assertion_identity,
        reference.count_assertion_identity,
        reference.locality_identity,
        reference.completeness_boundary_identity,
    )
    if any(type(value) is not str or not value for value in strings):
        raise ValueError("recurrent pair reference requires exact identities")
    if (
        type(reference.source_occurrence_identities) is not tuple
        or not reference.source_occurrence_identities
        or len(set(reference.source_occurrence_identities))
        != len(reference.source_occurrence_identities)
        or any(
            type(identity) is not str or not identity
            for identity in reference.source_occurrence_identities
        )
    ):
        raise ValueError("recurrent pair reference requires distinct source occurrences")
    if type(reference.exact_material) is not bytes or len(reference.exact_material) != 2:
        raise ValueError("recurrent pair reference requires exactly two bytes")


def _validate_finding(finding: FindingOfRecurrentBytePairOccurrencePositions) -> None:
    if type(finding) is not FindingOfRecurrentBytePairOccurrencePositions:
        raise TypeError("pair occurrence finding requires one exact finding")
    _validate_pair_reference(finding.pair_reference)
    if (
        type(finding.source_material_acquisition_occurrence_identity) is not str
        or not finding.source_material_acquisition_occurrence_identity
        or type(finding.source_locality_identity) is not str
        or not finding.source_locality_identity
        or not isinstance(finding.completeness_boundary, EventLedgerBoundary)
    ):
        raise ValueError("pair occurrence finding requires exact source coordinates")
    if type(finding.occurrence_count_boundary) is not int or finding.occurrence_count_boundary <= 0:
        raise ValueError("pair occurrence finding requires a positive exact count boundary")
    if (
        type(finding.available_occurrence_count) is not int
        or finding.available_occurrence_count < 0
        or finding.available_occurrence_count < len(finding.occurrences)
        or len(finding.occurrences) > finding.occurrence_count_boundary
    ):
        raise ValueError("pair occurrence finding carries an impossible count")
    if type(finding.occurrences) is not tuple:
        raise TypeError("pair occurrences require one exact tuple")
    seen = set()
    for occurrence in finding.occurrences:
        if (
            type(occurrence) is not tuple
            or len(occurrence) != 2
            or any(type(position) is not int or position < 0 for position in occurrence)
            or occurrence[0] == occurrence[1]
            or occurrence in seen
        ):
            raise ValueError("each pair occurrence requires two distinct positions")
        seen.add(occurrence)


def reference_to_recorded_recurrent_byte_pair(
    ledger: EventLedger,
    *,
    measurement_occurrence_identity: str,
    recurrence_assertion_identity: str,
) -> ReferenceToRecordedRecurrentBytePair:
    """Resolve one recurrence Assertion through its exact Measurement Yield."""

    return _references_to_recorded_recurrent_byte_pairs(
        ledger,
        measurement_occurrence_identity=measurement_occurrence_identity,
        recurrence_assertion_identities=(recurrence_assertion_identity,),
    )[0]


def _references_to_recorded_recurrent_byte_pairs(
    ledger: EventLedger,
    *,
    measurement_occurrence_identity: str,
    recurrence_assertion_identities: tuple[str, ...],
    prior_standing: dict[str, Any] | None = None,
) -> tuple[ReferenceToRecordedRecurrentBytePair, ...]:
    """Resolve several subjects from one independently validated result read."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recurrent pair reference requires one EventLedger")
    if (
        type(measurement_occurrence_identity) is not str
        or not measurement_occurrence_identity
        or type(recurrence_assertion_identities) is not tuple
        or not recurrence_assertion_identities
        or any(
            type(identity) is not str or not identity
            for identity in recurrence_assertion_identities
        )
    ):
        raise ValueError("recurrent pair reference requires exact occurrence identities")
    if len(set(recurrence_assertion_identities)) != len(
        recurrence_assertion_identities
    ):
        raise ValueError("recurrent pair Assertion entered one result twice")
    event = ledger.get(measurement_occurrence_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError("recurrent pair reference requires one intact pair Measurement")
    reading = (
        _validated_recorded_byte_position_pair_measurement(
            ledger,
            event.identity,
            findings_only=True,
            prior_standing=prior_standing,
        )
        if prior_standing is not None
        else _validated_recorded_byte_position_pair_measurement(
            ledger, event.identity, findings_only=True
        )
    )
    findings = reading.results if reading is not None else None
    findings_by_identity = {
        finding.assertion_identity: finding for finding in findings or ()
    }
    assignment = reading.assignment.material if reading is not None else None
    sources = (
        assignment.get("source_occurrence_references")
        if isinstance(assignment, dict)
        else None
    )
    boundary = event.material.get("completeness_boundary")
    if (
        type(sources) is not list
        or not sources
        or any(
            type(reference) is not dict
            or set(reference) != {"material_acquisition_occurrence_identity"}
            or type(reference["material_acquisition_occurrence_identity"]) is not str
            or not reference["material_acquisition_occurrence_identity"]
            for reference in sources
        )
        or type(boundary) is not dict
        or set(boundary) != {"identity"}
        or type(boundary["identity"]) is not str
        or not boundary["identity"]
    ):
        raise ValueError("the recurrent pair carries no exact source boundary")
    source_occurrence_identities = tuple(
        reference["material_acquisition_occurrence_identity"] for reference in sources
    )
    found = []
    for recurrence_assertion_identity in recurrence_assertion_identities:
        recurrence = findings_by_identity.get(recurrence_assertion_identity)
        if (
            recurrence is None
            or recurrence.result != "recurrence"
            or recurrence.exact_pair is None
        ):
            raise ValueError(
                "the addressed pair Assertion does not establish recurrence"
            )
        support = recurrence._local_support_assertion_identities
        if (
            len(support) != 1
            or type(support[0]) is not str
            or not support[0]
        ):
            raise ValueError(
                "the recurrent pair carries no exact count Assertion support"
            )
        count = findings_by_identity.get(support[0])
        if (
            count is None
            or count.result != "count"
            or count.exact_pair != recurrence.exact_pair
        ):
            raise ValueError(
                "the recurrent pair count support carries another exact Assertion reference"
            )
        reference = ReferenceToRecordedRecurrentBytePair(
            recorded_occurrence_identity=event.identity,
            recurrence_assertion_identity=recurrence.assertion_identity,
            count_assertion_identity=count.assertion_identity,
            locality_identity=event.locality_identity,
            source_occurrence_identities=source_occurrence_identities,
            completeness_boundary_identity=boundary["identity"],
            exact_material=bytes(recurrence.exact_pair),
        )
        _validate_pair_reference(reference)
        found.append(reference)
    return tuple(found)


def _exact_material_acquisition_event(ledger: EventLedger, event_identity: str) -> Event:
    try:
        return read_exact_material_acquisition_result(ledger, event_identity)
    except (TypeError, ValueError) as error:
        raise ValueError(
            "pair occurrence Measurement requires one intact material acquisition result"
        ) from error


def _measurement_source_position_coordinates(
    ledger: EventLedger,
    *,
    pair_references: tuple[ReferenceToRecordedRecurrentBytePair, ...],
    source_material_acquisition_occurrence_identity: str,
    boundary: EventLedgerBoundary,
) -> tuple[Event, tuple[tuple[int, ...], ...]]:
    if not pair_references:
        raise ValueError("pair occurrence Measurement requires one pair subject")
    source = _exact_material_acquisition_event(ledger, source_material_acquisition_occurrence_identity)
    pair_measurement_identity = pair_references[0].recorded_occurrence_identity
    if any(
        reference.recorded_occurrence_identity != pair_measurement_identity
        or reference.locality_identity != source.locality_identity
        for reference in pair_references
    ):
        raise ValueError("pair subject and measured source have distinct Localities")
    ledger.occurrences_in_append_order(
        (pair_measurement_identity, source.identity),
        locality_identity=source.locality_identity,
    )
    bounded_identities = {
        event.identity
        for event in ledger.list_locality(
            source.locality_identity,
            through=boundary,
        )
    }
    if (
        pair_measurement_identity not in bounded_identities
        or source.identity not in bounded_identities
    ):
        raise ValueError("pair occurrence source falls outside its exact boundary")
    exact = acquired_material_bytes(source)
    position_coordinates = [[] for _ in range(256)]
    for position, value in enumerate(exact):
        position_coordinates[value].append(position)
    return source, tuple(
        tuple(coordinates) for coordinates in position_coordinates
    )


def _finding_from_source_position_coordinates(
    *,
    pair_reference: ReferenceToRecordedRecurrentBytePair,
    source: Event,
    position_coordinates: tuple[tuple[int, ...], ...],
    boundary: EventLedgerBoundary,
    occurrence_count_boundary: int,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    first_byte, second_byte = pair_reference.exact_material
    first_position_coordinates = position_coordinates[first_byte]
    second_position_coordinates = position_coordinates[second_byte]
    overlap = (
        len(first_position_coordinates) if first_byte == second_byte else 0
    )
    available = (
        len(first_position_coordinates) * len(second_position_coordinates)
        - overlap
    )
    found = []
    for first_position in first_position_coordinates:
        for second_position in second_position_coordinates:
            if first_position == second_position:
                continue
            if len(found) == occurrence_count_boundary:
                break
            found.append((first_position, second_position))
        if len(found) == occurrence_count_boundary:
            break
    finding = FindingOfRecurrentBytePairOccurrencePositions(
        pair_reference=pair_reference,
        source_material_acquisition_occurrence_identity=source.identity,
        source_locality_identity=source.locality_identity,
        completeness_boundary=boundary,
        occurrence_count_boundary=occurrence_count_boundary,
        available_occurrence_count=available,
        occurrences=tuple(found),
    )
    _validate_finding(finding)
    return finding


def _measure_through(
    ledger: EventLedger,
    *,
    pair_reference: ReferenceToRecordedRecurrentBytePair,
    source_material_acquisition_occurrence_identity: str,
    boundary: EventLedgerBoundary,
    occurrence_count_boundary: int,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    source, position_coordinates = _measurement_source_position_coordinates(
        ledger,
        pair_references=(pair_reference,),
        source_material_acquisition_occurrence_identity=source_material_acquisition_occurrence_identity,
        boundary=boundary,
    )
    return _finding_from_source_position_coordinates(
        pair_reference=pair_reference,
        source=source,
        position_coordinates=position_coordinates,
        boundary=boundary,
        occurrence_count_boundary=occurrence_count_boundary,
    )


def measure_positions_of_recurrent_byte_pair_occurrences(
    ledger: EventLedger,
    *,
    pair_measurement_occurrence_identity: str,
    recurrence_assertion_identity: str,
    source_material_acquisition_occurrence_identity: str,
    occurrence_count_boundary: int,
    through: EventLedgerBoundary | None = None,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    """Measure one yielded pair subject in one later exact material acquisition result."""

    if type(occurrence_count_boundary) is not int or occurrence_count_boundary <= 0:
        raise ValueError("pair occurrence Measurement requires a positive exact count boundary")
    pair_reference = reference_to_recorded_recurrent_byte_pair(
        ledger,
        measurement_occurrence_identity=pair_measurement_occurrence_identity,
        recurrence_assertion_identity=recurrence_assertion_identity,
    )
    return _measure_through(
        ledger,
        pair_reference=pair_reference,
        source_material_acquisition_occurrence_identity=source_material_acquisition_occurrence_identity,
        boundary=through or ledger.append_boundary(),
        occurrence_count_boundary=occurrence_count_boundary,
    )


def measure_positions_for_recurrent_byte_pair_assertions(
    ledger: EventLedger,
    *,
    pair_measurement_occurrence_identity: str,
    recurrence_assertion_identities: tuple[str, ...],
    source_material_acquisition_occurrence_identity: str,
    occurrence_count_boundary: int,
    through: EventLedgerBoundary,
) -> tuple[FindingOfRecurrentBytePairOccurrencePositions, ...]:
    """Measure same-boundary pair subjects after one exact pair-result read."""

    if type(through) is not EventLedgerBoundary:
        raise TypeError(
            "Measurement of same-boundary pair subjects requires one exact boundary"
        )
    if type(occurrence_count_boundary) is not int or occurrence_count_boundary <= 0:
        raise ValueError("pair occurrence Measurement requires a positive exact count boundary")
    references = _references_to_recorded_recurrent_byte_pairs(
        ledger,
        measurement_occurrence_identity=pair_measurement_occurrence_identity,
        recurrence_assertion_identities=recurrence_assertion_identities,
    )
    source, position_coordinates = _measurement_source_position_coordinates(
        ledger,
        pair_references=references,
        source_material_acquisition_occurrence_identity=source_material_acquisition_occurrence_identity,
        boundary=through,
    )
    return tuple(
        _finding_from_source_position_coordinates(
            pair_reference=reference,
            source=source,
            position_coordinates=position_coordinates,
            boundary=through,
            occurrence_count_boundary=occurrence_count_boundary,
        )
        for reference in references
    )


def _responsibility_assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
        "book_clause_identity": assignment.material["book_clause_identity"],
        "result_boundary_identity": assignment.material[
            "result_boundary_identity"
        ],
    }


def _responsibility_assignment_material(
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    assignment_identity: str,
    assignment_subject_identity: str,
    measurement_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
    standing_boundary_identity: str,
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "measurement_act_identity": measurement_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "result_boundary_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
        "responsibility": (
            RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT
        ),
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_material_acquisition_occurrence_identity": (
            finding.source_material_acquisition_occurrence_identity
        ),
        "source_locality_identity": finding.source_locality_identity,
        "completeness_boundary_identity": finding.completeness_boundary.identity,
        "occurrence_count_boundary": finding.occurrence_count_boundary,
        "standing_boundary_identity": standing_boundary_identity,
        "scope": {
            "source_locality_identity": finding.source_locality_identity,
            "completeness_boundary_identity": (
                finding.completeness_boundary.identity
            ),
            "occurrence_count_boundary": finding.occurrence_count_boundary,
        },
        "unknown": [],
    }


def _require_current_assignment_standing(
    ledger: EventLedger,
    *,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    locality_standing: dict[str, Any],
    required_assignment_identity: str | None = None,
) -> str:
    if type(locality_standing) is not dict:
        raise ValueError(
            "pair occurrence Measurement requires exact current Locality Standing"
        )
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )
    from seed_runtime.material_acquisition import (
        read_material_acquisition_locality_relation_requirements,
    )

    current = read_operator_locality_standing(
        ledger, locality_identity=finding.source_locality_identity
    )
    measurements = locality_standing.get("measurement_occurrences")
    acquisition_results = locality_standing.get("material_acquisition_result_occurrences")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    boundary = locality_standing.get("through_event_occurrence_identity")
    source_has_exact_locality = all(
        read_material_acquisition_locality_relation_requirements(
            ledger,
            recorded_result_event_identity=(
                finding.source_material_acquisition_occurrence_identity
            ),
        ).values()
    )
    if (
        locality_standing != current
        or locality_standing.get("locality_identity")
        != finding.source_locality_identity
        or type(boundary) is not str
        or not boundary
        or type(measurements) is not dict
        or finding.pair_reference.recorded_occurrence_identity not in measurements
        or type(acquisition_results) is not list
        or not any(
            type(occurrence) is dict
            and occurrence.get("result_occurrence_identity")
            == finding.source_material_acquisition_occurrence_identity
            for occurrence in acquisition_results
        )
        or not source_has_exact_locality
        or (
            required_assignment_identity is not None
            and (
                type(assignments) is not dict
                or assignments.get(required_assignment_identity, object()) is not None
            )
        )
    ):
        raise ValueError(
            "pair occurrence Measurement requires exact current Locality Standing"
        )
    return boundary


def record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    *,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    locality_standing: dict[str, Any],
) -> Event:
    """Record one exact Responsibility assignment before its Measurement Act."""

    _validate_exact_finding_of_measurement(ledger, finding)
    standing_boundary_identity = _require_current_assignment_standing(
        ledger, finding=finding, locality_standing=locality_standing
    )
    identities = {
        "assignment_identity": new_identity(
            "recurrent_pair_position_measurement_assignment"
        ),
        "assignment_subject_identity": new_identity(
            "recurrent_pair_position_measurement_assignment_subject"
        ),
        "measurement_act_identity": new_identity(
            "act_of_measurement_of_recurrent_byte_pair_occurrence_position"
        ),
        "act_occurrence_identity": new_identity(
            "act_occurrence_of_measurement_of_recurrent_byte_pair_occurrence_position"
        ),
        "measurement_result_identity": new_identity(
            "result_of_measurement_of_recurrent_byte_pair_occurrence_position"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ValueError("pair occurrence Measurement lifecycle identities collapsed")
    return ledger.append(
        RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
        _responsibility_assignment_material(
            finding,
            standing_boundary_identity=standing_boundary_identity,
            **identities,
        ),
        locality_identity=finding.source_locality_identity,
    )


def _read_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    assignment_event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, FindingOfRecurrentBytePairOccurrencePositions]:
    if type(assignment_event_identity) is not str or not assignment_event_identity:
        raise ValueError("pair occurrence Measurement requires one exact assignment")
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind
        != RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        or type(assignment.locality_identity) is not str
        or not assignment.locality_identity
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence assignment is absent or corrupted")
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
    pair_reference = material.get("pair_assertion_reference")
    if (
        any(type(identity) is not str or not identity for identity in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(pair_reference) is not dict
        or set(pair_reference) != {"recorded_occurrence_identity", "assertion_identity"}
        or any(type(value) is not str or not value for value in pair_reference.values())
        or type(material.get("source_material_acquisition_occurrence_identity")) is not str
        or not material["source_material_acquisition_occurrence_identity"]
        or type(material.get("completeness_boundary_identity")) is not str
        or not material["completeness_boundary_identity"]
        or type(material.get("occurrence_count_boundary")) is not int
        or material["occurrence_count_boundary"] <= 0
        or type(material.get("standing_boundary_identity")) is not str
        or not material["standing_boundary_identity"]
    ):
        raise ValueError("pair occurrence assignment carries malformed coordinates")
    standing_boundary_identity = material["standing_boundary_identity"]
    if prior_standing is None:
        from seed_runtime.operator_locality_standing import (
            _operator_standing_validation_context,
        )

        prior_standing = _operator_standing_validation_context(
            ledger, locality_identity=assignment.locality_identity
        )
        if prior_standing is None:
            from seed_runtime.operator_locality_standing import (
                read_operator_locality_standing_through,
            )

            prior_standing = read_operator_locality_standing_through(
                ledger,
                locality_identity=assignment.locality_identity,
                through_event_occurrence_identity=standing_boundary_identity,
            )
    pair_validation_standing = (
        prior_standing
        if type(prior_standing.get("responsibility_assignment_occurrences"))
        is dict
        else None
    )
    pair_subject = _references_to_recorded_recurrent_byte_pairs(
        ledger,
        measurement_occurrence_identity=pair_reference[
            "recorded_occurrence_identity"
        ],
        recurrence_assertion_identities=(pair_reference["assertion_identity"],),
        prior_standing=pair_validation_standing,
    )[0]
    finding = _measure_through(
        ledger,
        pair_reference=pair_subject,
        source_material_acquisition_occurrence_identity=material[
            "source_material_acquisition_occurrence_identity"
        ],
        boundary=EventLedgerBoundary(material["completeness_boundary_identity"]),
        occurrence_count_boundary=material["occurrence_count_boundary"],
    )
    expected = _responsibility_assignment_material(
        finding,
        standing_boundary_identity=material["standing_boundary_identity"],
        **identities,
    )
    if (
        assignment.locality_identity != finding.source_locality_identity
        or material != expected
    ):
        raise ValueError("pair occurrence assignment coordinates are not exact")
    measurements = prior_standing.get("measurement_occurrences")
    acquisition_results = prior_standing.get("material_acquisition_result_occurrences")
    carried_assignments = prior_standing.get(
        "responsibility_assignment_occurrences"
    )
    prior_boundary_identity = prior_standing.get(
        "through_event_occurrence_identity"
    )
    # Every carried Standing crosses at least one ledger read.  Bind its two
    # addressed inputs to their intact occurrence coordinates instead of
    # trusting shaped membership, whether the carrier came from the bounded
    # replay context or one family-private same-call reading.
    pair_occurrence_identity = (
        finding.pair_reference.recorded_occurrence_identity
    )
    exact_measurement_occurrence = (
        _exact_measurement_occurrence_standing_coordinates(
            ledger, pair_occurrence_identity
        )
    )
    exact_material_acquisition_result_occurrence = _exact_material_acquisition_result_availability_coordinates(
        ledger, finding.source_material_acquisition_occurrence_identity
    )
    from seed_runtime.material_acquisition import (
        read_material_acquisition_locality_relation_requirements,
    )
    source_has_exact_locality = all(
        read_material_acquisition_locality_relation_requirements(
            ledger,
            recorded_result_event_identity=(
                finding.source_material_acquisition_occurrence_identity
            ),
        ).values()
    )
    carried_material_acquisition_result_occurrences = (
        [
            occurrence
            for occurrence in acquisition_results
            if type(occurrence) is dict
            and occurrence.get("result_occurrence_identity")
            == finding.source_material_acquisition_occurrence_identity
        ]
        if type(acquisition_results) is list
        else []
    )
    if (
        type(measurements) is not dict
        or measurements.get(pair_occurrence_identity, object())
        != exact_measurement_occurrence
        or carried_material_acquisition_result_occurrences != [exact_material_acquisition_result_occurrence]
        or not source_has_exact_locality
    ):
        raise ValueError(
            "pair occurrence assignment has no exact prior Standing"
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
        or type(measurements) is not dict
        or finding.pair_reference.recorded_occurrence_identity not in measurements
        or type(acquisition_results) is not list
        or not any(
            type(occurrence) is dict
            and occurrence.get("result_occurrence_identity")
            == finding.source_material_acquisition_occurrence_identity
            for occurrence in acquisition_results
        )
        or not source_has_exact_locality
    ):
        raise ValueError("pair occurrence assignment has no exact prior Standing")
    order = (
        (standing_boundary_identity, assignment.identity)
        if boundary_is_exact or prior_boundary_identity == assignment.identity
        else (
            standing_boundary_identity,
            assignment.identity,
            prior_boundary_identity,
        )
    )
    try:
        ledger.occurrences_in_append_order(
            order,
            locality_identity=assignment.locality_identity,
        )
    except ValueError as error:
        raise ValueError("pair occurrence assignment order is false") from error
    return assignment, finding


def get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger, assignment_event_identity: str
) -> Event:
    return _read_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger, assignment_event_identity
    )[0]


def _participation_in_measurement(
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    act_occurrence_identity: str,
) -> list[dict[str, Any]]:
    return [
        {
            "subject_reference": finding.pair_reference.assertion_reference,
            "role": "Yield-carried recurrent byte-pair subject",
            "act_occurrence_identity": act_occurrence_identity,
            "applicability": "applicable",
        },
        {
            "subject_reference": {
                "recorded_occurrence_identity": (
                    finding.source_material_acquisition_occurrence_identity
                )
            },
            "role": "exact material result input",
            "act_occurrence_identity": act_occurrence_identity,
            "applicability": "applicable",
        },
    ]


def _material_of_act_occurrence(
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    assignment: Event,
) -> dict[str, Any]:
    act_identity = assignment.material["measurement_act_identity"]
    act_occurrence_identity = assignment.material["act_occurrence_identity"]
    return {
        "addressed_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "act": ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "responsibility": RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": _responsibility_assignment_reference(
            assignment
        ),
        "measurement_rule": RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "source_localities": [finding.source_locality_identity],
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity,
        },
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_material_acquisition_occurrence_identity": (
            finding.source_material_acquisition_occurrence_identity
        ),
        "occurrence_count_boundary": finding.occurrence_count_boundary,
        "participation": _participation_in_measurement(
            finding,
            act_occurrence_identity=act_occurrence_identity,
        ),
    }


def _validate_exact_finding_of_measurement(
    ledger: EventLedger,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
) -> None:
    _validate_finding(finding)
    pair_reference = reference_to_recorded_recurrent_byte_pair(
        ledger,
        measurement_occurrence_identity=(
            finding.pair_reference.recorded_occurrence_identity
        ),
        recurrence_assertion_identity=(
            finding.pair_reference.recurrence_assertion_identity
        ),
    )
    exact = _measure_through(
        ledger,
        pair_reference=pair_reference,
        source_material_acquisition_occurrence_identity=finding.source_material_acquisition_occurrence_identity,
        boundary=finding.completeness_boundary,
        occurrence_count_boundary=finding.occurrence_count_boundary,
    )
    if exact != finding:
        raise ValueError("pair occurrence finding differs from its exact inputs")


def record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    """Record the responsible Measurement Act before its Yield and result."""

    assignment, finding = _read_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger, responsibility_assignment_event_identity
    )
    _require_current_assignment_standing(
        ledger,
        finding=finding,
        locality_standing=responsibility_assignment_standing,
        required_assignment_identity=assignment.identity,
    )
    for event in ledger.iter_locality_kind(
        assignment.locality_identity,
        RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT,
    ):
        if (
            event.material.get("responsibility_assignment_reference")
            == _responsibility_assignment_reference(assignment)
            or event.material.get("act_occurrence_identity")
            == assignment.material["act_occurrence_identity"]
        ):
            raise ValueError("pair occurrence assignment already carries an Act")
    return ledger.append(
        RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT,
        _material_of_act_occurrence(
            finding,
            assignment=assignment,
        ),
        locality_identity=assignment.locality_identity,
    )


def _finding_of_measurement_from_act_occurrence(
    ledger: EventLedger,
    act_occurrence: Event,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, FindingOfRecurrentBytePairOccurrencePositions]:
    material = act_occurrence.material
    assignment_reference = material.get("responsibility_assignment_reference")
    if (
        type(assignment_reference) is not dict
        or set(assignment_reference)
        != {
            "recorded_occurrence_identity",
            "assignment_identity",
            "assignment_subject_identity",
            "book_clause_identity",
            "result_boundary_identity",
        }
    ):
        raise ValueError("pair occurrence Act occurrence carries malformed coordinates")
    assignment, finding = _read_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        assignment_reference.get("recorded_occurrence_identity"),
        prior_standing=prior_standing,
    )
    expected = _material_of_act_occurrence(
        finding, assignment=assignment
    )
    if (
        act_occurrence.locality_identity != assignment.locality_identity
        or assignment_reference != _responsibility_assignment_reference(assignment)
        or material != expected
    ):
        raise ValueError("pair occurrence Act occurrence carries no exact assignment")
    return assignment, finding


def _identity_of_position_assertion(
    *,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    first_position: int,
    second_position: int,
) -> str:
    digest = hashlib.sha256()
    for coordinate in (
        finding.pair_reference.recorded_occurrence_identity,
        finding.pair_reference.recurrence_assertion_identity,
        finding.source_material_acquisition_occurrence_identity,
        finding.source_locality_identity,
        finding.completeness_boundary.identity,
        str(first_position),
        str(second_position),
    ):
        encoded = coordinate.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return "pair-occurrence-measurement:" + digest.hexdigest()


def _position_assertions_of_measurement(finding: FindingOfRecurrentBytePairOccurrencePositions) -> list[dict[str, Any]]:
    scope = {"source_localities": [finding.source_locality_identity]}
    subject = {
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_material_acquisition_occurrence_identity": (
            finding.source_material_acquisition_occurrence_identity
        ),
        "measurement_rule": RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
    }
    assertions = []
    for first_position, second_position in finding.occurrences:
        content = {
            "first_position": first_position,
            "second_position": second_position,
            "completeness_boundary": {
                "identity": finding.completeness_boundary.identity,
            },
        }
        assertions.append(
            {
                "dimensions": {
                    "identity": _identity_of_position_assertion(
                        finding=finding,
                        first_position=first_position,
                        second_position=second_position,
                    ),
                    "content": content,
                    "source_provenance": (
                        "the exact Yield-carried pair Assertion and later material acquisition result"
                    ),
                    "responsibility": RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_ASSERTION,
                },
                "subject_kind": "assertion",
                "responsible_boundary": "this recorded assertion",
                "result": "position",
                "assertion_subject": subject,
                "assertion_scope": scope,
                "input_support": {
                    "assertion_references": [
                        finding.pair_reference.assertion_reference
                    ],
                    "occurrence_references": [
                        finding.source_material_acquisition_occurrence_identity
                    ],
                    "local_assertion_references": [],
                },
                "conflicts": "Unknown",
                "unknown": [],
            }
        )
    return assertions


def _material_of_result_of_measurement(
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    assignment: Event,
) -> dict[str, Any]:
    known_loss = (
        ["pair occurrences beyond the exact occurrence count boundary are not carried"]
        if finding.available_occurrence_count > len(finding.occurrences)
        else []
    )
    return {
        "result_identity": assignment.material["measurement_result_identity"],
        "dimensions": {
            "identity": "recurrent-byte-pair-occurrence-position-measurement",
            "content": "exact ordered pair occurrence position Assertions",
            "source_provenance": (
                "one recurrence Assertion carried by Yield relation and one later "
                "exact material acquisition result"
            ),
        },
        "exact_act": ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "addressed_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material["act_occurrence_identity"],
        "responsibility": RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": _responsibility_assignment_reference(
            assignment
        ),
        "measurement_rule": RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "source_localities": [finding.source_locality_identity],
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity,
        },
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_material_acquisition_occurrence_identity": (
            finding.source_material_acquisition_occurrence_identity
        ),
        "occurrence_count_boundary": finding.occurrence_count_boundary,
        "available_occurrence_count": finding.available_occurrence_count,
        "known_loss": known_loss,
        "assertions": _position_assertions_of_measurement(finding),
    }


def record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
) -> Event:
    """Record the Yield and result for one exact pair occurrence Measurement."""

    if (
        type(act_occurrence_event_identity) is not str
        or not act_occurrence_event_identity
    ):
        raise ValueError("pair occurrence result requires exact Act occurrence")
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if (
        act_occurrence is None
        or act_occurrence.kind != RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT
        or type(act_occurrence.locality_identity) is not str
        or not act_occurrence.locality_identity
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence result requires intact Act occurrence")
    assignment, finding = _finding_of_measurement_from_act_occurrence(
        ledger, act_occurrence
    )
    expected_act = _material_of_act_occurrence(
        finding, assignment=assignment
    )
    if act_occurrence.material != expected_act:
        raise ValueError(
            "pair occurrence result differs from its exact Act occurrence"
        )
    act_occurrence_identity = act_occurrence.material["act_occurrence_identity"]
    for event in ledger.list_locality(act_occurrence.locality_identity):
        if event.kind in {
            RECORDED_YIELD_RELATION_EVENT,
            RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
        } and (
            event.material.get("act_occurrence_identity")
            == act_occurrence.identity
            or event.material.get("act_occurrence_identity")
            == act_occurrence_identity
            or event.material.get("dimensions", {}).get("act_occurrence_identity")
            == act_occurrence_identity
        ):
            raise ValueError("pair occurrence Measurement Act already has a result")
    result = _material_of_result_of_measurement(
        finding, assignment=assignment
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act_occurrence.locality_identity,
        exact_act=ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        act_occurrence_identity=act_occurrence_identity,
        act_occurrence_event_identity=act_occurrence.identity,
        result_kind=RESULT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KIND,
        result_identity=result["result_identity"],
        result_content=result,
        responsibility=RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        occurrence_boundary="measurement_of_recurrent_byte_pair_occurrence_position",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
        {
            "result_identity": result["result_identity"],
            "dimensions": result["dimensions"],
            "exact_act": result["exact_act"],
            "addressed_act_identity": result["addressed_act_identity"],
            "act_occurrence_identity": result["act_occurrence_identity"],
            "responsibility": result["responsibility"],
            "responsible_boundary": result["responsible_boundary"],
            "responsibility_assignment_reference": result[
                "responsibility_assignment_reference"
            ],
            "measurement_rule": result["measurement_rule"],
            "source_localities": result["source_localities"],
            "completeness_boundary": result["completeness_boundary"],
            "pair_assertion_reference": result["pair_assertion_reference"],
            "source_material_acquisition_occurrence_identity": result[
                "source_material_acquisition_occurrence_identity"
            ],
            "occurrence_count_boundary": result["occurrence_count_boundary"],
            "available_occurrence_count": result[
                "available_occurrence_count"
            ],
            "known_loss": result["known_loss"],
            "assertions": result["assertions"],
            "act_occurrence_event_identity": act_occurrence.identity,
            "yield_relation_identity": yield_relation.identity,
        },
        locality_identity=act_occurrence.locality_identity,
    )


def _recorded_result_of_recurrent_pair_position_measurement_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, FindingOfRecurrentBytePairOccurrencePositions]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence Measurement result is absent or corrupted")
    material = event.material
    if set(material) != RESULT_COORDINATES_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT | {
        "act_occurrence_identity",
        "act_occurrence_event_identity",
        "yield_relation_identity",
    }:
        raise ValueError("pair occurrence result carries malformed coordinates")
    act_occurrence_event_identity = material.get("act_occurrence_event_identity")
    act_occurrence = (
        ledger.get(act_occurrence_event_identity)
        if type(act_occurrence_event_identity) is str
        else None
    )
    if (
        act_occurrence is None
        or act_occurrence.kind != RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT
        or act_occurrence.locality_identity != event.locality_identity
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence result carries no exact Act occurrence")
    assignment, finding = _finding_of_measurement_from_act_occurrence(
        ledger, act_occurrence, prior_standing=prior_standing
    )
    expected_act = _material_of_act_occurrence(
        finding, assignment=assignment
    )
    if act_occurrence.material != expected_act:
        raise ValueError(
            "pair occurrence result differs from its exact Act occurrence"
        )
    result = _material_of_result_of_measurement(
        finding, assignment=assignment
    )
    carried = {
        key: value
        for key, value in material.items()
        if key
        not in {
            "act_occurrence_event_identity",
            "yield_relation_identity",
        }
    }
    if carried != result:
        raise ValueError("pair occurrence result differs from its exact finding")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=material.get("yield_relation_identity"),
        act_occurrence_event_identity=act_occurrence.identity,
    )
    yield_relation = ledger.get(material.get("yield_relation_identity"))
    if (
        not all(requirements.values())
        or yield_relation is None
        or yield_relation.material.get("occurrence_boundary")
        != MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_BOUNDARY
        or yield_relation.material.get("result_kind")
        != RESULT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KIND
    ):
        raise ValueError("pair occurrence result carries no exact Yield relation")
    return event, finding


def _read_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    return _recorded_result_of_recurrent_pair_position_measurement_reading(
        ledger,
        event_identity,
        prior_standing=prior_standing,
    )[1]


def get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    event_identity: str,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    """Read one pair-occurrence result through its exact Act and Yield."""

    return _read_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger, event_identity
    )


def _references_from_recorded_recurrent_pair_position_result(
    event: Event,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    assertion_identities: tuple[str, ...] | None = None,
) -> tuple[ReferenceToRecordedRecurrentBytePairOccurrencePosition, ...]:
    assertions = event.material["assertions"]
    if len(assertions) != len(finding.occurrences):
        raise ValueError("pair-position result carries a different Assertion population")
    references = []
    for assertion, (first_position, second_position) in zip(
        assertions, finding.occurrences
    ):
        assertion_identity = assertion.get("dimensions", {}).get("identity")
        if type(assertion_identity) is not str or not assertion_identity:
            raise ValueError("pair-position result carries no exact Assertion identity")
        references.append(
            ReferenceToRecordedRecurrentBytePairOccurrencePosition(
                recorded_occurrence_identity=event.identity,
                assertion_identity=assertion_identity,
                pair_measurement_occurrence_identity=(
                    finding.pair_reference.recorded_occurrence_identity
                ),
                recurrence_assertion_identity=(
                    finding.pair_reference.recurrence_assertion_identity
                ),
                count_assertion_identity=(
                    finding.pair_reference.count_assertion_identity
                ),
                source_material_acquisition_occurrence_identity=(
                    finding.source_material_acquisition_occurrence_identity
                ),
                locality_identity=finding.source_locality_identity,
                completeness_boundary_identity=(
                    finding.completeness_boundary.identity
                ),
                exact_pair=finding.pair_reference.exact_material,
                first_position=first_position,
                second_position=second_position,
            )
        )
    if assertion_identities is None:
        return tuple(references)
    if (
        type(assertion_identities) is not tuple
        or any(type(identity) is not str or not identity for identity in assertion_identities)
        or len(set(assertion_identities)) != len(assertion_identities)
    ):
        raise ValueError("pair-position references require exact Assertion identities")
    by_identity = {reference.assertion_identity: reference for reference in references}
    if any(identity not in by_identity for identity in assertion_identities):
        raise ValueError("pair-position result carries no addressed Assertion")
    return tuple(by_identity[identity] for identity in assertion_identities)


def _recurrent_pair_position_result_lifecycle_boundary(
    ledger: EventLedger,
    result_occurrence_identity: str,
) -> tuple[str, str]:
    if type(result_occurrence_identity) is not str or not result_occurrence_identity:
        raise ValueError("pair-position references require one exact result occurrence")
    result = ledger.get(result_occurrence_identity)
    if (
        result is None
        or result.kind
        != RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        or type(result.locality_identity) is not str
        or not result.locality_identity
        or ledger.integrity_of(result.identity) == CORRUPTED
    ):
        raise ValueError("pair-position result is absent or corrupted")
    act_identity = result.material.get("act_occurrence_event_identity")
    act = ledger.get(act_identity) if type(act_identity) is str else None
    if (
        act is None
        or act.kind
        != RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT
        or act.locality_identity != result.locality_identity
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ValueError("pair-position result carries no exact Act occurrence")
    assignment_reference = act.material.get("responsibility_assignment_reference")
    assignment_identity = (
        assignment_reference.get("recorded_occurrence_identity")
        if type(assignment_reference) is dict
        else None
    )
    assignment = (
        ledger.get(assignment_identity)
        if type(assignment_identity) is str
        else None
    )
    if (
        assignment is None
        or assignment.kind
        != RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        or assignment.locality_identity != result.locality_identity
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ValueError("pair-position result carries no exact assignment")
    boundary_identity = assignment.material.get("standing_boundary_identity")
    if type(boundary_identity) is not str or not boundary_identity:
        raise ValueError("pair-position assignment carries no exact Standing boundary")
    try:
        ordered = tuple(
            dict.fromkeys(
                (
                    boundary_identity,
                    assignment.identity,
                    act.identity,
                    result.identity,
                )
            )
        )
        resolved = ledger.occurrences_in_append_order(
            ordered,
            locality_identity=result.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ValueError("pair-position result lifecycle order is false") from error
    if tuple(event.identity for event in resolved) != ordered:
        raise ValueError("pair-position result lifecycle order is false")
    return boundary_identity, result.locality_identity


def _references_to_addressed_recorded_recurrent_pair_position_results(
    ledger: EventLedger,
    *,
    result_and_assertion_identities: tuple[
        tuple[str, str], tuple[str, str]
    ],
    prior_standing: dict[str, Any] | None = None,
) -> tuple[
    ReferenceToRecordedRecurrentBytePairOccurrencePosition,
    ReferenceToRecordedRecurrentBytePairOccurrencePosition,
]:
    """Address two distinct results through one exact current Standing read."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("pair-position references require one EventLedger")
    if (
        type(result_and_assertion_identities) is not tuple
        or len(result_and_assertion_identities) != 2
        or any(
            type(address) is not tuple
            or len(address) != 2
            or any(type(identity) is not str or not identity for identity in address)
            for address in result_and_assertion_identities
        )
        or result_and_assertion_identities[0][0]
        == result_and_assertion_identities[1][0]
    ):
        raise ValueError("two distinct pair-position results must be addressed")
    lifecycle_boundaries = tuple(
        _recurrent_pair_position_result_lifecycle_boundary(
            ledger, result_identity
        )
        for result_identity, _assertion_identity in result_and_assertion_identities
    )
    localities = tuple(locality for _boundary, locality in lifecycle_boundaries)
    if localities[0] != localities[1]:
        raise ValueError("addressed pair-position results require one exact Locality")
    boundaries = tuple(boundary for boundary, _locality in lifecycle_boundaries)
    if boundaries[0] == boundaries[1]:
        later_boundary = boundaries[0]
    else:
        later_boundary = None
        for ordered_boundaries in (boundaries, tuple(reversed(boundaries))):
            try:
                resolved = ledger.occurrences_in_append_order(
                    ordered_boundaries,
                    locality_identity=localities[0],
                )
            except (TypeError, ValueError):
                continue
            if tuple(event.identity for event in resolved) == ordered_boundaries:
                later_boundary = ordered_boundaries[1]
                break
        if later_boundary is None:
            raise ValueError("addressed pair-position Standing boundaries are crossed")
    if prior_standing is None:
        from seed_runtime.operator_locality_standing import (
            read_operator_locality_standing_through,
        )

        prior_standing = read_operator_locality_standing_through(
            ledger,
            locality_identity=localities[0],
            through_event_occurrence_identity=later_boundary,
        )
    elif type(prior_standing) is not dict:
        raise ValueError("addressed pair-position results require exact prior Standing")
    addressed = []
    for result_identity, assertion_identity in result_and_assertion_identities:
        event, finding = (
            _recorded_result_of_recurrent_pair_position_measurement_reading(
                ledger,
                result_identity,
                prior_standing=prior_standing,
            )
        )
        addressed.append(
            _references_from_recorded_recurrent_pair_position_result(
                event,
                finding,
                assertion_identities=(assertion_identity,),
            )[0]
        )
    return addressed[0], addressed[1]


def references_to_recorded_recurrent_byte_pair_occurrence_positions(
    ledger: EventLedger,
    *,
    result_occurrence_identity: str,
) -> tuple[ReferenceToRecordedRecurrentBytePairOccurrencePosition, ...]:
    """Read one intact result and address each exact position Assertion once."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("pair-position references require one EventLedger")
    if (
        type(result_occurrence_identity) is not str
        or not result_occurrence_identity
    ):
        raise ValueError("pair-position references require one exact result occurrence")
    finding = (
        get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, result_occurrence_identity
        )
    )
    event = ledger.get(result_occurrence_identity)
    if event is None:
        raise ValueError("pair-position result disappeared after validation")
    return _references_from_recorded_recurrent_pair_position_result(
        event, finding
    )
