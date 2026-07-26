from tests.test_goal_advancement_demand_set import _goal, _horizon, _inquiry
from seed_runtime.goal_advancement_demand_set import assemble_goal_advancement_demand_set
from seed_runtime.goal_advancement_demand_reference_set import project_goal_advancement_demand_reference_set

def test_reference_set_exposes_established_native_inquiry_demand_without_selecting():
    g=_goal(); h=_horizon(g); ns=assemble_goal_advancement_demand_set(h, inquiry=_inquiry(g,h)); rs=project_goal_advancement_demand_reference_set(ns)
    assert len(rs.references)==1
    ref=rs.references[0]
    assert ref.goal_advancement_demand_set_id==ns.goal_advancement_demand_set_id and ref.goal_establishment_id==g.goal_establishment_id and ref.horizon_id==h.horizon_id
    assert ref.family=="inquiry" and ref.selectable is True
    assert not rs.selects_demand and not rs.writes_event_ledger and not rs.mutates_cluster
