"""Exact O1 material acquisition for tests that require an operator source."""

from seed_runtime.events import EventLedger
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_material_acquisition import (
    record_operator_material_acquire_responsibility_assignment,
    record_operator_material_acquire_responsible_act_evidence,
    record_operator_material_acquire_result,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from seed_runtime.operator_representation import record_operator_representation


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
    representation = record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=standing,
    )
    standing = advance_operator_locality_standing(
        ledger,
        representation["recorded_occurrence_references"],
        locality_identity=locality_identity,
        prior=standing,
    )
    assignment = record_operator_material_acquire_responsibility_assignment(
        ledger,
        locality_identity=locality_identity,
        addressed_representation_event_identity=representation[
            "representation_event_identity"
        ],
        locality_standing=standing,
    )
    act_evidence = record_operator_material_acquire_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        ),
    )
    return record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
        boundary_material=OperatorBoundaryMaterial(
            exact_bytes=exact,
            eof=exact == b"",
            material_boundary=source_boundary,
            known_loss=(),
        ),
    )
