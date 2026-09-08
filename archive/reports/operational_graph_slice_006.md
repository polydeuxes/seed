# Operational Graph Slice 006 — Confidence aggregate-edge filtering

## District consistency gate

- Active district verified: **Operational Graph**.
- Latest relevant completed slice verified: **`operational_graph_slice_003.md`** before the batch and Slices 004-005 inside this batch.
- Latest local district scout verified: **`operational_graph_district_scout_001.md`**.

## Selected boundary

Confidence aggregate-edge filtering.

## Reassessment result

After Slices 004 and 005, `build_operational_graph_confidence(...)` was inspected. Aggregate-edge filtering remained a narrow implementation-local ownership boundary: it only filters completed Operational Graph edges according to aggregate endpoint presence when `exclude_aggregate` is requested. It is not confidence tier row assembly, important low-confidence edge selection, selected-tier orchestration, taxonomy inclusion, summary metadata construction, or public JSON shaping.

## Implementation evidence

`build_operational_graph_confidence(...)` builds the graph, maps nodes by id, and filtered `graph.edges` inline when `exclude_aggregate` was true by checking source and target node aggregate classification.

## Before

Aggregate-edge filtering was compressed inside the public confidence builder.

## After

`_filter_aggregate_operational_graph_edges(...)` owns the aggregate endpoint filtering decision and returns either the original edge tuple for unfiltered behavior or a filtered tuple for aggregate exclusion. `build_operational_graph_confidence(...)` continues to own graph construction, selected-tier orchestration, tier summary calls, important low-confidence edge selection, taxonomy inclusion, summary metadata, and public analysis assembly.

## Recovered producer

`_filter_aggregate_operational_graph_edges(...)`.

## Recovered artifact/helper

Private helper `_filter_aggregate_operational_graph_edges(edges, nodes, *, exclude_aggregate)`.

## Recovered consumer

`build_operational_graph_confidence(...)`.

## Compatibility preserved

No.

## Files changed

- `seed_runtime/operational_graph.py`
- `tests/test_operational_graph.py`
- `operational_graph_slice_006.md`

## LOC changed

Implementation-local extraction plus focused regression test and this report.

## Tests executed

- `pytest -q tests/test_operational_graph.py`

## Remaining compressed responsibilities

No additional narrow Operational Graph recovery was attempted. Taxonomy, formatting, JSON pass-through, CLI dispatch, diagnostic registration, selected-tier orchestration, important low-confidence edge selection, and summary metadata remain untouched.

## Required questions

1. Previously compressed responsibility: filtering completed Operational Graph edges by aggregate endpoint presence when aggregate exclusion is requested.
2. Directly observable boundary: confidence aggregate-edge filtering.
3. Producer: `_filter_aggregate_operational_graph_edges(...)`.
4. Artifact/helper: private helper `_filter_aggregate_operational_graph_edges(...)`.
5. Consumer: `build_operational_graph_confidence(...)`.
6. Compatibility boundary changed: No.
7. District containment: it only analyzes completed Operational Graph edges.
8. Distinct from Slice 001: it does not compose Emitter/Consumer Audit graph relationships.
9. Distinct from Slice 002: it does not compose Consumer Dependency Audit graph relationships.
10. Distinct from Slice 003: it does not assemble confidence tier rows; it only selects the edge tuple passed into tier assembly.
11. Distinct from Emitter Attribution Audit slices: it does not modify attribution audit behavior.
12. Distinct from Emitter/Consumer Audit slices: it does not scan, classify, or assemble emitter/consumer audit rows.
13. Distinct from Consumer Dependency Audit slices: it does not assemble consumer dependency audit rows.
14. Distinct from Frontier Pressure Admission slices: it does not admit or score pressure candidates.
15. Graph JSON schema is preserved because graph objects and confidence analysis keys are unchanged.
16. Diagnostic inventory and diagnostic-shape visibility are preserved because no diagnostic surface or registration changed.
17. Read-only and event-ledger behavior are preserved because summary flags remain read-only/non-mutating and no ledger write path was added.
18. Distinct from earlier slices in this batch: Slice 004 owns node registration, Slice 005 owns edge registration/merge, and this slice owns confidence aggregate-edge filtering.
