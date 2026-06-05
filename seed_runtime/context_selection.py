"""Useful ordering helpers for model-visible context sections.

These helpers intentionally do not perform semantic matching, token counting, or
LLM-based ranking. They provide deterministic freshness/relevance ordering inside
sections before :class:`seed_runtime.context_budget.ContextBudget` applies limits. This helper is retained for non-provider selection experiments; RuntimeLoop providers receive DecisionContextView instead.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from seed_runtime.evidence import Evidence
from seed_runtime.facts import Fact
from seed_runtime.models import Entity, Goal


def _datetime_desc_key(value: datetime) -> float:
    """Return a numeric key that sorts newer datetimes before older ones."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return -value.timestamp()


def _is_expired(fact: Fact, now: datetime) -> bool:
    if fact.expires_at is None:
        return False
    expires_at = fact.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return expires_at < now


def order_facts(facts: Iterable[Fact], now: datetime | None = None) -> list[Fact]:
    """Order facts by freshness, recency, confidence, then id.

    Fresh/unexpired facts are preferred over expired facts. Within each freshness
    group, newer observations and higher-confidence facts are preferred.
    """
    now = now or datetime.now(timezone.utc)
    return sorted(
        facts,
        key=lambda fact: (
            _is_expired(fact, now),
            _datetime_desc_key(fact.observed_at),
            -fact.confidence,
            fact.id,
        ),
    )


def order_evidence(evidence: Iterable[Evidence]) -> list[Evidence]:
    """Order evidence by recency, confidence, then id."""
    return sorted(
        evidence,
        key=lambda item: (
            _datetime_desc_key(item.observed_at),
            -item.confidence,
            item.id,
        ),
    )


def order_goals(goals: Iterable[Goal]) -> list[Goal]:
    """Order goals with active goals first and a deterministic id tie-break."""
    return sorted(goals, key=lambda goal: (goal.status != "active", goal.id))


def order_entities(entities: Iterable[Entity]) -> list[Entity]:
    """Order entities by confidence, then name/id for deterministic ties."""
    return sorted(
        entities,
        key=lambda entity: (-entity.confidence, entity.name, entity.id),
    )
