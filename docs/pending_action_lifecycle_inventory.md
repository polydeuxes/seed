# Pending-action lifecycle and approved-action resume inventory

> **Stale/quarantined RuntimeLoop-era inventory.** Current architecture treats `Runtime` as canonical and `RuntimeLoop` as deprecated/experimental, not CLI/API/default behavior. References to legacy/old Runtime or RuntimeLoop migration are historical audit wording, not current-core guidance; current architecture treats Runtime as canonical.


This is a source-file-based inventory only. It documents current behavior for pending confirmation/approval, pending-action status transitions, and approved-action resume. It intentionally proposes no implementation, refactor, runtime behavior change, CLI/API behavior change, test change, or event change.

## Scope and source files inspected

- Domain models: `seed_runtime/models.py` (`PolicyDecision`, `PendingAction`, `Approval`, status/outcome literals). [`seed_runtime/models.py:52-55`](../seed_runtime/models.py#L52-L55) [`seed_runtime/models.py:218-236`](../seed_runtime/models.py#L218-L236) [`seed_runtime/models.py:271-277`](../seed_runtime/models.py#L271-L277)
- Pending-action service: `seed_runtime/pending_actions.py`. [`seed_runtime/pending_actions.py:14-122`](../seed_runtime/pending_actions.py#L14-L122)
- Execution and resume: `seed_runtime/execution.py`. [`seed_runtime/execution.py:55-183`](../seed_runtime/execution.py#L55-L183) [`seed_runtime/execution.py:185-383`](../seed_runtime/execution.py#L185-L383)
- Policy: `seed_runtime/policy.py`. [`seed_runtime/policy.py:9-78`](../seed_runtime/policy.py#L9-L78)
- State projection: `seed_runtime/state.py`. [`seed_runtime/state.py:259-265`](../seed_runtime/state.py#L259-L265) [`seed_runtime/state.py:659-668`](../seed_runtime/state.py#L659-L668) [`seed_runtime/state.py:794-798`](../seed_runtime/state.py#L794-L798) [`seed_runtime/state.py:828-871`](../seed_runtime/state.py#L828-L871)
- Legacy runtime routing: `seed_runtime/runtime.py`. [`seed_runtime/runtime.py:37-67`](../seed_runtime/runtime.py#L37-L67) [`seed_runtime/runtime.py:298-310`](../seed_runtime/runtime.py#L298-L310)
- RuntimeLoop routing: `seed_runtime/runtime_loop.py`. [`seed_runtime/runtime_loop.py:123-157`](../seed_runtime/runtime_loop.py#L123-L157) [`seed_runtime/runtime_loop.py:395-626`](../seed_runtime/runtime_loop.py#L395-L626)
- CLI/API exposure: `scripts/seed_local.py`, `seed_runtime/api.py`. [`scripts/seed_local.py:828-843`](../scripts/seed_local.py#L828-L843) [`scripts/seed_local.py:1268-1320`](../scripts/seed_local.py#L1268-L1320) [`scripts/seed_local.py:3311-3333`](../scripts/seed_local.py#L3311-L3333) [`seed_runtime/api.py:15-44`](../seed_runtime/api.py#L15-L44)
- Tests: `tests/test_pending_actions.py`, `tests/test_action_resume.py`, `tests/test_policy.py`, `tests/test_tool_execution_policy.py`, `tests/test_runtime_loop.py`, and CLI action-plan approval assertions in `tests/test_seed_local_script.py`. [`tests/test_pending_actions.py:23-98`](../tests/test_pending_actions.py#L23-L98) [`tests/test_action_resume.py:25-159`](../tests/test_action_resume.py#L25-L159) [`tests/test_policy.py:38-53`](../tests/test_policy.py#L38-L53) [`tests/test_policy.py:74-121`](../tests/test_policy.py#L74-L121) [`tests/test_tool_execution_policy.py:130-153`](../tests/test_tool_execution_policy.py#L130-L153) [`tests/test_runtime_loop.py:898-923`](../tests/test_runtime_loop.py#L898-L923) [`tests/test_seed_local_script.py:1351-1379`](../tests/test_seed_local_script.py#L1351-L1379)

## 1. Models

### Policy outcomes related to pending actions

`PolicyOutcome` is `allow`, `block`, `require_confirmation`, or `require_approval`. [`seed_runtime/models.py:52`](../seed_runtime/models.py#L52) `PolicyDecision` stores:

- `outcome`: one of the `PolicyOutcome` values.
- `action`: the policy action, usually `ToolSpec.policy_action`.
- `reason`: human-readable policy explanation.
- `risk_class`: evaluated risk class.
- `approval_id`: optional approval that caused an `allow` decision. [`seed_runtime/models.py:218-224`](../seed_runtime/models.py#L218-L224)

`PolicyGate.evaluate()` creates the pending-action-triggering outcomes by risk class when no matching current approval exists:

- L1 returns `allow`.
- L2 returns `require_confirmation`.
- L3 returns `require_approval`.
- L4 returns `block`.
- Unknown actions are blocked when an explicit `action_risks` table is configured. [`seed_runtime/policy.py:25-73`](../seed_runtime/policy.py#L25-L73)

A matching `Approval` overrides risk and returns `allow` with `approval_id`; this means ordinary execution with a matching approval does not create a pending action. [`seed_runtime/policy.py:36-45`](../seed_runtime/policy.py#L36-L45)

### `PendingAction`

`PendingActionStatus` is `pending`, `approved`, `completed`, or `cancelled`. [`seed_runtime/models.py:54`](../seed_runtime/models.py#L54)

`PendingAction` fields are:

- `id`: generated with `new_id("pa")` by `PendingActionService.create_tool_call()`.
- `workspace_id`: defaults to `default` in the model, but creation passes the caller workspace.
- `action`: policy action, not necessarily the tool name.
- `tool_name`: registered tool name to resume.
- `arguments`: stored tool arguments; defaults to `{}` and are persisted as `to_plain(arguments)` at creation.
- `scope`: optional policy scope, copied from the original execution request.
- `status`: defaults to `pending`.
- `created_from_event_id`: usually the `tool.approval.required` event id.
- `causation_id`: optional original causation id. [`seed_runtime/models.py:226-236`](../seed_runtime/models.py#L226-L236) [`seed_runtime/pending_actions.py:35-45`](../seed_runtime/pending_actions.py#L35-L45)

Current assumptions encoded in services/tests:

- Pending actions are tool calls only; there is no generic pending-action type discriminator beyond `action`, `tool_name`, and `arguments`. [`seed_runtime/pending_actions.py:21-55`](../seed_runtime/pending_actions.py#L21-L55)
- A pending action is resumable only after its projected status is exactly `approved`. [`seed_runtime/execution.py:150-160`](../seed_runtime/execution.py#L150-L160)
- Completion is a status transition after successful resumed execution, not a separate result object stored on the pending action. [`seed_runtime/execution.py:175-183`](../seed_runtime/execution.py#L175-L183)
- The model has no `expires_at`, `approved_by`, retry count, result id, lock token, deduplication key, or completed output fields. [`seed_runtime/models.py:226-236`](../seed_runtime/models.py#L226-L236)

### `Approval`

`Approval` is a separate grant model, not the same thing as `PendingAction.status == "approved"`. It stores:

- `id`
- `action`
- `scope`
- `approved_by`
- `expires_at`
- `constraints` [`seed_runtime/models.py:271-277`](../seed_runtime/models.py#L271-L277)

State projection stores approvals from `approval.granted`; `State.has_approval()` matches by action, optionally by scope, and ignores expired grants. [`seed_runtime/state.py:794-798`](../seed_runtime/state.py#L794-L798) [`seed_runtime/state.py:659-668`](../seed_runtime/state.py#L659-L668)

Important model distinction: an `approval.granted` event can make future `PolicyGate.evaluate()` calls return `allow`, but it does not by itself transition a `PendingAction` to `approved`. Conversely, `PendingActionService.mark_approved()` emits `pending_action.approved`, but does not create an `Approval` model or `approval.granted` event. [`seed_runtime/pending_actions.py:57-74`](../seed_runtime/pending_actions.py#L57-L74) [`seed_runtime/state.py:794-798`](../seed_runtime/state.py#L794-L798)

## 2. Event lifecycle

### `tool.approval.required`

- **Emitter:** `ToolExecutor._policy_denied()` when policy outcome is `require_confirmation` or `require_approval`; despite the event name, it covers both confirmation and approval outcomes. [`seed_runtime/execution.py:275-287`](../seed_runtime/execution.py#L275-L287)
- **Payload:** `{"tool": tool.name, "policy": to_plain(policy)}`. The original tool arguments and scope are not included in this event payload. [`seed_runtime/execution.py:278-283`](../seed_runtime/execution.py#L278-L283)
- **Actor:** `system`. [`seed_runtime/execution.py:279-284`](../seed_runtime/execution.py#L279-L284)
- **Causation/correlation:** forwards `causation_id` and `correlation_id` passed into `ToolExecutor.execute()`. [`seed_runtime/execution.py:284-287`](../seed_runtime/execution.py#L284-L287)
- **Projector behavior:** no direct projection branch for `tool.approval.required`; its id becomes `PendingAction.created_from_event_id` when the pending action is created. [`seed_runtime/execution.py:291-302`](../seed_runtime/execution.py#L291-L302)

### `pending_action.created`

- **Emitter:** `PendingActionService.create_tool_call()`, currently called from `ToolExecutor._policy_denied()` for `require_confirmation` and `require_approval`. [`seed_runtime/pending_actions.py:21-55`](../seed_runtime/pending_actions.py#L21-L55) [`seed_runtime/execution.py:291-302`](../seed_runtime/execution.py#L291-L302)
- **Payload:** `{"pending_action": to_plain(pending_action)}`. This nested model includes stored `arguments`, `scope`, status `pending`, `created_from_event_id`, and `causation_id`. [`seed_runtime/pending_actions.py:35-49`](../seed_runtime/pending_actions.py#L35-L49)
- **Actor:** `system`. [`seed_runtime/pending_actions.py:46-51`](../seed_runtime/pending_actions.py#L46-L51)
- **Causation/correlation:** causation is `created_from_event_id or causation_id`; correlation is forwarded from creation caller. [`seed_runtime/pending_actions.py:51-53`](../seed_runtime/pending_actions.py#L51-L53)
- **Projector behavior:** creates/replaces `state.pending_actions[pending_action.id]` from the nested payload. [`seed_runtime/state.py:828-831`](../seed_runtime/state.py#L828-L831)

### `pending_action.approved`

- **Emitter:** `PendingActionService.mark_approved()`, via `_set_status(..., "approved")`. [`seed_runtime/pending_actions.py:57-74`](../seed_runtime/pending_actions.py#L57-L74) [`seed_runtime/pending_actions.py:95-122`](../seed_runtime/pending_actions.py#L95-L122)
- **Payload:** `{"pending_action_id": pending_action_id, "status": "approved"}`. [`seed_runtime/pending_actions.py:112-117`](../seed_runtime/pending_actions.py#L112-L117)
- **Actor:** `approver`. [`seed_runtime/pending_actions.py:117`](../seed_runtime/pending_actions.py#L117)
- **Causation/correlation:** caller-supplied values are forwarded. [`seed_runtime/pending_actions.py:118-120`](../seed_runtime/pending_actions.py#L118-L120)
- **Projector behavior:** if the pending action exists, updates its projected `status` to `approved`. Unknown ids are ignored by the projector, but `_set_status()` itself rejects unknown ids before emitting. [`seed_runtime/pending_actions.py:105-107`](../seed_runtime/pending_actions.py#L105-L107) [`seed_runtime/state.py:859-871`](../seed_runtime/state.py#L859-L871)

### `pending_action.completed`

- **Emitter:** `PendingActionService.mark_completed()`, currently called only by `ToolExecutor.resume_approved_tool_call()` after a resumed tool result has status `completed`. [`seed_runtime/pending_actions.py:76-93`](../seed_runtime/pending_actions.py#L76-L93) [`seed_runtime/execution.py:175-183`](../seed_runtime/execution.py#L175-L183)
- **Payload:** `{"pending_action_id": pending_action_id, "status": "completed"}`. [`seed_runtime/pending_actions.py:112-117`](../seed_runtime/pending_actions.py#L112-L117)
- **Actor:** `system`. [`seed_runtime/pending_actions.py:117`](../seed_runtime/pending_actions.py#L117)
- **Causation/correlation:** resume uses the `tool.call.completed` event id when available as the completion causation id, and preserves the reconstructed correlation id. [`seed_runtime/execution.py:175-182`](../seed_runtime/execution.py#L175-L182)
- **Projector behavior:** updates projected status to `completed`. [`seed_runtime/state.py:859-871`](../seed_runtime/state.py#L859-L871)

### `pending_action.cancelled`

- **Emitter:** no current service emits this event. `PendingActionService` exposes `mark_approved()` and `mark_completed()` only. [`seed_runtime/pending_actions.py:57-93`](../seed_runtime/pending_actions.py#L57-L93)
- **Payload supported by projector:** expected to include `pending_action_id` and optionally `status`; if `status` is absent, the projector derives `cancelled` from the event suffix. [`seed_runtime/state.py:859-867`](../seed_runtime/state.py#L859-L867)
- **Actor:** no service-defined actor because no service emits it.
- **Causation/correlation:** supported only insofar as any appended event carries event metadata; no current cancellation API sets it.
- **Projector behavior:** updates projected status to `cancelled` if the pending action exists. [`seed_runtime/state.py:859-871`](../seed_runtime/state.py#L859-L871)

### `pending_action.status_changed`

- **Emitter:** no current service emits this generic event. `_set_status()` emits event kinds of the form `pending_action.<status>` instead. [`seed_runtime/pending_actions.py:112-114`](../seed_runtime/pending_actions.py#L112-L114)
- **Payload supported by projector:** `pending_action_id` plus `status`; the projector includes this event kind in the same status-update branch. [`seed_runtime/state.py:859-871`](../seed_runtime/state.py#L859-L871)
- **Resume context behavior:** `ToolExecutor._resume_event_context()` treats `pending_action.status_changed` with status `approved` as an approval event for causation reconstruction. [`seed_runtime/execution.py:359-369`](../seed_runtime/execution.py#L359-L369)
- **Current behavior:** projector and resume logic support it, but services do not emit it.

### `approval.granted`

- **Emitter:** no pending-action service emits it. Tests append it directly for policy behavior; other code can append it to seed broad approval state. [`tests/test_policy.py:74-121`](../tests/test_policy.py#L74-L121)
- **Payload:** projector accepts either nested `{"approval": ...}` or direct approval fields; it parses `expires_at` then creates an `Approval`. [`seed_runtime/state.py:794-798`](../seed_runtime/state.py#L794-L798)
- **Actor:** event actor is not enforced by the projector. Tests use the default ledger actor because they do not pass one. [`tests/test_policy.py:74-89`](../tests/test_policy.py#L74-L89)
- **Causation/correlation:** no special pending-action reconstruction uses this event.
- **Projector behavior:** stores `state.approvals[approval.id]`; subsequent policy evaluation can return `allow` with that `approval_id`. [`seed_runtime/state.py:794-798`](../seed_runtime/state.py#L794-L798) [`seed_runtime/policy.py:36-45`](../seed_runtime/policy.py#L36-L45)

### Related operation implementation execution events during resume

- `tool.call.started`: emitted before loading/calling the registered operation, with payload `tool`, `arguments`, and optional `scope`; causation/correlation come from `_resume_event_context()` during resume. [`seed_runtime/execution.py:185-207`](../seed_runtime/execution.py#L185-L207)
- `tool.call.completed`: emitted after successful output validation, payload includes `tool` and `output`, causation is the started event id, and fact extraction observes it. [`seed_runtime/execution.py:244-260`](../seed_runtime/execution.py#L244-L260)
- `tool.call.failed`: emitted on execution/output-validation exceptions, payload includes `tool`, `error`, and phase `execution`; resume failures do not emit `pending_action.completed`. [`seed_runtime/execution.py:225-242`](../seed_runtime/execution.py#L225-L242) [`tests/test_action_resume.py:136-159`](../tests/test_action_resume.py#L136-L159)

## 3. Creation path

1. `ToolExecutor.execute()` calls the shared `ToolExecutionPolicyService.evaluate_with_state_factory()` to resolve/validate the tool and evaluate policy against projected state and optional scope. [`seed_runtime/execution.py:86-91`](../seed_runtime/execution.py#L86-L91)
2. If validation fails, the executor returns/raises failure before policy-created pending actions are considered. [`seed_runtime/execution.py:92-113`](../seed_runtime/execution.py#L92-L113)
3. If policy outcome is not `allow`, `_policy_denied()` handles `block`, `require_confirmation`, and `require_approval`. [`seed_runtime/execution.py:121-131`](../seed_runtime/execution.py#L121-L131)
4. `_policy_denied()` emits `tool.policy.blocked` for `block`; otherwise it emits `tool.approval.required`. [`seed_runtime/execution.py:275-287`](../seed_runtime/execution.py#L275-L287)
5. For `require_confirmation` and `require_approval`, `_policy_denied()` calls `PendingActionService.create_tool_call()` with:
   - `action=policy.action`
   - `tool_name=tool.name`
   - original `arguments`
   - original `scope`
   - `created_from_event_id=policy_event.id`
   - original `causation_id` and `correlation_id` [`seed_runtime/execution.py:291-302`](../seed_runtime/execution.py#L291-L302)
6. `create_tool_call()` stores `arguments` as `to_plain(arguments)`, stores `scope` unchanged, sets status `pending`, stores `created_from_event_id`, and stores original `causation_id` on the model. [`seed_runtime/pending_actions.py:35-45`](../seed_runtime/pending_actions.py#L35-L45)
7. The result returned to caller is a `ToolCallResult` with:
   - `kind` equal to the policy outcome.
   - `status` equal to `blocked`, `require_confirmation`, or `require_approval`.
   - `message` equal to `policy.reason`.
   - `policy` set to serialized policy.
   - `pending_action` set for confirmation/approval outcomes.
   - `payload` containing `policy` and, if created, serialized `pending_action`. [`seed_runtime/execution.py:288-312`](../seed_runtime/execution.py#L288-L312)

Creation behavior is covered for both L3 approval and L2 confirmation: `tests/test_pending_actions.py` verifies L3 creates `tool.approval.required` then `pending_action.created` without executing, and verifies an L2 path projects a pending action with stored arguments/scope. [`tests/test_pending_actions.py:23-73`](../tests/test_pending_actions.py#L23-L73)

## 4. Approval path

Current approval of a pending action means `PendingActionService.mark_approved()` setting pending-action status to `approved`. [`seed_runtime/pending_actions.py:57-74`](../seed_runtime/pending_actions.py#L57-L74)

Approval path facts:

- It projects current state and rejects unknown pending-action ids before emitting. [`seed_runtime/pending_actions.py:105-107`](../seed_runtime/pending_actions.py#L105-L107)
- It does not check the current status; approving an already completed/cancelled action would append a new `pending_action.approved` event if the id exists. [`seed_runtime/pending_actions.py:105-121`](../seed_runtime/pending_actions.py#L105-L121)
- It does not re-run policy. There is no call to `PolicyGate` or `ToolExecutionPolicyService` in `PendingActionService`. [`seed_runtime/pending_actions.py:14-122`](../seed_runtime/pending_actions.py#L14-L122)
- It does not create or require an `Approval` model. It emits `pending_action.approved`, not `approval.granted`. [`seed_runtime/pending_actions.py:112-117`](../seed_runtime/pending_actions.py#L112-L117)
- It records actor `approver`. [`seed_runtime/pending_actions.py:117`](../seed_runtime/pending_actions.py#L117)
- Existing test coverage calls the service directly, verifies projected status `approved`, event order, actor `approver`, and forwarded causation id. [`tests/test_pending_actions.py:76-98`](../tests/test_pending_actions.py#L76-L98)

Current caller/API/CLI exposure:

- There is no `SeedAPI` pending-action approve method; API exposes posting a user message, state, toolkits, registered operations/tools, and ToolNeeds / capability gaps. [`seed_runtime/api.py:15-44`](../seed_runtime/api.py#L15-L44)
- `scripts/seed_local.py` exposes action-plan approval (`--approve-plan`) but not pending-action approval. [`scripts/seed_local.py:828-843`](../scripts/seed_local.py#L828-L843) [`scripts/seed_local.py:3311-3333`](../scripts/seed_local.py#L3311-L3333)
- CLI tests explicitly assert `--approve-plan` appends `action_plan.approved` and not `pending_action.approved`, confirming that plan approval is not pending-action approval. [`tests/test_seed_local_script.py:1351-1379`](../tests/test_seed_local_script.py#L1351-L1379)

## 5. Resume path

### Where resume is implemented

Approved-action resume is implemented only in `ToolExecutor.resume_approved_tool_call()`. [`seed_runtime/execution.py:143-183`](../seed_runtime/execution.py#L143-L183)

### Required status

Resume requires that the projected pending action exists and has status exactly `approved`; unknown ids and every other status raise `ValueError`. [`seed_runtime/execution.py:150-160`](../seed_runtime/execution.py#L150-L160)

This gives current idempotency behavior: after successful completion, the projected status becomes `completed`, so a second resume attempt raises instead of executing again. [`seed_runtime/execution.py:175-183`](../seed_runtime/execution.py#L175-L183) [`tests/test_action_resume.py:112-133`](../tests/test_action_resume.py#L112-L133)

### Tool lookup behavior

Resume uses `registry.require(pending_action.tool_name)`, then `_execute_allowed_tool_call()` uses `_load_registered()` to ensure a matching registered implementation exists and imports the implementation path. [`seed_runtime/execution.py:165-166`](../seed_runtime/execution.py#L165-L166) [`seed_runtime/execution.py:385-396`](../seed_runtime/execution.py#L385-L396)

Notably, resume does not call `ToolExecutionPolicyService.evaluate()`, so it does not re-run input validation or current policy before execution. It relies on stored arguments from the pending action and then validates output after execution. [`seed_runtime/execution.py:166-174`](../seed_runtime/execution.py#L166-L174) [`seed_runtime/execution.py:222-224`](../seed_runtime/execution.py#L222-L224)

### Argument/scope reconstruction

Resume uses the stored pending-action arguments and scope directly:

- `pending_action.arguments` is passed to `_execute_allowed_tool_call()`.
- `scope=pending_action.scope` is forwarded and included in `tool.call.started` payload if non-null. [`seed_runtime/execution.py:166-174`](../seed_runtime/execution.py#L166-L174) [`seed_runtime/execution.py:196-199`](../seed_runtime/execution.py#L196-L199)

The successful resume test verifies `tool.call.started` receives the original arguments and scope. [`tests/test_action_resume.py:76-84`](../tests/test_action_resume.py#L76-L84)

### Causation/correlation reconstruction

`_resume_event_context()` starts causation from `pending_action.created_from_event_id or pending_action.causation_id`, then scans ledger events in reverse. [`seed_runtime/execution.py:343-350`](../seed_runtime/execution.py#L343-L350)

During the reverse scan:

- It records the matching `pending_action.created` event to recover correlation.
- It treats a matching `pending_action.approved` or `pending_action.status_changed` with status `approved` as the resume causation event and uses that event's correlation when present. [`seed_runtime/execution.py:350-370`](../seed_runtime/execution.py#L350-L370)

Fallback correlation lookup uses:

1. The matching `pending_action.created` event correlation.
2. The event referenced by `pending_action.created_from_event_id`.
3. The event referenced by `pending_action.causation_id`. [`seed_runtime/execution.py:372-381`](../seed_runtime/execution.py#L372-L381)

The resume test verifies `tool.call.started.causation_id` is the approval event id and correlation is preserved. [`tests/test_action_resume.py:76-85`](../tests/test_action_resume.py#L76-L85)

### Execution behavior

Resume delegates to `_execute_allowed_tool_call()`, which emits `tool.call.started`, imports the registered function, calls it with `ToolContext`, validates output schema, emits `tool.call.completed` on success, extracts facts from the completed event, and returns a completed `ToolCallResult`. [`seed_runtime/execution.py:185-260`](../seed_runtime/execution.py#L185-L260)

### Completion behavior

If the resumed result status is `completed`, resume calls `PendingActionService.mark_completed()` and uses the completed tool-call event id as causation when available. [`seed_runtime/execution.py:175-183`](../seed_runtime/execution.py#L175-L183)

The successful resume test verifies event order `tool.call.started`, `tool.call.completed`, fact observation, then `pending_action.completed`, and projected status `completed`. [`tests/test_action_resume.py:50-75`](../tests/test_action_resume.py#L50-L75)

### Failure behavior

If the resumed tool call fails during execution or output validation, `_execute_allowed_tool_call()` emits `tool.call.failed` and returns `ToolCallResult(status="failed")`. Resume does not mark the pending action completed unless result status is `completed`, so failed resumes leave the pending action status `approved`. [`seed_runtime/execution.py:225-242`](../seed_runtime/execution.py#L225-L242) [`seed_runtime/execution.py:175-183`](../seed_runtime/execution.py#L175-L183)

The failure test verifies status remains `approved`, event order ends with `tool.call.failed`, and no `pending_action.completed` is emitted. [`tests/test_action_resume.py:136-159`](../tests/test_action_resume.py#L136-L159)

### Idempotency / exactly-once behavior

Current exactly-once behavior is status-based, not lock-based:

- Successful resume changes the durable projected status to `completed`; a later resume raises because status is no longer `approved`. [`seed_runtime/execution.py:150-160`](../seed_runtime/execution.py#L150-L160) [`seed_runtime/execution.py:175-183`](../seed_runtime/execution.py#L175-L183)
- Failed resume leaves status `approved`, so the same pending action can be retried by calling resume again. [`tests/test_action_resume.py:136-159`](../tests/test_action_resume.py#L136-L159)
- There is no in-flight marker, lease, compare-and-swap, or deduplication key in the model/service. [`seed_runtime/models.py:226-236`](../seed_runtime/models.py#L226-L236) [`seed_runtime/pending_actions.py:95-122`](../seed_runtime/pending_actions.py#L95-L122)

## 6. Cancellation / expiry path

- **Cancellation service:** not implemented. There is no `mark_cancelled()` method in `PendingActionService`. [`seed_runtime/pending_actions.py:57-93`](../seed_runtime/pending_actions.py#L57-L93)
- **Cancellation projection:** supported if an event `pending_action.cancelled` is appended manually; projector updates status. [`seed_runtime/state.py:859-871`](../seed_runtime/state.py#L859-L871)
- **Expiry model:** pending actions have no expiry field. [`seed_runtime/models.py:226-236`](../seed_runtime/models.py#L226-L236)
- **Expiry service:** no pending-action expiry service or event appears in inspected sources.
- **Approval expiry:** broad `Approval` grants can expire through `Approval.expires_at` and `State.has_approval()` filtering, but this is separate from pending-action approval status. [`seed_runtime/models.py:271-277`](../seed_runtime/models.py#L271-L277) [`seed_runtime/state.py:659-668`](../seed_runtime/state.py#L659-L668)
- **`pending_action.status_changed`:** projector and resume causation logic support it, but no current service emits it. [`seed_runtime/state.py:859-871`](../seed_runtime/state.py#L859-L871) [`seed_runtime/execution.py:359-369`](../seed_runtime/execution.py#L359-L369) [`seed_runtime/pending_actions.py:112-114`](../seed_runtime/pending_actions.py#L112-L114)

## 7. Runtime vs RuntimeLoop

### Canonical `Runtime` / `ToolExecutor` (called legacy in this historical inventory)

Canonical `Runtime` owns a `ToolExecutor` dependency (this historical inventory previously called it legacy). [`seed_runtime/runtime.py:37-55`](../seed_runtime/runtime.py#L37-L55) For `call_tool`, `_route()` calls `ToolExecutor.execute()` with workspace, session, tool name, decision arguments, and causation id, then maps the `ToolCallResult` kind/message/payload into `RuntimeResponse`. [`seed_runtime/runtime.py:298-310`](../seed_runtime/runtime.py#L298-L310)

`ToolExecutor` implements the complete current pending-action lifecycle subset:

- Shared validation and policy evaluation before execution. [`seed_runtime/execution.py:86-121`](../seed_runtime/execution.py#L86-L121)
- Pending-action creation for `require_confirmation` and `require_approval`. [`seed_runtime/execution.py:263-312`](../seed_runtime/execution.py#L263-L312)
- Direct allowed operation implementation execution with `tool.call.*` events. [`seed_runtime/execution.py:185-260`](../seed_runtime/execution.py#L185-L260)
- Approved pending-action resume, completion, and failure behavior. [`seed_runtime/execution.py:143-183`](../seed_runtime/execution.py#L143-L183)

`Runtime` itself does not expose approval or resume as a user-message decision kind; resume is a `ToolExecutor` method that external callers/tests invoke directly. [`seed_runtime/runtime.py:252-354`](../seed_runtime/runtime.py#L252-L354) [`tests/test_action_resume.py:50-159`](../tests/test_action_resume.py#L50-L159)

### RuntimeLoop

RuntimeLoop uses the same shared `ToolExecutionPolicyService`, but handles non-allow policy outcomes as denial rather than pending actions. [`seed_runtime/runtime_loop.py:145-154`](../seed_runtime/runtime_loop.py#L145-L154) [`seed_runtime/runtime_loop.py:395-484`](../seed_runtime/runtime_loop.py#L395-L484)

Current RuntimeLoop behavior for a policy non-allow outcome:

- Emits `runtime.policy.denied` with tool name, tool args, serialized policy, and decision reason.
- Records a decision journal outcome `policy_denied`.
- Returns `RuntimeResult` with `policy_allowed=False`, an error string, and no pending-action id. [`seed_runtime/runtime_loop.py:440-484`](../seed_runtime/runtime_loop.py#L440-L484)

RuntimeLoop lacks all of the following pending-action behaviors:

- No `PendingActionService` construction or use. [`seed_runtime/runtime_loop.py:123-157`](../seed_runtime/runtime_loop.py#L123-L157)
- No `tool.approval.required` event emission.
- No `pending_action.created` event emission.
- No distinction between `require_confirmation`, `require_approval`, and `block` beyond serialized policy inside `runtime.policy.denied`.
- No pending-action approval path.
- No approved-action resume method.
- No pending-action completion/cancellation path.
- No RuntimeLoop test asserting pending-action creation or resume; the existing non-allow test asserts denial and no operation implementation execution. [`tests/test_runtime_loop.py:898-923`](../tests/test_runtime_loop.py#L898-L923)

## 8. CLI/API exposure

### CLI (`scripts/seed_local.py`)

Current inspected CLI lifecycle flags are for preconditions, proposals, handoffs, execution authorization, action-plan acceptance/approval/rejection/supersession, and inspection/reporting features. Pending-action list/approve/resume/cancel flags do not appear in the parser or lifecycle routing. [`scripts/seed_local.py:828-843`](../scripts/seed_local.py#L828-L843) [`scripts/seed_local.py:1268-1320`](../scripts/seed_local.py#L1268-L1320)

Action-plan approval is exposed through `--approve-plan`, implemented by `ActionPlanService.approve_plan()`, and returns an action-plan-shaped payload. [`scripts/seed_local.py:3311-3333`](../scripts/seed_local.py#L3311-L3333) This is not pending-action approval; tests assert it does not append `pending_action.approved`. [`tests/test_seed_local_script.py:1351-1379`](../tests/test_seed_local_script.py#L1351-L1379)

Current user-facing pending-action capabilities through CLI:

- List pending actions: not exposed as a dedicated command. State-oriented commands may reveal projected state, but there is no pending-action-specific list route in inspected lifecycle flags.
- Approve pending actions: not exposed.
- Resume pending actions: not exposed.
- Cancel pending actions: not exposed.

### API (`seed_runtime/api.py`)

Historical note: this audit described `SeedAPI` as wrapping RuntimeLoop. Current architecture uses canonical Runtime; the historical inventory exposed only:

- `post_user_message()`
- `get_state()`
- `get_toolkits()`
- `get_tools()`
- `get_tool_needs()` [`seed_runtime/api.py:15-44`](../seed_runtime/api.py#L15-L44)

Current user-facing pending-action capabilities through this API shell:

- List pending actions: only indirectly via `get_state()` returning full projected state; no dedicated method.
- Approve pending actions: not exposed.
- Resume pending actions: not exposed.
- Cancel pending actions: not exposed.

Historical note: this audit described API messages as going through RuntimeLoop; current architecture uses canonical Runtime. In that historical path, policy-gated RuntimeLoop tool calls currently return policy denial rather than creating pending actions. [`seed_runtime/api.py:23-32`](../seed_runtime/api.py#L23-L32) [`seed_runtime/runtime_loop.py:440-484`](../seed_runtime/runtime_loop.py#L440-L484)

## 9. Test coverage

### Covered

- **`require_confirmation` pending creation:** `test_pending_action_is_projected_in_state()` configures L2 and verifies a pending action is projected with status, workspace, action, tool name, arguments, scope, and source event linkage. [`tests/test_pending_actions.py:55-73`](../tests/test_pending_actions.py#L55-L73)
- **`require_approval` pending creation:** `test_approval_required_tool_does_not_execute()` configures L3, verifies no operation implementation execution, event order `tool.approval.required` then `pending_action.created`, pending status, action/tool/arguments/scope. [`tests/test_pending_actions.py:23-52`](../tests/test_pending_actions.py#L23-L52)
- **Policy outcomes:** `tests/test_policy.py` covers L2 `require_confirmation`, L3 `require_approval`, broad matching approval allowing execution, and nonmatching approval still requiring approval. [`tests/test_policy.py:38-53`](../tests/test_policy.py#L38-L53) [`tests/test_policy.py:74-121`](../tests/test_policy.py#L74-L121)
- **Shared execution-policy non-allow results:** `tests/test_tool_execution_policy.py` covers L2 and L3 returning non-allow and `allowed_to_execute is False`. [`tests/test_tool_execution_policy.py:130-153`](../tests/test_tool_execution_policy.py#L130-L153)
- **Approval event status transition:** `test_approval_event_can_mark_pending_action_approved()` covers direct `PendingActionService.mark_approved()`, projected status transition, event order, actor, and causation. [`tests/test_pending_actions.py:76-98`](../tests/test_pending_actions.py#L76-L98)
- **Resume success:** `test_approved_pending_action_resumes_echo_tool()` covers resumed output, projected completed status, event order, stored argument/scope replay, approval causation, and correlation preservation. [`tests/test_action_resume.py:50-85`](../tests/test_action_resume.py#L50-L85)
- **Resume before approval rejection:** `test_pending_action_cannot_resume_before_approval()` verifies resume raises and the tool is not called before approval. [`tests/test_action_resume.py:88-109`](../tests/test_action_resume.py#L88-L109)
- **Resume twice rejection:** `test_completed_action_cannot_resume_twice()` verifies second resume raises after completion and only one tool call/completion event occurs. [`tests/test_action_resume.py:112-133`](../tests/test_action_resume.py#L112-L133)
- **Failed resume remains approved:** `test_failed_resumed_tool_does_not_mark_completed()` verifies failed resumed execution leaves status `approved` and does not emit completion. [`tests/test_action_resume.py:136-159`](../tests/test_action_resume.py#L136-L159)
- **RuntimeLoop lack of pending-action support by behavior:** `test_loop_policy_denial_prevents_tool_execution()` verifies RuntimeLoop emits `runtime.policy.denied`, records `policy_denied`, and does not call the tool for L4 block. It does not explicitly cover L2/L3 pending-action absence. [`tests/test_runtime_loop.py:898-923`](../tests/test_runtime_loop.py#L898-L923)
- **CLI action-plan approval is separate:** `test_cli_approve_plan_prints_approved_without_executing_or_registering()` verifies action-plan approval and explicitly asserts no `pending_action.approved`. [`tests/test_seed_local_script.py:1351-1379`](../tests/test_seed_local_script.py#L1351-L1379)

### Missing or partial

- No test for pending-action cancellation, because no cancellation service exists.
- No test for pending-action expiry, because no expiry model/service exists.
- No test that `pending_action.status_changed` projects status changes or participates in resume causation, despite projector/resume support.
- No test that `approval.granted` by itself does not approve an existing pending action.
- No test that `mark_approved()` can re-approve a completed/cancelled pending action, or that it should not; current behavior has no status guard.
- No test for unknown pending-action id in `mark_completed()` or `mark_approved()` beyond service code path.
- No test for unknown pending-action id in `resume_approved_tool_call()`.
- No test for resume tool lookup failure, missing import, implementation mismatch, invalid implementation reference, or output-schema failure specifically under resume.
- No test for retrying a failed resume; current behavior leaves status `approved`, but a second retry is not asserted.
- No explicit RuntimeLoop L2/L3 tests showing `require_confirmation` / `require_approval` become `runtime.policy.denied` with no pending action. The existing RuntimeLoop policy-denial test uses L4 block. [`tests/test_runtime_loop.py:898-923`](../tests/test_runtime_loop.py#L898-L923)
- No CLI/API tests for pending-action list, approve, resume, or cancel, because those routes do not exist.

## 10. Migration risk

If canonical `Runtime` (called legacy in this historical audit) / `ToolExecutor` pending-action lifecycle were removed before RuntimeLoop parity exists, current source behavior would lose or change these capabilities:

- L2 `require_confirmation` and L3 `require_approval` tool calls would no longer create durable `PendingAction` records; RuntimeLoop currently records policy denial instead. [`seed_runtime/execution.py:291-312`](../seed_runtime/execution.py#L291-L312) [`seed_runtime/runtime_loop.py:440-484`](../seed_runtime/runtime_loop.py#L440-L484)
- Existing `tool.approval.required` and `pending_action.created` event consumers/tests would lose those events on policy-gated calls. [`tests/test_pending_actions.py:23-52`](../tests/test_pending_actions.py#L23-L52)
- Approved pending-action resume would disappear, including stored argument/scope replay, approval-event causation reconstruction, completion transition, and failed-resume-stays-approved behavior. [`seed_runtime/execution.py:143-183`](../seed_runtime/execution.py#L143-L183) [`tests/test_action_resume.py:50-159`](../tests/test_action_resume.py#L50-L159)
- Status-based exactly-once-after-success semantics would disappear. [`tests/test_action_resume.py:112-133`](../tests/test_action_resume.py#L112-L133)
- Broader approvals through `approval.granted` would still work at the state/policy layer if RuntimeLoop keeps using `PolicyGate`, but this does not replace per-pending-action approval/resume semantics. [`seed_runtime/state.py:794-798`](../seed_runtime/state.py#L794-L798) [`seed_runtime/policy.py:36-45`](../seed_runtime/policy.py#L36-L45)
- Any downstream audit/reporting relying on `pending_action.*` event vocabulary would see a different vocabulary (`runtime.policy.denied`, `tool.result`, `tool.failure`, and decision records) for RuntimeLoop calls. [`seed_runtime/runtime_loop.py:440-626`](../seed_runtime/runtime_loop.py#L440-L626)

The migration risk is therefore a user-visible safety/workflow regression, not only an internal routing or naming change.

## 11. Extraction / port candidates only

The following are boundary candidates identified from current source shape. They are listed only to support architectural decision-making; this inventory does not implement or recommend any one path.

- **PendingActionService expansion:** current service owns creation and two status transitions but lacks cancellation, status guards, expiry, approval-grant integration, and list helpers. [`seed_runtime/pending_actions.py:14-122`](../seed_runtime/pending_actions.py#L14-L122)
- **ApprovalResumeService:** resume logic currently lives inside `ToolExecutor`, combining pending-action lookup/status checks, causation/correlation reconstruction, registered implementation dispatch, completion marking, and failure semantics. [`seed_runtime/execution.py:143-183`](../seed_runtime/execution.py#L143-L183) [`seed_runtime/execution.py:343-383`](../seed_runtime/execution.py#L343-L383)
- **RuntimeLoop pending-action routing:** RuntimeLoop's non-allow policy branch is a single denial branch; a parity port would need a boundary at the post-policy, pre-handler point. [`seed_runtime/runtime_loop.py:440-484`](../seed_runtime/runtime_loop.py#L440-L484)
- **Shared resume executor:** direct operation implementation execution for legacy resume uses registered implementation import paths and `tool.call.*` events, while RuntimeLoop uses injected handlers and `tool.result` / `tool.failure` events. Any shared executor boundary would have to decide which dispatch/event contract it owns. [`seed_runtime/execution.py:185-260`](../seed_runtime/execution.py#L185-L260) [`seed_runtime/runtime_loop.py:486-626`](../seed_runtime/runtime_loop.py#L486-L626)
- **CLI/API approval surface:** no current CLI/API route covers pending-action list, approval, resume, or cancellation; the only approval-style CLI route is action-plan approval. [`scripts/seed_local.py:828-843`](../scripts/seed_local.py#L828-L843) [`scripts/seed_local.py:3311-3333`](../scripts/seed_local.py#L3311-L3333) [`seed_runtime/api.py:15-44`](../seed_runtime/api.py#L15-L44)
