# Inquiry Lineage Slice 004

## Selected architectural boundary

`Reference Choice != Comparison Lineage`

The implementation selected this boundary from `reference_selection`: the surface already distinguishes the chosen comparison reference from rationale, alternatives, and limitations, and it is a different inquiry domain from reasoning-path and selection-path audits.

## Implementation evidence

Reviewed implementation surfaces:

- `seed_runtime/reference_selection.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reasoning_path_audit.py`

Repository evidence supported `Reference Choice != Comparison Lineage` most directly:

- `ReferenceSelection.selected_reference` is the recovered reference choice.
- `ReferenceSelection.selection_rationale`, `alternative_references`, and `limitations` are comparison-lineage material explaining why the reference is usable, which alternatives remain only candidates, and which comparison authority is absent.
- `_build_history_reference_selection(...)` already computed a selected historical comparison reference separately from alternatives and limitations, but previously handed both groups into `ReferenceSelection(...)` at the same constructor boundary.
- Unsupported domains also exposed a choice-like unknown result separately from unsupported-domain comparison lineage, but directly mixed them in the public object constructor.
- `projection_shape` also has result/lineage pressure through stage products and influence fields, but `reference_selection` showed the stronger and smaller implementation-local slice because the public fields already map directly to choice and comparison lineage.

## Before

`build_reference_selection(...)` and `_build_history_reference_selection(...)` constructed `ReferenceSelection(...)` directly with both ownership groups:

- reference-choice material:
  - `selected_reference`
- comparison-lineage material:
  - `selection_rationale`
  - `alternative_references`
  - `limitations`

The public JSON and renderer already presented these as separate fields, but the implementation-local ownership handoff compressed the chosen reference and the comparison lineage into the same constructor calls.

## After

`seed_runtime/reference_selection.py` now has two private implementation-local payloads:

- `_ReferenceChoicePayload`
  - `selected_reference`
- `_ComparisonLineagePayload`
  - `selection_rationale`
  - `alternative_references`
  - `limitations`

`_reference_selection_from_payloads(...)` performs the explicit compatibility handoff into the unchanged public `ReferenceSelection` object for both supported history selection and unsupported-domain fallback selection.

## Boundary made explicit

The recovered boundary is now directly observable in implementation:

```text
Reference Choice
    !=
Comparison Lineage
```

Reference choice owns the implementation-selected comparison reference. Comparison lineage owns the rationale, candidate alternatives, and limitations that explain or bound the comparison.

## Compatibility preserved

Compatibility boundary changed: No.

The public `ReferenceSelection` dataclass remains unchanged. `reference_selection_json(...)` still returns the same keys. `format_reference_selection(...)` still renders the same sections. No renderer, CLI, schema, JSON, event, ledger, vocabulary migration, or cross-surface normalization changes were made.

## Files changed

- `seed_runtime/reference_selection.py`
- `tests/test_reference_selection.py`
- `inquiry_lineage_slice_004.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/reference_selection.py | 66 +++++++++++++++++++++++++++----------
tests/test_reference_selection.py   | 24 ++++++++++++++
2 files changed, 73 insertions(+), 17 deletions(-)
```

## Tests executed

```text
python -m pytest -q tests/test_reference_selection.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
49 passed
```

## Remaining compressed lineage responsibilities

- `ReferenceSelection` remains the public compatibility object combining choice, comparison lineage, authority boundary, and mutation flags for existing consumers.
- `projection_shape` still carries projection result material (`produces`) and influence lineage material (`consumes`, `influences`, `does_not_influence`, `authority_boundary`, `confidence`) together in `ProjectionShapeStage` without a private projection-result/influence-lineage handoff.
- Cross-surface family vocabulary remains intentionally unstabilized.

## Observations about family vocabulary

The recovered slices now provide four implementation-backed comparisons:

```text
Outcome != Lineage Frame
```

The first recovered boundary showed that an outcome should not be owned by the same implementation responsibility as the lineage frame explaining how that outcome came to exist.

```text
Selection Result != Selection Lineage
```

The second recovered boundary specialized the pattern in selection-path audit implementation: selected result and outcome are distinct from candidate, factor, non-selected, evidence, and unknown lineage.

```text
Derived Conclusion != Derivation Lineage
```

The third recovered boundary specialized the pattern in reasoning-path audit implementation: derived conclusions are distinct from evidence path, consumers, story impact, and incomplete-lineage unknowns.

```text
Reference Choice != Comparison Lineage
```

This slice extends the pattern into comparison-reference visibility: the selected comparison reference is distinct from the rationale, alternative references, and limitations that explain or bound the comparison.

Family vocabulary conclusion:

```text
Insufficient implementation evidence.
```

Implementation evidence now demonstrates recurrence beyond reasoning and selection into comparison-reference visibility, but this slice intentionally recovered exactly one additional specialization and did not stabilize cross-surface family vocabulary. One additional independent specialization, such as `Projection Result != Influence Lineage`, remains compressed and would provide stronger evidence before naming the responsibility family.

## Answers to required questions

### 1. Where were the recovered result and its lineage previously mixed?

They were mixed at `ReferenceSelection(...)` constructor handoffs in `build_reference_selection(...)` and `_build_history_reference_selection(...)`: `selected_reference` was passed beside `selection_rationale`, `alternative_references`, and `limitations` into the same public compatibility object construction.

### 2. Which recovered architectural boundary became more explicit?

`Reference Choice != Comparison Lineage` became explicit through `_ReferenceChoicePayload`, `_ComparisonLineagePayload`, and `_reference_selection_from_payloads(...)`.

### 3. How does the implementation now better reflect the recovered inquiry architecture?

The implementation now gives the chosen comparison reference a private payload separate from the rationale, alternatives, and limitations that explain how the comparison reference is bounded. The unchanged public object is now assembled by an explicit compatibility handoff rather than by mixing both ownership groups at each builder return.

### 4. Does this slice demonstrate that the recurring ownership pattern extends beyond reasoning and selection?

Yes. `reference_selection` is comparison-reference visibility, not a reasoning-path or selection-path audit. Its implementation now shows a chosen comparison reference separated from comparison lineage in the same ownership pattern recovered by the prior slices.

### 5. Based on implementation evidence alone, is there now sufficient evidence to stabilize the family vocabulary?

```text
Insufficient implementation evidence.
```

### 6. Did any compatibility boundary change?

No.
