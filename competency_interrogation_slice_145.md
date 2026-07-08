# Competency Interrogation Slice 145

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Explanation Consumption Line Delegation
        !=
Generic DiagnosticSurface Consumption Line Construction
```

This slice begins immediately adjacent to Slice 144 in the DiagnosticSurface explanation consumption row path in `seed_runtime/diagnostic_inventory.py`. After Slice 144 made explanation line-set consumption inclusion observable, the next adjacent responsibility is the explanation-specific consumption line renderer itself. `_render_diagnostic_surface_explanation_consumption_line(...)` owns the explanation-context request for a `diagnostic_surface_consumption` line, while `_render_diagnostic_surface_consumption_line(...)` owns the generic text-to-line construction.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, CLI behavior, or JSON behavior.

## Implementation evidence

Implementation evidence is concentrated around the DiagnosticSurface explanation consumption rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` consumes `_render_diagnostic_surface_explanation_consumption_line(...)` when adding the nested `diagnostic_surface_consumption` row to the explanation line set.
- `_render_diagnostic_surface_explanation_consumption_line(...)` accepts the explanation-prepared consumption text plus the explanation field label and indentation defaults.
- `_render_diagnostic_surface_explanation_consumption_line(...)` delegates the concrete line construction to `_render_diagnostic_surface_consumption_line(...)`.
- `_render_diagnostic_surface_consumption_line(...)` remains the generic producer of `_DiagnosticSurfaceConsumptionLine` text.
- `test_diagnostic_surface_explanation_consumption_line_rendering_precedes_line_set_assembly` now proves that explanation consumption line rendering remains an explanation-context delegation to the generic consumption line renderer.

The directly observable recurring local pattern is that explanation-specific renderers own explanation-context field requests, while generic renderers own reusable line construction.

## Before

The explanation consumption line rendering test proved consumption text preparation, field-label preparation, concrete rendered output, dataclass shape, and line-set readiness. It did not prove that the explanation-specific consumption renderer remained separate from generic consumption line construction.

Behavior was correct, but this local ownership boundary was still compressed in the test evidence for the explanation consumption line rendering path.

## After

`test_diagnostic_surface_explanation_consumption_line_rendering_precedes_line_set_assembly` now proves that `_render_diagnostic_surface_explanation_consumption_line(...)` delegates to `_render_diagnostic_surface_consumption_line(...)` while preserving the existing rendered output.

`_render_diagnostic_surface_explanation_consumption_line(...)` remains the producer for the explanation-context consumption line request. `_render_diagnostic_surface_consumption_line(...)` remains responsible for generic consumption line construction.

No public output, JSON shape, CLI behavior, diagnostics, event-ledger behavior, cluster mutation behavior, schema, or compatibility boundary changed.

## Recovered producer

`_render_diagnostic_surface_explanation_consumption_line(...)` is the recovered producer for DiagnosticSurface explanation consumption line delegation.

## Recovered artifact/helper

The recovered artifact is the already-existing `_DiagnosticSurfaceConsumptionLine`, which carries the rendered consumption row.

The helper carrying the boundary is `_render_diagnostic_surface_explanation_consumption_line(...)`, which accepts explanation-context consumption text, field label, and indentation before delegating generic line construction to `_render_diagnostic_surface_consumption_line(...)`.

It does not carry consumption text preparation authority, consumption field-label preparation authority, explanation line-set inclusion authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, or generalized rendering ownership beyond this delegation.

## Recovered consumer

The immediate consumer is:

- `_assemble_diagnostic_surface_explanation_line_set(...)`

Downstream existing consumers remain unchanged:

- `format_diagnostic_surface_explanation(...)`
- `seed --diagnostic-surface-explanation <surface>`
- `seed --diagnostic-surface-explanation <surface> --json` for the unchanged alternate JSON path

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

- `seed --diagnostic-surface-explanation diagnostic_shape_audit`
- `seed --diagnostic-surface-explanation diagnostic_shape_audit --json`
- `seed --diagnostic-surface-definition diagnostic_shape_audit`
- `seed --diagnostic-surface-definition diagnostic_shape_audit --json`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

## Required questions

### 1. What responsibilities were previously compressed?

DiagnosticSurface explanation consumption line delegation and generic DiagnosticSurface consumption line construction were previously compressed in the explanation consumption line rendering test evidence because the test did not prove that the explanation-specific renderer delegates concrete row construction to the generic consumption line renderer.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Explanation Consumption Line Delegation
        !=
Generic DiagnosticSurface Consumption Line Construction
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_explanation_consumption_line(...)` owns the recovered explanation consumption line delegation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceConsumptionLine` carries the rendered row, and `_render_diagnostic_surface_explanation_consumption_line(...)` is the helper that owns the explanation-context delegation boundary.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` consumes the rendered line while assembling the DiagnosticSurface explanation human line set. The formatted explanation and CLI explanation surface consume it downstream.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_145.md`

## LOC changed

Implementation and test diff before this report:

```text
tests/test_diagnostic_inventory.py | 3 +++
1 file changed, 3 insertions(+)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface explanation human rendering beyond nested definition consumption line delegation, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific CLI flags line rendering responsibilities outside prior recovered boundaries, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific description line rendering responsibilities outside prior recovered boundaries, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific JSON support line rendering responsibilities outside prior recovered boundaries, explanation-specific record support value preparation, explanation-specific record support field-label preparation, explanation-specific record support line-rendering responsibilities outside prior recovered boundaries, explanation-specific record scope value preparation, explanation-specific record scope field-label preparation, explanation-specific record scope line-rendering responsibilities outside prior recovered boundaries, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering responsibilities outside prior recovered boundaries, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, generic consumption line construction beyond this recovered delegation boundary, explanation line-set inclusion responsibilities outside prior recovered boundaries, and nested definition field indent selection;
- DiagnosticSurface definition human rendering beyond prior recovered definition and explanation line-set inclusion boundaries, including definition CLI flag display preparation, definition name value preparation, definition identity heading line rendering, definition status value preparation, definition status line rendering responsibilities outside prior recovered boundaries, definition CLI flags line rendering responsibilities outside prior recovered boundaries, definition description text preparation, definition description field-label preparation, definition description line rendering, definition JSON support value preparation, definition JSON support field-label preparation, definition JSON support line rendering, definition record support value preparation, definition record support field-label preparation, definition record support line rendering, definition record scope value preparation, definition record scope field-label production, definition record scope line rendering responsibilities outside prior recovered boundaries, definition boundary text preparation, definition boundary field-label production, definition boundary line rendering, definition consumption text preparation, definition consumption field-label production, definition consumption line rendering, definition consumption line-set inclusion, definition inventory-registration value preparation, definition inventory-registration field-label production, definition inventory-registration line rendering, definition inventory-registration line-set inclusion, definition shape-registration-status value preparation, definition shape-registration-status field-label production, definition shape-registration-status line rendering responsibilities outside prior recovered boundaries, definition implementation-reason value source extraction, definition implementation-reason line rendering responsibilities outside prior recovered boundaries, definition evidence-source value source extraction, definition evidence-source line rendering responsibilities outside prior recovered boundaries, and definition line-set assembly responsibilities outside prior recovered boundaries;
- DiagnosticSurface shape-registration formatter coordination beyond shape-registration lookup, shape-registration status identification, generic value production, generic field-label production, and generic line rendering;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local boundary delegation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
