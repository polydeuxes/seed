from seed_runtime.advancement_need_consideration_selection import AdvancementNeedConsiderationEvidence, select_advancement_need_for_consideration
from seed_runtime.advancement_need_reference_set import project_advancement_need_reference_set
from seed_runtime.goal_advancement_need_set import assemble_goal_advancement_need_set
from seed_runtime.inquiry_frontier_boundary_testimony import FrontierBoundaryClauseInput, preserve_inquiry_frontier_boundary_testimony
from tests.test_goal_advancement_need_set import _goal, _horizon, _inquiry

def _selection():
    g=_goal(); h=_horizon(g); rs=project_advancement_need_reference_set(assemble_goal_advancement_need_set(h, inquiry=_inquiry(g,h))); ref=rs.references[0]
    ev=AdvancementNeedConsiderationEvidence("ev:select","src:select",ref.reference_id,ref.need_set_id,ref.goal_establishment_id,ref.horizon_id,ref.family,ref.native_projection_id,ref.native_lineage)
    return select_advancement_need_for_consideration(rs,[ev]), ref

def test_frontier_boundary_testimony_preserves_selected_inquiry_need_identity_read_only():
    sel, ref=_selection(); t=preserve_inquiry_frontier_boundary_testimony(sel,[FrontierBoundaryClauseInput("clause:scope","included_excluded_inquiry_scope","scope",producer_ref="producer",producer_lineage=("lineage",),clause_standing="established",scope_disposition="included",evidence_currency="current",evidence_availability="available",family_disposition="inquiry")])
    assert t.selected_need_reference_id==ref.reference_id and t.need_set_id==ref.need_set_id and t.selected_need_goal_id==ref.goal_establishment_id and t.horizon_id==ref.horizon_id
    assert len(t.clauses)==1
    assert not t.assembles_frontier and not t.opens_inquiry and not t.writes_event_ledger and not t.mutates_cluster
