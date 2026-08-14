# Constitutional Relationship Implementation Slice 004

Repository authority wins.

## Selected boundary

Selected implementation-local ownership boundary:

```text
selected inquiry-orientation material authority-boundary selection
```

Implementation evidence selected this boundary immediately adjacent to Slice 003. The slice did not use constitutional prose to force answer construction, collected-evidence orchestration, rendering, a universal artifact, engine, registry, profile framework, workflow, planner, scheduler, Selection Path modification, or redesign.

The recovered handoff is now:

```text
_collect_inquiry_orientation_evidence(...)
→ _prepare_inquiry_orientation_selected_material(...)
→ _InquiryOrientationSelectedMaterial
→ _select_inquiry_orientation_reason(...)
→ _select_inquiry_orientation_authority_boundary(...)
→ _select_inquiry_orientation_limitations(...)
→ _compose_inquiry_orientation_answer(...)
→ _InquiryOrientationAnswer
→ build_inquiry_orientation(...)
```

## Implementation evidence

Slices 001 through 003 made these local boundaries directly observable before `_InquiryOrientationAnswer` construction:

1. selected-material support preservation;
2. selected-material limitation selection;
3. selected-material reason selection.

Immediately adjacent implementation evidence showed that `_compose_inquiry_orientation_answer(...)` still attached the authority-boundary text directly while constructing `_InquiryOrientationAnswer`:

```text
boundary=AUTHORITY_BOUNDARY
```

That attachment is implementation-local, deterministic, and scoped to the selected inquiry-orientation material handoff. It does not require note storage, rendering state, answer rendering, CLI transport, event-ledger writes, cluster mutation, fact recording, runtime-state projection, or public behavior changes.

The new `_select_inquiry_orientation_authority_boundary(...)` helper makes that local boundary directly observable while preserving the unchanged `_InquiryOrientationAnswer.boundary` compatibility field and unchanged public JSON/text behavior.

## Before

Before this slice, `_compose_inquiry_orientation_answer(...)` still owned all of these responsibilities at once after Slice 003:

1. collected-evidence consumption/orchestration;
2. authority-boundary attachment;
3. `_InquiryOrientationAnswer` construction.

## After

After this slice, exactly one additional responsibility was recovered:

```text
selected-material authority-boundary selection
```

`_compose_inquiry_orientation_answer(...)` still owns answer composition: collected-evidence consumption/orchestration and `_InquiryOrientationAnswer` construction. Slice 001 support preservation, Slice 002 limitation selection, and Slice 003 reason selection remain unchanged.

## Recovered producer

Recovered producer:

```text
_select_inquiry_orientation_authority_boundary(selected_material)
```

It consumes `_InquiryOrientationSelectedMaterial` and returns the exact authority-boundary text used by the inquiry-orientation answer.

## Recovered artifact/helper

Recovered artifact/helper:

```text
_select_inquiry_orientation_authority_boundary(...)
```

No new artifact was required. The existing `_InquiryOrientationSelectedMaterial` helper artifact carries the selected related material that this recovered helper is scoped to.

The helper does not carry or own note text, support preservation, limitation selection, reason selection, rendering fields, event-ledger writes, cluster mutation, fact recording, runtime-state projection, or `_InquiryOrientationAnswer` construction.

## Recovered consumer

Recovered consumer:

```text
_compose_inquiry_orientation_answer(state, request)
```

It consumes the helper result by copying the returned string into the unchanged `_InquiryOrientationAnswer.boundary` compatibility field.

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
- `constitutional_relationship_implementation_slice_004.md`

## LOC changed

Implementation/test diff before this document:

```text
37 insertions, 1 deletion: seed_runtime/inquiry_orientation.py and tests/test_inquiry_orientation.py
```

This document was added as the requested implementation-slice record.

## Tests executed

```text
pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
14 passed
```

## Remaining compressed responsibilities

The following responsibilities intentionally remain compressed inside `_compose_inquiry_orientation_answer(...)`:

1. collected-evidence consumption/orchestration;
2. `_InquiryOrientationAnswer` construction.

## Required questions

### 1. What responsibilities were previously compressed?

Collected-evidence consumption/orchestration, authority-boundary attachment, and `_InquiryOrientationAnswer` construction were previously compressed in `_compose_inquiry_orientation_answer(...)` after Slice 003.

### 2. Which implementation-local ownership boundary became directly observable?

Selected inquiry-orientation material authority-boundary selection became directly observable.

### 3. What producer now owns the recovered responsibility?

`_select_inquiry_orientation_authority_boundary(selected_material)` now owns the recovered responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_select_inquiry_orientation_authority_boundary(...)` carries the recovered boundary as a helper. No new dataclass artifact was introduced.

### 5. Who consumes it?

`_compose_inquiry_orientation_answer(state, request)` consumes it.

### 6. Did any compatibility boundary change?

```text
No.
```
