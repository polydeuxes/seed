# Frontier Pressure Admission Slice 042

## Selected boundary

Fragile-predicate pressure evidence payload ownership.

## Implementation evidence

Investigation began immediately adjacent to Slice 041 in `seed_runtime/pressure_audit.py`. Slice 041 recovered orphaned-predicate pressure evidence payload assembly from `_orphaned_predicate_pressure(audit)`. The neighboring producer in the same consumer-predicate pressure source is `_fragile_predicate_pressure(audit)`.

`_fragile_predicate_pressure(audit)` still compressed multiple implementation-local responsibilities:

- selecting observation-predicate consumer-audit items with exactly one implementation consumer;
- refusing output when no fragile predicates exist;
- scoring the candidate from the selected item count;
- assembling the fragile-predicate evidence payload fields;
- constructing the `_PressureItemCandidate`.

The directly observable implementation-local responsibility was the fragile-predicate evidence payload assembly: `single-consumer predicates` and `predicates` were built inline in the same return expression that constructs the pressure candidate. This mirrored the already-recovered evidence-payload ownership pattern in diagnostic-shape pressure, ownership pressure, capability pressure, and orphaned-predicate pressure without changing public behavior.

## Before

`_fragile_predicate_pressure(audit)` selected fragile predicate items, refused empty output, scored the pressure candidate, assembled the public evidence dictionary, and constructed the `_PressureItemCandidate` inline.

## After

`_fragile_predicate_pressure(audit)` still owns fragile item selection, empty-output refusal, candidate scoring, reason text, recommended command, and candidate construction. Fragile-predicate pressure evidence payload assembly is now owned by `_fragile_predicate_pressure_evidence(items)`, which returns the same payload shape as before.

## Required questions

1. **What responsibility was previously compressed?**

   Fragile-predicate pressure evidence payload assembly was compressed inside `_fragile_predicate_pressure(audit)` alongside fragile item selection, empty-output refusal, scoring, and candidate construction.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between fragile-predicate pressure candidate construction and fragile-predicate evidence payload assembly became directly observable.

3. **What producer now owns the recovered responsibility?**

   `_fragile_predicate_pressure_evidence(items)` owns fragile-predicate evidence payload assembly.

4. **What artifact or helper carries the recovered boundary, if any?**

   `_fragile_predicate_pressure_evidence(items)` carries the recovered boundary.

5. **Who consumes it?**

   `_fragile_predicate_pressure(audit)` consumes it while constructing the `Fragile Predicates` `_PressureItemCandidate`.

6. **Did any compatibility boundary change?**

   No.

7. **How does this respect the Slice 035 `selection_path_audit` stop marker?**

   This slice did not inspect, modify, or rely on `selection_path_audit`. It stays in `seed_runtime/pressure_audit.py`, outside the exhausted Slice 035 neighborhood, and no compatibility-preserving call-site update in that neighborhood was required.

8. **How is this distinct from the recent upstream pressure-audit recoveries, especially Slice 036 through Slice 041?**

   - Slice 036 recovered candidate admission/filtering/conversion/ordering in `_admitted_pressure_items(...)`; this slice does not change candidate admission.
   - Slice 037 recovered consumer-predicate pressure source admission in `_consumer_predicate_pressures(root)`; this slice does not change the single-audit producer or which predicate pressure producers are admitted from that source.
   - Slice 038 recovered diagnostic-shape pressure evidence payload ownership; this slice does not touch diagnostic-shape summaries or `_diagnostic_shape_pressure_evidence(summary)`.
   - Slice 039 recovered ownership-discrepancy pressure evidence aggregation; this slice does not touch ownership discrepancy rows or `_ownership_pressure_evidence(rows)`.
   - Slice 040 recovered capability pressure evidence payload ownership; this slice does not touch capability needs or `_capability_pressure_evidence(entries)`.
   - Slice 041 recovered orphaned-predicate pressure evidence payload ownership; this slice recovers the neighboring but distinct fragile-predicate evidence payload with its single-consumer predicate fields.

## Recovered producer

- `_fragile_predicate_pressure_evidence(items)`

## Recovered artifact/helper

- `_fragile_predicate_pressure_evidence(items)`

## Recovered consumer

- `_fragile_predicate_pressure(audit)`

## Compatibility preserved

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory, schema, event-ledger behavior, or read-only mutation boundary changed. The helper returns the same evidence dictionary that `_fragile_predicate_pressure(audit)` previously constructed inline.

Expected compatibility answer:

```text
No.
```

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_042.md`

## LOC changed

- `seed_runtime/pressure_audit.py`: 8 inserted lines, 4 removed lines.
- `tests/test_pressure_audit.py`: 17 inserted lines.
- `frontier_pressure_admission_slice_042.md`: 120 inserted lines.

## Tests executed

```text
pytest -q tests/test_pressure_audit.py
```

Result: `12 passed`.

## Remaining compressed responsibilities

Remaining compression, if any, should be selected only from future implementation evidence. In the immediate consumer-predicate pressure area, `_orphaned_predicate_pressure(audit)` still owns orphaned item selection, empty-output refusal, score computation, reason text, recommended command, and candidate construction. `_fragile_predicate_pressure(audit)` still owns fragile item selection, empty-output refusal, score computation, reason text, recommended command, and candidate construction. This slice does not claim those as recovered boundaries.

## Slice 035 stop-marker compliance

The exhausted `selection_path_audit` neighborhood was not reopened. The selected boundary is adjacent to Slice 041 through the implementation order inside `pressure_audit`, and the change remains local to pressure-audit candidate evidence construction plus its direct unit test.

## Distinction from recent upstream pressure-audit slices

This slice recovers exactly one narrower producer/consumer boundary: fragile-predicate pressure evidence payload ownership. It is not pressure candidate admission, source admission, diagnostic-shape evidence, ownership-discrepancy aggregation, capability evidence, or orphaned-predicate evidence. It preserves all pressure-audit outputs while making the next recurring evidence-payload producer explicit from implementation evidence.
