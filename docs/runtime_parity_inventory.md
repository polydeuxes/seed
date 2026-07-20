# Runtime Parity Inventory

> **Stale/quarantined RuntimeLoop-era parity inventory.** Current architecture treats `Runtime` as canonical and `RuntimeLoop` as deprecated/experimental, not CLI/API/default behavior. References to legacy/old Runtime, Runtime removal, or RuntimeLoop migration are historical audit wording, not current-core guidance.


This inventory compares `seed_runtime.runtime.Runtime` and `seed_runtime.runtime_loop.RuntimeLoop` from repository inspection only. File references point to the implementing code, tests, or call sites that demonstrate the behavior.


## Recent shared-service extraction delta

Recent Strategy B extractions moved duplicated infrastructure into shared services while preserving each runtime path's public behavior and event vocabulary. These are no longer parity gaps by themselves; the remaining gaps are semantic differences in routing, resume, retry, decision kinds, state mutation, and context shaping.

### `ToolRecommendationService`

- **Behavior moved:** capability-catalog lookup plus `RecommendationRanker` scoring for `ToolNeed` recommendations now lives in a read-only service that returns ranked recommendations without registering providers, mutating state, or emitting events. [`seed_runtime/tool_recommendations.py:11-35`](../seed_runtime/tool_recommendations.py#L11-L35)
- **Runtime path using it:** canonical `Runtime` constructs (called legacy in this historical inventory) `ToolRecommendationService` from its capability catalog and uses it when routing `request_tool`; `recommendation_ranker` remains exposed as a compatibility alias. [`seed_runtime/runtime.py:56-62`](../seed_runtime/runtime.py#L56-L62) [`seed_runtime/runtime.py:275-290`](../seed_runtime/runtime.py#L275-L290)
- **RuntimeLoop path using it:** `RuntimeLoop` accepts an optional `tool_recommendation_service`, defaults one when absent, projects current state for recommendation context, and includes the service-ranked recommendations in request-tool results. [`seed_runtime/runtime_loop.py:136-148`](../seed_runtime/runtime_loop.py#L136-L148) [`seed_runtime/runtime_loop.py:294-308`](../seed_runtime/runtime_loop.py#L294-L308)
- **Behavior still different:** Runtime still creates ToolNeeds / capability gaps through `ToolNeedService` and returns `RuntimeResponse` payloads; RuntimeLoop still appends its own `tool_need.created`, journals `tool_requested`, and returns `RuntimeResult`. Capability catalog ownership/injection also remains path-specific. [`seed_runtime/runtime.py:275-294`](../seed_runtime/runtime.py#L275-L294) [`seed_runtime/runtime_loop.py:274-322`](../seed_runtime/runtime_loop.py#L274-L322)
- **Files involved:** `seed_runtime/tool_recommendations.py`, `seed_runtime/runtime.py`, `seed_runtime/runtime_loop.py`, `seed_runtime/capability_catalog.py`, `seed_runtime/recommendation_ranker.py`, and recommendation tests in `tests/test_tool_recommendations.py`.

### `ToolValidationService`

- **Behavior moved:** registered-tool existence lookup, status validation, input schema validation, output schema validation, and legacy tool-input validation are centralized in `ToolValidationService`. [`seed_runtime/tool_validation.py:33-97`](../seed_runtime/tool_validation.py#L33-L97)
- **RuntimeLoop path using it:** `RuntimeLoop` accepts/defaults a `ToolValidationService`, passes it to `ToolExecutionPolicyService` for pre-policy checks, and uses it for post-handler output schema validation. [`seed_runtime/runtime_loop.py:136-154`](../seed_runtime/runtime_loop.py#L136-L154) [`seed_runtime/runtime_loop.py:369-394`](../seed_runtime/runtime_loop.py#L369-L394) [`seed_runtime/runtime_loop.py:533-548`](../seed_runtime/runtime_loop.py#L533-L548)
- **Behavior still different:** Runtime validation failures remain split across model-decision validation/retry and `tool.call.failed` events from `ToolExecutor`; RuntimeLoop records unknown/invalid tool validation through `runtime.tool.unknown` or `runtime.tool.invalid` and `decision.recorded`, with no retry loop. [`seed_runtime/runtime.py:123-166`](../seed_runtime/runtime.py#L123-L166) [`seed_runtime/execution.py:92-113`](../seed_runtime/execution.py#L92-L113) [`seed_runtime/runtime_loop.py:372-394`](../seed_runtime/runtime_loop.py#L372-L394)
- **Files involved:** `seed_runtime/tool_validation.py`, `seed_runtime/decisions.py`, `seed_runtime/execution.py`, `seed_runtime/runtime_loop.py`, and validation tests in `tests/test_tool_validation.py`.

### `ToolExecutionPolicyService`

- **Behavior moved:** the shared pre-execution sequence now resolves the tool, validates status, validates input schema, then evaluates policy with scope, returning the raw validation and policy result without executing tools, emitting events, creating pending actions, or collapsing non-allow outcomes. [`seed_runtime/tool_execution_policy.py:35-42`](../seed_runtime/tool_execution_policy.py#L35-L42) [`seed_runtime/tool_execution_policy.py:88-119`](../seed_runtime/tool_execution_policy.py#L88-L119)
- **Runtime path using it:** `ToolExecutor.execute()` calls `evaluate_with_state_factory()` so state projection remains lazy until after validation succeeds, then preserves the canonical Runtime behavior (called old in this historical inventory) for validation failures, policy blocks, confirmation/approval pending actions, allowed execution, and resume outside the service. [`seed_runtime/execution.py:56-73`](../seed_runtime/execution.py#L56-L73) [`seed_runtime/execution.py:86-128`](../seed_runtime/execution.py#L86-L128)
- **RuntimeLoop path using it:** `RuntimeLoop._run_tool_decision()` calls `evaluate()` against already projected state, then preserves RuntimeLoop-specific invalid-tool, non-allow policy, handler-missing, handler-failure, success, output-validation, and journaling behavior. [`seed_runtime/runtime_loop.py:360-410`](../seed_runtime/runtime_loop.py#L360-L410) [`seed_runtime/runtime_loop.py:448-548`](../seed_runtime/runtime_loop.py#L448-L548)
- **Behavior still different:** non-allow policy routing remains intentionally different: Runtime maps `block` to `tool.policy.blocked` and confirmation/approval to `tool.approval.required` plus pending actions, while RuntimeLoop maps every non-allow outcome to `runtime.policy.denied` and `policy_denied`. Approved-action resume remains Runtime-only. [`seed_runtime/execution.py:121-128`](../seed_runtime/execution.py#L121-L128) [`seed_runtime/execution.py:263-296`](../seed_runtime/execution.py#L263-L296) [`seed_runtime/runtime_loop.py:402-446`](../seed_runtime/runtime_loop.py#L402-L446)
- **Files involved:** `seed_runtime/tool_execution_policy.py`, `seed_runtime/tool_validation.py`, `seed_runtime/execution.py`, `seed_runtime/runtime_loop.py`, `seed_runtime/policy.py`, and policy-service tests in `tests/test_tool_execution_policy.py`.

## Runtime Systems

### `seed_runtime.runtime.Runtime`




**Event flow.** Runtime itself emits `input.user_message`, model decision proposal/invalid/parse-failed/intent-rejected events, response events, and state-patch rejection events. [`seed_runtime/runtime.py:66-72`](../seed_runtime/runtime.py#L66-L72) [`seed_runtime/runtime.py:85-92`](../seed_runtime/runtime.py#L85-L92) [`seed_runtime/runtime.py:105-112`](../seed_runtime/runtime.py#L105-L112) [`seed_runtime/runtime.py:125-132`](../seed_runtime/runtime.py#L125-L132) [`seed_runtime/runtime.py:147-154`](../seed_runtime/runtime.py#L147-L154) [`seed_runtime/runtime.py:251-268`](../seed_runtime/runtime.py#L251-L268) [`seed_runtime/runtime.py:317-324`](../seed_runtime/runtime.py#L317-L324) [`seed_runtime/runtime.py:340-347`](../seed_runtime/runtime.py#L340-L347) Tool-call and state-mutation sub-services emit additional events when Runtime delegates to them: `ToolExecutor` emits tool/policy/pending-action/evidence events, `ToolNeedService` emits `tool_need.created`, and `StatePatchService` emits state projection source events. [`seed_runtime/execution.py:69-127`](../seed_runtime/execution.py#L69-L127) [`seed_runtime/tool_needs.py:28-55`](../seed_runtime/tool_needs.py#L28-L55) [`seed_runtime/state_patches.py:70-145`](../seed_runtime/state_patches.py#L70-L145)

**Outputs.** Runtime returns `seed_runtime.models.RuntimeResponse`, a Pydantic model with `kind`, `message`, and `payload`. [`seed_runtime/models.py:318-321`](../seed_runtime/models.py#L318-L321) Its route outputs include `answer`, `question`, `tool_need`, `tool_result` or policy/tool failure kinds from `ToolExecutor`, `state_updated`, `invalid_state_patch`, `refusal`, `invalid_decision`, and `unsupported`. [`seed_runtime/runtime.py:247-350`](../seed_runtime/runtime.py#L247-L350)

### `seed_runtime.runtime_loop.RuntimeLoop`

**Entry point and responsibilities.** `RuntimeLoop` is described in its module docstring as a small deterministic coordinator that does not call LLMs, providers, shells, subprocesses, network clients, or generated toolkit operations; it coordinates `EventLedger`, `ProjectionStore`, `ToolRegistry`, `PolicyEngine`, and `DecisionProvider`. [`seed_runtime/runtime_loop.py:1-8`](../seed_runtime/runtime_loop.py#L1-L8) It is constructed with an `EventLedger`, optional `ProjectionStore`, `ToolRegistry`, optional `PolicyEngine`, `DecisionProvider`, optional tool handlers, and optional `StateProjector`; it creates a `DecisionJournal` and `FactExtractionService`. [`seed_runtime/runtime_loop.py:121-140`](../seed_runtime/runtime_loop.py#L121-L140) Its public entry point is `run(RuntimeInput)`. [`seed_runtime/runtime_loop.py:142-256`](../seed_runtime/runtime_loop.py#L142-L256)


**Decision flow.** RuntimeLoop appends `input.user_message`, uses `project_state_with_cache`, composes `RuntimeContext`, hashes the context, asks the provider for a decision, then validates it with `_validate_decision`. [`seed_runtime/runtime_loop.py:142-163`](../seed_runtime/runtime_loop.py#L142-L163) Malformed decisions append `runtime.decision.rejected`, write a `decision.recorded` journal record with `outcome="malformed_decision"`, and return an error-bearing `RuntimeResult`. [`seed_runtime/runtime_loop.py:163-200`](../seed_runtime/runtime_loop.py#L163-L200) Valid `answer` decisions append `assistant.answer` and journal `answered`; `request_tool` delegates to `_run_request_tool_decision`; every other valid kind is a `call_tool` and delegates to `_run_tool_decision`. [`seed_runtime/runtime_loop.py:202-256`](../seed_runtime/runtime_loop.py#L202-L256)

**Event flow.** RuntimeLoop directly emits input, assistant-answer, tool-need, tool-result/failure, unknown-tool, policy-denied, handler-missing, and malformed-decision events, and it appends `decision.recorded` journal events through `DecisionJournal`. [`seed_runtime/runtime_loop.py:144-150`](../seed_runtime/runtime_loop.py#L144-L150) [`seed_runtime/runtime_loop.py:164-186`](../seed_runtime/runtime_loop.py#L164-L186) [`seed_runtime/runtime_loop.py:203-222`](../seed_runtime/runtime_loop.py#L203-L222) [`seed_runtime/runtime_loop.py:270-289`](../seed_runtime/runtime_loop.py#L270-L289) [`seed_runtime/runtime_loop.py:338-361`](../seed_runtime/runtime_loop.py#L338-L361) [`seed_runtime/runtime_loop.py:380-408`](../seed_runtime/runtime_loop.py#L380-L408) [`seed_runtime/runtime_loop.py:427-450`](../seed_runtime/runtime_loop.py#L427-L450) [`seed_runtime/runtime_loop.py:471-493`](../seed_runtime/runtime_loop.py#L471-L493) [`seed_runtime/runtime_loop.py:510-533`](../seed_runtime/runtime_loop.py#L510-L533) Successful tool results also go through `FactExtractionService.observe_tool_result`, which can append `evidence.observed`. [`seed_runtime/runtime_loop.py:518-519`](../seed_runtime/runtime_loop.py#L518-L519) [`seed_runtime/fact_extraction.py:39-65`](../seed_runtime/fact_extraction.py#L39-L65)

**Outputs.** RuntimeLoop returns a frozen dataclass `RuntimeResult` containing workspace/run identifiers, decision kind, optional response text, appended event IDs, tool name/result, policy flag, error, decision ID, context hash, decision reason, and decision outcome. [`seed_runtime/runtime_loop.py:38-52`](../seed_runtime/runtime_loop.py#L38-L52) RuntimeLoop decision outputs are `answered`, `tool_requested`, `tool_unknown`, `policy_denied`, `tool_failed`, `tool_succeeded`, or `malformed_decision` as journal outcomes. [`seed_runtime/decision_journal.py:21-29`](../seed_runtime/decision_journal.py#L21-L29)

## Runtime Callers

| Runtime system | File | Function/class | Purpose |
| --- | --- | --- | --- |
| RuntimeLoop | `seed_runtime/api.py` | `SeedAPI.__init__`, `SeedAPI.post_user_message` | API shell stores a `RuntimeLoop` and turns `workspace_id`, `session_id`, and text into `RuntimeInput(... metadata={"session_id": session_id})` before calling `runtime.run`. [`seed_runtime/api.py:15-32`](../seed_runtime/api.py#L15-L32) |
| Runtime and RuntimeLoop | `scripts/seed_local.py` | Imports | CLI imports both `Runtime` and RuntimeLoop types. [`scripts/seed_local.py:98-104`](../scripts/seed_local.py#L98-L104) |
| RuntimeLoop | `scripts/seed_local.py` | `LocalSeedApp.run` | Normal local CLI path calls `self.runtime_loop.run(RuntimeInput(...))`, maps `RuntimeResult` to the existing CLI response shape, and returns response plus event ledger. [`scripts/seed_local.py:236-251`](../scripts/seed_local.py#L236-L251) |
| Runtime | `scripts/seed_local.py` | `LocalSeedApp._enrich_runtime_response` | Normal RuntimeLoop tool-need responses are enriched by using the canonical `Runtime` object (called legacy in this historical inventory)'s `recommendation_ranker` and `capability_catalog`. [`scripts/seed_local.py:253-288`](../scripts/seed_local.py#L253-L288) |
| Runtime | `scripts/seed_local.py` | `LocalSeedApp.run_legacy` | Legacy CLI path calls `self.runtime.handle_user_message(...)` and returns its response plus event ledger. [`scripts/seed_local.py:290-299`](../scripts/seed_local.py#L290-L299) |
| Runtime and RuntimeLoop | `scripts/seed_local.py` | `build_local_app` | Local app factory constructs both runtimes against the same ledger/projector/model and passes `EchoTool` as the RuntimeLoop handler. [`scripts/seed_local.py:641-695`](../scripts/seed_local.py#L641-L695) |
| Runtime / RuntimeLoop | `scripts/seed_local.py` | Shell and one-shot CLI dispatch | Historical note: this inventory described `--plan` / default routing before RuntimeLoop quarantine; current default guidance is canonical Runtime and RuntimeLoop is not the default path. [`scripts/seed_local.py:3450-3473`](../scripts/seed_local.py#L3450-L3473) [`scripts/seed_local.py:3961-3968`](../scripts/seed_local.py#L3961-L3968) |
| RuntimeLoop | `tests/test_api.py` | `build_api` and post tests | API tests instantiate `RuntimeLoop` and verify API `post_user_message` returns `RuntimeResult`; they also verify API migration does not import old runtime. [`tests/test_api.py:9-32`](../tests/test_api.py#L9-L32) [`tests/test_api.py:37-66`](../tests/test_api.py#L37-L66) [`tests/test_api.py:106-126`](../tests/test_api.py#L106-L126) |
| Runtime | `tests/test_runtime_loop.py` | first legacy test block | Legacy Runtime tests instantiate `Runtime` and call `handle_user_message` for answer/question/request_tool/call_tool/refuse/retry/parse-failure behaviors. [`tests/test_runtime_loop.py:10-49`](../tests/test_runtime_loop.py#L10-L49) [`tests/test_runtime_loop.py:54-97`](../tests/test_runtime_loop.py#L54-L97) [`tests/test_runtime_loop.py:171-326`](../tests/test_runtime_loop.py#L171-L326) |
| RuntimeLoop | `tests/test_runtime_loop.py` | second RuntimeLoop test block | RuntimeLoop tests instantiate `RuntimeLoop` via helpers and call `runtime.run(RuntimeInput(...))` for answer, context, tool, request-tool, policy, malformed decision, failure, projection, and boundary tests. [`tests/test_runtime_loop.py:346-397`](../tests/test_runtime_loop.py#L346-L397) [`tests/test_runtime_loop.py:423-847`](../tests/test_runtime_loop.py#L423-L847) |
| Runtime | `tests/test_capability_catalog.py` | runtime recommendation tests | Instantiates Runtime to verify request-tool responses include capability recommendations and unknown capabilities produce none. [`tests/test_capability_catalog.py:84-160`](../tests/test_capability_catalog.py#L84-L160) |
| Runtime | `tests/test_state_patches.py` | state-patch route test | Instantiates Runtime to verify `propose_state_patch` decisions apply state patch operations. [`tests/test_state_patches.py:140-174`](../tests/test_state_patches.py#L140-L174) |
| RuntimeLoop | `tests/test_runtime_trace.py` | trace fixture and tests | Instantiates RuntimeLoop to create runs that `RuntimeTraceReader` reconstructs without replay. [`tests/test_runtime_trace.py:4-82`](../tests/test_runtime_trace.py#L4-L82) [`tests/test_runtime_trace.py:100-252`](../tests/test_runtime_trace.py#L100-L252) |
| RuntimeLoop | `tests/test_cli_trace.py` | trace fixture and CLI trace tests | Instantiates RuntimeLoop runs for CLI `--trace-run`/`--why-run` tests. [`tests/test_cli_trace.py:9-70`](../tests/test_cli_trace.py#L9-L70) [`tests/test_cli_trace.py:84-238`](../tests/test_cli_trace.py#L84-L238) |
| Runtime / RuntimeLoop | `tests/test_seed_local_script.py` | CLI app tests | Historical tests in this inventory verified local app RuntimeLoop behavior; current docs must not present RuntimeLoop as default CLI behavior. [`tests/test_seed_local_script.py:28-116`](../tests/test_seed_local_script.py#L28-L116) |

## Context Systems





### `RuntimeContext`




## Decision Systems




### `seed_runtime.runtime_loop.Decision`


## Feature Parity Matrix

| Capability | Runtime | RuntimeLoop | Notes |
| --- | --- | --- | --- |
| User input event | Present | Present | Both append `input.user_message`; Runtime includes `session_id`, RuntimeLoop includes metadata and tracks the input event ID in `events_appended`. [`seed_runtime/runtime.py:66-72`](../seed_runtime/runtime.py#L66-L72) [`seed_runtime/runtime_loop.py:144-150`](../seed_runtime/runtime_loop.py#L144-L150) |
| State projection | Present | Present | Runtime calls `StateProjector.project`; RuntimeLoop calls `project_state_with_cache` with optional `ProjectionStore`. [`seed_runtime/runtime.py:73`](../seed_runtime/runtime.py#L73) [`seed_runtime/runtime_loop.py:153-158`](../seed_runtime/runtime_loop.py#L153-L158) |
| Projection cache | Missing | Present | RuntimeLoop uses `project_state_with_cache`; Runtime does not reference `ProjectionStore`. [`seed_runtime/runtime.py:8-20`](../seed_runtime/runtime.py#L8-L20) [`seed_runtime/runtime_loop.py:153-158`](../seed_runtime/runtime_loop.py#L153-L158) |
| Answer | Present | Present | Runtime routes to `response.answer` and `RuntimeResponse(kind="answer")`; RuntimeLoop routes to `assistant.answer`, journals `answered`, and returns `RuntimeResult(response_text=...)`. [`seed_runtime/runtime.py:250-259`](../seed_runtime/runtime.py#L250-L259) [`seed_runtime/runtime_loop.py:202-235`](../seed_runtime/runtime_loop.py#L202-L235) |
| Request tool / ToolNeed / capability-gap creation | Present | Present | Runtime delegates to `ToolNeedService.create_from_decision`, deduplicates open needs, and ranks recommendations; RuntimeLoop builds and appends a new `ToolNeed` directly and journals `tool_requested`. [`seed_runtime/runtime.py:270-294`](../seed_runtime/runtime.py#L270-L294) [`seed_runtime/tool_needs.py:28-55`](../seed_runtime/tool_needs.py#L28-L55) [`seed_runtime/runtime_loop.py:258-322`](../seed_runtime/runtime_loop.py#L258-L322) |
| Recommendation ranking | Present | Present | Both paths now use `ToolRecommendationService` for catalog lookup and ranking; Runtime still owns/loads the compatibility catalog while RuntimeLoop owns/injects its service separately, so response shape and tool-need event/journal behavior still differ. [`seed_runtime/tool_recommendations.py:11-35`](../seed_runtime/tool_recommendations.py#L11-L35) [`seed_runtime/runtime.py:56-62`](../seed_runtime/runtime.py#L56-L62) [`seed_runtime/runtime_loop.py:294-308`](../seed_runtime/runtime_loop.py#L294-L308) |
| Capability catalog | Present | Partial | Runtime owns/loads `CapabilityCatalog`; RuntimeLoop does not, although the CLI enrichment path reaches through `LocalSeedApp.runtime.capability_catalog`. [`seed_runtime/runtime.py:47-57`](../seed_runtime/runtime.py#L47-L57) [`scripts/seed_local.py:275-278`](../scripts/seed_local.py#L275-L278) |
| Call tool | Present | Present | Runtime delegates to `ToolExecutor.execute`; RuntimeLoop uses `ToolRegistry`, policy, and a local `tool_handlers` mapping. [`seed_runtime/runtime.py:295-307`](../seed_runtime/runtime.py#L295-L307) [`seed_runtime/runtime_loop.py:324-548`](../seed_runtime/runtime_loop.py#L324-L548) |
| Tool input schema validation | Present | Present | Both execution paths now validate executable tool calls through shared `ToolValidationService`/`ToolExecutionPolicyService`; Runtime also performs model-decision validation before routing and can retry, while RuntimeLoop returns invalid-tool results without retry. [`seed_runtime/tool_validation.py:61-88`](../seed_runtime/tool_validation.py#L61-L88) [`seed_runtime/tool_execution_policy.py:96-111`](../seed_runtime/tool_execution_policy.py#L96-L111) [`seed_runtime/decisions.py:79-85`](../seed_runtime/decisions.py#L79-L85) [`seed_runtime/runtime_loop.py:369-394`](../seed_runtime/runtime_loop.py#L369-L394) |
| Tool output schema validation | Present | Present | Both paths use `ToolValidationService.validate_output_schema`; Runtime emits legacy `tool.call.failed` on output validation failure, while RuntimeLoop emits/journals RuntimeLoop invalid-tool failure after handler output. [`seed_runtime/tool_validation.py:70-77`](../seed_runtime/tool_validation.py#L70-L77) [`seed_runtime/execution.py:195-209`](../seed_runtime/execution.py#L195-L209) [`seed_runtime/runtime_loop.py:533-548`](../seed_runtime/runtime_loop.py#L533-L548) |
| Tool status check | Present | Present | Both execution paths now check registered-tool status through shared `ToolExecutionPolicyService`; Runtime maps failures into legacy tool-call failure phases, while RuntimeLoop maps them through RuntimeLoop invalid-tool handling. [`seed_runtime/tool_execution_policy.py:96-109`](../seed_runtime/tool_execution_policy.py#L96-L109) [`seed_runtime/execution.py:92-113`](../seed_runtime/execution.py#L92-L113) [`seed_runtime/runtime_loop.py:369-394`](../seed_runtime/runtime_loop.py#L369-L394) |
| Policy evaluation | Present | Present | Both paths now share validation-before-policy sequencing through `ToolExecutionPolicyService`; Runtime evaluates lazily after validation via `evaluate_with_state_factory`, while RuntimeLoop evaluates against already projected state. Non-allow routing still diverges. [`seed_runtime/tool_execution_policy.py:71-119`](../seed_runtime/tool_execution_policy.py#L71-L119) [`seed_runtime/execution.py:86-128`](../seed_runtime/execution.py#L86-L128) [`seed_runtime/runtime_loop.py:369-446`](../seed_runtime/runtime_loop.py#L369-L446) |
| Policy confirmation/approval pending actions | Present | Missing | Shared policy evaluation returns raw `require_confirmation`/`require_approval` outcomes to both callers, but Runtime still creates approval-required events and pending actions while RuntimeLoop still treats every non-allow outcome as `runtime.policy.denied` and returns `policy_denied`. [`seed_runtime/tool_execution_policy.py:111-119`](../seed_runtime/tool_execution_policy.py#L111-L119) [`seed_runtime/execution.py:263-296`](../seed_runtime/execution.py#L263-L296) [`seed_runtime/runtime_loop.py:402-446`](../seed_runtime/runtime_loop.py#L402-L446) |
| Approved action resume | Present | Missing | `ToolExecutor.resume_approved_tool_call` exists on the Runtime tool path; RuntimeLoop has no resume entry point. [`seed_runtime/execution.py:129-169`](../seed_runtime/execution.py#L129-L169) [`seed_runtime/runtime_loop.py:118-142`](../seed_runtime/runtime_loop.py#L118-L142) |
| Retry handling | Present | Missing | Runtime retries validation, parse, and intent failures with retry prompts; RuntimeLoop returns immediately on malformed decision and has no retry loop. [`seed_runtime/runtime.py:81-166`](../seed_runtime/runtime.py#L81-L166) [`seed_runtime/runtime_loop.py:142-200`](../seed_runtime/runtime_loop.py#L142-L200) |
| State patch / state mutation decision | Present | Missing | Runtime routes `propose_state_patch` through `StatePatchService`; RuntimeLoop decision kind set excludes state patches. [`seed_runtime/runtime.py:308-338`](../seed_runtime/runtime.py#L308-L338) [`seed_runtime/runtime_loop.py:28`](../seed_runtime/runtime_loop.py#L28) |
| Decision journaling | Missing | Present | Runtime appends model proposal/invalid events but does not use `DecisionJournal`; RuntimeLoop journals every decision outcome. [`seed_runtime/runtime.py:105-112`](../seed_runtime/runtime.py#L105-L112) [`seed_runtime/runtime_loop.py:172-186`](../seed_runtime/runtime_loop.py#L172-L186) [`seed_runtime/decision_journal.py:48-93`](../seed_runtime/decision_journal.py#L48-L93) |
| Runtime trace | Missing | Present | `RuntimeTrace` is explicitly for RuntimeLoop runs and reconstructs `decision.recorded`, policy/tool/assistant events. [`seed_runtime/runtime_trace.py:1-45`](../seed_runtime/runtime_trace.py#L1-L45) [`03-runtime-loop.md:165-180`](../03-runtime-loop.md#L165-L180) |
| Evidence extraction from tool results | Present | Present | Runtime's `ToolExecutor` observes `tool.call.completed`; RuntimeLoop observes `tool.result`; `FactExtractionService` accepts both. [`seed_runtime/execution.py:228-238`](../seed_runtime/execution.py#L228-L238) [`seed_runtime/runtime_loop.py:510-519`](../seed_runtime/runtime_loop.py#L510-L519) [`seed_runtime/fact_extraction.py:39-65`](../seed_runtime/fact_extraction.py#L39-L65) |
| Direct registered Python operation execution | Present | Missing | Runtime's `ToolExecutor` loads registered operations via import path; RuntimeLoop only calls handlers explicitly supplied in `tool_handlers`. [`seed_runtime/execution.py:195-207`](../seed_runtime/execution.py#L195-L207) [`seed_runtime/runtime_loop.py:425-468`](../seed_runtime/runtime_loop.py#L425-L468) |
| Handler-missing handling | Partial | Present | Runtime fails earlier through registry/operation loading in `ToolExecutor`; RuntimeLoop has explicit `runtime.tool.handler_missing`. [`seed_runtime/execution.py:195-225`](../seed_runtime/execution.py#L195-L225) [`seed_runtime/runtime_loop.py:425-465`](../seed_runtime/runtime_loop.py#L425-L465) |
| Unknown operation/tool handling | Present | Present | Runtime validator rejects unknown operations/tools before route; RuntimeLoop emits `runtime.tool.unknown` and journals `tool_unknown`. [`seed_runtime/decisions.py:74-86`](../seed_runtime/decisions.py#L74-L86) [`seed_runtime/runtime_loop.py:335-376`](../seed_runtime/runtime_loop.py#L335-L376) |
| RuntimeResult with decision metadata | Missing | Present | Runtime returns `RuntimeResponse`; RuntimeLoop returns `RuntimeResult` with run/decision IDs, context hash, outcome, policy, and event IDs. [`seed_runtime/models.py:318-321`](../seed_runtime/models.py#L318-L321) [`seed_runtime/runtime_loop.py:38-52`](../seed_runtime/runtime_loop.py#L38-L52) |

## Event Comparison

### Input

| Event | Runtime | RuntimeLoop | Source |
| --- | --- | --- | --- |
| `input.user_message` | Present | Present | Runtime appends text with actor `user` and `session_id`; RuntimeLoop appends text plus metadata and actor `user`. [`seed_runtime/runtime.py:66-72`](../seed_runtime/runtime.py#L66-L72) [`seed_runtime/runtime_loop.py:144-150`](../seed_runtime/runtime_loop.py#L144-L150) |

### Decision

| Event | Runtime | RuntimeLoop | Source |
| --- | --- | --- | --- |
| `model.decision.invalid` | Present | Missing | Runtime records validator errors and attempt. [`seed_runtime/runtime.py:147-154`](../seed_runtime/runtime.py#L147-L154) |
| `model.decision.parse_failed` | Present | Missing | Runtime records parse failure and optional raw-failure classification. [`seed_runtime/runtime.py:85-92`](../seed_runtime/runtime.py#L85-L92) [`seed_runtime/runtime.py:227-245`](../seed_runtime/runtime.py#L227-L245) |
| `runtime.decision.rejected` | Missing | Present | RuntimeLoop records malformed provider decisions. [`seed_runtime/runtime_loop.py:163-171`](../seed_runtime/runtime_loop.py#L163-L171) |

### Policy

| Event | Runtime | RuntimeLoop | Source |
| --- | --- | --- | --- |
| `tool.policy.blocked` | Present | Missing | Runtime's `ToolExecutor` emits this for blocking policy outcomes. [`seed_runtime/execution.py:247-271`](../seed_runtime/execution.py#L247-L271) |
| `tool.approval.required` | Present | Missing | Runtime's `ToolExecutor` emits this for confirmation/approval outcomes. [`seed_runtime/execution.py:259-287`](../seed_runtime/execution.py#L259-L287) |
| `runtime.policy.denied` | Missing | Present | RuntimeLoop emits this for any non-allow policy outcome. [`seed_runtime/runtime_loop.py:378-392`](../seed_runtime/runtime_loop.py#L378-L392) |

### Tool

| Event | Runtime | RuntimeLoop | Source |
| --- | --- | --- | --- |
| `tool.call.started` | Present | Missing | Runtime's `ToolExecutor` emits this before loading/executing a registered tool. [`seed_runtime/execution.py:171-193`](../seed_runtime/execution.py#L171-L193) |
| `tool.call.completed` | Present | Missing | Runtime's `ToolExecutor` emits this after output schema validation. [`seed_runtime/execution.py:228-236`](../seed_runtime/execution.py#L228-L236) |
| `tool.call.failed` | Present | Missing | Runtime's `ToolExecutor` emits this for registration/input-validation/execution failures. [`seed_runtime/execution.py:209-226`](../seed_runtime/execution.py#L209-L226) [`seed_runtime/execution.py:298-325`](../seed_runtime/execution.py#L298-L325) |
| `runtime.tool.unknown` | Missing | Present | RuntimeLoop emits this when the tool registry cannot find the requested tool. [`seed_runtime/runtime_loop.py:335-345`](../seed_runtime/runtime_loop.py#L335-L345) |
| `runtime.tool.handler_missing` | Missing | Present | RuntimeLoop emits this when a registered tool has no supplied runtime handler. [`seed_runtime/runtime_loop.py:425-434`](../seed_runtime/runtime_loop.py#L425-L434) |
| `tool.failure` | Missing | Present | RuntimeLoop emits this when a supplied handler raises. [`seed_runtime/runtime_loop.py:467-478`](../seed_runtime/runtime_loop.py#L467-L478) |
| `tool.result` | Missing | Present | RuntimeLoop emits this when a handler returns successfully. [`seed_runtime/runtime_loop.py:510-517`](../seed_runtime/runtime_loop.py#L510-L517) |

### Response

| Event | Runtime | RuntimeLoop | Source |
| --- | --- | --- | --- |
| `response.answer` | Present | Missing | Runtime answer route. [`seed_runtime/runtime.py:250-259`](../seed_runtime/runtime.py#L250-L259) |
| `response.question` | Present | Missing | Runtime question route. [`seed_runtime/runtime.py:260-269`](../seed_runtime/runtime.py#L260-L269) |
| `response.refusal` | Present | Missing | Runtime refusal route. [`seed_runtime/runtime.py:339-348`](../seed_runtime/runtime.py#L339-L348) |
| `assistant.answer` | Missing | Present | RuntimeLoop answer route. [`seed_runtime/runtime_loop.py:202-210`](../seed_runtime/runtime_loop.py#L202-L210) |

### Journal and trace

| Event | Runtime | RuntimeLoop | Source |
| --- | --- | --- | --- |
| `decision.recorded` | Missing | Present | `DecisionJournal.event_kind` and `append_record` append the RuntimeLoop journal record. [`seed_runtime/decision_journal.py:48-93`](../seed_runtime/decision_journal.py#L48-L93) |
| Runtime trace read model | Missing | Present | `RuntimeTraceReader` reconstructs RuntimeLoop runs from ledger events without replay. [`seed_runtime/runtime_trace.py:1-45`](../seed_runtime/runtime_trace.py#L1-L45) |

### State and evidence

| Event | Runtime | RuntimeLoop | Source |
| --- | --- | --- | --- |
| `tool_need.created` | Present | Present | Runtime delegates to `ToolNeedService`; RuntimeLoop appends directly. [`seed_runtime/tool_needs.py:28-55`](../seed_runtime/tool_needs.py#L28-L55) [`seed_runtime/runtime_loop.py:270-277`](../seed_runtime/runtime_loop.py#L270-L277) |
| `tool_need.status_changed` | Present through service | Missing from RuntimeLoop | ToolNeed service can append status changes; RuntimeLoop does not call it. [`seed_runtime/tool_needs.py:57-66`](../seed_runtime/tool_needs.py#L57-L66) |
| `entity.upserted` | Present via state patch | Missing | Runtime state patch service supports entity upserts. [`seed_runtime/state_patches.py:87-96`](../seed_runtime/state_patches.py#L87-L96) |
| `evidence.observed` | Present | Present | Runtime state patch service and tool executor/fact extraction can append it; RuntimeLoop fact extraction can append it after `tool.result`. [`seed_runtime/state_patches.py:105-113`](../seed_runtime/state_patches.py#L105-L113) [`seed_runtime/fact_extraction.py:56-65`](../seed_runtime/fact_extraction.py#L56-L65) [`seed_runtime/runtime_loop.py:518-519`](../seed_runtime/runtime_loop.py#L518-L519) |
| `fact.observed` | Present via state patch | Missing | Runtime state patch service supports fact observations. [`seed_runtime/state_patches.py:119-128`](../seed_runtime/state_patches.py#L119-L128) |
| `goal.created` | Present via state patch | Missing | Runtime state patch service supports goal creation. [`seed_runtime/state_patches.py:135-144`](../seed_runtime/state_patches.py#L135-L144) |
| `state.patch.rejected` | Present | Missing | Runtime emits this when state patch validation fails. [`seed_runtime/runtime.py:317-324`](../seed_runtime/runtime.py#L317-L324) |

## Test Coverage

### Runtime tests

| Test file | Major behaviors covered |
| --- | --- |
| `tests/test_runtime_loop.py` | Legacy Runtime answer/question/request_tool/call_tool/refuse routes; runtime-loop MVP echo/tool-need projection behaviors using Runtime; invalid-decision retries; parse-failure retries and exhausted parse failures. [`tests/test_runtime_loop.py:45-326`](../tests/test_runtime_loop.py#L45-L326) |
| `tests/test_capability_catalog.py` | Capability catalog loading/recommendation plus Runtime request-tool responses with ranked or empty recommendations. [`tests/test_capability_catalog.py:15-164`](../tests/test_capability_catalog.py#L15-L164) |
| `tests/test_state_patches.py` | `StatePatchService` operations/rejections and Runtime `propose_state_patch` route to `state_updated`. [`tests/test_state_patches.py:29-174`](../tests/test_state_patches.py#L29-L174) |
| `tests/test_api.py` | Confirms API does not import canonical Runtime while the runtime module still exists for now. [`tests/test_api.py:106-126`](../tests/test_api.py#L106-L126) |
| `tests/test_seed_local_script.py` | Confirms local app still builds both paths and old runtime module remains available. [`tests/test_seed_local_script.py:28-116`](../tests/test_seed_local_script.py#L28-L116) |


### RuntimeLoop tests

| Test file | Major behaviors covered |
| --- | --- |
| `tests/test_api.py` | API `post_user_message` answer and request-tool paths return `RuntimeResult`. [`tests/test_api.py:37-66`](../tests/test_api.py#L37-L66) |
| `tests/test_runtime_trace.py` | Trace reconstruction for answer, tool success, unknown tool, policy denial, malformed decision, tool failure, event ordering, read-only behavior, and no provider/policy/tool calls during trace. [`tests/test_runtime_trace.py:76-252`](../tests/test_runtime_trace.py#L76-L252) |
| `tests/test_cli_trace.py` | CLI trace and why-run output for answer, tool success, policy denial, malformed decision, not-found trace, read-only trace commands, and no provider/policy/tool calls. [`tests/test_cli_trace.py:84-238`](../tests/test_cli_trace.py#L84-L238) |
| `tests/test_seed_local_script.py` | Normal CLI answer uses RuntimeLoop, deterministic echo uses fallback, operation output evidence appears in projected state, and missing capabilities/operations produce open ToolNeeds / capability gaps plus recommendation enrichment. [`tests/test_seed_local_script.py:50-103`](../tests/test_seed_local_script.py#L50-L103) |
| `tests/test_decision_journal.py` | Decision journal appends `decision.recorded` to EventLedger and context hashes are deterministic. [`tests/test_decision_journal.py:7-46`](../tests/test_decision_journal.py#L7-L46) |

RuntimeLoop behaviors observed in code with limited or no direct tests include the shared validation/status/output-schema paths now routed through `ToolValidationService` and `ToolExecutionPolicyService`, plus direct tests for policy outcomes other than denial-as-error remain absent because RuntimeLoop still treats every non-allow outcome as denied. [`seed_runtime/runtime_loop.py:369-394`](../seed_runtime/runtime_loop.py#L369-L394) [`seed_runtime/runtime_loop.py:402-446`](../seed_runtime/runtime_loop.py#L402-L446) [`seed_runtime/runtime_loop.py:533-548`](../seed_runtime/runtime_loop.py#L533-L548)

## Migration Risk Assessment

This section identifies risks only; it does not recommend migration, deletion, or refactoring.

The recent shared services mean these are no longer infrastructure gaps: shared recommendation lookup/ranking, shared tool validation, and shared validation-plus-policy-evaluation sequencing. The remaining migration risks are semantic/runtime-contract gaps: confirmation and approval pending actions, approved-action resume, retry and parse-failure handling, `state_patch`, and context budgeting. `ask_question`/`refuse` are no longer considered RuntimeLoop migration blockers because RuntimeLoop intentionally preserves clarify/refuse user-facing behavior through `answer` responses; distinct `question`/`refusal` response categories are canonical Runtime behavior; the “legacy Runtime” label in this inventory is stale.

### Current recommended next step

Continue Strategy B: do not delete `Runtime`, do not migrate the CLI yet, and choose next candidates based on semantic behavior gaps rather than remaining infrastructure duplication. Good next candidates are auditing `state_patch` behavior, auditing retry/parse-failure behavior, and deciding whether approval/resume should remain Runtime-only or become shared.

### Behaviors that would be lost if `Runtime` were deleted today

- Recommendation lookup/ranking is no longer a runtime-internal gap because both paths use `ToolRecommendationService`; deleting Runtime would still remove Runtime's compatibility catalog ownership, legacy response shape, and legacy request-tool route unless callers are updated. [`seed_runtime/tool_recommendations.py:11-35`](../seed_runtime/tool_recommendations.py#L11-L35) [`seed_runtime/runtime.py:56-62`](../seed_runtime/runtime.py#L56-L62) [`seed_runtime/runtime_loop.py:294-308`](../seed_runtime/runtime_loop.py#L294-L308)
- Operation implementation execution through registered operation import paths, pending-action creation for confirmation/approval, and approved-action resume would be lost from this runtime entry point; basic operation/tool existence/status/input validation and validation-before-policy sequencing are now shared and are no longer gaps by themselves. [`seed_runtime/tool_validation.py:33-97`](../seed_runtime/tool_validation.py#L33-L97) [`seed_runtime/tool_execution_policy.py:35-119`](../seed_runtime/tool_execution_policy.py#L35-L119) [`seed_runtime/execution.py:121-169`](../seed_runtime/execution.py#L121-L169) [`seed_runtime/execution.py:171-296`](../seed_runtime/execution.py#L171-L296)
- `propose_state_patch` routing to `StatePatchService` and its state mutation events would be lost from the runtime path. [`seed_runtime/runtime.py:308-338`](../seed_runtime/runtime.py#L308-L338) [`seed_runtime/state_patches.py:70-145`](../seed_runtime/state_patches.py#L70-L145)
- The CLI `--plan` path currently uses `LocalSeedApp.run_legacy`; deleting Runtime would break that path unless changed separately. [`scripts/seed_local.py:290-299`](../scripts/seed_local.py#L290-L299) [`scripts/seed_local.py:3450-3473`](../scripts/seed_local.py#L3450-L3473) [`scripts/seed_local.py:3961-3968`](../scripts/seed_local.py#L3961-L3968)

### Behaviors already covered by `RuntimeLoop`

- Default local CLI execution and API user-message posting already call RuntimeLoop. [`scripts/seed_local.py:236-251`](../scripts/seed_local.py#L236-L251) [`seed_runtime/api.py:15-32`](../seed_runtime/api.py#L15-L32)
- RuntimeLoop covers user input event recording, state projection through projection-cache plumbing, provider decision, answer responses, tool-need creation, registered-tool lookup, policy denial, supplied-handler execution, handler exception capture, successful tool results, evidence extraction, decision journaling, context hashes, and `RuntimeResult` output metadata. [`seed_runtime/runtime_loop.py:142-256`](../seed_runtime/runtime_loop.py#L142-L256) [`seed_runtime/runtime_loop.py:258-548`](../seed_runtime/runtime_loop.py#L258-L548)
- RuntimeLoop is covered by RuntimeTrace reconstruction and CLI trace/why-run commands. [`seed_runtime/runtime_trace.py:1-45`](../seed_runtime/runtime_trace.py#L1-L45) [`tests/test_runtime_trace.py:76-252`](../tests/test_runtime_trace.py#L76-L252) [`tests/test_cli_trace.py:84-238`](../tests/test_cli_trace.py#L84-L238)
- RuntimeLoop end-to-end clarify/refuse tests lock down that mapped clarify/refuse emits `assistant.answer`, journals `decision_kind="answer"`, and records `outcome="answered"`; dedicated direct-kind tests lock down rejection of unsupported `ask_question` and `refuse` RuntimeLoop decisions. [`tests/test_runtime_loop.py:428-489`](../tests/test_runtime_loop.py#L428-L489) [`tests/test_runtime_loop.py:934-979`](../tests/test_runtime_loop.py#L934-L979)
