# Implementation Recovery Slice 006

## Selected boundary

Recovered boundary: **Bounded Work Presentation Handoff for eligible bounded ask work**.

Implementation evidence selected this boundary because `apply_bounded_ask_dispatch(...)` already had an adjacent, repeated handoff for `--presentation` after bounded eligibility and before dispatch request construction. The handoff copied the exact eligible `QuestionFamily` into `args.question_family_explanation` and stopped normal bounded-work dispatch.

This slice does not recover dispatch request construction, dispatch execution, rendering, diagnostics, schema, event ledger behavior, or a framework.

## Implementation evidence

The local bounded ask chain before this slice was clean through selected dispatch and selected value:

```text
Exact Lookup
↓
Surface Args
↓
Refusal
↓
Selected Surface Value
↓
Selected Dispatch Surface
```

Adjacent implementation evidence showed one smaller recurring compressed responsibility in `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`:

1. After `eligible_with_parameters`, `--presentation` set `args.question_family_explanation = family`, cleared `args.message`, and returned before selection, dispatch request construction, and execution.
2. After permitted `eligible_now`, the same presentation handoff set `args.question_family_explanation = family`, cleared `args.message`, and returned before selection, dispatch request construction, and execution.

That repeated local behavior is now represented by `BoundedWorkPresentationHandoff` and produced by `bounded_work_presentation_handoff_for_eligibility(...)`.

## Before

```text
eligible bounded work
  -> optional surface args validation
  -> if presentation:
       mutate args.question_family_explanation directly
       clear args.message
       stop dispatch
  -> bounded work selection
  -> dispatch request construction
  -> dispatch execution
```

The presentation branch was compressed inside the CLI adapter alongside eligibility consumption, selection, dispatch request construction, and execution preparation.

## After

```text
eligible bounded work
  -> optional surface args validation
  -> if presentation:
       BoundedWorkPresentationHandoff
       CLI adapter applies existing args handoff
       stop dispatch
  -> bounded work selection
  -> dispatch request construction
  -> dispatch execution
```

The CLI adapter still performs the same namespace mutation, but it now consumes an explicit implementation-local handoff artifact for the presentation path.

## Recovered producer

Producer: `bounded_work_presentation_handoff_for_eligibility(...)`.

It consumes an already matched, permitted `BoundedWorkEligibilityResult` and returns the existing question-family explanation handoff value. It refuses mismatched or non-permitted eligibility.

## Recovered artifact/helper

Artifact: `BoundedWorkPresentationHandoff`.

The artifact carries:

- `question_family`;
- `question_family_explanation`;
- `reason`.

It intentionally does not carry dispatch surface, selected surface value, required surface args, bounded status, permission fields, dispatch request data, rendering output, diagnostic records, schema data, or event-ledger data.

## Recovered consumer

Consumer: `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`.

It consumes `BoundedWorkPresentationHandoff` only when the operator supplied `ask --question-family ... --presentation`. It preserves the existing behavior by assigning `args.question_family_explanation`, clearing `args.message`, and returning before dispatch.

## Required questions

### 1. What responsibilities were previously compressed?

The bounded ask CLI adapter previously compressed:

- eligible bounded-work consumption;
- presentation handoff construction;
- direct CLI namespace mutation for `question_family_explanation`;
- dispatch selection bypass when presentation was requested;
- downstream dispatch request construction and execution for non-presentation paths.

### 2. Which implementation-local ownership boundary became directly observable?

Bounded Work Presentation Handoff for eligible bounded ask work became directly observable.

### 3. What producer now owns the recovered responsibility?

`bounded_work_presentation_handoff_for_eligibility(...)` now owns construction of the local presentation handoff.

### 4. What artifact or helper carries the recovered boundary, if any?

`BoundedWorkPresentationHandoff` carries the recovered boundary.

### 5. Who consumes it?

`apply_bounded_ask_dispatch(...)` consumes it on the `--presentation` path.

### 6. Did any compatibility boundary change?

No.

## Compatibility preserved

No public compatibility boundary changed.

Preserved behavior:

- same CLI invocation shape;
- same accepted `ask --question-family ... --presentation` paths;
- same parser errors for unknown, diagnostic-only, non-dispatchable, or argument-invalid families;
- same `args.question_family_explanation` value;
- same `args.message = []` stop behavior;
- same dispatch selection, dispatch request construction, and dispatch execution behavior when `--presentation` is absent;
- same JSON output behavior;
- same diagnostics, schema, and event ledger behavior.

## Files changed

- `seed_runtime/question_surface_inventory.py`
  - Added `BoundedWorkPresentationHandoff`.
  - Added `bounded_work_presentation_handoff_for_eligibility(...)`.
- `scripts/seed_local.py`
  - Routed existing bounded ask presentation branches through the recovered handoff producer.
- `tests/test_question_surface_inventory.py`
  - Added tests proving the handoff is separate from dispatch request data.
  - Added bounded ask CLI coverage proving parameterized presentation still stops before dispatch and preserves the existing explanation handoff.
- `implementation_recovery_slice_006.md`
  - Recorded this implementation recovery slice.

## LOC changed

At the time of this slice note, implementation and test diff before this document was:

```text
3 files changed, 82 insertions(+), 2 deletions(-)
```

Including this recovery note, the final commit changes this document plus the implementation and test files.

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
55 passed in 53.06s
```

## Remaining compressed responsibilities

Remaining adjacent responsibilities are intentionally not recovered in this slice:

- dispatch request construction;
- dispatch execution preparation;
- bounded work invocation side effects;
- knowledge-reachability JSON compatibility adjustment after dispatch;
- result rendering handoff;
- diagnostic inventory and shape-audit surfaces;
- schema behavior;
- event ledger behavior.

These remain future implementation questions only if implementation evidence selects one of them as the next smallest adjacent ownership boundary.
