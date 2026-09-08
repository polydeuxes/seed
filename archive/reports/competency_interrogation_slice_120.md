# Competency Interrogation Slice 120

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Shape Registration Status Value Production
        !=
DiagnosticSurface Shape Registration Status Line Rendering
```

This slice begins immediately adjacent to Slice 119 in `seed_runtime/diagnostic_inventory.py`. After the generic evidence-source value producer was recovered before generic evidence-source line rendering, the next adjacent implementation-local responsibility was the generic shape-registration-status renderer's direct acceptance of an unprepared status value in the same local rendering neighborhood.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, or CLI behavior.

## Implementation evidence

Implementation evidence is concentrated around the generic DiagnosticSurface shape-registration-status human rendering path:

- `_DiagnosticSurfaceShapeRegistrationStatusValue` already exists as the implementation-local artifact for shape-registration-status values before line rendering.
- `_render_diagnostic_surface_definition_shape_registration_status_line(...)` already consumes a prepared `_DiagnosticSurfaceShapeRegistrationStatusValue` from `_prepare_diagnostic_surface_definition_shape_registration_status_value(...)` before delegating to `_render_diagnostic_surface_shape_registration_status_line(...)`.
- `_render_diagnostic_surface_shape_registration_status_line(...)` is the generic line renderer and combines the status value, field label, and indentation into the existing human line.
- Before this slice, the generic shape-registration-status renderer test still passed status text directly into the generic line renderer, compressing generic value production with generic line rendering.
- Existing tests directly exercise the generic renderer before definition line-set assembly, making the missing generic value producer directly observable in the same local neighborhood recovered by Slice 119.

The directly observable recurring local pattern is that shape-registration-status values are prepared as `_DiagnosticSurfaceShapeRegistrationStatusValue` before line rendering rather than being supplied as unprepared text at the rendering boundary.

## Before

The generic DiagnosticSurface shape-registration-status rendering path compressed two responsibilities:

1. DiagnosticSurface shape-registration-status value production:
   - carry the existing status value into the generic human rendering path;
   - preserve the existing line text without changing JSON output, schema, diagnostics, event-ledger behavior, cluster mutation behavior, or public CLI behavior.
2. DiagnosticSurface shape-registration-status line rendering:
   - combine status value, field label, and indentation into `_DiagnosticSurfaceShapeRegistrationStatusLine`.

Behavior was correct, but the generic shape-registration-status test supplied unprepared status text directly to `_render_diagnostic_surface_shape_registration_status_line(...)`.

## After

`_prepare_diagnostic_surface_shape_registration_status_value(...)` now produces the existing generic shape-registration-status value artifact.

`_render_diagnostic_surface_shape_registration_status_line(...)` remains the line renderer and receives the prepared value's `.value`, preserving the existing output exactly.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_prepare_diagnostic_surface_shape_registration_status_value(...)` is the recovered producer for generic DiagnosticSurface shape-registration-status value production.

## Recovered artifact/helper

The recovered artifact is the already-existing `_DiagnosticSurfaceShapeRegistrationStatusValue`, which carries the existing shape-registration-status value into generic shape-registration-status line rendering.

The recovered helper is `_prepare_diagnostic_surface_shape_registration_status_value(...)`.

It does not carry DiagnosticSurface shape-registration-status field-label authority, definition-specific shape-registration-status value authority, definition-specific shape-registration-status field-label authority, generic shape-registration-status line rendering authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_shape_registration_status_line(...)`

Downstream existing consumers remain unchanged:

- `_render_diagnostic_surface_definition_shape_registration_status_line(...)`
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

Generic DiagnosticSurface shape-registration-status value production and generic DiagnosticSurface shape-registration-status line rendering were previously compressed because the generic renderer path accepted unprepared status text directly where the local implementation already had a shape-registration-status value artifact.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Shape Registration Status Value Production
        !=
DiagnosticSurface Shape Registration Status Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_shape_registration_status_value(...)` now owns the recovered generic DiagnosticSurface shape-registration-status value production responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceShapeRegistrationStatusValue` carries the prepared shape-registration-status value, and `_prepare_diagnostic_surface_shape_registration_status_value(...)` is the helper that produces it.

### 5. Who consumes it?

`_render_diagnostic_surface_shape_registration_status_line(...)` consumes `_DiagnosticSurfaceShapeRegistrationStatusValue.value` before returning the unchanged `_DiagnosticSurfaceShapeRegistrationStatusLine` artifact.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_120.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py |  6 ++++++
tests/test_diagnostic_inventory.py   | 10 +++++++++-
2 files changed, 15 insertions(+), 1 deletion(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition CLI flag display preparation, definition name value preparation, definition identity heading line rendering, definition status value preparation, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description field-label preparation, definition description line rendering, definition JSON support value preparation, definition JSON support field-label preparation, definition JSON support line rendering, definition record support value preparation, definition record support field-label preparation, definition record scope value preparation, definition record scope field-label preparation, definition boundary text preparation, definition boundary field-label production, definition boundary line rendering, definition consumption text preparation, definition consumption field-label production, definition consumption line rendering, definition inventory-registration value preparation, definition inventory-registration field-label production, definition inventory-registration line rendering, definition shape-registration status field-label production, definition shape-registration status value preparation, definition shape-registration status line rendering, definition implementation-reason field-label production, definition implementation-reason value preparation, definition implementation-reason line rendering, definition evidence-source field-label production, definition evidence-source value preparation, definition evidence-source line rendering, top-level field indent selection, definition section label rendering, definition section indent rendering, nested definition field indent selection, and definition field label preparation outside this recovered generic shape-registration-status value path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface shape-registration formatter coordination beyond definition shape-registration status value preparation, definition shape-registration status field-label production, definition shape-registration status line rendering, generic line rendering, shape-registration lookup, shape-registration status identification, and generic shape-registration-status value production;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local generic shape-registration-status value production path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
