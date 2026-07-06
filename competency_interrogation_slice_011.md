# Competency Interrogation Slice 011

## Selected boundary

Recovered exactly one implementation-local DiagnosticSurface ownership boundary:

```text
DiagnosticSurface CLI Flag Display Preparation
        !=
DiagnosticSurface Human Rendering
```

This slice begins near the implementation modified for Slice 010 and follows only adjacent implementation evidence. It does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, router, planner, scheduler, orchestration layer, methodology owner, constitutional abstraction, diagnostic framework, or diagnostic-surface redesign.

## Implementation evidence

Implementation evidence was concentrated in `seed_runtime/diagnostic_inventory.py` immediately after the completed DiagnosticSurface explanation-composition recovery:

- `format_diagnostic_surface_explanation(...)` consumed an already-built DiagnosticSurface explanation payload, extracted the nested definition, normalized `cli_flags` into human display text, and then rendered the human-readable explanation lines.
- `format_diagnostic_surface_definition(...)` independently repeated the same `cli_flags` display normalization before rendering the human-readable definition lines.
- The repeated expression had no authority to change JSON shape, diagnostic inventory registration, shape-audit registration, event-ledger behavior, cluster mutation behavior, or CLI behavior. It only prepared display text for existing human-readable DiagnosticSurface output.
- Existing public JSON paths continued to consume the unchanged wrapped definition and explanation payloads.
- Existing tests already proved public JSON, human output, unknown-surface behavior, inventory visibility, and shape-audit guardrails for the DiagnosticSurface surfaces.

The directly observable pressure was narrow and recurring: preparing DiagnosticSurface CLI flag display text is a local display-preparation responsibility distinct from the surrounding human line rendering in both DiagnosticSurface definition and DiagnosticSurface explanation output.

## Before

Two human rendering functions each compressed the same local responsibilities:

1. DiagnosticSurface CLI flag display preparation:
   - consume the existing `cli_flags` value from the DiagnosticSurface definition payload;
   - join a non-empty list into comma-separated display text;
   - present missing, empty, or non-list values as `none`.
2. DiagnosticSurface human rendering:
   - assemble the public human-readable definition or explanation lines;
   - preserve indentation, labels, and existing field order.

Behavior was correct, but the recurring display-preparation responsibility was implicit inside each renderer.

## After

A private implementation-local display-preparation owner now exists:

- `_DiagnosticSurfaceCliFlagDisplay`
- `_prepare_diagnostic_surface_cli_flag_display(...)`

`format_diagnostic_surface_definition(...)` and `format_diagnostic_surface_explanation(...)` now ask that producer for the existing CLI flag display text and then continue to render their unchanged human-readable output.

## Recovered producer

`_prepare_diagnostic_surface_cli_flag_display(...)` is the recovered producer. It consumes an existing DiagnosticSurface `cli_flags` value and produces only the human display text used by existing DiagnosticSurface renderers.

## Recovered artifact/helper

`_DiagnosticSurfaceCliFlagDisplay` is the recovered private artifact. It carries only the prepared display `text` and does not carry definition identity, explanation payloads, boundary statements, consumption facts, registration status, or any diagnostic authority.

## Recovered consumer

The immediate consumers are:

- `format_diagnostic_surface_definition(...)`
- `format_diagnostic_surface_explanation(...)`

Downstream CLI consumers remain unchanged:

- `seed --diagnostic-surface-definition <surface>`
- `seed --diagnostic-surface-explanation <surface>`

JSON consumers are unchanged because the recovered boundary is used only by human rendering.

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

DiagnosticSurface CLI flag display preparation and DiagnosticSurface human rendering were previously compressed inside both `format_diagnostic_surface_definition(...)` and `format_diagnostic_surface_explanation(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface CLI Flag Display Preparation
        !=
DiagnosticSurface Human Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_cli_flag_display(...)` now owns the recovered display-preparation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceCliFlagDisplay` carries the prepared display text. It is a private implementation-local artifact.

### 5. Who consumes it?

`format_diagnostic_surface_definition(...)` and `format_diagnostic_surface_explanation(...)` consume the prepared display artifact before producing unchanged human-readable output.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_011.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 31 +++++++++++++++++++++++++------
tests/test_diagnostic_inventory.py   | 19 +++++++++++++++++++
2 files changed, 44 insertions(+), 6 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
53 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- human-readable DiagnosticSurface definition line assembly;
- human-readable DiagnosticSurface explanation line assembly;
- DiagnosticSurface boundary statement formatting;
- DiagnosticSurface consumption formatting;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local CLI flag display-preparation path.

Those responsibilities remain compressed unless future implementation evidence independently supports another local recovery.
