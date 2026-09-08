# Competency Interrogation Slice 033

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface JSON Support Line Rendering
        !=
DiagnosticSurface Human Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 032 in `seed_runtime/diagnostic_inventory.py`. After the DiagnosticSurface description line was routed through an implementation-local line renderer, the neighboring `supports_json:` line still remained directly interpolated inside both DiagnosticSurface human line-set assembly functions.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, or public surface.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface human rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` already delegates status line rendering, CLI flags line rendering, and description line rendering to implementation-local line renderers.
- `_assemble_diagnostic_surface_definition_line_set(...)` consumes the same status, CLI flags, and description line renderers for sibling definition output.
- Both line-set assemblers still directly interpolated the same `supports_json:` label and lower-case boolean display shape with their local indentation.
- The JSON support field already exists in the composed DiagnosticSurface definition JSON and did not require new discovery, schema, diagnostics, shape-audit registration, CLI behavior, or event-ledger behavior.
- The recurring local pattern was therefore directly observable: line-set assembly should collect a rendered JSON support line, while the JSON support line renderer owns only the label, lower-case display shape, and indentation.

## Before

The DiagnosticSurface explanation and definition line-set assemblers compressed two responsibilities:

1. DiagnosticSurface human line-set assembly:
   - collect existing DiagnosticSurface fields in the existing order;
   - include existing status, CLI flags, description, support, record-scope, boundary, consumption, registration, reason, and evidence presentation lines;
   - return the existing private line-set artifacts for human rendering.
2. DiagnosticSurface JSON support line rendering:
   - consume the existing definition `supports_json` value;
   - apply the caller's existing indentation;
   - lower-case the existing boolean-like display value;
   - add the existing `supports_json:` label;
   - include the resulting human line in explanation and definition output.

Behavior was correct, but the shared JSON support line shape remained implicit inside the broader line-set assembly owners.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` and `_assemble_diagnostic_surface_definition_line_set(...)` now pass the unchanged definition `supports_json` value to `_render_diagnostic_surface_json_support_line(...)` and include the unchanged rendered line in their existing line tuples.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_render_diagnostic_surface_json_support_line(...)` is the recovered producer for DiagnosticSurface JSON support line rendering. It consumes the existing support value plus the existing indentation and produces only the prefixed lower-case human line that the line-set assemblers already emitted.

## Recovered artifact/helper

`_DiagnosticSurfaceJsonSupportLine` is the recovered private artifact. It carries only:

- `line`

It does not carry DiagnosticSurface identity authority, explanation composition authority, definition production authority, CLI flag display preparation authority, status rendering authority, description rendering authority, JSON authority, diagnostic inventory registration authority, shape-audit registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

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

DiagnosticSurface human line-set assembly and DiagnosticSurface JSON support line rendering were previously compressed inside `_assemble_diagnostic_surface_explanation_line_set(...)` and `_assemble_diagnostic_surface_definition_line_set(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface JSON Support Line Rendering
        !=
DiagnosticSurface Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_json_support_line(...)` now owns the recovered prefixed lower-case JSON support line rendering responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceJsonSupportLine` carries the rendered JSON support line. It is a private implementation-local artifact.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` and `_assemble_diagnostic_surface_definition_line_set(...)` consume the rendered line before returning their unchanged private line-set artifacts to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `competency_interrogation_slice_033.md`

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
- DiagnosticSurface explanation and definition line rendering for record support fields that remain directly interpolated inside line-set assembly;
- DiagnosticSurface explanation and definition record-scope line rendering that remains directly interpolated inside line-set assembly;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local JSON support line path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
