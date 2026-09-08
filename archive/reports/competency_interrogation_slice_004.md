# Competency Interrogation Slice 004

## Selected implementation boundary

Recovered exactly one implementation-local Boundary Discipline ownership boundary:

```text
Diagnostic Surface Boundary Identification
        !=
Diagnostic Surface Boundary Presentation
```

This slice does not implement the Competency Interrogation Grammar, a boundary framework, a runtime engine, a registry, campaign logic, planner, scheduler, execution routing, or universal methodology owner.

## Implementation evidence

Representative implementation evidence supported the smallest recurring local boundary in `seed_runtime/diagnostic_inventory.py`:

- `build_diagnostic_surface_definition(...)` identifies a diagnostic surface from the static diagnostic inventory and composes the existing JSON-compatible definition report.
- The boundary fields for a known diagnostic surface were previously derived and returned as the final presentation dictionary in the same helper.
- Human rendering already consumed the composed report through `_format_diagnostic_surface_boundary(...)`, so the implementation pressure was not to change output shape. The pressure was to make the boundary facts observable before they become presentation JSON.
- Existing tests assert the JSON boundary shape and human boundary text for diagnostic surface definition/explanation output.

## Before

`_diagnostic_surface_boundary(entry)` both:

1. identified the implementation-backed boundary statements from `DiagnosticInventoryEntry`; and
2. returned the JSON/report dictionary consumed by `build_diagnostic_surface_definition(...)`.

That compressed boundary identification and report presentation into one private helper.

## After

Boundary identification is now a private implementation-local artifact before presentation:

- `_identify_diagnostic_surface_boundary(entry)` derives boundary statements from declared diagnostic inventory fields.
- `_DiagnosticSurfaceBoundaryIdentification` carries those boundary facts before report presentation.
- `_diagnostic_surface_boundary(identification)` converts the identified facts into the existing JSON-compatible boundary dictionary.

The public JSON output, CLI behavior, diagnostic inventory, diagnostic shape audit behavior, schema, event ledger behavior, runtime behavior, and human rendering are preserved.

## Recovered producer

Recovered producer:

```text
_identify_diagnostic_surface_boundary(entry)
```

It owns only implementation-local identification of the diagnostic surface boundary facts already declared by `DiagnosticInventoryEntry`.

## Recovered artifact/helper

Recovered artifact/helper:

```text
_DiagnosticSurfaceBoundaryIdentification
```

It carries the tuple of boundary statements before those facts are converted into the existing report dictionary.

## Recovered consumer

Recovered consumer:

```text
_diagnostic_surface_boundary(identification)
```

`build_diagnostic_surface_definition(...)` consumes the presented dictionary produced by that helper while preserving the existing report shape.

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

## Files changed

- `seed_runtime/diagnostic_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `competency_interrogation_slice_004.md`

## LOC changed

Current diff stat after implementation and slice report:

```text
3 files changed, 209 insertions(+), 8 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
47 passed
```

## Required questions

### 1. Where were boundary identification and boundary presentation previously mixed?

They were mixed in `_diagnostic_surface_boundary(entry)`, which derived boundary statements from a `DiagnosticInventoryEntry` and immediately returned the final JSON/report dictionary used in diagnostic surface definition output.

### 2. Which implementation-local boundary became directly observable?

The implementation-local boundary between Diagnostic Surface Boundary Identification and Diagnostic Surface Boundary Presentation became directly observable.

### 3. What private artifact or helper now carries the recovered boundary information?

`_DiagnosticSurfaceBoundaryIdentification` carries the recovered boundary information, and `_identify_diagnostic_surface_boundary(entry)` produces it.

### 4. Who consumes it?

`_diagnostic_surface_boundary(identification)` consumes `_DiagnosticSurfaceBoundaryIdentification` and presents it as the existing JSON-compatible diagnostic surface boundary dictionary. `build_diagnostic_surface_definition(...)` consumes that dictionary in the existing diagnostic surface definition report.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed competency-interrogation responsibilities

This slice intentionally stops after one Boundary Discipline recovery. Remaining compressed responsibilities include:

- broader capability-boundary identification and presentation outside the diagnostic surface definition path;
- neighboring responsibility and inquiry-boundary reporting outside this diagnostic inventory-local helper;
- report-boundary presentation in other diagnostic or audit surfaces;
- compatibility-boundary explanation in unrelated modules;
- responsibility evaluation and ownership-boundary analysis beyond this diagnostic surface boundary path.

Those responsibilities remain compressed unless future implementation evidence independently requires a separate local recovery.
