# Frontier Pressure Admission Slice 020

## Selected boundary

Recovered implementation-local ownership boundary: **unsupported-target result payload preparation inside `selection_path_audit`**.

The selected boundary is the local step where the unsupported-target selection path declares the selected value as `unknown`. Before this slice, `_unsupported_target_selection(...)` assembled the unsupported result, reason, empty support, candidate lineage, unknown factor, non-selected list, and typed unknown handoff in one body. The implementation evidence showed a narrower still-compressed responsibility inside that unsupported-target path: the unsupported-target selected-result payload was still constructed inline even though the unsupported-target reason payload and typed-unknown payload already had named local producers.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` around `build_selection_path_audit(...)`, `_unsupported_target_selection(...)`, and the most recent `_unsupported_target_reason_payload()` slice. Current implementation showed:

1. `build_selection_path_audit(...)` routes unsupported targets to `_unsupported_target_selection(...)` after implemented focus-selection and pressure-category target checks fail.
2. `_unsupported_target_selection(...)` already owns unsupported-target selection assembly.
3. `_unsupported_target_reason_payload()` already owns unsupported-target reason payload preparation.
4. `_unsupported_target_unknown_payload()` already owns unsupported-target typed-unknown preparation.
5. The unsupported-target result payload remained inline as `_SelectionResultPayload(selected="unknown")` inside `_unsupported_target_selection(...)`.

That made unsupported-target result payload preparation the smallest adjacent compressed implementation-local responsibility. Broader boundaries, such as unsupported-target support payload preparation or unsupported-target lineage assembly, remain broader than this one-line selected-result declaration and were not selected for this slice.

## Before

`_unsupported_target_selection(...)` directly constructed the unsupported-target `_SelectionResultPayload` inline while also orchestrating unsupported-target reason, empty support, candidate-set handoff, unknown factor, non-selected handoff, and typed-unknown payload.

## After

`_unsupported_target_selection(...)` delegates unsupported-target selected-result construction to `_unsupported_target_result_payload()`. The helper returns the same `_SelectionResultPayload(selected="unknown")` and preserves the existing public JSON/text behavior.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_unsupported_target_result_payload()` now owns unsupported-target result payload preparation.

## Recovered artifact/helper

Recovered helper: `_unsupported_target_result_payload()`.

Recovered artifact: `_SelectionResultPayload(selected="unknown")` for unsupported targets.

## Recovered consumer

`_unsupported_target_selection(...)` consumes `_unsupported_target_result_payload()` when assembling the unchanged unsupported-target `SelectionPathAudit` compatibility object.

## Compatibility preserved

No.

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic shape, schema, event-ledger behavior, and read-only mutation boundaries are unchanged. The slice only moved an existing private unsupported-target selected-result payload construction into a named local producer and added a direct unit test for that producer.

## LOC changed

Final diff:

```text
seed_runtime/selection_path_audit.py |  6 +++++-
tests/test_selection_path_audit.py   | 11 +++++++++++
2 files changed, 16 insertions(+), 1 deletion(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 133 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Unsupported-target selection assembly and unsupported-target selected-result payload preparation were compressed together in `_unsupported_target_selection(...)`.

2. **Which implementation-local ownership boundary became directly observable?**

   Unsupported-target result payload preparation became directly observable as its own local helper boundary.

3. **What implementation and/or test change made the boundary observable?**

   `_unsupported_target_selection(...)` now calls `_unsupported_target_result_payload()`, and `tests/test_selection_path_audit.py` directly exercises the helper while proving it does not own outcome, evidence, or candidate payload fields.

4. **What producer now owns the recovered responsibility?**

   `_unsupported_target_result_payload()` owns unsupported-target result payload preparation.

5. **What artifact or helper carries the recovered boundary, if any?**

   Helper: `_unsupported_target_result_payload()`.

   Artifact: `_SelectionResultPayload(selected="unknown")`.

6. **Who consumes it?**

   `_unsupported_target_selection(...)` consumes it while assembling the unsupported-target `SelectionPathAudit`.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated only from current implementation evidence rather than campaign history, naming symmetry, or architectural preference. After this slice, the unsupported-target branch still contains inline empty-support payload preparation and a lineage assembly that combines existing candidate-set, factor, non-selected, and typed-unknown payload producers. Those were not recovered here because this slice recovers exactly one smaller adjacent implementation-local boundary: unsupported-target result payload preparation.
