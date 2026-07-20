"""Read-only resolution of one testified bounded-goal candidate identity.

This boundary does not select a goal, establish focus, determine priority,
classify advancement needs, or open inquiry. It only compares attributed
candidate testimony with one visible goal-inventory snapshot.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Iterable, Literal

from seed_runtime.goal_orientation_inventory import (
    GoalOrientationArtifactView,
    GoalOrientationInventory,
)

GoalCandidateTestimonyState = Literal[
    "exact_goal_identity",
    "missing_goal_identity",
    "ambiguous",
    "conflict",
    "Unknown",
]
GoalCandidateResolutionState = Literal[
    "resolved",
    "no_candidate_testimony",
    "missing_goal_identity",
    "ambiguous",
    "conflict",
    "inventory_mismatch",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "GoalConsiderationCandidateResolution consumes attributed testimony naming bounded-goal candidate identities.",
    "Exact candidate-identity resolution is not Seed-owned goal selection, constitutional focus, priority, advancement, or inquiry applicability.",
    "Inventory uniqueness, dimensions, Null dimensions, pressures, labels, and topic similarity do not originate candidate testimony.",
    "The resolution is read-only and does not activate goals, classify needs, open inquiry, authorize work, execute, record, or mutate state.",
)


@dataclass(frozen=True)
class GoalConsiderationCandidateTestimony:
    """Attributed testimony naming a possible goal candidate for consideration."""

    testimony_ref: str
    source_ref: str
    goal_establishment_id: str | None = None
    testimony_state: GoalCandidateTestimonyState = "exact_goal_identity"
    candidate_goal_refs: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()


@dataclass(frozen=True)
class GoalConsiderationCandidateResolution:
    resolution_id: str
    inventory_candidate_set_id: str
    candidate_testimony_refs: tuple[str, ...]
    candidate_source_refs: tuple[str, ...]
    resolution_state: GoalCandidateResolutionState
    resolved_goal_establishment_id: str | None = None
    resolved_goal_source_ref: str | None = None
    visible_goal_candidates: tuple[GoalOrientationArtifactView, ...] = ()
    ambiguous_goal_refs: tuple[str, ...] = ()
    missing_identity_testimony_refs: tuple[str, ...] = ()
    inventory_mismatch_goal_refs: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    read_only: bool = True
    selects_goal: bool = False
    establishes_focus: bool = False
    prioritizes: bool = False
    activates_goal: bool = False
    classifies_advancement_need: bool = False
    requires_inquiry: bool = False
    opens_inquiry: bool = False
    moves_frontier: bool = False
    authorizes_work: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def visible_bounded_goal_candidates(
    inventory: GoalOrientationInventory,
) -> tuple[GoalOrientationArtifactView, ...]:
    """Return visible bounded-goal records from associated dimensions."""
    return tuple(
        goal
        for dimension in inventory.dimensions
        for goal in dimension.bounded_goals
        if goal.artifact_kind == "bounded_goal"
    )


def goal_consideration_candidate_set_id(
    inventory: GoalOrientationInventory,
) -> str:
    """Return a stable identity for the visible bounded-goal snapshot."""
    parts = [
        f"{goal.artifact_ref}\0{goal.source_ref}\0{goal.association_state}"
        for goal in visible_bounded_goal_candidates(inventory)
    ]
    return "goal_candidate_set:" + sha256("\n".join(parts).encode()).hexdigest()


def _resolution_id(
    candidate_set_id: str,
    testimony: tuple[GoalConsiderationCandidateTestimony, ...],
) -> str:
    parts = [candidate_set_id]
    parts.extend(
        f"{item.testimony_ref}\0{item.source_ref}\0{item.testimony_state}\0{item.goal_establishment_id or ''}"
        for item in testimony
    )
    return "goal_consideration_candidate_resolution:" + sha256(
        "\n".join(parts).encode()
    ).hexdigest()


def resolve_goal_consideration_candidate(
    inventory: GoalOrientationInventory,
    candidate_testimony: Iterable[GoalConsiderationCandidateTestimony] = (),
) -> GoalConsiderationCandidateResolution:
    """Resolve one exact testified candidate identity against the inventory."""
    testimony = tuple(candidate_testimony)
    candidate_set_id = goal_consideration_candidate_set_id(inventory)
    resolution_id = _resolution_id(candidate_set_id, testimony)
    candidates = visible_bounded_goal_candidates(inventory)
    testimony_refs = tuple(item.testimony_ref for item in testimony)
    source_refs = tuple(item.source_ref for item in testimony)

    def result(
        state: GoalCandidateResolutionState,
        **kwargs: object,
    ) -> GoalConsiderationCandidateResolution:
        return GoalConsiderationCandidateResolution(
            resolution_id=resolution_id,
            inventory_candidate_set_id=candidate_set_id,
            candidate_testimony_refs=testimony_refs,
            candidate_source_refs=source_refs,
            resolution_state=state,
            visible_goal_candidates=candidates,
            unknowns=tuple(
                dict.fromkeys(
                    unknown
                    for item in testimony
                    for unknown in item.unknowns
                )
            ),
            conflicts=tuple(
                dict.fromkeys(
                    conflict
                    for item in testimony
                    for conflict in item.conflicts
                )
            ),
            **kwargs,
        )

    if not testimony:
        return result("no_candidate_testimony")

    if any(item.testimony_state == "conflict" for item in testimony):
        refs = tuple(
            dict.fromkeys(
                ref
                for item in testimony
                for ref in ((item.goal_establishment_id,) + item.candidate_goal_refs)
                if ref
            )
        )
        return result("conflict", ambiguous_goal_refs=refs)

    if any(
        item.testimony_state in {"missing_goal_identity", "Unknown"}
        for item in testimony
    ):
        return result(
            "missing_goal_identity",
            missing_identity_testimony_refs=tuple(
                item.testimony_ref
                for item in testimony
                if item.testimony_state in {"missing_goal_identity", "Unknown"}
            ),
        )

    if any(item.testimony_state == "ambiguous" for item in testimony):
        return result(
            "ambiguous",
            ambiguous_goal_refs=tuple(
                dict.fromkeys(
                    ref for item in testimony for ref in item.candidate_goal_refs
                )
            ),
        )

    named_ids = tuple(
        item.goal_establishment_id
        for item in testimony
        if item.testimony_state == "exact_goal_identity"
        and item.goal_establishment_id
    )
    if not named_ids:
        return result(
            "missing_goal_identity",
            missing_identity_testimony_refs=testimony_refs,
        )
    if len(set(named_ids)) != 1:
        return result(
            "conflict",
            ambiguous_goal_refs=tuple(dict.fromkeys(named_ids)),
        )

    target = named_ids[0]
    matches = tuple(goal for goal in candidates if goal.artifact_ref == target)
    if len(matches) == 1:
        resolved = matches[0]
        return result(
            "resolved",
            resolved_goal_establishment_id=resolved.artifact_ref,
            resolved_goal_source_ref=resolved.source_ref,
        )
    if len(matches) > 1:
        return result(
            "ambiguous",
            ambiguous_goal_refs=tuple(goal.artifact_ref for goal in matches),
        )
    return result("inventory_mismatch", inventory_mismatch_goal_refs=(target,))


def goal_consideration_candidate_resolution_json(
    resolution: GoalConsiderationCandidateResolution,
) -> dict[str, object]:
    return resolution.to_json_dict()
