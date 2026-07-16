from seed_runtime.authority_need_projection import AuthorityRequirementTestimony, AuthorityStandingTestimony, authority_need_projection_json, project_authority_need
from seed_runtime.bounded_advancement_horizon import EvidenceSnapshotReference, establish_bounded_advancement_horizon
from seed_runtime.bounded_operator_goal_establishment import establish_bounded_operator_goal_from_interpretation
from seed_runtime.goal_inquiry_consideration_selection import GoalFocusEvidence, select_goal_for_inquiry_consideration
from seed_runtime.goal_orientation_inventory import association_from_bounded_goal, build_goal_orientation_inventory
from tests.test_bounded_operator_goal_establishment import _interpretation


def _goal(**overrides):
    return establish_bounded_operator_goal_from_interpretation(_interpretation(**overrides), stop_conditions=("stop before authority need",))


def _selection(goal):
    inventory = build_goal_orientation_inventory([association_from_bounded_goal(goal, dimension_refs=("knowledge_quality",), source_ref="goal-artifact:authority")])
    return select_goal_for_inquiry_consideration(inventory, [GoalFocusEvidence("focus:authority", "operator-focus:authority", goal.goal_establishment_id)])


def _horizon(selection, goal):
    return establish_bounded_advancement_horizon(
        selection,
        goal,
        present_movement_boundary="decide whether explicit authority requirement and standing testimony creates an authority need",
        evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:req", "snapshot:req"), EvidenceSnapshotReference("evidence:auth", "snapshot:auth"), EvidenceSnapshotReference("evidence:generic", "snapshot:generic")),
        potentially_relevant_need_families=("authority",),
    )


def _req(selection, goal, horizon, **overrides):
    base = dict(testimony_ref="req:1", source_ref="stage-testimony:req", selection_id=selection.selection_id, goal_establishment_id=goal.goal_establishment_id, horizon_id=horizon.horizon_id, evidence_ref="evidence:req", bounded_authority_component_ref="component:authority:1", required_authority_class_ref="authority-class:write", applicable_scope_ref="scope:repo", owning_stage="bounded_advancement_horizon", requirement_standing="required")
    base.update(overrides)
    return AuthorityRequirementTestimony(**base)


def _auth(selection, goal, horizon, **overrides):
    base = dict(testimony_ref="auth:1", source_ref="stage-testimony:auth", selection_id=selection.selection_id, goal_establishment_id=goal.goal_establishment_id, horizon_id=horizon.horizon_id, evidence_ref="evidence:auth", bounded_authority_component_ref="component:authority:1", required_authority_class_ref="authority-class:write", applicable_scope_ref="scope:repo", owning_stage="bounded_advancement_horizon", authority_standing="unavailable")
    base.update(overrides)
    return AuthorityStandingTestimony(**base)


def test_exact_selection_goal_horizon_evidence_component_authority_class_scope_and_ownership_joins():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_authority_need(selection, goal, horizon, [_req(selection, goal, horizon)], [_auth(selection, goal, horizon)])
    assert tuple(i.requirement_testimony_ref for i in projection.established) == ("req:1",)
    bad_cases = [
        (_req(selection, goal, horizon, testimony_ref="bad-selection", selection_id="other"), _auth(selection, goal, horizon, testimony_ref="a-bad-selection"), "selection_identity_mismatch"),
        (_req(selection, goal, horizon, testimony_ref="bad-goal", goal_establishment_id="other"), _auth(selection, goal, horizon, testimony_ref="a-bad-goal"), "goal_identity_mismatch"),
        (_req(selection, goal, horizon, testimony_ref="bad-horizon", horizon_id="other"), _auth(selection, goal, horizon, testimony_ref="a-bad-horizon"), "horizon_identity_mismatch"),
        (_req(selection, goal, horizon, testimony_ref="bad-evidence", evidence_ref="other"), _auth(selection, goal, horizon, testimony_ref="a-bad-evidence"), "evidence_identity_mismatch"),
        (_req(selection, goal, horizon, testimony_ref="bad-component", bounded_authority_component_ref=""), _auth(selection, goal, horizon, testimony_ref="a-bad-component", bounded_authority_component_ref=""), "not_component_bounded"),
        (_req(selection, goal, horizon, testimony_ref="bad-class", required_authority_class_ref=""), _auth(selection, goal, horizon, testimony_ref="a-bad-class", required_authority_class_ref=""), "missing_authority_class"),
        (_req(selection, goal, horizon, testimony_ref="bad-scope", applicable_scope_ref=""), _auth(selection, goal, horizon, testimony_ref="a-bad-scope", applicable_scope_ref=""), "missing_applicable_scope"),
        (_req(selection, goal, horizon, testimony_ref="bad-owner", owning_stage=""), _auth(selection, goal, horizon, testimony_ref="a-bad-owner", owning_stage=""), "ownership_mismatch"),
    ]
    projection = project_authority_need(selection, goal, horizon, [r for r, _, _ in bad_cases], [a for _, a, _ in bad_cases])
    assert tuple(i.unclassified_reason for i in projection.unclassified[: len(bad_cases)]) == tuple(reason for _, _, reason in bad_cases)


def test_required_conclusion_matrix_and_separate_dimensions():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    rows = [("required", "unavailable", "established"), ("required", "available", "unsupported"), ("required", "unknown", "unknown"), ("required", "conflicting", "conflicting"), ("required", "outside_current_scope", "outside_current_scope"), ("not_required", "unavailable", "unsupported"), ("unknown", "unavailable", "unknown"), ("conflicting", "unavailable", "conflicting")]
    reqs = [_req(selection, goal, horizon, testimony_ref=f"req:{n}", bounded_authority_component_ref=f"component:{n}", requirement_standing=req_standing) for n, (req_standing, _, _) in enumerate(rows)]
    auths = [_auth(selection, goal, horizon, testimony_ref=f"auth:{n}", bounded_authority_component_ref=f"component:{n}", authority_standing=auth_standing) for n, (_, auth_standing, _) in enumerate(rows)]
    projection = project_authority_need(selection, goal, horizon, reqs, auths)
    assert [projection.established[0].requirement_standing, projection.established[0].authority_standing, projection.established[0].scope_applicability, projection.established[0].horizon_materiality] == ["required", "unavailable", "applicable", "material"]
    assert tuple(i.requirement_testimony_ref for i in projection.established) == ("req:0",)
    assert tuple(i.requirement_testimony_ref for i in projection.unsupported) == ("req:1", "req:5")
    assert tuple(i.requirement_testimony_ref for i in projection.unknown) == ("req:2", "req:6")
    assert tuple(i.requirement_testimony_ref for i in projection.conflicting) == ("req:3", "req:7")
    assert tuple(i.requirement_testimony_ref for i in projection.outside_current_scope) == ("req:4",)


def test_unknown_conflicting_candidate_local_generic_and_other_components_do_not_establish():
    goal = _goal(unknowns=("generic blocker",), unresolved_references=("candidate-local authority blocker",)); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_authority_need(selection, goal, horizon, [
        _req(selection, goal, horizon, testimony_ref="clarification", component_family="clarification"),
        _req(selection, goal, horizon, testimony_ref="inquiry", component_family="inquiry"),
        _req(selection, goal, horizon, testimony_ref="realization", component_family="realization"),
        _req(selection, goal, horizon, testimony_ref="generic", component_family="generic_blocker"),
        _req(selection, goal, horizon, testimony_ref="candidate-local", component_family="candidate_local_authority_blocker"),
        _req(selection, goal, horizon, testimony_ref="unknown-req", requirement_standing="unknown", bounded_authority_component_ref="component:unknown"),
        _req(selection, goal, horizon, testimony_ref="conflict-req", requirement_standing="conflicting", bounded_authority_component_ref="component:conflict"),
    ], [
        _auth(selection, goal, horizon, testimony_ref="auth:unknown", bounded_authority_component_ref="component:unknown", authority_standing="unknown"),
        _auth(selection, goal, horizon, testimony_ref="auth:conflict", bounded_authority_component_ref="component:conflict", authority_standing="conflicting"),
    ])
    assert projection.established == ()
    assert tuple(i.unclassified_reason for i in projection.unclassified[:5]) == ("not_authority_requirement_component",) * 5
    assert tuple(i.requirement_testimony_ref for i in projection.unknown) == ("unknown-req",)
    assert tuple(i.requirement_testimony_ref for i in projection.conflicting) == ("conflict-req",)


def test_scope_and_materiality_failures_are_unclassified_not_scope_expansion_or_need():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_authority_need(selection, goal, horizon, [
        _req(selection, goal, horizon, testimony_ref="outside", scope_applicability="outside_current_scope", bounded_authority_component_ref="component:outside"),
        _req(selection, goal, horizon, testimony_ref="not-material", horizon_materiality="not_material", bounded_authority_component_ref="component:not-material"),
    ], [
        _auth(selection, goal, horizon, testimony_ref="auth:outside", scope_applicability="outside_current_scope", bounded_authority_component_ref="component:outside"),
        _auth(selection, goal, horizon, testimony_ref="auth:not-material", horizon_materiality="not_material", bounded_authority_component_ref="component:not-material"),
    ])
    assert projection.established == ()
    assert tuple(i.unclassified_reason for i in projection.unclassified[:2]) == ("scope_not_applicable", "not_material_to_horizon")


def test_read_only_no_request_source_grant_scope_authorization_execution_recording_event_or_cluster_mutation():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    payload = authority_need_projection_json(project_authority_need(selection, goal, horizon, [_req(selection, goal, horizon)], [_auth(selection, goal, horizon)]))
    assert payload["requests_authority"] is False
    assert payload["selects_authority_source"] is False
    assert payload["grants_authority"] is False
    assert payload["expands_scope"] is False
    assert payload["authorizes_movement"] is False
    assert payload["selects_realization"] is False
    assert payload["starts_execution"] is False
    assert payload["starts_recording"] is False
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False
    assert payload["read_only"] is True
