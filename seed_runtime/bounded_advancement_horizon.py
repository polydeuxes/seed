"""Read-only bounded advancement horizon construction.

A horizon preserves the present movement boundary for one already-selected
bounded goal.  It does not classify needs, judge sufficiency, choose a next
step, authorize work, execute, record, or mutate state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Literal

from seed_runtime.bounded_operator_goal_establishment import (
    BoundedOperatorGoalEstablishment,
)
from seed_runtime.goal_inquiry_consideration_selection import (
    GoalInquiryConsiderationSelection,
)

HorizonState = Literal["bounded", "refused"]
RefusalReason = Literal[
    "selection_not_resolved",
    "goal_artifact_identity_mismatch",
    "goal_artifact_not_established",
    "missing_present_movement_boundary",
    "excluded_need_family_missing_reason",
]

NEED_CLASSIFICATION_FIELDS: tuple[str, ...] = (
    "clarification_need",
    "inquiry_need",
    "authority_need",
    "operational_realization_need",
    "sufficient_for_now",
    "selected_next_action",
)

BOUNDARY_NOTES: tuple[str, ...] = (
    "BoundedAdvancementHorizon is not the goal itself.",
    "BoundedAdvancementHorizon is not need classification or sufficiency judgment.",
    "Included need family means potentially relevant to preserve, not that a need exists.",
    "Excluded need families must carry explicit reasons.",
    "The horizon is read-only and does not open inquiry, authorize, execute, record, or mutate state.",
)


@dataclass(frozen=True)
class NeedFamilyExclusion:
    need_family: str
    reason: str


@dataclass(frozen=True)
class EvidenceSnapshotReference:
    evidence_ref: str
    snapshot_ref: str
    evidence_state: str = "current"
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class BoundedAdvancementHorizon:
    artifact_type: str
    horizon_id: str
    horizon_state: HorizonState
    refusal_reason: RefusalReason | None
    selection_id: str
    selected_goal_establishment_id: str | None
    selected_goal_source_ref: str | None
    goal_establishment_id: str
    goal_artifact_type: str
    goal_ingress_artifact_ref: str
    goal_ingress_lineage: tuple[str, ...]
    present_movement_boundary: str
    included_scope: tuple[str, ...]
    excluded_scope: tuple[str, ...]
    evidence_snapshot_refs: tuple[EvidenceSnapshotReference, ...]
    time_bounds: tuple[str, ...]
    current_state_bounds: tuple[str, ...]
    potentially_relevant_need_families: tuple[str, ...]
    explicitly_excluded_need_families: tuple[NeedFamilyExclusion, ...]
    unknowns: tuple[str, ...]
    conflicts: tuple[str, ...]
    stale_evidence_refs: tuple[str, ...]
    unavailable_evidence_refs: tuple[str, ...]
    classified_need_families: tuple[str, ...] = ()
    judges_sufficiency: bool = False
    sufficient_for_now: None = None
    selects_next_action: bool = False
    selected_next_action: None = None
    opens_inquiry: bool = False
    requests_authority: bool = False
    selects_realization: bool = False
    schedules: bool = False
    authorizes_work: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    read_only: bool = True
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return prefix + ":" + sha256(encoded).hexdigest()


def _dedupe(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value)))


def _refuse(
    reason: RefusalReason,
    selection: GoalInquiryConsiderationSelection,
    goal: BoundedOperatorGoalEstablishment,
    *,
    present_movement_boundary: str = "",
    unknowns: Iterable[str] = (),
    conflicts: Iterable[str] = (),
) -> BoundedAdvancementHorizon:
    payload = {
        "state": "refused",
        "reason": reason,
        "selection": selection.selection_id,
        "goal": goal.goal_establishment_id,
        "boundary": present_movement_boundary,
    }
    return BoundedAdvancementHorizon(
        "BoundedAdvancementHorizon",
        _stable("bounded-advancement-horizon", payload),
        "refused",
        reason,
        selection.selection_id,
        selection.selected_goal_establishment_id,
        selection.selected_goal_source_ref,
        goal.goal_establishment_id,
        goal.artifact_type,
        goal.ingress_artifact_ref,
        goal.ingress_lineage,
        present_movement_boundary,
        (),
        (),
        (),
        (),
        (),
        (),
        (),
        _dedupe((*selection.unknowns, *goal.unknowns, *unknowns)),
        _dedupe((*selection.conflicts, *goal.conflicts, *conflicts)),
        (),
        (),
    )


def establish_bounded_advancement_horizon(
    selection: GoalInquiryConsiderationSelection,
    goal: BoundedOperatorGoalEstablishment,
    *,
    present_movement_boundary: str,
    included_scope: Iterable[str] = (),
    excluded_scope: Iterable[str] = (),
    evidence_snapshot_refs: Iterable[EvidenceSnapshotReference] = (),
    time_bounds: Iterable[str] = (),
    current_state_bounds: Iterable[str] = (),
    potentially_relevant_need_families: Iterable[str] = (),
    explicitly_excluded_need_families: Iterable[NeedFamilyExclusion] = (),
    unknowns: Iterable[str] = (),
    conflicts: Iterable[str] = (),
    stale_evidence_refs: Iterable[str] = (),
    unavailable_evidence_refs: Iterable[str] = (),
) -> BoundedAdvancementHorizon:
    """Preserve the current advancement boundary for one exact selected goal."""
    if (
        selection.selection_state != "selected"
        or not selection.selected_goal_establishment_id
    ):
        return _refuse(
            "selection_not_resolved",
            selection,
            goal,
            present_movement_boundary=present_movement_boundary,
        )
    if selection.selected_goal_establishment_id != goal.goal_establishment_id:
        return _refuse(
            "goal_artifact_identity_mismatch",
            selection,
            goal,
            present_movement_boundary=present_movement_boundary,
        )
    if (
        goal.artifact_type != "BoundedOperatorGoalEstablishment"
        or goal.establishment_state == "refused"
    ):
        return _refuse(
            "goal_artifact_not_established",
            selection,
            goal,
            present_movement_boundary=present_movement_boundary,
        )
    if not present_movement_boundary:
        return _refuse("missing_present_movement_boundary", selection, goal)

    excluded = tuple(explicitly_excluded_need_families)
    missing_reasons = tuple(item.need_family for item in excluded if not item.reason)
    if missing_reasons:
        return _refuse(
            "excluded_need_family_missing_reason",
            selection,
            goal,
            present_movement_boundary=present_movement_boundary,
            conflicts=(
                f"excluded need family lacks reason: {family}"
                for family in missing_reasons
            ),
        )

    snapshots = tuple(evidence_snapshot_refs)
    payload = {
        "selection": selection.selection_id,
        "goal": goal.goal_establishment_id,
        "source": selection.selected_goal_source_ref,
        "boundary": present_movement_boundary,
        "included_scope": list(_dedupe(included_scope)),
        "excluded_scope": list(_dedupe(excluded_scope)),
        "snapshots": [asdict(item) for item in snapshots],
        "time_bounds": list(_dedupe(time_bounds)),
        "current_state_bounds": list(_dedupe(current_state_bounds)),
        "need_families": list(_dedupe(potentially_relevant_need_families)),
        "excluded_need_families": [asdict(item) for item in excluded],
    }
    return BoundedAdvancementHorizon(
        "BoundedAdvancementHorizon",
        _stable("bounded-advancement-horizon", payload),
        "bounded",
        None,
        selection.selection_id,
        selection.selected_goal_establishment_id,
        selection.selected_goal_source_ref,
        goal.goal_establishment_id,
        goal.artifact_type,
        goal.ingress_artifact_ref,
        goal.ingress_lineage,
        present_movement_boundary,
        _dedupe(included_scope),
        _dedupe(excluded_scope),
        snapshots,
        _dedupe(time_bounds),
        _dedupe(current_state_bounds),
        _dedupe(potentially_relevant_need_families),
        excluded,
        _dedupe((*selection.unknowns, *goal.unknowns, *unknowns)),
        _dedupe((*selection.conflicts, *goal.conflicts, *conflicts)),
        _dedupe(stale_evidence_refs),
        _dedupe(unavailable_evidence_refs),
    )


def bounded_advancement_horizon_json(
    horizon: BoundedAdvancementHorizon,
) -> dict[str, object]:
    return horizon.to_json_dict()
