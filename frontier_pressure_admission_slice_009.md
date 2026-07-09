# Frontier Pressure Admission Slice 009

## Selected boundary

Recovered implementation-local ownership boundary: **focus-selection target matching ownership inside `selection_path_audit`**.

The selected boundary is the local recognition step where `build_selection_path_audit(...)` decides whether a normalized target names the implemented focus-backed selection route: `current_focus`, `primary_pressure`, or the current operational-story focus text. That recognition is now carried by `_target_matches_focus_selection(...)` before the existing pressure-backed selection explanation path runs.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` next to the most recent pressure-category target matching slice. The current implementation already separated pressure-category target matching into `_target_matches_pressure_category(...)`, unsupported-target refusal preparation into `_unsupported_target_selection(...)`, and payload ownership for result, reason, support, candidate set, selection factors, non-selected candidates, and typed unknowns.

The immediately adjacent supported focus route still compressed three target-recognition checks directly inside `build_selection_path_audit(...)`:

- exact normalized `current_focus` surface recognition;
- exact normalized `primary_pressure` surface recognition;
- normalized matching against `story.focus`.

Those checks were only used to decide whether to enter the existing focus/primary-pressure pressure-backed explanation path. They did not own selected-item lookup, selected-name production, payload construction, unknown preservation, candidate ordering, or output rendering.

## Before

`build_selection_path_audit(...)` directly evaluated:

```python
normalized in {"current_focus", "primary_pressure"} or _matches_target(normalized, story.focus)
```

That left focus-selection target recognition compressed inside the builder alongside pressure audit collection, operational story collection, selected-item lookup, selected-name preparation, pressure-category routing, and unsupported-target fallback routing.

## After

`build_selection_path_audit(...)` delegates exactly that recognition responsibility to `_target_matches_focus_selection(normalized, story.focus)`.

The helper returns only a boolean target-match result. It does not produce selected values, candidate payloads, selection factors, non-selected alternatives, supporting evidence, unknowns, public JSON, human-readable output, events, facts, cluster mutation, planning, action, or priority decisions.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_target_matches_focus_selection(...)` now owns production of the local focus-selection target-match decision.

## Recovered artifact/helper

`_target_matches_focus_selection(normalized_target, focus) -> bool` carries the recovered boundary.

## Recovered consumer

`build_selection_path_audit(...)` consumes the boolean focus-selection target-match result to decide whether to enter the existing `_from_pressure_selection(...)` path for implemented focus/primary-pressure selection explanation.

## Compatibility preserved

No.

No compatibility boundary changed. Public CLI behavior, JSON output shape, human-readable output, schema, diagnostic visibility, event-ledger behavior, and read-only mutation boundary are preserved. The change only names an implementation-local boolean handoff already present in code pressure.

## LOC changed

- `seed_runtime/selection_path_audit.py`: 8 insertions, 3 deletions.
- `tests/test_selection_path_audit.py`: 20 insertions, 0 deletions.
- Total: 28 insertions, 3 deletions.

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `python -m pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 121 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Focus-selection target recognition was compressed inside `build_selection_path_audit(...)` with pressure audit collection, operational story collection, selected-item lookup, selected-name preparation, pressure-category routing, selection payload construction, and unsupported-target fallback routing.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary for deciding whether a normalized target matches the implemented focus-selection route became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   The inline focus/primary-pressure/story-focus target check was replaced with `_target_matches_focus_selection(...)`, and `tests/test_selection_path_audit.py` now directly exercises exact normalized `current_focus` recognition, exact normalized `primary_pressure` recognition, normalized story-focus matching, and non-matching targets.

4. **What producer now owns the recovered responsibility?**

   `_target_matches_focus_selection(...)` owns production of the local focus-selection target-match result.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_target_matches_focus_selection(normalized_target, focus) -> bool` carries the boundary.

6. **Who consumes it?**

   `build_selection_path_audit(...)` consumes it before choosing the existing `_from_pressure_selection(...)` path or continuing to pressure-category matching and unsupported-target fallback.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should be evaluated from current implementation evidence rather than naming symmetry or campaign history. After this slice, nearby responsibilities still present in `build_selection_path_audit(...)` include selected-item lookup before `_from_pressure_selection(...)` in supported routes, selected-name preparation for focus/category routes, and target-route ordering among implemented selection surfaces. Those are not recovered here because this slice recovers exactly one directly evidenced boundary.
