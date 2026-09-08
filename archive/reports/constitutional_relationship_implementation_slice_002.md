# Constitutional Relationship Implementation Slice 002

Repository authority wins.

## Selected boundary

Selected implementation-local ownership boundary:

```text
selected inquiry-orientation material limitation selection
```

Implementation evidence selected this boundary adjacent to Slice 001. The slice did not use constitutional prose to force reason assignment, authority-boundary attachment, answer construction, a universal artifact, engine, registry, profile framework, workflow, planner, scheduler, or redesign.

The recovered handoff is now:

```text
_collect_inquiry_orientation_evidence(...)
→ _prepare_inquiry_orientation_selected_material(...)
→ _InquiryOrientationSelectedMaterial
→ _select_inquiry_orientation_limitations(...)
→ _compose_inquiry_orientation_answer(...)
→ _InquiryOrientationAnswer
→ build_inquiry_orientation(...)
```

## Implementation evidence

Slice 001 made `_InquiryOrientationSelectedMaterial` directly observable as the selected-material handoff carrying related material and preserved supports. Immediately adjacent implementation evidence showed that `_compose_inquiry_orientation_answer(...)` still selected limitations by inspecting the same selected material:

```text
UNCERTAINTY_WITH_MATCHES if selected_material.related_material else UNCERTAINTY_WITHOUT_MATCHES
```

That branch is implementation-local, deterministic, and selected only by whether the selected material contains related material. It does not need note text, rendering state, reason text, authority-boundary text, CLI transport, storage, event-ledger writes, cluster mutation, fact recording, or answer rendering.

The new `_select_inquiry_orientation_limitations(...)` helper makes that local boundary directly observable while preserving the unchanged `_InquiryOrientationAnswer.limitations` compatibility field and the unchanged `InquiryOrientationView.uncertainty` public rendering behavior.

## Before

Before this slice, `_compose_inquiry_orientation_answer(...)` still owned all of these responsibilities at once after Slice 001:

1. collected-evidence consumption/orchestration;
2. reason assignment;
3. authority-boundary attachment;
4. limitation selection from selected material;
5. `_InquiryOrientationAnswer` construction.

## After

After this slice, exactly one additional responsibility was recovered:

```text
selected-material limitation selection
```

`_compose_inquiry_orientation_answer(...)` still owns answer composition: collected-evidence consumption/orchestration, reason assignment, authority-boundary attachment, and `_InquiryOrientationAnswer` construction. Slice 001 remains unchanged.

## Recovered producer

Recovered producer:

```text
_select_inquiry_orientation_limitations(selected_material)
```

It consumes `_InquiryOrientationSelectedMaterial` and returns the exact uncertainty/limitations text selected by whether related material was selected.

## Recovered artifact/helper

Recovered artifact/helper:

```text
_select_inquiry_orientation_limitations(...)
```

No new artifact was required. The existing `_InquiryOrientationSelectedMaterial` helper artifact carries the selected related material that this recovered helper reads.

The helper does not carry or own note text, support preservation, reason assignment, authority-boundary attachment, rendering fields, event-ledger writes, cluster mutation, fact recording, or `_InquiryOrientationAnswer` construction.

## Recovered consumer

Recovered consumer:

```text
_compose_inquiry_orientation_answer(state, request)
```

It consumes the helper result by copying the returned string into the unchanged `_InquiryOrientationAnswer.limitations` compatibility field.

`build_inquiry_orientation(state, note)` remains the direct consumer of `_InquiryOrientationAnswer` and still maps `answer.limitations` to `InquiryOrientationView.uncertainty`.

## Compatibility preserved

Did any compatibility boundary change?

```text
No.
```

Preserved compatibility boundaries:

- public CLI behavior unchanged;
- JSON and text output unchanged;
- inquiry-note storage unchanged;
- deterministic lexical-overlap behavior unchanged;
- support text unchanged;
- reason behavior unchanged;
- uncertainty text unchanged;
- authority-boundary text unchanged;
- read-only behavior unchanged;
- no runtime-state projection added;
- no fact recording added;
- no event-ledger writes added;
- no cluster mutation added;
- `_InquiryOrientationSelectedMaterial` responsibility unchanged;
- `_InquiryOrientationAnswer` fields and consumer compatibility unchanged;
- Selection Path implementation not modified.

## Files changed

- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `constitutional_relationship_implementation_slice_002.md`

## LOC changed

Implementation/test diff before this document:

```text
58 insertions, 5 deletions: seed_runtime/inquiry_orientation.py and tests/test_inquiry_orientation.py
```

This document was added as the requested implementation-slice record.

## Tests executed

```text
pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
12 passed
```

## Remaining compressed responsibilities

The following responsibilities intentionally remain compressed inside `_compose_inquiry_orientation_answer(...)`:

1. collected-evidence consumption/orchestration;
2. reason assignment;
3. authority-boundary attachment;
4. `_InquiryOrientationAnswer` construction.

## Required questions

### 1. What responsibilities were previously compressed?

Collected-evidence consumption/orchestration, reason assignment, authority-boundary attachment, limitation selection, and `_InquiryOrientationAnswer` construction were previously compressed in `_compose_inquiry_orientation_answer(...)` after Slice 001.

### 2. Which implementation-local ownership boundary became directly observable?

Selected inquiry-orientation material limitation selection became directly observable.

### 3. What producer now owns the recovered responsibility?

`_select_inquiry_orientation_limitations(selected_material)` now owns the recovered responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_select_inquiry_orientation_limitations(...)` carries the recovered boundary as a helper. No new dataclass artifact was introduced.

### 5. Who consumes it?

`_compose_inquiry_orientation_answer(state, request)` consumes it.

### 6. Did any compatibility boundary change?

```text
No.
```
