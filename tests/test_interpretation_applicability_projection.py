from dataclasses import asdict

from seed_runtime.contextual_interpretation_selection import CandidateSelectionEvidence, select_contextual_interpretation
from seed_runtime.contextual_interpretation_warrant_set import (
    ExactOperatorMaterial,
    InterpretationCandidate,
    RetrospectiveEvidence,
    SourceSpan,
    produce_contextual_interpretation_warrant_set,
)
from seed_runtime.interpretation_applicability_projection import (
    BoundedDownstreamPurpose,
    PurposeLocalRequirementEvidence,
    project_interpretation_applicability,
)


def selected_result():
    material = ExactOperatorMaterial(
        "operator-material:applicability",
        "please establish the deployment goal if safe",
        (SourceSpan("span:goal", "operator:turn", 0, 41, "please establish the deployment goal if safe"),),
        ("operator-material",),
    )
    warrant_set = produce_contextual_interpretation_warrant_set(
        operator_material=material,
        candidates=(InterpretationCandidate("cand:goal", "goal establishment meaning", ("span:goal",), "operator asks to establish a goal"),),
        retrospective_evidence=(RetrospectiveEvidence("ev:goal", "cand:goal", "supporting", "retro:goal", "supports goal meaning"),),
    )
    return select_contextual_interpretation(
        warrant_set,
        selection_evidence=(
            CandidateSelectionEvidence("sel:goal", "cand:goal", "exact_operator_clarification", "Use the goal meaning.", ("operator",)),
        ),
    )


def purpose(ref="purpose:goal", consumer="consumer:goal-establisher", requirements=("req:goal-shape",), refusals=()):
    return BoundedDownstreamPurpose(
        ref,
        "goal establishment focused test consumer",
        consumer,
        "bounded goal establishment consumer",
        "ContextualInterpretationSelectionResult.selected_candidate",
        requirements,
        refusals,
        ("contract:local",),
    )


def evidence(req="req:goal-shape", state="satisfied", ref="ev:req", purp="purpose:goal", consumer="consumer:goal-establisher"):
    return PurposeLocalRequirementEvidence(ref, purp, consumer, req, state, f"{state} by consumer contract", ("consumer-evidence",))


def test_applicable_projection_preserves_selected_meaning_and_remains_read_only():
    selection = selected_result()
    projection = project_interpretation_applicability(selection, purpose(), requirement_evidence=(evidence(),))

    assert projection.applicability == "applicable"
    assert projection.selected_candidate_ref == selection.selected_candidate_ref
    assert projection.selected_meaning_snapshot == asdict(selection.selected_candidate)
    assert projection.downstream_admission is None
    assert projection.admitted is False
    assert projection.goal_established is False
    assert projection.authorized is False
    assert projection.executed is False
    assert projection.recorded is False
    assert projection.read_only is True
    assert projection.writes_event_ledger is False
    assert projection.mutates_state is False
    assert projection.mutates_cluster is False


def test_inapplicable_unknown_and_conflict_outcomes_preserve_refused_meaning():
    selection = selected_result()

    inapplicable = project_interpretation_applicability(selection, purpose(refusals=("refusal:goal-window-closed",)), requirement_evidence=(evidence(),))
    unknown = project_interpretation_applicability(selection, purpose(requirements=("req:goal-shape", "req:operator-authority-evidence")), requirement_evidence=(evidence(),))
    conflict = project_interpretation_applicability(selection, purpose(), requirement_evidence=(evidence(state="conflict"),))

    assert inapplicable.applicability == "inapplicable"
    assert unknown.applicability == "unknown"
    assert conflict.applicability == "conflict"
    for projection in (inapplicable, unknown, conflict):
        assert projection.selected_candidate_ref == "cand:goal"
        assert projection.selected_meaning_snapshot == asdict(selection.selected_candidate)
        assert projection.admitted is False
        assert projection.goal_established is False
        assert projection.correction_applied is False
        assert projection.inquiry_moved is False


def test_requirement_evidence_remains_consumer_owned_and_foreign_evidence_conflicts():
    selection = selected_result()
    foreign = evidence(ref="ev:foreign", purp="purpose:other", consumer="consumer:other")
    projection = project_interpretation_applicability(selection, purpose(), requirement_evidence=(foreign,))

    assert projection.requirement_evidence[0].consumer_owned is True
    assert projection.applicability == "conflict"
    assert any("foreign requirement evidence refused" in conflict for conflict in projection.conflicts)
    assert projection.selected_candidate_ref == selection.selected_candidate_ref


def test_same_interpretation_can_differ_for_different_purposes_without_closed_registry():
    selection = selected_result()
    goal = project_interpretation_applicability(selection, purpose(), requirement_evidence=(evidence(),))
    execution = project_interpretation_applicability(
        selection,
        purpose(ref="purpose:operational-execution", consumer="consumer:executor", requirements=("req:authorization-token",)),
        requirement_evidence=(evidence(req="req:authorization-token", state="unsatisfied", ref="ev:exec", purp="purpose:operational-execution", consumer="consumer:executor"),),
    )
    arbitrary = project_interpretation_applicability(
        selection,
        purpose(ref="purpose:not-in-a-registry", consumer="consumer:local-ad-hoc", requirements=("req:local",)),
        requirement_evidence=(evidence(req="req:local", ref="ev:local", purp="purpose:not-in-a-registry", consumer="consumer:local-ad-hoc"),),
    )

    assert goal.applicability == "applicable"
    assert execution.applicability == "inapplicable"
    assert arbitrary.applicability == "applicable"
    assert arbitrary.bounded_downstream_purpose.purpose_ref == "purpose:not-in-a-registry"
