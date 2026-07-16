# Constitutional Road Legitimacy Falsification Audit 001

## Scope and method

This audit reviewed live production roads that create, promote, select, authorize, execute, record, or consume constitutional artifacts, with special attention to the historically risky old tool district. The test was semantic sufficiency: whether the producer already possesses or consumes enough warrant for the exact destination assertion it makes. Older names, coarser representations, compatibility fields, and missing newer vocabulary were not treated as defects by themselves.

The audit did not add or modify a diagnostic, operational CLI flag, recordable output, event-ledger behavior, or runtime surface. It is a repository evidence report only.

## Evidence reviewed

Production implementation evidence:

- `seed_runtime/runtime.py`
- `seed_runtime/execution.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/tool_recommendations.py`
- `seed_runtime/registry.py`
- `seed_runtime/fact_extraction.py`
- `seed_runtime/models.py`

Selected preservation evidence:

- `tests/test_tool_recommendations.py`
- `tests/test_tool_intent.py`
- `tests/test_pending_actions.py`
- `tests/test_evaluations.py`
- `docs/recommendation_selection_boundary.md`
- `docs/observation_execution_transition_investigation.md`
- `implementation_execution_grammar_recovery_investigation.md`

Commands used:

```text
cat AGENTS.md
rg -n "class Tool|ToolExecutor|ToolRegistry|ToolRecommendation|ToolNeed|ExecutionPolicy|call_tool|request_tool|resolve_capability|extract" seed_runtime tests docs -S
sed -n '1,340p' seed_runtime/execution.py
sed -n '1,150p' seed_runtime/tool_needs.py
sed -n '1,140p' seed_runtime/tool_recommendations.py
sed -n '1,130p' seed_runtime/tool_validation.py
sed -n '1,130p' seed_runtime/decisions.py
sed -n '1,120p' seed_runtime/registry.py
rg -n "def _route|call_tool|request_tool|resolve_capability|ToolRecommendationService|ToolExecutor" seed_runtime/runtime.py -n -C 3
sed -n '80,220p' seed_runtime/runtime.py
sed -n '1,260p' seed_runtime/tool_execution_policy.py
sed -n '1,130p' seed_runtime/fact_extraction.py
sed -n '230,330p' seed_runtime/models.py
```

## Calibration result

The expected historical risk concentration did not currently reproduce as live production invalidity. The old tool district now shows mostly decompressed or explicitly bounded roads. The one old-tool-adjacent road that remains constitutionally suspect is not a live execution path; it is legacy/experimental `ExecutionAuthorization` metadata retained for historical projection compatibility and side-path tests. It is classified as **unsupported**, not invalid, because the model itself warns that it is non-core and secret-free, while this audit did not trace all historical projection consumers.

Result:

```text
invalid or compressed:
  none confirmed in live production roads

unsupported:
  legacy/experimental ExecutionAuthorization side-path metadata
  runtime call_tool decision origination / authority source after model decision authority excision

lawful:
  reviewed production tool recommendation, capability resolution, operation selection,
  policy authorization, invocation, realization, recording, and evidence extraction roads
```

This means the falsification audit did not find a smallest strongly evidenced destructive slice.

## Inventory of reviewed live production roads

| Road | Destination assertion | Required warrant | Producer warrant actually consumed or possessed | Downstream assumptions | Classification |
| --- | --- | --- | --- | --- | --- |
| Free-text user input -> runtime unsupported response | Free-text input cannot route Seed runtime movement through model-produced decisions. | Evidence that runtime has no Seed-owned free-text decision authority and records unsupported decision authority rather than routing. | `Runtime.handle_user_message()` records `runtime.decision_authority_unsupported` with reason that external model-produced Decisions cannot route movement, then returns `RuntimeResponse(kind="unsupported")`. | Callers may assume arbitrary operator prose is not converted into answer, request_tool, call_tool, state patch, or refusal movement. | lawful |
| Structured `request_tool` decision -> `ToolNeed` | A capability gap exists as a durable missing-capability request. | Valid `Decision(kind="request_tool")` carrying a tool_need name, summary, capability, and reason; current state check to avoid duplicate open needs. | `DecisionValidator._validate_tool_need()` checks fields; `ToolNeedService.create_from_decision()` slugifies name/capability, projects current state, returns matching open need if present, otherwise appends `tool_need.created`. | Consumers assume the artifact is a requested capability gap, not a provider adoption, operation selection, authorization, or execution. | lawful |
| `ToolNeed` -> ranked provider recommendations | Catalog recommendations are advisory candidates for satisfying the need. | Capability catalog entries and ranker output over projected state. | `ToolRecommendationService.recommend_for()` reads `CapabilityCatalog.recommend_for(tool_need)` and ranks against `State`; its docstring explicitly says it is read-only and does not create providers, register tools, or mutate state. | Runtime/request surfaces may display ranked possibilities without treating them as selected operations or authority. | lawful |
| `ToolNeed` -> read-only capability resolution payload | Known capability status, registered operation candidates, provider recommendations, and handoff candidates are descriptive metadata. | ToolNeed capability, capability catalog lookup, registry capability lookup, and already-supplied recommendation list. | `ToolNeedService.resolve_capability()` constructs `_CapabilityResolution`; docstring says catalog entries are non-executable suggestions, registered operation candidates come only from `ToolRegistry`, and the method does not execute, authorize, create pending actions, or mutate registry/catalog state. | Consumers may assume the payload is option reporting only. They may not assume selection, authorization, or execution. | lawful |
| Registry manifest -> registered operation catalog | A `ToolSpec` is registered inventory with name, schemas, policy action, implementation, status, visibility, risk class, and capabilities. | Manifest required keys, duplicate checks, capability normalization, in-memory registration. | `load_toolkit_manifest()` parses JSON, `toolkit_from_manifest()` requires toolkit/tool fields, `_RegisteredOperationIndex.add_toolkit()` rejects duplicate toolkit/tool names, and `ToolRegistry` exposes lookup/listing. | Consumers assume registry membership and callable implementation reference exist; they should not assume policy authorization or successful execution. | lawful |
| `call_tool` decision -> operation selection | The named registered operation exists and is the selected operation for this call. | A `call_tool` decision with a tool_name and argument object; registry/state lookup for exactly that name. | `DecisionValidator._validate_tool_call()` requires `tool_name` and delegates input validation. `ToolValidationService.select_operation()` resolves one named operation and explicitly says selection starts from an operation name, not catalog provider recommendations or handoff metadata. | Downstream policy/executor may assume there is one named operation candidate, not that it is authorized or already executed. | lawful for validation path; unsupported for decision origination source outside explicit tests/structured callers |
| Selected operation + arguments -> registered operation validation | The selected operation exists, has registered status, and accepts the input shape. | Registry existence, status check, input schema validation. | `ToolExecutionPolicyService._validate_registered_operation_call()` validates existence, status, and input schema before policy and says no policy state is projected and no policy decision is produced there. | Policy may assume operation contract validity only. | lawful |
| Validated registered operation -> policy authorization | The valid operation call may execute now if policy outcome is allow. | Validated operation plus projected state/scope evaluated by policy engine. | `_authorize_validated_operation()` rejects unvalidated operations, evaluates `policy_engine.evaluate(tool, state_provider(), scope=scope)`, and sets `allowed_to_execute` from policy outcome. | Executor may assume non-allow outcomes require block/approval/confirmation handling rather than invocation. | lawful |
| Policy non-allow -> blocked/approval result | The call is not executed and a policy/pending-action surface is recorded. | Policy decision outcome other than allow. | `ToolExecutor.execute()` branches on `policy.outcome != "allow"` to `_policy_denied()` instead of `_execute_allowed_tool_call()`. `_policy_denied()` appends policy events and returns blocked/approval results. | Consumers assume no registered operation implementation was invoked on this branch. | lawful |
| Policy allow -> invocation attempt | It is permissible to attempt running the registered implementation with supplied arguments. | Registered operation validation and policy allow result. | `ToolExecutor.execute()` only reaches `_execute_allowed_tool_call()` after validation succeeds and `policy.outcome == "allow"`. | Consumers may assume invocation was attempted, not necessarily successful. | lawful |
| Invocation attempt -> successful realization | The registered callable returned output that satisfies the output schema. | Callable import/reference, function return, output schema validation. | `_realize_registered_operation()` loads the registered callable, calls it, validates output schema, and raises on validation failure. `_execute_allowed_tool_call()` catches exceptions and records failure instead of completion. | Completion consumers may assume output schema validation passed. | lawful |
| Successful realization -> completed tool-call recording | A durable `tool.call.completed` event records a successful registered tool call and output. | Successful output from `_realize_registered_operation()`; no caught exception. | `_execute_allowed_tool_call()` calls `_record_completed_tool_call()` only after `_realize_registered_operation()` returns. `_record_completed_tool_call()` appends `tool.call.completed` with tool and output. | Fact extraction and projection consumers may assume the event represents successful, schema-validated tool output. | lawful |
| Failed invocation -> failed recording | A durable `tool.call.failed` event records execution failure. | Exception from `_realize_registered_operation()` or registration/input validation failure path. | `_execute_allowed_tool_call()` appends `tool.call.failed` when invocation raises; validation/status/input failures return failed results before invocation. | Consumers may assume failure is not success and should not trigger successful-output evidence extraction. | lawful |
| Completed tool-call recording -> post-execution evidence extraction | Tool output is preserved as evidence observation. | A completed tool-call or legacy tool.result event payload containing a tool name and output. | `_extract_post_execution_knowledge()` calls `FactExtractionService.observe_tool_result(completed_event)`. `observe_tool_result()` accepts only `tool.call.completed`/`tool.result`, requires tool/tool_name, and appends `evidence.observed` with source `tool:<name>`, kind `tool.output`, payload output, confidence 1.0. Its docstring says it records evidence only and intentionally does not infer facts unless a future explicit mapping is added. | Consumers may assume evidence exists for successful tool output; they may not assume output facts were inferred or promoted into cluster truth. | lawful |
| Approved pending action -> resumed execution | A pending action that is already approved may be executed once as its stored tool call. | Projected pending action exists with status `approved`; stored tool_name/arguments/scope; registry lookup. | `resume_approved_tool_call()` projects state, requires known pending action, requires status `approved`, requires tool from registry, executes stored call, and marks completed only on completed result. | Consumers may assume resumption is gated by prior approval state, not by provider recommendation or mere capability availability. | lawful |
| Legacy `ExecutionAuthorization` metadata -> authorization-like artifact | Secret-free grant metadata exists for a historical/side-path authorization. | Historical projection compatibility evidence and side-path tests; proof that it is not canonical runtime behavior. | Model docstring says `ExecutionAuthorization` is legacy/experimental, non-core authorization metadata, retained for historical projection compatibility and explicit side-path tests only, not canonical Runtime behavior, and must not be used to add internal execution lifecycle, credential prompts, retries, scheduling, or long-running job management. Field validators reject secret-bearing data. | Historical consumers may assume a grant metadata record exists; they must not assume canonical runtime authorization. Full consumer inventory was not completed here. | unsupported |

## Positive-control old tool roads

### Tool recommendation -> operation selection

Classification: **lawful in reviewed live production roads**.

Current evidence shows recommendation and selection are separated. `ToolRecommendationService.recommend_for()` uses catalog/ranker data and is read-only. Registered operation candidates in capability resolution come from `ToolRegistry.list_tools_for_capability(...)`, but `ToolValidationService.select_operation()` consumes an already named operation from a `call_tool` decision and explicitly excludes provider recommendation or handoff selection. Recommendation existence is therefore not used as operation selection warrant.

### Operation selection -> policy authorization

Classification: **lawful**.

`ToolExecutionPolicyService` preserves validation and policy as separately named boundaries. `_validate_registered_operation_call()` proves existence/status/input only and says it does not produce a policy decision. `_authorize_validated_operation()` requires that validated operation before evaluating policy with state and scope. Selection does not itself authorize execution.

### Policy authorization -> executable invocation

Classification: **lawful**.

`ToolExecutor.execute()` invokes `_execute_allowed_tool_call()` only after policy evaluation returns an allow outcome. Non-allow policy outcomes are routed to `_policy_denied()` and recorded as blocked/approval-required rather than invoked.

### Invocation -> successful operational realization

Classification: **lawful**.

The implementation distinguishes invocation attempt from success. `_realize_registered_operation()` can raise during load/call/output validation. `_execute_allowed_tool_call()` catches exceptions and records `tool.call.failed`; it records completion only after a returned output validates.

### Successful realization -> constitutional recording

Classification: **lawful**.

Completion recording is downstream of successful realization. `_record_completed_tool_call()` is called only after `_realize_registered_operation()` returns validated output. Failed invocation uses a separate failed event.

### Recording -> post-execution knowledge extraction

Classification: **lawful, with bounded assertion**.

The destination assertion is evidence observation, not fact truth. `FactExtractionService.observe_tool_result()` only accepts completed tool-result events, creates evidence with kind `tool.output`, and explicitly does not infer facts. This avoids silently turning diagnostic/tool output into cluster truth.

### Provider language -> registered constitutional operation

Classification: **lawful for registry manifest registration; unsupported for any unreviewed external provider adoption road**.

The live registry path registers only manifest-backed `ToolSpec` records after required-field and duplicate checks. Catalog/provider recommendation language is not registered by recommendation alone. No reviewed live production road showed provider language becoming a registered operation without manifest/toolkit registration. This audit did not trace every historical toolkit-generation or provider-adoption document, so any separate adoption road remains a local follow-up if it is still live.

### Capability availability -> authority to use capability

Classification: **lawful**.

Capability availability appears as read-only resolution metadata or registry inventory. Authority to execute is separately evaluated by `ToolExecutionPolicyService` and `PolicyGate` during registered operation execution. Availability does not bypass policy.

## Unsupported roads requiring narrow follow-up

### Runtime `call_tool` decision origination after model decision authority excision

Current road:

```text
structured caller/test/runtime branch supplies Decision(kind="call_tool")
-> DecisionValidator / ToolExecutor path
```

Destination assertion: the runtime has a selected operation request to validate and possibly execute.

Required warrant: a Seed-owned decision authority or explicit structured caller contract that is allowed to originate `call_tool` decisions.

Actual producer evidence: `Runtime.handle_user_message()` currently records that LLM/model-produced Decisions are external grammar and cannot route Seed runtime movement. Tests and internal helpers still construct `Decision(kind="call_tool")` directly. The execution path is lawful once the structured decision exists, but this audit did not establish the general production source that may originate that structured decision after free-text model authority was excised.

Classification: **unsupported**, not invalid. The unsupported area is origination authority, not operation validation, policy, execution, recording, or extraction.

Recommended follow-up: narrow audit of all production callers that can supply `Decision(kind="call_tool")` to `Runtime` or `ToolExecutor` outside tests, with special attention to whether they are explicit operator/automation contracts or remnants of excised model decision authority.

### Legacy/experimental `ExecutionAuthorization` side path

Current road:

```text
historical/side-path authorization metadata
-> ExecutionAuthorization model / projection compatibility
```

Destination assertion: a secret-free grant metadata record exists.

Required warrant: a concrete proposal/action-plan relationship, grant source, expiration, and proof that the record is not treated as canonical runtime authorization.

Actual producer evidence: the model is self-limiting and secret-free, but the audit did not complete a caller/export/projection/test inventory for all historical consumers.

Classification: **unsupported**, not invalid.

Recommended follow-up: narrow deletion-readiness audit for `ExecutionAuthorization` model, projection events, side-path tests, and documents. If no live production consumer relies on it, remove the compatibility artifact rather than decomposing it.

## Invalid roads

No reviewed live production road was classified as invalid.

Because no invalid road was confirmed, there are no entries for:

- callers preserving confirmed invalid roads;
- exports preserving confirmed invalid roads;
- diagnostics preserving confirmed invalid roads;
- tests preserving confirmed invalid roads;
- documents preserving confirmed invalid roads;
- destructive deletion candidates for confirmed invalid roads.

## Compressed roads

No reviewed live production road was classified as compressed.

The historical old-tool compression examples were reviewed as investigative leads. Current implementation evidence shows separate representation or explicit refusal at each critical seam:

- recommendation is advisory and read-only;
- operation selection consumes an already named registered operation;
- policy authorization requires validated operation and state/scope;
- invocation happens only on allow;
- realization and completion are separated by exception/output-schema handling;
- recording and evidence extraction are separate methods/services;
- extraction records evidence only, not inferred facts;
- capability availability is not execution authority.

## Destructive deletion candidates

None strongly evidenced by this audit.

The smallest possible future destructive slice, if locally confirmed by follow-up, is deletion of the legacy/experimental `ExecutionAuthorization` side path. This audit does not recommend deleting it yet because consumer evidence remains incomplete.

## Narrow follow-up audits

1. `call_tool` decision origination authority audit:
   - inventory non-test producers of `Decision(kind="call_tool")`;
   - distinguish explicit structured automation/operator contracts from excised model authority remnants;
   - stop at origination and do not reopen validated execution unless new evidence requires it.

2. `ExecutionAuthorization` deletion-readiness audit:
   - inventory model references, projection events, tests, docs, and exports;
   - determine whether any live production path still consumes it;
   - delete if compatibility-only and unused, otherwise preserve its non-core boundary explicitly.

3. Provider adoption / toolkit generation road audit, only if a live production caller is identified:
   - test whether provider language can become a registered operation without manifest/schema/policy/implementation warrant;
   - do not treat catalog recommendations as adoption by themselves.

## Conclusion

Only unsupported edges remain around decision origination and legacy authorization metadata. The old tool execution district itself did not glow under the semantic sufficiency test. Current implementation evidence supports the core road decomposition from advisory recommendation through registered selection, validation, policy, invocation, realization, recording, and evidence-only extraction.

Smallest strongly evidenced destructive slice: none.

Constitutional road legitimacy falsification audit complete.
