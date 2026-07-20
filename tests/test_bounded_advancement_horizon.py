from seed_runtime.bounded_advancement_horizon import (
    EvidenceSnapshotReference,
    NeedFamilyExclusion,
    bounded_advancement_horizon_json,
    establish_bounded_advancement_horizon,
)
from seed_runtime.bounded_operator_goal_establishment import (
    establish_bounded_operator_goal_from_interpretation,
)
from seed_runtime.goal_consideration_candidate_resolution import (
    GoalConsiderationCandidateTestimony,
    resolve_goal_consideration_candidate,
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


def _candidate_resolution(goal, *, testimony=None):
    inventory = build_goal_orientation_inventory(
        [
            association_from_bounded_goal(
                goal,
                dimension_refs=("knowledge_quality",),
                source_ref="goal-artifact:fixture",
            )
        ]
    )
    return resolve_goal_consideration_candidate(
        inventory,
        testimony
        or [
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:exact",
                "operator:testimony",
                goal.goal_establishment_id,
            )
        ],
    )


def test_horizon_requires_resolved_candidate_identity_and_matching_goal_artifact():
    goal = _goal()
    resolution = _candidate_resolution(goal)

    horizon = establish_bounded_advancement_horizon(
        resolution,
        goal,
        present_movement_boundary="consider only the current advancement boundary",
    )

    assert horizon.artifact_type == "BoundedAdvancementHorizon"
    assert horizon.horizon_state == "bounded"
    assert horizon.candidate_resolution_id == resolution.resolution_id
    assert horizon.resolved_goal_establishment_id == goal.goal_establishment_id
    assert horizon.resolved_goal_source_ref == "goal-artifact:fixture"
    assert horizon.goal_establishment_id == goal.goal_establishment_id
    assert horizon.goal_ingress_artifact_ref == goal.ingress_artifact_ref
    assert horizon.goal_ingress_lineage == goal.ingress_lineage


def test_horizon_preserves_supplied_boundary_scope_and_current_bounds():
    goal = _goal()
    horizon = establish_bounded_advancement_horizon(
        _candidate_resolution(goal),
        goal,
        present_movement_boundary="read-only boundary before need testimony",
        included_scope=("goal lineage", "present boundary", "evidence snapshots"),
        excluded_scope=("need classification", "execution planning"),
        time_bounds=("current session only",),
        current_state_bounds=("repository snapshot at horizon construction",),
    )

    assert horizon.present_movement_boundary == "read-only boundary before need testimony"
    assert horizon.included_scope == (
        "goal lineage",
        "present boundary",
        "evidence snapshots",
    )
    assert horizon.excluded_scope == ("need classification", "execution planning")
    assert horizon.time_bounds == ("current session only",)
    assert horizon.current_state_bounds == (
        "repository snapshot at horizon construction",
    )


def test_horizon_preserves_possible_and_excluded_need_families_without_classification():
    goal = _goal()
    horizon = establish_bounded_advancement_horizon(
        _candidate_resolution(goal),
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
                "scheduling", "outside this supplied movement boundary"
            ),
            NeedFamilyExclusion("execution", "would mutate the advancement stage"),
        ),
    )

    assert horizon.potentially_relevant_need_families == (
        "clarification",
        "inquiry",
        "authority",
        "operational-realization",
    )
    assert horizon.classified_need_families == ()
    assert horizon.sufficient_for_now is None


def test_horizon_preserves_evidence_quality_from_candidate_testimony_and_goal():
    goal = _goal(
        unknowns=("goal source omits current-state bound",),
        conflicts=("two source spans disagree on scope",),
    )
    resolution = _candidate_resolution(
        goal,
        testimony=[
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:exact",
                "operator:testimony",
                goal.goal_establishment_id,
                unknowns=("candidate testimony timestamp is Unknown",),
                conflicts=("candidate testimony conflicts with prior testimony",),
            )
        ],
    )

    horizon = establish_bounded_advancement_horizon(
        resolution,
        goal,
        present_movement_boundary="preserve evidence quality only",
        evidence_snapshot_refs=(
            EvidenceSnapshotReference("ev:current", "snapshot:current", "current"),
            EvidenceSnapshotReference("ev:stale", "snapshot:stale", "stale"),
            EvidenceSnapshotReference(
                "ev:missing", "snapshot:missing", "unavailable"
            ),
        ),
        unknowns=("movement boundary producer is Unknown",),
        conflicts=("snapshot order conflicts with presentation order",),
        stale_evidence_refs=("ev:stale",),
        unavailable_evidence_refs=("ev:missing",),
    )

    assert horizon.stale_evidence_refs == ("ev:stale",)
    assert horizon.unavailable_evidence_refs == ("ev:missing",)
    assert "candidate testimony timestamp is Unknown" in horizon.unknowns
    assert "candidate testimony conflicts with prior testimony" in horizon.conflicts


def test_horizon_refuses_mismatched_or_unresolved_candidate_identity():
    goal = _goal()
    other_goal = _goal(
        interpretation_projection_id="interpretation:other",
        relation_or_focus_expressions=("other bounded goal",),
    )
    inventory = build_goal_orientation_inventory(
        [association_from_bounded_goal(goal, dimension_refs=("knowledge_quality",))]
    )
    unresolved = resolve_goal_consideration_candidate(inventory)
    resolved = _candidate_resolution(goal)

    mismatch = establish_bounded_advancement_horizon(
        resolved,
        other_goal,
        present_movement_boundary="boundary cannot cross goal identity mismatch",
    )
    unresolved_horizon = establish_bounded_advancement_horizon(
        unresolved,
        goal,
        present_movement_boundary="boundary requires resolved candidate identity",
    )

    assert mismatch.horizon_state == "refused"
    assert mismatch.refusal_reason == "goal_artifact_identity_mismatch"
    assert unresolved_horizon.horizon_state == "refused"
    assert unresolved_horizon.refusal_reason == "candidate_not_resolved"


def test_horizon_does_not_promote_candidate_resolution_to_selection_or_focus():
    goal = _goal()
    horizon = establish_bounded_advancement_horizon(
        _candidate_resolution(goal),
        goal,
        present_movement_boundary="read-only boundary only",
    )
    data = bounded_advancement_horizon_json(horizon)

    assert data["candidate_identity_only"] is True
    assert data["selects_goal"] is False
    assert data["establishes_focus"] is False
    assert data["classified_need_families"] == ()
    assert data["judges_sufficiency"] is False
    assert data["selects_next_action"] is False
    assert data["opens_inquiry"] is False
    assert data["authorizes_work"] is False
    assert data["starts_execution"] is False
    assert data["writes_event_ledger"] is False
    assert data["mutates_cluster"] is False
