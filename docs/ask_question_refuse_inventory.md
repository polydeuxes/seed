# `ask_question` / `refuse` inventory

This inventory is source-file based and records current behavior only. It does not propose or implement behavior changes.

## 1. Models

### Legacy `seed_runtime.models.Decision`

- The shared legacy `DecisionKind` literal includes `answer`, `ask_question`, `call_tool`, `request_tool`, `propose_action_plan`, `propose_handoff_plan`, `propose_state_patch`, and `refuse`. [`seed_runtime/models.py:42-51`](../seed_runtime/models.py#L42-L51)
- `Decision` stores the common `kind` and required `reason` fields plus optional per-kind payload fields: `answer`, `question`, `tool_name`, `tool_arguments`, `tool_need`, `action_plan`, `handoff_plan`, and `state_patch`. [`seed_runtime/models.py:205-215`](../seed_runtime/models.py#L205-L215)
- `ask_question` uses `kind="ask_question"`, `reason`, and `question`. The validator requires `decision.question` to be truthy and reports `ask_question decisions require question` when missing or empty. [`seed_runtime/decisions.py:47-49`](../seed_runtime/decisions.py#L47-L49)
- `refuse` uses `kind="refuse"` and `reason`. There is no separate refusal-message field on the legacy model; the routed user-visible message is the same `reason`. The validator requires `decision.reason` to be truthy and reports `refuse decisions require reason` when missing or empty. [`seed_runtime/decisions.py:57-59`](../seed_runtime/decisions.py#L57-L59)
- The validator has explicit branches for `answer`, `ask_question`, `request_tool`, `call_tool`, `propose_state_patch`, and `refuse`; any other kind value that reaches the validator is reported as unsupported. [`seed_runtime/decisions.py:31-59`](../seed_runtime/decisions.py#L31-L59)

### `seed_runtime.runtime_loop.Decision`

- RuntimeLoop's local `DecisionKind` is only `Literal["answer", "call_tool", "request_tool"]`. [`seed_runtime/runtime_loop.py:32`](../seed_runtime/runtime_loop.py#L32)
- RuntimeLoop's `Decision` dataclass has `kind`, `text`, `tool_name`, `tool_args`, `tool_need`, and `reason`; it has no `question`, `answer`, or refusal-specific field. [`seed_runtime/runtime_loop.py:60-68`](../seed_runtime/runtime_loop.py#L60-L68)
- RuntimeLoop validation rejects any kind outside `answer`, `call_tool`, and `request_tool` with `decision kind must be 'answer', 'call_tool', or 'request_tool'`. [`seed_runtime/runtime_loop.py:725-729`](../seed_runtime/runtime_loop.py#L725-L729)
- Today, clarify/refuse semantics enter RuntimeLoop through intent classification and are represented as `answer` decisions with `text`, not distinct decision kinds. [`seed_runtime/intent_classifier.py:453-462`](../seed_runtime/intent_classifier.py#L453-L462)

## 2. Prompt / model-client behavior

### Legacy decision prompts

- `ContextComposer` exposes a legacy `decision_schema` whose kinds are `answer`, `ask_question`, `call_tool`, `request_tool`, and `refuse`. It does not include `propose_state_patch` in this composer-provided schema. [`seed_runtime/context.py:125-132`](../seed_runtime/context.py#L125-L132)
- `seed_runtime.model_client.render_decision_prompt` defaults to allowed kinds `answer`, `ask_question`, `call_tool`, `request_tool`, `propose_state_patch`, and `refuse` if the context does not provide a schema. [`seed_runtime/model_client.py:34-45`](../seed_runtime/model_client.py#L34-L45)
- The same prompt renderer includes allowed JSON shapes for `ask_question` as `{kind, reason, question}` and `refuse` as `{kind, reason}`. [`seed_runtime/model_client.py:195-221`](../seed_runtime/model_client.py#L195-L221)
- `StrictJSONDecisionParser` accepts `question` but has no refusal-specific field beyond `reason`; it rejects unexpected fields before constructing the legacy `Decision`. [`seed_runtime/model_client.py:338-355`](../seed_runtime/model_client.py#L338-L355)
- The local chat clients in `seed_runtime.model_clients` also expose an `ask_question` shape with `question` and a `refuse` shape with `reason`; their strict parser accepts `question` and `state_patch` but no refusal-specific payload. [`seed_runtime/model_clients.py:24-60`](../seed_runtime/model_clients.py#L24-L60)

### Intent classifier mapping

- The intent label set is `echo`, `answer`, `missing_tool`, `clarify`, and `refuse`, and the intent prompt tells models to return only that compact intent shape, not a runtime decision shape. [`seed_runtime/intent_classifier.py:35-37`](../seed_runtime/intent_classifier.py#L35-L37) [`seed_runtime/intent_classifier.py:280-315`](../seed_runtime/intent_classifier.py#L280-L315)
- For legacy `ContextPacket`, `clarify` builds `Decision(kind="ask_question", reason=..., question=...)`; the default question is `What would you like me to do?`. [`seed_runtime/intent_classifier.py:453-457`](../seed_runtime/intent_classifier.py#L453-L457)
- For legacy `ContextPacket`, `refuse` builds `Decision(kind="refuse", reason=...)`. If the classification has a `refusal` or `message` argument, that string is computed, but the legacy `Decision` has no field to carry it, so only `reason` survives the build. [`seed_runtime/intent_classifier.py:458-462`](../seed_runtime/intent_classifier.py#L458-L462)
- For `RuntimeContext`, both `clarify` and `refuse` build `RuntimeLoopDecision(kind="answer", text=...)`; clarify text is the question, and refuse text is `arguments.refusal`, `arguments.message`, or `reason`. [`seed_runtime/intent_classifier.py:453-462`](../seed_runtime/intent_classifier.py#L453-L462)
- If no deterministic fallback matches and no classifier is configured, `IntentDecisionModel` defaults to a `clarify` classification with `What would you like me to do?`. [`seed_runtime/intent_classifier.py:477-493`](../seed_runtime/intent_classifier.py#L477-L493)

## 3. Legacy Runtime behavior

### `ask_question`

- Old `Runtime.handle_user_message` appends `input.user_message`, projects state, composes a `ContextPacket`, and then loops through model decision attempts. Each parsed decision is appended as `model.decision.proposed` before validation. [`seed_runtime/runtime.py:68-118`](../seed_runtime/runtime.py#L68-L118)
- When an `ask_question` decision validates, `_route` appends `response.question` with payload `{"question": decision.question}` and returns `RuntimeResponse(kind="question", message=decision.question or "")`. [`seed_runtime/runtime.py:265-274`](../seed_runtime/runtime.py#L265-L274)
- If `question` is missing or empty, `DecisionValidator` returns `ask_question decisions require question`; Runtime appends `model.decision.invalid` with the errors and attempt number, retries until `max_decision_retries` is exhausted, and then returns `RuntimeResponse(kind="invalid_decision", message="Model decision failed validation.", payload={"errors": validation_errors})`. [`seed_runtime/decisions.py:47-49`](../seed_runtime/decisions.py#L47-L49) [`seed_runtime/runtime.py:150-170`](../seed_runtime/runtime.py#L150-L170)
- Parse failures are handled before decision validation: Runtime appends `model.decision.parse_failed`, retries with a JSON correction prompt if retries remain, and returns `RuntimeResponse(kind="invalid_decision", message="Model decision failed parsing.", payload={"errors": [str(exc)]})` when parse retries are exhausted. [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108) [`seed_runtime/runtime.py:213-230`](../seed_runtime/runtime.py#L213-L230)

### `refuse`

- When a `refuse` decision validates, `_route` appends `response.refusal` with payload `{"reason": decision.reason}` and returns `RuntimeResponse(kind="refusal", message=decision.reason)`. [`seed_runtime/runtime.py:342-351`](../seed_runtime/runtime.py#L342-L351)
- If `reason` is missing or empty, `DecisionValidator` returns `refuse decisions require reason`; Runtime handles it through the same `model.decision.invalid` retry loop and final `invalid_decision` response used for other validation failures. [`seed_runtime/decisions.py:57-59`](../seed_runtime/decisions.py#L57-L59) [`seed_runtime/runtime.py:150-170`](../seed_runtime/runtime.py#L150-L170)
- `ToolIntentGuard` is run after decision validation and before routing. It mainly guards `call_tool` decisions, so ask/refuse validation failures are the decision validator's responsibility. [`seed_runtime/runtime.py:118-147`](../seed_runtime/runtime.py#L118-L147)

## 4. RuntimeLoop behavior

- RuntimeLoop does not support `ask_question` or `refuse` as decision kinds; validation only accepts `answer`, `call_tool`, and `request_tool`. [`seed_runtime/runtime_loop.py:32`](../seed_runtime/runtime_loop.py#L32) [`seed_runtime/runtime_loop.py:725-757`](../seed_runtime/runtime_loop.py#L725-L757)
- RuntimeLoop receives the same `IntentDecisionModel` object in the local app as old Runtime, but the context type is `RuntimeContext`, so `clarify` and `refuse` are mapped to `RuntimeLoopDecision(kind="answer", text=...)`. [`scripts/seed_local.py:660-685`](../scripts/seed_local.py#L660-L685) [`seed_runtime/intent_classifier.py:453-462`](../seed_runtime/intent_classifier.py#L453-L462)
- A mapped clarify/refuse answer appends `assistant.answer` with payload `{"text": decision.text, "reason": decision.reason}`, appends a decision journal record with `decision_kind="answer"` and `outcome="answered"`, and returns `RuntimeResult(decision_kind="answer", response_text=decision.text, policy_allowed=True, decision_outcome="answered", ...)`. [`seed_runtime/runtime_loop.py:218-251`](../seed_runtime/runtime_loop.py#L218-L251)
- A provider-returned unsupported kind such as `ask_question` or `refuse` is rejected before routing: RuntimeLoop appends `runtime.decision.rejected`, records a decision journal entry with `outcome="malformed_decision"`, and returns `RuntimeResult(decision_kind=None, response_text=None, policy_allowed=False, error=..., decision_outcome="malformed_decision", ...)`. [`seed_runtime/runtime_loop.py:177-216`](../seed_runtime/runtime_loop.py#L177-L216)
- RuntimeLoop has no retry loop or parse-failure retry path; a malformed provider return produces a single rejection and a malformed-decision result. [`seed_runtime/runtime_loop.py:177-216`](../seed_runtime/runtime_loop.py#L177-L216)

## 5. CLI/API behavior

- `build_local_app` constructs both old `Runtime` and `RuntimeLoop`, sharing the same `IntentDecisionModel`; the default `LocalSeedApp.run` path calls `RuntimeLoop.run`, while `LocalSeedApp.run_legacy` calls old `Runtime.handle_user_message`. [`scripts/seed_local.py:641-695`](../scripts/seed_local.py#L641-L695) [`scripts/seed_local.py:236-299`](../scripts/seed_local.py#L236-L299)
- The CLI uses the RuntimeLoop path by default and switches to `run_legacy` when `--plan` is set. [`scripts/seed_local.py:3468-3473`](../scripts/seed_local.py#L3468-L3473) [`scripts/seed_local.py:3961-3968`](../scripts/seed_local.py#L3961-L3968)
- Old Runtime `ask_question`, if reached through `run_legacy`, serializes as `{"kind": "question", "message": <question>, "payload": ...}` because `RuntimeResponse(kind="question", message=...)` is converted with `to_plain`. [`seed_runtime/runtime.py:265-274`](../seed_runtime/runtime.py#L265-L274) [`scripts/seed_local.py:290-299`](../scripts/seed_local.py#L290-L299)
- Old Runtime `refuse`, if reached through `run_legacy`, serializes as `{"kind": "refusal", "message": <reason>, "payload": ...}`. [`seed_runtime/runtime.py:342-351`](../seed_runtime/runtime.py#L342-L351) [`scripts/seed_local.py:290-299`](../scripts/seed_local.py#L290-L299)
- RuntimeLoop mapped clarify/refuse results pass through `runtime_result_response` as ordinary `{"kind": "answer", "message": result.response_text, "payload": {"decision_kind": "answer", ...}}`; there is no CLI-visible `question` or `refusal` kind on that path. [`scripts/seed_local.py:169-220`](../scripts/seed_local.py#L169-L220)
- `SeedAPI` wraps RuntimeLoop directly and returns the `RuntimeResult` from `runtime.run`; therefore mapped clarify/refuse API responses have `decision_kind="answer"` and `response_text=<question or refusal text>`, while unsupported ask/refuse provider decisions return a malformed-decision `RuntimeResult`. [`seed_runtime/api.py:15-32`](../seed_runtime/api.py#L15-L32) [`seed_runtime/runtime_loop.py:177-251`](../seed_runtime/runtime_loop.py#L177-L251)

## 6. Test coverage

### Covered today

- Old Runtime ask-question route: `tests/test_runtime_loop.py::test_routes_question` verifies `Decision(kind="ask_question", question="Which host?")` returns response kind `question`. [`tests/test_runtime_loop.py:54-59`](../tests/test_runtime_loop.py#L54-L59)
- Old Runtime refusal route: `tests/test_runtime_loop.py::test_routes_refuse` verifies response kind `refusal`, response message `unsafe request`, and events `input.user_message`, `model.decision.proposed`, `response.refusal`. [`tests/test_runtime_loop.py:92-105`](../tests/test_runtime_loop.py#L92-L105)
- Old decision validation: `tests/test_decisions.py::test_ask_question_requires_question` and `tests/test_decisions.py::test_refuse_requires_reason` cover the required question/reason validation errors. [`tests/test_decisions.py:18-27`](../tests/test_decisions.py#L18-L27) [`tests/test_decisions.py:118-125`](../tests/test_decisions.py#L118-L125)
- Old Runtime invalid-decision retry behavior includes missing-answer followed by missing-question and checks final invalid-decision payload plus deterministic invalid-event payloads. [`tests/test_runtime_loop.py:213-262`](../tests/test_runtime_loop.py#L213-L262)
- Intent classifier `clarify` mapping for legacy `ContextPacket` is covered by `test_clarify_intent_asks_question_for_unknown_vague_input`. [`tests/test_intent_classifier.py:230-241`](../tests/test_intent_classifier.py#L230-L241)
- Intent prompt coverage verifies that the prompt exposes the compact intent labels including `clarify` and `refuse` and does not expose decision `kind` shapes. [`tests/test_intent_classifier.py:244-255`](../tests/test_intent_classifier.py#L244-L255)
- RuntimeContext mapping is covered for `echo`, `answer`, and `missing_tool`; these tests prove the builder switches to `RuntimeLoopDecision` for RuntimeLoop contexts, but they do not cover RuntimeContext `clarify` or `refuse`. [`tests/test_intent_classifier.py:444-507`](../tests/test_intent_classifier.py#L444-L507)
- RuntimeLoop unsupported-kind rejection is covered by the state-patch unsupported-kind test, which asserts the generic allowed-kind error, `runtime.decision.rejected`, decision journal `malformed_decision`, and no tool execution. [`tests/test_runtime_loop.py:865-901`](../tests/test_runtime_loop.py#L865-L901)
- RuntimeLoop malformed provider returns are covered by trace tests and request-tool validation tests that assert `runtime.decision.rejected` and `decision.recorded` with `malformed_decision`. [`tests/test_runtime_trace.py:165-176`](../tests/test_runtime_trace.py#L165-L176) [`tests/test_runtime_loop.py:610-627`](../tests/test_runtime_loop.py#L610-L627)
- Legacy/local model-client prompt tests cover filtering decision shapes and explicitly assert that an unallowed `ask_question` shape is omitted when the context schema excludes it. [`tests/test_model_clients.py:70-112`](../tests/test_model_clients.py#L70-L112)

### Missing or indirect coverage

- No dedicated RuntimeLoop test constructs a `RuntimeLoopDecision(kind="ask_question")` or `RuntimeLoopDecision(kind="refuse")` to document that those specific kinds are rejected; current coverage is generic through `propose_state_patch`.
- No RuntimeContext intent-builder tests cover `clarify -> RuntimeLoopDecision(kind="answer", text=<question>)` or `refuse -> RuntimeLoopDecision(kind="answer", text=<refusal/message/reason>)`.
- No RuntimeLoop end-to-end test covers mapped clarify/refuse through `IntentDecisionModel` and verifies emitted `assistant.answer`, decision journal `decision_kind="answer"`, and `RuntimeResult.response_text`.
- No CLI/API tests specifically cover old Runtime `question`/`refusal` response shape or RuntimeLoop mapped clarify/refuse response shape.
- No old Runtime test specifically covers missing `refuse.reason` through the retry loop; validation is covered at the validator level, and the retry-loop test uses missing `ask_question.question`.
- No parser test specifically covers a `refuse` JSON object with an extra refusal payload field and the resulting unexpected-field rejection.

## 7. Migration risk

If old Runtime were removed before ask-question/refusal parity or an intentional adaptation decision:

- Distinct old Runtime response kinds `question` and `refusal` would disappear from the reachable runtime route. RuntimeLoop maps clarify/refuse intent to `answer` or rejects direct ask/refuse decision kinds. [`seed_runtime/runtime.py:265-274`](../seed_runtime/runtime.py#L265-L274) [`seed_runtime/runtime.py:342-351`](../seed_runtime/runtime.py#L342-L351) [`seed_runtime/runtime_loop.py:725-757`](../seed_runtime/runtime_loop.py#L725-L757)
- Event taxonomy would change: old Runtime emits `response.question` / `response.refusal`; RuntimeLoop mapped behavior emits `assistant.answer`, and unsupported ask/refuse emits `runtime.decision.rejected` plus `decision.recorded`. [`seed_runtime/runtime.py:265-274`](../seed_runtime/runtime.py#L265-L274) [`seed_runtime/runtime.py:342-351`](../seed_runtime/runtime.py#L342-L351) [`seed_runtime/runtime_loop.py:180-216`](../seed_runtime/runtime_loop.py#L180-L216) [`seed_runtime/runtime_loop.py:218-251`](../seed_runtime/runtime_loop.py#L218-L251)
- Decision journal semantics would be answer-mapped for clarify/refuse (`decision_kind="answer"`, `outcome="answered"`) unless new kinds are added. [`seed_runtime/runtime_loop.py:227-250`](../seed_runtime/runtime_loop.py#L227-L250)
- Legacy prompt schemas and model clients would still document/expose `ask_question` and `refuse` for `ContextPacket` use, but RuntimeLoop would not accept those kinds directly. [`seed_runtime/context.py:125-132`](../seed_runtime/context.py#L125-L132) [`seed_runtime/model_client.py:195-221`](../seed_runtime/model_client.py#L195-L221) [`seed_runtime/runtime_loop.py:725-729`](../seed_runtime/runtime_loop.py#L725-L729)
- CLI consumers that currently reach old Runtime through `--plan` could see `question` or `refusal`; the default CLI and API paths already see RuntimeLoop answer-mapped behavior. [`scripts/seed_local.py:3468-3473`](../scripts/seed_local.py#L3468-L3473) [`scripts/seed_local.py:3961-3968`](../scripts/seed_local.py#L3961-L3968)
- Old Runtime's validation/parse retry loop around missing `question` or missing `reason` would not carry over; RuntimeLoop currently rejects malformed decisions once. [`seed_runtime/runtime.py:86-170`](../seed_runtime/runtime.py#L86-L170) [`seed_runtime/runtime_loop.py:177-216`](../seed_runtime/runtime_loop.py#L177-L216)

## 8. Extraction / port candidates

These are low-risk options to consider later; this inventory does not recommend one yet.

- Add distinct RuntimeLoop decision kinds for `ask_question` and `refuse`, with explicit validation rules, event kinds, journal outcomes, and `RuntimeResult` fields that preserve the old semantics.
- Keep the current mapping of `clarify` and `refuse` intents to RuntimeLoop `answer` decisions, but document it as intentional and add tests for the mapping and resulting events/results.
- Add a `RuntimeResult.response_kind` separate from `decision_kind`, allowing RuntimeLoop to preserve user-visible `question` / `refusal` response categories even if internal decisions stay answer-mapped.
- Adapt legacy responses at the CLI/API boundary so RuntimeLoop answer-mapped clarify/refuse can be rendered as `question` / `refusal` without changing RuntimeLoop decision kinds.
- If old Runtime remains as the only direct legacy-decision consumer, narrow legacy prompt exposure or adapters so models do not emit `ask_question` / `refuse` into RuntimeLoop unless the boundary maps them deliberately.
