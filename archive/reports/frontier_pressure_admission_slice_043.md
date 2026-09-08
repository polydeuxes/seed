# Frontier Pressure Admission Slice 043

## Selected boundary

Pressure-audit mapping evidence display ownership.

## Implementation evidence

Investigation began immediately adjacent to Slice 042 in `seed_runtime/pressure_audit.py`. Slice 042 recovered fragile-predicate pressure evidence payload assembly from `_fragile_predicate_pressure(audit)`. The next neighboring implementation is the pressure-audit human-readable evidence formatter.

`format_pressure_audit(audit)` delegates each evidence value to `_display_evidence(value)`. `_display_evidence(value)` still compressed multiple implementation-local responsibilities:

- dispatching by evidence value shape;
- rendering mapping evidence as stable `key=value` pairs;
- rendering list, tuple, and set evidence as comma-separated values;
- rendering scalar evidence through `str(value)`.

The directly observable implementation-local responsibility was mapping evidence display formatting. Pressure evidence producers repeatedly emit dictionaries, and the human-readable formatter has a distinct mapping branch whose output shape is consumed by `format_pressure_audit(audit)`. Recovering that branch preserves the public human-readable output while making the mapping-display owner explicit.

## Before

`_display_evidence(value)` selected the evidence display strategy and rendered mapping evidence inline with `", ".join(f"{key}={val}" for key, val in value.items()) or "none"`.

## After

`_display_evidence(value)` still owns evidence display dispatch for mappings, collections, and scalars. Mapping evidence display is now owned by `_display_mapping_evidence(value)`, which returns the same string shape as before.

## Required questions

1. **What responsibility was previously compressed?**

   Mapping evidence display formatting was compressed inside `_display_evidence(value)` alongside evidence-shape dispatch, collection evidence display, and scalar evidence display.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between pressure-audit evidence display dispatch and mapping evidence display formatting became directly observable.

3. **What producer now owns the recovered responsibility?**

   `_display_mapping_evidence(value)` owns mapping evidence display formatting.

4. **What artifact or helper carries the recovered boundary, if any?**

   `_display_mapping_evidence(value)` carries the recovered boundary.

5. **Who consumes it?**

   `_display_evidence(value)` consumes it when formatting dictionary evidence values for `format_pressure_audit(audit)`.

6. **Did any compatibility boundary change?**

   No.

7. **How does this respect the Slice 035 `selection_path_audit` stop marker?**

   This slice did not inspect, modify, or rely on `selection_path_audit`. It remains in `seed_runtime/pressure_audit.py`, outside the exhausted Slice 035 neighborhood, and no compatibility-preserving call-site update in that neighborhood was required.

8. **How is this distinct from the recent upstream pressure-audit recoveries, especially Slice 036 through Slice 042?**

   - Slice 036 recovered candidate admission/filtering/conversion/ordering in `_admitted_pressure_items(...)`; this slice does not change candidate admission.
   - Slice 037 recovered consumer-predicate pressure source admission in `_consumer_predicate_pressures(root)`; this slice does not change pressure source admission.
   - Slice 038 recovered diagnostic-shape pressure evidence payload ownership; this slice does not touch diagnostic-shape summaries or `_diagnostic_shape_pressure_evidence(summary)`.
   - Slice 039 recovered ownership-discrepancy pressure evidence aggregation; this slice does not touch ownership discrepancy rows or `_ownership_pressure_evidence(rows)`.
   - Slice 040 recovered capability pressure evidence payload ownership; this slice does not touch capability needs or `_capability_pressure_evidence(entries)`.
   - Slice 041 recovered orphaned-predicate pressure evidence payload ownership; this slice does not touch orphaned-predicate item payloads or `_orphaned_predicate_pressure_evidence(items)`.
   - Slice 042 recovered fragile-predicate pressure evidence payload ownership; this slice does not touch fragile-predicate item payloads or `_fragile_predicate_pressure_evidence(items)`.

## Recovered producer

- `_display_mapping_evidence(value)`

## Recovered artifact/helper

- `_display_mapping_evidence(value)`

## Recovered consumer

- `_display_evidence(value)`, and through it `format_pressure_audit(audit)`.

## Compatibility preserved

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory, schema, event-ledger behavior, or read-only mutation boundary changed. The helper returns the same mapping evidence string that `_display_evidence(value)` previously constructed inline.

Expected compatibility answer:

```text
No.
```

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_043.md`

## LOC changed

- `seed_runtime/pressure_audit.py`: 5 inserted lines, 1 removed line.
- `tests/test_pressure_audit.py`: 6 inserted lines.
- `frontier_pressure_admission_slice_043.md`: 117 inserted lines.

## Tests executed

```text
pytest -q tests/test_pressure_audit.py
```

Result: `13 passed`.

## Remaining compressed responsibilities

Remaining compression, if any, should be selected only from future implementation evidence. In the immediate pressure-audit display area, `_display_evidence(value)` still owns value-shape dispatch, collection evidence display, and scalar evidence display. This slice does not claim those as recovered boundaries.

## Slice 035 stop-marker compliance

The exhausted `selection_path_audit` neighborhood was not reopened. The selected boundary is adjacent to Slice 042 through the implementation order inside `pressure_audit`, and the change remains local to pressure-audit display formatting plus its direct unit test.

## Distinction from recent upstream pressure-audit slices

This slice recovers exactly one narrower producer/consumer boundary: mapping evidence display formatting for pressure-audit human-readable output. It is not pressure candidate admission, source admission, or any pressure evidence payload producer. It preserves all pressure-audit outputs while making the next implementation-evidenced formatting owner explicit.
