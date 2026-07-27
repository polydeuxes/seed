import pytest

from seed_runtime.bounded_operator_goal_establishment import (
    BoundedOperatorGoalEstablishmentError,
    establish_bounded_operator_goal_from_admitted_interpretation,
    establish_bounded_operator_goal_from_closed_choice,
)
from seed_runtime.closed_choice_selection_binding import (
    ClosedChoiceOption,
    OperatorSelectionTokenCapture,
    PresentedClosedChoiceSet,
    bind_closed_choice_selection,
)
from seed_runtime.downstream_interpretation_admission import admit_downstream_interpretation
from seed_runtime.interpretation_applicability_projection import project_interpretation_applicability
from tests.test_downstream_interpretation_admission import admission_evidence
from tests.test_interpretation_applicability_projection import evidence, purpose, selected_result


def _choice_binding(token="1"):
    choice_set = PresentedClosedChoiceSet(
        choice_set_ref="goal-choice-set:1",
        prompt="Choose the reversible goal orientation.",
        options=(
            ClosedChoiceOption("1", "inspect_repository", "Inspect repository"),
            ClosedChoiceOption("2", "summarize_unknowns", "Summarize unknowns"),
        ),
        presentation_ref="goal-presentation:1",
        provenance=("operator-facing-menu:1",),
    )
    capture = OperatorSelectionTokenCapture(
        capture_ref=f"operator-capture:{token}",
        choice_set_ref="goal-choice-set:1",
        captured_token=token,
        provenance=("operator-accepted-token",),
    )
    return bind_closed_choice_selection(choice_set, capture)


def test_raw_closed_choice_cannot_establish_bounded_goal():
    binding = _choice_binding("1")
    with pytest.raises(BoundedOperatorGoalEstablishmentError, match="unavailable"):
        establish_bounded_operator_goal_from_closed_choice(binding)


def test_arbitrary_refs_have_no_admission_api_and_labels_are_not_goal_meaning():
    import seed_runtime.bounded_operator_goal_establishment as boge

    assert not hasattr(boge, "admit_closed_choice_to_bounded_goal")
    assert not hasattr(boge, "ClosedChoiceBoundedGoalAdmission")
    binding = _choice_binding("1")
    assert binding.bound_option_label == "Inspect repository"
    assert binding.bound_option_ref == "inspect_repository"
    with pytest.raises(TypeError):
        establish_bounded_operator_goal_from_closed_choice(
            binding, eligibility_evidence_refs=("arbitrary string",)
        )


def test_closed_choice_requires_exact_positive_goal_admission():
    with pytest.raises(BoundedOperatorGoalEstablishmentError):
        establish_bounded_operator_goal_from_closed_choice(_choice_binding("1"))


def _goal_admission(*, consumer="consumer:bounded-operator-goal-establishment", purpose_ref="purpose:bounded-operator-goal-establishment", req_state="satisfied", adm_state="admit", selected=None):
    selection = selected or selected_result()
    purp = purpose(ref=purpose_ref, consumer=consumer, requirements=("req:bounded-goal-shape",))
    projection = project_interpretation_applicability(
        selection,
        purp,
        requirement_evidence=(evidence(req="req:bounded-goal-shape", state=req_state, ref="ev:bounded-goal", purp=purpose_ref, consumer=consumer),),
    )
    admission = admit_downstream_interpretation(
        selection,
        projection,
        admission_evidence=(admission_evidence(selection, projection, state=adm_state, ref="adm:bounded-goal"),),
    )
    return selection, projection, admission


def test_admitted_interpretation_for_exact_goal_consumer_establishes_goal_and_preserves_full_lineage():
    selection, projection, admission = _goal_admission()

    goal = establish_bounded_operator_goal_from_admitted_interpretation(admission)

    assert goal.establishment_state == "established"
    assert goal.ingress_artifact_type == "DownstreamInterpretationAdmission"
    assert goal.ingress_artifact_ref == admission.admission_id
    assert goal.intended_outcome == selection.selected_candidate.label
    assert goal.consumed_admitted_meaning_snapshot == projection.selected_meaning_snapshot
    assert admission.admission_id in goal.upstream_admission_refs
    assert projection.projection_id in goal.upstream_applicability_refs
    assert selection.selection_result_id in goal.upstream_selection_refs
    assert "contract:local" in goal.upstream_source_material_refs


def test_admission_for_another_consumer_or_purpose_is_refused_without_revising_selection():
    selection, _, admission = _goal_admission(consumer="consumer:other")
    goal = establish_bounded_operator_goal_from_admitted_interpretation(admission)

    assert admission.admitted is True
    assert selection.outcome == "selected"
    assert goal.establishment_state == "refused"
    assert goal.establishment_reason == "admission_identity_or_consumer_mismatch"
    assert any("consumer" in conflict for conflict in goal.conflicts)

    _, _, wrong_purpose = _goal_admission(purpose_ref="purpose:other")
    wrong_goal = establish_bounded_operator_goal_from_admitted_interpretation(wrong_purpose)
    assert wrong_goal.establishment_state == "refused"
    assert any("purpose" in conflict for conflict in wrong_goal.conflicts)


def test_applicable_but_unadmitted_interpretation_is_refused():
    selection = selected_result()
    purp = purpose(ref="purpose:bounded-operator-goal-establishment", consumer="consumer:bounded-operator-goal-establishment", requirements=("req:bounded-goal-shape",))
    projection = project_interpretation_applicability(selection, purp, requirement_evidence=(evidence(req="req:bounded-goal-shape", ref="ev:bounded-goal", purp=purp.purpose_ref, consumer=purp.consumer_ref),))
    admission = admit_downstream_interpretation(selection, projection)

    goal = establish_bounded_operator_goal_from_admitted_interpretation(admission)

    assert projection.applicability == "applicable"
    assert admission.applicable_but_unadmitted is True
    assert goal.establishment_state == "refused"
    assert goal.establishment_reason == "interpretation_not_admitted_to_bounded_goal_establishment"
    assert "lacks explicit admission evidence" in goal.unresolved_scope[0]


def test_unknown_conflict_and_mismatched_identity_are_refused_with_lineage_preserved():
    _, _, unknown_admission = _goal_admission(adm_state="unknown")
    unknown_goal = establish_bounded_operator_goal_from_admitted_interpretation(unknown_admission)
    assert unknown_goal.establishment_state == "refused"
    assert "adm:bounded-goal:unknown for exact consumer-local intake" in unknown_goal.unknowns

    _, _, conflict_admission = _goal_admission(adm_state="conflict")
    conflict_goal = establish_bounded_operator_goal_from_admitted_interpretation(conflict_admission)
    assert conflict_goal.establishment_state == "refused"
    assert any("adm:bounded-goal" in conflict for conflict in conflict_goal.conflicts)

    selection, projection, admission = _goal_admission()
    mismatched = admit_downstream_interpretation(selection, projection, admission_evidence=(admission_evidence(selection, projection, ref="adm:bounded-goal"),))
    object.__setattr__(mismatched, "selected_candidate_ref", "cand:other")
    mismatched_goal = establish_bounded_operator_goal_from_admitted_interpretation(mismatched)
    assert mismatched_goal.establishment_state == "refused"
    assert any("selected candidate identity" in conflict for conflict in mismatched_goal.conflicts)
    assert admission.selected_candidate_ref == selection.selected_candidate_ref
