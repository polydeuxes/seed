"""Caller-supplied candidate external grammar preservation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

BOUNDARY_NOTES: tuple[str, ...] = (
    "Candidate grammars are caller-supplied structural hypotheses.",
    "Supporting and contradicting testimony relationships are preserved, not evaluated.",
    "No candidate is selected, verified, promoted, or treated as semantic truth.",
    "Absence of support is not contradiction.",
    "Absence of contradiction is not verification.",
    "This artifact does not establish translator readiness or capability.",
)


class CandidateExternalGrammarValidationError(ValueError):
    """Structural validation failure for caller-supplied candidate grammar input."""


@dataclass(frozen=True)
class CandidateExternalGrammarInputCandidate:
    candidate_id: str
    structural_claim: str
    claim_scope: str = ""
    provenance: tuple[str, ...] = ()
    supporting_testimony: tuple[str, ...] = ()
    contradicting_testimony: tuple[str, ...] = ()
    unresolved_alternatives: tuple[str, ...] = ()
    explicit_unknowns: tuple[str, ...] = ()

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "CandidateExternalGrammarInputCandidate":
        return cls(
            candidate_id=_required_str(data, "candidate_id"),
            structural_claim=_required_str(data, "structural_claim"),
            claim_scope=_optional_str(data, "claim_scope"),
            provenance=_str_tuple(data.get("provenance", ()), "provenance"),
            supporting_testimony=_str_tuple(data.get("supporting_testimony", ()), "supporting_testimony"),
            contradicting_testimony=_str_tuple(data.get("contradicting_testimony", ()), "contradicting_testimony"),
            unresolved_alternatives=_str_tuple(data.get("unresolved_alternatives", ()), "unresolved_alternatives"),
            explicit_unknowns=_str_tuple(data.get("explicit_unknowns", ()), "explicit_unknowns"),
        )

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        for key, value in data.items():
            if isinstance(value, tuple):
                data[key] = list(value)
        return data


@dataclass(frozen=True)
class CandidateExternalGrammarInput:
    representation_scope: str
    candidates: tuple[CandidateExternalGrammarInputCandidate, ...] = ()
    set_unknowns: tuple[str, ...] = ()

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "CandidateExternalGrammarInput":
        raw_candidates = data.get("candidates", ())
        if not isinstance(raw_candidates, list):
            raise CandidateExternalGrammarValidationError("candidates must be a list")
        return cls(
            representation_scope=_required_str(data, "representation_scope"),
            candidates=tuple(
                CandidateExternalGrammarInputCandidate.from_json_dict(candidate)
                for candidate in raw_candidates
            ),
            set_unknowns=_str_tuple(data.get("set_unknowns", ()), "set_unknowns"),
        )


@dataclass(frozen=True)
class CandidateExternalGrammarSet:
    representation_scope: str
    candidates: tuple[CandidateExternalGrammarInputCandidate, ...]
    set_unknowns: tuple[str, ...]
    boundary_notes: tuple[str, ...]
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False

    def to_json_dict(self) -> dict[str, object]:
        return {
            "artifact_type": "CandidateExternalGrammarSet",
            "representation_scope": self.representation_scope,
            "candidates": [candidate.to_json_dict() for candidate in self.candidates],
            "set_unknowns": list(self.set_unknowns),
            "boundary_notes": list(self.boundary_notes),
            "read_only": self.read_only,
            "writes_event_ledger": self.writes_event_ledger,
            "mutates_cluster": self.mutates_cluster,
        }


def assemble_candidate_external_grammar_set(
    supplied: CandidateExternalGrammarInput,
) -> CandidateExternalGrammarSet:
    seen: set[str] = set()
    for candidate in supplied.candidates:
        if not candidate.candidate_id:
            raise CandidateExternalGrammarValidationError("candidate_id is required")
        if candidate.candidate_id in seen:
            raise CandidateExternalGrammarValidationError(
                f"duplicate candidate_id: {candidate.candidate_id}"
            )
        seen.add(candidate.candidate_id)
    return CandidateExternalGrammarSet(
        representation_scope=supplied.representation_scope,
        candidates=supplied.candidates,
        set_unknowns=supplied.set_unknowns,
        boundary_notes=BOUNDARY_NOTES,
    )


def candidate_external_grammar_json(
    artifact: CandidateExternalGrammarSet,
) -> dict[str, object]:
    return artifact.to_json_dict()


def format_candidate_external_grammar(artifact: CandidateExternalGrammarSet) -> str:
    lines = [
        "Candidate External Grammar Set",
        f"representation_scope: {artifact.representation_scope}",
        f"read_only: {str(artifact.read_only).lower()}",
        f"writes_event_ledger: {str(artifact.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(artifact.mutates_cluster).lower()}",
        "boundary_notes:",
    ]
    lines.extend(f"- {note}" for note in artifact.boundary_notes)
    lines.append("set_unknowns:")
    lines.extend(f"- {unknown}" for unknown in artifact.set_unknowns)
    if not artifact.set_unknowns:
        lines.append("- none supplied")
    lines.append("candidates:")
    if not artifact.candidates:
        lines.append("- none supplied (zero-candidate set, not failure)")
    for candidate in artifact.candidates:
        lines.extend(
            [
                f"- candidate_id: {candidate.candidate_id}",
                f"  structural_claim: {candidate.structural_claim}",
                f"  claim_scope: {candidate.claim_scope}",
                f"  provenance: {_joined(candidate.provenance)}",
                f"  supporting_testimony: {_joined(candidate.supporting_testimony)}",
                f"  contradicting_testimony: {_joined(candidate.contradicting_testimony)}",
                f"  unresolved_alternatives: {_joined(candidate.unresolved_alternatives)}",
                f"  explicit_unknowns: {_joined(candidate.explicit_unknowns)}",
            ]
        )
    return "\n".join(lines)


def _joined(values: tuple[str, ...]) -> str:
    return ", ".join(values) if values else "none supplied"


def _required_str(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise CandidateExternalGrammarValidationError(f"{key} is required")
    return value


def _optional_str(data: dict[str, Any], key: str) -> str:
    value = data.get(key, "")
    if not isinstance(value, str):
        raise CandidateExternalGrammarValidationError(f"{key} must be a string")
    return value


def _str_tuple(value: Any, key: str) -> tuple[str, ...]:
    if not isinstance(value, list | tuple):
        raise CandidateExternalGrammarValidationError(f"{key} must be a list")
    if not all(isinstance(item, str) for item in value):
        raise CandidateExternalGrammarValidationError(f"{key} entries must be strings")
    return tuple(value)
