# Frontier Pressure Admission Slice 016

## Selected boundary

Pressure-category selection path assembly is now owned by a local implementation helper, `_from_pressure_category_selection(...)`.

## Implementation evidence

`build_selection_path_audit(...)` already had a distinct pressure-category target branch after `_target_matches_pressure_category(...)`. That branch performed three local responsibilities inline:

1. locate the selected pressure item from pressure-audit ordering;
2. prepare the pressure-category selected name using the pressure-category selected-name helper;
3. hand the prepared selection into the existing pressure-selection compatibility handoff.

The target match was already separated, and the selected-name preparation was already separated. The remaining compressed responsibility was the pressure-category branch assembling the pressure-category selection path before returning to the generic pressure-selection handoff.

## Before

The pressure-category target branch in `build_selection_path_audit(...)` directly looked up `selected_item`, called `_pressure_category_selection_selected_name(...)`, and called `_from_pressure_selection(...)` inline. The branch therefore owned both orchestration and pressure-category selection path assembly.

## After

`build_selection_path_audit(...)` now delegates pressure-category selection path assembly to `_from_pressure_category_selection(...)`. The helper owns selected pressure item lookup for the pressure-category branch, pressure-category selected-name preparation, and the existing handoff into `_from_pressure_selection(...)`.

## Required questions

1. **What responsibilities were previously compressed?**
   Pressure-category branch routing, selected pressure item lookup, pressure-category selected-name preparation, and pressure-selection audit construction were compressed in the `build_selection_path_audit(...)` pressure-category branch.

2. **Which implementation-local ownership boundary became directly observable?**
   The pressure-category selection path assembly boundary became directly observable.

3. **What implementation and/or test change made the boundary observable?**
   The implementation added `_from_pressure_category_selection(...)` and changed the pressure-category branch to consume it. The test suite added `test_pressure_category_selection_is_owned_by_local_helper()` to exercise the helper directly.

4. **What producer now owns the recovered responsibility?**
   `_from_pressure_category_selection(...)` owns pressure-category selection path assembly.

5. **What artifact or helper carries the recovered boundary, if any?**
   `_from_pressure_category_selection(...)` carries the recovered boundary.

6. **Who consumes it?**
   `build_selection_path_audit(...)` consumes it when `_target_matches_pressure_category(...)` matches the requested target.

7. **Did any compatibility boundary change?**
   No.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

- `_from_pressure_category_selection(...)`

## Recovered artifact/helper

- `_from_pressure_category_selection(...)`

## Recovered consumer

- `build_selection_path_audit(...)`, specifically the pressure-category target branch.

## Compatibility preserved

No.

Public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and read-only mutation boundaries are unchanged. The existing pressure-selection handoff remains the compatibility-producing path.

## LOC changed

- `seed_runtime/selection_path_audit.py`: 14 insertions, 6 deletions in the final diff.
- `tests/test_selection_path_audit.py`: 42 insertions in the final diff.
- `frontier_pressure_admission_slice_016.md`: 87 new lines.

## Tests executed

- `pytest -q tests/test_selection_path_audit.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

Potentially compressed responsibilities remain only where implementation evidence later shows a concrete local owner is missing. In this neighborhood, unsupported-target preparation, focus selection selected-name preparation, pressure-category selected-name preparation, target matching, selected pressure item lookup, pressure-selection reason/support/lineage payloads, and pressure-category selection path assembly are now directly observable. No additional adjacent boundary is claimed by this slice.
