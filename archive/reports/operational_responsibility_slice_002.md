# Operational Responsibility Slice 002

## selected architectural boundary

Provider recommendation is not registered operation.

This slice selected the recovered boundary:

```text
Provider Recommendation
  !=
Registered Operation
```

The boundary was selected because the request-tool capability resolution path already preserves it in output shape and tests, but the implementation assembled provider recommendation payloads, handoff candidates, known-capability state, and registered operation candidates in one method-local dictionary construction.

## implementation evidence

Repository evidence supporting this boundary already existed before this slice:

- `docs/archive/original_book_of_seed/02-domain-model.md` states that the Core MVP path stops at ToolNeed, capability resolution, registered operation candidates, and provider/handoff recommendations, preserving provider/handoff recommendation metadata separately from registered operation execution.
- `tool_vocabulary_orientation_recovery_investigation.md` identifies `CapabilityRecommendation` as suggested provider metadata and `ToolRegistry` / `ToolSpec` as registered operation inventory.
- `operational_responsibility_slice_001.md` left `ToolNeedService` as a consumer that may expose registered operation candidates through `ToolRegistry.list_tools_for_capability()` while keeping capability/provider/handoff recommendation metadata separate.
- `tests/test_tool_recommendations.py` already proves that registered operations come only from registry capability lookup even when catalog handoff metadata names an operation.

Direct implementation evidence in this slice:

- `ToolNeedService.resolve_capability()` remains the request-tool capability resolution entry point.
- `_CapabilityResolution._registered_operation_candidates()` reads callable candidates only from `ToolRegistry.list_tools_for_capability(..., visible_only=True)`.
- `_CapabilityResolution._provider_recommendation_payload()` reads ranked provider recommendations only from the recommendation service output supplied to capability resolution.
- `_CapabilityResolution._handoff_candidates()` reads handoff candidates only from catalog recommendations attached to the capability catalog entry.

## before

Before this slice, `ToolNeedService.resolve_capability()` directly built the entire response dictionary inline.

That inline construction mixed these responsibilities in one implementation concept:

- known capability lookup from `CapabilityCatalog`;
- registered operation candidate lookup from `ToolRegistry`;
- provider recommendation payload shaping from ranked recommendations;
- handoff candidate shaping from catalog recommendation metadata.

The externally visible response was correct, but the implementation made the recovered boundary less visible because provider/handoff advisory metadata and registered callable operation inventory were neighboring list comprehensions inside one dictionary literal.

## after

After this slice, `ToolNeedService.resolve_capability()` delegates response assembly to `_CapabilityResolution`.

The implementation-local abstraction keeps the compatibility response shape unchanged while splitting source ownership:

- registered operation candidates are built by `_registered_operation_candidates()`;
- provider recommendation payloads are built by `_provider_recommendation_payload()`;
- handoff candidates are built by `_handoff_candidates()`;
- the final payload shape is centralized in `to_payload()`.

The abstraction is intentionally private and implementation-local. It does not rename public concepts, serialized fields, CLI vocabulary, events, schemas, manifests, or APIs.

## boundary made explicit

The boundary made more explicit is:

```text
Provider Recommendation
  !=
Registered Operation
```

The code now shows that provider recommendations and handoff candidates are catalog/recommendation-derived advisory metadata, while registered operations are registry-derived callable inventory.

This better reflects the recovered architecture because the implementation no longer makes catalog-derived recommendation metadata and registry-derived callable operation inventory appear as one mixed resolution calculation.

## compatibility preserved

No.

No compatibility boundary changed.

Preserved boundaries:

- no public rename;
- no schema change;
- no event change;
- no manifest change;
- no CLI change;
- no API change;
- no JSON shape change;
- no ledger change;
- no behavior change intended.

## files changed

- `seed_runtime/tool_needs.py`
  - Added private `_CapabilityResolution` implementation-local abstraction.
  - Updated `ToolNeedService.resolve_capability()` to delegate payload assembly to that abstraction.
- `operational_responsibility_slice_002.md`
  - Added this report.

## LOC changed

Implementation LOC changed, excluding this report:

```text
seed_runtime/tool_needs.py: +68 / -28 / net +40
```

## tests executed

```text
pytest -q tests/test_tool_recommendations.py tests/test_architecture_invariants.py tests/test_runtime_loop.py
```

Result:

```text
27 passed in 1.28s
```

## remaining compressed boundaries

The following recovered boundaries remain candidates for future slices, subject to fresh implementation evidence before any change:

- Capability recommendation versus operation selection in the request-tool path.
- Registered operation validation versus registered operation execution in the call-tool path.
- Execution result recording versus mutation or cluster truth.
- Observation-derived evidence versus capability promotion or availability claims.

No future slice should assume these are currently compressed without first re-reading implementation evidence.
