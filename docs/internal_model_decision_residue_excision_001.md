# Internal model-decision residue excision 001

## Deleted residue

- Removed the importable `DecisionProducer` protocol and `StaticDecisionProducer` test helper from `seed_runtime.runtime`; `Runtime` no longer accepts any decision producer, retry count, validator, context composer, tool executor, tool need service, or capability catalog constructor residue.
- Removed the `ParsedDecisionProducer` adapter from `seed_runtime.model_client`.
- Removed the golden-case `DecisionEvaluator` harness and its tests because it existed to score model-shaped runtime decisions.
- Removed stale runtime-routing tests and documentation that advertised `DecisionProducer.decide(...) -> model-shaped Decision -> Runtime routing` as a live road.

## Retained independent substrate

- `Runtime` remains a free-text input boundary that records `input.user_message`, records `runtime.decision_authority_unsupported`, and returns an unsupported response without producing, validating, or routing model-shaped decisions.
- `DecisionInputComposer` and `DecisionInputPacket` remain because local diagnostic/context-view surfaces still render deterministic read-only context.
- `DecisionValidator` remains as deterministic validation substrate for independently callable services and external testimony parsing tests.
- `ToolExecutor`, `ToolNeedService`, `CapabilityCatalog`, `EventLedger`, `StateProjector`, state-patch services, and RuntimeLoop-specific deterministic services remain outside this excision.

## Renamed or narrowed artifacts

- Renamed the compact intent adapter names from `DecisionBuilder` / `IntentDecisionProducer` to `RuntimeLoopIntentDecisionBuilder` / `RuntimeLoopIntentProducer` to avoid presenting them as Runtime decision authority.
- Regenerated the architecture graph so Runtime has no ToolExecutor or ToolNeedService routing edge.

## Remaining model-related code

- `seed_runtime.model_client` still contains prompt rendering, model transport helpers, and strict JSON parsing for external grammar/testimony.
- `seed_runtime.intent_classifier` still contains intent classification and parsing code used by explicit RuntimeLoop callers and local tooling, not by `Runtime`.

## Remaining lawful consumers

- `SeedAPI.post_user_message` delegates to the narrowed `Runtime` input boundary.
- Local script context-view code consumes `DecisionInputComposer` for deterministic read-only presentation.
- RuntimeLoop intent tests consume the renamed RuntimeLoop intent adapter as an explicit non-Runtime path.

## Preserved Unknowns

- The legacy `Decision` data model and `DecisionValidator` still have broad field vocabulary. They are retained only where tests demonstrate independent deterministic validation or external grammar parsing; a future inquiry should decide whether those shapes should be narrowed further.
- Historical audit documents outside this bounded neighborhood may still mention the generic word “Decision” for unrelated authority concepts.

removed authority residue
→ surviving independently lawful substrate
→ remaining Unknown requiring future inquiry
