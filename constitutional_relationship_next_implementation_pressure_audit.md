# Constitutional Relationship Next Implementation Pressure Audit

## Scope

This is exactly one bounded Implementation Neighborhood Transition Audit. It begins from the completed Inquiry Orientation implementation family and inspects only adjacent implementation surfaces that are already connected by repository code or by neighboring inquiry-answer composition behavior.

No implementation recovery is performed here.

## Inspected neighborhoods

### Completed starting family: Inquiry Orientation

Implementation evidence shows the completed family now has a narrow terminal orchestration body. `build_inquiry_orientation(...)` prepares a composition request, composes the answer, and maps the answer into `InquiryOrientationView`. `_compose_inquiry_orientation_answer(...)` only collects evidence, prepares selected material, and prepares the final answer artifact. The remaining body is orchestration rather than a newly exposed implementation-local producer or consumer.

Evidence inspected:

- `_InquiryOrientationCompositionRequest`, `_InquiryOrientationEvidence`, `_InquiryOrientationSelectedMaterial`, and `_InquiryOrientationAnswer` are explicit implementation-local handoffs and artifacts.
- `_compose_inquiry_orientation_answer(...)` delegates evidence collection, selected-material preparation, and answer preparation.
- `_prepare_inquiry_orientation_answer(...)` delegates reason, boundary, and limitations selection to local selectors.

Pressure observed: low. The repository evidence supports the prior completion result: the remaining body is lawful terminal orchestration.

### Inquiry Artifact composition

Implementation evidence shows a small visibility surface for repository-visible inquiry artifacts. It has a public `InquiryArtifactVisibility` artifact, two implementation-local payloads, and `_artifact_visibility_from_payloads(...)` for preserving public shape after local answer composition.

Evidence inspected:

- `_InquiryArtifactEvidencePayload` and `_InquiryArtifactLimitationsPayload` exist as implementation-local supporting evidence and limitations payloads.
- `_artifact_visibility_from_payloads(...)` consumes those payloads and emits `InquiryArtifactVisibility`.
- The `BOUNDARY` explicitly prevents recording, event-ledger writes, cluster mutation, inquiry movement inference, inquiry graph creation, pressure transformation inference, and workflow or planning behavior.
- The `ARTIFACTS` tuple still contains mixed construction styles: some entries use `_artifact_visibility_from_payloads(...)`, while others directly instantiate `InquiryArtifactVisibility` with evidence and limitations.

Pressure observed: medium-low. There is local composition asymmetry, but the surface is static, bounded, and not strongly connected to the completed Inquiry Orientation answer path beyond neighboring artifact vocabulary.

### Selection Path

Implementation evidence shows a read-only selection audit with many implementation-local payloads already exposed: result, reason, supporting evidence, candidate set, non-selected candidates, selection factors, unknowns, lineage, inputs, and payload bundle. The public `SelectionPathAudit` already has a boundary that prevents fact recording, event-ledger writes, and cluster mutation.

Evidence inspected:

- `build_selection_path_audit(...)` normalizes target input, collects local inputs, selects among focus, pressure category, or unsupported target handling, and returns a public audit.
- `_selection_path_inputs(...)` is already a local input-collection helper that consumes pressure audit and operational story.
- Unsupported-target handling is already decomposed through `_unsupported_target_selection(...)`, `_unsupported_target_lineage_payload(...)`, `_unsupported_target_result_payload(...)`, `_unsupported_target_reason_payload(...)`, supporting evidence, factors, non-selected payload, and unknown payload helpers.
- Pressure-selection handling is also substantially decomposed into result, reason, support, lineage, candidate rows, non-selected rows, selected evidence, and selected-name helpers.

Pressure observed: medium. Selection Path remains implementation-adjacent because it consumes pressure audit and operational story evidence to explain why a candidate is selected. However, the observed implementation pressure is already broadly decompressed inside this neighborhood.

### Reasoning Path

Implementation evidence shows a read-only derivation audit adjacent to inquiry-answer composition. It builds a public `ReasoningPathAudit` from evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and boundary. It also defines implementation-local artifacts for derived conclusions, supporting evidence, and derivation lineage.

Evidence inspected:

- `_DerivedConclusionPayload`, `_DerivationSupportingEvidencePayload`, and `_DerivationLineagePayload` already expose an implementation-local answer/lineage shape.
- `build_reasoning_path_audit(...)` directly collects from ownership discrepancies, capability needs, pressure audit, privilege discovery, and operational story.
- The same function directly constructs evidence rows, intermediate conclusions, derived conclusions, consumers, story impact, and unknown preservation before handing the result to `_reasoning_path_from_payloads(...)`.
- `_reasoning_path_from_payloads(...)` is the public compatibility handoff that consumes the compressed payload objects and returns `ReasoningPathAudit`.
- `format_reasoning_path_audit(...)` renders the resulting public artifact.

Pressure observed: high. Unlike the completed Inquiry Orientation family, the remaining implementation body is not merely terminal orchestration. The implementation evidence already exposes candidate artifacts and a consumer, while one producer-sized body still collects evidence, derives intermediate and derived conclusions, preserves consumers, tracks story impact, and preserves typed Unknowns.

### Question Surface Inventory

Implementation evidence shows bounded ask and inventory surfaces adjacent to inquiry answering. The inventory has exact lookup, eligibility input preparation, bounded eligibility, refusal, surface-argument validation, selected surface value, selected dispatch surface, presentation handoff, dispatch request, dispatch result, namespace update, post-dispatch handling, and message clearing.

Evidence inspected:

- `_lookup_exact_question_family(...)` admits only exact inventory-backed question families.
- `_prepare_question_family_eligibility_input(...)` explicitly refuses to own classification, selection, rendering, argument validation, or mutation.
- Bounded work selection and dispatch artifacts already separate eligibility, surface args, selected dispatch surface, selected surface value, dispatch request, dispatch result, presentation handoff, and post-dispatch compatibility handling.

Pressure observed: medium-low. The implementation is adjacent but already extensively boundary-labeled. The evidence does not show stronger remaining pressure than Reasoning Path.

### Operational Story

Implementation evidence shows a broad read-only story surface that composes pressure, capability, privilege, correlation, impact, investigation path, unknowns, and boundary into `OperationalStory`.

Evidence inspected:

- `_OperationalStoryAnswerPayload`, `_OperationalStoryLimitationsPayload`, `_OperationalStoryReasoningPayload`, `_OperationalStorySupportingEvidencePayload`, and `_OperationalStoryBoundaryPayload` already split answer, limitations, reasoning, support, and authority boundary.
- `build_operational_story(...)` collects upstream visibility surfaces, selects primary pressure, builds an investigation path, calls `_compose_operational_story_payloads(...)`, and maps payloads into the public story object.
- `_compose_operational_story_payloads(...)` still creates all story payload families together, but the public and implementation-local payload boundaries are explicit.

Pressure observed: medium. Operational Story is adjacent and broad, but its pressure appears less immediate for the post-Inquiry-Orientation transition because the answer/support/reason/boundary/limitations split is already explicit and the compression is surface-wide composition rather than a clearly exposed next local producer.

## Strongest adjacent pressure

**Reasoning Path** has the strongest remaining adjacent implementation pressure.

The reason is implementation evidence, not architectural preference:

1. It is directly adjacent to answer composition surfaces because it produces a rendered answer-like audit with evidence, conclusions, consumers, story impact, Unknowns, and an authority boundary.
2. It already exposes implementation-local artifacts that look like recovered boundaries: `_DerivedConclusionPayload`, `_DerivationSupportingEvidencePayload`, and `_DerivationLineagePayload`.
3. Its main builder still performs several separable responsibilities in one producer-sized body before handing payloads to `_reasoning_path_from_payloads(...)`.
4. The public consumer and renderer already exist, so the neighborhood is not blocked on conceptual visibility.

## Recurring compressed responsibility observed

The recurring compressed responsibility is:

> Collecting implementation evidence from multiple upstream surfaces, deriving conclusion rows, preserving lineage/consumer material, preserving limitations as typed Unknowns, and mapping all of that into a public read-only answer artifact inside one builder body.

This pattern appears most strongly in `build_reasoning_path_audit(...)`.

It appears more weakly in Operational Story composition and Inquiry Artifact static row construction, but those neighborhoods either already expose broader payload splits or lack the same direct producer-artifact-consumer pressure.

## Candidate producer

**Candidate producer:** `build_reasoning_path_audit(...)`, specifically the body that gathers upstream surfaces and constructs evidence, intermediate conclusions, derived conclusions, consumers, story impact, and unknowns before the compatibility handoff.

This is only a candidate for a future implementation recovery campaign. This audit does not recover it.

## Candidate artifact/helper

**Candidate artifact/helper:** the already exposed implementation-local payload family:

- `_DerivedConclusionPayload`
- `_DerivationSupportingEvidencePayload`
- `_DerivationLineagePayload`

These artifacts prove that the implementation already recognizes a local shape separating conclusions, support, and lineage/limitations.

## Candidate consumer

**Candidate consumer:** `_reasoning_path_from_payloads(...)`, with `ReasoningPathAudit` and `format_reasoning_path_audit(...)` as downstream public artifact and renderer.

The consumer already exists; the pressure is upstream of it, in the builder body that produces the payloads.

## Required-question answers

1. **Which adjacent implementation neighborhoods were inspected?**
   - Inquiry Orientation terminal orchestration.
   - Inquiry Artifact composition.
   - Selection Path.
   - Reasoning Path.
   - Question Surface Inventory / bounded ask handoff surfaces.
   - Operational Story.

2. **Which neighborhood has the strongest remaining implementation pressure?**
   - Reasoning Path.

3. **What recurring compressed responsibility was observed?**
   - Multi-surface evidence collection, conclusion derivation, lineage/consumer preservation, Unknown preservation, and public read-only answer mapping compressed inside a builder body.

4. **Does implementation evidence already expose a recoverable producer, artifact, or consumer?**
   - Yes.
   - Producer candidate: `build_reasoning_path_audit(...)`.
   - Artifact/helper candidates: `_DerivedConclusionPayload`, `_DerivationSupportingEvidencePayload`, `_DerivationLineagePayload`.
   - Consumer candidate: `_reasoning_path_from_payloads(...)`, with public `ReasoningPathAudit` and formatter downstream.

5. **Is the neighborhood ready for an implementation recovery campaign?**
   - Ready for implementation recovery.

## Readiness classification

```text
Ready for implementation recovery
```

## Preserved Unknowns

- Unknown whether the strongest future slice would begin with evidence collection, derived-conclusion production, consumer/story-impact lineage, or typed Unknown preservation. This audit identifies neighborhood pressure only.
- Unknown whether all Reasoning Path compression is harmful or merely terminal orchestration; only implementation-local pressure is observed here.
- Unknown whether Operational Story will become stronger after a Reasoning Path campaign; this audit does not rank beyond the single next adjacent pressure.
- Unknown whether Inquiry Artifact static construction asymmetry is intentional; its pressure is weaker than Reasoning Path in this bounded pass.

## Confidence

Medium-high.

Confidence is high that Inquiry Orientation itself is complete for this campaign and that Reasoning Path has the strongest adjacent implementation pressure among inspected neighborhoods. Confidence is medium rather than absolute because the audit intentionally avoids expanding beyond immediately adjacent implementation surfaces and does not perform implementation recovery.

Implementation neighborhood transition audit complete.
