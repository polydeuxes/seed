# Frontier Pressure Admission Slice 052

## Selected boundary

Recovered exactly one implementation-local ownership boundary: **ownership-discrepancy pressure score production from already selected conflicted ownership rows**.

## Implementation evidence

Investigation began adjacent to the Slice 051 stop result in `seed_runtime/pressure_audit.py` without continuing to mine the stopped diagnostic-shape pressure pocket. The next natural pressure producer consumed by `build_pressure_audit(...)` is `_ownership_pressure(state)`, which already had one recovered helper for ownership evidence payload aggregation but still computed the ownership pressure score inline from the selected conflicted rows:

```python
rows = [row for row in build_ownership_discrepancies(state) if row.conflict]
score = len(rows)
if score <= 0:
    return None
```

That inline score is a material producer boundary because the computed score is consumed by both the existing zero-score refusal and the unchanged `Ownership Attribution` `_PressureItemCandidate`. The selected boundary is smaller than candidate construction, does not alter row selection, and does not re-slice the already recovered ownership evidence payload helper.

## Before

`_ownership_pressure(state)` owned all of these local responsibilities together:

- selecting conflicted ownership-discrepancy rows from `build_ownership_discrepancies(state)`;
- computing the ownership pressure score with `len(rows)`;
- refusing candidate construction for non-positive score;
- consuming `_ownership_pressure_evidence(rows)`;
- constructing the unchanged `Ownership Attribution` `_PressureItemCandidate`.

## After

`_ownership_pressure(state)` still owns row selection, non-positive-score refusal, evidence helper consumption, reason text, recommended command, and candidate construction. `_ownership_pressure_score(rows)` now owns only the score production from the already selected conflicted ownership rows.

## Recovered producer

`_ownership_pressure_score(rows)` produces the ownership-discrepancy pressure score.

## Recovered artifact/helper

Recovered helper: `_ownership_pressure_score(rows)`.

Recovered artifact: the unchanged integer ownership pressure score, equal to the count of selected conflicted ownership-discrepancy rows.

## Recovered consumer

`_ownership_pressure(state)` consumes `_ownership_pressure_score(rows)` before preserving the existing non-positive-score refusal and unchanged `Ownership Attribution` pressure candidate construction.

## Compatibility preserved

No.

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and read-only mutation boundaries are preserved. The new helper returns the same integer that `_ownership_pressure(state)` previously computed inline.

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_052.md`

## LOC changed

```text
seed_runtime/pressure_audit.py       | 6 +++++-
tests/test_pressure_audit.py         | 8 ++++++++
frontier_pressure_admission_slice_052.md | 140 insertions
```

## Tests executed

```text
python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py
pytest -q tests/test_pressure_audit.py
pytest -q tests/test_pressure_audit.py tests/test_selection_path_audit.py
```

Result: all passed; the focused pressure test run reported `21 passed`, and the pressure plus selection-path stop-marker check reported `64 passed`.

## Remaining compressed responsibilities

The ownership pressure producer still owns conflicted-row selection, non-positive-score refusal, reason text, recommended command, and candidate construction. Capability pressure still owns entry selection, score production, non-positive-score refusal, top-need reason selection, reason text, recommended command, and candidate construction. Consumer-predicate pressure producers still own their predicate selection, non-empty refusal, candidate fields, and candidate construction. Any future recovery should be selected only from fresh implementation evidence and must not re-slice previously recovered evidence payload, display-formatting, candidate admission, diagnostic-shape, or stop-report boundaries.

## Slice 035 stop-marker compliance

This slice does not inspect, modify, or depend on `selection_path_audit`. It does not reopen the exhausted Slice 035 neighborhood and does not require any compatibility-preserving call-site update there.

## Slice 051 stop-marker compliance

This slice respects the Slice 051 stop marker by not continuing to extract anything from the immediate diagnostic-shape pressure candidate-construction pocket. The investigation moved only through adjacent implementation evidence: from `build_pressure_audit(...)` past the stopped diagnostic-shape producer to the next existing pressure producer, `_ownership_pressure(state)`.

## Distinction from recent upstream slices

- Slice 036 recovered pressure candidate admission/filtering/conversion/ordering in `_admitted_pressure_items(...)`; this slice does not touch admission.
- Slice 037 recovered consumer-predicate source collection and fan-out; this slice does not touch `_consumer_predicate_pressures(root)`.
- Slice 038 recovered diagnostic-shape pressure evidence payload projection; this slice does not touch `_diagnostic_shape_pressure_evidence(summary)`.
- Slice 039 recovered ownership-discrepancy pressure evidence aggregation; this slice leaves `_ownership_pressure_evidence(rows)` unchanged and recovers only the adjacent ownership score producer.
- Slice 040 recovered capability pressure evidence payload assembly; this slice does not touch capability evidence.
- Slice 041 recovered orphaned-predicate pressure evidence payload assembly; this slice does not touch orphaned-predicate evidence.
- Slice 042 recovered fragile-predicate pressure evidence payload assembly; this slice does not touch fragile-predicate evidence.
- Slices 043 through 045 recovered mapping, collection, and scalar evidence display formatting; this slice does not touch evidence display.
- Slice 046 recovered pressure item-section human-readable formatting; this slice does not touch report formatting.
- Slices 047 through 050 recovered diagnostic-shape audit-root selection, summary production, score production, and positive-finding refusal; this slice does not touch those helpers.
- Slice 051 stopped the immediate diagnostic-shape pressure candidate-construction pocket; this slice honors that stop and recovers a separate ownership-pressure scoring boundary.

## Required questions

### 1. What responsibility was previously compressed?

Ownership-discrepancy pressure score production was compressed inside `_ownership_pressure(state)` alongside conflicted-row selection, non-positive-score refusal, ownership evidence helper consumption, reason text, recommended command, and candidate construction.

### 2. Which implementation-local ownership boundary became directly observable?

The boundary between selected conflicted ownership rows and the ownership pressure score became directly observable because the score is separately consumed by the refusal guard and by the unchanged candidate construction.

### 3. What producer now owns the recovered responsibility?

`_ownership_pressure_score(rows)` owns ownership-discrepancy pressure score production.

### 4. What artifact or helper carries the recovered boundary, if any?

The helper `_ownership_pressure_score(rows)` carries the recovered boundary and returns the unchanged integer score.

### 5. Who consumes it?

`_ownership_pressure(state)` consumes the helper result before preserving the existing refusal guard and candidate construction.

### 6. Did any compatibility boundary change?

No.

### 7. How does this respect the Slice 035 `selection_path_audit` stop marker?

This slice does not inspect, modify, or rely on `selection_path_audit`. It remains in `seed_runtime/pressure_audit.py` and requires no selection-path compatibility call-site update.

### 8. How does this respect the Slice 051 diagnostic-shape pressure stop marker?

This slice does not mine the stopped diagnostic-shape candidate-construction pocket. It moves through the existing `build_pressure_audit(...)` producer list to the adjacent ownership-pressure producer and recovers only an ownership-score boundary supported by that implementation.

### 9. How is this distinct from the recent upstream recoveries, especially Slice 036 through Slice 051?

This slice is distinct because it recovers ownership-pressure score production from conflicted ownership rows. It is not pressure candidate admission, consumer-predicate audit fan-out, any evidence payload producer, evidence display formatting, pressure item-section formatting, diagnostic-shape root/summary/score/finding logic, or the Slice 051 stop result. The only implementation change is the compatibility-preserving extraction of the existing `len(rows)` score calculation into `_ownership_pressure_score(rows)` with direct test coverage.
