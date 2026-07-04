# Competency Interrogation Slice 005

## Selected boundary

Recovered exactly one implementation-local DiagnosticSurface ownership boundary:

```text
Diagnostic Surface Consumption Identification
        !=
Diagnostic Surface Consumption Presentation
```

This slice recovers only the smallest recurring implementation-local compression supported by neighboring implementation evidence in the diagnostic surface definition path. It does not introduce a framework, engine, registry, methodology owner, planner, scheduler, orchestration layer, compatibility redesign, or new diagnostic surface.

## Implementation evidence

Representative implementation evidence was concentrated in `seed_runtime/diagnostic_inventory.py`:

- `build_diagnostic_surface_definition(...)` already composes a JSON-compatible DiagnosticSurface definition from `DiagnosticInventoryEntry` evidence.
- Slice 004 recovered the adjacent boundary facts before presentation by introducing `_identify_diagnostic_surface_boundary(...)` and `_DiagnosticSurfaceBoundaryIdentification`.
- The neighboring `_diagnostic_surface_consumption(...)` helper still directly read consumption fields from `DiagnosticInventoryEntry` and returned the final JSON/report dictionary.
- The existing JSON surface already exposed consumption facts separately from boundary facts through `diagnostic_surface_consumption`, and human rendering consumed that already-composed report shape.

The smallest recurring implementation compression was therefore local consumption identification before report presentation. The evidence did not require a broader diagnostic-surface framework or any new public behavior.

## Before

`_diagnostic_surface_consumption(entry)` directly mixed two responsibilities:

1. identifying DiagnosticSurface consumption facts from the diagnostic inventory entry:
   - `uses_projected_state`;
   - `uses_repo_files`;
   - `reads_diagnostic_facts`;
2. presenting those facts as the existing JSON-compatible `diagnostic_surface_consumption` dictionary.

The behavior was correct, but consumption identification existed only inside the presentation helper.

## After

A private implementation-local consumption owner now exists:

- `_DiagnosticSurfaceConsumptionIdentification`
- `_identify_diagnostic_surface_consumption(...)`

`_diagnostic_surface_consumption(...)` now consumes that private identification artifact and remains the presentation helper for the unchanged public dictionary shape.

## Recovered producer

`_identify_diagnostic_surface_consumption(...)` is the recovered producer. It consumes a `DiagnosticInventoryEntry` and produces only the implementation-local consumption facts declared by the diagnostic inventory entry.

## Recovered artifact/helper

`_DiagnosticSurfaceConsumptionIdentification` is the recovered private artifact/helper. It carries only:

- `uses_projected_state`
- `uses_repo_files`
- `reads_diagnostic_facts`

It intentionally does not carry public report identity fields, CLI flags, boundary statements, record behavior, shape-registration status, JSON wrapper names, or human-readable rendering.

## Recovered consumer

`_diagnostic_surface_consumption(...)` consumes `_DiagnosticSurfaceConsumptionIdentification` and presents it as the unchanged JSON-compatible consumption dictionary.

`build_diagnostic_surface_definition(...)` continues to consume that presented dictionary as part of the existing DiagnosticSurface definition report.

## Compatibility preserved

No compatibility boundary changed.

Preserved surfaces include:

- `seed --diagnostic-surface-definition ... --json`
- `seed --diagnostic-surface-definition ...`
- `seed --diagnostic-surface-explanation ... --json`
- `seed --diagnostic-surface-explanation ...`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`

Expected answer to "Did any compatibility boundary change?":

```text
No.
```

## Required questions

### 1. What responsibilities were previously compressed?

Diagnostic surface consumption fact identification and diagnostic surface consumption report presentation were previously compressed inside `_diagnostic_surface_consumption(entry)`.

### 2. Which implementation-local boundary became directly observable?

```text
Diagnostic Surface Consumption Identification
        !=
Diagnostic Surface Consumption Presentation
```

### 3. What producer now owns the recovered responsibility?

`_identify_diagnostic_surface_consumption(...)` now owns the recovered consumption-identification responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`_DiagnosticSurfaceConsumptionIdentification` carries the recovered consumption facts before presentation.

### 5. Who consumes it?

`_diagnostic_surface_consumption(...)` consumes `_DiagnosticSurfaceConsumptionIdentification` and returns the unchanged report dictionary. `build_diagnostic_surface_definition(...)` consumes that report dictionary.

### 6. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_005.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/diagnostic_inventory.py | 53 ++++++++++++++++++++++++++++--------
tests/test_diagnostic_inventory.py   | 24 ++++++++++++++++
2 files changed, 65 insertions(+), 12 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
48 passed
```

## Remaining compressed responsibilities

This slice intentionally stops after one implementation-local recovery. Remaining compressed responsibilities include:

- unknown DiagnosticSurface definition fallback composition;
- DiagnosticSurface definition report assembly;
- DiagnosticSurface explanation report assembly;
- human-readable rendering of boundary and consumption reports;
- diagnostic inventory composition and sorting;
- shape-registration status lookup;
- broader diagnostic identity, capability, responsibility, or inquiry-boundary analysis outside this local DiagnosticSurface consumption path.

Those responsibilities remain compressed unless future implementation evidence independently supports another local recovery.
