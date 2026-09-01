# Frontier Pressure Admission Slice 027

Recovered implementation-local ownership boundary: **supported pressure-selection payload bundle preparation inside `selection_path_audit`**.

## Selected boundary

The selected boundary is the local producer that gathers the already-separated supported pressure-selection payloads before the compatibility handoff builds `SelectionPathAudit`.

This is narrower than broad route dispatch and audit assembly: each individual supported pressure-selection payload was already named, but `_from_pressure_selection(...)` still owned the coordination of selected-item lookup, unknown preparation, result payload, reason payload, supporting-evidence payload, and lineage payload in the same body that handed material to the public audit composer.

## Implementation evidence

Investigation began in `seed_runtime/selection_path_audit.py` at `build_selection_path_audit(...)`, `_from_focus_selection(...)`, `_from_pressure_category_selection(...)`, and `_from_pressure_selection(...)`.

Current repository evidence showed:

1. Focus and pressure-category branches already delegated selected-name preparation to named helpers.
2. Supported pressure-selection result, reason, supporting evidence, lineage, selected-item lookup, unknown preparation, candidate-set preparation, factor preparation, and non-selected preparation were already separated.
3. `_from_pressure_selection(...)` still directly gathered all payload pieces and passed them to the compatibility handoff.
4. No narrower inline payload construction remained inside `_from_pressure_selection(...)`; the remaining compressed responsibility was the local bundle preparation that decides which already-separated payload producers feed one supported pressure-selection audit.

## Before

`_from_pressure_selection(...)` did both jobs:

- prepared supported pressure-selection payload inputs (`selected_item` and `unknowns`);
- called each supported payload producer directly;
- handed individual payloads to `_selection_path_from_payloads(...)`.

That made the supported pressure-selection payload bundle implicit inside orchestration.

## After

`_from_pressure_selection(...)` now consumes `_pressure_selection_payloads(...)` and passes the returned `_SelectionPathPayloads` bundle to `_selection_path_from_payload_bundle(...)`.

`_pressure_selection_payloads(...)` owns only the local responsibility of preparing the supported pressure-selection payload bundle from already-existing payload producers. It does not route targets, choose acceptance, mutate state, record facts, write the event ledger, plan, prioritize, generate inquiries, or change public output.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`
  - Added `_SelectionPathPayloads` as the implementation-local artifact carrying result, reason, support, and lineage payloads together.
  - Added `_selection_path_from_payload_bundle(...)` while preserving `_selection_path_from_payloads(...)` as the compatibility wrapper for existing tests and callers.
  - Replaced direct payload gathering in `_from_pressure_selection(...)` with `_pressure_selection_payloads(...)`.
  - Added `_pressure_selection_payloads(...)` as the named producer for supported pressure-selection payload bundle preparation.

## Test files changed

- `tests/test_selection_path_audit.py`
  - Added `test_pressure_selection_payload_bundle_is_owned_by_local_helper` to directly exercise `_pressure_selection_payloads(...)` and prove it returns the expected result, reason, supporting-evidence, lineage, non-selected, and unknown payload positions without changing public audit behavior.

## Recovered producer

`_pressure_selection_payloads(selected, pressures, focus)`.

## Recovered artifact/helper

- Artifact: `_SelectionPathPayloads`.
- Helper: `_pressure_selection_payloads(...)`.

## Recovered consumer

`_from_pressure_selection(...)` consumes `_SelectionPathPayloads` and passes it to `_selection_path_from_payload_bundle(...)`, which performs the unchanged public `SelectionPathAudit` compatibility handoff.

## Compatibility preserved

No compatibility boundary changed.

Expected compatibility answer:

```text
No.
```

The public CLI, JSON shape, human-readable output, diagnostics, read-only boundary, event-ledger behavior, and mutation boundary remain unchanged.

## LOC changed

From `git diff --stat`:

```text
seed_runtime/selection_path_audit.py | 58 +++++++++++++++++++++++++++---------
tests/test_selection_path_audit.py   | 44 +++++++++++++++++++++++++++
2 files changed, 88 insertions(+), 14 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py`
- `python -m black tests/test_selection_path_audit.py`
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

Result: 140 passed.

## Required questions

1. **What responsibilities were previously compressed?**

   Supported pressure-selection orchestration and supported pressure-selection payload bundle preparation were compressed inside `_from_pressure_selection(...)`. The individual payload producers existed, but the local bundle that coordinates them for a supported pressure-selection audit was still implicit in the route helper.

2. **Which implementation-local ownership boundary became directly observable?**

   Supported pressure-selection payload bundle preparation became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   `_pressure_selection_payloads(...)` now prepares the bundle, `_SelectionPathPayloads` carries it, `_from_pressure_selection(...)` consumes it, and `test_pressure_selection_payload_bundle_is_owned_by_local_helper` directly exercises the helper.

4. **What producer now owns the recovered responsibility?**

   `_pressure_selection_payloads(...)`.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_SelectionPathPayloads` carries the bundle, and `_pressure_selection_payloads(...)` prepares it.

6. **Who consumes it?**

   `_from_pressure_selection(...)` consumes the bundle and passes it to `_selection_path_from_payload_bundle(...)`.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining candidates must continue to be selected from current implementation evidence, not campaign history or naming symmetry. After this slice, the immediate supported pressure-selection payload construction around `_from_pressure_selection(...)` is separated into named producers and a named bundle. Any future slice should first inspect whether a still-narrower implementation-local responsibility remains compressed before moving to broader target routing, public audit construction, formatting, target normalization, or generic abstractions. This slice does not introduce acceptance, action, mutation, execution, planning, prioritization, inquiry generation, route authority, readiness evaluation, event-ledger writes, or cluster mutation.
