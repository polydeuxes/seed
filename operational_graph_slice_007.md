# Operational Graph Slice 007 — Important low-confidence edge selection

## District consistency gate

- Active district verified: **Operational Graph**.
- Latest relevant completed slice verified: **`operational_graph_slice_006.md`**.
- Latest local district scout verified: **`operational_graph_district_scout_002.md`**.
- No available report, summary, branch state, or local file pointed to another active district.

## Selected boundary

Important low-confidence edge selection.

## Implementation evidence

`build_operational_graph_confidence(...)` still consumed already-filtered Operational Graph edges, sorted those edges by `_edge_sort_key`, selected only low-confidence edges with `_importance(edge)`, projected each selected edge through `_edge_example(edge, include_importance=True)`, and exposed the first ten rows as `important_low_confidence_edges`.

## Before

`build_operational_graph_confidence(...)` directly owned the important-low-confidence list comprehension and the public ten-row limit while also orchestrating graph construction, aggregate-edge filtering, tier summaries, taxonomy inclusion, summary metadata, and public analysis assembly.

## After

`build_operational_graph_confidence(...)` still owns high-level confidence-analysis orchestration and public result assembly, but delegates important-low-confidence edge row selection to `_important_low_confidence_edge_examples(...)`.

## Recovered producer

`_important_low_confidence_edge_examples(...)` now owns selecting operationally relevant low-confidence edge examples from already-filtered graph edges.

## Recovered artifact/helper

`_important_low_confidence_edge_examples(graph_edges)` carries the recovered boundary. It preserves sorted traversal, low-confidence filtering, importance filtering, projected example rows with importance, and the ten-row public limit.

## Recovered consumer

`build_operational_graph_confidence(...)` consumes the selected rows and exposes them under the unchanged `important_low_confidence_edges` JSON key.

## Compatibility preserved

No compatibility boundary changed.

The public JSON key, row shape, row ordering, ten-row limit, summary counts, confidence tier output, taxonomy inclusion, human-readable section, CLI behavior, read-only metadata, event-ledger behavior, diagnostic inventory behavior, and diagnostic-shape behavior remain unchanged.

## Files changed

- `seed_runtime/operational_graph.py`
- `tests/test_operational_graph.py`
- `operational_graph_slice_007.md`

## LOC changed

Before adding this report, implementation and test diff was 83 insertions and 6 deletions:

- `seed_runtime/operational_graph.py`: 12 insertions, 6 deletions.
- `tests/test_operational_graph.py`: 71 insertions, 0 deletions.

## Tests executed

- `pytest -q tests/test_operational_graph.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 137 tests.

## Remaining compressed responsibilities

Directly evident remaining responsibilities in `build_operational_graph_confidence(...)` include selected-tier orchestration, summary construction, taxonomy inclusion, metadata pass-through, and public analysis assembly. They were not recovered in this slice.

## District boundary compliance

This slice stays inside the Operational Graph district because it only analyzes completed Operational Graph edges after graph construction and aggregate-edge filtering. It does not modify upstream audits, CLI dispatch, diagnostic registration, event ledger behavior, schema, taxonomy internals, formatting internals, graph node creation, or graph edge merging.

## Required questions

1. **What responsibility was previously compressed?** Selecting operationally relevant low-confidence edge examples from filtered graph edges, including sorting, low-confidence filtering, importance filtering, row projection with importance, and ten-row limiting.
2. **Which implementation-local ownership boundary became directly observable?** Important low-confidence edge example selection inside Operational Graph confidence analysis.
3. **What producer now owns the recovered responsibility?** `_important_low_confidence_edge_examples(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** The private helper `_important_low_confidence_edge_examples(graph_edges)`.
5. **Who consumes it?** `build_operational_graph_confidence(...)`.
6. **Did any compatibility boundary change?** No.
7. **How does this stay inside the Operational Graph district?** It only consumes already-filtered Operational Graph edges and returns rows for the existing Operational Graph confidence analysis.
8. **How is this distinct from Operational Graph Slice 001 emitter/consumer audit graph composition?** Slice 001 composes graph nodes and edges from Emitter/Consumer Audit items; this slice only selects examples from completed graph edges.
9. **How is this distinct from Operational Graph Slice 002 consumer-dependency audit graph composition?** Slice 002 composes graph nodes and low-confidence consumes edges from Consumer Dependency Audit items; this slice does not compose edges or inspect audit items.
10. **How is this distinct from Operational Graph Slice 003 confidence tier row assembly?** Slice 003 builds tier summaries; this slice only builds the separate `important_low_confidence_edges` example list.
11. **How is this distinct from Operational Graph Slice 004 graph node registry / node creation?** Slice 004 owns node identifiers and node creation; this slice does not create or classify nodes.
12. **How is this distinct from Operational Graph Slice 005 graph edge registry / duplicate-edge merging?** Slice 005 owns edge accumulation and duplicate merging; this slice only reads finished edges.
13. **How is this distinct from Operational Graph Slice 006 confidence aggregate-edge filtering?** Slice 006 chooses which edges remain when aggregate exclusion is requested; this slice consumes those already-filtered edges and does not decide aggregate inclusion.
14. **How is this distinct from prior Emitter Attribution Audit slices?** It does not classify emitters, collect implementation evidence, construct attribution rows, or alter Emitter Attribution Audit output.
15. **How is this distinct from prior Emitter/Consumer Audit slices?** It does not collect scan results, derive relationship status, build unknown-emitter rows, build scanned emitted-item rows, or assemble that audit.
16. **How is this distinct from prior Consumer Dependency Audit slices?** It does not produce observation-predicate families, diagnostic item families, or matched consumer groups.
17. **How is this distinct from prior Frontier Pressure Admission slices?** It does not admit pressure candidates, fan out predicate sources, produce pressure scores, select pressure item sets, or add planning/action/readiness behavior.
18. **How does this preserve graph confidence JSON schema?** `important_low_confidence_edges` remains in the same analysis dictionary with the same projected row structure and the same ten-row limit.
19. **How does this preserve diagnostic inventory and diagnostic-shape visibility?** No diagnostic surface, CLI flag, recordability, or shape registration changed; the required diagnostic inventory and shape-audit tests still pass.
20. **How does this preserve read-only and event-ledger behavior?** The helper is pure selection over an in-memory edge tuple, and tests prove confidence analysis still leaves the event ledger unchanged with `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`.

## Focused test coverage

The new focused test proves the helper consumes an already-filtered edge tuple, sorts by `_edge_sort_key`, keeps only low-confidence edges, requires `_importance(edge)`, returns `_edge_example(..., include_importance=True)` rows, and applies the ten-row limit. It also verifies the public confidence analysis still exposes `important_low_confidence_edges`, preserves human-readable output, tier output, aggregate-edge filtering behavior, summary counts, taxonomy inclusion, read-only metadata, and event-ledger non-mutation.
