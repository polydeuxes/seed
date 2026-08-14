# Competency Interrogation Slice 022

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Consumption Line Rendering
        !=
DiagnosticSurface Consumption Text Preparation
```

This slice begins immediately adjacent to Slice 021 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface consumption declaration sequence extraction was separated from consumption text rendering, the next directly adjacent formatter path exposed a narrow local compression: `_format_diagnostic_surface_consumption(...)` both requested prepared consumption text and assembled the prefixed human output line consumed by DiagnosticSurface definition and explanation line sets.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, or public surface.

## Implementation evidence

Implementation evidence was concentrated in `_format_diagnostic_surface_consumption(...)`:

- `_format_diagnostic_surface_consumption(...)` already delegated declaration display text preparation to `_prepare_diagnostic_surface_consumption_text(...)`.
- The same function still owned the separate responsibility of applying indentation, adding the existing `diagnostic_surface_consumption:` label, and returning the final human line.
- The formatted line is consumed by existing DiagnosticSurface definition and explanation line-set assembly paths.
- The line renderer has no authority over DiagnosticSurface identity, consumption identification, declaration sequence extraction, consumption text preparation, boundary identification, read-only evaluation, JSON output, diagnostic inventory registration, shape-audit registration, CLI flag parsing, event-ledger behavior, cluster mutation behavior, or public compatibility.

The observable pressure was therefore narrow: rendering the existing prefixed consumption line is distinct from preparing the consumption declaration text embedded in that line.

## Before

`_format_diagnostic_surface_consumption(...)` compressed two responsibilities:

1. DiagnosticSurface consumption text preparation:
   - ask `_prepare_diagnostic_surface_consumption_text(...)` for the existing display text;
   - preserve the existing `unknown` fallback produced by text preparation.
2. DiagnosticSurface consumption line rendering:
   - apply the caller-provided indentation;
   - add the existing `diagnostic_surface_consumption:` label;
   - return the final human line as a string.

Behavior was correct, but consumption line rendering was implicit inside the formatter that also coordinated text preparation.

## After

A private implementation-local consumption line rendering owner now exists:

- `_DiagnosticSurfaceConsumptionLine`
- `_render_diagnostic_surface_consumption_line(...)`

`_format_diagnostic_surface_consumption(...)` now asks text preparation for the unchanged `_DiagnosticSurfaceConsumptionText`, passes that artifact to the recovered line renderer, and returns the unchanged line string.

## Recovered producer

`_render_diagnostic_surface_consumption_line(...)` is the recovered producer. It consumes an existing `_DiagnosticSurfaceConsumptionText` artifact plus the existing indentation argument and produces only the prefixed consumption line that `_format_diagnostic_surface_consumption(...)` already returned.

## Recovered artifact/helper

`_DiagnosticSurfaceConsumptionLine` is the recovered private artifact. It carries only:

- `line`

It does not carry DiagnosticSurface identity authority, JSON authority, shape-registration authority, consumption identification authority, declaration extraction authority, consumption text preparation authority, boundary identification authority, read-only evaluation authority, diagnostic inventory registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is `_format_diagnostic_surface_consumption(...)`.

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

DiagnosticSurface consumption text preparation and DiagnosticSurface consumption line rendering were previously compressed inside `_format_diagnostic_surface_consumption(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Consumption Line Rendering
        !=
DiagnosticSurface Consumption Text Preparation
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_consumption_line(...)` now owns the recovered prefixed consumption line rendering responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceConsumptionLine` carries the rendered consumption line. It is a private implementation-local artifact.

### 5. Who consumes it?

`_format_diagnostic_surface_consumption(...)` consumes the rendered line before returning the unchanged string to existing DiagnosticSurface definition and explanation line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_022.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 19 ++++++++++++++++++-
tests/test_diagnostic_inventory.py   | 32 ++++++++++++++++++++++++++++++++
2 files changed, 50 insertions(+), 1 deletion(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
64 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface boundary text rendering beyond statement sequence extraction;
- DiagnosticSurface boundary line rendering beyond boundary text preparation;
- DiagnosticSurface explanation human rendering beyond line-set assembly;
- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- DiagnosticSurface shape registration status presentation;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local consumption line path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
