# Competency Interrogation Slice 015

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Read-Only Boundary Evaluation
        !=
DiagnosticSurface Boundary Statement Identification
```

This slice begins immediately adjacent to Slice 014 in `seed_runtime/diagnostic_inventory.py`. The current Diagnostic Surface neighborhood was not exhausted: after shape-registration lookup was separated from shape-registration status identification, the same local definition-production path still exposed a separate compressed responsibility in `_identify_diagnostic_surface_boundary(...)`. The evidence is implementation-local and does not require Competency Interrogation Grammar, a framework, engine, registry, router, planner, scheduler, orchestration layer, methodology owner, constitutional abstraction, diagnostic framework, generalized Diagnostic Surface abstraction, or architectural redesign.

## Implementation evidence

Implementation evidence was concentrated in `_identify_diagnostic_surface_boundary(...)`:

- The function already produced the public boundary statement tuple used by the existing DiagnosticSurface definition payload.
- Inside that statement identification path, a distinct boolean expression evaluated whether the surface was read-only by combining five inventory fields: `supports_record`, `writes_event_ledger`, `mutates_cluster`, `emits_diagnostic_facts`, and `emits_cluster_facts`.
- That boolean was then consumed only to decide whether the existing `read-only` statement should be inserted before the rest of the boundary statements.
- The read-only evaluation has no authority over JSON shape, diagnostic inventory registration, shape-audit registration, event-ledger behavior, cluster mutation behavior, CLI flags, rendering, or the rest of the boundary statement vocabulary.

The observable pressure was therefore narrow: deciding whether a surface is read-only is distinct from identifying the full ordered boundary statement set.

## Before

`_identify_diagnostic_surface_boundary(...)` compressed two responsibilities:

1. DiagnosticSurface read-only boundary evaluation:
   - inspect existing diagnostic inventory fields that determine read-only status;
   - collapse those fields into one implementation-local boolean.
2. DiagnosticSurface boundary statement identification:
   - produce the ordered public boundary statement tuple;
   - insert the existing `read-only` statement when the read-only evaluation is true;
   - return `_DiagnosticSurfaceBoundaryIdentification` for definition composition.

Behavior was correct, but the read-only evaluation was implicit inside boundary statement identification.

## After

A private implementation-local read-only evaluation owner now exists:

- `_DiagnosticSurfaceReadOnlyEvaluation`
- `_evaluate_diagnostic_surface_read_only_boundary(...)`

`_identify_diagnostic_surface_boundary(...)` now asks that producer for the existing read-only fact and then continues to identify the unchanged boundary statement tuple.

## Recovered producer

`_evaluate_diagnostic_surface_read_only_boundary(...)` is the recovered producer. It consumes a `DiagnosticInventoryEntry` and produces only the implementation-local read-only boolean derived from existing diagnostic inventory fields.

## Recovered artifact/helper

`_DiagnosticSurfaceReadOnlyEvaluation` is the recovered private artifact. It carries only the `read_only` value and does not carry DiagnosticSurface identity, definition payloads, explanation payloads, boundary statement tuples, consumption facts, shape-registration status, indentation, line labels, JSON authority, diagnostic authority, CLI authority, event-ledger authority, or cluster mutation authority.

## Recovered consumer

The immediate consumer is `_identify_diagnostic_surface_boundary(...)`.

Downstream existing consumers remain unchanged:

- `_produce_known_diagnostic_surface_definition(...)`
- `_KnownDiagnosticSurfaceDefinition.to_json_dict(...)`
- `diagnostic_surface_definition_json(...)`
- `diagnostic_surface_explanation_json(...)`
- `format_diagnostic_surface_definition(...)`
- `format_diagnostic_surface_explanation(...)`
- `seed --diagnostic-surface-definition <surface>`
- `seed --diagnostic-surface-explanation <surface>`

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

DiagnosticSurface read-only boundary evaluation and DiagnosticSurface boundary statement identification were previously compressed inside `_identify_diagnostic_surface_boundary(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Read-Only Boundary Evaluation
        !=
DiagnosticSurface Boundary Statement Identification
```

### 3. What producer now owns the recovered responsibility?

`_evaluate_diagnostic_surface_read_only_boundary(...)` now owns the recovered read-only boundary evaluation responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceReadOnlyEvaluation` carries the read-only boolean. It is a private implementation-local artifact.

### 5. Who consumes it?

`_identify_diagnostic_surface_boundary(...)` consumes the evaluation before producing the unchanged boundary statement identification. Existing definition and explanation outputs consume that boundary identification through their existing calls.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_015.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 31 +++++++++++++++++++++++--------
tests/test_diagnostic_inventory.py   | 20 ++++++++++++++++++++
2 files changed, 43 insertions(+), 8 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
57 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- human-readable DiagnosticSurface definition line assembly;
- human-readable DiagnosticSurface explanation line assembly;
- DiagnosticSurface boundary statement vocabulary identification beyond the read-only predicate;
- DiagnosticSurface consumption identification from inventory entry fields;
- DiagnosticSurface shape registration status presentation;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local read-only evaluation path.

The current Diagnostic Surface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
