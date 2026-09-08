# Inquiry to presentation to answer implementation audit

## Current implementation path

The repository contains a bounded implementation path for exact question-family inquiry, but the path currently reaches the family-owned answering surface rather than the newer subject-specific presentation composition surfaces.

Current path recovered from implementation evidence:

```text
ask --question-family <exact QuestionFamily>
  -> exact QuestionFamily lookup in question_surface_inventory
  -> bounded_status / required argument validation
  -> dispatch_surface flag assignment on the CLI namespace
  -> existing answering surface formatter / JSON handler
```

The implementation also contains separate subject-specific composed explanation surfaces:

```text
--question-family-explanation <QuestionFamily>
  -> QuestionFamily definition fields
  -> composed QuestionFamily explanation

--diagnostic-surface-explanation <DiagnosticSurface>
  -> DiagnosticSurface definition / boundary / consumption fields
  -> composed DiagnosticSurface explanation

--projection-stage-explanation <ProjectionStage>
  -> ProjectionStage definition / boundary / relationship fields
  -> composed ProjectionStage explanation
```

These composed explanation surfaces are implemented and executable, but bounded inquiry dispatch does not currently select them as the answer target.

## Evidence

### Inquiry identifies the questioned subject by exact QuestionFamily

`ask --question-family` is bounded to an exact inventory family. The CLI rejects free-text routing when `--question-family` is present, checks that the supplied family exists in `build_question_surface_inventory()`, and derives eligibility from `bounded_status_for_question_family()`.

Implementation evidence:

- `apply_bounded_ask_dispatch()` states that it maps `ask --question-family` to an existing exact inquiry surface.
- It errors unless the message is exactly `ask` plus `--question-family <exact-question-family>`.
- It builds the allowed family set from `build_question_surface_inventory()`.
- It rejects unknown families.
- It branches on `bounded_status_for_question_family(family)`.

Therefore Inquiry currently identifies the subject being questioned as an exact `QuestionFamily`, not as free text and not as a later inferred `DiagnosticSurface` or `ProjectionStage`.

### QuestionFamily rows own the answer-surface relationship

`QuestionSurfaceInventoryRow` includes the implementation-backed subject-to-surface fields: `question_family`, `surface`, `surface_flag`, `answer_responsibility`, `authority_boundary`, `bounded_status`, `dispatch_surface`, required arguments, diagnostic registrations, and relationship status.

`build_question_surface_inventory()` declares examples including:

- `projection shape visibility` -> `projection_shape` / `--projection-shape`
- `derivation explanation` -> `reasoning_path` / `--reasoning-path`
- `selection explanation` -> `selection_path` / `--selection-path`
- `source definition/import lookup` -> `source_navigation` / `--source-navigation`
- `inquiry orientation` -> `inquiry_orientation` / `--inquiry-orientation`

The inventory enriches rows from bounded ask maps and diagnostic registrations. That makes the QuestionFamily inventory the implementation owner for selecting which existing surface produces the answer after subject selection.

### Bounded inquiry dispatch forwards to existing answering surfaces

For `eligible_now` families, `apply_bounded_ask_dispatch()` sets the CLI namespace attribute named by `BOUNDED_ASK_DISPATCH_SURFACES[family]` to `True` or a predeclared value. For parameterized families, it requires exact `--surface-args` and forwards those explicit values to the target surface attribute.

This proves that bounded inquiry dispatch terminates by selecting a target surface flag, not by invoking the subject-specific presentation composition commands.

### Presentation-composed explanation surfaces already exist separately

QuestionFamily composition exists: `build_composed_question_family_explanation()` explicitly composes fields from `build_question_family_definition()` into labeled presentation sections: Definition, Answer responsibility, Boundary, and Diagnostic relationship. The CLI exposes this through `--question-family-explanation`.

DiagnosticSurface composition exists: `--diagnostic-surface-explanation diagnostic_shape_audit --json` returns a composed object containing `diagnostic_surface_definition`, `diagnostic_surface_boundary`, and `diagnostic_surface_consumption`.

ProjectionStage composition exists: `build_projection_stage_explanation()` composes `projection_stage_definition`, `projection_stage_boundary`, and `projection_stage_relationships`. The CLI exposes this through `--projection-stage-explanation`.

### App-run evidence

Commands run during this audit:

```text
python scripts/seed_local.py ask --question-family "projection shape visibility" --json
python scripts/seed_local.py --question-family-explanation "projection shape visibility" --json
python scripts/seed_local.py --diagnostic-surface-explanation diagnostic_shape_audit --json
python scripts/seed_local.py --projection-stage-explanation inference --json
```

Observed results:

- `ask --question-family "projection shape visibility" --json` produced the raw `projection_shape` answer payload with `boundary` and `stages`; it did not produce a `composed_question_family_explanation` envelope.
- `--question-family-explanation "projection shape visibility" --json` produced `composed_question_family_explanation` with sections for definition, answer responsibility, boundary, and diagnostic relationship.
- `--diagnostic-surface-explanation diagnostic_shape_audit --json` produced `diagnostic_surface_explanation` with definition, boundary, and consumption fields.
- `--projection-stage-explanation inference --json` produced `projection_stage_explanation` with definition, boundary, and relationships.

## Current termination point

Inquiry currently terminates at bounded dispatch to the selected answering surface.

Smallest implementation boundary:

```text
apply_bounded_ask_dispatch()
  -> setattr(args, BOUNDED_ASK_DISPATCH_SURFACES[family], ...)
  -> args.message = []
  -> normal CLI handler for that existing surface renders output
```

For the audited example, the terminal surface is `projection_shape`, not `projection_stage_explanation` and not `question_family_explanation`.

## Missing connection

The missing connection is between existing bounded inquiry subject selection and existing presentation-composed explanation surfaces.

Repository evidence supports this as a missing connection, not a missing architecture:

- Exact QuestionFamily selection already exists.
- QuestionFamily-to-answering-surface ownership already exists in the inventory rows and bounded dispatch maps.
- Composed explanation surfaces already exist for QuestionFamily, DiagnosticSurface, and ProjectionStage.
- CLI exposure already exists for those composition surfaces.
- The bounded ask path does not currently select a presentation-composed explanation as its answer target.

No implementation evidence found in this audit shows bounded inquiry selecting a `DiagnosticSurface` or `ProjectionStage` subject and then routing to that subject's composed explanation command.

## Boundary

This audit did not infer, normalize, rank, or recommend any new architecture. The recovered topology is limited to implementation-backed paths in:

- bounded ask dispatch
- question surface inventory
- QuestionFamily definition and composed explanation
- DiagnosticSurface composed explanation CLI behavior
- ProjectionStage composed explanation implementation and CLI behavior
- diagnostic inventory and shape registration relationships referenced by the inventory

Presentation vocabulary was treated as implementation evidence only where executable surfaces and tests already supported it.

## Implementation readiness

The implementation has already earned the components required for:

```text
Inquiry
  -> exact QuestionFamily selection
  -> existing answer-surface selection
```

The implementation has also already earned independent presentation composition for:

```text
QuestionFamily
DiagnosticSurface
ProjectionStage
```

The path has not yet earned an integrated runtime/CLI path of:

```text
ask --question-family ...
  -> subject selection beyond QuestionFamily
  -> presentation selection
  -> presentation-composed answer
```

Current state: partial path exists. It terminates at existing answering-surface dispatch. The smallest missing connection is the bounded link from inquiry-selected subject/surface to an existing composed presentation surface.

## Files examined

- `AGENTS.md`
- `scripts/seed_local.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projection_shape.py`
- `tests/test_question_surface_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_projection_shape.py`

## Files modified

- `docs/inquiry_presentation_answer_implementation_audit.md`

## LOC changed

- Added 186 lines.
