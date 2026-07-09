# Frontier Pressure Admission Slice 039

Recovered implementation-local ownership boundary: **ownership-discrepancy pressure evidence aggregation inside `pressure_audit`**.

## Selected boundary

The selected boundary is the local handoff where `_ownership_pressure(...)` stops owning the inline conversion from ownership-discrepancy rows into the pressure evidence payload. The mapping is now carried by `_ownership_pressure_evidence(...)` and consumed by `_ownership_pressure(...)` when it builds the unchanged `Ownership Attribution` pressure candidate.

## Implementation evidence

Investigation began in `seed_runtime/pressure_audit.py`, immediately adjacent to Slice 038's diagnostic-shape pressure area. The current implementation already separated:

- pressure candidate admission through `_admitted_pressure_items(...)`;
- consumer-predicate pressure source collection through `_consumer_predicate_pressures(root)`;
- diagnostic-shape pressure evidence payload conversion through `_diagnostic_shape_pressure_evidence(summary)`.

The adjacent still-compressed responsibility was inside `_ownership_pressure(...)`: after collecting conflicting ownership-discrepancy rows and computing the pressure score, it still directly aggregated row kinds, conflict counts, sorted conflict evidence, and dominant conflict in the same function that selected rows, applied the zero-score refusal, and built the pressure candidate.

That evidence payload is material to the public `PressureItem` returned by `build_pressure_audit(...)`, but separating it does not change score computation, candidate admission, CLI output, JSON output, schema, diagnostic behavior, event-ledger behavior, or read-only boundaries.

## Before

`_ownership_pressure(...)` owned all of these at once:

1. collecting conflicted ownership-discrepancy rows from `build_ownership_discrepancies(state)`;
2. computing the pressure score from those rows;
3. refusing candidate construction when the score was non-positive;
4. aggregating evidence fields from the rows:
   - `service ambiguities`;
   - `storage ambiguities`;
   - sorted `conflict counts`;
   - `dominant conflict`;
5. constructing the `_PressureItemCandidate` for `Ownership Attribution`.

The row-to-evidence conversion was only indirectly observable through the full ownership pressure candidate test.

## After

`_ownership_pressure(...)` still owns ownership-pressure row selection, score computation, zero-score refusal, and candidate construction. `_ownership_pressure_evidence(rows)` now owns only the conversion of conflicted ownership-discrepancy rows into the ownership pressure evidence payload. A direct unit test proves the helper's output shape without relying on the full pressure-audit builder or candidate construction.

## Implementation files changed

- `seed_runtime/pressure_audit.py`
  - added `_ownership_pressure_evidence(rows)`;
  - changed `_ownership_pressure(...)` to consume the helper when building the unchanged `Ownership Attribution` pressure candidate.

## Test files changed

- `tests/test_pressure_audit.py`
  - imported `_ownership_pressure_evidence`;
  - added `test_ownership_pressure_evidence_is_owned_by_local_helper` to directly prove the recovered boundary.

## Recovered producer

`_ownership_pressure_evidence(...)` now produces the ownership-discrepancy pressure evidence payload.

## Recovered artifact/helper

Recovered helper: `_ownership_pressure_evidence(rows)`.

Recovered artifact: the unchanged ownership pressure evidence mapping:

```python
{
    "service ambiguities": ...,
    "storage ambiguities": ...,
    "conflict counts": ...,
    "dominant conflict": ...,
}
```

## Recovered consumer

`_ownership_pressure(...)` consumes the helper output while constructing the existing `_PressureItemCandidate` for the `Ownership Attribution` category.

## Compatibility preserved

No.

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic behavior, schema, event-ledger behavior, and read-only mutation boundaries are preserved.

## LOC changed

```text
seed_runtime/pressure_audit.py | 22 +++++++++++++---------
tests/test_pressure_audit.py   | 19 +++++++++++++++++++
2 files changed, 32 insertions(+), 9 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` — passed.
- `pytest -q tests/test_pressure_audit.py tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 156 tests.

## Remaining compressed responsibilities

Remaining responsibilities in `pressure_audit` include diagnostic-shape repo-root compatibility selection, diagnostic-shape score computation, ownership pressure row selection and scoring, capability pressure evidence aggregation, text rendering of nested evidence values, and the outer orchestration in `build_pressure_audit(...)`. They remain untouched because this slice recovered only one smallest implementation-backed boundary and did not select additional candidates.

## Required questions

### 1. What responsibility was previously compressed?

Ownership-discrepancy pressure evidence aggregation was compressed inside `_ownership_pressure(...)` along with row selection, score computation, zero-score refusal, and pressure-candidate construction.

### 2. Which implementation-local ownership boundary became directly observable?

The boundary between ownership-pressure candidate construction and row-to-evidence payload conversion became directly observable.

### 3. What implementation and/or test change made the boundary observable?

Implementation added `_ownership_pressure_evidence(rows)` and changed `_ownership_pressure(...)` to consume it. Test coverage added `test_ownership_pressure_evidence_is_owned_by_local_helper`, which directly asserts the evidence payload produced from representative ownership discrepancy rows.

### 4. What producer now owns the recovered responsibility?

`_ownership_pressure_evidence(...)` owns ownership pressure evidence payload production.

### 5. What artifact or helper carries the recovered boundary, if any?

The helper `_ownership_pressure_evidence(rows)` carries the recovered boundary.

### 6. Who consumes it?

`_ownership_pressure(...)` consumes it when constructing the existing `Ownership Attribution` `_PressureItemCandidate`.

### 7. Did any compatibility boundary change?

No.

### 8. How does this respect the Slice 035 `selection_path_audit` stop marker?

This slice does not touch `selection_path_audit` implementation or tests. The recovered boundary is in `pressure_audit`, upstream from the exhausted `selection_path_audit` neighborhood, and it does not reopen any Slice 035 stopped boundary.

### 9. How is this distinct from Slice 036 pressure candidate admission?

Slice 036 recovered the admission rule that filters absent/non-positive candidates, converts candidates to public `PressureItem` records, and orders admitted pressure items. This slice does not change or re-slice admission. It recovers only the ownership-discrepancy evidence payload produced before an ownership candidate reaches `_admitted_pressure_items(...)`.

### 10. How is this distinct from Slice 037 consumer-predicate pressure source admission?

Slice 037 recovered consumer-audit source collection and fan-out into orphaned/fragile predicate pressure candidates. This slice does not call, alter, or re-slice `_consumer_predicate_pressures(root)`, `_orphaned_predicate_pressure(...)`, or `_fragile_predicate_pressure(...)`. It recovers an ownership-discrepancy evidence payload in a different producer path.

### 11. How is this distinct from Slice 038 diagnostic-shape pressure evidence payload ownership?

Slice 038 recovered diagnostic-shape summary-to-evidence conversion through `_diagnostic_shape_pressure_evidence(summary)`. This slice does not alter or re-slice diagnostic-shape evidence. It recovers ownership-discrepancy row-to-evidence conversion through `_ownership_pressure_evidence(rows)`, using a different input producer and different evidence shape.

## Stop marker and prior-slice avoidance summary

- Slice 035 respected: no `selection_path_audit` implementation or tests were touched.
- Slice 036 avoided: `_admitted_pressure_items(...)` and pressure admission behavior were left unchanged.
- Slice 037 avoided: `_consumer_predicate_pressures(root)` and its orphaned/fragile predicate producers were left unchanged.
- Slice 038 avoided: `_diagnostic_shape_pressure_evidence(summary)` and diagnostic-shape pressure behavior were left unchanged.
