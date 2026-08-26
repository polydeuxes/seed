"""Record all declared Measurement subjects through B.

Each declaration names one existing Book-assigned Measurement Responsibility.
All subjects are recovered once from one exact bounded
Locality replay.  Each assignment preserves that same responsible boundary;
durable writes remain serial without making an earlier Measurement lifecycle
an input to a later assignment.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, NamedTuple

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    _record_byte_measurement_subject_to_act_binding_from_through_event_occurrence,
    _record_byte_measurement_act_occurrence_from_carried_coordinates,
    _record_byte_measurement_result_from_carried_act_occurrence,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _record_byte_pair_occurrence_position_measurement_act_occurrence_from_carried_assignment,
    _record_byte_pair_occurrence_position_measurement_subject_to_act_binding_from_responsibility_boundary,
    _record_byte_pair_occurrence_position_measurement_result_from_carried_act_occurrence,
    _material_acquisition_identities_with_exact_locality_from_bounded_replay,
    _unassigned_position_coordinate_measurement_acquisition_results_from_bounded_locality_replay,
    measure_position_coordinates_of_byte_pair_occurrences,
)
from seed_runtime.operator_locality_standing import (
    _carry_byte_measurement_binding_into_current_coordinates,
    _carry_byte_pair_occurrence_position_measurement_assignment_into_standing,
    _carry_byte_pair_occurrence_position_measurement_result_into_standing,
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
# The source-position proof remains explicitly invoked. Importing its first and
# later Measurements keeps the current runtime road reachable without
# pretending they are automatic declarations in the registry below.
from seed_runtime.source_position_recurrence import (
    record_corresponding_coordinate_material_measurements,
    record_source_position_measurements,
)


@dataclass(frozen=True)
class PositionCoordinateMeasurementSubject:
    source_material_result_occurrence_identity: str


@dataclass(frozen=True)
class ExactByteOccurrenceMeasurementSubject:
    source_material_result_occurrence_identities: tuple[str, ...]


DeclaredMeasurementSubject = (
    PositionCoordinateMeasurementSubject | ExactByteOccurrenceMeasurementSubject
)


class DeclaredMeasurementResponsibility(NamedTuple):
    book_clause_identity: str
    measurement_identity: str
    assignment_kind: str
    result_kind: str
    discover: Callable[
        [EventLedger, dict[str, Any], str], tuple[DeclaredMeasurementSubject, ...]
    ]
    record: Callable[
        [
            EventLedger,
            dict[str, Any],
            dict[str, Any],
            str,
            DeclaredMeasurementSubject,
        ],
        tuple[dict[str, Any], Event],
    ]


class RecordedDeclaredMeasurements(NamedTuple):
    bounded_locality_replay: dict[str, Any]
    result_occurrences: tuple[Event, ...]


def _advance(
    ledger: EventLedger,
    recording_replay: dict[str, Any],
    event_identities: tuple[str, ...],
    *,
    locality_identity: str,
) -> dict[str, Any]:
    return advance_operator_locality_standing(
        ledger,
        event_identities,
        locality_identity=locality_identity,
        prior=recording_replay,
    )


def _require_current_replay_boundary(
    ledger: EventLedger,
    bounded_locality_replay: dict[str, Any],
    *,
    locality_identity: str,
) -> None:
    if (
        not isinstance(ledger, EventLedger)
        or type(locality_identity) is not str
        or not locality_identity
        or type(bounded_locality_replay) is not dict
        or bounded_locality_replay.get("locality_identity") != locality_identity
        or type(
            bounded_locality_replay.get(
                "material_result_occurrences"
            )
        )
        is not list
        or type(bounded_locality_replay.get("measurement_occurrences")) is not dict
        or type(
            bounded_locality_replay.get("subject_to_act_binding_occurrences")
        )
        is not dict
    ):
        raise ValueError(
            "declared Measurement recording requires exact current bounded "
            "Locality replay"
        )
    boundary = bounded_locality_replay.get("through_event_occurrence_identity")
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
            "declared Measurement recording requires the current bounded "
            "Locality replay boundary"
        )


def _material_acquisition_identities(
    bounded_locality_replay: dict[str, Any],
) -> tuple[str, ...]:
    return _material_acquisition_identities_with_exact_locality_from_bounded_replay(
        bounded_locality_replay
    )


def _discover_direct_measurements(
    ledger: EventLedger,
    bounded_locality_replay: dict[str, Any],
    locality_identity: str,
) -> tuple[PositionCoordinateMeasurementSubject, ...]:
    sources = _unassigned_position_coordinate_measurement_acquisition_results_from_bounded_locality_replay(
        ledger,
        bounded_locality_replay,
        locality_identity=locality_identity,
    )
    return tuple(
        PositionCoordinateMeasurementSubject(
            source.source_material_result_occurrence_identity
        )
        for source in sources
    )


def _complete_direct_measurement(
    ledger: EventLedger,
    recording_replay: dict[str, Any],
    locality_identity: str,
    assignment: Event,
    finding,
) -> tuple[dict[str, Any], Event]:
    prior_boundary = recording_replay["through_event_occurrence_identity"]
    recording_replay = (
        _carry_byte_pair_occurrence_position_measurement_assignment_into_standing(
            ledger,
            recording_replay,
            assignment,
            finding,
            prior_through_event_occurrence_identity=prior_boundary,
        )
    )
    act = _record_byte_pair_occurrence_position_measurement_act_occurrence_from_carried_assignment(
        ledger,
        responsibility_assignment=assignment,
        finding=finding,
        responsibility_assignment_standing=recording_replay,
    )
    recording_replay = _advance(
        ledger,
        recording_replay,
        (act.identity,),
        locality_identity=locality_identity,
    )
    result = _record_byte_pair_occurrence_position_measurement_result_from_carried_act_occurrence(
        ledger,
        act_occurrence=act,
        responsibility_assignment=assignment,
        finding=finding,
    )
    recording_replay = (
        _carry_byte_pair_occurrence_position_measurement_result_into_standing(
            recording_replay,
            result,
            prior_through_event_occurrence_identity=act.identity,
        )
    )
    return recording_replay, result


def _record_direct_measurement(
    ledger: EventLedger,
    recording_replay: dict[str, Any],
    responsibility_boundary_replay: dict[str, Any],
    locality_identity: str,
    subject: DeclaredMeasurementSubject,
) -> tuple[dict[str, Any], Event]:
    if type(subject) is not PositionCoordinateMeasurementSubject:
        raise ValueError("position-coordinate Measurement requires its exact subject")
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_material_result_occurrence_identity=(
            subject.source_material_result_occurrence_identity
        ),
    )
    if finding.source_locality_identity != locality_identity:
        raise ValueError("direct Measurement subject belongs to another Locality")
    responsibility_boundary_identity = responsibility_boundary_replay.get(
        "through_event_occurrence_identity"
    )
    assignment = _record_byte_pair_occurrence_position_measurement_subject_to_act_binding_from_responsibility_boundary(
        ledger,
        finding=finding,
        responsibility_boundary_identity=responsibility_boundary_identity,
    )
    return _complete_direct_measurement(
        ledger, recording_replay, locality_identity, assignment, finding
    )


def _byte_assignment_source_sets(
    ledger: EventLedger, locality_identity: str
) -> set[tuple[str, ...]]:
    source_sets: set[tuple[str, ...]] = set()
    for assignment in ledger.iter_locality_kind(
        locality_identity, BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
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
                or set(reference) != {"material_result_occurrence_identity"}
                or type(reference["material_result_occurrence_identity"]) is not str
                or not reference["material_result_occurrence_identity"]
            ):
                raise ValueError("recorded byte Measurement source is malformed")
            identities.append(reference["material_result_occurrence_identity"])
        source_sets.add(tuple(identities))
    return source_sets


def _discover_byte_measurements(
    ledger: EventLedger,
    bounded_locality_replay: dict[str, Any],
    locality_identity: str,
) -> tuple[ExactByteOccurrenceMeasurementSubject, ...]:
    current_sources = _material_acquisition_identities(bounded_locality_replay)
    if not current_sources:
        return ()
    if current_sources in _byte_assignment_source_sets(ledger, locality_identity):
        return ()
    return (ExactByteOccurrenceMeasurementSubject(current_sources),)


def _require_exact_byte_occurrence_measurement_subject(
    ledger: EventLedger,
    bounded_locality_replay: dict[str, Any],
    subject: DeclaredMeasurementSubject,
) -> tuple[str, ...]:
    if type(subject) is not ExactByteOccurrenceMeasurementSubject:
        raise ValueError("exact-byte Measurement requires its exact subject")
    current_sources = _material_acquisition_identities(bounded_locality_replay)
    if subject.source_material_result_occurrence_identities != current_sources:
        raise ValueError(
            "exact-byte Measurement subject differs from the current acquisition-result set"
        )
    return current_sources


def _complete_byte_measurement(
    ledger: EventLedger,
    recording_replay: dict[str, Any],
    locality_identity: str,
    binding: Event,
    through_occurrence_coordinates: dict[str, Any],
) -> tuple[dict[str, Any], Event]:
    prior_boundary = recording_replay["through_event_occurrence_identity"]
    recording_replay = _carry_byte_measurement_binding_into_current_coordinates(
        ledger,
        recording_replay,
        binding,
        prior_through_event_occurrence_identity=prior_boundary,
        through_occurrence_coordinates=through_occurrence_coordinates,
    )
    act = _record_byte_measurement_act_occurrence_from_carried_coordinates(
        ledger,
        subject_to_act_binding=binding,
        current_coordinates=recording_replay,
    )
    recording_replay = _advance(
        ledger,
        recording_replay,
        (act.identity,),
        locality_identity=locality_identity,
    )
    result = _record_byte_measurement_result_from_carried_act_occurrence(
        ledger,
        act_occurrence=act,
        subject_to_act_binding=binding,
        current_coordinates=recording_replay,
    )
    recording_replay = _advance(
        ledger,
        recording_replay,
        (
            result.material["yield_relation_identity"],
            result.identity,
        ),
        locality_identity=locality_identity,
    )
    return recording_replay, result


def _record_byte_measurement(
    ledger: EventLedger,
    recording_replay: dict[str, Any],
    responsibility_boundary_replay: dict[str, Any],
    locality_identity: str,
    subject: DeclaredMeasurementSubject,
) -> tuple[dict[str, Any], Event]:
    _require_exact_byte_occurrence_measurement_subject(
        ledger, responsibility_boundary_replay, subject
    )
    responsibility_boundary_identity = responsibility_boundary_replay.get(
        "through_event_occurrence_identity"
    )
    assignment = _record_byte_measurement_subject_to_act_binding_from_through_event_occurrence(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
        through_event_occurrence_identity=responsibility_boundary_identity,
    )
    return _complete_byte_measurement(
        ledger,
        recording_replay,
        locality_identity,
        assignment,
        responsibility_boundary_replay,
    )


DECLARED_MEASUREMENT_RESPONSIBILITIES = (
    DeclaredMeasurementResponsibility(
        "01.Source.D",
        "measurement_of_position_coordinates_of_byte_pair_occurrences",
        BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        _discover_direct_measurements,
        _record_direct_measurement,
    ),
    DeclaredMeasurementResponsibility(
        "01.Source.D",
        "measurement_of_exact_byte_occurrences",
        BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        BYTE_MEASUREMENT_RECORDED_KIND,
        _discover_byte_measurements,
        _record_byte_measurement,
    ),
)


def _record_declared_measurements_from_carried_bounded_locality_replay(
    ledger: EventLedger,
    bounded_locality_replay: dict[str, Any],
    *,
    locality_identity: str,
) -> RecordedDeclaredMeasurements:
    """Record every exact subject recovered at one responsible boundary."""

    responsibility_boundary_replay = bounded_locality_replay
    recording_replay = deepcopy(bounded_locality_replay)
    results: list[Event] = []
    _require_current_replay_boundary(
        ledger,
        responsibility_boundary_replay,
        locality_identity=locality_identity,
    )
    complete_subjects = tuple(
        (declaration, subject)
        for declaration in DECLARED_MEASUREMENT_RESPONSIBILITIES
        for subject in declaration.discover(
            ledger,
            responsibility_boundary_replay,
            locality_identity,
        )
    )
    for declaration, subject in complete_subjects:
        _require_current_replay_boundary(
            ledger,
            recording_replay,
            locality_identity=locality_identity,
        )
        recording_replay, result = declaration.record(
            ledger,
            recording_replay,
            responsibility_boundary_replay,
            locality_identity,
            subject,
        )
        if result.kind != declaration.result_kind:
            raise ValueError("declared Measurement recorded another result kind")
        results.append(result)
    return RecordedDeclaredMeasurements(recording_replay, tuple(results))


def record_declared_measurements_from_current_bounded_locality_replay(
    ledger: EventLedger,
    *,
    locality_identity: str,
) -> RecordedDeclaredMeasurements:
    """Read one bounded Locality replay and record all exact subjects."""

    bounded_locality_replay = read_operator_locality_standing(
        ledger,
        locality_identity=locality_identity,
    )
    return _record_declared_measurements_from_carried_bounded_locality_replay(
        ledger,
        bounded_locality_replay,
        locality_identity=locality_identity,
    )
