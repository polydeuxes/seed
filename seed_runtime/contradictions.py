"""Read-only contradiction detection over projected State facts.

Contradiction Detection is a projection view derived from already-projected
State and, when available, the Evidence Graph. It never reads an event ledger,
appends events, mutates facts, executes runtime behavior, calls providers,
evaluates policy, executes tools, or persists a separate contradiction store.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Iterable, Literal

from seed_runtime.evidence_graph import (
    EvidenceGraph,
    FactEvidenceView,
    build_evidence_graph,
)
from seed_runtime.facts import Fact
from seed_runtime.state import State

Severity = Literal["high", "medium", "low"]

DEFAULT_EXCLUSIVE_PREDICATES: frozenset[str] = frozenset(
    {
        "status",
        "runs_on",
        "located_on",
        "ip",
        "hostname",
        "enabled",
        "available",
        "version",
    }
)


@dataclass(frozen=True)
class Contradiction:
    contradiction_id: str
    subject: str
    predicate: str
    fact_ids: list[str]
    values: list[Any]
    severity: Severity
    reason: str
    evidence_by_fact_id: dict[str, FactEvidenceView] = field(default_factory=dict)
    supporting_event_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ContradictionSummary:
    contradiction_count: int
    affected_fact_count: int
    high_severity_count: int
    medium_severity_count: int
    low_severity_count: int
    last_event_id: str | None
    projection_version: str


def build_contradictions(
    state: State,
    evidence_graph: EvidenceGraph | None = None,
    exclusive_predicates: set[str] | frozenset[str] | None = None,
) -> list[Contradiction]:
    """Return deterministic read-only contradictions from projected facts.

    The v1 detector is intentionally conservative: it only reports facts that
    share an exact subject and predicate while asserting different values for a
    built-in or caller-supplied exclusive predicate. Duplicate identical values
    are not contradictions, and no fact is resolved or rewritten.
    """

    exclusive = set(DEFAULT_EXCLUSIVE_PREDICATES)
    if exclusive_predicates is not None:
        exclusive.update(exclusive_predicates)

    graph = (
        evidence_graph if evidence_graph is not None else build_evidence_graph(state)
    )
    evidence_by_fact_id = {view.fact_id: view for view in graph.fact_evidence}

    grouped: dict[tuple[str, str], list[Fact]] = {}
    for fact in state.facts.values():
        grouped.setdefault((fact.subject_id, fact.predicate), []).append(fact)

    contradictions: list[Contradiction] = []
    for (subject, predicate), facts in sorted(grouped.items()):
        if predicate not in exclusive:
            continue
        values_by_key: dict[str, Any] = {}
        facts_by_value_key: dict[str, list[Fact]] = {}
        for fact in sorted(facts, key=_fact_key):
            value_key = _stable_value(fact.value)
            values_by_key.setdefault(value_key, fact.value)
            facts_by_value_key.setdefault(value_key, []).append(fact)
        if len(values_by_key) <= 1:
            continue

        conflicting_facts = [
            fact
            for value_key in sorted(facts_by_value_key)
            for fact in facts_by_value_key[value_key]
        ]
        fact_ids = [fact.id for fact in conflicting_facts]
        values = [values_by_key[value_key] for value_key in sorted(values_by_key)]
        attached_evidence = {
            fact_id: evidence_by_fact_id[fact_id]
            for fact_id in fact_ids
            if fact_id in evidence_by_fact_id
        }
        supporting_event_ids = _dedupe_sorted(
            [
                event_id
                for view in attached_evidence.values()
                for event_id in view.supporting_event_ids
            ]
            or [
                event_id
                for fact in conflicting_facts
                for event_id in [*fact.evidence_ids, fact.source_fact_id]
                if event_id
            ]
        )
        severity, reason = _classify_conflict(predicate, values)
        contradictions.append(
            Contradiction(
                contradiction_id=_contradiction_id(subject, predicate, fact_ids, values),
                subject=subject,
                predicate=predicate,
                fact_ids=fact_ids,
                values=values,
                severity=severity,
                reason=reason,
                evidence_by_fact_id=attached_evidence,
                supporting_event_ids=supporting_event_ids,
            )
        )

    return sorted(contradictions, key=_contradiction_key)


def build_contradiction_summary(
    state: State, contradictions: list[Contradiction] | None = None
) -> ContradictionSummary:
    """Return aggregate counts for the contradiction projection view."""

    items = contradictions if contradictions is not None else build_contradictions(state)
    affected_fact_ids = {
        fact_id for contradiction in items for fact_id in contradiction.fact_ids
    }
    return ContradictionSummary(
        contradiction_count=len(items),
        affected_fact_count=len(affected_fact_ids),
        high_severity_count=sum(1 for item in items if item.severity == "high"),
        medium_severity_count=sum(1 for item in items if item.severity == "medium"),
        low_severity_count=sum(1 for item in items if item.severity == "low"),
        last_event_id=state.last_event_id,
        projection_version=state.projection_version,
    )


def find_contradictions_for_fact(
    state: State, fact_id: str, evidence_graph: EvidenceGraph | None = None
) -> list[Contradiction]:
    """Return contradictions that include a projected fact id."""

    return [
        contradiction
        for contradiction in build_contradictions(state, evidence_graph=evidence_graph)
        if fact_id in contradiction.fact_ids
    ]


def _classify_conflict(_predicate: str, _values: Iterable[Any]) -> tuple[Severity, str]:
    return "high", "exclusive predicate has multiple values"


def _contradiction_id(
    subject: str, predicate: str, fact_ids: list[str], values: list[Any]
) -> str:
    payload = json.dumps(
        {
            "subject": subject,
            "predicate": predicate,
            "fact_ids": fact_ids,
            "values": [_stable_value(value) for value in values],
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"contradiction-{digest}"


def _contradiction_key(contradiction: Contradiction) -> tuple[str, str, str, str]:
    return (
        contradiction.subject,
        contradiction.predicate,
        ",".join(_stable_value(value) for value in contradiction.values),
        contradiction.contradiction_id,
    )


def _fact_key(fact: Fact) -> tuple[str, str, str, str]:
    return (fact.subject_id, fact.predicate, _stable_value(fact.value), fact.id)


def _dedupe_sorted(values: Iterable[str | None]) -> list[str]:
    return sorted({value for value in values if value})


def _stable_value(value: Any) -> str:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)
