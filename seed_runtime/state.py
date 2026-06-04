"""State projection from append-only events."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable

from seed_runtime.events import EventLedger
from seed_runtime.evidence import Evidence
from seed_runtime.inference_rules import infer_facts
from seed_runtime.facts import (
    StaleFactRefreshRecommendation,
    is_fact_expired,
    is_measurement_predicate,
    recommended_capability_for_stale_fact,
)
from seed_runtime.models import (
    ActionPlan,
    Approval,
    Entity,
    Event,
    ExecutionAuthorization,
    Fact,
    FactConflict,
    FactSupport,
    Goal,
    HandoffPlan,
    Observation,
    PendingAction,
    ToolNeed,
    ToolSpec,
)


def _parse_dt(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


@dataclass(frozen=True)
class EntityRelationship:
    """A directed subject-predicate-object relationship projected from facts."""

    subject: str
    predicate: str
    object: str
    fact_id: str
    source_type: str
    confidence: float
    observed_at: datetime
    evidence_ids: list[str]
    inferred: bool


@dataclass(frozen=True)
class EntityAlias:
    """An explicit alias edge projected from alias-like facts."""

    canonical: str
    subject: str
    alias: str
    predicate: str
    fact_id: str
    source_type: str
    confidence: float
    observed_at: datetime
    evidence_ids: list[str]
    inferred: bool


ALIAS_PREDICATES = {"alias", "ip_address", "hostname"}


def _is_alias_predicate(predicate: str) -> bool:
    """Return whether a predicate explicitly links two entity identifiers."""

    return predicate in ALIAS_PREDICATES or predicate.endswith("_instance")


class AliasResolver:
    """Deterministic identity resolver built only from explicit alias facts."""

    def __init__(self, facts: Iterable[Fact] = ()) -> None:
        self._aliases: list[EntityAlias] = []
        self._aliases_by_name: dict[str, set[str]] = {}
        self._canonical_by_name: dict[str, str] = {}
        self._build(list(facts))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AliasResolver):
            return NotImplemented
        return (
            self._aliases == other._aliases
            and self._aliases_by_name == other._aliases_by_name
            and self._canonical_by_name == other._canonical_by_name
        )

    @property
    def aliases(self) -> list[EntityAlias]:
        return list(self._aliases)

    def resolve(self, subject: str, *, exact: bool = False) -> set[str]:
        """Return explicit aliases for subject, or just subject in exact mode."""

        if exact:
            return {subject}
        return set(self._aliases_by_name.get(subject, {subject}))

    def canonical(self, subject: str, *, exact: bool = False) -> str:
        """Return the canonical entity name for subject when an alias links it."""

        if exact:
            return subject
        return self._canonical_by_name.get(subject, subject)

    def _build(self, facts: list[Fact]) -> None:
        edges: list[tuple[str, str, Fact]] = []
        names: set[str] = set()
        for fact in facts:
            if not _is_alias_predicate(fact.predicate):
                continue
            alias = _relationship_object(fact.value)
            if alias is None:
                continue
            edges.append((fact.subject_id, alias, fact))
            names.add(fact.subject_id)
            names.add(alias)

        if not edges:
            return

        adjacency: dict[str, set[str]] = {name: set() for name in names}
        for subject, alias, _fact in edges:
            adjacency.setdefault(subject, set()).add(alias)
            adjacency.setdefault(alias, set()).add(subject)

        visited: set[str] = set()
        canonical_by_component: dict[str, str] = {}
        for name in sorted(adjacency):
            if name in visited:
                continue
            stack = [name]
            component: set[str] = set()
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                component.add(current)
                stack.extend(sorted(adjacency[current] - visited, reverse=True))
            canonical = _choose_canonical_alias_name(component, edges)
            for component_name in component:
                canonical_by_component[component_name] = canonical
                self._aliases_by_name[component_name] = set(component)
                self._canonical_by_name[component_name] = canonical

        seen_aliases: set[tuple[str, str, str, str]] = set()
        for subject, alias, fact in edges:
            canonical = canonical_by_component[subject]
            key = (canonical, subject, alias, fact.predicate)
            if key in seen_aliases:
                continue
            seen_aliases.add(key)
            self._aliases.append(
                EntityAlias(
                    canonical=canonical,
                    subject=subject,
                    alias=alias,
                    predicate=fact.predicate,
                    fact_id=fact.id,
                    source_type=fact.source_type,
                    confidence=fact.confidence,
                    observed_at=fact.observed_at,
                    evidence_ids=list(fact.evidence_ids),
                    inferred=fact.inferred,
                )
            )


@dataclass
class State:
    workspace_id: str
    entities: dict[str, Entity] = field(default_factory=dict)
    facts: dict[str, Fact] = field(default_factory=dict)
    observed_facts: dict[str, Fact] = field(default_factory=dict)
    inferred_facts: dict[str, Fact] = field(default_factory=dict)
    entity_relationships: list[EntityRelationship] = field(default_factory=list)
    entity_aliases: list[EntityAlias] = field(default_factory=list)
    alias_resolver: AliasResolver = field(default_factory=AliasResolver)
    fact_supports: list[FactSupport] = field(default_factory=list)
    fact_conflicts: list[FactConflict] = field(default_factory=list)
    evidence: dict[str, Evidence] = field(default_factory=dict)
    observations: dict[str, Observation] = field(default_factory=dict)
    goals: dict[str, Goal] = field(default_factory=dict)
    tool_needs: dict[str, ToolNeed] = field(default_factory=dict)
    approvals: dict[str, Approval] = field(default_factory=dict)
    action_plan_approvals: dict[str, str] = field(default_factory=dict)
    execution_authorizations: dict[str, ExecutionAuthorization] = field(
        default_factory=dict
    )
    execution_proposals: dict[str, Any] = field(default_factory=dict)
    pending_actions: dict[str, PendingAction] = field(default_factory=dict)
    action_plans: dict[str, ActionPlan] = field(default_factory=dict)
    handoff_plans: dict[str, HandoffPlan] = field(default_factory=dict)
    tools: dict[str, ToolSpec] = field(default_factory=dict)

    @property
    def open_tool_needs(self) -> list[ToolNeed]:
        closed = {"registered", "rejected"}
        return [need for need in self.tool_needs.values() if need.status not in closed]

    def get_entity_relationships(self, entity: str) -> list[EntityRelationship]:
        """Return relationships where the entity is the subject or object."""
        return [
            relationship
            for relationship in self.entity_relationships
            if relationship.subject == entity or relationship.object == entity
        ]

    def find_entities(
        self, predicate: str, object: str, *, include_provenance: bool = False
    ) -> list[str] | list[dict[str, Any]]:
        """Return subjects related to an object by the given predicate."""
        relationships = [
            relationship
            for relationship in self.entity_relationships
            if relationship.predicate == predicate and relationship.object == object
        ]
        if include_provenance:
            return [
                _relationship_payload(relationship, "subject")
                for relationship in relationships
            ]
        return _dedupe(relationship.subject for relationship in relationships)

    def find_related(
        self, subject: str, predicate: str, *, include_provenance: bool = False
    ) -> list[str] | list[dict[str, Any]]:
        """Return objects related to a subject by the given predicate."""
        relationships = [
            relationship
            for relationship in self.entity_relationships
            if relationship.subject == subject and relationship.predicate == predicate
        ]
        if include_provenance:
            return [
                _relationship_payload(relationship, "object")
                for relationship in relationships
            ]
        return _dedupe(relationship.object for relationship in relationships)

    def get_best_fact(
        self,
        subject: str,
        predicate: str,
        *,
        include_expired: bool = False,
        resolve_aliases: bool = True,
        dimensions: dict[str, str] | None = None,
    ) -> Fact | None:
        """Return the representative fact for the best-supported current belief."""
        best_support = self.get_fact_support(
            subject,
            predicate,
            include_expired=include_expired,
            resolve_aliases=resolve_aliases,
            dimensions=dimensions,
        )
        if best_support is None:
            return None
        supporting_facts = [
            self.facts[fact_id]
            for fact_id in best_support.supporting_fact_ids
            if fact_id in self.facts
            and (include_expired or not is_fact_expired(self.facts[fact_id]))
        ]
        if not supporting_facts:
            return None
        return max(
            supporting_facts,
            key=lambda fact: (
                fact.confidence,
                not fact.inferred,
                fact.observed_at,
                fact.id,
            ),
        )

    def get_fact_supports(
        self,
        subject: str,
        predicate: str,
        *,
        include_expired: bool = False,
        resolve_aliases: bool = True,
        dimensions: dict[str, str] | None = None,
    ) -> list[FactSupport]:
        """Return aggregate support groups for a subject and predicate.

        The CLI and model-facing state can refer to subjects by exact fact subject
        IDs, entity names, or a short hostname for facts stored with a fully
        qualified hostname.  Resolve those aliases before filtering supports so
        persisted observation facts remain queryable after reopening a ledger.
        """
        resolved_subjects = self.resolve_fact_subjects(
            subject, resolve_aliases=resolve_aliases
        )
        if resolve_aliases:
            fact_supports = _project_fact_supports(
                (
                    fact
                    for fact in self.facts.values()
                    if fact.subject_id in resolved_subjects
                ),
                include_expired=include_expired,
                subject_key=self.alias_resolver.canonical,
            )
        else:
            fact_supports = (
                _project_fact_supports(self.facts.values(), include_expired=True)
                if include_expired
                else self.fact_supports or _project_fact_supports(self.facts.values())
            )
        canonical_subject = self.alias_resolver.canonical(subject)
        return [
            support
            for support in fact_supports
            if support.predicate == predicate
            and (dimensions is None or support.dimensions == dimensions)
            and (
                support.subject in resolved_subjects
                or (resolve_aliases and support.subject == canonical_subject)
            )
        ]

    def resolve_fact_subjects(
        self, subject: str, *, resolve_aliases: bool = True
    ) -> set[str]:
        """Return an exact fact subject, or all matching aliases when enabled."""

        candidates = {subject}
        if not resolve_aliases:
            return candidates

        candidates.update(self.alias_resolver.resolve(subject))
        for entity in self.entities.values():
            entity_aliases = [entity.id, entity.name, *entity.aliases]
            if any(_subject_alias_matches(subject, alias) for alias in entity_aliases):
                candidates.add(entity.id)

        for fact in self.facts.values():
            if _subject_alias_matches(subject, fact.subject_id):
                candidates.add(fact.subject_id)
        return candidates

    def get_fact_support(
        self,
        subject: str,
        predicate: str,
        *,
        include_expired: bool = False,
        resolve_aliases: bool = True,
        dimensions: dict[str, str] | None = None,
    ) -> FactSupport | None:
        """Return the unambiguous strongest aggregate support, if one exists."""
        candidates = self.get_fact_supports(
            subject,
            predicate,
            include_expired=include_expired,
            resolve_aliases=resolve_aliases,
            dimensions=dimensions,
        )
        return _select_unambiguous_best_support(candidates)

    def get_fact_conflicts(
        self, *, include_expired: bool = False
    ) -> list[FactConflict]:
        """Return projected fact conflicts, optionally including expired facts."""
        if include_expired:
            return _project_fact_conflicts(self, include_expired=True)
        return self.fact_conflicts or _project_fact_conflicts(self)

    def get_stale_facts(self) -> list[Fact]:
        """Return facts that no longer influence projected state due to expiry."""
        return sorted(
            (fact for fact in self.facts.values() if is_fact_expired(fact)),
            key=lambda fact: (
                fact.expires_at or datetime.min.replace(tzinfo=timezone.utc),
                fact.id,
            ),
        )

    def get_stale_fact_refresh_recommendations(
        self,
    ) -> list[StaleFactRefreshRecommendation]:
        """Return capability recommendations for refreshing expired facts."""

        recommendations: list[StaleFactRefreshRecommendation] = []
        for fact in self.get_stale_facts():
            capability = recommended_capability_for_stale_fact(fact.predicate)
            recommendations.append(
                StaleFactRefreshRecommendation(
                    fact_id=fact.id,
                    subject=fact.subject_id,
                    predicate=fact.predicate,
                    value=fact.value,
                    recommended_capability=capability,
                    reason=(
                        f"predicate {fact.predicate!r} maps to "
                        f"{capability!r} for stale fact refresh"
                    ),
                )
            )
        return recommendations

    def has_approval(self, action: str, scope: str | None = None) -> Approval | None:
        now = datetime.now(timezone.utc)
        for approval in self.approvals.values():
            if approval.action != action:
                continue
            if scope is not None and approval.scope != scope:
                continue
            if approval.expires_at is not None and approval.expires_at < now:
                continue
            return approval
        return None


class StateProjector:
    """Rebuild current inspectable state from ledger events."""

    def __init__(
        self, ledger: EventLedger, *, measurement_history_limit: int = 1
    ) -> None:
        if measurement_history_limit < 1:
            raise ValueError("measurement_history_limit must be at least 1")
        self.ledger = ledger
        self.measurement_history_limit = measurement_history_limit

    def project(self, workspace_id: str) -> State:
        state = State(workspace_id=workspace_id)
        for event in self.ledger.list_events(workspace_id):
            self.apply(state, event)
        _project_inferred_facts(state)
        state.alias_resolver = AliasResolver(state.facts.values())
        all_measurement_evidence_ids = {
            evidence_id
            for fact in state.facts.values()
            if is_measurement_predicate(fact.predicate)
            for evidence_id in fact.evidence_ids
        }
        state.facts = _retain_projected_measurement_history(
            state.facts.values(),
            subject_key=state.alias_resolver.canonical,
            limit=self.measurement_history_limit,
        )
        state.observed_facts = {
            fact_id: fact for fact_id, fact in state.facts.items() if not fact.inferred
        }
        state.inferred_facts = {
            fact_id: fact for fact_id, fact in state.facts.items() if fact.inferred
        }
        _prune_projected_measurement_provenance(state, all_measurement_evidence_ids)
        state.fact_supports = _project_fact_supports(state.facts.values())
        state.entity_relationships = _project_entity_relationships(state.facts.values())
        state.entity_aliases = state.alias_resolver.aliases
        state.fact_conflicts = _project_fact_conflicts(state)
        return state

    def apply(self, state: State, event: Event) -> None:
        payload = event.payload
        if event.kind == "entity.upserted":
            data = payload.get("entity", payload)
            entity = Entity(**data)
            state.entities[entity.id] = entity
        elif event.kind == "observation.observed":
            data = payload.get("observation", payload).copy()
            data["observed_at"] = _parse_dt(data.get("observed_at")) or event.timestamp
            observation = Observation(**data)
            state.observations[observation.id] = observation
        elif event.kind == "evidence.observed":
            data = payload.get("evidence", payload).copy()
            data["observed_at"] = _parse_dt(data.get("observed_at")) or event.timestamp
            evidence = Evidence(**data)
            state.evidence[evidence.id] = evidence
        elif event.kind in {"fact.observed", "fact.inferred"}:
            data = _normalize_fact_event_payload(payload, event)
            if event.kind == "fact.inferred":
                data["inferred"] = True
                data["source_type"] = "inferred"
            else:
                data["inferred"] = False
                if data.get("source_type") == "inferred":
                    data.pop("source_type")
            fact = Fact(**data)
            state.facts[fact.id] = fact
            state.entity_relationships = _project_entity_relationships(
                state.facts.values()
            )
        elif event.kind == "goal.created":
            data = payload.get("goal", payload)
            goal = Goal(**data)
            state.goals[goal.id] = goal
        elif event.kind == "tool_need.created":
            data = payload.get("tool_need", payload)
            need = ToolNeed(**data)
            state.tool_needs[need.id] = need
        elif event.kind == "tool_need.status_changed":
            need_id = payload["tool_need_id"]
            if need_id in state.tool_needs:
                current = state.tool_needs[need_id]
                state.tool_needs[need_id] = ToolNeed(
                    **{**current.__dict__, "status": payload["status"]}
                )
        elif event.kind == "approval.granted":
            data = payload.get("approval", payload).copy()
            data["expires_at"] = _parse_dt(data.get("expires_at"))
            approval = Approval(**data)
            state.approvals[approval.id] = approval
        elif event.kind == "execution_authorization.granted":
            data = payload.get("execution_authorization", payload).copy()
            data["expires_at"] = _parse_dt(data.get("expires_at")) or event.timestamp
            authorization = ExecutionAuthorization(**data)
            state.execution_authorizations[authorization.id] = authorization
            proposal = state.execution_proposals.get(
                authorization.execution_proposal_id
            )
            if (
                proposal is not None
                and proposal.action_plan_id == authorization.action_plan_id
                and proposal.tool_name == authorization.tool_name
                and proposal.arguments_fingerprint
                == authorization.arguments_fingerprint
                and authorization.expires_at >= datetime.now(timezone.utc)
            ):
                state.execution_proposals[proposal.id] = proposal.model_copy(
                    update={"authorized": True, "executable": True}
                )
        elif event.kind == "execution_proposal.created":
            from seed_runtime.execution_proposals import ExecutionProposal

            data = payload.get("execution_proposal", payload)
            proposal = ExecutionProposal(**data)
            state.execution_proposals[proposal.id] = proposal
        elif event.kind == "handoff_plan.created":
            data = payload.get("handoff_plan", payload)
            handoff_plan = HandoffPlan(**data)
            state.handoff_plans[handoff_plan.id] = handoff_plan
        elif event.kind == "pending_action.created":
            data = payload.get("pending_action", payload)
            pending_action = PendingAction(**data)
            state.pending_actions[pending_action.id] = pending_action
        elif event.kind == "action_plan.approved":
            state.action_plan_approvals[payload["action_plan_id"]] = event.id
        elif event.kind == "action_plan.created":
            data = payload.get("action_plan", payload)
            action_plan = ActionPlan(**data)
            state.action_plans[action_plan.id] = action_plan
        elif event.kind in {
            "action_plan.accepted",
            "action_plan.rejected",
            "action_plan.superseded",
        }:
            action_plan_id = payload["action_plan_id"]
            if action_plan_id in state.action_plans:
                current = state.action_plans[action_plan_id]
                update = {
                    "status": payload.get("status", event.kind.rsplit(".", 1)[-1])
                }
                if event.kind == "action_plan.rejected":
                    update["rejection_reason"] = payload.get("reason")
                    update["replacement_plan_id"] = None
                elif event.kind == "action_plan.superseded":
                    update["rejection_reason"] = None
                    update["replacement_plan_id"] = payload.get("replacement_plan_id")
                elif event.kind == "action_plan.accepted":
                    update["rejection_reason"] = None
                    update["replacement_plan_id"] = None
                state.action_plans[action_plan_id] = current.model_copy(update=update)
        elif event.kind in {
            "pending_action.status_changed",
            "pending_action.approved",
            "pending_action.completed",
            "pending_action.cancelled",
        }:
            pending_action_id = payload["pending_action_id"]
            status = payload.get("status", event.kind.rsplit(".", 1)[-1])
            if pending_action_id in state.pending_actions:
                current = state.pending_actions[pending_action_id]
                state.pending_actions[pending_action_id] = current.model_copy(
                    update={"status": status}
                )
        elif event.kind == "tool.registered":
            data = payload.get("tool", payload)
            tool = ToolSpec(**data)
            state.tools[tool.name] = tool


def _project_inferred_facts(state: State) -> None:
    state.observed_facts = {
        fact_id: fact for fact_id, fact in state.facts.items() if not fact.inferred
    }
    state.inferred_facts = {
        fact_id: fact for fact_id, fact in state.facts.items() if fact.inferred
    }
    inferable_observed_facts = _observed_facts_with_unambiguous_runtimes(
        state.observed_facts.values()
    )
    state.inferred_facts.update(infer_facts(inferable_observed_facts))
    state.facts = {**state.observed_facts}
    for fact_id, fact in state.inferred_facts.items():
        if fact_id not in state.facts:
            state.facts[fact_id] = fact


def _observed_facts_with_unambiguous_runtimes(facts: Iterable[Fact]) -> list[Fact]:
    observed_facts = list(facts)
    runtime_facts_by_subject: dict[str, list[Fact]] = {}
    for fact in observed_facts:
        if fact.predicate == "runtime":
            runtime_facts_by_subject.setdefault(fact.subject_id, []).append(fact)

    winning_runtime_value_by_subject: dict[str, str] = {}
    ambiguous_runtime_subjects: set[str] = set()
    for subject, runtime_facts in runtime_facts_by_subject.items():
        supports = _project_fact_supports(runtime_facts)
        best_support = _select_unambiguous_best_support(supports)
        if best_support is None:
            ambiguous_runtime_subjects.add(subject)
        else:
            winning_runtime_value_by_subject[subject] = _fact_value_key(
                best_support.value
            )

    inferable_facts: list[Fact] = []
    for fact in observed_facts:
        if fact.predicate != "runtime":
            inferable_facts.append(fact)
            continue
        if fact.subject_id in ambiguous_runtime_subjects:
            continue
        if _fact_value_key(fact.value) == winning_runtime_value_by_subject.get(
            fact.subject_id
        ):
            inferable_facts.append(fact)
    return inferable_facts


_SOURCE_SUPPORT_WEIGHT: dict[str, float] = {
    "discovery": 1.0,
    "provider": 1.0,
    "user": 0.85,
    "imported": 0.75,
    "inferred": 0.50,
}


def _normalize_fact_event_payload(
    payload: dict[str, Any], event: Event
) -> dict[str, Any]:
    """Return a Fact-compatible payload for observed/inferred fact events.

    Current ObservationIngestor events store facts under a ``fact`` key with the
    Fact model's ``subject_id`` field.  Older or hand-written events may use the
    observation-facing ``subject`` key either in that nested fact payload or as a
    flat fact event payload.  Preserve both shapes so persisted ledgers continue
    to project into FactSupport/current-belief state after reopen.
    """

    data = payload.get("fact", payload).copy()
    if "subject_id" not in data and "subject" in data:
        data["subject_id"] = data.pop("subject")
    data["observed_at"] = _parse_dt(data.get("observed_at")) or event.timestamp
    data["expires_at"] = _parse_dt(data.get("expires_at"))
    if "evidence_ids" not in data and "source_event_id" in data:
        data["evidence_ids"] = [data.pop("source_event_id")]
    return data


def _prune_projected_measurement_provenance(
    state: State, all_measurement_evidence_ids: set[str]
) -> None:
    """Remove provenance belonging only to measurement samples pruned from state."""

    retained_evidence_ids = {
        evidence_id
        for fact in state.facts.values()
        for evidence_id in fact.evidence_ids
    }
    pruned_evidence_ids = all_measurement_evidence_ids - retained_evidence_ids
    pruned_observation_ids = {
        observation_id
        for evidence_id in pruned_evidence_ids
        if (evidence := state.evidence.get(evidence_id)) is not None
        and isinstance((observation_id := evidence.payload.get("observation_id")), str)
    }
    for evidence_id in pruned_evidence_ids:
        state.evidence.pop(evidence_id, None)
    for observation_id in pruned_observation_ids:
        state.observations.pop(observation_id, None)


def _retain_projected_measurement_history(
    facts: Iterable[Fact], *, subject_key: Any, limit: int
) -> dict[str, Fact]:
    """Keep durable history and only recent measurement samples in projection.

    The append-only ledger remains untouched. Measurement series are identified by
    canonical alias component, predicate, and dimensions.
    """

    durable: list[Fact] = []
    measurements: dict[tuple[str, str, str], list[Fact]] = {}
    for fact in facts:
        if not is_measurement_predicate(fact.predicate):
            durable.append(fact)
            continue
        key = (
            subject_key(fact.subject_id),
            fact.predicate,
            _dimensions_key(fact.dimensions),
        )
        measurements.setdefault(key, []).append(fact)

    retained = list(durable)
    for samples in measurements.values():
        retained.extend(
            sorted(samples, key=lambda fact: (fact.observed_at, fact.id), reverse=True)[
                :limit
            ]
        )
    return {fact.id: fact for fact in retained}


def _project_fact_supports(
    facts: Iterable[Fact],
    *,
    include_expired: bool = False,
    subject_key: Any | None = None,
) -> list[FactSupport]:
    grouped: dict[tuple[str, str, str, str], list[Fact]] = {}
    values_by_key: dict[tuple[str, str, str, str], Any] = {}
    for fact in facts:
        if not include_expired and is_fact_expired(fact):
            continue
        subject = (
            subject_key(fact.subject_id) if subject_key is not None else fact.subject_id
        )
        # A measurement has one current sample per resolved subject/predicate,
        # regardless of how many alias subjects or historical values supplied it.
        value_key = (
            ""
            if is_measurement_predicate(fact.predicate)
            else _fact_value_key(fact.value)
        )
        key = (subject, fact.predicate, _dimensions_key(fact.dimensions), value_key)
        grouped.setdefault(key, []).append(fact)
        values_by_key.setdefault(key, fact.value)

    supports: list[FactSupport] = []
    for (
        subject,
        predicate,
        dimensions_key,
        _value_key,
    ), supporting_facts in grouped.items():
        ordered_facts = sorted(
            supporting_facts, key=lambda fact: (fact.observed_at, fact.id)
        )
        source_types = _dedupe(fact.source_type for fact in ordered_facts)
        expires_at_values = [fact.expires_at for fact in ordered_facts]
        support_expires_at = (
            max(
                expires_at for expires_at in expires_at_values if expires_at is not None
            )
            if all(expires_at is not None for expires_at in expires_at_values)
            else None
        )
        if is_measurement_predicate(predicate):
            current_sample = max(
                ordered_facts, key=lambda fact: (fact.observed_at, fact.id)
            )
            supports.append(
                FactSupport(
                    subject=subject,
                    predicate=predicate,
                    value=current_sample.value,
                    dimensions=dict(current_sample.dimensions),
                    supporting_fact_ids=[current_sample.id],
                    source_types=[current_sample.source_type],
                    confidence=current_sample.confidence,
                    observed_at=current_sample.observed_at,
                    latest_observed_at=current_sample.observed_at,
                    expired=is_fact_expired(current_sample),
                    expires_at=current_sample.expires_at,
                    predicate_semantics="measurement",
                    support_kind="current_sample",
                )
            )
        else:
            supports.append(
                FactSupport(
                    subject=subject,
                    predicate=predicate,
                    value=values_by_key[
                        (subject, predicate, dimensions_key, _value_key)
                    ],
                    dimensions=dict(ordered_facts[-1].dimensions),
                    supporting_fact_ids=[fact.id for fact in ordered_facts],
                    source_types=source_types,
                    confidence=_aggregate_support_confidence(ordered_facts),
                    observed_at=min(fact.observed_at for fact in ordered_facts),
                    latest_observed_at=max(fact.observed_at for fact in ordered_facts),
                    expired=all(is_fact_expired(fact) for fact in ordered_facts),
                    expires_at=support_expires_at,
                    predicate_semantics="durable",
                    support_kind="aggregate",
                )
            )
    return supports


def _aggregate_support_confidence(facts: Iterable[Fact]) -> float:
    independent_support: dict[tuple[str, ...], float] = {}
    for fact in facts:
        identity = _support_identity(fact)
        adjusted_confidence = fact.confidence * _SOURCE_SUPPORT_WEIGHT[fact.source_type]
        independent_support[identity] = max(
            independent_support.get(identity, 0.0), adjusted_confidence
        )

    unsupported_probability = 1.0
    for confidence in independent_support.values():
        unsupported_probability *= 1.0 - confidence
    return round(min(1.0, 1.0 - unsupported_probability), 6)


def _support_identity(fact: Fact) -> tuple[str, ...]:
    if fact.evidence_ids:
        return ("evidence", *sorted(fact.evidence_ids))
    return ("fact", fact.source_type, fact.id)


def _support_strength(source_types: Iterable[str]) -> float:
    return sum(_SOURCE_SUPPORT_WEIGHT[source_type] for source_type in set(source_types))


def _support_tie_key(support: FactSupport) -> tuple[Any, ...]:
    if support.predicate_semantics == "measurement":
        return (
            support.latest_observed_at,
            support.confidence,
            len(support.supporting_fact_ids),
        )
    return (support.confidence, len(support.supporting_fact_ids))


def _select_unambiguous_best_support(
    candidates: Iterable[FactSupport],
) -> FactSupport | None:
    ordered = list(candidates)
    if not ordered:
        return None
    top_key = max(_support_tie_key(support) for support in ordered)
    top_supports = [
        support for support in ordered if _support_tie_key(support) == top_key
    ]
    if len(top_supports) != 1:
        return None
    return top_supports[0]


def _project_fact_conflicts(
    state: State, *, include_expired: bool = False
) -> list[FactConflict]:
    if not include_expired and not state.fact_supports:
        state.fact_supports = _project_fact_supports(state.facts.values())
    grouped: dict[tuple[str, str, str], list[Fact]] = {}
    for fact in state.facts.values():
        if not include_expired and is_fact_expired(fact):
            continue
        canonical_subject = state.alias_resolver.canonical(fact.subject_id)
        grouped.setdefault(
            (canonical_subject, fact.predicate, _dimensions_key(fact.dimensions)), []
        ).append(fact)

    conflicts: list[FactConflict] = []
    for (subject, predicate, _dimensions), facts in grouped.items():
        values_by_key: dict[str, Any] = {}
        for fact in facts:
            values_by_key.setdefault(_fact_value_key(fact.value), fact.value)
        if len(values_by_key) <= 1:
            continue

        best_fact = state.get_best_fact(
            subject,
            predicate,
            include_expired=include_expired,
            dimensions=facts[0].dimensions,
        )
        if best_fact is None:
            winning_value = None
            best_fact_id = None
            conflicting_fact_ids = [fact.id for fact in facts]
        else:
            winning_value = best_fact.value
            best_fact_id = best_fact.id
            conflicting_fact_ids = [
                fact.id
                for fact in facts
                if _fact_value_key(fact.value) != _fact_value_key(best_fact.value)
            ]
        conflicts.append(
            FactConflict(
                subject=subject,
                predicate=predicate,
                dimensions=dict(facts[0].dimensions),
                values=list(values_by_key.values()),
                winning_value=winning_value,
                best_fact_id=best_fact_id,
                conflicting_fact_ids=conflicting_fact_ids,
                reason=(
                    f"multiple values for {subject}/{predicate}: "
                    + ", ".join(str(value) for value in values_by_key.values())
                ),
            )
        )
    return conflicts


def _dimensions_key(dimensions: dict[str, str]) -> str:
    return json.dumps(dimensions, sort_keys=True, separators=(",", ":"))


def _fact_value_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def _project_entity_relationships(facts: Iterable[Fact]) -> list[EntityRelationship]:
    relationships: list[EntityRelationship] = []
    seen: set[tuple[str, str, str]] = set()
    for fact in facts:
        object_value = _relationship_object(fact.value)
        if object_value is None:
            continue
        key = (fact.subject_id, fact.predicate, object_value)
        if key in seen:
            continue
        seen.add(key)
        relationships.append(
            EntityRelationship(
                subject=fact.subject_id,
                predicate=fact.predicate,
                object=object_value,
                fact_id=fact.id,
                source_type=fact.source_type,
                confidence=fact.confidence,
                observed_at=fact.observed_at,
                evidence_ids=list(fact.evidence_ids),
                inferred=fact.inferred,
            )
        )
    return relationships


def _choose_canonical_alias_name(
    component: set[str], edges: list[tuple[str, str, Fact]]
) -> str:
    component_edges = [
        edge for edge in edges if edge[0] in component and edge[1] in component
    ]
    subject_names = {subject for subject, _alias, _fact in component_edges}

    def sort_key(name: str) -> tuple[int, int, int, str]:
        return (
            0 if name in subject_names and _looks_like_stable_hostname(name) else 1,
            0 if _looks_like_stable_hostname(name) else 1,
            len(name),
            name,
        )

    return min(component, key=sort_key)


def _looks_like_stable_hostname(name: str) -> bool:
    if not name or ":" in name or "/" in name:
        return False
    if _looks_like_ip_address(name):
        return False
    return any(character.isalpha() for character in name)


def _looks_like_ip_address(name: str) -> bool:
    parts = name.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def _subject_alias_matches(requested: str, stored: str) -> bool:
    if requested == stored:
        return True
    requested_short = requested.split(".", 1)[0]
    stored_short = stored.split(".", 1)[0]
    return requested == stored_short or requested_short == stored


def _relationship_payload(
    relationship: EntityRelationship, value_key: str
) -> dict[str, Any]:
    value = relationship.subject if value_key == "subject" else relationship.object
    return {
        value_key: value,
        "fact_id": relationship.fact_id,
        "source_type": relationship.source_type,
        "confidence": relationship.confidence,
        "observed_at": relationship.observed_at,
        "evidence_ids": list(relationship.evidence_ids),
        "inferred": relationship.inferred,
    }


def _relationship_object(value: Any) -> str | None:
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return None


def _dedupe(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))
