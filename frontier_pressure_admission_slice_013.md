# Frontier Pressure Admission Slice 013

## Selected boundary

Recovered implementation-local ownership boundary: **supported pressure-selection lineage payload preparation inside `selection_path_audit`**.

The selected boundary is the local handoff where `_from_pressure_selection(...)` stops owning inline construction of the supported pressure-selection lineage payload. That responsibility is now carried by `_pressure_selection_lineage_payload(...)`, which assembles the already-separated candidate-set, selection-factor, non-selected-candidate, and typed-unknown payloads before the existing selection-path compatibility handoff runs.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` around `selection_path_audit` and the implementation immediately adjacent to the most recent `_pressure_selection_supporting_evidence_payload(...)` slice. The current implementation already separated selected pressure item lookup, supported pressure-selection reason payload preparation, supported pressure-selection supporting-evidence payload preparation, candidate-set preparation, selection-factor preparation, non-selected candidate preparation, typed unknown preparation, target matching, and unsupported-target selection preparation.

The adjacent supported-selection implementation still prepared the lineage payload inline inside `_from_pressure_selection(...)`:

- `_from_pressure_selection(...)` obtained the selected pressure item.
- `_from_pressure_selection(...)` prepared pressure-selection unknowns.
- `_from_pressure_selection(...)` directly constructed `_SelectionLineagePayload(...)` while also coordinating result, reason, support, and public selection-path handoff.
- The inline lineage construction grouped candidate-set, factor, non-selected, and unknown payloads even though each payload producer was already separately named.

That made supported pressure-selection lineage payload preparation observable only as an inline expression in the broader supported pressure-selection assembly path.

## Before

`_from_pressure_selection(...)` directly constructed `_SelectionLineagePayload(...)` while also assembling the selected result, supported reason payload, supporting-evidence payload, selected pressure item lookup, pressure unknowns, and public compatibility handoff.

The compressed responsibility was not the individual candidate, factor, non-selected, or unknown producers. Those were already separated. The still-compressed responsibility was the supported pressure-selection lineage payload assembly that grouped those already-owned payloads for `_selection_path_from_payloads(...)`.

## After

`_from_pressure_selection(...)` delegates exactly that lineage payload preparation to `_pressure_selection_lineage_payload(pressures, selected_item, unknowns)`. The helper owns only construction of `_SelectionLineagePayload` from the already-separated lineage component payloads. It does not select candidates, match targets, produce reasons, produce supporting evidence, mutate state, record facts, write events, or alter public output.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

Producer: `_pressure_selection_lineage_payload(...)`, called by `_from_pressure_selection(...)` while preparing supported pressure-selection audit output.

## Recovered artifact/helper

Artifact/helper: `_pressure_selection_lineage_payload(...)`, returning `_SelectionLineagePayload`.

## Recovered consumer

Consumer: `_from_pressure_selection(...)` consumes the lineage payload and passes it unchanged into `_selection_path_from_payloads(...)`, which preserves the existing public `SelectionPathAudit.candidates`, `SelectionPathAudit.selection_factors`, `SelectionPathAudit.non_selected`, and `SelectionPathAudit.unknowns` output.

## Compatibility preserved

No.

No compatibility boundary changed. Public CLI behavior, JSON shape, human-readable output, schema, diagnostic inventory behavior, diagnostic shape-audit behavior, event-ledger behavior, and read-only mutation boundary are preserved.

## LOC changed

`git diff --numstat` for the implementation and test slice showed:

- `seed_runtime/selection_path_audit.py`: 14 insertions, 6 deletions.
- `tests/test_selection_path_audit.py`: 57 insertions, 0 deletions.

After adding this report, the total repository diff also includes this new slice report.

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 125 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Supported pressure-selection assembly and supported pressure-selection lineage payload preparation were compressed inside `_from_pressure_selection(...)`. The already-separated candidate-set, selection-factor, non-selected-candidate, and typed-unknown producers were being grouped into `_SelectionLineagePayload(...)` inline next to result, reason, support, and compatibility handoff responsibilities.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between supported pressure-selection assembly and supported pressure-selection lineage payload preparation became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   `_from_pressure_selection(...)` now calls `_pressure_selection_lineage_payload(pressures, selected_item, unknowns)`, and `tests/test_selection_path_audit.py` directly exercises populated lineage payload production while proving the helper does not own selected result, outcome, or supporting evidence fields.

4. **What producer now owns the recovered responsibility?**

   `_pressure_selection_lineage_payload(...)` owns the recovered responsibility.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_pressure_selection_lineage_payload(...)` carries the boundary and returns `_SelectionLineagePayload`.

6. **Who consumes it?**

   `_from_pressure_selection(...)` consumes the helper result before handing the payload to `_selection_path_from_payloads(...)`.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated from current implementation evidence rather than campaign history, naming symmetry, or architectural preference. After this slice, the immediate supported pressure-selection path is primarily an orchestration function over already named payload producers. Nearby implementation responsibilities still include selected-name fallback preparation through `_selected_name(...)` and the target-route ordering between focus and pressure-category paths. They are not recovered here because this slice recovers exactly one implementation-local boundary supported by direct code pressure.
