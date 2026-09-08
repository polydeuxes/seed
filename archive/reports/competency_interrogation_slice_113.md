# Competency Interrogation Slice 113

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Shape Registration Status Field Label Production
        !=
DiagnosticSurface Definition Shape Registration Status Line Rendering
```

This slice begins immediately adjacent to Slice 112 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface definition inventory-registration field-label ownership was recovered, the same definition line-set assembly path exposed the next narrow recurring responsibility: shape-registration status line rendering still retained its own fallback `field_label="shape_registration_status"` even though definition line-set assembly already prepares and passes `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel` through `_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)`.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, or CLI behavior.

## Implementation evidence

Implementation evidence is concentrated around the adjacent DiagnosticSurface definition human rendering path:

- `_assemble_diagnostic_surface_definition_line_set(...)` prepares `shape_registration_status_field_label` from `_prepare_diagnostic_surface_definition_shape_registration_status_field_label()` and prepares `shape_registration_status_value` from `_prepare_diagnostic_surface_definition_shape_registration_status_value(definition)` before rendering the definition shape-registration status line.
- `_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)` already produces `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel(text="shape_registration_status")` for the definition shape-registration status line.
- `_render_diagnostic_surface_definition_shape_registration_status_line(...)` is the definition-specific producer for the rendered shape-registration status line consumed by definition line-set assembly.
- `_render_diagnostic_surface_shape_registration_status_line(...)` remains the generic shape-registration status renderer that combines the prepared value, field label, and indentation into the existing human line.
- Neighboring definition fields expose the recurring implementation-local pattern: field-label text is prepared by a context-specific producer and passed into context-specific rendering rather than being owned by the renderer fallback.
- Before this slice, definition shape-registration status field-label ownership was split: the definition assembler passed the prepared label, but the definition shape-registration status renderer still retained a default label fallback.
- Existing human definition output proves the prepared field label is consumed only by definition shape-registration status line rendering inside the definition line set.

The directly observable recurring local pattern is that the definition shape-registration status renderer should consume the definition-owned shape-registration status field-label artifact and should not also own a fallback copy of that label.

## Before

The DiagnosticSurface definition shape-registration status rendering path compressed two responsibilities:

1. DiagnosticSurface definition shape-registration status field-label production:
   - choose the existing human field label text `shape_registration_status` for the definition shape-registration status line;
   - preserve the existing line text without changing JSON output, schema, diagnostics, event-ledger behavior, cluster mutation behavior, or public CLI behavior.
2. DiagnosticSurface definition shape-registration status line rendering:
   - combine prepared shape-registration status value, prepared field label, and indentation before delegating to the generic shape-registration status renderer.

Behavior was correct, but the definition shape-registration status renderer still contained a fallback copy of the field-label text.

## After

`_render_diagnostic_surface_definition_shape_registration_status_line(...)` now requires an explicit `field_label` argument. The already-existing `_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)` producer remains the sole local source of the definition shape-registration status field-label text used by definition line-set assembly.

Rendering output is unchanged because `_assemble_diagnostic_surface_definition_line_set(...)` was already passing `shape_registration_status_field_label.text` to the renderer.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)` is the recovered producer for DiagnosticSurface definition shape-registration status field-label production. It produces the existing implementation-local `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel` artifact.

## Recovered artifact/helper

The recovered artifact is `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel`, which carries the existing prepared `shape_registration_status` field-label text between definition line-set assembly and definition shape-registration status line rendering.

The recovered helper is the already-existing `_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)` producer, now no longer shadowed by a default field-label fallback in `_render_diagnostic_surface_definition_shape_registration_status_line(...)`.

It does not carry DiagnosticSurface shape-registration status value preparation authority, generic shape-registration status line rendering authority, definition inventory-registration rendering authority, definition implementation-reason rendering authority, evidence-source rendering authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_definition_shape_registration_status_line(...)`

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

DiagnosticSurface definition shape-registration status field-label production and DiagnosticSurface definition shape-registration status line rendering were previously compressed because `_render_diagnostic_surface_definition_shape_registration_status_line(...)` retained a fallback `field_label="shape_registration_status"` while the assembler also prepared and passed `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Shape Registration Status Field Label Production
        !=
DiagnosticSurface Definition Shape Registration Status Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)` now solely owns the recovered DiagnosticSurface definition shape-registration status field-label production responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceShapeRegistrationStatusFieldLabel` carries the prepared `shape_registration_status` field-label text, and `_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)` is the helper that produces it.

### 5. Who consumes it?

`_render_diagnostic_surface_definition_shape_registration_status_line(...)` consumes `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel.text` before returning the unchanged `_DiagnosticSurfaceShapeRegistrationStatusLine` artifact to definition line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_113.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 2 +-
tests/test_diagnostic_inventory.py   | 5 +++++
2 files changed, 6 insertions(+), 1 deletion(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition CLI flag display preparation, definition name value preparation, definition identity heading line rendering, definition status value preparation, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description field-label preparation, definition description line rendering, definition JSON support value preparation, definition JSON support field-label preparation, definition JSON support line rendering, definition record support value preparation, definition record support field-label preparation, definition record support line rendering, definition record scope value preparation, definition record scope field-label preparation, definition record scope line rendering, definition boundary text preparation, definition boundary field-label production, definition boundary line rendering, definition consumption text preparation, definition consumption field-label production, definition consumption line rendering, definition inventory-registration value preparation, definition inventory-registration field-label production, definition inventory-registration line rendering, definition shape-registration status field-label production, definition shape-registration status value preparation, definition shape-registration status line rendering, definition implementation-reason field label preparation, definition implementation-reason value preparation, definition implementation-reason line rendering, definition evidence-source field label preparation, definition evidence-source value preparation, definition evidence-source line rendering, top-level field indent selection, definition section label rendering, definition section indent rendering, and definition field label preparation outside this recovered definition-specific shape-registration status field-label path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific record scope line rendering, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface shape-registration formatter coordination beyond definition shape-registration status value preparation, definition shape-registration status field-label production, definition shape-registration status line rendering, generic line rendering, shape-registration lookup, and shape-registration status identification;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local definition shape-registration status field-label production path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
