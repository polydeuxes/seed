from tests.test_interpretation_applicability_projection import evidence, purpose, selected_result

from seed_runtime.downstream_interpretation_admission import (
    ConsumerLocalAdmissionEvidence,
    admit_downstream_interpretation,
)
from seed_runtime.interpretation_applicability_projection import project_interpretation_applicability


def admission_evidence(selection, projection, state="admit", ref="adm:goal", consumer=None, purpose_ref=None):
    purpose_boundary = projection.bounded_downstream_purpose
    return ConsumerLocalAdmissionEvidence(
        ref,
        selection.selection_result_id,
        projection.projection_id,
        selection.selected_candidate_ref,
        purpose_ref or purpose_boundary.purpose_ref,
        consumer or purpose_boundary.consumer_ref,
        state,
        f"{state} for exact consumer-local intake",
        ("admission-record",),
    )


def applicable_projection(selection, purp=None, ev=None):
    purp = purp or purpose()
    ev = ev or evidence(purp=purp.purpose_ref, consumer=purp.consumer_ref)
    return project_interpretation_applicability(selection, purp, requirement_evidence=(ev,))


def test_admission_requires_applicable_status_and_explicit_consumer_local_evidence():
    selection = selected_result()
    projection = applicable_projection(selection)

    without_evidence = admit_downstream_interpretation(selection, projection)
    admitted = admit_downstream_interpretation(selection, projection, admission_evidence=(admission_evidence(selection, projection),))

    assert without_evidence.outcome == "unadmitted"
    assert without_evidence.admitted is False
    assert without_evidence.applicable_but_unadmitted is True
    assert "lacks explicit admission evidence" in without_evidence.applicable_but_unadmitted_reasons[0]
    assert admitted.outcome == "admitted"
    assert admitted.admitted is True
    assert admitted.consumer_ref == projection.bounded_downstream_purpose.consumer_ref
    assert admitted.purpose_ref == projection.bounded_downstream_purpose.purpose_ref
    assert admitted.selected_candidate_ref == selection.selected_candidate_ref
    assert admitted.applicability_projection == projection


def test_inapplicable_interpretations_cannot_be_admitted():
    selection = selected_result()
    purp = purpose(refusals=("refusal:closed",))
    projection = applicable_projection(selection, purp=purp, ev=evidence(purp=purp.purpose_ref, consumer=purp.consumer_ref))

    result = admit_downstream_interpretation(selection, projection, admission_evidence=(admission_evidence(selection, projection),))

    assert projection.applicability == "inapplicable"
    assert result.outcome == "unadmitted"
    assert result.admitted is False
    assert "not applicable" in result.applicable_but_unadmitted_reasons[0]


def test_unknown_and_conflicting_admission_evidence_remain_unresolved():
    selection = selected_result()
    projection = applicable_projection(selection)

    unknown = admit_downstream_interpretation(selection, projection, admission_evidence=(admission_evidence(selection, projection, state="unknown", ref="adm:unknown"),))
    conflict = admit_downstream_interpretation(selection, projection, admission_evidence=(admission_evidence(selection, projection, state="conflict", ref="adm:conflict"),))

    assert unknown.outcome == "unknown"
    assert unknown.admitted is False
    assert any("adm:unknown" in item for item in unknown.unknowns)
    assert conflict.outcome == "conflict"
    assert conflict.admitted is False
    assert any("adm:conflict" in item for item in conflict.conflicts)


def test_same_interpretation_may_be_admitted_independently_to_several_consumers():
    selection = selected_result()
    goal_projection = applicable_projection(selection)
    correction_purpose = purpose(ref="purpose:correction", consumer="consumer:corrector", requirements=("req:correction-shape",))
    correction_projection = applicable_projection(
        selection,
        purp=correction_purpose,
        ev=evidence(req="req:correction-shape", ref="ev:correction", purp="purpose:correction", consumer="consumer:corrector"),
    )

    goal_admission = admit_downstream_interpretation(selection, goal_projection, admission_evidence=(admission_evidence(selection, goal_projection, ref="adm:goal"),))
    correction_admission = admit_downstream_interpretation(selection, correction_projection, admission_evidence=(admission_evidence(selection, correction_projection, ref="adm:correction"),))

    assert goal_admission.admitted is True
    assert correction_admission.admitted is True
    assert goal_admission.selected_candidate_ref == correction_admission.selected_candidate_ref == selection.selected_candidate_ref
    assert goal_admission.consumer_ref != correction_admission.consumer_ref
    assert goal_admission.admission_id != correction_admission.admission_id


def test_admission_for_one_consumer_does_not_admit_another_consumer():
    selection = selected_result()
    goal_projection = applicable_projection(selection)
    other_purpose = purpose(ref="purpose:execution", consumer="consumer:executor", requirements=("req:exec",))
    other_projection = applicable_projection(selection, purp=other_purpose, ev=evidence(req="req:exec", ref="ev:exec", purp="purpose:execution", consumer="consumer:executor"))
    goal_only_evidence = admission_evidence(selection, goal_projection, ref="adm:goal-only")

    other = admit_downstream_interpretation(selection, other_projection, admission_evidence=(goal_only_evidence,))

    assert other.outcome == "conflict"
    assert other.admitted is False
    assert any("foreign admission evidence" in conflict for conflict in other.conflicts)


def test_no_downstream_transition_or_mutation_occurs():
    selection = selected_result()
    projection = applicable_projection(selection)
    result = admit_downstream_interpretation(selection, projection, admission_evidence=(admission_evidence(selection, projection),))

    assert result.consumed_by_consumer is False
    assert result.goal_established is False
    assert result.correction_applied is False
    assert result.inquiry_moved is False
    assert result.authorized is False
    assert result.executed is False
    assert result.presented is False
    assert result.recorded is False
    assert result.read_only is True
    assert result.writes_event_ledger is False
    assert result.mutates_state is False
    assert result.mutates_cluster is False
