# Frontier Pressure Admission Slice 018

## Selected boundary

Recovered implementation-local ownership boundary: **unsupported-target typed-unknown preparation inside `selection_path_audit`**.

This slice does not implement Frontier Pressure Admission, acceptance, readiness, planning, prioritization, action, mutation, or inquiry generation. It only separates the already-present typed unknown that explains unsupported selection targets from the broader unsupported-target refusal assembly.

## Implementation evidence

Investigation began in `seed_runtime/selection_path_audit.py`, immediately adjacent to the current `build_selection_path_audit(...)` branch dispatch. Focus-selection and pressure-category branch assembly were already named through `_from_focus_selection(...)` and `_from_pressure_category_selection(...)`. Supported pressure-selection internals were also already separated into helpers for selected item lookup, selected-name derivation, reason payload, supporting evidence, lineage, candidate set, factors, non-selected candidates, and empty-candidate unknowns.

The remaining compressed responsibility visible in the unsupported branch was narrower than branch-level assembly: `_unsupported_target_selection(...)` owned both the unsupported refusal assembly and inline construction of the `Implementation Unknown` explaining that no implementation-backed selection evidence exists for the requested target. That typed unknown is part of lineage/unknown transport, not the same responsibility as selecting `unknown`, setting the human refusal reason, preserving the candidate set, or preserving the read-only boundary.

Because unsupported-target refusal preparation already had a named helper and test coverage, the valid next boundary was not another broad unsupported branch assembly helper. The narrower still-compressed responsibility was the unsupported-target typed-unknown payload itself.

## Before

`_unsupported_target_selection(...)` directly built `_SelectionUnknownPayload(...)` inline while also assembling the complete unsupported-target `SelectionPathAudit` through `_selection_path_from_payloads(...)`. This compressed unsupported refusal assembly with the typed-unknown preservation that explains the unsupported selection logic.

## After

`_unsupported_target_selection(...)` now consumes `_unsupported_target_unknown_payload()`. The new helper owns only construction of the `Implementation Unknown` payload for unsupported targets and returns `_SelectionUnknownPayload` for the existing lineage handoff.

The public audit output, CLI behavior, JSON shape, human-readable output, diagnostic registration, event-ledger behavior, and read-only mutation boundary are unchanged.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`
  - Added `_unsupported_target_unknown_payload()`.
  - Updated `_unsupported_target_selection(...)` to consume the helper instead of constructing the typed unknown inline.

## Test files changed

- `tests/test_selection_path_audit.py`
  - Added `test_unsupported_target_unknown_payload_is_owned_by_local_helper()` to prove the recovered helper owns only the unsupported-target typed unknown payload and does not own candidates, selection factors, or non-selected candidates.

## Recovered producer

`_unsupported_target_unknown_payload()` now produces the unsupported-target `_SelectionUnknownPayload`.

## Recovered artifact/helper

Recovered helper: `_unsupported_target_unknown_payload()`.

Recovered artifact: `_SelectionUnknownPayload` containing one preserved `Implementation Unknown` for `selection_logic` with reason `no implementation-backed selection evidence discovered for target`.

## Recovered consumer

`_unsupported_target_selection(...)` consumes the helper and passes its payload into `_SelectionLineagePayload(...)`, which is then consumed by `_selection_path_from_payloads(...)`.

## Compatibility preserved

No.

No compatibility boundary changed. The expected compatibility answer remains `No.`: public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and read-only mutation boundaries were preserved.

## LOC changed

`git diff --stat` reported:

- `seed_runtime/selection_path_audit.py`: 22 changed lines.
- `tests/test_selection_path_audit.py`: 17 changed lines.
- Total: 30 insertions and 9 deletions across 2 files.

## Tests executed

- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`
  - Result: 131 passed.

## Required questions

1. **What responsibilities were previously compressed?**

   Unsupported-target refusal assembly and unsupported-target typed-unknown preparation were compressed inside `_unsupported_target_selection(...)`.

2. **Which implementation-local ownership boundary became directly observable?**

   Unsupported-target typed-unknown preparation became directly observable as its own implementation-local helper.

3. **What implementation and/or test change made the boundary observable?**

   The implementation now routes unsupported-target unknown construction through `_unsupported_target_unknown_payload()`. The new test `test_unsupported_target_unknown_payload_is_owned_by_local_helper()` verifies that this helper owns the typed unknown payload and does not own candidates, selection factors, or non-selected candidates.

4. **What producer now owns the recovered responsibility?**

   `_unsupported_target_unknown_payload()` owns production of the unsupported-target unknown payload.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_unsupported_target_unknown_payload()` carries the boundary and returns `_SelectionUnknownPayload`.

6. **Who consumes it?**

   `_unsupported_target_selection(...)` consumes it when preparing `_SelectionLineagePayload(...)` for `_selection_path_from_payloads(...)`.

7. **Did any compatibility boundary change?**

   No. Public output, CLI behavior, JSON shape, diagnostics, schema, event-ledger behavior, runtime behavior, and read-only mutation boundaries are unchanged.

## Remaining compressed responsibilities

Remaining pressure, if any, should continue to be selected from implementation evidence only. This slice does not claim that all adjacent boundaries are exhausted. It leaves any future candidate to be proven by the current implementation rather than by campaign history, naming symmetry, or architectural preference.
