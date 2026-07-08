# Competency Interrogation Slice 129

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Implementation-Reason Line Rendering Request
        !=
DiagnosticSurface Implementation-Reason Line Rendering
```

This slice begins immediately adjacent to Slice 128 in `seed_runtime/diagnostic_inventory.py`. After the definition shape-registration-status line-rendering request boundary was made observable, the next implementation-local responsibility in the same definition rendering neighborhood is the implementation-reason line-rendering path: the definition-specific renderer requests a line for the definition surface while the reusable DiagnosticSurface implementation-reason renderer owns concrete line text production.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, or CLI behavior.

## Implementation evidence

Implementation evidence is concentrated around the DiagnosticSurface definition implementation-reason human rendering path:

- `_DiagnosticSurfaceImplementationReasonLine` already exists as the implementation-local artifact for carrying the rendered implementation-reason line.
- `_render_diagnostic_surface_implementation_reason_line(...)` already exists as the generic producer for that artifact.
- `_render_diagnostic_surface_definition_implementation_reason_line(...)` is the definition-specific request point used by `_assemble_diagnostic_surface_definition_line_set(...)`.
- `_prepare_diagnostic_surface_definition_implementation_reason_value(...)` already delegates value production to `_prepare_diagnostic_surface_implementation_reason_value(...)`, making the next adjacent responsibility the line-rendering request boundary.
- The definition implementation-reason rendering test now proves that the definition-specific renderer delegates to the generic implementation-reason line renderer before definition line-set assembly.

The directly observable recurring local pattern is that definition-specific helpers keep definition path coordination and field-label/value handoff while generic producers own reusable DiagnosticSurface line artifact construction.

## Before

The definition DiagnosticSurface implementation-reason rendering test proved the field label, value artifact, required field-label argument, rendered text, and line artifact shape. It did not prove that the definition-specific line-rendering request remained separated from reusable DiagnosticSurface implementation-reason line production.

Behavior was correct, but this local ownership boundary was still compressed in the test evidence for the definition implementation-reason rendering path.

## After

`test_diagnostic_surface_definition_implementation_reason_line_rendering_precedes_line_set_assembly` now proves that `_render_diagnostic_surface_definition_implementation_reason_line(...)` delegates to `_render_diagnostic_surface_implementation_reason_line(...)`.

`_render_diagnostic_surface_implementation_reason_line(...)` remains the recovered producer for `_DiagnosticSurfaceImplementationReasonLine`.

No public output, JSON shape, CLI behavior, diagnostics, event-ledger behavior, cluster mutation behavior, schema, or compatibility boundary changed.

## Recovered producer

`_render_diagnostic_surface_implementation_reason_line(...)` is the recovered producer for DiagnosticSurface implementation-reason line rendering.

## Recovered artifact/helper

The recovered artifact is the already-existing `_DiagnosticSurfaceImplementationReasonLine`, which carries the rendered implementation-reason line into definition line-set assembly.

The recovered helper is `_render_diagnostic_surface_implementation_reason_line(...)`.

It does not carry definition field extraction authority, implementation-reason value production authority, implementation-reason field-label production authority, definition line-set assembly authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_definition_implementation_reason_line(...)`

Downstream existing consumers remain unchanged:

- `_assemble_diagnostic_surface_definition_line_set(...)`
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

DiagnosticSurface definition implementation-reason line rendering request and DiagnosticSurface implementation-reason line rendering were previously compressed in the definition rendering test evidence because the test asserted rendered output without proving that the definition-specific renderer delegates reusable line artifact production to the generic implementation-reason renderer.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Implementation-Reason Line Rendering Request
        !=
DiagnosticSurface Implementation-Reason Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_implementation_reason_line(...)` owns the recovered DiagnosticSurface implementation-reason line-rendering responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceImplementationReasonLine` carries the rendered implementation-reason line, and `_render_diagnostic_surface_implementation_reason_line(...)` is the helper that produces it.

### 5. Who consumes it?

`_render_diagnostic_surface_definition_implementation_reason_line(...)` consumes the generic renderer; the unchanged definition line-set assembly consumes the returned line artifact downstream.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_129.md`

## LOC changed

Implementation and test diff before this report:

```text
tests/test_diagnostic_inventory.py | 3 +++
1 file changed, 3 insertions(+)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition CLI flag display preparation, definition name value preparation, definition identity heading line rendering, definition status value preparation, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description field-label preparation, definition description line rendering, definition JSON support value preparation, definition JSON support field-label preparation, definition JSON support line rendering, definition record support value preparation, definition record support field-label preparation, definition record scope value preparation, definition record scope field-label preparation, definition boundary text preparation, definition boundary field-label production, definition boundary line rendering, definition consumption text preparation, definition consumption field-label production, definition consumption line rendering, definition inventory-registration value preparation, definition inventory-registration field-label production, definition inventory-registration line rendering, definition shape-registration-status value preparation, definition shape-registration-status field-label production, definition shape-registration-status line rendering, definition implementation-reason value source extraction, definition evidence-source value source extraction, and definition evidence-source line rendering outside this recovered implementation-reason line-rendering path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface shape-registration formatter coordination beyond shape-registration lookup, shape-registration status identification, generic value production, generic field-label production, and generic line rendering;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local implementation-reason line-rendering path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
