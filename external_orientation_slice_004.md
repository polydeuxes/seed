# external_orientation_slice_004

## Selected implementation boundary

Question Family Text Intake != Bounded Work Eligibility.

This slice recovers only the implementation-local owner that prepares externally supplied, exact question-family text for the bounded eligibility input used by existing question-surface behavior.

## Implementation evidence

Before this slice, `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` directly:

1. read `args.question_family`;
2. built the known inventory-family set;
3. rejected unknown text;
4. immediately called bounded work eligibility; and
5. continued into surface-argument validation, presentation handling, selection, dispatch request construction, and dispatch execution.

`seed_runtime/question_surface_inventory.py` now contains a private, narrow preparation helper and private handoff artifact:

- `_QuestionFamilyEligibilityInput` carries only `question_family`.
- `_prepare_question_family_eligibility_input(...)` admits only exact inventory-backed question-family text and returns that input.
- `_bounded_work_eligibility_for_prepared_question_family(...)` consumes the prepared input to produce the existing `BoundedWorkEligibilityResult`.

Focused tests prove the prepared handoff carries only prepared input and does not absorb dispatch, rendering, public result shape, bounded status, or permission ownership.

## Before

Question-family text intake and bounded eligibility were compressed in `apply_bounded_ask_dispatch(...)`: the CLI adapter validated the externally supplied family text against inventory rows and immediately evaluated bounded eligibility in the same local flow that also handles presentation, selection, and dispatch.

## After

External question-family text preparation is directly observable as a private implementation-local boundary in `seed_runtime/question_surface_inventory.py`. The CLI adapter still owns bounded ask orchestration, but it now asks the question-surface inventory module to prepare exact family text before eligibility evaluation.

## Recovered producer

`_prepare_question_family_eligibility_input(...)` produces the prepared bounded eligibility input from externally supplied exact question-family text.

## Recovered artifact/helper, if any

`_QuestionFamilyEligibilityInput` is the recovered private artifact. It carries only:

- `question_family`

It intentionally does not carry dispatch surface, surface value, required surface args, bounded status, permission, rendering, presentation, JSON shape, event, ledger, or diagnostic ownership.

## Consumer

`_bounded_work_eligibility_for_prepared_question_family(...)` consumes `_QuestionFamilyEligibilityInput` and returns the existing `BoundedWorkEligibilityResult` shape. `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` consumes the same eligibility result as before for the existing bounded ask behavior.

## Compatibility preserved

Yes.

No compatibility boundary changed. Public CLI behavior, JSON shape, schemas, events, ledgers, diagnostic inventory, inquiry orientation, source navigation, pressure audit, and runtime behavior were preserved.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `external_orientation_slice_004.md`

## LOC changed

Implementation/test/report delta at the time of this report:

- `scripts/seed_local.py`: 11 insertions, 7 deletions
- `seed_runtime/question_surface_inventory.py`: 45 insertions, 3 deletions
- `tests/test_question_surface_inventory.py`: 28 insertions
- `external_orientation_slice_004.md`: 110 insertion new report file

## Tests executed

- `python -m pytest -q tests/test_question_surface_inventory.py` — passed, 48 tests.

## Remaining compressed External Orientation responsibilities

Remaining compression intentionally not recovered in this slice:

- free-form question interpretation is still not implemented;
- generic Orientation is still not implemented;
- no orientation framework, registry, taxonomy, engine, planner, scheduler, routing framework, or source classifier exists;
- bounded ask presentation handling remains in `apply_bounded_ask_dispatch(...)`;
- bounded ask surface-argument validation remains in `apply_bounded_ask_dispatch(...)`;
- bounded work selection remains separate in `bounded_work_selection_for_question_family(...)`;
- dispatch request construction and dispatch execution remain separate from this recovered intake-to-eligibility handoff;
- question-surface inventory remains static and implementation-backed.

## Required questions

### 1. Where were Question Family Text Intake and Bounded Work Eligibility previously mixed?

They were mixed in `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`, where `args.question_family` was read, checked against `build_question_surface_inventory()`, and immediately passed into bounded eligibility before the same function continued with presentation, selection, and dispatch flow.

### 2. Which implementation-local boundary became directly observable?

The private boundary between externally supplied exact QuestionFamily text intake and bounded work eligibility input preparation became directly observable.

### 3. What private artifact or helper now carries the handoff, if any?

`_QuestionFamilyEligibilityInput` carries the handoff. `_prepare_question_family_eligibility_input(...)` produces it.

### 4. Who consumes that artifact/helper?

`_bounded_work_eligibility_for_prepared_question_family(...)` consumes `_QuestionFamilyEligibilityInput`. The existing CLI adapter consumes the resulting `BoundedWorkEligibilityResult` as before.

### 5. Did any compatibility boundary change?

No.
