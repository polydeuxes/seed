# Competency Interrogation Slice 014

## Selected boundary

Recovered exactly one implementation-local DiagnosticSurface ownership boundary:

```text
DiagnosticSurface Shape Registration Lookup
        !=
DiagnosticSurface Shape Registration Status Identification
```

This slice begins immediately adjacent to Slice 013 in `seed_runtime/diagnostic_inventory.py`. The current Diagnostic Surface neighborhood was not exhausted: after consumption declaration text preparation was separated from consumption line rendering, the same local definition-production path exposed a separate compressed responsibility in `_identify_diagnostic_surface_shape_registration(...)`. The evidence is implementation-local and does not require Competency Interrogation Grammar, a framework, engine, registry, router, planner, scheduler, orchestration layer, methodology owner, constitutional abstraction, diagnostic framework, or architectural redesign.

## Implementation evidence

Implementation evidence was concentrated in `_identify_diagnostic_surface_shape_registration(...)`:

- The function imported `IMPLEMENTATION_SPECS` from the existing diagnostic shape-audit implementation.
- It checked whether the requested diagnostic name was present in that existing shape-audit implementation spec set.
- It converted the boolean presence result into the public status vocabulary used by the existing DiagnosticSurface definition payload: `present` or `absent`.
- The resulting `_DiagnosticSurfaceShapeRegistrationIdentification` is consumed by `_produce_known_diagnostic_surface_definition(...)`, then by `_KnownDiagnosticSurfaceDefinition.to_json_dict(...)`, and then by existing JSON and human DiagnosticSurface definition and explanation surfaces.
- The lookup responsibility has no authority over JSON shape, inventory registration, shape-audit registration contents, event-ledger behavior, cluster mutation behavior, CLI flags, or DiagnosticSurface rendering.

The observable pressure was therefore narrow: checking existing shape-audit registration presence is distinct from identifying the DiagnosticSurface shape-registration status vocabulary.

## Before

`_identify_diagnostic_surface_shape_registration(...)` compressed two responsibilities:

1. DiagnosticSurface shape registration lookup:
   - import the existing `IMPLEMENTATION_SPECS` from `seed_runtime.diagnostic_shape_audit`;
   - determine whether a diagnostic name is present in that shape-audit implementation declaration set.
2. DiagnosticSurface shape registration status identification:
   - translate lookup presence into the existing `present` or `absent` status value;
   - return `_DiagnosticSurfaceShapeRegistrationIdentification` for definition composition.

Behavior was correct, but shape-audit presence lookup was implicit inside status identification.

## After

A private implementation-local lookup owner now exists:

- `_DiagnosticSurfaceShapeRegistrationLookup`
- `_lookup_diagnostic_surface_shape_registration(...)`

`_identify_diagnostic_surface_shape_registration(...)` now asks that producer for the existing registration presence fact and then continues to identify the unchanged `present` or `absent` status.

## Recovered producer

`_lookup_diagnostic_surface_shape_registration(...)` is the recovered producer. It consumes a diagnostic name and produces only the implementation-local boolean registration presence fact from the existing shape-audit implementation specs.

## Recovered artifact/helper

`_DiagnosticSurfaceShapeRegistrationLookup` is the recovered private artifact. It carries only the `present` value and does not carry DiagnosticSurface identity, definition payloads, explanation payloads, boundary facts, consumption facts, status vocabulary, indentation, line labels, JSON authority, diagnostic authority, CLI authority, event-ledger authority, or cluster mutation authority.

## Recovered consumer

The immediate consumer is `_identify_diagnostic_surface_shape_registration(...)`.

Downstream existing consumers remain unchanged:

- `_produce_known_diagnostic_surface_definition(...)`
- `_KnownDiagnosticSurfaceDefinition.to_json_dict(...)`
- `diagnostic_surface_definition_json(...)`
- `diagnostic_surface_explanation_json(...)`
- `format_diagnostic_surface_definition(...)`
- `format_diagnostic_surface_explanation(...)`
- `seed --diagnostic-surface-definition <surface>`
- `seed --diagnostic-surface-explanation <surface>`

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

DiagnosticSurface shape registration lookup and DiagnosticSurface shape registration status identification were previously compressed inside `_identify_diagnostic_surface_shape_registration(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Shape Registration Lookup
        !=
DiagnosticSurface Shape Registration Status Identification
```

### 3. What producer now owns the recovered responsibility?

`_lookup_diagnostic_surface_shape_registration(...)` now owns the recovered shape registration lookup responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceShapeRegistrationLookup` carries the shape-audit registration presence fact. It is a private implementation-local artifact.

### 5. Who consumes it?

`_identify_diagnostic_surface_shape_registration(...)` consumes the lookup before producing the unchanged shape registration status identification. Existing definition and explanation outputs consume that status through their existing calls.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_014.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 20 ++++++++++++++++++--
tests/test_diagnostic_inventory.py   | 15 +++++++++++++++
2 files changed, 33 insertions(+), 2 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
56 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- human-readable DiagnosticSurface definition line assembly;
- human-readable DiagnosticSurface explanation line assembly;
- DiagnosticSurface boundary identification from inventory entry fields;
- DiagnosticSurface consumption identification from inventory entry fields;
- DiagnosticSurface shape registration status presentation;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local shape registration lookup path.

The current Diagnostic Surface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
