# Frontier Pressure Admission Slice 045

## Selected boundary

Pressure-audit scalar evidence display ownership.

## Implementation evidence

Investigation began immediately adjacent to Slice 044 in `seed_runtime/pressure_audit.py`. Slice 044 recovered collection evidence display formatting from `_display_evidence(value)` into `_display_collection_evidence(value)`.

The next directly adjacent implementation in `_display_evidence(value)` was the scalar fallback branch. After mapping and collection evidence values are dispatched to their recovered local helpers, `_display_evidence(value)` still directly owned scalar evidence stringification through `str(value)`. Pressure evidence producers emit scalar-valued evidence such as integer counts and dominant-conflict text, and the human-readable formatter consumes those scalar values through the same evidence display dispatch path.

Recovering only the scalar fallback makes the remaining display producer explicit while preserving the exact stringification behavior. This is not a new pressure-admission feature and does not alter ranking, candidate construction, JSON output, CLI behavior, diagnostics, schema, event-ledger behavior, or read-only boundaries.

## Before

`_display_evidence(value)` selected the evidence display strategy and rendered scalar evidence inline with `str(value)` after mapping and collection checks.

## After

`_display_evidence(value)` still owns evidence value-shape dispatch for mappings, collections, and scalars. Scalar evidence display is now owned by `_display_scalar_evidence(value)`, which returns the same `str(value)` representation as before.

## Required questions

1. **What responsibility was previously compressed?**

   Scalar evidence display stringification was compressed inside `_display_evidence(value)` alongside evidence value-shape dispatch.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between pressure-audit evidence display dispatch and scalar evidence display stringification became directly observable.

3. **What producer now owns the recovered responsibility?**

   `_display_scalar_evidence(value)` owns scalar evidence display stringification.

4. **What artifact or helper carries the recovered boundary, if any?**

   `_display_scalar_evidence(value)` carries the recovered boundary.

5. **Who consumes it?**

   `_display_evidence(value)` consumes it for non-mapping, non-collection evidence values, and `format_pressure_audit(audit)` consumes the resulting display text through `_display_evidence(value)`.

6. **Did any compatibility boundary change?**

   No.

7. **How does this respect the Slice 035 `selection_path_audit` stop marker?**

   This slice did not inspect, modify, or rely on `selection_path_audit`. It remains in `seed_runtime/pressure_audit.py`, outside the exhausted Slice 035 neighborhood, and no compatibility-preserving call-site update in that neighborhood was required.

8. **How is this distinct from the recent upstream pressure-audit recoveries, especially Slice 036 through Slice 044?**

   - Slice 036 recovered candidate admission/filtering/conversion/ordering in `_admitted_pressure_items(...)`; this slice does not change candidate admission.
   - Slice 037 recovered consumer-predicate pressure source admission in `_consumer_predicate_pressures(root)`; this slice does not change pressure source admission.
   - Slice 038 recovered diagnostic-shape pressure evidence payload ownership; this slice does not touch diagnostic-shape summaries or `_diagnostic_shape_pressure_evidence(summary)`.
   - Slice 039 recovered ownership-discrepancy pressure evidence aggregation; this slice does not touch ownership discrepancy rows or `_ownership_pressure_evidence(rows)`.
   - Slice 040 recovered capability pressure evidence payload ownership; this slice does not touch capability needs or `_capability_pressure_evidence(entries)`.
   - Slice 041 recovered orphaned-predicate pressure evidence payload ownership; this slice does not touch orphaned-predicate item payloads or `_orphaned_predicate_pressure_evidence(items)`.
   - Slice 042 recovered fragile-predicate pressure evidence payload ownership; this slice does not touch fragile-predicate item payloads or `_fragile_predicate_pressure_evidence(items)`.
   - Slice 043 recovered mapping evidence display formatting; this slice does not re-slice mapping display.
   - Slice 044 recovered collection evidence display formatting; this slice does not re-slice collection display and recovers only the adjacent scalar fallback branch.

## Recovered producer

- `_display_scalar_evidence(value)`

## Recovered artifact/helper

- `_display_scalar_evidence(value)`

## Recovered consumer

- `_display_evidence(value)`, and through it `format_pressure_audit(audit)`.

## Compatibility preserved

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory, schema, event-ledger behavior, or read-only mutation boundary changed. The helper returns the same scalar evidence string that `_display_evidence(value)` previously constructed inline with `str(value)`.

Expected compatibility answer:

```text
No.
```

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_045.md`

## LOC changed

- `seed_runtime/pressure_audit.py`: 5 inserted lines, 1 removed line.
- `tests/test_pressure_audit.py`: 7 inserted lines.
- `frontier_pressure_admission_slice_045.md`: 123 inserted lines.

## Tests executed

```text
python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py
pytest -q tests/test_pressure_audit.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Results:

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` passed; 2 files left unchanged.
- `pytest -q tests/test_pressure_audit.py` passed; 15 tests.
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` passed; 104 tests.

## Remaining compressed responsibilities

Remaining compression, if any, should be selected only from future implementation evidence. In the immediate pressure-audit display area, `_display_evidence(value)` now owns only evidence value-shape dispatch across the recovered mapping, collection, and scalar display helpers. This slice does not claim dispatch itself as a recovered boundary.

## Slice 035 stop-marker compliance

The exhausted `selection_path_audit` neighborhood was not reopened. The selected boundary is adjacent to Slice 044 through the implementation order inside `pressure_audit`, and the change remains local to pressure-audit display formatting plus its direct unit test.

## Distinction from recent upstream pressure-audit slices

This slice recovers exactly one narrower producer/consumer boundary: scalar evidence display stringification for pressure-audit human-readable output. It is not pressure candidate admission, pressure source admission, any pressure evidence payload producer, the mapping display formatter recovered by Slice 043, or the collection display formatter recovered by Slice 044. It preserves all pressure-audit outputs while making the next implementation-evidenced formatting owner explicit.
