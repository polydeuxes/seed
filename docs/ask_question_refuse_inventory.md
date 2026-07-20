# `ask_question` / `refuse` inventory

> **Stale/quarantined RuntimeLoop-era inventory.** Current architecture treats `Runtime` as canonical and `RuntimeLoop` as deprecated/experimental, not CLI/API/default behavior. Statements about legacy Runtime or default RuntimeLoop routing are historical and must not be used as current-core guidance.

This inventory is source-file based and records current behavior only. It does not propose or implement behavior changes.

## 1. Models


- `Decision` stores the common `kind` and required `reason` fields plus optional per-kind payload fields: `answer`, `question`, `tool_name`, `tool_arguments`, `tool_need`, `action_plan`, `handoff_plan`, and `state_patch`. [`seed_runtime/models.py:205-215`](../seed_runtime/models.py#L205-L215)
- `ask_question` uses `kind="ask_question"`, `reason`, and `question`. The validator requires `decision.question` to be truthy and reports `ask_question decisions require question` when missing or empty. [`seed_runtime/decisions.py:47-49`](../seed_runtime/decisions.py#L47-L49)
- `refuse` uses `kind="refuse"` and `reason`. There is no separate refusal-message field on the legacy model; the routed user-visible message is the same `reason`. The validator requires `decision.reason` to be truthy and reports `refuse decisions require reason` when missing or empty. [`seed_runtime/decisions.py:57-59`](../seed_runtime/decisions.py#L57-L59)
- The validator has explicit branches for `answer`, `ask_question`, `request_tool`, `call_tool`, `propose_state_patch`, and `refuse`; any other kind value that reaches the validator is reported as unsupported. [`seed_runtime/decisions.py:31-59`](../seed_runtime/decisions.py#L31-L59)

### `seed_runtime.runtime_loop.Decision`

- RuntimeLoop's `Decision` dataclass has `kind`, `text`, `tool_name`, `tool_args`, `tool_need`, and `reason`; it has no `question`, `answer`, or refusal-specific field. [`seed_runtime/runtime_loop.py:60-68`](../seed_runtime/runtime_loop.py#L60-L68)
- RuntimeLoop validation rejects any kind outside `answer`, `call_tool`, and `request_tool` with `decision kind must be 'answer', 'call_tool', or 'request_tool'`. [`seed_runtime/runtime_loop.py:725-729`](../seed_runtime/runtime_loop.py#L725-L729)

## 2. Prompt / model-client behavior

### Legacy decision prompts

- `ContextComposer` exposes a legacy `decision_schema` whose kinds are `answer`, `ask_question`, `call_tool`, `request_tool`, and `refuse`. It does not include `propose_state_patch` in this composer-provided schema. [`seed_runtime/context.py:125-132`](../seed_runtime/context.py#L125-L132)

### Intent classifier mapping


## 3. Legacy Runtime behavior

### `ask_question`

- Old `Runtime.handle_user_message` appends `input.user_message`, projects state, composes a `ContextPacket`, and then loops through model decision attempts. Each parsed decision is appended as `model.decision.proposed` before validation. [`seed_runtime/runtime.py:68-118`](../seed_runtime/runtime.py#L68-L118)
- When an `ask_question` decision validates, `_route` appends `response.question` with payload `{"question": decision.question}` and returns `RuntimeResponse(kind="question", message=decision.question or "")`. [`seed_runtime/runtime.py:265-274`](../seed_runtime/runtime.py#L265-L274)
- Parse failures are handled before decision validation: Runtime appends `model.decision.parse_failed`, retries with a JSON correction prompt if retries remain, and returns `RuntimeResponse(kind="invalid_decision", message="Model decision failed parsing.", payload={"errors": [str(exc)]})` when parse retries are exhausted. [`seed_runtime/runtime.py:86-108`](../seed_runtime/runtime.py#L86-L108) [`seed_runtime/runtime.py:213-230`](../seed_runtime/runtime.py#L213-L230)

### `refuse`

- When a `refuse` decision validates, `_route` appends `response.refusal` with payload `{"reason": decision.reason}` and returns `RuntimeResponse(kind="refusal", message=decision.reason)`. [`seed_runtime/runtime.py:342-351`](../seed_runtime/runtime.py#L342-L351)

## 4. RuntimeLoop behavior

- RuntimeLoop does not support `ask_question` or `refuse` as decision kinds; validation only accepts `answer`, `call_tool`, and `request_tool`. This is intentional: RuntimeLoop represents clarify/refuse user-facing behavior as answer responses, while distinct response categories are canonical `Runtime` behavior; the old “legacy Runtime” label in this inventory is stale. [`seed_runtime/runtime_loop.py:32`](../seed_runtime/runtime_loop.py#L32) [`seed_runtime/runtime_loop.py:725-757`](../seed_runtime/runtime_loop.py#L725-L757)
- A mapped clarify/refuse answer appends `assistant.answer` with payload `{"text": decision.text, "reason": decision.reason}`, appends a decision journal record with `decision_kind="answer"` and `outcome="answered"`, and returns `RuntimeResult(decision_kind="answer", response_text=decision.text, policy_allowed=True, decision_outcome="answered", ...)`. [`seed_runtime/runtime_loop.py:218-251`](../seed_runtime/runtime_loop.py#L218-L251)
- A provider-returned unsupported kind such as `ask_question` or `refuse` is rejected before routing: RuntimeLoop appends `runtime.decision.rejected`, records a decision journal entry with `outcome="malformed_decision"`, and returns `RuntimeResult(decision_kind=None, response_text=None, policy_allowed=False, error=..., decision_outcome="malformed_decision", ...)`. [`seed_runtime/runtime_loop.py:177-216`](../seed_runtime/runtime_loop.py#L177-L216)
- RuntimeLoop has no retry loop or parse-failure retry path; a malformed provider return produces a single rejection and a malformed-decision result. [`seed_runtime/runtime_loop.py:177-216`](../seed_runtime/runtime_loop.py#L177-L216)

## 5. CLI/API behavior

- `build_local_app` was described by this historical inventory as constructing both Runtime and RuntimeLoop and routing the default path to RuntimeLoop. Current architecture treats `Runtime` as canonical and RuntimeLoop as quarantined/deprecated; do not use this note as current default-routing guidance. [`scripts/seed_local.py:641-695`](../scripts/seed_local.py#L641-L695) [`scripts/seed_local.py:236-299`](../scripts/seed_local.py#L236-L299)
- Historical note: this inventory described the CLI as using RuntimeLoop by default and switching to `run_legacy` for `--plan`; current architecture treats `Runtime` as canonical and RuntimeLoop as quarantined/deprecated. [`scripts/seed_local.py:3468-3473`](../scripts/seed_local.py#L3468-L3473) [`scripts/seed_local.py:3961-3968`](../scripts/seed_local.py#L3961-L3968)
- Canonical Runtime `ask_question`, if reached through the historical `run_legacy` label, serializes as `{"kind": "question", "message": <question>, "payload": ...}` because `RuntimeResponse(kind="question", message=...)` is converted with `to_plain`. [`seed_runtime/runtime.py:265-274`](../seed_runtime/runtime.py#L265-L274) [`scripts/seed_local.py:290-299`](../scripts/seed_local.py#L290-L299)
- Old Runtime `refuse`, if reached through `run_legacy`, serializes as `{"kind": "refusal", "message": <reason>, "payload": ...}`. [`seed_runtime/runtime.py:342-351`](../seed_runtime/runtime.py#L342-L351) [`scripts/seed_local.py:290-299`](../scripts/seed_local.py#L290-L299)
- RuntimeLoop mapped clarify/refuse results pass through `runtime_result_response` as ordinary `{"kind": "answer", "message": result.response_text, "payload": {"decision_kind": "answer", ...}}`; there is no CLI-visible `question` or `refusal` kind on that path. [`scripts/seed_local.py:169-220`](../scripts/seed_local.py#L169-L220)
- `SeedAPI` wraps RuntimeLoop directly and returns the `RuntimeResult` from `runtime.run`; therefore mapped clarify/refuse API responses have `decision_kind="answer"` and `response_text=<question or refusal text>`, while unsupported ask/refuse provider decisions return a malformed-decision `RuntimeResult`. [`seed_runtime/api.py:15-32`](../seed_runtime/api.py#L15-L32) [`seed_runtime/runtime_loop.py:177-251`](../seed_runtime/runtime_loop.py#L177-L251)

## 6. Test coverage

### Covered today

- Old Runtime refusal route: `tests/test_runtime_loop.py::test_routes_refuse` verifies response kind `refusal`, response message `unsafe request`, and events `input.user_message`, `model.decision.proposed`, `response.refusal`. [`tests/test_runtime_loop.py:92-105`](../tests/test_runtime_loop.py#L92-L105)
- Old decision validation: `tests/test_decisions.py::test_ask_question_requires_question` and `tests/test_decisions.py::test_refuse_requires_reason` cover the required question/reason validation errors. [`tests/test_decisions.py:18-27`](../tests/test_decisions.py#L18-L27) [`tests/test_decisions.py:118-125`](../tests/test_decisions.py#L118-L125)
- Old Runtime invalid-decision retry behavior includes missing-answer followed by missing-question and checks final invalid-decision payload plus deterministic invalid-event payloads. [`tests/test_runtime_loop.py:213-262`](../tests/test_runtime_loop.py#L213-L262)
- RuntimeLoop end-to-end mapped clarify/refuse coverage verifies `assistant.answer`, decision journal `decision_kind="answer"`, and `outcome="answered"`. [`tests/test_runtime_loop.py:428-489`](../tests/test_runtime_loop.py#L428-L489)
- RuntimeLoop unsupported-kind rejection is covered by dedicated direct `ask_question` and direct `refuse` tests, plus the generic state-patch unsupported-kind test; these assert the allowed-kind error, `runtime.decision.rejected`, decision journal `malformed_decision`, and no operation implementation execution. [`tests/test_runtime_loop.py:934-979`](../tests/test_runtime_loop.py#L934-L979) [`tests/test_runtime_loop.py:982-1018`](../tests/test_runtime_loop.py#L982-L1018)
- RuntimeLoop malformed provider returns are covered by trace tests and request-tool validation tests that assert `runtime.decision.rejected` and `decision.recorded` with `malformed_decision`. [`tests/test_runtime_trace.py:165-176`](../tests/test_runtime_trace.py#L165-L176) [`tests/test_runtime_loop.py:610-627`](../tests/test_runtime_loop.py#L610-L627)
- Legacy/local model-client prompt tests cover filtering decision shapes and explicitly assert that an unallowed `ask_question` shape is omitted when the context schema excludes it. [`tests/test_model_clients.py:70-112`](../tests/test_model_clients.py#L70-L112)

### Missing or indirect coverage

- No CLI/API tests in this historical inventory specifically covered canonical Runtime `question`/`refusal` response shape or RuntimeLoop mapped clarify/refuse response shape.
- No canonical Runtime test in this historical inventory specifically covers missing `refuse.reason` through the retry loop; validation is covered at the validator level, and the retry-loop test uses missing `ask_question.question`.
- No parser test specifically covers a `refuse` JSON object with an extra refusal payload field and the resulting unexpected-field rejection.

## 7. Migration risk

RuntimeLoop now has an intentional adaptation decision for clarify/refuse semantics:

- Distinct canonical Runtime response kinds `question` and `refusal` are Runtime behavior; the old “legacy Runtime” label in this inventory is stale. RuntimeLoop intentionally maps clarify/refuse intent to `answer` responses and rejects direct ask/refuse decision kinds. [`seed_runtime/runtime.py:265-274`](../seed_runtime/runtime.py#L265-L274) [`seed_runtime/runtime.py:342-351`](../seed_runtime/runtime.py#L342-L351) [`seed_runtime/runtime_loop.py:725-757`](../seed_runtime/runtime_loop.py#L725-L757)
- Event taxonomy would change: canonical Runtime emits `response.question` / `response.refusal`; RuntimeLoop mapped behavior emits `assistant.answer`, and unsupported ask/refuse emits `runtime.decision.rejected` plus `decision.recorded`. [`seed_runtime/runtime.py:265-274`](../seed_runtime/runtime.py#L265-L274) [`seed_runtime/runtime.py:342-351`](../seed_runtime/runtime.py#L342-L351) [`seed_runtime/runtime_loop.py:180-216`](../seed_runtime/runtime_loop.py#L180-L216) [`seed_runtime/runtime_loop.py:218-251`](../seed_runtime/runtime_loop.py#L218-L251)
- Decision journal semantics would be answer-mapped for clarify/refuse (`decision_kind="answer"`, `outcome="answered"`) unless new kinds are added. [`seed_runtime/runtime_loop.py:227-250`](../seed_runtime/runtime_loop.py#L227-L250)
- CLI consumers that this historical inventory described as reaching Runtime through `--plan` could see `question` or `refusal`; that was the historical audit finding; current architecture treats `Runtime` as canonical and RuntimeLoop as quarantined/deprecated. [`scripts/seed_local.py:3468-3473`](../scripts/seed_local.py#L3468-L3473) [`scripts/seed_local.py:3961-3968`](../scripts/seed_local.py#L3961-L3968)
- Canonical Runtime's validation/parse retry loop around missing `question` or missing `reason` would not carry over; RuntimeLoop currently rejects malformed decisions once. [`seed_runtime/runtime.py:86-170`](../seed_runtime/runtime.py#L86-L170) [`seed_runtime/runtime_loop.py:177-216`](../seed_runtime/runtime_loop.py#L177-L216)

## 8. Conclusion

`ask_question` and `refuse` are not currently considered RuntimeLoop migration blockers because RuntimeLoop already preserves the user-facing clarify/refuse behavior through `answer` responses. Direct `ask_question` and `refuse` RuntimeLoop decision kinds remain unsupported by design; distinct `question` and `refusal` response categories belong to canonical Runtime behavior; the “legacy Runtime” label in this inventory is stale.

## 9. Extraction / port candidates

These are low-risk options to consider later; this inventory does not recommend one yet.

- No RuntimeLoop migration work is currently recommended for `ask_question` or `refuse`; the intentional behavior is answer-mapped clarify/refuse plus direct-kind rejection.
- If canonical Runtime remains the direct legacy-decision consumer, narrow legacy prompt exposure or adapters so models do not emit `ask_question` / `refuse` into RuntimeLoop unless the boundary maps them deliberately.
