# Frontier Pressure Admission Slice 032

## Selected boundary

Recovered implementation-local ownership boundary: **pressure candidate rank assignment inside `selection_path_audit`**.

## Implementation evidence

Investigation began in `seed_runtime/selection_path_audit.py` at `selection_path_audit` and the implementation immediately adjacent to Slice 031's `_pressure_candidate_public_name(...)` public-name projection boundary. Current implementation evidence showed that pressure candidate public-name projection is already separated and reused by candidate-set rows, non-selected rows, and selected-name preparation. The next local pressure was not another projection rule.

The candidate-set producer still assigned public candidate ranks inline while also owning candidate-set payload construction and candidate-row construction:

- `_candidate_set_from_pressures(...)` created the `_SelectionCandidateSetPayload`;
- the same expression enumerated pressure candidates with `start=1` to assign public ranks;
- `_candidate(...)` then assembled each candidate row with candidate name, score, rank, reason, and evidence.

The rank assignment is a narrower implementation-local responsibility than candidate-set payload ownership or candidate-row construction. It is also separate from public-name projection: it preserves the current pressure ordering as one-based public rank numbers and does not derive display names.

## Before

Pressure candidate rank assignment was compressed into `_candidate_set_from_pressures(...)`:

- candidate-set payload construction;
- pressure candidate traversal;
- one-based public rank assignment;
- handoff to candidate-row construction.

The one-based rank rule was present in output behavior but was not directly observable as its own implementation-local ownership boundary.

## After

`_ranked_pressure_candidates(...)` owns pressure candidate rank assignment. `_candidate_set_from_pressures(...)` now consumes ranked pressure candidates and remains responsible for candidate-set payload construction. `_candidate(...)` continues to own candidate-row construction.

A focused test directly exercises `_ranked_pressure_candidates(...)` and proves both the one-based rank assignment and the empty-input behavior.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

`_ranked_pressure_candidates(...)` now produces the implementation-local `(rank, PressureItem)` sequence consumed by candidate-set payload construction.

## Recovered artifact/helper

`_ranked_pressure_candidates(pressures)` carries the recovered boundary by returning `tuple(enumerate(pressures, start=1))`.

## Recovered consumer

`_candidate_set_from_pressures(...)` consumes ranked pressure candidates and passes each rank to `_candidate(...)` without owning rank assignment inline.

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
- diagnostics unchanged because no diagnostic surface was added or modified;
- diagnostic inventory unchanged;
- diagnostic shape-audit behavior unchanged;
- event-ledger behavior unchanged;
- read-only `mutates_cluster=false` selection visibility boundary unchanged.

## LOC changed

```text
seed_runtime/selection_path_audit.py |  9 ++++++++-
tests/test_selection_path_audit.py   | 23 +++++++++++++++++++++++
2 files changed, 31 insertions(+), 1 deletion(-)
```

## Tests executed

```text
python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py
pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result: `145 passed`.

## Required questions

1. **What responsibilities were previously compressed?**

   Candidate-set payload construction, pressure candidate traversal, one-based public rank assignment, and candidate-row handoff were compressed in `_candidate_set_from_pressures(...)`.

2. **Which implementation-local ownership boundary became directly observable?**

   Pressure candidate rank assignment became directly observable as a local boundary separate from candidate-set payload construction and candidate-row construction.

3. **What implementation and/or test change made the boundary observable?**

   `_candidate_set_from_pressures(...)` now delegates rank assignment to `_ranked_pressure_candidates(...)`. `tests/test_selection_path_audit.py` directly exercises the helper for populated and empty pressure sequences.

4. **What producer now owns the recovered responsibility?**

   `_ranked_pressure_candidates(...)` owns pressure candidate rank assignment.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_ranked_pressure_candidates(pressures)` carries the boundary.

6. **Who consumes it?**

   `_candidate_set_from_pressures(...)` consumes the ranked pressure candidates and passes the rank into `_candidate(...)`.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Current implementation evidence still leaves route orchestration in `build_selection_path_audit(...)`, selected pressure evidence-record construction inside the existing `_evidence(...)` helper, candidate-row field assembly inside `_candidate(...)`, non-selected row field assembly inside `_non_selected(...)`, and generic human-readable formatting helpers. Those were not recovered here because this slice recovers exactly one narrower implementation-backed boundary: pressure candidate rank assignment. Further work should stop rather than mine helpers if the next candidate boundary is already separated with adequate test coverage or would only create stylistic movement.
