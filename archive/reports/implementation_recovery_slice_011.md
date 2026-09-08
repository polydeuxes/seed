# Implementation Recovery Slice 011

## Selected boundary

Recovered exactly one adjacent implementation-local ownership boundary:

```text
Post-presentation bounded ask message clearing

!=

QuestionFamily lookup
Eligibility
Surface-argument validation
Presentation handoff production
Presentation handoff consumption
Post-dispatch message clearing
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

The selected boundary is the existing `args.message = []` compatibility mutation that occurs after bounded ask presentation handoff has already been produced and consumed.

## Implementation evidence

Implementation evidence showed two bounded ask presentation branches in `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` performing the same local tail sequence:

```text
presentation handoff production
-> presentation handoff consumption
-> args.message = []
-> return
```

Slice 010 recovered the analogous non-presentation post-dispatch message clearing after dispatch result handoff consumption. The directly adjacent remaining post-dispatch implementation evidence was the presentation-side compatibility cleanup: bounded ask presentation activates the existing question-family explanation surface and then clears the original `ask` message before normal one-shot message handling can continue.

The evidence is intentionally narrow:

- the recovered helper consumes an already applied `BoundedWorkPresentationHandoffResult`;
- it mutates only `args.message`;
- it does not carry dispatch surface, surface value, required surface args, or presentation text ownership beyond the already consumed result;
- it does not handle non-presentation dispatch branches;
- it does not alter JSON compatibility handling for `knowledge reachability`;
- it does not decide lookup, eligibility, required arguments, selection, request construction, dispatch execution, rendering, diagnostics, schema, event ledger, or routing.

## Before

`apply_bounded_ask_dispatch(...)` still directly owned post-presentation message clearing in both presentation branches:

```text
apply_bounded_work_presentation_handoff(args, presentation_handoff)
args.message = []
return
```

That compressed bounded ask orchestration with the final CLI message cleanup required to stop the original `ask` token from continuing into normal message handling after presentation had been handed off.

## After

`clear_bounded_ask_presentation_message(...)` now owns only post-presentation bounded ask message clearing:

```text
presentation_result = apply_bounded_work_presentation_handoff(args, presentation_handoff)
clear_bounded_ask_presentation_message(args, presentation_result)
return
```

`apply_bounded_ask_dispatch(...)` still owns bounded ask orchestration. It still sequences the same lookup, eligibility, required-argument validation, presentation stop-before-dispatch behavior, selection, dispatch request construction, dispatch execution, dispatch result handoff consumption, post-dispatch message clearing, and return behavior.

## Recovered producer

`clear_bounded_ask_presentation_message(...)` is the recovered producer for the post-presentation message-clearing result. It performs the existing compatibility mutation:

```text
args.message = []
```

and returns a narrow `BoundedAskPresentationMessageClearResult`.

## Recovered artifact/helper

Recovered helper/artifact:

```text
clear_bounded_ask_presentation_message(...)
BoundedAskPresentationMessageClearResult
```

The result carries only:

```text
question_family
reason
```

It intentionally does not carry `dispatch_surface`, `surface_value`, `required_surface_args`, bounded status, permission, presentation handoff text, JSON compatibility flags, schema, diagnostics, event-ledger fields, or routing state.

## Recovered consumer

`apply_bounded_ask_dispatch(...)` consumes `clear_bounded_ask_presentation_message(...)` only after:

1. bounded ask presentation handoff has been produced from permitted eligibility;
2. the presentation handoff has been applied to the existing CLI namespace surface;
3. the flow is stopping before bounded work dispatch, preserving existing presentation behavior.

## Compatibility preserved

No.

No public compatibility boundary changed. Runtime behavior, CLI behavior, JSON output, diagnostics, schema, and event-ledger behavior are preserved. The same presentation bounded ask paths still activate the same existing CLI presentation surface and clear `args.message` before normal message handling can run.

## Files changed

- `seed_runtime/question_surface_inventory.py`
  - Added `BoundedAskPresentationMessageClearResult`.
  - Added `clear_bounded_ask_presentation_message(...)`.
- `scripts/seed_local.py`
  - Replaced the two presentation-branch post-handoff `args.message = []` assignments with the recovered helper.
- `tests/test_question_surface_inventory.py`
  - Added focused coverage proving the helper consumes only a presentation handoff result and clears the bounded ask message without absorbing dispatch-surface, surface-value, or required-argument ownership.
- `implementation_recovery_slice_011.md`
  - Recorded the slice evidence and boundary decision.

## LOC changed

Implementation and tests before this report:

```text
3 files changed, 72 insertions(+), 4 deletions(-)
```

Including this report, the final repository diff includes this documentation file as well.

## Tests executed

```text
python -m pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
61 passed in 52.80s
```

## Required questions

### 1. What responsibilities were previously compressed?

Bounded ask orchestration and post-presentation message cleanup were compressed. After presentation handoff consumption, `apply_bounded_ask_dispatch(...)` still directly cleared `args.message` in both presentation branches.

### 2. Which implementation-local ownership boundary became directly observable?

Post-presentation bounded ask message clearing became directly observable as its own implementation-local boundary because it recurred immediately after presentation handoff consumption and before returning from the presentation bounded ask flow.

### 3. What producer now owns the recovered responsibility?

`clear_bounded_ask_presentation_message(...)` now owns the recovered responsibility.

### 4. What artifact or helper carries the recovered boundary, if any?

`BoundedAskPresentationMessageClearResult` carries the recovered boundary. It records only `question_family` and a local `reason`.

### 5. Who consumes it?

`apply_bounded_ask_dispatch(...)` consumes the helper after bounded work presentation handoff production and consumption.

### 6. Did any compatibility boundary change?

No.

## Remaining compressed responsibilities

- Bounded ask orchestration still sequences exact lookup, eligibility, required surface-argument validation, refusal, presentation stop-before-dispatch behavior, selection, dispatch request construction, dispatch execution, dispatch result handoff consumption, post-dispatch message clearing, post-presentation message clearing, and returns.
- QuestionFamily lookup, bounded eligibility, surface argument validation, selected surface production, selected surface value production, presentation handoff production, presentation handoff consumption, dispatch request production, dispatch execution, dispatch result production, dispatch result handoff consumption, post-dispatch message clearing, and post-presentation message clearing remain separate from each other.
- Rendering, diagnostics, schema, event-ledger writes, and semantic routing remain untouched.
