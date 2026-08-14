# Competency Interrogation Slice 008

## Selected boundary

Recovered exactly one implementation-local DiagnosticSurface ownership boundary:

```text
Known DiagnosticSurface Definition Production
        !=
DiagnosticSurface Definition Wrapper Composition
```

This slice follows the implementation immediately adjacent to the completed DiagnosticSurface recoveries. It does not implement the Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, planner, scheduler, orchestration layer, or diagnostic-surface redesign.

## Implementation evidence

Implementation evidence was concentrated in `seed_runtime/diagnostic_inventory.py`:

- `build_diagnostic_surface_definition(...)` already had a known diagnostic-inventory-entry path and an unknown diagnostic-surface path.
- Slice 007 had already separated unknown DiagnosticSurface definition production from the public `diagnostic_surface_definition` wrapper.
- The known path still produced the complete known DiagnosticSurface definition payload directly at the wrapper return site.
- The known payload already consumed previously recovered local facts: boundary identification, consumption identification, and shape-registration identification.
- The known payload was stable public compatibility data: `status=known`, diagnostic identity, CLI flags, description, JSON and record fields, record scope, boundary payload, consumption payload, inventory registration, shape-registration status, evidence source, and implementation reason.
- No implementation evidence required a new global registry, diagnostic framework, runtime grammar, planner, scheduler, or methodology owner.

The directly observable pressure was therefore local and narrow: producing a known DiagnosticSurface definition from one diagnostic inventory entry can be separated from wrapping any produced definition under the existing public `diagnostic_surface_definition` key.

## Before

`build_diagnostic_surface_definition(...)` directly composed the known DiagnosticSurface definition payload and returned the public wrapper in the same branch when a diagnostic inventory entry matched the requested surface.

That compressed two responsibilities:

1. producing the implementation-local known DiagnosticSurface definition payload from an inventory entry plus already-recovered local facts;
2. composing the public `diagnostic_surface_definition` wrapper around a definition payload.

The behavior was correct, but known definition production had no local owner before wrapper composition.

## After

A private implementation-local known definition owner now exists:

- `_KnownDiagnosticSurfaceDefinition`
- `_produce_known_diagnostic_surface_definition(...)`

The existing wrapper helper now accepts either known or unknown local definition artifacts and continues to place the unchanged dictionary under the existing public `diagnostic_surface_definition` key.

`build_diagnostic_surface_definition(...)` now consumes the recovered known definition producer for the matched-entry branch and preserves the unchanged public JSON and human-readable output shape.

## Recovered producer

`_produce_known_diagnostic_surface_definition(...)` is the recovered producer. It consumes one `DiagnosticInventoryEntry`, invokes the existing implementation-local boundary, consumption, and shape-registration producers, and produces only the private known DiagnosticSurface definition artifact.

## Recovered artifact/helper

`_KnownDiagnosticSurfaceDefinition` is the recovered private artifact. It carries:

- the source diagnostic inventory entry;
- the recovered boundary identification;
- the recovered consumption identification;
- the recovered shape-registration identification.

`_diagnostic_surface_definition_wrapper(...)` remains the local helper that places a known or unknown definition artifact's unchanged dictionary under the existing public `diagnostic_surface_definition` key.

## Recovered consumer

`build_diagnostic_surface_definition(...)` consumes `_produce_known_diagnostic_surface_definition(...)` when the requested diagnostic surface has a diagnostic inventory entry. It then passes the artifact to `_diagnostic_surface_definition_wrapper(...)` and returns the same public report shape as before.

`build_diagnostic_surface_explanation(...)`, `diagnostic_surface_definition_json(...)`, and `format_diagnostic_surface_definition(...)` remain downstream consumers of the unchanged public definition payload.

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

- `seed --diagnostic-surface-definition diagnostic_shape_audit --json`
- `seed --diagnostic-surface-definition diagnostic_shape_audit`
- `seed --diagnostic-surface-definition missing --json`
- `seed --diagnostic-surface-explanation diagnostic_shape_audit --json`
- `seed --diagnostic-surface-explanation missing --json`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

## Required questions

### 1. What responsibilities were previously compressed?

Known DiagnosticSurface definition production and public `diagnostic_surface_definition` wrapper composition were previously compressed in the matched-entry branch of `build_diagnostic_surface_definition(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
Known DiagnosticSurface Definition Production
        !=
DiagnosticSurface Definition Wrapper Composition
```

### 3. What producer now owns the recovered responsibility?

`_produce_known_diagnostic_surface_definition(...)` now owns the recovered known definition production responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_KnownDiagnosticSurfaceDefinition` carries the known definition payload inputs before wrapper composition. `_diagnostic_surface_definition_wrapper(...)` carries the unchanged public wrapper composition helper.

### 5. Who consumes it?

`build_diagnostic_surface_definition(...)` consumes the producer in the known-surface branch and returns the helper-composed public wrapper. Existing JSON, human-readable definition, and DiagnosticSurface explanation consumers consume the unchanged public payload.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_008.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 142 ++++++++++++++++++++++-------------
tests/test_diagnostic_inventory.py   | 100 +++++++++++++++++-------
2 files changed, 165 insertions(+), 77 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
51 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface explanation report assembly;
- human-readable rendering of boundary and consumption reports;
- diagnostic inventory composition and sorting;
- broader diagnostic identity, capability, responsibility, or inquiry-boundary analysis outside this local known DiagnosticSurface definition path.

Those responsibilities remain compressed unless future implementation evidence independently supports another local recovery.
