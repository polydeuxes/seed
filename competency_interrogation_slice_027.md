# Competency Interrogation Slice 027

## Selected boundary

Recovered exactly one implementation-local ownership boundary:

```text
DiagnosticSurface Inventory Registration Line Rendering
        !=
DiagnosticSurface Definition Line-Set Assembly
```

This slice begins immediately adjacent to the implementation modified by Slice 026 in `seed_runtime/diagnostic_inventory.py`. After evidence-source line rendering was separated from DiagnosticSurface definition line-set assembly, the same assembly function still directly rendered the prefixed `diagnostic_inventory_registration:` human output line.

The evidence is implementation-local. This slice does not implement Competency Interrogation Grammar and does not introduce a framework, engine, registry, methodology owner, generalized renderer, architectural redesign, or public surface.

## Implementation evidence

Implementation evidence was concentrated in `_assemble_diagnostic_surface_definition_line_set(...)` and the existing DiagnosticSurface definition dictionary path:

- `_produce_known_diagnostic_surface_definition(...)` and `_produce_unknown_diagnostic_surface_definition(...)` already produce DiagnosticSurface definition dictionaries containing `diagnostic_inventory_registration`.
- `_assemble_diagnostic_surface_definition_line_set(...)` already consumes the prepared `definition["diagnostic_inventory_registration"]` value but still directly rendered the prefixed human line.
- Neighboring DiagnosticSurface boundary, consumption, shape-registration status, implementation-reason, and evidence-source fields already route through implementation-local line-rendering helpers before line-set assembly.
- The inventory-registration line renderer has no authority over DiagnosticSurface identity, known/unknown definition production, JSON output, diagnostic inventory registration, diagnostic shape-audit registration, CLI flag parsing, event-ledger behavior, cluster mutation behavior, or public compatibility.

The observable pressure was therefore narrow: rendering the existing prefixed `diagnostic_inventory_registration:` line is distinct from assembling the full DiagnosticSurface definition line set.

## Before

`_assemble_diagnostic_surface_definition_line_set(...)` compressed two responsibilities:

1. DiagnosticSurface definition line-set assembly:
   - collect the existing definition fields in the existing order;
   - return `_DiagnosticSurfaceDefinitionLineSet` for existing human rendering.
2. DiagnosticSurface inventory-registration line rendering:
   - apply the existing two-space indentation;
   - add the existing `diagnostic_inventory_registration:` label;
   - embed the prepared inventory-registration value in the human output line.

Behavior was correct, but inventory-registration line rendering was implicit inside the broader definition line-set assembly owner.

## After

A private implementation-local inventory-registration line rendering owner now exists:

- `_DiagnosticSurfaceInventoryRegistrationLine`
- `_render_diagnostic_surface_inventory_registration_line(...)`

`_assemble_diagnostic_surface_definition_line_set(...)` now passes the unchanged `definition["diagnostic_inventory_registration"]` value to the recovered line renderer and includes the unchanged rendered line in the existing line tuple.

## Recovered producer

`_render_diagnostic_surface_inventory_registration_line(...)` is the recovered producer. It consumes the existing inventory-registration value plus the existing indentation argument and produces only the prefixed human line that `_assemble_diagnostic_surface_definition_line_set(...)` already emitted.

## Recovered artifact/helper

`_DiagnosticSurfaceInventoryRegistrationLine` is the recovered private artifact. It carries only:

- `line`

It does not carry DiagnosticSurface identity authority, known/unknown definition production authority, JSON authority, diagnostic inventory registration authority, shape-audit registration authority, CLI flag parsing authority, event-ledger authority, cluster mutation authority, or generalized rendering authority.

## Recovered consumer

The immediate consumer is `_assemble_diagnostic_surface_definition_line_set(...)`.

Downstream existing consumers remain unchanged:

- `format_diagnostic_surface_definition(...)`
- `seed --diagnostic-surface-definition <surface>`

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

DiagnosticSurface definition line-set assembly and DiagnosticSurface inventory-registration line rendering were previously compressed inside `_assemble_diagnostic_surface_definition_line_set(...)`.

### 2. Which implementation-local ownership boundary became directly observable?

```text
DiagnosticSurface Inventory Registration Line Rendering
        !=
DiagnosticSurface Definition Line-Set Assembly
```

### 3. What producer now owns the recovered responsibility?

`_render_diagnostic_surface_inventory_registration_line(...)` now owns the recovered prefixed inventory-registration line rendering responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceInventoryRegistrationLine` carries the rendered inventory-registration line. It is a private implementation-local artifact.

### 5. Who consumes it?

`_assemble_diagnostic_surface_definition_line_set(...)` consumes the rendered line before returning the unchanged `_DiagnosticSurfaceDefinitionLineSet` to existing human rendering.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_027.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 19 ++++++++++++++++++-
tests/test_diagnostic_inventory.py   | 12 ++++++++++++
2 files changed, 30 insertions(+), 1 deletion(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
python -m black seed_runtime/diagnostic_inventory.py tests/test_diagnostic_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
69 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- DiagnosticSurface definition human rendering beyond line-set assembly;
- DiagnosticSurface explanation human rendering beyond line-set assembly;
- DiagnosticSurface explanation line rendering for fields that remain directly interpolated inside explanation line-set assembly;
- DiagnosticSurface definition line rendering for fields that remain directly interpolated inside definition line-set assembly;
- DiagnosticSurface explanation field display preparation beyond CLI flag display;
- DiagnosticSurface boundary formatter coordination beyond line rendering;
- DiagnosticSurface consumption formatter coordination beyond line rendering;
- DiagnosticSurface consumption identification beyond declared field set assembly;
- DiagnosticSurface boundary identification beyond ordered non-read-only statement-set assembly and read-only predicate insertion;
- diagnostic inventory table composition and sorting;
- broader diagnostic identity, capability, responsibility, inquiry-boundary, explanation, or rendering semantics outside this local inventory-registration line path.

The current DiagnosticSurface neighborhood is not declared exhausted by this slice; however, no additional ownership boundary is recovered here. Future work should follow implementation evidence and may move to the next adjacent compressed neighborhood if this one stops exposing narrow local responsibilities.
