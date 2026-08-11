"""Read-only confidence aggregation over projected State facts.

Confidence Aggregation is a deterministic projection view derived from already
projected State, the Evidence Graph, and Contradiction Detection. It estimates
support strength for facts but does not resolve truth, mutate State, append
events, execute runtime behavior, call providers, evaluate policy, execute
tools, or persist a separate confidence store.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterable

from seed_runtime.contradictions import Contradiction, build_contradictions
from seed_runtime.evidence_graph import (
    EvidenceGraph,
    FactEvidenceView,
    build_evidence_graph,
)
from seed_runtime.facts import DEFAULT_CONFIDENCE_BY_SOURCE_TYPE, Fact
from seed_runtime.state import State

STRONGLY_SUPPORTED_THRESHOLD = 0.75
CONTRADICTION_PENALTY = 0.75


@dataclass(frozen=True)
class FactConfidence:
    fact_id: str
    subject: str
    predicate: str
    object: Any
    confidence: float
    support_count: int
    contradiction_count: int
    unsupported: bool
    contradicted: bool
    reasons: list[str] = field(default_factory=list)
    supporting_event_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ConfidenceSummary:
    fact_count: int
    strongly_supported_count: int
    weakly_supported_count: int
    unsupported_count: int
    contradicted_count: int
    average_confidence: float
    last_event_id: str | None
    projection_version: str


def build_fact_confidences(
    state: State,
    evidence_graph: EvidenceGraph | None = None,
    contradictions: list[Contradiction] | None = None,
) -> list[FactConfidence]:
    """Build deterministic confidence records for all projected State facts."""

    graph = evidence_graph if evidence_graph is not None else build_evidence_graph(state)
    contradiction_items = (
        contradictions
        if contradictions is not None
        else build_contradictions(state, evidence_graph=graph)
    )
    evidence_by_fact_id = {view.fact_id: view for view in graph.fact_evidence}
    contradictions_by_fact_id = _contradictions_by_fact_id(contradiction_items)

    return [
        _fact_confidence(
            fact,
            evidence_by_fact_id.get(fact.id),
            contradictions_by_fact_id.get(fact.id, []),
        )
        for fact in _ordered_facts(state)
    ]


def build_fact_confidence(
    state: State,
    fact_id: str,
    evidence_graph: EvidenceGraph | None = None,
    contradictions: list[Contradiction] | None = None,
) -> FactConfidence | None:
    """Build one confidence record by fact id, or None when no fact exists."""

    fact = state.facts.get(fact_id)
    if fact is None:
        return None
    graph = evidence_graph if evidence_graph is not None else build_evidence_graph(state)
    contradiction_items = (
        contradictions
        if contradictions is not None
        else build_contradictions(state, evidence_graph=graph)
    )
    evidence_by_fact_id = {view.fact_id: view for view in graph.fact_evidence}
    return _fact_confidence(
        fact,
        evidence_by_fact_id.get(fact.id),
        _contradictions_by_fact_id(contradiction_items).get(fact.id, []),
    )


def build_confidence_summary(
    state: State, fact_confidences: list[FactConfidence] | None = None
) -> ConfidenceSummary:
    """Summarize confidence buckets for projected facts."""

    items = (
        fact_confidences
        if fact_confidences is not None
        else build_fact_confidences(state)
    )
    average = (
        round(sum(item.confidence for item in items) / len(items), 6) if items else 0.0
    )
    return ConfidenceSummary(
        fact_count=len(items),
        strongly_supported_count=sum(
            1 for item in items if item.confidence >= STRONGLY_SUPPORTED_THRESHOLD
        ),
        weakly_supported_count=sum(
            1 for item in items if 0.0 < item.confidence < STRONGLY_SUPPORTED_THRESHOLD
        ),
        unsupported_count=sum(1 for item in items if item.unsupported),
        contradicted_count=sum(1 for item in items if item.contradicted),
        average_confidence=average,
        last_event_id=state.last_event_id,
        projection_version=state.projection_version,
    )


def find_fact_confidence(
    state: State,
    subject: str,
    predicate: str,
    object: Any | None = None,
    evidence_graph: EvidenceGraph | None = None,
    contradictions: list[Contradiction] | None = None,
) -> list[FactConfidence]:
    """Find confidence records matching a subject/predicate/object query."""

    return [
        item
        for item in build_fact_confidences(state, evidence_graph, contradictions)
        if item.subject == subject
        and item.predicate == predicate
        and (object is None or _stable_value(item.object) == _stable_value(object))
    ]


def _fact_confidence(
    fact: Fact,
    evidence_view: FactEvidenceView | None,
    contradictions: list[Contradiction],
) -> FactConfidence:
    support_count = len(evidence_view.evidence) if evidence_view is not None else 0
    supporting_event_ids = (
        list(evidence_view.supporting_event_ids) if evidence_view is not None else []
    )
    reasons: list[str] = []

    evidence_confidence = _evidence_confidence(support_count)
    explicit_confidence = fact.confidence if _has_explicit_confidence(fact) else None
    confidence = max(evidence_confidence, explicit_confidence or 0.0)

    if support_count == 0:
        if explicit_confidence is None:
            reasons.append("unsupported: no linked supporting evidence")
        else:
            reasons.append("explicit fact confidence used without linked evidence")
    elif support_count == 1:
        reasons.append("supported by 1 evidence record")
    else:
        reasons.append(f"supported by {support_count} evidence records")

    if explicit_confidence is not None and explicit_confidence >= evidence_confidence:
        reasons.append("explicit fact confidence preserved")

    contradiction_count = len(contradictions)
    if contradiction_count:
        confidence *= CONTRADICTION_PENALTY
        reasons.append("confidence reduced because fact is contradicted")
        for contradiction in contradictions:
            reasons.append(f"contradiction: {contradiction.reason}")

    confidence = _clamp(confidence)
    unsupported = support_count == 0 and explicit_confidence is None
    return FactConfidence(
        fact_id=fact.id,
        subject=fact.subject_id,
        predicate=fact.predicate,
        object=fact.value,
        confidence=confidence,
        support_count=support_count,
        contradiction_count=contradiction_count,
        unsupported=unsupported,
        contradicted=contradiction_count > 0,
        reasons=reasons,
        supporting_event_ids=sorted(set(supporting_event_ids)),
    )


def _evidence_confidence(support_count: int) -> float:
    if support_count >= 2:
        return STRONGLY_SUPPORTED_THRESHOLD
    if support_count == 1:
        return 0.50
    return 0.0


def _has_explicit_confidence(fact: Fact) -> bool:
    default = DEFAULT_CONFIDENCE_BY_SOURCE_TYPE.get(fact.source_type)
    return default is None or fact.confidence != default


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, round(float(value), 6)))


def _contradictions_by_fact_id(
    contradictions: Iterable[Contradiction],
) -> dict[str, list[Contradiction]]:
    grouped: dict[str, list[Contradiction]] = {}
    for contradiction in contradictions:
        for fact_id in contradiction.fact_ids:
            grouped.setdefault(fact_id, []).append(contradiction)
    return grouped


def _ordered_facts(state: State) -> list[Fact]:
    return sorted(state.facts.values(), key=_fact_key)


def _fact_key(fact: Fact) -> tuple[str, str, str, str]:
    return (fact.subject_id, fact.predicate, _stable_value(fact.value), fact.id)


def _stable_value(value: Any) -> str:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)
