# Inquiry, subject, and presentation responsibility capture

This capture records only current implementation evidence for whether the repository has earned this responsibility invariant:

```text
Inquiry selects.
Subsystems expose explanation fields.
Presentation composes answers.
```

It is not a reconciliation, proposal, or design exercise.

## Observed responsibility ownership

### Inquiry

Implementation evidence assigns Inquiry a bounded selection and dispatch responsibility, not ownership of answer construction.

- `QuestionSurfaceInventoryRow` records question families, example questions, existing Seed surfaces, answer responsibilities, authority boundaries, bounded status, dispatch surfaces, required surface arguments, formatter metadata, diagnostic linkage, and relationship status.
- `bounded_status_for_question_family()` derives whether a question family is dispatchable from executable dispatch maps.
- `apply_bounded_ask_dispatch()` maps `ask --question-family <exact-question-family>` to an already existing exact surface. It rejects unknown families, wrong invocation shape, missing or extra explicit surface arguments, diagnostic-only families, and not-dispatchable families.

Observed Inquiry responsibility: select a known question family, validate its bounded dispatch eligibility, require explicit parameters where current implementation requires them, and activate an existing answering surface. Inquiry does not synthesize explanation fields or compose a new answer payload.

### Subject-owning subsystems

Implementation evidence assigns subject-owning subsystems responsibility for implementation-backed explanation fields. The subject examples are independent and use local registries or declarations as evidence sources.

- `QuestionFamily` exposes definition, answer-responsibility, boundary, and diagnostic-relationship fields from the question surface inventory.
- `DiagnosticSurface` exposes definition, boundary, and consumption fields from the diagnostic inventory plus diagnostic shape-audit registration.
- `ProjectionStage` exposes definition, boundary, and relationships from the projection shape stage registry.

These subsystems do not own the final composed answer as a generic answer object. Their fields can include an `answer_responsibility` value when that is part of the subject's own inventory, but implementation treats that as an explanation field over the subject-to-surface relationship, not as the composed answer itself.

### Presentation

Implementation evidence assigns Presentation a composition responsibility over existing fields.

- `build_composed_question_family_explanation()` composes existing `QuestionFamily` definition, answer-responsibility, boundary, and diagnostic-relationship fields into ordered presentation sections.
- `build_diagnostic_surface_explanation()` composes existing `DiagnosticSurface` definition, boundary, and consumption fields for presentation.
- `build_projection_stage_explanation()` composes existing `ProjectionStage` definition, boundary, and relationships without adding evidence.
- CLI branches print either JSON or human rendering for the composed explanation surfaces. The CLI exposes presentation output; it does not create the underlying subject evidence.

Observed Presentation responsibility: order, label, and render implementation-backed fields already exposed by subject-owning subsystems.

## Supporting implementation

| Responsibility | Implementation evidence | What it demonstrates |
| --- | --- | --- |
| Inquiry selection | `BOUNDED_ASK_DISPATCH_SURFACES`, `BOUNDED_ASK_REQUIRED_SURFACE_ARGS`, `bounded_status_for_question_family()` | Inquiry eligibility is map-backed and bounded. |
| Inquiry dispatch | `apply_bounded_ask_dispatch()` | Bounded ask selects an existing exact surface and validates explicit arguments. |
| QuestionFamily field ownership | `build_question_family_definition()` | The question-family subsystem exposes identity, boundary, answer-responsibility, and diagnostic relationship fields from inventory evidence. |
| DiagnosticSurface field ownership | `build_diagnostic_surface_definition()` | The diagnostic subsystem exposes identity, boundary, consumption, inventory, and shape-registration fields. |
| ProjectionStage field ownership | `build_projection_stage_definition()` and `build_projection_stage_relationships()` | The projection subsystem exposes identity, boundary, consumes, produces, and influences fields from projection stage declarations. |
| Presentation composition | `build_composed_question_family_explanation()`, `build_diagnostic_surface_explanation()`, `build_projection_stage_explanation()` | Presentation composes existing fields into explanation shapes and does not add authority. |
| CLI answer surface exposure | `--question-family-explanation`, `--diagnostic-surface-explanation`, `--projection-stage-explanation` handlers | Existing composed explanations are exposed through JSON/human presentation surfaces. |

## Observed boundaries

- Inquiry is exact-family and map-bounded. It rejects unknown, diagnostic-only, and not-dispatchable families instead of inventing a dispatch path.
- Question-family inventory rows explicitly state that inventory rows do not route operator questions; routing is limited to bounded ask dispatch maps.
- Subject-owning explanation builders use declared evidence sources such as `question_surface_inventory`, `diagnostic_inventory + diagnostic_shape_audit`, and `projection_shape_stage_registry`.
- Presentation composition reuses existing fields. Existing implementation names this boundary directly for QuestionFamily (`presentation only`), DiagnosticSurface (`for presentation`), and ProjectionStage (`without adding evidence`).
- No implementation evidence was found for a generic answer engine, generic presentation engine, ontology, planner, LLM integration, or `ExplainableSubject` abstraction as part of this chain.

## Observed responsibility chain

The repository currently supports this chain for the examined surfaces:

```text
Inquiry
  selects a known question family and bounded dispatch surface
Subject
  is the existing subsystem surface selected or described by inventory
Explanation fields
  are exposed by subject-owned builders from implementation registries/declarations
Presentation
  composes those fields into ordered JSON/human explanation output
Answer
  is the resulting bounded composed explanation surface, not a newly inferred generic answer
```

Evidence for the chain is strongest where `QuestionFamily` is involved because the same implementation includes both bounded inquiry dispatch and composed question-family explanation. `DiagnosticSurface` and `ProjectionStage` independently validate the subject-field and presentation-composition portions of the chain.

## Accepted invariant

Accepted, with implementation boundaries:

```text
Inquiry selects.
Subsystems expose explanation fields.
Presentation composes bounded explanation answers from those fields.
```

This is implementation-backed for the examined subject classes because selection, subject-owned explanation fields, and composed explanation presentation are all present in executable code and covered by tests elsewhere in the repository.

## Rejected invariants

Rejected as unsupported by current implementation evidence:

```text
Inquiry owns answers.
Subsystems own generic final answers.
Presentation discovers or infers explanation evidence.
A generic answer engine exists for all subject classes.
A generic presentation engine exists for all explanation classes.
```

The repository evidence instead shows bounded dispatch plus subject-specific explanation builders plus subject-specific composition functions.

## Implementation boundaries

- This capture does not change operational behavior.
- This capture does not add a diagnostic, audit, probe, CLI flag, recordable output, or event-ledger behavior.
- This capture does not promote presentation vocabulary into repository knowledge.
- This capture does not recommend implementation or propose future architecture.
- This capture is limited to implementation evidence surrounding Inquiry, QuestionFamily, DiagnosticSurface, ProjectionStage, Presentation, bounded dispatch, composed explanations, and answer composition.

## Files examined

- `AGENTS.md`
- `scripts/seed_local.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projection_shape.py`
- `tests/test_question_surface_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`
- `tests/test_projection_shape.py`

## Files modified

- `docs/inquiry_subject_presentation_responsibility_capture.md`

## LOC changed

One documentation file was added.
