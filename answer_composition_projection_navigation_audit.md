# Answer Composition Projection Navigation Audit

## Purpose

This audit determines where the Answer Composition responsibility family should continue after the local completion of `SelectionPathAudit` answer-composition projection. It is a navigation audit only: no runtime, schema, CLI, renderer, or behavior change is proposed.

Repository authority is implementation evidence. The reviewed evidence is the current implementation of the remaining inquiry surfaces plus the prior Answer Composition slice and completion reports.

## Executive answer

The strongest next implementation-backed Answer Composition projection opportunity is **`ReasoningPathAudit`**.

`ReasoningPathAudit` is **Partially Projected**: it already separates derived conclusion material from derivation-lineage material through `_DerivedConclusionPayload` and `_DerivationLineagePayload`, but answer-composition grammar remains compressed because `evidence`, `consumers`, `story_impact`, and `unknowns` are still bundled into one lineage payload and the public audit handoff has no separate support, boundary, or limitation payloads.

The recommended next slice is therefore a bounded `ReasoningPathAudit` slice that separates **derived conclusions / reason material** from **supporting evidence**, **consumer/story-impact lineage**, and **limitations**, while preserving public compatibility.

`SelectionPathAudit` should not continue under Answer Composition. Its remaining work is selection lineage and selection algorithm explanation, not answer composition.

## Reviewed inquiry surfaces

| Inquiry surface | State | Local Answer Composition maturity | Recommended next projection | Confidence |
|---|---|---:|---|---:|
| `OperationalStory` | Locally Complete | High | None; stop unless new evidence appears | High |
| `InquiryOrientationView` | Locally Complete | High | None; stop unless new evidence appears | High |
| `SelectionPathAudit` | Locally Complete | High | None under Answer Composition; remaining work belongs to Selection Path | High |
| `InquiryArtifactVisibility` | Partially Projected | Medium | Not strongest next; possible later evidence/limitation compatibility cleanup | Medium |
| `ReasoningPathAudit` | Partially Projected | Medium | Strongest next projection: separate support, lineage/impact, limitations, and boundary around derivation answer | High |
| `OperationalStory` renderer / formatters | Not an Answer Composition Owner | N/A | None; rendering-only | High |

## Surface findings

### 1. `OperationalStory`

**State:** Locally Complete.

**Already projected grammar:**

`OperationalStory` has the full recovered answer-composition grammar in implementation-local payloads:

- bounded answer material: `_OperationalStoryAnswerPayload`;
- reasoning material: `_OperationalStoryReasoningPayload`;
- supporting evidence: `_OperationalStorySupportingEvidencePayload`;
- authority boundary: `_OperationalStoryBoundaryPayload`;
- limitations / unknowns: `_OperationalStoryLimitationsPayload`.

The builder composes those payloads first and only then hands their fields into the unchanged public `OperationalStory` compatibility object.

**Remaining compressed ownership:**

No local Answer Composition compression remains. Remaining concerns are operational-audit input quality, pressure/capability/privilege/correlation/impact implementations, or rendering; those are not Answer Composition ownership.

**Implementation evidence:**

- The public object carries focus, pressure, supporting evidence, capabilities, constraints, correlation gaps, impact, recent changes, observed outcomes, investigation path, unknowns, and boundary.
- The private payload classes separate answer, limitations, reasoning, supporting evidence, and boundary.
- `_compose_operational_story_payloads(...)` explicitly returns the five separated payloads.
- `build_operational_story(...)` performs compatibility handoff from those payloads into `OperationalStory`.

**Supported next projection:** None.

**Unsupported projections:**

- Do not split rendering from answer composition; rendering is already downstream.
- Do not introduce a generic answer-composition framework.
- Do not migrate operational vocabulary into repository knowledge.

**Confidence:** High.

### 2. `InquiryOrientationView`

**State:** Locally Complete.

**Already projected grammar:**

`InquiryOrientationView` has implementation-local orientation evidence and an implementation-local answer object. `_ArchitecturalOrientationEvidence` collects related material before answer composition. `_ArchitecturalOrientationAnswer` separates answer material, reason, support, boundary, and limitations. `build_inquiry_orientation(...)` then maps that private answer object into the public view.

**Remaining compressed ownership:**

No local Answer Composition compression remains. The remaining implementation concerns are lexical matching, source navigation, inquiry-note preservation, and presentation. Those are evidence collection, inquiry navigation, or rendering concerns rather than Answer Composition.

**Implementation evidence:**

- The public view contains the note, related material, uncertainty, and authority boundary.
- `_ArchitecturalOrientationEvidence` isolates collected repository evidence.
- `_ArchitecturalOrientationAnswer` names answer, reason, support, boundary, and limitations.
- `_compose_architectural_orientation_answer(...)` consumes collected evidence and produces the answer object.
- The formatter only renders the view sections.

**Supported next projection:** None.

**Unsupported projections:**

- Do not promote lexical overlap into semantic intent or next-action routing.
- Do not migrate presentation vocabulary into preserved repository knowledge.
- Do not treat inquiry navigation or source-navigation matching as Answer Composition.

**Confidence:** High.

### 3. `SelectionPathAudit`

**State:** Locally Complete.

**Already projected grammar:**

`SelectionPathAudit` now separates:

- selected answer: `_SelectionResultPayload`;
- reason/outcome: `_SelectionReasonPayload`;
- supporting evidence: `_SelectionSupportingEvidencePayload`;
- selection lineage: `_SelectionLineagePayload`.

The compatibility handoff copies those separated payloads into the public `SelectionPathAudit` object.

**Remaining compressed ownership:**

The remaining compression is selection-path ownership, not Answer Composition. Candidate ordering, non-selected candidate reasoning, factor derivation, and unknown target handling are selection algorithm explanation and lineage concerns.

**Implementation evidence:**

- `_SelectionResultPayload`, `_SelectionReasonPayload`, `_SelectionSupportingEvidencePayload`, and `_SelectionLineagePayload` are distinct implementation-local payloads.
- `_selection_path_from_payloads(...)` maps selected, outcome, evidence, candidates, selection factors, non-selected candidates, and unknowns into the public audit object.
- The completion audit explicitly states that SelectionPathAudit reached a natural Answer Composition stopping point and that further work belongs to Selection Path ownership.

**Supported next projection:** None under Answer Composition.

**Unsupported projections:**

- Do not continue slicing `SelectionPathAudit` by momentum.
- Do not classify candidate ordering or non-selected candidate reasoning as Answer Composition.
- Do not alter CLI, JSON, rendering, schema, or selection behavior.

**Confidence:** High.

### 4. `InquiryArtifactVisibility`

**State:** Partially Projected.

**Already projected grammar:**

`InquiryArtifactVisibility` has a public record with artifact, classification, evidence, and limitations. Some records are constructed through `_InquiryArtifactEvidencePayload`, `_InquiryArtifactLimitationsPayload`, and `_artifact_visibility_from_payloads(...)`, separating support from limitations before the compatibility object.

**Remaining compressed ownership:**

The surface remains inconsistent: some artifact rows use the private payload handoff, while later rows instantiate `InquiryArtifactVisibility` directly. Classification remains adjacent to evidence and limitations rather than being represented as a separate answer/result payload. This is answer-like, but the surface is primarily an artifact visibility registry; much of its remaining work is classification/evaluation of repository visibility, not bounded answer composition.

**Implementation evidence:**

- The public dataclass carries artifact, classification, evidence, and limitations.
- `_InquiryArtifactEvidencePayload` and `_InquiryArtifactLimitationsPayload` exist.
- `_artifact_visibility_from_payloads(...)` preserves the public shape after local answer composition.
- Only the first artifact rows use the payload handoff; subsequent rows instantiate `InquiryArtifactVisibility` directly.
- The boundary explicitly denies recording, ledger writes, cluster mutation, inquiry graph creation, pressure transformation inference, and workflow/planning behavior.

**Supported next projection:** Possible later cleanup if repository evidence shows artifact visibility answer composition should be made uniform. A bounded slice could separate classification/result from supporting evidence and limitations for all rows without changing public output.

**Unsupported projections:**

- Do not turn artifact classification into a generalized inquiry-artifact model.
- Do not infer inquiry movement, workflow, planning, or pressure transformation from these rows.
- Do not prioritize this over `ReasoningPathAudit`; the stronger compression in this surface is classification/evaluation, not Answer Composition.

**Confidence:** Medium.

### 5. `ReasoningPathAudit`

**State:** Partially Projected.

**Already projected grammar:**

`ReasoningPathAudit` already has two implementation-local payloads:

- `_DerivedConclusionPayload`, which separates intermediate and derived conclusions from lineage;
- `_DerivationLineagePayload`, which carries evidence, consumers, story impact, and unknowns.

This shows prior projection pressure: conclusion material has been separated from derivation-lineage material before public compatibility handoff.

**Remaining compressed ownership:**

This is the next strongest Answer Composition opportunity. `_DerivationLineagePayload` still bundles several distinct answer-composition roles:

- supporting evidence for conclusions;
- consumers / downstream surfaces;
- operational-story impact;
- unknowns / limitations.

The public `ReasoningPathAudit` also has a boundary field, but there is no implementation-local boundary payload analogous to the completed `OperationalStory` grammar. The result is a partially projected derivation answer where conclusion material is separate, but support, lineage, impact, limitations, and boundary are still compressed around the audit handoff.

**Implementation evidence:**

- The public audit carries domain, subject, evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and a read-only boundary.
- The builder derives evidence and conclusions from implemented diagnostic surfaces: ownership discrepancies, capability needs, pressure audit, privilege discovery, and operational story.
- `_DerivedConclusionPayload` separates conclusion material.
- `_DerivationLineagePayload` still owns evidence, consumers, story impact, and unknowns together.
- `_reasoning_path_from_payloads(...)` maps conclusion payload and lineage payload directly into the public object.
- The formatter renders evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and boundary, but does not own derivation construction.

**Supported next projection:**

A bounded `ReasoningPathAudit` Answer Composition slice. The smallest implementation-backed slice should preserve public compatibility while separating one compressed role from `_DerivationLineagePayload`. The best first cut is:

```text
_DerivationSupportingEvidencePayload
```

separating `evidence` from consumers/story impact/unknowns. A follow-up, if still supported, could separate limitations (`unknowns`) or boundary. This mirrors the completed movement in `OperationalStory` and `SelectionPathAudit` without changing behavior.

**Unsupported projections:**

- Do not make a reasoning-engine framework.
- Do not change derivation algorithms, diagnostic inputs, CLI, JSON, or renderer behavior.
- Do not classify consumer paths or operational-story impact as answer material; they may be lineage/impact ownership.
- Do not treat all reasoning work as Answer Composition. Only the compatibility handoff around conclusion/support/limitation/boundary is in scope.

**Confidence:** High.

## Cross-surface counterexamples

The following implementation evidence prevents over-claiming Answer Composition ownership:

1. **Selection-path residual work is selection lineage.** Candidate sets, selection factors, non-selected alternatives, unknown targets, and ordering explanations are selection-path or algorithm explanation concerns.
2. **Inquiry orientation residual work is inquiry navigation / evidence collection.** Tokenization, lexical overlap, source navigation, and fact-support matching do not belong to Answer Composition once the answer/support/boundary/limitations object is separated.
3. **Operational story residual work is upstream operational visibility.** Pressure, capability, privilege, correlation, impact, and investigation path builders own their own evidence production.
4. **Inquiry artifact residual work is classification/evaluation.** The artifact surface classifies repository visibility and explicitly refuses inquiry graph creation, pressure transformation inference, workflow, and planning.
5. **Formatters are not Answer Composition owners.** The reviewed formatters render already-built view or audit objects.

## Recommended next slice

Proceed next with **`ReasoningPathAudit` supporting-evidence projection**.

Bounded slice shape:

```text
_DerivationSupportingEvidencePayload
```

Targeted effect:

- move `evidence` out of `_DerivationLineagePayload`;
- keep `consumers`, `story_impact`, and `unknowns` in lineage/remaining payloads unless implementation evidence supports further split;
- keep public `ReasoningPathAudit` JSON and text output unchanged;
- add or update tests proving the separated payload is used in the compatibility handoff;
- do not change derivation logic, rendering, CLI, schema, event ledger behavior, or cluster state.

This is the strongest implementation-backed continuation because it follows the observed local grammar without extending Answer Composition into selection algorithm explanation, inquiry navigation, artifact classification, or rendering.

## Architectural stopping points already reached

- `OperationalStory` has reached local completion for answer, reason, support, boundary, and limitations.
- `InquiryOrientationView` has reached local completion for orientation answer material, reason/support, boundary, and limitations after separating evidence collection.
- `SelectionPathAudit` has reached local Answer Composition completion; remaining work is Selection Path ownership.

## Final navigation answer

Answer Composition should continue next in **`ReasoningPathAudit`**, not `SelectionPathAudit`.

`ReasoningPathAudit` contains the strongest implementation-backed compressed Answer Composition ownership because conclusion material has already been separated, while supporting evidence, consumers, story impact, unknowns, and boundary remain compressed around the derivation-audit compatibility handoff. The next projection should start by separating supporting evidence from derivation lineage and preserve all public behavior.
