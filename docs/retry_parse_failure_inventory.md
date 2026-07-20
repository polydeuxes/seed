# Retry and parse-failure behavior inventory

> **Stale/quarantined RuntimeLoop-era inventory.** Current architecture treats `Runtime` as canonical and `RuntimeLoop` as deprecated/experimental, not CLI/API/default behavior. References to legacy/old Runtime or RuntimeLoop migration are historical audit wording, not current-core guidance; current architecture treats Runtime as canonical.


This inventory is source-file based and records current behavior only. It does not propose or implement behavior changes.

## Recent delta

- Provider exceptions from `RuntimeLoop` decision providers no longer escape `RuntimeLoop.run()`: exceptions raised by `decision_provider.decide(decision_input)` are caught after context composition and context hashing. [`seed_runtime/runtime_loop.py:175-180`](../seed_runtime/runtime_loop.py#L175-L180)
- Provider failures are now observable as their own RuntimeLoop failure path rather than being conflated with malformed returned decisions. RuntimeLoop emits `runtime.decision.provider_failed`, then appends a `decision.recorded` journal entry with `outcome="provider_failed"`. [`seed_runtime/runtime_loop.py:181-201`](../seed_runtime/runtime_loop.py#L181-L201)
- The deterministic `RuntimeResult` for this path uses `decision_outcome="provider_failed"`, carries the provider error, and does not execute policy or tools. [`seed_runtime/runtime_loop.py:202-215`](../seed_runtime/runtime_loop.py#L202-L215)
- `RuntimeTrace` includes provider failure coverage as an error event: `runtime.decision.provider_failed` is classified with the other trace error events and can contribute provider-failure outcome/error details to trace summaries. [`seed_runtime/runtime_trace.py:146-159`](../seed_runtime/runtime_trace.py#L146-L159) [`seed_runtime/runtime_trace.py:179-200`](../seed_runtime/runtime_trace.py#L179-L200)
- This delta does not add retry parity. RuntimeLoop still makes a single provider attempt: malformed returned objects continue to use `runtime.decision.rejected` and `outcome="malformed_decision"`, while provider exceptions use `runtime.decision.provider_failed` and `outcome="provider_failed"`. [`seed_runtime/runtime_loop.py:177-256`](../seed_runtime/runtime_loop.py#L177-L256)

## 1. Canonical `Runtime` retry loop (called legacy in this historical inventory)


### Retry bound

- `Runtime.__init__()` accepts `max_decision_retries` with a default of `1` and stores `max(0, max_decision_retries)`, so negative values are coerced to zero retries. [`seed_runtime/runtime.py:37-66`](../seed_runtime/runtime.py#L37-L66)
- `handle_user_message()` runs `for attempt in range(self.max_decision_retries + 1)`, meaning the configured value is the number of retries after the first attempt, not the total attempt count. With the default, the model can be called twice. [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108)
- Every retry reuses the original composed `DecisionInputPacket` plus a replacement `retry_prompt`; state and visible operations/tools are not recomposed between attempts. The original input event remains the causation root for parse failures and proposed decisions. [`seed_runtime/runtime.py:71-88`](../seed_runtime/runtime.py#L71-L88)

### Parse failure handling

- The legacy runtime catches only `DecisionParseError` around `self.decision_producer.decide(retry_decision_input)`. Other provider/parser exceptions are not caught by this retry loop. [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108)
- On each caught parse failure, it appends `model.decision.parse_failed` with payload from `_decision_parse_failed_payload()`, actor `system`, session id, and causation id set to the original `input.user_message`. [`seed_runtime/runtime.py:89-97`](../seed_runtime/runtime.py#L89-L97)
- The parse-failure payload always includes `attempt` and `parse_error`; it may include `raw_failure_classification` when the exception object exposes `raw_failure_classification`, `failure_classification`, or `classification`. [`seed_runtime/runtime.py:232-249`](../seed_runtime/runtime.py#L232-L249)
- If parse failures are exhausted, `Runtime` returns `RuntimeResponse(kind="invalid_decision", message="Model decision failed parsing.", payload={"errors": [str(exc)]})` without a `model.decision.proposed` event for the failed parse attempt. [`seed_runtime/runtime.py:98-103`](../seed_runtime/runtime.py#L98-L103)
- If another attempt remains, the retry context contains `retry_prompt` with instruction text for strict JSON, `retry_number`, `max_retries`, `invalid_event_id`, `parse_error`, and optionally `raw_failure_classification`. [`seed_runtime/runtime.py:213-230`](../seed_runtime/runtime.py#L213-L230)

### Validation failure handling

- After a model returns a `Decision`, the runtime always records `model.decision.proposed` with `{"decision": to_plain(decision), "attempt": attempt}` before validation. [`seed_runtime/runtime.py:110-118`](../seed_runtime/runtime.py#L110-L118)
- `DecisionValidator.validate()` handles the legacy decision kinds `answer`, `ask_question`, `request_tool`, `call_tool`, `propose_state_patch`, and `refuse`, and reports `unsupported decision kind ...` for anything else that reaches it. [`seed_runtime/decisions.py:31-62`](../seed_runtime/decisions.py#L31-L62)
- Validation failures append `model.decision.invalid` with `errors` and `attempt`, actor `system`, and causation id set to the proposed-decision event id. [`seed_runtime/runtime.py:150-159`](../seed_runtime/runtime.py#L150-L159)
- If validation failures are exhausted, the final response is `RuntimeResponse(kind="invalid_decision", message="Model decision failed validation.", payload={"errors": validation_errors})`. [`seed_runtime/runtime.py:150-171`](../seed_runtime/runtime.py#L150-L171)
- If another attempt remains, `retry_prompt` contains a correction instruction, `retry_number`, `max_retries`, `invalid_event_id`, `validation_errors`, and `invalid_decision` serialized through `to_plain()`. [`seed_runtime/runtime.py:173-191`](../seed_runtime/runtime.py#L173-L191)

### Intent rejection handling

- Validation success is followed by `ToolIntentGuard.validate(text, decision, context.tools)` before routing. [`seed_runtime/runtime.py:118-126`](../seed_runtime/runtime.py#L118-L126)
- Intent failures append `model.decision.intent_rejected` with `errors` and `attempt`, actor `system`, and causation id set to the proposed-decision event id. [`seed_runtime/runtime.py:128-147`](../seed_runtime/runtime.py#L128-L147)
- If intent rejections are exhausted, the final response is `RuntimeResponse(kind="invalid_decision", message="Model decision failed intent validation.", payload={"errors": validation_errors})`. [`seed_runtime/runtime.py:128-171`](../seed_runtime/runtime.py#L128-L171)
- If another attempt remains, `retry_prompt` contains an intent-specific correction instruction, `retry_number`, `max_retries`, `rejected_event_id`, `intent_errors`, and `rejected_decision`. [`seed_runtime/runtime.py:193-211`](../seed_runtime/runtime.py#L193-L211)

### Retry context shape summary

The legacy retry prompt has three mutually exclusive shapes:

1. Parse failure: strict JSON instruction, `retry_number`, `max_retries`, `invalid_event_id`, `parse_error`, optional `raw_failure_classification`. [`seed_runtime/runtime.py:213-230`](../seed_runtime/runtime.py#L213-L230)
2. Schema/state validation failure: correction instruction, `retry_number`, `max_retries`, `invalid_event_id`, `validation_errors`, `invalid_decision`. [`seed_runtime/runtime.py:173-191`](../seed_runtime/runtime.py#L173-L191)
3. Intent rejection: intent-matching correction instruction, `retry_number`, `max_retries`, `rejected_event_id`, `intent_errors`, `rejected_decision`. [`seed_runtime/runtime.py:193-211`](../seed_runtime/runtime.py#L193-L211)

The legacy text prompt renderer appends `CORRECTION REQUIRED` when `DecisionInputPacket.retry_prompt` is present. [`seed_runtime/model_client.py:67-69`](../seed_runtime/model_client.py#L67-L69)

## 2. Parse-failure sources that can raise `DecisionParseError`

### Shared strict JSON decision parser

- `DecisionParseError` is defined in `seed_runtime.model_client` as a `ValueError` subclass. [`seed_runtime/model_client.py:322-323`](../seed_runtime/model_client.py#L322-L323)
- `StrictJSONDecisionParser.parse()` raises it for invalid JSON, non-object JSON, missing `kind`/`reason`, and unexpected fields, then constructs the legacy `Decision`. [`seed_runtime/model_client.py:326-355`](../seed_runtime/model_client.py#L326-L355)
- `ParsedDecisionProducer.decide()` calls `client.complete(context)` and then `parser.parse(...)`; parse errors propagate as `DecisionParseError` to canonical `Runtime` (called legacy in this historical audit), where they are retried. [`seed_runtime/model_client.py:358-368`](../seed_runtime/model_client.py#L358-L368)

### Local model clients

- `seed_runtime.model_clients.parse_decision_text()` raises `DecisionParseError` for wrapper whitespace/prose, code fences, invalid JSON, non-object JSON, missing `kind`/`reason`, unexpected fields, and model-construction validation failures. [`seed_runtime/model_clients.py:197-228`](../seed_runtime/model_clients.py#L197-L228)
- `_post_json()` raises `DecisionParseError` when the local HTTP provider response itself is not valid JSON or not an object. Network/HTTP exceptions from `request.urlopen()` are not converted here. [`seed_runtime/model_clients.py:238-254`](../seed_runtime/model_clients.py#L238-L254)
- `_extract_ollama_text()` raises `DecisionParseError` when an Ollama response lacks decision text. [`seed_runtime/model_clients.py:257-264`](../seed_runtime/model_clients.py#L257-L264)
- `_extract_openai_chat_text()` raises `DecisionParseError` when an OpenAI-compatible chat response lacks decision text. [`seed_runtime/model_clients.py:267-278`](../seed_runtime/model_clients.py#L267-L278)
- `OllamaDecisionProducer.decide()` and `LlamaCppDecisionProducer.decide()` both call `_post_json()`, extract text, and feed `parse_decision_text()`, so their parser/shape failures are retryable by canonical `Runtime` (called old in this historical audit); in `RuntimeLoop`, equivalent provider exceptions are observable as `provider_failed` but are not retried. [`seed_runtime/model_clients.py:101-110`](../seed_runtime/model_clients.py#L101-L110) [`seed_runtime/model_clients.py:162-168`](../seed_runtime/model_clients.py#L162-L168)

### Intent parser


## 3. `RuntimeLoop` malformed-decision and provider-failure behavior

Source files inspected: `seed_runtime/runtime_loop.py`, `seed_runtime/decision_journal.py`, `seed_runtime/runtime_trace.py`, and RuntimeLoop/trace tests in `tests/test_runtime_loop.py` and `tests/test_runtime_trace.py`.

### Accepted provider return types

- The `DecisionProvider` protocol declares `decide(context: RuntimeContext) -> Decision`, but `FakeDecisionProvider` accepts and returns `object` in tests. Runtime validation is therefore the effective boundary. [`seed_runtime/runtime_loop.py:80-103`](../seed_runtime/runtime_loop.py#L80-L103)
- `_validate_decision()` accepts only instances of `seed_runtime.runtime_loop.Decision`; dictionaries, legacy `seed_runtime.models.Decision`, strings, `None`, or other objects are malformed with `decision provider must return a runtime_loop.Decision`. [`seed_runtime/runtime_loop.py:763-765`](../seed_runtime/runtime_loop.py#L763-L765)
- `_safe_decision_payload()` serializes a RuntimeLoop `Decision`, passes dictionaries through `to_plain()`, and otherwise records only `{"type": type(proposed).__name__}`. [`seed_runtime/runtime_loop.py:797-809`](../seed_runtime/runtime_loop.py#L797-L809)

### Unsupported object and unsupported kind handling

- `RuntimeLoop.run()` appends `input.user_message`, projects state, composes context, hashes that context, catches exceptions from `self.decision_provider.decide(decision_input)`, and validates only successfully returned objects. [`seed_runtime/runtime_loop.py:158-216`](../seed_runtime/runtime_loop.py#L158-L216)
- If a returned object fails validation, RuntimeLoop appends `runtime.decision.rejected` with `{"error": validation_error, "decision": safe_payload}` and actor `system`; this rejection path is for malformed returned objects, not provider exceptions. [`seed_runtime/runtime_loop.py:216-224`](../seed_runtime/runtime_loop.py#L216-L224)
- Unsupported decision kinds are rejected with `decision kind must be 'answer', 'call_tool', or 'request_tool'`; this includes direct `ask_question`, `refuse`, and `propose_state_patch` values. [`seed_runtime/runtime_loop.py:763-767`](../seed_runtime/runtime_loop.py#L763-L767)

### Per-kind validation failures

- `answer` decisions require non-empty string `text`, may not include tool fields, and may not include `tool_need`. [`seed_runtime/runtime_loop.py:770-776`](../seed_runtime/runtime_loop.py#L770-L776)
- `call_tool` decisions require non-empty string `tool_name`, require `tool_args` to be a dict, may not include answer text, and may not include `tool_need`. [`seed_runtime/runtime_loop.py:777-785`](../seed_runtime/runtime_loop.py#L777-L785)
- `request_tool` decisions require a `tool_need` dict with non-empty string `name`, `summary`, and `capability`, and may not include `tool_name`, `tool_args`, or `text`. [`seed_runtime/runtime_loop.py:786-794`](../seed_runtime/runtime_loop.py#L786-L794)

### Malformed-decision journal outcome and final `RuntimeResult`

- Malformed decisions produce a `decision.recorded` event with `policy_allowed=False`, `outcome="malformed_decision"`, `error=validation_error`, `decision_kind`/`reason`/tool fields pulled from the safe payload where possible, and causation id set to the rejection event. [`seed_runtime/runtime_loop.py:217-242`](../seed_runtime/runtime_loop.py#L217-L242)
- `DecisionJournal.append_record()` writes a `decision.recorded` event containing a `DecisionRecord` with `decision_id`, `run_id`, `workspace_id`, `decision_kind`, `reason`, `context_hash`, selected operation/tool fields, `policy_allowed`, `outcome`, `error`, and `created_at`. [`seed_runtime/decision_journal.py:56-93`](../seed_runtime/decision_journal.py#L56-L93)
- The malformed-decision `RuntimeResult` has `decision_kind=None`, `response_text=None`, `policy_allowed=False`, `error=validation_error`, the recorded `decision_id`, the context hash, journal reason, and `decision_outcome="malformed_decision"`. [`seed_runtime/runtime_loop.py:243-256`](../seed_runtime/runtime_loop.py#L243-L256)
- `runtime_trace` classifies `runtime.decision.rejected` as an error event and can surface the journal error in trace summaries. [`seed_runtime/runtime_trace.py:146-159`](../seed_runtime/runtime_trace.py#L146-L159) [`seed_runtime/runtime_trace.py:179-200`](../seed_runtime/runtime_trace.py#L179-L200)

### Provider exception handling today

- `RuntimeLoop.run()` wraps `self.decision_provider.decide(decision_input)` in `try`/`except Exception`, so provider exceptions, including `DecisionParseError` from an intent parser/provider adapter, are caught after context composition and hashing. [`seed_runtime/runtime_loop.py:175-180`](../seed_runtime/runtime_loop.py#L175-L180)
- A caught provider exception appends `runtime.decision.provider_failed` with `error` and `exception_type`, actor `system`, and causation id set to the original `input.user_message`; it does not append `runtime.decision.rejected` because no returned decision was validated. [`seed_runtime/runtime_loop.py:181-188`](../seed_runtime/runtime_loop.py#L181-L188)
- RuntimeLoop then journals `decision.recorded` with `decision_kind=None`, empty `reason`, `policy_allowed=False`, `outcome="provider_failed"`, the context hash, the provider error, causation id set to `runtime.decision.provider_failed`, and correlation id set to the input event. [`seed_runtime/runtime_loop.py:189-201`](../seed_runtime/runtime_loop.py#L189-L201)
- The provider-failed `RuntimeResult` has `decision_kind=None`, `response_text=None`, `policy_allowed=False`, the provider error, the recorded decision id, context hash, empty decision reason, and `decision_outcome="provider_failed"`. [`seed_runtime/runtime_loop.py:202-215`](../seed_runtime/runtime_loop.py#L202-L215)
- `runtime_trace` classifies `runtime.decision.provider_failed` as an error event and can surface the provider failure outcome and error from the decision journal or error event. [`seed_runtime/runtime_trace.py:146-159`](../seed_runtime/runtime_trace.py#L146-L159) [`seed_runtime/runtime_trace.py:179-200`](../seed_runtime/runtime_trace.py#L179-L200)
- RuntimeLoop still catches tool handler exceptions later in `_run_tool_decision()`, journals `tool_failed`, and returns a `RuntimeResult`; provider failures now follow their own earlier `provider_failed` path instead of the tool-failure path. [`seed_runtime/runtime_loop.py:530-571`](../seed_runtime/runtime_loop.py#L530-L571)

## 4. Intent classifier behavior and risks

- In canonical `Runtime` (called old in this historical audit), a `DecisionParseError` raised by an intent-backed `DecisionProducer` is caught by the canonical Runtime retry loop. [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108)
- In `RuntimeLoop`, the same `DecisionParseError` is handled as a provider exception: it becomes `runtime.decision.provider_failed`, a `decision.recorded` journal entry with `outcome="provider_failed"`, and a `RuntimeResult` with `decision_outcome="provider_failed"`. [`seed_runtime/runtime_loop.py:177-215`](../seed_runtime/runtime_loop.py#L177-L215)
- The remaining risk is retry-loop parity, not provider exception observability: parser/model exceptions from the provider path are observed and converted into a deterministic result, but RuntimeLoop still does not create a retry prompt or make a second provider attempt after that failure. [`seed_runtime/runtime_loop.py:177-215`](../seed_runtime/runtime_loop.py#L177-L215) [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108)

## 5. Test coverage inventory

### Covered

- Old Runtime validation retry and retry-prompt shape are covered by `test_retries_invalid_first_decision_with_corrected_valid_decision`. [`tests/test_runtime_loop.py:171-210`](../tests/test_runtime_loop.py#L171-L210)
- Old Runtime exhausted validation retry and deterministic invalid-event payloads are covered by `test_invalid_first_and_second_decision_returns_invalid_decision` and `test_decision_and_invalid_decision_events_are_recorded_deterministically`. [`tests/test_runtime_loop.py:213-232`](../tests/test_runtime_loop.py#L213-L232) [`tests/test_runtime_loop.py:235-262`](../tests/test_runtime_loop.py#L235-L262)
- Old Runtime parse-failure retry with a corrected decision is covered by `test_retries_parse_failed_first_decision_with_valid_decision`. [`tests/test_runtime_loop.py:265-310`](../tests/test_runtime_loop.py#L265-L310)
- Old Runtime exhausted parse failures, final response shape, and `raw_failure_classification` propagation are covered by `test_exhausted_parse_failures_return_invalid_decision_and_record_events`. [`tests/test_runtime_loop.py:313-340`](../tests/test_runtime_loop.py#L313-L340)
- Old Runtime validation failures from tool validation are covered by `test_runtime_still_rejects_unknown_tool_during_decision_validation`. [`tests/test_tool_validation.py:132-152`](../tests/test_tool_validation.py#L132-L152)
- Old Runtime intent rejection without retry is covered by `test_install_docker_echo_rejected` and `test_echo_wrong_message_rejected`. [`tests/test_tool_intent.py:57-75`](../tests/test_tool_intent.py#L57-L75) [`tests/test_tool_intent.py:78-91`](../tests/test_tool_intent.py#L78-L91)
- Strict local decision parsing rejects wrappers/fences and missing `kind`/`reason` in `tests/test_model_clients.py`. [`tests/test_model_clients.py:115-139`](../tests/test_model_clients.py#L115-L139)
- Prompt inclusion of `retry_prompt` is covered by `test_serialize_decision_prompt_includes_retry_prompt_when_present`. [`tests/test_model_client.py:165-178`](../tests/test_model_client.py#L165-L178)
- RuntimeLoop rejection of unsupported returned objects is covered by `test_loop_malformed_decision_is_rejected_before_policy_and_tool_execution`. [`tests/test_runtime_loop.py:799-829`](../tests/test_runtime_loop.py#L799-L829)
- RuntimeLoop rejection of unsupported direct `ask_question`, `refuse`, and `propose_state_patch` decision kinds is covered by dedicated tests. [`tests/test_runtime_loop.py:934-958`](../tests/test_runtime_loop.py#L934-L958) [`tests/test_runtime_loop.py:961-985`](../tests/test_runtime_loop.py#L961-L985) [`tests/test_runtime_loop.py:988-1024`](../tests/test_runtime_loop.py#L988-L1024)
- RuntimeLoop per-kind malformed payload coverage exists for request-tool malformed payloads and forbidden fields. [`tests/test_runtime_loop.py:698-741`](../tests/test_runtime_loop.py#L698-L741)
- RuntimeLoop provider failure observability is covered by tests that assert provider exceptions return `provider_failed`, append `runtime.decision.provider_failed` plus `decision.recorded`, preserve causation/correlation ids, and avoid `runtime.decision.rejected`. [`tests/test_runtime_loop.py:448-508`](../tests/test_runtime_loop.py#L448-L508)
- Runtime trace support for provider failures is covered by a trace test that expects `provider_failed` summary/error fields and `runtime.decision.provider_failed` in error events. [`tests/test_runtime_trace.py:184-209`](../tests/test_runtime_trace.py#L184-L209)

### Missing or not directly covered

- No test appears to cover canonical Runtime (called old in this historical audit) intent rejection followed by a successful retry using `_decision_intent_retry_decision_input()`; existing intent tests configure `max_decision_retries=0`. [`tests/test_tool_intent.py:13-29`](../tests/test_tool_intent.py#L13-L29)
- No test appears to cover RuntimeLoop retry after a provider exception; existing provider exception coverage asserts the single-attempt `provider_failed` outcome. [`tests/test_runtime_loop.py:448-508`](../tests/test_runtime_loop.py#L448-L508)
- RuntimeLoop malformed-decision tests cover unsupported returned objects and unsupported kinds, but not every answer/call-tool field-validation branch in `_validate_decision()`.

## 6. Migration risk if canonical `Runtime` (called old in this historical audit) were removed before retry/parse parity

- The bounded retry loop would be lost for model parse failures. Old Runtime can convert a `DecisionParseError` into `model.decision.parse_failed`, a correction prompt, and a second model attempt; RuntimeLoop currently has no equivalent retry context or retry prompt. [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108) [`seed_runtime/runtime_loop.py:177-215`](../seed_runtime/runtime_loop.py#L177-L215)
- The bounded retry loop would also be lost for structured validation failures and intent rejections. RuntimeLoop rejects malformed returned objects once and does not ask the provider for a corrected decision. [`seed_runtime/runtime.py:150-171`](../seed_runtime/runtime.py#L150-L171) [`seed_runtime/runtime_loop.py:216-256`](../seed_runtime/runtime_loop.py#L216-L256)
- Parse-failure observability would differ but is no longer absent. Old Runtime records `model.decision.parse_failed` and may retry with a correction prompt; RuntimeLoop records provider/parser exceptions as `runtime.decision.provider_failed` plus `decision.recorded` and returns `decision_outcome="provider_failed"` without retrying. [`seed_runtime/runtime.py:89-103`](../seed_runtime/runtime.py#L89-L103) [`seed_runtime/runtime_loop.py:177-215`](../seed_runtime/runtime_loop.py#L177-L215)
- Final response semantics would still change for retryable failures. Old Runtime may return a successful response after a corrected retry, or `RuntimeResponse(kind="invalid_decision", ...)` only after exhausting parse/validation/intent failures; RuntimeLoop returns a single-attempt `RuntimeResult` for malformed returned objects or provider exceptions. [`seed_runtime/runtime.py:98-103`](../seed_runtime/runtime.py#L98-L103) [`seed_runtime/runtime.py:167-171`](../seed_runtime/runtime.py#L167-L171) [`seed_runtime/runtime_loop.py:202-256`](../seed_runtime/runtime_loop.py#L202-L256)
- The old retry prompt shapes and their model-facing correction instructions would no longer be exercised unless intentionally ported or replaced. [`seed_runtime/runtime.py:173-230`](../seed_runtime/runtime.py#L173-L230)

## 7. Options only for future work

These are possible future choices only; this inventory does not recommend or implement one.

1. Keep RuntimeLoop single-shot for provider exceptions and malformed returned decisions, documenting the difference as intentional now that provider exceptions return a deterministic `provider_failed` result.
2. Add a bounded retry loop to RuntimeLoop with RuntimeLoop-native retry context and event/journal semantics.
3. Extend provider exception handling with retry prompts for retryable provider/parser exceptions while preserving the deterministic `provider_failed` outcome after exhaustion.
4. Add a retry policy service shared by canonical Runtime (called legacy in this historical audit) and RuntimeLoop so retry bounds, retry prompts, and retryable error classes are configured outside either loop.
