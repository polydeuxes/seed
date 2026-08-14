# Frontier Pressure Admission Slice 061

## Selected boundary

Orphaned-predicate item-set selection inside `_orphaned_predicate_pressure(audit)`.

## Implementation evidence

`_orphaned_predicate_pressure(audit)` consumed `ConsumerAudit.items` with a category-specific predicate: `item.kind == "observation_predicate" and item.orphaned`. That selection feeds the already separated orphaned-predicate finding refusal, score, and evidence producers.

## Before

`_orphaned_predicate_pressure(audit)` owned orphaned item-set selection, positive-finding refusal, score consumption, evidence consumption, reason text, recommended command selection, and candidate construction.

## After

`_orphaned_predicate_pressure(audit)` delegates only orphaned item-set selection to `_orphaned_predicate_pressure_items(audit)`, then continues to consume the returned items through unchanged finding refusal, score, evidence, and candidate construction paths.

## Recovered producer

`_orphaned_predicate_pressure_items(audit)` now owns orphaned-predicate item-set selection.

## Recovered artifact/helper

`_orphaned_predicate_pressure_items(audit)` carries the recovered implementation-local boundary.

## Recovered consumer

`_orphaned_predicate_pressure(audit)` consumes the selected item list.

## Compatibility preserved

No.

The helper preserves the existing selection predicate, item order, public fields, CLI behavior, JSON shape, diagnostics, schema, event-ledger behavior, and read-only boundaries.

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_061.md`

## LOC changed

Implementation/test diff before this report: 54 insertions and 5 deletions across `seed_runtime/pressure_audit.py` and `tests/test_pressure_audit.py`.

## Tests executed

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` — passed.
- `pytest -q tests/test_pressure_audit.py` — passed, 31 tests.

## Remaining compressed responsibilities

After this slice, `_orphaned_predicate_pressure(audit)` still owns orphaned-predicate candidate construction, reason text, and recommended command selection. Adjacent implementation evidence shows the parallel fragile-predicate item-set selection remains inline in `_fragile_predicate_pressure(audit)` and may be considered separately only if it is not a re-slice and remains implementation-backed.

## Required questions

1. What responsibility was previously compressed?
   - Orphaned-predicate item-set selection was compressed inside `_orphaned_predicate_pressure(audit)` alongside candidate construction and the already separated orphaned-predicate finding, score, and evidence paths.
2. Which implementation-local ownership boundary became directly observable?
   - The category-specific selection of consumer-audit rows matching `item.kind == "observation_predicate" and item.orphaned`.
3. What producer now owns the recovered responsibility?
   - `_orphaned_predicate_pressure_items(audit)`.
4. What artifact or helper carries the recovered boundary, if any?
   - `_orphaned_predicate_pressure_items(audit)`.
5. Who consumes it?
   - `_orphaned_predicate_pressure(audit)`.
6. Did any compatibility boundary change?
   - No.
7. How does this respect the Slice 035 `selection_path_audit` stop marker?
   - This slice does not inspect, modify, or rely on `selection_path_audit`. The only implementation change is local to `pressure_audit` consumer-predicate item selection.
8. How does this respect the Slice 051 diagnostic-shape pressure stop marker?
   - This slice does not inspect, modify, or rely on diagnostic-shape pressure candidate construction. The recovered boundary is in the consumer-predicate producer neighborhood.
9. How is this distinct from Slice 037 consumer-predicate source admission?
   - Slice 037 recovered the single `build_consumer_audit(root)` source handoff and fan-out. This slice starts after that fan-out and recovers only one category-specific item-set selector over an already provided `ConsumerAudit`.
10. How is this distinct from Slice 041 or Slice 042 evidence payload ownership?
    - Slice 041 recovered orphaned-predicate evidence payload assembly and Slice 042 recovered fragile-predicate evidence payload assembly. This slice leaves evidence payload production unchanged and recovers only the selected input item set for orphaned predicates.
11. How is this distinct from Slices 055 through 058 score/refusal ownership?
    - Slices 055 through 058 recovered score production and positive-finding refusal. This slice does not alter score or refusal helpers; it recovers the input item-set producer consumed by those helpers.
12. How is this distinct from any earlier slice in this batch?
    - This is the first slice in this batch.

## Slice 035 stop-marker compliance

The exhausted `selection_path_audit` neighborhood remains untouched. No selection-path route ordering, payloads, selected pressure evidence records, or target matching code changed.

## Slice 051 stop-marker compliance

The diagnostic-shape pressure neighborhood remains untouched. No diagnostic-shape summary, score, refusal, evidence, or candidate construction code changed.

## Distinction from relevant prior slices

This slice is not source admission, evidence payload ownership, score ownership, positive-finding refusal, candidate construction, reason text, command literal, or presentation formatting. It recovers only the orphaned-predicate item-set selection boundary directly evidenced by the existing inline predicate.
