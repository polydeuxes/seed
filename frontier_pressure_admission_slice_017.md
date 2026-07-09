# Frontier Pressure Admission Slice 017

## Selected boundary

Recovered implementation-local ownership boundary: **focus-selection path assembly inside `selection_path_audit`**.

The selected boundary is the local handoff where `build_selection_path_audit(...)` no longer owns the focus-selection branch assembly after target recognition. The branch assembly is now carried by `_from_focus_selection(...)`, which prepares the focus-selection selected name from already-separated helpers and delegates to the existing pressure-selection audit assembly.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` next to the most recent `_from_pressure_category_selection(...)` slice. Current implementation evidence showed the pressure-category branch already had a named assembly helper, while the focus-selection branch in `build_selection_path_audit(...)` still performed local assembly inline:

1. target recognition was already separated in `_target_matches_focus_selection(...)`;
2. selected pressure lookup was already separated in `_selected_pressure_item(...)`;
3. focus selected-name compatibility was already separated in `_focus_selection_selected_name(...)`;
4. supported pressure-selection audit assembly was already separated in `_from_pressure_selection(...)`;
5. however, `build_selection_path_audit(...)` still glued those owned steps together directly for the focus-selection branch.

Because the narrower responsibilities inside the branch were already named and covered, the remaining compressed responsibility was the branch-level focus-selection path assembly itself, not another payload, target match, selected-item lookup, selected-name, or pressure-selection payload slice.

## Before

`build_selection_path_audit(...)` directly assembled the focus-selection route after `_target_matches_focus_selection(...)` returned true. It selected the first pressure item, prepared the selected display value, and handed the result to `_from_pressure_selection(...)` inline.

That compressed focus-selection route assembly into the public builder alongside root resolution, target normalization, source audit collection, route ordering, pressure-category dispatch, and unsupported-target fallback.

## After

`build_selection_path_audit(...)` delegates the already-recognized focus-selection branch to `_from_focus_selection(...)`.

`_from_focus_selection(...)` owns only focus-selection path assembly:

- selected pressure lookup through `_selected_pressure_item(...)`;
- focus selected-name preparation through `_focus_selection_selected_name(...)`;
- handoff to `_from_pressure_selection(...)` with the unchanged selected string, pressure candidates, and focus.

The helper does not own target recognition, pressure-category assembly, unsupported-target refusal preparation, result/reason/support/lineage payload construction, JSON serialization, text formatting, recording, event-ledger writes, or cluster mutation.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_from_focus_selection(...)` now produces the focus-selection audit assembly for recognized focus-selection targets.

## Recovered artifact/helper

`_from_focus_selection(target, normalized_target, pressures, focus)` carries the recovered implementation-local ownership boundary.

## Recovered consumer

`build_selection_path_audit(...)` consumes `_from_focus_selection(...)` after `_target_matches_focus_selection(...)` admits a focus-selection target.

## Compatibility preserved

No.

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output shape, human-readable output shape, diagnostic inventory behavior, diagnostic shape-audit behavior, event-ledger behavior, and the read-only mutation boundary are preserved.

## LOC changed

`git diff --stat` reported:

```text
seed_runtime/selection_path_audit.py | 20 +++++++---
tests/test_selection_path_audit.py   | 75 ++++++++++++++++++++++++++++++++++++
2 files changed, 89 insertions(+), 6 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 130 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Focus-selection route assembly was compressed into `build_selection_path_audit(...)` together with source collection and route orchestration. The narrower responsibilities inside the branch were not selected because implementation already separated focus target matching, selected pressure item lookup, focus selected-name preparation, and supported pressure-selection audit assembly.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between public selection-path route orchestration and focus-selection path assembly became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   The inline focus-selection branch in `build_selection_path_audit(...)` was replaced with `_from_focus_selection(...)`. Tests now directly exercise `_from_focus_selection(...)` for the primary-pressure path and the current-focus compatibility case.

4. **What producer now owns the recovered responsibility?**

   `_from_focus_selection(...)` owns focus-selection path assembly.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_from_focus_selection(...)` carries the recovered boundary.

6. **Who consumes it?**

   `build_selection_path_audit(...)` consumes it after focus-selection target recognition.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated only from current implementation evidence, not campaign history, naming symmetry, or architectural preference. After this slice, the immediate focus and pressure-category selection branches both have named assembly helpers. The broader `build_selection_path_audit(...)` route ordering and audit-source collection remain in the builder, but this slice does not claim those broader responsibilities because the smallest adjacent compressed branch-level ownership boundary was focus-selection path assembly.
