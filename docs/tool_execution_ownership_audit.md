# Operation Implementation Execution Ownership Audit

> **Stale/quarantined RuntimeLoop-era audit.** Preserve this as historical analysis of a deprecated experimental path. Current architecture treats `Runtime` as canonical: only `call_tool` enters `ToolExecutor`, and `ToolExecutor` executes only registered `ToolRegistry` operations. RuntimeLoop-specific dispatcher recommendations below are not current-core guidance unless revived by a future architecture decision.

## Scope

This audit compares the registered `ToolExecutor` path with the remaining
RuntimeLoop-owned operation implementation execution path in `RuntimeLoop._run_tool_decision`. It is
focused on ownership only: no refactor, migration, runtime behavior change, or
test change is proposed here.

Inspected areas:

- `seed_runtime/execution.py`
- `seed_runtime/runtime_loop.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/fact_extraction.py`
- pending-action execution/resume code in `seed_runtime/pending_actions.py`,
  `seed_runtime/runtime.py`, and `seed_runtime/execution.py`
- RuntimeLoop and ToolExecutor operation implementation execution tests

## 1. ToolExecutor responsibilities

`ToolExecutor` is the production registered operation implementation executor. It owns the full
registered operation/tool call lifecycle for callers that invoke `execute` or
`resume_approved_tool_call`.

### Execution

`ToolExecutor.execute` accepts workspace/session identity, a tool name,
arguments, optional causation/correlation ids, and optional scope. It uses
`ToolExecutionPolicyService.evaluate_with_state_factory` to resolve the tool,
validate the call, and evaluate policy before execution. If policy allows the
call, it delegates to `_execute_allowed_tool_call`.

For allowed calls, `_execute_allowed_tool_call`:

- appends `tool.call.started` with `tool`, serialized `arguments`, and optional
  `scope`;
- loads the registered toolkit implementation from the tool spec's
  `module:function` implementation reference;
- calls the implementation with a `ToolContext` plus keyword arguments;
- validates the returned value against the registered output schema;
- appends `tool.call.failed` when implementation loading, handler execution, or
  output validation raises; and
- appends `tool.call.completed` on success and returns a `ToolCallResult` with
  `kind="tool_result"`, `status="completed"`, `output`, and a payload containing
  the output and completed event id.

### Approval lifecycle

`ToolExecutor` integrates non-allow policy outcomes with pending actions:

- `block` emits `tool.policy.blocked` and returns a blocked result;
- `require_confirmation` and `require_approval` emit `tool.approval.required`;
- confirmation/approval outcomes create a `PendingAction` through
  `PendingActionService.create_tool_call`; and
- the returned `ToolCallResult` includes the policy payload and pending action.

`PendingActionService` itself owns the event-level pending-action mutations:
creating `pending_action.created`, marking `pending_action.approved`, and
marking `pending_action.completed`.

### Resume

`ToolExecutor.resume_approved_tool_call` owns execution of approved pending tool
calls. It projects state, requires that the pending action exists and has status
`approved`, reconstructs causation/correlation context from the approval and
creation events, loads the stored tool call, executes it through the same allowed
execution path, and marks the pending action completed only after a completed
result.

### Event emission

The executor emits the registered-tool event vocabulary:

- `tool.call.started`
- `tool.call.completed`
- `tool.call.failed`
- `tool.policy.blocked`
- `tool.approval.required`
- `pending_action.created` through `PendingActionService`
- `pending_action.completed` through `PendingActionService` on successful resume

It also preserves session id and correlation id on the tool events it emits.

### Evidence extraction

On successful execution, `ToolExecutor` calls
`FactExtractionService.observe_tool_result` with the `tool.call.completed` event.
That shared extraction service appends `evidence.observed` for both executor
`tool.call.completed` and RuntimeLoop `tool.result` events.

### Policy integration

`ToolExecutor` owns the concrete policy routing for registered execution. It
constructs `ToolExecutionPolicyService` from the registry, validation service,
and policy gate, then maps service results to executor behavior. The shared
policy service intentionally stops at validation and raw policy evaluation; it
does not execute operation implementations, emit events, create pending actions, or collapse
non-allow outcomes.

### Validation integration

`ToolExecutor` relies on `ToolExecutionPolicyService` for existence/status/input
validation before policy evaluation and uses `ToolValidationService` directly for
output schema validation after invoking the registered function. Unknown tool
behavior is intentionally registry-backed: if the shared policy service cannot
resolve an operation/tool, the executor calls `registry.require(tool_name)`, preserving the
older raising behavior for unknown operations/tools.

## 2. RuntimeLoop operation implementation execution responsibilities

`RuntimeLoop._run_tool_decision` owns the entire `call_tool` decision execution
path for the deterministic RuntimeLoop. In order, it currently:

1. normalizes missing `decision.tool_name` to an empty string;
2. calls the same `ToolExecutionPolicyService.evaluate` with the already
   projected run state and `scope=None`;
3. converts unknown operations/tools into `runtime.tool.unknown` plus a decision journal
   record with outcome `tool_unknown`;
4. converts status/input validation failures into `runtime.tool.invalid` plus a
   decision journal record with outcome `tool_failed`;
5. converts non-allow policy outcomes into `runtime.policy.denied` plus a
   decision journal record with outcome `policy_denied`;
6. finds an in-memory `RuntimeTool` handler by operation/tool name in `self.tool_handlers`;
7. emits `runtime.tool.handler_missing` and journals `tool_failed` when no
   handler is registered;
8. calls `handler.execute(context, dict(decision.tool_args))`;
9. catches handler exceptions as `tool.failure` plus a decision journal record
   with outcome `tool_failed`;
10. validates handler output with `ToolValidationService.validate_output_schema`;
11. records invalid output as `runtime.tool.invalid` plus a decision journal
    record with outcome `tool_failed` and `policy_allowed=True`;
12. appends `tool.result` for successful output with the decision reason;
13. asks `FactExtractionService.observe_tool_result` to append evidence from the
    result event;
14. appends a `decision.recorded` journal entry with selected operation/tool name/args,
    context hash, reason, policy flag, and outcome; and
15. shapes the final `RuntimeResult` with RuntimeLoop decision metadata.

This path does not use registered implementation references, does not emit
`tool.call.started`, does not create pending actions, does not resume pending
actions, and does not return `ToolCallResult`.

## 3. Exact overlap

| Responsibility | ToolExecutor | RuntimeLoop | Shared service already exists? |
| --- | --- | --- | --- |
| Tool existence resolution | Uses `ToolExecutionPolicyService`, then `registry.require` for unknown-tool compatibility. | Uses `ToolExecutionPolicyService`, then records `runtime.tool.unknown`. | Yes: `ToolValidationService.validate_tool_exists` and `ToolExecutionPolicyService`. |
| Tool status validation | Uses `ToolExecutionPolicyService`; failure emits `tool.call.failed` with phase `registration`. | Uses `ToolExecutionPolicyService`; failure emits `runtime.tool.invalid` with phase `status`. | Yes: `ToolValidationService.validate_tool_status` and `ToolExecutionPolicyService`. |
| Input schema validation | Uses `ToolExecutionPolicyService`; failure emits `tool.call.failed` with phase `input_validation`. | Uses `ToolExecutionPolicyService`; failure emits `runtime.tool.invalid` with phase `input`. | Yes: `ToolValidationService.validate_input_schema` and `ToolExecutionPolicyService`. |
| Policy evaluation | Uses `ToolExecutionPolicyService.evaluate_with_state_factory` with lazy projection. | Uses `ToolExecutionPolicyService.evaluate` with state already projected for the run. | Yes: `ToolExecutionPolicyService`; event/result routing remains caller-owned. |
| Policy denial handling | Emits `tool.policy.blocked` or `tool.approval.required`; creates pending actions for confirmation/approval. | Emits one `runtime.policy.denied` event for every non-allow outcome; no pending action. | Partially: policy evaluation is shared; denial lifecycle is not. |
| Pending-action creation | Owns creation for `require_confirmation`/`require_approval` through `PendingActionService`. | None. | Yes for mutations: `PendingActionService`. RuntimeLoop does not use it. |
| Approved pending-action resume | Owns status checks, causation/correlation reconstruction, execution, and completion marking. | None. | Partially: `PendingActionService` mutates status, but resume orchestration is executor-owned. |
| Handler/function dispatch | Loads registered toolkit function from `ToolSpec.implementation` and calls it with `ToolContext`. | Calls an in-memory `RuntimeTool` from `self.tool_handlers` with `RuntimeContext` and argument dict. | No shared dispatcher for these two handler models. |
| Started event | Emits `tool.call.started`. | None. | No. |
| Successful result event | Emits `tool.call.completed`. | Emits `tool.result`. | No shared emitter; `FactExtractionService` accepts both shapes. |
| Execution failure event | Emits `tool.call.failed` with phase `execution`. | Emits `tool.failure`. | No. |
| Output schema validation | Validates after execution; records failures as `tool.call.failed` phase `execution`. | Validates after handler return; records failures as `runtime.tool.invalid` phase `output`. | Yes: `ToolValidationService.validate_output_schema`; failure semantics differ. |
| Evidence extraction | Calls shared extraction service after `tool.call.completed`; does not add evidence event id to result payload. | Calls shared extraction service after `tool.result`; appends evidence ids to `RuntimeResult.events_appended`. | Yes: `FactExtractionService`. |
| Decision journaling | None. | Owns `decision.recorded` entries for all RuntimeLoop outcomes. | Yes for journal append mechanics: `DecisionJournal`; not part of ToolExecutor. |
| Result shaping | Returns `ToolCallResult` with executor status/kind/message/payload. | Returns `RuntimeResult` with run id, decision id, context hash, decision reason/outcome, and tool result. | No shared result type. |

## 4. Semantic differences

### Registered toolkit functions

`ToolExecutor` is registry-implementation driven. It treats `ToolSpec` as an
executable manifest entry, imports the declared `module:function`, and calls it
with `ToolContext` and keyword arguments. This makes it the owner of registered
production toolkit execution.

### In-memory handlers

`RuntimeLoop` is handler-map driven. Its `RuntimeTool` protocol receives the full
`RuntimeContext` and an argument dictionary. This allows tests and deterministic
runtime experiments to install in-memory handlers that do not need importable
manifest implementations. The missing-handler case is RuntimeLoop-specific and
has no `ToolExecutor` equivalent.

### Pending-action support

`ToolExecutor` supports pending actions for `require_confirmation` and
`require_approval`; RuntimeLoop does not. RuntimeLoop collapses every non-allow
policy outcome to `runtime.policy.denied` and `decision_outcome="policy_denied"`.
That means adapting RuntimeLoop directly to `ToolExecutor.execute` would add
observable pending-action behavior unless deliberately suppressed or mapped.

### Approval support

`ToolExecutor` resume support is approval-aware: it requires an approved pending
action, executes stored arguments once, and marks completion only on successful
execution. RuntimeLoop has no approved-action resume path in `_run_tool_decision`.

### Event vocabulary differences

The two paths intentionally speak different event vocabularies today:

- `ToolExecutor`: `tool.call.started`, `tool.call.completed`,
  `tool.call.failed`, `tool.policy.blocked`, `tool.approval.required`, and
  pending-action events.
- `RuntimeLoop`: `runtime.tool.unknown`, `runtime.tool.invalid`,
  `runtime.policy.denied`, `runtime.tool.handler_missing`, `tool.failure`,
  `tool.result`, and `decision.recorded`.

Tests assert these differences, especially the absence of `tool.call.started` in
RuntimeLoop success and invalid-output cases, and the presence of RuntimeLoop
journal outcomes.

### Result-shaping differences

`ToolExecutor` returns a tool-call-centric `ToolCallResult` with executor status,
message, optional output/error/policy/pending action, and payload. RuntimeLoop
returns a run/decision-centric `RuntimeResult` that includes event ids, run id,
context hash, decision id, reason, outcome, policy flag, and optional tool
result. RuntimeLoop result shaping is orchestration state, not raw tool
execution.

## 5. Ownership conclusion

RuntimeLoop operation implementation execution is **mixed**.

It is not purely runtime-specific because several core execution concerns are
real duplicates of ToolExecutor/shared service ownership:

- policy/validation sequencing;
- output schema validation after handler execution;
- failure/result event emission around the executable call;
- evidence extraction from successful tool output; and
- conversion of execution outcomes into returned result objects.

However, it is not mostly simple duplication either. RuntimeLoop currently owns
substantial runtime-specific orchestration that `ToolExecutor` does not model:

- call decisions are tied to an input event, run id, context hash, and decision
  reason;
- every branch appends a `DecisionJournal` record with a RuntimeLoop-specific
  outcome;
- dispatch targets in-memory `RuntimeTool` handlers that receive
  `RuntimeContext`, not importable registered functions that receive
  `ToolContext`;
- RuntimeLoop deliberately preserves a separate event vocabulary; and
- RuntimeLoop intentionally lacks pending-action and approval behavior in this
  path.

Therefore the current state is **mixed: shared validation/policy/evidence
services have already removed some duplication, while execution dispatch and
branch-specific event/result/journal shaping remain duplicated but semantically
not identical**.

## 6. Extraction candidates

### RuntimeLoopToolDispatcher

A `RuntimeLoopToolDispatcher` would extract the existing RuntimeLoop-specific
handler-map dispatch and RuntimeLoop event vocabulary without changing behavior.
It would likely own:

- in-memory handler lookup;
- handler exception capture;
- output validation;
- `runtime.tool.*`, `tool.failure`, and `tool.result` event emission;
- evidence extraction event id collection; and
- returning a RuntimeLoop-shaped dispatch outcome for the caller to journal.

This is the lowest-risk extraction because it preserves RuntimeLoop semantics and
does not pretend to be the registered `ToolExecutor`. It would mostly move code
out of `RuntimeLoop`, but it would make ownership clearer by naming the
RuntimeLoop-specific dispatch boundary.

### ToolExecutorAdapter

A `ToolExecutorAdapter` would let RuntimeLoop call `ToolExecutor` and translate
`ToolCallResult`/executor events into RuntimeLoop `RuntimeResult` and journal
outcomes. This is attractive only if the intended future state is for RuntimeLoop
to execute registered toolkit functions and inherit pending-action semantics.
Today it is not the natural next step because it would have to bridge or suppress
several observable differences:

- registered functions vs in-memory handlers;
- `ToolContext` vs `RuntimeContext`;
- `tool.call.*` events vs RuntimeLoop event vocabulary;
- pending-action creation vs RuntimeLoop policy-denied behavior;
- unknown-tool raising behavior vs `runtime.tool.unknown`; and
- executor result payloads vs RuntimeLoop decision metadata.

An adapter would be behaviorally meaningful, not just an extraction.

### SharedToolExecutionService

A `SharedToolExecutionService` could factor the common skeleton: validate,
evaluate policy, dispatch an allowed call, validate output, emit a result event,
and extract evidence. To avoid accidentally creating a second `ToolExecutor`, it
would need explicit extension points for:

- tool dispatch strategy (`ToolContext` registered function vs `RuntimeContext`
  in-memory handler);
- event vocabulary and payload shape;
- non-allow policy routing;
- unknown/invalid/output failure mapping;
- pending-action creation/resume policy; and
- caller-specific result type and journal integration.

This could reduce real duplication, but only after the project decides which
semantics are shared and which are intentionally per-runtime.

### Most natural candidate

Given current code, **RuntimeLoopToolDispatcher** is the most natural immediate
extraction candidate. It acknowledges that RuntimeLoop is not using the same
executable target model as `ToolExecutor`, preserves event vocabulary and tests,
and avoids introducing a new generic executor before the ownership boundaries are
settled.

A later `SharedToolExecutionService` may become natural if both ToolExecutor and
RuntimeLoop converge on common dispatch abstractions. A `ToolExecutorAdapter`
should wait until there is an explicit product decision that RuntimeLoop should
execute registered toolkit implementations and participate in the same
pending-action/approval lifecycle as `ToolExecutor`.

## 7. Risk assessment

Extracting `_run_tool_decision` next would have these risks:

- **Reduce duplication:** only modestly, if extraction is a
  `RuntimeLoopToolDispatcher`. It would reduce `RuntimeLoop` size and isolate
  handler dispatch, output validation, event emission, and evidence extraction,
  but the duplicated executor-like algorithm would still exist.
- **Simply move code:** likely, if the extraction is done before deciding whether
  RuntimeLoop should share ToolExecutor semantics. A behavior-preserving
  dispatcher extraction is primarily a boundary cleanup.
- **Accidentally create a second ToolExecutor:** high risk, if the extraction is
  framed as a generic shared execution service too early. A service that owns
  validation, policy routing, dispatch, event emission, pending-action choices,
  evidence, and result shaping would duplicate `ToolExecutor` unless it is
  explicitly designed as either a thin strategy-based core used by
  `ToolExecutor`, or a RuntimeLoop-only dispatcher.

## Recommendation

Do **not** adapt RuntimeLoop directly to `ToolExecutor` yet. The two paths share
validation, policy evaluation, and evidence extraction, but they intentionally
differ on dispatch target, event vocabulary, pending-action semantics,
approval/resume support, and result shape.

If the goal is only to continue thinning `RuntimeLoop`, extract a
behavior-preserving **`RuntimeLoopToolDispatcher`** next. Treat it as
RuntimeLoop-specific orchestration, not as a new shared executor.

If the goal is to reduce execution duplication across RuntimeLoop and
ToolExecutor, first design a shared execution core around explicit strategy
interfaces and migrate `ToolExecutor` to use that core. Otherwise, extracting
`_run_tool_decision` as a generic service risks creating a second ToolExecutor
with slightly different semantics.
