# Competency Interrogation Slice 039

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Top-Level Definition Field Indent Selection
        !=
DiagnosticSurface Definition Human Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 038 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface nested definition field indent selection was recovered for explanation rendering, the neighboring DiagnosticSurface definition line-set assembler still relied on each field renderer and formatter default to supply the same top-level field indentation under `DiagnosticSurface definition: ...`.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface definition human rendering path:

- `_assemble_diagnostic_surface_definition_line_set(...)` already owns collection of the existing definition lines in the existing order.
- The assembler already delegates individual line rendering for status, CLI flags, description, JSON support, record support, record-scope, boundary, consumption, inventory registration, shape registration status, implementation reason, and evidence source.
- Those delegated renderers and formatters already expose an `indent` input with the existing two-space default, which made the top-level field indentation a recurring local rendering value rather than schema, CLI, diagnostic inventory, shape-audit, event-ledger, or cluster mutation authority.
- Slice 038 made the adjacent nested explanation indentation explicit; the immediately neighboring definition assembler still compressed top-level field indent selection by leaving the selection implicit across repeated renderer defaults.

The recurring local pattern was therefore directly observable: the definition line-set assembler should collect a selected top-level definition field indent, while a narrow helper owns only the existing indentation text used beneath the definition heading.

## Before

The DiagnosticSurface definition line-set assembler compressed two responsibilities:

1. DiagnosticSurface definition human line-set assembly:
   - collect existing definition lines in the existing order;
   - include the existing heading, status, CLI flags, description, JSON support, record support, record-scope, boundary, consumption, inventory registration, shape registration status, implementation reason, and evidence source presentation lines;
   - return the existing private line-set artifact for human rendering.
2. DiagnosticSurface top-level definition field indent selection:
   - rely on each delegated renderer or formatter default to provide the existing two-space indentation;
   - preserve the existing human indentation depth for all field lines beneath the definition heading;
   - keep the selected indentation local to definition rendering rather than promoting it to schema, CLI, diagnostics, or generalized rendering authority.

Behavior was correct, but the top-level field indentation producer remained implicit across the broader definition line-set assembly path.

## After

`_assemble_diagnostic_surface_definition_line_set(...)` now obtains the unchanged indentation from `_select_diagnostic_surface_top_level_definition_field_indent(...)` and passes that unchanged text to the existing line renderers and formatters.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_select_diagnostic_surface_top_level_definition_field_indent(...)` is the recovered producer for DiagnosticSurface top-level definition field indent selection. It produces only the existing two-space human indentation used by DiagnosticSurface definition output beneath the heading line.

## Recovered artifact/helper

`_DiagnosticSurfaceTopLevelDefinitionFieldIndent` is the recovered private artifact. It carries only:

- `text`

It does not carry DiagnosticSurface identity authority, definition composition authority, explanation composition authority, status rendering authority, CLI flag display preparation authority, description rendering authority, JSON support rendering authority, record support rendering authority, record-scope rendering authority, boundary formatting authority, consumption formatting authority, diagnostic inventory registration authority, shape-audit registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

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

DiagnosticSurface definition human line-set assembly and DiagnosticSurface top-level definition field indent selection were previously compressed inside `_assemble_diagnostic_surface_definition_line_set(...)` through repeated reliance on delegated renderer and formatter indentation defaults.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Top-Level Definition Field Indent Selection
        !=
DiagnosticSurface Definition Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_select_diagnostic_surface_top_level_definition_field_indent(...)` now owns the recovered DiagnosticSurface top-level definition field indent selection responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceTopLevelDefinitionFieldIndent` carries the selected indentation text. It is a private implementation-local artifact.

### 5. Who consumes it?

`_assemble_diagnostic_surface_definition_line_set(...)` consumes the selected indentation before returning its unchanged private line-set artifact to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `competency_interrogation_slice_039.md`

## LOC changed

Implementation diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 48 +++++++++++++++++++++++++++---------
1 file changed, 36 insertions(+), 12 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond top-level field indent selection;
- DiagnosticSurface explanation human rendering beyond nested definition field indent selection;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local top-level definition field indentation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
