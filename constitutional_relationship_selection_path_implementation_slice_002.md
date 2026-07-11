# Constitutional Relationship Selection Path Implementation Slice 002

## Selected boundary

Focus selected-result production is now an implementation-local ownership boundary.

This slice recovers only the responsibility immediately adjacent to Slice 001's selection-target resolution path: after `_selection_target_selection(...)` classifies a target as `focus`, `_from_focus_selection(...)` now consumes a local focus result artifact instead of directly holding the focus selected-result production expression.

This slice does not force pressure-category selected-result production, unsupported-target payload production, pressure-selection payload composition, candidate integration, factor integration, non-selected integration, evidence integration, lineage integration, typed Unknown integration, compatibility handoff, orchestration, or any architectural redesign.

## Implementation evidence

Repository implementation evidence selected this boundary:

- Slice 001 made target classification explicit with `_selection_target_selection(...)` and `_SelectionTargetSelection`.
- The first target-specific producer immediately adjacent to the `focus` dispatch branch is `_from_focus_selection(...)`.
- `_from_focus_selection(...)` already had a recurring local responsibility distinct from payload assembly: converting the resolved focus target context into the selected public result value.
- Existing helper evidence already separated the compatibility cases for `current_focus`, `primary_pressure`, and fallback pressure-name selection through `_focus_selection_selected_name(...)`.
- `_from_focus_selection(...)` consumed that selected value before handing off to the existing shared pressure-selection path.

The directly observable compressed responsibility was therefore focus selected-result production, not public audit assembly or broader pressure payload composition.

## Before

After Slice 001, `_from_focus_selection(...)` still compressed these responsibilities together:

1. selected pressure item lookup;
2. focus selected-name production;
3. handoff to shared pressure-selection audit construction.

The selected-name helper existed, but no local artifact represented the focus selected result as a producer-owned boundary between focus target handling and shared pressure-selection handoff.

## After

`_from_focus_selection(...)` still performs selected pressure item lookup and still hands off to `_from_pressure_selection(...)` with the same selected string.

The focus selected-result responsibility is now owned by `_focus_selection_result(...)`, which returns `_FocusSelectionResult` with only:

- `selected`

`_FocusSelectionResult` intentionally carries no target, outcome, evidence, candidate, lineage, Unknown, boundary, or compatibility fields.

## Recovered producer

`_focus_selection_result(...)` now owns the recovered implementation-local responsibility: producing the selected result for focus-target Selection Path handling.

## Recovered artifact/helper

`_FocusSelectionResult` carries the recovered boundary.

It is deliberately narrower than `_SelectionResultPayload`; it represents only the focus producer's local selected-result decision before the existing shared pressure-selection payload assembly runs.

Existing helper `_focus_selection_selected_name(...)` remains the compatibility-preserving name helper consumed by the recovered producer.

## Recovered consumer

`_from_focus_selection(...)` consumes `_FocusSelectionResult` and passes `result.selected` to `_from_pressure_selection(...)`.

The downstream consumer chain remains unchanged:

```text
_from_focus_selection(...)
→ _from_pressure_selection(...)
→ _pressure_selection_payloads(...)
→ _selection_path_from_payload_bundle(...)
→ SelectionPathAudit
```

## Compatibility preserved

No compatibility boundary changed.

Preserved boundaries:

- selection-target resolution ownership from Slice 001;
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
- `constitutional_relationship_selection_path_implementation_slice_002.md`

Slice 001 remains unchanged.

## LOC changed

Implementation and test diff before this report:

- `seed_runtime/selection_path_audit.py`: 15 insertions and 6 deletions.
- `tests/test_selection_path_audit.py`: 34 insertions.
- Combined implementation/test diff before this report: 49 insertions and 6 deletions.

Including this report, the final repository diff also adds this markdown deliverable.

## Tests executed

- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 157 tests.
- `git diff --check` — passed.

## Required questions

1. **What responsibilities were previously compressed?** Selected pressure item lookup, focus selected-result production, and shared pressure-selection handoff were compressed inside `_from_focus_selection(...)`.
2. **Which implementation-local ownership boundary became directly observable?** Focus selected-result production became directly observable between focus target handling and shared pressure-selection handoff.
3. **What producer now owns the recovered responsibility?** `_focus_selection_result(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** `_FocusSelectionResult` carries the selected focus result; `_focus_selection_selected_name(...)` remains the narrower name helper used by that producer.
5. **Who consumes it?** `_from_focus_selection(...)` consumes `_FocusSelectionResult` and passes `result.selected` to `_from_pressure_selection(...)`.
6. **Did any compatibility boundary change?** No.

## Remaining compressed responsibilities

The following responsibilities remain intentionally compressed or only partially separated for future repository-evidence-driven recovery slices:

- public audit construction and compatibility handoff;
- pressure-category selected-result production;
- pressure-selection payload bundle composition;
- unsupported-target payload bundle composition;
- candidate integration;
- factor integration;
- non-selected integration;
- evidence integration;
- lineage integration;
- typed Unknown integration.
