# Constitutional Relationship Implementation Slice 005

Repository authority wins.

## Selected boundary

Selected implementation-local ownership boundary:

```text
selected inquiry-orientation answer construction
```

Implementation evidence selected this boundary immediately adjacent to Slice 004. The slice did not use constitutional prose to force collected-evidence orchestration recovery, rendering, a universal answer builder, framework, engine, registry, workflow, planner, scheduler, Selection Path modification, or redesign.

The recovered handoff is now:

```text
_collect_inquiry_orientation_evidence(...)
→ _prepare_inquiry_orientation_selected_material(...)
→ _InquiryOrientationSelectedMaterial
→ _select_inquiry_orientation_reason(...)
→ _select_inquiry_orientation_authority_boundary(...)
→ _select_inquiry_orientation_limitations(...)
→ _prepare_inquiry_orientation_answer(...)
→ _InquiryOrientationAnswer
→ build_inquiry_orientation(...)
```

## Implementation evidence

Slices 001 through 004 made these local boundaries directly observable before `_InquiryOrientationAnswer` construction:

1. selected-material support preservation;
2. selected-material reason selection;
3. selected-material authority-boundary selection;
4. selected-material limitation selection.

Immediately adjacent implementation evidence showed that `_compose_inquiry_orientation_answer(...)` still performed two responsibilities after Slice 004:

1. collected-evidence consumption/orchestration;
2. `_InquiryOrientationAnswer` construction.

The directly observable next implementation-local boundary was answer construction, because the answer artifact was assembled entirely from already selected material and already recovered selected-material helpers:

```text
answer=selected_material.related_material
reason=_select_inquiry_orientation_reason(selected_material)
support=selected_material.support
boundary=_select_inquiry_orientation_authority_boundary(selected_material)
limitations=_select_inquiry_orientation_limitations(selected_material)
```

This construction does not require note storage, rendering state, CLI transport, event-ledger writes, cluster mutation, fact recording, runtime-state projection, or public behavior changes. It also does not require recovering collected-evidence orchestration.

The new `_prepare_inquiry_orientation_answer(...)` helper makes the local `_InquiryOrientationAnswer` construction boundary directly observable while preserving the unchanged `_InquiryOrientationAnswer` compatibility artifact and unchanged public JSON/text behavior.

## Before

Before this slice, `_compose_inquiry_orientation_answer(...)` still owned all of these responsibilities at once after Slice 004:

1. collected-evidence consumption/orchestration;
2. `_InquiryOrientationAnswer` construction.

## After

After this slice, exactly one additional responsibility was recovered:

```text
selected-material answer construction
```

`_compose_inquiry_orientation_answer(...)` still owns collected-evidence consumption/orchestration. Slice 001 support preservation, Slice 002 limitation selection, Slice 003 reason selection, and Slice 004 authority-boundary selection remain unchanged.

## Recovered producer

Recovered producer:

```text
_prepare_inquiry_orientation_answer(selected_material)
```

It consumes `_InquiryOrientationSelectedMaterial`, calls the already recovered selected-material reason, authority-boundary, and limitation selectors, preserves the selected support strings, and returns the unchanged `_InquiryOrientationAnswer` artifact.

## Recovered artifact/helper

Recovered artifact/helper:

```text
_prepare_inquiry_orientation_answer(...)
```

No new dataclass artifact was required. The existing `_InquiryOrientationAnswer` compatibility artifact remains unchanged and continues to carry:

```text
answer: list[RelatedMaterial]
reason: str
support: list[str]
boundary: str
limitations: str
```

The helper is implementation-local and inquiry-orientation-specific. It is not a universal answer builder and does not carry or own note text, rendering fields, event-ledger writes, cluster mutation, fact recording, runtime-state projection, or collected-evidence orchestration.

## Recovered consumer

Recovered consumer:

```text
_compose_inquiry_orientation_answer(state, request)
```

It consumes the helper result by returning the unchanged `_InquiryOrientationAnswer` compatibility artifact.

`build_inquiry_orientation(state, note)` remains the direct public-view adapter consumer of `_InquiryOrientationAnswer` and still maps `answer.answer`, `answer.limitations`, and `answer.boundary` into `InquiryOrientationView` fields.

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
- `constitutional_relationship_implementation_slice_005.md`

## LOC changed

Implementation/test diff before this document:

```text
45 insertions, 0 deletions: seed_runtime/inquiry_orientation.py and tests/test_inquiry_orientation.py
```

This document was added as the requested implementation-slice record.

## Tests executed

```text
pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
15 passed
```

## Remaining compressed responsibilities

The following responsibility intentionally remains compressed inside `_compose_inquiry_orientation_answer(...)`:

1. collected-evidence consumption/orchestration.

## Required questions

### 1. What responsibilities were previously compressed?

Collected-evidence consumption/orchestration and `_InquiryOrientationAnswer` construction were previously compressed in `_compose_inquiry_orientation_answer(...)` after Slice 004.

### 2. Which implementation-local ownership boundary became directly observable?

Selected inquiry-orientation answer construction became directly observable.

### 3. What producer now owns the recovered responsibility?

`_prepare_inquiry_orientation_answer(selected_material)` now owns the recovered responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_prepare_inquiry_orientation_answer(...)` carries the recovered boundary as a helper. No new dataclass artifact was introduced; `_InquiryOrientationAnswer` remains the unchanged compatibility artifact produced by the helper.

### 5. Who consumes it?

`_compose_inquiry_orientation_answer(state, request)` consumes it.

### 6. Did any compatibility boundary change?

```text
No.
```
