"""Read-only inquiry frontier-boundary testimony preservation.

This module preserves stage-owned frontier-boundary clauses for one exact
selected inquiry need.  It does not assemble a frontier, formulate a question,
open inquiry, authorize access, execute, record, write the event ledger, or
mutate cluster state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Literal

from seed_runtime.advancement_need_consideration_selection import AdvancementNeedConsiderationSelection

ClauseFamily = Literal[
    "included_excluded_inquiry_scope",
    "eligible_ineligible_evidence_territory",
    "sufficient_resolution_conditions",
    "lawful_stopping_conditions",
]
ClauseStanding = Literal["established", "unsupported", "unknown", "conflicting", "unclassified"]
ScopeDisposition = Literal["included", "excluded", "outside_current_scope", "conflicting", "not_applicable"]
EvidenceCurrency = Literal["current", "stale", "unknown", "conflicting"]
EvidenceAvailability = Literal["available", "unavailable", "unknown", "conflicting"]
FamilyDisposition = Literal["inquiry", "adjacent_family", "mixed", "unclassified"]
OwnershipBasis = Literal["stage_producer_lineage", "adapter_lineage", "unowned"]

BOUNDARY_NOTES: tuple[str, ...] = (
    "InquiryFrontierBoundaryTestimony preserves unordered stage-owned clauses for one exact selected inquiry need.",
    "Goal-horizon scope is not inquiry scope; visible evidence is not eligible evidence territory and is not selected source evidence.",
    "Uncertainty subject is not sufficient-resolution condition; stale or unavailable evidence is not a stopping condition.",
    "Boundary testimony is not frontier assembly, constitutional question formulation, inquiry opening, authorization, execution, recording, event-ledger write, or cluster mutation.",
)


@dataclass(frozen=True)
class FrontierBoundaryClauseInput:
    clause_ref: str
    clause_family: ClauseFamily
    clause_text: str
    producer_ref: str = ""
    producer_lineage: tuple[str, ...] = ()
    adapter_ref: str = ""
    adapter_lineage: tuple[str, ...] = ()
    source_lineage: tuple[str, ...] = ()
    evidence_classes: tuple[str, ...] = ()
    provenance_roles: tuple[str, ...] = ()
    already_visible_evidence_refs: tuple[str, ...] = ()
    eligible_evidence_territory_refs: tuple[str, ...] = ()
    clause_standing: ClauseStanding = "unclassified"
    scope_disposition: ScopeDisposition = "not_applicable"
    evidence_currency: EvidenceCurrency = "unknown"
    evidence_availability: EvidenceAvailability = "unknown"
    family_disposition: FamilyDisposition = "unclassified"
    caller_asserts_ownership: bool = False


@dataclass(frozen=True)
class InquiryFrontierBoundaryClause:
    clause_ref: str
    clause_family: ClauseFamily
    clause_text: str
    selected_need_reference_id: str
    native_projection_id: str
    native_lineage: tuple[str, ...]
    need_set_id: str
    selected_need_selection_id: str
    selected_need_goal_id: str
    horizon_id: str
    source_testimony_ref: str
    bounded_uncertainty_component_ref: str
    repository_world_subject_ref: str
    producer_ref: str
    producer_lineage: tuple[str, ...]
    adapter_ref: str
    adapter_lineage: tuple[str, ...]
    ownership_basis: OwnershipBasis
    source_lineage: tuple[str, ...]
    evidence_classes: tuple[str, ...]
    provenance_roles: tuple[str, ...]
    already_visible_evidence_refs: tuple[str, ...]
    eligible_evidence_territory_refs: tuple[str, ...]
    clause_standing: ClauseStanding
    scope_disposition: ScopeDisposition
    evidence_currency: EvidenceCurrency
    evidence_availability: EvidenceAvailability
    family_disposition: FamilyDisposition


@dataclass(frozen=True)
class InquiryFrontierBoundaryTestimony:
    testimony_id: str
    selected_need_reference_id: str | None
    native_projection_id: str | None
    native_lineage: tuple[str, ...]
    need_set_id: str
    selected_need_selection_id: str
    selected_need_goal_id: str
    horizon_id: str
    source_testimony_ref: str | None
    bounded_uncertainty_component_ref: str | None
    repository_world_subject_ref: str | None
    already_visible_evidence_refs: tuple[str, ...]
    clauses: tuple[InquiryFrontierBoundaryClause, ...]
    unowned_clause_refs: tuple[str, ...]
    read_only: bool = True
    assembles_frontier: bool = False
    formulates_question: bool = False
    opens_inquiry: bool = False
    authorizes_access: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    selects_sources: bool = False
    selects_observations: bool = False
    judges_collective_sufficiency: bool = False
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + sha256(encoded).hexdigest()


def _ownership(item: FrontierBoundaryClauseInput) -> OwnershipBasis:
    if item.producer_ref and item.producer_lineage:
        return "stage_producer_lineage"
    if item.adapter_ref and item.adapter_lineage:
        return "adapter_lineage"
    return "unowned"


def preserve_inquiry_frontier_boundary_testimony(
    selected_need: AdvancementNeedConsiderationSelection,
    clauses: Iterable[FrontierBoundaryClauseInput] = (),
) -> InquiryFrontierBoundaryTestimony:
    """Preserve unordered boundary clauses for the exact selected inquiry need."""
    clause_inputs = tuple(clauses)
    ref = selected_need.selected_reference if selected_need.selection_state == "selected" else None
    if ref is None or ref.family != "inquiry":
        payload = {"selection": selected_need.selection_id, "clauses": [c.clause_ref for c in clause_inputs], "state": "no-selected-inquiry"}
        return InquiryFrontierBoundaryTestimony(
            _stable("inquiry-frontier-boundary-testimony", payload),
            None, None, (), selected_need.reference_set_id, selected_need.need_set_id,
            selected_need.selected_goal_id, selected_need.horizon_id, None, None, None, (), (),
            tuple(c.clause_ref for c in clause_inputs if _ownership(c) == "unowned"),
        )

    source_testimony_ref, component_ref, subject_ref = ref.native_lineage
    visible_refs = ref.evidence_refs
    preserved: list[InquiryFrontierBoundaryClause] = []
    for item in clause_inputs:
        preserved.append(
            InquiryFrontierBoundaryClause(
                item.clause_ref, item.clause_family, item.clause_text,
                ref.reference_id, ref.native_projection_id, ref.native_lineage,
                ref.need_set_id, ref.selection_id, ref.goal_establishment_id, ref.horizon_id,
                source_testimony_ref, component_ref, subject_ref,
                item.producer_ref, tuple(item.producer_lineage), item.adapter_ref, tuple(item.adapter_lineage), _ownership(item),
                tuple(item.source_lineage), tuple(item.evidence_classes), tuple(item.provenance_roles),
                tuple(item.already_visible_evidence_refs), tuple(item.eligible_evidence_territory_refs),
                item.clause_standing, item.scope_disposition, item.evidence_currency, item.evidence_availability, item.family_disposition,
            )
        )
    payload = {"selected_need": ref.reference_id, "native": ref.native_lineage, "clauses": [c.clause_ref for c in clause_inputs]}
    return InquiryFrontierBoundaryTestimony(
        _stable("inquiry-frontier-boundary-testimony", payload),
        ref.reference_id, ref.native_projection_id, ref.native_lineage,
        ref.need_set_id, ref.selection_id, ref.goal_establishment_id, ref.horizon_id,
        source_testimony_ref, component_ref, subject_ref, visible_refs, tuple(preserved),
        tuple(c.clause_ref for c in preserved if c.ownership_basis == "unowned"),
    )


def inquiry_frontier_boundary_testimony_json(testimony: InquiryFrontierBoundaryTestimony) -> dict[str, object]:
    return testimony.to_json_dict()
