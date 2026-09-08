# Competency Interrogation Slice 106

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Description Field Label Preparation
        !=
Generic DiagnosticSurface Description Line Rendering
```

This slice begins immediately adjacent to Slice 105 in `seed_runtime/diagnostic_inventory.py`. After definition CLI flag display preparation was recovered, the same DiagnosticSurface definition line-set assembly path still exposed the next narrow compressed responsibility: definition description line rendering relied on the generic description line renderer's default `field_label="description"` instead of an explicit definition-owned field-label artifact.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface definition human rendering path:

- `_assemble_diagnostic_surface_definition_line_set(...)` prepares definition display artifacts before producing the human definition line set.
- `_prepare_diagnostic_surface_definition_description_text(...)` already owns definition-specific extraction of `definition["description"]` before description line rendering.
- `_render_diagnostic_surface_definition_description_line(...)` already exists as the definition-specific producer for the rendered `description` definition line consumed by definition line-set assembly.
- `_DiagnosticSurfaceDescriptionFieldLabel` already exists as the implementation-local artifact for carrying a prepared description field label before description line rendering.
- `_prepare_diagnostic_surface_explanation_description_field_label(...)` already prepares the same `description` field label for explanation-specific rendering, proving this module separates context-specific description field-label preparation from generic description line rendering.
- `_render_diagnostic_surface_description_line(...)` remains the generic renderer that combines a description value, field label, and indent into a line.
- Neighboring definition fields expose the recurring implementation-local pattern of definition-specific preparation before definition line rendering, including boundary field label, consumption field label, inventory-registration field label, shape-registration status field label, implementation-reason field label, and evidence-source field label.
- Before this slice, the definition description field label remained compressed as the generic renderer's default argument rather than a definition-owned artifact prepared by the definition path.
- Existing human definition output proves the prepared field label is consumed only by definition description line rendering inside the definition line set.

The directly observable recurring local pattern is that the definition line-set assembler should consume a definition-specific description field-label artifact before asking the definition description line renderer to render the line.

## Before

The DiagnosticSurface definition description rendering path compressed two responsibilities:

1. DiagnosticSurface definition description field-label preparation:
   - choose the existing human field label text `description` for the definition description line;
   - preserve the existing line text without changing JSON output, schema, diagnostics, event-ledger behavior, cluster mutation behavior, or public CLI behavior.
2. Generic DiagnosticSurface description line rendering:
   - combine description text, field label, and indentation into the existing human line.

Behavior was correct, but definition-specific field-label ownership remained compressed into the generic description line renderer's default argument.

## After

`_assemble_diagnostic_surface_definition_line_set(...)` now prepares `_DiagnosticSurfaceDescriptionFieldLabel` through `_prepare_diagnostic_surface_definition_description_field_label(...)` before passing the unchanged label text to `_render_diagnostic_surface_definition_description_line(...)`.

`_render_diagnostic_surface_definition_description_line(...)` now accepts the explicit field label and delegates unchanged rendering to `_render_diagnostic_surface_description_line(...)`.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_prepare_diagnostic_surface_definition_description_field_label(...)` is the recovered producer for DiagnosticSurface definition description field-label preparation. It produces the existing implementation-local `_DiagnosticSurfaceDescriptionFieldLabel` artifact.

## Recovered artifact/helper

The recovered helper is `_prepare_diagnostic_surface_definition_description_field_label(...)`.

The recovered artifact is `_DiagnosticSurfaceDescriptionFieldLabel`, which carries the existing prepared `description` field label between definition line-set assembly and definition description line rendering.

It does not carry DiagnosticSurface definition identity heading line rendering authority, definition name value preparation authority, definition CLI flag display preparation authority, definition CLI flags line rendering authority, status value preparation authority, status line rendering authority, description text preparation authority, generic description line rendering authority beyond delegation, JSON support value preparation authority, record support value preparation authority, record scope value preparation authority, boundary text preparation authority, consumption text preparation authority, inventory registration value preparation authority, shape-registration status value preparation authority, implementation-reason value preparation authority, evidence-source value preparation authority, top-level field indent selection authority, explanation rendering authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_definition_description_line(...)`

The upstream assembler that prepares and passes the artifact is:

- `_assemble_diagnostic_surface_definition_line_set(...)`

Downstream existing consumers remain unchanged:

- `format_diagnostic_surface_definition(...)`
- `seed --diagnostic-surface-definition <surface>`

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

- `seed --diagnostic-surface-definition diagnostic_shape_audit`
- `seed --diagnostic-surface-definition diagnostic_shape_audit --json`
- `seed --diagnostic-surface-explanation diagnostic_shape_audit`
- `seed --diagnostic-surface-explanation diagnostic_shape_audit --json`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

## Required questions

### 1. What responsibilities were previously compressed?

DiagnosticSurface definition description field-label preparation and generic DiagnosticSurface description line rendering were previously compressed through the generic renderer's default `field_label="description"` argument.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Description Field Label Preparation
        !=
Generic DiagnosticSurface Description Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_definition_description_field_label(...)` now owns the recovered DiagnosticSurface definition description field-label preparation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_prepare_diagnostic_surface_definition_description_field_label(...)` carries the recovered helper boundary, and `_DiagnosticSurfaceDescriptionFieldLabel` carries the prepared `description` field-label text.

### 5. Who consumes it?

`_render_diagnostic_surface_definition_description_line(...)` consumes `_DiagnosticSurfaceDescriptionFieldLabel.text` before returning the unchanged `_DiagnosticSurfaceDescriptionLine` artifact to definition line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_106.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 19 ++++++++++++++++---
tests/test_diagnostic_inventory.py   |  9 ++++++++-
2 files changed, 24 insertions(+), 4 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition CLI flag display preparation, definition name value preparation, definition identity heading line rendering, definition status value preparation, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description line rendering, definition JSON support value preparation, definition JSON support line rendering, definition record support value preparation, definition record support line rendering, definition record scope value preparation, definition boundary text preparation, definition boundary field-label preparation, definition boundary line rendering, definition consumption text preparation, definition consumption field label preparation, definition consumption line rendering, definition inventory-registration field label preparation, definition inventory-registration value preparation, definition inventory-registration line rendering, definition shape-registration status field label preparation, definition shape-registration status value preparation, definition shape-registration status line rendering, definition implementation-reason field label preparation, definition implementation-reason value preparation, definition implementation-reason line rendering, definition evidence-source field label preparation, definition evidence-source value preparation, definition evidence-source line rendering, top-level field indent selection, definition section label rendering, definition section indent rendering, and definition field label preparation outside this recovered definition-specific description field-label path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface boundary formatter coordination beyond definition boundary text preparation, definition boundary field-label preparation, definition boundary line rendering, explanation boundary text preparation, explanation boundary field label preparation, explanation boundary line rendering, line rendering, and statement-sequence extraction;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local definition description field-label preparation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
