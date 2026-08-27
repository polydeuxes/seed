"""Exact O1 material source for tests that require an operator source."""

from seed_runtime.events import EventLedger
from seed_runtime.operator_current_coordinates import (
    _advance_current_coordinates_with_operator_material_source_occurrence,
    read_operator_current_coordinates,
)
from seed_runtime.operator_material_source import (
    _record_operator_material_source_act_occurrence_from_binding,
    _record_operator_material_source_result,
    _record_operator_material_source_subject_to_act_binding_from_current_coordinates,
    record_operator_material_source_subject_to_act_binding,
    record_operator_material_source_act_occurrence,
    record_operator_material_source_result,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial


def record_operator_material_occurrence(
    ledger: EventLedger,
    *,
    exact: bytes,
    locality_identity: str,
    source_boundary: str = "operator boundary",
):
    """Record O1 through its exact Source.G physiology."""

    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    binding = record_operator_material_source_subject_to_act_binding(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=current_coordinates,
        source_boundary=source_boundary,
    )
    act_occurrence = record_operator_material_source_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=locality_identity
        ),
    )
    return record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
        boundary_material=OperatorBoundaryMaterial(
            exact_bytes=exact,
            eof=exact == b"",
            material_boundary=source_boundary,
        ),
    )


def record_operator_material_occurrence_from_current_coordinates(
    ledger: EventLedger,
    *,
    exact: bytes,
    locality_identity: str,
    current_coordinates: dict,
    source_boundary: str = "operator boundary",
):
    """Record O1 and return exact current coordinates through its result."""

    prior_occurrence_identity = current_coordinates[
        "through_event_occurrence_identity"
    ]
    binding = (
        _record_operator_material_source_subject_to_act_binding_from_current_coordinates(
            ledger,
            locality_identity=locality_identity,
            current_coordinates=current_coordinates,
            source_boundary=source_boundary,
        )
    )
    current_coordinates = (
        _advance_current_coordinates_with_operator_material_source_occurrence(
            ledger,
            current_coordinates,
            binding,
            prior_through_event_occurrence_identity=prior_occurrence_identity,
        )
    )
    act_occurrence = _record_operator_material_source_act_occurrence_from_binding(
        ledger,
        subject_to_act_binding=binding,
        current_coordinates=current_coordinates,
    )
    current_coordinates = (
        _advance_current_coordinates_with_operator_material_source_occurrence(
            ledger,
            current_coordinates,
            act_occurrence,
            prior_through_event_occurrence_identity=binding.identity,
        )
    )
    result = _record_operator_material_source_result(
        ledger,
        act_occurrence=act_occurrence,
        boundary_material=OperatorBoundaryMaterial(
            exact_bytes=exact,
            eof=exact == b"",
            material_boundary=source_boundary,
        ),
    )
    current_coordinates = (
        _advance_current_coordinates_with_operator_material_source_occurrence(
            ledger,
            current_coordinates,
            result,
            prior_through_event_occurrence_identity=act_occurrence.identity,
        )
    )
    return result, current_coordinates
