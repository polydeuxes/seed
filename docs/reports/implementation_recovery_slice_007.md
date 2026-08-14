# Implementation Recovery Slice 007

## Selected boundary

**Bounded work presentation handoff consumption.**

The adjacent implementation evidence showed that the bounded ask path already had a recovered `BoundedWorkPresentationHandoff`, but consumption of that handoff was still compressed into `apply_bounded_ask_dispatch(...)` as direct CLI namespace assignment in both permitted presentation branches.

## Implementation evidence

- `bounded_work_presentation_handoff_for_eligibility(...)` produces a narrow presentation handoff for permitted bounded work only.
- `apply_bounded_ask_dispatch(...)` consumed that handoff by directly assigning `args.question_family_explanation` in both the parameterized permitted presentation branch and the non-parameterized permitted presentation branch.
- Dispatch execution already had a local consumer boundary through `execute_bounded_work_dispatch(...)`, which made the adjacent missing presentation-side consumer directly observable without expanding into rendering, dispatch request construction, diagnostics, schema, or event ledger behavior.

## Before

Presentation handoff production was separated, but presentation handoff consumption remained compressed into the bounded ask orchestration function:

1. validate exact question family;
2. evaluate bounded eligibility;
3. validate surface args when permitted;
4. prepare presentation handoff;
5. mutate the CLI namespace for presentation;
6. clear `args.message` and stop before dispatch.

The same direct namespace assignment appeared in both permitted presentation branches.

## After

`apply_bounded_work_presentation_handoff(...)` now consumes the already prepared `BoundedWorkPresentationHandoff` and applies only the existing `question_family_explanation` namespace mutation. It returns `BoundedWorkPresentationHandoffResult` to make that consumption boundary testable without carrying dispatch surface, surface value, required args, rendering, diagnostics, schema, event-ledger, or semantic-routing responsibilities.

`apply_bounded_ask_dispatch(...)` still owns bounded ask orchestration and stop-before-dispatch control flow. It now delegates only the presentation namespace mutation to the recovered consumer helper.

## Recovered producer

`bounded_work_presentation_handoff_for_eligibility(...)` remains the producer. It owns preparing the permitted bounded work presentation handoff.

## Recovered artifact/helper

- Artifact: `BoundedWorkPresentationHandoffResult`
- Helper: `apply_bounded_work_presentation_handoff(...)`

The helper carries only the handoff consumption result. It does not select dispatch surfaces, construct dispatch requests, execute dispatch, render results, compose answers, update diagnostics, alter schema, write event-ledger entries, or perform semantic routing.

## Recovered consumer

`apply_bounded_ask_dispatch(...)` consumes the helper when `--presentation` is requested for permitted bounded work. The helper mutates only `args.question_family_explanation`; the bounded ask orchestration still clears `args.message` and returns before dispatch.

## Compatibility preserved

No.

No public compatibility boundary changed. CLI behavior, runtime behavior, JSON output, diagnostics, schema, and event-ledger behavior are preserved. The existing stop-before-dispatch presentation behavior is unchanged.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_007.md`

## LOC changed

Initial code/test diff before this report: **66 insertions, 4 deletions** across three implementation/test files.

This report adds one documentation artifact for Slice 007.

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result: `107 passed in 52.33s`.

## Required questions

1. **What responsibilities were previously compressed?**

   Presentation handoff production and presentation handoff consumption were adjacent, but consumption still lived inside bounded ask orchestration as direct CLI namespace mutation in both presentation branches.

2. **Which implementation-local ownership boundary became directly observable?**

   The local boundary between a prepared bounded work presentation handoff and the CLI namespace mutation that consumes that handoff.

3. **What producer now owns the recovered responsibility?**

   `bounded_work_presentation_handoff_for_eligibility(...)` owns production of the presentation handoff; `apply_bounded_work_presentation_handoff(...)` owns consuming that handoff.

4. **What artifact or helper carries the recovered boundary, if any?**

   `BoundedWorkPresentationHandoffResult` and `apply_bounded_work_presentation_handoff(...)` carry the recovered handoff-consumption boundary.

5. **Who consumes it?**

   `apply_bounded_ask_dispatch(...)` consumes the helper in the permitted `--presentation` branches.

6. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

- Bounded ask orchestration still sequences exact lookup, eligibility, surface-argument validation, refusal, presentation stop-before-dispatch behavior, selection, dispatch request construction, dispatch execution, knowledge-reachability JSON flag compatibility, and message clearing.
- Result rendering remains outside this slice.
- Dispatch request construction remains outside this slice.
- Selected surface value and dispatch surface selection remain separately recovered and unchanged.
- CLI namespace mutation for non-presentation dispatch remains owned by the existing dispatch execution helper and unchanged.
