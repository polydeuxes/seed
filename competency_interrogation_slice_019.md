# Competency Interrogation Slice 019

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Explanation Line Set Assembly
        !=
DiagnosticSurface Explanation Human Rendering
```

This slice begins immediately adjacent to Slice 018 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface definition line set assembly was separated from definition human rendering, the neighboring DiagnosticSurface explanation formatter exposed the same narrow local compression: `format_diagnostic_surface_explanation(...)` both assembled the existing ordered human-readable explanation lines and rendered those lines into the final newline-delimited string.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, router, planner, scheduler, orchestration layer, methodology owner, constitutional abstraction, diagnostic framework, generalized owner, or architectural redesign.

## Implementation evidence

Implementation evidence was concentrated in `format_diagnostic_surface_explanation(...)`:

- The function already consumed the existing DiagnosticSurface explanation dictionary produced by `build_diagnostic_surface_explanation(...)`.
- The same function also prepared display-only CLI flag text and selected the exact ordered human-readable explanation lines.
- Joining the already-selected lines into the final string is distinct from deciding which lines belong to the explanation view and in what order.
- The adjacent DiagnosticSurface definition path had already recovered the same kind of implementation-local line-set artifact without changing behavior, JSON, diagnostics, schema, event-ledger behavior, or CLI compatibility.
- The recovered line-set assembly has no authority over DiagnosticSurface identity, definition composition, boundary identification, consumption identification, JSON output, inventory registration, shape-audit registration, CLI flag parsing, event-ledger behavior, cluster mutation behavior, or unknown-surface semantics.

The observable pressure was therefore narrow: assembling the existing DiagnosticSurface explanation human line set is distinct from rendering that line set.

## Before

`format_diagnostic_surface_explanation(...)` compressed two responsibilities:

1. DiagnosticSurface explanation line set assembly:
   - consume the existing explanation dictionary;
   - prepare existing CLI flag display text;
   - select the existing ordered human-readable explanation lines;
   - preserve existing boundary and consumption line formatting through the existing local helpers.
2. DiagnosticSurface explanation human rendering:
   - join the selected lines with newlines;
   - return the unchanged CLI-facing string.

Behavior was correct, but ordered explanation line selection was implicit inside final string rendering.

## After

A private implementation-local line-set assembly owner now exists:

- `_DiagnosticSurfaceExplanationLineSet`
- `_assemble_diagnostic_surface_explanation_line_set(...)`

`format_diagnostic_surface_explanation(...)` now asks that producer for the existing ordered explanation lines and then continues to render the unchanged newline-delimited string.

## Recovered producer

`_assemble_diagnostic_surface_explanation_line_set(...)` is the recovered producer. It consumes an existing DiagnosticSurface explanation dictionary and produces only the ordered human-readable explanation lines used by the existing formatter.

## Recovered artifact/helper

`_DiagnosticSurfaceExplanationLineSet` is the recovered private artifact. It carries only:

- `lines`

It does not carry DiagnosticSurface identity authority, JSON authority, shape-registration authority, boundary identification authority, consumption identification authority, diagnostic inventory registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is `format_diagnostic_surface_explanation(...)`.

Downstream existing consumers remain unchanged:

- `seed --diagnostic-surface-explanation <surface>`
- human-readable DiagnosticSurface explanation output

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

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

DiagnosticSurface explanation line set assembly and DiagnosticSurface explanation human rendering were previously compressed inside `format_diagnostic_surface_explanation(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Explanation Line Set Assembly
        !=
DiagnosticSurface Explanation Human Rendering
```

### 3. What producer now owns the recovered responsibility?

`_assemble_diagnostic_surface_explanation_line_set(...)` now owns the recovered ordered explanation line assembly responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceExplanationLineSet` carries the ordered human-readable explanation lines. It is a private implementation-local artifact.

### 5. Who consumes it?

`format_diagnostic_surface_explanation(...)` consumes the line set before producing the unchanged newline-delimited human output.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_019.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 20 +++++++++++++++++---
tests/test_diagnostic_inventory.py   | 25 +++++++++++++++++++++++++
2 files changed, 42 insertions(+), 3 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
61 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface explanation human rendering beyond line-set assembly;
- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- DiagnosticSurface shape registration status presentation;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local explanation line-set path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
