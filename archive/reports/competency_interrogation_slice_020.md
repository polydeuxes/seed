# Competency Interrogation Slice 020

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Boundary Statement Sequence Extraction
        !=
DiagnosticSurface Boundary Text Rendering
```

This slice begins immediately adjacent to Slice 019 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface explanation line set assembly was separated from explanation human rendering, the next directly adjacent implementation-local formatter path exposed a narrower compression: `_prepare_diagnostic_surface_boundary_text(...)` both extracted the ordered `statements` sequence from the existing boundary payload and rendered that sequence into the semicolon-delimited text consumed by boundary line rendering.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, or public surface.

## Implementation evidence

Implementation evidence was concentrated in `_prepare_diagnostic_surface_boundary_text(...)`:

- `_format_diagnostic_surface_boundary(...)` already delegates boundary statement text preparation before adding the existing `diagnostic_surface_boundary:` line prefix.
- `_prepare_diagnostic_surface_boundary_text(...)` already handled two distinct local steps: validating/extracting the ordered boundary `statements` payload and joining those statements into the existing semicolon-delimited text.
- Boundary payloads are produced earlier from DiagnosticSurface boundary identification and consumed by both DiagnosticSurface definition and explanation human line assembly.
- Empty, missing, or non-dictionary boundary payloads already collapse to the existing `unknown` text; that behavior remains unchanged.
- The recovered sequence extractor has no authority over DiagnosticSurface identity, boundary identification, read-only evaluation, JSON output, diagnostic inventory registration, shape-audit registration, CLI flag parsing, event-ledger behavior, cluster mutation behavior, or public compatibility.

The observable pressure was therefore narrow: extracting the existing ordered boundary statement sequence is distinct from rendering that sequence as display text.

## Before

`_prepare_diagnostic_surface_boundary_text(...)` compressed two responsibilities:

1. DiagnosticSurface boundary statement sequence extraction:
   - confirm the boundary payload is a dictionary;
   - read the existing `statements` field;
   - reject missing, non-list, or empty statement payloads as no renderable sequence;
   - preserve the existing statement order.
2. DiagnosticSurface boundary text rendering:
   - render a missing sequence as `unknown`;
   - join the extracted statement sequence with `; `;
   - return the unchanged `_DiagnosticSurfaceBoundaryText` artifact.

Behavior was correct, but sequence extraction was implicit inside text rendering.

## After

A private implementation-local sequence extraction owner now exists:

- `_DiagnosticSurfaceBoundaryStatementSequence`
- `_extract_diagnostic_surface_boundary_statement_sequence(...)`

`_prepare_diagnostic_surface_boundary_text(...)` now asks that producer for the existing ordered boundary statement sequence and then continues to render the unchanged display text.

## Recovered producer

`_extract_diagnostic_surface_boundary_statement_sequence(...)` is the recovered producer. It consumes an existing boundary payload and produces only the ordered statement sequence that boundary text rendering already used.

## Recovered artifact/helper

`_DiagnosticSurfaceBoundaryStatementSequence` is the recovered private artifact. It carries only:

- `statements`

It does not carry DiagnosticSurface identity authority, JSON authority, shape-registration authority, boundary identification authority, read-only evaluation authority, diagnostic inventory registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is `_prepare_diagnostic_surface_boundary_text(...)`.

Downstream existing consumers remain unchanged:

- `_format_diagnostic_surface_boundary(...)`
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

DiagnosticSurface boundary statement sequence extraction and DiagnosticSurface boundary text rendering were previously compressed inside `_prepare_diagnostic_surface_boundary_text(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Boundary Statement Sequence Extraction
        !=
DiagnosticSurface Boundary Text Rendering
```

### 3. What producer now owns the recovered responsibility?

`_extract_diagnostic_surface_boundary_statement_sequence(...)` now owns the recovered ordered boundary statement sequence extraction responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceBoundaryStatementSequence` carries the ordered boundary statements. It is a private implementation-local artifact.

### 5. Who consumes it?

`_prepare_diagnostic_surface_boundary_text(...)` consumes the sequence before producing the unchanged `_DiagnosticSurfaceBoundaryText` display artifact.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_020.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 34 +++++++++++++++++++++---------
tests/test_diagnostic_inventory.py   | 40 +++++++++++++++++++++++++++++++-----
2 files changed, 59 insertions(+), 15 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
62 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface boundary text rendering beyond statement sequence extraction;
- DiagnosticSurface boundary line rendering beyond boundary text preparation;
- DiagnosticSurface consumption declaration text preparation;
- DiagnosticSurface consumption line rendering;
- DiagnosticSurface explanation human rendering beyond line-set assembly;
- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- DiagnosticSurface shape registration status presentation;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local boundary statement text path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
