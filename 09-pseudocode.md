# 09 Pseudocode

This file sketches implementation structures. It is not intended to be copy-pasted as complete production code.

## Package layout

```text
seed_runtime/
  events.py
  state.py
  context.py
  decisions.py
  capability_catalog.py
  policy.py
  handoff_plans.py
  tool_needs.py
  api.py

seed_builder/
  models.py
  planner.py
  generator.py
  validator.py
  registry_import.py
```

## Models

```python
from dataclasses import dataclass, field
from typing import Any, Literal

EventKind = str
DecisionKind = Literal[
    "answer",
    "ask_question",
    "request_tool",
    "propose_action_plan",
    "propose_handoff_plan",
    "propose_state_patch",
    "refuse",
]

@dataclass(frozen=True)
class Event:
    id: str
    kind: EventKind
    workspace_id: str
    session_id: str | None
    actor: str
    timestamp: str
    payload: dict[str, Any]
    causation_id: str | None = None
    correlation_id: str | None = None

@dataclass
class Entity:
    id: str
    kind: str
    name: str
    aliases: list[str] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0

@dataclass
class Fact:
    id: str
    subject_id: str
    predicate: str
    value: Any
    source_event_id: str
    observed_at: str
    expires_at: str | None = None
    confidence: float = 1.0

@dataclass
class Goal:
    id: str
    workspace_id: str
    summary: str
    status: str
    facts: dict[str, Any] = field(default_factory=dict)
    open_questions: list[str] = field(default_factory=list)
    related_entities: list[str] = field(default_factory=list)

@dataclass
class ToolSpec:
    name: str
    summary: str
    toolkit_id: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    policy_action: str
    implementation: str
    status: str = "registered"
    visibility: str = "model_visible"
    examples: list[dict[str, Any]] = field(default_factory=list)

@dataclass
class ToolNeed:
    id: str
    workspace_id: str
    name: str
    capability: str
    summary: str
    reason: str
    status: str
    risk_hint: str | None = None
    desired_inputs: list[str] = field(default_factory=list)
    desired_outputs: list[str] = field(default_factory=list)
```

## Event ledger

```python
class EventLedger:
    def append(
        self,
        kind: str,
        workspace_id: str,
        payload: dict[str, Any],
        *,
        actor: str = "system",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> Event:
        event = Event(
            id=new_id("evt"),
            kind=kind,
            workspace_id=workspace_id,
            session_id=session_id,
            actor=actor,
            timestamp=now_iso(),
            payload=payload,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        self._store.insert(event)
        return event

    def list_workspace_events(self, workspace_id: str) -> list[Event]:
        return self._store.query(workspace_id=workspace_id)
```

## State projector

```python
@dataclass
class State:
    workspace_id: str
    goals: dict[str, Goal]
    entities: dict[str, Entity]
    facts: dict[str, Fact]
    tool_needs: dict[str, ToolNeed]
    approvals: dict[str, Any]

class StateProjector:
    def project(self, workspace_id: str) -> State:
        state = State(
            workspace_id=workspace_id,
            goals={},
            entities={},
            facts={},
            tool_needs={},
            approvals={},
        )
        for event in self.ledger.list_workspace_events(workspace_id):
            self.apply(state, event)
        return state

    def apply(self, state: State, event: Event) -> None:
        if event.kind == "entity.upserted":
            entity = Entity(**event.payload["entity"])
            state.entities[entity.id] = entity

        elif event.kind == "fact.observed":
            fact = Fact(**event.payload["fact"])
            state.facts[fact.id] = fact

        elif event.kind == "goal.created":
            goal = Goal(**event.payload["goal"])
            state.goals[goal.id] = goal

        elif event.kind == "tool_need.created":
            need = ToolNeed(**event.payload["tool_need"])
            state.tool_needs[need.id] = need
```

## Decision schemas

```python
@dataclass
class Decision:
    kind: DecisionKind
    reason: str
    message: str | None = None
    question: str | None = None
    tool: str | None = None
    arguments: dict[str, Any] | None = None
    tool_need: dict[str, Any] | None = None
    patches: list[dict[str, Any]] | None = None
    safe_alternative: str | None = None
```

## Context composer

```python
class ContextComposer:
    def compose(self, workspace_id: str, session_id: str, trigger_event: Event, state: State) -> dict[str, Any]:
        active_goal = self.goal_selector.select(trigger_event, state)
        entities = self.entity_selector.select(trigger_event, active_goal, state)
        facts = self.fact_selector.select(entities, active_goal, state)
        tools = self.tool_selector.select(trigger_event, active_goal, entities, state)
        open_needs = self.tool_need_selector.select(trigger_event, active_goal, state)

        return {
            "workspace": {"id": workspace_id},
            "trigger": trigger_event.payload,
            "active_goal": summarize_goal(active_goal),
            "entities": [summarize_entity(e) for e in entities],
            "facts": [summarize_fact(f) for f in facts],
            "available_tools": [summarize_tool(t) for t in tools],  # legacy field name; entries are registered operations
            "open_tool_needs": [summarize_tool_need(n) for n in open_needs],
            "decision_schema": DecisionSchemaV1.model_json_schema(),
        }
```

## ToolRegistry registered operation inventory

```python
class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register_toolkit(self, toolkit: ToolkitManifest, base_path: Path) -> None:
        for tool_def in toolkit.tools:
            spec = ToolSpec(
                name=tool_def.name,
                summary=tool_def.summary,
                toolkit_id=toolkit.id,
                input_schema=read_json(base_path / tool_def.input_schema),
                output_schema=read_json(base_path / tool_def.output_schema),
                policy_action=tool_def.policy_action,
                implementation=f"{base_path}:{tool_def.implementation}",
                visibility=tool_def.visibility,
            )
            self._tools[spec.name] = spec

    def require(self, name: str) -> ToolSpec:
        try:
            return self._tools[name]
        except KeyError:
            raise UnknownTool(name)

    def visible_for_context(self, state: State, entities: list[Entity], goal: Goal | None) -> list[ToolSpec]:
        return relevance_filter(self._tools.values(), state=state, entities=entities, goal=goal)
```

## Policy gate

```python
@dataclass
class PolicyDecision:
    decision: Literal["allow", "confirm", "approve", "block"]
    action: str
    risk: str
    reason: str
    scope: str | None = None

    @property
    def allowed(self) -> bool:
        return self.decision == "allow"

class PolicyGate:
    def evaluate(self, action: str, *, scope: str | None, actor: str, state: State, args: dict[str, Any]) -> PolicyDecision:
        rule = self.rules.get(action, self.default_rule)
        if rule.risk in {"L3", "L4"} and not self.approvals.has_current(action, scope, actor):
            return PolicyDecision("approve", action, rule.risk, rule.reason, scope)
        if rule.blocked:
            return PolicyDecision("block", action, rule.risk, rule.reason, scope)
        return PolicyDecision("allow", action, rule.risk, rule.reason, scope)
```

## Handoff planning

```python
class HandoffPlanner:
    def create(self, action_plan: ActionPlan, target: str, *, workspace_id: str, causation_id: str) -> HandoffPlan:
        state = self.projector.project(workspace_id)
        capability = self.capability_catalog.require(action_plan.capability)

        policy = self.policy.summarize(
            capability.policy_action,
            scope=target,
            actor=self.actor.current(),
            state=state,
        )

        if policy.decision == "block":
            return HandoffPlanResult.blocked(policy)

        provider = self.recommendation_ranker.choose_provider(capability, target, state)
        handoff = HandoffPlan(
            action_plan_id=action_plan.id,
            provider=provider.name,
            backend_type=provider.backend_type,
            operation=provider.operation,
            target=target,
            policy_summary=policy.summary,
            secret_boundary=provider.secret_boundary_summary,
            requires_external_approval=policy.requires_external_approval,
            executable=False,
        )

        self.ledger.append(
            "handoff_plan.created",
            workspace_id,
            {"handoff_plan": handoff.to_payload()},
            causation_id=causation_id,
        )

        return handoff
```

No execution happens here. External providers own credentials, retries, schedules, and long-running jobs.


## Runtime handler

```python
class Runtime:
    def handle_user_message(self, workspace_id: str, session_id: str, text: str) -> Response:
        input_event = self.ledger.append(
            "input.user_message",
            workspace_id,
            {"text": text},
            actor="user",
            session_id=session_id,
        )

        state = self.projector.project(workspace_id)
        context = self.context_composer.compose(workspace_id, session_id, input_event, state)
        decision_text = self.model.decide(context)
        decision = self.decision_parser.parse(decision_text)

        decision_event = self.ledger.append(
            "model.decision.proposed",
            workspace_id,
            {"decision": decision.__dict__},
            actor="model",
            session_id=session_id,
            causation_id=input_event.id,
        )

        validation = self.decision_validator.validate(decision, state)
        if not validation.ok:
            return self.handle_invalid_decision(validation, decision_event)

        result = self.decision_router.route(decision, workspace_id, session_id, decision_event.id)
        return self.response_composer.compose(result)
```

## ToolNeed / capability-gap service

```python
class ToolNeedService:
    def create_from_decision(self, workspace_id: str, decision: Decision, causation_id: str) -> ToolNeed:
        payload = decision.tool_need or {}
        need = ToolNeed(
            id=new_id("need"),
            workspace_id=workspace_id,
            name=slugify(payload["name"]),
            capability=slugify(payload.get("capability", payload["name"])),
            summary=payload["summary"],
            reason=decision.reason,
            status="proposed",
            risk_hint=payload.get("risk_hint"),
            desired_inputs=payload.get("desired_inputs", []),
            desired_outputs=payload.get("desired_outputs", []),
        )
        self.ledger.append(
            "tool_need.created",
            workspace_id,
            {"tool_need": need.__dict__},
            causation_id=causation_id,
        )
        return need
```

## Builder generator

```python
class ToolkitGenerator:
    def generate(self, need: ToolNeed) -> ToolkitCandidate:
        plan = self.planner.plan(need)
        files = {
            "toolkit.yaml": self.manifest_renderer.render(plan),
            **self.schema_renderer.render_all(plan),
            "operations.py": self.operation_renderer.render(plan),
            **self.test_renderer.render_all(plan),
            "docs.md": self.docs_renderer.render(plan),
            "generation_notes.md": self.notes_renderer.render(plan),
        }
        candidate = self.candidate_store.write(new_id("cand"), files)
        self.ledger.append("toolkit.candidate.generated", need.workspace_id, candidate.to_payload())
        return candidate
```

## Validator

```python
class ToolkitValidator:
    def validate(self, candidate: ToolkitCandidate) -> ValidationReport:
        checks = [
            self.check_manifest,
            self.check_schemas,
            self.check_policy_actions,
            self.check_implementation_refs,
            self.check_forbidden_imports,
            self.run_tests,
            self.run_sandbox_smoke_tests,
        ]
        results = []
        for check in checks:
            results.append(check(candidate))
        return ValidationReport(candidate_id=candidate.id, checks=results)
```

## First generated operation template

```python
from seed_runtime.tool_context import ToolContext


def install_ssh_server(ctx: ToolContext, host: str, package_manager: str = "auto", start_service: bool = True) -> dict:
    host_ref = ctx.entities.require("host", host)

    package_name = ctx.providers.packages.resolve_name(
        capability="ssh_server",
        os_family=host_ref.attributes.get("os_family"),
        package_manager=package_manager,
    )

    install_result = ctx.providers.packages.install(host_ref, package_name)

    service_result = None
    if start_service:
        service_name = ctx.providers.services.resolve_name(capability="ssh_server", os_family=host_ref.attributes.get("os_family"))
        ctx.providers.services.enable(host_ref, service_name)
        service_result = ctx.providers.services.start(host_ref, service_name)

    return {
        "ok": bool(install_result.ok and (service_result is None or service_result.ok)),
        "host": host_ref.name,
        "installed": bool(install_result.ok),
        "service_running": bool(service_result.ok) if service_result else None,
        "changed": bool(install_result.changed or (service_result and service_result.changed)),
        "summary": f"SSH server install {'succeeded' if install_result.ok else 'failed'} on {host_ref.name}.",
        "evidence": {
            "package": install_result.to_public_dict(),
            "service": service_result.to_public_dict() if service_result else None,
        },
    }
```
