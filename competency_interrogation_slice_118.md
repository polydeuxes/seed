# Competency Interrogation Slice 118

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Implementation Reason Value Production
        !=
DiagnosticSurface Implementation Reason Line Rendering
```

This slice begins immediately adjacent to Slice 117 in `seed_runtime/diagnostic_inventory.py`. After the generic implementation-reason field-label fallback was moved out of `_render_diagnostic_surface_implementation_reason_line(...)`, the next adjacent implementation-local responsibility was the generic implementation-reason renderer's remaining direct acceptance of an unprepared reason value in the same local path.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, or CLI behavior.

## Implementation evidence

Implementation evidence is concentrated around the generic DiagnosticSurface implementation-reason human rendering path:

- `_DiagnosticSurfaceImplementationReasonValue` already exists as the implementation-local artifact for implementation-reason values before line rendering.
- `_render_diagnostic_surface_definition_implementation_reason_line(...)` already consumes a prepared `_DiagnosticSurfaceImplementationReasonValue` from `_prepare_diagnostic_surface_definition_implementation_reason_value(...)` before delegating to `_render_diagnostic_surface_implementation_reason_line(...)`.
- `_render_diagnostic_surface_implementation_reason_line(...)` is the generic line renderer and combines the implementation-reason value, prepared field label, and indentation into the existing human line.
- Before this slice, the generic implementation-reason renderer test still passed the reason text directly into the generic line renderer, compressing generic value production with generic line rendering.
- Existing tests directly exercise the generic renderer before definition line-set assembly, making the missing generic value producer directly observable in the same local neighborhood recovered by Slice 117.

The directly observable recurring local pattern is that implementation-reason values are prepared as `_DiagnosticSurfaceImplementationReasonValue` before line rendering rather than being supplied as unprepared text at the rendering boundary.

## Before

The generic DiagnosticSurface implementation-reason rendering path compressed two responsibilities:

1. DiagnosticSurface implementation-reason value production:
   - carry the existing implementation-reason value into the generic human rendering path;
   - preserve the existing line text without changing JSON output, schema, diagnostics, event-ledger behavior, cluster mutation behavior, or public CLI behavior.
2. DiagnosticSurface implementation-reason line rendering:
   - combine implementation-reason value, prepared field label, and indentation into `_DiagnosticSurfaceImplementationReasonLine`.

Behavior was correct, but the generic implementation-reason test supplied unprepared reason text directly to `_render_diagnostic_surface_implementation_reason_line(...)`.

## After

`_prepare_diagnostic_surface_implementation_reason_value(...)` now produces the existing generic implementation-reason value artifact.

`_render_diagnostic_surface_implementation_reason_line(...)` remains the line renderer and receives the prepared value's `.value`, preserving the existing output exactly.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_prepare_diagnostic_surface_implementation_reason_value(...)` is the recovered producer for generic DiagnosticSurface implementation-reason value production.

## Recovered artifact/helper

The recovered artifact is the already-existing `_DiagnosticSurfaceImplementationReasonValue`, which carries the existing implementation-reason value into generic implementation-reason line rendering.

The recovered helper is `_prepare_diagnostic_surface_implementation_reason_value(...)`.

It does not carry DiagnosticSurface implementation-reason field-label authority, definition-specific implementation-reason value authority, definition-specific implementation-reason field-label authority, generic implementation-reason line rendering authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_implementation_reason_line(...)`

Downstream existing consumers remain unchanged:

- `_render_diagnostic_surface_definition_implementation_reason_line(...)`
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

Generic DiagnosticSurface implementation-reason value production and generic DiagnosticSurface implementation-reason line rendering were previously compressed because the generic renderer path accepted unprepared reason text directly where the local implementation already had an implementation-reason value artifact.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Implementation Reason Value Production
        !=
DiagnosticSurface Implementation Reason Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_implementation_reason_value(...)` now owns the recovered generic DiagnosticSurface implementation-reason value production responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceImplementationReasonValue` carries the prepared implementation-reason value, and `_prepare_diagnostic_surface_implementation_reason_value(...)` is the helper that produces it.

### 5. Who consumes it?

`_render_diagnostic_surface_implementation_reason_line(...)` consumes `_DiagnosticSurfaceImplementationReasonValue.value` before returning the unchanged `_DiagnosticSurfaceImplementationReasonLine` artifact.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_118.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py |  6 ++++++
tests/test_diagnostic_inventory.py   | 12 +++++++++++-
2 files changed, 17 insertions(+), 1 deletion(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition CLI flag display preparation, definition name value preparation, definition identity heading line rendering, definition status value preparation, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description field-label preparation, definition description line rendering, definition JSON support value preparation, definition JSON support field-label preparation, definition JSON support line rendering, definition record support value preparation, definition record support field-label preparation, definition record support line rendering, definition record scope value preparation, definition record scope field-label preparation, definition record scope line rendering, definition boundary text preparation, definition boundary field-label production, definition boundary line rendering, definition consumption text preparation, definition consumption field-label production, definition consumption line rendering, definition inventory-registration value preparation, definition inventory-registration field-label production, definition inventory-registration line rendering, definition shape-registration status field-label production, definition shape-registration status value preparation, definition shape-registration status line rendering, definition implementation-reason field-label production, definition implementation-reason value preparation, definition implementation-reason line rendering, definition evidence-source field-label production, definition evidence-source value preparation, definition evidence-source line rendering, top-level field indent selection, definition section label rendering, definition section indent rendering, nested definition field indent selection, and definition field label preparation outside this recovered generic implementation-reason value path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface shape-registration formatter coordination beyond definition shape-registration status value preparation, definition shape-registration status field-label production, definition shape-registration status line rendering, generic line rendering, shape-registration lookup, and shape-registration status identification;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local generic implementation-reason value production path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
