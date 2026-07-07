# Competency Interrogation Slice 078

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Explanation Description Text Preparation
        !=
DiagnosticSurface Explanation Description Line Rendering
```

This slice begins immediately adjacent to Slice 077 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface explanation consumption text preparation was recovered, the neighboring DiagnosticSurface explanation description line still extracted description text directly while rendering the human description line.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface explanation human rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` already extracts the nested explanation definition before line-set assembly.
- `_assemble_diagnostic_surface_explanation_line_set(...)` already prepares neighboring explanation display artifacts before rendering lines, including CLI flag display, JSON support value, record support value, record scope value, boundary text, and consumption text.
- `_render_diagnostic_surface_explanation_description_line(...)` already exists as an explanation-specific producer for the rendered description line consumed by the explanation line-set assembler.
- Before this slice, `_render_diagnostic_surface_explanation_description_line(...)` still compressed description text preparation with description line rendering by reading `explanation_definition.definition["description"]` directly during line rendering.
- The top-level definition path already exposes the neighboring local pattern: `_prepare_diagnostic_surface_definition_description_text(...)` produces `_DiagnosticSurfaceDescriptionText`, and `_render_diagnostic_surface_definition_description_line(...)` consumes that prepared artifact.
- The existing human explanation output proves the rendered description line is consumed only as one member of the explanation line set.

The directly observable recurring local pattern is that the explanation line-set assembler should consume a prepared explanation description text artifact before asking the explanation description line renderer to render the line.

## Before

The DiagnosticSurface explanation description line renderer compressed two responsibilities:

1. DiagnosticSurface explanation description text preparation:
   - extract the existing nested `description` value from `_DiagnosticSurfaceExplanationDefinition`;
   - preserve the existing value without changing JSON output, schema, diagnostics, event-ledger behavior, cluster mutation behavior, or public CLI behavior.
2. DiagnosticSurface explanation description line rendering:
   - render the existing description line with the selected nested definition field indent;
   - preserve the existing `_DiagnosticSurfaceDescriptionLine` artifact and human output.

Behavior was correct, but explanation description text preparation remained compressed inside explanation description line rendering.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` now prepares `_DiagnosticSurfaceDescriptionText` through `_prepare_diagnostic_surface_explanation_description_text(...)` before passing it to `_render_diagnostic_surface_explanation_description_line(...)`.

`_render_diagnostic_surface_explanation_description_line(...)` now owns only explanation description line rendering from an already prepared description text artifact. No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_prepare_diagnostic_surface_explanation_description_text(...)` is the recovered producer for DiagnosticSurface explanation description text preparation. It produces the implementation-local `_DiagnosticSurfaceDescriptionText` artifact.

## Recovered artifact/helper

The recovered helper is `_prepare_diagnostic_surface_explanation_description_text(...)`.

The recovered artifact is `_DiagnosticSurfaceDescriptionText`, which carries the existing prepared description text between explanation definition extraction and line rendering.

It does not carry DiagnosticSurface explanation heading rendering authority, explanation definition section rendering authority, explanation status rendering authority, explanation CLI flags rendering authority, explanation description line rendering authority, explanation JSON support rendering authority, explanation record support rendering authority, explanation record scope rendering authority, explanation boundary text preparation authority, explanation boundary line rendering authority, explanation consumption text preparation authority, explanation consumption line rendering authority, explanation line-set assembly authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_explanation_description_line(...)`

The upstream assembler that prepares and passes the artifact is:

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

DiagnosticSurface explanation description text preparation and DiagnosticSurface explanation description line rendering were previously compressed inside `_render_diagnostic_surface_explanation_description_line(...)` through direct extraction of the nested definition description during line rendering.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Explanation Description Text Preparation
        !=
DiagnosticSurface Explanation Description Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_explanation_description_text(...)` now owns the recovered DiagnosticSurface explanation description text preparation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_prepare_diagnostic_surface_explanation_description_text(...)` carries the recovered helper boundary, and `_DiagnosticSurfaceDescriptionText` carries the prepared description text.

### 5. Who consumes it?

`_render_diagnostic_surface_explanation_description_line(...)` consumes `_DiagnosticSurfaceDescriptionText` before returning the unchanged `_DiagnosticSurfaceDescriptionLine` artifact to explanation line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_078.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 17 ++++++++++++++---
tests/test_diagnostic_inventory.py   | 13 ++++++++++++-
2 files changed, 26 insertions(+), 4 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition identity heading line production, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description line rendering, definition JSON support value preparation, definition JSON support line rendering, definition record support value preparation, definition record support line rendering, definition record scope value preparation, definition record scope line rendering, definition boundary line rendering, definition consumption line rendering, definition inventory registration line rendering, definition shape registration status line rendering, definition implementation reason rendering, definition evidence source rendering, and top-level field indent selection;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific definition heading line rendering, explanation-specific definition section line rendering, explanation-specific CLI flag display preparation, explanation-specific CLI flags line rendering, explanation-specific status line rendering, explanation-specific description text preparation, explanation-specific description line rendering, explanation-specific JSON support value preparation, explanation-specific record support value preparation, explanation-specific record scope value preparation, explanation-specific boundary text preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display, description text preparation, JSON support value preparation, record support value preparation, and record scope value preparation;
- DiagnosticSurface explanation field display preparation beyond CLI flag display, description text preparation, JSON support value preparation, record support value preparation, record scope value preparation, boundary text preparation, and consumption text preparation;
- DiagnosticSurface consumption formatter coordination beyond definition consumption line rendering, explanation consumption text preparation, explanation consumption line rendering, line rendering, and declaration-sequence extraction;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local explanation description text preparation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
