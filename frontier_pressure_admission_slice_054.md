# Frontier Pressure Admission Slice 054

## Selected boundary

Capability pressure positive-finding refusal inside `_capability_pressure(state)`.

## Implementation evidence

After Slice 053, `_capability_pressure(state)` consumes the capability score in an inline admission/refusal check before constructing the capability pressure candidate. The implementation evidence is the existing `score <= 0` non-positive refusal: it decides whether capability pressure has findings, while score production is now separately owned by `_capability_pressure_score(entries)`.

## Before

`_capability_pressure(state)` owned the positive-finding predicate inline with candidate construction, top-need selection, evidence consumption, reason text, and recommended command selection.

## After

`_capability_pressure(state)` delegates positive-finding refusal to `_capability_pressure_has_findings(score)` and preserves the same `return None` path for non-positive scores.

## Recovered producer

`_capability_pressure_has_findings(score)` now owns the capability pressure positive-finding predicate.

## Recovered artifact/helper

`_capability_pressure_has_findings(score)` carries the recovered implementation-local boundary.

## Recovered consumer

`_capability_pressure(state)` consumes the boolean to preserve the unchanged candidate refusal path.

## Compatibility preserved

No.

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, or read-only mutation boundary changed. The helper preserves the previous `score > 0` finding semantics and the previous refusal for zero or negative scores.

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_054.md`

## LOC changed

Implementation and tests before this report: `6` insertions and `1` deletion in `seed_runtime/pressure_audit.py`; `8` insertions in `tests/test_pressure_audit.py`.

## Tests executed

- `pytest -q tests/test_pressure_audit.py` — passed (`23 passed`).

## Remaining compressed responsibilities

Adjacent implementation evidence in `_capability_pressure(state)` now shows top-need selection, reason construction, recommended command selection, and candidate construction still inline. Reassessing the next district-scout queue item points to orphaned-predicate pressure score production or refusal as a stronger implementation-local boundary than carving capability reason/candidate text, because the latter would risk cosmetic construction movement without an independently consumed producer.

## Slice 035 stop-marker compliance

This slice does not touch `selection_path_audit` or its call sites.

## Slice 051 stop-marker compliance

This slice does not touch the diagnostic-shape pressure candidate-construction pocket or its call sites.

## Distinction from relevant recent upstream slices

- Slice 040 recovered capability pressure evidence payload ownership. This slice does not change `_capability_pressure_evidence(entries)` or evidence payload shape.
- Slice 052 recovered ownership-discrepancy pressure score production. This slice does not touch ownership score production; it separates only the capability positive-finding predicate that consumes the already-produced capability score.

## Distinction from earlier slices in this batch

Slice 053 recovered capability score production. This slice is distinct because it does not produce the score; it owns only the boolean finding/refusal predicate that consumes the score.
