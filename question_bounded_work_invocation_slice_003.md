# Question → Bounded Work Invocation Slice 003

## Selected architectural boundary

```text
Bounded Work Selection
        !=
Dispatch
```

This slice recovers exactly one implementation-local ownership boundary inside Question → Bounded Work Invocation:

```text
Given the selected bounded work,
how is that existing bounded work invoked?
```

The recovered owner is `BoundedWorkDispatchRequest`, produced by `bounded_work_dispatch_request_for_selection(...)`.

## Implementation evidence

Implementation evidence showed that `BoundedWorkSelectionResult` already carried the selected bounded work surface and selected surface value for an eligible exact `QuestionFamily`. However, `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` still consumed those selection fields directly when mutating the CLI namespace with `setattr(...)`.

The strongest recurring implementation-local pressure was not a new planner, workflow engine, semantic router, or evidence interpreter. It was the repeated local act of taking selected bounded work and invoking the existing CLI surface by writing the selected value to the selected dispatch surface attribute.

## Before

```text
bounded_work_selection_for_question_family(...)
    -> BoundedWorkSelectionResult

apply_bounded_ask_dispatch(...)
    -> reads selection.dispatch_surface
    -> reads selection.surface_value
    -> mutates argparse namespace with setattr(...)
```

Selection and dispatch invocation were adjacent but still mixed at the `apply_bounded_ask_dispatch(...)` call site.

## After

```text
bounded_work_selection_for_question_family(...)
    -> BoundedWorkSelectionResult

bounded_work_dispatch_request_for_selection(selection)
    -> BoundedWorkDispatchRequest

apply_bounded_ask_dispatch(...)
    -> consumes BoundedWorkDispatchRequest
    -> mutates argparse namespace with the request's dispatch surface and value
```

The dispatch request owns only the existing invocation shape:

- exact `question_family` already selected upstream;
- existing `dispatch_surface` attribute name;
- existing `surface_value` to place on that attribute;
- local reason explaining that selected bounded work is dispatched through the existing CLI namespace.

It does not own QuestionFamily lookup, bounded work eligibility, bounded work selection, evidence interpretation, answer composition, rendering, semantic routing, or free-text classification.

## Recovered producer

`bounded_work_dispatch_request_for_selection(...)` produces a dispatch request from an already selected `BoundedWorkSelectionResult`.

## Recovered artifact

`BoundedWorkDispatchRequest` is the recovered artifact.

It is intentionally smaller than selection. It does not carry `required_surface_args`, `bounded_status`, or `permitted`; those remain upstream eligibility/selection concerns.

## Consumer of the artifact

`scripts/seed_local.py::apply_bounded_ask_dispatch(...)` consumes `BoundedWorkDispatchRequest` and performs the existing namespace mutation with `setattr(args, dispatch_request.dispatch_surface, dispatch_request.surface_value)`.

## Compatibility preserved

No compatibility boundary changed.

Behavior, CLI compatibility, dispatch surfaces, answer composition, rendering, JSON behavior, tests, and existing bounded ask semantics remain unchanged.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `question_bounded_work_invocation_slice_003.md`

## LOC changed

Final staged repository diff:

```text
4 files changed, 214 insertions(+), 3 deletions(-)
```

Per-file numstat:

```text
161	0	question_bounded_work_invocation_slice_003.md
5	2	scripts/seed_local.py
28	0	seed_runtime/question_surface_inventory.py
20	1	tests/test_question_surface_inventory.py
```

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
45 passed
```

## Answers to requested questions

### 1. Where were Bounded Work Selection and Dispatch previously mixed?

They were mixed in `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`. After `bounded_work_selection_for_question_family(...)` produced `BoundedWorkSelectionResult`, the dispatch adapter still read `selection.dispatch_surface` and `selection.surface_value` directly and used them to mutate the parsed CLI namespace.

### 2. Which recovered architectural boundary became more explicit?

```text
Bounded Work Selection
        !=
Dispatch
```

Selection now produces selected bounded work. Dispatch request production now states how that already selected bounded work is invoked through the existing CLI namespace.

### 3. What implementation artifact is now produced, and who consumes it?

`bounded_work_dispatch_request_for_selection(...)` now produces `BoundedWorkDispatchRequest`.

`scripts/seed_local.py::apply_bounded_ask_dispatch(...)` consumes that artifact.

### 4. Did implementation evidence suggest a more precise responsibility name?

Yes. The implementation evidence suggested `BoundedWorkDispatchRequest` rather than a generic dispatcher. The recovered responsibility is not dispatch planning or routing; it is the concrete invocation request for already selected bounded work.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed Question → Bounded Work Invocation responsibilities

Remaining implementation pressure still inside or adjacent to `apply_bounded_ask_dispatch(...)`:

- exact `ask --question-family ...` command-shape validation;
- unknown QuestionFamily rejection against question surface inventory;
- bounded work eligibility error presentation;
- parameter count enforcement for parameterized bounded work;
- presentation-mode handoff to question family explanation;
- CLI namespace mutation as the final dispatch side effect;
- special JSON compatibility handling for `knowledge reachability`.

Evidence Interpretation remains independent and upstream. This slice did not introduce evidence readiness, observation interpretation, fact interpretation, authority carried by observations, semantic routing, or free-text classification.
