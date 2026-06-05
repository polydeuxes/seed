# Policy approval and pending-action inventory

This is a source-file-based inventory only. It documents current behavior for policy evaluation, approval, pending actions, and approved-action resume. It intentionally proposes no implementation, refactor, runtime behavior change, test change, or event change.


## Recent shared-service extraction delta

Recent Strategy B extractions moved duplicated lookup, validation, recommendation, and validation-before-policy sequencing into shared services without changing the policy and pending-action semantics documented below. These services remove infrastructure gaps, not the remaining semantic gaps around approval, resume, retry, unsupported decision kinds, state patches, or context budgeting.

### `ToolRecommendationService`

- **Behavior moved:** recommendation lookup against `CapabilityCatalog` and ranking through `RecommendationRanker` are now centralized in a read-only service. It does not create providers, register tools, append events, or mutate state. [`seed_runtime/tool_recommendations.py:11-35`](../seed_runtime/tool_recommendations.py#L11-L35)
- **Runtime path using it:** legacy `Runtime` builds the service from its capability catalog and uses it when `request_tool` creates a `ToolNeed`; it exposes the service ranker through `recommendation_ranker` for compatibility. [`seed_runtime/runtime.py:56-62`](../seed_runtime/runtime.py#L56-L62) [`seed_runtime/runtime.py:275-290`](../seed_runtime/runtime.py#L275-L290)
- **RuntimeLoop path using it:** `RuntimeLoop` accepts/defaults a recommendation service and uses it after projecting state for a request-tool decision. [`seed_runtime/runtime_loop.py:136-148`](../seed_runtime/runtime_loop.py#L136-L148) [`seed_runtime/runtime_loop.py:294-308`](../seed_runtime/runtime_loop.py#L294-L308)
- **Behavior still different:** tool-need creation, event/journal vocabulary, result types, and catalog ownership remain runtime-specific; this service does not affect approval or pending-action behavior. [`seed_runtime/tool_needs.py:28-55`](../seed_runtime/tool_needs.py#L28-L55) [`seed_runtime/runtime_loop.py:274-322`](../seed_runtime/runtime_loop.py#L274-L322)
- **Files involved:** `seed_runtime/tool_recommendations.py`, `seed_runtime/runtime.py`, `seed_runtime/runtime_loop.py`, `seed_runtime/capability_catalog.py`, `seed_runtime/recommendation_ranker.py`, and `tests/test_tool_recommendations.py`.

### `ToolValidationService`

- **Behavior moved:** tool existence lookup, registration-status checks, input schema validation, output schema validation, and the legacy decision-validator tool-input helper are centralized. [`seed_runtime/tool_validation.py:33-97`](../seed_runtime/tool_validation.py#L33-L97)
- **Runtime path using it:** `DecisionValidator` uses the service for `call_tool` decisions, and `ToolExecutor` uses the same validation service through `ToolExecutionPolicyService` before executing or routing policy outcomes. [`seed_runtime/decisions.py:34-40`](../seed_runtime/decisions.py#L34-L40) [`seed_runtime/decisions.py:79-85`](../seed_runtime/decisions.py#L79-L85) [`seed_runtime/execution.py:56-71`](../seed_runtime/execution.py#L56-L71)
- **RuntimeLoop path using it:** `RuntimeLoop` injects/defaults the service, shares it with `ToolExecutionPolicyService` for pre-policy validation, and calls it for post-handler output validation. [`seed_runtime/runtime_loop.py:136-154`](../seed_runtime/runtime_loop.py#L136-L154) [`seed_runtime/runtime_loop.py:369-394`](../seed_runtime/runtime_loop.py#L369-L394) [`seed_runtime/runtime_loop.py:533-548`](../seed_runtime/runtime_loop.py#L533-L548)
- **Behavior still different:** validation errors still surface through each path's own retry/event/result contract: Runtime can retry model-decision validation and emits legacy tool-call failures; RuntimeLoop emits RuntimeLoop-specific unknown/invalid tool events and journal records with no retry loop. [`seed_runtime/runtime.py:123-166`](../seed_runtime/runtime.py#L123-L166) [`seed_runtime/execution.py:92-113`](../seed_runtime/execution.py#L92-L113) [`seed_runtime/runtime_loop.py:372-394`](../seed_runtime/runtime_loop.py#L372-L394)
- **Files involved:** `seed_runtime/tool_validation.py`, `seed_runtime/decisions.py`, `seed_runtime/execution.py`, `seed_runtime/runtime_loop.py`, and `tests/test_tool_validation.py`.

### `ToolExecutionPolicyService`

- **Behavior moved:** both execution paths now share the sequence: resolve tool, validate status, validate input schema, then evaluate policy with scope. The service deliberately returns raw validation/policy details and does not execute operation implementations, emit events, create pending actions, or collapse non-allow outcomes. [`seed_runtime/tool_execution_policy.py:35-42`](../seed_runtime/tool_execution_policy.py#L35-L42) [`seed_runtime/tool_execution_policy.py:88-119`](../seed_runtime/tool_execution_policy.py#L88-L119)
- **Runtime path using it:** `ToolExecutor.execute()` calls `evaluate_with_state_factory()` so state projection is lazy after validation, then preserves legacy routing for validation failures, allow, block, confirmation/approval pending actions, and resume behavior outside the shared service. [`seed_runtime/execution.py:56-73`](../seed_runtime/execution.py#L56-L73) [`seed_runtime/execution.py:86-128`](../seed_runtime/execution.py#L86-L128) [`seed_runtime/execution.py:263-296`](../seed_runtime/execution.py#L263-L296)
- **RuntimeLoop path using it:** `RuntimeLoop._run_tool_decision()` calls `evaluate()` using already projected state, then preserves RuntimeLoop-specific handling for invalid tools, non-allow policy denial, handler lookup, handler failures, output validation, successful tool results, and decision journaling. [`seed_runtime/runtime_loop.py:360-410`](../seed_runtime/runtime_loop.py#L360-L410) [`seed_runtime/runtime_loop.py:448-548`](../seed_runtime/runtime_loop.py#L448-L548)
- **Behavior still different:** confirmation and approval outcomes remain semantic gaps. Runtime turns them into `tool.approval.required` plus `pending_action.created`; RuntimeLoop still emits `runtime.policy.denied`, journals `policy_denied`, and returns an error for every non-allow outcome. Approved-action resume remains Runtime-only. [`seed_runtime/execution.py:121-128`](../seed_runtime/execution.py#L121-L128) [`seed_runtime/execution.py:263-296`](../seed_runtime/execution.py#L263-L296) [`seed_runtime/runtime_loop.py:402-446`](../seed_runtime/runtime_loop.py#L402-L446)
- **Files involved:** `seed_runtime/tool_execution_policy.py`, `seed_runtime/tool_validation.py`, `seed_runtime/execution.py`, `seed_runtime/runtime_loop.py`, `seed_runtime/policy.py`, and `tests/test_tool_execution_policy.py`.

## 1. Policy model

### Core models and outcomes

Source files:

- `seed_runtime/models.py`
- `seed_runtime/policy.py`
- `seed_runtime/state.py`

Policy outcomes are represented by `PolicyOutcome` in `seed_runtime/models.py`:

- `allow`
- `block`
- `require_confirmation`
- `require_approval`

`PolicyDecision` payload shape in `seed_runtime/models.py`:

```text
{
  "outcome": "allow" | "block" | "require_confirmation" | "require_approval",
  "action": str,
  "reason": str,
  "risk_class": "L1" | "L2" | "L3" | "L4",
  "approval_id": str | null
}
```

`PendingAction` payload shape in `seed_runtime/models.py`:

```text
{
  "id": str,
  "workspace_id": str,
  "action": str,
  "tool_name": str,
  "arguments": dict,
  "scope": str | null,
  "status": "pending" | "approved" | "completed" | "cancelled",
  "created_from_event_id": str | null,
  "causation_id": str | null
}
```

`Approval` payload shape in `seed_runtime/models.py`:

```text
{
  "id": str,
  "action": str,
  "scope": str,
  "approved_by": str,
  "expires_at": datetime | null,
  "constraints": dict
}
```

### PolicyGate decisions

`PolicyGate.evaluate()` in `seed_runtime/policy.py` uses this order:

1. If `action_risks` is provided and the tool's `policy_action` is absent, return `block` with reason `unknown policy action is blocked by default`.
2. Resolve risk from `action_risks` when provided; otherwise trust `tool.risk_class`.
3. Check `state.has_approval(tool.policy_action, scope)`.
   - If matching current approval exists, return `allow` with `approval_id` set.
4. If no approval exists:
   - `L1` => `allow`, reason `low-risk read-only action`.
   - `L2` => `require_confirmation`, reason `action requires user confirmation`.
   - `L3` => `require_approval`, reason `high-risk action requires approval`.
   - `L4` or any other fallthrough risk => `block`, reason `critical action is blocked by default`.

### Approval projection

`StateProjector` in `seed_runtime/state.py` projects `approval.granted` events into `state.approvals`. It also parses `expires_at`. Policy approval matching happens through projected state, not directly from the ledger in `PolicyGate`.

`StateProjector` projects pending-action lifecycle events:

- `pending_action.created` inserts a `PendingAction` into `state.pending_actions`.
- `pending_action.status_changed`, `pending_action.approved`, `pending_action.completed`, and `pending_action.cancelled` update the pending action status when the pending action already exists in projected state.

## 2. Runtime / ToolExecutor behavior

Source files:

- `seed_runtime/runtime.py`
- `seed_runtime/execution.py`
- `seed_runtime/pending_actions.py`
- `seed_runtime/policy.py`
- `seed_runtime/state.py`

The old `Runtime` delegates tool calls to `ToolExecutor.execute()` from the `call_tool` decision route in `seed_runtime/runtime.py`.

### Allow behavior

`ToolExecutor.execute()` now delegates the common pre-execution sequence to `ToolExecutionPolicyService.evaluate_with_state_factory()`, which validates:

1. The tool exists through `ToolValidationService.validate_tool_exists()`.
2. Operation/tool registration status is valid.
3. Input schema is valid.
4. Policy is evaluated through the configured policy engine with `scope`.

`ToolExecutor` still owns the legacy routing and event behavior after the shared service returns.

When policy outcome is `allow`, `ToolExecutor` calls `_execute_allowed_tool_call()`.

`_execute_allowed_tool_call()` emits:

1. `tool.call.started`
   - actor: `tool`
   - payload: `{"tool": tool.name, "arguments": to_plain(arguments)}` plus `scope` when supplied
2. On success: `tool.call.completed`
   - actor: `tool`
   - payload: `{"tool": tool.name, "output": output}`
3. `FactExtractionService.observe_tool_result()` may append evidence events after `tool.call.completed`.

Return shape is a `ToolCallResult` with:

- `kind="tool_result"`
- `status="completed"`
- `tool_name`
- success message
- `output`
- `payload={"output": output, "completed_event_id": completed_event.id}`

### Deny / block behavior

When policy outcome is `block`, `ToolExecutor.execute()` calls `_policy_denied()`.

`_policy_denied()` emits:

- `tool.policy.blocked`
  - actor: `system`
  - payload: `{"tool": tool.name, "policy": to_plain(policy)}`

It does **not** create a pending action for `block`.

Return shape includes:

- `kind="block"`
- `status="blocked"`
- `message=policy.reason`
- `policy=to_plain(policy)`
- `pending_action=None`
- `payload={"policy": to_plain(policy)}`

### Confirmation behavior

When policy outcome is `require_confirmation`, `ToolExecutor.execute()` calls `_policy_denied()` and treats the result as a non-executing pending action flow, not as a hard block.

It emits:

1. `tool.approval.required`
   - actor: `system`
   - payload: `{"tool": tool.name, "policy": to_plain(policy)}`
2. `pending_action.created`
   - emitted by `PendingActionService.create_tool_call()`
   - actor: `system`
   - payload: `{"pending_action": to_plain(pending_action)}`

Return shape includes:

- `kind="require_confirmation"`
- `status="require_confirmation"`
- `message=policy.reason`
- `policy=to_plain(policy)`
- `pending_action=<PendingAction status="pending">`
- `payload={"policy": ..., "pending_action": ...}`

No tool implementation is called before confirmation.

### Approval behavior

When policy outcome is `require_approval`, the behavior is parallel to confirmation:

1. `tool.approval.required`
2. `pending_action.created`
3. no tool implementation call
4. `ToolCallResult.kind="require_approval"`
5. `ToolCallResult.status="require_approval"`
6. pending action status starts as `pending`

The pending action stores action, tool name, arguments, scope, source policy event id, causation id, and workspace id.

### Pending action creation

`PendingActionService.create_tool_call()` in `seed_runtime/pending_actions.py` creates a `PendingAction` with:

- generated id prefix `pa`
- `workspace_id`
- policy `action`
- `tool_name`
- `arguments` serialized with `to_plain()`
- optional `scope`
- `status="pending"`
- optional `created_from_event_id`
- optional `causation_id`

It appends `pending_action.created` with `causation_id=created_from_event_id or causation_id` and the supplied `correlation_id`.

### Marking approval

`PendingActionService.mark_approved()` delegates to `_set_status(..., "approved")`.

`_set_status()`:

1. Projects state.
2. Raises `ValueError` if the pending action is unknown.
3. Returns a copied pending action with updated status.
4. Appends `pending_action.approved`.
   - actor: `approver`
   - payload: `{"pending_action_id": pending_action_id, "status": "approved"}`

There is no resume in `mark_approved()` itself.

### Approved-action resume

`ToolExecutor.resume_approved_tool_call()` in `seed_runtime/execution.py` is the only current resume path found for pending tool calls.

Behavior:

1. Project state.
2. Raise `ValueError` for unknown pending action id.
3. Raise `ValueError` unless projected `pending_action.status == "approved"`.
4. Reconstruct causation/correlation with `_resume_event_context()`.
5. Load the stored tool by `pending_action.tool_name`.
6. Execute `_execute_allowed_tool_call()` using the pending action's stored arguments and scope.
7. If the result status is `completed`, call `PendingActionService.mark_completed()`.
8. If the resumed tool fails, do **not** mark the pending action completed; it remains `approved` in projected state.

Resume emits on success:

1. existing pre-resume events: `tool.approval.required`, `pending_action.created`, `pending_action.approved`
2. `tool.call.started`
3. `tool.call.completed`
4. optional evidence events from fact extraction
5. `pending_action.completed`

Resume emits on execution failure:

1. existing pre-resume events: `tool.approval.required`, `pending_action.created`, `pending_action.approved`
2. `tool.call.started`
3. `tool.call.failed`
4. no `pending_action.completed`

Important behavior: resume does **not** call `PolicyGate.evaluate()` again. The pending action status is the gate for resume.

### Runtime emitted events for this flow

The old `Runtime` also emits its regular user/model routing events around the `ToolExecutor` flow, for example:

- `input.user_message`
- `model.decision.proposed`
- then tool executor events such as `tool.policy.blocked`, `tool.approval.required`, `pending_action.created`, `tool.call.started`, `tool.call.completed`, or `tool.call.failed`

## 3. RuntimeLoop behavior

Source files:

- `seed_runtime/runtime_loop.py`
- `seed_runtime/policy.py`
- `seed_runtime/decision_journal.py`
- `seed_runtime/runtime_trace.py`

`RuntimeLoop` evaluates policy in `_run_tool_decision()` through `ToolExecutionPolicyService.evaluate()` after shared tool existence, status, and input validation. The service calls the configured policy engine with `scope=None`; RuntimeLoop still owns the RuntimeLoop-specific event, result, and journal routing after the shared service returns.

### Allow behavior

When policy outcome is `allow`, `RuntimeLoop`:

1. Looks up a runtime handler from `self.tool_handlers`.
2. Emits `runtime.tool.handler_missing` if no handler exists.
3. Calls `handler.execute(context, dict(decision.tool_args))` when a handler exists.
4. Emits `tool.failure` on handler exception.
5. Validates output schema.
6. Emits `runtime.tool.invalid` on output validation failure.
7. Emits `tool.result` on success.
8. Calls `FactExtractionService.observe_tool_result()` after `tool.result`.
9. Appends a `decision.recorded` journal event with `policy_allowed=True` and outcome such as `tool_succeeded` or `tool_failed`.

RuntimeLoop uses event names `tool.result` and `tool.failure`, not `tool.call.started`, `tool.call.completed`, or `tool.call.failed`.

### Deny behavior

When policy outcome is anything other than `allow`, `RuntimeLoop` treats it as denial.

It emits:

- `runtime.policy.denied`
  - actor: `system`
  - payload:

```text
{
  "tool_name": tool.name,
  "tool_args": to_plain(decision.tool_args),
  "policy": to_plain(policy),
  "reason": decision.reason
}
```

It then emits `decision.recorded` with:

- `policy_allowed=False`
- `outcome="policy_denied"`
- `error=f"policy denied tool {tool.name}: {policy.outcome}"`

Return shape is `RuntimeResult` with:

- `decision_kind="call_tool"`
- `response_text=None`
- `tool_name=tool.name`
- `policy_allowed=False`
- `error="policy denied tool <tool>: <outcome>"`
- `decision_outcome="policy_denied"`

### Missing approval / confirmation behavior

RuntimeLoop has no pending-action branch for `require_confirmation` or `require_approval`. Those outcomes follow the same non-allow path as `block`.

Observed consequences from source:

- No `tool.approval.required` event.
- No `pending_action.created` event.
- No `PendingActionService` dependency in `RuntimeLoop`.
- No pending action returned in `RuntimeResult`.
- No method analogous to `resume_approved_tool_call()`.
- No approved pending-action resume path.
- No status transitions to `pending_action.approved` or `pending_action.completed` from RuntimeLoop.

### RuntimeLoop emitted events for policy-related paths

Policy-related RuntimeLoop events include:

- `runtime.policy.denied` for every non-`allow` policy outcome.
- `decision.recorded` journal event after the denial.
- `runtime.tool.handler_missing`, `tool.failure`, `runtime.tool.invalid`, and `tool.result` for allowed policy paths that reach handler lookup/execution/validation.

## 4. Event inventory

Policy/action-related events found in the inspected source and tests:

| Event | Source file(s) | Current source behavior |
| --- | --- | --- |
| `approval.granted` | `seed_runtime/state.py`, tests | Projected into `state.approvals`; used by `PolicyGate` through `state.has_approval()`. |
| `tool.policy.blocked` | `seed_runtime/execution.py` | Old `ToolExecutor` emits for `PolicyDecision.outcome == "block"`; no pending action. |
| `tool.approval.required` | `seed_runtime/execution.py` | Old `ToolExecutor` emits for `require_confirmation` and `require_approval` before pending action creation. |
| `pending_action.created` | `seed_runtime/pending_actions.py`, `seed_runtime/state.py` | Emitted when old `ToolExecutor` creates a non-executed pending tool call; projected into `state.pending_actions`. |
| `pending_action.approved` | `seed_runtime/pending_actions.py`, `seed_runtime/state.py` | Emitted by `PendingActionService.mark_approved()`; projected as status `approved`; actor is `approver`. |
| `pending_action.completed` | `seed_runtime/pending_actions.py`, `seed_runtime/state.py` | Emitted by `PendingActionService.mark_completed()` after successful approved-action resume; projected as status `completed`. |
| `pending_action.cancelled` | `seed_runtime/state.py` | Projector recognizes it as a lifecycle status update. No service method was found in `PendingActionService` for cancellation. |
| `pending_action.status_changed` | `seed_runtime/state.py` | Projector recognizes generic status update. No emitter was found in inspected pending-action service. |
| `tool.call.started` | `seed_runtime/execution.py` | Old `ToolExecutor` emits before calling a registered implementation, including approved-action resume. |
| `tool.call.completed` | `seed_runtime/execution.py` | Old `ToolExecutor` emits after successful registered implementation execution. |
| `tool.call.failed` | `seed_runtime/execution.py` | Old `ToolExecutor` emits for registration/input/execution/output failures. |
| `runtime.policy.denied` | `seed_runtime/runtime_loop.py`, `seed_runtime/runtime_trace.py` | RuntimeLoop emits for every non-`allow` policy outcome. Trace code treats it as policy denial. |
| `decision.recorded` | `seed_runtime/decision_journal.py`, `seed_runtime/runtime_loop.py` | RuntimeLoop appends policy outcome summaries such as `policy_denied`, `tool_succeeded`, `tool_failed`. |
| `runtime.tool.unknown` | `seed_runtime/runtime_loop.py` | RuntimeLoop emits before policy when selected operation/tool is unknown. |
| `runtime.tool.invalid` | `seed_runtime/runtime_loop.py` | RuntimeLoop emits for tool status/input/output validation failure. |
| `runtime.tool.handler_missing` | `seed_runtime/runtime_loop.py` | RuntimeLoop emits after policy allow when no handler exists. |
| `tool.failure` | `seed_runtime/runtime_loop.py` | RuntimeLoop emits when a handler raises. |
| `tool.result` | `seed_runtime/runtime_loop.py` | RuntimeLoop emits on successful handler result. |

## 5. Test coverage

Existing tests covering the inventory:

### Policy

- `tests/test_policy.py::test_l1_allows` covers L1 => `allow`.
- `tests/test_policy.py::test_l2_requires_confirmation` covers L2 => `require_confirmation`.
- `tests/test_policy.py::test_l3_requires_approval` covers L3 => `require_approval`.
- `tests/test_policy.py::test_l4_blocks` covers L4 => `block`.
- `tests/test_policy.py::test_unknown_action_blocks` covers unknown action with explicit risk table => `block`.
- `tests/test_policy.py::test_existing_matching_approval_allows` covers `approval.granted` projection plus matching action/scope allowing a high-risk action and populating `approval_id`.
- `tests/test_policy.py::test_non_matching_approval_still_requires_approval` covers scope mismatch continuing to require approval.

### Old ToolExecutor / pending actions / resume

- `tests/test_execution.py::test_successful_echo_tool_execution` covers allowed execution and `tool.call.started` / `tool.call.completed` / evidence events.
- `tests/test_execution.py::test_invalid_input_schema_fails_before_execution` covers validation failure before execution and `tool.call.failed` with phase `input_validation`.
- `tests/test_execution.py::test_policy_block_prevents_execution` covers `block`, no operation implementation execution, and `tool.policy.blocked`.
- `tests/test_execution.py::test_output_schema_validation_failure_records_failed_event` covers started call then `tool.call.failed` on output validation / execution phase.
- `tests/test_execution.py::test_completed_tool_call_appends_tool_call_completed` covers completed event payload.
- `tests/test_pending_actions.py::test_approval_required_tool_does_not_execute` covers `require_approval`, no implementation call, `tool.approval.required`, `pending_action.created`, and pending-action payload fields.
- `tests/test_pending_actions.py::test_pending_action_is_projected_in_state` covers `require_confirmation` creating a projected pending action with source event id.
- `tests/test_pending_actions.py::test_approval_event_can_mark_pending_action_approved` covers `PendingActionService.mark_approved()`, `pending_action.approved`, projector status update, and actor `approver`.
- `tests/test_action_resume.py::test_approved_pending_action_resumes_echo_tool` covers successful approved pending-action resume, stored args/scope, event order, causation from approval event, correlation preservation, and completion status.
- `tests/test_action_resume.py::test_pending_action_cannot_resume_before_approval` covers refusing resume while status is still `pending` and no tool call.
- `tests/test_action_resume.py::test_completed_action_cannot_resume_twice` covers completed pending action cannot be resumed twice.
- `tests/test_action_resume.py::test_failed_resumed_tool_does_not_mark_completed` covers failed resumed execution leaving pending action `approved` and not emitting `pending_action.completed`.

### RuntimeLoop and trace

- `tests/test_runtime_loop.py::test_loop_tool_decision_executes_registered_echo_tool_and_appends_result_event` covers allowed RuntimeLoop operation implementation execution and `tool.result`.
- `tests/test_runtime_loop.py::test_loop_policy_denial_prevents_tool_execution` covers RuntimeLoop non-allow branch for `block`, no handler call, `runtime.policy.denied`, and `decision.recorded` outcome `policy_denied`.
- `tests/test_runtime_loop.py::test_loop_unknown_tool_is_rejected_and_logged_as_event` covers unknown tool before policy.
- `tests/test_runtime_loop.py::test_loop_malformed_decision_is_rejected_before_policy_and_tool_execution` covers malformed decision before policy/operation implementation execution.
- `tests/test_runtime_loop.py::test_loop_tool_handler_exception_is_caught_and_journaled_as_tool_failed` covers allowed policy path with handler exception.
- `tests/test_runtime_trace.py::test_trace_reconstructs_policy_denied_run` covers trace reconstruction for `runtime.policy.denied`.

Coverage gap in tests: no RuntimeLoop test explicitly feeds `PolicyDecision.outcome == "require_confirmation"` or `"require_approval"`; current source indicates those would be treated as `runtime.policy.denied`, but the named RuntimeLoop test only covers `block`.

## 6. Gaps: RuntimeLoop compared to Runtime / ToolExecutor

RuntimeLoop currently lacks these old Runtime / ToolExecutor behaviors:

1. Separate routing for `block` vs `require_confirmation` vs `require_approval`.
2. `tool.approval.required` emission for confirmation / approval outcomes.
3. `pending_action.created` emission for confirmation / approval outcomes.
4. Pending action payload in the runtime result.
5. Dependency on `PendingActionService`.
6. Pending action status transitions through `pending_action.approved` / `pending_action.completed`.
7. Approved pending-action resume API equivalent to `ToolExecutor.resume_approved_tool_call()`.
8. Resume causation/correlation reconstruction equivalent to `_resume_event_context()`.
9. Stored-argument/stored-scope execution from a pending action.
10. Exactly-once prevention through completed pending-action status.
11. Failure behavior that leaves a failed resumed action in `approved` status.
12. Old event vocabulary for operation implementation execution (`tool.call.started`, `tool.call.completed`, `tool.call.failed`) in the primary execution path.
13. Test coverage for RuntimeLoop `require_confirmation` and `require_approval` outcomes.

## 7. Extraction candidates only

These are possible shared service boundaries for future planning. No implementation is proposed here.

### `PolicyDecisionRouter`

Possible responsibility:

- Accept a `PolicyDecision`, tool metadata, arguments, scope, run/session/correlation ids, and caller flavor.
- Route `allow`, `block`, `require_confirmation`, and `require_approval` distinctly.
- Normalize result shape and event choices for old Runtime and RuntimeLoop, if parity is desired.

Current source seams:

- `ToolExecutor.execute()` has the old routing branch.
- `RuntimeLoop._run_tool_decision()` currently has a single `policy.outcome != "allow"` branch.

### `PendingActionService`

Already exists in `seed_runtime/pending_actions.py`.

Potential future expansion boundaries:

- Create pending action for tool call.
- Approve, complete, cancel, or generic status update.
- Own event payload shape and actor conventions.
- Provide idempotency / transition rules if desired.

Current service does not expose cancellation and does not enforce lifecycle transitions beyond unknown-id checks.

### `ApprovalResumeService`

Possible responsibility:

- Validate pending action exists and has `approved` status.
- Resolve causation/correlation for resume.
- Execute stored tool call once.
- Mark completed only on success.
- Preserve failure semantics.

Current source seam:

- `ToolExecutor.resume_approved_tool_call()` and `_resume_event_context()`.

### `ToolExecutionPolicyService`

Status: implemented as shared infrastructure. It now validates operation/tool existence/status/input, evaluates policy with scope, and returns a structured execution-policy result before handler/implementation execution. [`seed_runtime/tool_execution_policy.py:35-119`](../seed_runtime/tool_execution_policy.py#L35-L119)

Current source seams that remain:

- `ToolExecutor.execute()` uses the shared result but still owns legacy validation-failure mapping, `tool.policy.blocked`, confirmation/approval pending actions, allowed execution, and approved-action resume. [`seed_runtime/execution.py:86-128`](../seed_runtime/execution.py#L86-L128) [`seed_runtime/execution.py:263-296`](../seed_runtime/execution.py#L263-L296)
- `RuntimeLoop._run_tool_decision()` uses the shared result but still owns RuntimeLoop invalid-tool events, `runtime.policy.denied`, handler-missing/failure/success events, output validation handling, and decision journaling. [`seed_runtime/runtime_loop.py:369-446`](../seed_runtime/runtime_loop.py#L369-L446) [`seed_runtime/runtime_loop.py:448-548`](../seed_runtime/runtime_loop.py#L448-L548)
- The two paths still diverge after non-allow policy outcomes.

## 8. Risks if RuntimeLoop replaced Runtime today for policy / approval flows

Shared recommendation lookup/ranking, shared tool validation, and shared validation-plus-policy-evaluation sequencing are no longer gaps by themselves. If RuntimeLoop replaced old Runtime / ToolExecutor for policy and approval flows today, the remaining risks are semantic and contract-level: confirmation/approval pending actions, approved-action resume, retry handling, `ask_question`/`refuse`, `state_patch`, and context budgeting.

### Current recommended next step

Continue Strategy B. Do not delete `Runtime`, do not migrate the CLI yet, and choose next candidates by auditing semantic gaps rather than infrastructure duplication. Possible next candidates are auditing `state_patch` behavior, auditing retry/parse-failure behavior, auditing `ask_question`/`refuse` semantics, and deciding whether approval/resume should remain Runtime-only or become shared.

If RuntimeLoop replaced old Runtime / ToolExecutor for policy and approval flows today, source inspection indicates these risks:

1. L2 confirmation flows would become hard policy denials instead of pending actions awaiting confirmation.
2. L3 approval flows would become hard policy denials instead of pending actions awaiting approval.
3. Clients expecting `tool.approval.required` would not receive it.
4. Clients expecting `pending_action.created` would not receive it.
5. Existing approval UIs or APIs based on projected `state.pending_actions` would have no pending action to show.
6. Existing approval/resume workflows using `PendingActionService.mark_approved()` plus `ToolExecutor.resume_approved_tool_call()` would not have a RuntimeLoop-created pending action to approve or resume.
7. Approved-action resume would be unavailable through RuntimeLoop.
8. Existing event consumers expecting `tool.call.started` / `tool.call.completed` / `tool.call.failed` from old operation implementation execution would instead see RuntimeLoop's `tool.result`, `tool.failure`, or RuntimeLoop-specific events.
9. Correlation/causation semantics for approval resume would be lost because RuntimeLoop has no `_resume_event_context()` equivalent.
10. Exactly-once resume prevention through pending-action completion would not apply because RuntimeLoop does not create or complete pending actions.
11. Tests and traces that assume `runtime.policy.denied` means hard denial could become ambiguous if confirmation/approval outcomes were later routed through that same event.
12. Any consumers interpreting `decision.recorded.outcome="policy_denied"` as a final denial would misrepresent confirmation/approval-required states if RuntimeLoop continued to use that outcome for all non-allow policy results.
