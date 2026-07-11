# Constitutional Relationship Implementation Slice 001

Repository authority wins.

## Selected boundary

Selected implementation-local ownership boundary:

```text
selected inquiry-orientation material support preservation
```

Implementation evidence selected this boundary. The slice did not use constitutional prose to force a universal artifact, engine, registry, profile framework, or redesign.

The recovered handoff is now:

```text
_collect_inquiry_orientation_evidence(...)
→ _prepare_inquiry_orientation_selected_material(...)
→ _InquiryOrientationSelectedMaterial
→ _compose_inquiry_orientation_answer(...)
→ _InquiryOrientationAnswer
→ build_inquiry_orientation(...)
```

## Implementation evidence

The prior `_compose_inquiry_orientation_answer(...)` implementation consumed collected evidence directly, selected `evidence.related_material`, preserved support strings with `[item.support for item in related]`, assigned the fixed reason, attached the authority boundary, selected limitations, and constructed `_InquiryOrientationAnswer`.

The implementation-local pressure was strongest around support preservation because it was already a distinct computation over selected related material and was already asserted by tests as answer-local support:

```text
answer.support == [item.support for item in view.related_material]
```

The new `_prepare_inquiry_orientation_selected_material(...)` helper makes that local boundary directly observable without changing the answer artifact or any public view/rendering behavior.

## Before

Before this slice, `_compose_inquiry_orientation_answer(...)` owned all of these responsibilities at once:

1. collected-evidence consumption;
2. selected-material preparation;
3. support preservation;
4. reason assignment;
5. authority-boundary attachment;
6. limitation selection;
7. `_InquiryOrientationAnswer` construction.

## After

After this slice, exactly one responsibility was recovered:

```text
selected-material support preservation
```

`_compose_inquiry_orientation_answer(...)` still owns answer composition: reason assignment, authority-boundary attachment, limitation selection, and `_InquiryOrientationAnswer` construction. Evidence collection remains unchanged.

## Recovered producer

Recovered producer:

```text
_prepare_inquiry_orientation_selected_material(evidence)
```

It consumes `_InquiryOrientationEvidence`, selects the related material already collected for inquiry orientation, and preserves the selected material's support strings.

## Recovered artifact/helper

Recovered artifact/helper:

```text
_InquiryOrientationSelectedMaterial
```

It carries only:

```text
related_material: list[RelatedMaterial]
support: list[str]
```

It does not carry note text, reason, authority boundary, limitations, uncertainty, or rendering fields.

## Recovered consumer

Recovered consumer:

```text
_compose_inquiry_orientation_answer(state, request)
```

It consumes `_InquiryOrientationSelectedMaterial` and copies its `related_material` and `support` into the unchanged `_InquiryOrientationAnswer` compatibility artifact.

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
- reason behavior unchanged;
- uncertainty text unchanged;
- authority-boundary text unchanged;
- read-only behavior unchanged;
- no runtime-state projection added;
- no fact recording added;
- no event-ledger writes added;
- no cluster mutation added;
- `_InquiryOrientationAnswer` fields and consumer compatibility unchanged;
- Selection Path implementation not modified.

## Files changed

- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `constitutional_relationship_implementation_slice_001.md`

## LOC changed

Current implementation/test diff before this document:

```text
28 insertions, 4 deletions: seed_runtime/inquiry_orientation.py
12 insertions, 2 deletions: tests/test_inquiry_orientation.py
191 insertions, 0 deletions: constitutional_relationship_implementation_slice_001.md
```

This document was added as the requested implementation-slice record.

## Tests executed

```text
pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
11 passed
```

## Remaining compressed responsibilities

The following responsibilities intentionally remain compressed inside `_compose_inquiry_orientation_answer(...)`:

1. reason assignment;
2. authority-boundary attachment;
3. limitation selection;
4. `_InquiryOrientationAnswer` construction.

Collected-evidence consumption also remains in `_compose_inquiry_orientation_answer(...)` as the local orchestration step that calls evidence collection before selected-material preparation.

## Required questions

### 1. What responsibilities were previously compressed?

Collected-evidence consumption, selected-material preparation, support preservation, reason assignment, authority-boundary attachment, limitation selection, and `_InquiryOrientationAnswer` construction were previously compressed in `_compose_inquiry_orientation_answer(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

Selected inquiry-orientation material support preservation became directly observable.

### 3. What producer now owns the recovered responsibility?

`_prepare_inquiry_orientation_selected_material(evidence)` now owns the recovered responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_InquiryOrientationSelectedMaterial` carries the recovered boundary.

### 5. Who consumes it?

`_compose_inquiry_orientation_answer(state, request)` consumes it.

### 6. Did any compatibility boundary change?

```text
No.
```
