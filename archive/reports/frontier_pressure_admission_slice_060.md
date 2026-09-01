# Frontier Pressure Admission Slice 060

Selected boundary: **ownership-pressure conflicted-row selection inside `_ownership_pressure(state)`**.

## Implementation evidence

After Slice 059 landed cleanly, investigation returned to the modified `_ownership_pressure(state)` implementation. The function now delegated positive-finding refusal to `_ownership_pressure_has_findings(score)`, and prior slices had already separated score production and evidence aggregation. The next adjacent still-compressed responsibility was the source-row selection expression:

```python
[row for row in build_ownership_discrepancies(state) if row.conflict]
```

That expression is not merely naming: it owns the handoff from the ownership-discrepancy diagnostic surface into the ownership-pressure row set by selecting only conflicted rows. The selected rows are then consumed by three already distinct downstream responsibilities: score production, positive-finding refusal through the score, and evidence aggregation. This producer/consumer shape directly supports a separate implementation-local boundary while preserving every public artifact.

## Before

`_ownership_pressure(state)` directly called `build_ownership_discrepancies(state)`, filtered rows with truthy `row.conflict`, computed the score, applied positive-finding refusal, and built the unchanged candidate.

## After

`_ownership_pressure_conflicted_rows(state)` owns the ownership-discrepancy source read and conflicted-row filtering. `_ownership_pressure(state)` consumes the selected rows and still owns the outer candidate construction flow.

## Recovered producer

`_ownership_pressure_conflicted_rows(state)` now produces the selected ownership-pressure row set.

## Recovered artifact/helper

Recovered helper: `_ownership_pressure_conflicted_rows(state)`.

Recovered artifact: the list of ownership-discrepancy rows admitted into ownership pressure because they have a conflict.

## Recovered consumer

`_ownership_pressure(state)` consumes the selected conflicted rows before passing them to `_ownership_pressure_score(rows)` and `_ownership_pressure_evidence(rows)`.

## Compatibility preserved

No.

The change preserves public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and read-only mutation boundaries. It only moves the existing ownership-discrepancy row filter into an implementation-local helper with the same predicate.

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_060.md`

## LOC changed

Implementation/test diff before this report: 30 insertions and 1 deletion across `seed_runtime/pressure_audit.py` and `tests/test_pressure_audit.py`.

## Tests executed

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` — passed; reformatted `tests/test_pressure_audit.py`.
- `pytest -q tests/test_pressure_audit.py` — passed; 29 tests.

## Remaining compressed responsibilities

After this slice, `_ownership_pressure(state)` still owns the outer candidate construction shell: category, reason text, recommended command, and candidate object assembly. Those remaining literals and candidate metadata are not separated here because the prompt warns that candidate-field extraction alone is likely cosmetic unless direct producer/consumer evidence proves otherwise. No further boundary is claimed in this batch.

## Required questions

1. **What responsibility was previously compressed?**
   Ownership-pressure candidate construction also owned ownership-discrepancy source reading and conflicted-row selection.

2. **Which implementation-local ownership boundary became directly observable?**
   The boundary between ownership-discrepancy diagnostic rows and the conflicted row set admitted into ownership pressure became directly observable.

3. **What producer now owns the recovered responsibility?**
   `_ownership_pressure_conflicted_rows(state)` owns source-row selection for ownership pressure.

4. **What artifact or helper carries the recovered boundary, if any?**
   `_ownership_pressure_conflicted_rows(state)` carries the boundary and returns the selected conflicted rows.

5. **Who consumes it?**
   `_ownership_pressure(state)` consumes it as the input to score production, positive-finding refusal, evidence aggregation, and candidate construction.

6. **Did any compatibility boundary change?**
   No.

7. **How does this respect the Slice 035 `selection_path_audit` stop marker?**
   This slice does not inspect, modify, or rely on `selection_path_audit`. It remains inside pressure-audit ownership-pressure source selection and does not reopen any stopped selection-path boundary.

8. **How does this respect the Slice 051 diagnostic-shape pressure stop marker?**
   This slice does not touch diagnostic-shape pressure candidate construction or diagnostic-shape helper boundaries. It selects only ownership-discrepancy rows for ownership pressure.

9. **How is this distinct from Slice 039 ownership pressure evidence aggregation?**
   Slice 039 recovered conversion of already-selected rows into the ownership-pressure evidence payload. This slice recovers which ownership-discrepancy rows enter ownership pressure before score and evidence production.

10. **How is this distinct from Slice 052 ownership-discrepancy pressure score production?**
    Slice 052 recovered scoring of the selected rows. This slice recovers selection of those rows from the ownership-discrepancy source and does not change scoring.

11. **How is this distinct from Slices 053 through 058?**
    Slices 053 through 058 recovered score production and positive-finding refusal for capability, orphaned-predicate, and fragile-predicate pressure. This slice does not touch those categories; it recovers ownership-pressure source-row selection.

12. **How is this distinct from any earlier slice in this batch?**
    Slice 059 recovered the score-to-positive-finding refusal decision after rows had already been selected. This slice recovers the upstream source-row selection that produces those rows.

## Distinction from relevant recent upstream slices

- Slice 035 stopped the `selection_path_audit` neighborhood; this slice stays in `pressure_audit`.
- Slice 039 recovered ownership-pressure evidence aggregation; this slice recovers row selection.
- Slice 051 stopped diagnostic-shape pressure candidate construction; this slice does not touch diagnostic-shape pressure.
- Slice 052 recovered ownership-discrepancy pressure score production; this slice recovers the row set consumed by scoring.
- Slice 059 recovered ownership-pressure positive-finding refusal; this slice is upstream of that refusal.
- Slices 053 through 058 recovered capability and consumer-predicate pressure score/refusal boundaries; this slice is ownership-specific.
