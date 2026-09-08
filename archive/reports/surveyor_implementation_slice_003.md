# Surveyor Implementation Slice 003

Recovered exactly one implementation-local ownership boundary: **answer payload preparation from selected Inquiry Orientation material**.

This slice began only from implementation immediately adjacent to `_prepare_inquiry_orientation_support(...)`, `_prepare_inquiry_orientation_selected_material(...)`, and `_prepare_inquiry_orientation_answer(...)`. The constitutional Surveyor characterization was used only for orientation. Repository implementation selected the recovered boundary: after selected material is assembled, `_prepare_inquiry_orientation_answer(...)` still compressed preparation of answer fields with assembly of the `_InquiryOrientationAnswer` artifact.

## Selected boundary

The selected boundary is **answer payload preparation from assembled selected material**.

This is intentionally narrow. It does not redesign Surveyor, Inquiry Orientation, Recovery, CLI behavior, JSON output, diagnostics, schemas, event-ledger behavior, or public compatibility. It only makes the existing implementation-local handoff observable: selected material is assembled first, answer fields are prepared from that selected material, and the answer artifact is then assembled from the prepared payload.

## Implementation evidence

Implementation evidence exposed the boundary directly:

- `_prepare_inquiry_orientation_selected_material(...)` already returns `_InquiryOrientationSelectedMaterial` containing the selected `RelatedMaterial` list and prepared support strings.
- `_prepare_inquiry_orientation_answer(...)` already consumed `_InquiryOrientationSelectedMaterial` and populated all `_InquiryOrientationAnswer` fields.
- `_select_inquiry_orientation_reason(...)`, `_select_inquiry_orientation_authority_boundary(...)`, and `_select_inquiry_orientation_limitations(...)` already prepared answer-field values from selected material before rendering.
- `_InquiryOrientationAnswer` already carried only answer-facing fields consumed by `build_inquiry_orientation(...)`; it did not carry note, evidence, selected-material, renderer, CLI, diagnostic, schema, or event-ledger state.
- The compressed construction of `answer`, `reason`, `support`, `boundary`, and `limitations` inside `_prepare_inquiry_orientation_answer(...)` was not selected-material assembly and was not view rendering. It was the answer payload immediately adjacent to selected material and answer artifact assembly.

## Before

Before this slice, `_prepare_inquiry_orientation_answer(...)` performed two adjacent responsibilities:

1. prepared the answer payload fields from `_InquiryOrientationSelectedMaterial`; and
2. assembled the `_InquiryOrientationAnswer` artifact.

That compressed answer payload preparation and answer artifact assembly into one local function body.

## After

After this slice:

1. `_prepare_inquiry_orientation_selected_material(...)` still owns selected-material artifact assembly.
2. `_prepare_inquiry_orientation_answer_payload(...)` prepares answer fields from that selected material.
3. `_prepare_inquiry_orientation_answer(...)` assembles `_InquiryOrientationAnswer` from the prepared payload.
4. `_compose_inquiry_orientation_answer(...)`, `build_inquiry_orientation(...)`, and rendering continue to consume the same answer/view shapes unchanged.

Runtime output remains unchanged because the payload uses the same selected material, support list, reason selector, authority-boundary selector, and limitation selector that `_prepare_inquiry_orientation_answer(...)` used before this slice.

## Recovered producer

The recovered producer is `_prepare_inquiry_orientation_answer_payload(...)`.

It owns preparation of the answer field payload from the already-assembled `_InquiryOrientationSelectedMaterial`.

## Recovered artifact/helper

The recovered helper is `_prepare_inquiry_orientation_answer_payload(...)`.

The recovered implementation-local carrier is `_InquiryOrientationAnswerPayload`. No public artifact was introduced. `_InquiryOrientationAnswer` remains the compatibility-preserving answer artifact consumed downstream.

## Recovered consumer

The immediate consumer is `_prepare_inquiry_orientation_answer(...)`, which uses the prepared payload while constructing `_InquiryOrientationAnswer`.

Downstream consumers remain unchanged:

- `_compose_inquiry_orientation_answer(...)` returns the same `_InquiryOrientationAnswer` shape;
- `build_inquiry_orientation(...)` maps the same answer fields into `InquiryOrientationView`;
- `format_inquiry_orientation(...)` renders the same public text output.

## Required questions

### 1. What responsibilities were previously compressed?

Answer payload preparation and answer artifact assembly were previously compressed inside `_prepare_inquiry_orientation_answer(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

Answer payload preparation from already-assembled selected material became directly observable.

### 3. What producer now owns the recovered responsibility?

`_prepare_inquiry_orientation_answer_payload(...)` now owns answer payload preparation.

### 4. What artifact or helper carries the recovered boundary, if any?

The helper `_prepare_inquiry_orientation_answer_payload(...)` carries the recovered boundary. The implementation-local `_InquiryOrientationAnswerPayload` artifact carries the prepared fields to `_prepare_inquiry_orientation_answer(...)`.

### 5. Who consumes it?

`_prepare_inquiry_orientation_answer(...)` consumes the prepared payload immediately and assembles the unchanged `_InquiryOrientationAnswer` artifact.

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
- no support-string values changed;
- no reason, authority-boundary, or limitation text changed.

## Files changed

- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `surveyor_implementation_slice_003.md`

## LOC changed

Diffstat at implementation time:

```text
seed_runtime/inquiry_orientation.py    | 26 ++++++++++++++++++++++++++
surveyor_implementation_slice_003.md   | 153 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
tests/test_inquiry_orientation.py      | 42 ++++++++++++++++++++++++++++++++++++++++++
3 files changed, 221 insertions(+)
```

## Tests executed

```text
python -m pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
18 passed
```

## Remaining compressed responsibilities

The following responsibilities remain intentionally outside this slice because exactly one implementation-local ownership boundary was recovered:

- fact-support match construction inside `_fact_matches(...)`;
- source-navigation match construction inside `_source_navigation_matches(...)`;
- token normalization inside `_note_tokens(...)`;
- related-material dedupe ordering inside `_dedupe_related(...)`;
- answer reason selection;
- authority-boundary selection;
- limitation/uncertainty selection;
- answer artifact construction;
- view construction;
- text rendering.

No additional Surveyor capability, investigator, planner, workflow, registry, methodology redesign, orientation redesign, or recovery redesign was introduced.
