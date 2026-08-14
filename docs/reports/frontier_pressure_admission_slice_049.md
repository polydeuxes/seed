# Frontier Pressure Admission Slice 049

## Selected boundary

Recovered exactly one implementation-local ownership boundary: **diagnostic-shape pressure score production from diagnostic-shape audit summary counts**.

## Implementation evidence

Investigation began immediately adjacent to Slice 048 in `seed_runtime/pressure_audit.py`. Slice 048 moved diagnostic-shape audit summary production into `_diagnostic_shape_audit_summary(root)`, leaving `_diagnostic_shape_pressure(root)` to consume that summary and still compute the pressure score inline before the existing zero-score refusal and `_PressureItemCandidate` construction.

The directly observable boundary is the conversion of `DiagnosticShapeAuditSummary` mismatch, warning, and unknown counts into the numeric pressure score. That responsibility is implementation-local because the score is an internal candidate-admission value consumed before the public `PressureItem` is created. It is distinct from evidence payload projection, summary production, root compatibility selection, and candidate construction.

## Before

`_diagnostic_shape_pressure(root)` owned diagnostic-shape pressure score production inline:

```python
summary = _diagnostic_shape_audit_summary(root)
score = summary.mismatches + summary.warnings + summary.unknown
if score <= 0:
    return None
```

The same function also owned zero-score refusal, pressure evidence helper consumption, reason text, recommended command, and `_PressureItemCandidate` construction.

## After

`_diagnostic_shape_pressure(root)` now delegates only the summary-count-to-score calculation to `_diagnostic_shape_pressure_score(summary)`. It continues to own zero-score refusal, reason text, recommended command, evidence helper consumption, and candidate construction.

## Recovered producer

`_diagnostic_shape_pressure_score(summary)` owns diagnostic-shape pressure score production from `DiagnosticShapeAuditSummary` counts.

## Recovered artifact/helper

Recovered helper:

```python
def _diagnostic_shape_pressure_score(summary: DiagnosticShapeAuditSummary) -> int:
    return summary.mismatches + summary.warnings + summary.unknown
```

## Recovered consumer

`_diagnostic_shape_pressure(root)` consumes `_diagnostic_shape_pressure_score(summary)` before applying the unchanged zero-score refusal and pressure-candidate construction.

## Compatibility preserved

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory, schema, event-ledger behavior, or read-only mutation boundary changed. The helper returns the same integer expression that `_diagnostic_shape_pressure(root)` previously computed inline.

Expected compatibility answer:

```text
No.
```

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_049.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/pressure_audit.py |  6 +++++-
tests/test_pressure_audit.py   | 13 +++++++++++++
2 files changed, 18 insertions(+), 1 deletion(-)
```

Numstat before this report:

```text
5	1	seed_runtime/pressure_audit.py
13	0	tests/test_pressure_audit.py
```

## Tests executed

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` — passed; 2 files left unchanged.
- `pytest -q tests/test_pressure_audit.py` — passed; 19 tests.
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py tests/test_pressure_audit.py` — passed; 123 tests.

## Required questions

1. **What responsibility was previously compressed?**

   Diagnostic-shape pressure score production was compressed inside `_diagnostic_shape_pressure(root)` alongside zero-score refusal, evidence helper consumption, reason text, recommended command, and pressure-candidate construction.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between consuming a `DiagnosticShapeAuditSummary` and producing the internal numeric pressure score became directly observable after Slice 048 moved summary production out of `_diagnostic_shape_pressure(root)`.

3. **What producer now owns the recovered responsibility?**

   `_diagnostic_shape_pressure_score(summary)` owns the recovered score-production responsibility.

4. **What artifact or helper carries the recovered boundary, if any?**

   `_diagnostic_shape_pressure_score(summary)` carries the boundary by returning the integer score derived from `mismatches`, `warnings`, and `unknown` summary counts.

5. **Who consumes it?**

   `_diagnostic_shape_pressure(root)` consumes the score before preserving the existing `score <= 0` refusal and candidate construction behavior.

6. **Did any compatibility boundary change?**

   No.

7. **How does this respect the Slice 035 `selection_path_audit` stop marker?**

   This slice does not inspect, modify, or rely on `selection_path_audit`. It remains within the diagnostic-shape pressure path in `seed_runtime/pressure_audit.py`, and no selection-path compatibility call-site update was required.

8. **How is this distinct from the recent upstream recoveries, especially Slice 036 through Slice 048?**

   - Slice 036 recovered pressure candidate admission/filtering/conversion/ordering; this slice does not touch `_admitted_pressure_items(...)`.
   - Slice 037 recovered consumer-predicate pressure source admission; this slice does not collect or fan out consumer audits.
   - Slices 038 through 042 recovered pressure evidence payload ownership for diagnostic-shape, ownership, capability, orphaned-predicate, and fragile-predicate candidates; this slice does not assemble pressure evidence.
   - Slices 043 through 045 recovered mapping, collection, and scalar evidence display formatting; this slice does not format evidence values.
   - Slice 046 recovered one pressure item-section formatter; this slice does not change report rendering.
   - Slice 047 recovered repository-root compatibility selection for the diagnostic-shape audit; this slice consumes the summary after that compatibility boundary has already been handled.
   - Slice 048 recovered diagnostic-shape audit summary production; this slice does not build or summarize audit rows, and instead recovers only the adjacent pressure-score calculation from that summary.

## Remaining compressed responsibilities

Remaining compression, if any, should continue to be selected only from implementation evidence. After this slice, `_diagnostic_shape_pressure(root)` still owns zero-score refusal, reason text, recommended command, evidence helper consumption, and candidate construction. `_diagnostic_shape_audit_root(root)` owns only compatibility root selection, `_diagnostic_shape_audit_summary(root)` owns only audit summary production, `_diagnostic_shape_pressure_score(summary)` owns only score production, and `_diagnostic_shape_pressure_evidence(summary)` owns only evidence payload projection. No feature admission, acceptance, action, mutation, planning, prioritization, readiness evaluation, inquiry generation, route authority, scheduler, ontology, registry, or framework was introduced.

## Slice 035 stop-marker compliance

The exhausted `selection_path_audit` neighborhood remains closed. The selected boundary is in the adjacent diagnostic-shape pressure producer path and does not change any selection-path implementation or tests.

## Distinction from recent upstream pressure-audit slices

This slice recovers the local diagnostic-shape pressure-score producer. It is not a re-slice of candidate admission, consumer-predicate source fan-out, evidence payload ownership, evidence display formatting, pressure item-section formatting, diagnostic-shape root compatibility selection, or diagnostic-shape audit summary production. The implementation evidence is the existing score expression that was already present inline and is now owned by one local helper.
