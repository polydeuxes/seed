# 03 Runtime Loop

The runtime loop is the center of Seed. Seed is closer to a state engine / distributed state machine than an agent framework: a provider proposes a structured decision, but the runtime owns validation, policy boundaries, registered-handler execution, and append-only events.

## Loop overview

```text
Input
  -> EventLedger
  -> State Projection
  -> Context Composer
  -> DecisionProvider
  -> Decision Validation
  -> PolicyEngine
  -> ToolRegistry or Answer
  -> New Events
```

Runtime sovereignty:

1. Receive input and append an input event.
2. Project current state, optionally using `ProjectionStore` snapshot caching.
3. Compose the context packet and deterministic context hash.
4. Ask a `DecisionProvider` for a structured decision. The provider can be deterministic code or a model adapter; LLMs are not required.
5. Reject malformed decisions before policy or tool execution.
6. Evaluate valid tool decisions with `PolicyEngine`. Policy denial prevents tool execution.
7. Execute only registered `ToolRegistry` handlers, or return an answer. Raw provider output is never executed.
8. Append runtime outcome events and Decision Journal events.
9. Re-project state as needed and respond to the user.

## Decision branches

The broader runtime model supports answer/question/tool-need/plan/handoff/state-patch/refusal branches. RuntimeLoop v1 focuses on answers and registered tool calls: answers are recorded directly, and tool calls must pass validation, registry lookup, and policy before a registered handler can run. Seed never runs shell commands, subprocesses, network calls, generated code, or arbitrary provider output as part of Decision Journal v1.

### 1. Answer

Use when available context is enough.

```json
{
  "kind": "answer",
  "message": "Docker storage was last checked 2 hours ago and showed 87% usage. The fact is stale, so I should re-check before recommending cleanup."
}
```

### 2. Ask question

Use when required information is missing.

```json
{
  "kind": "ask_question",
  "question": "Which host should I check?",
  "missing_fields": ["host"]
}
```

### 3. Request ToolNeed

Use when the system lacks a needed capability or provider handoff target.

```json
{
  "kind": "request_tool",
  "reason": "The user wants SSH installed, but no registered capability/backend handoff exists.",
  "tool_need": {
    "name": "install_ssh_server",
    "capability": "ssh_access",
    "summary": "Install and start OpenSSH server on a Linux host.",
    "risk_hint": "mutating",
    "desired_inputs": ["host"],
    "desired_outputs": ["installed", "service_running", "verification_hint"]
  }
}
```

### 4. Propose ActionPlan

Use when Seed can produce a durable, text-only plan that a user can accept, reject, or supersede.

```json
{
  "kind": "propose_action_plan",
  "action_plan": {
    "tool_need_id": "need_ssh",
    "provider": "awx-prod",
    "capability": "ssh_access",
    "summary": "Use AWX to install and start OpenSSH on node-1.",
    "steps": ["Confirm node-1", "Launch AWX job template", "Review provider evidence"],
    "risk_class": "L3",
    "requires_approval": true,
    "executable": false
  }
}
```

### 5. Propose HandoffPlan

Use when an accepted ActionPlan can be handed to an external provider. The plan must remain non-executable inside Seed.

```json
{
  "kind": "propose_handoff_plan",
  "handoff_plan": {
    "action_plan_id": "plan_ssh",
    "provider": "awx-prod",
    "backend_type": "ansible",
    "operation": "ssh.install",
    "target": "host:node-1",
    "policy_summary": "Operator approval required in AWX before host mutation.",
    "secret_boundary": "AWX/Vault/ssh-agent own credentials, prompts, retries, and job lifecycle.",
    "requires_external_approval": true,
    "executable": false
  }
}
```

### 6. Propose state patch

Use for non-executable state updates, such as recognizing a named host or goal.

```json
{
  "kind": "propose_state_patch",
  "patches": [
    {
      "op": "upsert_entity",
      "entity": {
        "kind": "host",
        "name": "node-1"
      }
    }
  ],
  "reason": "The user named a host not yet in state."
}
```

### 7. Refuse or block

Use when the request is unsafe, impossible, or prohibited.

```json
{
  "kind": "refuse",
  "reason": "I cannot run arbitrary shell commands or execute external work from Seed.",
  "safe_alternative": "I can create a ToolNeed or HandoffPlan for an external provider such as AWX, MCP, Temporal/Prefect, or a manual runbook."
}
```

## Decision Journal

Decision Journal is an append-only event layer, not a separate mutable decision database. It records a `decision.recorded` event containing:

- `decision_id` and `run_id`
- workspace and decision kind
- provider reason
- deterministic `context_hash` of the context the provider saw
- selected tool name and arguments when present
- policy allowed/denied status
- final outcome: `answered`, `tool_succeeded`, `tool_failed`, `tool_unknown`, `policy_denied`, or `malformed_decision`
- error details when a decision is malformed, a tool is unknown, policy denies, or a handler fails

This journal explains why a path was chosen and what happened afterward. It prepares Seed for `--why`, `--impact`, `--state-summary`, `--relationships`, `--graph-issues`, audit/explain views, and verification commands while preserving `EventLedger` as the source of truth. If an outcome changes after a proposal, Seed appends another event instead of mutating a prior event.

## Runtime algorithm

```python
def handle_input(workspace_id: str, session_id: str, input_payload: dict) -> Response:
    input_event = ledger.append(
        kind="input.received",
        workspace_id=workspace_id,
        session_id=session_id,
        payload=input_payload,
    )

    state = projector.project(workspace_id)

    context = context_composer.compose(
        workspace_id=workspace_id,
        session_id=session_id,
        trigger_event_id=input_event.id,
        state=state,
    )

    model_event = ledger.append(
        kind="model.context_presented",
        workspace_id=workspace_id,
        session_id=session_id,
        payload={"context_packet_id": context.id},
        causation_id=input_event.id,
    )

    context_hash = decision_journal.context_hash(context)
    decision = decision_provider.decide(context)

    decision_event = ledger.append(
        kind="model.decision.proposed",
        workspace_id=workspace_id,
        session_id=session_id,
        payload=decision.model_dump(),
        causation_id=model_event.id,
    )

    validated = decision_validator.validate(decision, state)
    if not validated.ok:
        invalid_event = ledger.append(
            kind="model.decision.invalid",
            payload=validated.error_payload(),
            causation_id=decision_event.id,
        )
        decision_journal.append_record(
            decision_kind=decision.kind,
            reason=decision.reason,
            context_hash=context_hash,
            policy_allowed=False,
            outcome="malformed_decision",
            error=validated.error_text,
            causation_id=invalid_event.id,
        )
        return response_composer.invalid_decision(validated)

    result = runtime_loop.route_valid_decision(validated.decision, state, context_hash, causation_id=decision_event.id)

    final_state = projector.project(workspace_id)
    return response_composer.compose(result, final_state)
```

## Decision handling algorithm

```python
def handle_decision(decision: Decision, state: State, causation_id: str) -> DecisionResult:
    match decision.kind:
        case "answer":
            ledger.append("response.answer.created", decision.payload, causation_id=causation_id)
            return AnswerResult(message=decision.message)

        case "ask_question":
            ledger.append("response.question.created", decision.payload, causation_id=causation_id)
            return QuestionResult(question=decision.question)

        case "propose_state_patch":
            patches = state_patch_validator.validate(decision.patches, state)
            ledger.append("state.patch.applied", patches.to_event_payload(), causation_id=causation_id)
            return StatePatchResult(patches=patches)

        case "request_tool":
            need = tool_need_service.create(decision.tool_need, causation_id=causation_id)
            return ToolNeedResult(tool_need=need)

        case "propose_action_plan":
            plan = action_plan_service.create_plan(decision.action_plan, causation_id=causation_id)
            return ActionPlanResult(action_plan=plan)

        case "propose_handoff_plan":
            handoff = handoff_service.create_handoff(decision.handoff_plan, causation_id=causation_id)
            return HandoffPlanResult(handoff_plan=handoff)

        case "refuse":
            ledger.append("response.refusal.created", decision.payload, causation_id=causation_id)
            return RefusalResult(reason=decision.reason)
```

## Handoff branch

Seed does not invoke a tool after policy review. It creates a non-executable HandoffPlan that an external provider can consume or that a human can follow manually. The HandoffPlan is not an approval and does not imply user approval, execution authorization, credential availability, provider trust, or tool registration.

```python
def create_handoff_plan(action_plan: ActionPlan, target: str, causation_id: str) -> HandoffPlanResult:
    capability = capability_catalog.require(action_plan.capability)

    policy = policy_gate.summarize(
        action=capability.policy_action,
        scope=target,
        actor=current_actor(),
        state=current_state(),
    )

    provider = recommendation_ranker.choose_provider(
        capability=capability,
        preferred_backends=["ansible", "mcp", "temporal", "manual"],
        state=current_state(),
    )

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

    ledger.append("handoff_plan.created", {"handoff_plan": handoff.model_dump()}, causation_id=causation_id)
    return HandoffPlanResult.created(handoff)
```

External providers own actual execution, credentials, retries, scheduling, long-running jobs, and credential prompts. Preferred backends are Ansible/AWX for host automation, Temporal/Prefect for workflows, MCP servers for tool integration, and Vault/ssh-agent/sudo/become for secrets and privilege boundaries.


## Provider result ingestion loop

After an external provider completes work outside Seed, Seed may ingest a reported result as Evidence. The result should be recorded in the Event Ledger, projected into Facts where appropriate, and then exposed through normal context composition.

For LLM-facing user experiences, prefer this path:

```text
user input -> Seed proposes HandoffPlan -> external provider executes outside Seed -> provider result is ingested as Evidence -> state projects facts -> model explains result
```

## Handling ambiguity

Do not let the model guess high-impact missing arguments.

Rules:

- Low-risk read-only handoff recommendations may use high-confidence entity inference.
- Mutating tools require explicit scope.
- Unknown host/environment requires clarification.
- Tool generation requests should capture uncertainty in the Tool Need.

## Handling stale facts

Facts should include freshness metadata.

Context composer can mark facts:

```json
{
  "predicate": "docker.storage.used_percent",
  "value": 87,
  "freshness": "stale",
  "observed_at": "2026-06-01T08:00:00Z"
}
```

The model can then propose an observation HandoffPlan whose returned evidence becomes supporting or conflicting Facts, or request a missing ToolNeed.

## Model correction loop

If the model emits invalid JSON or invalid decisions:

1. record invalid decision event
2. optionally send validation error back to model
3. retry with strict budget
4. if still invalid, ask user or return safe fallback

Never silently coerce a dangerous invalid decision into an action.

## Runtime invariants

- RuntimeLoop is the coordinator; it does not own policy, projection storage, tool registration, or journal persistence responsibilities.
- EventLedger is the historical event source.
- ProjectionStore only caches projected state snapshots.
- DecisionProvider proposes; it does not execute.
- Decision validation happens before policy or tool execution.
- PolicyEngine denial prevents tool execution.
- ToolRegistry executes only registered handlers; raw provider output, shell commands, subprocesses, generated tools, and arbitrary host mutation are not execution paths.
- DecisionJournal records reasoning and outcomes as append-only events only.
- No credentials, retries, scheduling, or long-running job lifecycle in Seed.
- No HandoffPlan without CapabilityCatalog metadata and policy summary.
- No generated capability metadata before validation and registration.
- No durable state mutation without an event.
- No hidden model memory; memory is state plus ledger.
- No route-specific shortcut around the runtime loop for core actions.
