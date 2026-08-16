# Competency Interrogation Slice 167

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Evidence-Source Line Rendering
        !=
DiagnosticSurface Generic Evidence-Source Line Rendering
```

This slice begins from the implementation immediately adjacent to Slice 166 in `seed_runtime/diagnostic_inventory.py` and `tests/test_diagnostic_inventory.py`. After definition evidence-source value preparation became observable, the next adjacent implementation-local responsibility is the definition-specific evidence-source renderer adapter consumed by the definition line-set assembly path.

`_render_diagnostic_surface_definition_evidence_source_line(...)` owns unwrapping the prepared `_DiagnosticSurfaceEvidenceSourceValue` and forwarding the caller-selected field label and indent to the generic evidence-source line renderer. `_render_diagnostic_surface_evidence_source_line(...)` remains responsible for the generic formatted line from a raw value, label, and indent.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, cluster mutation behavior, CLI behavior, JSON behavior, or runtime behavior.

## Implementation evidence

Implementation evidence is concentrated around the DiagnosticSurface definition evidence-source line-rendering adapter:

- `_assemble_diagnostic_surface_definition_line_set(...)` passes `evidence_source_value`, `field_label=evidence_source_field_label.text`, and `indent=field_indent.text` into `_render_diagnostic_surface_definition_evidence_source_line(...)`.
- `_render_diagnostic_surface_definition_evidence_source_line(...)` accepts the prepared `_DiagnosticSurfaceEvidenceSourceValue` artifact, requires a caller-provided field label, keeps the existing default indent, unwraps `evidence_source_value.value`, and delegates final string construction to `_render_diagnostic_surface_evidence_source_line(...)`.
- `_render_diagnostic_surface_evidence_source_line(...)` remains the generic producer of `_DiagnosticSurfaceEvidenceSourceLine` from a raw evidence-source value, field label, and indent.
- `test_diagnostic_surface_definition_evidence_source_line_rendering_delegates_generic_line_rendering` proves the adapter signature, prepared-value consumption, generic renderer delegation, field-label forwarding, indent forwarding, output artifact, and unchanged rendered line.

The directly observable recurring local pattern is that definition-specific line renderers adapt prepared definition artifacts before delegating generic line construction.

## Before

The definition evidence-source line rendered correctly, and existing behavior was correct. However, the implementation evidence did not separately prove that definition evidence-source line rendering owns only the definition-specific adapter responsibility: consuming the prepared value artifact and forwarding its unwrapped value, the supplied label, and the supplied indent to the generic renderer.

Definition-specific evidence-source line rendering and generic evidence-source line construction were therefore compressed in the available test evidence.

## After

`test_diagnostic_surface_definition_evidence_source_line_rendering_delegates_generic_line_rendering` now proves that `_render_diagnostic_surface_definition_evidence_source_line(...)` consumes `_DiagnosticSurfaceEvidenceSourceValue`, unwraps `evidence_source_value.value`, forwards `field_label` and `indent`, and delegates final line construction to `_render_diagnostic_surface_evidence_source_line(...)`.

`_render_diagnostic_surface_definition_evidence_source_line(...)` remains the recovered definition-specific adapter producer. `_render_diagnostic_surface_evidence_source_line(...)` remains the generic evidence-source line producer.

No public output, JSON shape, CLI behavior, diagnostics, event-ledger behavior, cluster mutation behavior, schema, or compatibility boundary changed.

## Recovered producer

`_render_diagnostic_surface_definition_evidence_source_line(...)` is the recovered producer for DiagnosticSurface definition evidence-source line rendering.

## Recovered artifact/helper

The recovered helper is `_render_diagnostic_surface_definition_evidence_source_line(...)`.

The helper consumes the already-existing `_DiagnosticSurfaceEvidenceSourceValue` artifact and produces the already-existing `_DiagnosticSurfaceEvidenceSourceLine` artifact by delegating generic line construction.

It does not carry evidence-source value extraction authority, evidence-source field-label preparation authority, generic evidence-source line construction authority, implementation-reason field-label preparation authority, implementation-reason value preparation authority, implementation-reason line rendering authority, shape-registration-status field-label preparation authority, shape-registration-status value preparation authority, shape-registration-status line rendering authority, inventory-registration field-label preparation authority, inventory-registration value preparation authority, inventory-registration line rendering authority, consumption text preparation authority, consumption field-label preparation authority, boundary text preparation authority, boundary field-label preparation authority, record scope value preparation authority, record support value preparation authority, JSON support value preparation authority, description text extraction authority, description field-label preparation authority, CLI flag display authority, status preparation authority, field indent selection authority, line-set ordering authority, event-ledger authority, cluster mutation authority, schema authority, public CLI authority, or generalized rendering ownership.

## Recovered consumer

The immediate consumer is:

- `_assemble_diagnostic_surface_definition_line_set(...)`

Downstream existing consumers remain unchanged:

- `format_diagnostic_surface_definition(...)`
- `seed --diagnostic-surface-definition <surface>`
- `seed --diagnostic-surface-definition <surface> --json` for the unchanged alternate JSON path

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

DiagnosticSurface definition evidence-source line rendering and generic DiagnosticSurface evidence-source line construction were previously compressed in the test evidence because the test suite did not separately prove that the definition renderer only adapts the prepared definition value and delegates generic line construction.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Evidence-Source Line Rendering
        !=
DiagnosticSurface Generic Evidence-Source Line Rendering
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_definition_evidence_source_line(...)` owns the recovered definition evidence-source line-rendering adapter responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_render_diagnostic_surface_definition_evidence_source_line(...)` carries the recovered boundary. It consumes `_DiagnosticSurfaceEvidenceSourceValue` and produces `_DiagnosticSurfaceEvidenceSourceLine` through the generic renderer delegation.

### 5. Who consumes it?

`_assemble_diagnostic_surface_definition_line_set(...)` consumes the definition evidence-source line renderer by passing the prepared value artifact, field label, and indent into `_render_diagnostic_surface_definition_evidence_source_line(...)`. The definition formatter and CLI definition surface consume the assembled line set downstream.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_167.md`

## LOC changed

Implementation and test diff before this report:

```text
tests/test_diagnostic_inventory.py | 41 ++++++++++++++++++++++++++++++++++++++
1 file changed, 41 insertions(+)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond definition evidence-source value preparation, definition evidence-source field-label preparation, definition evidence-source line-rendering adapter delegation, definition implementation-reason field-label preparation, definition shape-registration-status field-label preparation, definition inventory-registration field-label preparation, definition consumption field-label preparation, definition consumption text preparation, definition boundary text preparation, definition record scope value preparation, definition record support value preparation, definition JSON support value preparation, definition description field-label preparation, definition description text preparation, definition CLI flag display preparation, definition name value preparation, and top-level definition field indent selection, including definition identity heading line rendering responsibilities outside prior recovered boundaries, definition status value preparation, definition status line rendering responsibilities outside prior recovered boundaries, definition CLI flags line rendering responsibilities outside prior recovered boundaries, definition description line rendering responsibilities outside prior recovered boundaries, definition JSON support field-label preparation, definition record support field-label preparation, definition record support line rendering responsibilities outside prior recovered boundaries, definition record scope field-label production, definition record scope line rendering responsibilities outside prior recovered boundaries, definition boundary field-label production, definition boundary line rendering responsibilities outside prior recovered boundaries, definition consumption line rendering responsibilities outside prior recovered boundaries, definition consumption line-set inclusion, definition inventory-registration value preparation, definition inventory-registration line rendering responsibilities outside prior recovered boundaries, definition shape-registration-status value preparation, definition shape-registration-status line rendering responsibilities outside prior recovered boundaries, definition implementation-reason value source extraction, definition implementation-reason line rendering responsibilities outside prior recovered boundaries, and definition line-set assembly responsibilities outside this recovered boundary;
- DiagnosticSurface explanation human rendering beyond nested definition field indent selection, nested definition consumption line delegation, explanation consumption text delegation, explanation definition heading line rendering, explanation definition section line rendering, explanation boundary extraction, explanation consumption extraction, explanation-specific name value preparation, explanation-specific CLI flag display preparation, explanation-specific definition section label preparation, explanation-specific definition section indent selection, explanation-specific status value preparation, explanation-specific status field label preparation, explanation-specific status line rendering, explanation-specific CLI flags field label preparation, explanation-specific CLI flags line rendering responsibilities outside prior recovered boundaries, explanation-specific description text preparation, explanation-specific description field label preparation, explanation-specific description line rendering responsibilities outside prior recovered boundaries, explanation-specific JSON support value preparation, explanation-specific JSON support field label preparation, explanation-specific JSON support line rendering responsibilities outside prior recovered boundaries, explanation-specific record support value preparation, explanation-specific record support field-label preparation, explanation-specific record scope value preparation, explanation-specific record scope field-label preparation, generic consumption text formatting beyond the prior recovered delegation boundary, generic consumption line construction beyond prior recovered delegation boundary, and explanation line-set inclusion responsibilities outside prior recovered boundaries;
- DiagnosticSurface shape-registration formatter coordination beyond shape-registration lookup, shape-registration status identification, generic value production, generic field-label production, and generic line rendering;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, definition, or rendering semantics outside this local boundary delegation path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
