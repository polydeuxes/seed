# Implementation Recovery Slice 005

## Selected boundary

Recovered boundary: **Selected Dispatch Surface for eligible bounded work**.

The boundary is intentionally local to the current Selection implementation pressure area. It covers only map-backed selection of the existing CLI dispatch surface for an already-eligible exact QuestionFamily invocation.

It is not dispatch request construction, dispatch execution, rendering, diagnostics, schema, event-ledger behavior, routing, scheduling, planning, or an architectural owner.

## Implementation evidence

Implementation evidence immediately adjacent to Slice 004 showed that `bounded_work_selection_for_question_family(...)` still compressed two sibling selection handoffs after eligibility:

1. selecting the dispatch surface from `BOUNDED_ASK_DISPATCH_SURFACES`; and
2. consuming `BoundedWorkSelectedSurfaceValue` to construct the existing `BoundedWorkSelectionResult`.

Slice 004 had already made selected surface-value preparation directly observable. The directly adjacent remaining compressed responsibility was the map-backed dispatch-surface lookup still inline in selection.

That recurring local work is now represented by `BoundedWorkSelectedDispatchSurface` and produced by `bounded_work_selected_dispatch_surface_for_eligibility(...)`.

## Before

`bounded_work_selection_for_question_family(...)` still owned dispatch-surface lookup while also consuming the selected surface value and constructing the downstream selection result:

```text
eligible exact QuestionFamily
  -> bounded work selection
      -> dispatch_surface lookup from BOUNDED_ASK_DISPATCH_SURFACES
      -> selected surface value handoff consumption
      -> BoundedWorkSelectionResult
```

That made the selected dispatch surface observable only as an inline construction detail of selection.

## After

The local dispatch-surface selection is now a separate handoff inside the same Selection pressure area:

```text
eligible exact QuestionFamily
  -> selected dispatch surface preparation
      -> BoundedWorkSelectedDispatchSurface
  -> selected surface value preparation
      -> BoundedWorkSelectedSurfaceValue
  -> bounded work selection
      -> BoundedWorkSelectionResult
```

Selection still produces `BoundedWorkSelectionResult`. The new helper only owns the already-existing map-backed dispatch surface identity consumed by that result.

## Recovered producer

`bounded_work_selected_dispatch_surface_for_eligibility(...)` now owns the recovered responsibility.

It consumes:

- exact `question_family` text already admitted by lookup and eligibility; and
- `BoundedWorkEligibilityResult` already produced by bounded work eligibility.

It produces only the selected dispatch-surface handoff.

## Recovered artifact/helper

Artifact: `BoundedWorkSelectedDispatchSurface`.

Helper: `bounded_work_selected_dispatch_surface_for_eligibility(...)`.

The artifact carries:

- `question_family`;
- `dispatch_surface`; and
- a local reason string.

It intentionally does not carry `surface_value`, `required_surface_args`, `bounded_status`, or `permitted`.

## Recovered consumer

`bounded_work_selection_for_question_family(...)` consumes `BoundedWorkSelectedDispatchSurface` alongside `BoundedWorkSelectedSurfaceValue` while continuing to produce `BoundedWorkSelectionResult` for downstream dispatch request construction.

## Compatibility preserved

No.

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, diagnostics, schema, and event-ledger behavior are preserved. The slice refactors implementation-local dispatch surface selection without adding a public surface or changing bounded ask output.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_005.md`

## LOC changed

Final repository diff after this slice:

```text
3 files changed, 227 insertions(+), 3 deletions(-)
```

The implementation/test portion before this report was:

```text
2 files changed, 65 insertions(+), 3 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
python scripts/seed_local.py ask --question-family "authority-constrained service ownership" --json >/tmp/seed_app_check.json && python - <<'PY'
import json
p=json.load(open('/tmp/seed_app_check.json'))
print(type(p).__name__)
PY
```

Result:

```text
54 passed
dict
```

## Remaining compressed responsibilities

The adjacent bounded ask implementation still includes compressed or partially adjacent responsibilities that were not recovered by this slice:

- exact CLI shape enforcement for bounded ask;
- presentation-mode handoff for exact QuestionFamily explanation;
- dispatch request construction from selection;
- dispatch execution handoff into the CLI namespace;
- compatibility-specific JSON flag normalization for knowledge reachability;
- final answer rendering outside this local selection pressure area.

This slice does not assert that the next recovery is request construction, execution, rendering, presentation, routing, planning, scheduling, or any architectural expansion. Future recovery must again be selected solely from implementation evidence.

## Required questions

### 1. What responsibilities were previously compressed?

Selection compressed map-backed dispatch-surface selection with selected surface value consumption and `BoundedWorkSelectionResult` construction.

### 2. Which implementation-local ownership boundary became directly observable?

Selected Dispatch Surface for eligible bounded work became directly observable.

### 3. What producer now owns the recovered responsibility?

`bounded_work_selected_dispatch_surface_for_eligibility(...)` owns selected dispatch-surface preparation.

### 4. What artifact or helper carries the recovered boundary, if any?

`BoundedWorkSelectedDispatchSurface` carries the recovered boundary.

### 5. Who consumes it?

`bounded_work_selection_for_question_family(...)` consumes it.

### 6. Did any compatibility boundary change?

No.
