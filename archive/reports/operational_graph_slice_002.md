# Operational Graph Slice 002 — Consumer-dependency audit composition

## District consistency gate

- Active district verified: **Operational Graph**.
- Handoff source verified: **`emitter_attribution_audit_outward_scout_004.md`**.
- Completed source district verified: **Emitter Attribution Audit**.
- Latest completed Emitter Attribution Audit slice verified: **`emitter_attribution_audit_slice_004.md`**.
- Slice 001 landed cleanly and reassessment found the consumer-dependency composition boundary still implementation-backed.

## Selected boundary

Operational Graph consumer-dependency audit composition.

## Implementation evidence

`build_operational_graph(...)` previously built Consumer Dependency Audit items, mapped item kinds to graph node kinds, created consumer surface nodes, built reference evidence from `CONSUMER_PATHS`, assigned low confidence, and merged duplicate consumes edges through the enclosing `add_edge` behavior.

## Before

The Operational Graph builder directly owned both Consumer Dependency Audit invocation and item-to-graph composition.

## After

`_compose_consumer_dependency_audit_graph(...)` owns consuming already-built Consumer Dependency Audit items and producing Operational Graph nodes, low-confidence consumes edges, reference evidence, item-kind node mapping, and duplicate-edge merge participation through the existing `add_edge` callback.

## Recovered producer

`_compose_consumer_dependency_audit_graph(...)`.

## Recovered artifact/helper

Private helper `_compose_consumer_dependency_audit_graph(audit, *, node, add_edge)`.

## Recovered consumer

`build_operational_graph(...)` consumes the helper output through the shared node and edge collectors.

## Compatibility preserved

No.

Public runtime behavior, CLI behavior, JSON schema, human-readable output, sorted graph output, node counts, edge counts, relationship-type counts, confidence counts, evidence entries, diagnostic inventory behavior, diagnostic-shape behavior, read-only metadata, and event-ledger behavior are preserved.

## Files changed

- `seed_runtime/operational_graph.py`
- `tests/test_operational_graph.py`
- `operational_graph_slice_002.md`

## LOC changed

Implementation and tests were changed as part of the batch; `git diff --stat` for the batch showed `seed_runtime/operational_graph.py` and `tests/test_operational_graph.py` changed. This report is slice-local documentation for the second boundary.

## Tests executed

- `pytest -q tests/test_operational_graph.py`

## Required questions

1. Previously compressed responsibility: consuming completed Consumer Dependency Audit items and composing item-kind nodes, consumer surface nodes, low-confidence consumes edges, reference evidence, and duplicate-edge merge participation.
2. Directly observable boundary: Consumer Dependency Audit item-to-Operational Graph composition.
3. Producer: `_compose_consumer_dependency_audit_graph(...)`.
4. Artifact/helper: private helper `_compose_consumer_dependency_audit_graph(audit, *, node, add_edge)`.
5. Consumer: `build_operational_graph(...)`.
6. Did any compatibility boundary change? No.
7. District containment: the helper only composes Operational Graph nodes and edges after the upstream audit already exists.
8. Distinct from Emitter Attribution Audit slices: it does not classify emitters, collect attribution evidence, or construct attribution rows/items.
9. Distinct from Emitter/Consumer Audit slices: it does not scan event emissions, derive relationship status, produce unknown-emitter rows, produce scanned rows, or assemble the audit.
10. Distinct from Consumer Dependency Audit slices: it consumes completed audit items; it does not produce observation-predicate item families, diagnostic item families, or matched consumer groups.
11. Distinct from Frontier Pressure Admission slices: it performs no pressure scoring, admission, refusal, or item-set selection.
12. Graph JSON schema preserved: node, edge, summary, metadata, evidence, and confidence fields are unchanged.
13. Diagnostic visibility preserved: no diagnostic surface, CLI flag, inventory registration, or shape-audit registration changed.
14. Read-only/event-ledger preserved: metadata remains `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`; focused tests assert no event ledger writes.
15. Distinct from Slice 001: Slice 001 composes Emitter/Consumer Audit event-emission relationships; this slice composes Consumer Dependency Audit reference-only consumer relationships.

## Remaining compressed responsibilities

After this slice, `build_operational_graph_confidence(...)` still contained a narrow tier-row assembly loop that was not graph composition, taxonomy, CLI plumbing, diagnostic registration, formatting, or JSON shaping. That justified reassessment for Slice 003.
