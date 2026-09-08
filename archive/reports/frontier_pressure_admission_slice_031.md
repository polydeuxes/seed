# Frontier Pressure Admission Slice 031

## Selected boundary

Recovered implementation-local ownership boundary: **pressure candidate public-name projection inside `selection_path_audit`**.

## Implementation evidence

I began from `selection_path_audit` immediately adjacent to Slice 030's `_non_selected_pressure_candidates(...)` change. The neighboring code showed that non-selected candidate enumeration and reason preparation were already separated, while pressure candidate display names were still produced by repeating `item.category.lower()` inside multiple downstream consumers:

- candidate-set row assembly in `_candidate(...)`;
- non-selected row assembly in `_non_selected(...)`;
- selected-name preparation via `_selected_name(...)`.

Those consumers were not independently choosing candidate identity. They were all applying the same implementation-local projection rule: a pressure audit category becomes the public selection-path candidate name by lowercasing the category string.

This is narrower than extracting row construction, payload bundling, branch assembly, or another enumeration boundary. The recovered boundary is only the public-name projection rule already required by existing behavior.

## Before

The pressure candidate public-name rule was compressed into each consumer that needed it. Each consumer also owned other responsibilities:

- `_candidate(...)` assembled candidate-set rows and lowercased the category;
- `_non_selected(...)` assembled non-selected rows and lowercased the category;
- `_selected_name(...)` handled focus fallback and lowercased the selected pressure category when present.

The shared projection rule was present in implementation behavior but not directly observable as its own ownership boundary.

## After

`_pressure_candidate_public_name(...)` owns the pressure candidate public-name projection rule. Candidate-set row assembly, non-selected row assembly, and selected-name preparation now consume that helper while preserving their existing responsibilities.

A focused unit test proves that the helper owns the lowercased public-name projection for pressure categories.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_pressure_candidate_public_name(...)` now produces the public selection-path name for a pressure candidate.

## Recovered artifact/helper

`_pressure_candidate_public_name(item)` carries the recovered boundary by returning `item.category.lower()`.

## Recovered consumer

The helper is consumed by:

- `_candidate(...)` for candidate-set row names;
- `_non_selected(...)` for non-selected row names;
- `_selected_name(...)` for selected pressure category names while preserving focus fallback behavior.

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
seed_runtime/selection_path_audit.py | 10 +++++++---
tests/test_selection_path_audit.py   | 15 +++++++++++++++
2 files changed, 22 insertions(+), 3 deletions(-)
```

## Tests executed

```text
python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py
pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result: `144 passed`.

## Required questions

1. **What responsibilities were previously compressed?**

   Pressure candidate public-name projection was compressed into candidate-set row assembly, non-selected row assembly, and selected-name preparation. Those consumers each lowercased `PressureItem.category` while also owning their separate row or selected-name responsibilities.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary for projecting a pressure candidate category into the public selection-path candidate name became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   Implementation now delegates the lowercased category projection to `_pressure_candidate_public_name(...)`. A new test directly exercises that helper and proves the projection rule.

4. **What producer now owns the recovered responsibility?**

   `_pressure_candidate_public_name(...)` owns pressure candidate public-name projection.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_pressure_candidate_public_name(item)` carries the recovered boundary.

6. **Who consumes it?**

   `_candidate(...)`, `_non_selected(...)`, and `_selected_name(...)` consume the helper.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Current implementation evidence still leaves route orchestration in `build_selection_path_audit(...)`, generic text formatting helpers, and field-level row details such as scores, reasons, evidence, and ranks inside their existing row producers. Those were not recovered here because this slice recovers exactly one narrower implementation-backed boundary: pressure candidate public-name projection.
