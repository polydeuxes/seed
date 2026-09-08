# Frontier Pressure Admission Slice 025

Recovered implementation-local ownership boundary: **selection-path input collection inside `selection_path_audit`**.

## Selected boundary

`build_selection_path_audit(...)` already owned target normalization, route dispatch, and branch handoff. Immediately after the repository-root preparation slice, it still directly collected the two upstream inputs required by every implemented selection path:

- pressure-audit pressures from `build_pressure_audit(state, repo_root=root)`;
- operational-story focus from `build_operational_story(state, repo_root=root)`.

This slice makes that input-collection responsibility directly observable as a local producer without changing route ordering, public compatibility, JSON shape, CLI behavior, diagnostics, event-ledger behavior, or read-only mutation boundaries.

## Implementation evidence

Current implementation evidence showed the smallest adjacent compressed responsibility after `_selection_path_repo_root(...)` was not another route branch and not another payload in an already-decomposed branch. The remaining compression was the local input collection that occurred before all branch decisions:

```python
root = _selection_path_repo_root(repo_root)
normalized = _normalize_target(target)
pressure = build_pressure_audit(state, repo_root=root)
story = build_operational_story(state, repo_root=root)
```

Those two upstream collection calls supplied only the local pressures and focus needed by focus-selection, pressure-category selection, and unsupported-target refusal. The responsibility was narrower than route orchestration because it does not decide the route and does not assemble any selection output.

## Before

`build_selection_path_audit(...)` simultaneously prepared the repository root, normalized the requested target, collected pressure-audit and operational-story inputs, performed route matching, and dispatched to the existing branch helpers.

## After

`build_selection_path_audit(...)` still prepares the root, normalizes the target, and owns route dispatch. The upstream pressure/focus input collection is now delegated to `_selection_path_inputs(state, root)`, which returns a `_SelectionPathInputs` payload containing only:

- `pressures`;
- `focus`.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`
  - Added `_SelectionPathInputs` as an implementation-local input payload.
  - Added `_selection_path_inputs(...)` as the local producer for pressure/focus collection.
  - Updated `build_selection_path_audit(...)` to consume the input payload instead of directly owning the two upstream collection calls.

## Test files changed

- `tests/test_selection_path_audit.py`
  - Added `test_selection_path_input_collection_is_owned_by_local_helper(...)`.
  - The test monkeypatches the upstream producers, proves both receive the already-prepared root, proves the payload carries the collected pressures and focus, and proves the payload does not own target/result/outcome responsibilities.

## Recovered producer

`_selection_path_inputs(state, root)` now owns selection-path input collection from the pressure audit and operational story.

## Recovered artifact/helper

- Artifact: `_SelectionPathInputs`
- Helper: `_selection_path_inputs(...)`

## Recovered consumer

`build_selection_path_audit(...)` consumes `_SelectionPathInputs` before performing the existing target-route checks and branch handoffs.

## Compatibility preserved

No.

No compatibility boundary changed. The public `SelectionPathAudit` dataclass, JSON output, human-readable output, CLI behavior, diagnostics inventory, diagnostic shape audit registration, event-ledger behavior, and read-only `mutates_cluster=false` boundary are unchanged.

## LOC changed

From `git diff --stat`:

```text
seed_runtime/selection_path_audit.py | 29 +++++++++++++++----------
tests/test_selection_path_audit.py   | 41 ++++++++++++++++++++++++++++++++++++
2 files changed, 59 insertions(+), 11 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result: passed, 138 tests.

## Required Questions

1. **What responsibilities were previously compressed?**

   Repository-root preparation, target normalization, pressure-audit input collection, operational-story input collection, target-route matching, and branch dispatch were adjacent in `build_selection_path_audit(...)`. The recovered compressed responsibility was only the pressure/focus input collection after root preparation and before route decisions.

2. **Which implementation-local ownership boundary became directly observable?**

   Selection-path input collection became directly observable as its own implementation-local boundary.

3. **What implementation and/or test change made the boundary observable?**

   `_SelectionPathInputs` and `_selection_path_inputs(...)` were added, `build_selection_path_audit(...)` now consumes that payload, and `test_selection_path_input_collection_is_owned_by_local_helper(...)` directly exercises the helper and its limited field ownership.

4. **What producer now owns the recovered responsibility?**

   `_selection_path_inputs(state, root)` owns the recovered responsibility.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_SelectionPathInputs` carries the collected `pressures` and `focus`; `_selection_path_inputs(...)` produces it.

6. **Who consumes it?**

   `build_selection_path_audit(...)` consumes it for the existing focus-selection, pressure-category selection, and unsupported-target branch handoffs.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated only from current implementation evidence. After this slice, `build_selection_path_audit(...)` still owns target normalization, route ordering, and dispatch among focus-selection, pressure-category selection, and unsupported-target refusal. Those responsibilities were not recovered here because the smallest adjacent implementation-backed compression was the upstream pressure/focus input collection. Existing branch payloads and selected-name/target-match helpers were not re-mined because they already have named helpers and direct tests.

## Constitutional guardrail

The change preserves `selection_path_audit` as a read-only explanation and visibility surface. It does not promote selection visibility into acceptance, reliance, action, mutation, execution, planning, prioritization, inquiry generation, or autonomous next-step selection.
