# Frontier Pressure Admission Slice 048

## Selected boundary

Recovered exactly one implementation-local ownership boundary: **diagnostic-shape audit summary production for pressure-audit input**.

## Implementation evidence

Investigation began immediately adjacent to Slice 047 in `seed_runtime/pressure_audit.py`. Slice 047 recovered the repository-root compatibility selection for diagnostic-shape audit execution through `_diagnostic_shape_audit_root(root)`, while `_diagnostic_shape_pressure(root)` still compressed the next implementation-local responsibility:

- it invoked `build_diagnostic_shape_audit(repo_root=_diagnostic_shape_audit_root(root))`;
- it immediately summarized those rows with `summarize_diagnostic_shape_audit(...)`;
- it then scored the summary, refused zero-score output, assembled evidence, and constructed the `Diagnostic Shape` pressure candidate.

The recurring local responsibility directly supported by implementation evidence is the production of a `DiagnosticShapeAuditSummary` from the pressure-audit root. That responsibility is separate from candidate scoring and construction because the candidate producer consumes only the summary fields after the audit rows have already been built and summarized.

## Before

`_diagnostic_shape_pressure(root)` owned diagnostic-shape audit summary production inline:

```python
summary = summarize_diagnostic_shape_audit(
    build_diagnostic_shape_audit(repo_root=_diagnostic_shape_audit_root(root))
)
```

The same function also owned pressure score calculation, zero-score refusal, reason text, recommended command, evidence helper consumption, and `_PressureItemCandidate` construction.

## After

`_diagnostic_shape_pressure(root)` now consumes `_diagnostic_shape_audit_summary(root)` and continues to own pressure-specific scoring, zero-score refusal, reason text, recommended command, evidence helper consumption, and candidate construction.

`_diagnostic_shape_audit_summary(root)` owns only the local audit-build-and-summarize responsibility. It preserves the Slice 047 root compatibility helper as its input boundary and returns the same `DiagnosticShapeAuditSummary` previously computed inline.

## Recovered producer

`_diagnostic_shape_audit_summary(root)` owns diagnostic-shape audit summary production for pressure-audit input.

## Recovered artifact/helper

Recovered helper:

```python
def _diagnostic_shape_audit_summary(root: Path) -> DiagnosticShapeAuditSummary:
    return summarize_diagnostic_shape_audit(
        build_diagnostic_shape_audit(repo_root=_diagnostic_shape_audit_root(root))
    )
```

## Recovered consumer

`_diagnostic_shape_pressure(root)` consumes `_diagnostic_shape_audit_summary(root)` before applying pressure-specific score calculation and candidate construction.

## Compatibility preserved

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory, schema, event-ledger behavior, or read-only mutation boundary changed. The helper returns the same summary object that `_diagnostic_shape_pressure(root)` previously computed inline.

Expected compatibility answer:

```text
No.
```

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_048.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/pressure_audit.py | 10 +++++++---
tests/test_pressure_audit.py   | 33 +++++++++++++++++++++++++++++++++
2 files changed, 40 insertions(+), 3 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` — passed; 2 files left unchanged.
- `pytest -q tests/test_pressure_audit.py` — passed; 18 tests.
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py tests/test_pressure_audit.py` — passed; 122 tests.

## Required questions

1. **What responsibility was previously compressed?**

   Diagnostic-shape audit summary production was compressed inside `_diagnostic_shape_pressure(root)` alongside pressure-specific scoring, zero-score refusal, evidence consumption, reason text, recommended command, and pressure-candidate construction.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between producing the diagnostic-shape audit summary and converting that summary into a pressure candidate became directly observable.

3. **What producer now owns the recovered responsibility?**

   `_diagnostic_shape_audit_summary(root)` owns the recovered audit-build-and-summarize responsibility.

4. **What artifact or helper carries the recovered boundary, if any?**

   `_diagnostic_shape_audit_summary(root)` carries the boundary by returning a `DiagnosticShapeAuditSummary` for the pressure producer.

5. **Who consumes it?**

   `_diagnostic_shape_pressure(root)` consumes the summary returned by `_diagnostic_shape_audit_summary(root)`.

6. **Did any compatibility boundary change?**

   No.

7. **How does this respect the Slice 035 `selection_path_audit` stop marker?**

   This slice does not inspect, modify, or rely on `selection_path_audit`. It remains within the diagnostic-shape pressure path in `seed_runtime/pressure_audit.py`, and no selection-path compatibility call-site update was required.

8. **How is this distinct from the recent upstream recoveries, especially Slice 036 through Slice 047?**

   - Slice 036 recovered pressure candidate admission/filtering/conversion/ordering; this slice does not touch `_admitted_pressure_items(...)`.
   - Slice 037 recovered consumer-predicate pressure source admission; this slice does not collect or fan out consumer audits.
   - Slices 038 through 042 recovered pressure evidence payload ownership for diagnostic-shape, ownership, capability, orphaned-predicate, and fragile-predicate candidates; this slice does not assemble pressure evidence.
   - Slices 043 through 045 recovered mapping, collection, and scalar evidence display formatting; this slice does not format evidence values.
   - Slice 046 recovered one pressure item-section formatter; this slice does not change report rendering.
   - Slice 047 recovered repository-root compatibility selection for the diagnostic-shape audit; this slice consumes that helper and recovers the adjacent audit-build-and-summarize producer, not the root-selection decision itself.

## Remaining compressed responsibilities

Remaining compression, if any, should continue to be selected only from implementation evidence. After this slice, `_diagnostic_shape_pressure(root)` still owns diagnostic-shape pressure score calculation, zero-score refusal, reason text, recommended command, evidence helper consumption, and candidate construction. `_diagnostic_shape_audit_root(root)` owns only compatibility root selection, `_diagnostic_shape_audit_summary(root)` owns only audit summary production, and `_diagnostic_shape_pressure_evidence(summary)` owns evidence payload projection. No feature admission, acceptance, action, mutation, planning, prioritization, readiness evaluation, inquiry generation, route authority, scheduler, ontology, registry, or framework was introduced.

## Slice 035 stop-marker compliance

The exhausted `selection_path_audit` neighborhood remains closed. The selected boundary is in the adjacent diagnostic-shape pressure producer path and does not change any selection-path implementation or tests.

## Distinction from recent upstream pressure-audit slices

This slice recovers a local audit-summary producer for the diagnostic-shape pressure source. It is not a re-slice of candidate admission, consumer-predicate source fan-out, evidence payload ownership, evidence display formatting, pressure item-section formatting, or diagnostic-shape root compatibility selection. The implementation evidence is the existing audit-build-and-summarize chain that was already present inline and is now owned by one local helper.
