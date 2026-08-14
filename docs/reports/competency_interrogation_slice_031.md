# Competency Interrogation Slice 031

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Explanation Status Line Rendering
        !=
DiagnosticSurface Explanation Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 030 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface explanation CLI flags line rendering was routed through `_render_diagnostic_surface_cli_flags_line(...)`, the neighboring explanation status line still rendered its own indented `status:` line directly inside `_assemble_diagnostic_surface_explanation_line_set(...)`.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, or public surface.

## Implementation evidence

Implementation evidence was concentrated in `_assemble_diagnostic_surface_explanation_line_set(...)` and the adjacent status line rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` already receives the composed DiagnosticSurface definition used by both explanation human rendering and definition human rendering.
- `_render_diagnostic_surface_status_line(...)` already owns the human `status:` line shape and already accepts an indentation argument.
- `_DiagnosticSurfaceStatusLine` already carries only the rendered status line before line-set assembly.
- `_assemble_diagnostic_surface_definition_line_set(...)` already consumes `_render_diagnostic_surface_status_line(...)` for the same status field in the sibling definition output.
- `_assemble_diagnostic_surface_explanation_line_set(...)` still directly interpolated `f"    status: {definition['status']}"`, compressing explanation line-set assembly with status line rendering.

The observable pressure was therefore narrow: explanation line-set assembly should consume the existing status line renderer instead of owning the local prefixed line interpolation itself.

## Before

`_assemble_diagnostic_surface_explanation_line_set(...)` compressed two responsibilities:

1. DiagnosticSurface explanation line-set assembly:
   - collect the existing explanation definition fields in the existing order;
   - include existing boundary and consumption presentation lines;
   - return `_DiagnosticSurfaceExplanationLineSet` for existing human rendering.
2. DiagnosticSurface explanation status line rendering:
   - consume the existing definition status value;
   - apply the existing four-space explanation-definition indentation;
   - add the existing `status:` label;
   - include the line in the explanation human output.

Behavior was correct, but explanation status line rendering remained implicit inside the broader explanation line-set assembly owner.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` now passes the unchanged definition status value to `_render_diagnostic_surface_status_line(...)` with the existing explanation indentation and includes the unchanged rendered line in the existing line tuple.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_render_diagnostic_surface_status_line(...)` is the recovered producer for the explanation status line. It consumes the existing status value plus the existing explanation indentation and produces only the prefixed human line that `_assemble_diagnostic_surface_explanation_line_set(...)` already emitted.

## Recovered artifact/helper

`_DiagnosticSurfaceStatusLine` is the recovered private artifact already available adjacent to Slice 030. It carries only:

- `line`

It does not carry DiagnosticSurface identity authority, explanation composition authority, definition production authority, CLI flag display preparation authority, JSON authority, diagnostic inventory registration authority, shape-audit registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is `_assemble_diagnostic_surface_explanation_line_set(...)`.

Downstream existing consumers remain unchanged:

- `format_diagnostic_surface_explanation(...)`
- `seed --diagnostic-surface-explanation <surface>`

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

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

DiagnosticSurface explanation line-set assembly and DiagnosticSurface explanation status line rendering were previously compressed inside `_assemble_diagnostic_surface_explanation_line_set(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Explanation Status Line Rendering
        !=
DiagnosticSurface Explanation Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_status_line(...)` now owns the recovered prefixed explanation status line rendering responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceStatusLine` carries the rendered status line. It is a private implementation-local artifact.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` consumes the rendered line before returning the unchanged `_DiagnosticSurfaceExplanationLineSet` to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `competency_interrogation_slice_031.md`

## LOC changed

Implementation diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 4 +++-
1 file changed, 3 insertions(+), 1 deletion(-)
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
- DiagnosticSurface explanation line rendering for fields that remain directly interpolated inside explanation line-set assembly;
- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface definition line rendering for fields that remain directly interpolated inside definition line-set assembly;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local explanation status line path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
