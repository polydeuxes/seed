# Frontier Pressure Admission Slice 030

## Selected boundary

Recovered implementation-local ownership boundary: **non-selected pressure candidate enumeration inside `selection_path_audit`**.

## Slice 030 exhaustion checkpoint

1. Adjacent responsibilities already named and tested: supported pressure-selection payload bundling, selected pressure item lookup, selected-name preparation, candidate-set payload preparation, selection-factor payload preparation, unknown payload preparation, non-selected payload preparation, non-selected row assembly, and non-selected reason preparation.
2. Still-inline responsibility found from current implementation evidence: `_non_selected_from_pressures(...)` still selected the non-selected candidate sequence with `pressures[1:]` inline while also building the `_SelectionNonSelectedPayload` rows.
3. The proposed slice is ownership recovery, not helper cleanup, because the helper now owns the concrete admission boundary for which pressure candidates are eligible to be explained as non-selected alternatives: every pressure candidate after the already-selected head.
4. A justified recovery remains, so this is not a stop report.

## Implementation evidence

The current neighborhood around `_non_selected_from_pressures(...)` showed that the payload helper had already separated non-selected payload ownership and the most recent slice had separated reason preparation through `_non_selected_reason(...)`. However, candidate admission into the non-selected set was still compressed into payload row construction by iterating directly over `pressures[1:]`.

That slice is implementation-backed because the public audit semantics distinguish the selected pressure item from non-selected alternatives. The first pressure item is selected by `_selected_pressure_item(...)`, while non-selected candidates are the remaining pressure candidates. Before this slice, that complementary candidate enumeration boundary was only visible as a slice expression inside `_non_selected_from_pressures(...)`.

## Before

`_non_selected_from_pressures(...)` simultaneously:

- owned `_SelectionNonSelectedPayload` construction;
- chose which pressure candidates entered the non-selected set by slicing `pressures[1:]` inline;
- delegated each admitted item to `_non_selected(...)` for row assembly;
- delegated row reason text to `_non_selected_reason(...)`.

This compressed non-selected candidate admission with payload construction.

## After

`_non_selected_pressure_candidates(...)` owns the candidate enumeration boundary. `_non_selected_from_pressures(...)` now consumes that helper and remains responsible for constructing the non-selected payload rows.

The new test directly exercises populated, selected-only, and empty pressure inputs, proving that non-selected candidate enumeration excludes the selected head and returns no candidates when no non-selected alternatives exist.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_non_selected_pressure_candidates(...)` now produces the tuple of pressure candidates eligible for non-selected explanation.

## Recovered artifact/helper

`_non_selected_pressure_candidates(pressures)` carries the recovered boundary by returning `pressures[1:]` as the non-selected candidate sequence.

## Recovered consumer

`_non_selected_from_pressures(...)` consumes `_non_selected_pressure_candidates(...)` before passing each admitted candidate to `_non_selected(...)`.

## Compatibility preserved

No compatibility boundary changed.

Expected compatibility answer:

```text
No.
```

Preserved behavior:

- public JSON output unchanged;
- human-readable output unchanged;
- CLI behavior unchanged;
- diagnostic inventory unchanged because no diagnostic surface was added or modified;
- diagnostic shape-audit behavior unchanged;
- event-ledger behavior unchanged;
- read-only `mutates_cluster=false` selection visibility boundary unchanged.

## LOC changed

```text
seed_runtime/selection_path_audit.py | 11 ++++++++++-
tests/test_selection_path_audit.py   | 33 +++++++++++++++++++++++++++++++++
2 files changed, 43 insertions(+), 1 deletion(-)
```

## Tests executed

```text
python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py
pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result: `143 passed`.

## Required questions

1. **What responsibilities were previously compressed?**

   Non-selected payload construction and non-selected pressure candidate enumeration were compressed together inside `_non_selected_from_pressures(...)` through the inline `pressures[1:]` slice.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary for enumerating pressure candidates eligible to appear as non-selected alternatives became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   Implementation now delegates candidate enumeration to `_non_selected_pressure_candidates(...)`. Tests now directly exercise that helper for populated, selected-only, and empty pressure candidate sequences.

4. **What producer now owns the recovered responsibility?**

   `_non_selected_pressure_candidates(...)` owns non-selected pressure candidate enumeration.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_non_selected_pressure_candidates(pressures)` carries the recovered boundary.

6. **Who consumes it?**

   `_non_selected_from_pressures(...)` consumes the helper result while constructing `_SelectionNonSelectedPayload`.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Current evidence still leaves broader route orchestration in `build_selection_path_audit(...)`, generic display formatting helpers, and pressure candidate row field assembly in `_candidate(...)` and `_non_selected(...)`. Those were not recovered here because this slice recovers exactly one directly evidenced boundary adjacent to the most recent non-selected reason preparation, and further movement should be justified only by a fresh implementation-local exhaustion check.
