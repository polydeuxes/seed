# Competency Interrogation Slice 007

## Selected boundary

Recovered exactly one implementation-local DiagnosticSurface ownership boundary:

```text
Unknown DiagnosticSurface Definition Production
        !=
DiagnosticSurface Definition Wrapper Composition
```

This slice follows the implementation immediately adjacent to the completed DiagnosticSurface recoveries. It does not implement the Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, planner, scheduler, orchestration layer, or diagnostic-surface redesign.

## Implementation evidence

Implementation evidence was concentrated in `seed_runtime/diagnostic_inventory.py`:

- `build_diagnostic_surface_definition(...)` already handled two distinct paths: a known diagnostic inventory entry and an unknown diagnostic surface fallback.
- The known path already consumed recovered local facts for boundary, consumption, and shape-registration status before composing the public `diagnostic_surface_definition` wrapper.
- The unknown path still embedded the complete unknown DiagnosticSurface definition directly inside the wrapper returned by `build_diagnostic_surface_definition(...)`.
- The embedded unknown fallback was stable public compatibility data: `status=unknown`, empty `cli_flags`, unknown support fields, unknown boundary/consumption payloads, absent inventory registration, unknown shape-registration status, and the existing implementation reason.
- No implementation evidence required a new framework, grammar, registry, methodology owner, planner, scheduler, or global diagnostic owner.

The directly observable pressure was therefore local and narrow: producing the unknown DiagnosticSurface definition payload can be separated from wrapping that payload under the public `diagnostic_surface_definition` key.

## Before

`build_diagnostic_surface_definition(...)` directly composed the unknown fallback payload and the public wrapper in the same branch when no diagnostic inventory entry matched the requested surface.

That compressed two responsibilities:

1. producing the implementation-local unknown DiagnosticSurface definition payload;
2. composing the public `diagnostic_surface_definition` wrapper around a definition payload.

The behavior was correct, but the unknown definition payload did not have a local owner before wrapper composition.

## After

A private implementation-local unknown definition owner now exists:

- `_UnknownDiagnosticSurfaceDefinition`
- `_produce_unknown_diagnostic_surface_definition(...)`

A private wrapper helper now carries the existing public envelope responsibility:

- `_diagnostic_surface_definition_wrapper(...)`

`build_diagnostic_surface_definition(...)` now consumes the recovered unknown definition producer for the missing-entry branch and preserves the unchanged public JSON shape.

## Recovered producer

`_produce_unknown_diagnostic_surface_definition(...)` is the recovered producer. It consumes only the requested diagnostic surface name and produces the private unknown DiagnosticSurface definition artifact.

## Recovered artifact/helper

`_UnknownDiagnosticSurfaceDefinition` is the recovered private artifact. It carries the unchanged unknown definition payload before wrapper composition.

`_diagnostic_surface_definition_wrapper(...)` is the local helper that places the artifact's unchanged dictionary under the existing public `diagnostic_surface_definition` key.

## Recovered consumer

`build_diagnostic_surface_definition(...)` consumes `_produce_unknown_diagnostic_surface_definition(...)` only when the requested diagnostic surface has no diagnostic inventory entry. It then passes the artifact to `_diagnostic_surface_definition_wrapper(...)` and returns the same public report shape as before.

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

- `seed --diagnostic-surface-definition missing --json`
- `seed --diagnostic-surface-definition missing`
- `seed --diagnostic-surface-explanation missing --json`
- `seed --diagnostic-surface-explanation missing`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

## Required questions

### 1. What responsibilities were previously compressed?

Unknown DiagnosticSurface definition production and public `diagnostic_surface_definition` wrapper composition were previously compressed in the missing-entry branch of `build_diagnostic_surface_definition(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
Unknown DiagnosticSurface Definition Production
        !=
DiagnosticSurface Definition Wrapper Composition
```

### 3. What producer now owns the recovered responsibility?

`_produce_unknown_diagnostic_surface_definition(...)` now owns the recovered unknown definition production responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_UnknownDiagnosticSurfaceDefinition` carries the unknown definition payload. `_diagnostic_surface_definition_wrapper(...)` carries the unchanged public wrapper composition helper.

### 5. Who consumes it?

`build_diagnostic_surface_definition(...)` consumes the producer in the unknown-surface branch and returns the helper-composed public wrapper.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_007.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 76 +++++++++++++++++++++++-------------
tests/test_diagnostic_inventory.py   | 37 ++++++++++++++++++
2 files changed, 86 insertions(+), 27 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
50 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- known DiagnosticSurface definition payload composition;
- DiagnosticSurface explanation report assembly;
- human-readable rendering of boundary and consumption reports;
- diagnostic inventory composition and sorting;
- broader diagnostic identity, capability, responsibility, or inquiry-boundary analysis outside this local unknown DiagnosticSurface definition path.

Those responsibilities remain compressed unless future implementation evidence independently supports another local recovery.
