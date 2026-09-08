# Competency Interrogation Slice 037

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Section Line Rendering
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 036 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface heading line rendering was recovered, the neighboring explanation-only line-set assembler still directly carried the literal `  definition:` section line before the already-rendered definition field lines.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, or public surface.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface explanation human rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` already delegates heading, status, CLI flags, description, JSON support, record support, record-scope, boundary, and consumption lines to implementation-local helpers.
- The same assembler still directly embedded the section label line that introduces the existing nested definition block.
- The section line has no schema authority, CLI authority, inventory authority, shape-audit authority, event-ledger authority, cluster mutation authority, or DiagnosticSurface definition production authority.
- The line's value and position were already established by existing human output; recovering it only made the local producer boundary explicit.

The recurring local pattern was therefore directly observable: the explanation line-set assembler should collect a rendered definition section line, while a narrow helper owns only the existing section label line.

## Before

The DiagnosticSurface explanation line-set assembler compressed two responsibilities:

1. DiagnosticSurface explanation human line-set assembly:
   - collect existing explanation lines in the existing order;
   - include the existing heading, definition section, status, CLI flags, description, JSON support, record support, record-scope, boundary, and consumption presentation lines;
   - return the existing private line-set artifact for human rendering.
2. DiagnosticSurface definition section line rendering:
   - provide the existing `  definition:` line;
   - preserve the existing indentation and punctuation;
   - place that rendered line before the nested definition field lines in explanation output.

Behavior was correct, but the section line's producer remained implicit inside the broader explanation line-set assembly owner.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` now collects the unchanged line from `_render_diagnostic_surface_definition_section_line(...)` before the unchanged nested definition field lines.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_render_diagnostic_surface_definition_section_line(...)` is the recovered producer for DiagnosticSurface definition section line rendering. It produces only the existing human section label line used by DiagnosticSurface explanation output.

## Recovered artifact/helper

`_DiagnosticSurfaceDefinitionSectionLine` is the recovered private artifact. It carries only:

- `line`

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

DiagnosticSurface explanation human line-set assembly and DiagnosticSurface definition section line rendering were previously compressed inside `_assemble_diagnostic_surface_explanation_line_set(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Section Line Rendering
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_definition_section_line(...)` now owns the recovered DiagnosticSurface definition section line rendering responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceDefinitionSectionLine` carries the rendered definition section line. It is a private implementation-local artifact.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` consumes the rendered line before returning its unchanged private line-set artifact to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `competency_interrogation_slice_037.md`

## LOC changed

Implementation diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 15 ++++++++++++++-
1 file changed, 14 insertions(+), 1 deletion(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface explanation human rendering beyond line-set assembly;
- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local definition section line path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
