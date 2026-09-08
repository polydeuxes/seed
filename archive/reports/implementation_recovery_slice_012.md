# Implementation Recovery Slice 012

## Selected boundary

Recovered exactly one implementation-local ownership boundary immediately adjacent to the bridge between selected bounded-work invocation construction and request consumption:

```text
BoundedWorkDispatchRequest
↓
apply_bounded_work_dispatch_namespace_update(...)
↓
execute_bounded_work_dispatch(...)
```

The selected boundary is the CLI namespace update for an already-selected bounded-work dispatch request.

## Implementation evidence

Adjacent implementation evidence showed that:

- `BoundedWorkDispatchRequest` already carries the selected `question_family`, `dispatch_surface`, and `surface_value`.
- `bounded_work_dispatch_request_for_selection(...)` already owns construction of that request from a completed selection.
- `bounded_work_dispatch_result_for_request(...)` already owns result production from the request.
- `execute_bounded_work_dispatch(...)` still directly performed the namespace update with `setattr(args, dispatch_request.dispatch_surface, dispatch_request.surface_value)` before producing the existing result.

That left one directly observable local responsibility compressed inside the consumer side of the bridge: applying the selected request surface value to the existing CLI namespace.

## Before

`execute_bounded_work_dispatch(...)` consumed `BoundedWorkDispatchRequest`, directly mutated the CLI namespace, and then delegated result production:

```text
execute_bounded_work_dispatch(...)
  -> setattr(args, dispatch_request.dispatch_surface, dispatch_request.surface_value)
  -> bounded_work_dispatch_result_for_request(dispatch_request)
```

The namespace update was present but did not have its own local ownership boundary.

## After

`apply_bounded_work_dispatch_namespace_update(...)` owns only the existing namespace update and returns the same `BoundedWorkDispatchRequest` for the already-existing result producer:

```text
execute_bounded_work_dispatch(...)
  -> apply_bounded_work_dispatch_namespace_update(args, dispatch_request)
  -> bounded_work_dispatch_result_for_request(applied_request)
```

The behavior is unchanged: the same namespace attribute is set to the same selected surface value, and the same dispatch result is produced.

## Recovered producer

`apply_bounded_work_dispatch_namespace_update(...)` is the recovered producer of the applied request handoff. It owns applying the selected bounded-work surface value to the CLI namespace.

## Recovered artifact/helper

Helper:

```text
apply_bounded_work_dispatch_namespace_update(...)
```

Artifact crossing the recovered boundary:

```text
BoundedWorkDispatchRequest
```

No new dataclass, framework, engine, registry, planner, scheduler, router, universal dispatcher, universal selector, Begin function, or Town Clock was introduced.

## Recovered consumer

`execute_bounded_work_dispatch(...)` consumes the helper immediately before delegating to `bounded_work_dispatch_result_for_request(...)`.

## Compatibility preserved

No compatibility boundary changed.

Public behavior, runtime behavior, CLI behavior, JSON output, diagnostics, schema, and event ledger behavior are preserved.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_012.md`

## LOC changed

Git diff before this report file showed:

```text
seed_runtime/question_surface_inventory.py | 29 ++++++++++++++++++++++++-----
tests/test_question_surface_inventory.py   | 29 +++++++++++++++++++++++++++++
2 files changed, 53 insertions(+), 5 deletions(-)
```

Including this report file, the slice adds the implementation-local helper, one adjacent regression test, and this recovery note.

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
62 passed in 39.48s
```

## Remaining compressed responsibilities

Remaining compressed responsibilities were not reopened. In particular, this slice did not recover or redesign:

- dispatch request construction;
- bounded work selection;
- eligibility;
- exact question-family lookup;
- request consumption beyond the namespace update;
- result construction;
- post-dispatch compatibility handling;
- message clearing;
- rendering;
- answer composition;
- diagnostics;
- schema;
- event ledger;
- semantic routing.

## Required questions

1. **What responsibilities were previously compressed?**

   Request consumption and CLI namespace update were compressed inside `execute_bounded_work_dispatch(...)`, even though result construction had already been delegated.

2. **Which implementation-local ownership boundary became directly observable?**

   The local boundary for applying a selected bounded-work dispatch request's surface value to the CLI namespace became directly observable.

3. **What producer now owns the recovered responsibility?**

   `apply_bounded_work_dispatch_namespace_update(...)` now owns the recovered namespace update responsibility.

4. **What artifact or helper carries the recovered boundary, if any?**

   The helper is `apply_bounded_work_dispatch_namespace_update(...)`; the artifact it consumes and returns is `BoundedWorkDispatchRequest`.

5. **Who consumes it?**

   `execute_bounded_work_dispatch(...)` consumes the helper result immediately before invoking `bounded_work_dispatch_result_for_request(...)`.

6. **Did any compatibility boundary change?**

   No.
