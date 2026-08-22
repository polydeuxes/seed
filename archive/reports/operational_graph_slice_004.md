# Operational Graph Slice 004 — Graph node registry / node creation

## District consistency gate

- Active district verified: **Operational Graph**.
- Latest relevant completed slice verified: **`operational_graph_slice_003.md`**.
- Latest local district scout verified: **`operational_graph_district_scout_001.md`**.
- No branch state or local file pointed to another active district.

## Selected boundary

Graph node registry / node creation.

## Implementation evidence

`build_operational_graph(...)` kept a local node registry and a nested `node(...)` factory that constructed stable ids from kind and label, de-duplicated nodes, constructed `OperationalGraphNode` values, applied `_node_classification(...)`, and returned the node id to graph composition helpers.

## Before

The node registry ownership was compressed inside `build_operational_graph(...)` beside graph orchestration and audit composition calls.

## After

`_operational_graph_node_id(...)` owns stable node id construction, node de-duplication, node value construction, classification application, and id return. `build_operational_graph(...)` keeps orchestration and delegates node registration through its existing callback shape.

## Recovered producer

`_operational_graph_node_id(...)`.

## Recovered artifact/helper

Private helper `_operational_graph_node_id(nodes, kind, label)`.

## Recovered consumer

The local `node(...)` callback inside `build_operational_graph(...)`, which is consumed by `_compose_emitter_consumer_audit_graph(...)` and `_compose_consumer_dependency_audit_graph(...)`.

## Compatibility preserved

No.

Public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory behavior, diagnostic shape-audit behavior, schema, node counts, edge counts, relationship-type counts, confidence counts, evidence entries, evidence ordering, sorted graph output, confidence analysis output, taxonomy output, event-ledger behavior, and read-only mutation boundaries are preserved.

## Files changed

- `seed_runtime/operational_graph.py`
- `tests/test_operational_graph.py`
- `operational_graph_slice_004.md`

## LOC changed

Implementation-local extraction plus focused regression test and this report.

## Tests executed

- `pytest -q tests/test_operational_graph.py`

## Remaining compressed responsibilities

After this slice, adjacent graph-builder evidence still showed duplicate-edge insertion/merge behavior compressed in `build_operational_graph(...)`, justifying reassessment for Slice 005.

## Required questions

1. Previously compressed responsibility: stable node id construction, node de-duplication, `OperationalGraphNode` construction, classification, and id return.
2. Directly observable boundary: shared Operational Graph node registry ownership.
3. Producer: `_operational_graph_node_id(...)`.
4. Artifact/helper: private helper `_operational_graph_node_id(nodes, kind, label)`.
5. Consumer: the `node(...)` callback in `build_operational_graph(...)` and the graph composition helpers using that callback.
6. Compatibility boundary changed: No.
7. District containment: it only constructs Operational Graph nodes inside the Operational Graph builder.
8. Distinct from Slice 001: it does not consume Emitter/Consumer Audit items or compose emitter/consumer audit relationships.
9. Distinct from Slice 002: it does not consume Consumer Dependency Audit items or compose consumer dependency relationships.
10. Distinct from Slice 003: it does not assemble confidence tier rows.
11. Distinct from Emitter Attribution Audit slices: it does not classify or construct attribution audit rows.
12. Distinct from Emitter/Consumer Audit slices: it does not scan emitted output, derive relationship status, or produce audit rows.
13. Distinct from Consumer Dependency Audit slices: it does not produce consumer audit item families or matched consumer groups.
14. Distinct from Frontier Pressure Admission slices: it does not admit pressure candidates or produce pressure scores/evidence payloads.
15. Graph JSON schema is preserved because node ids and `OperationalGraphNode.to_json_dict()` output are unchanged.
16. Diagnostic inventory and diagnostic-shape visibility are preserved because no diagnostic surface, registration, CLI flag, or output contract changed.
17. Read-only and event-ledger behavior are preserved because graph metadata remains read-only and no ledger write path was added.
18. Distinct from earlier slices in this batch: this is the first slice in this batch.
