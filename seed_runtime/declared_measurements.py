"""Record all Measurement subjects declared through B.

All subjects are read once from one exact current-coordinate projection. Each binding
preserves that same through-occurrence boundary; durable writes remain serial
without making an earlier Measurement lifecycle an input to a later binding.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, NamedTuple

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    _record_byte_measurement_subject_to_act_binding_from_through_event_occurrence,
    _record_byte_measurement_act_occurrence_from_current_coordinates,
    _record_byte_measurement_result_from_current_coordinates,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _record_byte_pair_occurrence_position_measurement_act_occurrence_from_carried_binding,
    _record_byte_pair_occurrence_position_measurement_subject_to_act_binding_from_through_event_occurrence,
    _record_byte_pair_occurrence_position_measurement_result_from_carried_act_occurrence,
    _material_result_identities_from_bounded_replay,
    _unbound_position_coordinate_measurement_material_results_from_bounded_locality_replay,
    measure_position_coordinates_of_byte_pair_occurrences,
)
from seed_runtime.comparison_of_shared_position_measurement_with_recorded_pair_findings import (
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
)
from seed_runtime.measurement_of_compare_distinctions import (
    COMPARE_DISTINCTION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND,
    COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
    CompareDistinctionMeasurementSubject,
    _read_binding as _read_compare_distinction_measurement_binding,
    record_compare_distinction_measurement_subject_to_act_binding,
    record_compare_distinction_measurement_act_occurrence,
    record_compare_distinction_measurement_result,
)
from seed_runtime.operator_current_coordinates import (
    _carry_byte_measurement_binding_into_current_coordinates,
    _carry_byte_pair_occurrence_position_measurement_binding_into_current_coordinates,
    _carry_byte_pair_occurrence_position_measurement_result_into_current_coordinates,
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
# This module invokes the source-position proof. Importing its first and later
# Measurements keeps the current runtime road reachable without
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
    PositionCoordinateMeasurementSubject
    | ExactByteOccurrenceMeasurementSubject
    | CompareDistinctionMeasurementSubject
)


class RecordedDeclaredMeasurements(NamedTuple):
    current_coordinates: dict[str, Any]
    result_occurrences: tuple[Event, ...]


def _advance(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event_identities: tuple[str, ...],
    *,
    locality_identity: str,
) -> dict[str, Any]:
    return advance_operator_current_coordinates(
        ledger,
        event_identities,
        locality_identity=locality_identity,
        prior=current_coordinates,
    )


def _require_current_coordinate_boundary(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    *,
    locality_identity: str,
) -> None:
    if (
        not isinstance(ledger, EventLedger)
        or type(locality_identity) is not str
        or not locality_identity
        or type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity") != locality_identity
        or type(
            current_coordinates.get(
                "material_result_occurrences"
            )
        )
        is not list
        or type(current_coordinates.get("measurement_occurrences")) is not dict
        or type(
            current_coordinates.get("subject_to_act_binding_occurrences")
        )
        is not dict
    ):
        raise ValueError(
            "declared Measurement recording requires exact current coordinates"
        )
    boundary = current_coordinates.get("through_event_occurrence_identity")
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
            "declared Measurement recording requires the exact current boundary"
        )


def _material_result_identities(
    current_coordinates: dict[str, Any],
) -> tuple[str, ...]:
    return _material_result_identities_from_bounded_replay(
        current_coordinates
    )


def _discover_direct_measurements(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    locality_identity: str,
) -> tuple[PositionCoordinateMeasurementSubject, ...]:
    sources = _unbound_position_coordinate_measurement_material_results_from_bounded_locality_replay(
        ledger,
        current_coordinates,
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
    current_coordinates: dict[str, Any],
    locality_identity: str,
    binding: Event,
    finding,
) -> tuple[dict[str, Any], Event]:
    prior_boundary = current_coordinates["through_event_occurrence_identity"]
    current_coordinates = (
        _carry_byte_pair_occurrence_position_measurement_binding_into_current_coordinates(
            ledger,
            current_coordinates,
            binding,
            finding,
            prior_through_event_occurrence_identity=prior_boundary,
        )
    )
    act = _record_byte_pair_occurrence_position_measurement_act_occurrence_from_carried_binding(
        ledger,
        binding=binding,
        finding=finding,
        binding_current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(
        ledger,
        current_coordinates,
        (act.identity,),
        locality_identity=locality_identity,
    )
    result = _record_byte_pair_occurrence_position_measurement_result_from_carried_act_occurrence(
        ledger,
        act_occurrence=act,
        binding=binding,
        finding=finding,
    )
    current_coordinates = (
        _carry_byte_pair_occurrence_position_measurement_result_into_current_coordinates(
            ledger,
            current_coordinates,
            result,
            prior_through_event_occurrence_identity=act.identity,
        )
    )
    return current_coordinates, result


def _record_direct_measurement(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    through_occurrence_coordinates: dict[str, Any],
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
    through_event_occurrence_identity = through_occurrence_coordinates.get(
        "through_event_occurrence_identity"
    )
    binding = _record_byte_pair_occurrence_position_measurement_subject_to_act_binding_from_through_event_occurrence(
        ledger,
        finding=finding,
        through_event_occurrence_identity=through_event_occurrence_identity,
    )
    return _complete_direct_measurement(
        ledger, current_coordinates, locality_identity, binding, finding
    )


def _byte_binding_source_sets(
    ledger: EventLedger, locality_identity: str
) -> set[tuple[str, ...]]:
    source_sets: set[tuple[str, ...]] = set()
    for binding in ledger.iter_locality_kind(
        locality_identity, BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    ):
        subject = binding.material.get("subject_reference")
        references = (
            subject.get("source_occurrence_references")
            if type(subject) is dict
            else None
        )
        if (
            ledger.integrity_of(binding.identity) == CORRUPTED
            or type(references) is not list
        ):
            raise ValueError("recorded byte Measurement binding is malformed")
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
    current_coordinates: dict[str, Any],
    locality_identity: str,
) -> tuple[ExactByteOccurrenceMeasurementSubject, ...]:
    current_sources = _material_result_identities(current_coordinates)
    if not current_sources:
        return ()
    if current_sources in _byte_binding_source_sets(ledger, locality_identity):
        return ()
    return (ExactByteOccurrenceMeasurementSubject(current_sources),)


def _require_exact_byte_occurrence_measurement_subject(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    subject: DeclaredMeasurementSubject,
) -> tuple[str, ...]:
    if type(subject) is not ExactByteOccurrenceMeasurementSubject:
        raise ValueError("exact-byte Measurement requires its exact subject")
    current_sources = _material_result_identities(current_coordinates)
    if subject.source_material_result_occurrence_identities != current_sources:
        raise ValueError(
            "exact-byte Measurement subject differs from the current material-result set"
        )
    return current_sources


def _complete_byte_measurement(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    locality_identity: str,
    binding: Event,
    through_occurrence_coordinates: dict[str, Any],
) -> tuple[dict[str, Any], Event]:
    prior_boundary = current_coordinates["through_event_occurrence_identity"]
    current_coordinates = _carry_byte_measurement_binding_into_current_coordinates(
        ledger,
        current_coordinates,
        binding,
        prior_through_event_occurrence_identity=prior_boundary,
        through_occurrence_coordinates=through_occurrence_coordinates,
    )
    act = _record_byte_measurement_act_occurrence_from_current_coordinates(
        ledger,
        subject_to_act_binding=binding,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(
        ledger,
        current_coordinates,
        (act.identity,),
        locality_identity=locality_identity,
    )
    result = _record_byte_measurement_result_from_current_coordinates(
        ledger,
        act_occurrence=act,
        subject_to_act_binding=binding,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(
        ledger,
        current_coordinates,
        (result.identity,),
        locality_identity=locality_identity,
    )
    return current_coordinates, result


def _record_byte_measurement(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    through_occurrence_coordinates: dict[str, Any],
    locality_identity: str,
    subject: DeclaredMeasurementSubject,
) -> tuple[dict[str, Any], Event]:
    _require_exact_byte_occurrence_measurement_subject(
        ledger, through_occurrence_coordinates, subject
    )
    through_event_occurrence_identity = through_occurrence_coordinates.get(
        "through_event_occurrence_identity"
    )
    binding = _record_byte_measurement_subject_to_act_binding_from_through_event_occurrence(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
    )
    return _complete_byte_measurement(
        ledger,
        current_coordinates,
        locality_identity,
        binding,
        through_occurrence_coordinates,
    )


def _discover_compare_distinction_measurements(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    locality_identity: str,
) -> tuple[CompareDistinctionMeasurementSubject, ...]:
    comparisons = current_coordinates.get("comparison_result_occurrences")
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    if type(comparisons) is not dict or type(bindings) is not dict:
        raise ValueError(
            "Compare Distinction Measurement requires exact current coordinates"
        )
    measured = set()
    for occurrence_identity in bindings:
        binding = ledger.get(occurrence_identity)
        if (
            binding is None
            or binding.kind
            != COMPARE_DISTINCTION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND
        ):
            continue
        exact_binding, _distinctions = _read_compare_distinction_measurement_binding(
            ledger,
            binding.identity,
            prior_coordinates=current_coordinates,
        )
        measured.add(
            exact_binding.material["subject_reference"][
                "comparison_result_occurrence_identity"
            ]
        )
    return tuple(
        CompareDistinctionMeasurementSubject(occurrence_identity)
        for occurrence_identity in comparisons
        if occurrence_identity not in measured
        and (
            (source := ledger.get(occurrence_identity)) is not None
            and source.kind
            == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
            and source.locality_identity == locality_identity
            and ledger.integrity_of(source.identity) != CORRUPTED
        )
    )


def _record_compare_distinction_measurement(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    through_occurrence_coordinates: dict[str, Any],
    locality_identity: str,
    subject: DeclaredMeasurementSubject,
) -> tuple[dict[str, Any], Event]:
    if type(subject) is not CompareDistinctionMeasurementSubject:
        raise ValueError("Compare Distinction Measurement requires its exact subject")
    binding = record_compare_distinction_measurement_subject_to_act_binding(
        ledger,
        comparison_result_occurrence_identity=(
            subject.comparison_result_occurrence_identity
        ),
        current_coordinates=current_coordinates,
        through_occurrence_coordinates=through_occurrence_coordinates,
    )
    current_coordinates = _advance(
        ledger,
        current_coordinates,
        (binding.identity,),
        locality_identity=locality_identity,
    )
    act = record_compare_distinction_measurement_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(
        ledger,
        current_coordinates,
        (act.identity,),
        locality_identity=locality_identity,
    )
    result = record_compare_distinction_measurement_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(
        ledger,
        current_coordinates,
        (result.identity,),
        locality_identity=locality_identity,
    )
    return current_coordinates, result


_DECLARED_MEASUREMENTS = (
    (
        COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
        _discover_compare_distinction_measurements,
        _record_compare_distinction_measurement,
    ),
    (
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        _discover_direct_measurements,
        _record_direct_measurement,
    ),
    (
        BYTE_MEASUREMENT_RECORDED_KIND,
        _discover_byte_measurements,
        _record_byte_measurement,
    ),
)


def _record_declared_measurements_from_carried_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    *,
    locality_identity: str,
) -> RecordedDeclaredMeasurements:
    """Record every exact subject carried through one exact occurrence."""

    through_occurrence_coordinates = current_coordinates
    current_coordinates = deepcopy(current_coordinates)
    results: list[Event] = []
    _require_current_coordinate_boundary(
        ledger,
        through_occurrence_coordinates,
        locality_identity=locality_identity,
    )
    complete_subjects = tuple(
        (result_kind, record, subject)
        for result_kind, discover, record in _DECLARED_MEASUREMENTS
        for subject in discover(
            ledger,
            through_occurrence_coordinates,
            locality_identity,
        )
    )
    for result_kind, record, subject in complete_subjects:
        _require_current_coordinate_boundary(
            ledger,
            current_coordinates,
            locality_identity=locality_identity,
        )
        current_coordinates, result = record(
            ledger,
            current_coordinates,
            through_occurrence_coordinates,
            locality_identity,
            subject,
        )
        if result.kind != result_kind:
            raise ValueError("declared Measurement recorded another result kind")
        results.append(result)
    return RecordedDeclaredMeasurements(current_coordinates, tuple(results))


def record_declared_measurements_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
) -> RecordedDeclaredMeasurements:
    """Read current coordinates once and record all exact subjects."""

    current_coordinates = read_operator_current_coordinates(
        ledger,
        locality_identity=locality_identity,
    )
    return _record_declared_measurements_from_carried_current_coordinates(
        ledger,
        current_coordinates,
        locality_identity=locality_identity,
    )
