# Frontier Pressure Admission Slice 058

## Selected boundary

Fragile-predicate pressure positive-finding refusal inside `_fragile_predicate_pressure(audit)`.

## Implementation evidence

After Slice 057, `_fragile_predicate_pressure(audit)` filtered single-consumer observation predicates, performed an inline empty-list refusal with `if not items: return None`, then consumed the separated `_fragile_predicate_pressure_score(items)` and `_fragile_predicate_pressure_evidence(items)` producers. The inline refusal was a distinct implementation-local decision: whether the fragile-predicate candidate has findings before candidate construction proceeds.

## Before

`_fragile_predicate_pressure(audit)` owned fragile item filtering, positive-finding refusal, score consumption, evidence consumption, reason text, recommended command selection, and candidate construction. The refusal predicate was not directly observable outside the candidate builder.

## After

`_fragile_predicate_pressure(audit)` still owns filtering and candidate construction, but delegates positive-finding refusal to `_fragile_predicate_pressure_has_findings(items)` and preserves the same `return None` path when no fragile predicate items exist.

## Recovered producer

`_fragile_predicate_pressure_has_findings(items)` now owns fragile-predicate pressure positive-finding refusal.

## Recovered artifact/helper

`_fragile_predicate_pressure_has_findings(items)` carries the recovered implementation-local boundary.

## Recovered consumer

`_fragile_predicate_pressure(audit)` consumes the boolean to preserve the unchanged empty-result candidate refusal path.

## Compatibility preserved

No.

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, or read-only mutation boundary changed. The helper returns the same truth value as the previous inline `if not items` check.

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_058.md`

## LOC changed

Implementation/test diff before this report: 15 insertions and 1 deletion across `seed_runtime/pressure_audit.py` and `tests/test_pressure_audit.py`.

## Tests executed

- `pytest -q tests/test_pressure_audit.py` — 27 passed.

## Required questions

1. What responsibility was previously compressed?
   - Fragile-predicate pressure positive-finding refusal was compressed inside `_fragile_predicate_pressure(audit)` alongside filtering, score consumption, evidence consumption, and candidate construction.
2. Which implementation-local ownership boundary became directly observable?
   - The boolean decision that fragile-predicate pressure has findings became directly observable.
3. What producer now owns the recovered responsibility?
   - `_fragile_predicate_pressure_has_findings(items)`.
4. What artifact or helper carries the recovered boundary, if any?
   - `_fragile_predicate_pressure_has_findings(items)`.
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
   - Slice 053 recovered capability score production; this slice does not touch capability pressure.
   - Slice 054 recovered capability positive-finding refusal; this slice recovers the analogous boundary in the adjacent fragile-predicate producer without touching capability pressure.
   - Slice 055 recovered orphaned-predicate score production; this slice does not touch orphaned score production.
10. How is this distinct from any earlier slice in this batch?
    - Slice 056 recovered orphaned-predicate positive-finding refusal. This slice recovers fragile-predicate positive-finding refusal from a different candidate producer.
    - Slice 057 recovered fragile-predicate score production. This slice recovers the separate boolean refusal decision that consumes the filtered items before score production is used.

## Remaining compressed responsibilities

After this slice, `_fragile_predicate_pressure(audit)` still owns fragile item filtering, reason text, recommended command selection, and candidate construction. The batch stops here because the requested maximum of three slice reports has been produced; any future boundary must be selected only from fresh adjacent implementation evidence.

## Slice 035 stop-marker compliance

No `selection_path_audit` code, tests, behavior, CLI surface, schema, or report neighborhood was reopened.

## Slice 051 stop-marker compliance

No diagnostic-shape pressure candidate-construction code, tests, behavior, CLI surface, schema, or report neighborhood was reopened.

## Distinction from relevant recent upstream slices

This slice recovers only fragile-predicate positive-finding refusal. It does not re-slice ownership-discrepancy score production, capability score production, capability refusal, orphaned-predicate score production, orphaned-predicate refusal, fragile-predicate score production, orphaned evidence payload ownership, fragile evidence payload ownership, or consumer-predicate source admission.

## Distinction from earlier slices in this batch

This slice is distinct from Slice 056 because it acts on the fragile-predicate producer rather than orphaned predicates. It is distinct from Slice 057 because it extracts the boolean finding/refusal predicate rather than numeric score production.
