# Constitutional Relationship Selection Path Implementation Slice 005

## Selected boundary

Unsupported-target payload bundle composition is now recorded as the next implementation-local ownership boundary immediately adjacent to Slice 004.

Repository implementation evidence selected this boundary because the unsupported target branch already has a local producer path that composes the public audit from unsupported-target payload helpers without entering the implemented pressure-selection bundle producer recovered in Slice 004.

This slice recovers orientation only. No implementation changes were required.

## Implementation evidence

The adjacent implementation path is directly observable in `seed_runtime/selection_path_audit.py`:

```text
build_selection_path_audit(...)
        ↓
_selection_target_selection(...)
        ↓
_SelectionTargetSelection(selection_kind="unsupported")
        ↓
_unsupported_target_selection(...)
        ↓
_selection_path_from_payloads(...)
        ↓
_SelectionPathPayloads
        ↓
_selection_path_from_payload_bundle(...)
        ↓
SelectionPathAudit
```

The unsupported branch is selected only after focus and pressure-category matching fail. `_unsupported_target_selection(...)` then owns the unsupported-target branch handoff by assembling the unsupported result, reason, supporting-evidence, and lineage payloads and passing them to `_selection_path_from_payloads(...)`.

The repository already contains the narrower unsupported-target payload producers:

- `_unsupported_target_result_payload(...)` produces the `selected="unknown"` result payload.
- `_unsupported_target_reason_payload(...)` produces the unsupported-target outcome reason.
- `_unsupported_target_supporting_evidence_payload(...)` produces an empty evidence payload.
- `_unsupported_target_lineage_payload(...)` composes candidate, factor, non-selected, and typed Unknown lineage for unsupported targets.
- `_unsupported_target_unknown_payload(...)` preserves the typed `Implementation Unknown` for missing implementation-backed selection evidence.

Existing tests already prove the observable public behavior for this branch: an unsupported selection target returns `selected == "unknown"`, exposes `selection_factors == ["unknown"]`, and carries the typed Unknown reason without changing public compatibility.

## Before

After Slice 004, the recovered progression made the implemented pressure-selection payload bundle explicit:

```text
_from_focus_selection(...)
        ↓
_focus_selection_result(...)
        ↓
_from_pressure_selection(...)
        ↓
_pressure_selection_payloads(...)
        ↓
_SelectionPathPayloads
        ↓
_selection_path_from_payload_bundle(...)
        ↓
SelectionPathAudit
```

and:

```text
_from_pressure_category_selection(...)
        ↓
_pressure_category_selection_result(...)
        ↓
_from_pressure_selection(...)
        ↓
_pressure_selection_payloads(...)
        ↓
_SelectionPathPayloads
        ↓
_selection_path_from_payload_bundle(...)
        ↓
SelectionPathAudit
```

The unsupported-target path was present, but the campaign had not yet recovered its immediately adjacent branch-local ownership boundary. Its result, reason, supporting evidence, lineage, Unknown, and compatibility handoff were still treated as a compressed unsupported-target responsibility.

## After

The unsupported branch remains implementation-local and unchanged:

```text
_unsupported_target_selection(...)
        ↓
_selection_path_from_payloads(...)
        ↓
_SelectionPathPayloads
        ↓
_selection_path_from_payload_bundle(...)
        ↓
SelectionPathAudit
```

`_unsupported_target_selection(...)` is now recorded as the producer that owns unsupported-target payload bundle composition for the branch where `_selection_target_selection(...)` returns `selection_kind="unsupported"`.

This recovery does not split candidate integration, factor integration, non-selected integration, evidence integration, lineage integration, typed Unknown integration, or public compatibility construction. Those remain separate candidate responsibilities for future slices if repository evidence selects them.

## Recovered producer

`_unsupported_target_selection(...)` owns the recovered responsibility.

It composes the unsupported-target result, reason, support, and lineage payload inputs and hands them to `_selection_path_from_payloads(...)`, which wraps them into `_SelectionPathPayloads` for the existing compatibility handoff.

## Recovered artifact/helper

The recovered boundary is carried by the existing payload helper set and the existing payload bundle artifact:

- `_unsupported_target_result_payload(...)`
- `_unsupported_target_reason_payload(...)`
- `_unsupported_target_supporting_evidence_payload(...)`
- `_unsupported_target_lineage_payload(...)`
- `_SelectionPathPayloads`

No new artifact or helper was introduced.

## Recovered consumer

`build_selection_path_audit(...)` consumes this branch producer when `_selection_target_selection(...)` identifies an unsupported target.

The immediate downstream consumer is `_selection_path_from_payloads(...)`, which converts the branch-local payload inputs into `_SelectionPathPayloads` and passes them to `_selection_path_from_payload_bundle(...)`.

The final public consumer remains `SelectionPathAudit` construction through `_selection_path_from_payload_bundle(...)`.

## Compatibility preserved

No compatibility boundary changed.

Preserved boundaries and behavior:

- selection-target resolution ownership from Slice 001;
- focus selected-result production ownership from Slice 002;
- pressure-category selected-result production ownership from Slice 003;
- pressure-selection payload bundle composition ownership from Slice 004;
- `SelectionPathAudit` public compatibility shape;
- `_SelectionPathPayloads` payload bundle shape;
- existing payload artifacts;
- existing helper artifacts;
- public CLI behavior;
- JSON output shape;
- text rendering;
- read-only behavior;
- typed Unknown behavior;
- lineage behavior;
- candidate behavior;
- evidence behavior;
- no fact recording;
- no event-ledger writes;
- no cluster mutation.

## Files changed

- `constitutional_relationship_selection_path_implementation_slice_005.md`

## LOC changed

Documentation diff for this slice:

- `constitutional_relationship_selection_path_implementation_slice_005.md`: 201 insertions.

No implementation or test source lines changed in this slice because the adjacent implementation-local producer already existed in repository authority.

## Tests executed

- `pytest -q tests/test_selection_path_audit.py` — passed.
- `git diff --check` — passed.

The diagnostic inventory and diagnostic shape-audit tests were not required because this slice added no diagnostic surface, audit behavior, CLI flag, recordable output, event-ledger write, fact recording, or cluster mutation.

## Required questions

1. **What responsibilities were previously compressed?** Unsupported-target result payload production, reason payload production, supporting-evidence payload production, lineage payload production, typed Unknown preservation, and compatibility handoff were previously compressed under the unsupported-target branch.
2. **Which implementation-local ownership boundary became directly observable?** Unsupported-target payload bundle composition became directly observable immediately adjacent to Slice 004's implemented pressure-selection payload bundle boundary.
3. **What producer now owns the recovered responsibility?** `_unsupported_target_selection(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** The existing unsupported-target payload helper set carries the branch-local inputs, and `_SelectionPathPayloads` carries the bundled payload through the compatibility handoff.
5. **Who consumes it?** `build_selection_path_audit(...)` consumes `_unsupported_target_selection(...)` for unsupported selections; `_selection_path_from_payloads(...)` and `_selection_path_from_payload_bundle(...)` consume the produced payloads downstream.
6. **Did any compatibility boundary change?** No.

## Remaining compressed responsibilities

The following responsibilities remain intentionally compressed or only partially separated for future repository-evidence-driven recovery slices:

- public audit construction and compatibility handoff;
- candidate integration;
- factor integration;
- non-selected integration;
- evidence integration;
- lineage integration;
- typed Unknown integration.

## Recovery type

Orientation recovery only.

Repository implementation already contained the adjacent producer and supporting helpers, so this slice records the ownership boundary without manufacturing implementation changes.
