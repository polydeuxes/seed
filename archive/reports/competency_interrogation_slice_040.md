# Competency Interrogation Slice 040

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Heading Line Production
        !=
DiagnosticSurface Definition Human Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 039 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface top-level definition field indent selection was recovered for definition rendering, the neighboring DiagnosticSurface definition line-set assembler still selected the literal definition heading kind while also assembling the full definition line set.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface definition human rendering path:

- `_assemble_diagnostic_surface_definition_line_set(...)` already owns collection of the existing definition lines in the existing order.
- The assembler already delegates most line production to narrow renderers and formatters.
- The first definition line was still produced by passing the definition-specific literal `"definition"` directly from the line-set assembler into the generic DiagnosticSurface heading renderer.
- The same generic heading renderer is shared by multiple human rendering paths, so selecting the definition heading kind is a local definition-output responsibility rather than generic heading formatting authority.

The recurring local pattern was therefore directly observable: the definition line-set assembler should consume a definition heading line, while a narrow producer owns the existing definition heading-kind selection.

## Before

The DiagnosticSurface definition line-set assembler compressed two responsibilities:

1. DiagnosticSurface definition human line-set assembly:
   - collect existing definition lines in the existing order;
   - include the existing heading, status, CLI flags, description, JSON support, record support, record-scope, boundary, consumption, inventory registration, shape registration status, implementation reason, and evidence source presentation lines;
   - return the existing private line-set artifact for human rendering.
2. DiagnosticSurface definition heading line production:
   - select the existing `definition` heading kind;
   - pass the selected kind and existing diagnostic name to the shared heading renderer;
   - preserve the existing heading text `DiagnosticSurface definition: <name>` without promoting the heading kind to schema, CLI, diagnostics, or generalized rendering authority.

Behavior was correct, but the definition heading producer remained compressed inside broader definition line-set assembly.

## After

`_assemble_diagnostic_surface_definition_line_set(...)` now consumes `_render_diagnostic_surface_definition_heading_line(...)` for the unchanged first line.

`_render_diagnostic_surface_definition_heading_line(...)` owns only the existing definition heading-kind selection and delegates the actual heading string construction to the existing shared `_render_diagnostic_surface_heading_line(...)` helper.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_render_diagnostic_surface_definition_heading_line(...)` is the recovered producer for DiagnosticSurface definition heading line production. It produces the existing private heading-line artifact for definition output.

## Recovered artifact/helper

The recovered helper is `_render_diagnostic_surface_definition_heading_line(...)`.

The existing `_DiagnosticSurfaceHeadingLine` private artifact carries the recovered boundary's output. It carries only:

- `line`

It does not carry DiagnosticSurface identity authority, definition composition authority, explanation composition authority, line-set assembly authority, field indentation authority, status rendering authority, CLI flag display preparation authority, description rendering authority, JSON support rendering authority, record support rendering authority, record-scope rendering authority, boundary formatting authority, consumption formatting authority, diagnostic inventory registration authority, shape-audit registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

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

DiagnosticSurface definition human line-set assembly and DiagnosticSurface definition heading line production were previously compressed inside `_assemble_diagnostic_surface_definition_line_set(...)` through direct selection of the `definition` heading kind during line-set assembly.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Heading Line Production
        !=
DiagnosticSurface Definition Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_definition_heading_line(...)` now owns the recovered DiagnosticSurface definition heading line production responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_render_diagnostic_surface_definition_heading_line(...)` carries the recovered helper boundary, and the existing `_DiagnosticSurfaceHeadingLine` carries its rendered line output.

### 5. Who consumes it?

`_assemble_diagnostic_surface_definition_line_set(...)` consumes the definition heading line before returning its unchanged private line-set artifact to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `competency_interrogation_slice_040.md`

## LOC changed

Implementation diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 10 ++++++++--
1 file changed, 8 insertions(+), 2 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition heading line production and top-level field indent selection;
- DiagnosticSurface explanation human rendering beyond nested definition field indent selection;
- DiagnosticSurface explanation heading-kind selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local definition heading path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
