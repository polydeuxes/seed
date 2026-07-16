from seed_runtime.bounded_advancement_horizon import (
    EvidenceSnapshotReference,
    NeedFamilyExclusion,
    bounded_advancement_horizon_json,
    establish_bounded_advancement_horizon,
)
from seed_runtime.bounded_operator_goal_establishment import (
    establish_bounded_operator_goal_from_interpretation,
)
from seed_runtime.goal_inquiry_consideration_selection import (
    GoalFocusEvidence,
    select_goal_for_inquiry_consideration,
)
from seed_runtime.goal_orientation_inventory import (
    association_from_bounded_goal,
    build_goal_orientation_inventory,
)
from tests.test_bounded_operator_goal_establishment import _interpretation


def _goal(**overrides):
    return establish_bounded_operator_goal_from_interpretation(
        _interpretation(**overrides),
        stop_conditions=("stop before need classification",),
    )


def _selection(goal, *, evidence=None):
    inventory = build_goal_orientation_inventory(
        [
            association_from_bounded_goal(
                goal,
                dimension_refs=("knowledge_quality",),
                source_ref="goal-artifact:fixture",
            )
        ]
    )
    return select_goal_for_inquiry_consideration(
        inventory,
        evidence
        or [
            GoalFocusEvidence(
                "focus:exact", "operator-focus:fixture", goal.goal_establishment_id
            )
        ],
    )


def test_horizon_requires_exact_selected_goal_and_goal_artifact_identity_match():
    goal = _goal()
    selection = _selection(goal)

    horizon = establish_bounded_advancement_horizon(
        selection,
        goal,
        present_movement_boundary="consider only whether inquiry-facing stages have an explicit boundary",
    )

    assert horizon.artifact_type == "BoundedAdvancementHorizon"
    assert horizon.horizon_state == "bounded"
    assert horizon.selection_id == selection.selection_id
    assert horizon.selected_goal_establishment_id == goal.goal_establishment_id
    assert horizon.selected_goal_source_ref == "goal-artifact:fixture"
    assert horizon.goal_establishment_id == goal.goal_establishment_id
    assert horizon.goal_artifact_type == "BoundedOperatorGoalEstablishment"
    assert horizon.goal_ingress_artifact_ref == goal.ingress_artifact_ref
    assert horizon.goal_ingress_lineage == goal.ingress_lineage


def test_horizon_preserves_present_movement_boundary_scope_and_current_bounds():
    goal = _goal()
    horizon = establish_bounded_advancement_horizon(
        _selection(goal),
        goal,
        present_movement_boundary="read-only boundary before clarification, inquiry, authority, or realization testimony",
        included_scope=(
            "selected goal lineage",
            "present boundary",
            "evidence snapshots",
        ),
        excluded_scope=("need classification", "execution planning"),
        time_bounds=("current session only",),
        current_state_bounds=("repository working tree at horizon construction",),
    )

    assert (
        horizon.present_movement_boundary
        == "read-only boundary before clarification, inquiry, authority, or realization testimony"
    )
    assert horizon.included_scope == (
        "selected goal lineage",
        "present boundary",
        "evidence snapshots",
    )
    assert horizon.excluded_scope == ("need classification", "execution planning")
    assert horizon.time_bounds == ("current session only",)
    assert horizon.current_state_bounds == (
        "repository working tree at horizon construction",
    )


def test_horizon_preserves_included_and_excluded_need_family_coverage_without_classification():
    goal = _goal()
    horizon = establish_bounded_advancement_horizon(
        _selection(goal),
        goal,
        present_movement_boundary="preserve possible need families only",
        potentially_relevant_need_families=(
            "clarification",
            "inquiry",
            "authority",
            "operational-realization",
        ),
        explicitly_excluded_need_families=(
            NeedFamilyExclusion(
                "scheduling", "scheduling is outside this present movement boundary"
            ),
            NeedFamilyExclusion(
                "execution", "execution would mutate the advancement stage"
            ),
        ),
    )

    assert horizon.potentially_relevant_need_families == (
        "clarification",
        "inquiry",
        "authority",
        "operational-realization",
    )
    assert horizon.explicitly_excluded_need_families == (
        NeedFamilyExclusion(
            "scheduling", "scheduling is outside this present movement boundary"
        ),
        NeedFamilyExclusion(
            "execution", "execution would mutate the advancement stage"
        ),
    )
    assert horizon.classified_need_families == ()
    assert horizon.sufficient_for_now is None


def test_horizon_preserves_stale_unavailable_unknown_and_conflicting_evidence():
    goal = _goal(
        unknowns=("goal source omits current-state bound",),
        conflicts=("two source spans disagree on scope",),
    )
    selection = _selection(
        goal,
        evidence=[
            GoalFocusEvidence(
                "focus:exact",
                "operator-focus:fixture",
                goal.goal_establishment_id,
                unknowns=("focus timestamp is Unknown",),
                conflicts=("focus conflicts with prior topic label",),
            )
        ],
    )

    horizon = establish_bounded_advancement_horizon(
        selection,
        goal,
        present_movement_boundary="preserve evidence quality only",
        evidence_snapshot_refs=(
            EvidenceSnapshotReference("ev:current", "snapshot:current", "current"),
            EvidenceSnapshotReference(
                "ev:stale",
                "snapshot:stale",
                "stale",
                ("superseded by operator correction",),
            ),
            EvidenceSnapshotReference("ev:missing", "snapshot:missing", "unavailable"),
        ),
        unknowns=("movement boundary has an Unknown downstream consumer",),
        conflicts=("snapshot order conflicts with presentation order",),
        stale_evidence_refs=("ev:stale",),
        unavailable_evidence_refs=("ev:missing",),
    )

    assert (
        EvidenceSnapshotReference(
            "ev:stale",
            "snapshot:stale",
            "stale",
            ("superseded by operator correction",),
        )
        in horizon.evidence_snapshot_refs
    )
    assert horizon.stale_evidence_refs == ("ev:stale",)
    assert horizon.unavailable_evidence_refs == ("ev:missing",)
    assert "goal source omits current-state bound" in horizon.unknowns
    assert "focus timestamp is Unknown" in horizon.unknowns
    assert "movement boundary has an Unknown downstream consumer" in horizon.unknowns
    assert "two source spans disagree on scope" in horizon.conflicts
    assert "focus conflicts with prior topic label" in horizon.conflicts
    assert "snapshot order conflicts with presentation order" in horizon.conflicts


def test_horizon_refuses_mismatched_or_unresolved_goal_selection():
    goal = _goal()
    other_goal = _goal(
        interpretation_projection_id="interpretation:other",
        relation_or_focus_expressions=("other bounded goal",),
    )
    unresolved = select_goal_for_inquiry_consideration(
        build_goal_orientation_inventory(
            [association_from_bounded_goal(goal, dimension_refs=("knowledge_quality",))]
        )
    )
    selected = _selection(goal)

    mismatch = establish_bounded_advancement_horizon(
        selected,
        other_goal,
        present_movement_boundary="boundary cannot cross goal identity mismatch",
    )
    unresolved_horizon = establish_bounded_advancement_horizon(
        unresolved,
        goal,
        present_movement_boundary="boundary requires resolved selection",
    )

    assert mismatch.horizon_state == "refused"
    assert mismatch.refusal_reason == "goal_artifact_identity_mismatch"
    assert unresolved_horizon.horizon_state == "refused"
    assert unresolved_horizon.refusal_reason == "selection_not_resolved"


def test_horizon_has_no_need_classification_sufficiency_action_authorization_execution_recording_or_mutation():
    goal = _goal()
    horizon = establish_bounded_advancement_horizon(
        _selection(goal),
        goal,
        present_movement_boundary="read-only boundary only",
        potentially_relevant_need_families=("clarification", "authority"),
    )
    data = bounded_advancement_horizon_json(horizon)

    assert data["classified_need_families"] == ()
    assert data["judges_sufficiency"] is False
    assert data["sufficient_for_now"] is None
    assert data["selects_next_action"] is False
    assert data["selected_next_action"] is None
    assert data["opens_inquiry"] is False
    assert data["requests_authority"] is False
    assert data["selects_realization"] is False
    assert data["schedules"] is False
    assert data["authorizes_work"] is False
    assert data["starts_execution"] is False
    assert data["starts_recording"] is False
    assert data["writes_event_ledger"] is False
    assert data["mutates_cluster"] is False
    assert data["read_only"] is True
