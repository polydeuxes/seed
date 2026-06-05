"""Read-only Context View projections for decision-ready knowledge.

Context Views are deterministic projections derived from already-projected
State, the Evidence Graph, Contradiction Detection, and Confidence Aggregation.
They are the boundary between Seed's knowledge system and decision-making: they
never read an event ledger, append events, mutate State, execute runtime
behavior, call providers, evaluate policy, execute tools, call LLMs, or persist a
separate context store.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterable

from seed_runtime.confidence import (
    STRONGLY_SUPPORTED_THRESHOLD,
    FactConfidence,
    build_fact_confidences,
)
from seed_runtime.contradictions import Contradiction, build_contradictions
from seed_runtime.evidence_graph import EvidenceGraph, build_evidence_graph
from seed_runtime.state import GraphValidationIssue, State
from seed_runtime.state_views import build_capability_view, build_requirement_view


@dataclass(frozen=True)
class ContextFact:
    fact_id: str
    subject: str
    predicate: str
    object: Any
    confidence: float
    contradicted: bool
    evidence_count: int


@dataclass(frozen=True)
class ContextIssue:
    issue_id: str
    summary: str
    severity: str


@dataclass(frozen=True)
class ContextRequirement:
    requirement_id: str
    requirement_name: str
    status: str


@dataclass(frozen=True)
class ContextCapability:
    capability_id: str
    capability_name: str
    status: str


@dataclass(frozen=True)
class ContextSummary:
    facts_count: int
    issues_count: int
    contradicted_fact_count: int
    strongly_supported_count: int
    weakly_supported_count: int
    unsupported_count: int


@dataclass(frozen=True)
class DecisionContextView:
    facts: list[ContextFact] = field(default_factory=list)
    issues: list[ContextIssue] = field(default_factory=list)
    requirements: list[ContextRequirement] = field(default_factory=list)
    capabilities: list[ContextCapability] = field(default_factory=list)
    summary: ContextSummary = field(
        default_factory=lambda: ContextSummary(
            facts_count=0,
            issues_count=0,
            contradicted_fact_count=0,
            strongly_supported_count=0,
            weakly_supported_count=0,
            unsupported_count=0,
        )
    )
    projection_version: str = "v1"
    last_event_id: str | None = None


def build_decision_context_view(
    state: State,
    evidence_graph: EvidenceGraph | None = None,
    contradictions: list[Contradiction] | None = None,
    fact_confidences: list[FactConfidence] | None = None,
    *,
    include_unsupported: bool = False,
) -> DecisionContextView:
    """Build the deterministic DecisionProvider context from knowledge layers.

    The caller may provide precomputed projection-layer inputs to make the data
    dependencies explicit. Missing inputs are built from projected State only;
    no runtime, provider, policy, tool, LLM, event append, or State mutation path
    is introduced.
    """

    graph = evidence_graph if evidence_graph is not None else build_evidence_graph(state)
    contradiction_items = (
        contradictions if contradictions is not None else build_contradictions(state, graph)
    )
    confidence_items = (
        fact_confidences
        if fact_confidences is not None
        else build_fact_confidences(state, graph, contradiction_items)
    )
    facts = select_context_facts(
        confidence_items, include_unsupported=include_unsupported
    )
    issues = _context_issues(state.graph_issues, contradiction_items)
    requirements = _context_requirements(state)
    capabilities = _context_capabilities(state)

    return DecisionContextView(
        facts=facts,
        issues=issues,
        requirements=requirements,
        capabilities=capabilities,
        summary=build_context_summary(facts, issues),
        projection_version=state.projection_version,
        last_event_id=state.last_event_id,
    )


def select_context_facts(
    fact_confidences: Iterable[FactConfidence], *, include_unsupported: bool = False
) -> list[ContextFact]:
    """Select decision-context facts using simple deterministic v1 rules."""

    selected = [
        item
        for item in fact_confidences
        if include_unsupported or not item.unsupported
    ]
    return [
        ContextFact(
            fact_id=item.fact_id,
            subject=item.subject,
            predicate=item.predicate,
            object=item.object,
            confidence=item.confidence,
            contradicted=item.contradicted,
            evidence_count=item.support_count,
        )
        for item in sorted(selected, key=_context_fact_confidence_key)
    ]


def build_context_summary(
    facts: Iterable[ContextFact], issues: Iterable[ContextIssue]
) -> ContextSummary:
    """Summarize the exact facts and issues included in a context view."""

    fact_items = list(facts)
    issue_items = list(issues)
    return ContextSummary(
        facts_count=len(fact_items),
        issues_count=len(issue_items),
        contradicted_fact_count=sum(1 for fact in fact_items if fact.contradicted),
        strongly_supported_count=sum(
            1 for fact in fact_items if fact.confidence >= STRONGLY_SUPPORTED_THRESHOLD
        ),
        weakly_supported_count=sum(
            1 for fact in fact_items if 0.0 < fact.confidence < STRONGLY_SUPPORTED_THRESHOLD
        ),
        unsupported_count=sum(1 for fact in fact_items if fact.evidence_count == 0),
    )


def _context_fact_confidence_key(item: FactConfidence) -> tuple[int, float, str, str, str, str]:
    return (
        0 if item.support_count > 0 else 1,
        -item.confidence,
        item.subject,
        item.predicate,
        _stable_value(item.object),
        item.fact_id,
    )


def _context_issues(
    graph_issues: Iterable[GraphValidationIssue], contradictions: Iterable[Contradiction]
) -> list[ContextIssue]:
    issues: list[ContextIssue] = []
    for contradiction in contradictions:
        issues.append(
            ContextIssue(
                issue_id=contradiction.contradiction_id,
                summary=(
                    f"contradiction: {contradiction.subject} {contradiction.predicate} "
                    f"has conflicting values "
                    + ", ".join(_stable_value(value) for value in contradiction.values)
                ),
                severity=contradiction.severity,
            )
        )
    for issue in graph_issues:
        issues.append(
            ContextIssue(
                issue_id=issue.id,
                summary=(
                    f"graph issue: {issue.subject} {issue.relationship} "
                    f"{issue.object}; {issue.reason}"
                ),
                severity=issue.severity,
            )
        )
    return sorted(issues, key=lambda item: (item.severity, item.summary, item.issue_id))


def _context_requirements(state: State) -> list[ContextRequirement]:
    return [
        ContextRequirement(
            requirement_id=view.requirement_id,
            requirement_name=view.requirement_name,
            status=view.status,
        )
        for view in build_requirement_view(state)
    ]


def _context_capabilities(state: State) -> list[ContextCapability]:
    return [
        ContextCapability(
            capability_id=view.capability_id,
            capability_name=view.capability_name,
            status=view.status,
        )
        for view in build_capability_view(state)
    ]


def _stable_value(value: Any) -> str:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)
