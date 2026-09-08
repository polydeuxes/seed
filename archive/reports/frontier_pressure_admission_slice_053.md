# Frontier Pressure Admission Slice 053

## Selected boundary

Capability pressure score production inside `_capability_pressure(state)`.

## Implementation evidence

`_capability_pressure(state)` builds capability-needs entries, consumes a numeric score for the positive-finding refusal, reuses that same score in the candidate record, and embeds it in the public reason text. Before this slice, the numeric score was produced inline as `sum(len(entry.subjects) for entry in entries)`, while Slice 040 had already separated only the capability evidence payload.

## Before

`_capability_pressure(state)` owned capability entry production, score production, positive-finding refusal, top-need selection, reason construction, evidence consumption, recommended command selection, and candidate construction.

## After

`_capability_pressure(state)` still orchestrates capability pressure construction, but the subject-occurrence score is produced by `_capability_pressure_score(entries)`.

## Recovered producer

`_capability_pressure_score(entries)` now owns capability pressure score production.

## Recovered artifact/helper

`_capability_pressure_score(entries)` carries the recovered implementation-local boundary.

## Recovered consumer

`_capability_pressure(state)` consumes the score for the unchanged refusal condition, candidate score, and reason text.

## Compatibility preserved

No.

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, or read-only mutation boundary changed. The helper returns the same integer previously computed inline.

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_053.md`

## LOC changed

Implementation and tests before this report: `5` insertions and `1` deletion in `seed_runtime/pressure_audit.py`; `19` insertions in `tests/test_pressure_audit.py`.

## Tests executed

- `pytest -q tests/test_pressure_audit.py` — passed (`22 passed`).

## Remaining compressed responsibilities

Adjacent implementation evidence now shows `_capability_pressure(state)` still owns capability positive-finding refusal (`if score <= 0: return None`) inline. That is distinct from score production because it consumes the score rather than producing it. It remains a possible next slice only after reassessment.

## Slice 035 stop-marker compliance

This slice does not touch `selection_path_audit` or its call sites.

## Slice 051 stop-marker compliance

This slice does not touch the diagnostic-shape pressure candidate-construction pocket or its call sites.

## Distinction from relevant recent upstream slices

- Slice 040 recovered capability pressure evidence payload ownership. This slice does not change evidence payload keys or assembly; it separates only numeric score production.
- Slice 052 recovered ownership-discrepancy pressure score production. This slice does not touch ownership discrepancy rows or `_ownership_pressure_score(rows)`; it applies the same narrow ownership recovery pattern to capability subject occurrences.

## Distinction from earlier slices in this batch

This is the first slice in this batch.
