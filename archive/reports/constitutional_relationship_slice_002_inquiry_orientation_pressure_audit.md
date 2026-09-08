# Constitutional Relationship Slice 002 Inquiry Orientation Pressure Audit

Repository authority wins.

## Scope

This is exactly one bounded inquiry-orientation Implementation Pressure Audit for the preserved boundary:

```text
A competent local producer preserves
a bounded constitutional profile.

A bounded downstream consumer uses
only that preserved profile
within its local role.
```

This audit does not modify implementation, recover another constitutional characterization, introduce an artifact framework, introduce a universal profile type, invent a producer or consumer, infer implementation from constitutional prose, or recommend architectural redesign.

## Inspected implementation

Implementation inspection began adjacent to warrant, reliance, inquiry-artifact, diagnostic, answer-composition, and typed-unknown surfaces, then stopped at the first implementation-backed local manifestation matching the requested shape.

Inspected implementation evidence:

- `seed_runtime/inquiry_orientation.py`
  - `InquiryNoteRecord`
  - `RelatedMaterial`
  - `InquiryOrientationView`
  - `_InquiryOrientationCompositionRequest`
  - `_InquiryOrientationEvidence`
  - `_InquiryOrientationAnswer`
  - `record_inquiry_note(...)`
  - `load_inquiry_notes(...)`
  - `select_inquiry_note(...)`
  - `build_inquiry_orientation(...)`
  - `_prepare_inquiry_orientation_composition(...)`
  - `_compose_inquiry_orientation_answer(...)`
  - `_collect_inquiry_orientation_evidence(...)`
  - `format_inquiry_orientation(...)`
  - `_fact_matches(...)`
  - `_source_navigation_matches(...)`
- `tests/test_inquiry_orientation.py`
  - tests proving raw note preservation and provenance;
  - tests proving the inquiry note is not projected into runtime state;
  - tests proving read-only orientation output, support, uncertainty, and authority boundary;
  - tests proving composition request, evidence, answer, and rendering remain separated.
- `seed_runtime/inquiry_artifacts.py`
  - `InquiryArtifactVisibility`
  - `_InquiryArtifactEvidencePayload`
  - `_InquiryArtifactLimitationsPayload`
  - `_artifact_visibility_from_payloads(...)`
  - `BOUNDARY`
  - `ARTIFACTS`
- `seed_runtime/typed_unknowns.py`
  - `TypedUnknownRecord`
  - `preserve_typed_unknown(...)`
  - `typed_unknowns_to_public_dicts(...)`
- `scripts/seed_local.py`
  - `--record-inquiry-note`
  - `--inquiry-orientation`
  - `--inquiry-artifacts`
  - `--diagnostic-inventory`
  - `inquiry_note_store_path_from_args(...)`
  - inquiry-note recording and inquiry-orientation dispatch paths.

App authority checks used:

```text
python scripts/seed_local.py --inquiry-artifacts
python scripts/seed_local.py --diagnostic-inventory
```

The app confirmed the inquiry-artifacts surface is read-only, has no recording, has no event-ledger writes, has no cluster mutation, and does not create inquiry graphs, infer pressure transformation, or perform workflow/planning behavior. The diagnostic inventory confirmed `inquiry_artifacts`, `diagnostic_inventory`, and `diagnostic_shape_audit` are declared read-only, non-recording, and non-mutating surfaces.

## Candidate producer

Candidate producer:

```text
_compose_inquiry_orientation_answer(state, request)
```

This function currently constructs and preserves a bounded implementation-local profile after evidence collection. It consumes only the prepared composition request and locally collected evidence, then returns `_InquiryOrientationAnswer`.

The producer preserves fields equivalent to the requested profile shape:

- subject or identity: bounded to the already selected `InquiryNoteRecord` carried through `_InquiryOrientationCompositionRequest`;
- evidence/support: `support=[item.support for item in related]`;
- provenance: preserved upstream by `InquiryNoteRecord.source`, `recorded_at`, optional `workspace_id`, optional `session_id`, and by `RelatedMaterial.support` strings;
- authority boundary: `boundary=AUTHORITY_BOUNDARY`;
- negative authority: `AUTHORITY_BOUNDARY` explicitly states the orientation is not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, runtime instruction, ownership claim, recommended action, or next safe move;
- Unknowns/limitations: `limitations=UNCERTAINTY_WITH_MATCHES` or `UNCERTAINTY_WITHOUT_MATCHES`;
- confidence/stop limits: deterministic lexical overlap only; no semantic interpretation; no assertion of importance, ownership, intent, concern, recommended action, or next safe move; absence of related material does not prove unrelatedness.

## Candidate artifact

Candidate artifact:

```text
_InquiryOrientationAnswer
```

The artifact carries the bounded profile with these fields:

```text
answer: list[RelatedMaterial]
reason: str
support: list[str]
boundary: str
limitations: str
```

It is implementation-local and not a universal profile type. It is narrower than `InquiryOrientationView`, because it does not carry the presentation-facing `note`, `related_material`, `uncertainty`, or `authority_boundary` fields. Existing tests explicitly prove this separation.

## Candidate consumer

Candidate consumer:

```text
build_inquiry_orientation(state, note)
```

This consumer uses the `_InquiryOrientationAnswer` only within its local role: building `InquiryOrientationView` for rendering. It maps:

- `answer.answer` to `InquiryOrientationView.related_material`;
- `answer.limitations` to `InquiryOrientationView.uncertainty`;
- `answer.boundary` to `InquiryOrientationView.authority_boundary`.

Downstream presentation is then handled by:

```text
format_inquiry_orientation(view)
```

The rendering path consumes the view, not the evidence-collection internals. This preserves the local producer/artifact/consumer boundary without requiring a broader artifact framework.

## Compressed responsibility

The compressed responsibility is:

```text
bounded inquiry-orientation profile composition
```

More specifically, `_compose_inquiry_orientation_answer(...)` currently owns all of the following in one place:

1. requesting local evidence through `_collect_inquiry_orientation_evidence(...)`;
2. selecting the bounded answer material from `evidence.related_material`;
3. preserving support strings for the selected material;
4. assigning the reason for the bounded composition;
5. attaching the authority boundary;
6. attaching limitations/Unknowns based on whether related material exists;
7. returning the implementation-local profile artifact consumed by `build_inquiry_orientation(...)`.

This is compressed but not incorrect. Existing implementation already separates request preparation, evidence collection, answer composition, view construction, and rendering. The remaining compression is local to answer-profile construction: evidence consumption, support preservation, boundary attachment, limitation selection, and artifact construction are adjacent in a single producer.

## Compatibility boundary

A behavior-preserving slice, if later performed, would need to preserve all current compatibility boundaries:

- no public CLI behavior change;
- no JSON or text output change;
- no event-ledger write change;
- no cluster mutation;
- no projection into runtime state;
- no new diagnostic, audit, probe, CLI flag, or recordable output;
- no change to `--record-inquiry-note` storage behavior;
- no change to `--inquiry-orientation` rendering behavior;
- no semantic promotion of inquiry note prose;
- no new universal artifact/profile framework;
- no change to deterministic lexical-overlap matching;
- no change to the negative authority boundary;
- no change to uncertainty text for matches or no matches.

The existing tests already protect the most important boundary facts: raw inquiry note/provenance preservation, non-projection into runtime state, no state mutation/action creation, required orientation output sections, support rendering, uncertainty rendering, authority-boundary rendering, and composition/request/evidence/answer separation.

## Required questions

### 1. Does an implementation-local manifestation exist?

Yes.

Implementation evidence shows the recurring shape:

```text
_compose_inquiry_orientation_answer(...)
→ _InquiryOrientationAnswer
→ build_inquiry_orientation(...)
```

The profile is bounded to inquiry orientation and contains answer material, support, reason, authority boundary, and limitations.

### 2. What responsibility is compressed?

The compressed responsibility is bounded inquiry-orientation profile composition: converting collected related-material evidence into an implementation-local answer profile that carries support, reason, authority boundary, and limitations before view construction.

### 3. What exact producer currently constructs or preserves the profile?

```text
_compose_inquiry_orientation_answer(state, request)
```

### 4. What artifact carries it?

```text
_InquiryOrientationAnswer
```

### 5. What exact consumer consumes it?

```text
build_inquiry_orientation(state, note)
```

`format_inquiry_orientation(view)` is the downstream presentation consumer of the view produced from the artifact, not the direct consumer of `_InquiryOrientationAnswer`.

### 6. Is the boundary ready for one behavior-preserving implementation slice?

```text
Ready for implementation slice
```

Reason: the producer, artifact, and consumer are exact, implementation-local, covered by tests, and adjacent to an already separated request/evidence/view/rendering path. A future slice could recover one narrow helper around answer-profile artifact construction without changing behavior, output, schema, diagnostics, event ledger behavior, mutation behavior, or authority semantics.

## Preserved Unknowns

- Whether another equally narrow producer/profile/consumer manifestation exists in warrant, reliance, diagnostic, answer-composition, or typed-unknown neighborhoods was not exhaustively searched after the inquiry-orientation manifestation was found.
- Whether the best future implementation slice should extract support preservation, limitation selection, boundary attachment, or final artifact construction is not decided here.
- Whether any downstream user depends on private helper names is unknown; the compatibility boundary therefore assumes no public behavior or output changes and no avoidable private churn.
- Whether `_InquiryOrientationAnswer.reason` needs direct rendering in a future surface is unknown; current rendering does not expose it as an independent output field.
- Whether confidence should ever become an explicit field in this local artifact is unknown and not recommended here; current confidence limit is encoded as deterministic lexical-overlap/uncertainty/authority-boundary text.

## Confidence

Confidence: high.

Basis:

- The producer, artifact, and consumer are concrete implementation symbols.
- Existing tests assert the handoff and field boundaries directly.
- The app surfaces confirm adjacent inquiry-artifact and diagnostic boundaries are read-only and non-mutating.
- The classification does not depend on constitutional prose alone; it follows implementation evidence in `seed_runtime/inquiry_orientation.py`, `tests/test_inquiry_orientation.py`, `seed_runtime/inquiry_artifacts.py`, `seed_runtime/typed_unknowns.py`, and `scripts/seed_local.py`.

Implementation pressure audit complete.
