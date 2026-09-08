# Competency Interrogation Slice 041

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Explanation Heading Line Production
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 040 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface definition heading line production was recovered, the neighboring DiagnosticSurface explanation line-set assembler still selected the literal explanation heading kind while also assembling the full explanation line set.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface explanation human rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` already owns collection of the existing explanation lines in the existing order.
- The assembler already delegates definition-section, field, boundary, and consumption line production to narrow helpers.
- The first explanation line was still produced by passing the explanation-specific literal `"explanation"` directly from the line-set assembler into the shared DiagnosticSurface heading renderer.
- Slice 040 made the same neighboring pattern explicit for definition heading line production, and the current implementation independently exposes the same local compression for explanation output.

The recurring local pattern was therefore directly observable: the explanation line-set assembler should consume an explanation heading line, while a narrow producer owns the existing explanation heading-kind selection.

## Before

The DiagnosticSurface explanation line-set assembler compressed two responsibilities:

1. DiagnosticSurface explanation human line-set assembly:
   - collect existing explanation lines in the existing order;
   - include the existing explanation heading, definition section marker, status, CLI flags, description, JSON support, record support, record-scope, boundary, and consumption presentation lines;
   - return the existing private line-set artifact for human rendering.
2. DiagnosticSurface explanation heading line production:
   - select the existing `explanation` heading kind;
   - pass the selected kind and existing diagnostic name to the shared heading renderer;
   - preserve the existing heading text `DiagnosticSurface explanation: <name>` without promoting the heading kind to schema, CLI, diagnostics, or generalized rendering authority.

Behavior was correct, but the explanation heading producer remained compressed inside broader explanation line-set assembly.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` now consumes `_render_diagnostic_surface_explanation_heading_line(...)` for the unchanged first line.

`_render_diagnostic_surface_explanation_heading_line(...)` owns only the existing explanation heading-kind selection and delegates the actual heading string construction to the existing shared `_render_diagnostic_surface_heading_line(...)` helper.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_render_diagnostic_surface_explanation_heading_line(...)` is the recovered producer for DiagnosticSurface explanation heading line production. It produces the existing private heading-line artifact for explanation output.

## Recovered artifact/helper

The recovered helper is `_render_diagnostic_surface_explanation_heading_line(...)`.

The existing `_DiagnosticSurfaceHeadingLine` private artifact carries the recovered boundary's output. It carries only:

- `line`

It does not carry DiagnosticSurface identity authority, explanation composition authority, definition composition authority, line-set assembly authority, field indentation authority, definition-section marker authority, status rendering authority, CLI flag display preparation authority, description rendering authority, JSON support rendering authority, record support rendering authority, record-scope rendering authority, boundary formatting authority, consumption formatting authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

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

DiagnosticSurface explanation human line-set assembly and DiagnosticSurface explanation heading line production were previously compressed inside `_assemble_diagnostic_surface_explanation_line_set(...)` through direct selection of the `explanation` heading kind during line-set assembly.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Explanation Heading Line Production
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_explanation_heading_line(...)` now owns the recovered DiagnosticSurface explanation heading line production responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_render_diagnostic_surface_explanation_heading_line(...)` carries the recovered helper boundary, and the existing `_DiagnosticSurfaceHeadingLine` carries its rendered line output.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` consumes the explanation heading line before returning its unchanged private line-set artifact to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `competency_interrogation_slice_041.md`

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
- DiagnosticSurface explanation human rendering beyond explanation heading line production and nested definition field indent selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local explanation heading path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
