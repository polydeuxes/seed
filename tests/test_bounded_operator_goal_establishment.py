import pytest

from seed_runtime.bounded_operator_goal_establishment import (
    establish_bounded_operator_goal_from_admitted_interpretation,
    examine_meaning_relation_applicability,
)
from seed_runtime.downstream_interpretation_admission import admit_downstream_interpretation
from seed_runtime.interpretation_applicability_projection import project_interpretation_applicability
from seed_runtime.contextual_interpretation_selection import CandidateSelectionEvidence, select_contextual_interpretation
from seed_runtime.contextual_interpretation_warrant_set import (
    InterpretationCandidate,
    RetrospectiveEvidence,
    produce_contextual_interpretation_warrant_set,
)
from seed_runtime.operator_ingress_addressable_material import ExactOperatorMaterial, SourceSpan
from tests.test_downstream_interpretation_admission import admission_evidence
from tests.test_interpretation_applicability_projection import evidence, purpose, selected_result


def test_relation_fields_and_source_role_do_not_supply_consumer_evidence():
    occurrence = {
        "id": "event:one",
        "payload": {
            "relation_ref": "relation:one",
            "source_role": "potential-goal candidate",
            "proposition": "same text",
            "scope": "scope:one",
            "provenance": ["source:one"],
            "known_loss": [],
            "conflicts": [],
        },
    }
    examination = examine_meaning_relation_applicability(occurrence)
    assert examination.applicability == "unknown"
    assert examination.evidence["condition_evidence"] == []
    assert examination.evidence["meaning_relation_warrant_occurrence"] is occurrence

    other = {
        **occurrence,
        "id": "event:two",
        "payload": {**occurrence["payload"], "relation_ref": "relation:two"},
    }
    other_examination = examine_meaning_relation_applicability(other)
    assert other_examination.evidence["meaning_relation_warrant_occurrence"] is other
    assert other_examination.evidence != examination.evidence


def test_relation_conflict_remains_conflict_at_consumer_boundary():
    examination = examine_meaning_relation_applicability(
        {"id": "event:conflict", "payload": {"conflicts": ["source conflict"]}}
    )
    assert examination.applicability == "conflict"
    assert examination.conflicts == ("source conflict",)


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
    assert goal.intended_outcome == selection.selected_candidate.proposed_meaning
    assert goal.consumed_admitted_meaning_snapshot == projection.selected_meaning_snapshot
    assert admission.admission_id in goal.upstream_admission_refs
    assert projection.projection_id in goal.upstream_applicability_refs
    assert selection.selection_result_id in goal.upstream_selection_refs
    assert "contract:local" in goal.upstream_source_material_refs


def _differently_labeled_goal_selection(proposed_meaning):
    material = ExactOperatorMaterial(
        "operator-material:goal-1",
        "Examine the repository under the bounded operator goal",
        (SourceSpan("span:goal-1", "operator:turn", 0, 54, "Examine the repository under the bounded operator goal"),),
        ("operator-material:goal-1",),
    )
    warrants = produce_contextual_interpretation_warrant_set(
        operator_material=material,
        candidates=(InterpretationCandidate("candidate:goal-1", "Short display label", ("span:goal-1",), proposed_meaning),),
        retrospective_evidence=(
            RetrospectiveEvidence("ev:goal-1", "candidate:goal-1", "supporting", "retro:goal-1", "supports this exact candidate proposition"),
        ),
    )
    return select_contextual_interpretation(
        warrants,
        selection_evidence=(
            CandidateSelectionEvidence("sel:goal-1", "candidate:goal-1", "exact_operator_clarification", "Select this candidate."),
        ),
    )


def test_goal_uses_exact_candidate_proposition_and_never_display_label_or_candidate_identity():
    proposition = "Examine the repository under the bounded operator goal"
    selection, projection, admission = _goal_admission(selected=_differently_labeled_goal_selection(proposition))

    goal = establish_bounded_operator_goal_from_admitted_interpretation(admission)

    assert selection.selected_candidate.warrant_standing == "warranted"
    assert projection.applicability == "applicable"
    assert admission.admitted is True
    assert goal.establishment_state == "established"
    assert goal.intended_outcome == proposition
    assert goal.intended_outcome != selection.selected_candidate.label
    assert goal.intended_outcome != selection.selected_candidate_ref
    assert goal.consumed_admitted_meaning_snapshot["proposed_meaning"] == proposition


@pytest.mark.parametrize("proposed_meaning", ["", "   "])
def test_missing_exact_candidate_proposition_refuses_without_semantic_fallback(proposed_meaning):
    selection, _, admission = _goal_admission(selected=_differently_labeled_goal_selection(proposed_meaning))

    goal = establish_bounded_operator_goal_from_admitted_interpretation(admission)

    assert admission.admitted is True
    assert selection.selected_candidate.label == "Short display label"
    assert selection.selected_candidate_ref == "candidate:goal-1"
    assert goal.establishment_state == "refused"
    assert goal.establishment_reason == "admitted_interpretation_lacks_exact_candidate_proposition"
    assert goal.intended_outcome == ""
    assert goal.consumed_admitted_meaning_snapshot["proposed_meaning"] == proposed_meaning


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
