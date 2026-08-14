# Competency Interrogation Slice 070

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition JSON Support Value Preparation
        !=
DiagnosticSurface Definition JSON Support Line Rendering
```

This slice begins immediately adjacent to Slice 069 in `seed_runtime/diagnostic_inventory.py`. After the DiagnosticSurface definition description text preparation boundary was recovered, the neighboring DiagnosticSurface definition JSON support line still extracted the `supports_json` field directly while rendering the human line.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface definition human rendering path:

- `_assemble_diagnostic_surface_definition_line_set(...)` already prepares or selects artifacts before line-set assembly, including CLI flag display, definition description text, and top-level field indent.
- `_render_diagnostic_surface_definition_json_support_line(...)` already exists as a definition-specific producer for the rendered JSON support line consumed by the definition line-set assembler.
- Before this slice, `_render_diagnostic_surface_definition_json_support_line(...)` still compressed JSON support value extraction with JSON support line rendering by reading `definition["supports_json"]` directly.
- `_prepare_diagnostic_surface_cli_flag_display(...)`, `_prepare_diagnostic_surface_definition_description_text(...)`, `_prepare_diagnostic_surface_boundary_text(...)`, and `_prepare_diagnostic_surface_consumption_text(...)` show the recurring local pattern that human rendering consumes prepared display/text/value artifacts rather than letting every line renderer own source-field extraction.
- `_render_diagnostic_surface_json_support_line(...)` already owns the stable JSON support line text format.
- The existing human output proves the rendered JSON support line is consumed only as one member of the definition line set.

The directly observable recurring local pattern is that the definition line-set assembler should consume a prepared definition JSON support value artifact before asking the definition JSON support line renderer to render the line.

## Before

The DiagnosticSurface definition JSON support line renderer compressed two responsibilities:

1. DiagnosticSurface definition JSON support value preparation:
   - extract the existing `supports_json` field from the definition object;
   - preserve the existing value without changing JSON output, schema, diagnostics, or public CLI behavior.
2. DiagnosticSurface definition JSON support line rendering:
   - render the existing JSON support line with the selected definition field indent;
   - preserve the existing `_DiagnosticSurfaceJsonSupportLine` artifact and human output.

Behavior was correct, but definition JSON support value preparation remained compressed inside definition JSON support line rendering.

## After

`_assemble_diagnostic_surface_definition_line_set(...)` now prepares `_DiagnosticSurfaceJsonSupportValue` through `_prepare_diagnostic_surface_definition_json_support_value(...)` before passing it to `_render_diagnostic_surface_definition_json_support_line(...)`.

`_render_diagnostic_surface_definition_json_support_line(...)` now owns only definition JSON support line rendering from an already prepared JSON support value artifact. No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_prepare_diagnostic_surface_definition_json_support_value(...)` is the recovered producer for DiagnosticSurface definition JSON support value preparation. It produces the implementation-local `_DiagnosticSurfaceJsonSupportValue` artifact.

## Recovered artifact/helper

The recovered helper is `_prepare_diagnostic_surface_definition_json_support_value(...)`.

The recovered artifact is `_DiagnosticSurfaceJsonSupportValue`, which carries the existing `supports_json` value between definition field extraction and line rendering.

It does not carry DiagnosticSurface definition heading rendering authority, definition status rendering authority, definition CLI flags rendering authority, definition description text preparation authority, definition description line rendering authority, definition JSON support line rendering authority, definition record support rendering authority, definition record scope rendering authority, definition boundary rendering authority, definition consumption rendering authority, definition inventory registration rendering authority, definition shape registration rendering authority, definition implementation reason rendering authority, definition evidence source rendering authority, definition line-set assembly authority, CLI flag display preparation authority, field indentation authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is:

- `_render_diagnostic_surface_definition_json_support_line(...)`

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

DiagnosticSurface definition JSON support value preparation and DiagnosticSurface definition JSON support line rendering were previously compressed inside `_render_diagnostic_surface_definition_json_support_line(...)` through direct extraction of `definition["supports_json"]` during line rendering.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition JSON Support Value Preparation
        !=
DiagnosticSurface Definition JSON Support Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_prepare_diagnostic_surface_definition_json_support_value(...)` now owns the recovered DiagnosticSurface definition JSON support value preparation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_prepare_diagnostic_surface_definition_json_support_value(...)` carries the recovered helper boundary, and `_DiagnosticSurfaceJsonSupportValue` carries the prepared JSON support value.

### 5. Who consumes it?

`_render_diagnostic_surface_definition_json_support_line(...)` consumes `_DiagnosticSurfaceJsonSupportValue` before returning the unchanged `_DiagnosticSurfaceJsonSupportLine` artifact to definition line-set assembly.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_070.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 22 +++++++++++++++++++---
tests/test_diagnostic_inventory.py   | 10 +++++++++-
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

- DiagnosticSurface definition human rendering beyond definition identity heading line production, definition status line rendering, definition CLI flags line rendering, definition description text preparation, definition description line rendering, definition JSON support value preparation, definition JSON support line rendering, definition record support rendering, definition record scope rendering, definition boundary line rendering, definition consumption line rendering, definition inventory registration line rendering, definition shape registration status line rendering, definition implementation reason rendering, definition evidence source rendering, and top-level field indent selection;
- DiagnosticSurface explanation human rendering beyond nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific definition heading line rendering, explanation-specific definition section line rendering, explanation-specific CLI flag display preparation, explanation-specific CLI flags line rendering, explanation-specific status line rendering, explanation-specific description line rendering, explanation-specific JSON support rendering, explanation-specific record support rendering, explanation-specific record scope line rendering, explanation-specific boundary line rendering, explanation-specific consumption line rendering, and nested definition field indent selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display, description text preparation, and JSON support value preparation;
- DiagnosticSurface explanation field display preparation beyond status, CLI flag, CLI flags line, description, JSON support, record support, record scope, boundary, consumption, definition heading display, and definition section line rendering;
- DiagnosticSurface consumption formatter coordination beyond definition consumption line rendering, explanation consumption line rendering, line rendering, and declaration-sequence extraction;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local definition JSON support value preparation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
