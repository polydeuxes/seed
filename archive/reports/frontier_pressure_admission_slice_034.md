# Frontier Pressure Admission Slice 034

## Selected boundary

Recovered implementation-local ownership boundary: **selected pressure supporting-evidence record construction inside `selection_path_audit`**.

This slice does not recover row construction, public-name projection, rank assignment, candidate enumeration, lineage assembly, payload bundling, or selection admission. It only names the already-present construction of the selected pressure evidence record consumed by the existing supporting-evidence payload.

## Implementation evidence

Investigation began at `seed_runtime/selection_path_audit.py` around `_candidate_set_from_pressures(...)`, `_pressure_candidate_row(...)`, `_pressure_selection_supporting_evidence_payload(...)`, and the immediately adjacent pressure-selection tests.

Current implementation evidence showed that candidate row construction, candidate ranking, public candidate naming, non-selected enumeration, non-selected reasoning, pressure-selection lineage, selected item lookup, selected-name preparation, and the supporting-evidence payload were already separated and tested. The remaining compressed responsibility in the adjacent supported pressure-selection path was narrower than the supporting-evidence payload: the concrete public evidence record for the selected pressure item.

Before this slice, `_pressure_selection_supporting_evidence_payload(...)` owned both:

1. whether selected pressure evidence is present; and
2. the handoff to a generic `_evidence(...)` helper whose signature still accepted `None` and could return an empty record.

That made selected-pressure evidence record construction observable only indirectly through the broader supporting-evidence payload test, even though the implementation already treated absence at the payload-list boundary.

## Before

`_pressure_selection_supporting_evidence_payload(...)` called `_evidence(selected_item)` inside an inline presence guard. `_evidence(...)` accepted `PressureItem | None`, returned `{}` for `None`, and otherwise built the public evidence record containing `surface`, `category`, `score`, `reason`, and `evidence`.

The broad supporting-evidence payload test proved final payload compatibility but did not directly prove the narrower producer that owns selected pressure evidence record shape.

## After

`_pressure_selection_supporting_evidence_payload(...)` still owns evidence presence and absence. It now delegates selected pressure evidence record construction to `_selected_pressure_evidence(selected_item)`, which accepts only a concrete `PressureItem` and returns the same public evidence record.

`tests/test_selection_path_audit.py` now directly exercises `_selected_pressure_evidence(...)`, proving the selected evidence record shape independently from the broader payload and without changing JSON, CLI, human-readable output, schema, diagnostic behavior, event-ledger behavior, or mutation boundaries.

## Required questions

1. **What responsibilities were previously compressed?**

   Selected pressure evidence presence/absence and selected pressure evidence record construction were compressed in the supporting-evidence path. The previous generic helper also retained an unreachable empty-record case even though the caller already guarded absence.

2. **Which implementation-local ownership boundary became directly observable?**

   Selected pressure supporting-evidence record construction became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   `_pressure_selection_supporting_evidence_payload(...)` now calls `_selected_pressure_evidence(...)` only for concrete selected pressure items, and a focused unit test asserts that helper's exact record shape.

4. **What producer now owns the recovered responsibility?**

   `_selected_pressure_evidence(...)` owns construction of the selected pressure evidence record.

5. **What artifact or helper carries the recovered boundary, if any?**

   The helper `_selected_pressure_evidence(...)` carries the recovered boundary.

6. **Who consumes it?**

   `_pressure_selection_supporting_evidence_payload(...)` consumes `_selected_pressure_evidence(...)` when a selected pressure item exists.

7. **Did any compatibility boundary change?**

   No.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_selected_pressure_evidence(...)`.

## Recovered artifact/helper

`_selected_pressure_evidence(item: PressureItem) -> dict[str, Any]`.

## Recovered consumer

`_pressure_selection_supporting_evidence_payload(...)`.

## Compatibility preserved

No.

Public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and the read-only mutation boundary are preserved. `selection_path_audit` remains a read-only visibility surface; this slice does not introduce acceptance, reliance, action, mutation, execution, planning, prioritization, inquiry generation, route authority, or autonomous next-step selection.

## LOC changed

`git diff --stat` reported:

```text
seed_runtime/selection_path_audit.py |  6 ++----
tests/test_selection_path_audit.py   | 21 +++++++++++++++++++++
2 files changed, 23 insertions(+), 4 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 147 tests.

## Remaining compressed responsibilities

Adjacent evidence shows that the nearest pressure candidate row, rank, projection, enumeration, lineage, payload bundle, selected-name, selected-item lookup, supported/unsupported target, and route-matching responsibilities are already separated by named helpers and covered by tests. Any future slice should begin again from current implementation evidence and should not re-slice those areas by inertia.

Potential remaining compression, if any, should be proven from implementation-local pressure rather than naming symmetry. In this neighborhood, broader supporting-evidence payload ownership remains intentionally broader than this slice: it owns whether evidence is emitted, while `_selected_pressure_evidence(...)` owns the concrete selected pressure evidence record.
