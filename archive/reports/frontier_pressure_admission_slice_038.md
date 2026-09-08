# Frontier Pressure Admission Slice 038

Recovered implementation-local ownership boundary: **diagnostic-shape pressure evidence payload ownership inside `pressure_audit`**.

## Selected boundary

The selected boundary is the local handoff where `_diagnostic_shape_pressure(...)` stops owning the inline conversion from a `DiagnosticShapeAuditSummary` into the pressure-candidate evidence payload. The mapping is now carried by `_diagnostic_shape_pressure_evidence(...)` and consumed by `_diagnostic_shape_pressure(...)` when it builds the unchanged `Diagnostic Shape` pressure candidate.

This is exactly one implementation-local responsibility: projecting diagnostic-shape summary counts into the `PressureItem` evidence keys used by the pressure audit.

## Implementation evidence

Investigation began in `seed_runtime/pressure_audit.py`, immediately adjacent to Slice 037's `_consumer_predicate_pressures(root)` fan-out. The current implementation already separated:

- pressure candidate admission through `_admitted_pressure_items(...)`;
- consumer-predicate pressure source collection through `_consumer_predicate_pressures(root)`;
- orphaned-predicate candidate construction through `_orphaned_predicate_pressure(...)`;
- fragile-predicate candidate construction through `_fragile_predicate_pressure(...)`.

The adjacent still-compressed responsibility was inside `_diagnostic_shape_pressure(...)`: after collecting and summarizing the diagnostic-shape audit, it still directly assembled the evidence payload keys (`mismatches`, `warnings`, `unknowns`) in the same function that selected the repo root, computed pressure score, applied the zero-score refusal, and built the pressure candidate.

That evidence payload is material to pressure admission because it is part of the public `PressureItem` returned by `build_pressure_audit(...)`, but separating it does not change score computation, candidate admission, CLI output, JSON output, schema, diagnostic behavior, event-ledger behavior, or read-only boundaries.

## Before

`_diagnostic_shape_pressure(...)` owned all of these at once:

1. diagnostic-shape repo-root compatibility selection;
2. diagnostic-shape audit execution;
3. diagnostic-shape summary creation;
4. pressure score computation;
5. zero-score non-admission;
6. diagnostic-shape evidence payload assembly;
7. `Diagnostic Shape` pressure-candidate construction.

The evidence payload conversion was only indirectly observable through aggregate pressure-audit output.

## After

`_diagnostic_shape_pressure(...)` still owns audit collection, scoring, zero-score refusal, and candidate construction. `_diagnostic_shape_pressure_evidence(summary)` now owns only the conversion of the diagnostic-shape summary into the pressure evidence payload. A direct unit test proves the helper's output shape without relying on the full pressure-audit builder.

## Implementation files changed

- `seed_runtime/pressure_audit.py`
  - imported `DiagnosticShapeAuditSummary` for the local helper type;
  - added `_diagnostic_shape_pressure_evidence(summary)`;
  - changed `_diagnostic_shape_pressure(...)` to consume the helper when building the unchanged `Diagnostic Shape` pressure candidate.

## Test files changed

- `tests/test_pressure_audit.py`
  - imported `DiagnosticShapeAuditSummary` and `_diagnostic_shape_pressure_evidence`;
  - added `test_diagnostic_shape_pressure_evidence_is_owned_by_local_helper` to directly prove the recovered boundary.

## Recovered producer

`_diagnostic_shape_pressure_evidence(...)` now produces the diagnostic-shape pressure evidence payload.

## Recovered artifact/helper

Recovered helper: `_diagnostic_shape_pressure_evidence(summary)`.

Recovered artifact: the pressure evidence dictionary containing:

- `mismatches`;
- `warnings`;
- `unknowns`.

## Recovered consumer

`_diagnostic_shape_pressure(...)` consumes the helper output while constructing the existing `_PressureItemCandidate` for the `Diagnostic Shape` category.

## Compatibility preserved

No.

No compatibility boundary changed. Public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory, diagnostic shape-audit behavior, schema, event-ledger behavior, and read-only mutation boundaries are preserved.

## LOC changed

`git diff --stat` reported:

```text
seed_runtime/pressure_audit.py | 18 ++++++++++++------
tests/test_pressure_audit.py   | 22 +++++++++++++++++++++-
2 files changed, 33 insertions(+), 7 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` — passed.
- `pytest -q tests/test_pressure_audit.py tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 155 tests.

## Required questions

### 1. What responsibility was previously compressed?

Diagnostic-shape pressure evidence payload assembly was compressed inside `_diagnostic_shape_pressure(...)` along with audit collection, summary scoring, zero-score refusal, and pressure-candidate construction.

### 2. Which implementation-local ownership boundary became directly observable?

The boundary between diagnostic-shape summary production and diagnostic-shape pressure evidence payload production became directly observable.

### 3. What implementation and/or test change made the boundary observable?

Implementation added `_diagnostic_shape_pressure_evidence(summary)` and changed `_diagnostic_shape_pressure(...)` to consume it. Test coverage added `test_diagnostic_shape_pressure_evidence_is_owned_by_local_helper`, which directly asserts the evidence payload produced from a `DiagnosticShapeAuditSummary`.

### 4. What producer now owns the recovered responsibility?

`_diagnostic_shape_pressure_evidence(...)` owns diagnostic-shape pressure evidence payload production.

### 5. What artifact or helper carries the recovered boundary, if any?

The helper `_diagnostic_shape_pressure_evidence(summary)` carries the recovered boundary.

### 6. Who consumes it?

`_diagnostic_shape_pressure(...)` consumes it when constructing the existing `Diagnostic Shape` `_PressureItemCandidate`.

### 7. Did any compatibility boundary change?

No.

### 8. How does this respect the Slice 035 `selection_path_audit` stop marker?

This slice does not touch `selection_path_audit` implementation or tests. The recovered boundary is in `pressure_audit`, one upstream implementation area already adjacent to the pressure output consumed by selection-path audit, and it does not reopen the exhausted Slice 035 neighborhood.

### 9. How is this distinct from Slice 036 pressure candidate admission?

Slice 036 recovered the admission rule that filters absent/non-positive candidates, converts candidates to public `PressureItem` records, and orders admitted pressure items. This slice does not change or re-slice admission. It recovers only the diagnostic-shape evidence payload produced before a diagnostic-shape candidate reaches `_admitted_pressure_items(...)`.

### 10. How is this distinct from Slice 037 consumer-predicate pressure source admission?

Slice 037 recovered the consumer-audit source collection and fan-out into orphaned/fragile predicate pressure candidates. This slice does not call, alter, or re-slice `_consumer_predicate_pressures(root)`, `_orphaned_predicate_pressure(...)`, or `_fragile_predicate_pressure(...)`. It recovers the diagnostic-shape pressure evidence payload in a different producer path.

## Remaining compressed responsibilities

Remaining responsibilities in `pressure_audit` include diagnostic-shape repo-root compatibility selection, diagnostic-shape score computation, ownership discrepancy evidence aggregation, capability pressure evidence aggregation, text rendering of nested evidence values, and the outer orchestration in `build_pressure_audit(...)`. They remain untouched because this slice recovered only one smallest implementation-backed boundary and did not select additional candidates.

## Stop marker and prior-slice compliance

- Slice 035 stop marker respected: no `selection_path_audit` file or test was changed.
- Slice 036 avoided: `_admitted_pressure_items(...)` and pressure admission behavior were left unchanged.
- Slice 037 avoided: `_consumer_predicate_pressures(root)` and its orphaned/fragile predicate producers were left unchanged.

## Constitutional guardrail

This slice only makes an existing read-only pressure evidence conversion observable in implementation. It does not introduce acceptance authority, reliance authority, action authority, mutation authority, execution authority, planning, prioritization, inquiry generation, route authority, autonomous next-step selection, a framework, an engine, a registry, a methodology owner, a planner, a scheduler, an ontology, or an architectural redesign.
