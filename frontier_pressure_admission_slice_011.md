# Frontier Pressure Admission Slice 011

## Selected boundary

Supported pressure-selection reason payload preparation.

## Implementation evidence

Investigation began at `selection_path_audit` and the implementation immediately adjacent to selected pressure item lookup. The supported pressure-selection path already had separately named payloads and lineage producers, and the most recent local neighbor `_selected_pressure_item(...)` owned pressure candidate lookup. The remaining compressed responsibility in the same supported path was the construction of the supported selection outcome/reason payload inside `_from_pressure_selection(...)` while that function also coordinated selected item lookup, supporting evidence, candidate set lineage, selection factors, non-selected explanation, and unknown preservation.

The implementation evidence was local: `_from_pressure_selection(...)` was still directly building `_SelectionReasonPayload(outcome={...})` inline even though `_SelectionReasonPayload` already represented the reason payload shape and other responsibilities in this neighborhood had local producers.

## Before

`_from_pressure_selection(...)` simultaneously:

1. selected the pressure item;
2. derived selection unknowns;
3. built the public result payload;
4. constructed the supported selection reason/outcome payload inline;
5. built supporting evidence;
6. built candidate lineage, factors, non-selected candidates, and unknowns;
7. handed all payloads to `_selection_path_from_payloads(...)`.

The supported selection reason payload existed as a data shape, but its producer was compressed into the broader pressure-selection assembly function.

## After

`_pressure_selection_reason_payload(selected, focus)` now owns construction of the supported selection reason payload. `_from_pressure_selection(...)` consumes that helper and remains the local assembly point for the supported pressure-selection audit without changing output or behavior.

## Required questions

1. **What responsibilities were previously compressed?**
   Supported pressure-selection assembly and supported pressure-selection reason payload construction were compressed inside `_from_pressure_selection(...)`.

2. **Which implementation-local ownership boundary became directly observable?**
   The boundary between assembling a supported pressure-selection audit and producing the supported selection reason/outcome payload became directly observable.

3. **What implementation and/or test change made the boundary observable?**
   The implementation added `_pressure_selection_reason_payload(selected, focus)` and changed `_from_pressure_selection(...)` to consume it. The test suite added `test_pressure_selection_reason_payload_is_owned_by_local_helper()` to prove the helper owns the reason payload and does not own evidence, candidates, or selection factors.

4. **What producer now owns the recovered responsibility?**
   `_pressure_selection_reason_payload(...)` owns supported pressure-selection reason payload construction.

5. **What artifact or helper carries the recovered boundary, if any?**
   `_pressure_selection_reason_payload(...)` carries the recovered boundary and returns `_SelectionReasonPayload`.

6. **Who consumes it?**
   `_from_pressure_selection(...)` consumes the recovered helper.

7. **Did any compatibility boundary change?**
   No.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

- `_pressure_selection_reason_payload(...)`

## Recovered artifact/helper

- Helper: `_pressure_selection_reason_payload(...)`
- Payload artifact: `_SelectionReasonPayload`

## Recovered consumer

- `_from_pressure_selection(...)`

## Compatibility preserved

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory, diagnostic shape-audit behavior, schema, event-ledger behavior, and the read-only mutation boundary are preserved.

Expected compatibility answer:

```text id="k8e6xd"
No.
```

## LOC changed

`git diff --numstat` after the slice showed:

- `seed_runtime/selection_path_audit.py`: 13 insertions, 7 deletions
- `tests/test_selection_path_audit.py`: 17 insertions, 0 deletions
- `frontier_pressure_admission_slice_011.md`: new slice report (100 lines)

## Tests executed

- `pytest -q tests/test_selection_path_audit.py` — passed, 19 tests.
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 104 tests.

## Remaining compressed responsibilities

Remaining compression should be evaluated only from future implementation evidence. In the immediate supported pressure-selection path, `_from_pressure_selection(...)` still coordinates multiple already named payload producers. Further movement is not justified here unless a future local implementation pressure shows another responsibility is still compressed and not already adequately separated and covered.
