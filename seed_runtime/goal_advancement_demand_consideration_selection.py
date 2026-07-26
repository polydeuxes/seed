"""Read-only selection of one exact advancement demand reference for consideration."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Iterable, Literal

from seed_runtime.goal_advancement_demand_reference_set import (
    GoalAdvancementDemandReference,
    GoalAdvancementDemandReferenceSet,
)
from seed_runtime.goal_advancement_demand_set import GoalAdvancementDemandFamily

GoalAdvancementDemandConsiderationEvidenceState = Literal[
    "exact_reference",
    "missing_identity",
    "ambiguous",
    "conflict",
    "Unknown",
]
SelectionState = Literal[
    "selected",
    "no_consideration_evidence",
    "missing_identity",
    "ambiguous",
    "conflict",
    "reference_mismatch",
    "absent_reference",
    "duplicate_lineage_conflict",
    "non_selectable",
]

BOUNDARY_NOTES: tuple[str, ...] = (
    "GoalAdvancementDemandConsiderationSelection consumes explicit consideration evidence naming exact visible goal-advancement-demand references only.",
    "The testified demand must match the same demand set, selected goal, bounded horizon, demand family, native projection, and native record lineage.",
    "Demand selected for consideration is not highest-priority demand, primary blocker, resolution selected, next action selected, realization selected, inquiry opened, authority requested, authorization, execution, recording, event-ledger write, or mutation.",
    "Uniqueness, sufficiency reasons, standing labels, presentation order, family, wording similarity, severity, and selectable count do not select a demand.",
)


@dataclass(frozen=True)
class GoalAdvancementDemandConsiderationEvidence:
    """Attributed testimony for one goal-advancement-demand consideration selection."""

    evidence_ref: str
    source_ref: str
    reference_id: str | None = None
    goal_advancement_demand_set_id: str | None = None
    goal_establishment_id: str | None = None
    horizon_id: str | None = None
    family: GoalAdvancementDemandFamily | None = None
    native_projection_id: str | None = None
    native_lineage: tuple[str, ...] = ()
    evidence_state: GoalAdvancementDemandConsiderationEvidenceState = "exact_reference"
    candidate_reference_ids: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()


@dataclass(frozen=True)
class GoalAdvancementDemandConsiderationSelection:
    selection_id: str
    reference_set_id: str
    goal_advancement_demand_set_id: str
    selected_goal_id: str
    horizon_id: str
    consideration_evidence_refs: tuple[str, ...]
    consideration_provenance_refs: tuple[str, ...]
    selection_state: SelectionState
    selected_reference: GoalAdvancementDemandReference | None = None
    visible_references: tuple[GoalAdvancementDemandReference, ...] = ()
    non_selected_references: tuple[GoalAdvancementDemandReference, ...] = ()
    ambiguous_reference_ids: tuple[str, ...] = ()
    missing_identity_evidence_refs: tuple[str, ...] = ()
    reference_mismatch_evidence_refs: tuple[str, ...] = ()
    absent_reference_ids: tuple[str, ...] = ()
    duplicate_lineage_reference_ids: tuple[str, ...] = ()
    non_selectable_reference_ids: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    read_only: bool = True
    selects_demand: bool = False
    prioritizes_demands: bool = False
    declares_primary_blocker: bool = False
    selects_resolution: bool = False
    selects_next_action: bool = False
    opens_inquiry: bool = False
    requests_authority: bool = False
    selects_realization: bool = False
    authorizes_work: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def _selection_id(
    reference_set: GoalAdvancementDemandReferenceSet,
    evidence: tuple[GoalAdvancementDemandConsiderationEvidence, ...],
) -> str:
    lines = [reference_set.reference_set_id]
    lines.extend(
        "\0".join(
            (
                item.evidence_ref,
                item.source_ref,
                item.evidence_state,
                item.reference_id or "",
                item.goal_advancement_demand_set_id or "",
                item.goal_establishment_id or "",
                item.horizon_id or "",
                item.family or "",
                item.native_projection_id or "",
                "|".join(item.native_lineage),
            )
        )
        for item in evidence
    )
    return "goal_advancement_demand_consideration_selection:" + sha256(
        "\n".join(lines).encode()
    ).hexdigest()


def select_goal_advancement_demand_for_consideration(
    reference_set: GoalAdvancementDemandReferenceSet,
    consideration_evidence: Iterable[GoalAdvancementDemandConsiderationEvidence] = (),
) -> GoalAdvancementDemandConsiderationSelection:
    """Select one demand only from exact, fully bound consideration evidence."""
    evidence = tuple(consideration_evidence)
    evidence_refs = tuple(item.evidence_ref for item in evidence)
    provenance_refs = tuple(item.source_ref for item in evidence)
    selection_id = _selection_id(reference_set, evidence)
    visible = reference_set.references

    def result(
        state: SelectionState, **kwargs: object
    ) -> GoalAdvancementDemandConsiderationSelection:
        selected = kwargs.get("selected_reference")
        non_selected = tuple(ref for ref in visible if ref != selected)
        return GoalAdvancementDemandConsiderationSelection(
            selection_id,
            reference_set.reference_set_id,
            reference_set.goal_advancement_demand_set_id,
            reference_set.goal_establishment_id,
            reference_set.horizon_id,
            evidence_refs,
            provenance_refs,
            state,
            visible_references=visible,
            non_selected_references=tuple(
                kwargs.pop("non_selected_references", non_selected)
            ),
            unknowns=tuple(
                dict.fromkeys(
                    unknown for item in evidence for unknown in item.unknowns
                )
            ),
            conflicts=tuple(
                dict.fromkeys(
                    conflict for item in evidence for conflict in item.conflicts
                )
            ),
            **kwargs,
        )

    if not evidence:
        return result("no_consideration_evidence")
    if any(item.evidence_state == "conflict" for item in evidence):
        return result(
            "conflict",
            ambiguous_reference_ids=tuple(
                dict.fromkeys(
                    ref
                    for item in evidence
                    for ref in ((item.reference_id,) + item.candidate_reference_ids)
                    if ref
                )
            ),
        )
    if any(item.evidence_state in {"missing_identity", "Unknown"} for item in evidence):
        return result(
            "missing_identity",
            missing_identity_evidence_refs=tuple(
                item.evidence_ref
                for item in evidence
                if item.evidence_state in {"missing_identity", "Unknown"}
            ),
        )
    if any(item.evidence_state == "ambiguous" for item in evidence):
        return result(
            "ambiguous",
            ambiguous_reference_ids=tuple(
                dict.fromkeys(
                    ref for item in evidence for ref in item.candidate_reference_ids
                )
            ),
        )

    exact = tuple(item for item in evidence if item.evidence_state == "exact_reference")
    if not exact or any(not item.reference_id for item in exact):
        return result("missing_identity", missing_identity_evidence_refs=evidence_refs)
    named_ids = tuple(item.reference_id for item in exact if item.reference_id)
    if len(set(named_ids)) != 1:
        return result(
            "conflict", ambiguous_reference_ids=tuple(dict.fromkeys(named_ids))
        )

    mismatched = tuple(
        item.evidence_ref
        for item in exact
        if item.goal_advancement_demand_set_id != reference_set.goal_advancement_demand_set_id
        or item.goal_establishment_id != reference_set.goal_establishment_id
        or item.horizon_id != reference_set.horizon_id
        or item.family is None
        or item.native_projection_id is None
        or not item.native_lineage
    )
    if mismatched:
        return result(
            "reference_mismatch", reference_mismatch_evidence_refs=mismatched
        )

    matches = tuple(ref for ref in visible if ref.reference_id == named_ids[0])
    if not matches:
        return result("absent_reference", absent_reference_ids=(named_ids[0],))
    if len(matches) != 1:
        if any(ref.conflict for ref in matches):
            return result(
                "duplicate_lineage_conflict",
                duplicate_lineage_reference_ids=tuple(
                    dict.fromkeys(ref.reference_id for ref in matches)
                ),
            )
        return result(
            "ambiguous",
            ambiguous_reference_ids=tuple(ref.reference_id for ref in matches),
        )
    ref = matches[0]
    if any(
        (item.family, item.native_projection_id, item.native_lineage)
        != (ref.family, ref.native_projection_id, ref.native_lineage)
        for item in exact
    ):
        return result(
            "reference_mismatch",
            reference_mismatch_evidence_refs=tuple(
                item.evidence_ref for item in exact
            ),
        )
    if ref.conflict:
        return result(
            "duplicate_lineage_conflict",
            duplicate_lineage_reference_ids=(ref.reference_id,),
        )
    if not ref.selectable:
        return result(
            "non_selectable", non_selectable_reference_ids=(ref.reference_id,)
        )
    return result("selected", selected_reference=ref)


def goal_advancement_demand_consideration_selection_json(
    selection: GoalAdvancementDemandConsiderationSelection,
) -> dict[str, object]:
    return selection.to_json_dict()
