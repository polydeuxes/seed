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


def test_frontier_binds_exact_selected_need_native_item_goal_horizon_and_testimony_identity_while_missing_unwarranted_evidence_family():
    selected, testimony, frontier = _frontier(*_required_clauses())
    ref = selected.selected_reference

    assert frontier.frontier_state == "missing_required_clause_family"
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
    assert frontier.operative_clause_refs == ("clause:scope", "clause:resolution", "clause:stop")
    assert frontier.missing_required_clause_families == ("eligible_ineligible_evidence_territory",)


def test_establishment_requires_all_four_coherent_clause_families_and_missing_remain_explicit():
    _, _, frontier = _frontier(*_required_clauses()[:3])

    assert frontier.frontier_state == "missing_required_clause_family"
    assert frontier.missing_required_clause_families == ("eligible_ineligible_evidence_territory", "lawful_stopping_conditions")
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

    assert frontier.frontier_state == "missing_required_clause_family"
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
    assert frontier.unknown_currency_clause_refs == ()
    assert frontier.unavailable_clause_refs == ("clause:unavailable",)
    assert frontier.unknown_availability_clause_refs == ()
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


def test_eligible_evidence_territory_reference_is_preserved_but_not_positive_family_support_without_warrant():
    selected, testimony, frontier = _frontier(*_required_clauses())

    evidence_clause = next(c for c in testimony.clauses if c.clause_ref == "clause:evidence")
    assert evidence_clause.clause_family == "eligible_ineligible_evidence_territory"
    assert evidence_clause.eligible_evidence_territory_refs == ("territory:repo-world",)
    assert evidence_clause.producer_ref == "stage:frontier-boundary"
    assert evidence_clause.ownership_basis == "stage_producer_lineage"
    assert "clause:evidence" in frontier.preserved_clause_refs
    assert "clause:evidence" in frontier.non_operative_clause_refs
    assert "clause:evidence" not in frontier.operative_clause_refs
    assert frontier.missing_required_clause_families == ("eligible_ineligible_evidence_territory",)
    assert frontier.frontier_state == "missing_required_clause_family"


def test_eligible_evidence_territory_label_without_territory_warrant_is_preserved_but_not_operative():
    clauses = list(_required_clauses())
    clauses[1] = _clause(
        "clause:evidence-unwarranted",
        "eligible_ineligible_evidence_territory",
        eligible_evidence_territory_refs=(),
    )

    _, testimony, frontier = _frontier(*clauses)

    evidence_clause = next(c for c in testimony.clauses if c.clause_ref == "clause:evidence-unwarranted")
    assert evidence_clause.clause_standing == "established"
    assert evidence_clause.family_disposition == "inquiry"
    assert evidence_clause.scope_disposition == "included"
    assert evidence_clause.evidence_currency == "current"
    assert evidence_clause.evidence_availability == "available"
    assert evidence_clause.clause_family == "eligible_ineligible_evidence_territory"
    assert evidence_clause.eligible_evidence_territory_refs == ()
    assert testimony.to_json_dict()["clauses"][1]["clause_ref"] == "clause:evidence-unwarranted"
    assert "clause:evidence-unwarranted" in frontier.preserved_clause_refs
    assert "clause:evidence-unwarranted" in frontier.non_operative_clause_refs
    assert "clause:evidence-unwarranted" not in frontier.operative_clause_refs
    assert frontier.missing_required_clause_families == ("eligible_ineligible_evidence_territory",)
    assert frontier.frontier_state == "missing_required_clause_family"


def test_positive_dispositions_and_family_label_do_not_repair_missing_eligible_territory_warrant_or_create_operations():
    clauses = list(_required_clauses())
    clauses[1] = _clause(
        "clause:evidence-positive-no-territory",
        "eligible_ineligible_evidence_territory",
        eligible_evidence_territory_refs=(),
        source_lineage=("source-lineage:stage-owned-frontier-boundary", "adapter:copied-positive-coordinates"),
        already_visible_evidence_refs=("visible:evidence:copied",),
    )

    _, testimony, frontier = _frontier(*clauses)

    evidence_clause = next(c for c in frontier.clauses if c.clause_ref == "clause:evidence-positive-no-territory")
    assert evidence_clause.producer_ref == "stage:frontier-boundary"
    assert evidence_clause.source_lineage == ("source-lineage:stage-owned-frontier-boundary", "adapter:copied-positive-coordinates")
    assert evidence_clause.already_visible_evidence_refs == ("visible:evidence:copied",)
    assert evidence_clause.eligible_evidence_territory_refs == ()
    assert evidence_clause.clause_standing == "established"
    assert evidence_clause.family_disposition == "inquiry"
    assert evidence_clause.evidence_currency == "current"
    assert evidence_clause.evidence_availability == "available"
    assert frontier.frontier_state == "missing_required_clause_family"
    assert frontier.missing_required_clause_families == ("eligible_ineligible_evidence_territory",)
    assert "clause:evidence-positive-no-territory" in frontier.preserved_clause_refs
    assert "clause:evidence-positive-no-territory" in frontier.non_operative_clause_refs
    assert not testimony.opens_inquiry
    assert not testimony.selects_sources
    assert not testimony.selects_observations
    assert not testimony.authorizes_access
    assert not testimony.starts_execution
    assert not testimony.starts_recording
    assert not testimony.writes_event_ledger
    assert not testimony.mutates_cluster
    assert not frontier.opens_inquiry
    assert not frontier.selects_sources
    assert not frontier.selects_observations
    assert not frontier.authorizes_access
    assert not frontier.starts_execution
    assert not frontier.starts_recording
    assert not frontier.writes_event_ledger
    assert not frontier.mutates_cluster


def test_non_empty_eligible_territory_ref_with_limited_availability_or_currency_is_preserved_non_operative():
    cases = (
        ("clause:evidence-unavailable", {"evidence_availability": "unavailable"}, "unavailable_clause_refs"),
        ("clause:evidence-unknown-availability", {"evidence_availability": "unknown"}, "unknown_availability_clause_refs"),
        ("clause:evidence-stale", {"evidence_currency": "stale"}, "stale_clause_refs"),
        ("clause:evidence-unknown-currency", {"evidence_currency": "unknown"}, "unknown_currency_clause_refs"),
    )

    for clause_ref, overrides, limitation_field in cases:
        clauses = list(_required_clauses())
        clauses[1] = _clause(
            clause_ref,
            "eligible_ineligible_evidence_territory",
            eligible_evidence_territory_refs=("territory:repo-world",),
            **overrides,
        )

        _, testimony, frontier = _frontier(*clauses)
        evidence_clause = next(c for c in testimony.clauses if c.clause_ref == clause_ref)

        assert evidence_clause.eligible_evidence_territory_refs == ("territory:repo-world",)
        assert clause_ref in frontier.preserved_clause_refs
        assert clause_ref in frontier.non_operative_clause_refs
        assert clause_ref not in frontier.operative_clause_refs
        assert clause_ref in getattr(frontier, limitation_field)
        assert frontier.missing_required_clause_families == ("eligible_ineligible_evidence_territory",)
        assert frontier.frontier_state == "missing_required_clause_family"
        assert not frontier.opens_inquiry
        assert not frontier.selects_sources
        assert not frontier.selects_observations
        assert not frontier.authorizes_access
        assert not frontier.starts_execution
        assert not frontier.starts_recording
        assert not frontier.writes_event_ledger
        assert not frontier.mutates_cluster


def test_unknown_currency_and_availability_are_not_reported_as_stale_or_unavailable():
    clauses = list(_required_clauses())
    clauses.extend([
        _clause("clause:unknown-currency", "eligible_ineligible_evidence_territory", evidence_currency="unknown"),
        _clause("clause:unknown-availability", "eligible_ineligible_evidence_territory", evidence_availability="unknown"),
    ])

    _, _, frontier = _frontier(*clauses)

    assert "clause:unknown-currency" in frontier.unknown_currency_clause_refs
    assert "clause:unknown-currency" not in frontier.stale_clause_refs
    assert "clause:unknown-availability" in frontier.unknown_availability_clause_refs
    assert "clause:unknown-availability" not in frontier.unavailable_clause_refs


def test_currency_and_availability_do_not_apply_as_unsupported_global_gates_to_neighboring_families():
    clauses = [
        _clause("clause:scope", "included_excluded_inquiry_scope", evidence_currency="unknown", evidence_availability="unknown"),
        _clause("clause:evidence", "eligible_ineligible_evidence_territory", eligible_evidence_territory_refs=("territory:repo-world",)),
        _clause("clause:resolution", "sufficient_resolution_conditions", evidence_currency="unknown"),
        _clause("clause:stop", "lawful_stopping_conditions", evidence_availability="unknown"),
    ]

    _, _, frontier = _frontier(*clauses)

    assert "clause:scope" in frontier.operative_clause_refs
    assert "clause:resolution" in frontier.operative_clause_refs
    assert "clause:stop" in frontier.operative_clause_refs
    assert "clause:evidence" not in frontier.operative_clause_refs
    assert frontier.missing_required_clause_families == ("eligible_ineligible_evidence_territory",)
