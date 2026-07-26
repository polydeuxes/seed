"""Read-only assembly of stage-owned demand projections for one advancement horizon."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Literal

from seed_runtime.authority_demand_projection import AuthorityDemandProjection
from seed_runtime.bounded_advancement_horizon import BoundedAdvancementHorizon
from seed_runtime.clarification_demand_projection import ClarificationDemandProjection
from seed_runtime.inquiry_demand_projection import InquiryDemandProjection
from seed_runtime.operational_realization_demand_projection import (
    OperationalRealizationDemandProjection,
)

GoalAdvancementDemandFamily = Literal[
    "clarification",
    "inquiry",
    "authority",
    "operational_realization",
]
GoalAdvancementDemandFamilyDisposition = Literal["supplied", "absent", "excluded"]
IdentityConflictKind = Literal[
    "goal_identity_mismatch",
    "horizon_identity_mismatch",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "GoalAdvancementDemandSet preserves supplied stage-owned demand projections without reinterpretation.",
    "Coexisting demands are an unordered set, not a priority order, overall blocker, route, or next action.",
    "Supplied, absent, and explicitly excluded demand families remain distinct.",
    "The demand set is not a sufficiency judgment and does not open inquiry, request authority, select realization, authorize, execute, record, write the event ledger, or mutate cluster state.",
)

FAMILIES: tuple[GoalAdvancementDemandFamily, ...] = (
    "clarification",
    "inquiry",
    "authority",
    "operational_realization",
)


@dataclass(frozen=True)
class GoalAdvancementDemandFamilyIdentityConflict:
    family: GoalAdvancementDemandFamily
    conflict_kind: IdentityConflictKind
    expected: str
    actual: str
    projection_id: str


@dataclass(frozen=True)
class GoalAdvancementDemandFamilyAssemblyRecord:
    family: GoalAdvancementDemandFamily
    disposition: GoalAdvancementDemandFamilyDisposition
    projection: (
        ClarificationDemandProjection
        | InquiryDemandProjection
        | AuthorityDemandProjection
        | OperationalRealizationDemandProjection
        | None
    ) = None
    exclusion_reason: str = ""
    identity_conflicts: tuple[GoalAdvancementDemandFamilyIdentityConflict, ...] = ()


@dataclass(frozen=True)
class GoalAdvancementDemandSet:
    goal_advancement_demand_set_id: str
    artifact_type: str
    goal_establishment_id: str
    horizon_id: str
    family_records: frozenset[GoalAdvancementDemandFamilyAssemblyRecord]
    horizon_unknowns: tuple[str, ...]
    horizon_conflicts: tuple[str, ...]
    horizon_exclusions: tuple[str, ...]
    refuses_mismatched_projection: bool
    classifies_demand: bool = False
    orders_demands: bool = False
    prioritizes_demands: bool = False
    declares_overall_blocker: bool = False
    selects_route: bool = False
    selects_next_action: bool = False
    judges_sufficiency: bool = False
    sufficient_for_now: None = None
    opens_inquiry: bool = False
    requests_authority: bool = False
    selects_realization: bool = False
    authorizes_work: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    read_only: bool = True
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        records = sorted(self.family_records, key=lambda record: record.family)
        return {
            "goal_advancement_demand_set_id": self.goal_advancement_demand_set_id,
            "artifact_type": self.artifact_type,
            "goal_establishment_id": self.goal_establishment_id,
            "horizon_id": self.horizon_id,
            "family_records": tuple(asdict(record) for record in records),
            "horizon_unknowns": self.horizon_unknowns,
            "horizon_conflicts": self.horizon_conflicts,
            "horizon_exclusions": self.horizon_exclusions,
            "refuses_mismatched_projection": self.refuses_mismatched_projection,
            "classifies_demand": self.classifies_demand,
            "orders_demands": self.orders_demands,
            "prioritizes_demands": self.prioritizes_demands,
            "declares_overall_blocker": self.declares_overall_blocker,
            "selects_route": self.selects_route,
            "selects_next_action": self.selects_next_action,
            "judges_sufficiency": self.judges_sufficiency,
            "sufficient_for_now": self.sufficient_for_now,
            "opens_inquiry": self.opens_inquiry,
            "requests_authority": self.requests_authority,
            "selects_realization": self.selects_realization,
            "authorizes_work": self.authorizes_work,
            "starts_execution": self.starts_execution,
            "starts_recording": self.starts_recording,
            "writes_event_ledger": self.writes_event_ledger,
            "mutates_cluster": self.mutates_cluster,
            "read_only": self.read_only,
            "boundary_notes": self.boundary_notes,
        }


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return prefix + ":" + sha256(encoded).hexdigest()


def _excluded_family_reason(horizon: BoundedAdvancementHorizon, family: GoalAdvancementDemandFamily) -> str:
    aliases = {family, f"{family}_demand"}
    for exclusion in horizon.explicitly_excluded_goal_advancement_demand_families:
        if exclusion.goal_advancement_demand_family in aliases:
            return exclusion.reason
    return ""


def _identity_conflicts(
    family: GoalAdvancementDemandFamily,
    projection: (
        ClarificationDemandProjection
        | InquiryDemandProjection
        | AuthorityDemandProjection
        | OperationalRealizationDemandProjection
    ),
    horizon: BoundedAdvancementHorizon,
) -> tuple[GoalAdvancementDemandFamilyIdentityConflict, ...]:
    conflicts: list[GoalAdvancementDemandFamilyIdentityConflict] = []
    expected = (
        (
            "goal_identity_mismatch",
            horizon.goal_establishment_id,
            projection.goal_establishment_id,
        ),
        ("horizon_identity_mismatch", horizon.horizon_id, projection.horizon_id),
    )
    for kind, wanted, actual in expected:
        if wanted != actual:
            conflicts.append(
                GoalAdvancementDemandFamilyIdentityConflict(
                    family,
                    kind,  # type: ignore[arg-type]
                    wanted,
                    actual,
                    projection.projection_id,
                )
            )
    return tuple(conflicts)


def assemble_goal_advancement_demand_set(
    horizon: BoundedAdvancementHorizon,
    *,
    clarification: ClarificationDemandProjection | None = None,
    inquiry: InquiryDemandProjection | None = None,
    authority: AuthorityDemandProjection | None = None,
    operational_realization: OperationalRealizationDemandProjection | None = None,
    refuse_mismatched_projection: bool = False,
) -> GoalAdvancementDemandSet:
    """Preserve supplied family projections for the exact bounded horizon."""
    supplied = {
        "clarification": clarification,
        "inquiry": inquiry,
        "authority": authority,
        "operational_realization": operational_realization,
    }
    records: set[GoalAdvancementDemandFamilyAssemblyRecord] = set()
    all_conflicts: list[GoalAdvancementDemandFamilyIdentityConflict] = []
    for family in FAMILIES:
        projection = supplied[family]
        exclusion_reason = _excluded_family_reason(horizon, family)
        if projection is None:
            records.add(
                GoalAdvancementDemandFamilyAssemblyRecord(
                    family,
                    "excluded" if exclusion_reason else "absent",
                    None,
                    exclusion_reason,
                    (),
                )
            )
            continue
        conflicts = _identity_conflicts(family, projection, horizon)
        all_conflicts.extend(conflicts)
        if conflicts and refuse_mismatched_projection:
            records.add(
                GoalAdvancementDemandFamilyAssemblyRecord(
                    family,
                    "absent",
                    None,
                    exclusion_reason,
                    conflicts,
                )
            )
            continue
        records.add(
            GoalAdvancementDemandFamilyAssemblyRecord(
                family,
                "supplied",
                projection,
                exclusion_reason,
                conflicts,
            )
        )

    payload = {
        "horizon": horizon.horizon_id,
        "records": sorted(
            (
                record.family,
                record.disposition,
                getattr(record.projection, "projection_id", ""),
                record.exclusion_reason,
                tuple((c.conflict_kind, c.expected, c.actual) for c in record.identity_conflicts),
            )
            for record in records
        ),
        "refuse_mismatched_projection": refuse_mismatched_projection,
    }
    return GoalAdvancementDemandSet(
        _stable("goal-advancement-demand-set", payload),
        "GoalAdvancementDemandSet",
        horizon.goal_establishment_id,
        horizon.horizon_id,
        frozenset(records),
        horizon.unknowns,
        horizon.conflicts,
        tuple(
            f"{item.goal_advancement_demand_family}: {item.reason}"
            for item in horizon.explicitly_excluded_goal_advancement_demand_families
        ),
        refuse_mismatched_projection,
    )


def goal_advancement_demand_set_json(demand_set: GoalAdvancementDemandSet) -> dict[str, object]:
    return demand_set.to_json_dict()
