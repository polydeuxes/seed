"""State projection from append-only events."""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Literal

from seed_runtime.events import EventLedger
from seed_runtime.execution_status import (
    ExecutionStatusConsumer,
    ProgressCadence,
    emit_progress_if_due,
)
from seed_runtime.evidence import Evidence
from seed_runtime.inference_catalog import InferenceCatalog
from seed_runtime.inference_rules import infer_facts
from seed_runtime.facts import (
    StaleFactRefreshRecommendation,
    is_fact_expired,
    is_measurement_predicate,
    recommended_capability_for_stale_fact,
)
from seed_runtime.entity_type_catalog import EntityTypeCatalog
from seed_runtime.predicate_catalog import PredicateCatalog
from seed_runtime.relationship_catalog import (
    RelationshipCatalog,
    RelationshipDefinition,
    RelationshipKind,
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


@dataclass(frozen=True)
class _AffectedScope:
    """Implementation-local description of the projected state touched by an event."""

    collection: str
    identity: str | None = None
    subject_id: str | None = None


@dataclass(frozen=True)
class _AffectedProjectionSet:
    """Implementation-local derived projections that may read an affected scope."""

    names: tuple[str, ...]


@dataclass(frozen=True)
class _ProjectionInfluenceLineage:
    """Implementation-local evidence for why a projection may need rebuilding.

    The lineage preserves source events, the direct state scopes they can touch,
    and the derived projection surfaces that may read those scopes. It is not a
    replay plan, cache dependency graph, invalidation policy, projection result,
    or read model.
    """

    source_event_ids: tuple[str, ...]
    affected_scopes: tuple[_AffectedScope, ...]
    affected_projections: _AffectedProjectionSet


@dataclass(frozen=True)
class _ReplayScopeAssessment:
    """Implementation-local assessment of replay necessity from lineage.

    Projection influence lineage is descriptive evidence for why projection work
    may be required. Replay scope assessment consumes that evidence to answer
    whether this compatible projector requires replay work. It does not select
    targets, execute replay, compute projections, invalidate caches, persist
    snapshots, or expose a runtime surface.
    """

    influence_lineage: _ProjectionInfluenceLineage
    replay_required: bool


@dataclass(frozen=True)
class _ReplaySelectionJustification:
    """Implementation-local justification for the compatible replay target set.

    Replay scope assessment determines whether replay is required from lineage
    evidence. Replay selection justification preserves why the compatible target
    set remains full event replay plus full finalization. It does not select,
    execute, narrow, schedule, invalidate, store, or compute replay work.
    """

    scope_assessment: _ReplayScopeAssessment
    compatible_replay_targets: tuple[str, ...]


@dataclass(frozen=True)
class _ReplaySelection:
    """Implementation-local replay target selection.

    Replay selection consumes a justification for the compatible target set and
    decides what this projector will execute. The current compatible choice
    remains full event replay plus full finalization whenever replay is assessed
    as required.
    """

    justification: _ReplaySelectionJustification
    replay_targets: tuple[str, ...]


@dataclass(frozen=True)
class _ReplayExecutionRequest:
    """Implementation-local request to execute an already selected replay."""

    selection: _ReplaySelection


@dataclass
class ProjectionBuildDiagnostics:
    """Optional, non-authoritative timings for projected-State construction."""

    timings: list[tuple[str, float]] = field(default_factory=list)
    counters: dict[str, int] = field(default_factory=dict)

    def timed(self, name: str, func: Callable[[], Any]) -> Any:
        started = time.perf_counter()
        try:
            return func()
        finally:
            elapsed = time.perf_counter() - started
            for index, (existing_name, existing_elapsed) in enumerate(self.timings):
                if existing_name == name:
                    self.timings[index] = (existing_name, existing_elapsed + elapsed)
                    break
            else:
                self.timings.append((name, elapsed))

    def add_count(self, name: str, amount: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + amount


def _parse_dt(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


@dataclass(frozen=True)
class EntityTypeAssertion:
    """One evidence-backed assertion that classifies an entity."""

    entity_id: str
    entity_type: str
    source: str
    confidence: float
    source_fact_id: str | None = None
    source_relationship_id: str | None = None
    reason: str = ""


@dataclass(frozen=True)
class EntityRelationship:
    """A catalog-defined semantic edge projected deterministically from a fact."""

    id: str
    subject: str
    relationship: str
    relationship_kind: RelationshipKind
    object: str
    source_fact_id: str
    source_type: str
    confidence: float
    observed_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphValidationIssue:
    """A suspicious or invalid projected relationship edge."""

    id: str
    severity: Literal["warning", "error"]
    subject: str
    relationship: str
    object: str
    relationship_ids: list[str]
    source_fact_ids: list[str]
    reason: str
    hint: str | None
    expected_subject_types: list[str]
    actual_subject_types: list[str]
    expected_object_types: list[str]
    actual_object_types: list[str]


@dataclass(frozen=True)
class LegacyEntityRelationship:
    """Backward-compatible direct string-fact projection."""

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

    return predicate in ALIAS_PREDICATES or (
        predicate.endswith("_instance") and predicate != "prometheus_instance"
    )


def _crosses_endpoint_identity_boundary(subject: str, alias: str) -> bool:
    """Return whether an alias would equate an endpoint with a non-endpoint."""

    return _looks_like_endpoint(subject) != _looks_like_endpoint(alias)


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
            if _crosses_endpoint_identity_boundary(fact.subject_id, alias):
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
    last_event_id: str | None = None
    projection_version: str = "v1"
    predicate_catalog: PredicateCatalog = field(
        default_factory=PredicateCatalog.load, compare=False, repr=False
    )
    entities: dict[str, Entity] = field(default_factory=dict)
    facts: dict[str, Fact] = field(default_factory=dict)
    observed_facts: dict[str, Fact] = field(default_factory=dict)
    inferred_facts: dict[str, Fact] = field(default_factory=dict)
    relationships: list[EntityRelationship] = field(default_factory=list)
    entity_relationships: list[LegacyEntityRelationship] = field(default_factory=list)
    entity_aliases: list[EntityAlias] = field(default_factory=list)
    entity_type_assertions: list[EntityTypeAssertion] = field(default_factory=list)
    graph_issues: list[GraphValidationIssue] = field(default_factory=list)
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

    def get_entity_type_assertions(
        self, entity_id: str | None = None
    ) -> list[EntityTypeAssertion]:
        """Return entity type assertions, optionally limited to one entity."""

        return [
            assertion
            for assertion in self.entity_type_assertions
            if entity_id is None or assertion.entity_id == entity_id
        ]

    def get_current_entity_types(self, entity_id: str) -> list[str]:
        """Return strongest supported types, preserving equal-rank ambiguity."""

        assertions = [
            assertion
            for assertion in self.entity_type_assertions
            if assertion.entity_id == entity_id and assertion.entity_type != "unknown"
        ]
        if not assertions:
            return ["unknown"]
        by_type: dict[str, list[EntityTypeAssertion]] = {}
        for assertion in assertions:
            by_type.setdefault(assertion.entity_type, []).append(assertion)
        ranks = {
            entity_type: (max(item.confidence for item in items), len(items))
            for entity_type, items in by_type.items()
        }
        best_rank = max(ranks.values())
        return sorted(
            entity_type for entity_type, rank in ranks.items() if rank == best_rank
        )

    @property
    def current_entity_types(self) -> dict[str, list[str]]:
        """Return current, potentially ambiguous classifications for all entities."""

        return {
            entity_id: self.get_current_entity_types(entity_id)
            for entity_id in sorted({a.entity_id for a in self.entity_type_assertions})
        }

    def get_graph_issues(
        self, severity: Literal["warning", "error"] | None = None
    ) -> list[GraphValidationIssue]:
        """Return graph validation issues, optionally filtered by severity."""

        return [
            issue
            for issue in self.graph_issues
            if severity is None or issue.severity == severity
        ]

    @property
    def open_tool_needs(self) -> list[ToolNeed]:
        closed = {"registered", "rejected"}
        return [need for need in self.tool_needs.values() if need.status not in closed]

    def get_relationships(
        self,
        subject: str | None = None,
        relationship: str | None = None,
        object: str | None = None,
        relationship_kind: RelationshipKind | None = None,
    ) -> list[EntityRelationship]:
        """Return catalog relationships matching all supplied filters."""

        return [
            edge
            for edge in self.relationships
            if (subject is None or edge.subject == subject)
            and (relationship is None or edge.relationship == relationship)
            and (object is None or edge.object == object)
            and (
                relationship_kind is None or edge.relationship_kind == relationship_kind
            )
        ]

    def find_dependencies(self, entity: str) -> list[str]:
        """Return entities reachable through dependency and hosting edges."""

        return self._traverse_relationships(entity, reverse=False)

    def find_dependents(self, entity: str) -> list[str]:
        """Return entities that reach this entity through dependency and hosting edges."""

        return self._traverse_relationships(entity, reverse=True)

    def _traverse_relationships(self, entity: str, *, reverse: bool) -> list[str]:
        traversable_kinds = {"dependency", "hosting"}
        found: list[str] = []
        seen = {entity}
        pending = [entity]
        while pending:
            current = pending.pop(0)
            for edge in self.relationships:
                source, target = (
                    (edge.object, edge.subject)
                    if reverse
                    else (edge.subject, edge.object)
                )
                if (
                    source == current
                    and edge.relationship_kind in traversable_kinds
                    and target not in seen
                ):
                    seen.add(target)
                    found.append(target)
                    pending.append(target)
        return found

    def find_subjects(self, relationship: str, object: str) -> list[str]:
        """Return deduplicated subjects connected to an object."""

        return _dedupe(
            edge.subject
            for edge in self.get_relationships(relationship=relationship, object=object)
        )

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
        self, subject: str, relationship: str, *, include_provenance: bool = False
    ) -> list[str] | list[dict[str, Any]]:
        """Return objects connected to a subject by a catalog relationship."""

        matches = self.get_relationships(subject=subject, relationship=relationship)
        if matches:
            if include_provenance:
                return [
                    {
                        "object": edge.object,
                        "source_fact_id": edge.source_fact_id,
                        "source_type": edge.source_type,
                        "confidence": edge.confidence,
                        "observed_at": edge.observed_at,
                        "metadata": dict(edge.metadata),
                    }
                    for edge in matches
                ]
            return _dedupe(edge.object for edge in matches)
        # Preserve the earlier direct-fact query behavior for callers using it.
        legacy_matches = [
            edge
            for edge in self.entity_relationships
            if edge.subject == subject and edge.predicate == relationship
        ]
        if include_provenance:
            return [_relationship_payload(edge, "object") for edge in legacy_matches]
        return _dedupe(edge.object for edge in legacy_matches)

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

    def get_current_facts(
        self,
        subject: str,
        predicate: str,
        *,
        include_expired: bool = False,
        resolve_aliases: bool = True,
        dimensions: dict[str, str] | None = None,
    ) -> list[Fact]:
        """Return all current facts allowed by the predicate's cardinality."""

        if not self.predicate_catalog.is_multi(predicate):
            best = self.get_best_fact(
                subject,
                predicate,
                include_expired=include_expired,
                resolve_aliases=resolve_aliases,
                dimensions=dimensions,
            )
            return [best] if best is not None else []

        current: list[Fact] = []
        for support in self.get_fact_supports(
            subject,
            predicate,
            include_expired=include_expired,
            resolve_aliases=resolve_aliases,
            dimensions=dimensions,
        ):
            representatives = [
                self.facts[fact_id]
                for fact_id in support.supporting_fact_ids
                if fact_id in self.facts
                and (include_expired or not is_fact_expired(self.facts[fact_id]))
            ]
            if representatives:
                current.append(
                    max(
                        representatives,
                        key=lambda fact: (
                            fact.confidence,
                            not fact.inferred,
                            fact.observed_at,
                            fact.id,
                        ),
                    )
                )
        return sorted(current, key=lambda fact: _fact_value_key(fact.value))

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
        if predicate in _ENDPOINT_SCOPED_PREDICATES:
            resolve_aliases = False
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

    __seed_arch__ = {
        "owner": "state_projection",
        "layer": "state",
        "summary": "Rebuilds inspectable state by applying ledger events and deriving projection indexes.",
        "edges": [
            {"to": "EventLedger", "label": "reads append-only events"},
            {"to": "GraphValidator", "label": "validates projected graph"},
            {"to": "State", "label": "produces projected state"},
        ],
    }

    def __init__(
        self,
        ledger: EventLedger,
        *,
        measurement_history_limit: int = 1,
        relationship_catalog: RelationshipCatalog | None = None,
        entity_type_catalog: EntityTypeCatalog | None = None,
        predicate_catalog: PredicateCatalog | None = None,
        inference_catalog: InferenceCatalog | None = None,
    ) -> None:
        if measurement_history_limit < 1:
            raise ValueError("measurement_history_limit must be at least 1")
        self.ledger = ledger
        self.measurement_history_limit = measurement_history_limit
        self.relationship_catalog = relationship_catalog or RelationshipCatalog.load()
        self.entity_type_catalog = entity_type_catalog or EntityTypeCatalog.load()
        self.predicate_catalog = predicate_catalog or PredicateCatalog.load()
        self.inference_catalog = inference_catalog or InferenceCatalog.load()

    def project(
        self,
        workspace_id: str,
        *,
        status_consumer: ExecutionStatusConsumer | None = None,
        diagnostics: ProjectionBuildDiagnostics | None = None,
    ) -> State:
        state = State(
            workspace_id=workspace_id, predicate_catalog=self.predicate_catalog
        )
        return self.project_from_state(
            state,
            self.ledger.list_events(workspace_id),
            status_consumer=status_consumer,
            status_phase="projection_replay",
            status_message="Projection replay",
            diagnostics=diagnostics,
        )

    def project_from_state(
        self,
        state: State,
        events: Iterable[Event],
        *,
        status_consumer: ExecutionStatusConsumer | None = None,
        status_phase: str | None = None,
        status_message: str | None = None,
        diagnostics: ProjectionBuildDiagnostics | None = None,
    ) -> State:
        """Apply ledger events to a projected State, then rebuild derived indexes.

        This supports safe incremental projection from a previously validated
        snapshot. The supplied events must be the ledger events that follow the
        snapshot's ``last_event_id`` in ledger order; event history remains the
        authority and this method only reuses derived state as an optimization.
        """

        event_list = (
            diagnostics.timed(
                "projection input event materialization", lambda: list(events)
            )
            if diagnostics is not None
            else list(events)
        )
        total = len(event_list)
        if diagnostics is not None:
            diagnostics.add_count("projection events", total)
        cadence = ProgressCadence()
        state.predicate_catalog = self.predicate_catalog

        def replay_events() -> None:
            for index, event in enumerate(event_list, start=1):
                state.last_event_id = event.id
                if diagnostics is not None:
                    diagnostics.add_count(f"projection event kind: {event.kind}")
                self.apply(state, event, diagnostics=diagnostics)
                if status_phase is not None and status_message is not None:
                    emit_progress_if_due(
                        status_consumer,
                        cadence,
                        status_phase,
                        status_message,
                        current=index,
                        total=total,
                    )

        influence_lineage = _recover_projection_influence_lineage(event_list)
        replay_assessment = _assess_replay_scope(influence_lineage)
        replay_justification = _justify_replay_selection(replay_assessment)
        replay_selection = _select_replay_targets(replay_justification)
        replay_request = _ReplayExecutionRequest(selection=replay_selection)
        return _execute_replay_selection(
            replay_request,
            replay_events=lambda: (
                diagnostics.timed("event replay", replay_events)
                if diagnostics is not None
                else replay_events()
            ),
            finalize=lambda: self.finalize(state, diagnostics=diagnostics),
        )

    def finalize(
        self, state: State, *, diagnostics: ProjectionBuildDiagnostics | None = None
    ) -> State:
        """Rebuild derived projection indexes after event application."""

        timed = (
            diagnostics.timed if diagnostics is not None else lambda _name, func: func()
        )
        timed(
            "finalization: initial alias projection",
            lambda: setattr(
                state, "alias_resolver", AliasResolver(state.facts.values())
            ),
        )
        all_measurement_evidence_ids = timed(
            "finalization: measurement evidence scan",
            lambda: {
                evidence_id
                for fact in state.facts.values()
                if is_measurement_predicate(fact.predicate)
                for evidence_id in fact.evidence_ids
            },
        )
        state.facts = timed(
            "finalization: measurement history retention before inference",
            lambda: _retain_projected_measurement_history(
                state.facts.values(),
                subject_key=lambda fact: _projection_subject(
                    fact, state.alias_resolver.canonical
                ),
                limit=self.measurement_history_limit,
            ),
        )
        timed(
            "finalization: inferred fact projection",
            lambda: _project_inferred_facts(
                state, self.inference_catalog, self.predicate_catalog
            ),
        )
        timed(
            "finalization: post-inference alias projection",
            lambda: setattr(
                state, "alias_resolver", AliasResolver(state.facts.values())
            ),
        )
        state.facts = timed(
            "finalization: measurement history retention after inference",
            lambda: _retain_projected_measurement_history(
                state.facts.values(),
                subject_key=lambda fact: _projection_subject(
                    fact, state.alias_resolver.canonical
                ),
                limit=self.measurement_history_limit,
            ),
        )
        state.observed_facts = timed(
            "finalization: observed/inferred fact partition",
            lambda: {
                fact_id: fact
                for fact_id, fact in state.facts.items()
                if not fact.inferred
            },
        )
        state.inferred_facts = timed(
            "finalization: inferred fact partition",
            lambda: {
                fact_id: fact for fact_id, fact in state.facts.items() if fact.inferred
            },
        )
        timed(
            "finalization: measurement provenance pruning",
            lambda: _prune_projected_measurement_provenance(
                state, all_measurement_evidence_ids
            ),
        )
        state.fact_supports = timed(
            "finalization: fact support construction",
            lambda: _project_fact_supports(state.facts.values()),
        )
        state.entity_relationships = timed(
            "finalization: legacy relationship projection",
            lambda: _project_entity_relationships(state.facts.values()),
        )
        state.relationships = timed(
            "finalization: catalog relationship projection",
            lambda: _project_catalog_relationships(
                state.facts.values(), self.relationship_catalog, state.evidence
            ),
        )
        state.entity_type_assertions = timed(
            "finalization: entity type assertion projection",
            lambda: _project_entity_type_assertions(state, self.entity_type_catalog),
        )
        state.graph_issues = timed(
            "finalization: graph issue construction",
            lambda: GraphValidator(
                self.relationship_catalog, self.entity_type_catalog
            ).validate(state),
        )
        state.entity_aliases = timed(
            "finalization: alias list materialization",
            lambda: state.alias_resolver.aliases,
        )
        state.fact_conflicts = timed(
            "finalization: fact conflict handling",
            lambda: _project_fact_conflicts(state),
        )
        if diagnostics is not None:
            diagnostics.counters.update(
                {
                    "entities": len(state.entities),
                    "facts": len(state.facts),
                    "observed facts": len(state.observed_facts),
                    "inferred facts": len(state.inferred_facts),
                    "fact supports": len(state.fact_supports),
                    "catalog relationships": len(state.relationships),
                    "legacy relationships": len(state.entity_relationships),
                    "entity aliases": len(state.entity_aliases),
                    "entity type assertions": len(state.entity_type_assertions),
                    "graph issues": len(state.graph_issues),
                    "fact conflicts": len(state.fact_conflicts),
                    "evidence": len(state.evidence),
                    "observations": len(state.observations),
                }
            )
        return state

    def apply(
        self,
        state: State,
        event: Event,
        *,
        diagnostics: ProjectionBuildDiagnostics | None = None,
    ) -> None:
        affected_scope = _recover_affected_scope(event)
        affected_projections = _recover_affected_projections(affected_scope)
        influence_lineage = _ProjectionInfluenceLineage(
            source_event_ids=(event.id,),
            affected_scopes=(affected_scope,) if affected_scope is not None else (),
            affected_projections=affected_projections,
        )
        replay_assessment = _assess_replay_scope(influence_lineage)
        replay_justification = _justify_replay_selection(replay_assessment)
        _select_replay_targets(replay_justification)
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
            timed = (
                diagnostics.timed
                if diagnostics is not None
                else lambda _name, func: func()
            )

            def decode_fact() -> Fact:
                data = _normalize_fact_event_payload(payload, event)
                if event.kind == "fact.inferred":
                    data["inferred"] = True
                    data["source_type"] = "inferred"
                else:
                    data["inferred"] = False
                    if data.get("source_type") == "inferred":
                        data.pop("source_type")
                return Fact(**data)

            fact = timed("event replay: fact event decoding", decode_fact)
            state.facts[fact.id] = fact
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


def _recover_affected_scope(event: Event) -> _AffectedScope | None:
    """Return the direct projected-State scope an event application may touch.

    The report is implementation-local visibility only; projection replay still
    applies every event and finalizes all derived indexes exactly as before.
    """

    payload = event.payload
    if event.kind == "entity.upserted":
        data = payload.get("entity", payload)
        return _AffectedScope("entities", data.get("id"))
    if event.kind == "observation.observed":
        data = payload.get("observation", payload)
        return _AffectedScope("observations", data.get("id"))
    if event.kind == "evidence.observed":
        data = payload.get("evidence", payload)
        return _AffectedScope("evidence", data.get("id"))
    if event.kind in {"fact.observed", "fact.inferred"}:
        data = payload.get("fact", payload)
        return _AffectedScope(
            "facts", data.get("id"), data.get("subject_id") or data.get("subject")
        )
    if event.kind == "goal.created":
        data = payload.get("goal", payload)
        return _AffectedScope("goals", data.get("id"))
    if event.kind in {"tool_need.created", "tool_need.status_changed"}:
        data = payload.get("tool_need", payload)
        return _AffectedScope(
            "tool_needs", data.get("id") or payload.get("tool_need_id")
        )
    if event.kind == "approval.granted":
        data = payload.get("approval", payload)
        return _AffectedScope("approvals", data.get("id"), data.get("scope"))
    if event.kind == "execution_authorization.granted":
        data = payload.get("execution_authorization", payload)
        return _AffectedScope("execution_authorizations", data.get("id"))
    if event.kind == "execution_proposal.created":
        data = payload.get("execution_proposal", payload)
        return _AffectedScope("execution_proposals", data.get("id"))
    if event.kind == "handoff_plan.created":
        data = payload.get("handoff_plan", payload)
        return _AffectedScope("handoff_plans", data.get("id"))
    if event.kind in {
        "pending_action.created",
        "pending_action.status_changed",
        "pending_action.approved",
        "pending_action.completed",
        "pending_action.cancelled",
    }:
        data = payload.get("pending_action", payload)
        return _AffectedScope(
            "pending_actions", data.get("id") or payload.get("pending_action_id")
        )
    if event.kind in {
        "action_plan.created",
        "action_plan.approved",
        "action_plan.accepted",
        "action_plan.rejected",
        "action_plan.superseded",
    }:
        data = payload.get("action_plan", payload)
        return _AffectedScope(
            "action_plans", data.get("id") or payload.get("action_plan_id")
        )
    if event.kind == "tool.registered":
        data = payload.get("tool", payload)
        return _AffectedScope("tools", data.get("name"))
    return None


def _recover_affected_projections(
    affected_scope: _AffectedScope | None,
) -> _AffectedProjectionSet:
    """Return derived projection surfaces that may read an affected scope.

    This is implementation-local visibility only. It does not track
    dependencies, mark projections dirty, change cache invalidation, or alter
    replay/finalization behavior.
    """

    if affected_scope is None:
        return _AffectedProjectionSet(())
    if affected_scope.collection == "facts":
        return _AffectedProjectionSet(
            (
                "alias_resolver",
                "measurement_history",
                "observed_facts",
                "inferred_facts",
                "fact_supports",
                "entity_relationships",
                "relationships",
                "entity_type_assertions",
                "graph_issues",
                "entity_aliases",
                "fact_conflicts",
            )
        )
    if affected_scope.collection == "evidence":
        return _AffectedProjectionSet(
            ("relationships", "entity_type_assertions", "graph_issues")
        )
    return _AffectedProjectionSet(())


def _recover_projection_influence_lineage(
    events: Iterable[Event],
) -> _ProjectionInfluenceLineage:
    """Return implementation-local projection influence evidence for events.

    Lineage recovery composes existing affected-scope and affected-projection
    evidence. It does not select replay targets, compute projections, invalidate
    caches, persist snapshots, or expose a runtime surface.
    """

    source_event_ids: list[str] = []
    affected_scopes: list[_AffectedScope] = []
    affected_projection_names: list[str] = []
    seen_projection_names: set[str] = set()
    for event in events:
        source_event_ids.append(event.id)
        affected_scope = _recover_affected_scope(event)
        if affected_scope is None:
            continue
        affected_scopes.append(affected_scope)
        affected_projections = _recover_affected_projections(affected_scope)
        for name in affected_projections.names:
            if name not in seen_projection_names:
                seen_projection_names.add(name)
                affected_projection_names.append(name)
    return _ProjectionInfluenceLineage(
        source_event_ids=tuple(source_event_ids),
        affected_scopes=tuple(affected_scopes),
        affected_projections=_AffectedProjectionSet(tuple(affected_projection_names)),
    )


def _execute_replay_selection(
    request: _ReplayExecutionRequest,
    *,
    replay_events: Callable[[], None],
    finalize: Callable[[], State],
) -> State:
    """Execute a compatible full replay request selected by replay selection.

    Execution consumes the selected replay request, but does not reinterpret it
    into narrowing, scheduling, cache invalidation, or projection optimization.
    The only compatible target set remains full event replay followed by full
    projection finalization.
    """

    if request.selection.replay_targets != (
        "event_replay",
        "projection_finalization",
    ):
        raise ValueError("unsupported replay execution target selection")
    replay_events()
    return finalize()


def _assess_replay_scope(
    influence_lineage: _ProjectionInfluenceLineage,
) -> _ReplayScopeAssessment:
    """Return whether lineage requires compatible replay work.

    The assessment preserves lineage evidence and answers replay necessity only.
    It intentionally does not narrow compatible targets; the existing projector
    still requires replay for every projection build, including empty lineage.
    """

    return _ReplayScopeAssessment(
        influence_lineage=influence_lineage,
        replay_required=True,
    )


def _justify_replay_selection(
    scope_assessment: _ReplayScopeAssessment,
) -> _ReplaySelectionJustification:
    """Preserve why the compatible replay target set is selected.

    The justification keeps replay-necessity evidence adjacent to the existing
    compatible target set without selecting or executing that target set.
    """

    return _ReplaySelectionJustification(
        scope_assessment=scope_assessment,
        compatible_replay_targets=("event_replay", "projection_finalization"),
    )


def _select_replay_targets(
    justification: _ReplaySelectionJustification,
) -> _ReplaySelection:
    """Return the replay work this compatible projector will execute.

    The selected targets intentionally do not narrow replay execution. Replay
    selection justification is preserved as input evidence, while execution
    remains the established full event replay and full projection finalization
    path.
    """

    return _ReplaySelection(
        justification=justification,
        replay_targets=justification.compatible_replay_targets,
    )


def _project_inferred_facts(
    state: State,
    inference_catalog: InferenceCatalog,
    predicate_catalog: PredicateCatalog,
) -> None:
    state.observed_facts = {
        fact_id: fact for fact_id, fact in state.facts.items() if not fact.inferred
    }
    state.inferred_facts = {
        fact_id: fact for fact_id, fact in state.facts.items() if fact.inferred
    }
    current_observed_facts = _current_belief_source_facts(
        state, predicate_catalog, exclude_predicates={"availability_status"}
    )
    state.inferred_facts.update(
        infer_facts(
            current_observed_facts,
            inference_catalog,
            predicate_catalog,
            subject_key=state.alias_resolver.canonical,
        )
    )
    endpoint_availability = _current_belief_source_facts(
        state,
        predicate_catalog,
        include_predicates={"availability_status"},
        subject_key=lambda subject: subject,
        subject_filter=_looks_like_endpoint,
    )
    state.inferred_facts.update(
        infer_facts(endpoint_availability, inference_catalog, predicate_catalog)
    )
    state.facts = {**state.observed_facts}
    for fact_id, fact in state.inferred_facts.items():
        if fact_id not in state.facts:
            state.facts[fact_id] = fact


def _current_belief_source_facts(
    state: State,
    predicate_catalog: PredicateCatalog,
    *,
    include_predicates: set[str] | None = None,
    exclude_predicates: set[str] | None = None,
    subject_key: Callable[[str], str] | None = None,
    subject_filter: Callable[[str], bool] | None = None,
) -> list[Fact]:
    """Return one representative source fact per selected current belief."""

    facts = (
        fact
        for fact in state.observed_facts.values()
        if (include_predicates is None or fact.predicate in include_predicates)
        and (exclude_predicates is None or fact.predicate not in exclude_predicates)
        and (subject_filter is None or subject_filter(fact.subject_id))
    )
    supports = _project_fact_supports(
        facts, subject_key=subject_key or state.alias_resolver.canonical
    )
    grouped: dict[tuple[str, str], list[FactSupport]] = {}
    for support in supports:
        grouped.setdefault((support.subject, support.predicate), []).append(support)

    selected: list[FactSupport] = []
    for (_, predicate), candidates in sorted(grouped.items()):
        if predicate_catalog.is_multi(predicate):
            selected.extend(candidates)
            continue
        best = _select_unambiguous_best_support(candidates)
        if best is not None:
            selected.append(best)

    representatives: list[Fact] = []
    for support in selected:
        supporting_facts = [
            state.observed_facts[fact_id]
            for fact_id in support.supporting_fact_ids
            if fact_id in state.observed_facts
        ]
        if supporting_facts:
            representatives.append(
                max(
                    supporting_facts,
                    key=lambda fact: (
                        fact.confidence,
                        fact.observed_at,
                        fact.id,
                    ),
                )
            )
    return representatives


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


def _projection_subject(fact: Fact, canonical: Callable[[str], str]) -> str:
    """Keep endpoint-scoped facts separate from their host alias component."""

    if fact.predicate in _ENDPOINT_SCOPED_PREDICATES:
        return fact.subject_id
    return canonical(fact.subject_id)


def _retain_projected_measurement_history(
    facts: Iterable[Fact], *, subject_key: Callable[[Fact], str], limit: int
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
            subject_key(fact),
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
        # Retained measurement samples are history, not competing durable claims.
        # Their newest sample has already been selected by fact-support projection.
        if is_measurement_predicate(fact.predicate):
            continue
        if state.predicate_catalog.is_multi(fact.predicate):
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


_HOST_PREDICATES = {"ip_address", "ansible_host", "architecture", "os"}
_ENDPOINT_SCOPED_PREDICATES = {
    "availability_status",
    "health_status",
    "endpoint_role",
}
_ENDPOINT_SUBJECT = re.compile(r"^(?:\[[^]]+\]|[^:]+):[0-9]{1,5}$")


class GraphValidator:
    """Validate projected edges against relationship and entity type catalogs."""

    def __init__(
        self,
        relationship_catalog: RelationshipCatalog,
        entity_type_catalog: EntityTypeCatalog,
    ) -> None:
        self.relationship_catalog = relationship_catalog
        self.entity_type_catalog = entity_type_catalog

    def validate(self, state: State) -> list[GraphValidationIssue]:
        """Return deterministic issues for suspicious or invalid graph edges."""

        issues_by_key: dict[tuple[str, str, str, str, str], GraphValidationIssue] = {}
        for edge in state.relationships:
            definition = self.relationship_catalog.get(edge.relationship)
            if definition is None:
                continue
            if definition.relationship_kind == "identity":
                continue

            subject_types = state.get_current_entity_types(edge.subject)
            object_types = state.get_current_entity_types(edge.object)
            checks = [
                self._check_side(
                    state, edge, "subject", definition.subject_type, subject_types
                ),
                self._check_side(
                    state, edge, "object", definition.object_type, object_types
                ),
            ]
            failures = [check for check in checks if check is not None]
            if not failures:
                continue
            severity: Literal["warning", "error"] = (
                "error" if any(item[0] == "error" for item in failures) else "warning"
            )
            reason = "; ".join(item[1] for item in failures)
            key = (edge.subject, edge.relationship, edge.object, severity, reason)
            existing = issues_by_key.get(key)
            if existing is not None:
                issues_by_key[key] = replace(
                    existing,
                    relationship_ids=[*existing.relationship_ids, edge.id],
                    source_fact_ids=list(
                        dict.fromkeys([*existing.source_fact_ids, edge.source_fact_id])
                    ),
                )
                continue
            issues_by_key[key] = self._issue(
                edge,
                severity,
                reason,
                [definition.subject_type],
                [definition.object_type],
                subject_types,
                object_types,
            )
        return list(issues_by_key.values())

    def _check_side(
        self,
        state: State,
        edge: EntityRelationship,
        side: str,
        expected: str,
        actual: list[str],
    ) -> tuple[Literal["warning", "error"], str] | None:
        if expected == "entity":
            return None
        if self.entity_type_catalog.get(expected) is None:
            return "warning", f"{side} expects unknown catalog type {expected}"
        if actual == ["unknown"]:
            return "warning", f"{side} type is unknown; expected {expected}"
        if len(actual) > 1:
            independent = _current_entity_types_excluding_relationship(
                state, getattr(edge, side), edge.id
            )
            if (
                independent != ["unknown"]
                and len(independent) == 1
                and expected not in independent
            ):
                return "error", f"{side} type is {independent[0]}; expected {expected}"
            return (
                "warning",
                f"{side} type is ambiguous ({', '.join(actual)}); expected {expected}",
            )
        if actual[0] != expected:
            return "error", f"{side} type is {actual[0]}; expected {expected}"
        return None

    @staticmethod
    def _issue(
        edge: EntityRelationship,
        severity: Literal["warning", "error"],
        reason: str,
        expected_subject_types: list[str],
        expected_object_types: list[str],
        actual_subject_types: list[str],
        actual_object_types: list[str],
    ) -> GraphValidationIssue:
        identity = "\0".join(
            [edge.subject, edge.relationship, edge.object, severity, reason]
        )
        return GraphValidationIssue(
            id="graph_issue_" + hashlib.sha256(identity.encode()).hexdigest()[:24],
            severity=severity,
            subject=edge.subject,
            relationship=edge.relationship,
            object=edge.object,
            relationship_ids=[edge.id],
            source_fact_ids=[edge.source_fact_id],
            reason=reason,
            hint=(
                "Add inventory or alias evidence if this monitored endpoint should "
                "map to a known host."
                if edge.relationship == "monitored_by"
                and actual_subject_types == ["unknown"]
                else None
            ),
            expected_subject_types=expected_subject_types,
            actual_subject_types=actual_subject_types,
            expected_object_types=expected_object_types,
            actual_object_types=actual_object_types,
        )


def _current_entity_types_excluding_relationship(
    state: State, entity_id: str, relationship_id: str
) -> list[str]:
    """Select current types without circular support from the edge being validated."""

    assertions = [
        assertion
        for assertion in state.entity_type_assertions
        if assertion.entity_id == entity_id
        and assertion.entity_type != "unknown"
        and assertion.source_relationship_id != relationship_id
    ]
    if not assertions:
        return ["unknown"]
    by_type: dict[str, list[EntityTypeAssertion]] = {}
    for assertion in assertions:
        by_type.setdefault(assertion.entity_type, []).append(assertion)
    ranks = {
        entity_type: (max(item.confidence for item in items), len(items))
        for entity_type, items in by_type.items()
    }
    best_rank = max(ranks.values())
    return sorted(
        entity_type for entity_type, rank in ranks.items() if rank == best_rank
    )


_RELATIONSHIP_TYPE_RULES = {
    "member_of": ("object", "group"),
    "runs_on": ("subject", "service"),
    "monitored_by": ("object", "monitoring_system"),
    "provides": ("object", "capability"),
}


def _project_entity_type_assertions(
    state: State, catalog: EntityTypeCatalog
) -> list[EntityTypeAssertion]:
    """Derive deterministic, provenance-bearing entity classifications."""

    assertions: list[EntityTypeAssertion] = []
    entities = {entity.id for entity in state.entities.values()}
    for entity in sorted(state.entities.values(), key=lambda item: item.id):
        if entity.kind != "unknown" and catalog.get(entity.kind) is not None:
            assertions.append(
                EntityTypeAssertion(
                    entity_id=entity.id,
                    entity_type=entity.kind,
                    source="entity_projection",
                    confidence=entity.confidence,
                    reason="entity kind",
                )
            )
    endpoint_facts: dict[str, Fact] = {}
    for fact in sorted(state.facts.values(), key=lambda item: item.id):
        entities.add(fact.subject_id)
        if fact.predicate in _HOST_PREDICATES:
            assertions.append(
                _fact_type_assertion(fact, "host", f"subject has {fact.predicate}")
            )
        if _looks_like_endpoint(fact.subject_id):
            current = endpoint_facts.get(fact.subject_id)
            if current is None or fact.confidence > current.confidence:
                endpoint_facts[fact.subject_id] = fact
    assertions.extend(
        _fact_type_assertion(fact, "endpoint", "subject looks like host:port")
        for fact in endpoint_facts.values()
    )

    for relationship in state.relationships:
        entities.update((relationship.subject, relationship.object))
        rule = _RELATIONSHIP_TYPE_RULES.get(relationship.relationship)
        if rule is None:
            continue
        side, entity_type = rule
        entity_id = getattr(relationship, side)
        assertions.append(
            EntityTypeAssertion(
                entity_id=entity_id,
                entity_type=entity_type,
                source="relationship_projection",
                confidence=relationship.confidence,
                source_relationship_id=relationship.id,
                reason=f"{side} of {relationship.relationship}",
            )
        )

    known = {assertion.entity_id for assertion in assertions}
    for entity_id in sorted(entities - known):
        assertions.append(
            EntityTypeAssertion(
                entity_id=entity_id,
                entity_type="unknown",
                source="entity_type_projection",
                confidence=0.0,
                reason="no supported entity type derivation",
            )
        )
    for assertion in assertions:
        if catalog.get(assertion.entity_type) is None:
            raise ValueError(f"unknown projected entity type {assertion.entity_type!r}")
    return sorted(
        assertions,
        key=lambda item: (
            item.entity_id,
            item.entity_type,
            item.source_fact_id or "",
            item.source_relationship_id or "",
        ),
    )


def _fact_type_assertion(
    fact: Fact, entity_type: str, reason: str
) -> EntityTypeAssertion:
    return EntityTypeAssertion(
        entity_id=fact.subject_id,
        entity_type=entity_type,
        source="fact_projection",
        confidence=fact.confidence,
        source_fact_id=fact.id,
        reason=reason,
    )


def _looks_like_endpoint(subject: str) -> bool:
    if not _ENDPOINT_SUBJECT.fullmatch(subject):
        return False
    try:
        port = int(subject.rsplit(":", 1)[1])
    except ValueError:
        return False
    return 0 < port <= 65535


def _project_entity_relationships(
    facts: Iterable[Fact],
) -> list[LegacyEntityRelationship]:
    relationships: list[LegacyEntityRelationship] = []
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
            LegacyEntityRelationship(
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


def _suppresses_catalog_relationship(
    fact: Fact,
    definition: RelationshipDefinition,
    evidence: dict[str, Evidence],
) -> bool:
    if (
        fact.predicate == "endpoint_role" and definition.relationship == "provides"
    ) or (
        fact.predicate == "prometheus_instance"
        and definition.relationship == "monitored_by"
    ):
        return _has_prometheus_source_evidence(fact, evidence)
    return False


def _has_prometheus_source_evidence(fact: Fact, evidence: dict[str, Evidence]) -> bool:
    for evidence_id in fact.evidence_ids:
        item = evidence.get(evidence_id)
        if item is None:
            continue
        payload = item.payload
        metadata = payload.get("metadata")
        if not isinstance(metadata, dict):
            continue
        source_name = metadata.get("source_name") or metadata.get("source")
        if isinstance(source_name, str) and source_name.strip().lower() == "prometheus":
            return True
    return False


def _project_catalog_relationships(
    facts: Iterable[Fact],
    catalog: RelationshipCatalog,
    evidence: dict[str, Evidence] | None = None,
) -> list[EntityRelationship]:
    relationships: list[EntityRelationship] = []
    evidence_by_id = evidence or {}
    for fact in sorted(facts, key=lambda item: item.id):
        fact_object = _relationship_object(fact.value)
        if fact_object is None:
            continue
        for definition in catalog.for_predicate(fact.predicate):
            if _suppresses_catalog_relationship(fact, definition, evidence_by_id):
                continue
            object_value = definition.object or fact_object
            if definition.relationship == "alias_of" and (
                fact.subject_id == object_value
                or _crosses_endpoint_identity_boundary(fact.subject_id, object_value)
            ):
                continue
            identity = "\0".join(
                [fact.id, fact.subject_id, definition.relationship, object_value]
            )
            relationship_id = (
                "rel_" + hashlib.sha256(identity.encode()).hexdigest()[:24]
            )
            relationships.append(
                EntityRelationship(
                    id=relationship_id,
                    subject=fact.subject_id,
                    relationship=definition.relationship,
                    relationship_kind=definition.relationship_kind,
                    object=object_value,
                    source_fact_id=fact.id,
                    source_type=fact.source_type,
                    confidence=fact.confidence,
                    observed_at=fact.observed_at,
                    metadata={
                        "source_predicate": fact.predicate,
                        "subject_type": definition.subject_type,
                        "object_type": definition.object_type,
                        "dimensions": dict(fact.dimensions),
                        "evidence_ids": list(fact.evidence_ids),
                        "inferred": fact.inferred,
                    },
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
    if _crosses_endpoint_identity_boundary(requested, stored):
        return False
    requested_short = requested.split(".", 1)[0]
    stored_short = stored.split(".", 1)[0]
    return requested == stored_short or requested_short == stored


def _relationship_payload(
    relationship: LegacyEntityRelationship, value_key: str
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
