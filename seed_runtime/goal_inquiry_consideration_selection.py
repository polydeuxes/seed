"""Read-only selection of one visible bounded goal for inquiry consideration."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Iterable, Literal

from seed_runtime.goal_orientation_inventory import (
    GoalOrientationArtifactView,
    GoalOrientationInventory,
)

FocusEvidenceState = Literal[
    "exact_goal_identity",
    "missing_goal_identity",
    "ambiguous",
    "conflict",
    "Unknown",
]
SelectionState = Literal[
    "selected",
    "no_focus_evidence",
    "missing_goal_identity",
    "ambiguous",
    "conflict",
    "inventory_mismatch",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "GoalInquiryConsiderationSelection consumes explicit focus evidence naming exact bounded-goal identities only.",
    "Focused goal is not highest-priority goal.",
    "Selected for inquiry consideration is not goal activation, inquiry required, inquiry opened, frontier moved, work authorized, execution, recording, or mutation.",
    "Inventory uniqueness, dimensions, Null dimensions, pressures, labels, and topic similarity are not selection evidence.",
)


@dataclass(frozen=True)
class GoalFocusEvidence:
    """Explicit focus evidence for this owner.

    `goal_establishment_id` is lawful only when it names an exact established
    bounded-goal identity. Other states are preserved, not repaired here.
    """

    evidence_ref: str
    source_ref: str
    goal_establishment_id: str | None = None
    evidence_state: FocusEvidenceState = "exact_goal_identity"
    candidate_goal_refs: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()


@dataclass(frozen=True)
class GoalInquiryConsiderationSelection:
    selection_id: str
    inventory_candidate_set_id: str
    focus_evidence_refs: tuple[str, ...]
    focus_provenance_refs: tuple[str, ...]
    selection_state: SelectionState
    selected_goal_establishment_id: str | None = None
    selected_goal_source_ref: str | None = None
    non_selected_goals: tuple[GoalOrientationArtifactView, ...] = ()
    ambiguous_goal_refs: tuple[str, ...] = ()
    missing_identity_evidence_refs: tuple[str, ...] = ()
    inventory_mismatch_goal_refs: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    read_only: bool = True
    prioritizes: bool = False
    activates_goal: bool = False
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


def visible_bounded_goals(
    inventory: GoalOrientationInventory,
) -> tuple[GoalOrientationArtifactView, ...]:
    """Return only visible bounded-goal candidate records from associated dimensions."""
    return tuple(
        goal
        for dimension in inventory.dimensions
        for goal in dimension.bounded_goals
        if goal.artifact_kind == "bounded_goal"
    )


def goal_inventory_candidate_set_id(
    inventory: GoalOrientationInventory,
) -> str:
    """Stable identity for the visible bounded-goal candidate snapshot."""
    parts = [
        f"{goal.artifact_ref}\0{goal.source_ref}\0{goal.association_state}"
        for goal in visible_bounded_goals(inventory)
    ]
    return "goal_candidate_set:" + sha256("\n".join(parts).encode()).hexdigest()


def _selection_id(candidate_set_id: str, evidence: tuple[GoalFocusEvidence, ...]) -> str:
    parts = [candidate_set_id]
    parts.extend(
        f"{item.evidence_ref}\0{item.source_ref}\0{item.evidence_state}\0{item.goal_establishment_id or ''}"
        for item in evidence
    )
    return "goal_inquiry_consideration_selection:" + sha256(
        "\n".join(parts).encode()
    ).hexdigest()


def select_goal_for_inquiry_consideration(
    inventory: GoalOrientationInventory,
    focus_evidence: Iterable[GoalFocusEvidence] = (),
) -> GoalInquiryConsiderationSelection:
    """Select one visible bounded goal only when exact focus evidence lawfully does so."""
    evidence = tuple(focus_evidence)
    candidate_set_id = goal_inventory_candidate_set_id(inventory)
    selection_id = _selection_id(candidate_set_id, evidence)
    candidates = visible_bounded_goals(inventory)
    focus_refs = tuple(item.evidence_ref for item in evidence)
    provenance_refs = tuple(item.source_ref for item in evidence)

    def result(state: SelectionState, **kwargs: object) -> GoalInquiryConsiderationSelection:
        return GoalInquiryConsiderationSelection(
            selection_id=selection_id,
            inventory_candidate_set_id=candidate_set_id,
            focus_evidence_refs=focus_refs,
            focus_provenance_refs=provenance_refs,
            selection_state=state,
            non_selected_goals=tuple(kwargs.pop("non_selected_goals", candidates)),
            unknowns=tuple(
                dict.fromkeys(
                    unknown
                    for item in evidence
                    for unknown in item.unknowns
                )
            ),
            conflicts=tuple(
                dict.fromkeys(
                    conflict
                    for item in evidence
                    for conflict in item.conflicts
                )
            ),
            **kwargs,
        )

    if not evidence:
        return result("no_focus_evidence")

    if any(item.evidence_state == "conflict" for item in evidence):
        refs = tuple(
            dict.fromkeys(
                ref
                for item in evidence
                for ref in ((item.goal_establishment_id,) + item.candidate_goal_refs)
                if ref
            )
        )
        return result("conflict", ambiguous_goal_refs=refs)

    if any(item.evidence_state in {"missing_goal_identity", "Unknown"} for item in evidence):
        return result(
            "missing_goal_identity",
            missing_identity_evidence_refs=tuple(
                item.evidence_ref
                for item in evidence
                if item.evidence_state in {"missing_goal_identity", "Unknown"}
            ),
        )

    if any(item.evidence_state == "ambiguous" for item in evidence):
        return result(
            "ambiguous",
            ambiguous_goal_refs=tuple(
                dict.fromkeys(
                    ref for item in evidence for ref in item.candidate_goal_refs
                )
            ),
        )

    named_ids = tuple(
        item.goal_establishment_id
        for item in evidence
        if item.evidence_state == "exact_goal_identity" and item.goal_establishment_id
    )
    if not named_ids:
        return result("missing_goal_identity", missing_identity_evidence_refs=focus_refs)
    if len(set(named_ids)) != 1:
        return result("conflict", ambiguous_goal_refs=tuple(dict.fromkeys(named_ids)))

    target = named_ids[0]
    matches = tuple(goal for goal in candidates if goal.artifact_ref == target)
    if len(matches) == 1:
        selected = matches[0]
        return result(
            "selected",
            selected_goal_establishment_id=selected.artifact_ref,
            selected_goal_source_ref=selected.source_ref,
            non_selected_goals=tuple(goal for goal in candidates if goal != selected),
        )
    if len(matches) > 1:
        return result("ambiguous", ambiguous_goal_refs=tuple(goal.artifact_ref for goal in matches))
    return result("inventory_mismatch", inventory_mismatch_goal_refs=(target,))


def goal_inquiry_consideration_selection_json(
    selection: GoalInquiryConsiderationSelection,
) -> dict[str, object]:
    return selection.to_json_dict()
