"""Read-only family-owned advancement need coverage assembly.

This assembler preserves native need-projection identity alongside family-owned
bounded candidate-space coverage testimony.  It does not own candidate spaces,
classify needs, plan, route, authorize, execute, record, write the event ledger,
or mutate cluster state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Literal

from seed_runtime.bounded_advancement_horizon import BoundedAdvancementHorizon
from seed_runtime.goal_advancement_need_set import FAMILIES, NeedFamily

ScopeDisposition = Literal["included", "excluded", "conflicting"]
CoverageStanding = Literal[
    "complete_for_horizon",
    "partial",
    "unknown",
    "conflicting",
    "not_evaluated",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "AdvancementNeedFamilyCoverageSet preserves family-owned coverage testimony without owning candidate spaces.",
    "Scope disposition and coverage standing are separate dimensions.",
    "Excluded families keep explicit horizon reasons and are not evaluated for coverage completeness.",
    "Complete coverage requires matching bounded candidate space testimony, complete included-component accounting, explicit exclusions, and no material coverage conflict.",
    "The coverage set is not sufficient-for-now, priority, routing, authority selection, realization selection, execution, recording, event-ledger write, or cluster mutation.",
)


@dataclass(frozen=True)
class FamilyBoundedCandidateSpace:
    family: NeedFamily
    candidate_space_id: str
    candidate_resolution_id: str
    goal_establishment_id: str
    horizon_id: str
    native_projection_id: str
    evidence_snapshot_ref: str
    component_refs: tuple[str, ...]


@dataclass(frozen=True)
class ExplicitComponentExclusion:
    component_ref: str
    reason: str


@dataclass(frozen=True)
class FamilyCoverageTestimony:
    family: NeedFamily
    testimony_id: str
    candidate_resolution_id: str
    goal_establishment_id: str
    horizon_id: str
    native_projection_id: str
    candidate_space_id: str
    evidence_snapshot_ref: str
    covered_component_refs: tuple[str, ...] = ()
    unexamined_component_refs: tuple[str, ...] = ()
    explicitly_excluded_components: tuple[ExplicitComponentExclusion, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    stale: bool = False
    unavailable: bool = False


@dataclass(frozen=True)
class FamilyCoverageIdentityConflict:
    family: NeedFamily
    conflict_kind: str
    expected: str
    actual: str


@dataclass(frozen=True)
class AdvancementNeedFamilyCoverageRecord:
    family: NeedFamily
    scope_disposition: ScopeDisposition
    coverage_standing: CoverageStanding
    candidate_resolution_id: str
    goal_establishment_id: str
    horizon_id: str
    native_projection_id: str = ""
    candidate_space_id: str = ""
    evidence_snapshot_ref: str = ""
    covered_component_refs: tuple[str, ...] = ()
    unexamined_component_refs: tuple[str, ...] = ()
    explicitly_excluded_components: tuple[ExplicitComponentExclusion, ...] = ()
    horizon_exclusion_reason: str = ""
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    identity_conflicts: tuple[FamilyCoverageIdentityConflict, ...] = ()


@dataclass(frozen=True)
class AdvancementNeedFamilyCoverageSet:
    coverage_set_id: str
    artifact_type: str
    candidate_resolution_id: str
    goal_establishment_id: str
    horizon_id: str
    family_records: frozenset[AdvancementNeedFamilyCoverageRecord]
    judges_sufficiency: bool = False
    sufficient_for_now: None = None
    prioritizes_families: bool = False
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
        data["family_records"] = tuple(
            asdict(record)
            for record in sorted(self.family_records, key=lambda r: r.family)
        )
        return data


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return prefix + ":" + sha256(encoded).hexdigest()


def _dedupe(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(v for v in values if v))


def _horizon_exclusion_reason(
    horizon: BoundedAdvancementHorizon, family: NeedFamily
) -> str:
    aliases = {family, f"{family}_need"}
    for exclusion in horizon.explicitly_excluded_need_families:
        if exclusion.need_family in aliases:
            return exclusion.reason
    return ""


def _identity_conflicts(
    horizon: BoundedAdvancementHorizon,
    space: FamilyBoundedCandidateSpace | None,
    testimony: FamilyCoverageTestimony | None,
    family: NeedFamily,
) -> tuple[FamilyCoverageIdentityConflict, ...]:
    conflicts: list[FamilyCoverageIdentityConflict] = []
    expected = {
        "candidate_resolution_identity_mismatch": horizon.candidate_resolution_id,
        "goal_identity_mismatch": horizon.goal_establishment_id,
        "horizon_identity_mismatch": horizon.horizon_id,
    }
    for owner, actuals in (("candidate_space", space), ("testimony", testimony)):
        if actuals is None:
            continue
        values = (
            actuals.candidate_resolution_id,
            actuals.goal_establishment_id,
            actuals.horizon_id,
        )
        for (kind, wanted), actual in zip(expected.items(), values):
            if wanted != actual:
                conflicts.append(
                    FamilyCoverageIdentityConflict(
                        family, f"{owner}_{kind}", wanted, actual
                    )
                )
    if space and testimony:
        pairs = (
            (
                "native_projection_identity_mismatch",
                space.native_projection_id,
                testimony.native_projection_id,
            ),
            (
                "candidate_space_identity_mismatch",
                space.candidate_space_id,
                testimony.candidate_space_id,
            ),
            (
                "evidence_snapshot_identity_mismatch",
                space.evidence_snapshot_ref,
                testimony.evidence_snapshot_ref,
            ),
        )
        for kind, wanted, actual in pairs:
            if wanted != actual:
                conflicts.append(
                    FamilyCoverageIdentityConflict(family, kind, wanted, actual)
                )
    return tuple(conflicts)


def _coverage_standing(
    space: FamilyBoundedCandidateSpace | None,
    testimony: FamilyCoverageTestimony | None,
    conflicts: tuple[FamilyCoverageIdentityConflict, ...],
) -> CoverageStanding:
    if conflicts or (testimony and testimony.conflicts):
        return "conflicting"
    if space is None or testimony is None or testimony.unavailable:
        return "unknown"
    if testimony.stale:
        return "partial"
    exclusions_missing_reasons = any(
        not item.reason for item in testimony.explicitly_excluded_components
    )
    components = set(space.component_refs)
    covered = set(testimony.covered_component_refs)
    unexamined = set(testimony.unexamined_component_refs)
    excluded = {item.component_ref for item in testimony.explicitly_excluded_components}
    outside = (covered | unexamined | excluded) - components
    if outside or exclusions_missing_reasons:
        return "conflicting"
    if testimony.unknowns:
        return "unknown"
    if components and components == covered | excluded and not unexamined:
        return "complete_for_horizon"
    return "partial"


def assemble_advancement_need_family_coverage_set(
    horizon: BoundedAdvancementHorizon,
    *,
    candidate_spaces: Iterable[FamilyBoundedCandidateSpace] = (),
    testimonies: Iterable[FamilyCoverageTestimony] = (),
) -> AdvancementNeedFamilyCoverageSet:
    """Assemble family coverage records for one exact bounded horizon."""
    spaces = {space.family: space for space in candidate_spaces}
    by_family = {testimony.family: testimony for testimony in testimonies}
    records: set[AdvancementNeedFamilyCoverageRecord] = set()
    for family in FAMILIES:
        exclusion_reason = _horizon_exclusion_reason(horizon, family)
        space = spaces.get(family)
        testimony = by_family.get(family)
        if exclusion_reason:
            records.add(
                AdvancementNeedFamilyCoverageRecord(
                    family,
                    "excluded",
                    "not_evaluated",
                    horizon.candidate_resolution_id,
                    horizon.goal_establishment_id,
                    horizon.horizon_id,
                    horizon_exclusion_reason=exclusion_reason,
                )
            )
            continue
        identity_conflicts = _identity_conflicts(horizon, space, testimony, family)
        standing = _coverage_standing(space, testimony, identity_conflicts)
        scope: ScopeDisposition = (
            "conflicting" if standing == "conflicting" else "included"
        )
        records.add(
            AdvancementNeedFamilyCoverageRecord(
                family,
                scope,
                standing,
                horizon.candidate_resolution_id,
                horizon.goal_establishment_id,
                horizon.horizon_id,
                native_projection_id=(
                    space.native_projection_id
                    if space
                    else (testimony.native_projection_id if testimony else "")
                ),
                candidate_space_id=(
                    space.candidate_space_id
                    if space
                    else (testimony.candidate_space_id if testimony else "")
                ),
                evidence_snapshot_ref=(
                    space.evidence_snapshot_ref
                    if space
                    else (testimony.evidence_snapshot_ref if testimony else "")
                ),
                covered_component_refs=(
                    ()
                    if testimony is None
                    else _dedupe(testimony.covered_component_refs)
                ),
                unexamined_component_refs=(
                    ()
                    if testimony is None
                    else _dedupe(testimony.unexamined_component_refs)
                ),
                explicitly_excluded_components=(
                    ()
                    if testimony is None
                    else testimony.explicitly_excluded_components
                ),
                unknowns=() if testimony is None else testimony.unknowns,
                conflicts=() if testimony is None else testimony.conflicts,
                identity_conflicts=identity_conflicts,
            )
        )
    payload = [
        (
            r.family,
            r.scope_disposition,
            r.coverage_standing,
            r.native_projection_id,
            r.candidate_space_id,
            r.evidence_snapshot_ref,
        )
        for r in records
    ]
    return AdvancementNeedFamilyCoverageSet(
        _stable(
            "advancement-need-family-coverage-set",
            {"horizon": horizon.horizon_id, "records": sorted(payload)},
        ),
        "AdvancementNeedFamilyCoverageSet",
        horizon.candidate_resolution_id,
        horizon.goal_establishment_id,
        horizon.horizon_id,
        frozenset(records),
    )


def advancement_need_family_coverage_set_json(
    coverage_set: AdvancementNeedFamilyCoverageSet,
) -> dict[str, object]:
    return coverage_set.to_json_dict()
