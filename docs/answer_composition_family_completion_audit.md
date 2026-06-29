# Answer Composition Family Completion Audit

## Scope

This is a bounded implementation audit of whether **Answer Composition** has enough repository evidence to be recognized as a completed responsibility family and reusable architectural layer. It does not add runtime surfaces, CLI, renderers, formatters, registries, metadata, planners, workflow behavior, or architectural recovery.

Reviewed implementation evidence:

- `seed_runtime/operational_story.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/question_surface_inventory.py`
- `answer_composition_slice_001.md`
- `answer_composition_slice_002.md`
- `answer_composition_slice_003.md`
- `answer_composition_slice_004.md`
- `architectural_orientation_answer_composition_slice_001.md`
- `docs/answer_composition_visibility_investigation.md`
- `docs/bounded_responsibility_question_ownership_investigation.md`
- `docs/reasoning_chain_visibility_investigation.md`
- `docs/context_preservation_surface_investigation.md`

## Executive conclusion

**Yes, Answer Composition has transitioned from a local implementation pattern into a reusable architectural layer, but the family is complete only for the currently projected answer-composition responsibility, not for every inquiry-oriented surface in the repository.**

Implementation evidence now shows the same responsibility separation in more than one surface:

```text
Repository Knowledge
↓
Answer Composition
  Answer
  Reason
  Supporting Evidence
  Boundary
  Limitations
↓
Compatibility Object
↓
Rendering
```

The strongest complete implementations are:

1. `operational_story`, which has implementation-local payloads for answer, reasoning, supporting evidence, boundary, and limitations before compatibility handoff to `OperationalStory`.
2. `inquiry_orientation`, where Architectural Orientation now composes an implementation-local `_ArchitecturalOrientationAnswer` with answer, reason, support, boundary, and limitations before compatibility handoff to `InquiryOrientationView`.

Several additional inquiry surfaces already compose bounded answers, but their boundaries remain compressed in public dataclasses or builder logic rather than using the full implementation-local five-part primitive.

## Identified inquiry surfaces

| Surface | Already composes an answer? | Answer | Reason | Supporting evidence | Boundary | Limitations | Current status |
|---|---:|---|---|---|---|---|---|
| `operational_story` | Yes | `focus`, `pressure`, capabilities, constraints, correlation gaps, impact, recent changes, observed outcomes | `investigation_path` | `supporting_evidence` | `boundary` payload | `unknowns` payload | Complete Answer Composition layer evidence. |
| `inquiry_orientation` / Architectural Orientation | Yes | related material | composed `reason` string | composed support list and per-item support | authority boundary | uncertainty/limitations | Complete composition layer evidence internally; compatibility object remains narrower. |
| `inquiry_artifacts` | Yes, partially | artifact classification | implicit in artifact descriptions | artifact `evidence` tuple | surface-level `BOUNDARY` | artifact `limitations` tuple | Bounded answer exists, but answer/reason/support separation is compressed. |
| `reasoning_path` | Yes, partially | derivation path for a domain/subject | intermediate and derived conclusions | evidence and consumers | dataclass boundary | unknowns | Strong inquiry answer surface; reason/support are domain-shaped rather than five-part answer payloads. |
| `selection_path` | Yes, partially | selected item/outcome | selection factors and non-selected reasons | evidence and candidates | dataclass boundary | unknowns | Strong inquiry answer surface; reason/support are compressed into selection-specific fields. |
| `reference_selection` | Yes, partially | selected reference | selection rationale and alternatives | impact/snapshot evidence via selected/alternative records | authority boundary | limitations | Strong bounded answer; no separate implementation-local answer payload layer. |
| `question_surface_inventory` | Yes, as static responsibility inventory | surface rows and dispatch relationships | implementation reason | diagnostic inventory and shape-spec relationships | authority boundary text | relationship status gaps | It answers ownership/routing questions, not an answer-composition primitive. |
| Other bounded ask surfaces | Some compose answers | surface-specific outputs | surface-specific | surface-specific | surface-specific | surface-specific | Not audited as completed Answer Composition slices. |

## Implemented answer-composition boundaries

### Operational Story

`OperationalStory` is the clearest completed implementation. The public compatibility object still carries the historical public fields, but `build_operational_story(...)` now delegates to `_compose_operational_story_payloads(...)` and then performs explicit handoff into `OperationalStory`.

Implementation-local payloads separate:

- `_OperationalStoryAnswerPayload`
- `_OperationalStoryReasoningPayload`
- `_OperationalStorySupportingEvidencePayload`
- `_OperationalStoryBoundaryPayload`
- `_OperationalStoryLimitationsPayload`

The composer returns all five payloads and documents the separation as answer, reason, support, authority boundary, and limitations. The renderer consumes only the compatibility object and does not own the reasoning or selection logic.

Evidence:

- `OperationalStory` is still the compatibility object with focus, pressure, supporting evidence, investigation path, unknowns, and boundary fields.
- `_compose_operational_story_payloads(...)` returns five implementation-local payloads.
- `build_operational_story(...)` maps those payloads into `OperationalStory`.
- `format_operational_story(...)` renders the compatibility object without recomputing the answer.

### Architectural Orientation / Inquiry Orientation

Architectural Orientation now composes through an implementation-local `_ArchitecturalOrientationAnswer` before compatibility handoff. Its fields are exactly the architectural primitive:

- `answer`
- `reason`
- `support`
- `boundary`
- `limitations`

`build_inquiry_orientation(...)` calls `_compose_architectural_orientation_answer(...)`, then hands compatible fields to `InquiryOrientationView`. The public view remains unchanged and the formatter renders the view without selecting related material, deciding uncertainty, or constructing the boundary.

Important limitation: the public `InquiryOrientationView` currently preserves only `related_material`, `uncertainty`, and `authority_boundary`. The composed `reason` and support list are implementation-local, while per-item support and why-related material remain available through `RelatedMaterial` and renderer sections.

Evidence:

- `_ArchitecturalOrientationAnswer` explicitly owns answer, reason, support, boundary, and limitations.
- `_compose_architectural_orientation_answer(...)` selects related material by deterministic lexical overlap and returns the five-part answer object.
- `build_inquiry_orientation(...)` performs compatibility handoff into `InquiryOrientationView`.
- `format_inquiry_orientation(...)` renders the view and does not own answer composition.

## Remaining compressed boundaries

### Inquiry Artifacts

`inquiry_artifacts` exposes a bounded answer surface, but not the full reusable Answer Composition layer. Each artifact has `classification`, `evidence`, and `limitations`; the surface separately returns a read-only `BOUNDARY`. That gives answer, evidence, boundary, and limitations, but reason remains implicit in artifact classification text and evidence strings.

Compression:

```text
Artifact classification + evidence + limitations
```

is still stored as one public artifact visibility record, while the boundary is surface-level.

### Reasoning Path

`reasoning_path` is an inquiry answer about derivation. It carries evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and a boundary. This is a strong bounded-answer implementation, but it is domain-shaped. It has no implementation-local answer-composition object separating answer, reason, support, boundary, and limitations before compatibility handoff.

Compression remains between:

- answer and reasoning (`intermediate_conclusions`, `derived_conclusions`, `story_impact`);
- supporting evidence and consumers (`evidence`, `consumers`);
- compatibility object and rendered shape.

### Selection Path

`selection_path` answers selection questions with `selected`, `candidates`, `selection_factors`, `non_selected`, `evidence`, `outcome`, `unknowns`, and `boundary`. It naturally separates selected answer, reasons, evidence, limits, and boundary at the public dataclass level, but the builder constructs those fields directly into `SelectionPathAudit`.

Compression remains because the selection-specific compatibility object is also the first explicit ownership boundary for the answer.

### Reference Selection

`reference_selection` is already a bounded answer surface: selected reference, selection rationale, alternatives, authority boundary, limitations, and read-only mutation flags. It demonstrates answer composition as a recurring responsibility, but the answer/reason/evidence/boundary/limitations split is public and local rather than represented by a reusable implementation-local composition layer.

### Question Surface Inventory

`question_surface_inventory` does not compose operator-facing answers in the same sense as Operational Story or Architectural Orientation. It statically identifies question families, surfaces, answer responsibility, authority boundary, bounded status, dispatch surface, and diagnostic relationships. It supports the conclusion that inquiry surfaces have answer owners, but it does not itself prove a generic answer-composition payload layer.

## Relationship between Answer Composition and rendering

The current implementation naturally separates Answer Composition from rendering in the strongest completed surfaces.

### Operational Story

Rendering happens in `format_operational_story(story)`. It formats `story.focus`, `story.supporting_evidence`, `story.investigation_path`, `story.unknowns`, and `story.boundary`. It does not call pressure/capability/privilege/correlation/impact builders, does not select the focus, and does not decide unknowns. Those responsibilities are already owned by `build_operational_story(...)` and `_compose_operational_story_payloads(...)`.

### Inquiry Orientation

Rendering happens in `format_inquiry_orientation(view)`. It formats note text, related material, support/why-related, uncertainty, and authority boundary. It does not tokenize notes, match facts, call source navigation, choose uncertainty, or construct the boundary. Those responsibilities are owned by `_compose_architectural_orientation_answer(...)` and compatibility handoff in `build_inquiry_orientation(...)`.

### Other surfaces

`reasoning_path`, `selection_path`, `reference_selection`, and `inquiry_artifacts` also keep formatting functions separate from builder logic. However, because their answer-composition fields are still surface-specific public objects, they demonstrate renderer separation more strongly than reusable composition-layer separation.

## Relationship between Answer Composition and compatibility handoff

The repository now has explicit evidence for a compatibility handoff pattern:

```text
implementation-local composed answer
↓
legacy/public compatibility object
↓
JSON and human rendering
```

Operational Story proves this with private payload dataclasses and unchanged public `OperationalStory` fields. Architectural Orientation proves this with `_ArchitecturalOrientationAnswer` and unchanged public `InquiryOrientationView` fields.

This matters because it shows Answer Composition is not a renderer refactor and not a public schema migration. It is an internal responsibility boundary that can be projected without changing CLI, JSON, rendering, diagnostic inventory, event ledger, or cluster mutation behavior.

## Evidence supporting a reusable architectural layer

The implementation evidence supports reusability because the pattern is now repeated across distinct inquiry domains:

1. **Operational explanation** composes from operational pressure, capability needs, privilege discovery, correlation, impact, and investigation-path surfaces.
2. **Architectural orientation** composes from preserved inquiry notes, projected fact supports, and source-navigation matches.
3. Both completed surfaces separate bounded answer material from compatibility handoff and rendering.
4. Both preserve authority boundaries and limitations without making diagnostic or inquiry findings cluster truth.
5. Existing bounded answer surfaces (`reasoning_path`, `selection_path`, `reference_selection`, and `inquiry_artifacts`) independently carry compatible answer/reason/evidence/boundary/limitation material, showing that the primitive is not isolated to one module.

The prior Answer Composition slices also support this conclusion: they progressively separated Operational Story answer, reason, supporting evidence, boundary, and limitations while preserving public behavior. The Architectural Orientation slice then reused the same primitive in a different surface.

## Counterexamples and architectural projection still needed

The following counterexamples prevent claiming that every inquiry surface has completed Answer Composition projection:

- `inquiry_artifacts` still compresses classification, evidence, and limitations in public artifact records and has no explicit reason payload.
- `reasoning_path` and `selection_path` expose rich bounded answers, but their answer ownership is expressed through surface-specific dataclasses rather than implementation-local answer-composition payloads.
- `reference_selection` separates selected reference, rationale, alternatives, boundary, and limitations, but no compatibility handoff boundary exists between a local answer-composition object and the public compatibility object.
- `question_surface_inventory` records answer responsibility and bounded dispatch relationships, but does not inspect or compose the answer payloads of those surfaces.
- Several bounded ask surfaces answer questions with surface-specific models and were not projected into the five-part Answer Composition primitive during this milestone.

These are not failures of the completed family; they are evidence that projection is bounded. The completed claim should be limited to Answer Composition as a reusable architectural layer with completed representative implementations, not universal retrofitting of every answer-like surface.

## Supported conclusions

Supported by implementation evidence:

1. Answer Composition is now a reusable architectural layer, not merely a local Operational Story pattern.
2. Operational Story fully demonstrates the five-part answer-composition boundary before compatibility handoff.
3. Architectural Orientation reuses the same five-part primitive before compatibility handoff.
4. Rendering does not own reasoning in the completed surfaces.
5. Compatibility objects remain stable, proving the layer can be introduced without runtime surface or schema expansion.
6. Inquiry surfaces already participating in bounded answer composition include `operational_story`, `inquiry_orientation`, `inquiry_artifacts`, `reasoning_path`, `selection_path`, `reference_selection`, and, as responsibility metadata, `question_surface_inventory`.
7. The family is complete enough to stop doing Answer Composition slices as the current responsibility family.

## Unsupported conclusions

Not supported by current implementation evidence:

1. Every inquiry-oriented surface has been projected into a reusable five-part Answer Composition object.
2. `inquiry_artifacts`, `reasoning_path`, `selection_path`, and `reference_selection` have the same implementation-local compatibility handoff pattern as Operational Story and Architectural Orientation.
3. Answer Composition has become a public runtime registry, schema, CLI, formatter, planner, or workflow concept.
4. Presentation vocabulary alone is repository knowledge.
5. Diagnostic findings become cluster truth when composed into answers.
6. The next work should perform architectural recovery; this audit found enough implementation evidence to avoid recovery.

## Recommendation: next responsibility family

Implementation should now begin a new responsibility family rather than continue Answer Composition as the active family.

Recommended next responsibility family:

```text
Context Preservation / Reasoning-Chain Visibility
```

Reasoning:

- Existing implementation evidence shows multiple surfaces preserve parts of derivation, selection, reference, operational context, and inquiry orientation.
- `reasoning_path`, `selection_path`, and `reference_selection` already expose chain-preserving material, but cross-surface context remains fragmented.
- This recommendation follows existing implementation evidence and does not require treating presentation vocabulary as knowledge.

A bounded next slice should still obey repository authority: choose one implementation-backed compression point, avoid new runtime surfaces unless required, and preserve diagnostic inventory / shape-audit visibility if any operational surface changes.

## Acceptance answers

### Has Answer Composition become a reusable architectural layer?

Yes. The implementation now demonstrates the same answer-composition primitive in Operational Story and Architectural Orientation, two different inquiry surfaces with different sources and compatibility objects.

### Is the family complete?

Yes for the current projected Answer Composition responsibility family. No for universal conversion of every answer-like surface. The family can be considered complete as a reusable architectural layer because it has representative, implementation-backed reuse and clear counterexamples for future families rather than unresolved recovery work.

### What implementation evidence supports that conclusion?

- Five implementation-local Operational Story payloads before compatibility handoff.
- Five-field `_ArchitecturalOrientationAnswer` before compatibility handoff.
- Rendering functions that consume compatibility objects rather than composing answers.
- Existing bounded answer surfaces that already carry answer/reason/evidence/boundary/limitation material in surface-specific forms.
- Question Surface Inventory rows that identify answer responsibility and bounded dispatch ownership.

### Which inquiry surfaces already participate?

- `operational_story`
- `inquiry_orientation`
- `inquiry_artifacts`
- `reasoning_path`
- `selection_path`
- `reference_selection`
- `question_surface_inventory` as responsibility metadata

### Which still require architectural projection?

If future work chooses to normalize more surfaces into the reusable layer, the strongest candidates are:

- `inquiry_artifacts`
- `reasoning_path`
- `selection_path`
- `reference_selection`

These already contain bounded answer material, but responsibilities remain compressed compared with the completed primitive.

### Should implementation now begin a new responsibility family?

Yes. The next family should begin only after selecting an implementation-backed compression point. The strongest candidate from current evidence is Context Preservation / Reasoning-Chain Visibility.
