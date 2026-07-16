from seed_runtime.bounded_operator_goal_establishment import (
    bounded_operator_goal_establishment_json,
    establish_bounded_operator_goal_from_admitted_interpretation,
    establish_bounded_operator_goal_from_closed_choice,
    establish_bounded_operator_goal_from_interpretation,
)
from seed_runtime.closed_choice_selection_binding import (
    ClosedChoiceOption,
    OperatorSelectionTokenCapture,
    PresentedClosedChoiceSet,
    bind_closed_choice_selection,
)
from seed_runtime.operator_expression_interpretation import OperatorExpressionInterpretationProjection
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


def _interpretation(**overrides):
    base = dict(
        artifact_type="OperatorExpressionInterpretationProjection",
        interpretation_projection_id="interpretation:1",
        attributed_expression_ref="attributed-expression:1",
        grammar_recovery_ref="grammar-recovery:1",
        recovered_grammar_ref="grammar:1",
        grammar_applicability_ref="grammar-applicability:1",
        interpretation_mechanism_ref="mechanism:1",
        invocation_contract_ref="contract:1",
        interpretation_state="interpreted",
        interpretation_reason="one bounded interpretation is supported",
        expression_form="show",
        inquiry_or_request_kind="show",
        relation_or_focus_expressions=("repository diagnostic inventory",),
        subject_expressions=(),
        object_expressions=(),
        scope_expressions=("this repository",),
        operator_stated_effect_constraints=("do not modify anything", "within two minutes"),
        unresolved_references=(),
        unresolved_lexical_bindings=(),
        unsupported_residual_spans=(),
        known_loss=("presentation wording normalized",),
        provenance=("attributed-expression:1", "grammar:1"),
        unknowns=(),
        conflicts=(),
    )
    base.update(overrides)
    return OperatorExpressionInterpretationProjection(**base)


def test_closed_choice_ingress_establishes_bounded_goal_with_exact_lineage():
    binding = _choice_binding("1")

    goal = establish_bounded_operator_goal_from_closed_choice(
        binding,
        sufficiency_conditions=("operator selected one presented option",),
        stop_conditions=("before opening inquiry frontier",),
    )

    assert goal.artifact_type == "BoundedOperatorGoalEstablishment"
    assert goal.ingress_artifact_type == "ClosedChoiceSelectionBinding"
    assert goal.ingress_artifact_ref == binding.binding_id
    assert goal.establishment_state == "established"
    assert goal.intended_outcome == "Inspect repository"
    assert goal.known_scope == ("inspect_repository",)
    assert binding.exact_choice_set_fingerprint in goal.ingress_lineage
    assert goal.operator_acceptance_provenance == (binding.token_capture_ref,)


def test_interpreted_expression_ingress_establishes_provisional_goal_and_preserves_unknowns():
    interpretation = _interpretation(unknowns=("which diagnostic depth is enough remains unresolved",))

    goal = establish_bounded_operator_goal_from_interpretation(
        interpretation,
        stop_conditions=("stop before authorization",),
    )

    assert goal.ingress_artifact_type == "OperatorExpressionInterpretationProjection"
    assert goal.ingress_artifact_ref == "interpretation:1"
    assert goal.establishment_state == "provisional"
    assert "repository diagnostic inventory" in goal.known_scope
    assert goal.unknowns == ("which diagnostic depth is enough remains unresolved",)
    assert goal.sufficiency_state == "provisional"
    assert "attributed-expression:1" in goal.ingress_lineage


def test_refuses_when_no_bounded_orientation_is_supportable():
    unsupported_choice = establish_bounded_operator_goal_from_closed_choice(_choice_binding("9"))
    unsupported_expression = establish_bounded_operator_goal_from_interpretation(
        _interpretation(
            interpretation_state="unsupported",
            relation_or_focus_expressions=(),
            scope_expressions=(),
            unsupported_residual_spans=(),
        )
    )

    assert unsupported_choice.establishment_state == "refused"
    assert unsupported_choice.intended_outcome == ""
    assert unsupported_expression.establishment_state == "refused"
    assert unsupported_expression.known_scope == ()


def test_operator_constraints_are_preserved_but_not_enforced():
    goal = establish_bounded_operator_goal_from_interpretation(_interpretation())

    assert goal.operator_constraints == ("do not modify anything", "within two minutes")
    assert goal.constraints_enforced is False
    assert goal.resources_observed is False


def test_establishment_has_no_inquiry_authorization_execution_recording_or_satisfaction_effects():
    goal = establish_bounded_operator_goal_from_interpretation(_interpretation())
    data = bounded_operator_goal_establishment_json(goal)

    assert data["inquiry_opened"] is False
    assert data["work_authorized"] is False
    assert data["execution_started"] is False
    assert data["recording_started"] is False
    assert data["satisfaction_judged"] is False
    assert data["read_only"] is True
    assert data["writes_event_ledger"] is False
    assert data["mutates_cluster"] is False


def test_corrections_remain_possible_without_rewriting_ingress_lineage():
    original = establish_bounded_operator_goal_from_interpretation(_interpretation())
    corrected = establish_bounded_operator_goal_from_interpretation(
        _interpretation(
            interpretation_projection_id="interpretation:correction",
            attributed_expression_ref="attributed-expression:correction",
            relation_or_focus_expressions=("repository diagnostic inventory tests",),
            provenance=("attributed-expression:correction", "operator-correction:1"),
        ),
        correction_of_goal_ref=original.goal_establishment_id,
    )

    assert corrected.correction_of_goal_ref == original.goal_establishment_id
    assert corrected.correction_possible_without_rewriting_ingress is True
    assert original.ingress_artifact_ref == "interpretation:1"
    assert "attributed-expression:1" in original.ingress_lineage
    assert "attributed-expression:correction" in corrected.ingress_lineage


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

    goal = establish_bounded_operator_goal_from_admitted_interpretation(
        admission,
        sufficiency_conditions=("consumer-local admission is explicit",),
        stop_conditions=("stop before inquiry opening",),
    )

    assert goal.establishment_state == "established"
    assert goal.ingress_artifact_type == "DownstreamInterpretationAdmission"
    assert goal.ingress_artifact_ref == admission.admission_id
    assert goal.intended_outcome == selection.selected_candidate.label
    assert goal.consumed_admitted_meaning_snapshot == projection.selected_meaning_snapshot
    assert admission.admission_id in goal.upstream_admission_refs
    assert projection.projection_id in goal.upstream_applicability_refs
    assert selection.selection_result_id in goal.upstream_selection_refs
    assert selection.selected_candidate_ref in goal.upstream_warrant_refs
    assert "contract:local" in goal.upstream_source_material_refs
    assert "adm:bounded-goal" in goal.operator_acceptance_provenance
    assert goal.reinterpreted_source is False
    assert goal.regenerated_warrants is False
    assert goal.reselected_candidate is False
    assert goal.recomputed_applicability is False
    assert goal.recomputed_admission is False


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


def test_admitted_interpretation_handoff_has_no_inquiry_authorization_execution_recording_satisfaction_or_mutation():
    _, _, admission = _goal_admission()
    goal = establish_bounded_operator_goal_from_admitted_interpretation(admission)

    assert goal.inquiry_opened is False
    assert goal.work_authorized is False
    assert goal.execution_started is False
    assert goal.recording_started is False
    assert goal.satisfaction_judged is False
    assert goal.read_only is True
    assert goal.writes_event_ledger is False
    assert goal.mutates_cluster is False
