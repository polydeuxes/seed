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
7. Execute decision branch.
8. Append result events.
9. Re-project state.
10. Respond to user.
```

## Decision branches

The model may choose one of six branches.

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

### 3. Call tool

Use when a registered tool can answer or advance the goal.

```json
{
  "kind": "call_tool",
  "tool": "docker_storage_summary",
  "arguments": {
    "host": "node-1"
  },
  "reason": "The user asked whether node-1 is out of disk and the existing Docker storage fact is stale."
}
```

### 4. Request tool

Use when the system lacks a needed tool.

```json
{
  "kind": "request_tool",
  "reason": "The user wants SSH installed, but no registered install tool exists.",
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

### 5. Propose state patch

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

### 6. Refuse or block

Use when the request is unsafe, impossible, or prohibited.

```json
{
  "kind": "refuse",
  "reason": "I cannot run arbitrary shell commands without a registered tool and policy approval.",
  "safe_alternative": "I can create a Tool Need for a reviewed diagnostic command."
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

    result = decision_executor.execute(validated.decision, state, causation_id=decision_event.id)

    final_state = projector.project(workspace_id)
    return response_composer.compose(result, final_state)
```

## Decision execution algorithm

```python
def execute_decision(decision: Decision, state: State, causation_id: str) -> DecisionResult:
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

        case "call_tool":
            return tool_call_service.call(decision.tool, decision.arguments, causation_id=causation_id)

        case "refuse":
            ledger.append("response.refusal.created", decision.payload, causation_id=causation_id)
            return RefusalResult(reason=decision.reason)
```

## Tool call branch

```python
def call_tool(tool_name: str, arguments: dict, causation_id: str) -> ToolCallResult:
    tool = registry.require_tool(tool_name)

    args = schema_validator.validate(tool.input_schema, arguments)

    policy = policy_gate.evaluate(
        action=tool.policy_action,
        scope=args.scope(),
        actor=current_actor(),
        state=current_state(),
    )

    if policy.decision == "block":
        ledger.append("tool.policy.blocked", {"tool": tool_name, "policy": policy.model_dump()}, causation_id=causation_id)
        return ToolCallResult.blocked(policy)

    if policy.decision in {"confirm", "approve"}:
        approval_request = approvals.create(tool=tool, arguments=args, policy=policy)
        ledger.append("tool.approval.requested", approval_request.model_dump(), causation_id=causation_id)
        return ToolCallResult.waiting_for_approval(approval_request)

    call_event = ledger.append("tool.call.started", {"tool": tool_name, "arguments": args.redacted()}, causation_id=causation_id)

    raw_result = executor.invoke(tool, args)
    normalized = schema_validator.validate(tool.output_schema, raw_result)

    ledger.append("tool.call.completed", {"tool": tool_name, "result": normalized}, causation_id=call_event.id)

    fact_extractor.extract_and_append(tool, normalized, causation_id=call_event.id)

    return ToolCallResult.completed(normalized)
```

## Re-entrant loop

After a tool call completes, the system may either:

1. return the raw/summary result directly, or
2. compose a new context packet including the tool result and ask the model to produce a final response.

For LLM-facing user experiences, prefer the second path:

```text
user input -> model decides tool -> tool executes -> state records result -> model explains result
```

## Handling ambiguity

Do not let the model guess high-impact missing arguments.

Rules:

- Low-risk read-only tools may use high-confidence entity inference.
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

The model can then decide to call a verification tool.

## Model correction loop

If the model emits invalid JSON or invalid decisions:

1. record invalid decision event
2. optionally send validation error back to model
3. retry with strict budget
4. if still invalid, ask user or return safe fallback

Never silently coerce a dangerous invalid decision into an action.

## Runtime invariants

- No tool execution without registered tool metadata.
- No registered tool execution without policy evaluation.
- No generated toolkit execution before validation and registration.
- No durable state mutation without an event.
- No hidden model memory; memory is state plus ledger.
- No route-specific shortcut around the runtime loop for core actions.
