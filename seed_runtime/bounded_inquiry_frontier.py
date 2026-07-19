"""Read-only bounded inquiry frontier assembly.

The assembler consumes one exact selected inquiry need plus its preserved
frontier-boundary testimony. It only determines whether the already supplied
boundary clauses coherently establish a bounded inquiry frontier; it does not
invent scope, admit evidence, formulate a question, open inquiry, authorize,
execute, record, write the event ledger, or mutate state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Literal

from seed_runtime.advancement_need_consideration_selection import AdvancementNeedConsiderationSelection
from seed_runtime.inquiry_frontier_boundary_testimony import (
    ClauseFamily,
    InquiryFrontierBoundaryClause,
    InquiryFrontierBoundaryTestimony,
)

FrontierState = Literal[
    "established",
    "missing_required_clause_family",
    "material_binding_conflict",
    "not_selected_inquiry_need",
]

REQUIRED_CLAUSE_FAMILIES: tuple[ClauseFamily, ...] = (
    "included_excluded_inquiry_scope",
    "eligible_ineligible_evidence_territory",
    "sufficient_resolution_conditions",
    "lawful_stopping_conditions",
)

BOUNDARY_NOTES: tuple[str, ...] = (
    "BoundedInquiryFrontier assembles only from already-preserved boundary testimony for one exact selected inquiry need.",
    "Frontier establishment requires included inquiry scope, eligible evidence territory, sufficient-resolution condition, lawful stopping condition, and no material binding conflict.",
    "Eligible evidence territory is not source selection or observation selection.",
    "Frontier established is not inquiry executed and not result known.",
)


@dataclass(frozen=True)
class BoundedInquiryFrontier:
    frontier_id: str
    frontier_state: FrontierState
    selected_need_selection_id: str
    selected_need_reference_id: str | None
    native_projection_id: str | None
    native_lineage: tuple[str, ...]
    need_set_id: str
    selected_goal_id: str
    horizon_id: str
    testimony_id: str
    source_testimony_ref: str | None
    bounded_uncertainty_component_ref: str | None
    repository_world_subject_ref: str | None
    operative_clause_refs: tuple[str, ...]
    preserved_clause_refs: tuple[str, ...]
    missing_required_clause_families: tuple[ClauseFamily, ...]
    material_conflict_clause_refs: tuple[str, ...]
    non_operative_clause_refs: tuple[str, ...]
    unsupported_clause_refs: tuple[str, ...]
    unknown_clause_refs: tuple[str, ...]
    conflicting_clause_refs: tuple[str, ...]
    mixed_clause_refs: tuple[str, ...]
    adjacent_family_clause_refs: tuple[str, ...]
    stale_clause_refs: tuple[str, ...]
    unknown_currency_clause_refs: tuple[str, ...]
    unavailable_clause_refs: tuple[str, ...]
    unknown_availability_clause_refs: tuple[str, ...]
    out_of_scope_clause_refs: tuple[str, ...]
    clauses: tuple[InquiryFrontierBoundaryClause, ...]
    read_only: bool = True
    invents_scope: bool = False
    invents_evidence_admission: bool = False
    formulates_question: bool = False
    opens_inquiry: bool = False
    selects_sources: bool = False
    selects_observations: bool = False
    authorizes_access: bool = False
    starts_execution: bool = False
    starts_recording: bool = False
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    result_known: bool = False
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + sha256(encoded).hexdigest()


def _is_operatively_coherent(clause: InquiryFrontierBoundaryClause) -> bool:
    if clause.clause_standing != "established":
        return False
    if clause.family_disposition != "inquiry":
        return False
    if clause.evidence_currency == "conflicting":
        return False
    if clause.evidence_availability == "conflicting":
        return False
    if clause.clause_family == "included_excluded_inquiry_scope":
        return clause.scope_disposition == "included"
    if clause.clause_family == "eligible_ineligible_evidence_territory":
        if clause.evidence_currency != "current":
            return False
        if clause.evidence_availability != "available":
            return False
        # No repository-local witness currently establishes claim-relative
        # territory eligibility for the selected need, frontier boundary, and
        # reliance purpose. Preserve supplied refs and the presently insufficient
        # standing, but do not count tuple non-emptiness as positive
        # required-family support or as proof that future warrant is impossible.
        return False
    return True


def assemble_bounded_inquiry_frontier(
    selected_need: AdvancementNeedConsiderationSelection,
    testimony: InquiryFrontierBoundaryTestimony,
) -> BoundedInquiryFrontier:
    """Assemble a read-only frontier only from coherent required testimony."""
    clauses = testimony.clauses
    preserved_refs = tuple(c.clause_ref for c in clauses)
    identity_conflict = selected_need.selection_state != "selected" or selected_need.selected_reference is None
    ref = selected_need.selected_reference
    if ref is not None:
        identity_conflict = identity_conflict or any(
            (
                testimony.selected_need_reference_id != ref.reference_id,
                testimony.native_projection_id != ref.native_projection_id,
                testimony.native_lineage != ref.native_lineage,
                testimony.need_set_id != ref.need_set_id,
                testimony.selected_need_selection_id != ref.selection_id,
                testimony.selected_need_goal_id != ref.goal_establishment_id,
                testimony.horizon_id != ref.horizon_id,
            )
        )

    operative = tuple(c for c in clauses if _is_operatively_coherent(c))
    operative_families = {c.clause_family for c in operative}
    missing = tuple(f for f in REQUIRED_CLAUSE_FAMILIES if f not in operative_families)
    explicit_conflicts = tuple(
        c.clause_ref
        for c in clauses
        if c.clause_standing == "conflicting"
        or c.scope_disposition == "conflicting"
        or c.evidence_currency == "conflicting"
        or c.evidence_availability == "conflicting"
    )
    material_conflicts = tuple(dict.fromkeys((*(('identity:selection-testimony',) if identity_conflict else ()), *explicit_conflicts)))

    if selected_need.selection_state != "selected" or ref is None or ref.family != "inquiry":
        state: FrontierState = "not_selected_inquiry_need"
    elif material_conflicts:
        state = "material_binding_conflict"
    elif missing:
        state = "missing_required_clause_family"
    else:
        state = "established"

    non_operative = tuple(c.clause_ref for c in clauses if c not in operative)
    payload = {
        "selection": selected_need.selection_id,
        "testimony": testimony.testimony_id,
        "state": state,
        "operative": tuple(c.clause_ref for c in operative),
        "missing": missing,
        "conflicts": material_conflicts,
    }
    return BoundedInquiryFrontier(
        _stable("bounded-inquiry-frontier", payload),
        state,
        selected_need.selection_id,
        testimony.selected_need_reference_id,
        testimony.native_projection_id,
        testimony.native_lineage,
        testimony.need_set_id,
        testimony.selected_need_goal_id,
        testimony.horizon_id,
        testimony.testimony_id,
        testimony.source_testimony_ref,
        testimony.bounded_uncertainty_component_ref,
        testimony.repository_world_subject_ref,
        tuple(c.clause_ref for c in operative),
        preserved_refs,
        missing,
        material_conflicts,
        non_operative,
        tuple(c.clause_ref for c in clauses if c.clause_standing == "unsupported"),
        tuple(c.clause_ref for c in clauses if c.clause_standing == "unknown"),
        tuple(c.clause_ref for c in clauses if c.clause_standing == "conflicting"),
        tuple(c.clause_ref for c in clauses if c.family_disposition == "mixed"),
        tuple(c.clause_ref for c in clauses if c.family_disposition == "adjacent_family"),
        tuple(c.clause_ref for c in clauses if c.evidence_currency == "stale"),
        tuple(c.clause_ref for c in clauses if c.evidence_currency == "unknown"),
        tuple(c.clause_ref for c in clauses if c.evidence_availability == "unavailable"),
        tuple(c.clause_ref for c in clauses if c.evidence_availability == "unknown"),
        tuple(c.clause_ref for c in clauses if c.scope_disposition == "outside_current_scope"),
        clauses,
    )


def bounded_inquiry_frontier_json(frontier: BoundedInquiryFrontier) -> dict[str, object]:
    return frontier.to_json_dict()
