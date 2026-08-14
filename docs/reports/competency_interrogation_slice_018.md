# Competency Interrogation Slice 018

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Definition Line Set Assembly
        !=
DiagnosticSurface Definition Human Rendering
```

This slice begins immediately adjacent to Slice 017 in `seed_runtime/diagnostic_inventory.py`. After consumption declaration set assembly was separated from consumption identification, the same DiagnosticSurface neighborhood still exposed one narrow compressed responsibility: `format_diagnostic_surface_definition(...)` both assembled the ordered human-readable definition lines and rendered those lines into the final newline-delimited string. The evidence is implementation-local and does not introduce Competency Interrogation Grammar, a framework, engine, registry, router, planner, scheduler, orchestration layer, methodology owner, constitutional abstraction, diagnostic framework, generalized owner, or architectural redesign.

## Implementation evidence

Implementation evidence was concentrated in `format_diagnostic_surface_definition(...)`:

- The function already consumed the existing DiagnosticSurface definition dictionary produced by `build_diagnostic_surface_definition(...)`.
- The same function also prepared the display-only CLI flag text and selected the exact ordered human-readable lines for the definition view.
- Joining the already-selected lines into the final string is distinct from deciding which lines belong to the definition view and in what order.
- Existing nearby helpers had already recovered comparable presentation-preparation artifacts for CLI flag display, boundary text, and consumption text, making line-set assembly directly observable as a local presentation responsibility rather than a new generalized renderer.
- The recovered line-set assembly has no authority over JSON output, diagnostic inventory registration, shape-audit registration, boundary identification, consumption identification, read-only evaluation, CLI behavior, event-ledger behavior, cluster mutation behavior, or unknown-surface semantics.

The observable pressure was therefore narrow: assembling the existing DiagnosticSurface definition human line set is distinct from rendering that line set.

## Before

`format_diagnostic_surface_definition(...)` compressed two responsibilities:

1. DiagnosticSurface definition line set assembly:
   - consume the existing definition dictionary;
   - prepare existing CLI flag display text;
   - select the existing ordered human-readable definition lines;
   - preserve existing boundary and consumption line formatting through the existing local helpers.
2. DiagnosticSurface definition human rendering:
   - join the selected lines with newlines;
   - return the unchanged CLI-facing string.

Behavior was correct, but ordered line selection was implicit inside final string rendering.

## After

A private implementation-local line-set assembly owner now exists:

- `_DiagnosticSurfaceDefinitionLineSet`
- `_assemble_diagnostic_surface_definition_line_set(...)`

`format_diagnostic_surface_definition(...)` now asks that producer for the existing ordered definition lines and then continues to render the unchanged newline-delimited string.

## Recovered producer

`_assemble_diagnostic_surface_definition_line_set(...)` is the recovered producer. It consumes an existing DiagnosticSurface definition dictionary and produces only the ordered human-readable definition lines used by the existing formatter.

## Recovered artifact/helper

`_DiagnosticSurfaceDefinitionLineSet` is the recovered private artifact. It carries only:

- `lines`

It does not carry DiagnosticSurface identity authority, JSON authority, shape-registration authority, boundary identification authority, consumption identification authority, diagnostic inventory registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is `format_diagnostic_surface_definition(...)`.

Downstream existing consumers remain unchanged:

- `seed --diagnostic-surface-definition <surface>`
- human-readable DiagnosticSurface definition output

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

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

DiagnosticSurface definition line set assembly and DiagnosticSurface definition human rendering were previously compressed inside `format_diagnostic_surface_definition(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Definition Line Set Assembly
        !=
DiagnosticSurface Definition Human Rendering
```

### 3. What producer now owns the recovered responsibility?

`_assemble_diagnostic_surface_definition_line_set(...)` now owns the recovered ordered definition line assembly responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceDefinitionLineSet` carries the ordered human-readable definition lines. It is a private implementation-local artifact.

### 5. Who consumes it?

`format_diagnostic_surface_definition(...)` consumes the line set before producing the unchanged newline-delimited human output.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_018.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 20 +++++++++++++++++---
tests/test_diagnostic_inventory.py   | 23 +++++++++++++++++++++++
2 files changed, 40 insertions(+), 3 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
60 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- human-readable DiagnosticSurface explanation line assembly;
- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- DiagnosticSurface shape registration status presentation;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local definition line-set path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
