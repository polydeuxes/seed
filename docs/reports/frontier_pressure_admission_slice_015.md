# Frontier Pressure Admission Slice 015

Recovered implementation-local ownership boundary: **pressure-category selection selected-name preparation inside `selection_path_audit`**.

## Selected boundary

The selected boundary is the local handoff where the pressure-category route in `build_selection_path_audit(...)` stops preparing the selected display name inline before entering `_from_pressure_selection(...)`. The selected-name preparation for pressure-category selection is now owned by `_pressure_category_selection_selected_name(...)`.

This slice does not change selection behavior, public compatibility, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, or the read-only mutation boundary.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` around `build_selection_path_audit(...)`, the recently separated `_focus_selection_selected_name(...)`, and the existing `_from_pressure_selection(...)` handoff.

Current implementation evidence showed:

1. The focus-selection route already delegated route-specific selected-name preparation to `_focus_selection_selected_name(...)` before `_from_pressure_selection(...)`.
2. The pressure-category route still prepared its selected name directly inside `build_selection_path_audit(...)` by calling `_selected_name(selected_item, story.focus)` at the handoff site.
3. `_selected_name(...)` already owned the shared fallback rule, so this slice did not re-slice fallback naming. The still-compressed responsibility was only the pressure-category route's ownership of when that fallback rule is used before the pressure-selection handoff.
4. `_from_pressure_selection(...)` continues to consume a selected string and remains unchanged in behavior.

## Before

`build_selection_path_audit(...)` matched a pressure category, looked up the selected pressure item, directly called `_selected_name(selected_item, story.focus)`, and immediately passed that selected string to `_from_pressure_selection(...)`. That compressed pressure-category route recognition, selected-item lookup, selected-name preparation, and the pressure-selection handoff in one branch.

## After

`build_selection_path_audit(...)` still matches the pressure-category route and looks up the selected pressure item, but it now delegates pressure-category selected-name preparation to `_pressure_category_selection_selected_name(selected_item, story.focus)` before the existing `_from_pressure_selection(...)` handoff.

The new helper owns only pressure-category selected-name preparation:

- selected pressure item present: preserve existing selected category lower-casing through `_selected_name(...)`;
- no selected pressure item: preserve existing focus fallback through `_selected_name(...)`.

It does not match targets, select candidates, evaluate readiness, plan action, mutate state, record facts, write event-ledger entries, or alter public output.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

Producer: `_pressure_category_selection_selected_name(...)`.

## Recovered artifact/helper

Recovered helper: `_pressure_category_selection_selected_name(selected_item, focus)`.

The helper returns the selected name string consumed by the existing pressure-selection compatibility handoff.

## Recovered consumer

Consumer: the pressure-category branch of `build_selection_path_audit(...)`, which passes the selected name to `_from_pressure_selection(...)`.

## Compatibility preserved

No.

No compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory behavior, diagnostic shape-audit behavior, schema, event-ledger behavior, and the read-only selection visibility boundary are preserved.

## LOC changed

`git diff --numstat` reported:

- `seed_runtime/selection_path_audit.py`: 7 insertions, 1 deletion.
- `tests/test_selection_path_audit.py`: 24 insertions, 0 deletions.

Total: 31 insertions, 1 deletion.

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `python -m pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 127 tests.

## Required questions

### 1. What responsibilities were previously compressed?

The pressure-category branch compressed route matching, selected pressure item lookup, pressure-category selected-name preparation, and the `_from_pressure_selection(...)` handoff. Existing helpers already owned pressure-category target matching, selected pressure item lookup, shared selected-name fallback, and the pressure-selection handoff. The still-compressed responsibility selected here was only pressure-category route selected-name preparation at the handoff site.

### 2. Which implementation-local ownership boundary became directly observable?

Pressure-category selection selected-name preparation became directly observable.

### 3. What implementation and/or test change made the boundary observable?

`build_selection_path_audit(...)` now calls `_pressure_category_selection_selected_name(selected_item, story.focus)` instead of calling `_selected_name(...)` inline in the pressure-category route. `tests/test_selection_path_audit.py` now directly tests the selected-item and no-selected-item cases for `_pressure_category_selection_selected_name(...)`.

### 4. What producer now owns the recovered responsibility?

`_pressure_category_selection_selected_name(...)` owns pressure-category selected-name preparation.

### 5. What artifact or helper carries the recovered boundary, if any?

The helper `_pressure_category_selection_selected_name(selected_item, focus)` carries the recovered boundary.

### 6. Who consumes it?

The pressure-category branch of `build_selection_path_audit(...)` consumes the helper result and passes it to `_from_pressure_selection(...)`.

### 7. Did any compatibility boundary change?

No.

## Remaining compressed responsibilities

Remaining compression should continue to be evaluated from current implementation evidence rather than campaign history, naming symmetry, or architectural preference. After this slice, nearby implementation still includes the broader route orchestration inside `build_selection_path_audit(...)`, shared selected-name fallback inside `_selected_name(...)`, and supported pressure-selection assembly inside `_from_pressure_selection(...)`. They are not recovered here because this slice recovers exactly one implementation-local boundary and preserves the existing read-only selection visibility surface.
