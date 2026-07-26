from seed_runtime.bounded_advancement_horizon import EvidenceSnapshotReference, GoalAdvancementDemandFamilyExclusion, establish_bounded_advancement_horizon
from seed_runtime.bounded_operator_goal_establishment import establish_bounded_operator_goal_from_closed_choice
from seed_runtime.inquiry_demand_projection import RepositoryWorldUncertaintyTestimony, project_inquiry_demand
from typing import get_args

from seed_runtime.goal_advancement_demand_set import GoalAdvancementDemandFamily, assemble_goal_advancement_demand_set
from tests.test_bounded_operator_goal_establishment import _choice_binding

def _goal(): return establish_bounded_operator_goal_from_closed_choice(_choice_binding("1"))
def _horizon(g, **kw):
    base=dict(present_movement_boundary="boundary", evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:1","snapshot:1"),), potentially_relevant_goal_advancement_demand_families=("inquiry",)); base.update(kw); return establish_bounded_advancement_horizon(g, **base)
def _inquiry(g,h): return project_inquiry_demand(g,h,[RepositoryWorldUncertaintyTestimony("t:1","src:1",g.goal_establishment_id,h.horizon_id,"evidence:1","component:1","subject:1","bounded_advancement_horizon","established")])
def test_demand_set_preserves_supplied_absent_and_excluded_family_distinctions_read_only():
    g=_goal(); h=_horizon(g, explicitly_excluded_goal_advancement_demand_families=(GoalAdvancementDemandFamilyExclusion("authority","outside"),)); ns=assemble_goal_advancement_demand_set(h, inquiry=_inquiry(g,h))
    assert ns.goal_establishment_id==g.goal_establishment_id and ns.horizon_id==h.horizon_id
    dispositions={r.family:r.disposition for r in ns.family_records}
    assert dispositions["inquiry"]=="supplied" and dispositions["authority"]=="excluded" and dispositions["clarification"]=="absent"
    assert not ns.opens_inquiry and not ns.writes_event_ledger and not ns.mutates_cluster


def test_goal_advancement_demand_family_inventory_is_exactly_the_four_local_families():
    families = set(get_args(GoalAdvancementDemandFamily))
    assert families == {
        "clarification",
        "inquiry",
        "authority",
        "operational_realization",
    }
    assert families.isdisjoint({"capability", "common_grammar", "competency", "learning"})
