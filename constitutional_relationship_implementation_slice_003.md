# Constitutional Relationship Implementation Slice 003

Repository authority wins.

## Selected boundary

Selected implementation-local ownership boundary:

```text
selected inquiry-orientation material reason selection
```

Implementation evidence selected this boundary adjacent to Slice 002. The slice did not use constitutional prose to force authority-boundary attachment, answer construction, collected-evidence orchestration, a universal artifact, engine, registry, profile framework, workflow, planner, scheduler, or redesign.

The recovered handoff is now:

```text
_collect_inquiry_orientation_evidence(...)
→ _prepare_inquiry_orientation_selected_material(...)
→ _InquiryOrientationSelectedMaterial
→ _select_inquiry_orientation_reason(...)
→ _select_inquiry_orientation_limitations(...)
→ _compose_inquiry_orientation_answer(...)
→ _InquiryOrientationAnswer
→ build_inquiry_orientation(...)
```

## Implementation evidence

Slice 001 made `_InquiryOrientationSelectedMaterial` directly observable as the selected-material handoff carrying related material and preserved supports. Slice 002 made selected-material limitation selection directly observable before answer construction.

Immediately adjacent implementation evidence showed that `_compose_inquiry_orientation_answer(...)` still assigned the answer reason while constructing `_InquiryOrientationAnswer`:

```text
"deterministic lexical overlaps against projected fact supports and source-navigation matches"
```

That reason text is implementation-local, deterministic, and tied to the selected inquiry-orientation material's evidence sources. It does not need note storage, rendering state, authority-boundary text, uncertainty selection, CLI transport, event-ledger writes, cluster mutation, fact recording, or public answer rendering.

The new `_select_inquiry_orientation_reason(...)` helper makes that local boundary directly observable while preserving the unchanged `_InquiryOrientationAnswer.reason` compatibility field and unchanged public JSON/text behavior.

## Before

Before this slice, `_compose_inquiry_orientation_answer(...)` still owned all of these responsibilities at once after Slice 002:

1. collected-evidence consumption/orchestration;
2. reason assignment;
3. authority-boundary attachment;
4. `_InquiryOrientationAnswer` construction.

## After

After this slice, exactly one additional responsibility was recovered:

```text
selected-material reason selection
```

`_compose_inquiry_orientation_answer(...)` still owns answer composition: collected-evidence consumption/orchestration, authority-boundary attachment, and `_InquiryOrientationAnswer` construction. Slice 001 support preservation and Slice 002 limitation selection remain unchanged.

## Recovered producer

Recovered producer:

```text
_select_inquiry_orientation_reason(selected_material)
```

It consumes `_InquiryOrientationSelectedMaterial` and returns the exact reason text describing the deterministic lexical-overlap basis for the selected material.

## Recovered artifact/helper

Recovered artifact/helper:

```text
_select_inquiry_orientation_reason(...)
```

No new artifact was required. The existing `_InquiryOrientationSelectedMaterial` helper artifact carries the selected related material that this recovered helper is scoped to.

The helper does not carry or own note text, support preservation, limitation selection, authority-boundary attachment, rendering fields, event-ledger writes, cluster mutation, fact recording, or `_InquiryOrientationAnswer` construction.

## Recovered consumer

Recovered consumer:

```text
_compose_inquiry_orientation_answer(state, request)
```

It consumes the helper result by copying the returned string into the unchanged `_InquiryOrientationAnswer.reason` compatibility field.

`build_inquiry_orientation(state, note)` remains the direct consumer of `_InquiryOrientationAnswer`.

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
- reason text unchanged;
- uncertainty text unchanged;
- authority-boundary text unchanged;
- read-only behavior unchanged;
- no runtime-state projection added;
- no fact recording added;
- no event-ledger writes added;
- no cluster mutation added;
- `_InquiryOrientationSelectedMaterial` shape unchanged;
- `_InquiryOrientationAnswer` shape and consumer compatibility unchanged;
- Selection Path implementation not modified.

## Files changed

- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `constitutional_relationship_implementation_slice_003.md`

## LOC changed

Implementation/test diff before this document:

```text
41 insertions, 4 deletions: seed_runtime/inquiry_orientation.py and tests/test_inquiry_orientation.py
```

This document was added as the requested implementation-slice record.

## Tests executed

```text
pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
13 passed
```

## Remaining compressed responsibilities

The following responsibilities intentionally remain compressed inside `_compose_inquiry_orientation_answer(...)`:

1. collected-evidence consumption/orchestration;
2. authority-boundary attachment;
3. `_InquiryOrientationAnswer` construction.

## Required questions

### 1. What responsibilities were previously compressed?

Collected-evidence consumption/orchestration, reason assignment, authority-boundary attachment, and `_InquiryOrientationAnswer` construction were previously compressed in `_compose_inquiry_orientation_answer(...)` after Slice 002.

### 2. Which implementation-local ownership boundary became directly observable?

Selected inquiry-orientation material reason selection became directly observable.

### 3. What producer now owns the recovered responsibility?

`_select_inquiry_orientation_reason(selected_material)` now owns the recovered responsibility.

### 4. What artifact or helper carries the boundary, if any?

`_select_inquiry_orientation_reason(...)` carries the recovered boundary as a helper. No new dataclass artifact was introduced.

### 5. Who consumes it?

`_compose_inquiry_orientation_answer(state, request)` consumes it.

### 6. Did any compatibility boundary change?

```text
No.
```
