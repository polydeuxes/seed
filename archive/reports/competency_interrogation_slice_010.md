# Competency Interrogation Slice 010

## Selected boundary

Recovered exactly one implementation-local DiagnosticSurface ownership boundary:

```text
DiagnosticSurface Explanation Composition
        !=
DiagnosticSurface Explanation Wrapper Composition
```

This slice follows implementation evidence immediately adjacent to the completed DiagnosticSurface definition recoveries. It does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, router, planner, scheduler, orchestration layer, methodology owner, or diagnostic-surface redesign.

## Implementation evidence

Implementation evidence was concentrated in `seed_runtime/diagnostic_inventory.py`:

- `build_diagnostic_surface_explanation(...)` already consumed the existing `diagnostic_surface_definition` payload and selected only three existing fields for explanation output: the full definition, the definition's boundary, and the definition's consumption.
- The same function also wrapped that selected explanation payload under the public `diagnostic_surface_explanation` key.
- The diagnostic inventory entry for `diagnostic_surface_explanation` states that the surface composes existing DiagnosticSurface definition, boundary, and consumption explanation fields without discovery, inference, reasoning, recording, event-ledger writes, or cluster mutation.
- Existing tests already proved public JSON, human output, unknown-surface behavior, inventory visibility, and guardrails for this surface.
- No evidence required a new global explanation framework, runtime grammar, planner, scheduler, registry, router, methodology owner, or broader diagnostic framework.

The directly observable pressure was narrow: selecting the existing definition/boundary/consumption fields that make up a DiagnosticSurface explanation is a local composition responsibility distinct from placing that payload under the unchanged public wrapper key.

## Before

`build_diagnostic_surface_explanation(...)` directly mixed two responsibilities:

1. DiagnosticSurface explanation composition:
   - consume an existing DiagnosticSurface definition payload;
   - carry the unchanged definition;
   - select the existing `diagnostic_surface_boundary` field;
   - select the existing `diagnostic_surface_consumption` field.
2. Public wrapper composition:
   - place the composed explanation under the `diagnostic_surface_explanation` JSON key.

Behavior was correct, but the local producer of the explanation payload was implicit inside the public wrapper return value.

## After

A private implementation-local explanation composition owner now exists:

- `_DiagnosticSurfaceExplanationComposition`
- `_compose_diagnostic_surface_explanation(...)`

A narrow wrapper helper now owns only the unchanged public wrapper key:

- `_diagnostic_surface_explanation_wrapper(...)`

`build_diagnostic_surface_explanation(...)` now obtains the existing definition payload, asks the recovered producer to compose the explanation payload, and passes that artifact to the wrapper helper.

## Recovered producer

`_compose_diagnostic_surface_explanation(...)` is the recovered producer. It consumes an existing DiagnosticSurface definition payload and produces only the private explanation composition artifact.

## Recovered artifact/helper

`_DiagnosticSurfaceExplanationComposition` is the recovered private artifact. It carries only the existing definition payload and projects the unchanged explanation fields from it:

- `diagnostic_surface_definition`
- `diagnostic_surface_boundary`
- `diagnostic_surface_consumption`

`_diagnostic_surface_explanation_wrapper(...)` is the local helper that preserves the public wrapper shape.

## Recovered consumer

`build_diagnostic_surface_explanation(...)` consumes `_compose_diagnostic_surface_explanation(...)` and `_diagnostic_surface_explanation_wrapper(...)` to return the unchanged public `diagnostic_surface_explanation` payload.

Downstream consumers remain unchanged:

- `diagnostic_surface_explanation_json(...)`
- `format_diagnostic_surface_explanation(...)`
- CLI handling for `seed --diagnostic-surface-explanation`

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

- `seed --diagnostic-surface-explanation diagnostic_shape_audit --json`
- `seed --diagnostic-surface-explanation diagnostic_shape_audit`
- `seed --diagnostic-surface-explanation missing_surface --json`
- `seed --diagnostic-surface-definition diagnostic_shape_audit --json`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

## Required questions

### 1. What responsibilities were previously compressed?

DiagnosticSurface explanation composition and public `diagnostic_surface_explanation` wrapper composition were previously compressed in `build_diagnostic_surface_explanation(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Explanation Composition
        !=
DiagnosticSurface Explanation Wrapper Composition
```

### 3. What producer now owns the recovered responsibility?

`_compose_diagnostic_surface_explanation(...)` now owns the recovered explanation composition responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceExplanationComposition` carries the composed explanation payload before wrapper composition. `_diagnostic_surface_explanation_wrapper(...)` carries the unchanged public wrapper helper.

### 5. Who consumes it?

`build_diagnostic_surface_explanation(...)` consumes the recovered composition artifact and wrapper helper. Existing JSON, human-readable explanation, and CLI consumers consume the unchanged public payload.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_010.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 42 ++++++++++++++++++++++++++++--------
tests/test_diagnostic_inventory.py   | 26 ++++++++++++++++++++++
2 files changed, 59 insertions(+), 9 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
52 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- human-readable DiagnosticSurface definition rendering;
- human-readable DiagnosticSurface explanation rendering;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, or explanation semantics outside this local DiagnosticSurface explanation-composition path.

Those responsibilities remain compressed unless future implementation evidence independently supports another local recovery.
