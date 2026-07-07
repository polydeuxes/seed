# Competency Interrogation Slice 032

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Description Line Rendering
        !=
DiagnosticSurface Human Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 031 in `seed_runtime/diagnostic_inventory.py`. After the DiagnosticSurface status line and CLI flags line were routed through implementation-local line renderers, the neighboring `description:` line still remained directly interpolated inside both DiagnosticSurface human line-set assembly functions.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, or public surface.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface human rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` already delegates status line rendering to `_render_diagnostic_surface_status_line(...)` and CLI flags line rendering to `_render_diagnostic_surface_cli_flags_line(...)`.
- `_assemble_diagnostic_surface_definition_line_set(...)` consumes the same status and CLI flags line renderers for the sibling definition output.
- Both line-set assemblers still directly interpolated the same `description:` label with their local indentation.
- The description field already exists in the composed DiagnosticSurface definition JSON and did not require new discovery, schema, diagnostics, shape-audit registration, CLI behavior, or event-ledger behavior.
- The recurring local pattern was therefore directly observable: line-set assembly should collect a rendered description line, while the description line renderer owns only the label and indentation shape.

## Before

The DiagnosticSurface explanation and definition line-set assemblers compressed two responsibilities:

1. DiagnosticSurface human line-set assembly:
   - collect existing DiagnosticSurface fields in the existing order;
   - include existing status, CLI flags, boundary, consumption, registration, reason, and evidence presentation lines;
   - return the existing private line-set artifacts for human rendering.
2. DiagnosticSurface description line rendering:
   - consume the existing definition description value;
   - apply the caller's existing indentation;
   - add the existing `description:` label;
   - include the resulting human line in explanation and definition output.

Behavior was correct, but the shared description line shape remained implicit inside the broader line-set assembly owners.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` and `_assemble_diagnostic_surface_definition_line_set(...)` now pass the unchanged definition description value to `_render_diagnostic_surface_description_line(...)` and include the unchanged rendered line in their existing line tuples.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_render_diagnostic_surface_description_line(...)` is the recovered producer for DiagnosticSurface description line rendering. It consumes the existing description value plus the existing indentation and produces only the prefixed human line that the line-set assemblers already emitted.

## Recovered artifact/helper

`_DiagnosticSurfaceDescriptionLine` is the recovered private artifact. It carries only:

- `line`

It does not carry DiagnosticSurface identity authority, explanation composition authority, definition production authority, CLI flag display preparation authority, status rendering authority, JSON authority, diagnostic inventory registration authority, shape-audit registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumers are:

- `_assemble_diagnostic_surface_explanation_line_set(...)`
- `_assemble_diagnostic_surface_definition_line_set(...)`

Downstream existing consumers remain unchanged:

- `format_diagnostic_surface_explanation(...)`
- `format_diagnostic_surface_definition(...)`
- `seed --diagnostic-surface-explanation <surface>`
- `seed --diagnostic-surface-definition <surface>`

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

- `seed --diagnostic-surface-explanation diagnostic_shape_audit`
- `seed --diagnostic-surface-explanation diagnostic_shape_audit --json`
- `seed --diagnostic-surface-definition diagnostic_shape_audit`
- `seed --diagnostic-surface-definition diagnostic_shape_audit --json`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

## Required questions

### 1. What responsibilities were previously compressed?

DiagnosticSurface human line-set assembly and DiagnosticSurface description line rendering were previously compressed inside `_assemble_diagnostic_surface_explanation_line_set(...)` and `_assemble_diagnostic_surface_definition_line_set(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Description Line Rendering
        !=
DiagnosticSurface Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_description_line(...)` now owns the recovered prefixed description line rendering responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceDescriptionLine` carries the rendered description line. It is a private implementation-local artifact.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` and `_assemble_diagnostic_surface_definition_line_set(...)` consume the rendered line before returning their unchanged private line-set artifacts to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `competency_interrogation_slice_032.md`

## LOC changed

Implementation diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 19 +++++++++++++++++--
1 file changed, 17 insertions(+), 2 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface explanation human rendering beyond line-set assembly;
- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface explanation and definition line rendering for boolean support fields that remain directly interpolated inside line-set assembly;
- DiagnosticSurface explanation and definition record-scope line rendering that remains directly interpolated inside line-set assembly;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local description line path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
