# Competency Interrogation Slice 091

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Consumption Field Label Preparation
        !=
DiagnosticSurface Definition Consumption Line Rendering
```

This slice begins immediately adjacent to Slice 090 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface explanation consumption field label preparation was recovered, the neighboring DiagnosticSurface definition consumption line still rendered with the `diagnostic_surface_consumption:` field label supplied only as the default inside definition consumption line rendering.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface definition human rendering path:

- `_assemble_diagnostic_surface_definition_line_set(...)` prepares definition display artifacts and selects the top-level definition field indent before producing the human definition line set.
- `_render_diagnostic_surface_definition_consumption_line(...)` already exists as the definition-specific producer for the rendered top-level `diagnostic_surface_consumption:` line consumed by definition line-set assembly.
- `_prepare_diagnostic_surface_consumption_text(...)` already owns extraction and text preparation for the consumption declaration text before line rendering.
- `_select_diagnostic_surface_top_level_definition_field_indent(...)` already establishes that top-level field indentation is selected as an implementation-local artifact before definition field line rendering.
- Slice 090 made the adjacent explanation consumption line consume a prepared `diagnostic_surface_consumption` field label artifact before rendering.
- Before this slice, the definition consumption field label remained compressed inside definition consumption line rendering through `_render_diagnostic_surface_definition_consumption_line(...)` depending on the generic renderer default for `diagnostic_surface_consumption`.
- Existing human definition output proves the rendered consumption line is consumed only as one member of the definition line set.

The directly observable recurring local pattern is that the definition line-set assembler should consume a prepared consumption field label artifact before asking the definition consumption line renderer to render the consumption line.

## Before

The DiagnosticSurface definition consumption line renderer compressed two responsibilities:

1. DiagnosticSurface definition consumption field label preparation:
   - prepare the existing `diagnostic_surface_consumption` field label used by the top-level definition consumption line;
   - preserve the existing line text without changing JSON output, schema, diagnostics, event-ledger behavior, cluster mutation behavior, or public CLI behavior.
2. DiagnosticSurface definition consumption line rendering:
   - render the existing top-level `diagnostic_surface_consumption: <consumption text>` line from the prepared consumption text, prepared field label, and selected top-level field indent;
   - preserve the existing `_DiagnosticSurfaceConsumptionLine` artifact and human output.

Behavior was correct, but definition consumption field label preparation remained compressed inside consumption line rendering.

## After

`_assemble_diagnostic_surface_definition_line_set(...)` now prepares `_DiagnosticSurfaceConsumptionFieldLabel` through `_prepare_diagnostic_surface_definition_consumption_field_label(...)` before passing the unchanged label text to `_render_diagnostic_surface_definition_consumption_line(...)`.

`_render_diagnostic_surface_definition_consumption_line(...)` now receives an already prepared definition consumption field label while preserving its existing consumption text preparation and line-rendering behavior. No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_prepare_diagnostic_surface_definition_consumption_field_label(...)` is the recovered producer for DiagnosticSurface definition consumption field label preparation. It produces the implementation-local `_DiagnosticSurfaceConsumptionFieldLabel` artifact.

## Recovered artifact/helper

The recovered helper is `_prepare_diagnostic_surface_definition_consumption_field_label(...)`.

The recovered artifact is `_DiagnosticSurfaceConsumptionFieldLabel`, which carries the existing `diagnostic_surface_consumption` field label between definition line-set assembly and definition consumption line rendering.

It does not carry DiagnosticSurface definition identity heading rendering authority, definition status line rendering authority, definition CLI flags line rendering authority, definition description text preparation authority, definition description line rendering authority, definition JSON support value preparation authority, definition JSON support line rendering authority, definition record support value preparation authority, definition record support line rendering authority, definition record scope value preparation authority, definition record scope line rendering authority, definition boundary text preparation authority, definition boundary line rendering authority, definition consumption text preparation authority, definition consumption line rendering authority, inventory registration rendering authority, shape registration rendering authority, implementation reason rendering authority, evidence source rendering authority, top-level field indent selection authority, explanation rendering authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_definition_consumption_line(...)`

The upstream assembler that prepares and passes the artifact is:

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

DiagnosticSurface definition consumption field label preparation and DiagnosticSurface definition consumption line rendering were previously compressed inside definition consumption line rendering through an implicit default `diagnostic_surface_consumption` field label.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Consumption Field Label Preparation
        !=
DiagnosticSurface Definition Consumption Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_definition_consumption_field_label(...)` now owns the recovered DiagnosticSurface definition consumption field label preparation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_prepare_diagnostic_surface_definition_consumption_field_label(...)` carries the recovered helper boundary, and `_DiagnosticSurfaceConsumptionFieldLabel` carries the prepared consumption field label.

### 5. Who consumes it?

`_render_diagnostic_surface_definition_consumption_line(...)` consumes `_DiagnosticSurfaceConsumptionFieldLabel.text` before returning the unchanged `_DiagnosticSurfaceConsumptionLine` artifact to definition line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_091.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 23 ++++++++++++++++++++---
tests/test_diagnostic_inventory.py   |  9 ++++++++-
2 files changed, 28 insertions(+), 4 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition identity heading line production, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description line rendering, definition JSON support value preparation, definition JSON support line rendering, definition record support value preparation, definition record support line rendering, definition record scope value preparation, definition record scope line rendering, definition boundary text preparation, definition boundary line rendering, definition consumption text preparation, definition consumption field label preparation, definition consumption line rendering, definition inventory registration line rendering, definition shape registration status line rendering, definition implementation reason rendering, definition evidence source rendering, top-level field indent selection, definition section label rendering, definition section indent rendering, and definition field label preparation outside this recovered definition-specific consumption field label path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flag display preparation, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display, description text preparation, JSON support value preparation, record support value preparation, record scope value preparation, and definition consumption field label preparation;
- DiagnosticSurface consumption formatter coordination beyond definition consumption field label preparation, definition consumption line rendering, explanation consumption text preparation, explanation consumption field label preparation, explanation consumption line rendering, line rendering, and declaration-sequence extraction;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local definition consumption field label preparation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
