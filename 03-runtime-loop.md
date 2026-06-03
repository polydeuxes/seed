# 03 Runtime Loop

The runtime loop is the center of Seed.

## Loop overview

```text
1. Receive input.
2. Append input event.
3. Project current state.
4. Compose context packet.
5. Ask model for a structured decision.
6. Validate decision.
7. Handle decision branch without execution.
8. Append result or handoff events.
9. Re-project state.
10. Respond to user.
```

## Decision branches

The model may choose one of seven branches. None of them causes Seed to execute external work.

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

    decision = model_orchestrator.decide(context)

    decision_event = ledger.append(
        kind="model.decision.proposed",
        workspace_id=workspace_id,
        session_id=session_id,
        payload=decision.model_dump(),
        causation_id=model_event.id,
    )

    validated = decision_validator.validate(decision, state)
    if not validated.ok:
        ledger.append(
            kind="model.decision.invalid",
            payload=validated.error_payload(),
            causation_id=decision_event.id,
        )
        return response_composer.invalid_decision(validated)

    result = decision_handler.handle(validated.decision, state, causation_id=decision_event.id)

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

The model can then propose a verification HandoffPlan or request a missing ToolNeed.

## Model correction loop

If the model emits invalid JSON or invalid decisions:

1. record invalid decision event
2. optionally send validation error back to model
3. retry with strict budget
4. if still invalid, ask user or return safe fallback

Never silently coerce a dangerous invalid decision into an action.

## Runtime invariants

- No actual execution in Seed.
- No credentials, retries, scheduling, or long-running job lifecycle in Seed.
- No HandoffPlan without CapabilityCatalog metadata and policy summary.
- No generated capability metadata before validation and registration.
- No durable state mutation without an event.
- No hidden model memory; memory is state plus ledger.
- No route-specific shortcut around the runtime loop for core actions.
