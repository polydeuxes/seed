# Frontier Pressure Admission Slice 029

## Selected boundary

Recovered implementation-local ownership boundary: **non-selected pressure candidate reason preparation inside `selection_path_audit`**.

The selected boundary is the local step where a pressure-selection lineage row explains why an unselected pressure candidate remained non-selected. Current implementation evidence showed that candidate-set payloads, selection factors, typed unknowns, selected-item lookup, pressure-selection lineage payloads, pressure-selection payload bundles, and unsupported-target lineage payload preparation were already named. The smallest adjacent compressed responsibility still present in the current code was inside `_non_selected(...)`: it both assembled the public non-selected row and decided the explanatory reason string for that row.

## Implementation evidence

Investigation began in `seed_runtime/selection_path_audit.py` at `build_selection_path_audit(...)`, the pressure-selection path, and the implementation immediately adjacent to `_unsupported_target_lineage_payload(pressures)`.

Evidence from current implementation:

1. `_unsupported_target_selection(...)` already delegates lineage construction to `_unsupported_target_lineage_payload(pressures)`, so unsupported-target lineage preparation was not eligible for another slice.
2. `_pressure_selection_payloads(...)` already owns pressure-selection payload bundling, and `_pressure_selection_lineage_payload(...)` already owns lineage payload construction.
3. `_non_selected_from_pressures(...)` already owns the non-selected payload container for remaining pressure candidates.
4. `_non_selected(...)` still compressed two responsibilities:
   - assembling the compatibility row with `candidate`, `score`, and `reason` fields;
   - deciding which local reason string applies based on selected-item presence and score comparison.
5. The reason decision is narrower than the row assembly and is implementation-backed by existing public output: lower-score candidates report a lower-score reason, same-score candidates report category-name ordering, and no selected item falls back to generic sorted-earlier explanation.

## Before

`_non_selected(...)` directly computed the non-selected reason string and returned the public row in the same helper. This made row assembly observable, but the reason-preparation responsibility remained compressed inside it.

## After

`_non_selected(...)` now delegates reason preparation to `_non_selected_reason(item, selected_item)`. The new helper owns only the score/selected-item explanation decision and returns the same strings as before. `_non_selected(...)` remains the compatibility row producer and consumes the reason helper while preserving the public JSON and human-readable shape.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_non_selected_reason(item, selected_item)` now produces the non-selected explanatory reason for pressure-selection lineage rows.

## Recovered artifact/helper

`_non_selected_reason(...)` carries the recovered boundary.

## Recovered consumer

`_non_selected(...)` consumes `_non_selected_reason(...)` while assembling the public non-selected row.

## Compatibility preserved

No compatibility boundary changed.

Public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic registration, schema shape, event-ledger behavior, and the read-only selection visibility boundary are preserved. The change only moves an existing implementation-local reason decision behind a named helper and adds direct test coverage for that helper.

Expected compatibility answer:

```text
No.
```

## LOC changed

```text
seed_runtime/selection_path_audit.py | 17 ++++++++++-----
tests/test_selection_path_audit.py   | 40 ++++++++++++++++++++++++++++++++++++
2 files changed, 52 insertions(+), 5 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 142 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   `_non_selected(...)` previously compressed public non-selected row assembly with the decision of which explanatory reason string applies for a non-selected pressure candidate.

2. **Which implementation-local ownership boundary became directly observable?**

   Non-selected pressure candidate reason preparation became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   The implementation added `_non_selected_reason(item, selected_item)` and changed `_non_selected(...)` to consume it. The tests added `test_non_selected_reason_is_owned_by_local_helper()`, which directly exercises lower-score, same-score, and no-selected-item reason cases.

4. **What producer now owns the recovered responsibility?**

   `_non_selected_reason(...)` owns the recovered reason-preparation responsibility.

5. **What artifact or helper carries the recovered boundary, if any?**

   The helper `_non_selected_reason(...)` carries the boundary.

6. **Who consumes it?**

   `_non_selected(...)` consumes it when assembling each non-selected row.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining candidates should continue to be determined only from implementation evidence. After this slice, the pressure-selection non-selected path has named producers for the non-selected payload, individual non-selected row assembly, and non-selected reason preparation. Broader orchestration in `build_selection_path_audit(...)`, target routing, payload handoff, formatting, and compatibility object construction still exist, but this slice does not claim them because the narrowest adjacent compressed responsibility evidenced by the current code was the reason decision inside non-selected row assembly.
