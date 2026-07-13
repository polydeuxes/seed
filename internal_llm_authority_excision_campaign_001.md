# Internal LLM Authority Excision Campaign 001

## Governing architectural requirement

For this campaign, the governing requirement is explicit task authority rather than an inferred repository fact:

```text
LLM output
→ external grammar
→ externally attributed testimony
→ observation candidate
→ Seed-controlled admission, rejection, or preserved Unknown
```

An LLM has no internal constitutional standing inside Seed. Model output is foreign testimony expressed in external grammar; it is not Seed decision, command, capability need, operation selection, execution request, bounded answer, lawful question, refusal, plan, handoff, state patch, evidence, or mutation authority.

## Inspected implementation neighborhood

Inspected implementation evidence included:

- `seed_runtime/runtime.py`: `DecisionProducer`, `StaticDecisionProducer`, `Runtime.handle_user_message`, decision retry prompts, validation/intent guard, and routing to answer/question/refusal/tool need/tool call/state patch.
- `seed_runtime/context.py`: `DecisionInputPacket`, `DecisionInputComposer`, model-visible state, evidence, open needs, visible tools, and allowed decision schema.
- `seed_runtime/model_clients.py`: local provider adapters, prompt construction, strict JSON parsing, allowed model decision shapes, and provider-backed `decide(...)` methods.
- `seed_runtime/model_client.py`: prompt adapter, parsed decision producer compatibility surface, and decision prompt rendering.
- `seed_runtime/intent_classifier.py`: intent classifier, `DecisionBuilder`, and `IntentDecisionProducer` compatibility path that builds `Decision` objects.
- `seed_runtime/decisions.py`: `DecisionValidator` shape validation for answer, ask_question, request_tool, call_tool, propose_state_patch, and refuse.
- `seed_runtime/tool_intent.py`: post-selection intent guard for model-selected tool decisions.
- `seed_runtime/tool_needs.py`, `seed_runtime/execution.py`, `seed_runtime/state_patches.py`, `seed_runtime/action_plans.py`, and `seed_runtime/handoff_plans.py`: reusable service substrates reached by the old corridor or adjacent non-LLM CLI routes.
- `scripts/seed_local.py`: canonical local app constructor that installed an intent-classifier-backed producer into `Runtime`.
- Tests referencing `Runtime`, `StaticDecisionProducer`, provider adapters, and model-decision events.
- Architecture metadata in `docs/capability_ownership_matrix.md` describing the old runtime corridor.

## Classified dependency inventory

| Occurrence | Classification | Reason |
| --- | --- | --- |
| `Runtime.handle_user_message -> decision_producer.decide(...) -> Runtime._route(...)` | Internal authority corridor | Model-shaped output selected runtime movement and initiated response, need creation, execution, or patching. |
| `model.decision.proposed` event as causation for `_route` | Internal authority corridor | Event attribution did not prevent the artifact from controlling downstream Seed movement. |
| Decision retry prompts in `Runtime` | Internal authority corridor | Runtime asked a model to correct an internal decision shape and try again. |
| `DecisionValidator.validate(...)` when used by `Runtime` | Internal authority corridor support | It validated shape after selection; it did not change who selected the movement. |
| `ToolIntentGuard.validate(...)` when used by `Runtime` | Internal authority corridor support | It could reject unsafe tool choices but did not become the selector. |
| `DecisionInputPacket.tools` and prompt-visible tool inventory | Internal authority corridor support | It existed to let a model select registered operations. |
| `OllamaDecisionProducer`, `LlamaCppDecisionProducer`, `ParsedDecisionProducer` | Compatibility residue after this slice | They can still parse/generate `Decision` artifacts, but the canonical runtime no longer consumes them. |
| `IntentDecisionProducer` and `DecisionBuilder` | Compatibility residue / reusable deterministic substrate | Deterministic classification pieces may be independently tested, but their `DecisionProducer` shape no longer grants runtime authority. |
| `EventLedger`, causation, actor fields | Reusable non-LLM substrate | Deterministic append/project behavior remains valid without model authority. |
| `ToolNeedService` | Reusable non-LLM substrate | Capability-gap creation remains a service only when called by a lawful non-model caller. Runtime no longer calls it from model output. |
| `ToolExecutor`, validation, policy, result recording | Reusable non-LLM substrate | Execution services remain valid for explicit registered operation flows; model output no longer selects them through `Runtime`. |
| `StatePatchService` | Reusable non-LLM substrate | Explicit patch validation remains; model-produced patches no longer reach it through `Runtime`. |
| `ActionPlanService`, `HandoffPlanService` | Reusable non-LLM substrate | CLI lifecycle services remain independently owned and were not part of the selected runtime route. |
| Legacy tests asserting `model.decision.proposed` routing | Dead or test-only legacy implementation for this corridor | They celebrated the removed authority path and are superseded by focused excision tests. |

## Before topology

```text
user input
→ Runtime.handle_user_message
→ DecisionInputComposer.compose(...)
→ DecisionProducer.decide(DecisionInputPacket)
→ model/intention-produced Decision
→ model.decision.proposed
→ DecisionValidator / ToolIntentGuard
→ Runtime._route(...)
→ response.answer / response.question / response.refusal
  or ToolNeedService.create_from_decision
  or ToolExecutor.execute
  or StatePatchService.apply
```

## Selected excision boundary

The selected boundary is the first complete crossing inside `Runtime.handle_user_message`: `DecisionProducer.decide(...)` returning a `Decision` that `Runtime` consumed as routing authority.

## Producer / artifact / consumer

- Producer: any object implementing the legacy `DecisionProducer` shape, including local provider adapters, parsed decision adapters, static tests, and intent-classifier adapters.
- Artifact: `seed_runtime.models.Decision`, including answer, ask_question, request_tool, call_tool, propose_state_patch, refuse, and schema-adjacent plan/handoff kinds.
- Consumer: `seed_runtime.runtime.Runtime`, formerly via validation/intent guard followed by `_route(...)`.

## Authority previously granted

A model-produced `Decision` could initiate:

- internally authoritative answer production;
- question production;
- refusal production;
- capability/tool-need creation;
- registered tool selection and execution;
- state patch validation/application;
- retry prompts asking the model to correct an internal decision;
- event-ledger records with model-authored causation for downstream runtime movement.

## Implementation changes

- Replaced the old routing runtime with an input boundary that records `input.user_message`, emits `runtime.decision_authority_unsupported`, and returns an unsupported response rather than asking any producer to decide.
- Left `DecisionProducer` as an import-only compatibility protocol and made `StaticDecisionProducer.decide(...)` explicitly unsupported.
- Kept the `Runtime.__init__` `decision_producer` keyword as inert compatibility residue; it is ignored and cannot restore routing authority.
- Updated the canonical local app constructor so it no longer creates an `IntentPromptModelClient`, `TextIntentClassifier`, or `IntentDecisionProducer`, and no longer passes a producer to `Runtime`.
- Added focused tests proving model-shaped `Decision` artifacts are inert at the runtime boundary and that the static compatibility alias cannot restore `decide(...)` movement.

## Removed routes

The selected corridor removed runtime consumption of model-produced decisions for:

- `response.answer`;
- `response.question`;
- `response.refusal`;
- `tool_need.created`;
- `tool.call.started` / `tool.call.completed`;
- `state.patch.*` via runtime route;
- retry prompts for invalid model decisions;
- model-visible operation inventory as a requirement for the surviving runtime path.

## Retained Seed-owned substrate

Retained without assigning new authority:

- event ledger and projection;
- decision schemas/validators as compatibility and non-runtime substrate;
- tool validation, policy, executor, and result recording services;
- tool need service;
- capability catalog and recommendation services;
- state patch service;
- action plan and handoff plan services;
- deterministic read models and CLI diagnostic/read-only surfaces.

## External-grammar boundary

No broad new external-grammar framework was added. Existing model/provider adapters may still produce parseable `Decision` objects as external artifacts, but there is no surviving canonical `seed_runtime.Runtime` consumer that treats those artifacts as Seed authority. The preserved Unknown is the future lawful admission route for LLM testimony; this campaign does not create it.

## Compatibility breaks

| Public symbol or behavior | Previous authority | Compatibility status | Consequence |
| --- | --- | --- | --- |
| `Runtime(..., decision_producer=...)` | Producer output controlled runtime routing | Keyword remains inert; `runtime.decision_producer is None` | Callers receive unsupported free-text runtime response instead of model-selected movement. |
| `StaticDecisionProducer.decide(...)` | Test helper could feed authoritative decisions | Alias remains, but `decide` raises `RuntimeError` | Tests/callers must stop using model-shaped Decisions as runtime authority. |
| `build_local_app(...)` model-backed setup | Installed intent-classifier-backed producer | Constructor still returns `LocalSeedApp`, but with `model_client=None` | Local free-text app no longer calls an LLM/provider for movement. |
| `model.decision.proposed` in canonical runtime | Model event caused downstream routing | No longer emitted by `Runtime` | Trace/tests relying on that event must migrate to non-LLM explicit services or unsupported boundary records. |

## Test changes

Added `tests/test_internal_llm_authority_excision.py` with proof that answer, question, refusal, request_tool, call_tool, and propose_state_patch `Decision` objects supplied through the removed boundary produce only input and unsupported-boundary events.

## Tests executed

- `python -m black seed_runtime/runtime.py scripts/seed_local.py tests/test_internal_llm_authority_excision.py`
- `pytest -q tests/test_internal_llm_authority_excision.py`
- `python -m scripts.seed_local --question-surface-inventory --json`
- `python - <<'PY' ... import seed_runtime ... PY`
- `rg -n "decision_producer\.decide\(|self\.decision_producer\.decide\(|model\.decision\.proposed" seed_runtime scripts tests/test_internal_llm_authority_excision.py -S`

## Files changed

- `seed_runtime/runtime.py`
- `scripts/seed_local.py`
- `tests/test_internal_llm_authority_excision.py`
- `internal_llm_authority_excision_campaign_001.md`

## LOC delta

Final staged delta before commit: 398 insertions and 355 deletions across four files. Per-file numstat: `internal_llm_authority_excision_campaign_001.md` +207/-0, `scripts/seed_local.py` +56/-33, `seed_runtime/runtime.py` +43/-322, and `tests/test_internal_llm_authority_excision.py` +92/-0.

## Required questions answered

1. First crossing: `Runtime.handle_user_message` consuming the return value of `DecisionProducer.decide(...)`.
2. Artifact: `seed_runtime.models.Decision`.
3. Producer: model/provider/intent/static objects implementing `DecisionProducer`.
4. Consumer: `seed_runtime.runtime.Runtime`.
5. Movements: answer, question, refusal, tool need, tool execution, state patch, retry, and model-authored event causation.
6. Validation only validated shape; it did not alter authority.
7. Policy/intent checks did not alter who selected the movement.
8. Dependent routes: `_route` branches for answer, ask_question, request_tool, call_tool, propose_state_patch, refuse, plus retry inputs.
9. Model-facing support surfaces: decision prompt, allowed JSON shapes, visible tool inventory, retry prompts, parse adapters.
10. Valid without LLM: ledger, projector, validators, executor, policy, tool needs, capability catalog, state patch service, action/handoff services, read models.
11. No lawful non-LLM caller after excision in this selected path: free-text runtime answer/question/refusal/request_tool/call_tool/patch routing from `Runtime`.
12. Removed: runtime call to `decision_producer.decide`, model decision event routing, retries, and `_route` authority consumption.
13. Retained: substrate services and inert compatibility names.
14. Compatibility changed: constructor producer is ignored; `StaticDecisionProducer.decide` raises; local app no longer installs a model producer.
15. No model-produced output can trigger Seed mutation or execution through the selected canonical runtime boundary.
16. No model-produced output can become authoritative answer, question, refusal, need, plan, patch, or decision through the selected canonical runtime boundary.
17. Some LLM-related adapters remain inside `seed_runtime` as compatibility residue.
18. They are not a corridor because `Runtime` no longer calls or consumes them for movement.
19. No new LLM external-grammar boundary remains beyond inert parse/provider artifacts; lawful admission remains Unknown.
20. Next smallest target: remaining provider/intent/evaluation compatibility residue that still names `DecisionProducer` and may be callable outside canonical `Runtime`, especially `ParsedDecisionProducer`, local provider producers, and `DecisionEvaluator`.

## Remaining internal LLM dependencies

- `seed_runtime/model_client.py` and `seed_runtime/model_clients.py` still contain prompt/parse/provider code.
- `seed_runtime/intent_classifier.py` still contains intent-classifier and decision-builder compatibility code.
- `seed_runtime/evaluations.py` still evaluates producer-shaped objects for legacy tests.

These were not removed because the stopping condition required one complete corridor, not adjacent residue cleanup.

## Preserved Unknowns

- Whether a future lawful LLM testimony adapter should preserve raw output as evidence candidate, observation candidate, provider response, or typed Unknown remains intentionally unresolved.
- Whether legacy evaluation surfaces should be deleted or converted in the next campaign remains unresolved.
- Whether documentation outside the selected runtime boundary should be rewritten globally remains unresolved.

## Next bounded excision target

The next bounded excision target is the model/provider adapter and evaluation neighborhood that can still produce `Decision` objects, even though canonical `Runtime` no longer consumes them.

## Confidence statement

High confidence for the selected canonical runtime corridor: the runtime no longer calls `decide(...)`, ignores supplied producers, and focused tests prove model-shaped `Decision` objects cannot create response, need, execution, or patch events through that boundary. Medium confidence for whole-repository absence: compatibility residue remains intentionally outside this campaign's stopping boundary and should be excised next.

The selected internal LLM authority corridor has been excised.
