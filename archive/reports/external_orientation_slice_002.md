# External Orientation Slice 002

## Selected implementation boundary

Recovered implementation-local boundary:

```text
Inquiry Note Preservation
        !=
Inquiry Orientation Composition
```

More precise local owner:

```text
Preserved inquiry note material
        -> private inquiry-orientation composition request
        -> inquiry orientation evidence/composition
```

This is the smallest lawful slice under the committed `External Material != External Orientation` boundary. It does not implement generic Orientation, does not implement `External Orientation != Orientation`, and does not add any framework, registry, taxonomy, classifier, schema, ledger behavior, CLI behavior, JSON shape, or runtime redesign.

## Implementation evidence

The concrete implementation surface is `seed_runtime/inquiry_orientation.py`.

- `record_inquiry_note(...)` still owns preservation of externally supplied inquiry material by validating and appending one raw note to the isolated JSONL probe store.
- `build_inquiry_orientation(...)` still owns the public compatibility handoff into unchanged `InquiryOrientationView`.
- `_prepare_inquiry_orientation_composition(...)` now makes the implementation-local handoff explicit by preparing a private `_InquiryOrientationCompositionRequest` from the preserved note.
- `_collect_inquiry_orientation_evidence(...)` consumes that request and collects the same deterministic fact-support and source-navigation matches as before.
- `_compose_inquiry_orientation_answer(...)` consumes that evidence and composes the same answer payload before the unchanged public view/rendering handoff.
- `format_inquiry_orientation(...)` remains unchanged and renders the same V1 text sections.

## Before

External Material preservation and External Orientation composition were mixed in the inquiry-orientation path immediately after note selection:

```text
build_inquiry_orientation(state, note)
        -> _compose_architectural_orientation_answer(state, note)
        -> _collect_architectural_orientation_evidence(state, note)
        -> _note_tokens(note.raw_note)
        -> fact/source-navigation matching
        -> InquiryOrientationView
```

The preserved `InquiryNoteRecord` was passed directly into answer composition and evidence collection. That made the local boundary between preserved operator prose and inquiry-orientation evidence preparation observable only indirectly.

## After

The local boundary is now directly observable:

```text
record_inquiry_note(...)
        -> InquiryNoteRecord

build_inquiry_orientation(state, note)
        -> _prepare_inquiry_orientation_composition(note)
        -> _InquiryOrientationCompositionRequest
        -> _collect_inquiry_orientation_evidence(state, request)
        -> _compose_inquiry_orientation_answer(state, request)
        -> InquiryOrientationView
```

The new handoff carries only the preserved note plus deterministic note tokens needed by the existing orientation behavior. It does not classify sources, introduce orientation kinds, or change matching, rendering, recording, or authority behavior.

## Recovered producer

Recovered producer:

```text
Inquiry orientation input preparer
```

Concrete producer:

```text
_prepare_inquiry_orientation_composition(note)
```

It prepares bounded inquiry-orientation input from externally supplied material that has already been accepted by the existing inquiry-note preservation surface.

## Recovered artifact/helper, if any

Recovered private artifact/helper:

```text
_InquiryOrientationCompositionRequest
_prepare_inquiry_orientation_composition(...)
```

The artifact is private and implementation-local. It carries:

- the preserved `InquiryNoteRecord`; and
- the deterministic token set derived from the preserved raw note.

It deliberately does not carry public output fields such as uncertainty, authority boundary, rendered sections, or related material.

## Consumer

Consumers:

- `_collect_inquiry_orientation_evidence(state, request)` consumes `_InquiryOrientationCompositionRequest` for deterministic evidence collection.
- `_compose_inquiry_orientation_answer(state, request)` consumes the same request as the bounded input to answer composition.
- `build_inquiry_orientation(state, note)` consumes the composed private answer and preserves the existing compatibility handoff to `InquiryOrientationView`.

## Compatibility preserved

No.

No compatibility boundary changed:

- No CLI flags changed.
- No JSON output changed.
- No schema changed.
- No event or ledger behavior changed.
- No diagnostic inventory behavior changed.
- No source-navigation behavior changed.
- No bounded ask behavior changed.
- No pressure-audit behavior changed.
- No runtime behavior changed.
- No public `InquiryOrientationView` fields changed.
- No rendering sections changed.

## Files changed

- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `external_orientation_slice_002.md`

## LOC changed

Staged diff summary:

```text
external_orientation_slice_002.md   | 216 ++++++++++++++++++++++++++++++++++++
seed_runtime/inquiry_orientation.py |  58 ++++++----
tests/test_inquiry_orientation.py   |  27 +++--
3 files changed, 274 insertions(+), 27 deletions(-)
```

Staged numeric diff:

```text
216 insertions, 0 deletions: external_orientation_slice_002.md
40 insertions, 18 deletions: seed_runtime/inquiry_orientation.py
18 insertions, 9 deletions: tests/test_inquiry_orientation.py
```

## Tests executed

Commands executed:

```text
pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
11 passed in 1.06s
```

## Required questions

### 1. Where were External Material preservation and External Orientation composition previously mixed?

They were mixed in `build_inquiry_orientation(...)` and its private downstream helpers. The preserved `InquiryNoteRecord` was passed directly into `_compose_architectural_orientation_answer(...)`, which passed it directly into `_collect_architectural_orientation_evidence(...)`; evidence collection then tokenized `note.raw_note` inline before matching projected fact supports and source-navigation rows.

### 2. Which implementation-local boundary became directly observable?

The boundary between inquiry note preservation and inquiry orientation composition became directly observable:

```text
Inquiry Note Preservation
        !=
Inquiry Orientation Composition
```

In external-orientation terms, this is the concrete implementation-local form of:

```text
External Material Intake
        !=
External Orientation Composition
```

### 3. What private artifact or helper now carries the handoff, if any?

`_InquiryOrientationCompositionRequest` carries the private handoff, and `_prepare_inquiry_orientation_composition(...)` constructs it.

### 4. Who consumes that artifact/helper?

`_collect_inquiry_orientation_evidence(...)` consumes the request for deterministic fact-support and source-navigation matching. `_compose_inquiry_orientation_answer(...)` consumes the request as its bounded orientation input before `build_inquiry_orientation(...)` maps the composed private answer into the unchanged `InquiryOrientationView`.

### 5. Did any compatibility boundary change?

No.

## Why `orientation_slice_001.md` remains overbroad for implementation

`orientation_slice_001.md` attempted to recover `External Orientation != Orientation` and named a report-level orientation source specialization classifier. That is overbroad for the current implementation because the repository does not show a concrete runtime consumer for a generic orientation source classifier, enum, registry, taxonomy, or framework.

This slice is smaller and lawful because it stays under the committed `External Material != External Orientation` recovery and selects exactly one implementation-local owner already present in code: the inquiry-orientation handoff from preserved external material to bounded inquiry-orientation evidence/composition.

## Remaining compressed External Orientation responsibilities

The following responsibilities remain intentionally compressed and unrecovered:

- Whether source navigation needs its own external-query handoff.
- Whether bounded ask needs a similar external question-family handoff beyond existing eligibility/selection records.
- Whether operational or diagnostic visibility surfaces need additional local external-material boundaries.
- Whether old report-level “architectural orientation” vocabulary should be updated in historical documents.
- Whether any future implementation surface needs a shared external-orientation artifact.

Current implementation evidence supports only this private inquiry-orientation slice.
