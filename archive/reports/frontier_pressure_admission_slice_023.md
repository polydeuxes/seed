# Frontier Pressure Admission Slice 023

## Selected boundary

Recovered implementation-local ownership boundary: **unsupported-target selection-factor payload preparation inside `selection_path_audit`**.

The selected boundary is the local step where the unsupported-target selection path declares that its selection factors are `unknown`. Before this slice, `_unsupported_target_selection(...)` assembled unsupported-target selection while still constructing `_SelectionFactorPayload(selection_factors=["unknown"])` inline. The unsupported-target result, reason, supporting-evidence, non-selected-candidate, and typed-unknown payload preparations were already separated, so repository evidence identified the unsupported-target factor payload as the smallest remaining compressed responsibility inside that branch.

## Implementation evidence

Investigation began in `seed_runtime/selection_path_audit.py` at `build_selection_path_audit(...)`, `_unsupported_target_selection(...)`, and the helpers immediately adjacent to the most recent unsupported-target non-selected-candidate payload slice.

Current implementation evidence showed:

1. `build_selection_path_audit(...)` routes unrecognized targets to `_unsupported_target_selection(...)` after focus-selection and pressure-category target checks fail.
2. `_unsupported_target_selection(...)` already delegates unsupported-target selected result, reason, empty supporting evidence, non-selected candidates, and typed unknowns to named helpers.
3. `_unsupported_target_selection(...)` still directly constructed the unsupported-target selection-factor payload inline as `_SelectionFactorPayload(selection_factors=["unknown"])`.
4. The candidate set is not unsupported-target-specific; it remains owned by `_candidate_set_from_pressures(pressures)` because the implementation still exposes pressure candidates even for an unsupported target.
5. The read-only boundary is still carried by the unchanged `SelectionPathAudit` default boundary and the existing public compatibility handoff.

That made unsupported-target factor-payload preparation a narrower implementation-backed boundary than broader unsupported-target lineage assembly or route orchestration.

## Before

`_unsupported_target_selection(...)` directly owned both unsupported-target selection assembly and the local decision that unsupported-target selection factors are exactly `["unknown"]`.

## After

`_unsupported_target_selection(...)` delegates unsupported-target factor-payload construction to `_unsupported_target_factor_payload()`. The helper returns the same `_SelectionFactorPayload(selection_factors=["unknown"])`, preserving public JSON output, human-readable rendering, CLI behavior, schema shape, and read-only behavior.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_unsupported_target_factor_payload()` now owns producing the unsupported-target selection-factor payload.

## Recovered artifact/helper

- Helper: `_unsupported_target_factor_payload()`
- Artifact: `_SelectionFactorPayload(selection_factors=["unknown"])`

## Recovered consumer

`_unsupported_target_selection(...)` consumes `_unsupported_target_factor_payload()` while assembling the unsupported-target `SelectionPathAudit` compatibility object.

## Compatibility preserved

No.

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and the read-only mutation boundary are unchanged.

## LOC changed

```text
seed_runtime/selection_path_audit.py |  6 +++++-
tests/test_selection_path_audit.py   | 11 +++++++++++
2 files changed, 16 insertions(+), 1 deletion(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 136 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Unsupported-target selection assembly and unsupported-target selection-factor payload preparation were compressed together in `_unsupported_target_selection(...)`.

2. **Which implementation-local ownership boundary became directly observable?**

   Unsupported-target selection-factor payload preparation became directly observable as a separate local producer.

3. **What implementation and/or test change made the boundary observable?**

   `_unsupported_target_selection(...)` now calls `_unsupported_target_factor_payload()`, and `tests/test_selection_path_audit.py` directly exercises the helper while proving it does not own candidates, non-selected candidates, or unknowns.

4. **What producer now owns the recovered responsibility?**

   `_unsupported_target_factor_payload()` owns unsupported-target selection-factor payload preparation.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_unsupported_target_factor_payload()` carries the boundary by returning `_SelectionFactorPayload(selection_factors=["unknown"])`.

6. **Who consumes it?**

   `_unsupported_target_selection(...)` consumes it while assembling the unsupported-target selection path.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated only from current implementation evidence, not campaign history, naming symmetry, or architectural preference. After this slice, the unsupported-target branch has named local producers for result, reason, supporting evidence, factors, non-selected candidates, and typed unknowns; its pressure-derived candidate set remains intentionally owned by the general candidate-set helper. Broader route orchestration and source collection remain in `build_selection_path_audit(...)`, but this slice does not claim those broader responsibilities because the smallest adjacent compressed responsibility evidenced in the current unsupported-target branch was the unsupported-target selection-factor payload.
