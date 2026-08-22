# Competency Interrogation Slice 006

## Selected boundary

Recovered exactly one implementation-local DiagnosticSurface ownership boundary:

```text
Diagnostic Surface Shape Registration Identification
        !=
Diagnostic Surface Definition Composition
```

This slice recovers only the smallest neighboring compression exposed by implementation evidence in the DiagnosticSurface definition path. It does not implement the Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, planner, scheduler, orchestration layer, or diagnostic-surface redesign.

## Implementation evidence

Representative implementation evidence was concentrated in `seed_runtime/diagnostic_inventory.py`:

- `build_diagnostic_surface_definition(...)` already composes the public JSON-compatible DiagnosticSurface definition.
- Prior slices recovered adjacent implementation-local boundary and consumption identification before presentation.
- The remaining neighboring call `_shape_registration_status(entry.name)` still performed shape-registration lookup directly for definition composition.
- The existing public field `shape_registration_status` already represented a distinct fact from diagnostic inventory registration, boundary statements, consumption fields, CLI flags, descriptions, record behavior, and rendering.
- The lookup was bounded to static diagnostic shape-audit registration evidence and returned only the existing public status values: `present` or `absent`.

The implementation therefore exposed a small local ownership boundary: shape-registration identification can be owned before the DiagnosticSurface definition composer places the unchanged status into the public report.

## Before

`build_diagnostic_surface_definition(...)` directly called `_shape_registration_status(entry.name)` while composing the public DiagnosticSurface definition. That compressed two responsibilities:

1. identifying whether the diagnostic surface is present in static diagnostic shape-audit implementation specs;
2. composing the already-identified status into the existing `shape_registration_status` report field.

The behavior was correct, but the identification responsibility existed only as a direct composition-time lookup.

## After

A private implementation-local shape-registration owner now exists:

- `_DiagnosticSurfaceShapeRegistrationIdentification`
- `_identify_diagnostic_surface_shape_registration(...)`

`build_diagnostic_surface_definition(...)` now consumes the recovered identification through `_diagnostic_surface_shape_registration_status(...)` and preserves the unchanged public `shape_registration_status` string.

## Recovered producer

`_identify_diagnostic_surface_shape_registration(...)` is the recovered producer. It consumes a diagnostic surface name, checks static diagnostic shape-audit implementation specs, and produces only the implementation-local shape-registration status.

## Recovered artifact/helper

`_DiagnosticSurfaceShapeRegistrationIdentification` is the recovered private artifact/helper. It carries only:

- `status`

It intentionally does not carry public DiagnosticSurface identity, CLI flags, descriptions, inventory registration, boundary statements, consumption declarations, record behavior, event-ledger behavior, JSON wrapper names, or human-readable rendering.

## Recovered consumer

`_diagnostic_surface_shape_registration_status(...)` consumes `_DiagnosticSurfaceShapeRegistrationIdentification` and exposes the unchanged status string to `build_diagnostic_surface_definition(...)`.

`build_diagnostic_surface_definition(...)` remains the public report composer for the existing DiagnosticSurface definition shape.

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

- `seed --diagnostic-surface-definition ... --json`
- `seed --diagnostic-surface-definition ...`
- `seed --diagnostic-surface-explanation ... --json`
- `seed --diagnostic-surface-explanation ...`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

## Required questions

### 1. What responsibilities were previously compressed?

Diagnostic surface shape-registration identification and DiagnosticSurface definition composition were previously compressed at the `shape_registration_status` lookup site inside `build_diagnostic_surface_definition(...)`.

### 2. Which implementation-local boundary became directly observable?

```text
Diagnostic Surface Shape Registration Identification
        !=
Diagnostic Surface Definition Composition
```

### 3. What producer now owns the recovered responsibility?

`_identify_diagnostic_surface_shape_registration(...)` now owns the recovered shape-registration-identification responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceShapeRegistrationIdentification` carries the recovered shape-registration status before definition composition.

### 5. Who consumes it?

`_diagnostic_surface_shape_registration_status(...)` consumes `_DiagnosticSurfaceShapeRegistrationIdentification` and returns the unchanged status string. `build_diagnostic_surface_definition(...)` consumes that string as the existing `shape_registration_status` field.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_006.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 24 +++++++++++++++++++++---
tests/test_diagnostic_inventory.py   | 21 +++++++++++++++++++++
2 files changed, 42 insertions(+), 3 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
49 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- unknown DiagnosticSurface definition fallback composition;
- DiagnosticSurface definition report assembly;
- DiagnosticSurface explanation report assembly;
- human-readable rendering of boundary and consumption reports;
- diagnostic inventory composition and sorting;
- broader diagnostic identity, capability, responsibility, or inquiry-boundary analysis outside this local DiagnosticSurface shape-registration path.

Those responsibilities remain compressed unless future implementation evidence independently supports another local recovery.
