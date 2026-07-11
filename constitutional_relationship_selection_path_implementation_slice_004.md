# Constitutional Relationship Selection Path Implementation Slice 004

## Selected boundary

Pressure-selection payload bundle composition is now recorded as the next implementation-local ownership boundary.

This slice recovers only the responsibility immediately adjacent to Slice 003's pressure-category selected-result handoff: both implemented selected-result producers now converge through `_from_pressure_selection(...)`, which delegates pressure-selection payload bundle production to `_pressure_selection_payloads(...)` before the existing compatibility handoff constructs `SelectionPathAudit`.

This slice does not force unsupported-target payload production, candidate integration, factor integration, non-selected integration, evidence integration, lineage integration, typed Unknown integration, compatibility handoff, orchestration, or any architectural redesign.

## Implementation evidence

Repository implementation evidence selected this boundary:

- Slice 002 made focus selected-result production explicit with `_focus_selection_result(...)` and `_FocusSelectionResult`.
- Slice 003 made pressure-category selected-result production explicit with `_pressure_category_selection_result(...)` and `_PressureCategorySelectionResult`.
- The next shared implementation step immediately downstream of both selected-result producers is `_from_pressure_selection(...)`.
- `_from_pressure_selection(...)` does not build candidates, factors, non-selected rows, evidence rows, Unknowns, or public audit fields directly; it consumes a selected string and hands off to `_pressure_selection_payloads(...)`.
- `_pressure_selection_payloads(...)` is already the local producer that composes the existing `_SelectionPathPayloads` bundle from the selected result, reason, support, and lineage payload producers.
- Existing focused test coverage proves that the bundle producer owns result, reason, support, lineage, non-selected, and Unknown payload wiring while still excluding compatibility construction.

The directly observable compressed responsibility was therefore pressure-selection payload bundle composition, not unsupported-target payload production and not any individual candidate, factor, evidence, lineage, Unknown, or compatibility integration boundary.

## Before

After Slice 003, the recovered progression exposed both implemented selected-result branches but still left the shared pressure-selection handoff as the next compressed area:

1. `_from_focus_selection(...)` produced a local focus selected result.
2. `_from_pressure_category_selection(...)` produced a local pressure-category selected result.
3. Both producers handed a selected string into `_from_pressure_selection(...)`.
4. `_from_pressure_selection(...)` immediately requested a complete pressure-selection payload bundle and handed that bundle to the public compatibility constructor.

The shared bundle producer existed, but this slice had not yet recorded it as the next implementation-local ownership boundary immediately adjacent to the recovered branch-local selected-result producers.

## After

`_from_pressure_selection(...)` still preserves the same handoff shape:

```text
_from_pressure_selection(...)
→ _pressure_selection_payloads(...)
→ _selection_path_from_payload_bundle(...)
→ SelectionPathAudit
```

The pressure-selection payload bundle responsibility is owned by `_pressure_selection_payloads(...)`, which returns `_SelectionPathPayloads` with only the existing payload bundle members:

- `result`
- `reason`
- `support`
- `lineage`

`_SelectionPathPayloads` intentionally carries no target, boundary flags, rendering behavior, CLI behavior, event-ledger behavior, fact-recording behavior, or cluster-mutation behavior.

## Recovered producer

`_pressure_selection_payloads(...)` owns the recovered implementation-local responsibility: composing the pressure-selection payload bundle for implemented focus and pressure-category selection paths.

## Recovered artifact/helper

`_SelectionPathPayloads` carries the recovered boundary.

It is deliberately narrower than `SelectionPathAudit`; it represents only the implementation-local payload bundle passed to the existing compatibility handoff. The existing member payload helpers remain narrower producers consumed by this bundle producer:

- `_pressure_selection_result_payload(...)`
- `_pressure_selection_reason_payload(...)`
- `_pressure_selection_supporting_evidence_payload(...)`
- `_pressure_selection_lineage_payload(...)`

## Recovered consumer

`_from_pressure_selection(...)` consumes the recovered producer by passing `_pressure_selection_payloads(...)` into `_selection_path_from_payload_bundle(...)`.

The downstream compatibility consumer remains unchanged:

```text
_selection_path_from_payload_bundle(...)
→ SelectionPathAudit
```

## Compatibility preserved

No compatibility boundary changed.

Preserved boundaries:

- selection-target resolution ownership from Slice 001;
- focus selected-result production ownership from Slice 002;
- pressure-category selected-result production ownership from Slice 003;
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

- `constitutional_relationship_selection_path_implementation_slice_004.md`

Slices 001–003 remain unchanged.

## LOC changed

Documentation diff for this slice:

- `constitutional_relationship_selection_path_implementation_slice_004.md`: 144 insertions.

No implementation or test source lines changed in this slice because the adjacent implementation-local producer and focused proof already existed in repository authority.

## Tests executed

- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed.
- `git diff --check` — passed.

## Required questions

1. **What responsibilities were previously compressed?** Shared pressure-selection result payload production, reason payload production, supporting-evidence payload production, lineage payload production, and bundle handoff were previously compressed as the shared downstream handoff after focus and pressure-category selected-result production.
2. **Which implementation-local ownership boundary became directly observable?** Pressure-selection payload bundle composition became directly observable immediately downstream of the recovered focus and pressure-category selected-result producers.
3. **What producer now owns the recovered responsibility?** `_pressure_selection_payloads(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** `_SelectionPathPayloads` carries the result, reason, support, and lineage payload bundle.
5. **Who consumes it?** `_from_pressure_selection(...)` consumes `_pressure_selection_payloads(...)` and passes the bundle to `_selection_path_from_payload_bundle(...)`; `_selection_path_from_payload_bundle(...)` then constructs `SelectionPathAudit`.
6. **Did any compatibility boundary change?** No.

## Remaining compressed responsibilities

The following responsibilities remain intentionally compressed or only partially separated for future repository-evidence-driven recovery slices:

- public audit construction and compatibility handoff;
- unsupported-target payload bundle composition;
- candidate integration;
- factor integration;
- non-selected integration;
- evidence integration;
- lineage integration;
- typed Unknown integration.
