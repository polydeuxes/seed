"""Read-only references for native advancement demand projection items."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal
from urllib.parse import quote

from seed_runtime.goal_advancement_demand_set import GoalAdvancementDemandSet, GoalAdvancementDemandFamily

ReferenceConflictKind = Literal["duplicate_native_lineage"]

BOUNDARY_NOTES: tuple[str, ...] = (
    "GoalAdvancementDemandReferenceSet exposes one reference for each native item in supplied demand projections.",
    "Reference identity binds demand set, family, native projection, and family-local native lineage only.",
    "Standing, bucket, evidence quality, and selectability are preserved as metadata rather than identity.",
    "Visible references are not necessarily selectable; only established native records are selectable.",
    "The reference set does not reclassify, select, prioritize, route, request clarification, open inquiry, request authority, select realization, authorize, execute, record, write the event ledger, or mutate cluster state.",
)

_REFERENCE_BUCKETS: dict[GoalAdvancementDemandFamily, tuple[str, ...]] = {
    "clarification": ("established", "unsupported", "unknown", "conflicting", "excluded_family", "unclassified"),
    "inquiry": ("established", "unsupported", "unknown", "conflicting", "excluded_family", "unclassified"),
    "authority": ("established", "unsupported", "unknown", "conflicting", "outside_current_scope", "unclassified"),
    "operational_realization": ("established", "unsupported", "unknown", "conflicting", "unclassified_here", "unclassified"),
}


def _part(value: str) -> str:
    return quote(value, safe="")


@dataclass(frozen=True)
class GoalAdvancementDemandReference:
    reference_id: str
    goal_advancement_demand_set_id: str
    goal_establishment_id: str
    horizon_id: str
    family: GoalAdvancementDemandFamily
    native_projection_id: str
    native_lineage: tuple[str, ...]
    native_bucket: str
    native_standing: str | None
    evidence_refs: tuple[str, ...]
    evidence_quality: tuple[str, ...]
    visible: bool
    selectable: bool
    conflict: bool = False
    conflict_kind: ReferenceConflictKind | None = None


@dataclass(frozen=True)
class GoalAdvancementDemandReferenceConflict:
    conflict_kind: ReferenceConflictKind
    goal_advancement_demand_set_id: str
    family: GoalAdvancementDemandFamily
    native_projection_id: str
    native_lineage: tuple[str, ...]
    visible: bool = True
    selectable: bool = False


@dataclass(frozen=True)
class GoalAdvancementDemandReferenceSet:
    reference_set_id: str
    artifact_type: str
    goal_advancement_demand_set_id: str
    goal_establishment_id: str
    horizon_id: str
    references: tuple[GoalAdvancementDemandReference, ...]
    conflicts: tuple[GoalAdvancementDemandReferenceConflict, ...]
    reclassifies_demand: bool = False
    selects_demand: bool = False
    prioritizes_demands: bool = False
    selects_route: bool = False
    requests_clarification: bool = False
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
        return asdict(self)


def _reference_id(goal_advancement_demand_set_id: str, family: GoalAdvancementDemandFamily, projection_id: str, lineage: tuple[str, ...]) -> str:
    parts = ("goal-advancement-demand-reference", goal_advancement_demand_set_id, family, projection_id, *lineage)
    return "/".join(_part(part) for part in parts)


def _reference_set_id(demand_set: GoalAdvancementDemandSet) -> str:
    return "/".join(_part(part) for part in ("goal-advancement-demand-reference-set", demand_set.goal_advancement_demand_set_id))


def _lineage(family: GoalAdvancementDemandFamily, item: object) -> tuple[str, ...]:
    if family == "clarification":
        return (getattr(item, "testimony_ref"), getattr(item, "bounded_uncertainty_component_ref"))
    if family == "inquiry":
        return (getattr(item, "testimony_ref"), getattr(item, "bounded_uncertainty_component_ref"), getattr(item, "repository_world_subject_ref"))
    if family == "authority":
        return (getattr(item, "requirement_testimony_ref"), getattr(item, "authority_testimony_ref"), getattr(item, "bounded_authority_component_ref"), getattr(item, "required_authority_class_ref"), getattr(item, "applicable_scope_ref"))
    return (getattr(item, "requirement_testimony_ref"), getattr(item, "standing_testimony_ref"), getattr(item, "bounded_realization_component_ref"), getattr(item, "required_transformation_ref"), getattr(item, "applicable_scope_ref"))


def _standing(family: GoalAdvancementDemandFamily, item: object) -> str | None:
    if family in ("clarification", "inquiry"):
        return getattr(item, "standing")
    if family == "authority":
        return getattr(item, "authority_demand_standing")
    return getattr(item, "operational_realization_demand_standing")


def _evidence_refs(item: object) -> tuple[str, ...]:
    refs = getattr(item, "evidence_refs", None)
    if refs is not None:
        return tuple(refs)
    ref = getattr(item, "evidence_ref", "")
    return (ref,) if ref else ()


def _evidence_quality(item: object) -> tuple[str, ...]:
    quality: list[str] = []
    for name in ("evidence_freshness", "evidence_availability"):
        value = getattr(item, name, None)
        if value is not None:
            quality.append(f"{name}={value}")
    return tuple(quality)


def project_goal_advancement_demand_reference_set(demand_set: GoalAdvancementDemandSet) -> GoalAdvancementDemandReferenceSet:
    """Project visible, read-only references without changing native demand meaning."""
    references: list[GoalAdvancementDemandReference] = []
    for record in sorted(demand_set.family_records, key=lambda item: item.family):
        if record.disposition != "supplied" or record.projection is None:
            continue
        projection = record.projection
        for bucket in _REFERENCE_BUCKETS[record.family]:
            for item in getattr(projection, bucket):
                lineage = _lineage(record.family, item)
                standing = _standing(record.family, item)
                references.append(
                    GoalAdvancementDemandReference(
                        _reference_id(demand_set.goal_advancement_demand_set_id, record.family, projection.projection_id, lineage),
                        demand_set.goal_advancement_demand_set_id,
                        demand_set.goal_establishment_id,
                        demand_set.horizon_id,
                        record.family,
                        projection.projection_id,
                        lineage,
                        bucket,
                        standing,
                        _evidence_refs(item),
                        _evidence_quality(item),
                        True,
                        bucket == "established" and standing == "established",
                    )
                )
    counts: dict[tuple[GoalAdvancementDemandFamily, str, tuple[str, ...]], int] = {}
    for ref in references:
        key = (ref.family, ref.native_projection_id, ref.native_lineage)
        counts[key] = counts.get(key, 0) + 1
    conflicts = tuple(
        GoalAdvancementDemandReferenceConflict("duplicate_native_lineage", demand_set.goal_advancement_demand_set_id, family, projection_id, lineage)
        for (family, projection_id, lineage), count in sorted(counts.items(), key=lambda entry: (entry[0][0], entry[0][1], entry[0][2]))
        if count > 1
    )
    conflict_keys = {(c.family, c.native_projection_id, c.native_lineage) for c in conflicts}
    marked = tuple(
        GoalAdvancementDemandReference(
            ref.reference_id, ref.goal_advancement_demand_set_id, ref.goal_establishment_id, ref.horizon_id,
            ref.family, ref.native_projection_id, ref.native_lineage, ref.native_bucket, ref.native_standing,
            ref.evidence_refs, ref.evidence_quality, ref.visible, ref.selectable,
            (ref.family, ref.native_projection_id, ref.native_lineage) in conflict_keys,
            "duplicate_native_lineage" if (ref.family, ref.native_projection_id, ref.native_lineage) in conflict_keys else None,
        )
        for ref in sorted(references, key=lambda ref: (ref.family, ref.native_projection_id, ref.native_lineage, ref.native_bucket))
    )
    return GoalAdvancementDemandReferenceSet(
        _reference_set_id(demand_set),
        "GoalAdvancementDemandReferenceSet",
        demand_set.goal_advancement_demand_set_id,
        demand_set.goal_establishment_id,
        demand_set.horizon_id,
        marked,
        conflicts,
    )


def goal_advancement_demand_reference_set_json(reference_set: GoalAdvancementDemandReferenceSet) -> dict[str, object]:
    return reference_set.to_json_dict()
