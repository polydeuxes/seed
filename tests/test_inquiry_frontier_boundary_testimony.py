from seed_runtime.advancement_need_consideration_selection import AdvancementNeedConsiderationEvidence, select_advancement_need_for_consideration
from seed_runtime.advancement_need_reference_set import project_advancement_need_reference_set
from seed_runtime.inquiry_frontier_boundary_testimony import (
    FrontierBoundaryClauseInput,
    preserve_inquiry_frontier_boundary_testimony,
)
from tests.test_advancement_need_reference_set import _need_set


def _selected_inquiry_need():
    reference_set = project_advancement_need_reference_set(_need_set())
    ref = next(r for r in reference_set.references if r.family == "inquiry" and r.native_bucket == "established")
    focus = AdvancementNeedConsiderationEvidence(
        evidence_ref="focus:inquiry-frontier-boundary",
        source_ref="operator:focus",
        reference_id=ref.reference_id,
        need_set_id=ref.need_set_id,
        selection_id=ref.selection_id,
        goal_establishment_id=ref.goal_establishment_id,
        horizon_id=ref.horizon_id,
        family=ref.family,
        native_projection_id=ref.native_projection_id,
        native_lineage=ref.native_lineage,
    )
    return select_advancement_need_for_consideration(reference_set, [focus])


def _clause(ref, family, **overrides):
    data = dict(
        clause_ref=ref,
        clause_family=family,
        clause_text=f"{family} clause",
        producer_ref="stage:frontier-boundary",
        producer_lineage=("producer-lineage:1", "adapter-input:need-selection"),
        source_lineage=("source-lineage:stage-owned-frontier-boundary",),
        evidence_classes=("repository-world-uncertainty-testimony",),
        provenance_roles=("stage-owned-boundary-clause",),
        clause_standing="established",
        scope_disposition="included",
        evidence_currency="current",
        evidence_availability="available",
        family_disposition="inquiry",
    )
    data.update(overrides)
    return FrontierBoundaryClauseInput(**data)


def test_clauses_bind_exact_selected_need_native_item_component_subject_goal_horizon_producer_and_lineage():
    selected = _selected_inquiry_need()
    ref = selected.selected_reference
    testimony = preserve_inquiry_frontier_boundary_testimony(
        selected,
        [_clause("clause:scope", "included_excluded_inquiry_scope", already_visible_evidence_refs=ref.evidence_refs)],
    )

    clause = testimony.clauses[0]
    assert testimony.selected_need_reference_id == ref.reference_id
    assert testimony.native_projection_id == ref.native_projection_id
    assert testimony.native_lineage == ref.native_lineage
    assert testimony.source_testimony_ref == ref.native_lineage[0]
    assert testimony.bounded_uncertainty_component_ref == ref.native_lineage[1]
    assert testimony.repository_world_subject_ref == ref.native_lineage[2]
    assert testimony.need_set_id == ref.need_set_id
    assert testimony.selected_need_selection_id == ref.selection_id
    assert testimony.selected_need_goal_id == ref.goal_establishment_id
    assert testimony.horizon_id == ref.horizon_id
    assert clause.selected_need_reference_id == ref.reference_id
    assert clause.producer_ref == "stage:frontier-boundary"
    assert clause.producer_lineage == ("producer-lineage:1", "adapter-input:need-selection")
    assert clause.source_lineage == ("source-lineage:stage-owned-frontier-boundary",)
    assert clause.ownership_basis == "stage_producer_lineage"


def test_all_clause_families_coexist_unordered_and_dispositions_remain_separate():
    selected = _selected_inquiry_need()
    clauses = [
        _clause("clause:stop", "lawful_stopping_conditions", clause_standing="unknown", scope_disposition="not_applicable"),
        _clause("clause:evidence", "eligible_ineligible_evidence_territory", evidence_currency="stale", evidence_availability="unavailable"),
        _clause("clause:resolution", "sufficient_resolution_conditions", family_disposition="mixed"),
        _clause("clause:scope", "included_excluded_inquiry_scope", scope_disposition="excluded"),
    ]

    testimony = preserve_inquiry_frontier_boundary_testimony(selected, clauses)

    assert tuple(c.clause_ref for c in testimony.clauses) == ("clause:stop", "clause:evidence", "clause:resolution", "clause:scope")
    assert {c.clause_family for c in testimony.clauses} == {
        "included_excluded_inquiry_scope",
        "eligible_ineligible_evidence_territory",
        "sufficient_resolution_conditions",
        "lawful_stopping_conditions",
    }
    evidence_clause = next(c for c in testimony.clauses if c.clause_ref == "clause:evidence")
    assert evidence_clause.clause_standing == "established"
    assert evidence_clause.scope_disposition == "included"
    assert evidence_clause.evidence_currency == "stale"
    assert evidence_clause.evidence_availability == "unavailable"
    assert evidence_clause.family_disposition == "inquiry"


def test_stale_unavailable_out_of_scope_adjacent_and_mixed_do_not_replace_standing():
    selected = _selected_inquiry_need()
    testimony = preserve_inquiry_frontier_boundary_testimony(
        selected,
        [
            _clause("clause:stale", "eligible_ineligible_evidence_territory", clause_standing="unsupported", evidence_currency="stale"),
            _clause("clause:unavailable", "eligible_ineligible_evidence_territory", clause_standing="unknown", evidence_availability="unavailable"),
            _clause("clause:outside", "included_excluded_inquiry_scope", clause_standing="conflicting", scope_disposition="outside_current_scope"),
            _clause("clause:adjacent", "lawful_stopping_conditions", clause_standing="established", family_disposition="adjacent_family"),
            _clause("clause:mixed", "sufficient_resolution_conditions", clause_standing="unclassified", family_disposition="mixed"),
        ],
    )

    by_ref = {c.clause_ref: c for c in testimony.clauses}
    assert by_ref["clause:stale"].clause_standing == "unsupported"
    assert by_ref["clause:unavailable"].clause_standing == "unknown"
    assert by_ref["clause:outside"].clause_standing == "conflicting"
    assert by_ref["clause:adjacent"].clause_standing == "established"
    assert by_ref["clause:mixed"].clause_standing == "unclassified"


def test_ownership_cannot_be_asserted_through_payload_flags():
    selected = _selected_inquiry_need()
    testimony = preserve_inquiry_frontier_boundary_testimony(
        selected,
        [
            _clause("clause:payload-owned", "included_excluded_inquiry_scope", producer_ref="", producer_lineage=(), caller_asserts_ownership=True),
            _clause("clause:adapter-owned", "included_excluded_inquiry_scope", producer_ref="", producer_lineage=(), adapter_ref="adapter:stage", adapter_lineage=("adapter-lineage:1",), caller_asserts_ownership=False),
        ],
    )

    by_ref = {c.clause_ref: c for c in testimony.clauses}
    assert by_ref["clause:payload-owned"].ownership_basis == "unowned"
    assert "clause:payload-owned" in testimony.unowned_clause_refs
    assert by_ref["clause:adapter-owned"].ownership_basis == "adapter_lineage"


def test_visible_evidence_is_not_automatically_eligible_and_eligible_territory_selects_nothing():
    selected = _selected_inquiry_need()
    ref = selected.selected_reference
    testimony = preserve_inquiry_frontier_boundary_testimony(
        selected,
        [_clause("clause:evidence", "eligible_ineligible_evidence_territory", already_visible_evidence_refs=ref.evidence_refs, eligible_evidence_territory_refs=("territory:repo-world-current-state",))],
    )

    clause = testimony.clauses[0]
    assert testimony.already_visible_evidence_refs == ref.evidence_refs
    assert clause.already_visible_evidence_refs == ref.evidence_refs
    assert clause.eligible_evidence_territory_refs == ("territory:repo-world-current-state",)
    assert clause.eligible_evidence_territory_refs != clause.already_visible_evidence_refs
    assert not testimony.selects_sources
    assert not testimony.selects_observations


def test_boundary_testimony_has_no_frontier_question_opening_authorization_execution_recording_ledger_or_mutation():
    selected = _selected_inquiry_need()
    testimony = preserve_inquiry_frontier_boundary_testimony(selected, [_clause("clause:scope", "included_excluded_inquiry_scope")])

    assert testimony.read_only
    assert not testimony.assembles_frontier
    assert not testimony.formulates_question
    assert not testimony.opens_inquiry
    assert not testimony.authorizes_access
    assert not testimony.starts_execution
    assert not testimony.starts_recording
    assert not testimony.writes_event_ledger
    assert not testimony.mutates_cluster
    assert not testimony.judges_collective_sufficiency
