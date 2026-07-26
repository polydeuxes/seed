from seed_runtime.goal_advancement_demand_consideration_selection import GoalAdvancementDemandConsiderationEvidence, select_goal_advancement_demand_for_consideration
from seed_runtime.goal_advancement_demand_reference_set import project_goal_advancement_demand_reference_set
from seed_runtime.goal_advancement_demand_set import assemble_goal_advancement_demand_set
from tests.test_goal_advancement_demand_set import _goal, _horizon, _inquiry

def test_demand_selection_selects_exact_selectable_reference_read_only():
    g=_goal(); h=_horizon(g); rs=project_goal_advancement_demand_reference_set(assemble_goal_advancement_demand_set(h, inquiry=_inquiry(g,h))); ref=rs.references[0]
    ev=GoalAdvancementDemandConsiderationEvidence("ev:select","src:select",ref.reference_id,ref.goal_advancement_demand_set_id,ref.goal_establishment_id,ref.horizon_id,ref.family,ref.native_projection_id,ref.native_lineage)
    selection=select_goal_advancement_demand_for_consideration(rs,[ev])
    assert selection.selection_state=="selected" and selection.selected_reference==ref
    assert not selection.prioritizes_demands and not selection.opens_inquiry and not selection.writes_event_ledger and not selection.mutates_cluster
