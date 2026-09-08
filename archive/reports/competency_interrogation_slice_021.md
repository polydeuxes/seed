# Competency Interrogation Slice 021

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Consumption Declaration Sequence Extraction
        !=
DiagnosticSurface Consumption Text Rendering
```

This slice begins immediately adjacent to Slice 020 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface boundary statement sequence extraction was separated from boundary text rendering, the next directly adjacent DiagnosticSurface formatter path exposed the same kind of narrow local compression: `_prepare_diagnostic_surface_consumption_text(...)` both extracted the ordered `declared_consumption` items from the existing consumption payload and rendered those items into the semicolon-delimited text consumed by consumption line rendering.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, or public surface.

## Implementation evidence

Implementation evidence was concentrated in `_prepare_diagnostic_surface_consumption_text(...)`:

- `_format_diagnostic_surface_consumption(...)` already delegates consumption declaration text preparation before adding the existing `diagnostic_surface_consumption:` line prefix.
- `_prepare_diagnostic_surface_consumption_text(...)` already handled two distinct local steps: validating/extracting the ordered `declared_consumption` mapping items and rendering those declarations into the existing semicolon-delimited text.
- Consumption payloads are produced earlier from DiagnosticSurface consumption identification and consumed by both DiagnosticSurface definition and explanation human line assembly.
- Empty, missing, or non-dictionary consumption payloads already collapse to the existing `unknown` text; that behavior remains unchanged.
- The recovered sequence extractor has no authority over DiagnosticSurface identity, consumption identification, boundary identification, read-only evaluation, JSON output, diagnostic inventory registration, shape-audit registration, CLI flag parsing, event-ledger behavior, cluster mutation behavior, or public compatibility.

The observable pressure was therefore narrow: extracting the existing ordered consumption declaration sequence is distinct from rendering that sequence as display text.

## Before

`_prepare_diagnostic_surface_consumption_text(...)` compressed two responsibilities:

1. DiagnosticSurface consumption declaration sequence extraction:
   - confirm the consumption payload is a dictionary;
   - read the existing `declared_consumption` field;
   - reject missing, non-dictionary, or empty declaration payloads as no renderable sequence;
   - preserve the existing declaration order from the payload mapping.
2. DiagnosticSurface consumption text rendering:
   - render a missing sequence as `unknown`;
   - render declaration values through the existing lowercase string conversion;
   - join the extracted declaration sequence with `; `;
   - return the unchanged `_DiagnosticSurfaceConsumptionText` artifact.

Behavior was correct, but declaration sequence extraction was implicit inside text rendering.

## After

A private implementation-local declaration sequence extraction owner now exists:

- `_DiagnosticSurfaceConsumptionDeclarationSequence`
- `_extract_diagnostic_surface_consumption_declaration_sequence(...)`

`_prepare_diagnostic_surface_consumption_text(...)` now asks that producer for the existing ordered consumption declaration sequence and then continues to render the unchanged display text.

## Recovered producer

`_extract_diagnostic_surface_consumption_declaration_sequence(...)` is the recovered producer. It consumes an existing consumption payload and produces only the ordered declaration sequence that consumption text rendering already used.

## Recovered artifact/helper

`_DiagnosticSurfaceConsumptionDeclarationSequence` is the recovered private artifact. It carries only:

- `declarations`

It does not carry DiagnosticSurface identity authority, JSON authority, shape-registration authority, consumption identification authority, boundary identification authority, read-only evaluation authority, diagnostic inventory registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is `_prepare_diagnostic_surface_consumption_text(...)`.

Downstream existing consumers remain unchanged:

- `_format_diagnostic_surface_consumption(...)`
- `_assemble_diagnostic_surface_definition_line_set(...)`
- `_assemble_diagnostic_surface_explanation_line_set(...)`
- `seed --diagnostic-surface-definition <surface>`
- `seed --diagnostic-surface-explanation <surface>`

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

- `seed --diagnostic-surface-definition diagnostic_shape_audit`
- `seed --diagnostic-surface-explanation diagnostic_shape_audit`
- `seed --diagnostic-surface-definition diagnostic_shape_audit --json`
- `seed --diagnostic-surface-explanation diagnostic_shape_audit --json`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

## Required questions

### 1. What responsibilities were previously compressed?

DiagnosticSurface consumption declaration sequence extraction and DiagnosticSurface consumption text rendering were previously compressed inside `_prepare_diagnostic_surface_consumption_text(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Consumption Declaration Sequence Extraction
        !=
DiagnosticSurface Consumption Text Rendering
```

### 3. What producer now owns the recovered responsibility?

`_extract_diagnostic_surface_consumption_declaration_sequence(...)` now owns the recovered ordered consumption declaration sequence extraction responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceConsumptionDeclarationSequence` carries the ordered consumption declarations. It is a private implementation-local artifact.

### 5. Who consumes it?

`_prepare_diagnostic_surface_consumption_text(...)` consumes the sequence before producing the unchanged `_DiagnosticSurfaceConsumptionText` display artifact.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_021.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 26 ++++++++++++++++++++----
tests/test_diagnostic_inventory.py   | 39 ++++++++++++++++++++++++++++++++++++
2 files changed, 61 insertions(+), 4 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
63 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface consumption text rendering beyond declaration sequence extraction;
- DiagnosticSurface consumption line rendering beyond consumption text preparation;
- DiagnosticSurface boundary text rendering beyond statement sequence extraction;
- DiagnosticSurface boundary line rendering beyond boundary text preparation;
- DiagnosticSurface explanation human rendering beyond line-set assembly;
- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- DiagnosticSurface shape registration status presentation;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local consumption declaration text path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
