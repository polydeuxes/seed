# Competency Interrogation Slice 082

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Explanation Definition Section Indent Selection
        !=
DiagnosticSurface Explanation Definition Section Line Rendering
```

This slice begins immediately adjacent to Slice 081 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface explanation definition section label preparation was recovered, the next neighboring section-line responsibility still rendered the nested `definition:` section line from an implicit hard-coded section indent.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface explanation human rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` already extracts and prepares explanation artifacts before rendering the human line set.
- `_prepare_diagnostic_surface_explanation_definition_section_label(...)` already prepares the nested definition section label before `_render_diagnostic_surface_explanation_definition_section_line(...)` renders the section line.
- `_select_diagnostic_surface_nested_definition_field_indent(...)` and `_select_diagnostic_surface_top_level_definition_field_indent(...)` already establish that DiagnosticSurface human indentation is selected as an implementation-local artifact before line rendering.
- `_render_diagnostic_surface_explanation_definition_section_line(...)` already exists as the explanation-specific producer for the rendered nested `definition:` section line consumed by explanation line-set assembly.
- Before this slice, section line indentation remained compressed inside section line rendering through `_render_diagnostic_surface_definition_section_line(...)` hard-coding the leading two spaces.
- The existing human explanation output proves the rendered section line is consumed only as one member of the explanation line set.

The directly observable recurring local pattern is that the explanation line-set assembler should consume a selected section indent artifact before asking the explanation definition section line renderer to render the section line.

## Before

The DiagnosticSurface explanation definition section line renderer compressed two responsibilities:

1. DiagnosticSurface explanation definition section indent selection:
   - select the existing two-space indentation used by the nested `definition:` section line;
   - preserve the existing line text without changing JSON output, schema, diagnostics, event-ledger behavior, cluster mutation behavior, or public CLI behavior.
2. DiagnosticSurface explanation definition section line rendering:
   - render the existing `  definition:` section line from the prepared section label and selected indent;
   - preserve the existing `_DiagnosticSurfaceDefinitionSectionLine` artifact and human output.

Behavior was correct, but explanation definition section indent selection remained compressed inside section line rendering.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` now selects `_DiagnosticSurfaceDefinitionSectionIndent` through `_select_diagnostic_surface_explanation_definition_section_indent(...)` before passing the unchanged indent text to `_render_diagnostic_surface_explanation_definition_section_line(...)`.

`_render_diagnostic_surface_explanation_definition_section_line(...)` now owns only explanation definition section line rendering from an already prepared section label artifact and an already selected section indent. No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_select_diagnostic_surface_explanation_definition_section_indent(...)` is the recovered producer for DiagnosticSurface explanation definition section indent selection. It produces the implementation-local `_DiagnosticSurfaceDefinitionSectionIndent` artifact.

## Recovered artifact/helper

The recovered helper is `_select_diagnostic_surface_explanation_definition_section_indent(...)`.

The recovered artifact is `_DiagnosticSurfaceDefinitionSectionIndent`, which carries the existing selected two-space section indent between explanation line-set assembly and section line rendering.

It does not carry DiagnosticSurface explanation heading rendering authority, explanation name value preparation authority, explanation definition section label preparation authority, explanation definition section line rendering authority, nested definition field indent selection authority, explanation status value preparation authority, explanation status line rendering authority, explanation CLI flag display preparation authority, explanation CLI flags rendering authority, explanation description text preparation authority, explanation description line rendering authority, explanation JSON support value preparation authority, explanation JSON support rendering authority, explanation record support value preparation authority, explanation record support rendering authority, explanation record scope value preparation authority, explanation record scope rendering authority, explanation boundary text preparation authority, explanation boundary line rendering authority, explanation consumption text preparation authority, explanation consumption line rendering authority, explanation line-set assembly authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_explanation_definition_section_line(...)`

The upstream assembler that selects and passes the artifact is:

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

DiagnosticSurface explanation definition section indent selection and DiagnosticSurface explanation definition section line rendering were previously compressed inside section line rendering through implicit hard-coded section indentation.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Explanation Definition Section Indent Selection
        !=
DiagnosticSurface Explanation Definition Section Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_select_diagnostic_surface_explanation_definition_section_indent(...)` now owns the recovered DiagnosticSurface explanation definition section indent selection responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_select_diagnostic_surface_explanation_definition_section_indent(...)` carries the recovered helper boundary, and `_DiagnosticSurfaceDefinitionSectionIndent` carries the selected section indent.

### 5. Who consumes it?

`_render_diagnostic_surface_explanation_definition_section_line(...)` consumes `_DiagnosticSurfaceDefinitionSectionIndent.text` before returning the unchanged `_DiagnosticSurfaceDefinitionSectionLine` artifact to explanation line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_082.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 28 +++++++++++++++++++++++-----
tests/test_diagnostic_inventory.py   |  8 +++++++-
2 files changed, 30 insertions(+), 6 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
python scripts/seed_local.py --diagnostic-surface-explanation diagnostic_shape_audit
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition identity heading line production, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description line rendering, definition JSON support value preparation, definition JSON support line rendering, definition record support value preparation, definition record support line rendering, definition record scope value preparation, definition record scope line rendering, definition boundary line rendering, definition consumption line rendering, definition inventory registration line rendering, definition shape registration status line rendering, definition implementation reason rendering, definition evidence source rendering, top-level field indent selection, and definition section label or section indent rendering outside this recovered explanation-specific nested section indent path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status line rendering, explanation-specific CLI flag display preparation, explanation-specific CLI flags line rendering, explanation-specific description text preparation, explanation-specific description line rendering, explanation-specific JSON support value preparation, explanation-specific JSON support line rendering, explanation-specific record support value preparation, explanation-specific record support line rendering, explanation-specific record scope value preparation, explanation-specific record scope line rendering, explanation-specific boundary text preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display, description text preparation, JSON support value preparation, record support value preparation, and record scope value preparation;
- DiagnosticSurface explanation field display preparation beyond name value preparation, section label preparation, section indent selection, status value preparation, CLI flag display, description text preparation, JSON support value preparation, record support value preparation, record scope value preparation, boundary text preparation, and consumption text preparation;
- DiagnosticSurface consumption formatter coordination beyond definition consumption line rendering, explanation consumption text preparation, explanation consumption line rendering, line rendering, and declaration-sequence extraction;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local explanation definition section indent selection path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
