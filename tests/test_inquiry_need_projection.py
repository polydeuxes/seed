from seed_runtime.bounded_advancement_horizon import EvidenceSnapshotReference, NeedFamilyExclusion, establish_bounded_advancement_horizon
from seed_runtime.bounded_operator_goal_establishment import establish_bounded_operator_goal_from_closed_choice
from seed_runtime.inquiry_need_projection import RepositoryWorldUncertaintyTestimony, project_inquiry_need
from tests.test_bounded_operator_goal_establishment import _choice_binding

def _goal(): return establish_bounded_operator_goal_from_closed_choice(_choice_binding("1"), stop_conditions=("stop",))
def _horizon(goal, **kw):
    base=dict(present_movement_boundary="boundary", evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:1","snapshot:1"),), potentially_relevant_need_families=("inquiry",)); base.update(kw); return establish_bounded_advancement_horizon(goal, **base)
def _t(goal,horizon,**kw):
    base=dict(testimony_ref="t:1", source_ref="src:1", goal_establishment_id=goal.goal_establishment_id, horizon_id=horizon.horizon_id, evidence_ref="evidence:1", bounded_uncertainty_component_ref="component:1", repository_world_subject_ref="subject:1", owning_stage="bounded_advancement_horizon", standing="established"); base.update(kw); return RepositoryWorldUncertaintyTestimony(**base)
def test_requires_exact_goal_horizon_component_subject_and_evidence_identity_matching():
    goal=_goal(); horizon=_horizon(goal); p=project_inquiry_need(goal,horizon,[_t(goal,horizon),_t(goal,horizon,testimony_ref="bad-goal",goal_establishment_id="other"),_t(goal,horizon,testimony_ref="bad-horizon",horizon_id="other"),_t(goal,horizon,testimony_ref="bad-evidence",evidence_ref="other"),_t(goal,horizon,testimony_ref="bad-component",bounded_uncertainty_component_ref=""),_t(goal,horizon,testimony_ref="bad-subject",repository_world_subject_ref="")])
    assert len(p.established)==1
    assert tuple(i.unclassified_reason for i in p.unclassified)==("goal_identity_mismatch","horizon_identity_mismatch","evidence_identity_mismatch","not_component_bounded","missing_repository_world_subject")
def test_excluded_inquiry_family_remains_distinct_and_read_only():
    goal=_goal(); horizon=_horizon(goal, explicitly_excluded_need_families=(NeedFamilyExclusion("inquiry","outside"),)); p=project_inquiry_need(goal,horizon,[_t(goal,horizon)])
    assert len(p.excluded_family)==1; assert not p.opens_inquiry and not p.writes_event_ledger and not p.mutates_cluster
