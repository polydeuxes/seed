# Question → Bounded Work Invocation Slice 004

## Selected architectural boundary

```text
BoundedWorkDispatchRequest
        !=
Bounded Work Dispatch
```

Recovered owner:

```text
execute_bounded_work_dispatch(...)
```

Responsibility:

```text
Given a BoundedWorkDispatchRequest and the existing CLI namespace,
perform the existing bounded work invocation.
```

This slice remains inside Question → Bounded Work Invocation. It does not move into Evidence Interpretation or Answer Composition.

## Implementation evidence

Implementation evidence before the slice showed that `BoundedWorkDispatchRequest` already existed as the artifact for an already-selected bounded work invocation, but dispatch execution still happened directly inside `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`.

The mixed code path was:

```text
selection = bounded_work_selection_for_question_family(...)
dispatch_request = bounded_work_dispatch_request_for_selection(selection)
setattr(args, dispatch_request.dispatch_surface, dispatch_request.surface_value)
args.message = []
```

That appeared in both bounded ask execution branches:

1. parameterized bounded work dispatch;
2. non-parameterized bounded work dispatch.

The implementation pressure was therefore not another selection owner and not an answer owner. It was the final namespace mutation step that consumes the dispatch request.

## Before

```text
apply_bounded_ask_dispatch(...)
    -> QuestionFamily lookup
    -> BoundedWorkEligibilityResult
    -> BoundedWorkSelectionResult
    -> BoundedWorkDispatchRequest
    -> setattr(args, dispatch_request.dispatch_surface, dispatch_request.surface_value)
    -> compatibility JSON handling
    -> downstream answer composition/rendering via existing CLI branch
```

`BoundedWorkDispatchRequest` and Dispatch were mixed at the call site. The request artifact existed, but its consumer was an inline `setattr(...)` inside `apply_bounded_ask_dispatch(...)`.

## After

```text
apply_bounded_ask_dispatch(...)
    -> QuestionFamily lookup
    -> BoundedWorkEligibilityResult
    -> BoundedWorkSelectionResult
    -> BoundedWorkDispatchRequest
    -> execute_bounded_work_dispatch(args, dispatch_request)
    -> compatibility JSON handling
    -> downstream answer composition/rendering via existing CLI branch
```

The recovered dispatch owner is intentionally narrow. It performs the existing CLI namespace mutation and returns `BoundedWorkDispatchResult` as an implementation-backed record of the dispatch execution.

## Recovered producer

```text
bounded_work_dispatch_request_for_selection(...)
```

The producer remains the request construction owner recovered in slice 003. It produces the artifact representing an already-selected bounded work invocation.

## Recovered artifact

```text
BoundedWorkDispatchRequest
```

This remains the consumed dispatch artifact.

This slice also adds:

```text
BoundedWorkDispatchResult
```

That result records the performed bounded dispatch surface, value, and question family. It does not become answer composition, rendering, routing, or evidence interpretation.

## Consumer of the artifact

```text
execute_bounded_work_dispatch(args, dispatch_request)
```

The consumer performs the existing bounded work invocation by applying the request to the existing CLI namespace:

```text
setattr(args, dispatch_request.dispatch_surface, dispatch_request.surface_value)
```

## Compatibility preserved

No compatibility boundary changed.

Preserved behavior:

- existing `ask --question-family ...` CLI shape;
- existing exact QuestionFamily matching;
- existing eligibility rejection behavior;
- existing required `--surface-args` validation;
- existing presentation override behavior;
- existing selected dispatch surfaces;
- existing selected dispatch values;
- existing JSON compatibility handling for `knowledge reachability`;
- existing downstream answer composition and rendering paths.

## Files changed

```text
scripts/seed_local.py
seed_runtime/question_surface_inventory.py
tests/test_question_surface_inventory.py
question_bounded_work_invocation_slice_004.md
```

## LOC changed

Implementation/test LOC before this report:

```text
scripts/seed_local.py                         +3 -2
seed_runtime/question_surface_inventory.py   +35 -0
tests/test_question_surface_inventory.py     +24 -0
```

Report LOC:

```text
question_bounded_work_invocation_slice_004.md +253 -0
```

## Tests executed

```text
python -m pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
46 passed in 51.81s
```

Compatibility smoke checks:

```text
python scripts/seed_local.py ask --question-family "knowledge reachability" --json >/tmp/knowledge_reachability.json
python -m json.tool /tmp/knowledge_reachability.json >/dev/null
python scripts/seed_local.py ask --question-family "selection explanation" --surface-args target:one >/tmp/selection_path.txt
```

Result:

```text
all commands exited 0
```

## Remaining compressed Question → Bounded Work Invocation responsibilities

Remaining responsibilities in or adjacent to `apply_bounded_ask_dispatch(...)`:

- exact CLI shape enforcement for bounded ask;
- exact QuestionFamily lookup against the question surface inventory;
- bounded eligibility rejection and error wording;
- required surface-argument validation;
- presentation override short-circuit;
- compatibility-specific JSON handling after dispatch execution;
- handoff to existing downstream answer composition and rendering through the selected CLI branch.

The recovered invocation chain is now:

```text
Question Family

↓

Bounded Work Eligibility

↓

Bounded Work Selection

↓

BoundedWorkDispatchRequest

↓

Bounded Work Dispatch

↓

Surface-local Answer Composition

↓

Rendering
```

Current implementation pressure now appears to terminate naturally at already-existing Answer Composition and compatibility handling rather than requiring another Question → Bounded Work Invocation ownership slice.

## Questions

### 1. Where were `BoundedWorkDispatchRequest` and Dispatch previously mixed?

They were mixed in `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`. The function created `BoundedWorkDispatchRequest` and immediately consumed its `dispatch_surface` and `surface_value` through inline CLI namespace mutation.

### 2. Which recovered architectural boundary became more explicit?

```text
BoundedWorkDispatchRequest != Bounded Work Dispatch
```

The request artifact is now separate from the execution owner that applies it to the CLI namespace.

### 3. What implementation artifact is now produced, and who consumes it?

`bounded_work_dispatch_request_for_selection(...)` produces `BoundedWorkDispatchRequest`.

`execute_bounded_work_dispatch(...)` consumes `BoundedWorkDispatchRequest` and performs the existing namespace mutation.

`execute_bounded_work_dispatch(...)` also produces `BoundedWorkDispatchResult` as a narrow implementation-backed execution record.

### 4. Did implementation evidence suggest a more precise responsibility name?

Yes.

The implementation evidence suggested `execute_bounded_work_dispatch(...)` rather than a generic dispatcher, planner, workflow engine, semantic router, or answer composer. The recovered responsibility is concrete execution of an already-selected bounded work dispatch request.

### 5. Did any compatibility boundary change?

No.
