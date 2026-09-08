# Competency Interrogation Slice 097

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Implementation Reason Value Preparation
        !=
DiagnosticSurface Definition Implementation Reason Line Rendering
```

This slice begins immediately adjacent to Slice 096 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface definition evidence-source value preparation was recovered, the next neighboring DiagnosticSurface definition metadata line still extracted `definition["implementation_reason"]` from inside the definition-specific implementation-reason line renderer instead of consuming a prepared definition implementation-reason value artifact.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface definition human rendering path:

- `_assemble_diagnostic_surface_definition_line_set(...)` prepares definition display artifacts before producing the human definition line set.
- `_render_diagnostic_surface_definition_implementation_reason_line(...)` already exists as the definition-specific producer for the rendered top-level `implementation_reason:` line consumed by definition line-set assembly.
- Neighboring definition fields expose the recurring implementation-local pattern of preparing display values before line rendering, including description text, JSON support value, record support value, record scope value, and Slice 096's evidence-source value.
- Before this slice, definition implementation-reason value preparation remained compressed inside `_render_diagnostic_surface_definition_implementation_reason_line(...)` through direct extraction from `definition["implementation_reason"]`.
- Existing human definition output proves the rendered implementation-reason line is consumed only as one member of the definition line set.

The directly observable recurring local pattern is that the definition line-set assembler should consume a prepared implementation-reason value artifact before asking the definition implementation-reason line renderer to render the implementation-reason line.

## Before

The DiagnosticSurface definition implementation-reason line renderer compressed two responsibilities:

1. DiagnosticSurface definition implementation-reason value preparation:
   - extract the existing `implementation_reason` value from the definition dictionary;
   - preserve the existing line text without changing JSON output, schema, diagnostics, event-ledger behavior, cluster mutation behavior, or public CLI behavior.
2. DiagnosticSurface definition implementation-reason line rendering:
   - render the existing top-level `implementation_reason: <reason>` line from the prepared implementation-reason value, prepared field label, and selected top-level field indent;
   - preserve the existing `_DiagnosticSurfaceImplementationReasonLine` artifact and human output.

Behavior was correct, but definition implementation-reason value preparation remained compressed inside definition implementation-reason line rendering.

## After

`_assemble_diagnostic_surface_definition_line_set(...)` now prepares `_DiagnosticSurfaceImplementationReasonValue` through `_prepare_diagnostic_surface_definition_implementation_reason_value(...)` before passing the unchanged value to `_render_diagnostic_surface_definition_implementation_reason_line(...)`.

`_render_diagnostic_surface_definition_implementation_reason_line(...)` now receives an already prepared definition implementation-reason value while preserving its existing line-rendering behavior. `_render_diagnostic_surface_implementation_reason_line(...)` remains unchanged.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_prepare_diagnostic_surface_definition_implementation_reason_value(...)` is the recovered producer for DiagnosticSurface definition implementation-reason value preparation. It produces the implementation-local `_DiagnosticSurfaceImplementationReasonValue` artifact.

## Recovered artifact/helper

The recovered helper is `_prepare_diagnostic_surface_definition_implementation_reason_value(...)`.

The recovered artifact is `_DiagnosticSurfaceImplementationReasonValue`, which carries the existing `implementation_reason` value between definition line-set assembly and definition implementation-reason line rendering.

It does not carry DiagnosticSurface definition identity heading rendering authority, definition status line rendering authority, definition CLI flags line rendering authority, definition description text preparation authority, definition description line rendering authority, definition JSON support value preparation authority, definition JSON support line rendering authority, definition record support value preparation authority, definition record support line rendering authority, definition record scope value preparation authority, definition record scope line rendering authority, definition boundary text preparation authority, definition boundary line rendering authority, definition consumption text preparation authority, definition consumption field label preparation authority, definition consumption line rendering authority, definition inventory registration field label preparation authority, definition inventory registration line rendering authority, definition shape-registration status field label preparation authority, definition shape-registration status line rendering authority, definition implementation-reason field label preparation authority, definition implementation-reason field label rendering authority, definition evidence-source value preparation authority, definition evidence-source field label preparation authority, definition evidence-source line rendering authority, top-level field indent selection authority, explanation rendering authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_definition_implementation_reason_line(...)`

The upstream assembler that prepares and passes the artifact is:

- `_assemble_diagnostic_surface_definition_line_set(...)`

Downstream existing consumers remain unchanged:

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

DiagnosticSurface definition implementation-reason value preparation and DiagnosticSurface definition implementation-reason line rendering were previously compressed inside definition implementation-reason line rendering through direct extraction from `definition["implementation_reason"]`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Implementation Reason Value Preparation
        !=
DiagnosticSurface Definition Implementation Reason Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_definition_implementation_reason_value(...)` now owns the recovered DiagnosticSurface definition implementation-reason value preparation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_prepare_diagnostic_surface_definition_implementation_reason_value(...)` carries the recovered helper boundary, and `_DiagnosticSurfaceImplementationReasonValue` carries the prepared implementation-reason value.

### 5. Who consumes it?

`_render_diagnostic_surface_definition_implementation_reason_line(...)` consumes `_DiagnosticSurfaceImplementationReasonValue.value` before returning the unchanged `_DiagnosticSurfaceImplementationReasonLine` artifact to definition line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_097.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 24 +++++++++++++++++++++---
tests/test_diagnostic_inventory.py   | 13 ++++++++++++-
2 files changed, 33 insertions(+), 4 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition identity heading line production, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description line rendering, definition JSON support value preparation, definition JSON support line rendering, definition record support value preparation, definition record support line rendering, definition record scope value preparation, definition record scope line rendering, definition boundary text preparation, definition boundary line rendering, definition consumption text preparation, definition consumption field label preparation, definition consumption line rendering, definition inventory registration field label preparation, definition inventory registration line rendering, definition shape-registration status field label preparation, definition shape-registration status line rendering, definition implementation-reason field label preparation, definition implementation-reason value preparation, definition implementation-reason line rendering, definition evidence-source field label preparation, definition evidence-source value preparation, definition evidence-source line rendering, top-level field indent selection, definition section label rendering, definition section indent rendering, and definition field label preparation outside this recovered definition-specific implementation-reason value path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flag display preparation, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display, description text preparation, JSON support value preparation, record support value preparation, record scope value preparation, consumption field label preparation, inventory registration field label preparation, shape-registration status field label preparation, implementation-reason field label preparation, implementation-reason value preparation, evidence-source field label preparation, and evidence-source value preparation;
- DiagnosticSurface implementation-reason formatter coordination beyond definition implementation-reason value preparation and line rendering;
- DiagnosticSurface evidence-source formatter coordination beyond definition evidence-source value preparation and line rendering;
- DiagnosticSurface shape-registration formatter coordination beyond status identification, definition shape-registration status field label preparation, and line rendering;
- DiagnosticSurface inventory registration formatter coordination beyond definition inventory registration field label preparation and line rendering;
- DiagnosticSurface consumption formatter coordination beyond definition consumption field label preparation, definition consumption line rendering, explanation consumption text preparation, explanation consumption field label preparation, explanation consumption line rendering, line rendering, and declaration-sequence extraction;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local definition implementation-reason value preparation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
