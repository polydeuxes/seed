# Implementation Recovery Slice 009

## Selected boundary

**Bounded work dispatch result production.**

The adjacent implementation evidence showed that `execute_bounded_work_dispatch(...)` already owned the existing CLI namespace mutation for a selected bounded work dispatch request, while it also constructed the `BoundedWorkDispatchResult` consumed by the post-dispatch compatibility handoff recovered in Slice 008.

This slice recovers only the local producer side of that result. It does not recover dispatch execution, request construction, rendering, diagnostics, schema, event-ledger behavior, semantic routing, or CLI mutation after dispatch.

## Implementation evidence

- `BoundedWorkDispatchRequest` already carried the selected dispatch surface and value.
- `execute_bounded_work_dispatch(...)` performed the existing dispatch execution by mutating the CLI namespace with `setattr(args, dispatch_request.dispatch_surface, dispatch_request.surface_value)`.
- The same function also constructed `BoundedWorkDispatchResult` from the request fields.
- Slice 008 made `apply_bounded_work_dispatch_result(...)` consume the produced result, which made the producer side directly observable as a separate adjacent local seam.
- Producing the result from the request does not require the CLI namespace, rendering, answer composition, diagnostics, schema, event ledger, or semantic routing.

## Before

The non-presentation permitted bounded ask path had these adjacent responsibilities in and around dispatch execution:

1. selected bounded work;
2. dispatch request construction;
3. CLI namespace mutation for dispatch execution;
4. dispatch result construction;
5. post-dispatch dispatch-result compatibility consumption;
6. message clearing;
7. downstream rendering handoff.

The result artifact existed, but its production was compressed into the same helper that mutates the CLI namespace.

## After

`bounded_work_dispatch_result_for_request(...)` now produces the existing `BoundedWorkDispatchResult` from an already selected `BoundedWorkDispatchRequest`.

`execute_bounded_work_dispatch(...)` still owns dispatch execution and still returns the same result, but it delegates only result construction to the recovered producer helper after performing the existing namespace mutation.

## Recovered producer

`bounded_work_dispatch_result_for_request(...)` owns production of the `BoundedWorkDispatchResult` artifact from the dispatch request.

## Recovered artifact/helper

- Artifact: `BoundedWorkDispatchResult`
- Helper: `bounded_work_dispatch_result_for_request(...)`

The helper carries only the result-production boundary. It does not mutate the CLI namespace, decide exact lookup, eligibility, surface arguments, selection, dispatch request construction, dispatch execution, presentation, answer composition, rendering, diagnostics, schema, event-ledger behavior, or semantic routing.

## Recovered consumer

`execute_bounded_work_dispatch(...)` consumes the helper after performing the existing dispatch execution namespace mutation and returns the produced result to `apply_bounded_ask_dispatch(...)`.

`apply_bounded_work_dispatch_result(...)` remains the post-dispatch result-handoff consumer recovered by Slice 008.

## Compatibility preserved

No.

No public compatibility boundary changed. CLI behavior, runtime behavior, JSON output, diagnostics, schema, and event-ledger behavior are preserved. The existing `knowledge reachability` JSON compatibility handoff remains unchanged and still occurs only after dispatch execution.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_009.md`

## LOC changed

Code and tests before this report:

```text
seed_runtime/question_surface_inventory.py | 31 ++++++++++++++++++++++--------
tests/test_question_surface_inventory.py   | 25 +++++++++++++++++++++++++
2 files changed, 48 insertions(+), 8 deletions(-)
```

Including this report, total repository diff LOC is larger because this file is the deliverable artifact for Slice 009.

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
59 passed in 51.62s
```

```text
pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
110 passed in 54.56s
```

## Required questions

1. **What responsibilities were previously compressed?**

   Dispatch execution through CLI namespace mutation and production of the `BoundedWorkDispatchResult` were compressed inside `execute_bounded_work_dispatch(...)`.

2. **Which implementation-local ownership boundary became directly observable?**

   The producer-side boundary between performing the dispatch namespace mutation and producing the immutable dispatch-result artifact from the already selected dispatch request.

3. **What producer now owns the recovered responsibility?**

   `bounded_work_dispatch_result_for_request(...)` owns producing the dispatch result artifact.

4. **What artifact or helper carries the recovered boundary, if any?**

   `BoundedWorkDispatchResult` is the artifact, and `bounded_work_dispatch_result_for_request(...)` is the helper carrying the recovered boundary.

5. **Who consumes it?**

   `execute_bounded_work_dispatch(...)` consumes the helper immediately after the existing CLI namespace mutation and returns the result. `apply_bounded_work_dispatch_result(...)` remains the downstream post-dispatch compatibility consumer.

6. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

- Bounded ask orchestration still sequences exact lookup, eligibility, surface-argument validation, refusal, presentation stop-before-dispatch behavior, selection, dispatch request construction, dispatch execution, dispatch-result production, dispatch-result consumption, and message clearing.
- Dispatch execution still owns the existing CLI namespace mutation and does not own answer composition or rendering.
- Message clearing remains inline in `apply_bounded_ask_dispatch(...)` and unchanged.
- Request construction remains owned by `bounded_work_dispatch_request_for_selection(...)` and unchanged.
- Selected surface value and selected dispatch surface production remain separately recovered and unchanged.
- Presentation handoff production and consumption remain separate from this non-presentation dispatch result producer boundary.
