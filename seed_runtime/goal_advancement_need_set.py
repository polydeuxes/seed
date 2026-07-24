"""Read-only assembly of stage-owned need projections for one advancement horizon."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Literal

from seed_runtime.authority_need_projection import AuthorityNeedProjection
from seed_runtime.bounded_advancement_horizon import BoundedAdvancementHorizon
from seed_runtime.clarification_need_projection import ClarificationNeedProjection
from seed_runtime.inquiry_need_projection import InquiryNeedProjection
from seed_runtime.operational_realization_need_projection import (
    OperationalRealizationNeedProjection,
)

NeedFamily = Literal[
    "clarification",
    "inquiry",
    "authority",
    "operational_realization",
]
NeedFamilyDisposition = Literal["supplied", "absent", "excluded"]
IdentityConflictKind = Literal[
    "goal_identity_mismatch",
    "horizon_identity_mismatch",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "GoalAdvancementNeedSet preserves supplied stage-owned need projections without reinterpretation.",
    "Coexisting needs are an unordered set, not a priority order, overall blocker, route, or next action.",
    "Supplied, absent, and explicitly excluded need families remain distinct.",
    "The need set is not a sufficiency judgment and does not open inquiry, request authority, select realization, authorize, execute, record, write the event ledger, or mutate cluster state.",
)

FAMILIES: tuple[NeedFamily, ...] = (
    "clarification",
    "inquiry",
    "authority",
    "operational_realization",
)


@dataclass(frozen=True)
class NeedFamilyIdentityConflict:
    family: NeedFamily
    conflict_kind: IdentityConflictKind
    expected: str
    actual: str
    projection_id: str


@dataclass(frozen=True)
class NeedFamilyAssemblyRecord:
    family: NeedFamily
    disposition: NeedFamilyDisposition
    projection: (
        ClarificationNeedProjection
        | InquiryNeedProjection
        | AuthorityNeedProjection
        | OperationalRealizationNeedProjection
        | None
    ) = None
    exclusion_reason: str = ""
    identity_conflicts: tuple[NeedFamilyIdentityConflict, ...] = ()


@dataclass(frozen=True)
class GoalAdvancementNeedSet:
    need_set_id: str
    artifact_type: str
    goal_establishment_id: str
    horizon_id: str
    family_records: frozenset[NeedFamilyAssemblyRecord]
    horizon_unknowns: tuple[str, ...]
    horizon_conflicts: tuple[str, ...]
    horizon_exclusions: tuple[str, ...]
    refuses_mismatched_projection: bool
    classifies_need: bool = False
    orders_needs: bool = False
    prioritizes_needs: bool = False
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
            "need_set_id": self.need_set_id,
            "artifact_type": self.artifact_type,
            "goal_establishment_id": self.goal_establishment_id,
            "horizon_id": self.horizon_id,
            "family_records": tuple(asdict(record) for record in records),
            "horizon_unknowns": self.horizon_unknowns,
            "horizon_conflicts": self.horizon_conflicts,
            "horizon_exclusions": self.horizon_exclusions,
            "refuses_mismatched_projection": self.refuses_mismatched_projection,
            "classifies_need": self.classifies_need,
            "orders_needs": self.orders_needs,
            "prioritizes_needs": self.prioritizes_needs,
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


def _excluded_family_reason(horizon: BoundedAdvancementHorizon, family: NeedFamily) -> str:
    aliases = {family, f"{family}_need"}
    for exclusion in horizon.explicitly_excluded_need_families:
        if exclusion.need_family in aliases:
            return exclusion.reason
    return ""


def _identity_conflicts(
    family: NeedFamily,
    projection: (
        ClarificationNeedProjection
        | InquiryNeedProjection
        | AuthorityNeedProjection
        | OperationalRealizationNeedProjection
    ),
    horizon: BoundedAdvancementHorizon,
) -> tuple[NeedFamilyIdentityConflict, ...]:
    conflicts: list[NeedFamilyIdentityConflict] = []
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
                NeedFamilyIdentityConflict(
                    family,
                    kind,  # type: ignore[arg-type]
                    wanted,
                    actual,
                    projection.projection_id,
                )
            )
    return tuple(conflicts)


def assemble_goal_advancement_need_set(
    horizon: BoundedAdvancementHorizon,
    *,
    clarification: ClarificationNeedProjection | None = None,
    inquiry: InquiryNeedProjection | None = None,
    authority: AuthorityNeedProjection | None = None,
    operational_realization: OperationalRealizationNeedProjection | None = None,
    refuse_mismatched_projection: bool = False,
) -> GoalAdvancementNeedSet:
    """Preserve supplied family projections for the exact bounded horizon."""
    supplied = {
        "clarification": clarification,
        "inquiry": inquiry,
        "authority": authority,
        "operational_realization": operational_realization,
    }
    records: set[NeedFamilyAssemblyRecord] = set()
    all_conflicts: list[NeedFamilyIdentityConflict] = []
    for family in FAMILIES:
        projection = supplied[family]
        exclusion_reason = _excluded_family_reason(horizon, family)
        if projection is None:
            records.add(
                NeedFamilyAssemblyRecord(
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
                NeedFamilyAssemblyRecord(
                    family,
                    "absent",
                    None,
                    exclusion_reason,
                    conflicts,
                )
            )
            continue
        records.add(
            NeedFamilyAssemblyRecord(
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
    return GoalAdvancementNeedSet(
        _stable("goal-advancement-need-set", payload),
        "GoalAdvancementNeedSet",
        horizon.goal_establishment_id,
        horizon.horizon_id,
        frozenset(records),
        horizon.unknowns,
        horizon.conflicts,
        tuple(
            f"{item.need_family}: {item.reason}"
            for item in horizon.explicitly_excluded_need_families
        ),
        refuse_mismatched_projection,
    )


def goal_advancement_need_set_json(need_set: GoalAdvancementNeedSet) -> dict[str, object]:
    return need_set.to_json_dict()
