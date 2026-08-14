# Competency Interrogation Slice 160

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Consumption Text Preparation
        !=
DiagnosticSurface Definition Consumption Line Rendering
```

This slice begins from the implementation immediately adjacent to Slice 159 in `seed_runtime/diagnostic_inventory.py` and `tests/test_diagnostic_inventory.py`. After the definition diagnostic-surface-boundary text preparation boundary became observable, the next adjacent definition line-set evidence is the definition diagnostic-surface-consumption text path in `_assemble_diagnostic_surface_definition_line_set(...)`.

`_prepare_diagnostic_surface_definition_consumption_text(...)` owns preparation of the definition diagnostic-surface-consumption text. `_render_diagnostic_surface_definition_consumption_line(...)` remains responsible only for rendering an already-prepared consumption text artifact with the existing field-label input into the definition diagnostic-surface-consumption line.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, CLI behavior, or JSON behavior.

## Implementation evidence

Implementation evidence is concentrated around the DiagnosticSurface definition consumption text path:

- `_assemble_diagnostic_surface_definition_line_set(...)` prepares `consumption_text` with `_prepare_diagnostic_surface_definition_consumption_text(definition)` before rendering definition lines.
- `_prepare_diagnostic_surface_definition_consumption_text(...)` returns the existing `_DiagnosticSurfaceConsumptionText` artifact by delegating to the generic diagnostic-surface-consumption text preparer with the existing `diagnostic_surface_consumption` payload from the definition.
- `_assemble_diagnostic_surface_definition_line_set(...)` passes `consumption_text` into `_render_diagnostic_surface_definition_consumption_line(...)`.
- `_render_diagnostic_surface_definition_consumption_line(...)` consumes the already-prepared consumption text as a rendering input and delegates final line rendering without owning definition consumption payload extraction or consumption text preparation.
- `test_diagnostic_surface_definition_consumption_line_rendering_precedes_line_set_assembly` now proves that the definition line-set assembly path contains the producer, consumer, and `consumption_text` handoff.

The directly observable recurring local pattern is that definition display values are prepared as dedicated implementation-local artifacts before line rendering consumes those artifacts.

## Before

The definition rendering path already produced the correct `diagnostic_surface_consumption` line, and existing behavior was correct. However, test evidence did not prove that the consumption text used by the definition diagnostic-surface-consumption line was produced by the dedicated definition consumption text preparer before line rendering consumed it.

Definition consumption text preparation and definition consumption line rendering were therefore compressed in the implementation evidence available to the test suite.

## After

`test_diagnostic_surface_definition_consumption_line_rendering_precedes_line_set_assembly` now proves that `_assemble_diagnostic_surface_definition_line_set(...)` calls `_prepare_diagnostic_surface_definition_consumption_text(...)` and passes `consumption_text` into the definition consumption line rendering path.

`_prepare_diagnostic_surface_definition_consumption_text(...)` remains the producer for definition consumption text preparation. The definition consumption line renderer remains responsible for rendering the line from the already-prepared consumption text artifact.

No public output, JSON shape, CLI behavior, diagnostics, event-ledger behavior, cluster mutation behavior, schema, or compatibility boundary changed.

## Recovered producer

`_prepare_diagnostic_surface_definition_consumption_text(...)` is the recovered producer for DiagnosticSurface definition consumption text preparation.

## Recovered artifact/helper

The recovered artifact is the already-existing `_DiagnosticSurfaceConsumptionText`, which carries the prepared definition consumption text.

The helper carrying the boundary is `_prepare_diagnostic_surface_definition_consumption_text(...)`, which prepares the definition consumption text before definition consumption line rendering.

It does not carry consumption field-label preparation authority, consumption line rendering authority, boundary text preparation authority, boundary field-label preparation authority, record scope value preparation authority, record support value preparation authority, JSON support value preparation authority, description text extraction authority, description field-label preparation authority, CLI flag display authority, status preparation authority, field indent selection authority, line-set ordering authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, or generalized rendering ownership.

## Recovered consumer

The immediate consumer is:

- `_assemble_diagnostic_surface_definition_line_set(...)`

Downstream existing consumers remain unchanged:

- `_render_diagnostic_surface_definition_consumption_line(...)`
- `_render_diagnostic_surface_consumption_line(...)`
- `format_diagnostic_surface_definition(...)`
- `seed --diagnostic-surface-definition <surface>`
- `seed --diagnostic-surface-definition <surface> --json` for the unchanged alternate JSON path

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

DiagnosticSurface definition consumption text preparation and DiagnosticSurface definition consumption line rendering were previously compressed in the test evidence because the test suite did not prove that the consumption renderer consumes a consumption text artifact prepared before rendering.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Consumption Text Preparation
        !=
DiagnosticSurface Definition Consumption Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_definition_consumption_text(...)` owns the recovered definition consumption text preparation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceConsumptionText` carries the prepared consumption text, and `_prepare_diagnostic_surface_definition_consumption_text(...)` is the helper that owns the definition consumption text preparation boundary.

### 5. Who consumes it?

`_assemble_diagnostic_surface_definition_line_set(...)` consumes the prepared consumption text artifact by passing `consumption_text` into `_render_diagnostic_surface_definition_consumption_line(...)`. The definition formatter and CLI definition surface consume the assembled line set downstream.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_160.md`

## LOC changed

Implementation and test diff before this report:

```text
tests/test_diagnostic_inventory.py | 6 ++++++
1 file changed, 6 insertions(+)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition consumption text preparation, definition boundary text preparation, definition record scope value preparation, definition record support value preparation, definition JSON support value preparation, definition description field-label preparation, definition description text preparation, definition CLI flag display preparation, definition name value preparation, and top-level definition field indent selection, including definition identity heading line rendering responsibilities outside prior recovered boundaries, definition status value preparation, definition status line rendering responsibilities outside prior recovered boundaries, definition CLI flags line rendering responsibilities outside prior recovered boundaries, definition description line rendering responsibilities outside prior recovered boundaries, definition JSON support field-label preparation, definition record support field-label preparation, definition record support line rendering responsibilities outside prior recovered boundaries, definition record scope field-label production, definition record scope line rendering responsibilities outside prior recovered boundaries, definition boundary field-label production, definition boundary line rendering responsibilities outside prior recovered boundaries, definition consumption field-label production, definition consumption line rendering responsibilities outside this recovered boundary, definition consumption line-set inclusion, definition inventory-registration value preparation, definition inventory-registration field-label production, definition inventory-registration line rendering, definition inventory-registration line-set inclusion, definition shape-registration-status value preparation, definition shape-registration-status field-label production, definition shape-registration-status line rendering responsibilities outside prior recovered boundaries, definition implementation-reason value source extraction, definition implementation-reason line rendering responsibilities outside prior recovered boundaries, definition evidence-source value source extraction, definition evidence-source line rendering responsibilities outside prior recovered boundaries, and definition line-set assembly responsibilities outside this recovered boundary;
- DiagnosticSurface explanation human rendering beyond nested definition field indent selection, nested definition consumption line delegation, explanation consumption text delegation, explanation definition heading line rendering, explanation definition section line rendering, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific CLI flags line rendering responsibilities outside prior recovered boundaries, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific description line rendering responsibilities outside prior recovered boundaries, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific JSON support line rendering responsibilities outside prior recovered boundaries, explanation-specific record support value preparation, explanation-specific record support field-label preparation, explanation-specific record scope value preparation, explanation-specific record scope field-label preparation, generic consumption text formatting beyond the prior recovered delegation boundary, generic consumption line construction beyond prior recovered delegation boundary, and explanation line-set inclusion responsibilities outside prior recovered boundaries;
- DiagnosticSurface shape-registration formatter coordination beyond shape-registration lookup, shape-registration status identification, generic value production, generic field-label production, and generic line rendering;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local boundary delegation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
