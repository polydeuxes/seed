# Inquiry Lineage Slice 003

## Selected architectural boundary

`Derived Conclusion != Derivation Lineage`

The selected slice is the reasoning-path audit handoff where conclusion records were already public fields, but their implementation-local ownership was still constructed beside derivation evidence, consumers, story impact, and unknowns in one builder path.

## Implementation evidence

Reviewed implementation surfaces:

- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/projection_shape.py`

Implementation evidence confirmed recurring compression:

- `ReasoningPathAudit` exposes `intermediate_conclusions` and `derived_conclusions` as separate public fields from `evidence`, `consumers`, and `story_impact`.
- `build_reasoning_path_audit(...)` previously accumulated those lists together and handed them directly into the public compatibility object.
- `SelectionPathAudit` already had the recovered pattern from the prior slice: `_SelectionResultPayload` is distinct from `_SelectionLineagePayload`, with `_selection_path_from_payloads(...)` preserving compatibility.
- `OperationalStory` and `InquiryOrientationView` already use implementation-local composition payloads before compatibility handoff.

## Before

`build_reasoning_path_audit(...)` mixed derived conclusion ownership with derivation lineage ownership by accumulating and directly passing these values together:

- derived conclusion material:
  - `intermediate`
  - `derived`
- derivation lineage material:
  - `evidence`
  - `consumers`
  - `story_impact`
  - `unknowns`

The public JSON and renderer were already behaviorally separated, but the implementation handoff did not make the ownership boundary directly observable.

## After

`seed_runtime/reasoning_path_audit.py` now has two private implementation-local payloads:

- `_DerivedConclusionPayload`
  - `intermediate_conclusions`
  - `derived_conclusions`
- `_DerivationLineagePayload`
  - `evidence`
  - `consumers`
  - `story_impact`
  - `unknowns`

`_reasoning_path_from_payloads(...)` performs the explicit compatibility handoff into the unchanged public `ReasoningPathAudit` object.

## Boundary made explicit

The recovered boundary is now directly observable in implementation:

```text
Derived Conclusion
    !=
Derivation Lineage
```

Derived conclusions own the conclusions produced by reasoning-path derivation. Derivation lineage owns the implementation-backed evidence path, consumers, story impact, and incomplete-lineage unknowns that justify or bound those conclusions.

## Compatibility preserved

Compatibility boundary changed: No.

The public `ReasoningPathAudit` dataclass remains unchanged. `reasoning_path_audit_json(...)` still returns the same keys. `format_reasoning_path_audit(...)` still renders the same sections. No renderer, CLI, schema, JSON, event, ledger, vocabulary migration, or cross-surface normalization changes were made.

## Files changed

- `seed_runtime/reasoning_path_audit.py`
- `tests/test_reasoning_path_audit.py`

## LOC changed

```text
seed_runtime/reasoning_path_audit.py | 55 ++++++++++++++++++++++++++++++++----
tests/test_reasoning_path_audit.py   | 38 +++++++++++++++++++++++++
2 files changed, 87 insertions(+), 6 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_reasoning_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
50 passed in 18.04s
```

## Remaining compressed lineage responsibilities

- `ReasoningPathAudit` still remains a public compatibility object combining conclusion fields, lineage fields, boundary, and unknowns for existing consumers.
- `reference_selection` still has selected reference, alternatives, rationale, limitations, and boundary on one public surface without an implementation-local result/lineage compatibility handoff.
- `projection_shape` still exposes projection stages and authority boundaries without recovering a separate derived-conclusion/derivation-lineage payload boundary.
- Cross-surface lineage vocabulary remains intentionally unstabilized.

## Observations about family vocabulary

The recovered slices now provide three implementation-backed comparisons:

```text
Outcome != Lineage Frame
```

The first recovered boundary showed that a resulting outcome should not be owned by the same implementation responsibility as the frame that explains where that outcome came from.

```text
Selection Result != Selection Lineage
```

The second recovered boundary specialized that pressure into selection: the selected result and selected outcome are distinct from candidates, factors, non-selected candidates, evidence, and selection unknowns.

```text
Derived Conclusion != Derivation Lineage
```

This slice adds another specialization: conclusions derived by a reasoning-path audit are distinct from the evidence path, consumers, story impact, and unknowns that justify or bound those conclusions.

These three slices look like recurring specializations of one implementation responsibility, but the family name is not yet earned. Current implementation evidence supports recurrence across outcome, selection, and derived-conclusion surfaces. It does not yet prove a stable family vocabulary across the remaining compressed surfaces or establish repository-wide naming authority.

Family vocabulary conclusion:

```text
Insufficient implementation evidence.
```

## Answers to required questions

### 1. Where were derived conclusion and derivation lineage previously mixed?

They were mixed in `build_reasoning_path_audit(...)`, where `intermediate`, `derived`, `evidence`, `consumers`, `story_impact`, and `unknowns` were accumulated in one construction path and handed directly into `ReasoningPathAudit`.

### 2. Which recovered architectural boundary became more explicit?

`Derived Conclusion != Derivation Lineage` became explicit through private implementation-local payloads and a compatibility handoff helper.

### 3. How does the implementation now better reflect the recovered inquiry architecture?

The implementation now lets reasoning-path conclusion ownership and derivation-lineage ownership be inspected independently before compatibility handoff. The public audit still carries the same historical fields, but implementation ownership now matches the inquiry architecture more closely.

### 4. Based on implementation evidence, is there now sufficient evidence to stabilize the family vocabulary?

Insufficient implementation evidence.

### 5. Did any compatibility boundary change?

No.
