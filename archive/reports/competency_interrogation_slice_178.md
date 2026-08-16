# Competency Interrogation Slice 178

## Selected boundary

DiagnosticSurface Definition Line-Set Record Scope Line Consumption != DiagnosticSurface Definition Record Scope Line Rendering.

## Implementation evidence

After completing Slice 177, the current implementation independently supports this recovery: `_assemble_diagnostic_surface_definition_line_set(...)` prepares the existing typed record-scope value and field-label artifacts, invokes `_render_diagnostic_surface_definition_record_scope_line(...)`, consumes the returned `_DiagnosticSurfaceRecordScopeLine.line`, and places that line as `line_set.lines[6]` in `_DiagnosticSurfaceDefinitionLineSet.lines`.

The focused test `test_diagnostic_surface_definition_line_set_assembly_consumes_record_scope_line` verifies that the assembler forwards the prepared `_DiagnosticSurfaceRecordScopeValue`, forwards the prepared `record_scope` field label text, receives a sentinel `_DiagnosticSurfaceRecordScopeLine`, and consumes that artifact's `.line` at the existing seventh tuple position.

## Before

Record-scope preparation, record-scope rendering, and record-scope line inclusion were easy to read as one compressed implementation-local responsibility when scanning the definition line-set assembler.

## After

The implementation-local ownership boundary is observable: record-scope line rendering remains owned by `_render_diagnostic_surface_definition_record_scope_line(...)`, while `_assemble_diagnostic_surface_definition_line_set(...)` owns only inclusion and ordering of the already-rendered record-scope line in the definition line set.

## Recovered producer

`_assemble_diagnostic_surface_definition_line_set(...)` is the recovered producer for DiagnosticSurface definition line-set record-scope line consumption and tuple placement.

## Recovered artifact/helper

The existing `_DiagnosticSurfaceRecordScopeLine` artifact carries the rendered line across the boundary. No new helper or public surface was introduced.

## Recovered consumer

The immediate consumer is `format_diagnostic_surface_definition(...)`, which joins `_DiagnosticSurfaceDefinitionLineSet.lines` for the existing human DiagnosticSurface definition output.

## Compatibility preserved

No.

No compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and output ordering are preserved.

## Files changed

- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_178.md`

## LOC changed

- Added one focused regression test and this report.
- No production implementation lines changed.

## Tests executed

- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

The assembler still contains later definition line-set inclusion responsibilities after record scope, including boundary, consumption, inventory registration, shape-registration status, implementation reason, and evidence source line consumption. This slice does not recover any of those, and this batch does not attempt a third slice.

## Distinction from Slices 172 through 176

Slices 172 through 176 recovered identity heading, status, CLI flags, description, and JSON support line consumption. Slice 178 is distinct because it recovers only the seventh tuple position: record-scope line consumption at `line_set.lines[6]`.

## Distinction from prior field preparation and rendering slices

This slice does not recover record-scope value preparation, record-scope field-label preparation, generic record-scope rendering, or definition record-scope rendering. It is limited to the assembler consuming the already-rendered `_DiagnosticSurfaceRecordScopeLine.line` and placing it in the line-set tuple.

## Distinction from Slice 177

Slice 178 concerns `record_scope` and the `_DiagnosticSurfaceRecordScopeLine` placed at `line_set.lines[6]`. Slice 177 concerns `supports_record` and `_DiagnosticSurfaceRecordSupportLine` at `line_set.lines[5]`.

## Required questions

1. What responsibility was previously compressed?
   - Record-scope line rendering and record-scope line-set inclusion/ordering were compressed in the definition line-set assembly region.
2. Which implementation-local ownership boundary became directly observable?
   - DiagnosticSurface definition line-set record-scope line consumption is distinct from DiagnosticSurface definition record-scope line rendering.
3. What producer owns the recovered responsibility?
   - `_assemble_diagnostic_surface_definition_line_set(...)`.
4. What artifact or helper carries the recovered boundary, if any?
   - `_DiagnosticSurfaceRecordScopeLine` carries the rendered `.line` consumed by the assembler.
5. Who consumes it?
   - `_assemble_diagnostic_surface_definition_line_set(...)` consumes the rendered line; `format_diagnostic_surface_definition(...)` consumes the assembled line set.
6. Did any compatibility boundary change?
   - No.
7. How is this distinct from Slices 172 through 176?
   - It targets only record-scope line inclusion at the seventh line-set position, not identity, status, CLI flags, description, or JSON support.
8. How is this distinct from the prior value, field-label, and rendering slices for the same field?
   - It does not own value extraction, label preparation, or line rendering; it owns only consuming the rendered line artifact into the tuple.
9. How is Slice 178 distinct from Slice 177?
   - Slice 178 addresses record-scope line consumption at `line_set.lines[6]`, while Slice 177 addresses record-support line consumption at `line_set.lines[5]`.
10. What current implementation evidence justified continuing rather than stopping?
    - After Slice 177, the assembler independently prepares `record_scope_value` and `record_scope_field_label`, invokes `_render_diagnostic_surface_definition_record_scope_line(...)`, consumes `.line`, and places it at `line_set.lines[6]`; the focused test proves that boundary without changing output.
