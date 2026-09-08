# Implementation Recovery Slice 008

## Selected boundary

**Bounded work dispatch result handoff consumption.**

The adjacent implementation evidence showed that non-presentation bounded ask dispatch already produced a `BoundedWorkDispatchResult`, but the post-dispatch compatibility handoff for `knowledge reachability` JSON output was still compressed into `apply_bounded_ask_dispatch(...)` after dispatch execution.

## Implementation evidence

- `execute_bounded_work_dispatch(...)` already consumed a `BoundedWorkDispatchRequest`, performed the existing CLI namespace mutation, and returned a `BoundedWorkDispatchResult`.
- `apply_bounded_ask_dispatch(...)` ignored that result and directly owned the immediately adjacent compatibility handoff: when the selected family was `knowledge reachability` and `--json` was still active, it set `args.knowledge_reachability_audit_json = True` and reset `args.json_output = False`.
- That compatibility handoff belongs after dispatch execution and before downstream rendering, but it does not construct the request, execute dispatch, compose answers, render output, alter diagnostics, alter schema, write the event ledger, or route semantically.

## Before

The non-presentation permitted bounded ask path compressed these responsibilities in the CLI adapter:

1. exact question-family lookup;
2. bounded eligibility;
3. optional surface-argument validation;
4. selection;
5. dispatch request construction;
6. dispatch execution;
7. direct post-dispatch JSON compatibility mutation for `knowledge reachability`;
8. message clearing and downstream CLI rendering handoff.

The `BoundedWorkDispatchResult` was produced, but no local owner consumed it.

## After

`apply_bounded_work_dispatch_result(...)` now consumes the already produced `BoundedWorkDispatchResult` and applies only the existing post-dispatch CLI compatibility handoff.

`apply_bounded_ask_dispatch(...)` still owns bounded ask orchestration, selection sequencing, dispatch-request invocation, message clearing, and downstream rendering handoff. It now delegates only dispatch-result compatibility consumption to the recovered helper.

## Recovered producer

`execute_bounded_work_dispatch(...)` remains the producer. It owns the existing dispatch execution namespace mutation and returns the dispatch result.

## Recovered artifact/helper

- Artifact: `BoundedWorkDispatchResult`
- Helper: `apply_bounded_work_dispatch_result(...)`

The helper carries only the result-handoff consumption boundary. It does not decide exact lookup, eligibility, surface arguments, selection, dispatch request construction, dispatch execution, presentation, answer composition, rendering, diagnostics, schema, event-ledger behavior, or semantic routing.

## Recovered consumer

`apply_bounded_ask_dispatch(...)` consumes the helper after `execute_bounded_work_dispatch(...)` in the non-presentation permitted paths.

## Compatibility preserved

No.

No public compatibility boundary changed. CLI behavior, runtime behavior, JSON output, diagnostics, schema, and event-ledger behavior are preserved. The existing `knowledge reachability` JSON compatibility behavior is unchanged and remains scoped to post-dispatch bounded ask handling.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_008.md`

## LOC changed

Initial code/test diff before this report: **76 insertions, 5 deletions** across three implementation/test files.

This report adds one documentation artifact for Slice 008.

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
```

Result: `58 passed in 52.73s`.

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result: `51 passed in 1.49s`.

## Required questions

1. **What responsibilities were previously compressed?**

   Dispatch execution and dispatch-result compatibility consumption were adjacent, but the post-dispatch `knowledge reachability` JSON namespace mutation still lived directly inside bounded ask orchestration.

2. **Which implementation-local ownership boundary became directly observable?**

   The local boundary between a completed bounded work dispatch result and the post-dispatch CLI compatibility mutation that consumes that result.

3. **What producer now owns the recovered responsibility?**

   `execute_bounded_work_dispatch(...)` owns production of the `BoundedWorkDispatchResult`; `apply_bounded_work_dispatch_result(...)` owns consuming that result for the existing compatibility handoff.

4. **What artifact or helper carries the recovered boundary, if any?**

   `BoundedWorkDispatchResult` carries the dispatch result artifact, and `apply_bounded_work_dispatch_result(...)` carries the recovered result-handoff consumption boundary.

5. **Who consumes it?**

   `apply_bounded_ask_dispatch(...)` consumes the helper after dispatch execution in the non-presentation permitted bounded ask paths.

6. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

- Bounded ask orchestration still sequences exact lookup, eligibility, surface-argument validation, refusal, presentation stop-before-dispatch behavior, selection, dispatch request construction, dispatch execution, dispatch-result consumption, and message clearing.
- Result rendering remains outside this slice.
- Dispatch request construction remains outside this slice.
- Presentation handoff production and consumption remain separately recovered and unchanged.
- Selected surface value and selected dispatch surface production remain separately recovered and unchanged.
- CLI namespace mutation for dispatch execution remains owned by `execute_bounded_work_dispatch(...)` and unchanged.
