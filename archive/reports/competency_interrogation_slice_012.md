# Competency Interrogation Slice 012

## Selected boundary

Recovered exactly one implementation-local DiagnosticSurface ownership boundary:

```text
DiagnosticSurface Boundary Statement Text Preparation
        !=
DiagnosticSurface Boundary Line Rendering
```

This slice begins immediately adjacent to Slice 011 in `seed_runtime/diagnostic_inventory.py`. The current neighborhood was not exhausted: after CLI flag display preparation was separated from human rendering, the next directly observable compressed responsibility remained in the same local DiagnosticSurface human-output path. The evidence is implementation-local and does not require Competency Interrogation Grammar, a framework, engine, registry, router, planner, scheduler, orchestration layer, methodology owner, constitutional abstraction, diagnostic framework, or architectural redesign.

## Implementation evidence

Implementation evidence was concentrated in `_format_diagnostic_surface_boundary(...)`:

- The function accepted an already-produced DiagnosticSurface boundary payload from existing definition and explanation composition paths.
- It validated that the payload was a dictionary, extracted `statements`, handled unknown or empty statement shapes as `unknown`, and joined known statements with `; `.
- The same function also applied the rendered human line prefix, indentation, and `diagnostic_surface_boundary:` label.
- The prepared statement text is consumed by both existing human DiagnosticSurface surfaces because `_format_diagnostic_surface_boundary(...)` is called from `format_diagnostic_surface_definition(...)` and `format_diagnostic_surface_explanation(...)`.
- The responsibility has no authority over JSON shape, inventory registration, shape-audit registration, event-ledger behavior, cluster mutation behavior, CLI flags, or DiagnosticSurface boundary identification.

The observable pressure was therefore narrow: preparing boundary statement text from an existing payload is distinct from rendering the final indented human line.

## Before

`_format_diagnostic_surface_boundary(...)` compressed two responsibilities:

1. DiagnosticSurface boundary statement text preparation:
   - accept an existing boundary payload;
   - treat non-dictionary payloads as `unknown`;
   - treat missing, empty, or non-list `statements` as `unknown`;
   - join known statements into the existing semicolon-separated display text.
2. DiagnosticSurface boundary line rendering:
   - apply the caller-provided indentation;
   - apply the `diagnostic_surface_boundary:` label;
   - return the final human-readable line consumed by existing definition and explanation output.

Behavior was correct, but the statement-text preparation responsibility was implicit inside line rendering.

## After

A private implementation-local text-preparation owner now exists:

- `_DiagnosticSurfaceBoundaryText`
- `_prepare_diagnostic_surface_boundary_text(...)`

`_format_diagnostic_surface_boundary(...)` now asks that producer for the existing boundary statement display text and then continues to render the unchanged human-readable line.

## Recovered producer

`_prepare_diagnostic_surface_boundary_text(...)` is the recovered producer. It consumes an existing DiagnosticSurface boundary payload and produces only the human boundary statement text already used by existing human renderers.

## Recovered artifact/helper

`_DiagnosticSurfaceBoundaryText` is the recovered private artifact. It carries only the prepared `text` value and does not carry DiagnosticSurface identity, definition payloads, explanation payloads, consumption facts, registration status, indentation, line labels, JSON authority, diagnostic authority, or CLI authority.

## Recovered consumer

The immediate consumer is `_format_diagnostic_surface_boundary(...)`.

Downstream existing consumers remain unchanged:

- `format_diagnostic_surface_definition(...)`
- `format_diagnostic_surface_explanation(...)`
- `seed --diagnostic-surface-definition <surface>`
- `seed --diagnostic-surface-explanation <surface>`

JSON consumers are unchanged because the recovered boundary is used only by existing human line rendering.

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

DiagnosticSurface boundary statement text preparation and DiagnosticSurface boundary line rendering were previously compressed inside `_format_diagnostic_surface_boundary(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Boundary Statement Text Preparation
        !=
DiagnosticSurface Boundary Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_boundary_text(...)` now owns the recovered boundary statement text-preparation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceBoundaryText` carries the prepared boundary statement text. It is a private implementation-local artifact.

### 5. Who consumes it?

`_format_diagnostic_surface_boundary(...)` consumes the prepared text before producing the unchanged human-readable boundary line. Existing definition and explanation human output consume that line through their existing calls.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_012.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 24 +++++++++++++++++++-----
tests/test_diagnostic_inventory.py   | 27 +++++++++++++++++++++++++++
2 files changed, 46 insertions(+), 5 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
54 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface consumption display text preparation inside `_format_diagnostic_surface_consumption(...)`;
- DiagnosticSurface consumption line rendering;
- human-readable DiagnosticSurface definition line assembly;
- human-readable DiagnosticSurface explanation line assembly;
- DiagnosticSurface boundary identification from inventory entry fields;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local boundary statement text-preparation path.

Those responsibilities remain compressed unless future implementation evidence independently supports another local recovery.
