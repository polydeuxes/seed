# Question → Bounded Work Invocation Slice 001

## Selected architectural boundary

Recovered boundary: **Bounded Work Eligibility for an exact QuestionFamily**.

The recovered owner answers only:

```text
Given this exact QuestionFamily, is bounded work permitted to execute?
```

It remains inside the existing Question → Bounded Work Invocation responsibility and does not select a surface, dispatch work, mutate CLI arguments, compose answers, render output, or route free text.

## Implementation evidence

Implementation evidence before this slice showed bounded ask runtime behavior using:

- exact QuestionFamily lookup from `build_question_surface_inventory(...)`;
- bounded status derived by `bounded_status_for_question_family(...)`;
- required-argument metadata from `BOUNDED_ASK_REQUIRED_SURFACE_ARGS`;
- dispatchability metadata from `BOUNDED_ASK_DISPATCH_SURFACES`;
- diagnostic-only metadata from `BOUNDED_ASK_DIAGNOSTIC_ONLY_FAMILIES`;
- CLI mutation inside `apply_bounded_ask_dispatch(...)`.

This slice keeps `bounded_status_for_question_family(...)` as status derivation and adds a named artifact around the existing permission decision.

## Before

Question Family resolution and Bounded Work Eligibility were mixed in `apply_bounded_ask_dispatch(...)`.

The function:

1. validated the invocation shape;
2. checked whether the exact family existed in `build_question_surface_inventory(...)`;
3. derived bounded status;
4. rejected non-permitted statuses;
5. validated required surface args;
6. selected the mapped surface;
7. mutated the parsed CLI namespace.

That compressed QuestionFamily resolution, eligibility, required-argument permission checks, surface selection, and dispatch mutation in one runtime owner.

## After

`bounded_work_eligibility_for_question_family(...)` now produces a `BoundedWorkEligibilityResult` for the exact QuestionFamily.

`apply_bounded_ask_dispatch(...)` consumes that artifact for permission decisions and required-argument count, while it continues to own surface selection and CLI argument mutation.

## Recovered producer

Producer: `bounded_work_eligibility_for_question_family(question_family)`.

The producer consumes implementation-backed status and metadata only:

- exact QuestionFamily;
- `bounded_status_for_question_family(...)`;
- required surface argument metadata;
- diagnostic-only and dispatchability metadata through the bounded status derivation.

## Recovered artifact

Artifact: `BoundedWorkEligibilityResult`.

Fields:

- `question_family`;
- `bounded_status`;
- `permitted`;
- `required_surface_args`;
- `reason`.

The artifact intentionally does **not** carry a dispatch surface. The test coverage asserts that surface selection did not move into eligibility.

## Consumer of the artifact

Consumer: `apply_bounded_ask_dispatch(...)`.

It uses the artifact to:

- reject `--surface-args` for currently parameterless eligible families;
- require exact `--surface-args` for parameterized eligible families;
- reject diagnostic-only families;
- reject not-dispatchable families.

It still performs the existing compatibility handoff to the selected surface after eligibility has allowed execution.

## Compatibility preserved

No compatibility boundary changed.

The CLI remains an exact QuestionFamily invocation mechanism. It still rejects unknown families, free-text routing misuse, diagnostic-only families, not-dispatchable families, missing required surface args, extra required surface args, and direct surface args outside eligible parameterized families.

## Answers to requested questions

### 1. Where were Question Family resolution and Bounded Work Eligibility previously mixed?

They were mixed in `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`, where exact family lookup against `build_question_surface_inventory(...)`, bounded status derivation, required-argument validation, rejection handling, surface selection, and CLI namespace mutation all occurred together.

### 2. Which recovered architectural boundary became more explicit?

The boundary between **Question Family** and **Bounded Work Eligibility** became explicit.

### 3. What implementation artifact is now produced, and who consumes it?

`seed_runtime/question_surface_inventory.py` now produces `BoundedWorkEligibilityResult` through `bounded_work_eligibility_for_question_family(...)`. `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` consumes it.

### 4. Did implementation evidence suggest a more precise responsibility name?

Insufficient implementation evidence.

### 5. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `question_bounded_work_invocation_slice_001.md`

## LOC changed

Current diff stat at report time:

```text
scripts/seed_local.py                      | 15 ++++++-------
seed_runtime/question_surface_inventory.py | 36 ++++++++++++++++++++++++++++++
tests/test_question_surface_inventory.py   | 29 ++++++++++++++++++++++++
3 files changed, 72 insertions(+), 8 deletions(-)
```

This report file is additional documentation for the requested deliverable.

## Tests executed

- `pytest -q tests/test_question_surface_inventory.py` → passed, 42 tests.
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` → passed, 44 tests.
- `pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` → passed, 86 tests.

## Remaining compressed Question → Bounded Work Invocation responsibilities

The remaining compressed responsibilities now belong to later owners and were intentionally not recovered in this slice:

- exact QuestionFamily existence lookup in the runtime dispatch adapter;
- existing surface selection from `BOUNDED_ASK_DISPATCH_SURFACES`;
- presentation override handling;
- CLI namespace mutation;
- compatibility JSON special-casing for `knowledge reachability`;
- surface-local answer composition;
- rendering.

Stop condition: the next implementation pressure is surface selection/dispatch compatibility, not Bounded Work Eligibility.
