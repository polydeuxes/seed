# Operational Graph Slice 005 — Graph edge registry / duplicate-edge merging

## District consistency gate

- Active district verified: **Operational Graph**.
- Latest relevant completed slice verified: **`operational_graph_slice_003.md`** before the batch and **`operational_graph_slice_004.md`** inside this batch.
- Latest local district scout verified: **`operational_graph_district_scout_001.md`**.

## Selected boundary

Graph edge registry / duplicate-edge merging.

## Implementation evidence

After Slice 004, `build_operational_graph(...)` still kept a local edge accumulator and nested `add_edge(...)` callback that omitted evidence-free edges, keyed edges by `(source, target, edge_type)`, inserted `OperationalGraphEdge` values, merged duplicate evidence with order-preserving de-duplication, and preserved stronger confidence.

## Before

Duplicate-edge ownership was compressed inside `build_operational_graph(...)` beside graph orchestration.

## After

`_add_operational_graph_edge(...)` owns evidence-free omission, edge key construction, edge insertion, duplicate evidence merge ordering, and stronger-confidence preservation. `build_operational_graph(...)` keeps orchestration and delegates edge registration through its existing callback shape.

## Recovered producer

`_add_operational_graph_edge(...)`.

## Recovered artifact/helper

Private helper `_add_operational_graph_edge(edges, source, target, edge_type, evidence, confidence)`.

## Recovered consumer

The local `add_edge(...)` callback inside `build_operational_graph(...)`, consumed by the Operational Graph composition helpers.

## Compatibility preserved

No.

## Files changed

- `seed_runtime/operational_graph.py`
- `tests/test_operational_graph.py`
- `operational_graph_slice_005.md`

## LOC changed

Implementation-local extraction plus focused regression test and this report.

## Tests executed

- `pytest -q tests/test_operational_graph.py`

## Remaining compressed responsibilities

After this slice, reassessment found aggregate-edge filtering still locally compressed in `build_operational_graph_confidence(...)` and separate from confidence tier row assembly, important low-confidence selection, selected-tier orchestration, taxonomy inclusion, summary metadata construction, and JSON shaping.

## Required questions

1. Previously compressed responsibility: evidence-free edge omission, edge keying, new edge construction, duplicate evidence merging, and stronger-confidence merge behavior.
2. Directly observable boundary: shared Operational Graph edge registry ownership.
3. Producer: `_add_operational_graph_edge(...)`.
4. Artifact/helper: private helper `_add_operational_graph_edge(...)`.
5. Consumer: the `add_edge(...)` callback in `build_operational_graph(...)` and graph composition helpers using that callback.
6. Compatibility boundary changed: No.
7. District containment: it only constructs and merges Operational Graph edges inside the Operational Graph builder.
8. Distinct from Slice 001: it does not compose Emitter/Consumer Audit-specific graph relationships.
9. Distinct from Slice 002: it does not compose Consumer Dependency Audit-specific graph relationships.
10. Distinct from Slice 003: it does not assemble confidence tier rows.
11. Distinct from Emitter Attribution Audit slices: it does not modify attribution classification, evidence collection, or item construction.
12. Distinct from Emitter/Consumer Audit slices: it does not scan or produce Emitter/Consumer Audit rows.
13. Distinct from Consumer Dependency Audit slices: it does not produce Consumer Dependency Audit rows or consumer groups.
14. Distinct from Frontier Pressure Admission slices: it does not admit pressure candidates, score pressure, or create pressure evidence payloads.
15. Graph JSON schema is preserved because `OperationalGraphEdge` fields and serialization are unchanged.
16. Diagnostic inventory and diagnostic-shape visibility are preserved because no diagnostic registration or shape spec changed.
17. Read-only and event-ledger behavior are preserved because graph metadata and ledger behavior are unchanged.
18. Distinct from Slice 004: Slice 004 owns nodes; this slice owns edge insertion and duplicate merging.
