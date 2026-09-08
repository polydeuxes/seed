# Inquiry Lineage Slice 002

## Selected architectural boundary

**Recovered boundary:** Selection Result is not Selection Lineage.

This slice does not rename or stabilize the emerging implementation responsibility family. It recovers one implementation-backed ownership boundary:

```text
Selection Result
    !=
Selection Lineage
```

## Implementation evidence

Implementation evidence was recovered from existing code and tests around `selection_path_audit`, `reference_selection`, `operational_story`, `reasoning_path_audit`, `projection_shape`, and `diagnostic_inventory`.

### Recurring selection-result material

The result-like side appears as the currently selected or produced answer:

- `SelectionPathAudit.selected` and `SelectionPathAudit.outcome` expose the chosen operational selection.
- `ReferenceSelection.selected_reference` exposes the implementation-selected comparison reference.
- `OperationalStory.focus` exposes the selected current operational focus while the story preserves why that focus is interpretable.
- `ReasoningPathAudit.derived_conclusions` and `ProjectionShapeStage.produces` are not selection surfaces, but they provide adjacent evidence that chosen/result material is not sufficient without lineage.
- `DiagnosticInventoryEntry.name` and public flags declare surfaces, while shape-audit rows preserve conformance lineage.

### Recurring selection-lineage material

The lineage side appears as candidate, comparison, authority, unknown, and limitation material:

- `SelectionPathAudit.candidates`, `selection_factors`, `non_selected`, `evidence`, `unknowns`, and `boundary` preserve why the selected value is safe to interpret.
- `ReferenceSelection.selection_rationale`, `alternative_references`, `authority_boundary`, and `limitations` preserve comparison lineage after a reference has been selected.
- `OperationalStory.supporting_evidence`, `investigation_path`, `unknowns`, and `boundary` preserve interpretive lineage around the selected focus.
- `ProjectionShapeStage.consumes`, `influences`, `does_not_influence`, `authority_boundary`, and `confidence` preserve stage lineage around produced state shape.
- `DiagnosticInventoryEntry` plus diagnostic shape audit preserve declared compatibility and mutation lineage around diagnostic surfaces.

## Before

`seed_runtime/selection_path_audit.py` already exposed the right public shape, but selected result and lineage were composed together directly at each `SelectionPathAudit(...)` construction site.

The compressed constructor handoff mixed:

```text
selected / outcome
```

with:

```text
candidates / selection factors / non-selected alternatives / evidence / unknowns
```

That meant the public object preserved the boundary, but the implementation-local ownership boundary was less directly observable.

## After

`seed_runtime/selection_path_audit.py` now has private implementation-local payloads:

```text
_SelectionResultPayload
_SelectionLineagePayload
```

The selected result payload owns only:

```text
selected
outcome
```

The selection lineage payload owns only:

```text
candidates
selection_factors
non_selected
evidence
unknowns
```

`_selection_path_from_payloads(...)` performs the explicit compatibility handoff into the unchanged public `SelectionPathAudit` object.

## Boundary made explicit

The recovered boundary is:

```text
Selection Result
    !=
Selection Lineage
```

This slice makes that boundary directly observable in implementation-local composition without changing CLI behavior, renderer behavior, JSON keys, event behavior, ledger behavior, diagnostic inventory entries, diagnostic shape-audit specs, or public dataclass compatibility.

## Compatibility preserved

No compatibility boundary changed.

The public `SelectionPathAudit` dataclass remains unchanged. `selection_path_audit_json(...)` still delegates to `to_json_dict()`. `format_selection_path_audit(...)` still renders the same public fields. The CLI still dispatches to the same builder and serializer.

The new test proves the compatibility handoff keeps selection result fields separate from lineage fields in the emitted JSON shape without adding new keys.

## Files changed

- `seed_runtime/selection_path_audit.py`
- `tests/test_selection_path_audit.py`
- `inquiry_lineage_slice_002.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/selection_path_audit.py | 108 ++++++++++++++++++++++++-----------
tests/test_selection_path_audit.py   |  23 ++++++++
2 files changed, 99 insertions(+), 32 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_selection_path_audit.py tests/test_reference_selection.py tests/test_operational_story.py tests/test_reasoning_path_audit.py tests/test_projection_shape.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
90 passed in 45.99s
```

## Remaining compressed lineage responsibilities

Implementation evidence still shows other compressed lineage responsibilities that this slice intentionally did not change:

- `reference_selection` still composes selected reference and reference lineage directly into the public compatibility object.
- `reasoning_path_audit` still carries conclusions and derivation lineage in one public object without an implementation-local conclusion/lineage handoff.
- `projection_shape` still carries produced projection shape and stage lineage in one stage object.
- `diagnostic_inventory` and `diagnostic_shape_audit` still share responsibility for declared surface shape and conformance lineage across separate modules.
- `operational_story` already has richer implementation-local payloads, but selection lineage is not normalized across surfaces.

These are observations only. This slice stops after recovering one recurring ownership boundary.

## Observations about family vocabulary

Insufficient implementation evidence.

The repository now provides additional implementation evidence that selected results are repeatedly preserved separately from candidate/comparison/authority lineage, but this slice does not establish the final family name. The evidence supports the narrower boundary, not a vocabulary migration.

## Questions

### 1. Where were selection result and selection lineage previously mixed?

They were previously mixed at the `SelectionPathAudit(...)` constructor handoff in `seed_runtime/selection_path_audit.py`, where `selected` and `outcome` were constructed alongside `candidates`, `selection_factors`, `non_selected`, `evidence`, and `unknowns`.

### 2. Which recovered architectural boundary became more explicit?

`Selection Result != Selection Lineage` became more explicit through private `_SelectionResultPayload` and `_SelectionLineagePayload` objects plus a single compatibility handoff helper.

### 3. How does the implementation now better reflect the recovered inquiry architecture?

The builder now composes the selected result separately from the candidate, factor, alternative, evidence, and unknown lineage before handing both into the unchanged public audit object. The public behavior remains the same, but implementation ownership mirrors the inquiry architecture more directly.

### 4. Based on implementation evidence, has family vocabulary become more stable?

Insufficient implementation evidence.

### 5. Did any compatibility boundary change?

No.
