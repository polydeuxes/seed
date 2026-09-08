# Frontier Pressure Admission Slice 033

## Selected boundary

Recovered implementation-local ownership boundary: **pressure candidate row construction inside `selection_path_audit` candidate-set construction**.

This is not a new selection rule, admission rule, ranking rule, or projection rule. It only makes the already-present read-only candidate-row shape ownership directly observable after rank assignment and public-name projection have already been separated.

## Implementation evidence

Investigation began in `seed_runtime/selection_path_audit.py` at `build_selection_path_audit(...)` and the implementation immediately adjacent to the most recent `_ranked_pressure_candidates(...)` slice. Current code already separated:

- target dispatch;
- supported and unsupported payload preparation;
- lineage payload assembly;
- selected pressure item lookup;
- public-name projection via `_pressure_candidate_public_name(...)`;
- non-selected candidate enumeration and reasoning;
- one-based rank assignment via `_ranked_pressure_candidates(...)`.

The still-compressed adjacent responsibility was the handoff from ranked pressure candidates into public candidate-set rows. `_candidate_set_from_pressures(...)` owned candidate-set payload construction, while a generic private row builder accepted split `item` and `rank` arguments. That left the concrete row-shape responsibility observable only as part of candidate-set construction rather than as the producer that consumes a ranked pressure candidate and emits one public candidate row.

The narrower responsibility inside the broader candidate-set boundary was therefore pressure candidate row construction: carrying the ranked candidate pair into the unchanged public row fields (`candidate`, `score`, `rank`, `reason`, `evidence`). Broader candidate-set construction was not selected because it was already separated as `_candidate_set_from_pressures(...)`, and rank assignment/public-name projection were not selected because they were already separated and tested.

## Before

`_candidate_set_from_pressures(...)` iterated over `_ranked_pressure_candidates(...)`, destructured each ranked pair inline, and passed separate `item` and `rank` values into a generic `_candidate(...)` helper. The ranked candidate row shape was not directly named as a ranked-candidate consumer.

## After

`_candidate_set_from_pressures(...)` now passes each ranked candidate pair to `_pressure_candidate_row(...)`. The row producer owns the tuple handoff from rank assignment and produces exactly one unchanged public candidate row. A focused test directly exercises `_pressure_candidate_row(...)` and verifies the row fields without exercising the broader candidate-set payload or ranking helper again.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`
  - Replaced inline ranked-pair destructuring in candidate-set construction with `_pressure_candidate_row(ranked_candidate)`.
  - Replaced the generic `_candidate(...)` row helper with `_pressure_candidate_row(...)`, whose input shape makes the ranked-candidate row boundary directly observable.

## Test files changed

- `tests/test_selection_path_audit.py`
  - Added `test_pressure_candidate_row_is_owned_by_local_helper`, proving the recovered helper owns public candidate-row fields while preserving the existing candidate JSON shape.

## Recovered producer

`_pressure_candidate_row(...)` now owns pressure candidate row construction for the read-only selection-path candidate set.

## Recovered artifact/helper

`_pressure_candidate_row(ranked_candidate: tuple[int, PressureItem]) -> dict[str, Any]` carries the recovered boundary.

## Recovered consumer

`_candidate_set_from_pressures(...)` consumes ranked pressure candidates and delegates row construction to `_pressure_candidate_row(...)` while retaining candidate-set payload ownership.

## Required questions

1. **What responsibilities were previously compressed?**

   Candidate-set payload construction, ranked-candidate pair consumption, and public candidate-row field assembly were adjacent. Rank assignment was separated, but the row producer did not visibly consume the ranked candidate as a single implementation-local artifact.

2. **Which implementation-local ownership boundary became directly observable?**

   Pressure candidate row construction became directly observable as the boundary that consumes one ranked pressure candidate and emits one public candidate row.

3. **What implementation and/or test change made the boundary observable?**

   `_candidate_set_from_pressures(...)` now calls `_pressure_candidate_row(ranked_candidate)`, and `test_pressure_candidate_row_is_owned_by_local_helper` directly verifies the helper's row output.

4. **What producer now owns the recovered responsibility?**

   `_pressure_candidate_row(...)`.

5. **What artifact or helper carries the recovered boundary, if any?**

   The helper `_pressure_candidate_row(...)` carries it.

6. **Who consumes it?**

   `_candidate_set_from_pressures(...)` consumes it to build `_SelectionCandidateSetPayload`.

7. **Did any compatibility boundary change?**

   No.

## Compatibility preserved

- Public JSON output: preserved.
- Human-readable output: preserved.
- CLI behavior: preserved.
- Diagnostic inventory and diagnostic shape audit behavior: preserved.
- Schema: preserved.
- Event ledger behavior: preserved.
- Read-only mutation boundary: preserved.
- Expected compatibility answer: No.

## LOC changed

Final diff stat:

```text
seed_runtime/selection_path_audit.py |  9 ++++++---
tests/test_selection_path_audit.py   | 23 +++++++++++++++++++++++
2 files changed, 29 insertions(+), 3 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 146 tests.

## Remaining compressed responsibilities

Remaining code should not be mined by naming symmetry or campaign history. Current implementation still contains generic output formatting helpers, outer target dispatch orchestration, target normalization/matching helpers, selected-evidence row preparation, and compatibility construction. Those were not recovered here because this slice recovers exactly one narrower implementation-backed boundary adjacent to the rank-assignment slice: pressure candidate row construction. Future work should stop rather than force a slice if no fresh compressed implementation responsibility remains.

## Constitutional guardrail

This slice preserves `selection_path_audit` as read-only explanation and visibility. It does not introduce acceptance, reliance, action, mutation, execution, planning, prioritization, inquiry generation, route authority, readiness evaluation, event-ledger writes, or cluster mutation.
