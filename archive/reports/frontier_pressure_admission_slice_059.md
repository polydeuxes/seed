# Frontier Pressure Admission Slice 059

Selected boundary: **ownership-pressure positive-finding refusal inside `_ownership_pressure(state)`**.

## Implementation evidence

Investigation began at `_ownership_pressure(state)` in `seed_runtime/pressure_audit.py`. The implementation already had separate local producers for ownership-pressure score production (`_ownership_pressure_score(rows)`) and ownership-pressure evidence aggregation (`_ownership_pressure_evidence(rows)`). The adjacent still-compressed responsibility was the positive-finding refusal: `_ownership_pressure(state)` computed the score and also owned the inline `score <= 0` decision that refuses candidate construction.

That refusal is an implementation-local producer/consumer boundary because the score producer emits a scalar finding count, and candidate construction only proceeds when the pressure category has a positive finding. Neighboring pressure categories already expose that decision through category-local `*_has_findings(...)` helpers, so preserving the same compatibility while making ownership pressure's refusal observable is directly supported by implementation evidence.

## Before

`_ownership_pressure(state)` selected conflicted ownership rows, computed `_ownership_pressure_score(rows)`, inlined `if score <= 0: return None`, and then built the unchanged `Ownership Attribution` candidate.

## After

`_ownership_pressure_has_findings(score)` owns the positive-finding predicate for ownership pressure. `_ownership_pressure(state)` consumes that helper and still returns `None` for zero or negative scores before building the unchanged candidate.

## Recovered producer

`_ownership_pressure_has_findings(score)` now produces the ownership-pressure positive-finding decision.

## Recovered artifact/helper

Recovered helper: `_ownership_pressure_has_findings(score)`.

Recovered artifact: a boolean positive-finding/refusal decision for ownership-pressure candidate construction.

## Recovered consumer

`_ownership_pressure(state)` consumes the helper output when deciding whether to refuse candidate construction.

## Compatibility preserved

No.

The change preserves public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and read-only mutation boundaries. It only replaces an inline `score <= 0` candidate-refusal check with an equivalent local helper.

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_059.md`

## LOC changed

Implementation/test diff before this report: 12 insertions and 1 deletion across `seed_runtime/pressure_audit.py` and `tests/test_pressure_audit.py`.

## Tests executed

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` — passed; 2 files left unchanged.
- `pytest -q tests/test_pressure_audit.py` — passed; 28 tests.

## Remaining compressed responsibilities

After this slice, `_ownership_pressure(state)` still owns the outer ownership-pressure candidate construction flow. The adjacent conflicted-row selection remains inline as `[row for row in build_ownership_discrepancies(state) if row.conflict]`; it must be reassessed separately before any next slice because it may be a real source-selection boundary or may be too small/cosmetic depending on direct implementation evidence.

## Required questions

1. **What responsibility was previously compressed?**
   Ownership-pressure candidate construction had compressed the positive-finding refusal decision inline with row selection, score computation, evidence consumption, reason text, command literal, and candidate construction.

2. **Which implementation-local ownership boundary became directly observable?**
   The boundary between ownership-pressure score production and ownership-pressure candidate admission/refusal became directly observable.

3. **What producer now owns the recovered responsibility?**
   `_ownership_pressure_has_findings(score)` owns the positive-finding decision.

4. **What artifact or helper carries the recovered boundary, if any?**
   `_ownership_pressure_has_findings(score)` carries the recovered boundary by returning the boolean finding decision.

5. **Who consumes it?**
   `_ownership_pressure(state)` consumes it before constructing the existing `Ownership Attribution` candidate.

6. **Did any compatibility boundary change?**
   No.

7. **How does this respect the Slice 035 `selection_path_audit` stop marker?**
   This slice does not inspect, modify, or depend on `selection_path_audit`. The recovered boundary remains inside `pressure_audit` ownership-pressure candidate construction and does not reopen the stopped selection-path neighborhood.

8. **How does this respect the Slice 051 diagnostic-shape pressure stop marker?**
   This slice does not touch diagnostic-shape pressure candidate construction, diagnostic-shape score production, diagnostic-shape evidence, or diagnostic-shape audit root handling. It stays in ownership-pressure code.

9. **How is this distinct from Slice 039 ownership pressure evidence aggregation?**
   Slice 039 recovered row-to-evidence payload aggregation through `_ownership_pressure_evidence(rows)`. This slice recovers only the score-to-positive-finding refusal decision and does not change evidence aggregation.

10. **How is this distinct from Slice 052 ownership-discrepancy pressure score production?**
    Slice 052 recovered score production through `_ownership_pressure_score(rows)`. This slice consumes that score through `_ownership_pressure_has_findings(score)` and does not change how the score is computed.

11. **How is this distinct from Slices 053 through 058?**
    Slices 053 through 058 recovered score production and positive-finding refusal for capability, orphaned-predicate, and fragile-predicate pressure. This slice applies the adjacent implementation evidence to ownership pressure only and does not touch those categories.

12. **How is this distinct from any earlier slice in this batch?**
    This is the first slice in this batch, so there is no earlier batch slice to distinguish from.

## Distinction from relevant recent upstream slices

- Slice 035 stopped the `selection_path_audit` neighborhood; this slice stays in `pressure_audit`.
- Slice 039 recovered ownership-pressure evidence aggregation; this slice recovers positive-finding refusal.
- Slice 051 stopped diagnostic-shape pressure candidate construction; this slice does not touch diagnostic-shape pressure.
- Slice 052 recovered ownership-discrepancy pressure score production; this slice only consumes the score.
- Slices 053 through 058 recovered analogous score/refusal boundaries for other pressure categories; this slice is ownership-specific.
