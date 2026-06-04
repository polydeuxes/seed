"""Deterministic human-readable traversal of projected fact provenance."""

from __future__ import annotations

from collections import deque
from datetime import datetime
from importlib.util import find_spec
from typing import Any, Literal

from seed_runtime.base import SeedModel
from seed_runtime.facts import FactConflict, FactSupport
from seed_runtime.inference_catalog import InferenceRule
from seed_runtime.state import State

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field


class FactExplanation(SeedModel):
    """Provenance and inference details for one supporting fact."""

    fact_id: str
    subject: str
    predicate: str
    value: Any
    source_type: str
    confidence: float
    observed_at: datetime
    evidence_ids: list[str] = Field(default_factory=list)
    inference_rule_id: str | None = None
    inference_rule: InferenceRule | None = None
    source_fact_id: str | None = None
    confidence_cap: float | None = None
    source_fact: FactExplanation | None = None
    resolution_chain: list[str] = Field(default_factory=list)
    recursion_stopped: bool = False


class BeliefExplanation(SeedModel):
    """One value and every projected fact supporting it."""

    value: Any
    confidence: float
    supporting_fact_ids: list[str] = Field(default_factory=list)
    facts: list[FactExplanation] = Field(default_factory=list)


class Explanation(SeedModel):
    """Result of a why query over projected state.

    The shape intentionally separates the query result from its fact traversal so
    future ``why-not``, ``how``, and ``what-changed`` builders can reuse the same
    fact-level explanation model without changing reasoning behavior.
    """

    subject: str
    predicate: str
    status: Literal["current", "ambiguous", "none"]
    current_beliefs: list[BeliefExplanation] = Field(default_factory=list)
    competing_beliefs: list[BeliefExplanation] = Field(default_factory=list)
    conflicts: list[FactConflict] = Field(default_factory=list)


class ExplanationBuilder:
    """Build deterministic explanations entirely from a projected ``State``."""

    def __init__(self, state: State) -> None:
        self.state = state

    def why(self, subject: str, predicate: str) -> Explanation:
        """Explain the current value(s), ambiguity, and active conflicts."""

        supports = self.state.get_fact_supports(subject, predicate)
        conflicts = self._matching_conflicts(subject, predicate)

        if self.state.predicate_catalog.is_multi(predicate):
            beliefs = [self._explain_support(subject, support) for support in supports]
            return Explanation(
                subject=subject,
                predicate=predicate,
                status="current" if beliefs else "none",
                current_beliefs=beliefs,
                conflicts=conflicts,
            )

        current_support = self.state.get_fact_support(subject, predicate)
        if current_support is None:
            competing = [
                self._explain_support(subject, support) for support in supports
            ]
            return Explanation(
                subject=subject,
                predicate=predicate,
                status="ambiguous" if competing else "none",
                competing_beliefs=competing,
                conflicts=conflicts,
            )

        current = self._explain_support(subject, current_support)
        competing = [
            self._explain_support(subject, support)
            for support in supports
            if support is not current_support and support.value != current_support.value
        ]
        return Explanation(
            subject=subject,
            predicate=predicate,
            status="current",
            current_beliefs=[current],
            competing_beliefs=competing,
            conflicts=conflicts,
        )

    def _explain_support(
        self, query_subject: str, support: FactSupport
    ) -> BeliefExplanation:
        facts = [
            self._explain_fact(query_subject, fact_id, seen=frozenset())
            for fact_id in support.supporting_fact_ids
            if fact_id in self.state.facts
        ]
        return BeliefExplanation(
            value=support.value,
            confidence=support.confidence,
            supporting_fact_ids=list(support.supporting_fact_ids),
            facts=facts,
        )

    def _explain_fact(
        self, query_subject: str, fact_id: str, *, seen: frozenset[str]
    ) -> FactExplanation:
        fact = self.state.facts[fact_id]
        if fact_id in seen:
            return FactExplanation(
                fact_id=fact.id,
                subject=fact.subject_id,
                predicate=fact.predicate,
                value=fact.value,
                source_type=fact.source_type,
                confidence=fact.confidence,
                observed_at=fact.observed_at,
                evidence_ids=list(fact.evidence_ids),
                inference_rule_id=fact.inference_rule_id,
                inference_rule=self._inference_rule(fact.inference_rule_id),
                source_fact_id=fact.source_fact_id,
                confidence_cap=fact.confidence_cap,
                resolution_chain=self._resolution_chain(query_subject, fact.subject_id),
                recursion_stopped=True,
            )

        source_fact = None
        if fact.source_fact_id and fact.source_fact_id in self.state.facts:
            source_fact = self._explain_fact(
                query_subject,
                fact.source_fact_id,
                seen=seen | {fact_id},
            )
        return FactExplanation(
            fact_id=fact.id,
            subject=fact.subject_id,
            predicate=fact.predicate,
            value=fact.value,
            source_type=fact.source_type,
            confidence=fact.confidence,
            observed_at=fact.observed_at,
            evidence_ids=list(fact.evidence_ids),
            inference_rule_id=fact.inference_rule_id,
            inference_rule=self._inference_rule(fact.inference_rule_id),
            source_fact_id=fact.source_fact_id,
            confidence_cap=fact.confidence_cap,
            source_fact=source_fact,
            resolution_chain=self._resolution_chain(query_subject, fact.subject_id),
        )

    def _inference_rule(self, rule_id: str | None) -> InferenceRule | None:
        if rule_id is None:
            return None
        return self.state.inference_catalog.get(rule_id)

    def _resolution_chain(self, start: str, target: str) -> list[str]:
        """Return a deterministic shortest explicit-alias path to a fact subject."""

        if start == target:
            return [start]
        adjacency: dict[str, set[str]] = {}
        for alias in self.state.entity_aliases:
            adjacency.setdefault(alias.subject, set()).add(alias.alias)
            adjacency.setdefault(alias.alias, set()).add(alias.subject)
        if start not in adjacency or target not in adjacency:
            return []

        pending: deque[tuple[str, list[str]]] = deque([(start, [start])])
        visited = {start}
        while pending:
            current, path = pending.popleft()
            for neighbor in sorted(adjacency.get(current, set())):
                if neighbor in visited:
                    continue
                next_path = [*path, neighbor]
                if neighbor == target:
                    return next_path
                visited.add(neighbor)
                pending.append((neighbor, next_path))
        return []

    def _matching_conflicts(self, subject: str, predicate: str) -> list[FactConflict]:
        resolved = self.state.resolve_fact_subjects(subject)
        canonical = self.state.alias_resolver.canonical(subject)
        return [
            conflict
            for conflict in self.state.get_fact_conflicts()
            if conflict.predicate == predicate
            and (conflict.subject in resolved or conflict.subject == canonical)
        ]
