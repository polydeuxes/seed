# Competency Interrogation Slice 122

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Implementation-Reason Source Extraction
        !=
DiagnosticSurface Implementation-Reason Value Production
```

This slice begins immediately adjacent to Slice 121 in `seed_runtime/diagnostic_inventory.py`. After the generic shape-registration-status field-label producer was recovered before generic shape-registration-status line rendering, the next adjacent implementation-local responsibility appears in the definition human rendering path: the definition-specific implementation-reason helper still constructed the implementation-reason value artifact directly even though the generic implementation-reason value producer already existed immediately below the definition-specific renderer neighborhood.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, or CLI behavior.

## Implementation evidence

Implementation evidence is concentrated around the DiagnosticSurface definition implementation-reason human rendering path:

- `_DiagnosticSurfaceImplementationReasonValue` already exists as the implementation-local artifact for implementation-reason values before line rendering.
- `_prepare_diagnostic_surface_implementation_reason_value(...)` already exists as the generic producer for that artifact.
- `_prepare_diagnostic_surface_definition_implementation_reason_value(...)` is the definition-specific preparation point that extracts `definition["implementation_reason"]` before `_render_diagnostic_surface_definition_implementation_reason_line(...)` delegates to the generic implementation-reason line renderer.
- Before this slice, the definition-specific helper compressed definition-field extraction with direct construction of `_DiagnosticSurfaceImplementationReasonValue`.
- Existing tests already exercised definition implementation-reason value preparation before definition line-set assembly, making the local producer boundary directly observable without changing output.

The directly observable recurring local pattern is that definition-specific helpers extract values from the definition payload while generic producers own reusable DiagnosticSurface value-artifact construction.

## Before

The definition DiagnosticSurface implementation-reason path compressed two responsibilities:

1. DiagnosticSurface definition implementation-reason source extraction:
   - read the existing `implementation_reason` field from the definition payload;
   - preserve the existing definition-specific path into human rendering.
2. DiagnosticSurface implementation-reason value production:
   - construct `_DiagnosticSurfaceImplementationReasonValue` for line rendering.

Behavior was correct, but the definition-specific extraction helper still owned the generic value-artifact construction that the adjacent generic implementation-reason producer already made observable.

## After

`_prepare_diagnostic_surface_definition_implementation_reason_value(...)` now only extracts `definition["implementation_reason"]` and delegates value-artifact production to `_prepare_diagnostic_surface_implementation_reason_value(...)`.

`_prepare_diagnostic_surface_implementation_reason_value(...)` remains the recovered producer for `_DiagnosticSurfaceImplementationReasonValue`.

No public output, JSON shape, CLI behavior, diagnostics, event-ledger behavior, cluster mutation behavior, schema, or compatibility boundary changed.

## Recovered producer

`_prepare_diagnostic_surface_implementation_reason_value(...)` is the recovered producer for DiagnosticSurface implementation-reason value production.

## Recovered artifact/helper

The recovered artifact is the already-existing `_DiagnosticSurfaceImplementationReasonValue`, which carries the existing implementation-reason value into implementation-reason line rendering.

The recovered helper is `_prepare_diagnostic_surface_implementation_reason_value(...)`.

It does not carry definition-field extraction authority, implementation-reason line rendering authority, definition line-set assembly authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_prepare_diagnostic_surface_definition_implementation_reason_value(...)`

Downstream existing consumers remain unchanged:

- `_render_diagnostic_surface_definition_implementation_reason_line(...)`
- `_assemble_diagnostic_surface_definition_line_set(...)`
- `format_diagnostic_surface_definition(...)`
- `seed --diagnostic-surface-definition <surface>`

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

DiagnosticSurface definition implementation-reason source extraction and DiagnosticSurface implementation-reason value production were previously compressed because `_prepare_diagnostic_surface_definition_implementation_reason_value(...)` both read `definition["implementation_reason"]` and directly constructed `_DiagnosticSurfaceImplementationReasonValue`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Implementation-Reason Source Extraction
        !=
DiagnosticSurface Implementation-Reason Value Production
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_implementation_reason_value(...)` now owns the recovered DiagnosticSurface implementation-reason value production responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceImplementationReasonValue` carries the prepared implementation-reason value, and `_prepare_diagnostic_surface_implementation_reason_value(...)` is the helper that produces it.

### 5. Who consumes it?

`_prepare_diagnostic_surface_definition_implementation_reason_value(...)` consumes the generic producer after extracting `definition["implementation_reason"]`; the unchanged definition implementation-reason renderer consumes the returned value artifact downstream.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_122.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 4 ++--
tests/test_diagnostic_inventory.py   | 6 ++++++
2 files changed, 8 insertions(+), 2 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition CLI flag display preparation, definition name value preparation, definition identity heading line rendering, definition status value preparation, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description field-label preparation, definition description line rendering, definition JSON support value preparation, definition JSON support field-label preparation, definition JSON support line rendering, definition record support value preparation, definition record support field-label preparation, definition record scope value preparation, definition record scope field-label preparation, definition boundary text preparation, definition boundary field-label production, definition boundary line rendering, definition consumption text preparation, definition consumption field-label production, definition consumption line rendering, definition inventory-registration value preparation, definition inventory-registration field-label production, definition inventory-registration line rendering, definition shape-registration status field-label production, definition shape-registration status value preparation, definition shape-registration status line rendering, definition implementation-reason field-label production, definition implementation-reason value source extraction, definition implementation-reason line rendering, definition evidence-source field-label production, definition evidence-source value preparation, and definition evidence-source line rendering outside this recovered implementation-reason value-production path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface shape-registration formatter coordination beyond definition shape-registration status value preparation, definition shape-registration status field-label production, definition shape-registration status line rendering, generic line rendering, shape-registration lookup, shape-registration status identification, generic shape-registration-status value production, and generic shape-registration-status field-label production;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local implementation-reason value-production path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
