# Surveyor Implementation Slice 004

## Selected boundary

Answer artifact assembly from prepared answer payload.

This slice began only from implementation immediately adjacent to `_prepare_inquiry_orientation_answer_payload(...)`, `_prepare_inquiry_orientation_answer(...)`, and `_compose_inquiry_orientation_answer(...)`. The constitutional Surveyor characterization remained orientation only. Repository implementation selected the recovered boundary: after answer payload fields are prepared, `_prepare_inquiry_orientation_answer(...)` still compressed delegation to payload preparation with direct `_InquiryOrientationAnswer` artifact assembly.

## Implementation evidence

- `_compose_inquiry_orientation_answer(...)` already consumes selected material preparation and delegates final answer preparation to `_prepare_inquiry_orientation_answer(...)`.
- `_prepare_inquiry_orientation_answer_payload(...)` already owns preparation of the `answer`, `reason`, `support`, `boundary`, and `limitations` fields from selected material.
- The immediately adjacent remaining responsibility was converting that prepared payload into the private `_InquiryOrientationAnswer` artifact consumed by composition and public view construction.
- The new `_assemble_inquiry_orientation_answer_artifact(...)` helper takes only `_InquiryOrientationAnswerPayload` and produces the unchanged `_InquiryOrientationAnswer` artifact.
- Tests prove the assembled artifact is identical to the prepared answer and composed answer, preserving the public compatibility boundary.

## Before

Before this slice, `_prepare_inquiry_orientation_answer(...)` performed two adjacent responsibilities after Slice 003:

1. request the prepared answer payload from `_prepare_inquiry_orientation_answer_payload(...)`;
2. directly assemble `_InquiryOrientationAnswer` from that payload.

## After

After this slice, the implementation-local progression is:

1. `_compose_inquiry_orientation_answer(...)` collects evidence and prepares selected material.
2. `_prepare_inquiry_orientation_answer_payload(...)` prepares answer fields from selected material.
3. `_assemble_inquiry_orientation_answer_artifact(...)` assembles `_InquiryOrientationAnswer` from the prepared payload.
4. `_prepare_inquiry_orientation_answer(...)` remains the compatibility handoff from selected material to the unchanged answer artifact.
5. `build_inquiry_orientation(...)` and rendering continue to consume the same answer/view shapes unchanged.

Runtime output remains unchanged because the new helper copies the same payload fields into the same `_InquiryOrientationAnswer` dataclass fields that `_prepare_inquiry_orientation_answer(...)` populated before this slice.

## Recovered producer

The recovered producer is `_assemble_inquiry_orientation_answer_artifact(...)`.

It owns only answer artifact assembly from already prepared answer payload fields.

## Recovered artifact/helper

The recovered helper is `_assemble_inquiry_orientation_answer_artifact(...)`.

No new public artifact was introduced. `_InquiryOrientationAnswer` remains the unchanged implementation-local compatibility artifact returned through `_prepare_inquiry_orientation_answer(...)` and `_compose_inquiry_orientation_answer(...)`.

## Recovered consumer

The immediate consumer is `_prepare_inquiry_orientation_answer(...)`, which now consumes `_InquiryOrientationAnswerPayload` through the recovered assembly helper instead of assembling `_InquiryOrientationAnswer` inline.

Downstream consumers remain unchanged:

- `_compose_inquiry_orientation_answer(...)` returns the same `_InquiryOrientationAnswer` shape;
- `build_inquiry_orientation(...)` maps the same answer fields into `InquiryOrientationView`;
- formatting and JSON serialization remain unchanged.

## Compatibility preserved

No public compatibility boundary changed.

The unchanged compatibility path remains:

```text
_prepare_inquiry_orientation_answer_payload(...)
        ↓
_assemble_inquiry_orientation_answer_artifact(...)
        ↓
_prepare_inquiry_orientation_answer(...)
        ↓
_compose_inquiry_orientation_answer(...)
        ↓
build_inquiry_orientation(...)
        ↓
InquiryOrientationView / JSON / text rendering
```

`_assemble_inquiry_orientation_answer_artifact(...)` is private and implementation-local. It does not change CLI behavior, JSON output, schemas, diagnostic surfaces, or event-ledger behavior.

## Required questions

### 1. What responsibilities were previously compressed?

Payload delegation and `_InquiryOrientationAnswer` artifact assembly were previously compressed inside `_prepare_inquiry_orientation_answer(...)` after Slice 003.

### 2. Which implementation-local ownership boundary became directly observable?

Answer artifact assembly from prepared answer payload became directly observable.

### 3. What producer now owns the recovered responsibility?

`_assemble_inquiry_orientation_answer_artifact(...)` now owns the recovered responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

The helper `_assemble_inquiry_orientation_answer_artifact(...)` carries the recovered boundary. The existing `_InquiryOrientationAnswer` artifact carries the assembled private answer shape; no new public artifact was introduced.

### 5. Who consumes it?

`_prepare_inquiry_orientation_answer(...)` consumes it immediately. `_compose_inquiry_orientation_answer(...)`, `build_inquiry_orientation(...)`, and render/serialization paths consume the unchanged downstream answer/view shapes.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `surveyor_implementation_slice_004.md`

## LOC changed

Current working tree stat after this slice:

```text
seed_runtime/inquiry_orientation.py     |  8 ++++++++
tests/test_inquiry_orientation.py       | 36 +++++++++++++++++++++++++++++++++++-
surveyor_implementation_slice_004.md    | 154 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

## Tests executed

```text
pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
19 passed
```

## Remaining compressed responsibilities

After this slice, the recovered Surveyor implementation progression is:

```text
Collect evidence
        ↓
Select bounded related material
        ↓
Prepare support payload
        ↓
Prepare answer payload
        ↓
Assemble answer artifact
        ↓
Build view
        ↓
Render
```

The intentionally remaining adjacent responsibilities are the already explicit compatibility handoff into public view construction and rendering. This slice does not recover them, does not redesign Surveyor, does not redesign Inquiry Orientation, and does not change Recovery.
