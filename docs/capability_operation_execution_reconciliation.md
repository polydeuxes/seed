# Capability / operation / execution / tool reconciliation

## Scope and method

This report is an observational reconciliation of implementation evidence. It does not recommend renaming, runtime redesign, execution redesign, toolkit-manifest redesign, or new operation vocabulary.

Commands executed during the investigation:

```bash
pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' && git status --short
cat AGENTS.md && rg -n "CapabilityCatalog|ToolRegistry|ToolExecutor|ToolNeedService|ToolValidationService|ToolRecommendationService|toolkit|registered implementation|diagnostic-inventory|diagnostic-shape-audit" .
rg -n "class CapabilityCatalog|class ToolRegistry|class ToolExecutor|class ToolNeedService|class ToolValidationService|class ToolRecommendationService|@dataclass.*ToolSpec|class ToolSpec|def resolve_capability|def register|def execute|__seed_arch__" seed_runtime seed_builder tests docs/tool_vocabulary_reconciliation.md | head -250
sed -n '1,220p' seed_runtime/capability_catalog.py; sed -n '1,180p' seed_runtime/registry.py; sed -n '230,280p' seed_runtime/models.py; sed -n '1,240p' seed_runtime/execution.py; sed -n '1,140p' seed_runtime/tool_needs.py; sed -n '1,140p' seed_runtime/tool_recommendations.py; sed -n '1,130p' seed_runtime/tool_validation.py
sed -n '140,340p' seed_runtime/tool_needs.py; sed -n '180,360p' seed_runtime/execution.py; sed -n '1,160p' seed_runtime/tool_execution_policy.py; sed -n '1,140p' toolkits/core/echo/toolkit.yaml; find capability_catalog -maxdepth 1 -type f -print -exec sed -n '1,120p' {} \;
python scripts/seed_local.py --help | head -80
python scripts/seed_local.py --capability-relationship service_management
```

Files inspected:

- `seed_runtime/capability_catalog.py`
- `seed_runtime/registry.py`
- `seed_runtime/models.py`
- `seed_runtime/execution.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/tool_recommendations.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_builder/registration.py`
- `seed_builder/validator.py`
- `toolkits/core/echo/toolkit.yaml`
- `capability_catalog/*.yml`
- selected tests and prior reconciliation documents located by ripgrep

## Executive answer

Yes, the implementation already separates capability, registered operation, and execution more strongly than the shared `tool` vocabulary suggests.

The strongest implementation-backed model is:

```text
Inquiry / request_tool decision
  -> ToolNeed capability request
  -> CapabilityCatalog provider/handoff metadata plus ToolRegistry registered operation candidates
  -> ToolExecutor execution only for a registered ToolSpec implementation selected by call_tool
  -> Event-ledger evidence from completed execution and fact extraction
```

The answer is not that the repository has fully renamed or conceptually redesigned `tool`. It has not. The answer is that the code already assigns different responsibilities to distinct components while retaining shared `tool` names in classes, methods, events, and manifest fields.

The responsibility that actually satisfies a capability today is not one thing. A capability can be partially satisfied or resolved by several read-only candidates: registered operations from `ToolRegistry`, ranked provider recommendations from `CapabilityCatalog` through `ToolRecommendationService`, handoff candidates from catalog metadata, and future generated/validated toolkit implementations. Actual in-process execution is satisfied only by a registered `ToolSpec` implementation invoked through `ToolExecutor`.

## 1. Implementation-backed responsibility ownership

| Subject | Responsibility actually owned | Supporting implementation | Strongest contradictory evidence | Confidence |
| --- | --- | --- | --- | --- |
| Capability | Normalized ability label used to connect needs, catalog entries, provider/handoff recommendations, and registered operation candidates. | `CapabilityCatalogEntry` stores `capability`, `summary`, and `recommendations`; `ToolSpec` stores normalized `capabilities`; `ToolNeedService` resolves by `tool_need.capability`. | The field is embedded inside `ToolSpec`, so capabilities are not isolated from registered operation metadata. | High |
| ToolNeed | Durable runtime record of a requested/missing capability and associated desired IO/risk metadata. | `ToolNeedService.create_from_decision()` normalizes `name` and `capability`, deduplicates against open needs, and appends `tool_need.created`. | The object and service retain `ToolNeed` vocabulary, which may imply a missing executable rather than a broader capability request. | High |
| ToolSpec | Registered callable operation contract: schemas, policy action, implementation path, visibility/status/risk, toolkit, and capabilities. | `ToolSpec` fields include `input_schema`, `output_schema`, `policy_action`, `implementation`, `status`, `visibility`, and `capabilities`. | It is named `ToolSpec`, not `OperationSpec`, and manifests store entries under `tools`. | High |
| Registered implementation | Python callable identified by a `ToolSpec.implementation` import path and invoked only after lookup, validation, and policy allow. | `ToolExecutor._load_registered()` imports from `tool.implementation`; the core echo manifest points to `toolkits.core.echo.operations:echo`. | The implementation path is only a string in the spec until execution time; registry registration alone does not prove importability or successful execution. | High |
| ToolExecutor | Runtime execution boundary for registered implementations, including validation/policy mediation, event recording, output validation, pending-action behavior, and fact extraction on completed calls. | `ToolExecutor.__seed_arch__` declares `registered_tool_execution`; `execute()` uses `ToolExecutionPolicyService`; `_execute_allowed_tool_call()` appends started/completed/failed events and calls the imported implementation. | Name says `ToolExecutor`, and events are `tool.call.*`, so vocabulary still collapses execution target and broader tool concepts. | High |
| ToolRegistry | Registered operation inventory loaded from toolkit manifests; maps names and capabilities to `ToolSpec` entries. | `ToolRegistry.__seed_arch__` owner is `registered_operation_catalog`; `register_toolkit()` stores toolkit tools; `list_tools_for_capability()` filters registered specs by normalized capability. | Public methods are `list_tools`, `get`, and `require`, and manifest entries are still called `tools`. | High |
| Provider recommendation | Read-only suggestion that a provider/backend/handoff path may satisfy a capability. | `CapabilityRecommendation` includes `provider`, `backend_type`, and optional `operation`; `ToolRecommendationService.recommend_for()` ranks catalog recommendations without registering or executing anything. | Recommendation metadata may include an `operation` string, which looks like an executable operation even though it is not a registered `ToolSpec`. | High |
| Tool invocation | A `call_tool` attempt identified by `tool_name` and arguments; executable only after registry lookup, status/input validation, and policy allow. | `ToolExecutionPolicyService.evaluate()` validates existence/status/input and policy; `ToolExecutor.execute()` only calls `_execute_allowed_tool_call()` when the policy outcome is `allow`. | Validation can also consult `state.tools` in some helper paths, so not every validation helper is registry-only in every context. | Medium-high |

## 2. Does the implementation naturally form a progression?

### Inquiry -> Capability

Supported. A `request_tool` decision is converted by `ToolNeedService.create_from_decision()` into a normalized capability-bearing `ToolNeed`. The service defaults capability from name when missing, deduplicates by either need name or capability, and records the need event. This supports an inquiry/request becoming a capability request, not an executable call.

Contradiction: this transition is named `request_tool`, and the event is `tool_need.created`, so presentation vocabulary still says tool.

Confidence: high.

### Capability -> Registered operation

Partially supported. `ToolNeedService.resolve_capability()` asks `ToolRegistry.list_tools_for_capability()` for visible registered operation candidates matching `tool_need.capability`. This means registered operations can be candidate satisfiers for a capability.

Not fully supported as a required progression: a capability can be known in `CapabilityCatalog` even when no registered operation exists, and catalog recommendations can exist without registry entries.

Confidence: medium-high.

### Capability -> Provider/handoff recommendation

Supported. `CapabilityCatalog.recommend_for()` maps a capability-bearing `ToolNeed` to `CapabilityRecommendation` entries, and `ToolRecommendationService` ranks those recommendations against state. `ToolNeedService.resolve_capability()` also returns handoff candidates from catalog recommendations carrying `backend_type` or `operation`.

Contradiction: recommendations may contain `operation`, which can blur the distinction from registered operation. The implementation nevertheless keeps these in `provider_recommendations` and `handoff_candidates`, not executable registry entries.

Confidence: high.

### Registered operation -> Execution

Supported with prerequisites. A registered `ToolSpec` becomes executable only when a `call_tool` decision supplies its name and arguments, `ToolExecutionPolicyService` validates existence/status/input, policy allows, and `ToolExecutor` imports and calls the implementation.

Contradiction: registration itself does not guarantee successful import, valid output, or allowed policy outcome.

Confidence: high.

### Execution -> Evidence

Supported for completed registered implementation calls. `_execute_allowed_tool_call()` appends `tool.call.completed` with output and immediately calls `FactExtractionService.observe_tool_result(completed_event)`. That makes execution output recordable evidence for later knowledge projection.

Contradiction: failed calls and policy-denied calls record events but do not represent the same completed-output evidence path.

Confidence: high for completed calls; medium for all invocation outcomes.

## 3. What does `ToolRegistry` primarily register?

`ToolRegistry` primarily registers registered operation contracts / implementation-backed callable specs loaded from toolkit manifests.

It does not primarily register abstract capabilities, because capabilities are only fields on `ToolSpec` and are used for filtering. It does not primarily register providers, because provider recommendations live in `CapabilityCatalog`. It does not itself execute implementations; it stores and retrieves `ToolSpec` objects.

The contradictory evidence is vocabulary: the storage dictionary is `_tools`, methods are `list_tools()` and `require()`, the model is `ToolSpec`, and toolkit manifests contain a `tools` list. The architectural owner metadata and behavior nevertheless point to a registered operation catalog.

Confidence: high.

## 4. What exactly satisfies a capability today?

A capability is satisfied or resolved differently depending on the boundary:

1. Multiple registered implementations can satisfy one capability as candidates. `ToolRegistry.list_tools_for_capability()` returns every visible registered `ToolSpec` whose normalized `capabilities` contains the requested capability.
2. Provider recommendations can satisfy capability resolution as non-executable suggestions. `CapabilityCatalog` maps one capability to a list of recommendations, and `ToolRecommendationService` ranks them.
3. Handoff candidates can satisfy capability resolution as external/backend candidates when catalog recommendations include `backend_type` or `operation` metadata.
4. Future implementations can satisfy a capability after generation, validation, and registration. `seed_builder.registration.RegistrationService` loads a validated toolkit manifest and registers it through `ToolRegistry`, while builder design and validator code keep candidate artifacts separate from active registration.
5. Actual in-process execution satisfies only a selected registered implementation, not the capability label directly.

Therefore, the precise answer is: capability satisfaction today is a read-only resolution set until a `call_tool` path selects a registered `ToolSpec` implementation and policy allows execution.

Strongest contradiction: `CapabilityCatalogEntry` may mark a capability as known even when there are zero registered operations and no current executable implementation. Known capability is not the same as executable satisfaction.

Confidence: high.

## 5. Is execution coupled to capabilities or only to registered implementations?

Execution is coupled to registered implementations, not to capabilities directly.

`ToolExecutor.execute()` takes `tool_name` and `arguments`, not a capability. `ToolExecutionPolicyService` validates a named registered tool. `_execute_allowed_tool_call()` receives a `ToolSpec`, imports `tool.implementation`, and calls it. Capability fields are useful before execution for candidate discovery and model visibility, but the execution boundary is a registered implementation path.

Contradictory evidence: `ToolSpec` carries `capabilities`, and the model-visible context can expose tools with capability metadata. That creates indirect coupling between capability reasoning and available execution targets, but execution itself is name/spec/implementation based.

Confidence: high.

## 6. Would removing `ToolRegistry` remove execution, registration, capability reasoning, or only registration?

Removing `ToolRegistry` would directly remove registration/inventory of registered operation specs and the lookup source required by canonical execution. It would also remove the registry-backed capability-to-operation candidate query. In practical terms, canonical `ToolExecutor` execution would break because it depends on registry lookup and validation.

It would not remove all capability reasoning: `CapabilityCatalog`, provider recommendations, handoff candidates, and `ToolNeedService` creation could still exist conceptually without registered operations. But capability resolution would lose the `registered_operations` slice.

Therefore: remove `ToolRegistry` and you remove registration plus the registry dependency needed for execution, but not all capability/provider reasoning.

Strongest contradiction: since `ToolExecutor` requires a `ToolRegistry` in its constructor and policy service, removing the registry would remove the currently implemented execution path in practice, not merely a passive list.

Confidence: high.

## 7. Would removing `CapabilityCatalog` remove execution, registered operations, provider reasoning, capability reasoning, or another bounded responsibility?

Removing `CapabilityCatalog` would remove read-only capability metadata and provider/handoff recommendation reasoning. It would not remove `ToolRegistry` registration, `ToolSpec` registered operations, or `ToolExecutor` execution of named registered implementations.

It would weaken capability reasoning because `ToolNeedService.resolve_capability()` uses the catalog for `known_capability` and `handoff_candidates`, and `ToolRecommendationService` uses it as the source of recommendations. However, registry-backed `list_tools_for_capability()` could still return registered operation candidates for capability labels stored on `ToolSpec`.

Strongest contradiction: `ToolNeedService.resolve_capability()` requires a `CapabilityCatalog` argument, so the current complete capability-resolution payload expects catalog participation. Removing the catalog removes more than provider ranking; it removes the known-capability and handoff portions of the current resolution shape.

Confidence: high.

## 8. Vocabulary places that obscure already-separated responsibilities

| Vocabulary | Obscured separation | Evidence | Confidence |
| --- | --- | --- | --- |
| `tool` | Means registered operation spec in registry, execution target in executor, capability need in `ToolNeed`, and event prefix for execution lifecycle. | `ToolRegistry` stores `ToolSpec`; `ToolExecutor` emits `tool.call.*`; `ToolNeedService` emits `tool_need.*`; `request_tool` creates a capability need instead of executing. | High |
| `operation` | Means provider/handoff metadata in catalog recommendations and registered callable behavior in toolkit manifests/registry. | `CapabilityRecommendation.operation` is optional handoff metadata; `ToolSpec.implementation` is the executable callable path for registered specs. | High |
| `capability` | Means catalog key, need key, and metadata tag on registered specs, not a directly executable target. | `CapabilityCatalogEntry.capability`, `ToolNeed.capability`, and `ToolSpec.capabilities` all exist, but executor takes `tool_name`. | High |
| `provider` | Means recommendation/backend candidate, not an execution owner in the registered implementation path. | Catalog recommendation fields include `provider`, `backend_type`, and source/risk notes; `ToolExecutor` imports Python implementation paths instead of provider records. | High |
| `implementation` | Means concrete import path in `ToolSpec`, but can be conflated with tool, provider, or toolkit. | Manifest `implementation` points to a Python callable; registry registration stores the string; executor imports/calls it. | High |
| `toolkit` | Means packaging source of tools/specs and validation artifacts, not execution permission by itself. | `ToolRegistry.register_toolkit()` adds specs; builder registration registers only after validation; executor still validates status/input/policy before invoking. | High |

## 9. Proposed separations and strongest contradictory evidence

| Separation observed | Supporting evidence | Strongest contradictory evidence | Confidence |
| --- | --- | --- | --- |
| Capability is separate from registered operation. | Catalog entries can exist without registry entries; registered specs merely carry capability tags. | `ToolSpec.capabilities` embeds capability metadata inside the registered operation contract. | High |
| Registered operation is separate from execution. | Registry stores specs; executor separately validates policy and imports/calls implementation. | Executor cannot function without registry, making execution operationally dependent on registered specs. | High |
| Provider recommendation is separate from registered operation. | Recommendations live in `CapabilityCatalog` and are ranked read-only; registry stores `ToolSpec`. | Recommendations include an `operation` string, which can look like an operation identifier. | High |
| ToolNeed is separate from ToolSpec. | `ToolNeedService` creates durable capability needs and resolution metadata; it does not create a `ToolSpec`. | Both use `tool` vocabulary, and a need may resolve to registered operations. | High |
| Execution is separate from capability reasoning. | Executor takes `tool_name`/arguments and imports `ToolSpec.implementation`; catalog/recommendation services do not execute. | Capabilities influence which registered operations are discoverable before execution. | High |
| Toolkit packaging is separate from active execution authority. | Toolkit manifests are loaded into registry; validation/registration and executor policy are separate steps. | Once a toolkit is registered, its specs become visible candidates for execution subject to status/policy. | Medium-high |

## Files changed and LOC changed

Files changed:

- `docs/capability_operation_execution_reconciliation.md`

LOC changed at report creation time: +210 lines, -0 lines.

Tests run:

```bash
python -m pytest -q tests/test_tool_recommendations.py tests/test_runtime_tool_needs.py tests/test_tool_execution_policy.py
python -m pytest -q tests/test_tool_needs.py tests/test_capability_catalog.py tests/test_tool_execution_policy.py tests/test_tool_validation.py
```

The first pytest command did not run because `tests/test_runtime_tool_needs.py` does not exist. The second targeted pytest command passed with 23 tests.

## Recommended bounded implementation slice

No rename or architecture redesign is recommended. The smallest bounded implementation slice, if the team chooses to make the already-existing separation more observable later, would be characterization tests around the current boundaries:

- one test proving `request_tool` capability resolution can return `known_capability`, `provider_recommendations`, `handoff_candidates`, and `registered_operations` without executing a tool;
- one test proving a catalog recommendation with an `operation` string is not executable unless a matching `ToolSpec` is registered;
- one test proving `ToolExecutor.execute()` is driven by `tool_name`/`ToolSpec.implementation`, not by a capability string.

This is intentionally a test-only slice. It does not rename `tool`, introduce `OperationRegistry`, redesign runtime, or redesign execution.

## Final answers

Has the implementation already separated capability, operation, execution, and tool while retaining shared vocabulary?

Yes. The repository has implementation-backed separations for capability metadata/request resolution, registered operation inventory, provider/handoff recommendation, and registered implementation execution. The shared `tool` vocabulary obscures these bounded responsibilities but does not erase them.

What responsibility actually satisfies a capability?

Capability satisfaction is currently a resolution set: registered operation candidates from `ToolRegistry`, provider recommendations from `CapabilityCatalog`/`ToolRecommendationService`, handoff candidates from catalog metadata, and future validated toolkit implementations after registration. Actual executable satisfaction is only a selected registered `ToolSpec` implementation executed by `ToolExecutor` after validation and policy allow.

Is the repository already implementing a stronger architecture than its current words describe?

Yes, with high confidence. The implementation already behaves closer to capability -> candidate registered operation/provider/handoff -> policy-mediated registered implementation execution -> evidence than the single word `tool` suggests. The strongest caution is that the vocabulary and data model still intentionally retain `tool` names, so this report should be read as observational evidence of existing boundaries, not as authorization to rename or redesign them.
