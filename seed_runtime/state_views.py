"""Read-only views over projected Seed State.

State Views are deterministic projections of an already-built State object. They do
not read ledgers, append events, invoke providers, evaluate policy, or execute
runtime behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from seed_runtime.facts import FactSupport
from seed_runtime.read_model_ownership import read_model_construction_inputs
from seed_runtime.state import GraphValidationIssue, State


@dataclass(frozen=True)
class FactView:
    fact_id: str
    subject: str
    predicate: str
    object: Any
    confidence: float
    dimensions: dict[str, str] = field(default_factory=dict)
    supporting_event_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ObservationView:
    observation_id: str
    observation_type: str
    summary: str
    supporting_event_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RequirementView:
    requirement_id: str
    requirement_name: str
    status: str
    supporting_event_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CapabilityView:
    capability_id: str
    capability_name: str
    status: str
    supporting_event_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class IssueView:
    issue_id: str
    summary: str
    severity: str
    supporting_event_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class StateSummary:
    facts_count: int
    observations_count: int
    requirements_count: int
    capabilities_count: int
    issues_count: int
    last_event_id: str | None
    projection_version: str


def build_fact_view(state: State) -> list[FactView]:
    """Return deterministic read-only Fact views from current projected claims.

    The append-only ledger can contain many fact records for the same durable
    claim when a source is observed repeatedly.  Current fact views render the
    support projection instead of raw fact rows so identical durable claims are
    shown once while their supporting provenance remains attached.
    """

    fact_supports = state.fact_supports or _fact_supports_from_raw_facts(state)
    return [
        FactView(
            fact_id=_representative_fact_id(state, support.supporting_fact_ids),
            subject=support.subject,
            predicate=support.predicate,
            object=support.value,
            confidence=support.confidence,
            dimensions=_sorted_dimensions(support.dimensions),
            supporting_event_ids=_supporting_ids_for_facts(
                state, support.supporting_fact_ids
            ),
        )
        for support in sorted(
            fact_supports,
            key=lambda item: (
                item.subject,
                item.predicate,
                _stable_value(item.value),
                _stable_value(item.dimensions),
                _stable_value(item.supporting_fact_ids),
            ),
        )
    ]



def _fact_supports_from_raw_facts(state: State) -> list[FactSupport]:
    """Fallback for tests and callers that construct State facts directly."""

    return [
        FactSupport(
            subject=fact.subject_id,
            predicate=fact.predicate,
            value=fact.value,
            dimensions=dict(fact.dimensions),
            supporting_fact_ids=[fact.id],
            source_types=[fact.source_type],
            confidence=fact.confidence,
            observed_at=fact.observed_at,
            latest_observed_at=fact.observed_at,
            expired=False,
            expires_at=fact.expires_at,
        )
        for fact in state.facts.values()
    ]

def _representative_fact_id(state: State, fact_ids: list[str]) -> str:
    facts = [state.facts[fact_id] for fact_id in fact_ids if fact_id in state.facts]
    if not facts:
        return fact_ids[-1] if fact_ids else ""
    return max(
        facts,
        key=lambda fact: (
            fact.confidence,
            not fact.inferred,
            fact.observed_at,
            fact.id,
        ),
    ).id


def _supporting_ids_for_facts(state: State, fact_ids: list[str]) -> list[str]:
    supporting_ids: list[str] = []
    for fact_id in fact_ids:
        fact = state.facts.get(fact_id)
        if fact is None:
            supporting_ids.append(fact_id)
            continue
        supporting_ids.extend(fact.evidence_ids)
        if fact.source_fact_id:
            supporting_ids.append(fact.source_fact_id)
    return _dedupe_sorted(supporting_ids)


def build_observation_view(state: State) -> list[ObservationView]:
    """Return deterministic read-only Observation views from projected State."""

    return [
        ObservationView(
            observation_id=observation.id,
            observation_type=observation.source_type,
            summary=(
                f"{observation.subject} {observation.predicate} "
                f"{_stable_value(observation.value)}"
            ),
            supporting_event_ids=_supporting_ids_for_observation(state, observation.id),
        )
        for observation in sorted(
            state.observations.values(),
            key=lambda item: (item.subject, item.predicate, _stable_value(item.value), item.id),
        )
    ]


def build_requirement_view(state: State) -> list[RequirementView]:
    """Return deterministic read-only Requirement views from projected goals."""

    return [
        RequirementView(
            requirement_id=goal.id,
            requirement_name=goal.summary,
            status=goal.status,
            supporting_event_ids=_dedupe_sorted(
                [goal.created_from_event_id] if goal.created_from_event_id else []
            ),
        )
        for goal in sorted(state.goals.values(), key=lambda item: (item.summary, item.id))
    ]


def build_capability_view(state: State) -> list[CapabilityView]:
    """Return deterministic read-only Capability views from projected State."""

    views: list[CapabilityView] = []
    for need in sorted(
        state.tool_needs.values(), key=lambda item: (item.capability, item.name, item.id)
    ):
        views.append(
            CapabilityView(
                capability_id=need.id,
                capability_name=need.capability,
                status=need.status,
                supporting_event_ids=_dedupe_sorted(
                    [need.requested_by_event_id] if need.requested_by_event_id else []
                ),
            )
        )
    for tool in sorted(state.tools.values(), key=lambda item: (item.name, item.toolkit_id)):
        views.append(
            CapabilityView(
                capability_id=tool.name,
                capability_name=tool.name,
                status="registered",
                supporting_event_ids=[],
            )
        )
    return views


def build_issue_view(state: State) -> list[IssueView]:
    """Return deterministic read-only Issue views from projected graph/issues state."""

    return [
        IssueView(
            issue_id=issue.id,
            summary=_issue_summary(issue),
            severity=_view_severity(issue.severity),
            supporting_event_ids=_dedupe_sorted(
                [*issue.relationship_ids, *issue.source_fact_ids]
            ),
        )
        for issue in sorted(
            state.graph_issues,
            key=lambda item: (item.severity, item.subject, item.relationship, item.object, item.id),
        )
    ]


def build_state_summary(state: State) -> StateSummary:
    """Return a compact read-only summary of the projected world model."""

    inputs = read_model_construction_inputs(state)
    visible_state = inputs.visible_state
    return StateSummary(
        facts_count=_fact_view_count(visible_state),
        observations_count=len(visible_state.observations),
        requirements_count=len(visible_state.goals),
        capabilities_count=len(visible_state.tool_needs) + len(visible_state.tools),
        issues_count=len(visible_state.graph_issues),
        last_event_id=visible_state.last_event_id,
        projection_version=visible_state.projection_version,
    )


def _fact_view_count(state: State) -> int:
    if state.fact_supports:
        return len(state.fact_supports)
    return len(state.facts)


def _supporting_ids_for_observation(state: State, observation_id: str) -> list[str]:
    ids = [observation_id]
    for evidence in state.evidence.values():
        if evidence.payload.get("observation_id") == observation_id:
            ids.append(evidence.id)
    for fact in state.facts.values():
        if any(evidence_id in ids for evidence_id in fact.evidence_ids):
            ids.append(fact.id)
    return _dedupe_sorted(ids)


def _issue_summary(issue: GraphValidationIssue) -> str:
    return f"{issue.subject} {issue.relationship} {issue.object}: {issue.reason}"


def _view_severity(severity: str) -> str:
    if severity == "error":
        return "high"
    if severity == "warning":
        return "medium"
    return severity


def _dedupe_sorted(values: list[str | None]) -> list[str]:
    return sorted({value for value in values if value})


def _sorted_dimensions(dimensions: dict[str, str]) -> dict[str, str]:
    return {key: dimensions[key] for key in sorted(dimensions)}


def _stable_value(value: Any) -> str:
    if isinstance(value, (dict, list, tuple)):
        import json

        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)
