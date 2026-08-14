# Operational Responsibility Slice 004

## Selected architectural boundary

```text
Capability Recommendation
    !=
Operation Selection
```

This slice makes the existing transition more directly visible without changing behavior, compatibility, public names, schemas, CLI, JSON, events, manifests, policy, ranking, or selection logic.

## Implementation evidence

Reviewed implementation evidence:

- `ToolNeedService.resolve_capability()` returns read-only capability resolution metadata for `request_tool` decisions. It separates catalog-derived provider/handoff metadata from registry-derived registered operation candidates and explicitly does not execute, authorize, create pending actions, or mutate state.
- `ToolRecommendationService.recommend_for()` ranks catalog recommendations for a `ToolNeed` using `CapabilityCatalog` and `RecommendationRanker`; it does not register tools or select executable operations.
- `CapabilityCatalog.recommend_for()` returns provider recommendation metadata for a capability.
- `ToolRegistry` stores registered operation specs and lists registered operations by name or capability.
- `Runtime._route()` keeps `request_tool` and `call_tool` on separate branches: `request_tool` records a need and returns recommendations/resolution; `call_tool` dispatches one selected operation through `ToolExecutor`.
- `ToolValidationService.validate_tool_input()` was the compressed implementation point: it both resolved the already-selected `tool_name` to a registered operation and validated the selected operation's input schema.

## Before

Operation selection was behaviorally present but not named as its own responsibility inside registered-tool validation.

```text
call_tool decision
  -> DecisionValidator._validate_tool_call()
  -> ToolValidationService.validate_tool_input()
       -> registry/state lookup for tool_name
       -> input schema validation
```

The registry/state lookup was the implementation transition from the recommendation-capable runtime world into the single operation that would proceed toward execution, but that transition was mixed into generic validation.

## After

Operation selection is now an explicit bounded responsibility inside `ToolValidationService`.

```text
call_tool decision
  -> DecisionValidator._validate_tool_call()
  -> ToolValidationService.validate_tool_input()
       -> ToolValidationService.select_operation()
            -> resolve one selected registered operation by name
       -> input schema validation
```

The new `OperationSelectionResult` names the result of resolving exactly one registered operation. `select_operation()` starts from an already-formed operation name from a `call_tool` decision and preserves the prior registry/state lookup behavior.

## Boundary made explicit

Capability recommendation remains owned by the `request_tool` path:

```text
ToolNeedService
ToolRecommendationService
CapabilityCatalog
```

Operation selection is now directly observable as a separate implementation-local step in the `call_tool` validation path:

```text
ToolValidationService.select_operation()
OperationSelectionResult
```

The implementation now states and enforces the distinction that recommendations surface bounded possibilities, while selection resolves the single registered operation named by an already-formed `call_tool` decision.

## Compatibility preserved

No compatibility boundary changed.

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

No compatibility boundary changed. The slice did not change public CLI behavior, event payloads, JSON response shape, manifests, schemas, recommendation ranking, operation selection behavior, policy behavior, or execution dispatch behavior.

## Files changed

- `seed_runtime/tool_validation.py`
- `tests/test_tool_validation.py`
- `operational_responsibility_slice_004.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/tool_validation.py | 65 ++++++++++++++++++++++++++++++++++++-----
tests/test_tool_validation.py   | 24 +++++++++++++++
2 files changed, 81 insertions(+), 8 deletions(-)
```

Report added:

```text
operational_responsibility_slice_004.md
```

## Tests executed

```text
pytest -q tests/test_tool_validation.py tests/test_tool_recommendations.py tests/test_architecture_invariants.py
```

Result:

```text
22 passed in 0.85s
```

## Remaining compressed operational boundaries

Potential remaining boundaries were not changed in this slice:

- Action-plan creation still chooses the top provider recommendation for a safe text-only plan outside this operation-selection slice.
- Execution validation and execution dispatch remain closely adjacent in the execution path.
- Model-visible registered operation presentation and model decision production remain separate in behavior, but further architectural visibility could be added in future slices if implementation evidence shows compression.

This slice intentionally changed exactly one recovered architectural boundary: capability recommendation is now more explicitly separate from operation selection.
