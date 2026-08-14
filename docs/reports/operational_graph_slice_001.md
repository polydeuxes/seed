# Operational Graph Slice 001 — Emitter/consumer audit composition

## District consistency gate

- Active district verified: **Operational Graph**.
- Handoff source verified: **`emitter_attribution_audit_outward_scout_004.md`**.
- Completed source district verified: **Emitter Attribution Audit**.
- Latest completed Emitter Attribution Audit slice verified: **`emitter_attribution_audit_slice_004.md`**.
- No available report, summary, branch state, or local file pointed to another active district for this slice.

## Selected boundary

Operational Graph emitter/consumer audit composition.

## Implementation evidence

`build_operational_graph(...)` previously built Emitter/Consumer Audit items, created emitter nodes, event nodes, direct high-confidence `emits` edges, indirect medium-confidence event-to-surface `consumes` edges, and relied on the enclosing duplicate-edge merge behavior in one compressed body.

## Before

The Operational Graph builder directly owned both audit invocation and all Emitter/Consumer Audit item-to-graph composition details.

## After

`_compose_emitter_consumer_audit_graph(...)` owns consuming already-built Emitter/Consumer Audit items and producing the corresponding nodes, emits edges, consumes edges, edge evidence, confidence assignments, and duplicate-edge merge participation through the existing `add_edge` callback.

## Recovered producer

`_compose_emitter_consumer_audit_graph(...)`.

## Recovered artifact/helper

Private helper `_compose_emitter_consumer_audit_graph(audit, *, node, add_edge)`.

## Recovered consumer

`build_operational_graph(...)` consumes the helper output through the shared node and edge collectors.

## Compatibility preserved

No.

Public runtime behavior, CLI behavior, JSON schema, human-readable output, sorted graph output, node counts, edge counts, relationship-type counts, confidence counts, evidence entries, diagnostic inventory behavior, diagnostic-shape behavior, read-only metadata, and event-ledger behavior are preserved.

## Files changed

- `seed_runtime/operational_graph.py`
- `tests/test_operational_graph.py`
- `operational_graph_slice_001.md`

## LOC changed

Implementation and tests were changed as part of the batch; `git diff --stat` for the batch showed `seed_runtime/operational_graph.py` and `tests/test_operational_graph.py` changed. This report is slice-local documentation for the first boundary.

## Tests executed

- `pytest -q tests/test_operational_graph.py`

## Required questions

1. Previously compressed responsibility: consuming completed Emitter/Consumer Audit items and composing Operational Graph nodes, high-confidence emits edges, medium-confidence consumes edges, direct evidence, indirect evidence, confidence assignments, and duplicate-edge merge participation.
2. Directly observable boundary: Emitter/Consumer Audit item-to-Operational Graph composition.
3. Producer: `_compose_emitter_consumer_audit_graph(...)`.
4. Artifact/helper: private helper `_compose_emitter_consumer_audit_graph(audit, *, node, add_edge)`.
5. Consumer: `build_operational_graph(...)`.
6. Did any compatibility boundary change? No.
7. District containment: the helper only composes Operational Graph nodes and edges after the upstream audit already exists.
8. Distinct from Emitter Attribution Audit slices: it does not classify emitters, collect attribution evidence, or construct attribution rows/items.
9. Distinct from Emitter/Consumer Audit slices: it does not scan, classify relationship status, build audit rows, or assemble the Emitter/Consumer Audit.
10. Distinct from Consumer Dependency Audit slices: it does not produce consumer audit item families or matched consumer groups.
11. Distinct from Frontier Pressure Admission slices: it performs no candidate admission, pressure scoring, positive-finding refusal, or item-set selection.
12. Graph JSON schema preserved: node, edge, summary, metadata, evidence, and confidence fields are unchanged.
13. Diagnostic visibility preserved: no diagnostic surface, CLI flag, inventory registration, or shape-audit registration changed.
14. Read-only/event-ledger preserved: metadata remains `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`; focused tests assert no event ledger writes.
15. Distinct from earlier slices in this batch: this is Slice 001, so no earlier Operational Graph batch slice exists.

## Remaining compressed responsibilities

After this slice, consumer-dependency audit composition remained directly evident and compressed in `build_operational_graph(...)`, justifying reassessment for Slice 002.
