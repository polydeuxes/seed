# Competency Interrogation Slice 044

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Explanation Consumption Extraction
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

This slice begins immediately adjacent to Slice 043 in `seed_runtime/diagnostic_inventory.py`. After DiagnosticSurface explanation boundary extraction was recovered, the neighboring explanation line-set assembler still directly selected the nested `diagnostic_surface_consumption` payload while also assembling the complete human explanation line set.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, public surface, diagnostic surface, schema field, event-ledger behavior, or cluster mutation behavior.

## Implementation evidence

Implementation evidence was concentrated around the adjacent DiagnosticSurface explanation human rendering path:

- `build_diagnostic_surface_explanation(...)` composes an explanation wrapper whose payload contains `diagnostic_surface_definition`, `diagnostic_surface_boundary`, and `diagnostic_surface_consumption` members.
- `_DiagnosticSurfaceExplanationComposition.to_json_dict(...)` preserves the existing `diagnostic_surface_consumption` member by copying it from the existing DiagnosticSurface definition payload.
- `_assemble_diagnostic_surface_explanation_line_set(...)` already consumed extracted explanation definition and explanation boundary artifacts before rendering unchanged explanation lines.
- The same assembler still selected `explanation["diagnostic_surface_consumption"]` directly during line-set assembly, making consumption extraction the next implementation-local responsibility directly observable beside the Slice 043 boundary extraction path.

The directly observable recurring local pattern is that the explanation line-set assembler should consume a prepared explanation consumption artifact, while a narrow producer owns the existing extraction of the consumption payload.

## Before

The DiagnosticSurface explanation line-set assembler compressed two responsibilities:

1. DiagnosticSurface explanation human line-set assembly:
   - collect existing explanation lines in the existing order;
   - include the existing explanation heading, definition section marker, definition fields, boundary line, and consumption line;
   - return the existing private line-set artifact for human rendering.
2. DiagnosticSurface explanation consumption extraction:
   - read the existing `diagnostic_surface_consumption` member from the explanation payload;
   - make that consumption payload available to the existing consumption formatter;
   - preserve the existing JSON and human output without promoting the consumption member to a new schema authority or generalized explanation model.

Behavior was correct, but consumption extraction remained compressed inside broader explanation line-set assembly.

## After

`_assemble_diagnostic_surface_explanation_line_set(...)` now consumes `_extract_diagnostic_surface_explanation_consumption(...)` before rendering unchanged explanation lines.

`_extract_diagnostic_surface_explanation_consumption(...)` owns only the existing `diagnostic_surface_consumption` extraction and returns a private `_DiagnosticSurfaceExplanationConsumption` artifact. No new public surface or generalized rendering abstraction was introduced.

## Recovered producer

`_extract_diagnostic_surface_explanation_consumption(...)` is the recovered producer for DiagnosticSurface explanation consumption extraction. It produces the existing consumption payload as a private implementation-local artifact for explanation human rendering.

## Recovered artifact/helper

The recovered helper is `_extract_diagnostic_surface_explanation_consumption(...)`.

The recovered private artifact is `_DiagnosticSurfaceExplanationConsumption`. It carries only:

- `consumption`

It does not carry DiagnosticSurface identity authority, explanation composition authority, explanation definition extraction authority, explanation boundary extraction authority, explanation line-set assembly authority, heading rendering authority, definition-section marker authority, field indentation authority, field display preparation authority, field line rendering authority, boundary formatting authority, boundary statement extraction authority, consumption formatting authority, consumption declaration extraction authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, schema authority, or generalized rendering authority.

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

DiagnosticSurface explanation human line-set assembly and DiagnosticSurface explanation consumption extraction were previously compressed inside `_assemble_diagnostic_surface_explanation_line_set(...)` through direct selection of the `diagnostic_surface_consumption` member during line-set assembly.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Explanation Consumption Extraction
        !=
DiagnosticSurface Explanation Human Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_extract_diagnostic_surface_explanation_consumption(...)` now owns the recovered DiagnosticSurface explanation consumption extraction responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_extract_diagnostic_surface_explanation_consumption(...)` carries the recovered helper boundary, and `_DiagnosticSurfaceExplanationConsumption` carries its extracted consumption output.

### 5. Who consumes it?

`_assemble_diagnostic_surface_explanation_line_set(...)` consumes the extracted explanation consumption before returning its unchanged private line-set artifact to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_044.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 20 +++++++++++++++++++-
tests/test_diagnostic_inventory.py   | 19 +++++++++++++++++++
2 files changed, 38 insertions(+), 1 deletion(-)
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
- DiagnosticSurface explanation human rendering beyond explanation heading line production, nested definition extraction, explanation boundary extraction, explanation consumption extraction, and nested definition field indent selection;
- DiagnosticSurface definition field display preparation beyond CLI flag display;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering and statement-sequence extraction;
- DiagnosticSurface consumption formatter coordination beyond line rendering and declaration-sequence extraction;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local explanation consumption extraction path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
