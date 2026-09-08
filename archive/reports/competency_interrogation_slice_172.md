# Competency Interrogation Slice 172

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Line-Set Identity Heading Consumption
        !=
DiagnosticSurface Definition Identity Heading Line Rendering
```

This slice begins from the implementation immediately adjacent to Slice 171 in `seed_runtime/diagnostic_inventory.py` and `tests/test_diagnostic_inventory.py`. After DiagnosticSurface definition human formatting became directly observable as the consumer of an already assembled definition line set, the next adjacent implementation-local responsibility is the definition line-set assembler's responsibility for consuming the already rendered identity heading line as the first line in the returned `_DiagnosticSurfaceDefinitionLineSet`.

`_assemble_diagnostic_surface_definition_line_set(...)` owns ordering the identity heading line into the line set. `_render_diagnostic_surface_definition_identity_heading_line(...)` remains responsible for rendering the heading line from the prepared name value and does not own line-set placement or line-set assembly.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, CLI behavior, JSON behavior, or runtime behavior.

## Implementation evidence

Implementation evidence is concentrated around DiagnosticSurface definition line-set assembly:

- `_assemble_diagnostic_surface_definition_line_set(...)` prepares `name_value` with `_prepare_diagnostic_surface_definition_name_value(definition)`.
- `_assemble_diagnostic_surface_definition_line_set(...)` passes that prepared `name_value` to `_render_diagnostic_surface_definition_identity_heading_line(...)`.
- `_assemble_diagnostic_surface_definition_line_set(...)` consumes the returned `_DiagnosticSurfaceHeadingLine.line` as the first entry of `_DiagnosticSurfaceDefinitionLineSet.lines`.
- `test_diagnostic_surface_definition_line_set_assembly_consumes_identity_heading_line` proves that line-set assembly forwards the definition into name-value preparation, forwards the prepared name-value artifact into identity heading rendering, consumes the returned heading line, and places it at `line_set.lines[0]`.

The directly observable recurring local pattern is that definition line-set assembly owns line ordering and consumption of rendered line artifacts, while identity heading rendering owns only heading line production.

## Before

The DiagnosticSurface definition human output appeared correctly, and existing behavior was correct. However, the available test evidence still compressed definition line-set identity heading consumption with identity heading line rendering because it verified the heading renderer and inspected the assembler source, but did not separately prove that the assembler consumes the returned heading-line artifact as the first line-set entry.

Identity heading line rendering and identity heading line-set placement were therefore compressed in the available test evidence.

## After

`test_diagnostic_surface_definition_line_set_assembly_consumes_identity_heading_line` now proves that `_assemble_diagnostic_surface_definition_line_set(...)` consumes the existing identity heading producer, forwards the prepared `_DiagnosticSurfaceNameValue`, and uses the returned `_DiagnosticSurfaceHeadingLine.line` as the first line of the assembled `_DiagnosticSurfaceDefinitionLineSet`.

`_assemble_diagnostic_surface_definition_line_set(...)` is the recovered producer for DiagnosticSurface definition line-set identity heading consumption. `_render_diagnostic_surface_definition_identity_heading_line(...)` remains the identity heading line rendering producer.

No public output, JSON shape, CLI behavior, diagnostics, event-ledger behavior, cluster mutation behavior, schema, or compatibility boundary changed.

## Recovered producer

`_assemble_diagnostic_surface_definition_line_set(...)` is the recovered producer for DiagnosticSurface definition line-set identity heading consumption and placement.

## Recovered artifact/helper

The recovered artifact is the already-existing `_DiagnosticSurfaceHeadingLine` returned by `_render_diagnostic_surface_definition_identity_heading_line(...)` and consumed by `_assemble_diagnostic_surface_definition_line_set(...)`.

The recovered helper boundary is carried by `_assemble_diagnostic_surface_definition_line_set(...)` only for consuming that rendered heading line as the first `_DiagnosticSurfaceDefinitionLineSet.lines` entry.

It does not carry identity heading rendering authority, name value preparation authority, status rendering authority, CLI flag rendering authority, description rendering authority, JSON support rendering authority, record support rendering authority, record scope rendering authority, boundary rendering authority, consumption rendering authority, inventory-registration rendering authority, shape-registration rendering authority, implementation-reason rendering authority, evidence-source rendering authority, final human text formatting authority, CLI authority, JSON output authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering ownership.

## Recovered consumer

The immediate consumer is `format_diagnostic_surface_definition(...)`, which consumes `_assemble_diagnostic_surface_definition_line_set(...)` and joins the assembled `line_set.lines` for the existing human DiagnosticSurface definition CLI path:

- `seed --diagnostic-surface-definition <surface>`

The JSON path remains unchanged and continues to use `diagnostic_surface_definition_json(...)` rather than the human line-set output.

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

DiagnosticSurface definition identity heading line rendering and DiagnosticSurface definition line-set identity heading consumption were previously compressed in the test evidence because the suite did not separately prove that the assembler consumes the returned heading-line artifact as the first line of the definition line set.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Line-Set Identity Heading Consumption
        !=
DiagnosticSurface Definition Identity Heading Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_assemble_diagnostic_surface_definition_line_set(...)` owns the recovered DiagnosticSurface definition line-set identity heading consumption responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

The already-existing `_DiagnosticSurfaceHeadingLine` artifact carries the rendered heading line across the boundary, and `_assemble_diagnostic_surface_definition_line_set(...)` consumes its `.line` value for first-line placement.

### 5. Who consumes it?

`format_diagnostic_surface_definition(...)` consumes the assembled `_DiagnosticSurfaceDefinitionLineSet` for the existing human DiagnosticSurface definition CLI path.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_172.md`

## LOC changed

Implementation and test diff before this report:

```text
tests/test_diagnostic_inventory.py | 49 ++++++++++++++++++++++++++++++++++++++
1 file changed, 49 insertions(+)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond final human text formatting, definition line-set identity heading consumption, definition evidence-source line-set inclusion, definition implementation-reason line-set inclusion, definition implementation-reason line-rendering adapter delegation, definition evidence-source value preparation, definition evidence-source field-label preparation, definition evidence-source line-rendering adapter delegation, definition implementation-reason field-label preparation, definition implementation-reason value preparation, definition shape-registration-status field-label preparation, definition inventory-registration field-label preparation, definition consumption field-label preparation, definition consumption text preparation, definition boundary text preparation, definition boundary field-label preparation, definition record scope value preparation, definition record support value preparation, definition JSON support value preparation, definition description field-label preparation, definition description text preparation, definition CLI flag display preparation, definition name value preparation, and top-level definition field indent selection, including definition status value preparation, definition status line rendering responsibilities outside prior recovered boundaries, definition CLI flags line rendering responsibilities outside prior recovered boundaries, definition description line rendering responsibilities outside prior recovered boundaries, definition JSON support field-label preparation, definition record support field-label preparation, definition record support line rendering responsibilities outside prior recovered boundaries, definition record scope field-label production, definition record scope line rendering responsibilities outside prior recovered boundaries, definition boundary field-label production, definition boundary line rendering responsibilities outside prior recovered boundaries, definition consumption line rendering responsibilities outside prior recovered boundaries, definition consumption line-set inclusion, definition inventory-registration value preparation, definition inventory-registration line rendering responsibilities outside prior recovered boundaries, definition shape-registration-status value preparation, definition shape-registration-status line rendering responsibilities outside prior recovered boundaries, definition implementation-reason value source extraction, and definition line-set assembly responsibilities outside prior recovered boundaries;
- DiagnosticSurface explanation human rendering beyond nested definition field indent selection, nested definition consumption line delegation, explanation consumption text delegation, explanation definition heading line rendering, explanation definition section line rendering, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific CLI flags line rendering responsibilities outside prior recovered boundaries, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific JSON support line rendering responsibilities outside prior recovered boundaries, explanation-specific record support value preparation, explanation-specific record support field-label preparation, explanation-specific record scope value preparation, explanation-specific record scope field-label preparation, generic consumption text formatting beyond the prior recovered delegation boundary, generic consumption line construction beyond prior recovered delegation boundary, and explanation line-set inclusion responsibilities outside prior recovered boundaries;
- DiagnosticSurface shape-registration formatter coordination beyond shape-registration lookup, shape-registration status identification, generic value production, generic field-label production, and generic line rendering;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local boundary delegation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
