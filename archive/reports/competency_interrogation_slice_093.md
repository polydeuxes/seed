# Competency Interrogation Slice 093

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Shape Registration Status Field Label Preparation
        !=
DiagnosticSurface Definition Shape Registration Status Line Rendering
```

This slice begins immediately adjacent to Slice 092 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface definition inventory registration field label preparation was recovered, the neighboring DiagnosticSurface definition shape-registration status line still rendered the `shape_registration_status:` field label from the line renderer's default instead of consuming a prepared definition field label artifact.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface definition human rendering path:

- `_assemble_diagnostic_surface_definition_line_set(...)` prepares definition display artifacts and selects the top-level definition field indent before producing the human definition line set.
- `_render_diagnostic_surface_definition_shape_registration_status_line(...)` already exists as the definition-specific producer for the rendered top-level `shape_registration_status:` line consumed by definition line-set assembly.
- `_select_diagnostic_surface_top_level_definition_field_indent(...)` already establishes that top-level field indentation is selected as an implementation-local artifact before definition field line rendering.
- Slice 092 made the immediately preceding definition inventory registration line consume a prepared `diagnostic_inventory_registration` field label artifact before rendering.
- Before this slice, definition shape-registration status field label preparation remained compressed inside shape-registration status line rendering through `_render_diagnostic_surface_shape_registration_status_line(...)` using the generic renderer's default `shape_registration_status` label.
- Existing human definition output proves the rendered shape-registration status line is consumed only as one member of the definition line set.

The directly observable recurring local pattern is that the definition line-set assembler should consume a prepared shape-registration status field label artifact before asking the definition shape-registration status line renderer to render the status line.

## Before

The DiagnosticSurface definition shape-registration status line renderer compressed two responsibilities:

1. DiagnosticSurface definition shape-registration status field label preparation:
   - prepare the existing `shape_registration_status` field label used by the top-level definition shape-registration status line;
   - preserve the existing line text without changing JSON output, schema, diagnostics, event-ledger behavior, cluster mutation behavior, or public CLI behavior.
2. DiagnosticSurface definition shape-registration status line rendering:
   - render the existing top-level `shape_registration_status: <status>` line from the prepared status value, prepared field label, and selected top-level field indent;
   - preserve the existing `_DiagnosticSurfaceShapeRegistrationStatusLine` artifact and human output.

Behavior was correct, but definition shape-registration status field label preparation remained compressed inside shape-registration status line rendering.

## After

`_assemble_diagnostic_surface_definition_line_set(...)` now prepares `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel` through `_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)` before passing the unchanged label text to `_render_diagnostic_surface_definition_shape_registration_status_line(...)`.

`_render_diagnostic_surface_definition_shape_registration_status_line(...)` now receives an already prepared definition shape-registration status field label while preserving its existing status extraction and line-rendering behavior. `_render_diagnostic_surface_shape_registration_status_line(...)` preserves its default label for existing local callers while also accepting the prepared field label from the definition-specific path.

No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)` is the recovered producer for DiagnosticSurface definition shape-registration status field label preparation. It produces the implementation-local `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel` artifact.

## Recovered artifact/helper

The recovered helper is `_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)`.

The recovered artifact is `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel`, which carries the existing `shape_registration_status` field label between definition line-set assembly and definition shape-registration status line rendering.

It does not carry DiagnosticSurface definition identity heading rendering authority, definition status line rendering authority, definition CLI flags line rendering authority, definition description text preparation authority, definition description line rendering authority, definition JSON support value preparation authority, definition JSON support line rendering authority, definition record support value preparation authority, definition record support line rendering authority, definition record scope value preparation authority, definition record scope line rendering authority, definition boundary text preparation authority, definition boundary line rendering authority, definition consumption text preparation authority, definition consumption field label preparation authority, definition consumption line rendering authority, definition inventory registration field label preparation authority, definition inventory registration line rendering authority, definition shape-registration status extraction authority, definition shape-registration status line rendering authority, implementation reason rendering authority, evidence source rendering authority, top-level field indent selection authority, explanation rendering authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_definition_shape_registration_status_line(...)`

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

DiagnosticSurface definition shape-registration status field label preparation and DiagnosticSurface definition shape-registration status line rendering were previously compressed inside shape-registration status line rendering through an implicit default `shape_registration_status` field label.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Shape Registration Status Field Label Preparation
        !=
DiagnosticSurface Definition Shape Registration Status Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)` now owns the recovered DiagnosticSurface definition shape-registration status field label preparation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_prepare_diagnostic_surface_definition_shape_registration_status_field_label(...)` carries the recovered helper boundary, and `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel` carries the prepared shape-registration status field label.

### 5. Who consumes it?

`_render_diagnostic_surface_definition_shape_registration_status_line(...)` consumes `_DiagnosticSurfaceShapeRegistrationStatusFieldLabel.text` before returning the unchanged `_DiagnosticSurfaceShapeRegistrationStatusLine` artifact to definition line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_093.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 34 +++++++++++++++++++++++++++++-----
tests/test_diagnostic_inventory.py   | 12 +++++++++++-
2 files changed, 40 insertions(+), 6 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition identity heading line production, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description line rendering, definition JSON support value preparation, definition JSON support line rendering, definition record support value preparation, definition record support line rendering, definition record scope value preparation, definition record scope line rendering, definition boundary text preparation, definition boundary line rendering, definition consumption text preparation, definition consumption field label preparation, definition consumption line rendering, definition inventory registration field label preparation, definition inventory registration line rendering, definition shape-registration status field label preparation, definition shape-registration status line rendering, definition implementation reason rendering, definition evidence source rendering, top-level field indent selection, definition section label rendering, definition section indent rendering, and definition field label preparation outside this recovered definition-specific shape-registration status field label path;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific definition heading line rendering, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific definition section line rendering, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flag display preparation, explanation-specific CLI flags field label preparation, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific record support value preparation, explanation-specific record support field label preparation, explanation-specific record scope value preparation, explanation-specific record scope field label preparation, explanation-specific boundary text preparation, explanation-specific boundary field label preparation, explanation-specific boundary line rendering, explanation-specific consumption text preparation, explanation-specific consumption field label preparation, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display, description text preparation, JSON support value preparation, record support value preparation, record scope value preparation, consumption field label preparation, inventory registration field label preparation, and shape-registration status field label preparation;
- DiagnosticSurface shape-registration formatter coordination beyond status identification, definition shape-registration status field label preparation, and line rendering;
- DiagnosticSurface inventory registration formatter coordination beyond definition inventory registration field label preparation and line rendering;
- DiagnosticSurface consumption formatter coordination beyond definition consumption field label preparation, definition consumption line rendering, explanation consumption text preparation, explanation consumption field label preparation, explanation consumption line rendering, line rendering, and declaration-sequence extraction;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local definition shape-registration status field label preparation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
