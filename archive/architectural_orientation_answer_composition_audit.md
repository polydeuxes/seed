# Architectural Orientation Answer Composition Audit

## Scope

This is a bounded implementation audit. It does not implement a runtime surface, CLI, renderer, metadata registry, status registry, planner, active-edge tracker, or manual architectural explanation text.

The question is whether Seed already contains sufficient implementation evidence to answer:

```text
Why do I believe
this is the current
architectural orientation?
```

Repository authority wins. This audit treats implementation files, tests, implementation-backed slice reports, and prior implementation audits as evidence. It does not treat operator intuition, conversation memory, architectural preference, or unsupported vocabulary as authority.

## Short answer

Yes, but only as an implementation-backed composition opportunity, not as an already implemented architectural-orientation runtime surface.

Seed already has enough repository evidence to support an architectural orientation inquiry shaped as:

```text
answer
reason
support
boundary
limitations
```

for the currently audited responsibility-family orientation fields:

```text
active responsibility family
current boundary
implemented boundaries
remaining compressed boundaries
natural stopping point
confidence
recommended next inquiry
```

The evidence is sufficient because existing answer-responsible surfaces already use the same discipline: they return a bounded conclusion with supporting evidence, unknowns or limitations, and authority boundaries. The architectural-orientation-specific evidence exists in implementation-backed responsibility-family slices and audits. What is missing is not new architectural recovery. What is missing is an implementation that composes those existing artifacts into a stable answer surface.

Therefore architectural orientation naturally becomes another inquiry answer rather than a special subsystem. The next implementation work should be answer composition, not orientation rendering. Rendering before composition would only display manually reconstructed reasoning and would preserve the current dependence on operator interpretation.

## Evidence reviewed

This audit reviewed:

- `architectural_inquiry_orientation_surface_audit.md`.
- `responsibility_family_completion_inquiry_audit.md`.
- `inquiry_lineage_architectural_projection_slice_methodology.md`.
- `operational_responsibility_slice_001.md` through `operational_responsibility_slice_006.md`.
- `execution_visibility_slice_001.md` through `execution_visibility_slice_005.md`.
- `observation_derived_capability_slice_001.md` through `observation_derived_capability_slice_005.md`.
- `seed_runtime/inquiry_orientation.py` and `tests/test_inquiry_orientation.py`.
- `seed_runtime/inquiry_artifacts.py` and `tests/test_inquiry_artifacts.py`.
- `seed_runtime/operational_story.py` and `tests/test_operational_story.py`.
- `seed_runtime/reasoning_path_audit.py` and `tests/test_reasoning_path_audit.py`.
- `seed_runtime/selection_path_audit.py` and `tests/test_selection_path_audit.py`.
- `seed_runtime/reference_selection.py` and `tests/test_reference_selection.py`.
- `docs/bounded_answer_responsibility_investigation.md`.
- `docs/answer_attached_reasoning_investigation.md`.
- `docs/answer_support_relationships_investigation.md`.
- `docs/inquiry_presentation_answer_implementation_audit.md`.

## Repository answer-composition pattern

The repository already supports the general answer-composition pattern needed by architectural orientation.

### Existing implemented examples

- `seed_runtime/inquiry_orientation.py` composes a read-only orientation view for preserved inquiry prose. It selects deterministic lexical overlap against projected fact supports and source-navigation matches, returns related material, support, uncertainty, and an authority boundary. Its boundary explicitly prevents inquiry prose and matches from becoming facts, goals, requirements, commands, plans, operator intent, recommended actions, or next safe moves.
- `seed_runtime/operational_story.py` composes current operational focus from existing visibility surfaces. Its dataclass carries focus, pressure, supporting evidence, capabilities, constraints, correlation gaps, impact, recent changes, observed outcomes, investigation path, unknowns, and a read-only/no-mutation boundary.
- `seed_runtime/inquiry_artifacts.py` classifies inquiry artifacts with evidence and limitations while preserving a read-only boundary that forbids recording, event-ledger writes, cluster mutation, inquiry-graph creation, pressure-transformation inference, workflow behavior, and planning behavior.
- The answer-responsibility investigations conclude that answer composition is not merely rendering. It must select, aggregate, derive, or organize existing authorities into a bounded answer while exposing why the authorities are relevant and what remains outside authority.

### Consequence for architectural orientation

Architectural orientation does not need a special architectural subsystem if it follows the existing pattern:

```text
bounded orientation answer
  + reason for the answer
  + supporting implementation evidence
  + authority boundary
  + limitations / unsupported conclusions
```

The repository evidence supports that shape. It does not support a renderer-only implementation, because a renderer would not determine which family, boundary, support, confidence, or next inquiry is justified.

## Field-by-field audit

### 1. Active responsibility family

#### Answer

Seed can justify the active architectural orientation only for responsibility families already expressed by implementation-backed slice lineages:

```text
Operational Responsibility
Execution Visibility
Observation-Derived Capability
```

#### Reason

Those families recur as ordered implementation-slice sequences and are summarized as bounded recovered chains by the family completion audit. Family identity is therefore repository-derived, not manually chosen during this audit.

#### Supporting implementation evidence

- The architectural orientation audit says the strongest evidence identifies those three completed or bounded families.
- The responsibility-family completion audit lists implemented boundaries, remaining compressed boundaries, completed slice counts, natural termination points, and confidence for each of those families.
- The lineage methodology defines the recurring slice method as recovering one boundary, making one implementation change, preserving behavior, and stopping.

#### Boundary

This supports orientation inside the documented responsibility-family slice corpus only.

#### Limitations

Seed cannot infer an arbitrary operator's active family from conversation memory, prose preference, or a newly coined vocabulary term. A family label is unsupported unless it is backed by repeated slice lineage or equivalent implementation evidence.

### 2. Current boundary

#### Answer

Seed can justify the current boundary for each known family as the latest implementation-backed boundary in that family:

- Operational Responsibility: `Execution Recording != Post-Execution Knowledge Extraction`.
- Execution Visibility: `State Build Visibility != Projection Cache Diagnostics`.
- Observation-Derived Capability: `Capability Inventory != Executable Operation Contract`.

#### Reason

The latest slice in each family names a selected boundary and records before/after responsibility separation, implementation evidence, files changed, compatibility preservation, tests, and remaining compression.

#### Supporting implementation evidence

- The architectural orientation audit names these three terminal/current boundaries.
- The family completion audit identifies the same natural termination points for the three recovered chains.
- The individual latest slices preserve implementation-backed evidence for the named boundaries rather than only naming them in prose.

#### Boundary

The answer is valid for a known slice family. It is not a universal current-work-position detector.

#### Limitations

Boundary vocabulary alone is not enough. A phrase such as `current boundary` or `active edge` is not repository knowledge unless implementation evidence ties it to a recovered slice.

### 3. Implemented boundaries

#### Answer

Seed can justify implemented boundaries as the ordered boundary chains listed in the family completion audit.

Operational Responsibility:

```text
Capability Recommendation != Operation Selection
Operation Selection != Registered Operation Validation
Registered Operation Validation != Policy Authorization
Policy Authorization != Execution Realization
Execution Realization != Execution Recording
Execution Recording != Post-Execution Knowledge Extraction
```

Execution Visibility:

```text
Status Emission != Status Consumption
Execution Status != Execution Timing
Execution Timing != Cache Visibility
Execution Visibility != Execution Diagnostics
State Build Visibility != Projection Cache Diagnostics
```

Observation-Derived Capability:

```text
Observed Evidence != Executable Operation Contract
Observed Evidence != Capability Verification
Capability Verification != Capability Promotion
Capability Promotion != Capability Inventory
Capability Inventory != Executable Operation Contract
```

#### Reason

Each boundary is represented by a compatibility-preserving slice report and supporting implementation/test evidence. The family completion audit derives completion from that recurring implementation evidence, not from a status registry.

#### Supporting implementation evidence

- The family completion audit lists implementation evidence for each family, including registry/tool validation/policy/execution/extraction separation, execution status/timing/cache/diagnostic separation, and capability evidence/verification/promotion/inventory/contract separation.
- The architectural orientation audit says implemented boundaries can be derived from family completion and individual slice reports without a completion registry.

#### Boundary

This supports the recovered boundary chains. It does not assert all possible architectural boundaries in those domains are implemented.

#### Limitations

Investigation prose alone can name a candidate boundary without proving it implemented. Implemented-boundary status requires slice-backed implementation evidence and preservation tests or generated architecture evidence.

### 4. Remaining compressed boundaries

#### Answer

Seed can justify remaining compressed boundaries from the latest slice reports and family completion audit.

Examples include:

- Pending-action creation vs. policy denial routing.
- Approved pending-action resumption vs. fresh call authorization.
- Projection build diagnostics passing replay/build evidence through cache-building paths.
- Fact-index cache lookup/load timing adjacent to cache-status reporting.
- Capability inventory presenting a compatibility union of registered operation contract labels, requested capabilities, and admitted verification fact subjects.
- Registered operation contract derivation still represented by `ToolSpec` capability metadata rather than a public contract-derivation API.

#### Reason

The remaining-compression lists are counterexamples discovered while implementing bounded slices. They are not a manually curated backlog.

#### Supporting implementation evidence

- The architectural orientation audit identifies remaining compressed boundaries as repository-visible in latest slice reports.
- The family completion audit preserves remaining compression separately for Operational Responsibility, Execution Visibility, and Observation-Derived Capability.

#### Boundary

Remaining compression can be used as evidence for adjacent or future inquiry candidates, not as proof that a manual queue or planner exists.

#### Limitations

Seed cannot rank these items by urgency, operator preference, or next safe move from the existing architectural-orientation evidence. It can only identify that they remain implementation-backed compression.

### 5. Natural stopping point

#### Answer

Seed can justify a natural stopping point for each recovered chain:

- Operational Responsibility naturally stops after `Execution Recording != Post-Execution Knowledge Extraction`.
- Execution Visibility naturally stops after `State Build Visibility != Projection Cache Diagnostics`.
- Observation-Derived Capability naturally stops after `Capability Inventory != Executable Operation Contract`.

#### Reason

A chain naturally stops when every recovered boundary in that chain has implementation-backed slices and further work would require a new recovered boundary or adjacent family rather than continuing the same bounded projection.

#### Supporting implementation evidence

- The responsibility-family completion audit defines natural termination as the point where further work in the same family would require recovering new boundaries.
- The architectural orientation audit repeats that natural stopping point is a derived conclusion, not a stored completion flag.

#### Boundary

The stopping point applies to the recovered chain, not to the entire architectural domain.

#### Limitations

Natural stopping does not mean architectural exhaustion. Remaining compressed boundaries explicitly prevent that stronger conclusion.

### 6. Confidence

#### Answer

Seed can justify confidence qualitatively:

- High confidence for the named recovered chains.
- Medium confidence for broader domain labels.
- Low or unsupported confidence for presentation vocabulary not backed by implementation evidence.

#### Reason

Confidence follows the strength and scope of implementation evidence: slice-by-slice implementation, compatibility preservation, tests, generated architecture evidence where relevant, and whether remaining compression is inside or adjacent to the claimed family.

#### Supporting implementation evidence

- The family completion audit assigns high confidence to recovered chains and medium confidence to broader labels where adjacent compression remains.
- The architectural orientation audit uses the same confidence distinction and rejects operator certainty as a confidence source.

#### Boundary

Confidence is evidence-scope confidence, not probabilistic truth and not operator certainty.

#### Limitations

There is no implemented architectural-orientation confidence calculator. Today the confidence rule is document-visible and implementation-backed by prior audits, but not automatically composed by a runtime surface.

### 7. Recommended next inquiry

#### Answer

Seed can justify the next implementation work as architectural orientation answer composition, not orientation rendering.

#### Reason

The repository already has the evidence needed for the answer fields, and existing inquiry/answer surfaces prove the accepted shape: bounded answer plus reason, support, boundary, and limitations. The missing piece is composition of existing evidence into an architectural orientation answer. A renderer without composition would still depend on manual reconstruction.

#### Supporting implementation evidence

- The architectural orientation audit recommended a read-only architectural inquiry orientation surface because the required fields are already present in implementation-backed artifacts.
- Existing inquiry orientation proves a safe read-only orientation surface pattern, but it only orients a preserved inquiry note to related material; it does not compose responsibility-family progression.
- Existing operational story proves multi-surface answer composition with support, unknowns, investigation path, and read-only/no-mutation boundaries.
- Existing inquiry artifact visibility proves Seed can expose inquiry artifact evidence and limitations without creating workflow, planning behavior, or an inquiry graph.

#### Boundary

The recommended next step is a read-only answer-composition implementation over existing repository evidence. It should not introduce manual state, a planner, an active-edge tracker, architectural recovery, or a status registry.

#### Limitations

This audit does not define the final API, CLI flag, renderer, schema, or extraction grammar. Those remain implementation design work. The supported conclusion is about responsibility order: compose the answer first; render it only after the answer shape exists.

## Counterexample audit

### Operator intuition

No orientation field requires operator intuition if scoped to known responsibility-family slice lineages. Operator intuition would only enter if Seed tried to pick an arbitrary current family without repository evidence.

### Conversation memory

Conversation memory is not needed for the three known families, their current boundaries, implemented boundaries, remaining compression, stopping points, or confidence. It would be needed only if the orientation surface attempted to infer the user's current intent from this conversation rather than from repository evidence.

### Manual interpretation

Manual interpretation is still required today to assemble the answer across documents. That is the main missing implementation evidence: no runtime surface currently composes the architectural-orientation answer. The required ingredients are repository-backed, but the composition is not implemented.

### Unstated reasoning

The reasoning can be stated using existing repository patterns: recovered family chain, latest slice, remaining compression, natural termination, confidence from evidence strength, and next inquiry from uncomposed answer need. An implemented composition surface should make those reasons explicit rather than relying on readers to reconstruct them.

### Implicit evidence

The evidence is currently distributed across slice reports, audits, and implementation surfaces. It is not hidden, but it is not yet normalized into an architectural-orientation answer result.

### Hidden assumptions

The strongest hidden-assumption risk is treating presentation vocabulary as repository knowledge. The current evidence avoids that by requiring slice lineage, implementation changes, tests, or existing read-only surface behavior.

## Missing implementation evidence

The repository is missing an implemented architectural-orientation answer-composition surface that:

1. Selects the bounded family corpus from repository evidence.
2. Derives active responsibility family candidates from slice lineage rather than operator memory.
3. Extracts current/latest boundary per family from implementation-backed slice reports.
4. Aggregates implemented boundaries with supporting implementation references.
5. Preserves remaining compressed boundaries as limitations and adjacent inquiry candidates.
6. Derives natural stopping point from recovered-chain closure.
7. Derives confidence from evidence strength and unresolved-compression scope.
8. Produces a stable answer structure with `answer`, `reason`, `support`, `boundary`, and `limitations`.
9. Preserves read-only/no-record/no-event-ledger/no-cluster-mutation boundaries unless a future task explicitly changes them.

The repository is not missing architectural recovery for the currently audited families. It is missing composition.

## Supported conclusions

- Seed can explain why it believes the current architectural orientation for the audited responsibility-family corpus.
- That explanation is implementation-backed when scoped to the documented slice families and prior implementation audits.
- Architectural orientation naturally fits Seed's existing answer-composition discipline: answer, reason, support, boundary, limitations.
- The next implementation work should be answer composition over existing evidence, not orientation rendering.
- A future surface should be read-only and should not create architectural truth, planner state, active-edge state, or manual status metadata.

## Unsupported conclusions

- Seed already has a dedicated runtime or CLI architectural-orientation answer surface.
- Seed can infer the operator's current architectural position from conversation memory or arbitrary prose.
- Seed can treat presentation labels such as `active edge`, `current work position`, or `orientation` as preserved knowledge without implementation evidence.
- Natural stopping point means the broader architecture domain is exhausted.
- Remaining compressed boundaries are a priority queue, status registry, or plan.
- Rendering the existing documents is sufficient to answer why Seed believes its orientation.

## Recommended next implementation step

Implement a read-only architectural-orientation answer-composition surface.

The first implementation should compose existing evidence into a stable answer object before any user-facing rendering work. The minimal answer object should preserve, for each orientation field:

```text
answer
reason
support
boundary
limitations
```

It should follow existing read-only inquiry and operational-story boundaries: no event-ledger writes, no cluster mutation, no workflow/planning behavior, no architectural recovery, and no manual status registry.

## Acceptance answers

### Can Seed explain why it believes its current architectural orientation?

Yes, when the question is scoped to the current audited responsibility-family corpus. The explanation is available from implementation-backed slice lineage, family completion evidence, architectural-orientation audit findings, and existing answer-composition patterns.

### Is that explanation already implementation-backed?

Yes for the evidence ingredients and answer discipline. No for an already implemented architectural-orientation answer-composition surface.

### Does architectural orientation naturally become another inquiry answer rather than a special subsystem?

Yes. Existing Seed surfaces already show that bounded inquiry answers carry reasons, support, boundaries, unknowns, and limitations. Architectural orientation can use the same pattern.

### Should the next implementation work be answer composition or orientation rendering?

Answer composition. Rendering should follow only after Seed has an implemented way to derive the architectural-orientation answer and its reasons from repository evidence.
