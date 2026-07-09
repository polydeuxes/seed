# Frontier Pressure Admission Slice 010

## Selected boundary

Recovered implementation-local ownership boundary: **selected pressure item lookup ownership inside `selection_path_audit`**.

The selected boundary is the local lookup step that identifies the leading `PressureItem` used by existing pressure-backed selection explanation paths. The lookup is now carried by `_selected_pressure_item(...)` before existing selected-name, evidence, and non-selected-candidate preparation continue unchanged.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` in the implementation immediately adjacent to the most recent focus-selection target matching slice. The current implementation already separated target matching for focus selection and pressure categories, unsupported-target refusal preparation, selected result/reason/support payload ownership, candidate set ownership, selection-factor ownership, non-selected ownership, and typed-unknown ownership.

The remaining adjacent pressure-backed path still repeated the same leading-candidate lookup in three places:

- the focus-selection route in `build_selection_path_audit(...)` looked at the first pressure item before preparing the selected value;
- the pressure-category route in `build_selection_path_audit(...)` looked at the first pressure item before preparing the selected value;
- `_from_pressure_selection(...)` looked at the first pressure item before preparing supporting evidence and non-selected candidates.

That repeated lookup was a local implementation responsibility. It did not own target matching, selected-name fallback, payload construction, public rendering, JSON shape, diagnostic registration, recording, event-ledger writes, mutation, planning, prioritization, inquiry generation, or acceptance authority.

## Before

The selected pressure item lookup was compressed into the callers as inline tuple access:

```python
selected_item = pressure.pressures[0] if pressure.pressures else None
```

and:

```python
selected_item = pressures[0] if pressures else None
```

That left leading-pressure lookup mixed with route handling in `build_selection_path_audit(...)` and with pressure-backed selection payload assembly in `_from_pressure_selection(...)`.

## After

`build_selection_path_audit(...)` and `_from_pressure_selection(...)` now delegate exactly that lookup responsibility to `_selected_pressure_item(pressures)`.

The helper returns only the first `PressureItem` when pressure candidates exist, or `None` when they do not. It does not decide whether a target is implemented, choose a route, prepare selected-name fallback, build output payloads, mutate state, write events, or create any new authority surface.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_selected_pressure_item(...)` now owns production of the local selected-pressure-item lookup result.

## Recovered artifact/helper

`_selected_pressure_item(pressures: tuple[PressureItem, ...]) -> PressureItem | None` carries the recovered boundary.

## Recovered consumer

`build_selection_path_audit(...)` consumes the lookup result for the existing focus-selection and pressure-category routes before calling `_from_pressure_selection(...)`. `_from_pressure_selection(...)` consumes the same helper result before preparing supporting evidence and non-selected-candidate lineage.

## Compatibility preserved

No.

No compatibility boundary changed. Public CLI behavior, JSON output shape, human-readable output, schema, diagnostic visibility, event-ledger behavior, and the read-only mutation boundary are preserved. The change only names an implementation-local lookup handoff already present in code pressure.

## LOC changed

- `seed_runtime/selection_path_audit.py`: 7 insertions, 3 deletions.
- `tests/test_selection_path_audit.py`: 23 insertions, 0 deletions.
- `frontier_pressure_admission_slice_010.md`: 112 insertions, 0 deletions.
- Total: 142 insertions, 3 deletions.

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `python -m pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 122 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Selected pressure item lookup was compressed with focus-route selected-value preparation, pressure-category selected-value preparation, supporting-evidence preparation, and non-selected-candidate preparation.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary for identifying the leading pressure candidate, or absence of one, became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   Repeated inline first-pressure tuple access was replaced with `_selected_pressure_item(...)`, and `tests/test_selection_path_audit.py` now directly exercises populated and empty pressure candidate lookup through that helper.

4. **What producer now owns the recovered responsibility?**

   `_selected_pressure_item(...)` owns production of the local selected-pressure-item lookup result.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_selected_pressure_item(pressures: tuple[PressureItem, ...]) -> PressureItem | None` carries the boundary.

6. **Who consumes it?**

   `build_selection_path_audit(...)` consumes it in the supported focus-selection and pressure-category routes, and `_from_pressure_selection(...)` consumes it while preparing the existing pressure-backed selection explanation.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated from current implementation evidence rather than campaign history, naming symmetry, or architectural preference. After this slice, nearby responsibilities still present in `build_selection_path_audit(...)` include selected-name fallback preparation for focus/category routes and target-route ordering among implemented selection surfaces. Those are not recovered here because this slice recovers exactly one directly evidenced boundary.
