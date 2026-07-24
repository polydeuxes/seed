from tests.test_goal_advancement_need_set import _goal, _horizon, _inquiry
from seed_runtime.goal_advancement_need_set import assemble_goal_advancement_need_set
from seed_runtime.advancement_need_reference_set import project_advancement_need_reference_set

def test_reference_set_exposes_established_native_inquiry_need_without_selecting():
    g=_goal(); h=_horizon(g); ns=assemble_goal_advancement_need_set(h, inquiry=_inquiry(g,h)); rs=project_advancement_need_reference_set(ns)
    assert len(rs.references)==1
    ref=rs.references[0]
    assert ref.need_set_id==ns.need_set_id and ref.goal_establishment_id==g.goal_establishment_id and ref.horizon_id==h.horizon_id
    assert ref.family=="inquiry" and ref.selectable is True
    assert not rs.selects_need and not rs.writes_event_ledger and not rs.mutates_cluster
