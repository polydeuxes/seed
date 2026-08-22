# Frontier Pressure Admission Slice 036

## Selected boundary

Recovered implementation-local ownership boundary: **pressure candidate admission ownership inside `pressure_audit`**.

The recovered boundary is the local handoff where `build_pressure_audit(...)` stops owning the inline conversion, rejection, and ordering rules for candidate pressure producers. Those rules are now carried by `_admitted_pressure_items(...)`, which admits only present positive-score pressure candidates, converts them to public `PressureItem` records, and preserves the existing pressure ordering by descending score and category name.

## Implementation evidence

Investigation began from the producer immediately consumed by `selection_path_audit`: `build_selection_path_audit(...)` calls `_selection_path_inputs(...)`, which calls `build_pressure_audit(...)` and passes the resulting `pressure.pressures` into focus-selection, pressure-category matching, pressure candidate rows, non-selected rows, selection factors, and unknown handling.

`frontier_pressure_admission_slice_035.md` was used only as the stop marker for the exhausted `selection_path_audit` neighborhood. The implementation hop outward showed that `build_pressure_audit(...)` still compressed one implementation-local responsibility after collecting adjacent producers: it converted private `_PressureItemCandidate` objects into public `PressureItem` objects, rejected `None` and non-positive candidates, and sorted the admitted public pressure items in the same inline expression that orchestrated the pressure input producers.

That admission step is upstream of `selection_path_audit` and materially determines the `pressures` tuple consumed by the selection-path audit surface, but it is not a selection-path route, payload, selected-evidence, candidate-row, target-matching, unsupported-target, or formatting boundary.

## Before

`build_pressure_audit(...)` directly owned three responsibilities in one list/sort expression after invoking the pressure candidate producers:

- reject absent candidate outputs;
- reject candidates with non-positive scores;
- convert and order the remaining candidates before constructing `PressureAudit`.

The only direct pressure candidate conversion test exercised `_PressureItemCandidate.to_pressure_item()` for one candidate shape, while existing aggregate tests inferred admission through `build_pressure_audit(...)` output.

## After

`build_pressure_audit(...)` still owns the orchestration of existing pressure candidate producers, but delegates admission of produced candidates to `_admitted_pressure_items(...)`. The helper owns candidate filtering, public-item conversion, and ordering. `tests/test_pressure_audit.py` now directly proves that boundary by passing positive candidates, `None`, a zero-score candidate, and score/category tie cases into the helper and asserting the admitted output order.

## Implementation files changed

- `seed_runtime/pressure_audit.py`

## Test files changed

- `tests/test_pressure_audit.py`

## Recovered producer

`seed_runtime.pressure_audit.build_pressure_audit(...)` remains the public producer of `PressureAudit`, while `_admitted_pressure_items(...)` is now the implementation-local producer of the admitted `PressureItem` tuple used in that audit.

## Recovered artifact/helper

`_admitted_pressure_items(...)` carries the recovered boundary.

## Recovered consumer

`build_pressure_audit(...)` consumes `_admitted_pressure_items(...)` when constructing `PressureAudit`. Downstream, `selection_path_audit` consumes `PressureAudit.pressures` through `_selection_path_inputs(...)` without any compatibility change.

## Compatibility preserved

No compatibility boundary changed.

Expected compatibility answer:

```text
No.
```

Runtime behavior, CLI behavior, JSON output, human-readable output, diagnostics, schema, event-ledger behavior, and read-only mutation boundaries are preserved. The same candidate sources are called, the same candidates are rejected, and the same admitted `PressureItem` records are sorted with the same key.

## LOC changed

`git diff --stat` reported:

```text
seed_runtime/pressure_audit.py | 20 +++++++++++++-------
tests/test_pressure_audit.py   | 39 +++++++++++++++++++++++++++++++++++++++
2 files changed, 52 insertions(+), 7 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` — passed.
- `pytest -q tests/test_pressure_audit.py tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 153 tests.

## Required Questions

### 1. What responsibility was previously compressed?

Pressure candidate admission was compressed inside `build_pressure_audit(...)`: absent candidate rejection, non-positive-score rejection, conversion from private `_PressureItemCandidate` to public `PressureItem`, and deterministic admitted-item ordering.

### 2. Which implementation-local ownership boundary became directly observable?

The implementation-local boundary between pressure source orchestration and admitted pressure item production became directly observable.

### 3. What implementation and/or test change made the boundary observable?

`build_pressure_audit(...)` now delegates admitted pressure tuple construction to `_admitted_pressure_items(...)`. `tests/test_pressure_audit.py` directly exercises that helper with present, absent, zero-score, lower-score, and same-score/category-tie candidates.

### 4. What producer now owns the recovered responsibility?

`_admitted_pressure_items(...)` owns admitted pressure item production.

### 5. What artifact or helper carries the recovered boundary, if any?

The helper `_admitted_pressure_items(...)` carries the recovered boundary.

### 6. Who consumes it?

`build_pressure_audit(...)` consumes the helper output to construct `PressureAudit`. `selection_path_audit` then consumes the resulting `PressureAudit.pressures` through its existing input path.

### 7. Did any compatibility boundary change?

No.

### 8. Why is this outside the exhausted `selection_path_audit` neighborhood from Slice 035?

This slice changes only `pressure_audit`, the upstream producer of `PressureAudit.pressures`. It does not reopen route ordering, pressure-selection payloads, selected pressure evidence records, candidate-set rows, ranking inside selection-path presentation, selected-name/public-name projection, target matching, unsupported-target helpers, or generic formatting inside `selection_path_audit`. The recovered boundary was selected from implementation evidence in the producer immediately consumed by `selection_path_audit`, one implementation hop outward from the exhausted Slice 035 neighborhood.

## Remaining compressed responsibilities

Remaining pressure-audit compression should be evaluated only from current implementation evidence. The pressure source functions still contain their own evidence shaping and scoring logic, but this slice does not claim those boundaries because it recovers exactly one implementation-local ownership boundary: admission of already-produced pressure candidates into the public pressure tuple. Further movement would need fresh evidence that a source-local responsibility is compressed and not already adequately named and tested.

## Slice 035 stop-marker respect

This slice used `frontier_pressure_admission_slice_035.md` only to avoid the exhausted immediate `selection_path_audit` neighborhood. No `selection_path_audit` implementation or tests were changed. The recovered ownership boundary is in `pressure_audit`, the nearest upstream producer whose material output is consumed by the selection-path audit surface.
