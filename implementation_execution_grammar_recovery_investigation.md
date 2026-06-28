# Implementation execution grammar recovery investigation

## Scope and method

This is a recovery report, not a redesign. It asks what `execution` already means in implementation before tool vocabulary is stabilized. Repository code, tests, CLI surfaces, architecture metadata, and prior investigations were treated as evidence; implementation evidence overrides architectural preference and vocabulary in older reports.

Commands used during this investigation:

```bash
pwd && rg --files -g 'AGENTS.md' -g '! .git' && find .. -name AGENTS.md -print
cat AGENTS.md && rg -n "capability_operation_execution_reconciliation|ToolExecutor|diagnostic-inventory|execution" -S .
sed -n '1,240p' seed_runtime/execution.py && sed -n '1,220p' seed_runtime/runtime.py
sed -n '240,520p' seed_runtime/execution.py; sed -n '220,520p' seed_runtime/runtime.py; sed -n '1,260p' seed_runtime/state.py
rg -n "class StateProjector|def project\(|def append\(|class EventLedger|class ToolRegistry|class DiagnosticInventoryEntry|record_scope|mutates_cluster|class CapabilityCatalog|class ToolNeedService|class ToolRecommendationService|class StatePatchService|def apply\(" seed_runtime scripts tests -S
sed -n '1,140p' seed_runtime/events.py; sed -n '715,840p' seed_runtime/state.py; sed -n '1,120p' seed_runtime/state_patches.py; sed -n '1,130p' seed_runtime/registry.py; sed -n '1,120p' seed_runtime/capability_catalog.py; sed -n '1,100p' seed_runtime/tool_needs.py; sed -n '1,120p' seed_runtime/tool_recommendations.py; sed -n '1,80p' seed_runtime/diagnostic_inventory.py
for f in capability_operation_execution_reconciliation capability_authority_and_execution_boundary_reconciliation execution_concepts_implementation_investigation execution_characterization_inquiry_surface_investigation execution_inquiry_orientation_investigation execution_visibility_investigation execution_timing_adversarial_audit observation_execution_transition_investigation tool_execution_ownership_audit tool_vocabulary_reconciliation natural_language_execution_path_inventory_audit current_implementation_audit_execution_observation_projection_cache_capability; do rg --files docs | rg "$f"; done
```

Primary evidence files reviewed include:

- `seed_runtime/execution.py`
- `seed_runtime/runtime.py`
- `seed_runtime/state.py`
- `seed_runtime/events.py`
- `seed_runtime/state_patches.py`
- `seed_runtime/registry.py`
- `seed_runtime/capability_catalog.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/tool_recommendations.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `scripts/seed_local.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`
- prior investigation documents listed in the prompt

No runtime framework, registry, policy, provider, or tool behavior was changed.

## Executive answer

Implementation already contains an execution grammar, but it is not a single universal `ToolExecutor` grammar.

The strongest implementation-backed grammar is:

```text
append-only events
  -> projection replay / derived indexes
  -> read-only observation, diagnostic, presentation, and inquiry surfaces

runtime decision
  -> answer / question / refusal event termination
  -> request_tool capability-gap recording and read-only resolution
  -> call_tool registered-operation execution through ToolExecutor
  -> propose_state_patch ledger mutation through StatePatchService

capability metadata
  -> registered operation candidates from ToolRegistry
  -> provider / handoff recommendations from CapabilityCatalog
  -> no provider execution inside Seed
```

Therefore, `ToolExecutor` owns one execution family: **registered operation execution**. It does not own projection replay, event ledger writes, read-only diagnostic evaluation, capability-gap creation, provider recommendation, state-patch mutation, presentation rendering, cache reuse, or observation adaptation. Those paths perform work, and some record or mutate Seed state, but they are not ToolExecutor-owned execution.

## Implementation-backed execution paths currently present

| Path | Implementation evidence | Read only | Records events | Mutates projected Seed state | Mutates runtime state | Mutates external systems | Delegates externally | Requires policy / approval | Requires registration | Termination point |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Append-only event recording | `EventLedger.append()` creates an `Event`, stores it, and returns it; `append_many()` validates and stores events in order. | No | Yes | Indirectly, after projection | Yes, ledger storage | No | No | No generic policy | No | Stored event |
| Projection replay / state build | `StateProjector.project()` creates `State`, reads workspace events, calls `project_from_state()`, applies each event, then finalizes derived indexes. | Reads ledger, mutates in-memory projection | No | Yes, in-memory projected state | Yes, local `State` object | No | No | No | No | Projected `State` |
| Projection diagnostics/status | `ProjectionBuildDiagnostics` stores optional timings/counters and projector emits progress when supplied. | Yes with respect to cluster truth | No | No authoritative mutation | Local timing/status only | No | No | No | No | Diagnostics/status metadata |
| Runtime answer/question/refusal | `Runtime._route()` appends `response.answer`, `response.question`, or `response.refusal` and returns `RuntimeResponse`. | No, ledger recording | Yes | Indirectly, if projected | Runtime response | No | No | Decision validation before routing, not tool policy | No | Answer/question/refusal response plus event |
| Capability-gap / request_tool path | `Runtime._route()` calls `ToolNeedService.create_from_decision()`, recommendation ranking, and `resolve_capability()`. | Mixed: creates need, resolves read-only | Yes for need creation | Indirectly via projected need | Yes, need record | No | No actual execution; provider metadata only | No execution policy; decision validation applies | Registered candidates only for operation listing | ToolNeed and capability-resolution payload |
| Registered operation execution | `ToolExecutor.execute()` validates through `ToolExecutionPolicyService`, enforces policy outcomes, appends tool call events, imports the registered implementation, invokes it, validates output, and extracts facts from completed results. | No | Yes | Indirectly via emitted events/fact extraction | Yes, call/pending events | Only if registered implementation does so; core boundary does not imply host mutation | No provider delegation in executor | Yes, policy can allow/block/require confirmation/approval | Yes, `ToolRegistry.require()` / registered `ToolSpec` | Completed/failed/blocked/pending tool result |
| Pending approved registered execution | `resume_approved_tool_call()` projects state, requires pending action status `approved`, executes stored call, and marks completed after success. | No | Yes | Indirectly | Yes | Same as implementation | No | Requires prior approval state | Yes | Tool result and pending completion |
| Declarative state patch mutation | Runtime `propose_state_patch` calls `StatePatchService.apply()`, which translates operations to ledger events such as `entity.upserted`, `evidence.observed`, and `fact.observed`. | No | Yes | Indirectly, after projection | Yes, ledger | No | No | State patch validation, not tool policy | No | `state_updated` response with event IDs |
| Provider recommendation / handoff metadata | `CapabilityCatalog` loads capability recommendations with provider, backend, and operation metadata; `ToolRecommendationService` ranks recommendations without registering or executing providers. | Yes | No by recommendation itself | No | No | No | Recommendation points outside Seed but does not invoke | No Seed policy/approval for execution | No, unless separately represented as registered operation candidate | Recommendation payload |
| Diagnostic / audit surfaces | `DiagnosticInventoryEntry` declares `supports_record`, `record_scope`, `writes_event_ledger`, and `mutates_cluster`; tests assert recording scopes and non-mutation. | Usually yes; recording entries write diagnostic facts | Sometimes | Diagnostic scope only when recorded | Surface-local/report or diagnostic ledger writes | No, inventory says no cluster mutation | No | No | Inventory registration, not operation registry | Report JSON/text, diagnostic facts, or audit rows |
| Presentation / inquiry surfaces | Question inventory, reasoning/selection paths, projection shape, operational graph, and similar surfaces consume projected/repo state and render bounded reports. | Yes by declared boundary in inventory/tests | Usually no | No | Local report only | No | No | No | Diagnostic inventory row, not operation registry | Rendered answer/report |
| Cache / read-model work | Prior audit found projection cache and dependent read-model snapshots reuse derived state keyed by event/projection identity; current implementation exposes projection/cache status and cache-debug surfaces. | Reads/writes local cache, not cluster truth | No event recording as cache authority | Reuses derived projections/read models | Yes, cache storage | No | No | No | No | Cache hit/miss status, snapshot, read model |
| Observation ingestion / adaptation | Prior audit found observation ingestion converts `Observation` objects into observation, evidence, and optional fact events, while observation sources adapt external/repo information into observations without owning ledger/projection internals. | Sources can be read-only; ingestion records | Yes during ingestion | Indirectly via events | Yes, ledger | Observation sources may read external or filesystem information, but reviewed boundaries avoid mutation | Not execution delegation | No tool policy | No operation registration | Observation/evidence/fact events |

## Recurring execution families recovered

### 1. Registered operation execution — supported

Supported. This family is explicitly named by `ToolExecutor.__seed_arch__` as `registered_tool_execution`, requires `ToolRegistry`, validates through the tool execution policy service, records `tool.call.*` events, and invokes only the registered implementation reference. It also owns pending-action resumption after approval.

Boundary: this is the only family where `ToolExecutor` participates. It is downstream of a `call_tool` decision, registry membership, schema/status validation, and policy outcome.

### 2. Projection execution — supported as implementation work, not ToolExecutor execution

Supported if named carefully as projection replay/build work. `StateProjector` reads events, mutates an in-memory `State`, applies event-specific transformations, and rebuilds derived indexes. It can emit transient progress and diagnostics. It does not require registry registration, tool policy, approval, or provider delegation.

Boundary: projection mutates projected state, not event history or external systems. Event history remains authority.

### 3. Observation execution — partially supported, better phrased as observation adaptation/ingestion

Partially supported. Prior implementation audit distinguishes observation sources from observation ingestion: sources collect/adapt information into `Observation` objects; ingestion records observation/evidence/fact events. This is recurring implementation work and may be operationally described as observation execution, but code evidence is stronger for `observation source` and `ingestion` than for a first-class `ObservationExecutor`.

Boundary: observation ingestion can write the ledger; observation sources should not be collapsed into ToolExecutor or mutation authority.

### 4. Diagnostic execution — supported as diagnostic/audit surface execution, with inventory guardrails

Supported. Diagnostic and audit surfaces are invoked by CLI flags, have inventory rows, can be read-only or record diagnostic facts, and are shape-audited for fields including `record_scope`, `writes_event_ledger`, and `mutates_cluster`. The family is not ToolExecutor-owned and not registry-operation execution.

Boundary: recordable diagnostics should use `record_scope=diagnostic_run` and keep `mutates_cluster=false` unless intentionally different.

### 5. Provider execution — supported only as external boundary, not Seed-owned execution

Accepted only with a strict boundary. `CapabilityCatalog` can name provider/handoff recommendations, backend types, and operation metadata; `ToolRecommendationService` ranks these against projected state. Implementation evidence does not show Seed invoking those providers as execution. The architectural documents repeatedly preserve provider execution outside Seed.

Boundary: provider recommendation is not approval, registration, credential availability, or execution.

### 6. Mutation execution — supported for Seed-internal ledger/state mutation, not necessarily external mutation

Supported in two separate senses:

- registered operation execution may produce events and, through implementations, can potentially perform side effects only if a registered implementation does so after validation/policy;
- declarative state patches mutate Seed's event ledger directly through `StatePatchService`, bypassing ToolExecutor and ToolRegistry.

Boundary: state-patch mutation is not provider execution and not tool execution. It is ledger mutation that later changes projected state.

### 7. Internal execution — supported as an umbrella, but too broad to be a stable class

The repository contains internal work loops: event append, projection replay, cache lookup/rebuild, diagnostics, rendering, policy evaluation, recommendation ranking, and state patch application. Calling all of this `internal execution` is descriptively true but too compressed to be a useful class unless narrowed by responsibility.

### 8. Presentation execution — supported as rendering/report generation, not knowledge mutation

Supported as work performed by CLI/read-model surfaces. Presentation surfaces render reports, answers, paths, graphs, or summaries. The AGENTS guidance is consistent with implementation: presentation vocabulary is not automatically knowledge and should not be promoted without implementation evidence.

## Does ToolExecutor participate in all execution?

No.

`ToolExecutor` participates in registered operation execution only. It is reached from canonical `Runtime` through the `call_tool` decision branch. The same `Runtime._route()` method has branches that terminate as response events, capability-gap creation/resolution, state-patch application, or refusal without entering `ToolExecutor`.

Counterexamples that bypass `ToolExecutor`:

- `answer`, `ask_question`, and `refuse` append response events and return responses.
- `request_tool` records a `ToolNeed`, ranks provider recommendations, and resolves registered operation candidates without executing anything.
- `propose_state_patch` applies declarative ledger events through `StatePatchService`.
- `StateProjector.project()` performs event replay and derived-index finalization.
- diagnostic and audit CLI surfaces render or record diagnostic outputs based on their own inventory contracts.
- provider recommendations are metadata, not executor calls.

Therefore, any claim that `ToolExecutor owns execution` is only safe if the noun phrase is expanded to **registered operation execution**.

## Does implementation consistently follow capability -> operation -> execution?

No as a universal path; yes as one registered-operation path.

Supported path:

```text
request_tool decision
  -> ToolNeed capability
  -> ToolRegistry registered operation candidates
  -> call_tool decision naming a registered ToolSpec
  -> ToolExecutor registered operation execution
```

But multiple implementation paths do not follow that progression:

- projection begins from event history and terminates in projected `State`, not capability;
- answer/question/refusal runtime branches terminate in response events and `RuntimeResponse` objects;
- state patches translate declarative operations directly to ledger events;
- diagnostics execute from CLI flags and inventory rows, not capability resolution;
- provider recommendations can be returned for a capability without becoming registered operations or execution;
- cache/read-model paths begin from projection identity and stored snapshots, not operations;
- observation ingestion begins from observations and emits events, not `ToolSpec` registrations.

The progression is therefore a **specific registered-operation grammar**, not the grammar of all work performed by Seed.

## Where execution terminates

Implementation-backed termination points include:

- **projected state:** projection replay and finalization return `State`.
- **answer / question / refusal:** runtime response branches append response events and return `RuntimeResponse`.
- **recorded event:** ledger append, observation ingestion, tool calls, pending actions, state patches, and diagnostic recording terminate in stored events.
- **registered operation result:** ToolExecutor returns `ToolCallResult` with completed, failed, blocked, confirmation, or approval-required status.
- **pending action:** policy outcomes that require confirmation/approval terminate in `pending_action.created` until later approval/resume.
- **provider recommendation:** capability resolution terminates in ranked recommendation metadata, not provider invocation.
- **mutation:** state patch application terminates in appended domain events that later affect projection.
- **diagnostic/report output:** diagnostic, audit, presentation, and inquiry surfaces terminate in JSON/text reports and sometimes diagnostic-scoped facts.
- **cache/read model:** cache work terminates in snapshot reuse/save status, derived read model, or rendered cache-debug metadata.
- **operator feedback:** execution status/progress surfaces terminate in transient status messages and reports rather than durable cluster truth.

## Execution vocabulary compression

The implementation uses many verbs and nouns for work:

- `execute`: `ToolExecutor.execute()`, `resume_approved_tool_call()`, execution policy, execution status.
- `run`: CLI and tests run diagnostics/audits; historical RuntimeLoop language remains quarantined in docs.
- `apply`: `StatePatchService.apply()` and `StateProjector.apply()` both perform state-changing work in different domains.
- `project`: state projection replays events and rebuilds derived indexes.
- `observe` / `ingest`: observation and evidence paths record findings without becoming tool calls.
- `recommend` / `resolve`: capability path returns metadata and candidates without execution.
- `append` / `record`: event ledger and diagnostic recording write durable history.
- `render` / `format`: presentation surfaces produce operator-facing output.
- `invoke` / `call_tool`: model/runtime vocabulary for registered operation attempts.

Compression is real. The same word `tool` currently covers at least:

- missing capability request (`request_tool`, `ToolNeed`);
- registered operation spec (`ToolSpec`);
- model-visible callable (`ToolRegistry.list_tools()`);
- registered implementation invocation (`ToolExecutor`);
- events (`tool.call.*`);
- non-executable provider capability recommendations that may include an `operation` field.

The same word `execution` also covers or shadows registered operation execution, projection replay work, CLI diagnostic runs, cache/rebuild timing, observation ingestion, state patch mutation, external provider ownership, and operator-visible progress/status. Implementation supports separating these by owner and termination point.

## Counterexamples recovered

Implementation where work is performed but `execution` is not the owner:

- `EventLedger.append()` records events but is event history, not ToolExecutor execution.
- `StateProjector.project()` and `project_from_state()` rebuild state but are projection, not operation execution.
- `ToolNeedService.resolve_capability()` returns registered operations and provider recommendations but explicitly does not execute tools, authorize actions, create pending actions, or mutate registry/catalog state.
- `ToolRecommendationService.recommend_for()` ranks recommendations without creating providers, registering tools, or mutating state.
- `StatePatchService.apply()` appends domain events from declarative patches without ToolRegistry or ToolExecutor.
- diagnostic inventory rows define read-only, recording, and mutation boundaries without operation registration.

Places where ToolExecutor could be incorrectly assumed to own execution:

- docs that say `ToolExecutor owns execution` are accurate only when read as registered-operation execution.
- `Runtime` has a `call_tool` branch into ToolExecutor, but also routes other valid decisions elsewhere.
- capability recommendations may contain provider `operation` strings, but those strings are not registered executable `ToolSpec` implementations.
- projection/cache/debug surfaces may use execution-status vocabulary for progress, but this does not make them tool execution.

Paths bypassing registered operations entirely:

- projection replay;
- event ledger append/append_many;
- state patch application;
- response event emission;
- capability-gap recording and provider recommendation;
- diagnostics/audits and presentation reports;
- cache/read-model construction;
- observation ingestion/adaptation.

## Supported conclusions

1. **Execution paths already exist beyond ToolExecutor.** The code performs projection, event recording, diagnostics, state patch mutation, capability resolution, recommendation ranking, observation ingestion, cache/read-model work, presentation rendering, and registered operation execution.
2. **ToolExecutor owns only registered operation execution.** It requires registered specs, validation, policy, event recording, implementation import/invocation, output validation, and fact extraction.
3. **Capability, operation, and execution are distinct in implementation.** Capabilities can resolve to provider recommendations or registered operation candidates; only a later `call_tool` path invokes ToolExecutor.
4. **Provider is external boundary metadata in current implementation.** Seed recommends/ranks providers but does not become the provider executor.
5. **Mutation is not one thing.** Ledger writes, projected-state mutation, diagnostic-scoped recording, pending-action status changes, and potential registered implementation side effects have different owners and boundaries.
6. **Observation and projection are not presentation only.** They perform implementation work and can terminate in events or projected state, but they do not require ToolExecutor.
7. **Execution vocabulary is compressed.** `tool`, `execute`, `run`, `apply`, `project`, `observe`, `recommend`, `record`, and `render` currently overlap in operator-facing and code vocabulary.
8. **The grammar is stable enough to begin reconciling tool vocabulary if reconciliation preserves owner-specific boundaries.** The safe starting point is not `tool`; it is owner + input + boundary + termination point.

## Unsupported conclusions

- Unsupported: Seed has one universal execution framework.
- Unsupported: all execution should flow capability -> operation -> execution.
- Unsupported: provider recommendation is execution, approval, credential availability, or registration.
- Unsupported: projection/cache/presentation vocabulary should become preserved knowledge without reachability evidence.
- Unsupported: diagnostic recording mutates cluster truth by default.
- Unsupported: `ToolExecutor` should be generalized to own projection, diagnostics, state patches, provider delegation, or observation ingestion.
- Unsupported: `operation` strings in provider metadata are equivalent to registered operations.
- Unsupported: read-only observation or diagnostic surfaces require policy approval unless their specific implementation says so.

## Recommended next investigation

Investigate tool vocabulary only after preserving the execution grammar recovered here. The next investigation should map current `tool` vocabulary by responsibility:

```text
ToolNeed        -> capability gap / requested ability
ToolSpec        -> registered operation contract
ToolRegistry    -> registered operation catalog
ToolExecutor    -> registered operation executor
CapabilityCatalog recommendation -> provider/handoff metadata
call_tool       -> registered operation invocation request
request_tool    -> capability-gap request, not execution
```

The investigation should explicitly test whether proposed vocabulary preserves these boundaries:

- capability metadata versus registered operation contract;
- provider recommendation versus provider execution;
- diagnostic recording versus cluster mutation;
- projection replay versus runtime operation execution;
- state patch ledger mutation versus registered implementation execution;
- presentation labels versus knowledge facts.

Do not implement a new execution framework, registry, provider adapter, or tool runtime as part of that vocabulary reconciliation.
