# Selected Recommendation Boundary Design Report

## 0. Current boundary finding

There is a real missing ownership boundary.

Today, the runtime can produce capability-resolution metadata for a `ToolNeed`: `known_capability`, `registered_operations`, `provider_recommendations`, and `handoff_candidates`. That happens in `ToolNeedService.resolve_capability`, and the method is explicitly a read-only capability-resolution reporter: it does not execute tools, authorize actions, create pending actions, or mutate registry/catalog state.

Separately, `ActionPlanService.create_plan` requires one `ToolNeed` and one `RankedRecommendation`, and creates a non-executable `ActionPlan` for the chosen provider.

What is missing is a durable, auditable record that says: "for this `ToolNeed`, this candidate was selected, from this candidate set, for this reason." The current code ranks and returns recommendations, but does not persist which one was chosen. `ToolRecommendationService` is intentionally read-only and only returns ranked recommendations.

## 1. Should there be a `RecommendationSelection` / `CapabilityResolutionSelection` object?

Yes. The object should exist, but the recommended name is **`CapabilityResolutionSelection`**, not `RecommendationSelection`.

Reason: the selection boundary is broader than recommendations. The current resolution output contains:

- catalog-backed provider recommendations,
- registered operation candidates,
- handoff candidates,
- and should also support manual/no-op choices.

`RecommendationSelection` sounds too narrow and would bias the model toward catalog recommendations only. `CapabilityResolutionSelection` better describes the durable decision: it selects one way to resolve a `ToolNeed`, without implying executability.

The existing `ToolNeed` model records the missing capability and desired shape, but it has no selected candidate field. The existing `ActionPlan` records provider/capability text-plan metadata, but it does not record the selection event that caused the plan.

Recommended conceptual model:

```text
CapabilityResolutionSelection
- id
- workspace_id
- tool_need_id
- capability
- selected_kind
- selected_ref
- selection_reason
- selected_by
- selected_at
- source_event_id / causation_id / correlation_id
- candidate_set_fingerprint
- selected_candidate_fingerprint
- status: active | superseded | cancelled
```

This should be durable event-sourced state, projected from events, just like `ToolNeed`, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and pending-action lifecycle are currently projected from ledger events.

## 2. Should it support selecting provider recommendation, registered operation candidate, handoff candidate, manual/no-op?

Yes. It should support all four categories, with distinct semantics.

Recommended enum:

```text
CapabilityResolutionSelectionKind =
  "provider_recommendation"
  "registered_operation"
  "handoff_candidate"
  "manual"
  "no_op"
```

### `provider_recommendation`

Selects a catalog/ranker provider recommendation. It is suitable input for non-executable `ActionPlan` creation.

Provider recommendations currently come from the capability catalog and are ranked by `RecommendationRanker`. The ranked object includes provider, summary, kind, source, risk class, notes, score, reasons, and reasoning.

### `registered_operation`

Selects an already registered, model-visible tool operation from `ToolRegistry.list_tools_for_capability`. This is not the same thing as choosing a provider recommendation. Registered operations are real tools in the registry, with input/output schema, policy action, implementation, status, visibility, risk class, and capabilities.

Selection of a registered operation should produce a **call-tool suggestion / affordance**, not an `ActionPlan` by default.

### `handoff_candidate`

Selects a catalog-backed handoff option: provider plus optional backend type and operation. `ToolNeedService.resolve_capability` currently derives handoff candidates from catalog recommendations where `backend_type` or `operation` is present.

A handoff candidate remains non-executable. It may feed a non-executable `ActionPlan`, and after the `ActionPlan` is accepted, a non-executable `HandoffPlan` can be created.

### `manual`

Records that the selected resolution is manual/human-owned. It should not fabricate an executable operation. If it creates anything downstream, it should be a non-executable text plan or handoff boundary only.

### `no_op`

Records that the `ToolNeed` was intentionally not resolved now. This is useful for audit and avoids ambiguity between "not selected yet" and "explicitly declined/deferred."

## 3. Where should selection live?

Selection should live in a **new service**, for example:

```text
CapabilityResolutionSelectionService
```

or, if shorter:

```text
ToolNeedSelectionService
```

It should not live inside the existing three services.

### Not `ToolNeedService`

`ToolNeedService` should continue to own creation, deduplication, status transitions, and read-only resolution metadata. Its `resolve_capability` method already establishes a safety boundary as an option reporter. Adding durable candidate selection there would mix "describe options" with "choose one option."

### Not `ToolRecommendationService`

`ToolRecommendationService` is intentionally read-only and exists to look up/rank catalog recommendations. It should remain stateless and deterministic over current state/catalog.

### Not `ActionPlanService`

`ActionPlanService` owns non-executable action-plan generation and action-plan lifecycle. It currently creates a plan from an already chosen `RankedRecommendation`; it should not decide which candidate won. Selection is upstream of plan creation.

### New service responsibility

The new service should:

1. Load the current `ToolNeed`.
2. Read current resolution candidates.
3. Validate the selected candidate still exists.
4. Persist a `capability_resolution_selection.created` event.
5. Project the active selection into `State`.
6. Optionally supersede prior active selections for the same `ToolNeed`.
7. Never execute tools.
8. Never create pending actions.
9. Never call `ToolExecutor`.

That separation preserves the current architectural rule that runtime remains canonical and RuntimeLoop stays quarantined.

## 4. What should be durable vs. derived?

### Durable

The durable selection should store **identity, audit, and drift-detection data**, not copied catalog/tool metadata.

Recommended durable fields:

```text
id
workspace_id
tool_need_id
capability
selected_kind
selected_ref
selection_reason
selected_by
selected_at
source_event_id
causation_id
correlation_id
candidate_set_fingerprint
selected_candidate_fingerprint
status
supersedes_selection_id
```

The `selected_ref` should be small and type-specific.

#### Provider recommendation ref

```text
{
  "provider": "open_meteo",
  "capability": "weather_lookup",
  "catalog_source": "capability_catalog",
  "recommendation_kind": "provider"
}
```

#### Registered operation ref

```text
{
  "tool_name": "environment_inventory.list_open_tool_needs",
  "toolkit_id": "environment_inventory",
  "capability": "environment_inventory"
}
```

#### Handoff candidate ref

```text
{
  "provider": "ansible",
  "capability": "service_management",
  "backend_type": "ansible",
  "operation": "restart_service"
}
```

For handoff candidates, `backend_type` and `operation` are acceptable as identifying ref fields because the handoff candidate itself is currently derived from those fields. Downstream handoff creation should still re-resolve against current catalog metadata and detect drift.

#### Manual/no-op ref

```text
{
  "mode": "manual"
}
```

or:

```text
{
  "mode": "no_op"
}
```

### Derived

The following should be derived at use time from the current canonical source:

- provider summary,
- provider notes,
- provider risk class,
- ranked score,
- ranked reasons,
- backend policy wording,
- operation display text,
- registered tool summary,
- registered tool schema,
- registered tool implementation,
- registered tool status,
- registered tool visibility,
- registered tool risk class.

The reason is simple: catalog and registry metadata can change. The selection should say what was selected, not freeze stale operational metadata.

### Durable fingerprints, not durable copied metadata

To avoid stale copies while preserving auditability, store fingerprints:

```text
candidate_set_fingerprint
selected_candidate_fingerprint
catalog_entry_fingerprint
tool_spec_fingerprint
```

If a selected provider/tool/handoff candidate later resolves to different current metadata, the system can mark the selection as "stale" or "needs review" without having copied the old metadata into active execution/planning paths.

## 5. How should selected provider recommendation feed `ActionPlanService`?

A selected provider recommendation should feed `ActionPlanService` through a **materialization step**, not by copying the ranked recommendation into the selection forever.

Recommended flow:

```text
ToolNeed
  -> ToolRecommendationService.recommend_for(...)
  -> CapabilityResolutionSelectionService.select_provider(...)
  -> persisted CapabilityResolutionSelection
  -> materialize current RankedRecommendation from selection ref
  -> ActionPlanService.create_plan(tool_need, ranked_recommendation, state)
```

`ActionPlanService.create_plan` already expects a `ToolNeed`, a `RankedRecommendation`, and a state snapshot. The new selection service should provide a helper such as:

```text
materialize_ranked_recommendation(selection, tool_need, state) -> RankedRecommendation
```

That helper should:

1. Re-run or read current ranked recommendations.
2. Match by provider/capability/kind/source.
3. Compare fingerprint if available.
4. Return the current `RankedRecommendation`.
5. Fail with a stale-selection diagnostic if the selected recommendation no longer exists.

The resulting `ActionPlan` should ideally gain an optional field:

```text
capability_resolution_selection_id: str | None
```

That keeps the causal link durable without forcing the plan itself to own selection. Until that field exists, the selection event ID can be carried as `causation_id` or `correlation_id` when creating the action plan.

## 6. How should selected registered operation candidate differ from selected provider/handoff candidate?

A registered operation selection is different in kind, not merely different in source.

### Registered operation candidate

A registered operation candidate points to a real `ToolSpec` in `ToolRegistry`. `ToolSpec` includes schemas, policy action, implementation, status, visibility, risk class, and capabilities.

It should be treated as:

```text
"This already-registered tool may satisfy the ToolNeed."
```

It should not be treated as:

```text
"Create an external-provider action plan."
```

It should produce a **suggestion to call a visible registered tool**, subject to normal runtime validation/policy, but the selection event itself must not execute anything.

### Provider recommendation

A provider recommendation points to a catalog suggestion. It may be useful for a non-executable `ActionPlan`. Catalog recommendations can include provider, summary, kind, source, risk class, notes, backend type, and operation.

It should be treated as:

```text
"This provider could satisfy the missing capability; propose a non-executable plan."
```

### Handoff candidate

A handoff candidate is provider-backed but handoff-specific. It identifies an external-provider boundary. Handoff plans are explicitly non-executable and may not imply approval, credentials, provider trust, tool registration, or execution authorization.

It should be treated as:

```text
"This external handoff boundary could satisfy the accepted action plan."
```

### Practical distinction

| Selection kind | Canonical source | Downstream artifact | Executable? |
| --- | --- | --- | --- |
| `registered_operation` | `ToolRegistry` / `ToolSpec` | call-tool suggestion only | Selection: no. Later `call_tool`: policy-controlled |
| `provider_recommendation` | `CapabilityCatalog` + ranker | non-executable `ActionPlan` | no |
| `handoff_candidate` | `CapabilityCatalog` handoff metadata | non-executable `ActionPlan` then non-executable `HandoffPlan` | no |
| `manual` | user/system rationale | optional text-only plan | no |
| `no_op` | user/system rationale | none | no |

## 7. Should selecting a registered operation create an `ActionPlan`, or should it remain only a `call_tool` suggestion?

It should remain only a `call_tool` suggestion by default.

Reason:

- `ActionPlanService` is designed around a chosen provider recommendation and creates a non-executable proposal for satisfying a ToolNeed / capability gap.
- Registered operations are already model-visible tools that the runtime can expose in context.
- Actual tool execution is already isolated under the `call_tool` decision branch in canonical `Runtime`, which invokes `ToolExecutor.execute`.

Creating an `ActionPlan` for a registered operation would blur two boundaries:

1. **Planning boundary:** provider/handoff plan, non-executable.
2. **Tool-call boundary:** registered operation, policy-gated execution path.

The selection service should therefore emit something like:

```text
selected registered operation:
  tool_name
  toolkit_id
  capability
  message: "This registered operation can satisfy the ToolNeed via normal call_tool flow."
```

But it must not:

- call the tool,
- create a pending action,
- call `ToolExecutor`,
- grant authorization,
- or fabricate a provider/handoff plan.

If a UI wants to show a human-readable explanation, that should be a **selection explanation**, not an `ActionPlan`.

## 8. What fields are needed to avoid copying stale catalog metadata?

Use **references and fingerprints**, not copied mutable metadata.

### Required common fields

```text
id
workspace_id
tool_need_id
capability
selected_kind
selected_ref
selection_reason
selected_by
selected_at
source_event_id
causation_id
correlation_id
candidate_set_fingerprint
selected_candidate_fingerprint
status
```

### Provider recommendation `selected_ref`

```text
provider
capability
recommendation_kind
source
catalog_namespace/catalog_source
```

Avoid durably copying:

- summary,
- notes,
- risk class,
- rank score,
- rank reasons,
- backend type,
- operation.

Those should be derived from current catalog/ranker state when needed.

### Registered operation `selected_ref`

```text
tool_name
toolkit_id
capability
```

Optionally:

```text
tool_contract_fingerprint
```

Avoid durably copying:

- input schema,
- output schema,
- implementation,
- policy action,
- visibility,
- status,
- examples.

Those are current `ToolSpec` metadata and should be read from registry/projection at use time.

### Handoff candidate `selected_ref`

```text
provider
capability
backend_type
operation
```

Optionally:

```text
catalog_recommendation_fingerprint
```

Avoid durably copying:

- handoff policy summary,
- secret boundary text,
- current provider notes,
- approval wording.

`HandoffPlanService` should continue deriving backend type, operation, target, policy summary, and secret boundary from the accepted `ActionPlan`, current state, and catalog metadata.

### Manual/no-op fields

Manual/no-op needs durable rationale because there may be no catalog/registry source:

```text
manual_label
manual_reason
no_op_reason
expires_at/revisit_after optional
```

These are not stale catalog metadata; they are the selection itself.

## 9. Smallest safe implementation path

No code should be implemented as part of this report. The smallest safe future path would be:

### Step 1: Add model and event projection only

Add:

```text
CapabilityResolutionSelection
CapabilityResolutionSelectionKind
```

Add `State.capability_resolution_selections` and project:

```text
capability_resolution_selection.created
capability_resolution_selection.superseded
capability_resolution_selection.cancelled
```

This mirrors existing event-projection style for ToolNeeds / capability gaps, action plans, handoff plans, pending actions, and execution proposals.

### Step 2: Add new service

Add:

```text
CapabilityResolutionSelectionService
```

Responsibilities:

- validate selected candidate against current resolution output,
- persist selection event,
- supersede previous active selection for same `ToolNeed`,
- compute candidate/ref fingerprints,
- never execute tools,
- never create pending actions,
- never call `ToolExecutor`.

### Step 3: Keep `ToolNeedService.resolve_capability` read-only

Do not move selection into `resolve_capability`. That method should remain an option reporter.

### Step 4: Provider selection adapter to `ActionPlanService`

For `selected_kind = provider_recommendation`:

1. Re-resolve ranked recommendations.
2. Match selected provider ref.
3. Pass the materialized current `RankedRecommendation` into `ActionPlanService.create_plan`.

`ActionPlanService` should remain non-executable.

### Step 5: Handoff selection adapter

For `selected_kind = handoff_candidate`:

1. Create a provider-backed non-executable `ActionPlan`, or require an existing accepted action plan.
2. Use `HandoffPlanService` only after the action plan is accepted.
3. Keep the handoff non-executable.

### Step 6: Registered operation suggestion only

For `selected_kind = registered_operation`:

- Return/store a suggestion such as:

```text
selected_registered_operation:
  tool_name
  toolkit_id
  capability
  message: "This registered operation can satisfy the ToolNeed via normal call_tool flow."
```

- Do not create an `ActionPlan`.
- Do not execute.
- Do not create a pending action.
- Do not call `ToolExecutor`.

This preserves the hard separation from the current `Runtime` branch where only a `call_tool` decision invokes `ToolExecutor.execute`.

### Step 7: Manual/no-op

For `manual`:

- Store the rationale.
- Optionally create a text-only manual plan later, but not by default.

For `no_op`:

- Store the rationale.
- Optionally close or mark the `ToolNeed` with a separate status transition if desired.

The existing `ToolNeedStatus` enum has lifecycle statuses but no `deferred` or `resolved_by_existing_tool` status today, so avoid overloading status until a lifecycle design is explicit.

## Final recommendation

The clean boundary is:

```text
ToolNeedService
  owns ToolNeed creation/status and read-only capability resolution.

ToolRecommendationService
  owns read-only ranking of catalog provider recommendations.

CapabilityResolutionSelectionService
  owns durable selected-candidate choice.

ActionPlanService
  consumes selected provider/handoff materialization to create non-executable ActionPlans.

HandoffPlanService
  consumes accepted ActionPlans to create non-executable HandoffPlans.

Runtime
  remains canonical.

RuntimeLoop
  remains quarantined/read-only historical path.
```

This satisfies the hard constraints:

- Runtime remains canonical.
- RuntimeLoop remains quarantined.
- No tools are executed.
- `ToolExecutor` is not called by selection.
- No pending actions are created.
- `CapabilityCatalog` remains metadata/planning, not execution.
- Provider/handoff operations remain non-executable.
- `ActionPlan` remains non-executable.
- `HandoffPlan` remains non-executable.
