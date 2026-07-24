"""Read-only authority-need projection from explicit component-bounded authority testimony."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Literal

from seed_runtime.bounded_advancement_horizon import BoundedAdvancementHorizon
from seed_runtime.bounded_operator_goal_establishment import BoundedOperatorGoalEstablishment

RequirementStanding = Literal["required", "not_required", "unknown", "conflicting"]
AuthorityStanding = Literal["available", "unavailable", "unknown", "conflicting", "outside_current_scope"]
AuthorityNeedStanding = Literal["established", "unsupported", "unknown", "conflicting", "outside_current_scope"]
ScopeApplicability = Literal["applicable", "outside_current_scope", "unknown", "conflicting"]
HorizonMateriality = Literal["material", "not_material", "unknown", "conflicting"]
UnclassifiedReason = Literal[
    "goal_identity_mismatch",
    "horizon_identity_mismatch",
    "evidence_identity_mismatch",
    "not_authority_requirement_component",
    "not_authority_standing_component",
    "not_component_bounded",
    "missing_authority_class",
    "missing_applicable_scope",
    "scope_not_applicable",
    "not_material_to_horizon",
    "ownership_mismatch",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "AuthorityNeedProjection consumes only explicit component-bounded authority requirement and authority standing testimony.",
    "Requirement standing, authority standing, scope applicability, and horizon materiality remain separate dimensions.",
    "Authority need established is not authority requested, source selected, permission granted, scope expanded, authorization, execution, recording, event-ledger writing, or cluster mutation.",
    "Generic blockers, denied execution, absent observations, candidate-local authority blockers, and downstream silence are not authority-need evidence.",
)

@dataclass(frozen=True)
class AuthorityRequirementTestimony:
    testimony_ref: str
    source_ref: str
    goal_establishment_id: str
    horizon_id: str
    evidence_ref: str
    bounded_authority_component_ref: str
    required_authority_class_ref: str
    applicable_scope_ref: str
    owning_stage: str
    requirement_standing: RequirementStanding
    component_family: str = "authority_requirement"
    component_bounded: bool = True
    scope_applicability: ScopeApplicability = "applicable"
    horizon_materiality: HorizonMateriality = "material"
    notes: tuple[str, ...] = ()

@dataclass(frozen=True)
class AuthorityStandingTestimony:
    testimony_ref: str
    source_ref: str
    goal_establishment_id: str
    horizon_id: str
    evidence_ref: str
    bounded_authority_component_ref: str
    required_authority_class_ref: str
    applicable_scope_ref: str
    owning_stage: str
    authority_standing: AuthorityStanding
    component_family: str = "authority_standing"
    component_bounded: bool = True
    scope_applicability: ScopeApplicability = "applicable"
    horizon_materiality: HorizonMateriality = "material"
    selected_authority_source_ref: str = ""
    notes: tuple[str, ...] = ()

@dataclass(frozen=True)
class AuthorityNeedProjectionItem:
    requirement_testimony_ref: str
    authority_testimony_ref: str
    bounded_authority_component_ref: str
    required_authority_class_ref: str
    applicable_scope_ref: str
    owning_stage: str
    requirement_standing: RequirementStanding | None
    authority_standing: AuthorityStanding | None
    scope_applicability: ScopeApplicability | None
    horizon_materiality: HorizonMateriality | None
    need_standing: AuthorityNeedStanding | None
    evidence_refs: tuple[str, ...]
    unclassified_reason: UnclassifiedReason | None = None

@dataclass(frozen=True)
class AuthorityNeedProjection:
    projection_id: str
    goal_establishment_id: str
    horizon_id: str
    evidence_refs: tuple[str, ...]
    established: tuple[AuthorityNeedProjectionItem, ...]
    unsupported: tuple[AuthorityNeedProjectionItem, ...]
    unknown: tuple[AuthorityNeedProjectionItem, ...]
    conflicting: tuple[AuthorityNeedProjectionItem, ...]
    outside_current_scope: tuple[AuthorityNeedProjectionItem, ...]
    unclassified: tuple[AuthorityNeedProjectionItem, ...]
    requests_authority: bool = False
    selects_authority_source: bool = False
    grants_authority: bool = False
    expands_scope: bool = False
    authorizes_movement: bool = False
    selects_realization: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    read_only: bool = True
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES
    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)

def _stable(prefix: str, payload: object) -> str:
    return prefix + ":" + sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _horizon_evidence_refs(horizon: BoundedAdvancementHorizon) -> tuple[str, ...]:
    return tuple(item.evidence_ref for item in horizon.evidence_snapshot_refs)

def _base_reason(t, goal, horizon, evidence_refs, expected_family: str) -> UnclassifiedReason | None:
    if t.goal_establishment_id != goal.goal_establishment_id: return "goal_identity_mismatch"
    if t.horizon_id != horizon.horizon_id: return "horizon_identity_mismatch"
    if t.evidence_ref not in evidence_refs: return "evidence_identity_mismatch"
    if t.component_family != expected_family:
        return "not_authority_requirement_component" if expected_family == "authority_requirement" else "not_authority_standing_component"
    if not t.component_bounded or not t.bounded_authority_component_ref: return "not_component_bounded"
    if not t.required_authority_class_ref: return "missing_authority_class"
    if not t.applicable_scope_ref: return "missing_applicable_scope"
    if not t.owning_stage: return "ownership_mismatch"
    if t.scope_applicability != "applicable": return "scope_not_applicable"
    if t.horizon_materiality != "material": return "not_material_to_horizon"
    return None

def _join_reason(req: AuthorityRequirementTestimony, auth: AuthorityStandingTestimony) -> UnclassifiedReason | None:
    if req.bounded_authority_component_ref != auth.bounded_authority_component_ref: return "not_component_bounded"
    if req.required_authority_class_ref != auth.required_authority_class_ref: return "missing_authority_class"
    if req.applicable_scope_ref != auth.applicable_scope_ref: return "missing_applicable_scope"
    if req.owning_stage != auth.owning_stage: return "ownership_mismatch"
    return None

def _conclude(requirement: RequirementStanding, authority: AuthorityStanding) -> AuthorityNeedStanding:
    if requirement == "not_required": return "unsupported"
    if requirement == "unknown": return "unknown"
    if requirement == "conflicting": return "conflicting"
    if authority == "unavailable": return "established"
    if authority == "available": return "unsupported"
    if authority == "unknown": return "unknown"
    if authority == "conflicting": return "conflicting"
    return "outside_current_scope"

def project_authority_need(goal: BoundedOperatorGoalEstablishment, horizon: BoundedAdvancementHorizon, requirements: Iterable[AuthorityRequirementTestimony] = (), standings: Iterable[AuthorityStandingTestimony] = ()) -> AuthorityNeedProjection:
    reqs = tuple(requirements); auths = tuple(standings); evidence_refs = _horizon_evidence_refs(horizon)
    buckets: dict[str, list[AuthorityNeedProjectionItem]] = {k: [] for k in ("established","unsupported","unknown","conflicting","outside_current_scope","unclassified")}
    used_auth: set[str] = set()
    for req in reqs:
        reason = _base_reason(req, goal, horizon, evidence_refs, "authority_requirement")
        matches = [a for a in auths if a.bounded_authority_component_ref == req.bounded_authority_component_ref and a.required_authority_class_ref == req.required_authority_class_ref and a.applicable_scope_ref == req.applicable_scope_ref]
        auth = matches[0] if matches else None
        if auth is not None:
            used_auth.add(auth.testimony_ref)
            reason = reason or _base_reason(auth, goal, horizon, evidence_refs, "authority_standing") or _join_reason(req, auth)
        else:
            reason = reason or "not_authority_standing_component"
        need = None if reason else _conclude(req.requirement_standing, auth.authority_standing)  # type: ignore[union-attr]
        item = AuthorityNeedProjectionItem(req.testimony_ref, auth.testimony_ref if auth else "", req.bounded_authority_component_ref, req.required_authority_class_ref, req.applicable_scope_ref, req.owning_stage, None if reason else req.requirement_standing, None if reason or auth is None else auth.authority_standing, None if reason else req.scope_applicability, None if reason else req.horizon_materiality, need, (req.evidence_ref,) + ((auth.evidence_ref,) if auth else ()), reason)
        buckets[need or "unclassified"].append(item)
    for auth in auths:
        if auth.testimony_ref in used_auth: continue
        reason = _base_reason(auth, goal, horizon, evidence_refs, "authority_standing") or "not_authority_requirement_component"
        buckets["unclassified"].append(AuthorityNeedProjectionItem("", auth.testimony_ref, auth.bounded_authority_component_ref, auth.required_authority_class_ref, auth.applicable_scope_ref, auth.owning_stage, None, None, None, None, None, (auth.evidence_ref,), reason))
    payload = {"goal": goal.goal_establishment_id, "horizon": horizon.horizon_id, "requirements": [r.testimony_ref for r in reqs], "standings": [a.testimony_ref for a in auths]}
    return AuthorityNeedProjection(_stable("authority-need-projection", payload), goal.goal_establishment_id, horizon.horizon_id, evidence_refs, *(tuple(buckets[k]) for k in ("established","unsupported","unknown","conflicting","outside_current_scope","unclassified")))

def authority_need_projection_json(projection: AuthorityNeedProjection) -> dict[str, object]:
    return projection.to_json_dict()
