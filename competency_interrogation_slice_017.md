# Competency Interrogation Slice 017

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Consumption Declaration Set Assembly
        !=
DiagnosticSurface Consumption Identification
```

This slice begins immediately adjacent to Slice 016 in `seed_runtime/diagnostic_inventory.py`. After boundary statement set assembly was separated from boundary identification, the same implementation neighborhood still exposed one narrow compressed responsibility: `_identify_diagnostic_surface_consumption(...)` both copied declared consumption fields from a `DiagnosticInventoryEntry` and identified the presentation-facing consumption fact. The evidence is implementation-local and does not require Competency Interrogation Grammar, a framework, engine, registry, router, planner, scheduler, orchestration layer, methodology owner, constitutional abstraction, diagnostic framework, generalized owner, or architectural redesign.

## Implementation evidence

Implementation evidence was concentrated in `_identify_diagnostic_surface_consumption(...)`:

- The function produced `_DiagnosticSurfaceConsumptionIdentification`, the existing presentation-facing consumption fact consumed by known DiagnosticSurface definition composition.
- The same function also performed a distinct field-derived declaration set assembly responsibility by selecting the existing `uses_projected_state`, `uses_repo_files`, and `reads_diagnostic_facts` values from `DiagnosticInventoryEntry`.
- That declaration set assembly is different from consumption identification because identification still owns the presentation-facing `_DiagnosticSurfaceConsumptionIdentification` artifact and its JSON shape.
- The declaration set assembly has no authority over JSON output, human rendering, diagnostic inventory registration, shape-audit registration, boundary statements, read-only evaluation, event-ledger behavior, cluster mutation behavior, CLI flags, or unknown-surface behavior.

The observable pressure was therefore narrow: assembling the existing declared DiagnosticSurface consumption fields is distinct from identifying the final consumption fact.

## Before

`_identify_diagnostic_surface_consumption(...)` compressed two responsibilities:

1. DiagnosticSurface consumption declaration set assembly:
   - inspect the existing diagnostic inventory entry;
   - select the existing declared consumption fields;
   - preserve the implementation-backed field values used by known DiagnosticSurface definitions.
2. DiagnosticSurface consumption identification:
   - consume those declared values;
   - produce `_DiagnosticSurfaceConsumptionIdentification`;
   - preserve the existing JSON shape and presentation-facing consumption semantics.

Behavior was correct, but field-derived declaration set assembly was implicit inside final consumption identification.

## After

A private implementation-local declaration set assembly owner now exists:

- `_DiagnosticSurfaceConsumptionDeclarationSet`
- `_assemble_diagnostic_surface_consumption_declaration_set(...)`

`_identify_diagnostic_surface_consumption(...)` now asks that producer for the existing declared consumption values and then continues to produce the unchanged final consumption identification.

## Recovered producer

`_assemble_diagnostic_surface_consumption_declaration_set(...)` is the recovered producer. It consumes a `DiagnosticInventoryEntry` and produces only the existing declared consumption values used by DiagnosticSurface consumption identification.

## Recovered artifact/helper

`_DiagnosticSurfaceConsumptionDeclarationSet` is the recovered private artifact. It carries only:

- `uses_projected_state`
- `uses_repo_files`
- `reads_diagnostic_facts`

It does not carry DiagnosticSurface identity, definition payloads, explanation payloads, JSON authority, shape-registration status, boundary statements, read-only evaluation, indentation, line labels, CLI authority, diagnostic authority, event-ledger authority, or cluster mutation authority.

## Recovered consumer

The immediate consumer is `_identify_diagnostic_surface_consumption(...)`.

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

DiagnosticSurface consumption declaration set assembly and DiagnosticSurface consumption identification were previously compressed inside `_identify_diagnostic_surface_consumption(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Consumption Declaration Set Assembly
        !=
DiagnosticSurface Consumption Identification
```

### 3. What producer now owns the recovered responsibility?

`_assemble_diagnostic_surface_consumption_declaration_set(...)` now owns the recovered declared consumption field assembly responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceConsumptionDeclarationSet` carries the declared consumption values. It is a private implementation-local artifact.

### 5. Who consumes it?

`_identify_diagnostic_surface_consumption(...)` consumes the declaration set before producing the unchanged final consumption identification. Existing definition and explanation outputs consume that consumption identification through their existing calls.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_017.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 20 ++++++++++++++++++++
tests/test_diagnostic_inventory.py   | 18 ++++++++++++++++++
2 files changed, 38 insertions(+)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
59 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- human-readable DiagnosticSurface definition line assembly;
- human-readable DiagnosticSurface explanation line assembly;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- DiagnosticSurface shape registration status presentation;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local consumption declaration path.

The current Diagnostic Surface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
