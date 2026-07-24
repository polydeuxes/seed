from seed_runtime.bounded_advancement_horizon import EvidenceSnapshotReference, establish_bounded_advancement_horizon
from seed_runtime.bounded_operator_goal_establishment import establish_bounded_operator_goal_from_closed_choice
from seed_runtime.operational_realization_need_projection import OperationalRealizationRequirementTestimony, OperationalRealizationStandingTestimony, project_operational_realization_need
from tests.test_bounded_operator_goal_establishment import _choice_binding

def _goal(): return establish_bounded_operator_goal_from_closed_choice(_choice_binding("1"), stop_conditions=("stop",))
def _horizon(goal): return establish_bounded_advancement_horizon(goal, present_movement_boundary="boundary", evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:1","snapshot:1"),), potentially_relevant_need_families=("operational_realization",))
def _req(goal,h,**kw):
    base=dict(testimony_ref="req:1",source_ref="src:req",goal_establishment_id=goal.goal_establishment_id,horizon_id=h.horizon_id,evidence_ref="evidence:1",bounded_realization_component_ref="component:1",required_transformation_ref="transform:apply",applicable_scope_ref="scope:repo",owning_stage="bounded_advancement_horizon",requirement_standing="required"); base.update(kw); return OperationalRealizationRequirementTestimony(**base)
def _standing(goal,h,**kw):
    base=dict(testimony_ref="standing:1",source_ref="src:standing",goal_establishment_id=goal.goal_establishment_id,horizon_id=h.horizon_id,evidence_ref="evidence:1",bounded_realization_component_ref="component:1",required_transformation_ref="transform:apply",applicable_scope_ref="scope:repo",owning_stage="bounded_advancement_horizon",availability_standing="unavailable",coverage_standing="complete_for_horizon",blocker_family_ownership="operational_realization"); base.update(kw); return OperationalRealizationStandingTestimony(**base)
def test_exact_goal_horizon_evidence_component_transformation_scope_and_ownership_joins():
    g=_goal(); h=_horizon(g); p=project_operational_realization_need(g,h,[_req(g,h)],[_standing(g,h)])
    assert len(p.established)==1; assert p.established[0].need_standing=="established"
def test_operational_realization_projection_is_read_only():
    g=_goal(); h=_horizon(g); p=project_operational_realization_need(g,h,[_req(g,h)],[_standing(g,h)])
    assert not p.selects_realization and not p.writes_event_ledger and not p.mutates_cluster
