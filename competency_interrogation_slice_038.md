# Competency Interrogation Slice 038

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Nested Definition Field Indent Selection
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 037 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface definition section line rendering was recovered, the neighboring explanation line-set assembler still directly repeated the nested definition field indentation literal for every field line and nested formatter under the `  definition:` section.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface explanation human rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` already delegates heading, definition section, status, CLI flags, description, JSON support, record support, record-scope, boundary, and consumption rendering to implementation-local helpers.
- The same assembler still directly repeated the same nested field indentation literal for each definition field line and for the nested boundary and consumption formatter calls.
- That indentation value has no schema authority, CLI authority, inventory authority, shape-audit authority, event-ledger authority, cluster mutation authority, or DiagnosticSurface definition production authority.
- The value and placement were already established by existing human output; recovering it only made the local producer boundary explicit.

The recurring local pattern was therefore directly observable: the explanation line-set assembler should collect a selected nested definition field indent, while a narrow helper owns only the existing indentation text used beneath the definition section line.

## Before

The DiagnosticSurface explanation line-set assembler compressed two responsibilities:

1. DiagnosticSurface explanation human line-set assembly:
   - collect existing explanation lines in the existing order;
   - include the existing heading, definition section, status, CLI flags, description, JSON support, record support, record-scope, boundary, and consumption presentation lines;
   - return the existing private line-set artifact for human rendering.
2. DiagnosticSurface nested definition field indent selection:
   - provide the existing four-space indentation used under `  definition:`;
   - preserve the existing human indentation depth for status, CLI flags, description, JSON support, record support, record-scope, boundary, and consumption lines;
   - keep the selected indentation local to explanation rendering rather than promoting it to schema, CLI, diagnostics, or generalized rendering authority.

Behavior was correct, but the nested field indentation producer remained implicit inside the broader explanation line-set assembly owner.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` now obtains the unchanged indentation from `_select_diagnostic_surface_nested_definition_field_indent(...)` and passes that unchanged text to the existing line renderers and nested formatters.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_select_diagnostic_surface_nested_definition_field_indent(...)` is the recovered producer for DiagnosticSurface nested definition field indent selection. It produces only the existing four-space human indentation used by DiagnosticSurface explanation output beneath the `definition` section.

## Recovered artifact/helper

`_DiagnosticSurfaceNestedDefinitionFieldIndent` is the recovered private artifact. It carries only:

- `text`

It does not carry DiagnosticSurface identity authority, explanation composition authority, definition production authority, status rendering authority, CLI flag display preparation authority, description rendering authority, JSON support rendering authority, record support rendering authority, record-scope rendering authority, boundary formatting authority, consumption formatting authority, diagnostic inventory registration authority, shape-audit registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_assemble_diagnostic_surface_explanation_line_set(...)`

Downstream existing consumers remain unchanged:

- `format_diagnostic_surface_explanation(...)`
- `seed --diagnostic-surface-explanation <surface>`

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

DiagnosticSurface explanation human line-set assembly and DiagnosticSurface nested definition field indent selection were previously compressed inside `_assemble_diagnostic_surface_explanation_line_set(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Nested Definition Field Indent Selection
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_select_diagnostic_surface_nested_definition_field_indent(...)` now owns the recovered DiagnosticSurface nested definition field indent selection responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceNestedDefinitionFieldIndent` carries the selected indentation text. It is a private implementation-local artifact.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` consumes the selected indentation before returning its unchanged private line-set artifact to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `competency_interrogation_slice_038.md`

## LOC changed

Implementation diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 32 ++++++++++++++++++++++++--------
1 file changed, 24 insertions(+), 8 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface explanation human rendering beyond nested definition field indent selection;
- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local nested definition field indentation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
