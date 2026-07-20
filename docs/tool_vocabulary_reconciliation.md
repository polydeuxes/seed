# Tool Vocabulary Reconciliation

## Scope


This report does not recommend renaming, runtime redesign, execution redesign, or tool redesign.

Repository authority wins over naming expectations.

## Commands executed

```text
pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' && git status --short
rg -n "class ToolExecutor|class ToolNeedService|class ToolValidationService|class ToolRegistry|def execute|def register|call_tool|request_tool|tool_intent|recommend" seed_runtime tests toolkits -S
sed -n '120,320p' seed_runtime/execution.py; sed -n '1,140p' seed_runtime/decisions.py; sed -n '1,130p' seed_runtime/models.py; sed -n '1,180p' seed_runtime/context.py; sed -n '1,170p' seed_runtime/capability_catalog.py; sed -n '1,170p' seed_runtime/tool_recommendations.py; sed -n '1,190p' seed_runtime/tool_execution_policy.py
sed -n '190,320p' seed_runtime/execution.py; sed -n '130,230p' seed_runtime/models.py; find toolkits -maxdepth 4 -type f | sort | sed -n '1,80p'; sed -n '1,140p' toolkits/core/echo/toolkit.yaml; sed -n '1,160p' toolkits/core/echo/operations.py; sed -n '1,200p' toolkits/generated/ssh_access/toolkit.yaml; sed -n '1,220p' toolkits/generated/ssh_access/operations.py
```

## Files inspected

- `seed_runtime/execution.py`
- `seed_runtime/registry.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/runtime.py`
- `seed_runtime/decisions.py`
- `seed_runtime/models.py`
- `seed_runtime/context.py`
- `seed_runtime/capability_catalog.py`
- `seed_runtime/tool_recommendations.py`
- `seed_runtime/tool_execution_policy.py`
- `toolkits/core/echo/toolkit.yaml`
- `toolkits/core/echo/operations.py`
- `toolkits/generated/ssh_access/toolkit.yaml`
- `toolkits/generated/ssh_access/operations.py`

## Files changed

- `docs/tool_vocabulary_reconciliation.md`

## LOC changed

- Added this report only.

## Tests run

No test suite was run. This was a documentation-only observational report and did not modify production code, tests, diagnostic inventory, shape-audit specs, runtime behavior, CLI flags, recordable output, or diagnostic/audit surfaces.

## Executive answer

`tool` is not one coherent architectural responsibility today. The repository uses shared `tool` vocabulary for several bounded implementation concepts:

1. a registered callable operation represented by `ToolSpec` in `ToolRegistry`;
2. an executable runtime target for `ToolExecutor` after validation and policy checks;
3. a missing capability request represented as `ToolNeed` and created by `request_tool`;
4. read-only capability resolution and provider/handoff recommendation metadata;
5. model-visible operation affordances in decision input;
6. deterministic intent validation for proposed `call_tool` decisions;
7. event vocabulary for calls, registration, policy outcomes, and needs.

The responsibility that actually owns execution is `ToolExecutor`, but only for registered implementation calls that pass validation and policy. It does not own registration, recommendation, capability reasoning, or provider/handoff metadata.

## Major occurrences and implementation-backed responsibilities

| Occurrence | Current responsibility | Supporting implementation | Strongest contradictory evidence |
| --- | --- | --- | --- |
| `ToolExecutor` | Executes registered implementations after lookup, status/input validation, policy evaluation, event recording, output validation, and fact extraction. | `ToolExecutor.__seed_arch__` declares owner `registered_tool_execution`; `execute()` delegates to `ToolExecutionPolicyService`; `_execute_allowed_tool_call()` loads and calls the registered implementation, appends `tool.call.started`, `tool.call.completed` or `tool.call.failed`, and validates output. | Its name says `ToolExecutor`, but it does not register tools, create needs, or rank recommendations. Non-allow policy outcomes create pending actions instead of executing. |
| `ToolRegistry` / tool registry | Catalogs registered operation specs from toolkit manifests and exposes model-visible and capability-filtered operations. | `ToolRegistry.__seed_arch__` declares owner `registered_operation_catalog`; `register_toolkit()` stores `Toolkit.tools`; `list_tools()` and `list_tools_for_capability()` return registered `ToolSpec` entries. | The concrete model is still named `ToolSpec`, and registry methods are `list_tools`; vocabulary could imply a single tool concept even though owner says registered-operation catalog. |
| Toolkit manifest `tools` entries | Declarative registered callable metadata: name, schemas, policy action, implementation import path, risk, visibility, capabilities. | `toolkit_from_manifest()` requires `name`, `summary`, `input_schema`, `output_schema`, `policy_action`, and `implementation`, then builds `ToolSpec`; manifests such as `echo` and `ssh_access` map names to import paths. | A manifest entry may be read-only, plan-only, or otherwise not a host binary; therefore “tool” here is not necessarily a command-line executable. |
| `ToolValidationService` | Validates tool lookup, registration status, input schema, and output schema against `ToolSpec` and `ToolRegistry`. | `validate_tool_exists()`, `validate_tool_status()`, `validate_input_schema()`, `validate_output_schema()`, and `validate_executable_tool_call()` operate on registered tool specs. | `validate_tool_exists()` can consult projected `state.tools` when a state is supplied, so validation is not purely registry-only in every context. |
| `ToolExecutionPolicyService` | Resolves, validates, and policy-checks a proposed tool call without executing or appending events. | Class docstring says it does not execute, append events, create pending actions, or collapse non-allow outcomes; `_evaluate()` checks existence, status, input schema, then policy. | It returns `allowed_to_execute`, so it is adjacent to execution and can look like part of execution ownership, but the implementation leaves actual invocation to callers. |
| `ToolNeedService` | Owns capability-gap creation and read-only capability resolution for `request_tool`. | `__seed_arch__` owner is `tool_need_capability_resolution`; `create_from_decision()` appends `tool_need.created`; `resolve_capability()` returns `known_capability`, `registered_operations`, `provider_recommendations`, and `handoff_candidates`. | The service name says `ToolNeed`, but the normalized field driving resolution is `capability`, not executable presence alone. |
| Tool recommendations | Read-only provider/handoff metadata for a capability need, ranked against state. | `CapabilityCatalog` maps capabilities to `CapabilityRecommendation`; `ToolRecommendationService.recommend_for()` ranks catalog recommendations. | Some recommendations can carry an `operation` string and `backend_type`, which may resemble executable operations; however they are not registered `ToolSpec` entries and are returned as handoff metadata. |
| Decision input `tools` | Model-visible operation affordances for the decision producer. | `DecisionInputComposer.compose()` serializes only `registry.list_tools(visible_only=True)` into `tools` with schemas, policy action, and risk. | Visible tools are context, not execution. Listing a tool does not execute it or imply capability verification. |
| Event names such as `tool.call.started`, `tool.call.completed`, `tool.call.failed`, `tool_need.created` | Ledger vocabulary for runtime call lifecycle and capability-need lifecycle. | `ToolExecutor` appends call events; `ToolNeedService` appends need events. | Shared event prefix `tool` spans different lifecycles: call execution and capability request creation. |

## Distinct meanings of `tool` today

### 1. Registered callable operation

A registered tool is a `ToolSpec` loaded from a toolkit manifest and stored in `ToolRegistry`. Its defining fields are schemas, policy action, implementation import path, status, visibility, risk class, and capabilities. The registry exposes it to the model and to capability lookup.

This is the strongest implementation meaning behind “tool” in `ToolRegistry`, `ToolValidationService`, `DecisionInputComposer`, and most `call_tool` paths.

### 2. Execution target

A tool becomes an execution target only after a `call_tool` decision supplies `tool_name` and `tool_arguments`, validation resolves the name to a registered `ToolSpec`, policy allows it, and `ToolExecutor` loads the implementation. Execution target is therefore narrower than registered tool.

### 3. Missing capability / desired future ability

A `ToolNeed` is not a callable. It is a recorded capability gap with normalized `name` and `capability`, summary, reason, and desired inputs/outputs. `request_tool` creates this need and returns metadata about possible satisfaction paths.

### 4. Provider or handoff recommendation metadata

Capability recommendations are not registered tools. They are catalog metadata that can identify providers, backend type, source, risk class, notes, or an operation label. They are ranked and reported without registering or executing anything.

### 5. Model-visible affordance

Decision input exposes visible registry entries as `tools`. This is not the full registry and not host availability. It is a bounded model-facing affordance list.

### 6. Intent-checked proposed invocation


## Evaluation of adjacent concepts

| Concept | Same as `tool` today? | Implementation-backed evaluation |
| --- | --- | --- |
| capability | No. A capability is normalized metadata used on `ToolNeed`, `ToolSpec.capabilities`, and catalog entries. It can exist without a registered callable and can have provider recommendations. |
| operation | Partly overlapping. Registry architecture labels registered tools as registered operations, and manifests map names to callable implementations. But catalog recommendation `operation` values and handoff plan operations are not automatically registered tools. |
| registered callable | Yes for the registry/execution meaning. A `ToolSpec` with an implementation import path is a registered callable candidate. It becomes executable only after status, schema, and policy checks. |
| execution target | Narrower than tool. Only a validated, policy-allowed registered tool in `ToolExecutor._execute_allowed_tool_call()` is the actual target. |
| host binary | No. Manifests point to Python import paths, and generated SSH operations explicitly avoid shell execution and network access. A host binary is not represented as a tool unless a registered implementation chooses to use one. |
| provider | No. Providers appear in capability recommendations and handoff metadata; they are not registered in `ToolRegistry` and are not invoked by `ToolExecutor`. |
| tool | Shared vocabulary, not one concept. It covers registered callable specs, execution targets, needs, visible affordances, validation subjects, recommendation context, and event labels. |
| tool invocation | A proposed or attempted `call_tool` with `tool_name` and `tool_arguments`. Actual invocation occurs only when `ToolExecutor` loads the implementation and calls it. |

## What `call_tool` means today

`call_tool` means: route a validated decision to the registered-tool execution boundary.

It does not inherently mean “run a host command.” The implementation loads a Python callable from a registered `ToolSpec.implementation` import path and calls it with `ToolContext` and schema-validated arguments. The registered callable might internally do anything allowed by its implementation and policy, but the checked-in examples include an echo operation and safe SSH stubs, not raw shell execution.

It does not inherently mean mutation. Policy can block or require approval, and some registered operations are read-only or plan-only. If policy allows and the callable mutates, mutation would be behavior of that registered implementation, not the semantic meaning of `call_tool` itself.

It does not mean “execute an observation” in general. A registered callable can produce observation-like output and `ToolExecutor` runs fact extraction on completed tool results, but observation is an outcome/consumer of the result, not the definition of `call_tool`.

## What `request_tool` means today

`request_tool` means: record or reuse a missing capability need and return read-only resolution metadata.

It most directly represents a missing or desired capability, not specifically a missing executable, missing authority, or missing provider. The payload requires `tool_need.capability`, and `ToolNeedService` normalizes and de-duplicates by name or capability. The runtime then ranks provider recommendations and resolves catalog/registry metadata.

Contradictory evidence: the response may include `registered_operations` for the same capability. Therefore a `request_tool` can coexist with registered operations and is better understood as capability-gap/resolution vocabulary than pure “missing executable.” It may also reflect missing authority or provider in specific catalog/ranker contexts, but those are recommendation details, not the core representation.

## Does `ToolExecutor` execute tools, operations, providers, or simply registered implementations?

`ToolExecutor` executes registered implementations. In repository vocabulary these are also called registered tools and registered operations.

The exact flow is:

1. resolve `tool_name` through validation/registry;
2. validate status and input schema;
3. evaluate policy;
4. append `tool.call.started`;
5. import and call the registered implementation path;
6. validate output schema;
7. append completion or failure;
8. observe completed tool results for fact extraction.

It does not execute providers. It does not execute catalog recommendations or handoff candidates. It does not own operation registration.

## Are host binaries considered tools?

Host binaries are not considered tools merely by existing on a host. The repository evidence supports “tool” as a repository-registered callable with metadata and validation. The checked-in toolkit manifests register Python import paths, not shell binary names. The safe SSH operations explicitly avoid sockets, shell commands, and live host inspection.

A host binary could only become involved if a registered implementation called it internally. That would not make every host binary a Seed tool; repository registration and validation are what make a callable visible and eligible for `call_tool` routing.

## What would removing `ToolExecutor` remove?

Removing `ToolExecutor` would remove the bounded runtime execution path for registered implementations: validation/policy-mediated invocation, call lifecycle event append, output validation, pending-action handling for non-allow policy outcomes, approved-call resumption, and fact extraction from completed tool results.

It would not remove:

- toolkit manifest parsing or registry storage;
- decision validation against registered schemas;
- `request_tool` capability need creation;
- capability catalog recommendations;
- recommendation ranking;
- model-visible tool listing in decision input;
- provider/handoff metadata.

Contradictory evidence: some of these surfaces import or refer to `ToolSpec` and “tool” vocabulary, so removing `ToolExecutor` would leave many “tool” concepts behind. That is exactly why execution ownership is bounded rather than global.

## Strongest contradictory evidence by interpretation

### Interpretation: `tool` means execution

Contradiction: `ToolNeedService`, `CapabilityCatalog`, `ToolRecommendationService`, and decision input all use tool vocabulary without executing anything. `request_tool` explicitly records needs and returns metadata.

### Interpretation: `tool` means capability

Contradiction: `ToolSpec` has concrete schemas, policy action, implementation path, visibility, and status. `ToolExecutor` imports and calls the implementation. That is more concrete than capability metadata.

### Interpretation: `tool` means provider

Contradiction: providers live in capability recommendations and handoff metadata, while `ToolRegistry` stores `ToolSpec` entries. `ToolExecutor` loads registered implementation import paths, not provider records.

### Interpretation: `tool` means host binary

Contradiction: toolkit manifests register Python implementation paths. The SSH toolkit explicitly returns stubs/plans and avoids shell/network behavior.

### Interpretation: `tool` means operation

Contradiction: this is the closest fit for registry/execution paths, but not all `operation` strings are registered tools. Capability recommendation `operation` is handoff metadata unless registered in `ToolRegistry`.

### Interpretation: `request_tool` means “missing executable”

Contradiction: it is keyed by capability and can report existing registered operations for that capability. It also reports provider recommendations and handoff candidates.

### Interpretation: `call_tool` means “perform a mutation”

Contradiction: checked-in tools include read-only or plan-only behavior. Policy may block or require approval. Mutation is implementation-specific, not the decision kind.

## Reconciliation

The repository currently demonstrates shared vocabulary covering several bounded responsibilities, not one architectural concept.

Current meanings of `tool` are:

- registered callable/operation metadata in `ToolRegistry` and toolkit manifests;
- execution target in `ToolExecutor` after validation and policy;
- capability need in `ToolNeed` and `request_tool`;
- model-visible affordance in decision input;
- validation subject in `ToolValidationService`;
- provider/handoff recommendation context in capability resolution;
- event vocabulary for call and need lifecycles.


## Recommended bounded implementation slice

No runtime, execution, registry, or vocabulary redesign is recommended by this observational report.

If an implementation slice is needed, the bounded slice is to preserve the current evidence with tests or documentation checks that distinguish these responsibilities:

- `call_tool` reaches `ToolExecutor` and `request_tool` does not;
- `request_tool` can return read-only capability resolution without calling `ToolExecutor`;
- provider recommendation `operation` metadata is not treated as a registered operation unless it appears in `ToolRegistry`;
- registered tool visibility comes from registry status and visibility, not host binary discovery.

This slice is preservation-only. It does not rename concepts or redesign execution.
