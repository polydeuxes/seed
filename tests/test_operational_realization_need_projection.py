from seed_runtime.bounded_advancement_horizon import EvidenceSnapshotReference, establish_bounded_advancement_horizon
from seed_runtime.bounded_operator_goal_establishment import establish_bounded_operator_goal_from_interpretation
from seed_runtime.goal_inquiry_consideration_selection import GoalFocusEvidence, select_goal_for_inquiry_consideration
from seed_runtime.goal_orientation_inventory import association_from_bounded_goal, build_goal_orientation_inventory
from seed_runtime.operational_realization_need_projection import (
    OperationalRealizationRequirementTestimony,
    OperationalRealizationStandingTestimony,
    operational_realization_need_projection_json,
    project_operational_realization_need,
)
from tests.test_bounded_operator_goal_establishment import _interpretation


def _goal(**overrides):
    return establish_bounded_operator_goal_from_interpretation(_interpretation(**overrides), stop_conditions=("stop before realization need",))


def _selection(goal):
    inv = build_goal_orientation_inventory([association_from_bounded_goal(goal, dimension_refs=("knowledge_quality",), source_ref="goal-artifact:realization")])
    return select_goal_for_inquiry_consideration(inv, [GoalFocusEvidence("focus:realization", "operator-focus:realization", goal.goal_establishment_id)])


def _horizon(selection, goal):
    return establish_bounded_advancement_horizon(
        selection,
        goal,
        present_movement_boundary="decide whether explicit operational-realization testimony creates a need",
        evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:req", "snapshot:req"), EvidenceSnapshotReference("evidence:standing", "snapshot:standing"), EvidenceSnapshotReference("evidence:generic", "snapshot:generic")),
        potentially_relevant_need_families=("operational_realization",),
    )


def _req(selection, goal, horizon, **overrides):
    base = dict(testimony_ref="req:1", source_ref="stage-testimony:req", selection_id=selection.selection_id, goal_establishment_id=goal.goal_establishment_id, horizon_id=horizon.horizon_id, evidence_ref="evidence:req", bounded_realization_component_ref="component:realization:1", required_transformation_ref="transformation:apply", applicable_scope_ref="scope:repo", owning_stage="bounded_advancement_horizon", requirement_standing="required")
    base.update(overrides)
    return OperationalRealizationRequirementTestimony(**base)


def _standing(selection, goal, horizon, **overrides):
    base = dict(testimony_ref="standing:1", source_ref="stage-testimony:standing", selection_id=selection.selection_id, goal_establishment_id=goal.goal_establishment_id, horizon_id=horizon.horizon_id, evidence_ref="evidence:standing", bounded_realization_component_ref="component:realization:1", required_transformation_ref="transformation:apply", applicable_scope_ref="scope:repo", owning_stage="bounded_advancement_horizon", availability_standing="unavailable", coverage_standing="complete_for_horizon", blocker_family_ownership="operational_realization")
    base.update(overrides)
    return OperationalRealizationStandingTestimony(**base)


def test_exact_selection_goal_horizon_evidence_component_transformation_scope_and_ownership_joins():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_operational_realization_need(selection, goal, horizon, [_req(selection, goal, horizon)], [_standing(selection, goal, horizon)])
    assert tuple(i.requirement_testimony_ref for i in projection.established) == ("req:1",)
    bad_cases = [
        (_req(selection, goal, horizon, testimony_ref="bad-selection", selection_id="other"), _standing(selection, goal, horizon, testimony_ref="s-bad-selection"), "selection_identity_mismatch"),
        (_req(selection, goal, horizon, testimony_ref="bad-goal", goal_establishment_id="other"), _standing(selection, goal, horizon, testimony_ref="s-bad-goal"), "goal_identity_mismatch"),
        (_req(selection, goal, horizon, testimony_ref="bad-horizon", horizon_id="other"), _standing(selection, goal, horizon, testimony_ref="s-bad-horizon"), "horizon_identity_mismatch"),
        (_req(selection, goal, horizon, testimony_ref="bad-evidence", evidence_ref="other"), _standing(selection, goal, horizon, testimony_ref="s-bad-evidence"), "evidence_identity_mismatch"),
        (_req(selection, goal, horizon, testimony_ref="bad-component", bounded_realization_component_ref=""), _standing(selection, goal, horizon, testimony_ref="s-bad-component", bounded_realization_component_ref=""), "not_component_bounded"),
        (_req(selection, goal, horizon, testimony_ref="bad-transformation", required_transformation_ref=""), _standing(selection, goal, horizon, testimony_ref="s-bad-transformation", required_transformation_ref=""), "missing_transformation"),
        (_req(selection, goal, horizon, testimony_ref="bad-scope", applicable_scope_ref=""), _standing(selection, goal, horizon, testimony_ref="s-bad-scope", applicable_scope_ref=""), "missing_applicable_scope"),
        (_req(selection, goal, horizon, testimony_ref="bad-owner", owning_stage=""), _standing(selection, goal, horizon, testimony_ref="s-bad-owner", owning_stage=""), "ownership_mismatch"),
    ]
    projection = project_operational_realization_need(selection, goal, horizon, [r for r, _, _ in bad_cases], [s for _, s, _ in bad_cases])
    assert tuple(i.unclassified_reason for i in projection.unclassified[: len(bad_cases)]) == tuple(reason for _, _, reason in bad_cases)


def test_conclusion_matrix_preserves_requirement_availability_coverage_blocker_scope_and_materiality_separately():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    rows = [
        ("not_required", "unavailable", "complete_for_horizon", "operational_realization", "unsupported"),
        ("required", "available", "complete_for_horizon", "operational_realization", "unsupported"),
        ("required", "unavailable", "complete_for_horizon", "operational_realization", "established"),
        ("required", "unavailable", "partial", "operational_realization", "unknown"),
        ("required", "unavailable", "unknown", "operational_realization", "unknown"),
        ("required", "unavailable", "conflicting", "operational_realization", "conflicting"),
        ("required", "unavailable", "complete_for_horizon", "authority", "unclassified_here"),
        ("required", "unknown", "complete_for_horizon", "operational_realization", "unknown"),
        ("required", "conflicting", "complete_for_horizon", "operational_realization", "conflicting"),
    ]
    reqs = [_req(selection, goal, horizon, testimony_ref=f"req:{n}", bounded_realization_component_ref=f"component:{n}", requirement_standing=r) for n, (r, _, _, _, _) in enumerate(rows)]
    standings = [_standing(selection, goal, horizon, testimony_ref=f"standing:{n}", bounded_realization_component_ref=f"component:{n}", availability_standing=a, coverage_standing=c, blocker_family_ownership=o) for n, (_, a, c, o, _) in enumerate(rows)]
    projection = project_operational_realization_need(selection, goal, horizon, reqs, standings)
    item = projection.established[0]
    assert [item.requirement_standing, item.availability_standing, item.coverage_standing, item.blocker_family_ownership, item.scope_applicability, item.horizon_materiality] == ["required", "unavailable", "complete_for_horizon", "operational_realization", "applicable", "material"]
    assert tuple(i.requirement_testimony_ref for i in projection.unsupported) == ("req:0", "req:1")
    assert tuple(i.requirement_testimony_ref for i in projection.established) == ("req:2",)
    assert tuple(i.requirement_testimony_ref for i in projection.unknown) == ("req:3", "req:4", "req:7")
    assert tuple(i.requirement_testimony_ref for i in projection.conflicting) == ("req:5", "req:8")
    assert tuple(i.requirement_testimony_ref for i in projection.unclassified_here) == ("req:6",)


def test_authority_clarification_inquiry_generic_candidate_local_failure_and_missing_selection_do_not_establish_unavailability():
    goal = _goal(unknowns=("generic blocker",), unresolved_references=("candidate-local failure",)); selection = _selection(goal); horizon = _horizon(selection, goal)
    reqs = [_req(selection, goal, horizon, testimony_ref=f"req:{n}", bounded_realization_component_ref=f"component:{n}") for n in range(7)]
    standings = [
        _standing(selection, goal, horizon, testimony_ref="authority", bounded_realization_component_ref="component:0", blocker_family_ownership="authority"),
        _standing(selection, goal, horizon, testimony_ref="clarification", bounded_realization_component_ref="component:1", blocker_family_ownership="clarification"),
        _standing(selection, goal, horizon, testimony_ref="inquiry", bounded_realization_component_ref="component:2", blocker_family_ownership="inquiry"),
        _standing(selection, goal, horizon, testimony_ref="generic", bounded_realization_component_ref="component:3", blocker_family_ownership="generic"),
        _standing(selection, goal, horizon, testimony_ref="one-candidate-blocked", bounded_realization_component_ref="component:4", coverage_standing="partial"),
        _standing(selection, goal, horizon, testimony_ref="missing-selection", bounded_realization_component_ref="component:5", availability_standing="unknown", selection_ref=""),
        _standing(selection, goal, horizon, testimony_ref="no-supporting-candidate", bounded_realization_component_ref="component:6", coverage_standing="unknown", candidate_existence_ref="candidate-set:no-supporting-candidate"),
    ]
    projection = project_operational_realization_need(selection, goal, horizon, reqs, standings)
    assert projection.established == ()
    assert tuple(i.requirement_testimony_ref for i in projection.unclassified_here) == ("req:0", "req:1", "req:2", "req:3")
    assert tuple(i.requirement_testimony_ref for i in projection.unknown) == ("req:4", "req:5", "req:6")


def test_scope_materiality_family_mismatches_and_orphan_standing_remain_unclassified():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_operational_realization_need(selection, goal, horizon, [
        _req(selection, goal, horizon, testimony_ref="outside", scope_applicability="outside_current_scope", bounded_realization_component_ref="component:outside"),
        _req(selection, goal, horizon, testimony_ref="not-material", horizon_materiality="not_material", bounded_realization_component_ref="component:not-material"),
        _req(selection, goal, horizon, testimony_ref="wrong-family", component_family="authority", bounded_realization_component_ref="component:wrong-family"),
    ], [
        _standing(selection, goal, horizon, testimony_ref="standing:outside", scope_applicability="outside_current_scope", bounded_realization_component_ref="component:outside"),
        _standing(selection, goal, horizon, testimony_ref="standing:not-material", horizon_materiality="not_material", bounded_realization_component_ref="component:not-material"),
        _standing(selection, goal, horizon, testimony_ref="standing:wrong-family", bounded_realization_component_ref="component:wrong-family"),
        _standing(selection, goal, horizon, testimony_ref="standing:orphan", bounded_realization_component_ref="component:orphan"),
    ])
    assert projection.established == ()
    assert tuple(i.unclassified_reason for i in projection.unclassified) == ("scope_not_applicable", "not_material_to_horizon", "not_requirement_component", "not_requirement_component")


def test_read_only_no_selection_warrant_translation_invocation_authorization_execution_recording_event_or_mutation():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    payload = operational_realization_need_projection_json(project_operational_realization_need(selection, goal, horizon, [_req(selection, goal, horizon)], [_standing(selection, goal, horizon)]))
    assert payload["selects_realization"] is False
    assert payload["warrants_realization"] is False
    assert payload["translates_representation"] is False
    assert payload["prepares_invocation"] is False
    assert payload["requests_authority"] is False
    assert payload["authorizes_movement"] is False
    assert payload["starts_execution"] is False
    assert payload["starts_recording"] is False
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False
    assert payload["read_only"] is True
