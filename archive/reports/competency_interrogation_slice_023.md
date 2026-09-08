# Competency Interrogation Slice 023

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Boundary Line Rendering
        !=
DiagnosticSurface Boundary Text Preparation
```

This slice begins immediately adjacent to Slice 022 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface consumption line rendering was separated from consumption text preparation, the neighboring boundary formatter exposed the same narrow local compression: `_format_diagnostic_surface_boundary(...)` both requested prepared boundary text and assembled the prefixed human output line consumed by DiagnosticSurface definition and explanation line sets.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, or public surface.

## Implementation evidence

Implementation evidence was concentrated in `_format_diagnostic_surface_boundary(...)`:

- `_format_diagnostic_surface_boundary(...)` already delegated boundary display text preparation to `_prepare_diagnostic_surface_boundary_text(...)`.
- The same function still owned the separate responsibility of applying indentation, adding the existing `diagnostic_surface_boundary:` label, and returning the final human line.
- The formatted line is consumed by existing DiagnosticSurface definition and explanation line-set assembly paths.
- The line renderer has no authority over DiagnosticSurface identity, boundary identification, statement sequence extraction, boundary text preparation, consumption identification, read-only evaluation, JSON output, diagnostic inventory registration, shape-audit registration, CLI flag parsing, event-ledger behavior, cluster mutation behavior, or public compatibility.

The observable pressure was therefore narrow: rendering the existing prefixed boundary line is distinct from preparing the boundary statement text embedded in that line.

## Before

`_format_diagnostic_surface_boundary(...)` compressed two responsibilities:

1. DiagnosticSurface boundary text preparation:
   - ask `_prepare_diagnostic_surface_boundary_text(...)` for the existing display text;
   - preserve the existing `unknown` fallback produced by text preparation.
2. DiagnosticSurface boundary line rendering:
   - apply the caller-provided indentation;
   - add the existing `diagnostic_surface_boundary:` label;
   - return the final human line as a string.

Behavior was correct, but boundary line rendering was implicit inside the formatter that also coordinated text preparation.

## After

A private implementation-local boundary line rendering owner now exists:

- `_DiagnosticSurfaceBoundaryLine`
- `_render_diagnostic_surface_boundary_line(...)`

`_format_diagnostic_surface_boundary(...)` now asks text preparation for the unchanged `_DiagnosticSurfaceBoundaryText`, passes that artifact to the recovered line renderer, and returns the unchanged line string.

## Recovered producer

`_render_diagnostic_surface_boundary_line(...)` is the recovered producer. It consumes an existing `_DiagnosticSurfaceBoundaryText` artifact plus the existing indentation argument and produces only the prefixed boundary line that `_format_diagnostic_surface_boundary(...)` already returned.

## Recovered artifact/helper

`_DiagnosticSurfaceBoundaryLine` is the recovered private artifact. It carries only:

- `line`

It does not carry DiagnosticSurface identity authority, JSON authority, shape-registration authority, boundary identification authority, statement extraction authority, boundary text preparation authority, consumption identification authority, read-only evaluation authority, diagnostic inventory registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is `_format_diagnostic_surface_boundary(...)`.

Downstream existing consumers remain unchanged:

- `_assemble_diagnostic_surface_definition_line_set(...)`
- `_assemble_diagnostic_surface_explanation_line_set(...)`
- `seed --diagnostic-surface-definition <surface>`
- `seed --diagnostic-surface-explanation <surface>`

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

- `seed --diagnostic-surface-definition diagnostic_shape_audit`
- `seed --diagnostic-surface-explanation diagnostic_shape_audit`
- `seed --diagnostic-surface-definition diagnostic_shape_audit --json`
- `seed --diagnostic-surface-explanation diagnostic_shape_audit --json`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

## Required questions

### 1. What responsibilities were previously compressed?

DiagnosticSurface boundary text preparation and DiagnosticSurface boundary line rendering were previously compressed inside `_format_diagnostic_surface_boundary(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Boundary Line Rendering
        !=
DiagnosticSurface Boundary Text Preparation
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_boundary_line(...)` now owns the recovered prefixed boundary line rendering responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceBoundaryLine` carries the rendered boundary line. It is a private implementation-local artifact.

### 5. Who consumes it?

`_format_diagnostic_surface_boundary(...)` consumes the rendered line before returning the unchanged string to existing DiagnosticSurface definition and explanation line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_023.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 17 ++++++++++++++++-
tests/test_diagnostic_inventory.py   | 19 +++++++++++++++++++
2 files changed, 35 insertions(+), 1 deletion(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
65 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface explanation human rendering beyond line-set assembly;
- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- DiagnosticSurface shape registration status presentation;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local boundary line path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
