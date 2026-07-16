"""Read-only operational-realization need projection from explicit family testimony."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Literal

from seed_runtime.bounded_advancement_horizon import BoundedAdvancementHorizon
from seed_runtime.bounded_operator_goal_establishment import BoundedOperatorGoalEstablishment
from seed_runtime.goal_inquiry_consideration_selection import GoalInquiryConsiderationSelection

RequirementStanding = Literal["required", "not_required", "unknown", "conflicting"]
AvailabilityStanding = Literal["available", "unavailable", "unknown", "conflicting"]
CoverageStanding = Literal["complete_for_horizon", "partial", "unknown", "conflicting"]
BlockerFamilyOwnership = Literal["operational_realization", "authority", "clarification", "inquiry", "generic", "unknown", "conflicting"]
ScopeApplicability = Literal["applicable", "outside_current_scope", "unknown", "conflicting"]
HorizonMateriality = Literal["material", "not_material", "unknown", "conflicting"]
NeedStanding = Literal["established", "unsupported", "unknown", "conflicting", "unclassified_here"]
UnclassifiedReason = Literal[
    "selection_identity_mismatch",
    "goal_identity_mismatch",
    "horizon_identity_mismatch",
    "evidence_identity_mismatch",
    "not_requirement_component",
    "not_standing_component",
    "not_component_bounded",
    "missing_transformation",
    "missing_applicable_scope",
    "scope_not_applicable",
    "not_material_to_horizon",
    "ownership_mismatch",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "OperationalRealizationNeedProjection consumes only explicit operational-realization requirement and standing testimony.",
    "Requirement standing, realization-family availability standing, realization-family coverage standing, blocker-family ownership, scope applicability, and horizon materiality remain separate dimensions.",
    "Unavailability establishes need only when coverage is complete for the bounded horizon and the deficiency is owned by the operational-realization family.",
    "No selected realization, no supporting candidate observed, one candidate blocked, reachability blocked, missing selection, failed implementation, authority failure, and downstream silence do not by themselves establish realization-family unavailability or need.",
    "Operational realization need established is not realization selection, warrant, representation translation, invocation preparation, authority request, authorization, execution, recording, event-ledger writing, or cluster mutation.",
)


@dataclass(frozen=True)
class OperationalRealizationRequirementTestimony:
    testimony_ref: str
    source_ref: str
    selection_id: str
    goal_establishment_id: str
    horizon_id: str
    evidence_ref: str
    bounded_realization_component_ref: str
    required_transformation_ref: str
    applicable_scope_ref: str
    owning_stage: str
    requirement_standing: RequirementStanding
    component_family: str = "operational_realization_requirement"
    component_bounded: bool = True
    scope_applicability: ScopeApplicability = "applicable"
    horizon_materiality: HorizonMateriality = "material"
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class OperationalRealizationStandingTestimony:
    testimony_ref: str
    source_ref: str
    selection_id: str
    goal_establishment_id: str
    horizon_id: str
    evidence_ref: str
    bounded_realization_component_ref: str
    required_transformation_ref: str
    applicable_scope_ref: str
    owning_stage: str
    availability_standing: AvailabilityStanding
    coverage_standing: CoverageStanding
    blocker_family_ownership: BlockerFamilyOwnership
    component_family: str = "operational_realization_standing"
    component_bounded: bool = True
    scope_applicability: ScopeApplicability = "applicable"
    horizon_materiality: HorizonMateriality = "material"
    candidate_existence_ref: str = ""
    reachability_ref: str = ""
    selection_ref: str = ""
    warrant_ref: str = ""
    representation_applicability_ref: str = ""
    dependency_ref: str = ""
    behavior_support_ref: str = ""
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class OperationalRealizationNeedProjectionItem:
    requirement_testimony_ref: str
    standing_testimony_ref: str
    bounded_realization_component_ref: str
    required_transformation_ref: str
    applicable_scope_ref: str
    owning_stage: str
    requirement_standing: RequirementStanding | None
    availability_standing: AvailabilityStanding | None
    coverage_standing: CoverageStanding | None
    blocker_family_ownership: BlockerFamilyOwnership | None
    scope_applicability: ScopeApplicability | None
    horizon_materiality: HorizonMateriality | None
    need_standing: NeedStanding | None
    evidence_refs: tuple[str, ...]
    unclassified_reason: UnclassifiedReason | None = None


@dataclass(frozen=True)
class OperationalRealizationNeedProjection:
    projection_id: str
    selection_id: str
    goal_establishment_id: str
    horizon_id: str
    evidence_refs: tuple[str, ...]
    established: tuple[OperationalRealizationNeedProjectionItem, ...]
    unsupported: tuple[OperationalRealizationNeedProjectionItem, ...]
    unknown: tuple[OperationalRealizationNeedProjectionItem, ...]
    conflicting: tuple[OperationalRealizationNeedProjectionItem, ...]
    unclassified_here: tuple[OperationalRealizationNeedProjectionItem, ...]
    unclassified: tuple[OperationalRealizationNeedProjectionItem, ...]
    selects_realization: bool = False
    warrants_realization: bool = False
    translates_representation: bool = False
    prepares_invocation: bool = False
    requests_authority: bool = False
    authorizes_movement: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    read_only: bool = True
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def _stable(prefix: str, payload: object) -> str:
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + sha256(blob).hexdigest()


def _horizon_evidence_refs(horizon: BoundedAdvancementHorizon) -> tuple[str, ...]:
    return tuple(item.evidence_ref for item in horizon.evidence_snapshot_refs)


def _base_reason(t, selection, goal, horizon, evidence_refs, expected_family: str) -> UnclassifiedReason | None:
    if t.selection_id != selection.selection_id:
        return "selection_identity_mismatch"
    if t.goal_establishment_id != goal.goal_establishment_id:
        return "goal_identity_mismatch"
    if t.horizon_id != horizon.horizon_id:
        return "horizon_identity_mismatch"
    if t.evidence_ref not in evidence_refs:
        return "evidence_identity_mismatch"
    if t.component_family != expected_family:
        return "not_requirement_component" if expected_family.endswith("requirement") else "not_standing_component"
    if not t.component_bounded or not t.bounded_realization_component_ref:
        return "not_component_bounded"
    if not t.required_transformation_ref:
        return "missing_transformation"
    if not t.applicable_scope_ref:
        return "missing_applicable_scope"
    if not t.owning_stage:
        return "ownership_mismatch"
    if t.scope_applicability != "applicable":
        return "scope_not_applicable"
    if t.horizon_materiality != "material":
        return "not_material_to_horizon"
    return None


def _join_reason(req: OperationalRealizationRequirementTestimony, standing: OperationalRealizationStandingTestimony) -> UnclassifiedReason | None:
    if req.bounded_realization_component_ref != standing.bounded_realization_component_ref:
        return "not_component_bounded"
    if req.required_transformation_ref != standing.required_transformation_ref:
        return "missing_transformation"
    if req.applicable_scope_ref != standing.applicable_scope_ref:
        return "missing_applicable_scope"
    if req.owning_stage != standing.owning_stage:
        return "ownership_mismatch"
    return None


def _conclude(req: RequirementStanding, avail: AvailabilityStanding, coverage: CoverageStanding, owner: BlockerFamilyOwnership) -> NeedStanding:
    if req == "not_required":
        return "unsupported"
    if req == "unknown":
        return "unknown"
    if req == "conflicting":
        return "conflicting"
    if avail == "available":
        return "unsupported"
    if avail == "unknown":
        return "unknown"
    if avail == "conflicting":
        return "conflicting"
    if avail == "unavailable":
        if owner == "authority":
            return "unclassified_here"
        if owner in ("clarification", "inquiry", "generic"):
            return "unclassified_here"
        if owner == "conflicting":
            return "conflicting"
        if owner == "unknown":
            return "unknown"
        if coverage == "complete_for_horizon" and owner == "operational_realization":
            return "established"
        if coverage == "conflicting":
            return "conflicting"
        return "unknown"
    return "unknown"


def project_operational_realization_need(
    selection: GoalInquiryConsiderationSelection,
    goal: BoundedOperatorGoalEstablishment,
    horizon: BoundedAdvancementHorizon,
    requirements: Iterable[OperationalRealizationRequirementTestimony] = (),
    standings: Iterable[OperationalRealizationStandingTestimony] = (),
) -> OperationalRealizationNeedProjection:
    reqs = tuple(requirements)
    standing_items = tuple(standings)
    evidence_refs = _horizon_evidence_refs(horizon)
    buckets: dict[str, list[OperationalRealizationNeedProjectionItem]] = {k: [] for k in ("established", "unsupported", "unknown", "conflicting", "unclassified_here", "unclassified")}
    used: set[str] = set()
    for req in reqs:
        reason = _base_reason(req, selection, goal, horizon, evidence_refs, "operational_realization_requirement")
        matches = [s for s in standing_items if s.bounded_realization_component_ref == req.bounded_realization_component_ref and s.required_transformation_ref == req.required_transformation_ref and s.applicable_scope_ref == req.applicable_scope_ref]
        standing = matches[0] if matches else None
        if standing is not None:
            used.add(standing.testimony_ref)
            reason = reason or _base_reason(standing, selection, goal, horizon, evidence_refs, "operational_realization_standing") or _join_reason(req, standing)
        else:
            reason = reason or "not_standing_component"
        need = None if reason else _conclude(req.requirement_standing, standing.availability_standing, standing.coverage_standing, standing.blocker_family_ownership)  # type: ignore[union-attr]
        item = OperationalRealizationNeedProjectionItem(
            req.testimony_ref,
            standing.testimony_ref if standing else "",
            req.bounded_realization_component_ref,
            req.required_transformation_ref,
            req.applicable_scope_ref,
            req.owning_stage,
            None if reason else req.requirement_standing,
            None if reason or standing is None else standing.availability_standing,
            None if reason or standing is None else standing.coverage_standing,
            None if reason or standing is None else standing.blocker_family_ownership,
            None if reason else req.scope_applicability,
            None if reason else req.horizon_materiality,
            need,
            (req.evidence_ref,) + ((standing.evidence_ref,) if standing else ()),
            reason,
        )
        buckets[need or "unclassified"].append(item)
    for standing in standing_items:
        if standing.testimony_ref in used:
            continue
        reason = _base_reason(standing, selection, goal, horizon, evidence_refs, "operational_realization_standing") or "not_requirement_component"
        buckets["unclassified"].append(OperationalRealizationNeedProjectionItem("", standing.testimony_ref, standing.bounded_realization_component_ref, standing.required_transformation_ref, standing.applicable_scope_ref, standing.owning_stage, None, None, None, None, None, None, None, (standing.evidence_ref,), reason))
    payload = {"selection": selection.selection_id, "goal": goal.goal_establishment_id, "horizon": horizon.horizon_id, "requirements": [r.testimony_ref for r in reqs], "standings": [s.testimony_ref for s in standing_items]}
    return OperationalRealizationNeedProjection(_stable("operational-realization-need-projection", payload), selection.selection_id, goal.goal_establishment_id, horizon.horizon_id, evidence_refs, *(tuple(buckets[k]) for k in ("established", "unsupported", "unknown", "conflicting", "unclassified_here", "unclassified")))


def operational_realization_need_projection_json(projection: OperationalRealizationNeedProjection) -> dict[str, object]:
    return projection.to_json_dict()
