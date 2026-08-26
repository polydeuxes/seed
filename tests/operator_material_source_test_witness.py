"""Exact O1 material source for tests that require an operator source."""

from seed_runtime.events import EventLedger
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates
from seed_runtime.operator_material_source import (
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

    standing = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    binding = record_operator_material_source_subject_to_act_binding(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=standing,
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
            known_loss=(),
        ),
    )
