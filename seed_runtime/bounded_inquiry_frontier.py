"""Read-only implementation-local inquiry-frontier compatibility assessment.

The assembler consumes one exact selected inquiry need plus preserved
implementation-defined boundary testimony. It reports the current realization's
local coherence result. Clause families, required-family coverage, territory
references, and derived warrant labels in this module are compatibility
vocabulary, not canonical Book grammar or proof that the named constitutional
subjects exist. The assembler does not formulate a question, open inquiry,
authorize, execute, record, write the event ledger, or mutate state.
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

# Legacy diagnostic vocabulary retained for compatibility only. These values do
# not represent an independently produced constitutional warrant standing.
EligibleEvidenceTerritoryWarrantStanding = Literal[
    "not_supplied",
    "insufficient",
    "unknown",
    "conflicting",
    "sufficient",
]

FrontierState = Literal[
    "established",
    "missing_required_clause_family",
    "material_binding_conflict",
    "not_selected_inquiry_need",
]

# Implementation-local completeness inventory retained for public compatibility.
# It is not a canonical constitutional family inventory.
REQUIRED_CLAUSE_FAMILIES: tuple[ClauseFamily, ...] = (
    "included_excluded_inquiry_scope",
    "eligible_ineligible_evidence_territory",
    "sufficient_resolution_conditions",
    "lawful_stopping_conditions",
)

BOUNDARY_NOTES: tuple[str, ...] = (
    "BoundedInquiryFrontier reports compatibility coherence over already-preserved implementation-defined clauses for one exact selected inquiry need.",
    "Its established state is implementation-local compatibility standing, not proof of a canonical frontier, fixed family inventory, evidence territory, or constitutional inquiry opening.",
    "Opaque territory references and derived territory-warrant buckets are legacy diagnostic testimony and do not establish eligibility, admission, source selection, or constitutional warrant standing.",
    "Frontier compatibility established is not inquiry executed and not result known.",
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
    eligible_territory_warrant_not_supplied_clause_refs: tuple[str, ...]
    eligible_territory_warrant_insufficient_clause_refs: tuple[str, ...]
    eligible_territory_warrant_unknown_clause_refs: tuple[str, ...]
    eligible_territory_warrant_conflicting_clause_refs: tuple[str, ...]
    eligible_territory_warrant_sufficient_clause_refs: tuple[str, ...]
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
    constitutional_frontier_standing: Literal["unknown"] = "unknown"
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + sha256(encoded).hexdigest()


def _eligible_territory_warrant_standing(
    clause: InquiryFrontierBoundaryClause,
) -> EligibleEvidenceTerritoryWarrantStanding:
    """Return a legacy diagnostic classification, not constitutional standing."""
    if clause.clause_family != "eligible_ineligible_evidence_territory":
        raise ValueError("legacy territory diagnostic applies only to its compatibility family")
    if (
        clause.clause_standing == "conflicting"
        or clause.evidence_currency == "conflicting"
        or clause.evidence_availability == "conflicting"
    ):
        return "conflicting"
    if (
        clause.clause_standing == "unknown"
        or clause.evidence_currency == "unknown"
        or clause.evidence_availability == "unknown"
    ):
        return "unknown"
    if not clause.eligible_evidence_territory_refs:
        return "not_supplied"
    # The implementation preserves an opaque reference plus neighboring
    # coordinates but has no independent producer for the claim that the named
    # constitutional subject exists or is warranted. Keep this legacy bucket
    # non-positive and constitutionally Unknown.
    return "insufficient"


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
        return False
    return True


def assemble_bounded_inquiry_frontier(
    selected_need: AdvancementNeedConsiderationSelection,
    testimony: InquiryFrontierBoundaryTestimony,
) -> BoundedInquiryFrontier:
    """Report implementation-local compatibility coherence read-only."""
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
    material_conflicts = tuple(
        dict.fromkeys(
            (*(("identity:selection-testimony",) if identity_conflict else ()), *explicit_conflicts)
        )
    )

    if selected_need.selection_state != "selected" or ref is None or ref.family != "inquiry":
        state: FrontierState = "not_selected_inquiry_need"
    elif material_conflicts:
        state = "material_binding_conflict"
    elif missing:
        state = "missing_required_clause_family"
    else:
        state = "established"

    non_operative = tuple(c.clause_ref for c in clauses if c not in operative)
    eligible_warrant_standings = {
        c.clause_ref: _eligible_territory_warrant_standing(c)
        for c in clauses
        if c.clause_family == "eligible_ineligible_evidence_territory"
    }
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
        tuple(ref for ref, standing in eligible_warrant_standings.items() if standing == "not_supplied"),
        tuple(ref for ref, standing in eligible_warrant_standings.items() if standing == "insufficient"),
        tuple(ref for ref, standing in eligible_warrant_standings.items() if standing == "unknown"),
        tuple(ref for ref, standing in eligible_warrant_standings.items() if standing == "conflicting"),
        tuple(ref for ref, standing in eligible_warrant_standings.items() if standing == "sufficient"),
        clauses,
    )


def bounded_inquiry_frontier_json(frontier: BoundedInquiryFrontier) -> dict[str, object]:
    return frontier.to_json_dict()
