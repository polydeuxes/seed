"""Read-only inquiry-need projection from explicit repository/world uncertainty testimony."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Literal

from seed_runtime.bounded_advancement_horizon import BoundedAdvancementHorizon
from seed_runtime.bounded_operator_goal_establishment import BoundedOperatorGoalEstablishment

InquiryNeedStanding = Literal[
    "established", "unsupported", "unknown", "conflicting", "excluded_family"
]
EvidenceFreshness = Literal["current", "stale", "unknown"]
EvidenceAvailability = Literal["available", "unavailable", "unknown"]
UnclassifiedReason = Literal[
    "goal_identity_mismatch",
    "horizon_identity_mismatch",
    "evidence_identity_mismatch",
    "not_repository_world_uncertainty",
    "not_stage_owned",
    "not_component_bounded",
    "missing_repository_world_subject",
    "not_material_to_horizon",
    "mixed_or_non_inquiry_component",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "InquiryNeedProjection consumes only explicit component-bounded repository/world uncertainty testimony.",
    "Generic Unknowns, observations, unsupported facts, stale evidence, absent artifacts, and mixed unresolved material are not inquiry-need evidence.",
    "Inquiry standing is preserved separately from evidence freshness and evidence availability.",
    "Inquiry need established is not inquiry opened, question selected, observation authorized, action selected, sufficiency judged, execution, recording, event-ledger writing, or cluster mutation.",
)


@dataclass(frozen=True)
class RepositoryWorldUncertaintyTestimony:
    testimony_ref: str
    source_ref: str
    goal_establishment_id: str
    horizon_id: str
    evidence_ref: str
    bounded_uncertainty_component_ref: str
    repository_world_subject_ref: str
    owning_stage: str
    standing: InquiryNeedStanding
    uncertainty_family: str = "repository_world"
    stage_owns_repository_world_uncertainty: bool = True
    component_bounded: bool = True
    material_to_present_movement_boundary: bool = True
    mixed_or_non_inquiry_component: bool = False
    evidence_freshness: EvidenceFreshness = "current"
    evidence_availability: EvidenceAvailability = "available"
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class InquiryNeedProjectionItem:
    testimony_ref: str
    source_ref: str
    bounded_uncertainty_component_ref: str
    repository_world_subject_ref: str
    owning_stage: str
    standing: InquiryNeedStanding | None
    evidence_ref: str
    evidence_freshness: EvidenceFreshness
    evidence_availability: EvidenceAvailability
    unclassified_reason: UnclassifiedReason | None = None


@dataclass(frozen=True)
class InquiryNeedProjection:
    projection_id: str
    goal_establishment_id: str
    horizon_id: str
    evidence_refs: tuple[str, ...]
    established: tuple[InquiryNeedProjectionItem, ...]
    unsupported: tuple[InquiryNeedProjectionItem, ...]
    unknown: tuple[InquiryNeedProjectionItem, ...]
    conflicting: tuple[InquiryNeedProjectionItem, ...]
    excluded_family: tuple[InquiryNeedProjectionItem, ...]
    unclassified: tuple[InquiryNeedProjectionItem, ...]
    opens_inquiry: bool = False
    selects_question: bool = False
    authorizes_observation: bool = False
    selects_next_action: bool = False
    judges_sufficiency: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    read_only: bool = True
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + sha256(encoded).hexdigest()


def _horizon_evidence_refs(horizon: BoundedAdvancementHorizon) -> tuple[str, ...]:
    return tuple(item.evidence_ref for item in horizon.evidence_snapshot_refs)


def _excluded_inquiry_family(horizon: BoundedAdvancementHorizon) -> bool:
    return any(item.need_family in {"inquiry", "inquiry_need"} for item in horizon.explicitly_excluded_need_families)


def _unclassified_reason(
    testimony: RepositoryWorldUncertaintyTestimony,
    goal: BoundedOperatorGoalEstablishment,
    horizon: BoundedAdvancementHorizon,
    evidence_refs: tuple[str, ...],
) -> UnclassifiedReason | None:
    if testimony.goal_establishment_id != goal.goal_establishment_id:
        return "goal_identity_mismatch"
    if testimony.horizon_id != horizon.horizon_id:
        return "horizon_identity_mismatch"
    if testimony.evidence_ref not in evidence_refs:
        return "evidence_identity_mismatch"
    if testimony.uncertainty_family != "repository_world":
        return "not_repository_world_uncertainty"
    if not testimony.stage_owns_repository_world_uncertainty or not testimony.owning_stage:
        return "not_stage_owned"
    if not testimony.component_bounded or not testimony.bounded_uncertainty_component_ref:
        return "not_component_bounded"
    if not testimony.repository_world_subject_ref:
        return "missing_repository_world_subject"
    if not testimony.material_to_present_movement_boundary:
        return "not_material_to_horizon"
    if testimony.mixed_or_non_inquiry_component:
        return "mixed_or_non_inquiry_component"
    return None


def project_inquiry_need(
    goal: BoundedOperatorGoalEstablishment,
    horizon: BoundedAdvancementHorizon,
    testimony: Iterable[RepositoryWorldUncertaintyTestimony] = (),
) -> InquiryNeedProjection:
    """Project inquiry-need standings without opening inquiry or authorizing observation."""
    testimony_items = tuple(testimony)
    evidence_refs = _horizon_evidence_refs(horizon)
    buckets: dict[str, list[InquiryNeedProjectionItem]] = {
        "established": [],
        "unsupported": [],
        "unknown": [],
        "conflicting": [],
        "excluded_family": [],
        "unclassified": [],
    }
    excluded = _excluded_inquiry_family(horizon)
    for item in testimony_items:
        reason = _unclassified_reason(item, goal, horizon, evidence_refs)
        projection_item = InquiryNeedProjectionItem(
            testimony_ref=item.testimony_ref,
            source_ref=item.source_ref,
            bounded_uncertainty_component_ref=item.bounded_uncertainty_component_ref,
            repository_world_subject_ref=item.repository_world_subject_ref,
            owning_stage=item.owning_stage,
            standing=None if reason else ("excluded_family" if excluded else item.standing),
            evidence_ref=item.evidence_ref,
            evidence_freshness=item.evidence_freshness,
            evidence_availability=item.evidence_availability,
            unclassified_reason=reason,
        )
        if reason:
            buckets["unclassified"].append(projection_item)
        else:
            buckets[projection_item.standing or "unclassified"].append(projection_item)
    payload = {
        "goal": goal.goal_establishment_id,
        "horizon": horizon.horizon_id,
        "testimony": [item.testimony_ref for item in testimony_items],
    }
    return InquiryNeedProjection(
        _stable("inquiry-need-projection", payload),
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


def inquiry_need_projection_json(projection: InquiryNeedProjection) -> dict[str, object]:
    return projection.to_json_dict()
