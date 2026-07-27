"""Read-only bounded advancement horizon construction.

A horizon preserves a caller-supplied present movement boundary for one bounded
goal identity. It
does not select the goal, choose a next step,
authorize work, execute, record, or mutate state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Literal

from seed_runtime.bounded_operator_goal_establishment import (
    BoundedOperatorGoalEstablishment,
)
HorizonState = Literal["bounded", "refused"]
RefusalReason = Literal[
    "goal_artifact_not_established",
    "missing_present_movement_boundary",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "BoundedAdvancementHorizon is not the goal itself.",
    "Bounded goal identity is not Seed-owned goal selection, constitutional focus, priority, or advancement.",
    "BoundedAdvancementHorizon preserves a supplied movement boundary; it does not produce that boundary's constitutional standing.",
    "The horizon is read-only and does not open inquiry, authorize, execute, record, or mutate state.",
)


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
    unknowns: tuple[str, ...]
    conflicts: tuple[str, ...]
    stale_evidence_refs: tuple[str, ...]
    unavailable_evidence_refs: tuple[str, ...]
    selects_goal: bool = False
    establishes_focus: bool = False
    selects_next_action: bool = False
    selected_next_action: None = None
    opens_inquiry: bool = False
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
    goal: BoundedOperatorGoalEstablishment,
    *,
    present_movement_boundary: str = "",
    unknowns: Iterable[str] = (),
    conflicts: Iterable[str] = (),
) -> BoundedAdvancementHorizon:
    payload = {
        "state": "refused",
        "reason": reason,
        "goal": goal.goal_establishment_id,
        "boundary": present_movement_boundary,
    }
    return BoundedAdvancementHorizon(
        artifact_type="BoundedAdvancementHorizon",
        horizon_id=_stable("bounded-advancement-horizon", payload),
        horizon_state="refused",
        refusal_reason=reason,
        goal_establishment_id=goal.goal_establishment_id,
        goal_artifact_type=goal.artifact_type,
        goal_ingress_artifact_ref=goal.ingress_artifact_ref,
        goal_ingress_lineage=goal.ingress_lineage,
        present_movement_boundary=present_movement_boundary,
        included_scope=(),
        excluded_scope=(),
        evidence_snapshot_refs=(),
        time_bounds=(),
        current_state_bounds=(),
        unknowns=_dedupe((*goal.unknowns, *unknowns)),
        conflicts=_dedupe((*goal.conflicts, *conflicts)),
        stale_evidence_refs=(),
        unavailable_evidence_refs=(),
    )

def establish_bounded_advancement_horizon(
    goal: BoundedOperatorGoalEstablishment,
    *,
    present_movement_boundary: str,
    included_scope: Iterable[str] = (),
    excluded_scope: Iterable[str] = (),
    evidence_snapshot_refs: Iterable[EvidenceSnapshotReference] = (),
    time_bounds: Iterable[str] = (),
    current_state_bounds: Iterable[str] = (),
    unknowns: Iterable[str] = (),
    conflicts: Iterable[str] = (),
    stale_evidence_refs: Iterable[str] = (),
    unavailable_evidence_refs: Iterable[str] = (),
) -> BoundedAdvancementHorizon:
    """Preserve a supplied advancement boundary for one exact bounded goal identity."""
    if (
        goal.artifact_type != "BoundedOperatorGoalEstablishment"
        or goal.establishment_state == "refused"
    ):
        return _refuse(
            "goal_artifact_not_established",
            goal,
            present_movement_boundary=present_movement_boundary,
        )
    if not present_movement_boundary:
        return _refuse("missing_present_movement_boundary", goal)

    snapshots = tuple(evidence_snapshot_refs)
    payload = {
        "goal": goal.goal_establishment_id,
        "source": goal.ingress_artifact_ref,
        "boundary": present_movement_boundary,
        "included_scope": list(_dedupe(included_scope)),
        "excluded_scope": list(_dedupe(excluded_scope)),
        "snapshots": [asdict(item) for item in snapshots],
        "time_bounds": list(_dedupe(time_bounds)),
        "current_state_bounds": list(_dedupe(current_state_bounds)),
    }
    return BoundedAdvancementHorizon(
        artifact_type="BoundedAdvancementHorizon",
        horizon_id=_stable("bounded-advancement-horizon", payload),
        horizon_state="bounded",
        refusal_reason=None,
        goal_establishment_id=goal.goal_establishment_id,
        goal_artifact_type=goal.artifact_type,
        goal_ingress_artifact_ref=goal.ingress_artifact_ref,
        goal_ingress_lineage=goal.ingress_lineage,
        present_movement_boundary=present_movement_boundary,
        included_scope=_dedupe(included_scope),
        excluded_scope=_dedupe(excluded_scope),
        evidence_snapshot_refs=snapshots,
        time_bounds=_dedupe(time_bounds),
        current_state_bounds=_dedupe(current_state_bounds),
        unknowns=_dedupe((*goal.unknowns, *unknowns)),
        conflicts=_dedupe((*goal.conflicts, *conflicts)),
        stale_evidence_refs=_dedupe(stale_evidence_refs),
        unavailable_evidence_refs=_dedupe(unavailable_evidence_refs),
    )


def bounded_advancement_horizon_json(
    horizon: BoundedAdvancementHorizon,
) -> dict[str, object]:
    return horizon.to_json_dict()
