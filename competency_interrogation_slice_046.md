# Competency Interrogation Slice 046

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Explanation Status Line Rendering
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

This slice begins immediately adjacent to Slice 045 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface explanation CLI flag display preparation was recovered, the same explanation line-set assembler still selected the nested definition `status` field and rendered the human status line while also assembling the complete explanation line set.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface explanation human rendering path:

- `_assemble_diagnostic_surface_explanation_line_set(...)` already consumes extracted explanation definition, boundary, consumption, CLI flag display, and nested field-indent artifacts before rendering unchanged explanation lines.
- The assembler still selected `definition["status"]` directly and invoked `_render_diagnostic_surface_status_line(...)` while owning the broader explanation line-set artifact.
- `_render_diagnostic_surface_status_line(...)` already owns generic status-line formatting, but the explanation-specific handoff from the extracted explanation definition to that rendered status-line artifact remained compressed in the assembler.
- The existing human output proves the rendered status line is consumed only as one member of the explanation definition section line set.

The directly observable recurring local pattern is that the explanation line-set assembler should consume a rendered status-line artifact, while a narrow explanation-specific producer owns selecting the existing status field from the extracted explanation definition and delegating to the existing status-line renderer.

## Before

The DiagnosticSurface explanation line-set assembler compressed two responsibilities:

1. DiagnosticSurface explanation human line-set assembly:
   - collect existing explanation lines in the existing order;
   - include the existing explanation heading, definition section marker, definition fields, boundary line, and consumption line;
   - return the existing private line-set artifact for human rendering.
2. DiagnosticSurface explanation status line rendering:
   - read the existing `status` member from the extracted explanation definition;
   - render the existing `_DiagnosticSurfaceStatusLine` artifact through the existing status-line renderer;
   - preserve the existing human output without promoting status rendering to a new public schema or generalized explanation renderer.

Behavior was correct, but explanation-specific status line rendering remained compressed inside broader explanation line-set assembly.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` now consumes `_render_diagnostic_surface_explanation_status_line(...)` before returning unchanged explanation lines.

`_render_diagnostic_surface_explanation_status_line(...)` owns only the existing handoff from `_DiagnosticSurfaceExplanationDefinition.definition["status"]` to `_render_diagnostic_surface_status_line(...)`. No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_render_diagnostic_surface_explanation_status_line(...)` is the recovered producer for DiagnosticSurface explanation status line rendering. It produces the existing `_DiagnosticSurfaceStatusLine` artifact for explanation human rendering.

## Recovered artifact/helper

The recovered helper is `_render_diagnostic_surface_explanation_status_line(...)`.

The carried artifact remains the existing `_DiagnosticSurfaceStatusLine`. This slice intentionally did not add a new artifact because the implementation evidence already contained the rendered status-line artifact needed by the consumer.

It does not carry DiagnosticSurface identity authority, explanation composition authority, explanation definition extraction authority, explanation boundary extraction authority, explanation consumption extraction authority, explanation CLI flag display preparation authority, explanation line-set assembly authority, heading rendering authority, definition-section marker authority, field indentation authority, generic status formatting rules, CLI flag rendering authority, description rendering authority, support-field rendering authority, boundary formatting authority, consumption formatting authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering authority.

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

DiagnosticSurface explanation human line-set assembly and DiagnosticSurface explanation status line rendering were previously compressed inside `_assemble_diagnostic_surface_explanation_line_set(...)` through direct selection of the extracted definition's `status` member during line-set assembly.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Explanation Status Line Rendering
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_explanation_status_line(...)` now owns the recovered DiagnosticSurface explanation status line rendering responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_render_diagnostic_surface_explanation_status_line(...)` carries the recovered helper boundary, and the existing `_DiagnosticSurfaceStatusLine` carries its rendered line output.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` consumes the rendered status line before returning its unchanged private line-set artifact to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_046.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 12 ++++++++++--
tests/test_diagnostic_inventory.py   | 18 ++++++++++++++++++
2 files changed, 28 insertions(+), 2 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition heading line production and top-level field indent selection;
- DiagnosticSurface explanation human rendering beyond explanation heading line production, nested definition extraction, explanation boundary extraction, explanation consumption extraction, explanation-specific CLI flag display preparation, explanation-specific status line rendering, and nested definition field indent selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display;
- DiagnosticSurface explanation field display preparation beyond status and CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering and statement-sequence extraction;
- DiagnosticSurface consumption formatter coordination beyond line rendering and declaration-sequence extraction;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local explanation status line rendering path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
