# Question → Bounded Work Invocation Slice 002

## Selected architectural boundary

Recovered boundary:

```text
Bounded Work Eligibility
    !=
Bounded Work Selection
```

The recovered owner remains entirely inside Question → Bounded Work Invocation. It answers only:

```text
Given an eligible exact QuestionFamily,
which existing bounded work should be selected?
```

It does not own eligibility decisions, evidence sufficiency, observation interpretation, fact readiness, dispatch execution, CLI namespace mutation, answer composition, rendering, semantic routing, or free-text classification.

## Implementation evidence

Implementation evidence showed that `bounded_work_eligibility_for_question_family(...)` already produced a permission-only `BoundedWorkEligibilityResult`, while `apply_bounded_ask_dispatch(...)` still selected the dispatch surface and selected the value to place on that surface.

Before this slice, `apply_bounded_ask_dispatch(...)` directly consumed:

- `BOUNDED_ASK_DISPATCH_SURFACES[family]` to choose the target bounded work surface;
- `BOUNDED_ASK_ARG_VALUES.get(family, True)` to choose the default bounded work value for eligible-now families;
- parameterized `--surface-args` to choose the bounded work value for eligible-with-parameters families.

That meant eligibility and selection had been partially separated, but bounded work selection still lived inside the dispatch adapter.

## Before

```text
bounded_work_eligibility_for_question_family(...)
    -> BoundedWorkEligibilityResult

apply_bounded_ask_dispatch(...)
    -> validates exact ask shape
    -> validates known QuestionFamily
    -> consumes eligibility
    -> validates required surface args
    -> selects dispatch surface
    -> selects dispatch value
    -> mutates CLI namespace
```

## After

```text
bounded_work_eligibility_for_question_family(...)
    -> BoundedWorkEligibilityResult

bounded_work_selection_for_question_family(...)
    -> BoundedWorkSelectionResult

apply_bounded_ask_dispatch(...)
    -> validates exact ask shape
    -> validates known QuestionFamily
    -> consumes eligibility
    -> validates required surface args
    -> consumes selection
    -> mutates CLI namespace
```

## Recovered producer

Producer:

```text
bounded_work_selection_for_question_family(question_family, eligibility, surface_args=None)
```

The producer requires an exact `QuestionFamily` and a permitted `BoundedWorkEligibilityResult`. It rejects mismatched or non-permitted eligibility inputs rather than making eligibility decisions itself.

## Recovered artifact

Artifact:

```text
BoundedWorkSelectionResult
```

Fields:

- `question_family`
- `dispatch_surface`
- `surface_value`
- `required_surface_args`
- `reason`

The artifact intentionally does not carry `permitted` or `bounded_status`; those remain owned by `BoundedWorkEligibilityResult`.

## Consumer of the artifact

Consumer:

```text
scripts/seed_local.py::apply_bounded_ask_dispatch(...)
```

The dispatch adapter now consumes `BoundedWorkSelectionResult.dispatch_surface` and `BoundedWorkSelectionResult.surface_value` when mutating the parsed CLI namespace.

## Compatibility preserved

No compatibility boundary changed.

CLI shape, exact QuestionFamily requirements, unknown-family errors, diagnostic-only rejection, required `--surface-args` validation, parameter forwarding, special JSON behavior for knowledge reachability, inventory JSON shape, diagnostic inventory behavior, diagnostic shape-audit behavior, answer composition, and rendering are preserved.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `question_bounded_work_invocation_slice_002.md`

## LOC changed

Code/test diff before this report:

```text
3 files changed, 117 insertions(+), 9 deletions(-)
```

This report adds one markdown deliverable file.

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
python scripts/seed_local.py ask --question-family "observation domain coverage" --json | head -n 20
python scripts/seed_local.py ask --question-family "selection explanation" --surface-args target:one --json | head -n 20
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Observed results:

- `tests/test_question_surface_inventory.py`: 44 passed.
- app command for `observation domain coverage`: rendered JSON through the selected existing surface.
- app command for `selection explanation`: rendered JSON through the selected existing parameterized surface.
- diagnostic inventory and shape-audit tests: 44 passed.

## Acceptance notes

- Exactly one implementation-local ownership boundary became directly observable: Bounded Work Selection.
- The recovered boundary follows the established producer → artifact → consumer pattern.
- Behavior is unchanged; selection is the existing static map-backed decision.
- Compatibility is preserved.
- Evidence Interpretation remains independent and upstream.
- Question → Bounded Work Invocation continues to model only invocation decisions, not evidence semantics.

## Required questions

### 1. Where were Bounded Work Eligibility and Bounded Work Selection previously mixed?

They were previously mixed in `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` after the eligibility slice. The function consumed `BoundedWorkEligibilityResult`, but still selected the bounded work dispatch surface and selected the CLI surface value before mutating the namespace.

### 2. Which recovered architectural boundary became more explicit?

```text
Bounded Work Eligibility
    !=
Bounded Work Selection
```

Eligibility now produces permission and required-argument metadata. Selection now produces the chosen existing bounded work target and selected value for an already eligible exact `QuestionFamily`.

### 3. What implementation artifact is now produced, and who consumes it?

`seed_runtime/question_surface_inventory.py` now produces `BoundedWorkSelectionResult` through `bounded_work_selection_for_question_family(...)`.

`scripts/seed_local.py::apply_bounded_ask_dispatch(...)` consumes that artifact.

### 4. Did implementation evidence suggest a more precise responsibility name?

Yes. Implementation evidence supported `Bounded Work Selection`: the recovered code chooses a static dispatch surface and selected surface value for an eligible exact `QuestionFamily`. It does not perform generic dispatch or routing.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed Question → Bounded Work Invocation responsibilities

Remaining compressed responsibilities still inside `apply_bounded_ask_dispatch(...)` or adjacent CLI code:

- exact `ask --question-family` invocation-shape enforcement;
- exact known-QuestionFamily validation against `build_question_surface_inventory(...)`;
- required `--surface-args` count validation;
- presentation-mode diversion to question-family explanation;
- CLI namespace mutation for the selected bounded work;
- special JSON compatibility handling for knowledge reachability;
- final clearing of `args.message` after bounded ask handling.

The next slice should continue only if implementation pressure remains within Question → Bounded Work Invocation. If the pressure shifts toward observation, evidence, fact readiness, answer composition, rendering, semantic routing, or free-text classification, this responsibility family should stop.
