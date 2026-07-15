from seed_runtime.bounded_operator_goal_establishment import (
    bounded_operator_goal_establishment_json,
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
