# Tool vocabulary orientation recovery investigation

## Scope and method

This is a recovery investigation only. It does not rename concepts, introduce a new vocabulary, redesign runtime routing, change registries, or add execution behavior. It asks what orientation the current operational vocabulary already expresses in implementation, with repository code and prior recovery documents treated as authority over architectural preference.

Commands used during this investigation:

```bash
pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' .. /workspace 2>/dev/null | head -50 && rg --files | head -50
cat AGENTS.md && rg -n "class ToolNeed|ToolNeed|ToolRecommendation|ToolRegistry|ToolSpec|ToolExecutor|CapabilityCatalog|request_tool|call_tool|provider recommendation|reconciliation|execution" -S .
sed -n '1,260p' seed_runtime/runtime.py; sed -n '1,320p' seed_runtime/execution.py; sed -n '1,260p' seed_runtime/tools.py; sed -n '1,260p' seed_runtime/capabilities.py
sed -n '200,420p' seed_runtime/runtime.py; sed -n '1,260p' seed_runtime/models.py; sed -n '1,260p' seed_runtime/registry.py; sed -n '1,260p' seed_runtime/tool_needs.py; sed -n '1,280p' seed_runtime/tool_recommendations.py; sed -n '1,260p' seed_runtime/capability_catalog.py
for f in implementation_execution_grammar_recovery_investigation.md docs/tool_vocabulary_reconciliation.md docs/tool_execution_ownership_audit.md docs/capability_operation_execution_reconciliation.md docs/execution_concepts_implementation_investigation.md docs/execution_inquiry_orientation_investigation.md docs/execution_characterization_inquiry_surface_investigation.md docs/natural_language_execution_path_inventory_audit.md; do echo ---$f; test -f $f && sed -n '1,220p' $f | head -220; done
```

Primary implementation evidence reviewed:

- `seed_runtime/runtime.py`
- `seed_runtime/execution.py`
- `seed_runtime/models.py`
- `seed_runtime/registry.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/tool_recommendations.py`
- `seed_runtime/capability_catalog.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/context.py`
- `seed_runtime/recommendation_ranker.py`
- prior execution, tool-vocabulary, natural-language-routing, and capability/execution recovery documents listed in the prompt

## Executive answer

Current operational vocabulary is mixed, but the most visible runtime vocabulary is still strongly oriented toward **model/tool invocation**:

```text
Decision.kind == request_tool
Decision.kind == call_tool
ToolNeed
ToolSpec
ToolRegistry
ToolExecutor
ToolRecommendationService
ToolContext
ToolCallResult
```

Implementation responsibility is more nuanced than those names imply. The code usually does not begin from a generic external agent wanting a tool. In the canonical `request_tool` branch it begins from a validated runtime decision, records a capability gap, resolves registered operation candidates, and returns provider/handoff metadata without execution. In the canonical `call_tool` branch it executes exactly one registered operation after registry validation and policy checks. In other branches it records answers/questions/refusals or applies state patches without tools.

Therefore the hypothesis is **partially supported**:

- Supported: many current names speak to the model-visible/tool-call boundary more naturally than to Seed's inquiry lifecycle.
- Supported: several names are architecturally sound in responsibility but orientation-inverted in vocabulary, especially `ToolNeed`, `request_tool`, `ToolRecommendationService`, and `ToolRegistry`.
- Rejected as universal: implementation does not treat `tool` as the architectural center of all work. Runtime routing, projection, state patches, diagnostics, observations, and provider recommendations are owned by other responsibilities.
- Supported with boundary: `ToolExecutor` is correctly tool-centered for the one family it owns: registered operation execution.

## Concept responsibility and orientation matrix

| Concept | Implementation-backed responsibility | Primary orientation expressed by name/API | Actual owner/boundary | Orientation finding |
| --- | --- | --- | --- | --- |
| `Decision.kind` | Enumerates structured runtime outcomes: answer, question, `call_tool`, `request_tool`, legacy plan kinds, state patch, refusal. | Model/runtime decision vocabulary. | Runtime decision validation and routing. | Mixed: Seed has structured outcomes, but two central work-continuation branches are named from tool invocation. |
| `request_tool` | Runtime branch creates or reuses a `ToolNeed`, ranks provider recommendations, resolves known capability, registered operation candidates, and handoff candidates; it does not execute. | LLM/external-agent request for a tool. | Capability-gap recording and read-only capability resolution. | Orientation-inverted: responsibility is capability gap / continuation need, but vocabulary begins with tool. |
| `call_tool` | Runtime branch delegates to `ToolExecutor.execute()` with a named registered tool and arguments. | Model/tool invocation. | Registered operation execution path. | Correctly tool-oriented within this narrow branch. |
| `ToolNeed` | Durable model with name, summary, capability, reason, requested event, risk hint, desired inputs/outputs, and lifecycle status. | Need for a tool. | Missing capability / inquiry continuation gap. | Orientation-inverted: implementation stores a capability need, not proof that a tool is architecturally required. |
| `ToolNeedService` | Creates deduplicated need events from decisions and returns read-only capability resolution metadata. | Tool-need lifecycle. | Runtime service for capability-gap creation and resolution. | Mostly orientation-inverted: implementation is Seed capability-resolution oriented, but API is tool-worded. |
| `ToolRecommendationService` | Looks up and ranks catalog recommendations for a `ToolNeed` using a capability catalog and ranker; read-only and non-mutating. | Tool recommendation. | Provider/handoff recommendation ranking for a capability gap. | Orientation-inverted: service recommends providers/handoffs, not tools to execute. |
| `CapabilityCatalog` | Read-only catalog of normalized capabilities to provider and handoff suggestions; explicitly does not execute tools. | Capability/provider. | Capability metadata boundary. | Already Seed/capability-oriented; not inverted. |
| `CapabilityRecommendation` | Suggested provider metadata with optional backend type and operation. | Provider capability metadata. | External provider/handoff suggestion. | Correctly provider-oriented; counterexample to tool-centered grammar. |
| `ToolRegistry` | Loads manifests, stores `ToolSpec`s, lists model-visible registered operations, and maps capabilities to registered operations. | Tool registry. | Registered operation catalog. | Partly inverted: registry entries are called tools, but architecture metadata says registered operations and capability mappings. |
| `ToolSpec` | Registered callable manifest record: name, schemas, policy action, implementation reference, visibility, risk, capabilities, examples. | Tool specification. | Registered operation specification made visible to model and executor. | Mixed: tool name is apt for model-visible callable; operation responsibility is broader and more precise. |
| `ToolExecutor` | Validates a registered tool through policy, appends tool-call events, imports implementation, invokes it, validates output, extracts facts, and handles pending approved calls. | Tool execution. | Registered operation execution. | Sound and only mildly inverted: name is acceptable inside registered-tool family, but unsafe if read as owning all execution. |
| `ToolContext` | Provides ledger/workspace/session/tool/call/registry context to a registered operation implementation. | Tool implementation context. | Registered operation invocation context. | Correctly tool-oriented for implementation call boundary. |
| `ToolCallResult` | Structured result for completed, failed, blocked, confirmation, or approval-required registered operation calls. | Tool-call result. | Registered operation result / pending policy outcome. | Correctly tool-oriented for call branch. |
| `CapabilityCatalog.recommend_for()` | Returns provider recommendations matching a need capability. | Capability recommendation. | Provider metadata lookup. | Seed/capability-oriented counterexample. |
| `ToolRegistry.list_tools_for_capability()` | Returns visible registered operations whose normalized capability list contains the requested capability. | Tool listing for capability. | Capability-to-registered-operation mapping. | Mixed: starts from capability, returns tools/operations. |
| Provider recommendation payload | Runtime returns provider, score, and reasons, plus handoff candidates; no provider invocation. | Provider/operator-facing metadata. | Read-only recommendation boundary. | Provider-oriented; rejects tool-as-center for this path. |
| Execution reconciliation documents | Prior recovery found multiple execution families and limited `ToolExecutor` ownership. | Execution-family responsibility. | Repository-level recovery evidence. | Supports responsibility-oriented grammar over universal tool execution. |
| Tool vocabulary reconciliation documents | Prior recovery distinguishes tool vocabulary compression and registered operation boundaries. | Vocabulary audit. | Documentation/recovery evidence. | Supports that current names compress several responsibilities into `tool`. |

## Recurring orientation perspectives

### Agent- or model-oriented vocabulary — accepted, but scoped

Accepted. `Decision` is proposed by the model and persisted as `model.decision.proposed`; retry prompts tell the model to return corrected JSON. The context composer exposes visible tools to the decision producer, and the runtime has explicit `request_tool` and `call_tool` decision kinds. This vocabulary answers, "What structured decision did the model make?" and "Which tool did it ask to call/request?"

Scope limit: this orientation is strongest at the model/runtime interface. It does not own projection, diagnostics, state patches, observation ingestion, provider recommendation, or presentation.

### Operator-oriented vocabulary — partially accepted

Partially accepted. Runtime records `input.user_message`, returns answers/questions/refusals, and diagnostic/report surfaces are operator-facing. However, the tool vocabulary under review is not primarily operator-oriented. `ToolNeed.summary`, recommendation reasons, and runtime response messages are readable by an operator, but the naming center is still tool/model-call vocabulary.

### Runtime-oriented vocabulary — accepted

Accepted. `Runtime.__seed_arch__` says runtime orchestration routes validated model decisions to owner services without owning their behavior. The implementation enforces owner separation by routing `request_tool` to `ToolNeedService`, `call_tool` to `ToolExecutor`, `propose_state_patch` to `StatePatchService`, and answer/question/refusal to response event branches.

### Seed-oriented vocabulary — partially accepted

Partially accepted. `CapabilityCatalog`, capability normalization, capability resolution, state projection, event ledger ownership, and policy boundaries are Seed-oriented implementation responsibilities. But the most visible work-continuation nouns remain `ToolNeed`, `ToolRecommendationService`, `ToolRegistry`, and `ToolExecutor`, which can make Seed's own inquiry continuation appear subordinate to tool acquisition/invocation.

### Provider-oriented vocabulary — accepted

Accepted. `CapabilityRecommendation` stores provider, backend type, operation, risk, notes, and source. Runtime recommendation payloads expose provider scores and reasons. The catalog explicitly does not execute tools. This is external-provider metadata, not Seed-owned operation execution.

### Registry-oriented vocabulary — accepted

Accepted. `ToolRegistry` owns registered operation catalog behavior: manifest loading, uniqueness, `require()`, visible listing, toolkit listing, and capability mapping. This perspective is appropriate for operation inventory, but it should not be confused with capability authority or provider recommendation authority.

## Does implementation naturally begin from tools?

No as a universal answer; yes in the model-visible operation path.

The canonical runtime begins from:

```text
operator input event
  -> projected state
  -> composed decision input
  -> model decision
  -> validation / intent guard
  -> owner-specific route
```

Only after that route does the path become tool-centered for `call_tool`, or tool-named capability-gap-centered for `request_tool`.

For `request_tool`, implementation more naturally proceeds as:

```text
validated request_tool decision
  -> ToolNeed(capability gap)
  -> provider recommendation ranking
  -> capability resolution
  -> registered operation candidates / handoff candidates
  -> RuntimeResponse(kind="tool_need")
```

For `call_tool`, implementation naturally proceeds as:

```text
validated call_tool decision
  -> ToolExecutionPolicyService
  -> ToolRegistry / ToolSpec
  -> policy outcome
  -> registered implementation import/invocation
  -> tool.call.* events
  -> ToolCallResult
```

For state patches, answers, questions, refusals, projections, diagnostics, presentation, and observations, implementation does not begin from tools at all.

## Actual responsibility recovered for named concepts

### `ToolNeed`

`ToolNeed` is a durable capability-gap record created from a `request_tool` decision. It stores `capability`, `summary`, `reason`, `risk_hint`, desired inputs/outputs, status, and the event that requested it. Its implementation responsibility is not "the LLM wants a tool" in isolation; it is "Seed recorded a missing capability or work-continuation gap from a validated decision."

The name is orientation-inverted because the strongest field is `capability`, and resolution asks whether the capability is known, whether registered operations exist, and whether provider/handoff metadata exists.

### `ToolRecommendationService`

`ToolRecommendationService` does not recommend executable tools. It ranks catalog recommendations for the need's capability against projected state. Its docstring explicitly says it is read-only and does not create providers, register tools, or mutate state. Its responsibility is provider/handoff recommendation enrichment for a capability gap.

The name is orientation-inverted because "tool recommendation" suggests an operation-selection service, while the implementation returns provider recommendations.

### `ToolRegistry`

`ToolRegistry` stores registered `ToolSpec`s and toolkits, validates duplicate registration, lists visible model-callable entries, and maps capabilities to registered operations. Its architecture metadata calls the owner `registered_operation_catalog` and says it exposes registered model-visible operations and capability mappings.

The name is partially inverted because it is a registry of model-visible registered operations, not a universal catalog of all capabilities or providers. It is correct only if "tool" is read narrowly as registered operation callable.

### `ToolSpec`

`ToolSpec` is the manifest-backed registered operation specification: schemas, policy action, implementation import path, status, visibility, risk, and capabilities. It is model-visible when status and visibility allow it.

The name is acceptable at the model-tool boundary and for manifests, but its responsibility is more exact than "tool": it is a registered operation contract plus capability labels and policy metadata.

### `ToolExecutor`

`ToolExecutor` owns registered operation execution only. It validates tool existence/status/input through policy services, records started/completed/failed/policy events, imports the registered implementation, invokes it with a `ToolContext`, validates output, extracts facts from completed output, and resumes approved pending actions.

The name is not wrong inside that boundary. The risk is interpretive: because many other implementation families perform work, the name encourages over-reading if "execution" is treated as universal Seed execution.

### `request_tool`

`request_tool` is not execution. It creates or reuses a need, ranks provider recommendations, resolves the capability against catalog and registry, and returns metadata. It does not call `ToolExecutor`, execute providers, authorize actions, create pending actions, or mutate registry/catalog state.

The name is the clearest orientation mismatch: implementation asks "what capability is missing and what metadata/candidates exist?" while the vocabulary says "request a tool."

### `call_tool`

`call_tool` is the narrow point where tool vocabulary is correct. It names a registered operation call after a validated decision. Runtime delegates to `ToolExecutor`; `ToolExecutor` enforces registry, validation, policy, event recording, and output validation.

### `CapabilityCatalog`

`CapabilityCatalog` is already aligned with Seed-oriented capability metadata. It maps normalized capabilities to provider/handoff suggestions and explicitly does not execute tools. This is a counterexample to the claim that all operational vocabulary is inverted.

## Does implementation already follow a Seed-oriented progression?

Partially, but not as a fully explicit lifecycle object.

Implementation evidence supports this progression for the capability-gap branch:

```text
Inquiry context / user input
  -> structured decision input
  -> validated request_tool decision
  -> capability gap (`ToolNeed.capability`)
  -> registered operation candidates (`ToolRegistry.list_tools_for_capability`)
  -> provider / handoff candidates (`CapabilityCatalog` + ranker)
  -> no execution unless a later `call_tool` decision names a registered operation
```

Implementation evidence supports this progression for registered operation execution:

```text
validated call_tool decision
  -> registered operation contract (`ToolSpec`)
  -> policy / validation result
  -> allowed registered implementation invocation
  -> event-backed result / pending outcome / failure
```

Implementation does **not** support a single explicit chain named:

```text
Inquiry -> Capability gap -> Operation candidate -> Execution path -> Termination
```

as one first-class runtime object. That chain is recoverable by composing current implementation responsibilities, not by pointing to a dedicated lifecycle class.

## Where vocabulary faces the wrong direction

The strongest orientation-inverted concepts are:

1. **`request_tool`**: implementation records and resolves a capability gap; name centers tool acquisition.
2. **`ToolNeed`**: implementation's durable meaning is missing capability / continuation need; name centers tool absence.
3. **`ToolRecommendationService`**: implementation ranks provider/handoff recommendations; name suggests recommending tools.
4. **`ToolRegistry`**: architecture metadata and behavior are registered operation catalog; name suggests generic tool universe.
5. **`ToolSpec`**: implementation is a registered operation contract; name is acceptable only at the model-visible callable boundary.

The following concepts are sound and not meaningfully inverted within their boundary:

- `call_tool`, because it invokes a registered operation through the tool execution path.
- `ToolExecutor`, if read as registered-tool executor only.
- `ToolContext`, because it is passed to registered operation implementations.
- `ToolCallResult`, because it is returned from registered tool-call execution.
- `CapabilityCatalog`, because it already starts from capability metadata.
- `CapabilityRecommendation`, because it is provider-oriented recommendation metadata.

## Counterexamples to the inversion hypothesis

Implementation evidence rejects any broad claim that Seed operational vocabulary is only agent/tool-invocation oriented:

- Runtime answer, question, refusal, and state-patch branches do not use the executor or registry.
- Capability catalog and recommendation entries are capability/provider-centered and explicitly non-executable.
- Tool need resolution starts from normalized capability and returns known-capability status, registered operations, provider recommendations, and handoff candidates.
- Prior execution grammar recovery found projection replay, event recording, observation ingestion, diagnostic surfaces, provider recommendation, state patch application, and presentation rendering as separate work families.
- The registry can list tools by capability, showing that capability is already an implementation axis even inside tool vocabulary.

## Supported conclusions

1. Current operational vocabulary speaks first to the **model/runtime tool-decision interface** in the canonical request/call paths.
2. Implementation responsibility is more Seed-oriented than the names imply: `request_tool` and `ToolNeed` preserve capability gaps and continuation needs, not merely agent desire for tools.
3. `ToolExecutor` does not own execution generally; it owns registered operation execution only.
4. `ToolRecommendationService` is provider/handoff recommendation ranking, not executable tool recommendation.
5. `ToolRegistry` and `ToolSpec` are registered operation inventory/contracts, not capability authority or provider authority.
6. Execution grammar exposes a deeper orientation mismatch: the repository already separates work by owner and termination point, while common vocabulary compresses capability gap, registered operation, provider suggestion, and invocation into `tool`.
7. Implementation evidence supports a recoverable Seed-oriented progression for one branch, but not a first-class universal inquiry lifecycle object.

## Unsupported conclusions

1. Unsupported: all execution in Seed is tool execution.
2. Unsupported: `ToolExecutor` owns projection, diagnostics, provider recommendation, state patches, observation ingestion, presentation, or capability resolution.
3. Unsupported: provider recommendations are executable handoffs or approvals.
4. Unsupported: `request_tool` proves a tool must be built, installed, registered, or called.
5. Unsupported: current implementation has a complete explicit `Inquiry -> Capability gap -> Operation candidate -> Execution path -> Termination` lifecycle model.
6. Unsupported: current names are uniformly wrong. Several are correct at the model-visible registered-operation boundary.
7. Unsupported: a rename or redesign is required by this investigation. This report recovers orientation only.

## Recommended next investigation

The next lowest-risk investigation should recover **where inquiry lifecycle evidence is already preserved across runtime, context composition, decision validation, capability resolution, and execution result events**.

Suggested question:

```text
Which current event fields, response payloads, and projected-state indexes preserve the chain from operator input to capability gap, registered operation candidate, provider recommendation, call result, or non-tool termination?
```

That investigation should remain read-only and implementation-backed. It should avoid renaming and should verify whether the recoverable Seed-oriented progression is visible in durable records or only reconstructable from code paths.

## Final recovery answer

Who is the current operational vocabulary speaking to?

- Primarily the model/runtime tool-decision interface for `request_tool`, `call_tool`, `ToolNeed`, `ToolSpec`, `ToolRegistry`, and `ToolExecutor`.
- Secondarily the registry/implementation boundary for registered operation contracts and invocation.
- Separately the provider/capability boundary for `CapabilityCatalog` and `CapabilityRecommendation`.

Does implementation naturally begin with tools, or with Seed's inquiry?

- The whole runtime begins with user input, projected state, context composition, and structured decision routing.
- The `call_tool` branch begins with a registered tool call after validation.
- The `request_tool` branch is named as a tool request but implemented as capability-gap creation and read-only resolution.

Which concepts are architecturally sound but orientation-inverted?

- `ToolNeed`, `ToolNeedService`, `ToolRecommendationService`, `request_tool`, and partly `ToolRegistry`/`ToolSpec`.

Has execution grammar exposed a deeper orientation mismatch?

- Yes. Execution recovery shows many owners and termination points. Tool vocabulary compresses missing capability, registered operation, provider metadata, and invocation into one word even though implementation keeps their responsibilities separate.

What evidence supports or rejects a Seed-oriented operational grammar?

- Supports: capability normalization, `ToolNeed.capability`, capability resolution payloads, registry capability mapping, provider/handoff catalog boundaries, and owner-specific runtime routes.
- Rejects as complete: no first-class universal inquiry lifecycle object currently owns the full progression from inquiry through termination.
