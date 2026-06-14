"""Read-only capability-candidate observation from projected evidence.

This module preserves evidence-derived capability candidates only. A candidate is
not a capability, execution authority, an execution decision, policy evaluation,
or tool invocation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from seed_runtime.evidence_graph import build_fact_evidence_view
from seed_runtime.facts import Fact
from seed_runtime.state import State

CapabilityCandidateConfidence = Literal["supported_by_observed_package"]

_PACKAGE_CAPABILITY_CANDIDATES: dict[str, tuple[str, ...]] = {
    "openssh-client": ("ssh_client",),
    "python3": ("python_runtime",),
    "python": ("python_runtime",),
    "docker.io": ("docker_client",),
    "docker-ce-cli": ("docker_client",),
    "docker-ce": ("docker_client",),
    "git": ("git_client",),
    "curl": ("http_client",),
}

_BOUNDARY_NOTES = (
    "capability_candidate_not_capability",
    "capability_candidate_not_execution_authority",
    "capability_candidate_not_execution_decision",
    "capability_candidate_not_tool_invocation",
    "observed_evidence_not_capability_proof",
    "capability_presence_not_capability_permission",
    "no_capability_selection",
    "no_policy_evaluation",
    "no_tool_execution",
    "read_only_inspection",
)


@dataclass(frozen=True)
class CapabilityCandidateEvidence:
    """Evidence/fact support for one capability candidate."""

    fact_id: str
    predicate: str
    subject_id: str
    value: str
    source_type: str
    confidence: float
    evidence_ids: list[str] = field(default_factory=list)
    evidence_summaries: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CapabilityCandidate:
    """A possible capability preserved from observable evidence."""

    candidate: str
    confidence: CapabilityCandidateConfidence
    rationale: str
    supporting_evidence: list[CapabilityCandidateEvidence] = field(default_factory=list)
    boundary: str = "capability_candidate_preservation_only"
    notes: list[str] = field(default_factory=lambda: list(_BOUNDARY_NOTES))


@dataclass(frozen=True)
class CapabilityCandidateInspection:
    """Read-only inspection result for evidence-derived capability candidates."""

    candidates: list[CapabilityCandidate] = field(default_factory=list)
    filter: str | None = None
    boundary: str = "capability_candidate_preservation_only"
    notes: list[str] = field(default_factory=lambda: list(_BOUNDARY_NOTES))


def build_capability_candidates(
    state: State, *, filter_text: str | None = None
) -> CapabilityCandidateInspection:
    """Build capability candidates from projected State without side effects."""

    wanted = _normalize_filter(filter_text)
    support_by_candidate: dict[str, list[CapabilityCandidateEvidence]] = {}
    for fact in state.facts.values():
        if fact.predicate != "package_installed":
            continue
        package_name = str(fact.value).strip().lower()
        for candidate in _PACKAGE_CAPABILITY_CANDIDATES.get(package_name, ()):
            if wanted and wanted not in {candidate, package_name}:
                continue
            support_by_candidate.setdefault(candidate, []).append(
                _candidate_evidence(state, fact)
            )

    candidates = [
        CapabilityCandidate(
            candidate=candidate,
            confidence="supported_by_observed_package",
            rationale=(
                "projected package_installed evidence names package(s) associated "
                "with this capability candidate; this is not capability proof, "
                "permission, selection, planning, or execution"
            ),
            supporting_evidence=sorted(
                evidence, key=lambda item: (item.value, item.fact_id)
            ),
        )
        for candidate, evidence in sorted(support_by_candidate.items())
    ]
    return CapabilityCandidateInspection(candidates=candidates, filter=filter_text)


def _candidate_evidence(state: State, fact: Fact) -> CapabilityCandidateEvidence:
    summaries: list[str] = []
    view = build_fact_evidence_view(state, fact.id)
    if view is not None:
        summaries = [node.summary for node in view.evidence]
    return CapabilityCandidateEvidence(
        fact_id=fact.id,
        predicate=fact.predicate,
        subject_id=fact.subject_id,
        value=str(fact.value),
        source_type=fact.source_type,
        confidence=fact.confidence,
        evidence_ids=list(fact.evidence_ids),
        evidence_summaries=summaries,
    )


def _normalize_filter(filter_text: str | None) -> str | None:
    if filter_text is None:
        return None
    normalized = filter_text.strip().lower().replace("-", "_")
    aliases = {
        "ssh": "ssh_client",
        "python": "python_runtime",
        "docker": "docker_client",
        "git": "git_client",
        "curl": "http_client",
    }
    return aliases.get(normalized, normalized)
