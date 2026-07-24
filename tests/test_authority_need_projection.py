from seed_runtime.bounded_advancement_horizon import EvidenceSnapshotReference, establish_bounded_advancement_horizon
from seed_runtime.bounded_operator_goal_establishment import establish_bounded_operator_goal_from_closed_choice
from seed_runtime.authority_need_projection import AuthorityRequirementTestimony, AuthorityStandingTestimony, project_authority_need
from tests.test_bounded_operator_goal_establishment import _choice_binding

def _goal(): return establish_bounded_operator_goal_from_closed_choice(_choice_binding("1"), stop_conditions=("stop",))
def _horizon(goal): return establish_bounded_advancement_horizon(goal, present_movement_boundary="boundary", evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:1","snapshot:1"),), potentially_relevant_need_families=("authority",))
def _req(goal,h,**kw):
    base=dict(testimony_ref="req:1",source_ref="src:req",goal_establishment_id=goal.goal_establishment_id,horizon_id=h.horizon_id,evidence_ref="evidence:1",bounded_authority_component_ref="component:1",required_authority_class_ref="authority:write",applicable_scope_ref="scope:repo",owning_stage="bounded_advancement_horizon",requirement_standing="required"); base.update(kw); return AuthorityRequirementTestimony(**base)
def _auth(goal,h,**kw):
    base=dict(testimony_ref="auth:1",source_ref="src:auth",goal_establishment_id=goal.goal_establishment_id,horizon_id=h.horizon_id,evidence_ref="evidence:1",bounded_authority_component_ref="component:1",required_authority_class_ref="authority:write",applicable_scope_ref="scope:repo",owning_stage="bounded_advancement_horizon",authority_standing="unavailable"); base.update(kw); return AuthorityStandingTestimony(**base)
def test_exact_goal_horizon_evidence_component_authority_class_scope_and_ownership_joins():
    g=_goal(); h=_horizon(g); p=project_authority_need(g,h,[_req(g,h)],[_auth(g,h)])
    assert len(p.established)==1; assert p.established[0].need_standing=="established"
    bad=project_authority_need(g,h,[_req(g,h,testimony_ref="bad-goal",goal_establishment_id="other"),_req(g,h,testimony_ref="bad-scope",applicable_scope_ref="")],[_auth(g,h,testimony_ref="a-bad-goal"),_auth(g,h,testimony_ref="a-bad-scope")])
    assert tuple(i.unclassified_reason for i in bad.unclassified)[:2]==("goal_identity_mismatch","missing_applicable_scope")
def test_authority_projection_is_read_only():
    g=_goal(); h=_horizon(g); p=project_authority_need(g,h,[_req(g,h)],[_auth(g,h)])
    assert not p.requests_authority and not p.writes_event_ledger and not p.mutates_cluster
