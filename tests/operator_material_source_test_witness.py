"""Exact O1 material source for tests that require an operator source."""

from seed_runtime.events import EventLedger
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_material_source import (
    record_operator_material_source_responsibility_assignment,
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

    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    assignment = record_operator_material_source_responsibility_assignment(
        ledger,
        locality_identity=locality_identity,
        locality_standing=standing,
    )
    act_occurrence = record_operator_material_source_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
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
