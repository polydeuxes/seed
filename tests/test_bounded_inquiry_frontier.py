from seed_runtime.bounded_inquiry_frontier import assemble_bounded_inquiry_frontier
from seed_runtime.inquiry_frontier_boundary_testimony import preserve_inquiry_frontier_boundary_testimony
from tests.test_inquiry_frontier_boundary_testimony import _clause, _selected_inquiry_need


def _frontier(*clauses):
    selected = _selected_inquiry_need()
    testimony = preserve_inquiry_frontier_boundary_testimony(selected, clauses)
    return selected, testimony, assemble_bounded_inquiry_frontier(selected, testimony)


def _required_clauses():
    return (
        _clause("clause:scope", "included_excluded_inquiry_scope", scope_disposition="included"),
        _clause("clause:evidence", "eligible_ineligible_evidence_territory", eligible_evidence_territory_refs=("territory:repo-world",)),
        _clause("clause:resolution", "sufficient_resolution_conditions"),
        _clause("clause:stop", "lawful_stopping_conditions"),
    )


def test_established_frontier_binds_exact_selected_need_native_item_goal_horizon_and_testimony_identity():
    selected, testimony, frontier = _frontier(*_required_clauses())
    ref = selected.selected_reference

    assert frontier.frontier_state == "established"
    assert frontier.selected_need_selection_id == selected.selection_id
    assert frontier.selected_need_reference_id == ref.reference_id
    assert frontier.native_projection_id == ref.native_projection_id
    assert frontier.native_lineage == ref.native_lineage
    assert frontier.source_testimony_ref == ref.native_lineage[0]
    assert frontier.bounded_uncertainty_component_ref == ref.native_lineage[1]
    assert frontier.repository_world_subject_ref == ref.native_lineage[2]
    assert frontier.need_set_id == ref.need_set_id
    assert frontier.selected_goal_id == ref.goal_establishment_id
    assert frontier.horizon_id == ref.horizon_id
    assert frontier.testimony_id == testimony.testimony_id
    assert frontier.preserved_clause_refs == tuple(c.clause_ref for c in testimony.clauses)
    assert frontier.operative_clause_refs == frontier.preserved_clause_refs


def test_establishment_requires_all_four_coherent_clause_families_and_missing_remain_explicit():
    _, _, frontier = _frontier(*_required_clauses()[:3])

    assert frontier.frontier_state == "missing_required_clause_family"
    assert frontier.missing_required_clause_families == ("lawful_stopping_conditions",)
    assert frontier.material_conflict_clause_refs == ()


def test_material_conflicts_prevent_establishment_without_repairing_boundary():
    clauses = list(_required_clauses())
    clauses.append(_clause("clause:conflict", "lawful_stopping_conditions", clause_standing="conflicting"))

    _, _, frontier = _frontier(*clauses)

    assert frontier.frontier_state == "material_binding_conflict"
    assert "clause:conflict" in frontier.material_conflict_clause_refs
    assert "clause:conflict" in frontier.conflicting_clause_refs
    assert "clause:conflict" in frontier.preserved_clause_refs


def test_unsupported_unknown_mixed_adjacent_stale_unavailable_and_out_of_scope_are_preserved_non_operative():
    clauses = list(_required_clauses())
    clauses.extend(
        [
            _clause("clause:unsupported", "eligible_ineligible_evidence_territory", clause_standing="unsupported"),
            _clause("clause:unknown", "sufficient_resolution_conditions", clause_standing="unknown"),
            _clause("clause:mixed", "lawful_stopping_conditions", family_disposition="mixed"),
            _clause("clause:adjacent", "lawful_stopping_conditions", family_disposition="adjacent_family"),
            _clause("clause:stale", "eligible_ineligible_evidence_territory", evidence_currency="stale"),
            _clause("clause:unavailable", "eligible_ineligible_evidence_territory", evidence_availability="unavailable"),
            _clause("clause:outside", "included_excluded_inquiry_scope", scope_disposition="outside_current_scope"),
        ]
    )

    _, _, frontier = _frontier(*clauses)

    assert frontier.frontier_state == "established"
    for ref in (
        "clause:unsupported",
        "clause:unknown",
        "clause:mixed",
        "clause:adjacent",
        "clause:outside",
    ):
        assert ref in frontier.preserved_clause_refs
        assert ref in frontier.non_operative_clause_refs
        assert ref not in frontier.operative_clause_refs
    assert frontier.unsupported_clause_refs == ("clause:unsupported",)
    assert frontier.unknown_clause_refs == ("clause:unknown",)
    assert frontier.mixed_clause_refs == ("clause:mixed",)
    assert frontier.adjacent_family_clause_refs == ("clause:adjacent",)
    assert frontier.stale_clause_refs == ("clause:stale",)
    assert frontier.unavailable_clause_refs == ("clause:unavailable",)
    assert frontier.out_of_scope_clause_refs == ("clause:outside",)


def test_no_scope_invention_question_opening_source_selection_authorization_execution_recording_ledger_or_mutation():
    _, _, frontier = _frontier(*_required_clauses())

    assert frontier.read_only
    assert not frontier.invents_scope
    assert not frontier.invents_evidence_admission
    assert not frontier.formulates_question
    assert not frontier.opens_inquiry
    assert not frontier.selects_sources
    assert not frontier.selects_observations
    assert not frontier.authorizes_access
    assert not frontier.starts_execution
    assert not frontier.starts_recording
    assert not frontier.writes_event_ledger
    assert not frontier.mutates_cluster
    assert not frontier.result_known
