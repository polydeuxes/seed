"""Read-only sufficiency projection for one goal advancement horizon."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Literal

from seed_runtime.advancement_need_family_coverage_set import (
    AdvancementNeedFamilyCoverageRecord,
    AdvancementNeedFamilyCoverageSet,
)
from seed_runtime.goal_advancement_need_set import (
    FAMILIES,
    GoalAdvancementNeedSet,
    NeedFamily,
    NeedFamilyAssemblyRecord,
)

SufficiencyConclusion = Literal[
    "sufficient_for_now",
    "insufficient_for_now",
    "unknown",
    "conflicting",
]
ReasonKind = Literal[
    "material_conflict",
    "established_unresolved_native_need",
    "unknown",
    "sufficient_family",
    "lawful_exclusion",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "GoalAdvancementSufficiencyProjection consumes already-owned need and coverage standings without reinterpretation.",
    "Family reasons are preserved as an unordered set, not priority, route, next action, or authorization.",
    "Coverage gaps may prevent sufficiency but are not promoted into native advancement needs.",
    "Sufficient for now is bounded to the present horizon and is not permanent goal satisfaction or movement authorization.",
    "Insufficient for now is not global blockage, priority, selected resolution, routing, execution, recording, event-ledger writing, or cluster mutation.",
)


@dataclass(frozen=True)
class GoalAdvancementSufficiencyReason:
    family: NeedFamily | str
    reason_kind: ReasonKind
    reason: str
    native_projection_id: str = ""
    coverage_set_id: str = ""
    need_set_id: str = ""


@dataclass(frozen=True)
class GoalAdvancementSufficiencyProjection:
    projection_id: str
    artifact_type: str
    need_set_id: str
    coverage_set_id: str
    goal_establishment_id: str
    horizon_id: str
    conclusion: SufficiencyConclusion
    family_reasons: frozenset[GoalAdvancementSufficiencyReason]
    preserves_unordered_reasons: bool = True
    promotes_coverage_gap_to_native_need: bool = False
    ranks_needs: bool = False
    prioritizes_needs: bool = False
    selects_route: bool = False
    selects_next_action: bool = False
    opens_inquiry: bool = False
    requests_authority: bool = False
    selects_authority_source: bool = False
    selects_realization: bool = False
    authorizes_work: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    read_only: bool = True
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["family_reasons"] = tuple(
            asdict(reason)
            for reason in sorted(
                self.family_reasons,
                key=lambda r: (r.family, r.reason_kind, r.reason, r.native_projection_id),
            )
        )
        return data


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + sha256(encoded).hexdigest()


def _need_records(need_set: GoalAdvancementNeedSet) -> dict[NeedFamily, NeedFamilyAssemblyRecord]:
    return {record.family: record for record in need_set.family_records}


def _coverage_records(coverage_set: AdvancementNeedFamilyCoverageSet) -> dict[NeedFamily, AdvancementNeedFamilyCoverageRecord]:
    return {record.family: record for record in coverage_set.family_records}


def _item_ref(item: object) -> str:
    for name in ("testimony_ref", "requirement_testimony_ref", "standing_testimony_ref", "bounded_uncertainty_component_ref", "bounded_authority_component_ref", "bounded_realization_component_ref"):
        value = getattr(item, name, "")
        if value:
            return str(value)
    return repr(item)


def project_goal_advancement_sufficiency(
    need_set: GoalAdvancementNeedSet,
    coverage_set: AdvancementNeedFamilyCoverageSet,
) -> GoalAdvancementSufficiencyProjection:
    """Project bounded sufficiency without ranking, selecting, recording, or mutating."""
    reasons: set[GoalAdvancementSufficiencyReason] = set()

    if (need_set.goal_establishment_id, need_set.horizon_id) != (
        coverage_set.goal_establishment_id,
        coverage_set.horizon_id,
    ):
        reasons.add(GoalAdvancementSufficiencyReason("set", "material_conflict", "need_set_and_coverage_set_identity_mismatch", coverage_set_id=coverage_set.coverage_set_id, need_set_id=need_set.need_set_id))

    for conflict in need_set.horizon_conflicts:
        reasons.add(GoalAdvancementSufficiencyReason("horizon", "material_conflict", conflict, need_set_id=need_set.need_set_id))

    needs = _need_records(need_set)
    coverages = _coverage_records(coverage_set)
    for family in FAMILIES:
        need = needs[family]
        coverage = coverages[family]
        projection = need.projection
        projection_id = getattr(projection, "projection_id", "")
        if need.identity_conflicts:
            for conflict in need.identity_conflicts:
                reasons.add(GoalAdvancementSufficiencyReason(family, "material_conflict", conflict.conflict_kind, projection_id, need_set_id=need_set.need_set_id))
        if coverage.identity_conflicts or coverage.conflicts or coverage.coverage_standing == "conflicting" or coverage.scope_disposition == "conflicting":
            for conflict in coverage.identity_conflicts:
                reasons.add(GoalAdvancementSufficiencyReason(family, "material_conflict", conflict.conflict_kind, coverage.native_projection_id, coverage_set.coverage_set_id))
            for conflict in coverage.conflicts or ("coverage_conflicting",):
                reasons.add(GoalAdvancementSufficiencyReason(family, "material_conflict", conflict, coverage.native_projection_id, coverage_set.coverage_set_id))
        if need.disposition == "supplied" and projection_id and coverage.scope_disposition == "included" and coverage.native_projection_id != projection_id:
            reasons.add(GoalAdvancementSufficiencyReason(family, "material_conflict", "native_projection_identity_mismatch_between_need_and_coverage_sets", projection_id, coverage_set.coverage_set_id, need_set.need_set_id))
        if projection is not None:
            for item in getattr(projection, "conflicting", ()): 
                reasons.add(GoalAdvancementSufficiencyReason(family, "material_conflict", f"native_need_conflicting:{_item_ref(item)}", projection_id, need_set_id=need_set.need_set_id))
            for item in getattr(projection, "established", ()): 
                reasons.add(GoalAdvancementSufficiencyReason(family, "established_unresolved_native_need", _item_ref(item), projection_id, need_set_id=need_set.need_set_id))
            for item in getattr(projection, "unknown", ()): 
                reasons.add(GoalAdvancementSufficiencyReason(family, "unknown", f"unknown_native_standing:{_item_ref(item)}", projection_id, need_set_id=need_set.need_set_id))
        if need.disposition == "absent":
            reasons.add(GoalAdvancementSufficiencyReason(family, "unknown", "absent_native_projection", need_set_id=need_set.need_set_id))
        if need.disposition == "excluded":
            if need.exclusion_reason:
                reasons.add(GoalAdvancementSufficiencyReason(family, "lawful_exclusion", need.exclusion_reason, need_set_id=need_set.need_set_id))
            else:
                reasons.add(GoalAdvancementSufficiencyReason(family, "unknown", "excluded_family_without_explicit_reason", need_set_id=need_set.need_set_id))
        if coverage.scope_disposition == "excluded":
            if coverage.horizon_exclusion_reason:
                reasons.add(GoalAdvancementSufficiencyReason(family, "lawful_exclusion", coverage.horizon_exclusion_reason, coverage_set_id=coverage_set.coverage_set_id))
            else:
                reasons.add(GoalAdvancementSufficiencyReason(family, "unknown", "coverage_exclusion_without_explicit_reason", coverage_set_id=coverage_set.coverage_set_id))
        elif coverage.coverage_standing == "complete_for_horizon":
            reasons.add(GoalAdvancementSufficiencyReason(family, "sufficient_family", "complete_for_horizon_with_no_unresolved_native_need", projection_id, coverage_set.coverage_set_id, need_set.need_set_id))
        elif coverage.coverage_standing in {"partial", "unknown", "not_evaluated"}:
            reasons.add(GoalAdvancementSufficiencyReason(family, "unknown", f"coverage_{coverage.coverage_standing}", coverage.native_projection_id, coverage_set.coverage_set_id))

    if any(r.reason_kind == "material_conflict" for r in reasons):
        conclusion: SufficiencyConclusion = "conflicting"
    elif any(r.reason_kind == "established_unresolved_native_need" for r in reasons):
        conclusion = "insufficient_for_now"
    elif any(r.reason_kind == "unknown" for r in reasons):
        conclusion = "unknown"
    else:
        conclusion = "sufficient_for_now"

    payload = {
        "need_set": need_set.need_set_id,
        "coverage_set": coverage_set.coverage_set_id,
        "conclusion": conclusion,
        "reasons": sorted((r.family, r.reason_kind, r.reason, r.native_projection_id) for r in reasons),
    }
    return GoalAdvancementSufficiencyProjection(
        _stable("goal-advancement-sufficiency-projection", payload),
        "GoalAdvancementSufficiencyProjection",
        need_set.need_set_id,
        coverage_set.coverage_set_id,
        need_set.goal_establishment_id,
        need_set.horizon_id,
        conclusion,
        frozenset(reasons),
    )


def goal_advancement_sufficiency_projection_json(
    projection: GoalAdvancementSufficiencyProjection,
) -> dict[str, object]:
    return projection.to_json_dict()
