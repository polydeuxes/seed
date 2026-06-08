"""Fixture-level self-model alignment records and deterministic rules.

This module intentionally does not inspect the repository, parse documentation,
project state, or integrate with runtime execution. It only reconciles supplied
fixture records.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Sequence


SUPPORTED = "supported"
MISSING_SUPPORT = "missing_support"
POTENTIAL_CONFLICT = "potential_conflict"
NOT_EVALUABLE = "not_evaluable"

OWNERSHIP = "ownership"
REJECTED_CONCEPT = "rejected_concept"
FRONTIER = "frontier"

_PROJECTION_STORE_SYMBOLS = frozenset(
    {"ProjectionStore", "SQLiteProjectionStore", "InMemoryProjectionStore"}
)
_TOOL_EXECUTOR_SYMBOLS = frozenset({"ToolExecutor"})


@dataclass(frozen=True)
class DocumentationClaim:
    claim: str
    claim_family: str
    source_path: str
    source_heading: str | None = None


@dataclass(frozen=True)
class RepositoryArtifactFact:
    fact: str
    artifact_kind: str
    path: str
    symbol: str | None = None


@dataclass(frozen=True)
class AlignmentRecord:
    claim: DocumentationClaim
    artifact_facts: tuple[RepositoryArtifactFact, ...]
    outcome: str
    rule_id: str
    reason: str


def reconcile_claims(
    claims: Sequence[DocumentationClaim],
    artifact_facts: Sequence[RepositoryArtifactFact],
) -> list[AlignmentRecord]:
    """Reconcile supplied fixture claims against supplied fixture artifact facts.

    The helper applies only tiny, explicit rules for ownership, rejected concept,
    and frontier claims. Unknown claim families and unsupported text patterns are
    returned as ``not_evaluable``.
    """

    artifact_fact_tuple = tuple(artifact_facts)
    return [
        _reconcile_claim(claim, artifact_fact_tuple)
        for claim in claims
    ]


def _reconcile_claim(
    claim: DocumentationClaim,
    artifact_facts: tuple[RepositoryArtifactFact, ...],
) -> AlignmentRecord:
    if claim.claim_family == OWNERSHIP:
        return _reconcile_ownership_claim(claim, artifact_facts)
    if claim.claim_family == REJECTED_CONCEPT:
        return _reconcile_rejected_concept_claim(claim, artifact_facts)
    if claim.claim_family == FRONTIER:
        return _reconcile_frontier_claim(claim, artifact_facts)
    return AlignmentRecord(
        claim=claim,
        artifact_facts=(),
        outcome=NOT_EVALUABLE,
        rule_id="claim_family.not_evaluable",
        reason=f"Claim family {claim.claim_family!r} is not supported by v0 rules.",
    )


def _reconcile_ownership_claim(
    claim: DocumentationClaim,
    artifact_facts: tuple[RepositoryArtifactFact, ...],
) -> AlignmentRecord:
    if "ProjectionStore" in claim.claim:
        matches = _artifact_facts_matching_symbols(
            artifact_facts, _PROJECTION_STORE_SYMBOLS
        )
        if matches:
            return AlignmentRecord(
                claim=claim,
                artifact_facts=matches,
                outcome=SUPPORTED,
                rule_id="ownership.projection_store.supported",
                reason="A ProjectionStore artifact fact supports the ownership claim.",
            )
        return AlignmentRecord(
            claim=claim,
            artifact_facts=(),
            outcome=MISSING_SUPPORT,
            rule_id="ownership.projection_store.missing_support",
            reason="No ProjectionStore artifact fact supports the ownership claim.",
        )

    if "ToolExecutor" in claim.claim:
        matches = _artifact_facts_matching_symbols(artifact_facts, _TOOL_EXECUTOR_SYMBOLS)
        if matches:
            return AlignmentRecord(
                claim=claim,
                artifact_facts=matches,
                outcome=SUPPORTED,
                rule_id="ownership.tool_executor.supported",
                reason="A ToolExecutor artifact fact supports the ownership claim.",
            )
        return AlignmentRecord(
            claim=claim,
            artifact_facts=(),
            outcome=MISSING_SUPPORT,
            rule_id="ownership.tool_executor.missing_support",
            reason="No ToolExecutor artifact fact supports the ownership claim.",
        )

    return AlignmentRecord(
        claim=claim,
        artifact_facts=(),
        outcome=NOT_EVALUABLE,
        rule_id="ownership.not_evaluable",
        reason="Ownership claim does not match a v0 ownership rule.",
    )


def _reconcile_rejected_concept_claim(
    claim: DocumentationClaim,
    artifact_facts: tuple[RepositoryArtifactFact, ...],
) -> AlignmentRecord:
    rejected_concept = _rejected_concept(claim.claim)
    if rejected_concept is None:
        return AlignmentRecord(
            claim=claim,
            artifact_facts=(),
            outcome=NOT_EVALUABLE,
            rule_id="rejected_concept.not_evaluable",
            reason="Rejected concept claim does not match the v0 text pattern.",
        )

    matches = tuple(
        artifact_fact
        for artifact_fact in artifact_facts
        if _artifact_fact_contains(artifact_fact, rejected_concept)
    )
    if matches:
        return AlignmentRecord(
            claim=claim,
            artifact_facts=matches,
            outcome=POTENTIAL_CONFLICT,
            rule_id="rejected_concept.potential_conflict",
            reason=f"Artifact facts mention rejected concept {rejected_concept!r}.",
        )
    return AlignmentRecord(
        claim=claim,
        artifact_facts=(),
        outcome=SUPPORTED,
        rule_id="rejected_concept.supported",
        reason=f"No artifact facts mention rejected concept {rejected_concept!r}.",
    )


def _reconcile_frontier_claim(
    claim: DocumentationClaim,
    artifact_facts: tuple[RepositoryArtifactFact, ...],
) -> AlignmentRecord:
    frontier_name = _frontier_observation_name(claim.claim)
    if frontier_name is None:
        return AlignmentRecord(
            claim=claim,
            artifact_facts=(),
            outcome=NOT_EVALUABLE,
            rule_id="frontier.not_evaluable",
            reason="Frontier claim does not match a v0 observation text pattern.",
        )

    matches = tuple(
        artifact_fact
        for artifact_fact in artifact_facts
        if _artifact_fact_contains_any(
            artifact_fact, _frontier_artifact_needles(frontier_name)
        )
    )
    if matches:
        return AlignmentRecord(
            claim=claim,
            artifact_facts=matches,
            outcome=POTENTIAL_CONFLICT,
            rule_id="frontier.potential_conflict",
            reason=f"Artifact facts mention frontier observation {frontier_name!r}.",
        )
    return AlignmentRecord(
        claim=claim,
        artifact_facts=(),
        outcome=SUPPORTED,
        rule_id="frontier.supported",
        reason=f"No artifact facts mention frontier observation {frontier_name!r}.",
    )


def _artifact_facts_matching_symbols(
    artifact_facts: tuple[RepositoryArtifactFact, ...], symbols: frozenset[str]
) -> tuple[RepositoryArtifactFact, ...]:
    return tuple(
        artifact_fact
        for artifact_fact in artifact_facts
        if any(_artifact_fact_contains(artifact_fact, symbol) for symbol in symbols)
    )


def _artifact_fact_contains_any(
    artifact_fact: RepositoryArtifactFact, needles: tuple[str, ...]
) -> bool:
    return any(_artifact_fact_contains(artifact_fact, needle) for needle in needles)


def _artifact_fact_contains(artifact_fact: RepositoryArtifactFact, needle: str) -> bool:
    values = (artifact_fact.symbol, artifact_fact.fact, artifact_fact.path)
    return any(value is not None and needle in value for value in values)


def _rejected_concept(claim_text: str) -> str | None:
    match = re.fullmatch(r"\s*(?P<concept>.+?)\s+is rejected\.?\s*", claim_text)
    if match is None:
        return None
    return match.group("concept")


def _frontier_observation_name(claim_text: str) -> str | None:
    match = re.fullmatch(
        r"\s*(?P<name>.+? Observation)\s+is a current "
        r"(?:frontier|capability-growth priority)\.?\s*",
        claim_text,
    )
    if match is None:
        return None
    return match.group("name")


def _frontier_artifact_needles(frontier_name: str) -> tuple[str, ...]:
    compact_name = frontier_name.replace(" ", "")
    snake_name = re.sub(r"(?<!^)(?=[A-Z])", "_", compact_name).lower()
    return (frontier_name, compact_name, snake_name)
