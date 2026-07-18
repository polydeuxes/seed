import pytest

from seed_runtime.bounded_advancement_horizon import EvidenceSnapshotReference, establish_bounded_advancement_horizon
from seed_runtime.bounded_constitutional_question import BoundedConstitutionalQuestion, produce_bounded_constitutional_question_from_inquiry_pressure
from seed_runtime.bounded_operator_goal_establishment import establish_bounded_operator_goal_from_interpretation
from seed_runtime.goal_inquiry_consideration_selection import GoalFocusEvidence, select_goal_for_inquiry_consideration
from seed_runtime.goal_orientation_inventory import association_from_bounded_goal, build_goal_orientation_inventory
from seed_runtime.inquiry_need_projection import RepositoryWorldUncertaintyTestimony, project_inquiry_need, recognize_goal_relative_inquiry_pressure
from tests.test_bounded_operator_goal_establishment import _interpretation


def _goal():
    return establish_bounded_operator_goal_from_interpretation(
        _interpretation(), stop_conditions=("stop before question formation",)
    )


def _selection(goal):
    inventory = build_goal_orientation_inventory([
        association_from_bounded_goal(goal, dimension_refs=("knowledge_quality",), source_ref="goal-artifact:pressure")
    ])
    return select_goal_for_inquiry_consideration(
        inventory,
        [GoalFocusEvidence("focus:pressure", "operator-focus:pressure", goal.goal_establishment_id)],
    )


def _horizon(selection, goal):
    return establish_bounded_advancement_horizon(
        selection,
        goal,
        present_movement_boundary="decide whether repository/world uncertainty matters to this bounded goal",
        evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:repo-world:1", "snapshot:repo-world:1"),),
        potentially_relevant_need_families=("inquiry",),
    )


def _testimony(selection, goal, horizon, **overrides):
    base = dict(
        testimony_ref="finding:unknown-schema",
        source_ref="shape-audit:finding",
        selection_id=selection.selection_id,
        goal_establishment_id=goal.goal_establishment_id,
        horizon_id=horizon.horizon_id,
        evidence_ref="evidence:repo-world:1",
        bounded_uncertainty_component_ref="component:unknown-schema",
        repository_world_subject_ref="subject:diagnostic-shape",
        owning_stage="bounded_advancement_horizon",
        standing="unknown",
    )
    base.update(overrides)
    return RepositoryWorldUncertaintyTestimony(**base)


def test_operator_testimony_alone_does_not_produce_bounded_question():
    class RawOperatorTestimony:
        pressure_id = "operator:said-please-ask"
        standing_for_question_formation = False
        question_wording = None

    with pytest.raises(ValueError, match="recognized goal-relative inquiry pressure is required"):
        produce_bounded_constitutional_question_from_inquiry_pressure(
            pressure=RawOperatorTestimony(),
            bounded_question="What did the operator ask?",
            constitutional_intent="invalid direct testimony path",
            scope_status="bounded",
        )


def test_established_goal_without_goal_relative_evidence_pressure_does_not_automatically_produce_question():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_inquiry_need(selection, goal, horizon, [])
    pressure = recognize_goal_relative_inquiry_pressure(selection, goal, horizon, projection)
    assert pressure.recognized_standing == "unavailable"
    assert pressure.standing_for_question_formation is False
    with pytest.raises(ValueError):
        produce_bounded_constitutional_question_from_inquiry_pressure(
            pressure=pressure,
            bounded_question="What evidence is missing?",
            constitutional_intent="question formation",
            scope_status="bounded",
        )


def test_examined_evidence_without_established_bounded_goal_does_not_produce_goal_relative_pressure():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_inquiry_need(selection, goal, horizon, [_testimony(selection, goal, horizon)])
    unselected = select_goal_for_inquiry_consideration(build_goal_orientation_inventory([]), [])
    pressure = recognize_goal_relative_inquiry_pressure(unselected, goal, horizon, projection)
    assert pressure.recognized_standing == "unsupported"
    assert pressure.examined_evidence_refs == ()
    assert pressure.standing_for_question_formation is False


def test_typed_unknown_may_produce_bounded_inquiry_pressure_relative_to_goal():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_inquiry_need(selection, goal, horizon, [_testimony(selection, goal, horizon)])
    pressure = recognize_goal_relative_inquiry_pressure(selection, goal, horizon, projection)
    assert pressure.recognized_standing == "recognized"
    assert pressure.recognized_pressure_kinds == ("unknown",)
    assert pressure.source_finding_refs == ("finding:unknown-schema",)
    assert pressure.standing_for_question_formation is True


def test_pressure_artifact_remains_distinct_from_resulting_question_and_is_consumed_by_formation():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_inquiry_need(selection, goal, horizon, [_testimony(selection, goal, horizon, standing="conflicting")])
    pressure = recognize_goal_relative_inquiry_pressure(selection, goal, horizon, projection)
    question = produce_bounded_constitutional_question_from_inquiry_pressure(
        pressure=pressure,
        bounded_question="What bounded repository evidence resolves the diagnostic-shape conflict?",
        constitutional_intent="resolve goal-relative repository/world uncertainty",
        scope_status="bounded",
    )
    assert pressure.question_wording is None
    assert isinstance(question, BoundedConstitutionalQuestion)
    assert question.bounded_question != pressure.pressure_id
    assert ("pressure_id", pressure.pressure_id) in question.caller_supplied_fields
    assert question.inquiry_provenance == pressure.pressure_id


def test_question_formation_refuses_silent_reconstruction_from_raw_caller_fields():
    raw_fields = {"pressure_id": "pressure:not-an-artifact", "goal_establishment_id": "goal:1"}
    with pytest.raises(ValueError):
        produce_bounded_constitutional_question_from_inquiry_pressure(
            pressure=raw_fields,
            bounded_question="What raw field should be trusted?",
            constitutional_intent="invalid raw reconstruction",
            scope_status="bounded",
        )


def test_read_only_orientation_does_not_mutate_cluster_or_fabricate_missing_evidence():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_inquiry_need(selection, goal, horizon, [
        _testimony(selection, goal, horizon, evidence_ref="evidence:not-in-horizon")
    ])
    pressure = recognize_goal_relative_inquiry_pressure(selection, goal, horizon, projection)
    assert projection.unclassified[0].unclassified_reason == "evidence_identity_mismatch"
    assert pressure.recognized_standing == "unavailable"
    assert pressure.examined_evidence_refs == ("evidence:repo-world:1",)
    assert pressure.read_only is True
    assert pressure.writes_event_ledger is False
    assert pressure.mutates_cluster is False
