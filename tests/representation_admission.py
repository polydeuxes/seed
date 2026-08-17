"""Focused test mechanics for the explicit Candidate and Admission stages."""

from io import BytesIO

from seed_runtime.operator_egress import operator_emission_boundary
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_representation_admission import (
    record_representation_candidate_responsibility_assignment,
    record_representation_candidate_act_evidence,
    record_representation_candidate_result,
    record_exact_material_representation_admission_responsibility_assignment,
    record_exact_material_representation_admission_act_evidence,
    record_exact_material_representation_admission_result,
)
from seed_runtime.operator_representation_applicability import (
    record_representation_emission_applicability_act_evidence,
    record_representation_emission_applicability_result,
)


def admit_representation(
    ledger,
    representation,
    *,
    boundary_identity="fixture_operator_boundary",
    operator_locality_identity="fixture_operator_locality",
    output_stream=None,
):
    """Return Admission, Applicability, final Standing, and the output boundary."""

    locality_identity = representation["locality_identity"]
    boundary = operator_emission_boundary(
        BytesIO() if output_stream is None else output_stream,
        boundary_identity=boundary_identity,
        locality_identity=operator_locality_identity,
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    candidate_assignment = (
        record_representation_candidate_responsibility_assignment(
            ledger,
            representation_event_identity=representation[
                "representation_event_identity"
            ],
            locality_standing=standing,
            destination_operator_boundary=boundary,
        )
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    candidate_act = record_representation_candidate_act_evidence(
        ledger,
        assignment_event_identity=candidate_assignment.identity,
        locality_standing=standing,
    )
    candidate = record_representation_candidate_result(
        ledger,
        responsible_act_evidence_event_identity=candidate_act.identity,
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    admission_assignment = (
        record_exact_material_representation_admission_responsibility_assignment(
            ledger,
            candidate_result_event_identity=candidate.identity,
            locality_standing=standing,
        )
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    admission_act = record_exact_material_representation_admission_act_evidence(
        ledger,
        assignment_event_identity=admission_assignment.identity,
        locality_standing=standing,
    )
    admission = record_exact_material_representation_admission_result(
        ledger,
        responsible_act_evidence_event_identity=admission_act.identity,
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    applicability_act = record_representation_emission_applicability_act_evidence(
        ledger,
        admission_result_event_identity=admission.identity,
        locality_standing=standing,
        destination_operator_boundary=boundary,
    )
    applicability = record_representation_emission_applicability_result(
        ledger,
        responsible_act_evidence_event_identity=applicability_act.identity,
    )
    return (
        admission,
        applicability,
        read_operator_locality_standing(ledger, locality_identity=locality_identity),
        boundary,
    )
