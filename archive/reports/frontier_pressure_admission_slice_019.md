# Frontier Pressure Admission Slice 019

## Selected boundary

Recovered implementation-local ownership boundary: **unsupported-target reason payload preparation inside `selection_path_audit`**.

The selected boundary is the local step where the unsupported-target selection path explains why the selected value is `unknown`. Before this slice, `_unsupported_target_selection(...)` assembled the unsupported result, reason, empty evidence, candidate lineage, unknown factor, non-selected list, and typed unknown handoff in one body. The implementation evidence showed a narrower still-compressed responsibility inside that unsupported-target path: the unsupported-target reason outcome dictionary was still constructed inline even though result/reason/support/lineage are already distinct compatibility payloads and the unsupported-target typed unknown payload already has its own producer.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` around `build_selection_path_audit(...)`, `_unsupported_target_selection(...)`, and the most recent `_unsupported_target_unknown_payload()` slice. Current implementation showed:

1. `build_selection_path_audit(...)` routes unsupported targets to `_unsupported_target_selection(...)` after implemented focus-selection and pressure-category target checks fail.
2. `_unsupported_target_selection(...)` already owns the unsupported-target selection assembly boundary.
3. `_unsupported_target_unknown_payload()` already owns unsupported-target typed-unknown preparation and is consumed by `_unsupported_target_selection(...)`.
4. The unsupported-target reason payload remained inline as `_SelectionReasonPayload(outcome={...})` inside `_unsupported_target_selection(...)`.
5. The reason payload is a narrower implementation-local responsibility than broad unsupported-target selection assembly because it carries only the selected/reason outcome and excludes candidates, evidence, selection factors, non-selected alternatives, and typed unknowns.

The narrower compressed responsibility inside the unsupported-target branch was therefore unsupported-target reason payload preparation, not broad unsupported-target selection assembly or typed-unknown preparation.

## Before

`_unsupported_target_selection(...)` directly constructed the unsupported-target `_SelectionReasonPayload` inline while also orchestrating the unsupported-target selected result, empty support, candidate-set handoff, unknown factor, non-selected handoff, and typed-unknown payload.

## After

`_unsupported_target_selection(...)` delegates unsupported-target reason outcome construction to `_unsupported_target_reason_payload()`. The helper returns the same `_SelectionReasonPayload` and preserves the existing public JSON/text behavior.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_unsupported_target_reason_payload()` now owns unsupported-target reason payload preparation.

## Recovered artifact/helper

Recovered helper: `_unsupported_target_reason_payload()`.

Recovered artifact: `_SelectionReasonPayload` for unsupported-target selection, containing:

```python
{
    "selected": "unknown",
    "reason": "target is not an implemented selection surface",
}
```

## Recovered consumer

`_unsupported_target_selection(...)` consumes `_unsupported_target_reason_payload()` when assembling the unchanged unsupported-target `SelectionPathAudit` compatibility object.

## Compatibility preserved

No.

No compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and read-only mutation boundaries are preserved. The slice only moved existing unsupported-target reason payload construction behind a local producer and added a direct helper-level test.

## LOC changed

Final diff stat:

```text
seed_runtime/selection_path_audit.py | 16 ++++++++++------
tests/test_selection_path_audit.py   | 14 ++++++++++++++
2 files changed, 24 insertions(+), 6 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 132 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Unsupported-target selection assembly and unsupported-target reason payload construction were compressed together in `_unsupported_target_selection(...)`. The helper also still coordinated selected result, empty support, candidate-set handoff, unknown factor, non-selected handoff, and typed-unknown handoff, but this slice recovered only the narrower inline reason payload preparation.

2. **Which implementation-local ownership boundary became directly observable?**

   Unsupported-target reason payload preparation became directly observable as a named local helper.

3. **What implementation and/or test change made the boundary observable?**

   The inline `_SelectionReasonPayload(...)` construction in `_unsupported_target_selection(...)` was replaced with `_unsupported_target_reason_payload()`. `tests/test_selection_path_audit.py` now directly exercises that helper and proves it owns only the reason outcome fields, not evidence, candidates, or selection factors.

4. **What producer now owns the recovered responsibility?**

   `_unsupported_target_reason_payload()` owns the recovered responsibility.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_unsupported_target_reason_payload()` carries the boundary and returns the `_SelectionReasonPayload` artifact.

6. **Who consumes it?**

   `_unsupported_target_selection(...)` consumes the helper while assembling the unsupported-target selection audit.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated only from current implementation evidence. Adjacent unsupported-target assembly still includes inline production of the selected `unknown` result, empty supporting evidence, unknown selection factor, and empty non-selected payload. Those were not recovered here because this slice selected exactly one narrower implementation-backed responsibility: unsupported-target reason payload preparation. Further recovery should first inspect whether one of those inline payload preparations remains compressed and justified by code pressure, rather than relying on naming symmetry or campaign history.
