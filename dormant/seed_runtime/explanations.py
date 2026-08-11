"""Deterministic human-readable traversal of projected fact provenance."""

from __future__ import annotations

from collections import deque
from importlib.util import find_spec
from typing import Any, Literal

from seed_runtime.base import SeedModel
from seed_runtime.facts import Fact, FactConflict, FactSupport, is_fact_expired
from seed_runtime.state import State

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field


class FactExplanation(SeedModel):
    """Recursive explanation for one supporting projected fact."""

    fact_id: str
    subject: str
    predicate: str
    value: Any
    evidence_ids: list[str]
    source_type: str
    observed_at: str
    observed_confidence: float | None = None
    inferred_confidence: float | None = None
    confidence_cap: float | None = None
    inference_rule_id: str | None = None
    source_fact_id: str | None = None
    source_fact: "FactExplanation | None" = None
    entity_resolution: list[str] = Field(default_factory=list)


class BeliefExplanation(SeedModel):
    """Explanation of one supported value for a queried predicate."""

    subject: str
    predicate: str
    value: Any
    support_confidence: float
    supporting_fact_ids: list[str]
    evidence_ids: list[str]
    source_types: list[str]
    observed_at: str
    latest_observed_at: str
    facts: list[FactExplanation]


class Explanation(SeedModel):
    """Result of a why query over projected state.

    The shape intentionally separates current and competing beliefs so future
    query modes such as why-not, how, and what-changed can reuse the same
    recursive fact explanations without changing reasoning behavior.
    """

    query_subject: str
    query_predicate: str
    status: Literal["current", "ambiguous", "no_current_belief"]
    current_beliefs: list[BeliefExplanation] = Field(default_factory=list)
    competing_beliefs: list[BeliefExplanation] = Field(default_factory=list)
    conflict: FactConflict | None = None


class ExplanationBuilder:
    """Build deterministic explanations entirely from a projected :class:`State`."""

    def __init__(self, state: State) -> None:
        self.state = state

    def why(self, subject: str, predicate: str) -> Explanation:
        """Explain the current value(s), ambiguity, or conflict for a query."""

        supports = self.state.get_fact_supports(subject, predicate)
        if self.state.predicate_catalog.is_multi(predicate):
            return Explanation(
                query_subject=subject,
                query_predicate=predicate,
                status="current" if supports else "no_current_belief",
                current_beliefs=[
                    self._explain_support(subject, item) for item in supports
                ],
            )

        best = self.state.get_fact_support(subject, predicate)
        conflict = self._conflict(subject, predicate)
        if best is None:
            return Explanation(
                query_subject=subject,
                query_predicate=predicate,
                status="ambiguous" if supports else "no_current_belief",
                competing_beliefs=[
                    self._explain_support(subject, item) for item in supports
                ],
                conflict=conflict,
            )

        competing = [item for item in supports if repr(item.value) != repr(best.value)]
        return Explanation(
            query_subject=subject,
            query_predicate=predicate,
            status="current",
            current_beliefs=[self._explain_support(subject, best)],
            competing_beliefs=[
                self._explain_support(subject, item) for item in competing
            ],
            conflict=conflict,
        )

    def _explain_support(
        self, query_subject: str, support: FactSupport
    ) -> BeliefExplanation:
        facts = [
            self.state.facts[fact_id]
            for fact_id in support.supporting_fact_ids
            if fact_id in self.state.facts
            and not is_fact_expired(self.state.facts[fact_id])
        ]
        return BeliefExplanation(
            subject=support.subject,
            predicate=support.predicate,
            value=support.value,
            support_confidence=support.confidence,
            supporting_fact_ids=list(support.supporting_fact_ids),
            evidence_ids=sorted({item for fact in facts for item in fact.evidence_ids}),
            source_types=list(support.source_types),
            observed_at=support.observed_at.isoformat(),
            latest_observed_at=support.latest_observed_at.isoformat(),
            facts=[self._explain_fact(query_subject, fact, set()) for fact in facts],
        )

    def _explain_fact(
        self, query_subject: str, fact: Fact, visited: set[str]
    ) -> FactExplanation:
        source_fact = None
        source = None
        if fact.source_fact_id and fact.source_fact_id not in visited:
            source = self.state.facts.get(fact.source_fact_id)
            if source is not None:
                source_fact = self._explain_fact(
                    query_subject, source, visited | {fact.id}
                )
        confidence_cap = (
            fact.confidence
            if fact.inferred
            and source is not None
            and fact.confidence < source.confidence
            else None
        )
        return FactExplanation(
            fact_id=fact.id,
            subject=fact.subject_id,
            predicate=fact.predicate,
            value=fact.value,
            evidence_ids=list(fact.evidence_ids),
            source_type=fact.source_type,
            observed_at=fact.observed_at.isoformat(),
            observed_confidence=None if fact.inferred else fact.confidence,
            inferred_confidence=fact.confidence if fact.inferred else None,
            confidence_cap=confidence_cap,
            inference_rule_id=fact.inference_rule_id,
            source_fact_id=fact.source_fact_id,
            source_fact=source_fact,
            entity_resolution=self._resolution_chain(query_subject, fact.subject_id),
        )

    def _resolution_chain(self, start: str, target: str) -> list[str]:
        if start == target:
            return [start]
        adjacency: dict[str, set[str]] = {}
        for alias in self.state.entity_aliases:
            adjacency.setdefault(alias.subject, set()).add(alias.alias)
            adjacency.setdefault(alias.alias, set()).add(alias.subject)
        queue: deque[list[str]] = deque([[start]])
        visited = {start}
        while queue:
            path = queue.popleft()
            for neighbor in sorted(adjacency.get(path[-1], set())):
                if neighbor == target:
                    return [*path, neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append([*path, neighbor])
        return [start] if start == target else []

    def _conflict(self, subject: str, predicate: str) -> FactConflict | None:
        canonical = self.state.alias_resolver.canonical(subject)
        return next(
            (
                conflict
                for conflict in self.state.get_fact_conflicts()
                if conflict.subject == canonical and conflict.predicate == predicate
            ),
            None,
        )
