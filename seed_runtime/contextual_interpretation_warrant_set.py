"""Read-only candidate-scoped contextual interpretation warrant production."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Iterable

CONVENTION = "contextual_interpretation_warrant_set_v1"
WARRANT_STANDINGS = {"warranted", "unwarranted", "ambiguous", "conflicted", "unresolved"}
EVIDENCE_DISPOSITIONS = {"supporting", "contradicting", "irrelevant", "unresolved"}
BOUNDARY_NOTES = (
    "Conversation history is not the bounded retrospective corpus.",
    "Examined material is not automatically supporting evidence.",
    "Source material is preserved separately from corrected material.",
    "Correction candidates are not interpretation candidates.",
    "A candidate warrant is scoped only to its candidate and cannot support another candidate.",
    "Warrant standing is not interpretation selection.",
    "A unique warranted candidate is not a selected candidate.",
    "This producer stops before interpretation selection, goal binding, inquiry movement, authorization, execution, recording, or state mutation.",
)


class ContextualInterpretationWarrantSetError(ValueError):
    pass


def _refs(values: Iterable[str] = ()) -> tuple[str, ...]:
    return tuple(sorted({str(value) for value in values if value}))


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class SourceSpan:
    span_ref: str
    source_ref: str
    start: int
    end: int
    exact_text: str

    def __post_init__(self) -> None:
        if not self.span_ref or not self.source_ref:
            raise ContextualInterpretationWarrantSetError("source spans require span_ref and source_ref")
        if self.start < 0 or self.end < self.start:
            raise ContextualInterpretationWarrantSetError("source span offsets must be bounded and ordered")


@dataclass(frozen=True)
class ExactOperatorMaterial:
    material_ref: str
    exact_text: str
    source_spans: tuple[SourceSpan, ...]
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.material_ref:
            raise ContextualInterpretationWarrantSetError("operator material_ref is required")


@dataclass(frozen=True)
class InterpretationCandidate:
    candidate_ref: str
    label: str
    source_span_refs: tuple[str, ...]
    proposed_meaning: str = ""

    def __post_init__(self) -> None:
        if not self.candidate_ref:
            raise ContextualInterpretationWarrantSetError("interpretation candidate_ref is required")


@dataclass(frozen=True)
class CorrectionCandidate:
    correction_ref: str
    candidate_ref: str
    source_span_refs: tuple[str, ...]
    original_text: str
    corrected_text: str
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class RetrospectiveEvidence:
    evidence_ref: str
    candidate_ref: str
    disposition: str
    material_ref: str
    exact_text: str
    source_span_refs: tuple[str, ...] = ()
    rationale: str = ""

    def __post_init__(self) -> None:
        if self.disposition not in EVIDENCE_DISPOSITIONS:
            raise ContextualInterpretationWarrantSetError(
                f"retrospective evidence disposition must be one of {sorted(EVIDENCE_DISPOSITIONS)}"
            )
        if not self.evidence_ref or not self.candidate_ref or not self.material_ref:
            raise ContextualInterpretationWarrantSetError("retrospective evidence requires evidence_ref, candidate_ref, and material_ref")


@dataclass(frozen=True)
class ClarificationEvidence:
    clarification_ref: str
    candidate_ref: str
    exact_text: str
    disposition: str = "unresolved"


@dataclass(frozen=True)
class CandidateWarrant:
    candidate_ref: str
    label: str
    source_spans: tuple[SourceSpan, ...]
    proposed_corrections: tuple[CorrectionCandidate, ...]
    examined_retrospective_material: tuple[RetrospectiveEvidence, ...]
    supporting_evidence: tuple[RetrospectiveEvidence, ...]
    contradicting_evidence: tuple[RetrospectiveEvidence, ...]
    irrelevant_evidence: tuple[RetrospectiveEvidence, ...]
    unresolved_evidence: tuple[RetrospectiveEvidence, ...]
    clarification_evidence: tuple[ClarificationEvidence, ...]
    warrant_standing: str
    standing_reason: str
    unknowns: tuple[str, ...]
    conflicts: tuple[str, ...]
    residual_source_material: tuple[SourceSpan, ...]
    known_loss: tuple[str, ...]


@dataclass(frozen=True)
class ContextualInterpretationWarrantSet:
    artifact_type: str
    warrant_set_id: str
    operator_material: ExactOperatorMaterial
    candidate_warrants: tuple[CandidateWarrant, ...]
    closed_choice_selection_binding_ref: str | None = None
    selected_candidate_ref: None = None
    interpretation_selected: bool = False
    goal_bound: bool = False
    inquiry_moved: bool = False
    authorized: bool = False
    executed: bool = False
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_state: bool = False
    mutates_cluster: bool = False
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES
    convention: str = CONVENTION

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def produce_contextual_interpretation_warrant_set(
    *,
    operator_material: ExactOperatorMaterial,
    candidates: tuple[InterpretationCandidate, ...],
    corrections: tuple[CorrectionCandidate, ...] = (),
    retrospective_evidence: tuple[RetrospectiveEvidence, ...] = (),
    clarification_evidence: tuple[ClarificationEvidence, ...] = (),
    unknowns_by_candidate: dict[str, tuple[str, ...]] | None = None,
    conflicts_by_candidate: dict[str, tuple[str, ...]] | None = None,
    known_loss_by_candidate: dict[str, tuple[str, ...]] | None = None,
    closed_choice_selection_binding_ref: str | None = None,
) -> ContextualInterpretationWarrantSet:
    """Produce candidate-local warrants from explicit candidates and supplied evidence only."""
    candidate_refs = [candidate.candidate_ref for candidate in candidates]
    if len(candidate_refs) != len(set(candidate_refs)):
        raise ContextualInterpretationWarrantSetError("interpretation candidate refs must be unique")
    candidate_ref_set = set(candidate_refs)
    span_by_ref = {span.span_ref: span for span in operator_material.source_spans}

    def assert_candidate_ref(ref: str, kind: str) -> None:
        if ref not in candidate_ref_set:
            raise ContextualInterpretationWarrantSetError(f"{kind} references unknown interpretation candidate {ref!r}")

    for correction in corrections:
        assert_candidate_ref(correction.candidate_ref, "correction candidate")
    for evidence in retrospective_evidence:
        assert_candidate_ref(evidence.candidate_ref, "retrospective evidence")
    for clarification in clarification_evidence:
        assert_candidate_ref(clarification.candidate_ref, "clarification evidence")
        if clarification.disposition not in EVIDENCE_DISPOSITIONS:
            raise ContextualInterpretationWarrantSetError("clarification disposition must be an evidence disposition")

    unknowns_by_candidate = unknowns_by_candidate or {}
    conflicts_by_candidate = conflicts_by_candidate or {}
    known_loss_by_candidate = known_loss_by_candidate or {}
    warrants: list[CandidateWarrant] = []
    for candidate in candidates:
        candidate_spans = tuple(span_by_ref[ref] for ref in candidate.source_span_refs if ref in span_by_ref)
        candidate_corrections = tuple(c for c in corrections if c.candidate_ref == candidate.candidate_ref)
        examined = tuple(e for e in retrospective_evidence if e.candidate_ref == candidate.candidate_ref)
        by_disposition = {d: tuple(e for e in examined if e.disposition == d) for d in EVIDENCE_DISPOSITIONS}
        clarifications = tuple(c for c in clarification_evidence if c.candidate_ref == candidate.candidate_ref)
        unknowns = _refs(unknowns_by_candidate.get(candidate.candidate_ref, ()))
        conflicts = _refs(conflicts_by_candidate.get(candidate.candidate_ref, ()))
        if conflicts:
            standing, reason = "conflicted", "candidate has preserved conflicts"
        elif unknowns or by_disposition["unresolved"] or any(c.disposition == "unresolved" for c in clarifications):
            standing, reason = "unresolved", "candidate has unknown or unresolved evidence"
        elif by_disposition["supporting"] and not by_disposition["contradicting"]:
            standing, reason = "warranted", "candidate has supporting evidence and no contradiction"
        elif by_disposition["contradicting"] and not by_disposition["supporting"]:
            standing, reason = "unwarranted", "candidate has contradiction and no support"
        elif by_disposition["supporting"] and by_disposition["contradicting"]:
            standing, reason = "ambiguous", "candidate has both supporting and contradicting evidence"
        else:
            standing, reason = "unresolved", "candidate has no supplied supporting or contradicting evidence"
        residual = tuple(span for span in operator_material.source_spans if span.span_ref not in set(candidate.source_span_refs))
        warrants.append(CandidateWarrant(candidate.candidate_ref, candidate.label, candidate_spans, candidate_corrections, examined, by_disposition["supporting"], by_disposition["contradicting"], by_disposition["irrelevant"], by_disposition["unresolved"], clarifications, standing, reason, unknowns, conflicts, residual, _refs(known_loss_by_candidate.get(candidate.candidate_ref, ()))) )
    payload = {"operator_material": asdict(operator_material), "candidates": [asdict(w) for w in warrants], "binding": closed_choice_selection_binding_ref, "convention": CONVENTION}
    return ContextualInterpretationWarrantSet("ContextualInterpretationWarrantSet", _stable("contextual-interpretation-warrant-set", payload), operator_material, tuple(warrants), closed_choice_selection_binding_ref)
