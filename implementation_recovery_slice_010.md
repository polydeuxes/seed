# Implementation Recovery Slice 010

## Selected boundary

Recovered exactly one adjacent implementation-local ownership boundary:

```text
Post-dispatch bounded ask message clearing

!=

QuestionFamily lookup
Eligibility
Surface-argument validation
Presentation handoff
Selection
Dispatch request construction
Dispatch execution
Dispatch result production
Dispatch result handoff consumption
Rendering
Diagnostics
Schema
Event Ledger
Routing
```

The selected boundary is the existing `args.message = []` compatibility mutation that occurs after non-presentation bounded ask dispatch has already executed and the dispatch result handoff has already been consumed.

## Implementation evidence

Implementation evidence showed two non-presentation bounded ask branches in `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` performing the same local tail sequence:

```text
selection
-> dispatch request construction
-> dispatch execution
-> dispatch result handoff consumption
-> args.message = []
-> return / function exit
```

The immediately preceding slices had already exposed dispatch request production, dispatch result production, and dispatch result handoff consumption. The next directly adjacent recurring compressed responsibility was not another dispatch decision; it was the final bounded ask compatibility cleanup that clears the original `ask` message after the selected existing CLI surface has been activated.

The evidence is intentionally narrow:

- the recovered helper consumes an already produced `BoundedWorkDispatchResult`;
- it mutates only `args.message`;
- it does not carry dispatch surface or surface value;
- it does not handle presentation branches;
- it does not alter JSON compatibility handling for `knowledge reachability`;
- it does not decide lookup, eligibility, required arguments, selection, request construction, dispatch execution, rendering, diagnostics, schema, event ledger, or routing.

## Before

`apply_bounded_ask_dispatch(...)` still directly owned post-dispatch message clearing in both non-presentation dispatch branches:

```text
apply_bounded_work_dispatch_result(args, dispatch_result)
args.message = []
```

That compressed bounded ask orchestration with the final CLI message cleanup required to prevent the original `ask` token from continuing into normal one-shot message handling.

## After

`clear_bounded_ask_dispatch_message(...)` now owns only post-dispatch bounded ask message clearing:

```text
apply_bounded_work_dispatch_result(args, dispatch_result)
clear_bounded_ask_dispatch_message(args, dispatch_result)
```

`apply_bounded_ask_dispatch(...)` still owns bounded ask orchestration. It still sequences the same lookup, eligibility, required-argument validation, presentation stop-before-dispatch behavior, selection, dispatch request construction, dispatch execution, dispatch result handoff consumption, and return behavior.

## Recovered producer

`clear_bounded_ask_dispatch_message(...)` is the recovered producer for the post-dispatch message-clearing result. It performs the existing compatibility mutation:

```text
args.message = []
```

and returns a narrow `BoundedAskDispatchMessageClearResult`.

## Recovered artifact/helper

Recovered helper/artifact:

```text
clear_bounded_ask_dispatch_message(...)
BoundedAskDispatchMessageClearResult
```

The result carries only:

```text
question_family
reason
```

It intentionally does not carry `dispatch_surface`, `surface_value`, `required_surface_args`, bounded status, permission, presentation handoff, JSON compatibility flags, schema, diagnostics, event-ledger fields, or routing state.

## Recovered consumer

`apply_bounded_ask_dispatch(...)` consumes `clear_bounded_ask_dispatch_message(...)` only after:

1. selected bounded work has been converted to a dispatch request;
2. dispatch execution has mutated the selected existing CLI namespace surface;
3. dispatch result handoff consumption has preserved existing compatibility behavior.

## Compatibility preserved

No.

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, diagnostics, schema, and event-ledger behavior are preserved. The same non-presentation bounded ask paths still activate the same existing CLI surfaces and clear `args.message` before normal message handling can run.

## Files changed

- `seed_runtime/question_surface_inventory.py`
  - Added `BoundedAskDispatchMessageClearResult`.
  - Added `clear_bounded_ask_dispatch_message(...)`.
- `scripts/seed_local.py`
  - Replaced the two non-presentation post-dispatch `args.message = []` assignments with the recovered helper.
- `tests/test_question_surface_inventory.py`
  - Added focused coverage proving the helper consumes only a dispatch result and clears the bounded ask message without absorbing dispatch-surface, surface-value, or required-argument ownership.
- `implementation_recovery_slice_010.md`
  - Recorded the slice evidence and boundary decision.

## LOC changed

Implementation and tests before this report:

```text
3 files changed, 60 insertions(+), 2 deletions(-)
```

Including this report, the final repository diff includes this documentation file as well.

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
60 passed
```

## Required questions

### 1. What responsibilities were previously compressed?

Bounded ask orchestration and post-dispatch message cleanup were compressed. After dispatch result handoff consumption, `apply_bounded_ask_dispatch(...)` still directly cleared `args.message` in both non-presentation dispatch branches.

### 2. Which implementation-local ownership boundary became directly observable?

Post-dispatch bounded ask message clearing became directly observable as its own implementation-local boundary because it recurred immediately after dispatch result handoff consumption and before returning from the non-presentation bounded ask flow.

### 3. What producer now owns the recovered responsibility?

`clear_bounded_ask_dispatch_message(...)` now owns the recovered responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`BoundedAskDispatchMessageClearResult` carries the recovered boundary. It records only `question_family` and a local `reason`.

### 5. Who consumes it?

`apply_bounded_ask_dispatch(...)` consumes the helper after dispatch execution and dispatch result handoff consumption.

### 6. Did any compatibility boundary change?

No.

## Remaining compressed responsibilities

- Bounded ask orchestration still sequences exact lookup, eligibility, required surface-argument validation, refusal, presentation stop-before-dispatch behavior, selection, dispatch request construction, dispatch execution, dispatch result handoff consumption, post-dispatch message clearing, and returns.
- Presentation branch message clearing remains unchanged and intentionally outside this slice.
- QuestionFamily lookup, bounded eligibility, surface argument validation, selected surface production, selected surface value production, dispatch request production, dispatch execution, dispatch result production, dispatch result handoff consumption, and presentation handoff consumption remain separate from this recovered post-dispatch message-clearing boundary.
- Rendering, diagnostics, schema, event-ledger writes, and semantic routing remain untouched.
