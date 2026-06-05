# Retry and parse-failure behavior inventory

This inventory is source-file based and records current behavior only. It does not propose or implement behavior changes.

## 1. Legacy `Runtime` retry loop

Source files inspected: `seed_runtime/runtime.py`, `seed_runtime/model_client.py`, `seed_runtime/model_clients.py`, `seed_runtime/intent_classifier.py`, `seed_runtime/decisions.py`, and legacy-runtime tests in `tests/test_runtime_loop.py`, `tests/test_tool_validation.py`, `tests/test_tool_intent.py`, and `tests/test_model_client.py`.

### Retry bound

- `Runtime.__init__()` accepts `max_decision_retries` with a default of `1` and stores `max(0, max_decision_retries)`, so negative values are coerced to zero retries. [`seed_runtime/runtime.py:37-66`](../seed_runtime/runtime.py#L37-L66)
- `handle_user_message()` runs `for attempt in range(self.max_decision_retries + 1)`, meaning the configured value is the number of retries after the first attempt, not the total attempt count. With the default, the model can be called twice. [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108)
- Every retry reuses the original composed `ContextPacket` plus a replacement `retry_prompt`; state and visible tools are not recomposed between attempts. The original input event remains the causation root for parse failures and proposed decisions. [`seed_runtime/runtime.py:71-88`](../seed_runtime/runtime.py#L71-L88)

### Parse failure handling

- The legacy runtime catches only `DecisionParseError` around `self.model.decide(retry_context)`. Other provider/parser exceptions are not caught by this retry loop. [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108)
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

The legacy text prompt renderer appends `CORRECTION REQUIRED` when `ContextPacket.retry_prompt` is present. [`seed_runtime/model_client.py:67-69`](../seed_runtime/model_client.py#L67-L69)

## 2. Parse-failure sources that can raise `DecisionParseError`

### Shared strict JSON decision parser

- `DecisionParseError` is defined in `seed_runtime.model_client` as a `ValueError` subclass. [`seed_runtime/model_client.py:322-323`](../seed_runtime/model_client.py#L322-L323)
- `StrictJSONDecisionParser.parse()` raises it for invalid JSON, non-object JSON, missing `kind`/`reason`, and unexpected fields, then constructs the legacy `Decision`. [`seed_runtime/model_client.py:326-355`](../seed_runtime/model_client.py#L326-L355)
- `ParsedDecisionModel.decide()` calls `client.complete(context)` and then `parser.parse(...)`; parse errors propagate as `DecisionParseError` to legacy `Runtime`, where they are retried. [`seed_runtime/model_client.py:358-368`](../seed_runtime/model_client.py#L358-L368)

### Local model clients

- `seed_runtime.model_clients.parse_decision_text()` raises `DecisionParseError` for wrapper whitespace/prose, code fences, invalid JSON, non-object JSON, missing `kind`/`reason`, unexpected fields, and model-construction validation failures. [`seed_runtime/model_clients.py:197-228`](../seed_runtime/model_clients.py#L197-L228)
- `_post_json()` raises `DecisionParseError` when the local HTTP provider response itself is not valid JSON or not an object. Network/HTTP exceptions from `request.urlopen()` are not converted here. [`seed_runtime/model_clients.py:238-254`](../seed_runtime/model_clients.py#L238-L254)
- `_extract_ollama_text()` raises `DecisionParseError` when an Ollama response lacks decision text. [`seed_runtime/model_clients.py:257-264`](../seed_runtime/model_clients.py#L257-L264)
- `_extract_openai_chat_text()` raises `DecisionParseError` when an OpenAI-compatible chat response lacks decision text. [`seed_runtime/model_clients.py:267-278`](../seed_runtime/model_clients.py#L267-L278)
- `OllamaDecisionModel.decide()` and `LlamaCppDecisionModel.decide()` both call `_post_json()`, extract text, and feed `parse_decision_text()`, so their parser/shape failures are retryable by old `Runtime` but not by `RuntimeLoop` unless adapted through a provider that catches them. [`seed_runtime/model_clients.py:101-110`](../seed_runtime/model_clients.py#L101-L110) [`seed_runtime/model_clients.py:162-168`](../seed_runtime/model_clients.py#L162-L168)

### Intent parser

- `StrictJSONIntentParser.parse()` raises `DecisionParseError` for invalid JSON, non-object JSON, missing `intent`/`reason`, unexpected fields, non-object `arguments`, and `IntentClassification` validation failures. [`seed_runtime/intent_classifier.py:139-171`](../seed_runtime/intent_classifier.py#L139-L171)
- `TextIntentClassifier.classify()` directly returns `self.parser.parse(self.client.complete(context))`; it does not catch parser or transport exceptions. [`seed_runtime/intent_classifier.py:216-274`](../seed_runtime/intent_classifier.py#L216-L274)
- `IntentDecisionModel.decide()` invokes `self.classifier.classify(context)` only when deterministic fallback did not produce a classification and a classifier is configured; it does not catch `DecisionParseError`. [`seed_runtime/intent_classifier.py:477-493`](../seed_runtime/intent_classifier.py#L477-L493)

## 3. `RuntimeLoop` malformed-decision behavior

Source files inspected: `seed_runtime/runtime_loop.py`, `seed_runtime/decision_journal.py`, `seed_runtime/runtime_trace.py`, and RuntimeLoop tests in `tests/test_runtime_loop.py`.

### Accepted provider return types

- The `DecisionProvider` protocol declares `decide(context: RuntimeContext) -> Decision`, but `FakeDecisionProvider` accepts and returns `object` in tests. Runtime validation is therefore the effective boundary. [`seed_runtime/runtime_loop.py:80-103`](../seed_runtime/runtime_loop.py#L80-L103)
- `_validate_decision()` accepts only instances of `seed_runtime.runtime_loop.Decision`; dictionaries, legacy `seed_runtime.models.Decision`, strings, `None`, or other objects are malformed with `decision provider must return a runtime_loop.Decision`. [`seed_runtime/runtime_loop.py:725-727`](../seed_runtime/runtime_loop.py#L725-L727)
- `_safe_decision_payload()` serializes a RuntimeLoop `Decision`, passes dictionaries through `to_plain()`, and otherwise records only `{"type": type(proposed).__name__}`. [`seed_runtime/runtime_loop.py:759-771`](../seed_runtime/runtime_loop.py#L759-L771)

### Unsupported object and unsupported kind handling

- `RuntimeLoop.run()` appends `input.user_message`, projects state, composes context, hashes that context, calls `self.decision_provider.decide(context)`, then validates the returned object. [`seed_runtime/runtime_loop.py:158-178`](../seed_runtime/runtime_loop.py#L158-L178)
- If validation returns an error, RuntimeLoop appends `runtime.decision.rejected` with `{"error": validation_error, "decision": safe_payload}` and actor `system`. [`seed_runtime/runtime_loop.py:179-187`](../seed_runtime/runtime_loop.py#L179-L187)
- Unsupported decision kinds are rejected with `decision kind must be 'answer', 'call_tool', or 'request_tool'`; this includes direct `ask_question`, `refuse`, and `propose_state_patch` values. [`seed_runtime/runtime_loop.py:725-729`](../seed_runtime/runtime_loop.py#L725-L729)

### Per-kind validation failures

- `answer` decisions require non-empty string `text`, may not include tool fields, and may not include `tool_need`. [`seed_runtime/runtime_loop.py:732-738`](../seed_runtime/runtime_loop.py#L732-L738)
- `call_tool` decisions require non-empty string `tool_name`, require `tool_args` to be a dict, may not include answer text, and may not include `tool_need`. [`seed_runtime/runtime_loop.py:739-747`](../seed_runtime/runtime_loop.py#L739-L747)
- `request_tool` decisions require a `tool_need` dict with non-empty string `name`, `summary`, and `capability`, and may not include `tool_name`, `tool_args`, or `text`. [`seed_runtime/runtime_loop.py:748-756`](../seed_runtime/runtime_loop.py#L748-L756)

### Decision journal outcome and final `RuntimeResult`

- Malformed decisions produce a `decision.recorded` event with `policy_allowed=False`, `outcome="malformed_decision"`, `error=validation_error`, `decision_kind`/`reason`/tool fields pulled from the safe payload where possible, and causation id set to the rejection event. [`seed_runtime/runtime_loop.py:188-202`](../seed_runtime/runtime_loop.py#L188-L202)
- `DecisionJournal.append_record()` writes a `decision.recorded` event containing a `DecisionRecord` with `decision_id`, `run_id`, `workspace_id`, `decision_kind`, `reason`, `context_hash`, selected tool fields, `policy_allowed`, `outcome`, `error`, and `created_at`. [`seed_runtime/decision_journal.py:56-93`](../seed_runtime/decision_journal.py#L56-L93)
- The malformed-decision `RuntimeResult` has `decision_kind=None`, `response_text=None`, `policy_allowed=False`, `error=validation_error`, the recorded `decision_id`, the context hash, journal reason, and `decision_outcome="malformed_decision"`. [`seed_runtime/runtime_loop.py:203-216`](../seed_runtime/runtime_loop.py#L203-L216)
- `runtime_trace` classifies `runtime.decision.rejected` as an error event and can surface the journal error in trace summaries. [`seed_runtime/runtime_trace.py:146-158`](../seed_runtime/runtime_trace.py#L146-L158) [`seed_runtime/runtime_trace.py:178-200`](../seed_runtime/runtime_trace.py#L178-L200)

### Provider exception handling today

- There is no `try`/`except` around `self.decision_provider.decide(context)` in `RuntimeLoop.run()`. Provider exceptions, including `DecisionParseError` from an intent parser/provider adapter, escape after `input.user_message` is appended and before `runtime.decision.rejected` or `decision.recorded` can be emitted. [`seed_runtime/runtime_loop.py:158-178`](../seed_runtime/runtime_loop.py#L158-L178)
- RuntimeLoop catches tool handler exceptions later in `_run_tool_decision()`, journals `tool_failed`, and returns a `RuntimeResult`; this catch does not apply to provider exceptions. [`seed_runtime/runtime_loop.py:490-531`](../seed_runtime/runtime_loop.py#L490-L531)

## 4. Intent classifier behavior and risks

- `IntentDecisionModel` supports both legacy `ContextPacket` and RuntimeLoop `RuntimeContext`. The builder returns legacy `Decision` objects for `ContextPacket`, but RuntimeLoop `Decision` objects for `RuntimeContext`. [`seed_runtime/intent_classifier.py:35-37`](../seed_runtime/intent_classifier.py#L35-L37) [`seed_runtime/intent_classifier.py:411-463`](../seed_runtime/intent_classifier.py#L411-L463)
- Deterministic fallback paths do not parse JSON and therefore do not raise `DecisionParseError`. They can return direct echo, general informational answer, a missing-tool classification, or a default clarify classification when no classifier is configured. [`seed_runtime/intent_classifier.py:477-513`](../seed_runtime/intent_classifier.py#L477-L513)
- RuntimeContext intent parsing can raise when a configured `TextIntentClassifier` is needed and its transport/parser fails. `TextIntentClassifier.classify()` and `IntentDecisionModel.decide()` do not catch these exceptions. [`seed_runtime/intent_classifier.py:273-274`](../seed_runtime/intent_classifier.py#L273-L274) [`seed_runtime/intent_classifier.py:477-493`](../seed_runtime/intent_classifier.py#L477-L493)
- In old `Runtime`, a `DecisionParseError` raised by an intent-backed `DecisionModel` is caught by the legacy retry loop. [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108)
- In `RuntimeLoop`, the same `DecisionParseError` would be a provider exception and would not be converted into `runtime.decision.rejected`, a journal record, or a `RuntimeResult`. [`seed_runtime/runtime_loop.py:158-178`](../seed_runtime/runtime_loop.py#L158-L178)
- The primary risk is observability and control-flow divergence: malformed returned objects are journaled as `malformed_decision`, but parser/model exceptions from the provider path currently fail fast with only the input event appended. [`seed_runtime/runtime_loop.py:179-216`](../seed_runtime/runtime_loop.py#L179-L216)

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
- Intent parser failure behavior is covered for non-object `arguments`, invalid intent validation wrapping, and unexpected fields through `TextIntentClassifier`. [`tests/test_intent_classifier.py:338-381`](../tests/test_intent_classifier.py#L338-L381)

### Missing or not directly covered

- No test appears to cover old Runtime intent rejection followed by a successful retry using `_decision_intent_retry_context()`; existing intent tests configure `max_decision_retries=0`. [`tests/test_tool_intent.py:13-29`](../tests/test_tool_intent.py#L13-L29)
- No test appears to cover RuntimeLoop provider exceptions escaping from `decision_provider.decide()`; the nearby exception test covers tool handler exceptions after a valid provider decision, not provider failures. [`tests/test_runtime_loop.py:834-865`](../tests/test_runtime_loop.py#L834-L865)
- No test appears to assert that RuntimeLoop appends only `input.user_message` when the provider raises before validation.
- No test appears to exercise a RuntimeLoop provider backed by `IntentDecisionModel` with `TextIntentClassifier` raising `DecisionParseError` from `StrictJSONIntentParser`.
- RuntimeLoop malformed-decision tests cover unsupported objects and unsupported kinds, but not every answer/call-tool field-validation branch in `_validate_decision()`.

## 6. Migration risk if old `Runtime` were removed before retry/parse parity

- The bounded retry loop would be lost for model parse failures. Old Runtime can convert a `DecisionParseError` into `model.decision.parse_failed`, a correction prompt, and a second model attempt; RuntimeLoop currently has no equivalent retry context or retry prompt. [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108) [`seed_runtime/runtime_loop.py:158-178`](../seed_runtime/runtime_loop.py#L158-L178)
- The bounded retry loop would also be lost for structured validation failures and intent rejections. RuntimeLoop rejects malformed returned objects once and does not ask the provider for a corrected decision. [`seed_runtime/runtime.py:150-171`](../seed_runtime/runtime.py#L150-L171) [`seed_runtime/runtime_loop.py:179-216`](../seed_runtime/runtime_loop.py#L179-L216)
- Parse-failure observability would change. Old Runtime records `model.decision.parse_failed`; RuntimeLoop records malformed returned objects as `runtime.decision.rejected` plus `decision.recorded`, but provider exceptions currently escape before those events. [`seed_runtime/runtime.py:89-103`](../seed_runtime/runtime.py#L89-L103) [`seed_runtime/runtime_loop.py:179-216`](../seed_runtime/runtime_loop.py#L179-L216)
- Final response semantics would change. Old Runtime returns a `RuntimeResponse(kind="invalid_decision", ...)` after exhausted parse/validation/intent failures; RuntimeLoop returns a `RuntimeResult` only for returned malformed objects, and returns nothing when the provider raises. [`seed_runtime/runtime.py:98-103`](../seed_runtime/runtime.py#L98-L103) [`seed_runtime/runtime.py:167-171`](../seed_runtime/runtime.py#L167-L171) [`seed_runtime/runtime_loop.py:203-216`](../seed_runtime/runtime_loop.py#L203-L216)
- The old retry prompt shapes and their model-facing correction instructions would no longer be exercised unless intentionally ported or replaced. [`seed_runtime/runtime.py:173-230`](../seed_runtime/runtime.py#L173-L230)

## 7. Options only for future work

These are possible future choices only; this inventory does not recommend or implement one.

1. Keep RuntimeLoop fail-fast for provider exceptions and single-shot for malformed returned decisions, documenting the difference as intentional.
2. Add a bounded retry loop to RuntimeLoop with RuntimeLoop-native retry context and event/journal semantics.
3. Add provider exception handling only, converting provider/parser exceptions into a deterministic `RuntimeResult` and journal outcome without retrying.
4. Add a retry policy service shared by legacy Runtime and RuntimeLoop so retry bounds, retry prompts, and retryable error classes are configured outside either loop.
5. Adapt intent classification so parser/model failures are converted into malformed RuntimeLoop decisions instead of raising, leaving RuntimeLoop itself fail-fast for other provider exceptions.
