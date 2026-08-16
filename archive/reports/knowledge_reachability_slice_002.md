# Knowledge Reachability Slice 002 — Staged index construction across audit surfaces

## District consistency gate

- Active district verified: **Knowledge Reachability**.
- Handoff source verified: **`operational_graph_outward_scout_005.md`**.
- Completed source district verified: **Operational Graph**.
- Latest completed Operational Graph slice verified: **`operational_graph_slice_008.md`**.
- Slice 001 landed cleanly enough to reassess; repository authority continued to support staged index construction as a separate boundary.

## Selected boundary

Knowledge Reachability index construction across staged surfaces.

## Implementation evidence

After candidate admission was isolated, `build_knowledge_reachability_audit_result(...)` still performed a distinct `build_indexes` phase that produced `_AuditIndexes` through preserved event payload surfaces, projected state surfaces, read-model/source-navigation surfaces, and inquiry-orientation surfaces while maintaining timing metadata and counters.

## Before

The result builder directly invoked `_build_indexes(...)` inside its `build_indexes` phase, keeping the phase handoff less visible in the public audit orchestration.

## After

`_construct_knowledge_reachability_indexes(...)` now names the staged index construction boundary and returns the unchanged `_AuditIndexes` artifact to the result builder.

## Recovered producer

`_construct_knowledge_reachability_indexes(...)`.

## Recovered artifact/helper

`_AuditIndexes` remains the handoff artifact carrying preserved, projected, read-model, and inquiry term indexes.

## Recovered consumer

`build_knowledge_reachability_audit_result(...)` consumes `_AuditIndexes` during the evaluate phase.

## Compatibility preserved

No.

Public row booleans, metadata timing/index keys, algorithmic counters, JSON output, table/human output, read-only behavior, event-ledger behavior, and diagnostic inventory/shape behavior are preserved.

## Files changed

- `seed_runtime/knowledge_reachability.py`
- `tests/test_knowledge_reachability.py`
- `knowledge_reachability_slice_002.md`

## LOC changed

Part of the batch diff: `seed_runtime/knowledge_reachability.py` and `tests/test_knowledge_reachability.py` changed with 352 insertions and 55 deletions before reports.

## Tests executed

- `pytest -q tests/test_knowledge_reachability.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed.

Focused coverage includes preserved, projected, read-model, source-navigation, and inquiry indexes; phase/index timings; counters; `_AuditIndexes` handoff; public row booleans; public JSON/table output; read-only ledger preservation.

## Remaining compressed responsibilities

Candidate stage evaluation and first-loss row production remained visible after this slice and was reassessed before Slice 003.

## Required questions

1. **What responsibility was previously compressed?** Staged construction of Knowledge Reachability indexes across preserved, projected, read-model/source-navigation, and inquiry surfaces.
2. **Which implementation-local ownership boundary became directly observable?** The index-construction handoff from audit inputs to `_AuditIndexes`.
3. **What producer now owns the recovered responsibility?** `_construct_knowledge_reachability_indexes(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** `_AuditIndexes`.
5. **Who consumes it?** `build_knowledge_reachability_audit_result(...)` and then candidate evaluation.
6. **Did any compatibility boundary change?** No.
7. **How does this stay inside the Knowledge Reachability district?** It constructs only indexes used by the Knowledge Reachability audit.
8. **How is this distinct from prior Operational Graph slices?** It does not build, summarize, filter, or render Operational Graph structures.
9. **How is this distinct from prior Emitter Attribution Audit slices?** It does not inspect emitter attribution evidence or construct emitter attribution items.
10. **How is this distinct from prior Emitter/Consumer Audit slices?** It does not scan emitted-output relationships or produce audit rows.
11. **How is this distinct from prior Consumer Dependency Audit slices?** It does not build dependency item families or matched groups.
12. **How is this distinct from prior Frontier Pressure Admission slices?** It does not evaluate pressure, fragile/orphaned predicates, or pressure item sets.
13. **How does this avoid Source Navigation direct work?** It only indexes terms already derivable from fact support; it does not invoke Source Navigation query composition.
14. **How does this avoid Question Surface Inventory and bounded ask work?** It does not alter question inventories, dispatch, or bounded ask compatibility.
15. **How does this preserve Knowledge Reachability JSON and table output?** The same result metadata and rows feed unchanged JSON/table renderers.
16. **How does this preserve diagnostic inventory and diagnostic-shape visibility?** No visibility registry/spec changed and diagnostic tests pass.
17. **How does this preserve read-only and event-ledger behavior?** Index construction reads events/state and tests assert no event ledger mutation.
18. **How is this distinct from any earlier slice in this batch?** Slice 001 admits/sorts/caps candidates; this slice constructs indexes for already-admitted candidates to be evaluated against.

## District boundary compliance

The slice remains local to Knowledge Reachability index construction. It avoids Operational Graph, direct Source Navigation work, Question Surface Inventory, bounded ask dispatch, diagnostic registration, CLI dispatch, JSON serialization internals, table formatting internals, and public result assembly.
