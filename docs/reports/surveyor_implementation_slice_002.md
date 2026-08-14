# Surveyor Implementation Slice 002

Recovered exactly one implementation-local ownership boundary: **support-string preparation for selected Inquiry Orientation material**.

This slice began only from implementation immediately adjacent to `_select_inquiry_orientation_related_material(...)`, `_prepare_inquiry_orientation_selected_material(...)`, and `_prepare_inquiry_orientation_answer(...)`. The constitutional Surveyor characterization was used only for orientation. The repository implementation selected the recovered boundary: after bounded related material is selected, `_prepare_inquiry_orientation_selected_material(...)` still compressed the separate responsibility of deriving the support-string payload that `_prepare_inquiry_orientation_answer(...)` carries forward.

## Selected boundary

The selected boundary is **support-string preparation from already-selected related material**.

This is intentionally narrow. It does not redesign Surveyor, Inquiry Orientation, recovery, CLI behavior, JSON output, diagnostics, schemas, event-ledger behavior, or public compatibility. It only makes the existing implementation-local handoff observable: selected related material is selected first, then support strings are prepared from that selected material before the selected-material artifact is constructed.

## Implementation evidence

Implementation evidence exposed the boundary directly:

- `_select_inquiry_orientation_related_material(...)` already returns the bounded `list[RelatedMaterial]` selected from collected evidence.
- `_prepare_inquiry_orientation_selected_material(...)` already consumes that bounded selected material to construct `_InquiryOrientationSelectedMaterial`.
- `_InquiryOrientationSelectedMaterial` already carries both `related_material` and `support` for downstream answer composition.
- `_prepare_inquiry_orientation_answer(...)` already forwards `selected_material.support` into `_InquiryOrientationAnswer` without recalculating support strings.
- The compressed line `support=[item.support for item in related]` was neither evidence collection nor answer construction; it was a local preparation step between bounded related-material selection and selected-material artifact construction.

## Before

Before this slice, `_prepare_inquiry_orientation_selected_material(...)` performed two adjacent responsibilities:

1. consumed bounded related material selected by `_select_inquiry_orientation_related_material(...)`; and
2. derived the support-string payload inline while constructing `_InquiryOrientationSelectedMaterial`.

That compressed selected-material assembly and support-string preparation into one local function body.

## After

After this slice:

1. `_select_inquiry_orientation_related_material(...)` still owns bounded related-material selection.
2. `_prepare_inquiry_orientation_support(...)` prepares support strings from that already-selected related material.
3. `_prepare_inquiry_orientation_selected_material(...)` assembles `_InquiryOrientationSelectedMaterial` from the selected related material and prepared support strings.
4. `_prepare_inquiry_orientation_answer(...)` continues to consume `_InquiryOrientationSelectedMaterial` unchanged.

Runtime output remains unchanged because the support list still uses the same order and values: `[item.support for item in selected_related_material]`.

## Recovered producer

The recovered producer is `_prepare_inquiry_orientation_support(...)`.

It owns preparation of the support-string payload from the already-selected `list[RelatedMaterial]`.

## Recovered artifact/helper

The recovered helper is `_prepare_inquiry_orientation_support(...)`.

No new public artifact or dataclass was introduced. The existing `_InquiryOrientationSelectedMaterial.support` field remains the compatibility-preserving carrier consumed by answer preparation.

## Recovered consumer

The immediate consumer is `_prepare_inquiry_orientation_selected_material(...)`, which uses the prepared support strings while constructing `_InquiryOrientationSelectedMaterial`.

Downstream consumers remain unchanged:

- `_prepare_inquiry_orientation_answer(...)` consumes `_InquiryOrientationSelectedMaterial.support`;
- `_compose_inquiry_orientation_answer(...)` returns the same answer artifact shape;
- `build_inquiry_orientation(...)` returns the same `InquiryOrientationView` shape;
- `format_inquiry_orientation(...)` renders the same support output.

## Required questions

### 1. What responsibilities were previously compressed?

Selected-material assembly and support-string preparation were previously compressed inside `_prepare_inquiry_orientation_selected_material(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

Support-string preparation from already-selected related material became directly observable.

### 3. What producer now owns the recovered responsibility?

`_prepare_inquiry_orientation_support(...)` now owns support-string preparation.

### 4. What artifact or helper carries the recovered boundary, if any?

The helper `_prepare_inquiry_orientation_support(...)` carries the recovered boundary. The existing `_InquiryOrientationSelectedMaterial.support` field carries the prepared payload downstream.

### 5. Who consumes it?

`_prepare_inquiry_orientation_selected_material(...)` consumes the helper output immediately. `_prepare_inquiry_orientation_answer(...)` then consumes the unchanged `_InquiryOrientationSelectedMaterial.support` payload.

### 6. Did any compatibility boundary change?

```text
No.
```

## Compatibility preserved

Public compatibility is preserved:

- no CLI flag changed;
- no JSON shape changed;
- no diagnostic surface changed;
- no schema changed;
- no event-ledger behavior changed;
- no record behavior changed;
- no public dataclass field changed;
- no renderer section changed;
- no related-material ordering changed;
- no support-string values changed.

## Files changed

- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `surveyor_implementation_slice_002.md`

## LOC changed

Diffstat at implementation time:

```text
seed_runtime/inquiry_orientation.py  |  10 ++-
surveyor_implementation_slice_002.md | 154 +++++++++++++++++++++++++++++++++++
tests/test_inquiry_orientation.py    |  28 +++++++
3 files changed, 191 insertions(+), 1 deletion(-)
```

## Tests executed

```text
python -m pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
17 passed
```

## Remaining compressed responsibilities

The following responsibilities remain intentionally outside this slice because exactly one implementation-local ownership boundary was recovered:

- fact-support match construction inside `_fact_matches(...)`;
- source-navigation match construction inside `_source_navigation_matches(...)`;
- token normalization inside `_note_tokens(...)`;
- related-material dedupe ordering inside `_dedupe_related(...)`;
- selected-material artifact assembly inside `_prepare_inquiry_orientation_selected_material(...)`;
- answer reason selection;
- authority-boundary selection;
- limitation/uncertainty selection;
- answer artifact construction;
- view construction;
- text rendering.

No additional Surveyor capability, investigator, planner, workflow, registry, methodology redesign, orientation redesign, or recovery redesign was introduced.
