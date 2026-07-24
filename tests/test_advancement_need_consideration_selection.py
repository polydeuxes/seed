from seed_runtime.advancement_need_consideration_selection import AdvancementNeedConsiderationEvidence, select_advancement_need_for_consideration
from seed_runtime.advancement_need_reference_set import project_advancement_need_reference_set
from seed_runtime.goal_advancement_need_set import assemble_goal_advancement_need_set
from tests.test_goal_advancement_need_set import _goal, _horizon, _inquiry

def test_need_selection_selects_exact_selectable_reference_read_only():
    g=_goal(); h=_horizon(g); rs=project_advancement_need_reference_set(assemble_goal_advancement_need_set(h, inquiry=_inquiry(g,h))); ref=rs.references[0]
    ev=AdvancementNeedConsiderationEvidence("ev:select","src:select",ref.reference_id,ref.need_set_id,ref.goal_establishment_id,ref.horizon_id,ref.family,ref.native_projection_id,ref.native_lineage)
    selection=select_advancement_need_for_consideration(rs,[ev])
    assert selection.selection_state=="selected" and selection.selected_reference==ref
    assert not selection.prioritizes_needs and not selection.opens_inquiry and not selection.writes_event_ledger and not selection.mutates_cluster
