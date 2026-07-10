# Frontier Pressure Admission Slice 057

## Selected boundary

Fragile-predicate pressure score production inside `_fragile_predicate_pressure(audit)`.

## Implementation evidence

After Slice 056, the next adjacent pressure-audit implementation is `_fragile_predicate_pressure(audit)`. It filters single-consumer observation predicates, refuses empty output, then embedded the numeric score inline as `len(items)` in the `_PressureItemCandidate`. The same count is an implementation-local score producer, distinct from the already separated fragile evidence payload helper.

## Before

`_fragile_predicate_pressure(audit)` owned fragile item filtering, empty-output refusal, score production, evidence consumption, reason text, recommended command selection, and candidate construction.

## After

`_fragile_predicate_pressure(audit)` still owns filtering, refusal, and candidate construction, but delegates score production to `_fragile_predicate_pressure_score(items)` and consumes the returned integer in the unchanged candidate score field.

## Recovered producer

`_fragile_predicate_pressure_score(items)` now owns fragile-predicate pressure score production.

## Recovered artifact/helper

`_fragile_predicate_pressure_score(items)` carries the recovered implementation-local boundary.

## Recovered consumer

`_fragile_predicate_pressure(audit)` consumes the score while constructing the `Fragile Predicates` `_PressureItemCandidate`.

## Compatibility preserved

No.

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, or read-only mutation boundary changed. The helper returns the same `len(items)` value previously embedded inline in the candidate.

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_057.md`

## LOC changed

Implementation/test diff before this report: 17 insertions and 1 deletion across `seed_runtime/pressure_audit.py` and `tests/test_pressure_audit.py`.

## Tests executed

- `pytest -q tests/test_pressure_audit.py` — 26 passed.

## Required questions

1. What responsibility was previously compressed?
   - Fragile-predicate pressure score production was compressed inside `_fragile_predicate_pressure(audit)` alongside filtering, refusal, evidence consumption, and candidate construction.
2. Which implementation-local ownership boundary became directly observable?
   - The integer score production for fragile-predicate pressure became directly observable.
3. What producer now owns the recovered responsibility?
   - `_fragile_predicate_pressure_score(items)`.
4. What artifact or helper carries the recovered boundary, if any?
   - `_fragile_predicate_pressure_score(items)`.
5. Who consumes it?
   - `_fragile_predicate_pressure(audit)`.
6. Did any compatibility boundary change?
   - No.
7. How does this respect the Slice 035 `selection_path_audit` stop marker?
   - This slice touches only the pressure-audit fragile-predicate candidate path and does not inspect or modify the exhausted `selection_path_audit` neighborhood.
8. How does this respect the Slice 051 diagnostic-shape pressure stop marker?
   - This slice does not touch diagnostic-shape pressure candidate construction or the stopped diagnostic-shape pressure pocket.
9. How is this distinct from prior pressure-audit slices, especially Slices 037, 041, 042, and 052–055?
   - Slice 037 recovered consumer-audit source admission; this slice does not change `_consumer_predicate_pressures(root)` or audit collection.
   - Slice 041 recovered orphaned-predicate evidence payload ownership; this slice does not touch orphaned evidence.
   - Slice 042 recovered fragile-predicate evidence payload ownership; this slice leaves `_fragile_predicate_pressure_evidence(items)` and its public payload unchanged.
   - Slice 052 recovered ownership-discrepancy score production; this slice does not touch ownership pressure.
   - Slice 053 recovered capability score production; this slice applies a separate score-production boundary in the adjacent fragile-predicate producer, not capability pressure.
   - Slice 054 recovered capability positive-finding refusal; this slice does not touch refusal logic.
   - Slice 055 recovered orphaned-predicate score production; this slice recovers fragile-predicate score production from a different candidate producer.
10. How is this distinct from any earlier slice in this batch?
    - Slice 056 recovered orphaned-predicate positive-finding refusal. This slice recovers fragile-predicate score production and does not touch orphaned-predicate refusal or score helpers.

## Remaining compressed responsibilities

After this slice, `_fragile_predicate_pressure(audit)` still owns fragile item filtering, empty-output refusal, reason text, recommended command selection, and candidate construction. Adjacent implementation evidence must be reassessed before any later slice.

## Slice 035 stop-marker compliance

No `selection_path_audit` code, tests, behavior, CLI surface, schema, or report neighborhood was reopened.

## Slice 051 stop-marker compliance

No diagnostic-shape pressure candidate-construction code, tests, behavior, CLI surface, schema, or report neighborhood was reopened.

## Distinction from relevant recent upstream slices

This slice recovers only fragile-predicate score production. It does not re-slice ownership-discrepancy score production, capability score production, capability refusal, orphaned-predicate score production, orphaned-predicate refusal, orphaned evidence payload ownership, fragile evidence payload ownership, or consumer-predicate source admission.

## Distinction from earlier slices in this batch

This slice is distinct from Slice 056 because it acts on the fragile-predicate producer and extracts numeric score production, while Slice 056 acted on the orphaned-predicate producer and extracted positive-finding refusal.
