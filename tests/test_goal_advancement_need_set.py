from seed_runtime.bounded_advancement_horizon import EvidenceSnapshotReference, NeedFamilyExclusion, establish_bounded_advancement_horizon
from seed_runtime.bounded_operator_goal_establishment import establish_bounded_operator_goal_from_closed_choice
from seed_runtime.inquiry_need_projection import RepositoryWorldUncertaintyTestimony, project_inquiry_need
from seed_runtime.goal_advancement_need_set import assemble_goal_advancement_need_set
from tests.test_bounded_operator_goal_establishment import _choice_binding

def _goal(): return establish_bounded_operator_goal_from_closed_choice(_choice_binding("1"), stop_conditions=("stop",))
def _horizon(g, **kw):
    base=dict(present_movement_boundary="boundary", evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:1","snapshot:1"),), potentially_relevant_need_families=("inquiry",)); base.update(kw); return establish_bounded_advancement_horizon(g, **base)
def _inquiry(g,h): return project_inquiry_need(g,h,[RepositoryWorldUncertaintyTestimony("t:1","src:1",g.goal_establishment_id,h.horizon_id,"evidence:1","component:1","subject:1","bounded_advancement_horizon","established")])
def test_need_set_preserves_supplied_absent_and_excluded_family_distinctions_read_only():
    g=_goal(); h=_horizon(g, explicitly_excluded_need_families=(NeedFamilyExclusion("authority","outside"),)); ns=assemble_goal_advancement_need_set(h, inquiry=_inquiry(g,h))
    assert ns.goal_establishment_id==g.goal_establishment_id and ns.horizon_id==h.horizon_id
    dispositions={r.family:r.disposition for r in ns.family_records}
    assert dispositions["inquiry"]=="supplied" and dispositions["authority"]=="excluded" and dispositions["clarification"]=="absent"
    assert not ns.opens_inquiry and not ns.writes_event_ledger and not ns.mutates_cluster
