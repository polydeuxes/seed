from dataclasses import replace

from seed_runtime.advancement_need_family_coverage_set import (
    ExplicitComponentExclusion,
    FamilyBoundedCandidateSpace,
    FamilyCoverageTestimony,
    assemble_advancement_need_family_coverage_set,
    advancement_need_family_coverage_set_json,
)
from seed_runtime.bounded_advancement_horizon import (
    EvidenceSnapshotReference,
    NeedFamilyExclusion,
    establish_bounded_advancement_horizon,
)
from tests.test_clarification_need_projection import _goal, _selection

FAMILIES = ("clarification", "inquiry", "authority", "operational_realization")


def _horizon(selection, goal, **overrides):
    base = dict(
        present_movement_boundary="family coverage for exact selected goal and horizon",
        evidence_snapshot_refs=(
            EvidenceSnapshotReference("evidence:coverage", "snapshot:coverage"),
        ),
        potentially_relevant_need_families=FAMILIES,
    )
    base.update(overrides)
    return establish_bounded_advancement_horizon(selection, goal, **base)


def _space(family, selection, goal, horizon, components=("component:1", "component:2")):
    return FamilyBoundedCandidateSpace(
        family,
        f"candidate-space:{family}",
        selection.selection_id,
        goal.goal_establishment_id,
        horizon.horizon_id,
        f"projection:{family}",
        "snapshot:coverage",
        components,
    )


def _testimony(family, selection, goal, horizon, **overrides):
    base = dict(
        family=family,
        testimony_id=f"testimony:{family}",
        selection_id=selection.selection_id,
        goal_establishment_id=goal.goal_establishment_id,
        horizon_id=horizon.horizon_id,
        native_projection_id=f"projection:{family}",
        candidate_space_id=f"candidate-space:{family}",
        evidence_snapshot_ref="snapshot:coverage",
        covered_component_refs=("component:1",),
        unexamined_component_refs=("component:2",),
    )
    base.update(overrides)
    return FamilyCoverageTestimony(**base)


def _records(coverage_set):
    return {record.family: record for record in coverage_set.family_records}


def test_exact_identity_matching_for_goal_horizon_evidence_projection_and_candidate_space():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(selection, goal)
    testimony = _testimony(
        "clarification",
        selection,
        goal,
        horizon,
        covered_component_refs=("component:1", "component:2"),
        unexamined_component_refs=(),
    )
    coverage_set = assemble_advancement_need_family_coverage_set(
        horizon,
        candidate_spaces=(_space("clarification", selection, goal, horizon),),
        testimonies=(testimony,),
    )
    record = _records(coverage_set)["clarification"]

    assert record.selection_id == selection.selection_id
    assert record.goal_establishment_id == goal.goal_establishment_id
    assert record.horizon_id == horizon.horizon_id
    assert record.native_projection_id == "projection:clarification"
    assert record.candidate_space_id == "candidate-space:clarification"
    assert record.evidence_snapshot_ref == "snapshot:coverage"
    assert record.coverage_standing == "complete_for_horizon"


def test_scope_disposition_is_separate_from_coverage_standing_and_excluded_is_not_evaluated():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(
        selection,
        goal,
        explicitly_excluded_need_families=(
            NeedFamilyExclusion("inquiry", "outside this horizon"),
        ),
    )
    coverage_set = assemble_advancement_need_family_coverage_set(
        horizon,
        candidate_spaces=(_space("clarification", selection, goal, horizon),),
        testimonies=(_testimony("clarification", selection, goal, horizon),),
    )
    records = _records(coverage_set)

    assert records["clarification"].scope_disposition == "included"
    assert records["clarification"].coverage_standing == "partial"
    assert records["inquiry"].scope_disposition == "excluded"
    assert records["inquiry"].horizon_exclusion_reason == "outside this horizon"
    assert records["inquiry"].coverage_standing == "not_evaluated"


def test_complete_requires_bounded_candidate_space_and_complete_accounting_with_reasoned_exclusions():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(selection, goal)
    testimony = _testimony(
        "authority",
        selection,
        goal,
        horizon,
        covered_component_refs=("component:1",),
        unexamined_component_refs=(),
        explicitly_excluded_components=(
            ExplicitComponentExclusion(
                "component:2", "not relevant to bounded horizon"
            ),
        ),
    )
    without_space = assemble_advancement_need_family_coverage_set(
        horizon, testimonies=(testimony,)
    )
    with_space = assemble_advancement_need_family_coverage_set(
        horizon,
        candidate_spaces=(_space("authority", selection, goal, horizon),),
        testimonies=(testimony,),
    )

    assert _records(without_space)["authority"].coverage_standing == "unknown"
    assert _records(with_space)["authority"].coverage_standing == "complete_for_horizon"


def test_partial_absent_stale_unavailable_unknown_and_conflicting_testimony_cannot_become_complete():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(selection, goal)
    cases = [
        (
            "clarification",
            _testimony("clarification", selection, goal, horizon),
            "partial",
        ),
        ("inquiry", None, "unknown"),
        (
            "authority",
            _testimony("authority", selection, goal, horizon, stale=True),
            "partial",
        ),
        (
            "operational_realization",
            _testimony(
                "operational_realization", selection, goal, horizon, unavailable=True
            ),
            "unknown",
        ),
    ]
    coverage_set = assemble_advancement_need_family_coverage_set(
        horizon,
        candidate_spaces=tuple(_space(f, selection, goal, horizon) for f in FAMILIES),
        testimonies=tuple(t for _, t, _ in cases if t),
    )
    records = _records(coverage_set)
    for family, _, expected in cases:
        assert records[family].coverage_standing == expected

    conflicted = replace(
        _testimony("authority", selection, goal, horizon),
        conflicts=("material coverage conflict",),
    )
    assert (
        _records(
            assemble_advancement_need_family_coverage_set(
                horizon,
                candidate_spaces=(_space("authority", selection, goal, horizon),),
                testimonies=(conflicted,),
            )
        )["authority"].coverage_standing
        == "conflicting"
    )


def test_supplied_or_empty_projection_identity_does_not_imply_complete_coverage():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(selection, goal)
    space = _space("clarification", selection, goal, horizon, components=())
    testimony = _testimony(
        "clarification",
        selection,
        goal,
        horizon,
        covered_component_refs=(),
        unexamined_component_refs=(),
    )
    coverage_set = assemble_advancement_need_family_coverage_set(
        horizon, candidate_spaces=(space,), testimonies=(testimony,)
    )

    assert (
        _records(coverage_set)["clarification"].native_projection_id
        == "projection:clarification"
    )
    assert _records(coverage_set)["clarification"].coverage_standing == "partial"


def test_all_four_family_records_coexist_without_priority_sufficiency_or_mutation():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(selection, goal)
    coverage_set = assemble_advancement_need_family_coverage_set(
        horizon,
        candidate_spaces=tuple(_space(f, selection, goal, horizon) for f in FAMILIES),
        testimonies=tuple(_testimony(f, selection, goal, horizon) for f in FAMILIES),
    )
    payload = advancement_need_family_coverage_set_json(coverage_set)

    assert set(_records(coverage_set)) == set(FAMILIES)
    assert payload["judges_sufficiency"] is False
    assert payload["sufficient_for_now"] is None
    assert payload["prioritizes_families"] is False
    assert payload["selects_route"] is False
    assert payload["selects_next_action"] is False
    assert payload["opens_inquiry"] is False
    assert payload["requests_authority"] is False
    assert payload["selects_authority_source"] is False
    assert payload["selects_realization"] is False
    assert payload["authorizes_work"] is False
    assert payload["starts_execution"] is False
    assert payload["starts_recording"] is False
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False
    assert payload["read_only"] is True


def test_mismatched_stale_identity_is_conflicting_not_complete():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(selection, goal)
    mismatched = replace(
        _testimony(
            "clarification",
            selection,
            goal,
            horizon,
            covered_component_refs=("component:1", "component:2"),
            unexamined_component_refs=(),
        ),
        horizon_id="horizon:stale",
    )
    record = _records(
        assemble_advancement_need_family_coverage_set(
            horizon,
            candidate_spaces=(_space("clarification", selection, goal, horizon),),
            testimonies=(mismatched,),
        )
    )["clarification"]

    assert record.scope_disposition == "conflicting"
    assert record.coverage_standing == "conflicting"
    assert (
        record.identity_conflicts[0].conflict_kind
        == "testimony_horizon_identity_mismatch"
    )
