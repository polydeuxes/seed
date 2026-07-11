# Constitutional Relationship Selection Path Implementation Slice 003

## Selected boundary

Pressure-category selected-result production is now an implementation-local ownership boundary.

This slice recovers only the responsibility immediately adjacent to Slice 002's focus selected-result path: after `_selection_target_selection(...)` classifies a target as `pressure_category`, `_from_pressure_category_selection(...)` now consumes a local pressure-category result artifact instead of directly holding the pressure-category selected-result production expression.

This slice does not force unsupported-target payload production, pressure-selection payload bundle composition, candidate integration, factor integration, non-selected integration, evidence integration, lineage integration, typed Unknown integration, compatibility handoff, orchestration, or any architectural redesign.

## Implementation evidence

Repository implementation evidence selected this boundary:

- Slice 001 made target classification explicit with `_selection_target_selection(...)` and `_SelectionTargetSelection`.
- Slice 002 made focus selected-result production explicit with `_focus_selection_result(...)` and `_FocusSelectionResult`.
- The directly adjacent sibling target-specific producer is `_from_pressure_category_selection(...)`.
- `_from_pressure_category_selection(...)` already had the same recurring local responsibility shape as the recovered focus path: selected pressure item lookup, selected public result production, and handoff to `_from_pressure_selection(...)`.
- Existing helper evidence already separated pressure-category selected-name compatibility through `_pressure_category_selection_selected_name(...)`.
- `_from_pressure_category_selection(...)` consumed that selected value before handing off to the existing shared pressure-selection path.

The directly observable compressed responsibility was therefore pressure-category selected-result production, not payload composition or compatibility handoff.

## Before

After Slice 002, `_from_pressure_category_selection(...)` still compressed these responsibilities together:

1. selected pressure item lookup;
2. pressure-category selected-name production;
3. handoff to shared pressure-selection audit construction.

The selected-name helper existed, but no local artifact represented the pressure-category selected result as a producer-owned boundary between pressure-category target handling and shared pressure-selection handoff.

## After

`_from_pressure_category_selection(...)` still performs selected pressure item lookup and still hands off to `_from_pressure_selection(...)` with the same selected string.

The pressure-category selected-result responsibility is now owned by `_pressure_category_selection_result(...)`, which returns `_PressureCategorySelectionResult` with only:

- `selected`

`_PressureCategorySelectionResult` intentionally carries no target, outcome, evidence, candidate, lineage, Unknown, boundary, or compatibility fields.

## Recovered producer

`_pressure_category_selection_result(...)` now owns the recovered implementation-local responsibility: producing the selected result for pressure-category Selection Path handling.

## Recovered artifact/helper

`_PressureCategorySelectionResult` carries the recovered boundary.

It is deliberately narrower than `_SelectionResultPayload`; it represents only the pressure-category producer's local selected-result decision before the existing shared pressure-selection payload assembly runs.

Existing helper `_pressure_category_selection_selected_name(...)` remains the compatibility-preserving name helper consumed by the recovered producer.

## Recovered consumer

`_from_pressure_category_selection(...)` consumes `_PressureCategorySelectionResult` and passes `result.selected` to `_from_pressure_selection(...)`.

The downstream consumer chain remains unchanged:

```text
_from_pressure_category_selection(...)
→ _from_pressure_selection(...)
→ _pressure_selection_payloads(...)
→ _selection_path_from_payload_bundle(...)
→ SelectionPathAudit
```

## Compatibility preserved

No compatibility boundary changed.

Preserved boundaries:

- selection-target resolution ownership from Slice 001;
- focus selected-result production ownership from Slice 002;
- public CLI behavior;
- JSON output shape;
- text rendering;
- `SelectionPathAudit` compatibility shape;
- existing payload artifacts;
- existing helper artifacts;
- read-only behavior;
- typed Unknown behavior;
- lineage behavior;
- candidate behavior;
- evidence behavior;
- no fact recording;
- no event-ledger writes;
- no cluster mutation.

## Files changed

- `seed_runtime/selection_path_audit.py`
- `tests/test_selection_path_audit.py`
- `constitutional_relationship_selection_path_implementation_slice_003.md`

Slices 001–002 remain unchanged.

## LOC changed

Implementation and test diff before this report:

- `seed_runtime/selection_path_audit.py`: 15 insertions and 6 deletions.
- `tests/test_selection_path_audit.py`: 23 insertions.
- Combined implementation/test diff before this report: 38 insertions and 6 deletions.

Including this report, the final repository diff also adds this markdown deliverable.

## Tests executed

- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed.
- `git diff --check` — passed.

## Required questions

1. **What responsibilities were previously compressed?** Selected pressure item lookup, pressure-category selected-result production, and shared pressure-selection handoff were compressed inside `_from_pressure_category_selection(...)`.
2. **Which implementation-local ownership boundary became directly observable?** Pressure-category selected-result production became directly observable between pressure-category target handling and shared pressure-selection handoff.
3. **What producer now owns the recovered responsibility?** `_pressure_category_selection_result(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** `_PressureCategorySelectionResult` carries the selected pressure-category result; `_pressure_category_selection_selected_name(...)` remains the narrower name helper used by that producer.
5. **Who consumes it?** `_from_pressure_category_selection(...)` consumes `_PressureCategorySelectionResult` and passes `result.selected` to `_from_pressure_selection(...)`.
6. **Did any compatibility boundary change?** No.

## Remaining compressed responsibilities

The following responsibilities remain intentionally compressed or only partially separated for future repository-evidence-driven recovery slices:

- public audit construction and compatibility handoff;
- pressure-selection payload bundle composition;
- unsupported-target payload bundle composition;
- candidate integration;
- factor integration;
- non-selected integration;
- evidence integration;
- lineage integration;
- typed Unknown integration.
