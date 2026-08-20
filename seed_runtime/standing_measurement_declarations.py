"""Record declared Measurements whose exact subjects are carried in Standing.

The declarations in this module do not assign a new Responsibility.  Each
entry names one existing Book-assigned Measurement road.  Each road recovers
its own exact subject at one current Standing boundary, records its own
assignment, Act, Yield, and result, and Standing is advanced before discovery
continues.

Ledger writes remain serial and deterministic.  A later implementation may
compute pure discovery findings concurrently, but no two Measurement occurrences
may be appended from one stale Standing boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, NamedTuple

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    _record_byte_measurement_responsibility_assignment_from_carried_standing,
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
    _unassigned_position_coordinate_measurement_acquisition_results_from_bounded_locality_replay,
    measure_position_coordinates_of_byte_pair_occurrences,
    record_byte_pair_occurrence_position_measurement_responsibility_assignment,
)
from seed_runtime.material_acquisition import read_exact_material_acquisition_result
from seed_runtime.operator_locality_standing import (
    _carry_byte_measurement_assignment_into_standing,
    _carry_byte_pair_occurrence_position_measurement_assignment_into_standing,
    _carry_byte_pair_occurrence_position_measurement_result_into_standing,
    advance_operator_locality_standing,
    read_operator_locality_standing,
)


@dataclass(frozen=True)
class PositionCoordinateMeasurementSubject:
    source_material_acquisition_occurrence_identity: str


@dataclass(frozen=True)
class ExactByteOccurrenceMeasurementSubject:
    source_material_acquisition_occurrence_identities: tuple[str, ...]


DeclaredMeasurementSubject = (
    PositionCoordinateMeasurementSubject | ExactByteOccurrenceMeasurementSubject
)


class StandingMeasurementDeclaration(NamedTuple):
    order: int
    book_clause_identity: str
    assignment_kind: str
    result_kind: str
    discover: Callable[
        [EventLedger, dict[str, Any], str], DeclaredMeasurementSubject | None
    ]
    record: Callable[
        [EventLedger, dict[str, Any], str, DeclaredMeasurementSubject],
        tuple[dict[str, Any], Event],
    ]
    record_from_current: Callable[
        [EventLedger, dict[str, Any], str, DeclaredMeasurementSubject],
        tuple[dict[str, Any], Event],
    ]


class RecordedStandingMeasurements(NamedTuple):
    locality_standing: dict[str, Any]
    result_occurrences: tuple[Event, ...]


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
        or type(standing.get("material_acquisition_result_occurrences")) is not list
        or type(standing.get("measurement_occurrences")) is not dict
        or type(standing.get("responsibility_assignment_occurrences")) is not dict
    ):
        raise ValueError("declared Measurement recording requires exact current Standing")
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
        raise ValueError("declared Measurement recording requires current Locality Standing")


def _material_acquisition_identities(
    ledger: EventLedger, bounded_locality_replay: dict[str, Any]
) -> tuple[str, ...]:
    from seed_runtime.operator_material_acquisition import (
        read_operator_material_acquire_locality_relation_requirements,
    )

    identities = []
    for occurrence in bounded_locality_replay[
        "material_acquisition_result_occurrences"
    ]:
        if (
            type(occurrence) is not dict
            or type(occurrence.get("result_occurrence_identity")) is not str
            or not occurrence["result_occurrence_identity"]
        ):
            raise ValueError(
                "bounded Locality replay contains a malformed material acquisition result"
            )
        identity = occurrence["result_occurrence_identity"]
        if all(
            read_operator_material_acquire_locality_relation_requirements(
                ledger,
                recorded_result_event_identity=identity,
            ).values()
        ):
            identities.append(identity)
    return tuple(identities)


def _discover_direct_measurement(
    ledger: EventLedger, standing: dict[str, Any], locality_identity: str
) -> PositionCoordinateMeasurementSubject | None:
    sources = _unassigned_position_coordinate_measurement_acquisition_results_from_bounded_locality_replay(
        ledger,
        standing,
        locality_identity=locality_identity,
    )
    if not sources:
        return None
    return PositionCoordinateMeasurementSubject(
        sources[0].source_material_acquisition_occurrence_identity
    )


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
    subject: DeclaredMeasurementSubject,
) -> tuple[dict[str, Any], Event]:
    if type(subject) is not PositionCoordinateMeasurementSubject:
        raise ValueError("position-coordinate Measurement requires its exact subject")
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_material_acquisition_occurrence_identity=(
            subject.source_material_acquisition_occurrence_identity
        ),
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
    subject: DeclaredMeasurementSubject,
) -> tuple[dict[str, Any], Event]:
    if type(subject) is not PositionCoordinateMeasurementSubject:
        raise ValueError("position-coordinate Measurement requires its exact subject")
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_material_acquisition_occurrence_identity=(
            subject.source_material_acquisition_occurrence_identity
        ),
    )
    if finding.source_locality_identity != locality_identity:
        raise ValueError("direct Measurement subject belongs to another Locality")
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_material_acquisition_occurrence_identity=(
            subject.source_material_acquisition_occurrence_identity
        ),
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
                or set(reference) != {"material_acquisition_occurrence_identity"}
                or type(reference["material_acquisition_occurrence_identity"]) is not str
                or not reference["material_acquisition_occurrence_identity"]
            ):
                raise ValueError("recorded byte Measurement source is malformed")
            identities.append(reference["material_acquisition_occurrence_identity"])
        source_sets.add(tuple(identities))
    return source_sets


def _discover_byte_measurement(
    ledger: EventLedger, standing: dict[str, Any], locality_identity: str
) -> ExactByteOccurrenceMeasurementSubject | None:
    current_sources = _material_acquisition_identities(ledger, standing)
    if not current_sources:
        return None
    if current_sources in _byte_assignment_source_sets(ledger, locality_identity):
        return None
    return ExactByteOccurrenceMeasurementSubject(current_sources)


def _require_exact_byte_occurrence_measurement_subject(
    ledger: EventLedger,
    standing: dict[str, Any],
    subject: DeclaredMeasurementSubject,
) -> tuple[str, ...]:
    if type(subject) is not ExactByteOccurrenceMeasurementSubject:
        raise ValueError("exact-byte Measurement requires its exact subject")
    current_sources = _material_acquisition_identities(ledger, standing)
    if subject.source_material_acquisition_occurrence_identities != current_sources:
        raise ValueError(
            "exact-byte Measurement subject differs from the current acquisition-result set"
        )
    return current_sources


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
    subject: DeclaredMeasurementSubject,
) -> tuple[dict[str, Any], Event]:
    _require_exact_byte_occurrence_measurement_subject(ledger, standing, subject)
    assignment = _record_byte_measurement_responsibility_assignment_from_carried_standing(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
        locality_standing=standing,
    )
    return _complete_byte_measurement(
        ledger, standing, locality_identity, assignment
    )


def _record_byte_measurement_from_current(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    subject: DeclaredMeasurementSubject,
) -> tuple[dict[str, Any], Event]:
    _require_exact_byte_occurrence_measurement_subject(ledger, standing, subject)
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
        locality_standing=standing,
    )
    return _complete_byte_measurement(
        ledger, standing, locality_identity, assignment
    )


STANDING_MEASUREMENT_DECLARATIONS = (
    StandingMeasurementDeclaration(
        0,
        "01.Source.D",
        BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        _discover_direct_measurement,
        _record_direct_measurement,
        _record_direct_measurement_from_current,
    ),
    StandingMeasurementDeclaration(
        1,
        "01.Source.D",
        BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        BYTE_MEASUREMENT_RECORDED_KIND,
        _discover_byte_measurement,
        _record_byte_measurement,
        _record_byte_measurement_from_current,
    ),
)


def _record_declared_measurements_from_carried_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    *,
    locality_identity: str,
) -> RecordedStandingMeasurements:
    """Record one lawful declaration per exact Standing boundary until quiet."""

    standing = locality_standing
    results: list[Event] = []
    while True:
        _require_current_pin(
            ledger,
            standing,
            locality_identity=locality_identity,
        )
        eligible = []
        for declaration in STANDING_MEASUREMENT_DECLARATIONS:
            subject = declaration.discover(ledger, standing, locality_identity)
            if subject is not None:
                eligible.append((declaration.order, subject, declaration))
        if not eligible:
            return RecordedStandingMeasurements(standing, tuple(results))
        _order, subject, declaration = min(eligible, key=lambda item: item[:2])
        standing, result = declaration.record(
            ledger,
            standing,
            locality_identity,
            subject,
        )
        if result.kind != declaration.result_kind:
            raise ValueError("declared Measurement recorded another result kind")
        results.append(result)


def record_declared_measurements_from_current_standing(
    ledger: EventLedger,
    *,
    locality_identity: str,
) -> RecordedStandingMeasurements:
    """Read one current Locality Standing and record its declared Measurements."""

    standing = read_operator_locality_standing(
        ledger,
        locality_identity=locality_identity,
    )
    eligible = []
    for declaration in STANDING_MEASUREMENT_DECLARATIONS:
        subject = declaration.discover(ledger, standing, locality_identity)
        if subject is not None:
            eligible.append((declaration.order, subject, declaration))
    if not eligible:
        return RecordedStandingMeasurements(standing, ())
    _order, subject, declaration = min(eligible, key=lambda item: item[:2])
    standing, result = declaration.record_from_current(
        ledger,
        standing,
        locality_identity,
        subject,
    )
    remaining = _record_declared_measurements_from_carried_standing(
        ledger,
        standing,
        locality_identity=locality_identity,
    )
    return RecordedStandingMeasurements(
        remaining.locality_standing,
        (result, *remaining.result_occurrences),
    )
