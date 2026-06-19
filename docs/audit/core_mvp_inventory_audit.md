# Core MVP Inventory Audit

## Executive Summary

After the RuntimeLoop and planning/execution quarantines, the current Seed core is **not** an internal workflow executor. The active architecture is:

```text
Raw input / observations
  -> Evidence
  -> Facts
  -> Relationships
  -> Entity types
  -> Projected State
  -> Explanation / why queries
  -> ToolNeed
  -> capability_resolution
      -> registered_operations
      -> provider_recommendations
      -> handoff_candidates
```

The canonical live user-message runtime is `Runtime`: it appends the user input event, projects state, composes model context, validates a model decision through `DecisionValidator`, applies the deterministic tool-intent guard, and routes only the supported canonical decision branches.

For `request_tool`, canonical Runtime records/deduplicates a `ToolNeed`, ranks provider recommendations, and returns read-only `capability_resolution` metadata. It does **not** create an `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, `ExecutionAuthorization`, workflow, job, retry system, secret flow, or provider execution.

For registered callable operations, `ToolExecutor` is still the canonical registered-operation executor, but it is **not** part of provider/handoff recommendation execution. It executes only registered `ToolSpec` implementations through `ToolRegistry`, after validation and policy preflight.

The knowledge path is anchored in append-only events and projection: observations become evidence/facts, facts are projected into relationships, entity types, conflicts, graph issues, and read-only views.

---

## Core MVP Graph

### Canonical user-message/runtime path

```text
LocalSeedApp.run
  -> Runtime.handle_user_message
      -> EventLedger.append(input.user_message)
      -> StateProjector.project
      -> ContextComposer.compose
      -> model.decide(ContextPacket)
      -> DecisionValidator.validate
          -> ToolValidationService.validate_tool_input for call_tool
      -> ToolIntentGuard.validate for call_tool
      -> Runtime._route
          -> answer/refuse/ask_question response events
          -> request_tool
              -> ToolNeedService.create_from_decision
              -> ToolRecommendationService.recommend_for
                  -> CapabilityCatalog
                  -> RecommendationRanker
              -> ToolNeedService.resolve_capability
                  -> ToolRegistry.list_tools_for_capability
                  -> CapabilityCatalog recommendations
          -> call_tool
              -> ToolExecutor.execute
          -> propose_state_patch
              -> StatePatchService.apply
```

### Registered operation execution path

```text
ToolExecutor.execute
  -> ToolExecutionPolicyService.evaluate_with_state_factory
      -> ToolValidationService.validate_tool_exists
      -> ToolValidationService.validate_tool_status
      -> ToolValidationService.validate_input_schema
      -> PolicyGate.evaluate
  -> if non-allow:
      -> tool.policy.blocked OR tool.approval.required
      -> PendingActionService.create_tool_call for confirmation/approval
  -> if allow:
      -> ToolRegistry confirms registered implementation
      -> import implementation function
      -> call function with ToolContext
      -> ToolValidationService.validate_output_schema
      -> EventLedger tool.call.completed / failed
      -> FactExtractionService.observe_tool_result
```

The policy service explicitly does not execute tools, append events, create pending actions, or collapse non-allow outcomes; the caller owns routing.

### Knowledge/read-only query path

```text
InputInspector / ObservationSource
  -> ObservationCollectionService
      -> ObservationNormalizationPipeline
      -> ObservationIngestor
          -> observation.observed
          -> evidence.observed
          -> fact.observed / fact.inferred
  -> EventLedger
  -> StateProjector
      -> PredicateCatalog
      -> RelationshipCatalog
      -> EntityTypeCatalog
      -> InferenceCatalog
      -> FactSupport / FactConflict / graph issues
  -> ProjectionStore / project_state_with_cache
  -> CLI read-only queries
      -> --state-build
      -> --impact
      -> --why
      -> --relationships
      -> --graph-issues
      -> --entity-types
      -> --current-facts
      -> --unhealthy / --down
```

---

## Inventory Table

Legend:

- **Runtime?** = reachable from canonical `Runtime.handle_user_message` / `Runtime._route`.
- **Executor?** = reachable from `ToolExecutor.execute` / `resume_approved_tool_call`.
- **CLI RO?** = reachable from read-only CLI state/query path.
- **Capability?** = required for `ToolNeed -> capability_resolution`.
- **Knowledge?** = required for observation/knowledge projection.

| Name | File/module | What it owns | Who creates it | Who consumes it | Runtime? | Executor? | CLI RO? | Capability? | Knowledge? | Classification | Notes / concerns |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| `Runtime` | `seed_runtime/runtime.py` | Canonical user-message routing, event append, decision validation loop, request-tool/call-tool routing. | `build_local_app` | CLI/API/local app | Yes | Indirect | No | Yes | Indirect | **Core MVP** | Single active runtime path. |
| `RuntimeResponse` | `seed_runtime/models.py` | Canonical response envelope. | `Runtime._route` | CLI/API | Yes | Indirect | No | Yes | No | **Core MVP** | Duplicates `RuntimeResult` naming from quarantined RuntimeLoop. |
| `Decision` | `seed_runtime/models.py` | Canonical model decision shape. | Model adapter / tests | `DecisionValidator`, `Runtime._route` | Yes | Indirect | No | Yes | No | **Core MVP** | Contains legacy fields `action_plan`/`handoff_plan`, but validator rejects unsupported decision kinds. |
| `DecisionValidator` | `seed_runtime/decisions.py` | Validates canonical model decisions and tool-call inputs. | Runtime wiring | `Runtime.handle_user_message` | Yes | Indirect | No | Yes | No | **Core MVP** | No branches for `propose_action_plan` or `propose_handoff_plan`; those fall to unsupported. |
| `ToolIntentGuard` | `seed_runtime/tool_intent.py` | Deterministic intent guard for tool calls. | `Runtime.__init__` | `Runtime.handle_user_message` | Yes | No | No | No | No | **Supporting infrastructure** | Guardrail against schema-valid but intent-mismatched tool calls. |
| `ContextComposer` / `ContextPacket` | `seed_runtime/context.py` | Runtime decision context, visible tools, facts/evidence budget. | Runtime wiring | Runtime model | Yes | No | No | Indirect | Indirect | **Supporting infrastructure** | Its decision schema lists current canonical kinds only: answer, ask_question, call_tool, request_tool, refuse. |
| `EventLedger` | `seed_runtime/events.py` | Append-only events and workspace-scoped listing. | Runtime/CLI/tests | Runtime, projector, executor, ingestors | Yes | Yes | Yes | Yes | Yes | **Supporting infrastructure** | Also validates historical `execution_authorization.granted` events for compatibility. |
| `SQLiteEventLedger` | `seed_runtime/events.py` | SQLite-backed ledger compatibility/local persistence. | CLI with `--db` | CLI/runtime/projection | Yes if `--db` | Yes if `--db` | Yes | Yes | Yes | **Supporting infrastructure / historical compatibility** | Retains ID prefixes for old payload IDs including `plan`, `handoff`, `auth`. |
| `ToolNeed` | `seed_runtime/models.py` | Missing capability request. | `ToolNeedService` | Runtime, projection, capability resolution | Yes | No | Yes, projected | Yes | Indirect | **Core MVP** | Correct endpoint of planning/capability path. |
| `ToolNeedService` | `seed_runtime/tool_needs.py` | ToolNeed create/dedupe/status and read-only capability resolution. | Runtime wiring | Runtime | Yes | No | Indirect | Yes | No | **Core MVP** | Explicitly says it does not execute, authorize, create pending actions, or mutate registry/catalog state. |
| `CapabilityCatalog` | `seed_runtime/capability_catalog.py` | Read-only capability-to-provider metadata. | Runtime/ToolRecommendationService | ToolRecommendationService, ToolNeedService | Yes | No | Indirect | Yes | No | **Core MVP** | Recommendations are metadata, not registered operations. |
| `CapabilityRecommendation` | `seed_runtime/capability_catalog.py` | Provider/handoff metadata fields including `backend_type`/`operation`. | Catalog loading | Recommendation/ranking/capability resolution | Yes | No | Indirect | Yes | No | **Core MVP** | Naming concern: `operation` here means provider/handoff metadata, not `ToolRegistry` operation. |
| `ToolRecommendationService` | `seed_runtime/tool_recommendations.py` | Read-only lookup + rank of catalog recommendations. | Runtime | Runtime request_tool route | Yes | No | No | Yes | No | **Core MVP** | Explicitly non-mutating/non-registering. |
| `RecommendationRanker` / `RankedRecommendation` | `seed_runtime/recommendation_ranker.py` | Read-only ranking based on projected state and environment facts. | ToolRecommendationService | ToolRecommendationService | Yes | No | No | Yes | No | **Core MVP** | Ranking only; no provider execution/installation. |
| `ToolRegistry` | `seed_runtime/registry.py` | Registered callable operation inventory/toolkit manifests. | Runtime app builder / tests | ContextComposer, ToolExecutor, ToolNeedService | Yes | Yes | Indirect through projected `tool.registered` | Yes | Indirect | **Core MVP / supporting infrastructure** | `list_tools_for_capability` is the registered-operation side of capability resolution. |
| `ToolSpec` | `seed_runtime/models.py` | Registered operation contract: schemas, implementation, policy action, visibility, capabilities. | Manifest loader / projection | Registry, validation, executor, capability resolution | Yes | Yes | Yes, projected | Yes | Indirect | **Core MVP / supporting infrastructure** | `capabilities` is the operation-to-capability link. |
| `Toolkit` | `seed_runtime/models.py` | Collection of `ToolSpec`s. | Manifest loader | Registry/API | Yes | Yes | No | Yes | No | **Supporting infrastructure** | Contract packaging for registered operation inventory. |
| `ToolExecutor` | `seed_runtime/execution.py` | Registered-operation execution, policy outcome routing, pending-action creation/resume, events, output validation. | Runtime app builder | Runtime `call_tool`; external callers may resume | Yes | Yes | No | No | Indirect via tool result extraction | **Supporting infrastructure** | Canonical executor for registered tools only; not provider/handoff execution. |
| `ToolContext` | `seed_runtime/execution.py` | Execution context passed to registered operation function. | ToolExecutor | Registered implementation function | Via call_tool | Yes | No | No | No | **Supporting infrastructure** | Should stay narrowly scoped to registered operations. |
| `ToolValidationService` | `seed_runtime/tool_validation.py` | Tool existence/status/input/output schema validation. | DecisionValidator, ToolExecutor, policy service | Runtime/executor | Yes | Yes | No | Indirect | No | **Supporting infrastructure** | Correctly validates registered operation contracts, not provider recommendations. |
| `ToolExecutionPolicyService` | `seed_runtime/tool_execution_policy.py` | Validation-before-policy preflight and raw policy result. | ToolExecutor | ToolExecutor | Via call_tool | Yes | No | No | No | **Supporting infrastructure** | Explicitly non-executing/non-eventing; good boundary. |
| `PolicyGate` / `PolicyDecision` | `seed_runtime/policy.py`, `seed_runtime/models.py` | Operation policy outcome metadata. | ToolExecutionPolicyService | ToolExecutor | Via call_tool | Yes | No | No | No | **Supporting infrastructure** | Naming concern: policy “approval” creates pending action, not `ExecutionAuthorization`. |
| `PendingAction` | `seed_runtime/models.py` | Pending registered tool call awaiting confirmation/approval. | PendingActionService | StateProjector, ToolExecutor resume | Via call_tool policy outcome | Yes | Yes, projected | No | No | **Supporting infrastructure** | Must remain distinct from `ExecutionAuthorization`. |
| `PendingActionService` | `seed_runtime/pending_actions.py` | Pending-action lifecycle events. | ToolExecutor | ToolExecutor, projection | Via call_tool | Yes | Yes, projected | No | No | **Supporting infrastructure** | Correctly scoped to registered tool calls only. |
| `FactExtractionService` | `seed_runtime/fact_extraction.py` | Derives observations/facts from tool results and compatibility event names. | ToolExecutor/RuntimeLoop | State projection via events | Via ToolExecutor | Yes | Indirect | No | Yes | **Supporting infrastructure / historical compatibility** | Mentions RuntimeLoop `tool.result` vs canonical `tool.call.completed`; keep until old traces are retired. |
| `StatePatchService` | `seed_runtime/state_patches.py` | Declarative state-patch operations to ledger events. | Runtime | Runtime `propose_state_patch` | Yes | No | Projected | No | Yes | **Supporting infrastructure / concern** | This is host-safe event mutation, but is still a Runtime route; not part of stated Core MVP path unless intentionally retained. |
| `StateProjector` | `seed_runtime/state.py` | Rebuilds inspectable state from events and derives aliases, facts, relationships, entity types, graph issues, conflicts. | Runtime/CLI/ToolExecutor | Runtime, CLI, executor, services | Yes | Yes | Yes | Yes | Yes | **Core MVP** | Projection also retains legacy plan/proposal event support. |
| `ProjectionStore` | `seed_runtime/projection_store.py` | Snapshot store protocol for projected-state cache. | CLI/RuntimeLoop historical | `project_state_with_cache` | No direct Runtime | No | Yes | No | Yes | **Supporting infrastructure** | Cache plumbing for read-only query performance. |
| `SQLiteProjectionStore` | `seed_runtime/projection_store.py` | SQLite projection snapshot persistence. | CLI `--db` | CLI projected state | No direct Runtime | No | Yes | No | Yes | **Supporting infrastructure** | Local CLI state cache. |
| `project_state_with_cache` | `seed_runtime/projection_store.py` | Load/save projected state snapshots by last event id. | CLI state query helpers | CLI read-only paths | No direct Runtime | No | Yes | No | Yes | **Supporting infrastructure** | Canonical read-only state cache path. |
| `InputInspector` / `InputArtifact` | `seed_runtime/input_inspector.py` | Bounded safe file classification and hashing. | CLI/tests | Ingestion prep | No | No | No | No | Yes | **Core MVP** | Safely inspects without executing content. |
| `ObservationSource` | `seed_runtime/observation_sources.py` | Adapter protocol for external observation providers. | Source adapters | ObservationCollectionService | No | No | No | No | Yes | **Core MVP** | Sources are ledger/projector unaware. |
| `LocalHostObservationSource` | `seed_runtime/observation_sources.py` | Read-only local host observations via stdlib. | CLI ingestion args | ObservationCollectionService | No | No | No | No | Yes | **Core MVP** | Explicitly avoids shell/subprocesses. |
| `ObservationCollectionService` | `seed_runtime/observation_sources.py` | Collects, normalizes, and ingests observations atomically. | CLI ingestion helpers | ObservationIngestor | No | No | No | No | Yes | **Core MVP** | Projects current state before normalizing to support alias/identity derivation. |
| `Observation` | `seed_runtime/observations.py` | Canonical external observation model. | Sources/CLI | Normalizers/ingestor/projector | No | No | Yes, projected | No | Yes | **Core MVP** | Rejects secret fields. |
| `ObservationNormalizer` / `ObservationNormalizationPipeline` | `seed_runtime/observation_normalizers.py` | Derive normalized observations without mutating originals. | ObservationCollectionService | Ingestion | No | No | No | No | Yes | **Core MVP** | Default order: endpoint alias, endpoint identity, predicate normalization. |
| `ObservationIngestor` | `seed_runtime/observations.py` | Appends observation, evidence, and fact events. | CLI/source collection | EventLedger/StateProjector | No | No | Indirect | No | Yes | **Core MVP** | Primary observation-to-knowledge event writer. |
| `Evidence` | `seed_runtime/evidence.py` | Source payload/provenance for facts. | ObservationIngestor/state patch | StateProjector/explanations | Via state patch | No | Yes | No | Yes | **Core MVP** | Required for why/provenance. |
| `Fact`, `FactSupport`, `FactConflict` | `seed_runtime/facts.py` | Knowledge claims, projected support, active conflicts. | ObservationIngestor/projector | StateProjector/explanations/CLI | Via state patch/projected context | No | Yes | Indirect | Yes | **Core MVP** | Core knowledge substrate. |
| `PredicateCatalog` | `seed_runtime/predicate_catalog.py` | Canonical predicate vocabulary and provider mappings. | StateProjector/normalizers/CLI | Projection/query | Yes via projector | No | Yes | No | Yes | **Core MVP** | Defines what Seed can know; separate from capabilities. |
| `RelationshipCatalog` | `seed_runtime/relationship_catalog.py` | Relationship vocabulary derived from facts. | StateProjector | Projection/graph queries | Yes via projector | No | Yes | No | Yes | **Core MVP** | Relationship semantics are read-only projection. |
| `EntityTypeCatalog` | `seed_runtime/entity_type_catalog.py` | Entity type vocabulary. | StateProjector | Projection/graph validation | Yes via projector | No | Yes | No | Yes | **Core MVP** | Required for graph issue classification. |
| `InferenceCatalog` | `seed_runtime/inference_catalog.py` | Deterministic local fact projection rules. | StateProjector/CLI | Projection/explanations | Yes via projector | No | Yes | No | Yes | **Core MVP** | Local deterministic reasoning, not orchestration. |
| `GraphValidator` / graph issue models | `seed_runtime/state.py` | Type/topology validation findings. | StateProjector | CLI `--graph-issues`, `--state-build`, `--unhealthy` | Yes via projector | No | Yes | No | Yes | **Core MVP** | Read-only diagnostics. |
| `ExplanationBuilder` | `seed_runtime/explanations.py` | Why/belief explanations from projected state. | CLI | CLI `--why` | No direct Runtime | No | Yes | No | Yes | **Core MVP** | Read-only explanation path. |
| State View builders | `seed_runtime/state_views.py` | Read-only projected state views. | CLI | `--state-build`, current views | No direct Runtime | No | Yes | No | Yes | **Core MVP** | Views are projection surfaces, not persistence. |
| `RuntimeTrace` / `RuntimeTraceReader` | `seed_runtime/runtime_trace.py` | Read-only RuntimeLoop trace reconstruction. | CLI trace paths | `--trace-run`, `--why-run` | No | No | Yes, historical | No | No | **Historical compatibility** | Explicitly for historical RuntimeLoop runs. |
| `DecisionJournal` | `seed_runtime/decision_journal.py` | RuntimeLoop decision audit event records. | RuntimeLoop | RuntimeTrace | No canonical Runtime | No | Historical trace only | No | No | **Historical compatibility** | Runtime is canonical; RuntimeLoop traces may read records. |
| `RuntimeLoop` | `seed_runtime/runtime_loop.py` | Deprecated deterministic orchestration prototype. | Experimental tests only | RuntimeLoop tests/trace compatibility | No | No | Historical trace only | No | No | **Experimental/quarantined** | Must not be wired into CLI/API/default/canonical tests per module doc. |
| `RuntimeInput` / `RuntimeResult` / loop `Decision` / `RuntimeContext` | `seed_runtime/runtime_loop.py` | RuntimeLoop-specific request/result/context/decision models. | RuntimeLoop tests | RuntimeLoop | No | No | No | No | No | **Experimental/quarantined** | Naming collision with canonical Runtime response/result concepts. |
| `RuntimeTool` / `EchoTool` | `seed_runtime/runtime_loop.py` | RuntimeLoop in-memory handler protocol/test tool. | Tests | RuntimeLoop | No | No canonical executor | No | No | No | **Experimental/quarantined** | Duplicate execution concept vs registered `ToolSpec`/`ToolExecutor`. |
| `RuntimeLoopDecisionValidator` | `seed_runtime/runtime_loop_decisions.py` | RuntimeLoop-only decision validation. | RuntimeLoop | RuntimeLoop | No | No | No | No | No | **Experimental/quarantined** | Duplicate decision validator. |
| `RuntimeLoopToolRequestHandler` | `seed_runtime/runtime_loop_tool_requests.py` | RuntimeLoop request_tool branch. | RuntimeLoop | RuntimeLoop | No | No | No | No | No | **Experimental/quarantined** | Duplicate ToolNeed/recommendation path. |
| `ActionPlan` | `seed_runtime/models.py` | Text-only legacy plan model. | ActionPlanService / legacy CLI | Projection/legacy CLI/tests | No | No | Historical projection | No | No | **Experimental/quarantined + historical compatibility** | Non-executable by model contract. |
| `ActionPlanService` | `seed_runtime/action_plans.py` | Legacy text-only plan creation/lifecycle/authorization helper. | CLI `--plan` and lifecycle flags/tests | Legacy CLI/tests | No | No | Legacy side path | No | No | **Experimental/quarantined** | Explicitly read-only/non-executing. |
| `HandoffPlan` | `seed_runtime/models.py` | Non-executable external-provider handoff boundary. | HandoffPlanService/legacy CLI | Projection/legacy CLI/tests | No | No | Historical projection | No | No | **Experimental/quarantined + historical compatibility** | Constructor rejects execution/approval/trust/registration claims. |
| `HandoffPlanService` | `seed_runtime/handoff_plans.py` | Legacy handoff creation from accepted action plans. | CLI `--handoff`/tests | Legacy CLI/tests | No | No | Legacy side path | No | No | **Experimental/quarantined** | Does not execute provider or authorize execution. |
| `ExecutionProposal` | `seed_runtime/execution_proposals.py` | Experimental concrete-call proposal shape. | ExecutionProposalService/legacy CLI | Projection/legacy CLI/tests | No | No | Historical projection | No | No | **Experimental/quarantined + historical compatibility** | Not executable by itself; delete candidate after compatibility review. |
| `ExecutionProposalService` | `seed_runtime/execution_proposals.py` | Experimental proposal generation. | CLI `--proposal`/tests | Legacy CLI/tests | No | No | Legacy side path | No | No | **Experimental/quarantined** | Never invokes tools or grants authorization. |
| `ExecutionAuthorization` | `seed_runtime/models.py` | Experimental non-core authorization metadata. | ActionPlanService legacy grant helper | Projection/precondition checks | No | No | Historical projection | No | No | **Experimental/quarantined + historical compatibility** | Not pending-action approval; secret-free metadata only. |
| `PreconditionEvaluator` / helpers | `seed_runtime/preconditions.py` | Legacy action-plan precondition reports. | ActionPlanService/ExecutionProposalService/CLI | Legacy CLI/tests | No | No | Legacy side path | No | No | **Experimental/quarantined** | “Executable” wording is risky; inspect-only in code docs. |
| CLI `--plan` | `scripts/seed_local.py` | Legacy post-runtime output side path. | CLI only | ActionPlanService | No, wraps after Runtime result | No | No | No | No | **Experimental/quarantined** | Not Runtime routing, but still creates plan output/events when requested. |
| CLI `--preconditions` | `scripts/seed_local.py` | Legacy inspect-only plan report. | CLI only | Precondition helpers | No | No | Legacy side path | No | No | **Experimental/quarantined** | Requires explicit side path. |
| CLI `--proposal` | `scripts/seed_local.py` | Legacy inspect-only execution proposal. | CLI only | ExecutionProposalService | No | No | Legacy side path | No | No | **Experimental/quarantined** | Wording still includes “execution proposal”; quarantined in help. |
| CLI `--handoff` | `scripts/seed_local.py` | Legacy non-executable handoff plan. | CLI only | HandoffPlanService | No | No | Legacy side path | No | No | **Experimental/quarantined** | Not Core MVP routing. |
| CLI `--authorize-proposal` | `scripts/seed_local.py` | Legacy execution authorization metadata grant. | CLI only | ActionPlanService | No | No | Legacy side path | No | No | **Experimental/quarantined** | Biggest terminology risk. |
| `ToolkitCandidate` | `seed_runtime/models.py` | Builder/generated toolkit candidate metadata. | Builder/tests | Builder compatibility | No | No | No | Indirect/future | No | **Supporting infrastructure / possible delete candidate later** | Needs separate builder audit before removal. |

---

## Runtime-Reachable Models

Canonical Runtime reaches these active models/services:

1. `Runtime`, `RuntimeResponse`, canonical `Decision`.
2. `EventLedger` for input, decision, response, tool, and state-patch events.
3. `StateProjector` for current state before context/validation and during tool need dedupe/ranking.
4. `ContextComposer` / `ContextPacket`.
5. `DecisionValidator` and `ToolValidationService` for `call_tool` validation.
6. `ToolIntentGuard`.
7. `ToolNeedService`, `ToolNeed`, `CapabilityCatalog`, `ToolRecommendationService`, `RecommendationRanker`, `ToolRegistry`, and `ToolSpec` for request-tool capability resolution.
8. `ToolExecutor` for `call_tool` decisions only.
9. `StatePatchService` for `propose_state_patch`; this is reachable but outside the strict ToolNeed/capability-resolution MVP.

Notably **not** reached by canonical Runtime:

- `RuntimeLoop` and RuntimeLoop-only models.
- `ActionPlanService`, `HandoffPlanService`, `ExecutionProposalService`, `PreconditionEvaluator`.
- `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and `ExecutionAuthorization` as active routing targets.

---

## ToolExecutor-Reachable Models

`ToolExecutor` reaches:

1. `ToolRegistry` / `ToolSpec` as the registered operation inventory and contract.
2. `ToolValidationService` for output schema validation and through policy preflight.
3. `ToolExecutionPolicyService` for existence/status/input validation before policy.
4. `PolicyGate`/`PolicyDecision` for allow/block/confirmation/approval outcomes.
5. `PendingActionService` / `PendingAction` for confirmation/approval outcomes and resume lifecycle.
6. Registered implementation function loaded from `ToolSpec.implementation`.
7. `FactExtractionService` after completed tool calls.

`ToolExecutor` does **not** reach `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, or `ExecutionAuthorization` except indirectly through `StateProjector` if old events exist in state. Its pending-action resume path uses `PendingAction`, not `ExecutionAuthorization`.

---

## Read-only Knowledge Query Path

The maintained read-only CLI query paths are:

- `--state-build`
- `--impact`
- `--why`
- `--relationships`
- `--graph-issues`
- `--entity-types`
- `--current-facts`
- `--unhealthy` / `--down`

`projected_state_from_args` opens the ledger/store, builds a `StateProjector`, optionally uses `project_state_with_cache`, and returns projected state without ingesting or executing anything. Routing dispatches these commands before normal message execution.

Projection derives:

- observations/evidence/facts from events.
- ToolNeeds, pending actions, registered tools, and legacy artifacts from events.
- aliases, inferred facts, fact supports, relationships, entity type assertions, graph issues, and conflicts.

---

## Capability Resolution Path

Exact canonical path:

```text
Runtime._route(decision.kind == "request_tool")
  -> ToolNeedService.create_from_decision
      -> slugify name/capability
      -> project state
      -> dedupe against state.open_tool_needs
      -> append tool_need.created if new
  -> ToolRecommendationService.recommend_for
      -> CapabilityCatalog.recommend_for
      -> RecommendationRanker.rank
  -> ToolNeedService.resolve_capability
      -> CapabilityCatalog.get(capability)
      -> ToolRegistry.list_tools_for_capability(capability, visible_only=True)
      -> provider_recommendations from ranked recommendations
      -> handoff_candidates from catalog recommendations with backend_type or operation
  -> RuntimeResponse(kind="tool_need", payload={tool_need, recommendations, capability_resolution})
```

Important boundary conclusion: `CapabilityRecommendation.operation` is **not** a registered operation. Registered operations come only from `ToolRegistry.list_tools_for_capability(...)`; provider/handoff candidates come from catalog recommendation metadata.

---

## Quarantined / Experimental Artifacts

The following are quarantined and should not be treated as current-core:

1. **RuntimeLoop cluster**
   - `RuntimeLoop`, `RuntimeInput`, `RuntimeResult`, RuntimeLoop `Decision`, `RuntimeContext`, `RuntimeTool`, `EchoTool`.
   - `RuntimeLoopDecisionValidator`.
   - `RuntimeLoopToolRequestHandler`.

2. **Planning/execution artifact cluster**
   - `ActionPlan` and `ActionPlanService`: text-only, non-executable, legacy/experimental.
   - `HandoffPlan` and `HandoffPlanService`: non-executable boundary; no provider execution, approval, authorization, registration, credential, retry, or job ownership.
   - `ExecutionProposal` and `ExecutionProposalService`: legacy/experimental concrete-call proposal generation; not executable by itself.
   - `ExecutionAuthorization`: experimental non-core metadata; not internal execution lifecycle.
   - Precondition helpers: inspect-only reports for action plans.

3. **CLI side paths**
   - `--plan`, `--preconditions`, `--proposal`, `--handoff`, `--authorize-proposal` are marked experimental/legacy in help.
   - Their runtime dispatch is separate from normal Runtime message execution.

---

## Historical Compatibility Artifacts

These remain primarily to project/read old events or support old traces:

1. `StateProjector` projection of:
   - `execution_authorization.granted`
   - `execution_proposal.created`
   - `handoff_plan.created`
   - `action_plan.*`
   - `pending_action.*`
   - `tool.registered`
2. `EventLedger` validation of historical `execution_authorization.granted` event payloads.
3. `SQLiteEventLedger` persisted payload ID prefix reservation for `plan`, `handoff`, `auth`, and other old payload IDs.
4. `RuntimeTrace` / `RuntimeTraceReader` for read-only RuntimeLoop traces.
5. `DecisionJournal` records used by historical RuntimeLoop trace reconstruction.

---

## Suspicious Duplicates / Naming Collisions

1. **`operation` means two different things**
   - `ToolSpec` is a registered callable operation contract with implementation and schemas.
   - `CapabilityRecommendation.operation` is provider/handoff metadata only: it is not executable and is not a `ToolRegistry` operation unless separately registered as a `ToolSpec`.
   - Risk: provider/handoff operation metadata strings may be mistaken for executable registered operations. `ToolNeedService.resolve_capability` currently keeps the boundary clear by sourcing registered operations only from `ToolRegistry`.

2. **`PendingAction` vs `ExecutionAuthorization`**
   - `PendingAction` is part of canonical ToolExecutor policy outcome/resume flow.
   - `ExecutionAuthorization` is experimental/non-core legacy metadata.
   - Risk: “authorization” terminology may imply it approves pending tool calls. It does not.

3. **`ActionPlan` vs `ToolNeed` vs handoff candidates**
   - `ToolNeed` is current core.
   - `ActionPlan` is legacy/non-executable.
   - `handoff_candidates` in capability resolution are simple recommendation metadata, not `HandoffPlan` orchestration.

4. **`RuntimeResponse` vs `RuntimeResult`**
   - Canonical Runtime returns `RuntimeResponse`.
   - RuntimeLoop owns `RuntimeResult`.
   - Risk: both sound like current runtime result objects; only `RuntimeResponse` is canonical.

5. **Duplicate decision models / validators**
   - Canonical `Decision` / `DecisionValidator` are in `models.py` and `decisions.py`.
   - RuntimeLoop has its own `Decision` and `RuntimeLoopDecisionValidator`.

6. **Documentation drift remains in older audit docs**
   - Historical audit finding: `docs/runtime_reassessment.md` previously said default CLI/HTTP paths use RuntimeLoop, which contradicted current `build_local_app` wiring to `Runtime`; the cleanup now marks that wording stale/quarantined.
   - This appears to be stale audit documentation, not current code behavior.

7. **Tests still exercise quarantined artifacts**
   - RuntimeLoop tests are marked experimental in some places.
   - Planning/proposal tests still import `ActionPlanService` and `ExecutionProposalService`.
   - CLI parser tests still cover `--plan`, `--preconditions`, and `--proposal`.
   - These tests are not necessarily wrong, but they can make delete candidates look artificially required.

---

## Delete Candidates

Do **not** delete now. Candidate status means “appears removable later after migration/compatibility review.”

1. **RuntimeLoop cluster**
   - `seed_runtime/runtime_loop.py`
   - `seed_runtime/runtime_loop_decisions.py`
   - `seed_runtime/runtime_loop_tool_requests.py`
   - `seed_runtime/runtime_loop_context.py`
   - RuntimeLoop tests and old trace-specific tests after any desired trace migration.
   - Risk: historical `RuntimeTrace` / `DecisionJournal` readers and experimental tests depend on this vocabulary.

2. **Planning/execution side paths**
   - `ActionPlanService`, `HandoffPlanService`, `ExecutionProposalService`, `PreconditionEvaluator`, CLI `--plan`, `--preconditions`, `--proposal`, `--handoff`, `--authorize-proposal`.
   - The existing quarantine audit already lists these as later delete candidates after stored-ledger/test compatibility review.

3. **Historical projection branches**
   - `action_plan.*`, `handoff_plan.created`, `execution_proposal.created`, `execution_authorization.granted` projection in `StateProjector`.
   - Risk: old SQLite ledgers may still contain these events.

4. **`ExecutionAuthorization` validation in EventLedger**
   - Candidate only if historical `execution_authorization.granted` events are migrated or dropped.

5. **Package exports that previously kept quarantined concepts looking current**
   - `seed_runtime.__init__` no longer exports `HandoffPlan`, `Precondition`, or `PreconditionReport`; import them from implementation modules for explicit legacy side-path tests.
   - Risk: direct package-root import compatibility was intentionally narrowed while preserving implementation-module compatibility.

6. **`ToolkitCandidate`**
   - Possible delete candidate only after a builder/toolkit-generation audit; it is not Runtime or Core MVP reachable.

---

## Recommended Next Cleanup

Smallest safe next cleanup step:

1. **Documentation cleanup only, no behavior change**
   - Keep stale audit docs quarantined whenever they present RuntimeLoop as default/current. `docs/runtime_reassessment.md` is marked as historical because it previously said default CLI/HTTP use RuntimeLoop while current `build_local_app` constructs `Runtime`.

2. **Then quarantine-by-test-marker cleanup**
   - Ensure all RuntimeLoop tests are consistently marked experimental/quarantined.

3. **Then delete-candidate planning**
   - Prepare a separate migration/delete plan for `ExecutionProposal`, `ExecutionAuthorization`, preconditions, `ActionPlanService`, `HandoffPlanService`, and CLI side flags. Do not wire any of these into Runtime.

Do **not** add new orchestration systems, new planning selection objects, new execution proposals, or any RuntimeLoop wiring.

---

## Files Inspected

Primary files inspected:

- `seed_runtime/runtime.py`
- `seed_runtime/models.py`
- `seed_runtime/decisions.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/capability_catalog.py`
- `seed_runtime/tool_recommendations.py`
- `seed_runtime/recommendation_ranker.py`
- `seed_runtime/registry.py`
- `seed_runtime/execution.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/pending_actions.py`
- `seed_runtime/events.py`
- `seed_runtime/state.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/input_inspector.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/observations.py`
- `seed_runtime/evidence.py`
- `seed_runtime/facts.py`
- `seed_runtime/predicate_catalog.py`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/entity_type_catalog.py`
- `seed_runtime/inference_catalog.py`
- `seed_runtime/runtime_loop.py`
- `seed_runtime/runtime_loop_decisions.py`
- `seed_runtime/runtime_loop_tool_requests.py`
- `seed_runtime/action_plans.py`
- `seed_runtime/handoff_plans.py`
- `seed_runtime/execution_proposals.py`
- `seed_runtime/preconditions.py`
- `seed_runtime/runtime_trace.py`
- `seed_runtime/decision_journal.py`
- `seed_runtime/__init__.py`
- `scripts/seed_local.py`
- `docs/audit/planning_execution_artifact_quarantine.md`
- `docs/runtime_reassessment.md`
- `README.md`
- selected tests covering RuntimeLoop, action plans, execution proposals, and CLI side-path parsing.

---

## Commands Run During Audit

- `pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' | sort && git status --short`
- `find .. -name AGENTS.md -print; printf '\nTop files:\n'; rg --files | sed -n '1,200p'; printf '\nStatus:\n'; git status --short`
- `rg -n "class Runtime|def handle_user_message|def _route|class DecisionValidator|class ToolExecutor|def execute|resume_approved|class ToolNeedService|class ToolRecommendationService|class CapabilityCatalog|class ToolRegistry|class ToolSpec|class ToolValidationService|class ToolExecutionPolicyService|class StateProjector|def project_state_with_cache|class ProjectionStore|class InputInspector|class ObservationSource|class ObservationNormalizer|class ObservationIngestor|class ActionPlan|class HandoffPlan|class ExecutionProposal|class ExecutionAuthorization|RuntimeLoop|RuntimeInput|RuntimeResult|RuntimeTool|--plan|--handoff|--proposal|--authorize-proposal|state-summary|impact|relationships|graph-issues|entity-types|current-facts|unhealthy|down" seed_runtime scripts tests docs README.md *.md`
- `sed -n '1,340p' seed_runtime/runtime.py`
- `sed -n '120,330p' seed_runtime/runtime.py`
- `sed -n '330,430p' seed_runtime/runtime.py`
- `sed -n '1,260p' seed_runtime/models.py`
- `sed -n '1,260p' seed_runtime/decisions.py`
- `sed -n '1,240p' seed_runtime/registry.py`
- `sed -n '1,280p' seed_runtime/tool_needs.py`
- `sed -n '1,260p' seed_runtime/capability_catalog.py`
- `sed -n '1,220p' seed_runtime/tool_recommendations.py`
- `sed -n '1,220p' seed_runtime/recommendation_ranker.py`
- `sed -n '1,320p' seed_runtime/execution.py`
- `sed -n '1,260p' seed_runtime/tool_validation.py`
- `sed -n '1,260p' seed_runtime/tool_execution_policy.py`
- `sed -n '1,260p' seed_runtime/pending_actions.py`
- `sed -n '1,220p' seed_runtime/events.py`
- `sed -n '1,220p' seed_runtime/state.py`
- `sed -n '672,830p' seed_runtime/state.py`
- `sed -n '1,260p' seed_runtime/projection_store.py`
- `sed -n '1,220p' seed_runtime/input_inspector.py`
- `sed -n '1,180p' seed_runtime/observation_sources.py`
- `sed -n '1,260p' seed_runtime/observation_normalizers.py`
- `sed -n '1,260p' seed_runtime/observations.py`
- `sed -n '1,180p' seed_runtime/evidence.py`
- `sed -n '1,220p' seed_runtime/facts.py`
- `rg -n "class .*ObservationSource|class ObservationCollectionService|def collect|def ingest|def ingest_input" seed_runtime/observation_sources.py seed_runtime/ansible_inventory_source.py scripts/seed_local.py`
- `rg -n "state_summary|state-summary|impact|why|relationships|graph-issues|entity-types|current-facts|unhealthy|down|decision-context|project_state_with_cache|SQLiteProjectionStore|format_" scripts/seed_local.py`
- `sed -n '1,220p' seed_runtime/runtime_loop.py`
- `sed -n '1,220p' seed_runtime/runtime_loop_decisions.py`
- `sed -n '1,180p' seed_runtime/runtime_loop_tool_requests.py`
- `sed -n '1,160p' seed_runtime/runtime_loop_context.py`
- `sed -n '1,240p' seed_runtime/action_plans.py`
- `sed -n '1,240p' seed_runtime/handoff_plans.py`
- `sed -n '1,180p' seed_runtime/execution_proposals.py`
- `sed -n '1,220p' seed_runtime/preconditions.py`
- `rg -n -e "--plan|--handoff|--proposal|--authorize-proposal|args\.plan|args\.handoff|args\.proposal|args\.authorize_proposal|ExecutionProposalService|HandoffPlanService|ActionPlanService|grant_execution_authorization|preconditions" scripts/seed_local.py seed_runtime docs README.md tests`
- `rg -n -e "workflow engine|internal executor|execution proposal|execution authorization|RuntimeLoop|default CLI.*RuntimeLoop|HTTP.*RuntimeLoop|Seed owns|execute.*action plan|--plan.*core|action plan orchestration|call providers|provider executes|authorize execution|grant.*execution" docs README.md *.md tests seed_runtime scripts | sed -n '1,220p'`
- multiple `nl -ba ... | sed -n ...` commands to collect line-numbered citations.
- `git status --short`
