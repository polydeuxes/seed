# Constitutional Relationship Selection Path Implementation Slice 006

## Selected boundary

Payload-bundle compatibility construction is now recorded as the next implementation-local ownership boundary immediately downstream of the recovered branch producers.

Repository implementation evidence selected this boundary because both recovered branch producer families converge on `_SelectionPathPayloads` before a single shared helper constructs the public `SelectionPathAudit` compatibility shape.

This slice recovers orientation only. No implementation changes were required.

## Implementation evidence

The shared downstream implementation path is directly observable in `seed_runtime/selection_path_audit.py`:

```text
_selection_path_from_payloads(...)
        ↓
_SelectionPathPayloads
        ↓
_selection_path_from_payload_bundle(...)
        ↓
SelectionPathAudit
```

The pressure-selection branch reaches the same compatibility helper through its branch-local bundle producer:

```text
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

The unsupported-target branch reaches the same compatibility helper through the generic payload wrapping handoff:

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

`_selection_path_from_payload_bundle(...)` owns the public audit compatibility construction by reading only the already-composed bundle fields and projecting them into `SelectionPathAudit` fields:

- `payloads.result.selected` becomes `SelectionPathAudit.selected`.
- `payloads.lineage.candidate_set.candidates` becomes `SelectionPathAudit.candidates`.
- `payloads.lineage.factors.selection_factors` becomes `SelectionPathAudit.selection_factors`.
- `payloads.lineage.non_selected.non_selected` becomes `SelectionPathAudit.non_selected`.
- `payloads.support.evidence` becomes `SelectionPathAudit.evidence`.
- `payloads.reason.outcome` becomes `SelectionPathAudit.outcome`.
- `payloads.lineage.unknowns.unknowns` is converted with `typed_unknowns_to_public_dicts(...)` before becoming `SelectionPathAudit.unknowns`.

The helper does not select candidates, create factors, decide non-selected candidates, gather supporting evidence, produce lineage, preserve typed Unknowns, record facts, write the event ledger, or mutate cluster state. Those responsibilities remain owned upstream or by existing read-only public conversion helpers.

Existing tests already prove this boundary by constructing payload artifacts directly, handing them through `_selection_path_from_payloads(...)`, and asserting that public fields preserve the separated payload responsibilities without leaking fields between result, reason, support, lineage, candidate, factor, non-selected, or typed Unknown artifacts.

## Before

After Slice 005, the recovered progression was:

```text
build_selection_path_audit(...)
        ↓
_selection_target_selection(...)
        ↓
_SelectionTargetSelection
        ├── Focus
        │      ↓
        │  _focus_selection_result(...)
        │      ↓
        │  _from_pressure_selection(...)
        │      ↓
        │  _pressure_selection_payloads(...)
        │
        ├── Pressure Category
        │      ↓
        │  _pressure_category_selection_result(...)
        │      ↓
        │  _from_pressure_selection(...)
        │      ↓
        │  _pressure_selection_payloads(...)
        │
        └── Unsupported
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

The shared downstream construction step was present, but the campaign had not yet recovered its ownership boundary. Compatibility construction was still compressed with the broader payload-composition layer.

## After

The shared downstream compatibility step remains implementation-local and unchanged:

```text
_SelectionPathPayloads
        ↓
_selection_path_from_payload_bundle(...)
        ↓
SelectionPathAudit
```

`_selection_path_from_payload_bundle(...)` is now recorded as the producer that owns payload-bundle compatibility construction for all branch producers that have already produced `_SelectionPathPayloads`.

This recovery does not split candidate integration, factor integration, non-selected integration, supporting-evidence integration, lineage integration, or typed Unknown production. Those remain separate candidate responsibilities for future slices if repository evidence selects them.

## Recovered producer

`_selection_path_from_payload_bundle(...)` owns the recovered responsibility.

It receives a complete `_SelectionPathPayloads` artifact and constructs the public `SelectionPathAudit` compatibility shape from the already-owned payload components.

## Recovered artifact/helper

The recovered boundary is carried by the existing `_SelectionPathPayloads` artifact and the existing `_selection_path_from_payload_bundle(...)` helper.

No new artifact or helper was introduced.

## Recovered consumer

The immediate consumers of this recovered boundary are the upstream handoff helpers that call `_selection_path_from_payload_bundle(...)`:

- `_selection_path_from_payloads(...)` for the unsupported-target payload wrapping path.
- `_from_pressure_selection(...)` for implemented pressure-selection payload bundles shared by focus and pressure-category targets.

The final consumer remains the public `SelectionPathAudit` object returned by `build_selection_path_audit(...)` and rendered or serialized by existing CLI behavior.

## Compatibility preserved

No compatibility boundary changed.

Preserved boundaries and behavior:

- selection-target resolution ownership from Slice 001;
- focus selected-result production ownership from Slice 002;
- pressure-category selected-result production ownership from Slice 003;
- pressure-selection payload bundle composition ownership from Slice 004;
- unsupported-target payload bundle composition ownership from Slice 005;
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

- `constitutional_relationship_selection_path_implementation_slice_006.md`

## LOC changed

Documentation diff for this slice:

- `constitutional_relationship_selection_path_implementation_slice_006.md`: 215 insertions.

No implementation or test source lines changed in this slice because the adjacent implementation-local producer already existed in repository authority.

## Tests executed

- `pytest -q tests/test_selection_path_audit.py` — passed.
- `git diff --check` — passed.

The diagnostic inventory and diagnostic shape-audit tests were not required because this slice added no diagnostic surface, audit behavior, CLI flag, recordable output, event-ledger write, fact recording, or cluster mutation.

## Required questions

1. **What responsibilities were previously compressed?** Public `SelectionPathAudit` compatibility construction was previously compressed with the shared payload-composition layer after `_SelectionPathPayloads`; specifically, selected-field projection, candidate projection, factor projection, non-selected projection, evidence projection, outcome projection, and typed Unknown public conversion were treated as one unresolved downstream handoff.
2. **Which implementation-local ownership boundary became directly observable?** Payload-bundle compatibility construction became directly observable immediately downstream of `_SelectionPathPayloads`.
3. **What producer now owns the recovered responsibility?** `_selection_path_from_payload_bundle(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** The existing `_SelectionPathPayloads` artifact carries the already-composed branch payloads, and `_selection_path_from_payload_bundle(...)` carries the compatibility construction helper boundary.
5. **Who consumes it?** `_selection_path_from_payloads(...)` and `_from_pressure_selection(...)` call `_selection_path_from_payload_bundle(...)`; the resulting `SelectionPathAudit` is consumed by the existing JSON and text rendering paths.
6. **Did any compatibility boundary change?** No.

## Remaining compressed responsibilities

The following responsibilities remain intentionally compressed or only partially separated for future repository-evidence-driven recovery slices:

- candidate integration;
- factor integration;
- non-selected integration;
- supporting-evidence integration;
- lineage integration;
- typed Unknown production and integration.

## Recovery type

Orientation recovery only.

Repository implementation already contained the adjacent producer and supporting payload artifact, so this slice records the ownership boundary without manufacturing implementation changes.
