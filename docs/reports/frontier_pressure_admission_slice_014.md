# Frontier Pressure Admission Slice 014

Recovered implementation-local ownership boundary: **focus-selection selected-name preparation inside `selection_path_audit`**.

## Selected boundary

The selected boundary is the local handoff where `build_selection_path_audit(...)` no longer owns the inline compatibility decision for the selected value used by focus-selection targets. That responsibility is now carried by `_focus_selection_selected_name(...)` before the existing supported pressure-selection handoff to `_from_pressure_selection(...)`.

Expected compatibility answer: No.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` around `build_selection_path_audit(...)`, `_from_pressure_selection(...)`, `_pressure_selection_lineage_payload(...)`, `_pressure_selection_reason_payload(...)`, `_pressure_selection_supporting_evidence_payload(...)`, `_selected_pressure_item(...)`, and the adjacent selection-path tests.

The current implementation already separated supported pressure-selection lineage payload preparation, supporting-evidence payload preparation, reason payload preparation, selected pressure item lookup, target matching, candidate-set payload preparation, selection-factor payload preparation, non-selected payload preparation, typed-unknown payload preparation, and unsupported-target refusal preparation.

The adjacent still-compressed responsibility was narrower than those recovered boundaries: focus-selection selected-name preparation. The focus-selection branch needed to preserve two existing selected-value cases before delegating to `_from_pressure_selection(...)`:

- `current_focus` must preserve the operational story focus string directly.
- Other focus-selection aliases, such as `primary_pressure` or a focus-name match, must use the selected pressure item's lower-case category when available, falling back to focus when no pressure item exists.

That selected-name compatibility decision was inline in the focus-selection route even though route matching and selected pressure item lookup were already owned by nearby helpers.

## Before

`build_selection_path_audit(...)` performed route matching, selected pressure item lookup, and the focus-selection selected-name compatibility decision in the same branch before calling `_from_pressure_selection(...)`.

## After

`build_selection_path_audit(...)` still owns route dispatch, but delegates the selected-name compatibility decision to `_focus_selection_selected_name(normalized, selected_item, story.focus)`.

The new helper owns only that local selected-name preparation. It does not select targets, admit pressure, evaluate readiness, mutate state, record facts, write events, plan work, prioritize work, or change public output.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`
  - Added `_focus_selection_selected_name(...)`.
  - Replaced inline focus-selection selected-name preparation in `build_selection_path_audit(...)` with a call to the helper.

## Test files changed

- `tests/test_selection_path_audit.py`
  - Added direct helper coverage proving the boundary preserves the current-focus display value, the primary-pressure selected pressure category value, and the no-pressure fallback value.

## Recovered producer

Producer: `_focus_selection_selected_name(...)`.

## Recovered artifact/helper

Artifact/helper: `_focus_selection_selected_name(...)`, returning the selected string consumed by the existing supported pressure-selection handoff.

## Recovered consumer

Consumer: `build_selection_path_audit(...)` consumes `_focus_selection_selected_name(...)` in the focus-selection route and passes its result to `_from_pressure_selection(...)`.

## Compatibility preserved

No compatibility boundary changed.

The slice preserves:

- public compatibility;
- runtime behavior;
- CLI behavior;
- JSON output;
- human-readable output;
- diagnostics;
- schema;
- event-ledger behavior;
- read-only mutation boundary;
- existing tests.

`selection_path_audit` remains a read-only visibility surface. The changed code only names an existing selected-value compatibility decision; it does not promote visibility into acceptance, reliance, action, mutation, execution, planning, prioritization, inquiry generation, or autonomous next-step selection.

## LOC changed

From `git diff --stat` before commit:

- `seed_runtime/selection_path_audit.py`: 14 insertions, 6 deletions.
- `tests/test_selection_path_audit.py`: 35 insertions, 0 deletions.
- Total: 49 insertions, 6 deletions.

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 126 tests.

## Required Questions

1. What responsibilities were previously compressed?

   Focus-selection route dispatch, selected pressure item lookup, the `current_focus` selected-value compatibility case, the focus-alias selected pressure category case, and the no-pressure fallback case were adjacent in `build_selection_path_audit(...)`. The recovered compressed responsibility was only the focus-selection selected-name preparation.

2. Which implementation-local ownership boundary became directly observable?

   Focus-selection selected-name preparation became directly observable.

3. What implementation and/or test change made the boundary observable?

   `build_selection_path_audit(...)` now delegates selected-name preparation to `_focus_selection_selected_name(...)`, and `tests/test_selection_path_audit.py` directly exercises the helper's current-focus, primary-pressure, and no-pressure fallback cases.

4. What producer now owns the recovered responsibility?

   `_focus_selection_selected_name(...)` owns the recovered responsibility.

5. What artifact or helper carries the recovered boundary, if any?

   `_focus_selection_selected_name(...)` carries the boundary.

6. Who consumes it?

   `build_selection_path_audit(...)` consumes it in the focus-selection branch before passing the unchanged selected string to `_from_pressure_selection(...)`.

7. Did any compatibility boundary change?

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated from current implementation evidence rather than campaign history, naming symmetry, or architectural preference. After this slice, nearby implementation responsibilities still include the broader supported-selection orchestration in `_from_pressure_selection(...)`, the pressure-category route's selected-name preparation through `_selected_name(...)`, and route ordering between focus-selection and pressure-category targets. They are not recovered here because this slice recovers exactly one implementation-local boundary supported by direct code pressure.
