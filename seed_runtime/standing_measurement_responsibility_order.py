"""Record Measurements in the Standing Measurement Responsibility order.

The coordinates in this module do not assign a new Responsibility.  Each
entry names one existing Book-assigned Measurement road.  Discovery chooses
one exact subject at one current Standing boundary, the family records its own
assignment, Act, Yield, and result, and Standing is advanced before discovery
continues.

Ledger writes remain serial and deterministic.  A later implementation may
compute pure discovery findings concurrently, but no two family occurrences
may be appended from one stale Standing boundary.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, NamedTuple

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    _record_byte_measurement_lifecycle_from_carried_standing,
    _record_byte_measurement_responsible_act_evidence_from_carried_standing,
    _record_byte_measurement_result_from_carried_act_evidence,
    record_byte_measurement_responsibility_assignment,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _record_byte_pair_occurrence_position_measurement_act_evidence_from_carried_assignment,
    _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_carried_finding,
    _record_byte_pair_occurrence_position_measurement_result_from_carried_act_evidence,
    measure_position_coordinates_of_byte_pair_occurrences,
    record_byte_pair_occurrence_position_measurement_responsibility_assignment,
)
from seed_runtime.material_ingest import read_exact_ingest_result
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    RESPONSIBILITY_ASSIGNMENT_KIND as ADDRESSED_BYTE_REFERENCE_ASSIGNMENT_KIND,
    DETERMINATION_RESULT_KIND as ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND,
    SOURCE_REFERENCE_FOR_STANDING_MEASUREMENT_RESPONSIBILITY_ORDER_COORDINATE,
    _determination_result_reference as _addressed_byte_reference_result_reference,
    _incomplete_determination_assignment_for_subject,
    _continue_addressed_byte_occurrence_reference_determination_lifecycle,
    _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing,
)
from seed_runtime.measurement_of_source_position_coordinates_carrying_addressed_material import (
    RESPONSIBILITY_ASSIGNMENT_KIND as ADDRESSED_MATERIAL_COORDINATE_ASSIGNMENT_KIND,
    MEASUREMENT_RESULT_KIND as ADDRESSED_MATERIAL_COORDINATE_RESULT_KIND,
    measurement_result_reference as _addressed_material_result_reference,
    _population_references as _addressed_material_population_references,
    _incomplete_assignment_for_subject as _addressed_material_incomplete_assignment,
    _continue_addressed_material_coordinate_measurement_lifecycle,
    _record_addressed_material_coordinate_measurement_lifecycle_from_carried_standing,
    _subject_is_unmeasured as _addressed_material_subject_is_unmeasured,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    D2_RESULT_REFERENCE_COORDINATE,
    _incomplete_shared_position_assignment_for_determination,
    _continue_shared_position_measurement_lifecycle,
    _record_shared_position_measurement_lifecycle_from_carried_d2_result,
)
from seed_runtime.operator_locality_standing import (
    _carry_byte_measurement_assignment_into_standing,
    _carry_byte_pair_occurrence_position_measurement_assignment_into_standing,
    _carry_byte_pair_occurrence_position_measurement_result_into_standing,
    advance_operator_locality_standing,
    read_operator_locality_standing,
)


class StandingMeasurementResponsibilityOrderCoordinate(NamedTuple):
    order: int
    book_clause_identity: str
    measurement_identity: str
    assignment_kind: str
    result_kind: str
    discover: Callable[[EventLedger, dict[str, Any], str], str | None]
    record: Callable[
        [EventLedger, dict[str, Any], str, str], tuple[dict[str, Any], Event]
    ]
    record_from_current: Callable[
        [EventLedger, dict[str, Any], str, str], tuple[dict[str, Any], Event]
    ]


class RecordedMeasurementsInStandingMeasurementResponsibilityOrder(NamedTuple):
    locality_standing: dict[str, Any]
    result_occurrences: tuple[Event, ...]


class StandingMeasurementResponsibilityLifecyclePrefix(NamedTuple):
    subject: Any
    assignment_event_identity: str


class AddressedCoordinateSubjectForStandingMeasurementResponsibilityOrder(NamedTuple):
    direct_result_event_identity: str
    source_position_coordinate_reference: dict[str, Any]
    trigger_result_event_identity: str
    trigger_finding: dict[str, Any]


def _advance(
    ledger: EventLedger,
    standing: dict[str, Any],
    event_identities: tuple[str, ...],
    *,
    locality_identity: str,
) -> dict[str, Any]:
    return advance_operator_locality_standing(
        ledger,
        event_identities,
        locality_identity=locality_identity,
        prior=standing,
    )


def _require_current_pin(
    ledger: EventLedger,
    standing: dict[str, Any],
    *,
    locality_identity: str,
) -> None:
    if (
        not isinstance(ledger, EventLedger)
        or type(locality_identity) is not str
        or not locality_identity
        or type(standing) is not dict
        or standing.get("locality_identity") != locality_identity
        or type(standing.get("ingest_occurrences")) is not list
        or type(standing.get("measurement_occurrences")) is not dict
        or type(standing.get("responsibility_assignment_occurrences")) is not dict
    ):
        raise ValueError(
            "recording a Measurement in the Standing Measurement Responsibility order "
            "requires exact current Standing"
        )
    boundary = standing.get("through_event_occurrence_identity")
    event = ledger.get(boundary) if type(boundary) is str and boundary else None
    locality_events = (
        ledger.list_locality(locality_identity) if event is not None else ()
    )
    if (
        event is None
        or event.locality_identity != locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or not locality_events
        or locality_events[-1].identity != event.identity
    ):
        raise ValueError(
            "recording a Measurement in the Standing Measurement Responsibility order "
            "requires the current append boundary"
        )


def _ingest_identities(standing: dict[str, Any]) -> tuple[str, ...]:
    identities = []
    for occurrence in standing["ingest_occurrences"]:
        if (
            type(occurrence) is not dict
            or type(occurrence.get("evidence_event_identity")) is not str
            or not occurrence["evidence_event_identity"]
        ):
            raise ValueError("current Standing carries a malformed Ingest occurrence")
        identities.append(occurrence["evidence_event_identity"])
    return tuple(identities)


def _direct_assignment_sources(
    ledger: EventLedger, locality_identity: str
) -> set[str]:
    sources: set[str] = set()
    for assignment in ledger.iter_locality_kind(
        locality_identity, BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND
    ):
        source = assignment.material.get("source_ingest_occurrence_identity")
        if (
            ledger.integrity_of(assignment.identity) == CORRUPTED
            or type(source) is not str
            or not source
        ):
            raise ValueError("recorded direct Measurement assignment is malformed")
        sources.add(source)
    return sources


def _discover_direct_measurement(
    ledger: EventLedger, standing: dict[str, Any], locality_identity: str
) -> str | None:
    assigned = _direct_assignment_sources(ledger, locality_identity)
    for identity in _ingest_identities(standing):
        if identity in assigned:
            continue
        event = ledger.get(identity)
        if event is None or event.locality_identity != locality_identity:
            raise ValueError("current Standing carries an absent Ingest occurrence")
        if not all(
            type(event.material.get(key)) is str and event.material[key]
            for key in (
                "responsible_act_evidence_identity",
                "evidence_of_yield_relation_identity",
            )
        ):
            # Older preserved material can be an Ingest occurrence without an
            # exact Act/Yield result.  It is input to the aggregate byte road,
            # but it is not the exact subject of this direct Measurement.
            continue
        read_exact_ingest_result(ledger, identity)
        return identity
    return None


def _complete_direct_measurement(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    assignment: Event,
    finding,
) -> tuple[dict[str, Any], Event]:
    prior_boundary = standing["through_event_occurrence_identity"]
    standing = _carry_byte_pair_occurrence_position_measurement_assignment_into_standing(
        ledger,
        standing,
        assignment,
        finding,
        prior_through_event_occurrence_identity=prior_boundary,
    )
    act = _record_byte_pair_occurrence_position_measurement_act_evidence_from_carried_assignment(
        ledger,
        responsibility_assignment=assignment,
        finding=finding,
        responsibility_assignment_standing=standing,
    )
    standing = _advance(
        ledger,
        standing,
        (act.identity,),
        locality_identity=locality_identity,
    )
    result = _record_byte_pair_occurrence_position_measurement_result_from_carried_act_evidence(
        ledger,
        responsible_act_evidence=act,
        responsibility_assignment=assignment,
        finding=finding,
    )
    standing = _carry_byte_pair_occurrence_position_measurement_result_into_standing(
        standing,
        result,
        prior_through_event_occurrence_identity=act.identity,
    )
    return standing, result


def _record_direct_measurement(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    source_ingest_occurrence_identity: str,
) -> tuple[dict[str, Any], Event]:
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
    )
    if finding.source_locality_identity != locality_identity:
        raise ValueError("direct Measurement subject belongs to another Locality")
    assignment = _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_carried_finding(
        ledger,
        finding=finding,
        locality_standing=standing,
    )
    return _complete_direct_measurement(
        ledger, standing, locality_identity, assignment, finding
    )


def _record_direct_measurement_from_current(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    source_ingest_occurrence_identity: str,
) -> tuple[dict[str, Any], Event]:
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
    )
    if finding.source_locality_identity != locality_identity:
        raise ValueError("direct Measurement subject belongs to another Locality")
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
        locality_standing=standing,
    )
    return _complete_direct_measurement(
        ledger, standing, locality_identity, assignment, finding
    )


def _byte_assignment_source_sets(
    ledger: EventLedger, locality_identity: str
) -> set[tuple[str, ...]]:
    source_sets: set[tuple[str, ...]] = set()
    for assignment in ledger.iter_locality_kind(
        locality_identity, BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    ):
        references = assignment.material.get("source_occurrence_references")
        if (
            ledger.integrity_of(assignment.identity) == CORRUPTED
            or type(references) is not list
        ):
            raise ValueError("recorded byte Measurement assignment is malformed")
        identities = []
        for reference in references:
            if (
                type(reference) is not dict
                or set(reference) != {"ingest_occurrence_identity"}
                or type(reference["ingest_occurrence_identity"]) is not str
                or not reference["ingest_occurrence_identity"]
            ):
                raise ValueError("recorded byte Measurement source is malformed")
            identities.append(reference["ingest_occurrence_identity"])
        source_sets.add(tuple(identities))
    return source_sets


def _discover_byte_measurement(
    ledger: EventLedger, standing: dict[str, Any], locality_identity: str
) -> str | None:
    current_sources = _ingest_identities(standing)
    if not current_sources:
        return None
    if current_sources in _byte_assignment_source_sets(ledger, locality_identity):
        return None
    return current_sources[-1]


def _complete_byte_measurement(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    assignment: Event,
) -> tuple[dict[str, Any], Event]:
    prior_boundary = standing["through_event_occurrence_identity"]
    standing = _carry_byte_measurement_assignment_into_standing(
        ledger,
        standing,
        assignment,
        prior_through_event_occurrence_identity=prior_boundary,
    )
    act = _record_byte_measurement_responsible_act_evidence_from_carried_standing(
        ledger,
        responsibility_assignment=assignment,
        responsibility_assignment_standing=standing,
    )
    standing = _advance(
        ledger,
        standing,
        (act.identity,),
        locality_identity=locality_identity,
    )
    result = _record_byte_measurement_result_from_carried_act_evidence(
        ledger,
        responsible_act_evidence=act,
        responsibility_assignment=assignment,
        locality_standing=standing,
    )
    standing = _advance(
        ledger,
        standing,
        (
            result.material["evidence_of_yield_relation_identity"],
            result.identity,
        ),
        locality_identity=locality_identity,
    )
    return standing, result


def _record_byte_measurement(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    _subject_identity: str,
) -> tuple[dict[str, Any], Event]:
    result, _source, standing = (
        _record_byte_measurement_lifecycle_from_carried_standing(
            ledger,
            source_localities=(locality_identity,),
            recording_locality_identity=locality_identity,
            locality_standing=standing,
        )
    )
    return standing, result


def _record_byte_measurement_from_current(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    _subject_identity: str,
) -> tuple[dict[str, Any], Event]:
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
        locality_standing=standing,
    )
    return _complete_byte_measurement(
        ledger, standing, locality_identity, assignment
    )


def _discover_addressed_material_coordinate_measurement(
    ledger: EventLedger, standing: dict[str, Any], locality_identity: str
) -> str | None:
    measurements = standing["measurement_occurrences"]
    for occurrence_identity in measurements:
        event = ledger.get(occurrence_identity)
        if event is None or event.kind != ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND:
            continue
        if (
            ledger.integrity_of(event.identity) == CORRUPTED
            or event.exact_material is not None
            or measurements[occurrence_identity]
            != _addressed_byte_reference_result_reference(event)
        ):
            raise ValueError("current Standing carries an inexact addressed result")
        if _d2_subject_was_emitted_by_addressed_material(
            ledger,
            standing=standing,
            determination_result=event,
        ):
            continue
        population = _addressed_material_population_references(
            ledger,
            standing,
            locality_identity=locality_identity,
        )
        partial = _addressed_material_incomplete_assignment(
            ledger,
            locality_identity=locality_identity,
            addressed_result_identity=occurrence_identity,
            population=population,
        )
        if partial is not None:
            return StandingMeasurementResponsibilityLifecyclePrefix(
                occurrence_identity, partial.identity
            )
        if _addressed_material_subject_is_unmeasured(
                ledger,
                locality_identity=locality_identity,
                addressed_result_identity=occurrence_identity,
                population=population,
            ):
            return occurrence_identity
    return None


def _record_addressed_material_coordinate_measurement(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    addressed_result_identity: str,
) -> tuple[dict[str, Any], Event]:
    if isinstance(
        addressed_result_identity, StandingMeasurementResponsibilityLifecyclePrefix
    ):
        return _continue_addressed_material_coordinate_measurement_lifecycle(
            ledger,
            responsibility_assignment_event_identity=(
                addressed_result_identity.assignment_event_identity
            ),
            locality_standing=standing,
        )
    population = _addressed_material_population_references(
        ledger, standing, locality_identity=locality_identity
    )
    partial = _addressed_material_incomplete_assignment(
        ledger,
        locality_identity=locality_identity,
        addressed_result_identity=addressed_result_identity,
        population=population,
    )
    if partial is not None:
        return _continue_addressed_material_coordinate_measurement_lifecycle(
            ledger,
            responsibility_assignment_event_identity=partial.identity,
            locality_standing=standing,
        )
    return _record_addressed_material_coordinate_measurement_lifecycle_from_carried_standing(
        ledger,
        addressed_determination_result_event_identity=addressed_result_identity,
        locality_standing=standing,
    )


def _record_addressed_material_coordinate_measurement_from_current(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    addressed_result_identity: str,
) -> tuple[dict[str, Any], Event]:
    if isinstance(
        addressed_result_identity, StandingMeasurementResponsibilityLifecyclePrefix
    ):
        return _record_addressed_material_coordinate_measurement(
            ledger, standing, locality_identity, addressed_result_identity
        )
    _require_current_pin(ledger, standing, locality_identity=locality_identity)
    return _record_addressed_material_coordinate_measurement(
        ledger, standing, locality_identity, addressed_result_identity
    )


def _d2_subject_key(material: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    direct = material.get("direct_pair_position_result_reference")
    coordinate = material.get("addressed_source_byte_position_coordinate_reference")
    identity = (
        direct.get("recorded_occurrence_identity")
        if type(direct) is dict
        else None
    )
    if type(identity) is not str or not identity or type(coordinate) is not dict:
        raise ValueError("recorded D.2 subject is malformed")
    return identity, coordinate


def _d2_subject_was_emitted_by_addressed_material(
    ledger: EventLedger,
    *,
    standing: dict[str, Any],
    determination_result: Event,
) -> bool:
    assignment_reference = determination_result.material.get(
        "responsibility_assignment_reference"
    )
    assignment_identity = (
        assignment_reference.get("recorded_occurrence_identity")
        if type(assignment_reference) is dict
        else None
    )
    assignment = ledger.get(assignment_identity)
    if (
        assignment is None
        or assignment.kind != ADDRESSED_BYTE_REFERENCE_ASSIGNMENT_KIND
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ValueError("recorded D.2 assignment provenance is malformed")
    source_reference_for_standing_measurement_responsibility_order = assignment.material.get(
        SOURCE_REFERENCE_FOR_STANDING_MEASUREMENT_RESPONSIBILITY_ORDER_COORDINATE
    )
    if source_reference_for_standing_measurement_responsibility_order is None:
        return False
    result_reference = (
        source_reference_for_standing_measurement_responsibility_order.get("measurement_result_reference")
        if type(source_reference_for_standing_measurement_responsibility_order) is dict
        else None
    )
    result_identity = (
        result_reference.get("recorded_occurrence_identity")
        if type(result_reference) is dict
        else None
    )
    result = ledger.get(result_identity)
    if (
        type(source_reference_for_standing_measurement_responsibility_order) is not dict
        or set(source_reference_for_standing_measurement_responsibility_order)
        != {"measurement_result_reference", "finding"}
        or result is None
        or result.kind != ADDRESSED_MATERIAL_COORDINATE_RESULT_KIND
        or ledger.integrity_of(result.identity) == CORRUPTED
        or result_reference != _addressed_material_result_reference(result)
        or standing["measurement_occurrences"].get(result.identity)
        != _addressed_material_result_reference(result)
    ):
        raise ValueError(
            "recorded D.2 Measurement order source provenance is malformed"
        )
    return True


def _d2_subject_is_unassigned(
    ledger: EventLedger,
    *,
    locality_identity: str,
    subject: AddressedCoordinateSubjectForStandingMeasurementResponsibilityOrder,
) -> bool:
    expected = (
        subject.direct_result_event_identity,
        subject.source_position_coordinate_reference,
    )
    for kind in (
        ADDRESSED_BYTE_REFERENCE_ASSIGNMENT_KIND,
        ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND,
    ):
        for event in ledger.iter_locality_kind(locality_identity, kind):
            if ledger.integrity_of(event.identity) == CORRUPTED:
                raise ValueError("recorded D.2 history is corrupted")
            if _d2_subject_key(event.material) == expected:
                return False
    return True


def _discover_d2_from_addressed_material_coordinate(
    ledger: EventLedger, standing: dict[str, Any], locality_identity: str
) -> AddressedCoordinateSubjectForStandingMeasurementResponsibilityOrder | None:
    for occurrence_identity in standing["measurement_occurrences"]:
        event = ledger.get(occurrence_identity)
        if event is None or event.kind != ADDRESSED_MATERIAL_COORDINATE_RESULT_KIND:
            continue
        findings = event.material.get("ordered_source_position_coordinate_findings")
        if (
            ledger.integrity_of(event.identity) == CORRUPTED
            or event.exact_material is not None
            or standing["measurement_occurrences"].get(event.identity)
            != _addressed_material_result_reference(event)
            or type(findings) is not list
        ):
            raise ValueError("current Standing carries a malformed addressed-material result")
        for finding in findings:
            direct = (
                finding.get("direct_pair_position_result_reference")
                if type(finding) is dict
                else None
            )
            coordinate = (
                finding.get("source_position_coordinate_reference")
                if type(finding) is dict
                else None
            )
            direct_identity = (
                direct.get("recorded_occurrence_identity")
                if type(direct) is dict
                else None
            )
            if (
                type(direct_identity) is not str
                or not direct_identity
                or type(coordinate) is not dict
            ):
                raise ValueError("current Standing carries a malformed addressed-material finding")
            subject = AddressedCoordinateSubjectForStandingMeasurementResponsibilityOrder(
                direct_identity,
                deepcopy(coordinate),
                event.identity,
                deepcopy(finding),
            )
            partial = _incomplete_determination_assignment_for_subject(
                ledger,
                locality_identity=locality_identity,
                direct_result_event_identity=direct_identity,
                addressed_source_byte_position_coordinate_reference=coordinate,
            )
            if partial is not None:
                return StandingMeasurementResponsibilityLifecyclePrefix(
                    subject, partial.identity
                )
            if _d2_subject_is_unassigned(
                ledger,
                locality_identity=locality_identity,
                subject=subject,
            ):
                return subject
    return None


def _record_d2_from_addressed_material_coordinate(
    ledger: EventLedger,
    standing: dict[str, Any],
    _locality_identity: str,
    subject: AddressedCoordinateSubjectForStandingMeasurementResponsibilityOrder,
) -> tuple[dict[str, Any], Event]:
    if isinstance(subject, StandingMeasurementResponsibilityLifecyclePrefix):
        return _continue_addressed_byte_occurrence_reference_determination_lifecycle(
            ledger,
            responsibility_assignment_event_identity=subject.assignment_event_identity,
            locality_standing=standing,
        )
    return _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing(
        ledger,
        direct_result_event_identity=subject.direct_result_event_identity,
        addressed_source_byte_position_coordinate_reference=(
            subject.source_position_coordinate_reference
        ),
        locality_standing=standing,
        source_reference_for_standing_measurement_responsibility_order={
            "measurement_result_reference": _addressed_material_result_reference(
                ledger.get(subject.trigger_result_event_identity)
            ),
            "finding": deepcopy(subject.trigger_finding),
        },
    )


def _shared_position_subject_is_unassigned(
    ledger: EventLedger,
    *,
    locality_identity: str,
    determination_result_identity: str,
) -> bool:
    for event in ledger.iter_locality_kind(
        locality_identity, SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND
    ):
        if ledger.integrity_of(event.identity) == CORRUPTED:
            raise ValueError("recorded shared-position history is corrupted")
        reference = event.material.get(D2_RESULT_REFERENCE_COORDINATE)
        if reference is None:
            continue
        if type(reference) is not dict:
            raise ValueError("recorded shared-position D.2 reference is malformed")
        identity = reference.get("recorded_occurrence_identity")
        if type(identity) is not str or not identity:
            raise ValueError("recorded shared-position D.2 reference is malformed")
        if identity == determination_result_identity:
            return False
    return True


def _discover_shared_position_from_d2_result(
    ledger: EventLedger, standing: dict[str, Any], locality_identity: str
) -> str | None:
    for occurrence_identity in standing["measurement_occurrences"]:
        event = ledger.get(occurrence_identity)
        if event is None or event.kind != ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND:
            continue
        references = event.material.get("ordered_assertion_references")
        if (
            ledger.integrity_of(event.identity) == CORRUPTED
            or event.exact_material is not None
            or standing["measurement_occurrences"].get(event.identity)
            != _addressed_byte_reference_result_reference(event)
            or type(references) is not list
        ):
            raise ValueError("current Standing carries a malformed D.2 result")
        if len(references) != 2:
            continue
        partial = _incomplete_shared_position_assignment_for_determination(
            ledger,
            locality_identity=locality_identity,
            determination_result_event_identity=event.identity,
        )
        if partial is not None:
            return StandingMeasurementResponsibilityLifecyclePrefix(
                event.identity, partial.identity
            )
        if _shared_position_subject_is_unassigned(
            ledger,
            locality_identity=locality_identity,
            determination_result_identity=event.identity,
        ):
            return event.identity
    return None


def _record_shared_position_from_d2_result(
    ledger: EventLedger,
    standing: dict[str, Any],
    _locality_identity: str,
    determination_result_identity: str,
) -> tuple[dict[str, Any], Event]:
    if isinstance(
        determination_result_identity,
        StandingMeasurementResponsibilityLifecyclePrefix,
    ):
        return _continue_shared_position_measurement_lifecycle(
            ledger,
            responsibility_assignment_event_identity=(
                determination_result_identity.assignment_event_identity
            ),
            locality_standing=standing,
        )
    return _record_shared_position_measurement_lifecycle_from_carried_d2_result(
        ledger,
        determination_result_event_identity=determination_result_identity,
        locality_standing=standing,
    )


STANDING_MEASUREMENT_RESPONSIBILITY_ORDER = (
    StandingMeasurementResponsibilityOrderCoordinate(
        0,
        "01.Source.D",
        "measurement_of_position_coordinates_of_byte_pair_occurrences",
        BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        _discover_direct_measurement,
        _record_direct_measurement,
        _record_direct_measurement_from_current,
    ),
    StandingMeasurementResponsibilityOrderCoordinate(
        1,
        "01.Source.D",
        "measurement_of_exact_byte_occurrences",
        BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        BYTE_MEASUREMENT_RECORDED_KIND,
        _discover_byte_measurement,
        _record_byte_measurement,
        _record_byte_measurement_from_current,
    ),
    StandingMeasurementResponsibilityOrderCoordinate(
        2,
        "01.Source.D",
        "measurement_of_source_position_coordinates_carrying_addressed_material",
        ADDRESSED_MATERIAL_COORDINATE_ASSIGNMENT_KIND,
        ADDRESSED_MATERIAL_COORDINATE_RESULT_KIND,
        _discover_addressed_material_coordinate_measurement,
        _record_addressed_material_coordinate_measurement,
        _record_addressed_material_coordinate_measurement_from_current,
    ),
    StandingMeasurementResponsibilityOrderCoordinate(
        3,
        "01.Source.D.2",
        "addressed_byte_occurrence_reference_determination",
        ADDRESSED_BYTE_REFERENCE_ASSIGNMENT_KIND,
        ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND,
        _discover_d2_from_addressed_material_coordinate,
        _record_d2_from_addressed_material_coordinate,
        _record_d2_from_addressed_material_coordinate,
    ),
    StandingMeasurementResponsibilityOrderCoordinate(
        4,
        "01.Source.D",
        "measurement_of_shared_position_of_byte_pair_occurrences",
        SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
        SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        _discover_shared_position_from_d2_result,
        _record_shared_position_from_d2_result,
        _record_shared_position_from_d2_result,
    ),
)


def _record_measurements_in_standing_measurement_responsibility_order_from_carried_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    *,
    locality_identity: str,
) -> RecordedMeasurementsInStandingMeasurementResponsibilityOrder:
    """Record each Responsibility in the order at its exact Standing boundary."""

    standing = locality_standing
    results: list[Event] = []
    while True:
        _require_current_pin(
            ledger,
            standing,
            locality_identity=locality_identity,
        )
        eligible = []
        for responsibility_coordinate in STANDING_MEASUREMENT_RESPONSIBILITY_ORDER:
            subject = responsibility_coordinate.discover(
                ledger, standing, locality_identity
            )
            if subject is not None:
                eligible.append(
                    (
                        responsibility_coordinate.order,
                        subject,
                        responsibility_coordinate,
                    )
                )
        if not eligible:
            return RecordedMeasurementsInStandingMeasurementResponsibilityOrder(standing, tuple(results))
        _order, subject, responsibility_coordinate = min(
            eligible,
            key=lambda item: (
                0
                if isinstance(
                    item[1], StandingMeasurementResponsibilityLifecyclePrefix
                )
                else 1,
                item[0],
            ),
        )
        standing, result = responsibility_coordinate.record(
            ledger,
            standing,
            locality_identity,
            subject,
        )
        if result.kind != responsibility_coordinate.result_kind:
            raise ValueError(
                "a Measurement in the Standing Measurement Responsibility order "
                "recorded another result kind"
            )
        results.append(result)


def record_measurements_in_standing_measurement_responsibility_order_from_current_standing(
    ledger: EventLedger,
    *,
    locality_identity: str,
) -> RecordedMeasurementsInStandingMeasurementResponsibilityOrder:
    """Read current Standing and record Measurements in its Responsibility order."""

    standing = read_operator_locality_standing(
        ledger,
        locality_identity=locality_identity,
    )
    eligible = []
    for responsibility_coordinate in STANDING_MEASUREMENT_RESPONSIBILITY_ORDER:
        subject = responsibility_coordinate.discover(
            ledger, standing, locality_identity
        )
        if subject is not None:
            eligible.append(
                (
                    responsibility_coordinate.order,
                    subject,
                    responsibility_coordinate,
                )
            )
    if not eligible:
        return RecordedMeasurementsInStandingMeasurementResponsibilityOrder(standing, ())
    _order, subject, responsibility_coordinate = min(
        eligible,
        key=lambda item: (
            0
            if isinstance(item[1], StandingMeasurementResponsibilityLifecyclePrefix)
            else 1,
            item[0],
        ),
    )
    standing, result = responsibility_coordinate.record_from_current(
        ledger,
        standing,
        locality_identity,
        subject,
    )
    remaining = _record_measurements_in_standing_measurement_responsibility_order_from_carried_standing(
        ledger,
        standing,
        locality_identity=locality_identity,
    )
    return RecordedMeasurementsInStandingMeasurementResponsibilityOrder(
        remaining.locality_standing,
        (result, *remaining.result_occurrences),
    )
