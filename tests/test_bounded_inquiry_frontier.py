from seed_runtime.inquiry_frontier_boundary_testimony import FrontierBoundaryClauseInput, preserve_inquiry_frontier_boundary_testimony
from seed_runtime.bounded_inquiry_frontier import assemble_bounded_inquiry_frontier
from tests.test_inquiry_frontier_boundary_testimony import _selection

def _clause(ref,family):
    return FrontierBoundaryClauseInput(ref,family,ref,producer_ref="producer",producer_lineage=("lineage",),clause_standing="established",scope_disposition="included",evidence_currency="current",evidence_availability="available",family_disposition="inquiry")
def test_bounded_inquiry_frontier_preserves_selected_need_and_remains_read_only():
    sel, ref=_selection(); testimony=preserve_inquiry_frontier_boundary_testimony(sel,[_clause("scope","included_excluded_inquiry_scope"),_clause("resolution","sufficient_resolution_conditions"),_clause("stop","lawful_stopping_conditions")])
    frontier=assemble_bounded_inquiry_frontier(sel,testimony)
    assert frontier.advancement_need_selection_id==sel.selection_id and frontier.selected_need_reference_id==ref.reference_id
    assert frontier.need_set_id==ref.need_set_id and frontier.selected_goal_id==ref.goal_establishment_id and frontier.horizon_id==ref.horizon_id
    assert not frontier.formulates_question and not frontier.opens_inquiry and not frontier.writes_event_ledger and not frontier.mutates_cluster
