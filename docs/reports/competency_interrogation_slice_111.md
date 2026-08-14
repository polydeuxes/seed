# Competency Interrogation Slice 111

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Consumption Field Label Production
        !=
DiagnosticSurface Definition Consumption Line Rendering
```

This slice begins immediately adjacent to Slice 110 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface definition boundary field-label ownership was recovered, the same definition line-set assembly path exposed the next narrow recurring responsibility: definition consumption line rendering still retained its own fallback `field_label="diagnostic_surface_consumption"` even though the definition assembler already prepares and passes `_DiagnosticSurfaceConsumptionFieldLabel` through `_prepare_diagnostic_surface_definition_consumption_field_label(...)`.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, or CLI behavior.

## Implementation evidence

Implementation evidence is concentrated around the adjacent DiagnosticSurface definition human rendering path:

- `_assemble_diagnostic_surface_definition_line_set(...)` prepares `consumption_text` from `_prepare_diagnostic_surface_definition_consumption_text(definition)` and prepares `consumption_field_label` from `_prepare_diagnostic_surface_definition_consumption_field_label()` before rendering the definition consumption line.
- `_prepare_diagnostic_surface_definition_consumption_field_label(...)` already produces `_DiagnosticSurfaceConsumptionFieldLabel(text="diagnostic_surface_consumption")` for the definition consumption line.
- `_render_diagnostic_surface_definition_consumption_line(...)` is the definition-specific producer for the rendered consumption line consumed by definition line-set assembly.
- `_render_diagnostic_surface_consumption_line(...)` remains the generic consumption renderer that combines consumption text, field label, and indentation into the existing human line.
- Neighboring definition fields expose the recurring implementation-local pattern: field-label text is prepared by a context-specific producer and passed into context-specific rendering rather than being owned by the renderer fallback.
- Before this slice, definition consumption field-label ownership was split: the definition assembler passed the prepared label, but the definition consumption renderer still retained a default label fallback.
- Existing human definition output proves the prepared field label is consumed only by definition consumption line rendering inside the definition line set.

The directly observable recurring local pattern is that the definition consumption renderer should consume the definition-owned consumption field-label artifact and should not also own a fallback copy of that label.

## Before

The DiagnosticSurface definition consumption rendering path compressed two responsibilities:

1. DiagnosticSurface definition consumption field-label production:
   - choose the existing human field label text `diagnostic_surface_consumption` for the definition consumption line;
   - preserve the existing line text without changing JSON output, schema, diagnostics, event-ledger behavior, cluster mutation behavior, or public CLI behavior.
2. DiagnosticSurface definition consumption line rendering:
   - combine prepared consumption text, prepared field label, and indentation before delegating to the generic consumption renderer.

Behavior was correct, but the definition consumption renderer still contained a fallback copy of the field-label text.

## After

`_render_diagnostic_surface_definition_consumption_line(...)` now requires an explicit `field_label` argument. The already-existing `_prepare_diagnostic_surface_definition_consumption_field_label(...)` producer remains the sole local source of the definition consumption field-label text used by definition line-set assembly.

Rendering output is unchanged because `_assemble_diagnostic_surface_definition_line_set(...)` was already passing `consumption_field_label.text` to the renderer.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_prepare_diagnostic_surface_definition_consumption_field_label(...)` is the recovered producer for DiagnosticSurface definition consumption field-label production. It produces the existing implementation-local `_DiagnosticSurfaceConsumptionFieldLabel` artifact.

## Recovered artifact/helper

The recovered artifact is `_DiagnosticSurfaceConsumptionFieldLabel`, which carries the existing prepared `diagnostic_surface_consumption` field-label text between definition line-set assembly and definition consumption line rendering.

The recovered helper is the already-existing `_prepare_diagnostic_surface_definition_consumption_field_label(...)` producer, now no longer shadowed by a default field-label fallback in `_render_diagnostic_surface_definition_consumption_line(...)`.

It does not carry DiagnosticSurface consumption text preparation authority, generic consumption line rendering authority, definition consumption declaration extraction authority, definition boundary rendering authority, definition inventory-registration rendering authority, explanation rendering authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_definition_consumption_line(...)`

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

DiagnosticSurface definition consumption field-label production and DiagnosticSurface definition consumption line rendering were previously compressed because `_render_diagnostic_surface_definition_consumption_line(...)` retained a fallback `field_label="diagnostic_surface_consumption"` while the assembler also prepared and passed `_DiagnosticSurfaceConsumptionFieldLabel`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Consumption Field Label Production
        !=
DiagnosticSurface Definition Consumption Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_definition_consumption_field_label(...)` now solely owns the recovered DiagnosticSurface definition consumption field-label production responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceConsumptionFieldLabel` carries the prepared `diagnostic_surface_consumption` field-label text, and `_prepare_diagnostic_surface_definition_consumption_field_label(...)` is the helper that produces it.

### 5. Who consumes it?

`_render_diagnostic_surface_definition_consumption_line(...)` consumes `_DiagnosticSurfaceConsumptionFieldLabel.text` before returning the unchanged `_DiagnosticSurfaceConsumptionLine` artifact to definition line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_111.md`

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

- DiagnosticSurface definition human rendering beyond definition CLI flag display preparation, definition name value preparation, definition identity heading line rendering, definition status value preparation, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description field-label preparation, definition description line rendering, definition JSON support value preparation, definition JSON support field-label preparation, definition JSON support line rendering, definition record support value preparation, definition record support field-label preparation, definition record support line rendering, definition record scope value preparation, definition record scope field-label preparation, definition record scope line rendering, definition boundary text preparation, definition boundary field-label production, definition boundary line rendering, definition consumption text preparation, definition consumption field label preparation, definition consumption line rendering, definition inventory-registration field label preparation, definition inventory-registration value preparation, definition inventory-registration line rendering, definition shape-registration status field label preparation, definition shape-registration status value preparation, definition shape-registration status line rendering, definition implementation-reason field label preparation, definition implementation-reason value preparation, definition implementation-reason line rendering, definition evidence-source field label preparation, definition evidence-source value preparation, definition evidence-source line rendering, top-level field indent selection, definition section label rendering, definition section indent rendering, and definition field label preparation outside this recovered definition-specific consumption field-label path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific record scope line rendering, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface consumption formatter coordination beyond definition consumption text preparation, definition consumption field-label production, definition consumption line rendering, explanation consumption text preparation, explanation consumption field label preparation, explanation consumption line rendering, line rendering, and declaration-sequence extraction;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local definition consumption field-label production path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
