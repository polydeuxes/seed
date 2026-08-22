# Competency Interrogation Slice 171

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Human Text Formatting
        !=
DiagnosticSurface Definition Line-Set Assembly
```

This slice begins from the implementation immediately adjacent to Slice 170 in `seed_runtime/diagnostic_inventory.py` and `tests/test_diagnostic_inventory.py`. After the definition evidence-source line-set inclusion responsibility became directly observable, the next adjacent implementation-local responsibility is the top-level human formatter's responsibility for consuming the already assembled DiagnosticSurface definition line set and joining its lines into the public human text output.

`format_diagnostic_surface_definition(...)` owns building the requested definition payload, passing the extracted `diagnostic_surface_definition` object to `_assemble_diagnostic_surface_definition_line_set(...)`, and returning the newline-joined `line_set.lines`. `_assemble_diagnostic_surface_definition_line_set(...)` remains responsible for producing the ordered `_DiagnosticSurfaceDefinitionLineSet` and does not own the final human text join.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, CLI behavior, JSON behavior, or runtime behavior.

## Implementation evidence

Implementation evidence is concentrated around DiagnosticSurface definition human formatting:

- `format_diagnostic_surface_definition(...)` calls `build_diagnostic_surface_definition(diagnostic_surface)` and extracts `diagnostic_surface_definition`.
- `format_diagnostic_surface_definition(...)` passes that extracted definition to `_assemble_diagnostic_surface_definition_line_set(...)`.
- `format_diagnostic_surface_definition(...)` returns `"\n".join(line_set.lines)` and does not render individual definition lines itself.
- `test_diagnostic_surface_definition_human_formatting_consumes_line_set` proves that human formatting consumes the definition line-set assembler, forwards the extracted definition artifact, preserves build-before-assemble ordering, and owns only the final newline join over the returned `_DiagnosticSurfaceDefinitionLineSet`.

The directly observable recurring local pattern is that definition human formatting owns final text composition from an assembled line set, while line-set assembly owns ordered definition line production.

## Before

The DiagnosticSurface definition human output appeared correctly, and existing behavior was correct. However, the available test evidence still compressed final human text formatting with definition line-set assembly because it only compared the formatter result to an independently assembled line set.

Definition human text joining and definition line-set assembly were therefore compressed in the available test evidence.

## After

`test_diagnostic_surface_definition_human_formatting_consumes_line_set` now proves that `format_diagnostic_surface_definition(...)` calls the existing builder, forwards the extracted `diagnostic_surface_definition` object to `_assemble_diagnostic_surface_definition_line_set(...)`, consumes the returned `_DiagnosticSurfaceDefinitionLineSet`, and returns only the newline-joined `line_set.lines`.

`format_diagnostic_surface_definition(...)` is the recovered producer for DiagnosticSurface definition human text formatting. `_assemble_diagnostic_surface_definition_line_set(...)` remains the definition line-set assembly producer.

No public output, JSON shape, CLI behavior, diagnostics, event-ledger behavior, cluster mutation behavior, schema, or compatibility boundary changed.

## Recovered producer

`format_diagnostic_surface_definition(...)` is the recovered producer for DiagnosticSurface definition human text formatting.

## Recovered artifact/helper

The recovered helper is the already-existing `format_diagnostic_surface_definition(...)` function for the narrow responsibility of converting an assembled `_DiagnosticSurfaceDefinitionLineSet` into newline-delimited human text.

The carried artifact is the already-existing `_DiagnosticSurfaceDefinitionLineSet` consumed by `format_diagnostic_surface_definition(...)`.

It does not carry definition line-set assembly authority, individual definition line rendering authority, evidence-source rendering authority, evidence-source line-set inclusion authority, implementation-reason rendering authority, field-label preparation authority, value preparation authority, status preparation authority, CLI flag display authority, shape-registration authority, inventory-registration authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, JSON output authority, or generalized rendering ownership.

## Recovered consumer

The immediate consumer is the existing DiagnosticSurface definition CLI path that emits human output for:

- `seed --diagnostic-surface-definition <surface>`

The JSON path remains unchanged and continues to use `diagnostic_surface_definition_json(...)` rather than this human formatter.

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

DiagnosticSurface definition human text formatting and DiagnosticSurface definition line-set assembly were previously compressed in the test evidence because the test suite did not separately prove that the formatter only builds, forwards to line-set assembly, and joins the returned lines.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Human Text Formatting
        !=
DiagnosticSurface Definition Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`format_diagnostic_surface_definition(...)` owns the recovered DiagnosticSurface definition human text formatting responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`format_diagnostic_surface_definition(...)` carries the recovered boundary by consuming `_DiagnosticSurfaceDefinitionLineSet` and producing the newline-delimited human text output.

### 5. Who consumes it?

The existing human DiagnosticSurface definition CLI path consumes `format_diagnostic_surface_definition(...)` for `seed --diagnostic-surface-definition <surface>`.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_171.md`

## LOC changed

Implementation and test diff before this report:

```text
tests/test_diagnostic_inventory.py | 40 ++++++++++++++++++++++++++++++++++++++
1 file changed, 40 insertions(+)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond final human text formatting, definition evidence-source line-set inclusion, definition implementation-reason line-set inclusion, definition implementation-reason line-rendering adapter delegation, definition evidence-source value preparation, definition evidence-source field-label preparation, definition evidence-source line-rendering adapter delegation, definition implementation-reason field-label preparation, definition implementation-reason value preparation, definition shape-registration-status field-label preparation, definition inventory-registration field-label preparation, definition consumption field-label preparation, definition consumption text preparation, definition boundary text preparation, definition boundary field-label preparation, definition record scope value preparation, definition record support value preparation, definition JSON support value preparation, definition description field-label preparation, definition description text preparation, definition CLI flag display preparation, definition name value preparation, and top-level definition field indent selection, including definition identity heading line rendering responsibilities outside prior recovered boundaries, definition status value preparation, definition status line rendering responsibilities outside prior recovered boundaries, definition CLI flags line rendering responsibilities outside prior recovered boundaries, definition description line rendering responsibilities outside prior recovered boundaries, definition JSON support field-label preparation, definition record support field-label preparation, definition record support line rendering responsibilities outside prior recovered boundaries, definition record scope field-label production, definition record scope line rendering responsibilities outside prior recovered boundaries, definition boundary field-label production, definition boundary line rendering responsibilities outside prior recovered boundaries, definition consumption line rendering responsibilities outside prior recovered boundaries, definition consumption line-set inclusion, definition inventory-registration value preparation, definition inventory-registration line rendering responsibilities outside prior recovered boundaries, definition shape-registration-status value preparation, definition shape-registration-status line rendering responsibilities outside prior recovered boundaries, definition implementation-reason value source extraction, and definition line-set assembly responsibilities outside prior recovered boundaries;
- DiagnosticSurface explanation human rendering beyond nested definition field indent selection, nested definition consumption line delegation, explanation consumption text delegation, explanation definition heading line rendering, explanation definition section line rendering, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific CLI flags line rendering responsibilities outside prior recovered boundaries, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific description line rendering responsibilities outside prior recovered boundaries, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific JSON support line rendering responsibilities outside prior recovered boundaries, explanation-specific record support value preparation, explanation-specific record support field-label preparation, explanation-specific record scope value preparation, explanation-specific record scope field-label preparation, generic consumption text formatting beyond the prior recovered delegation boundary, generic consumption line construction beyond prior recovered delegation boundary, and explanation line-set inclusion responsibilities outside prior recovered boundaries;
- DiagnosticSurface shape-registration formatter coordination beyond shape-registration lookup, shape-registration status identification, generic value production, generic field-label production, and generic line rendering;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local boundary delegation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
