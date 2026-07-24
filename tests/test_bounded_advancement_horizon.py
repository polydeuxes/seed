from dataclasses import replace

from seed_runtime.bounded_advancement_horizon import (
    EvidenceSnapshotReference,
    NeedFamilyExclusion,
    bounded_advancement_horizon_json,
    establish_bounded_advancement_horizon,
)
from seed_runtime.bounded_operator_goal_establishment import (
    establish_bounded_operator_goal_from_closed_choice,
)
from tests.test_bounded_operator_goal_establishment import _choice_binding


def _goal(**overrides):
    token = overrides.pop("token", "2" if overrides else "1")
    goal = establish_bounded_operator_goal_from_closed_choice(
        _choice_binding(token),
        stop_conditions=("stop before need classification",),
    )
    return replace(goal, **overrides) if overrides else goal


def test_horizon_binds_exact_bounded_goal_identity_and_ingress_lineage():
    goal = _goal()
    horizon = establish_bounded_advancement_horizon(
        goal,
        present_movement_boundary="consider only the current advancement boundary",
    )
    assert horizon.artifact_type == "BoundedAdvancementHorizon"
    assert horizon.horizon_state == "bounded"
    assert horizon.goal_establishment_id == goal.goal_establishment_id
    assert horizon.goal_ingress_artifact_ref == goal.ingress_artifact_ref
    assert horizon.goal_ingress_lineage == goal.ingress_lineage


def test_horizon_preserves_supplied_boundary_scope_and_current_bounds():
    goal = _goal()
    horizon = establish_bounded_advancement_horizon(
        goal,
        present_movement_boundary="read-only boundary before need testimony",
        included_scope=("goal lineage", "present boundary", "evidence snapshots"),
        excluded_scope=("need classification", "execution planning"),
        time_bounds=("current session only",),
        current_state_bounds=("repository snapshot at horizon construction",),
    )
    assert horizon.present_movement_boundary == "read-only boundary before need testimony"
    assert horizon.included_scope == ("goal lineage", "present boundary", "evidence snapshots")
    assert horizon.excluded_scope == ("need classification", "execution planning")
    assert horizon.time_bounds == ("current session only",)
    assert horizon.current_state_bounds == ("repository snapshot at horizon construction",)


def test_horizon_preserves_possible_and_excluded_need_families_without_classification():
    goal = _goal()
    horizon = establish_bounded_advancement_horizon(
        goal,
        present_movement_boundary="preserve possible need families only",
        potentially_relevant_need_families=("clarification", "inquiry", "authority", "operational-realization"),
        explicitly_excluded_need_families=(
            NeedFamilyExclusion("scheduling", "outside this supplied movement boundary"),
            NeedFamilyExclusion("execution", "would mutate the advancement stage"),
        ),
    )
    assert horizon.potentially_relevant_need_families == ("clarification", "inquiry", "authority", "operational-realization")
    assert horizon.classified_need_families == ()
    assert horizon.sufficient_for_now is None


def test_horizon_preserves_goal_unknowns_conflicts_and_supplied_evidence_quality():
    goal = _goal(unknowns=("goal source omits current-state bound",), conflicts=("two source spans disagree on scope",))
    horizon = establish_bounded_advancement_horizon(
        goal,
        present_movement_boundary="preserve evidence quality only",
        evidence_snapshot_refs=(
            EvidenceSnapshotReference("ev:current", "snapshot:current", "current"),
            EvidenceSnapshotReference("ev:stale", "snapshot:stale", "stale"),
            EvidenceSnapshotReference("ev:missing", "snapshot:missing", "unavailable"),
        ),
        unknowns=("movement boundary producer is Unknown",),
        conflicts=("snapshot order conflicts with presentation order",),
        stale_evidence_refs=("ev:stale",),
        unavailable_evidence_refs=("ev:missing",),
    )
    assert horizon.stale_evidence_refs == ("ev:stale",)
    assert horizon.unavailable_evidence_refs == ("ev:missing",)
    assert "goal source omits current-state bound" in horizon.unknowns
    assert "movement boundary producer is Unknown" in horizon.unknowns
    assert "two source spans disagree on scope" in horizon.conflicts


def test_refused_bounded_goal_and_missing_boundary_cannot_establish_horizon():
    refused_goal = _goal(establishment_state="refused")
    missing = establish_bounded_advancement_horizon(_goal(), present_movement_boundary="")
    refused = establish_bounded_advancement_horizon(refused_goal, present_movement_boundary="boundary")
    assert missing.horizon_state == "refused"
    assert missing.refusal_reason == "missing_present_movement_boundary"
    assert refused.horizon_state == "refused"
    assert refused.refusal_reason == "goal_artifact_not_established"


def test_horizon_does_not_select_goal_or_establish_focus_and_remains_read_only():
    horizon = establish_bounded_advancement_horizon(_goal(), present_movement_boundary="read-only boundary only")
    data = bounded_advancement_horizon_json(horizon)
    assert data["selects_goal"] is False
    assert data["establishes_focus"] is False
    assert data["classified_need_families"] == ()
    assert data["judges_sufficiency"] is False
    assert data["opens_inquiry"] is False
    assert data["writes_event_ledger"] is False
    assert data["mutates_cluster"] is False
    assert data["read_only"] is True
