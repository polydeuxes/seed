"""State projection from append-only events."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable

from seed_runtime.events import EventLedger
from seed_runtime.evidence import Evidence
from seed_runtime.inference_rules import infer_facts
from seed_runtime.models import (
    ActionPlan,
    Approval,
    Entity,
    Event,
    ExecutionAuthorization,
    Fact,
    FactConflict,
    Goal,
    HandoffPlan,
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


@dataclass
class State:
    workspace_id: str
    entities: dict[str, Entity] = field(default_factory=dict)
    facts: dict[str, Fact] = field(default_factory=dict)
    observed_facts: dict[str, Fact] = field(default_factory=dict)
    inferred_facts: dict[str, Fact] = field(default_factory=dict)
    entity_relationships: list[EntityRelationship] = field(default_factory=list)
    fact_conflicts: list[FactConflict] = field(default_factory=list)
    evidence: dict[str, Evidence] = field(default_factory=dict)
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

    def get_best_fact(self, subject: str, predicate: str) -> Fact | None:
        """Return the highest-confidence fact for a subject and predicate."""
        candidates = [
            fact
            for fact in self.facts.values()
            if fact.subject_id == subject and fact.predicate == predicate
        ]
        if not candidates:
            return None
        return max(
            candidates,
            key=lambda fact: (
                fact.confidence,
                not fact.inferred,
                fact.observed_at,
                fact.id,
            ),
        )

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

    def __init__(self, ledger: EventLedger) -> None:
        self.ledger = ledger

    def project(self, workspace_id: str) -> State:
        state = State(workspace_id=workspace_id)
        for event in self.ledger.list_events(workspace_id):
            self.apply(state, event)
        _project_inferred_facts(state)
        state.entity_relationships = _project_entity_relationships(
            state.facts.values()
        )
        state.fact_conflicts = _project_fact_conflicts(state)
        return state

    def apply(self, state: State, event: Event) -> None:
        payload = event.payload
        if event.kind == "entity.upserted":
            data = payload.get("entity", payload)
            entity = Entity(**data)
            state.entities[entity.id] = entity
        elif event.kind == "evidence.observed":
            data = payload.get("evidence", payload).copy()
            data["observed_at"] = _parse_dt(data.get("observed_at")) or event.timestamp
            evidence = Evidence(**data)
            state.evidence[evidence.id] = evidence
        elif event.kind == "fact.observed":
            data = payload.get("fact", payload).copy()
            data["observed_at"] = _parse_dt(data.get("observed_at")) or event.timestamp
            data["expires_at"] = _parse_dt(data.get("expires_at"))
            if "evidence_ids" not in data and "source_event_id" in data:
                data["evidence_ids"] = [data.pop("source_event_id")]
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
            data["expires_at"] = (
                _parse_dt(data.get("expires_at")) or event.timestamp
            )
            authorization = ExecutionAuthorization(**data)
            state.execution_authorizations[authorization.id] = authorization
            proposal = state.execution_proposals.get(authorization.execution_proposal_id)
            if (
                proposal is not None
                and proposal.action_plan_id == authorization.action_plan_id
                and proposal.tool_name == authorization.tool_name
                and proposal.arguments_fingerprint == authorization.arguments_fingerprint
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
                update = {"status": payload.get("status", event.kind.rsplit(".", 1)[-1])}
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
    state.inferred_facts = infer_facts(state.observed_facts.values())
    state.facts = {**state.observed_facts}
    for fact_id, fact in state.inferred_facts.items():
        if fact_id not in state.facts:
            state.facts[fact_id] = fact


def _project_fact_conflicts(state: State) -> list[FactConflict]:
    grouped: dict[tuple[str, str], list[Fact]] = {}
    for fact in state.facts.values():
        grouped.setdefault((fact.subject_id, fact.predicate), []).append(fact)

    conflicts: list[FactConflict] = []
    for (subject, predicate), facts in grouped.items():
        values_by_key: dict[str, Any] = {}
        for fact in facts:
            values_by_key.setdefault(_fact_value_key(fact.value), fact.value)
        if len(values_by_key) <= 1:
            continue

        best_fact = state.get_best_fact(subject, predicate)
        if best_fact is None:
            continue
        conflicts.append(
            FactConflict(
                subject=subject,
                predicate=predicate,
                values=list(values_by_key.values()),
                best_fact_id=best_fact.id,
                conflicting_fact_ids=[
                    fact.id
                    for fact in facts
                    if _fact_value_key(fact.value) != _fact_value_key(best_fact.value)
                ],
                reason=(
                    f"multiple values for {subject}/{predicate}: "
                    + ", ".join(str(value) for value in values_by_key.values())
                ),
            )
        )
    return conflicts


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
