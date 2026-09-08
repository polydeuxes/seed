# Surveyor Implementation Ownership Audit

## Scope

This audit performs exactly one bounded Surveyor Implementation Ownership Audit. It does not recover another implementation slice, does not modify implementation, and does not modify existing slice records.

Repository implementation inspected was limited to implementation immediately adjacent to:

- `_prepare_inquiry_orientation_answer(...)`
- `_compose_inquiry_orientation_answer(...)`
- `build_inquiry_orientation(...)`
- `format_inquiry_orientation(...)`

The inspection expanded only where those functions naturally led inside `seed_runtime/inquiry_orientation.py`: the private answer payload/artifact helpers, the public `InquiryOrientationView` handoff, and the text formatter body.

## Implementation inspected

The adjacent implementation currently exposes this local chain:

```text
_prepare_inquiry_orientation_composition(note)
        ↓
_compose_inquiry_orientation_answer(state, request)
        ↓
_collect_inquiry_orientation_evidence(state, request)
        ↓
_prepare_inquiry_orientation_selected_material(evidence)
        ↓
_prepare_inquiry_orientation_answer(selected_material)
        ↓
_prepare_inquiry_orientation_answer_payload(selected_material)
        ↓
_assemble_inquiry_orientation_answer_artifact(payload)
        ↓
build_inquiry_orientation(state, note)
        ↓
InquiryOrientationView
        ↓
format_inquiry_orientation(view)
```

The directly inspected implementation evidence is:

- `build_inquiry_orientation(...)` prepares an inquiry-orientation composition request, composes the private answer, and maps private answer fields into `InquiryOrientationView`.
- `_compose_inquiry_orientation_answer(...)` delegates to evidence collection, selected-material preparation, and answer preparation, then returns the answer artifact.
- `_prepare_inquiry_orientation_answer(...)` delegates payload preparation and answer-artifact assembly.
- `_prepare_inquiry_orientation_answer_payload(...)` prepares the answer-facing fields.
- `_assemble_inquiry_orientation_answer_artifact(...)` copies prepared payload fields into `_InquiryOrientationAnswer`.
- `format_inquiry_orientation(...)` consumes `InquiryOrientationView` and renders deterministic V1 text sections.

## Recovered implementation progression

Surveyor Implementation Slice 004 recovered exactly one implementation-local ownership boundary:

```text
answer artifact assembly from prepared answer payload
```

The recovered implementation progression is now:

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
Compatibility handoff
        ↓
Build view
        ↓
Render
```

Four adjacent implementation-local ownership boundaries have now been recovered by repository implementation evidence. This audit treats those recovered boundaries as already owned and does not reopen them.

## Remaining implementation responsibilities

The visible remaining responsibilities adjacent to the inspected functions are:

1. answer artifact compatibility handoff;
2. public view construction;
3. renderer preparation;
4. text rendering;
5. JSON compatibility;
6. orchestration.

Each responsibility was assessed independently below.

## Ownership assessment by responsibility

### 1. Answer artifact compatibility handoff

**Implementation evidence.** `_prepare_inquiry_orientation_answer(...)` accepts `_InquiryOrientationSelectedMaterial`, obtains `_InquiryOrientationAnswerPayload`, and returns `_assemble_inquiry_orientation_answer_artifact(payload)`. Its body now exists as a narrow handoff between already recovered payload preparation and already recovered answer artifact assembly.

1. **Independent implementation-local producer?** No. The adjacent producers are already explicit: `_prepare_inquiry_orientation_answer_payload(...)` produces the prepared fields, and `_assemble_inquiry_orientation_answer_artifact(...)` produces `_InquiryOrientationAnswer`.
2. **Independently recoverable ownership boundary?** No. The handoff does not introduce a new artifact, select new material, derive new fields, or transform the public shape. It connects two already owned implementation-local producers.
3. **Would recovering this reduce ownership compression?** No. A new producer would wrap a two-step delegation and increase indirection without separating a hidden responsibility.
4. **Already lawful compatibility/orchestration?** Yes. It is lawful implementation-local compatibility handoff from selected material into the unchanged answer artifact path.

### 2. Public view construction

**Implementation evidence.** `build_inquiry_orientation(...)` prepares the composition request, obtains `_InquiryOrientationAnswer`, and constructs `InquiryOrientationView` by assigning `note=note`, `related_material=answer.answer`, `uncertainty=answer.limitations`, and `authority_boundary=answer.boundary`.

1. **Independent implementation-local producer?** Yes, but it is already the public producer: `build_inquiry_orientation(...)` produces `InquiryOrientationView`.
2. **Independently recoverable ownership boundary?** No. The implementation evidence shows a compatibility mapping from private answer names to the public view names rather than a compressed implementation-local producer. The mapping does not compute answer material, support, boundary, or limitations.
3. **Would recovering this reduce ownership compression?** No. Extracting a private `_build_inquiry_orientation_view(...)` would only repackage the public dataclass constructor and obscure the compatibility handoff already visible in `build_inquiry_orientation(...)`.
4. **Already lawful compatibility/orchestration?** Yes. The remaining responsibility is the lawful public compatibility handoff from `_InquiryOrientationAnswer` to `InquiryOrientationView`.

### 3. Renderer preparation

**Implementation evidence.** There is no distinct renderer-preparation artifact or helper adjacent to `format_inquiry_orientation(...)`. The formatter begins with a local `lines` list and appends rendered sections from the already prepared `InquiryOrientationView`.

1. **Independent implementation-local producer?** No. No adjacent helper prepares a renderer model, line bundle, section bundle, or formatting payload before text rendering.
2. **Independently recoverable ownership boundary?** No, based on current implementation evidence. The visible implementation proceeds directly from `InquiryOrientationView` fields to deterministic line appends.
3. **Would recovering this reduce ownership compression?** No. There is no separate renderer-preparation pressure visible in the adjacent implementation; creating one would introduce a new concept not demanded by the current code.
4. **Already lawful compatibility/orchestration?** Yes. The formatter consumes the public view directly, so any preparation is currently local presentation mechanics, not a separate implementation-local ownership boundary.

### 4. Text rendering

**Implementation evidence.** `format_inquiry_orientation(...)` renders five public text sections: inquiry note, potentially related material, support / why related, uncertainty, and authority boundary. It branches only on whether `view.related_material` is empty.

1. **Independent implementation-local producer?** Yes. `format_inquiry_orientation(...)` is the text producer.
2. **Independently recoverable ownership boundary?** No. It is already a named public rendering function and consumes the public `InquiryOrientationView`; no hidden implementation-local producer remains adjacent to it.
3. **Would recovering this reduce ownership compression?** No. Splitting text section rendering into private helpers would be presentation refactoring, not recovery of ownership pressure exposed by repository implementation.
4. **Already lawful compatibility/orchestration?** Yes. Text rendering is already lawfully owned by `format_inquiry_orientation(...)`.

### 5. JSON compatibility

**Implementation evidence.** No JSON renderer or JSON compatibility helper is adjacent to `_prepare_inquiry_orientation_answer(...)`, `_compose_inquiry_orientation_answer(...)`, `build_inquiry_orientation(...)`, or `format_inquiry_orientation(...)`. The adjacent implementation only imports `json` for inquiry-note persistence, through `_record_to_json(...)` and JSONL load/store behavior outside the inspected answer/view/rendering handoff.

1. **Independent implementation-local producer?** No adjacent producer is visible for inquiry-orientation JSON output.
2. **Independently recoverable ownership boundary?** No. The inspected neighborhood exposes no JSON compatibility implementation to recover.
3. **Would recovering this reduce ownership compression?** No. There is no local JSON compression in the inspected implementation neighborhood.
4. **Already lawful compatibility/orchestration?** Not applicable inside this bounded neighborhood. JSON compatibility is not visible here as an adjacent remaining responsibility.

### 6. Orchestration

**Implementation evidence.** `_compose_inquiry_orientation_answer(...)` now performs a short linear sequence: collect evidence, prepare selected material, prepare answer. `build_inquiry_orientation(...)` performs a short linear sequence: prepare composition request, compose answer, construct public view.

1. **Independent implementation-local producer?** No new independent producer is exposed by the remaining orchestration. The producers it calls are already explicit.
2. **Independently recoverable ownership boundary?** No. The remaining bodies are sequencing code, not compressed field derivation, artifact construction, selection, or rendering preparation.
3. **Would recovering this reduce ownership compression?** No. Further extraction would wrap already named steps and would not uncover a new local artifact or consumer.
4. **Already lawful compatibility/orchestration?** Yes. The remaining orchestration is lawful and visible.

## Candidate producer assessment

No candidate remaining responsibility exposes a new independent implementation-local producer adjacent to the inspected functions.

The already explicit producers are:

- `_collect_inquiry_orientation_evidence(...)` for evidence collection;
- `_select_inquiry_orientation_related_material(...)` for bounded related-material selection;
- `_prepare_inquiry_orientation_support(...)` for support payload preparation;
- `_prepare_inquiry_orientation_answer_payload(...)` for answer payload preparation;
- `_assemble_inquiry_orientation_answer_artifact(...)` for answer artifact assembly;
- `build_inquiry_orientation(...)` for the public `InquiryOrientationView` compatibility handoff;
- `format_inquiry_orientation(...)` for public text rendering.

The remaining visible code does not expose another producer that would own a distinct implementation-local responsibility between answer artifact assembly, public view construction, and rendering.

## Compatibility/orchestration assessment

The remaining visible implementation responsibilities are already lawfully owned as compatibility/orchestration:

- `_prepare_inquiry_orientation_answer(...)` is a compatibility handoff from selected material to the unchanged answer artifact path.
- `_compose_inquiry_orientation_answer(...)` is orchestration across already owned evidence, selected-material, and answer producers.
- `build_inquiry_orientation(...)` is orchestration plus compatibility mapping from private answer artifact to public view.
- `format_inquiry_orientation(...)` is the already named text renderer for the public view.

The inspected implementation does not show an adjacent hidden renderer-preparation producer or JSON compatibility producer.

## Implementation pressure assessment

There is no remaining recoverable implementation-local ownership pressure visible in the inspected neighborhood.

The remaining pressure is compatibility/orchestration pressure only:

- preserve the private `_InquiryOrientationAnswer` shape for composition;
- preserve the public `InquiryOrientationView` shape for callers, CLI output, and tests;
- preserve deterministic V1 text rendering;
- sequence already owned implementation-local producers without inventing another boundary.

A further implementation slice would require evidence of a hidden producer, hidden artifact, hidden consumer, or compressed transformation. The adjacent code currently shows none.

## Readiness classification

```text
Implementation family complete
```

The Surveyor implementation family is not ready for another implementation slice based on the inspected implementation evidence. The remaining visible responsibilities represent already lawful compatibility/orchestration ownership, not recoverable implementation-local ownership pressure.

## Preserved Unknowns

- This audit did not inspect unrelated implementation neighborhoods, so it does not classify Surveyor-like pressure elsewhere in the repository.
- This audit did not inspect broader CLI JSON handling, because no adjacent JSON compatibility implementation was visible in the bounded neighborhood.
- This audit did not assert that renderer preparation can never become separable; it only found no current adjacent implementation evidence for such a boundary.
- This audit did not reinterpret presentation vocabulary as repository knowledge.

## Confidence

Confidence is high for the bounded neighborhood inspected. The adjacent implementation is short, explicit, and already separates the previously recovered producers from the remaining compatibility and orchestration handoffs.

Surveyor implementation ownership audit complete.
