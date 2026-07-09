# Frontier Pressure Admission Slice 026

Recovered implementation-local ownership boundary: **supported pressure-selection result payload preparation inside `selection_path_audit`**.

## Selected boundary

The selected boundary is the local preparation step where supported pressure-backed selection turns the already-selected string into the implementation-local `_SelectionResultPayload` consumed by the unchanged public `SelectionPathAudit` compatibility handoff.

This boundary was selected from current implementation evidence after starting at `seed_runtime/selection_path_audit.py` around `build_selection_path_audit(...)`, `_selection_path_inputs(...)`, `_from_focus_selection(...)`, `_from_pressure_category_selection(...)`, and `_from_pressure_selection(...)`. The immediately adjacent input collection, route branches, selected-name preparation, selected-item lookup, reason payload, supporting-evidence payload, lineage payload, and unsupported-target payloads were already named. The remaining compressed responsibility inside `_from_pressure_selection(...)` was narrower than broader route dispatch or audit assembly: supported selections still constructed `_SelectionResultPayload(selected=selected)` inline while adjacent supported-selection payload producers were already explicit.

## Implementation evidence

Before this slice, `_from_pressure_selection(...)` performed multiple local responsibilities in one body:

1. looked up the selected pressure item;
2. collected pressure-selection unknowns;
3. prepared the supported selected-result payload inline with `_SelectionResultPayload(selected=selected)`;
4. delegated pressure-selection reason preparation;
5. delegated pressure-selection supporting-evidence preparation;
6. delegated pressure-selection lineage preparation;
7. handed all payloads to `_selection_path_from_payloads(...)`.

The result payload preparation was still compressed into the supported pressure-selection assembly body even though the adjacent reason, evidence, and lineage payload responsibilities already had named implementation-local producers.

## Before

`_from_pressure_selection(...)` directly constructed `_SelectionResultPayload(selected=selected)` while also coordinating selected pressure lookup, unknown collection, pressure reason payload production, supporting-evidence payload production, lineage payload production, and compatibility handoff.

## After

`_from_pressure_selection(...)` delegates supported selected-result payload preparation to `_pressure_selection_result_payload(selected)`. The helper owns only the supported pressure-selection result payload and returns the same `_SelectionResultPayload` shape as before.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`
  - Replaced inline supported result payload construction in `_from_pressure_selection(...)` with `_pressure_selection_result_payload(selected)`.
  - Added `_pressure_selection_result_payload(...)` as the named local producer for supported pressure-selection result payload preparation.

## Test files changed

- `tests/test_selection_path_audit.py`
  - Added `test_pressure_selection_result_payload_is_owned_by_local_helper` to prove the helper owns only the selected result payload and does not own outcome, evidence, or candidate lineage fields.

## Recovered producer

Producer: `_pressure_selection_result_payload(selected)`.

It owns converting the already-selected supported pressure-selection string into `_SelectionResultPayload` before the public compatibility handoff.

## Recovered artifact/helper

Artifact/helper: `_pressure_selection_result_payload(...)`, carrying `_SelectionResultPayload(selected=selected)`.

## Recovered consumer

Consumer: `_from_pressure_selection(...)`, which consumes the helper result as the `result` payload passed to `_selection_path_from_payloads(...)`.

## Compatibility preserved

No.

No compatibility boundary changed. Public `SelectionPathAudit` shape, JSON output, human-readable output, CLI behavior, diagnostic inventory behavior, diagnostic shape-audit behavior, event-ledger behavior, schema, and read-only mutation boundary are unchanged. The selected string is handed to the same `_SelectionResultPayload` dataclass and then to the same `_selection_path_from_payloads(...)` compatibility handoff.

`selection_path_audit` remains a read-only explanation and visibility surface. This slice does not promote selection visibility into acceptance, reliance, action, mutation, execution, planning, prioritization, inquiry generation, route authority, readiness evaluation, or autonomous next-step selection.

## LOC changed

Final diff:

```text
seed_runtime/selection_path_audit.py |  6 +++++-
tests/test_selection_path_audit.py   | 11 +++++++++++
2 files changed, 16 insertions(+), 1 deletion(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 139 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Supported pressure-selection orchestration and supported selected-result payload preparation were compressed inside `_from_pressure_selection(...)`. The function already coordinated selected-item lookup, unknown collection, reason payload preparation, supporting-evidence payload preparation, lineage payload preparation, and the final compatibility handoff while still constructing the result payload inline.

2. **Which implementation-local ownership boundary became directly observable?**

   Supported pressure-selection result payload preparation became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   `_from_pressure_selection(...)` now calls `_pressure_selection_result_payload(selected)` instead of constructing `_SelectionResultPayload` inline. `tests/test_selection_path_audit.py` directly exercises `_pressure_selection_result_payload(...)` and proves it owns only the selected result field.

4. **What producer now owns the recovered responsibility?**

   `_pressure_selection_result_payload(selected)` owns the recovered responsibility.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_pressure_selection_result_payload(...)` carries the boundary and returns `_SelectionResultPayload`.

6. **Who consumes it?**

   `_from_pressure_selection(...)` consumes the helper result and passes it to `_selection_path_from_payloads(...)`.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining candidates must still be selected from implementation evidence, not naming symmetry. After this slice, the immediate supported pressure-selection payload responsibilities around `_from_pressure_selection(...)` are named for result, reason, supporting evidence, lineage, unknowns, selected pressure lookup, selected-name preparation, and route-specific assembly. Any future slice should first inspect current code for a narrower still-compressed responsibility before moving to broader dispatch, formatting, target normalization, or compatibility assembly. No acceptance, action, planning, prioritization, route authority, readiness evaluation, inquiry generation, event-ledger mutation, or cluster mutation responsibility is introduced or implied by this slice.
