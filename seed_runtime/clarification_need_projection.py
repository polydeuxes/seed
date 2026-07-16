"""Read-only clarification-need projection from explicit operator-meaning testimony."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Literal

from seed_runtime.bounded_advancement_horizon import BoundedAdvancementHorizon
from seed_runtime.bounded_operator_goal_establishment import (
    BoundedOperatorGoalEstablishment,
)
from seed_runtime.goal_inquiry_consideration_selection import (
    GoalInquiryConsiderationSelection,
)

ClarificationNeedStanding = Literal[
    "established", "unsupported", "unknown", "conflicting", "excluded_family"
]
UnclassifiedReason = Literal[
    "selection_identity_mismatch",
    "goal_identity_mismatch",
    "horizon_identity_mismatch",
    "evidence_identity_mismatch",
    "not_operator_meaning_uncertainty",
    "not_stage_owned",
    "not_component_bounded",
    "not_material_to_horizon",
    "mixed_or_non_clarification_component",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "ClarificationNeedProjection consumes only explicit component-bounded operator-meaning uncertainty testimony.",
    "Generic unresolved material, family hints, mixed prose, and unresolved goal fields are not clarification evidence.",
    "Clarification need established is not clarification requested, question wording selected, inquiry opened, action selected, authorization, execution, recording, or mutation.",
    "The projection does not inspect wording to discover operator meaning or reinterpret the goal.",
)


@dataclass(frozen=True)
class OperatorMeaningUncertaintyTestimony:
    testimony_ref: str
    source_ref: str
    selection_id: str
    goal_establishment_id: str
    horizon_id: str
    evidence_ref: str
    bounded_uncertainty_component_ref: str
    owning_stage: str
    standing: ClarificationNeedStanding
    uncertainty_family: str = "operator_meaning"
    stage_owns_operator_meaning: bool = True
    component_bounded: bool = True
    material_to_present_movement_boundary: bool = True
    mixed_or_non_clarification_component: bool = False
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class ClarificationNeedProjectionItem:
    testimony_ref: str
    source_ref: str
    bounded_uncertainty_component_ref: str
    owning_stage: str
    standing: ClarificationNeedStanding | None
    unclassified_reason: UnclassifiedReason | None = None
    evidence_ref: str = ""


@dataclass(frozen=True)
class ClarificationNeedProjection:
    projection_id: str
    selection_id: str
    goal_establishment_id: str
    horizon_id: str
    evidence_refs: tuple[str, ...]
    established: tuple[ClarificationNeedProjectionItem, ...]
    unsupported: tuple[ClarificationNeedProjectionItem, ...]
    unknown: tuple[ClarificationNeedProjectionItem, ...]
    conflicting: tuple[ClarificationNeedProjectionItem, ...]
    excluded_family: tuple[ClarificationNeedProjectionItem, ...]
    unclassified: tuple[ClarificationNeedProjectionItem, ...]
    requests_clarification: bool = False
    selects_question_wording: bool = False
    opens_inquiry: bool = False
    selects_next_action: bool = False
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


def _horizon_evidence_refs(horizon: BoundedAdvancementHorizon) -> tuple[str, ...]:
    return tuple(item.evidence_ref for item in horizon.evidence_snapshot_refs)


def _excluded_clarification_family(horizon: BoundedAdvancementHorizon) -> bool:
    return any(
        item.need_family in {"clarification", "clarification_need"}
        for item in horizon.explicitly_excluded_need_families
    )


def _unclassified_reason(
    testimony: OperatorMeaningUncertaintyTestimony,
    selection: GoalInquiryConsiderationSelection,
    goal: BoundedOperatorGoalEstablishment,
    horizon: BoundedAdvancementHorizon,
    evidence_refs: tuple[str, ...],
) -> UnclassifiedReason | None:
    if testimony.selection_id != selection.selection_id:
        return "selection_identity_mismatch"
    if testimony.goal_establishment_id != goal.goal_establishment_id:
        return "goal_identity_mismatch"
    if testimony.horizon_id != horizon.horizon_id:
        return "horizon_identity_mismatch"
    if testimony.evidence_ref not in evidence_refs:
        return "evidence_identity_mismatch"
    if testimony.uncertainty_family != "operator_meaning":
        return "not_operator_meaning_uncertainty"
    if not testimony.stage_owns_operator_meaning or not testimony.owning_stage:
        return "not_stage_owned"
    if (
        not testimony.component_bounded
        or not testimony.bounded_uncertainty_component_ref
    ):
        return "not_component_bounded"
    if not testimony.material_to_present_movement_boundary:
        return "not_material_to_horizon"
    if testimony.mixed_or_non_clarification_component:
        return "mixed_or_non_clarification_component"
    return None


def project_clarification_need(
    selection: GoalInquiryConsiderationSelection,
    goal: BoundedOperatorGoalEstablishment,
    horizon: BoundedAdvancementHorizon,
    testimony: Iterable[OperatorMeaningUncertaintyTestimony] = (),
) -> ClarificationNeedProjection:
    """Project clarification need standings without requesting clarification."""
    testimony_items = tuple(testimony)
    evidence_refs = _horizon_evidence_refs(horizon)
    buckets: dict[str, list[ClarificationNeedProjectionItem]] = {
        "established": [],
        "unsupported": [],
        "unknown": [],
        "conflicting": [],
        "excluded_family": [],
        "unclassified": [],
    }
    excluded = _excluded_clarification_family(horizon)
    for item in testimony_items:
        reason = _unclassified_reason(item, selection, goal, horizon, evidence_refs)
        projection_item = ClarificationNeedProjectionItem(
            testimony_ref=item.testimony_ref,
            source_ref=item.source_ref,
            bounded_uncertainty_component_ref=item.bounded_uncertainty_component_ref,
            owning_stage=item.owning_stage,
            standing=(
                None if reason else ("excluded_family" if excluded else item.standing)
            ),
            unclassified_reason=reason,
            evidence_ref=item.evidence_ref,
        )
        if reason:
            buckets["unclassified"].append(projection_item)
        else:
            buckets[projection_item.standing or "unclassified"].append(projection_item)
    payload = {
        "selection": selection.selection_id,
        "goal": goal.goal_establishment_id,
        "horizon": horizon.horizon_id,
        "testimony": [item.testimony_ref for item in testimony_items],
    }
    return ClarificationNeedProjection(
        _stable("clarification-need-projection", payload),
        selection.selection_id,
        goal.goal_establishment_id,
        horizon.horizon_id,
        evidence_refs,
        tuple(buckets["established"]),
        tuple(buckets["unsupported"]),
        tuple(buckets["unknown"]),
        tuple(buckets["conflicting"]),
        tuple(buckets["excluded_family"]),
        tuple(buckets["unclassified"]),
    )


def clarification_need_projection_json(
    projection: ClarificationNeedProjection,
) -> dict[str, object]:
    return projection.to_json_dict()
