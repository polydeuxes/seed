# Constitutional Relationship Implementation Slice 005 Completion Audit

Repository authority wins.

## Scope

This is a bounded Implementation Pressure Audit of the implementation immediately adjacent to:

```text
_compose_inquiry_orientation_answer(...)
_collect_inquiry_orientation_evidence(...)
_prepare_inquiry_orientation_answer(...)
```

No implementation was modified. No additional constitutional boundary, orchestration framework, workflow, planner, scheduler, or universal answer builder was introduced or recommended.

## Inspected implementation

Inspected only the adjacent Inquiry Orientation implementation in `seed_runtime/inquiry_orientation.py`:

- `build_inquiry_orientation(...)`
- `_prepare_inquiry_orientation_composition(...)`
- `_compose_inquiry_orientation_answer(...)`
- `_prepare_inquiry_orientation_answer(...)`
- `_select_inquiry_orientation_reason(...)`
- `_select_inquiry_orientation_authority_boundary(...)`
- `_select_inquiry_orientation_limitations(...)`
- `_prepare_inquiry_orientation_selected_material(...)`
- `_collect_inquiry_orientation_evidence(...)`
- `_fact_matches(...)`
- `_source_navigation_matches(...)`
- `_dedupe_related(...)`
- the adjacent implementation-local dataclasses:
  - `_InquiryOrientationCompositionRequest`
  - `_InquiryOrientationEvidence`
  - `_InquiryOrientationSelectedMaterial`
  - `_InquiryOrientationAnswer`

Also inspected the adjacent preservation tests in `tests/test_inquiry_orientation.py` that already prove the recovered handoffs remain behavior-preserving.

## Current implementation progression

The implementation-local progression is:

```text
_prepare_inquiry_orientation_composition(...)
→ _InquiryOrientationCompositionRequest
→ _compose_inquiry_orientation_answer(...)
→ _collect_inquiry_orientation_evidence(...)
→ _InquiryOrientationEvidence
→ _prepare_inquiry_orientation_selected_material(...)
→ _InquiryOrientationSelectedMaterial
→ _select_inquiry_orientation_reason(...)
→ _select_inquiry_orientation_authority_boundary(...)
→ _select_inquiry_orientation_limitations(...)
→ _prepare_inquiry_orientation_answer(...)
→ _InquiryOrientationAnswer
→ build_inquiry_orientation(...)
→ InquiryOrientationView
```

Inside this progression, `_compose_inquiry_orientation_answer(...)` now performs only the local sequencing of already owned implementation steps:

```text
evidence = _collect_inquiry_orientation_evidence(state, request)
selected_material = _prepare_inquiry_orientation_selected_material(evidence)
return _prepare_inquiry_orientation_answer(selected_material)
```

## Remaining responsibilities

The remaining collected-evidence consumption/orchestration consists of:

1. invoking the evidence producer with the state and prepared request;
2. passing produced evidence into selected-material preparation;
3. passing selected material into answer preparation;
4. returning the prepared `_InquiryOrientationAnswer` compatibility artifact to the public-view adapter.

The evidence producer itself owns repository evidence collection:

```text
_fact_matches(state, request.note_tokens)
_source_navigation_matches(state, request.note_tokens)
_dedupe_related(...)
[:_MAX_RELATED_ITEMS]
_InquiryOrientationEvidence(related_material=related)
```

The selected-material producer owns selected related material and support preservation. The answer producer owns answer construction from selected material. The remaining orchestration does not still construct facts, source-navigation rows, selected support, reason text, authority-boundary text, limitation text, or the answer dataclass fields.

## Are the remaining responsibilities implementation-local orchestration responsibilities?

Yes.

The remaining responsibility is implementation-local orchestration because it only sequences three implementation-local producers and returns the implementation-local answer artifact. It does not own an independent data shape, selection rule, support transformation, authority decision, limitation decision, rendering section, event-ledger write, cluster mutation, or public compatibility field.

The orchestration is also inquiry-orientation-specific. It is not a reusable workflow or universal answer builder; it wires this local Inquiry Orientation request/evidence/selected-material/answer chain.

## Candidate producer

No additional candidate producer is exposed by implementation evidence.

Existing adjacent producers already own the separable work:

| Producer | Owned responsibility |
| --- | --- |
| `_prepare_inquiry_orientation_composition(...)` | converts preserved note prose into the implementation-local composition request and note-token set |
| `_collect_inquiry_orientation_evidence(...)` | collects and limits related projected-fact and source-navigation evidence |
| `_prepare_inquiry_orientation_selected_material(...)` | preserves selected related material and its support strings |
| `_select_inquiry_orientation_reason(...)` | selects reason text |
| `_select_inquiry_orientation_authority_boundary(...)` | selects the authority-boundary text |
| `_select_inquiry_orientation_limitations(...)` | selects uncertainty text from whether material was selected |
| `_prepare_inquiry_orientation_answer(...)` | constructs the implementation-local answer artifact |

The only conceivable new producer would be a wrapper around the already linear call chain. That would not recover ownership; it would rename orchestration.

## Candidate artifact/helper

No additional candidate artifact or helper is exposed by implementation evidence.

Existing adjacent artifacts already carry the implementation-local handoffs:

| Artifact | Carries |
| --- | --- |
| `_InquiryOrientationCompositionRequest` | preserved note plus tokenized note material for composition |
| `_InquiryOrientationEvidence` | collected related material |
| `_InquiryOrientationSelectedMaterial` | selected related material plus preserved support strings |
| `_InquiryOrientationAnswer` | answer material, reason, support, authority boundary, and limitations |
| `InquiryOrientationView` | public rendered-view compatibility fields |

A further artifact between evidence, selected material, and answer would have no implementation-backed field ownership. It would duplicate either `_InquiryOrientationEvidence`, `_InquiryOrientationSelectedMaterial`, or `_InquiryOrientationAnswer`, or it would become an artificial orchestration envelope.

## Candidate consumer

The existing candidate consumers are already explicit:

1. `_compose_inquiry_orientation_answer(...)` consumes `_InquiryOrientationEvidence`, `_InquiryOrientationSelectedMaterial`, and `_InquiryOrientationAnswer` as the implementation-local orchestrator.
2. `build_inquiry_orientation(...)` consumes `_InquiryOrientationAnswer` and adapts it to `InquiryOrientationView`.
3. `format_inquiry_orientation(...)` consumes `InquiryOrientationView` for text rendering outside the inspected composition boundary.

No additional consumer is exposed inside the bounded neighborhood.

## Implementation pressure assessment

### Evidence for a lawful terminal orchestration responsibility

Implementation evidence supports terminal orchestration:

- `_collect_inquiry_orientation_evidence(...)` already owns all evidence acquisition, deduplication, deterministic ordering, and maximum related-item limiting.
- `_prepare_inquiry_orientation_selected_material(...)` already owns preservation of selected material and support strings.
- `_prepare_inquiry_orientation_answer(...)` already owns construction of the `_InquiryOrientationAnswer` artifact.
- Reason, authority-boundary, and limitation selection are already individually owned helpers.
- `_compose_inquiry_orientation_answer(...)` now contains no inline branching, no inline shape construction, no local string choice, no local support extraction, and no public rendering adaptation.
- The remaining body is exactly the lawful call-order required to connect request, evidence, selected material, answer, and public view.

### Evidence against another recoverable producer

No adjacent implementation exposes a separate unnamed computation. Another producer would have to own one of these shapes:

```text
request → evidence

evidence → selected material

selected material → answer
```

Each is already owned. A new producer over all three would merely wrap orchestration and would not reduce implementation compression.

### Evidence against another recoverable artifact/helper

No remaining intermediate data exists between:

```text
_InquiryOrientationEvidence
_InquiryOrientationSelectedMaterial
_InquiryOrientationAnswer
```

The orchestration body does not compute a hidden value that needs carrying. It only names already existing artifacts. A new artifact would therefore duplicate an existing artifact or record call-chain state rather than implementation-owned material.

### Would another slice reduce compression without merely wrapping orchestration?

No.

Another slice would not recover an implementation-local ownership boundary. It would move this body:

```text
evidence = _collect_inquiry_orientation_evidence(state, request)
selected_material = _prepare_inquiry_orientation_selected_material(evidence)
return _prepare_inquiry_orientation_answer(selected_material)
```

behind another function or object. That would make the same orchestration less direct without exposing a distinct producer, artifact, or consumer.

## Required questions

### 1. What responsibilities currently remain inside the orchestration?

Only call sequencing remains:

1. collect evidence from the state and request;
2. prepare selected material from evidence;
3. prepare answer from selected material;
4. return the implementation-local answer artifact.

### 2. Are they implementation-local orchestration responsibilities?

Yes. They are Inquiry Orientation implementation-local orchestration responsibilities. They do not carry independent answer, reason, support, boundary, limitation, rendering, event-ledger, cluster-mutation, or public API ownership.

### 3. Does implementation evidence expose another recoverable producer?

No. The adjacent producers are already explicit. Another producer would merely wrap `_collect_inquiry_orientation_evidence(...)`, `_prepare_inquiry_orientation_selected_material(...)`, and `_prepare_inquiry_orientation_answer(...)`.

### 4. Does implementation evidence expose another recoverable artifact or helper?

No. The adjacent artifacts already preserve the observable handoffs. There is no hidden intermediate shape between evidence, selected material, and answer.

### 5. Would another slice reduce compression without merely wrapping orchestration?

No. The only possible additional slice would be an orchestration wrapper. That is explicitly unsupported by the implementation evidence and by the bounded audit goal.

### 6. Is this neighborhood implementation-complete?

Yes. The neighborhood is implementation-complete for this family. The remaining orchestration is a lawful terminal responsibility.

## Completion classification

```text
Implementation family complete
```

## Preserved Unknowns

- This audit does not assert that unrelated inquiry surfaces are complete; they were intentionally not inspected.
- This audit does not assert that no future requirement could change Inquiry Orientation composition; it only classifies the current adjacent implementation evidence.
- This audit does not promote presentation vocabulary into repository knowledge.
- This audit does not evaluate CLI inventory or diagnostic-shape surfaces because no diagnostic, audit, probe, view, operational CLI flag, or recordable output was added or modified.
- This audit does not claim semantic interpretation of inquiry notes; Inquiry Orientation remains deterministic lexical overlap against existing projected read models.

## Confidence

High.

The inspected implementation shows all previously recovered local ownership boundaries as explicit producers, helpers, and artifacts. The remaining `_compose_inquiry_orientation_answer(...)` body is a short linear sequence whose only responsibility is connecting those already owned steps. No implementation evidence exposes another distinct producer, artifact, helper, or consumer.

Implementation completion audit complete.
