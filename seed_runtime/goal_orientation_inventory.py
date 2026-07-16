"""Read-only goal-orientation inventory over explicit association evidence."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Literal

from seed_runtime.bounded_operator_goal_establishment import (
    BoundedOperatorGoalEstablishment,
)

DimensionState = Literal["Null", "Associated"]
AssociationState = Literal["associated", "Unknown", "unmatched", "conflicting"]
ArtifactKind = Literal["pressure", "bounded_goal", "inquiry_reference", "material"]

SUPPORTED_GOAL_DIMENSIONS: tuple[str, ...] = (
    "operator_interaction",
    "operational_continuity",
    "resource_stewardship",
    "capability_recovery",
    "knowledge_quality",
    "implementation_maintenance",
)

BOUNDARY_NOTES: tuple[str, ...] = (
    "GoalOrientationInventory is read-only orientation, not a registry, planner, queue, or priority order.",
    "Dimensions are not pressures, bounded goals, active inquiries, hidden tasks, or execution authority.",
    "Visible pressure does not activate a goal; bounded goals do not grant inquiry, authorization, execution, recording, or mutation authority.",
    "Membership is consumed only from explicit association evidence and is not inferred from wording.",
)


@dataclass(frozen=True)
class GoalOrientationAssociation:
    """Explicit artifact-to-dimension association evidence."""

    artifact_kind: ArtifactKind
    artifact_ref: str
    source_ref: str
    dimension_refs: tuple[str, ...] = ()
    association_state: AssociationState = "associated"
    label: str = ""
    conflict_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class GoalOrientationArtifactView:
    artifact_kind: ArtifactKind
    artifact_ref: str
    source_ref: str
    association_state: AssociationState
    label: str = ""
    conflict_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class GoalOrientationDimensionEntry:
    dimension_ref: str
    state: DimensionState
    pressures: tuple[GoalOrientationArtifactView, ...] = ()
    bounded_goals: tuple[GoalOrientationArtifactView, ...] = ()
    inquiry_references: tuple[GoalOrientationArtifactView, ...] = ()
    other_material: tuple[GoalOrientationArtifactView, ...] = ()


@dataclass(frozen=True)
class GoalOrientationInventory:
    dimensions: tuple[GoalOrientationDimensionEntry, ...]
    unknown_association_material: tuple[GoalOrientationArtifactView, ...]
    unmatched_material: tuple[GoalOrientationArtifactView, ...]
    conflicting_material: tuple[GoalOrientationArtifactView, ...]
    read_only: bool = True
    activates_goals: bool = False
    moves_inquiries: bool = False
    prioritizes: bool = False
    schedules: bool = False
    authorizes_work: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def association_from_bounded_goal(
    goal: BoundedOperatorGoalEstablishment,
    *,
    dimension_refs: Iterable[str] = (),
    source_ref: str = "",
) -> GoalOrientationAssociation:
    """Create explicit inventory evidence for a bounded goal without deriving dimensions."""
    dimensions = tuple(dimension_refs)
    return GoalOrientationAssociation(
        artifact_kind="bounded_goal",
        artifact_ref=goal.goal_establishment_id,
        source_ref=source_ref or goal.ingress_artifact_ref,
        dimension_refs=dimensions,
        association_state="associated" if dimensions else "Unknown",
        label=goal.intended_outcome,
        conflict_refs=goal.conflicts,
    )


def _view(association: GoalOrientationAssociation) -> GoalOrientationArtifactView:
    return GoalOrientationArtifactView(
        artifact_kind=association.artifact_kind,
        artifact_ref=association.artifact_ref,
        source_ref=association.source_ref,
        association_state=association.association_state,
        label=association.label,
        conflict_refs=association.conflict_refs,
    )


def build_goal_orientation_inventory(
    associations: Iterable[GoalOrientationAssociation] = (),
    *,
    supported_dimensions: Iterable[str] = SUPPORTED_GOAL_DIMENSIONS,
) -> GoalOrientationInventory:
    """Build a read-only inventory from explicit association evidence only."""
    dimensions = tuple(supported_dimensions)
    buckets: dict[str, dict[str, list[GoalOrientationArtifactView]]] = {
        dimension: {
            "pressure": [],
            "bounded_goal": [],
            "inquiry_reference": [],
            "material": [],
        }
        for dimension in dimensions
    }
    unknown: list[GoalOrientationArtifactView] = []
    unmatched: list[GoalOrientationArtifactView] = []
    conflicting: list[GoalOrientationArtifactView] = []

    for association in associations:
        view = _view(association)
        if association.association_state == "Unknown" or not association.dimension_refs:
            unknown.append(view)
        if association.association_state == "conflicting" or association.conflict_refs:
            conflicting.append(view)
        known_dimension_seen = False
        has_unmatched_dimension = False
        for dimension_ref in association.dimension_refs:
            if dimension_ref not in buckets:
                has_unmatched_dimension = True
                continue
            known_dimension_seen = True
            buckets[dimension_ref][association.artifact_kind].append(view)
        if has_unmatched_dimension or (
            association.dimension_refs and not known_dimension_seen
        ):
            unmatched.append(view)

    entries = []
    for dimension in dimensions:
        bucket = buckets[dimension]
        state: DimensionState = "Associated" if any(bucket.values()) else "Null"
        entries.append(
            GoalOrientationDimensionEntry(
                dimension_ref=dimension,
                state=state,
                pressures=tuple(bucket["pressure"]),
                bounded_goals=tuple(bucket["bounded_goal"]),
                inquiry_references=tuple(bucket["inquiry_reference"]),
                other_material=tuple(bucket["material"]),
            )
        )
    return GoalOrientationInventory(
        dimensions=tuple(entries),
        unknown_association_material=tuple(unknown),
        unmatched_material=tuple(unmatched),
        conflicting_material=tuple(conflicting),
    )


def goal_orientation_inventory_json(
    inventory: GoalOrientationInventory,
) -> dict[str, object]:
    return inventory.to_json_dict()
