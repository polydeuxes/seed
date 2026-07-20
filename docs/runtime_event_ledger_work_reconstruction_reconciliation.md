---
doc_type: reconciliation
status: implementation-backed finding
domain: runtime event ledger reconstruction
reconciles:
  - runtime work reconstruction
  - event ledger evidence boundary
  - transient execution evidence boundary
defines:
  - runtime event ledger work reconstruction
  - event-backed runtime work evidence
  - transient runtime evidence boundary
depends_on:
  - runtime_orientation_evidence_inventory.md
related:
  - runtime_orientation_reconciliation.md
  - preservation_vs_continuation_investigation.md
  - observation_question_template_reconciliation.md
---

# Runtime Event Ledger Work Reconstruction Reconciliation

## Scope

This report is observational. It asks whether the current event ledger preserves enough implementation-backed evidence to reconstruct Seed's own completed runtime work, and which execution evidence remains transient. It does not propose a planner, scheduler, runtime memory model, internal thought log, continuous execution, or agent loop.

Repository authority comes from the current implementation in `seed_runtime/`.

## Commands executed

```text
pwd
rg --files -g 'AGENTS.md' -g '!tmp' -g '!venv'
git status --short
cat AGENTS.md
rg -n "event ledger|EventLedger|append|DecisionInputPacket|projection|observation|runtime|tool execution|state patch|response" -S .
sed -n '1,240p' seed_runtime/events.py
sed -n '1,260p' seed_runtime/runtime.py
sed -n '1,220p' seed_runtime/execution.py
sed -n '1,220p' seed_runtime/state.py
sed -n '220,520p' seed_runtime/runtime.py
sed -n '120,380p' seed_runtime/execution.py
rg -n "event.kind|kind ==|elif kind|append\(" seed_runtime/state.py seed_runtime/observations.py seed_runtime/state_patches.py seed_runtime/tool_needs.py seed_runtime/projection_store.py seed_runtime/models.py
sed -n '760,1110p' seed_runtime/state.py
sed -n '1,180p' seed_runtime/state_patches.py
sed -n '1,190p' seed_runtime/tool_needs.py
sed -n '130,190p' seed_runtime/observations.py
sed -n '1,220p' seed_runtime/context.py
rg -n "class Event|class RuntimeResponse|class Decision|class Observation|class Fact" seed_runtime/models.py
sed -n '1,120p' seed_runtime/models.py
sed -n '220,360p' seed_runtime/models.py
sed -n '1,120p' seed_runtime/projection_store.py
```

## Files inspected

- `AGENTS.md`
- `seed_runtime/events.py`
- `seed_runtime/runtime.py`
- `seed_runtime/execution.py`
- `seed_runtime/state.py`
- `seed_runtime/state_patches.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/observations.py`
- `seed_runtime/context.py`
- `seed_runtime/models.py`
- `seed_runtime/projection_store.py`

## Files changed

- `docs/runtime_event_ledger_work_reconstruction_reconciliation.md`

## LOC changed

- Added one documentation report.

## Tests run

No automated tests were run. This change is an observational documentation report and does not modify runtime code, diagnostic surfaces, event definitions, projection behavior, or runnable application behavior.

## Implementation baseline

The ledger is append-only runtime history. `EventLedger.append()` constructs an `Event` with kind, workspace, actor, payload, session, causation, and correlation metadata, stores it by id and workspace, and returns the stored event. `SQLiteEventLedger` persists the same public event model in a SQLite `events` table. The `Event` model has open string `kind`, timestamp, payload, actor, session, causation, and correlation fields, and rejects secret fields in event payloads.

Projection is replay-based. `StateProjector.project()` reads ledger events for a workspace, `project_from_state()` applies them in append order, records `last_event_id`, and then finalizes derived indexes. Projection snapshots are explicitly derived caches: event ledgers own append-only history, while projection stores own reusable snapshots derived from those events.

## Event coverage matrix

| Runtime activity | Event generated | Projection impact | Durable evidence | Transient evidence | Reconstructable from ledger/projection/observations? | Strongest supporting evidence | Strongest contradictory evidence |
|---|---|---|---|---|---|---|---|
| Operator input | `input.user_message` | No direct `StateProjector.apply()` branch | User text, actor `user`, session id, event id | The composed `DecisionInputPacket` built after projection | Yes for submitted input; no for the exact composed context unless inferred from surrounding state | `Runtime.handle_user_message()` appends `input.user_message` before projection and decision composition | `StateProjector.apply()` has no branch for `input.user_message`, so projected `State` does not expose it as domain state |
| State projection before decision | No event | Projection is computed by replay; `last_event_id` recorded in the in-memory state/snapshot | Durable only if a projection snapshot is saved elsewhere; event ledger remains authority | Local `state` object and projection diagnostics | Reconstructable by replaying ledger; snapshot can justify current projected state when available | `project_from_state()` materializes events, applies each, and finalizes derived indexes | Projection timing diagnostics are optional and non-authoritative |
| Decision input composition | No event | None | Equivalent source evidence exists in input event plus projected state at that point, but not the budgeted packet itself | `DecisionInputPacket`, context budget trace, selected tools/facts/evidence | Partially: source state can be reconstructed, exact budgeted packet only if deterministically recomposed with same code/config | `DecisionInputComposer.compose()` returns a packet from the input event, projected state, registry tools, and budgeted sections | No ledger append occurs in composer; `StaticDecisionProducer` keeps only `last_decision_input` in memory |
| Decision produced | `model.decision.proposed` | No direct projection branch | Full serialized decision and attempt number, causally linked to input event | Validator object/result unless failure recorded | Yes for what the model proposed | Runtime appends `model.decision.proposed` before validation | Projection ignores `model.decision.proposed` |
| Decision schema validation failure | `model.decision.invalid` | No direct projection branch | Validation errors and attempt number, causally linked to decision event | `validation` result object and retry packet | Yes for failed validation and retry attempts that produced events | Runtime appends `model.decision.invalid` and builds retry input | Final `RuntimeResponse(kind="invalid_decision")` is not appended |
| Tool-intent validation rejection | `model.decision.intent_rejected` | No direct projection branch | Intent errors and attempt number | Guard internals and retry packet | Yes for rejection; no for full transient guard context | Runtime appends `model.decision.intent_rejected` on intent mismatch | Projection ignores it |
| Answer response | `response.answer` | No direct projection branch | Answer text, session, causation to decision | Returned `RuntimeResponse` object | Yes from ledger, but not from projected domain state | `_route()` appends `response.answer` | Projection ignores response events |
| Question response | `response.question` | No direct projection branch | Question text, session, causation to decision | Returned `RuntimeResponse` object | Yes from ledger, but not from projected domain state | `_route()` appends `response.question` | Projection ignores response events |
| Refusal response | `response.refusal` | No direct projection branch | Refusal reason, session, causation to decision | Returned `RuntimeResponse` object | Yes from ledger, but not from projected domain state | `_route()` appends `response.refusal` | Projection ignores response events |
| Tool need creation | `tool_need.created` unless an equivalent open need already exists | Projects into `state.tool_needs`; open needs derive from state | ToolNeed payload, requested-by event id, reason, capability, desired inputs/outputs | Recommendation ranking and capability-resolution response metadata | Yes for created need; duplicate detection returns existing need without a new event | `ToolNeedService.create_from_decision()` appends `tool_need.created`; projector handles it | If an existing open need matches, the method returns it without appending a new event for the current request |
| Tool need status change | `tool_need.status_changed` | Updates projected tool need status | Need id and new status | Returned replaced object | Yes if the original need is in projected state | `ToolNeedService.set_status()` appends status change; projector applies it | None for status change itself |
| Capability resolution / provider recommendation for request_tool | No event | None | Durable only indirectly if tool need was created; response payload may be caller-visible but not ledger durable | Ranked recommendations, registered operation candidates, handoff candidates, capability resolution payload | No, except by recomputing with same catalog/registry at that time | `resolve_capability()` docstring says it is read-only and does not mutate registry/catalog state | Runtime returns recommendation payload without appending it |
| Tool execution start | `tool.call.started` | No direct projection branch | Tool name, arguments, optional scope, causation/correlation | Policy evaluation result and loaded callable | Yes for attempted allowed execution | `_execute_allowed_tool_call()` appends `tool.call.started` before loading/running the operation | Projection ignores tool call lifecycle events |
| Tool execution success | `tool.call.completed` plus possible fact extraction events | Tool call lifecycle itself ignored; extracted observation/fact/evidence events can project | Tool output; extracted facts/evidence if `FactExtractionService` emits them | Python return object, output validation object | Yes for completed call and output; domain impact only if emitted as observation/evidence/fact events | `_execute_allowed_tool_call()` appends `tool.call.completed` and invokes `observe_tool_result()` | Output validation context and local operation details are not stored separately |
| Tool execution failure | `tool.call.failed` | No direct projection branch | Tool name, error string, phase | Exception object and stack/context | Yes for failure phase/error at summary level | `_execute_allowed_tool_call()` catches exceptions and appends `tool.call.failed`; `_failed()` records validation/status failures | Unknown-tool `registry.require()` can raise before a failed event is appended when no tool can be resolved |
| Tool policy blocked / approval required | `tool.policy.blocked` or `tool.approval.required`; confirmation/approval also creates `pending_action.created` | Policy event ignored; pending action projects into `state.pending_actions` | Policy payload; pending action tool, args, scope, status | Full policy evaluation context/state factory output | Yes for blocked/approval-required outcome and pending action when created | `_policy_denied()` appends policy event and creates pending action for confirmation/approval | Policy evaluation itself is not a projected domain object |
| Pending action completion after approved resume | `tool.call.started`, `tool.call.completed`, then `pending_action.completed` if success | Pending action status updates to completed | Resume causation/correlation found from ledger and status change event | Local resume lookup variables | Yes for successful resumed execution | `resume_approved_tool_call()` executes and marks completed when result status is completed | Failed resumed execution does not mark completed; incompleteness is inferred from pending status plus tool failure |
| State patch accepted | `entity.upserted`, `evidence.observed`, `fact.observed`, and/or `goal.created` per operation | Projects into entities, evidence, facts, goals | Domain event payloads and causation to decision event | StatePatchResult wrapper and operation parsing locals | Yes for applied domain mutations | `StatePatchService.apply()` translates operations into ledger events; projector has branches for those event kinds | No wrapper event records "state patch accepted" as a single operation |
| State patch rejected | `state.patch.rejected` | No direct projection branch | Error and rejected patch payload | Exception object | Yes for rejection in ledger; not in projected state | Runtime catches `StatePatchError` and appends `state.patch.rejected` | Projection ignores it |
| Observation ingestion | `observation.observed`, `evidence.observed`, and optionally `fact.observed` / `fact.inferred` via `append_many()` | Projects observations, evidence, facts; finalization derives relationships, aliases, conflicts, inferred facts | Observation, evidence, fact payloads with batch-preserving event granularity | Collection source objects, normalization pipeline locals, status/progress | Yes for ingested observations/facts/evidence | `ObservationIngestor` builds per-observation events and ledger `append_many()` preserves each supplied event as its own event | Collection activity/progress itself is emitted through status consumer, not ledger events |
| Projection finalization | No event | Mutates in-memory projected indexes derived from replay | Durable only as snapshot if saved through projection store | Alias resolver, relationship lists, graph issues, conflicts, diagnostics | Reconstructable by replaying ledger with implementation; snapshot can cache result | `finalize()` rebuilds derived indexes after event application | No ledger event says projection was updated |
| Projection snapshot save/load | No ledger event | Snapshot cache stores derived state | Snapshot rows if a store is used | Store operation locals | Reconstructable as cache, not authoritative history | Projection store module states snapshots are derived from events | Event ledger does not record snapshot creation |
| Unsupported valid decision kind | No event | None | Prior `model.decision.proposed` only | Returned unsupported response | Partially: proposed decision remains, unsupported response does not | `_route()` falls through to `RuntimeResponse(kind="unsupported")` | No event appended for unsupported route response |

## Activities that currently append events

The implementation appends events for these runtime categories:

1. User/operator input: `input.user_message`.
2. Model decision proposals: `model.decision.proposed`.
3. Decision parse failures: `model.decision.parse_failed`.
4. Decision validation failures: `model.decision.invalid`.
5. Tool-intent rejections: `model.decision.intent_rejected`.
6. Response emissions for answer, question, and refusal: `response.answer`, `response.question`, `response.refusal`.
7. Tool needs and status changes: `tool_need.created`, `tool_need.status_changed`.
8. Tool execution lifecycle: `tool.call.started`, `tool.call.completed`, `tool.call.failed`.
9. Tool policy outcomes: `tool.policy.blocked`, `tool.approval.required`.
10. Pending actions through the pending-action service when policy requires confirmation or approval, and completion after successful approved resume.
11. State patch domain mutations: `entity.upserted`, `evidence.observed`, `fact.observed`, `goal.created`.
12. State patch rejection: `state.patch.rejected`.
13. Observation ingestion: `observation.observed`, `evidence.observed`, `fact.observed`, and `fact.inferred`.
14. Legacy/side-path projected events supported by `StateProjector.apply()`: approvals, execution authorizations, execution proposals, handoff plans, action plans, and tool registration.

## Activities that intentionally do not append events

These omissions are implementation-backed rather than speculative:

1. Decision input composition does not append an event. It returns a `DecisionInputPacket` built from the current input event, projected state, registry tools, and budget-selected sections.
2. Projection replay and finalization do not append events. Projection reads events, applies known kinds to state, and finalizes derived indexes. Projection diagnostics are optional counters/timings, not ledger records.
3. Projection cache save/load does not append ledger events. Projection stores are explicitly derived snapshot stores; the event ledger remains authoritative history.
4. Capability resolution and provider recommendation do not append events. `resolve_capability()` states that it is read-only and does not execute tools, authorize actions, create pending actions, or mutate registry/catalog state; runtime returns this metadata in the response payload.
5. Duplicate tool-need requests do not append a new event when an equivalent open need already exists. The service returns the existing need.
6. Successful state patches do not append a single wrapper event that says "state patch accepted". Instead, each accepted operation becomes its own domain event.
7. The final returned `RuntimeResponse` object is not generally appended for tool results, tool needs, invalid decisions, state updates, or unsupported decisions. Only answer/question/refusal response surfaces have explicit response events.
8. Collection/progress/status messages used during event persistence, ingestion, and projection are emitted to `ExecutionStatusConsumer`, not persisted as ledger events.
9. Unknown-tool execution can raise via registry lookup before a `tool.call.failed` event is appended when no tool object can be resolved.
10. Python local variables, exception objects beyond string summaries, validation objects, policy evaluation objects, retry packet objects, callable objects, and routing locals are not appended.

## Reconstruction summary

### What Seed attempted

The ledger can reconstruct the major completed runtime attempt chain for normal user-message handling:

`input.user_message` -> `model.decision.proposed` -> one of response event, tool-need event, tool-call events, state-patch domain events, state-patch rejection, or validation/retry events.

Tool execution attempts are especially explicit once an allowed tool call reaches `_execute_allowed_tool_call()`: `tool.call.started` records the attempted tool and arguments, and completion/failure records the outcome.

### What succeeded

Success is durable when success has an event:

- `tool.call.completed` records successful tool completion and output.
- State patch success is durable as the resulting domain events (`entity.upserted`, `evidence.observed`, `fact.observed`, `goal.created`).
- Observation ingestion success is durable as observation/evidence/fact events.
- Answer/question/refusal emission is durable as response events.
- Pending action completion is durable through pending-action status events.

Projection can reconstruct durable domain success for entities, observations, evidence, facts, goals, tool needs, pending actions, action plans, tools, and related legacy side-path objects because `StateProjector.apply()` has branches for those event kinds.

### What failed

Failure is durable when implementation appends failure events:

- Decision parse failure: `model.decision.parse_failed`.
- Decision schema validation failure: `model.decision.invalid`.
- Tool-intent rejection: `model.decision.intent_rejected`.
- Tool execution or validation/status failure after a tool is resolved: `tool.call.failed`.
- Tool policy block/approval requirement: `tool.policy.blocked` / `tool.approval.required`.
- State patch rejection: `state.patch.rejected`.

Projection generally does not expose those failures in `State`; they remain reconstructable from ledger history rather than from projected domain state.

### What remains incomplete

The implementation can reconstruct some incomplete work:

- Open tool needs are projected from `tool_need.created` plus status changes.
- Pending actions are projected from `pending_action.created` plus pending-action status events.
- A `tool.call.started` without a later `tool.call.completed` or `tool.call.failed` with matching causation is ledger evidence of an interrupted or incomplete tool call.
- A `model.decision.proposed` without a routed follow-up event is evidence that routing may have stopped after decision production.

Other incompleteness is not directly durable:

- A composed decision input with no proposed decision is not persisted as its own unit.
- Capability-resolution metadata returned with a tool-need response is not persisted.
- Projection-building progress is not persisted.
- Status/progress emission is not persisted.

## Transient-only execution evidence

The following evidence exists during execution but disappears unless equivalent source evidence is available elsewhere:

- `DecisionInputPacket`: not stored; equivalent ingredients are partly durable through input event and projected state, but exact budget selection depends on code/config and registry state.
- Validation context: only errors and attempts are stored on failure; successful validation has no separate event.
- Retry context: retry prompt is a replacement packet in memory; failure event ids and errors are durable, but the exact next packet is not stored.
- Policy evaluation context: final block/approval policy payload is durable, but state factory output and evaluation internals are transient.
- Tool callable/import state and exception objects: only started/completed/failed summaries are durable.
- Capability recommendation/ranking response: transient unless recomputed; only the created need is durable.
- Projection diagnostics and status/progress counters: transient unless separately printed/recorded by a caller outside the ledger.
- Collection activity objects and normalization locals: not durable; observations/evidence/facts are durable.

## Can projected state justify what happened previously without replaying runtime execution?

Projected state can justify current domain facts without replaying runtime execution when it contains or loads a projection derived from ledger events. The projector records `last_event_id`, materializes observations/evidence/facts/goals/tool needs/pending actions/etc. from event payloads, and finalizes deterministic indexes such as inferred facts, relationships, aliases, graph issues, and conflicts.

However, projected state is not a full runtime transcript. It does not project user messages, model decisions, response events, tool call lifecycle events, decision failures, intent rejections, policy events, or state-patch rejection events. Those remain available in the ledger, not in the projected `State` object.

Therefore: projected state can justify "what is currently known / open / pending" for projected domain objects, but the ledger is required to justify "what happened" for runtime orchestration and failures.

## Interruption analysis

Using only event ledger, projection, and existing observations:

Supported reconstruction cases:

- Interrupted after user input: `input.user_message` exists; no decision event follows.
- Interrupted after decision proposal: `model.decision.proposed` exists; no corresponding response/tool/state/failure event follows.
- Interrupted during allowed tool execution after start: `tool.call.started` exists without completion/failure.
- Interrupted after policy requires approval/confirmation: policy event and `pending_action.created` can project a pending action.
- Interrupted after observation ingestion batch partially persisted: persisted per-observation events remain individually durable; unpersisted collected observations are not reconstructable.
- Interrupted after accepted state patch operation(s): already appended operation events project; later operations not appended are not reconstructable.

Unsupported or only partial reconstruction cases:

- Interrupted during decision input composition before model decision: no `DecisionInputPacket` event exists.
- Interrupted during capability resolution/recommendation after tool need creation: created need is durable; recommendation payload is not.
- Interrupted before tool call start while evaluating policy: no durable event records the in-progress policy evaluation unless it reaches policy-denied event or allowed start.
- Interrupted during projection replay/finalization: event ledger can be replayed again, but projection progress/status is not durable.
- Interrupted while collecting observations before `append_many()`: collected-but-unappended observations disappear.

## Strongest contradictory evidence

The strongest evidence against full reconstruction of Seed's own work is that several important runtime surfaces are deliberately computed and returned without corresponding ledger events or projection branches:

1. `DecisionInputPacket` is central to decision production but is not appended. Exact selected context and budget trace are transient.
2. Many appended runtime events are ignored by projection: user input, model decisions, responses, tool lifecycle, validation failures, policy blocks, and state-patch rejections do not become projected domain state.
3. Capability resolution/recommendation metadata is returned to the caller but not persisted.
4. Successful state patch application lacks a wrapper event tying all operation events into one accepted patch boundary.
5. A few failure paths can escape before a ledger failure event, especially unknown-tool registry lookup before a validated tool exists.
6. Status/progress emission and projection diagnostics are not event-ledger evidence.

## Direct answer: can the current event ledger reconstruct Seed's own completed work?

Yes, for completed runtime work that crosses implemented event boundaries. The ledger preserves a strong append-only transcript of operator input, model decisions and retries/failures, answer/question/refusal responses, tool needs, tool execution starts/completions/failures, policy-denied outcomes, pending actions, state-patch domain mutations/rejections, and observation/evidence/fact ingestion.

No, not as a complete replay of every runtime object or local execution context. The current ledger does not preserve exact decision input packets, successful validation context, recommendation payloads, projection progress, collection pre-persistence state, or every returned response object. Projection also intentionally omits many runtime transcript events.

## What already allows Seed to determine what naturally comes next without separate runtime memory?

Implementation-backed evidence already supports next-step determination for bounded cases:

- Projected open tool needs identify missing capabilities that remain unresolved.
- Projected pending actions identify work awaiting approval/confirmation or completion.
- Projected goals, observations, evidence, facts, inferred facts, conflicts, relationships, and graph issues identify current known state and evidence-backed gaps.
- Ledger-visible incomplete chains identify interrupted attempts, such as started tool calls without completion/failure or decisions without routed follow-up.
- Ledger-visible failures identify retry/repair context at the event level: parse failures, validation failures, intent rejections, tool failures, policy blocks, and state patch rejections.

This is enough to derive many "what happened previously" and "what remains open" answers from the ledger plus projection. It is not enough to reconstruct all transient execution context exactly.

## Recommended bounded implementation slice

Observationally, the smallest bounded implementation slice suggested by the current evidence would be a diagnostic-only audit that reports event-chain completeness for existing ledger events: input-to-decision-to-route chains, tool started-without-terminal-outcome chains, open tool needs, and pending actions. Such a slice would not introduce runtime memory, scheduling, planning, or new orchestration. If implemented, it would be an operational diagnostic surface and therefore would need diagnostic inventory, shape-audit specs, and tests under the repository's operational visibility contract.
