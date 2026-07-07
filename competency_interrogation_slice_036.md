# Competency Interrogation Slice 036

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Heading Line Rendering
        !=
DiagnosticSurface Human Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 035 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface record-scope line rendering was recovered, the neighboring first line of both DiagnosticSurface human line-set assemblers still directly formatted the `DiagnosticSurface <kind>: <diagnostic_name>` heading.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, or public surface.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface human rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` already delegates status line rendering, CLI flags line rendering, description line rendering, JSON support line rendering, record support line rendering, and record-scope line rendering to implementation-local line renderers.
- `_assemble_diagnostic_surface_definition_line_set(...)` consumes the same line renderers for sibling definition output.
- Both line-set assemblers still directly interpolated the same heading shape with the existing DiagnosticSurface label, a local surface kind, and the existing diagnostic name.
- The diagnostic name already exists in the composed DiagnosticSurface definition JSON and did not require new discovery, schema, diagnostics, shape-audit registration, CLI behavior, or event-ledger behavior.
- The recurring local pattern was therefore directly observable: line-set assembly should collect a rendered heading line, while the heading line renderer owns only the existing label, surface kind placement, diagnostic-name placement, and punctuation.

## Before

The DiagnosticSurface explanation and definition line-set assemblers compressed two responsibilities:

1. DiagnosticSurface human line-set assembly:
   - collect existing DiagnosticSurface fields in the existing order;
   - include existing heading, status, CLI flags, description, JSON support, record support, record-scope, boundary, consumption, registration, reason, and evidence presentation lines;
   - return the existing private line-set artifacts for human rendering.
2. DiagnosticSurface heading line rendering:
   - consume the existing DiagnosticSurface surface kind;
   - consume the existing definition `diagnostic_name` value;
   - add the existing `DiagnosticSurface` label and colon punctuation;
   - include the resulting human heading in explanation and definition output.

Behavior was correct, but the shared heading line shape remained implicit inside the broader line-set assembly owners.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` and `_assemble_diagnostic_surface_definition_line_set(...)` now pass the unchanged local surface kind and unchanged definition `diagnostic_name` value to `_render_diagnostic_surface_heading_line(...)` and include the unchanged rendered line in their existing line tuples.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_render_diagnostic_surface_heading_line(...)` is the recovered producer for DiagnosticSurface heading line rendering. It consumes the existing surface kind plus the existing diagnostic name and produces only the human heading line that the line-set assemblers already emitted.

## Recovered artifact/helper

`_DiagnosticSurfaceHeadingLine` is the recovered private artifact. It carries only:

- `line`

It does not carry DiagnosticSurface identity authority, explanation composition authority, definition production authority, CLI flag display preparation authority, status rendering authority, description rendering authority, JSON support rendering authority, record support rendering authority, record-scope rendering authority, diagnostic inventory registration authority, shape-audit registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

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

DiagnosticSurface human line-set assembly and DiagnosticSurface heading line rendering were previously compressed inside `_assemble_diagnostic_surface_explanation_line_set(...)` and `_assemble_diagnostic_surface_definition_line_set(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Heading Line Rendering
        !=
DiagnosticSurface Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_heading_line(...)` now owns the recovered DiagnosticSurface heading line rendering responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceHeadingLine` carries the rendered heading line. It is a private implementation-local artifact.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` and `_assemble_diagnostic_surface_definition_line_set(...)` consume the rendered line before returning their unchanged private line-set artifacts to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `competency_interrogation_slice_036.md`

## LOC changed

Implementation diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 23 +++++++++++++++++++++--
1 file changed, 21 insertions(+), 2 deletions(-)
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
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local heading line path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
