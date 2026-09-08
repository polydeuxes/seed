# Implementation Recovery Slice 004

## Selected boundary

Recovered boundary: **Selected Surface Value for eligible bounded work**.

The boundary is intentionally local to the existing Selection implementation pressure area. It covers only preparation of the value that will be assigned to the already-selected CLI surface for an already-eligible exact QuestionFamily invocation.

It is not dispatch, request construction, rendering, diagnostics, schema, event-ledger behavior, or an architectural owner.

## Implementation evidence

Implementation evidence immediately adjacent to the recovered bounded ask refusal showed that `bounded_work_selection_for_question_family(...)` still compressed two responsibilities:

1. selecting the dispatch surface from `BOUNDED_ASK_DISPATCH_SURFACES`; and
2. preparing the surface value to pass to that selected surface.

The compressed value preparation was visible because non-parameterized families use the existing `BOUNDED_ASK_ARG_VALUES` fallback behavior, while parameterized families collapse exact operator surface args from `BoundedWorkSurfaceArgsResult` into the value shape consumed by the existing CLI namespace.

That recurring local work is now represented by `BoundedWorkSelectedSurfaceValue` and produced by `bounded_work_selected_surface_value_for_eligibility(...)`.

## Before

`bounded_work_selection_for_question_family(...)` both selected the dispatch surface and prepared `surface_value`:

```text
eligible exact QuestionFamily
  -> bounded work selection
      -> dispatch_surface lookup
      -> required surface arg handling
      -> parameterized surface value shaping
      -> default/static surface value shaping
      -> BoundedWorkSelectionResult
```

That made the selected surface value observable only as an inline construction detail of selection.

## After

The local surface-value preparation is now a separate handoff inside the same Selection pressure area:

```text
eligible exact QuestionFamily
  -> selected surface value preparation
      -> BoundedWorkSelectedSurfaceValue
  -> bounded work selection
      -> dispatch_surface lookup
      -> BoundedWorkSelectionResult
```

Selection still owns selecting the dispatch surface. The new helper only owns the already-existing surface value shape that selection consumes.

## Recovered producer

`bounded_work_selected_surface_value_for_eligibility(...)` now owns the recovered responsibility.

It consumes:

- exact `question_family` text already admitted by lookup and eligibility;
- `BoundedWorkEligibilityResult` already produced by bounded work eligibility; and
- optional `BoundedWorkSurfaceArgsResult` already produced by surface-argument validation.

It produces only the selected surface value handoff.

## Recovered artifact/helper

Artifact: `BoundedWorkSelectedSurfaceValue`.

Helper: `bounded_work_selected_surface_value_for_eligibility(...)`.

The artifact carries:

- `question_family`;
- `surface_value`;
- `required_surface_args`; and
- a local reason string.

It intentionally does not carry `dispatch_surface`, `bounded_status`, or `permitted`.

## Recovered consumer

`bounded_work_selection_for_question_family(...)` consumes `BoundedWorkSelectedSurfaceValue` while continuing to produce `BoundedWorkSelectionResult` for downstream dispatch request construction.

## Compatibility preserved

No.

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, diagnostics, schema, and event-ledger behavior are preserved. The slice refactors implementation-local value preparation without adding a public surface or changing bounded ask output.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_004.md`

## LOC changed

Final repository diff after this slice:

```text
3 files changed, 254 insertions(+), 19 deletions(-)
```

The implementation/test portion before this report was:

```text
2 files changed, 95 insertions(+), 19 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
53 passed
```

## Remaining compressed responsibilities

The adjacent bounded ask implementation still includes compressed or partially adjacent responsibilities that were not recovered by this slice:

- exact CLI shape enforcement for bounded ask;
- presentation-mode handoff for exact QuestionFamily explanation;
- dispatch request construction from selection;
- dispatch execution handoff into the CLI namespace;
- compatibility-specific JSON flag normalization for knowledge reachability;
- final answer rendering outside this local selection pressure area.

This slice does not assert that the next recovery is dispatch, request construction, execution, rendering, or presentation. Future recovery must again be selected solely from implementation evidence.

## Required questions

### 1. What responsibilities were previously compressed?

Selection compressed dispatch-surface selection with selected surface value preparation for default/static and parameterized bounded ask invocations.

### 2. Which implementation-local ownership boundary became directly observable?

Selected Surface Value for eligible bounded work became directly observable.

### 3. What producer now owns the recovered responsibility?

`bounded_work_selected_surface_value_for_eligibility(...)` owns selected surface value preparation.

### 4. What artifact or helper carries the recovered boundary, if any?

`BoundedWorkSelectedSurfaceValue` carries the recovered boundary.

### 5. Who consumes it?

`bounded_work_selection_for_question_family(...)` consumes it.

### 6. Did any compatibility boundary change?

No.
