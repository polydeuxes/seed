# Competency Interrogation Slice 043

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Explanation Boundary Extraction
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 042 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface explanation definition extraction was recovered, the neighboring explanation line-set assembler still both selected the nested `diagnostic_surface_boundary` payload from the explanation structure and assembled the complete human explanation line set.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface explanation human rendering path:

- `build_diagnostic_surface_explanation(...)` composes an explanation wrapper whose payload contains a `diagnostic_surface_boundary` member beside the nested DiagnosticSurface definition.
- `_DiagnosticSurfaceExplanationComposition.to_json_dict(...)` preserves that existing `diagnostic_surface_boundary` member as part of the explanation JSON shape.
- `_assemble_diagnostic_surface_explanation_line_set(...)` consumed that boundary member to render the existing boundary line while also assembling the full explanation line set.
- The same assembler separately consumes the extracted `diagnostic_surface_definition` and the remaining `diagnostic_surface_consumption`, so extracting the boundary payload is a local preparation responsibility before boundary formatting rather than line-set assembly authority itself.

The directly observable recurring local pattern is that the explanation line-set assembler should consume a prepared explanation boundary artifact, while a narrow producer owns the existing extraction of the boundary payload.

## Before

The DiagnosticSurface explanation line-set assembler compressed two responsibilities:

1. DiagnosticSurface explanation human line-set assembly:
   - collect existing explanation lines in the existing order;
   - include the existing explanation heading, definition section marker, definition fields, boundary line, and consumption line;
   - return the existing private line-set artifact for human rendering.
2. DiagnosticSurface explanation boundary extraction:
   - read the existing `diagnostic_surface_boundary` member from the explanation payload;
   - make that boundary payload available to the existing boundary formatter;
   - preserve the existing JSON and human output without promoting the boundary member to a new schema authority or generalized explanation model.

Behavior was correct, but boundary extraction remained compressed inside broader explanation line-set assembly.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` now consumes `_extract_diagnostic_surface_explanation_boundary(...)` before rendering unchanged explanation lines.

`_extract_diagnostic_surface_explanation_boundary(...)` owns only the existing `diagnostic_surface_boundary` extraction and returns a private `_DiagnosticSurfaceExplanationBoundary` artifact. No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_extract_diagnostic_surface_explanation_boundary(...)` is the recovered producer for DiagnosticSurface explanation boundary extraction. It produces the existing boundary payload as a private implementation-local artifact for explanation human rendering.

## Recovered artifact/helper

The recovered helper is `_extract_diagnostic_surface_explanation_boundary(...)`.

The recovered private artifact is `_DiagnosticSurfaceExplanationBoundary`. It carries only:

- `boundary`

It does not carry DiagnosticSurface identity authority, explanation composition authority, explanation definition extraction authority, explanation line-set assembly authority, heading rendering authority, definition-section marker authority, field indentation authority, field display preparation authority, field line rendering authority, boundary formatting authority, boundary statement extraction authority, consumption extraction authority, consumption formatting authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering authority.

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

DiagnosticSurface explanation human line-set assembly and DiagnosticSurface explanation boundary extraction were previously compressed inside `_assemble_diagnostic_surface_explanation_line_set(...)` through direct selection of the `diagnostic_surface_boundary` member during line-set assembly.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Explanation Boundary Extraction
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_extract_diagnostic_surface_explanation_boundary(...)` now owns the recovered DiagnosticSurface explanation boundary extraction responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_extract_diagnostic_surface_explanation_boundary(...)` carries the recovered helper boundary, and `_DiagnosticSurfaceExplanationBoundary` carries its extracted boundary output.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` consumes the extracted explanation boundary before returning its unchanged private line-set artifact to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `competency_interrogation_slice_043.md`

## LOC changed

Implementation diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 18 +++++++++++++++++-
1 file changed, 17 insertions(+), 1 deletion(-)
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
- DiagnosticSurface explanation human rendering beyond explanation heading line production, nested definition extraction, explanation boundary extraction, and nested definition field indent selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering and statement-sequence extraction;
- DiagnosticSurface consumption formatter coordination beyond line rendering and declaration-sequence extraction;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local explanation boundary extraction path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
