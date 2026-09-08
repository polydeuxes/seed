# Frontier Pressure Admission Slice 008

## Selected boundary

Recovered implementation-local ownership boundary: **pressure-category target matching ownership inside `selection_path_audit`**.

The selected boundary is the local handoff where `build_selection_path_audit(...)` stops owning the inline scan that decides whether the requested target names an implemented pressure-category selection surface. That category-match admission check is now carried by `_target_matches_pressure_category(...)` before the existing supported-selection payload construction or unsupported-target refusal preparation runs.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` next to the most recent unsupported-target slice. The current builder already separated unsupported-target audit preparation into `_unsupported_target_selection(...)`, while the immediately adjacent supported pressure-category branch still compressed target matching into an inline `matching = [...]` list whose contents were only used as a truth test. The selected pressure item and selected name remained owned by the existing `_from_pressure_selection(...)` path; the still-compressed responsibility was only the determination that a normalized target matches at least one pressure category.

This is implementation evidence rather than campaign-history evidence because the inline list was adjacent to the unsupported-target fallback and was not consumed for candidate construction, scoring, ranking, selected item ownership, non-selected explanation, unknown ownership, or payload composition. It existed solely to determine whether the target should use the implemented pressure-backed selection explanation path.

## Before

`build_selection_path_audit(...)` directly built a local `matching` list by scanning `pressure.pressures` for `_matches_target(normalized, item.category)`. The branch then used only the list truthiness, leaving pressure-category target recognition compressed inside the builder alongside target routing, pressure/story collection, selected-name preparation, payload production, and fallback refusal handoff.

## After

`build_selection_path_audit(...)` delegates that one responsibility to `_target_matches_pressure_category(normalized, pressure.pressures)`. The helper returns only whether the normalized target matches any pressure category and does not produce selected results, candidate payloads, selection factors, unknowns, refusal payloads, or public output.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_target_matches_pressure_category(...)` now owns pressure-category target-match production for the local selection-path builder.

## Recovered artifact/helper

`_target_matches_pressure_category(normalized_target, pressures) -> bool` carries the recovered boundary.

## Recovered consumer

`build_selection_path_audit(...)` consumes the boolean pressure-category target-match result to decide whether to enter the existing pressure-backed selection explanation path or continue to `_unsupported_target_selection(...)`.

## Compatibility preserved

No.

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and the read-only mutation boundary are preserved. The helper only replaces an inline truthiness check with the same `any(_matches_target(...))` predicate.

## Required questions

1. **What responsibilities were previously compressed?**

   Pressure-category target recognition was compressed inside `build_selection_path_audit(...)` with target routing, selection payload preparation, and unsupported-target fallback routing.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between target-category match recognition and selection audit payload construction became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   The inline `matching = [...]` scan was replaced with `_target_matches_pressure_category(...)`, and `tests/test_selection_path_audit.py` now directly exercises exact normalized category matching, partial normalized category matching, and non-matching targets.

4. **What producer now owns the recovered responsibility?**

   `_target_matches_pressure_category(...)` owns production of the local pressure-category match decision.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_target_matches_pressure_category(...)` carries the recovered boundary.

6. **Who consumes it?**

   `build_selection_path_audit(...)` consumes it before choosing the existing `_from_pressure_selection(...)` path or falling through to `_unsupported_target_selection(...)`.

7. **Did any compatibility boundary change?**

   No.

## LOC changed

- `seed_runtime/selection_path_audit.py`: 7 insertions, 6 deletions.
- `tests/test_selection_path_audit.py`: 26 insertions, 0 deletions.
- Total: 33 insertions, 6 deletions.

## Tests executed

- `python -m pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 120 tests.

## Remaining compressed responsibilities

Remaining compression should be evaluated from current implementation evidence, not naming symmetry or campaign history. After this slice, nearby responsibilities still present in `build_selection_path_audit(...)` include supported target routing for current focus / primary pressure / story focus, repeated selected-item lookup before `_from_pressure_selection(...)`, and the compatibility seam between normalized user target strings and implemented selection surfaces. Those are not recovered here because this slice recovers exactly one directly evidenced boundary.
