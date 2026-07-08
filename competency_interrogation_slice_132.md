# Competency Interrogation Slice 132

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Line-Set Implementation-Reason Inclusion Request
        !=
DiagnosticSurface Definition Implementation-Reason Line Rendering
```

This slice begins immediately adjacent to Slice 131 in `seed_runtime/diagnostic_inventory.py`. After the definition line-set evidence-source inclusion request boundary became observable, the neighboring implementation-local responsibility in the same definition rendering line-set is the definition line-set assembly request that includes the already-rendered implementation-reason line. The definition line-set assembler owns ordered inclusion in the human-rendering line set, while the definition implementation-reason line renderer owns producing the implementation-reason line artifact.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, CLI behavior, or JSON behavior.

## Implementation evidence

Implementation evidence is concentrated around the DiagnosticSurface definition human line-set assembly path:

- `_assemble_diagnostic_surface_definition_line_set(...)` prepares the definition implementation-reason field label and value before returning `_DiagnosticSurfaceDefinitionLineSet`.
- `_render_diagnostic_surface_definition_implementation_reason_line(...)` already exists as the producer for the definition implementation-reason line request.
- `_DiagnosticSurfaceDefinitionLineSet` already carries the final ordered human-rendering lines downstream to `format_diagnostic_surface_definition(...)`.
- The line-set assembly implementation calls `_render_diagnostic_surface_definition_implementation_reason_line(...)` for the implementation-reason row rather than constructing the row inline.
- The definition line-set assembly test now proves that the implementation-reason row appears in the assembled line set and that line-set assembly delegates implementation-reason row production to the definition implementation-reason line renderer.

The directly observable recurring local pattern is that line-set assembly owns ordered inclusion of already-rendered field lines, while field-specific line renderers own concrete field line production.

## Before

The definition line-set assembly test proved the line-set artifact, heading placement, CLI flag inclusion, evidence-source inclusion, diagnostic-surface consumption inclusion, dataclass shape, and downstream formatting join. It did not prove that implementation-reason inclusion in the line set remained separated from implementation-reason line rendering.

Behavior was correct, but this local ownership boundary was still compressed in the test evidence for the definition line-set assembly path.

## After

`test_diagnostic_surface_definition_line_set_assembly_precedes_human_rendering` now proves that `_assemble_diagnostic_surface_definition_line_set(...)` includes the rendered implementation-reason row and delegates that row's production to `_render_diagnostic_surface_definition_implementation_reason_line(...)`.

`_render_diagnostic_surface_definition_implementation_reason_line(...)` remains the producer for the definition implementation-reason line. `_assemble_diagnostic_surface_definition_line_set(...)` remains responsible only for line-set assembly and inclusion order.

No public output, JSON shape, CLI behavior, diagnostics, event-ledger behavior, cluster mutation behavior, schema, or compatibility boundary changed.

## Recovered producer

`_assemble_diagnostic_surface_definition_line_set(...)` is the recovered producer for DiagnosticSurface definition line-set implementation-reason inclusion.

## Recovered artifact/helper

The recovered artifact is the already-existing `_DiagnosticSurfaceDefinitionLineSet`, which carries the ordered definition human-rendering lines.

The helper carrying the boundary is `_assemble_diagnostic_surface_definition_line_set(...)`, which consumes the field-specific implementation-reason line renderer rather than owning implementation-reason line text construction.

It does not carry implementation-reason value production authority, implementation-reason field-label production authority, implementation-reason line-rendering authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `format_diagnostic_surface_definition(...)`

Downstream existing consumers remain unchanged:

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

DiagnosticSurface definition line-set implementation-reason inclusion and DiagnosticSurface definition implementation-reason line rendering were previously compressed in the definition line-set assembly test evidence because the test asserted surrounding line-set behavior without proving that the implementation-reason row is included through the field-specific line renderer.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Line-Set Implementation-Reason Inclusion Request
        !=
DiagnosticSurface Definition Implementation-Reason Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_assemble_diagnostic_surface_definition_line_set(...)` owns the recovered line-set implementation-reason inclusion responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceDefinitionLineSet` carries the assembled lines, and `_assemble_diagnostic_surface_definition_line_set(...)` is the helper that owns the inclusion request while delegating line production.

### 5. Who consumes it?

`format_diagnostic_surface_definition(...)` consumes the assembled line set by joining its lines for human output. The CLI definition surface consumes that formatted output downstream.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_132.md`

## LOC changed

Implementation and test diff before this report:

```text
tests/test_diagnostic_inventory.py | 8 ++++++++
1 file changed, 8 insertions(+)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition CLI flag display preparation, definition name value preparation, definition identity heading line rendering, definition status value preparation, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description field-label preparation, definition description line rendering, definition JSON support value preparation, definition JSON support field-label preparation, definition JSON support line rendering, definition record support value preparation, definition record support field-label preparation, definition record scope value preparation, definition record scope field-label preparation, definition boundary text preparation, definition boundary field-label production, definition boundary line rendering, definition consumption text preparation, definition consumption field-label production, definition consumption line rendering, definition inventory-registration value preparation, definition inventory-registration field-label production, definition inventory-registration line rendering, definition shape-registration-status value preparation, definition shape-registration-status field-label production, definition shape-registration-status line rendering, definition implementation-reason value source extraction, definition implementation-reason line rendering responsibilities outside the prior recovered request-to-generic-renderer boundary, definition evidence-source value source extraction, definition evidence-source line rendering responsibilities outside prior recovered boundaries, and definition line-set assembly responsibilities outside this recovered implementation-reason inclusion boundary;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface shape-registration formatter coordination beyond shape-registration lookup, shape-registration status identification, generic value production, generic field-label production, and generic line rendering;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local implementation-reason line-set inclusion path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
