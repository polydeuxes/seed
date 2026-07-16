"""Read-only contextual interpretation selection from explicit candidate-bound evidence."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

from seed_runtime.contextual_interpretation_warrant_set import (
    CandidateWarrant,
    ContextualInterpretationWarrantSet,
    ExactOperatorMaterial,
)

CONVENTION = "contextual_interpretation_selection_result_v1"
SELECTION_EVIDENCE_KINDS = {"exact_operator_clarification", "candidate_bound_selection_artifact"}
BOUNDARY_NOTES = (
    "Warranted is not selected.",
    "Selected interpretation is not downstream applicability.",
    "Selected interpretation is not downstream admission.",
    "Operator clarification may select meaning without rewriting the original source.",
    "Downstream inability to consume an interpretation must not erase or refuse the selected meaning.",
    "A unique warranted candidate is not an automatic selection.",
    "This producer stops before downstream applicability, goal binding, inquiry movement, authorization, execution, recording, conversation mutation, state mutation, or cluster mutation.",
)


class ContextualInterpretationSelectionError(ValueError):
    pass


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class CandidateSelectionEvidence:
    evidence_ref: str
    candidate_ref: str
    evidence_kind: str
    exact_text: str
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.evidence_ref or not self.candidate_ref:
            raise ContextualInterpretationSelectionError("selection evidence requires evidence_ref and candidate_ref")
        if self.evidence_kind not in SELECTION_EVIDENCE_KINDS:
            raise ContextualInterpretationSelectionError(
                f"selection evidence kind must be one of {sorted(SELECTION_EVIDENCE_KINDS)}"
            )


@dataclass(frozen=True)
class ContextualInterpretationSelectionResult:
    artifact_type: str
    selection_result_id: str
    warrant_set_id: str
    operator_material: ExactOperatorMaterial
    selection_evidence: tuple[CandidateSelectionEvidence, ...]
    selected_candidate_ref: str | None
    selected_candidate: CandidateWarrant | None
    non_selected_candidates: tuple[CandidateWarrant, ...]
    candidate_warrants: tuple[CandidateWarrant, ...]
    proposed_corrections: tuple[object, ...]
    residual_source_material: tuple[object, ...]
    unknowns: tuple[str, ...]
    conflicts: tuple[str, ...]
    selection_provenance: tuple[str, ...]
    outcome: str
    interpretation_selected: bool
    downstream_applicability: None = None
    downstream_admission: None = None
    goal_bound: bool = False
    inquiry_moved: bool = False
    authorized: bool = False
    executed: bool = False
    recorded: bool = False
    mutates_conversation: bool = False
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_state: bool = False
    mutates_cluster: bool = False
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES
    convention: str = CONVENTION

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def select_contextual_interpretation(
    warrant_set: ContextualInterpretationWarrantSet,
    *,
    selection_evidence: tuple[CandidateSelectionEvidence, ...] = (),
) -> ContextualInterpretationSelectionResult:
    """Select exactly one warranted candidate only from explicit candidate-bound selection evidence."""
    warrants_by_ref = {w.candidate_ref: w for w in warrant_set.candidate_warrants}
    unknowns = sorted({u for w in warrant_set.candidate_warrants for u in w.unknowns})
    conflicts = sorted({c for w in warrant_set.candidate_warrants for c in w.conflicts})
    proposed_corrections = tuple(c for w in warrant_set.candidate_warrants for c in w.proposed_corrections)
    residual_source_material = tuple(
        {span.span_ref: span for w in warrant_set.candidate_warrants for span in w.residual_source_material}.values()
    )
    provenance = tuple(p for evidence in selection_evidence for p in ((evidence.evidence_ref,) + evidence.provenance))

    selected_ref: str | None = None
    selected: CandidateWarrant | None = None
    outcome = "no_selection_evidence"
    result_conflicts = list(conflicts)

    evidence_candidate_refs = tuple(e.candidate_ref for e in selection_evidence)
    distinct_evidence_refs = tuple(sorted(set(evidence_candidate_refs)))
    if selection_evidence:
        unknown_refs = [ref for ref in distinct_evidence_refs if ref not in warrants_by_ref]
        if unknown_refs:
            outcome = "selection_refused_unwarranted_candidate"
            result_conflicts.append("selection evidence references unknown or unwarranted candidate: " + ", ".join(unknown_refs))
        elif len(distinct_evidence_refs) > 1:
            outcome = "conflicting_selection_evidence"
            result_conflicts.append("selection evidence names multiple candidates: " + ", ".join(distinct_evidence_refs))
        else:
            candidate = warrants_by_ref[distinct_evidence_refs[0]]
            if candidate.warrant_standing != "warranted":
                outcome = "selection_refused_unwarranted_candidate"
                result_conflicts.append(
                    f"selection evidence names candidate {candidate.candidate_ref} with standing {candidate.warrant_standing}"
                )
            else:
                selected_ref = candidate.candidate_ref
                selected = candidate
                outcome = "selected"
    elif len([w for w in warrant_set.candidate_warrants if w.warrant_standing == "warranted"]) > 1:
        outcome = "multiple_warranted_candidates_without_selection_evidence"
    elif any(w.warrant_standing == "warranted" for w in warrant_set.candidate_warrants):
        outcome = "warranted_candidate_without_selection_evidence"

    non_selected = tuple(w for w in warrant_set.candidate_warrants if w.candidate_ref != selected_ref)
    payload = {
        "warrant_set_id": warrant_set.warrant_set_id,
        "evidence": [asdict(e) for e in selection_evidence],
        "selected": selected_ref,
        "outcome": outcome,
        "convention": CONVENTION,
    }
    return ContextualInterpretationSelectionResult(
        "ContextualInterpretationSelectionResult",
        _stable("contextual-interpretation-selection-result", payload),
        warrant_set.warrant_set_id,
        warrant_set.operator_material,
        selection_evidence,
        selected_ref,
        selected,
        non_selected,
        warrant_set.candidate_warrants,
        proposed_corrections,
        residual_source_material,
        tuple(unknowns),
        tuple(result_conflicts),
        provenance,
        outcome,
        selected is not None,
    )
