# Competency Interrogation Slice 013

## Selected boundary

Recovered exactly one implementation-local DiagnosticSurface ownership boundary:

```text
DiagnosticSurface Consumption Declaration Text Preparation
        !=
DiagnosticSurface Consumption Line Rendering
```

This slice begins immediately adjacent to Slice 012 in `seed_runtime/diagnostic_inventory.py`. The Slice 012 neighborhood was not exhausted: after DiagnosticSurface boundary statement text preparation was separated from boundary line rendering, the same local human-output path exposed the next compressed responsibility in `_format_diagnostic_surface_consumption(...)`. The evidence is implementation-local and does not require Competency Interrogation Grammar, a framework, engine, registry, router, planner, scheduler, orchestration layer, methodology owner, constitutional abstraction, diagnostic framework, or architectural redesign.

## Implementation evidence

Implementation evidence was concentrated in `_format_diagnostic_surface_consumption(...)`:

- The function accepted an already-produced DiagnosticSurface consumption payload from existing definition and explanation composition paths.
- It validated that the payload was a dictionary, extracted `declared_consumption`, handled unknown or empty declaration shapes as `unknown`, and joined known declarations with `; `.
- The same function also applied the rendered human line prefix, indentation, and `diagnostic_surface_consumption:` label.
- The prepared consumption declaration text is consumed by both existing human DiagnosticSurface surfaces because `_format_diagnostic_surface_consumption(...)` is called from `format_diagnostic_surface_definition(...)` and `format_diagnostic_surface_explanation(...)`.
- The responsibility has no authority over JSON shape, inventory registration, shape-audit registration, event-ledger behavior, cluster mutation behavior, CLI flags, or DiagnosticSurface consumption identification.

The observable pressure was therefore narrow: preparing consumption declaration text from an existing payload is distinct from rendering the final indented human line.

## Before

`_format_diagnostic_surface_consumption(...)` compressed two responsibilities:

1. DiagnosticSurface consumption declaration text preparation:
   - accept an existing consumption payload;
   - treat non-dictionary payloads as `unknown`;
   - treat missing, empty, or non-dictionary `declared_consumption` values as `unknown`;
   - join known declarations into the existing semicolon-separated display text.
2. DiagnosticSurface consumption line rendering:
   - apply the caller-provided indentation;
   - apply the `diagnostic_surface_consumption:` label;
   - return the final human-readable line consumed by existing definition and explanation output.

Behavior was correct, but the declaration-text preparation responsibility was implicit inside line rendering.

## After

A private implementation-local text-preparation owner now exists:

- `_DiagnosticSurfaceConsumptionText`
- `_prepare_diagnostic_surface_consumption_text(...)`

`_format_diagnostic_surface_consumption(...)` now asks that producer for the existing consumption declaration display text and then continues to render the unchanged human-readable line.

## Recovered producer

`_prepare_diagnostic_surface_consumption_text(...)` is the recovered producer. It consumes an existing DiagnosticSurface consumption payload and produces only the human consumption declaration text already used by existing human renderers.

## Recovered artifact/helper

`_DiagnosticSurfaceConsumptionText` is the recovered private artifact. It carries only the prepared `text` value and does not carry DiagnosticSurface identity, definition payloads, explanation payloads, boundary facts, registration status, indentation, line labels, JSON authority, diagnostic authority, or CLI authority.

## Recovered consumer

The immediate consumer is `_format_diagnostic_surface_consumption(...)`.

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

DiagnosticSurface consumption declaration text preparation and DiagnosticSurface consumption line rendering were previously compressed inside `_format_diagnostic_surface_consumption(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Consumption Declaration Text Preparation
        !=
DiagnosticSurface Consumption Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_consumption_text(...)` now owns the recovered consumption declaration text-preparation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceConsumptionText` carries the prepared consumption declaration text. It is a private implementation-local artifact.

### 5. Who consumes it?

`_format_diagnostic_surface_consumption(...)` consumes the prepared text before producing the unchanged human-readable consumption line. Existing definition and explanation human output consume that line through their existing calls.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_013.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 20 +++++++++++++++++---
tests/test_diagnostic_inventory.py   | 34 ++++++++++++++++++++++++++++++++++
2 files changed, 51 insertions(+), 3 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
55 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- human-readable DiagnosticSurface definition line assembly;
- human-readable DiagnosticSurface explanation line assembly;
- DiagnosticSurface boundary identification from inventory entry fields;
- DiagnosticSurface consumption identification from inventory entry fields;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local consumption declaration text-preparation path.

Those responsibilities remain compressed unless future implementation evidence independently supports another local recovery.
