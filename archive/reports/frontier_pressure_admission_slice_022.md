# Frontier Pressure Admission Slice 022

## Selected boundary

Recovered implementation-local ownership boundary: **unsupported-target non-selected-candidate payload preparation inside `selection_path_audit`**.

The selected boundary is the unsupported-target branch's explicit decision that an unimplemented selection target has no non-selected candidates. This was previously embedded directly inside `_unsupported_target_selection(...)` as an inline `_SelectionNonSelectedPayload(non_selected=[])` while adjacent unsupported-target result, reason, supporting-evidence, and typed-unknown payloads already had named local producers.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` around `selection_path_audit` and the implementation immediately adjacent to the most recent unsupported-target supporting-evidence payload slice. Current implementation evidence showed that `_unsupported_target_selection(...)` still constructed one lineage member inline:

```python
lineage=_SelectionLineagePayload(
    candidate_set=_candidate_set_from_pressures(pressures),
    factors=_SelectionFactorPayload(selection_factors=["unknown"]),
    non_selected=_SelectionNonSelectedPayload(non_selected=[]),
    unknowns=_unsupported_target_unknown_payload(),
)
```

The narrower compressed responsibility selected here was not the whole unsupported-target lineage assembly. The branch still delegates candidate-set production to `_candidate_set_from_pressures(...)` and typed-unknown production to `_unsupported_target_unknown_payload()`, while the inline non-selected payload had no named producer and represented the concrete unsupported-target rule that no implemented winner exists from which to explain alternatives.

## Before

`_unsupported_target_selection(...)` owned unsupported-target branch assembly and directly created the empty non-selected payload inline. That compressed branch orchestration with the local non-selected-candidate payload decision for unsupported targets.

## After

`_unsupported_target_selection(...)` delegates non-selected-candidate payload preparation to `_unsupported_target_non_selected_payload()`. The helper returns `_SelectionNonSelectedPayload(non_selected=[])`, preserving the exact public JSON and human-readable output while making the local ownership boundary directly observable in implementation and tests.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_unsupported_target_non_selected_payload()` now owns unsupported-target non-selected payload preparation.

## Recovered artifact/helper

`_unsupported_target_non_selected_payload()` carries the recovered boundary by producing `_SelectionNonSelectedPayload(non_selected=[])` for unsupported selection targets.

## Recovered consumer

`_unsupported_target_selection(...)` consumes `_unsupported_target_non_selected_payload()` while assembling the existing `_SelectionLineagePayload` for the unsupported-target audit.

## Compatibility preserved

No.

No compatibility boundary changed. The selected target, outcome, candidates, selection factors, evidence, unknowns, boundary flags, CLI behavior, JSON shape, human-readable rendering, diagnostic registration, event-ledger behavior, and read-only mutation boundary are unchanged.

## LOC changed

Final diff before this report:

- `seed_runtime/selection_path_audit.py`: 5 insertions, 1 deletion.
- `tests/test_selection_path_audit.py`: 13 insertions, 0 deletions.
- Total: 18 insertions, 1 deletion.

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 135 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Unsupported-target branch assembly and unsupported-target non-selected-candidate payload preparation were compressed inside `_unsupported_target_selection(...)`.

2. **Which implementation-local ownership boundary became directly observable?**

   Unsupported-target non-selected-candidate payload preparation became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   The inline `_SelectionNonSelectedPayload(non_selected=[])` construction was replaced with `_unsupported_target_non_selected_payload()`, and `test_unsupported_target_non_selected_payload_is_owned_by_local_helper()` directly exercises the helper and asserts it does not own candidate-set, selection-factor, or unknown payload fields.

4. **What producer now owns the recovered responsibility?**

   `_unsupported_target_non_selected_payload()`.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_unsupported_target_non_selected_payload()` carries the boundary and returns `_SelectionNonSelectedPayload`.

6. **Who consumes it?**

   `_unsupported_target_selection(...)` consumes it as the `non_selected` member of `_SelectionLineagePayload`.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated only from current implementation evidence, not campaign history, naming symmetry, or architectural preference. After this slice, the unsupported-target branch still contains inline unsupported-target factor payload preparation (`_SelectionFactorPayload(selection_factors=["unknown"])`) and the branch-level lineage assembly itself. Those were not recovered here because this slice recovers exactly one narrower implementation-backed boundary.
