# 03 Runtime Loop

> **Stale/quarantined RuntimeLoop-era document.** Canonical runtime behavior lives in `seed_runtime.runtime.Runtime`: `request_tool` creates `ToolNeed` / `capability_resolution` metadata only, `call_tool` is the only Runtime path into `ToolExecutor`, and `ToolExecutor` executes only registered `ToolRegistry` operations. `RuntimeLoop` is deprecated/experimental, is not the CLI/API/default runtime path, and any RuntimeLoop-specific algorithms below are historical notes unless explicitly labeled as canonical `Runtime` behavior.

Runtime is the canonical runtime orchestration path in Seed. RuntimeLoop v1 is deprecated/experimental and is not wired into CLI, API, or default production paths. It may remain only as quarantined historical/experimental code and must not define canonical runtime behavior.

The canonical Runtime request flow is the center of Seed. Seed is closer to a state engine / distributed state machine than an agent framework: a provider proposes a structured decision, but the runtime owns validation, policy boundaries, registered operation-handler dispatch, and append-only events.

## Loop overview

```text
Input
  -> EventLedger
  -> State Projection
  -> Context Composer
  -> DecisionProvider
  -> Decision Validation
  -> PolicyEngine for valid `call_tool` decisions
  -> ToolExecutor for registered ToolRegistry operations, or Answer
  -> New Events
```

Runtime sovereignty:

1. Receive input and append an input event.
2. Project current state, optionally using `ProjectionStore` snapshot caching.
3. Compose the context packet and deterministic context hash.
4. Ask a `DecisionProvider` for a structured decision. The provider can be deterministic code or a model adapter; LLMs are not required.
5. Reject malformed decisions before policy or operation implementation execution.
6. Evaluate valid operation-call decisions with `PolicyEngine`. Policy denial prevents operation implementation execution.
7. Dispatch only registered `ToolRegistry` operation handlers, or return an answer. Raw provider output is never executed.
8. Append runtime outcome events and Decision Journal events.
9. Re-project state as needed and respond to the user.

## Decision branches

The broader runtime model supports answer/question/tool-need/plan/handoff/state-patch/refusal branches. Runtime focuses on the canonical answer/question/tool-need/plan/handoff/state-patch/refusal branches. Deprecated RuntimeLoop v1 focused on answers and registered operation/tool calls (legacy decision field: `tool`): answers are recorded directly, and operation/tool calls must pass validation, registry lookup, and policy before a registered handler can run. Seed never runs shell commands, subprocesses, network calls, generated code, or arbitrary provider output as part of Decision Journal v1.

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

A `request_tool` decision records a `ToolNeed` / capability gap and may return capability-resolution recommendations. It is not an executable tool request, does not identify a `ToolSpec.name`, and never enters `ToolExecutor`; only a later, separate `call_tool` decision for a registered `ToolRegistry` operation can execute.

### 4. Legacy planning/handoff decisions are quarantined

`propose_action_plan` and `propose_handoff_plan` are historical decision literals only. Canonical Runtime rejects them as unsupported and does not route them. Current Core MVP decisions stop at ToolNeed/capability_resolution/recommendations, state patches, answers, questions, refusals, and registered tool calls.

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
- selected operation/tool name and arguments when present
- policy allowed/denied status
- final outcome: `answered`, `tool_succeeded`, `tool_failed`, `tool_unknown`, `policy_denied`, or `malformed_decision`
- error details when a decision is malformed, a tool is unknown, policy denies, or a handler fails

This journal explains why a path was chosen and what happened afterward. It prepares Seed for `--why`, `--impact`, `--state-summary`, `--relationships`, `--graph-issues`, audit/explain views, and verification commands while preserving `EventLedger` as the source of truth. If an outcome changes after a proposal, Seed appends another event instead of mutating a prior event.

## Runtime Trace

`RuntimeTrace` is a read-only view over one historical/experimental RuntimeLoop run. Given a `workspace_id` and `run_id`, the trace reader loads matching `EventLedger` events, preserves append order, snapshots their payloads, and reconstructs the user input, `decision.recorded` journal record, policy denial event, tool result/failure/unknown event, assistant answer, and errors. It does not replay the runtime and does not call `DecisionProvider`, `PolicyEngine`, registered operations/tools, projectors, shell commands, subprocesses, network clients, generated toolkit operations, LLMs, or host-mutating code.

Trace summaries expose the operator-facing facts needed for audit and explanation surfaces: input text, decision kind and reason, outcome, selected operation/tool, policy allowed/denied status, final response text, and any error. Missing run IDs return an empty trace with `summary.found = false`, rather than inventing or replaying state.

Runtime responsibilities stay separated:

- `Runtime` is the canonical coordinator and appends canonical runtime events through `EventLedger` and owned services.
- `ToolExecutor` owns registered tool execution and its events.
- `PendingActionService` owns pending-action lifecycle events.
- `DecisionJournal` records historical experimental RuntimeLoop decision intent, context hash, selected operation/tool, policy status, outcome, and errors.
- `RuntimeTrace` reconstructs one run from those events only.
- CLI `--trace-run RUN_ID` renders the full ordered trace without mutating history.
- CLI `--why-run RUN_ID` renders a concise human explanation from the same read-only trace.
- Future `--audit`, `--explain`, and `--impact` views can render the trace without mutating history.

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

    result = runtime.route_valid_decision(validated.decision, state, context_hash, causation_id=decision_event.id)

    final_state = projector.project(workspace_id)
    return response_composer.compose(result, final_state)
```

## Decision handling algorithm

This is an abridged canonical `Runtime` sketch for non-execution branches. Only a valid `call_tool` decision may enter `ToolExecutor`; `request_tool` stops after creating ToolNeed / capability-gap and capability-resolution metadata.

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

        case "refuse":
            ledger.append("response.refusal.created", decision.payload, causation_id=causation_id)
            return RefusalResult(reason=decision.reason)
```

## Handoff branch

> **Historical/quarantined planning note.** Core MVP Runtime does not route `propose_action_plan` / `propose_handoff_plan`; provider/handoff recommendations are metadata.

Seed does not invoke a provider/handoff operation implementation after policy review. It creates a non-executable HandoffPlan that an external provider can consume or that a human can follow manually. The HandoffPlan is not an approval and does not imply user approval, execution authorization, credential availability, provider trust, or operation registration.

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
        operation=provider.operation,  # provider/handoff metadata only; not executable ToolSpec.name
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
- Mutating operations/provider handoffs require explicit scope.
- Unknown host/environment requires clarification.
- Toolkit generation requests should capture uncertainty in the ToolNeed / capability gap.

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

The model can then propose an observation HandoffPlan whose returned evidence becomes supporting or conflicting Facts, or request a missing ToolNeed / capability gap.

## Model correction loop

If the model emits invalid JSON or invalid decisions:

1. record invalid decision event
2. optionally send validation error back to model
3. retry with strict budget
4. if still invalid, ask user or return safe fallback

Never silently coerce a dangerous invalid decision into an action.

## Runtime invariants

- Runtime is the canonical coordinator; RuntimeLoop is deprecated/experimental and not an active CLI/API/default path.
- ToolExecutor owns registered tool execution.
- PendingActionService owns pending-action lifecycle events.
- EventLedger is the append-only historical event source.
- ProjectionStore only caches projected state snapshots.
- DecisionProvider proposes; it does not execute.
- Decision validation happens before policy or operation implementation execution.
- PolicyEngine denial prevents operation implementation execution.
- ToolRegistry dispatches only registered operation handlers; raw provider output, shell commands, subprocesses, generated toolkit operations, and arbitrary host mutation are not execution paths.
- DecisionJournal records reasoning and outcomes as append-only events only.
- No credentials, retries, scheduling, or long-running job lifecycle in Seed.
- No HandoffPlan without CapabilityCatalog metadata and policy summary.
- No generated capability metadata before validation and registration.
- No durable state mutation without an event.
- No hidden model memory; memory is state plus ledger.
- No route-specific shortcut around the runtime loop for core actions.
