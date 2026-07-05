# Implementation Recovery Slice 002 — Bounded Surface Argument Satisfaction Boundary

## Selected boundary

This slice recovers the implementation-local boundary for **bounded surface argument satisfaction for eligible exact QuestionFamily invocation**.

The boundary is intentionally narrow: after exact QuestionFamily lookup and bounded work eligibility have already admitted a permitted family, it validates whether the operator-provided `--surface-args` match the existing implementation-backed required surface-argument contract. It does not own exact lookup, eligibility, diagnostic-only refusal, not-dispatchable refusal, dispatch surface selection, dispatch execution, presentation, rendering, JSON shape, schema, diagnostics, event ledger behavior, or cluster mutation.

## Implementation evidence

Implementation evidence immediately adjacent to Slice 001 showed the bounded ask path still carrying separate responsibilities in one runtime adapter:

1. exact QuestionFamily lookup was recovered in Slice 001;
2. bounded work eligibility was already an explicit result;
3. `apply_bounded_ask_dispatch(...)` still owned the `--surface-args` admission rules for both `eligible_now` and `eligible_with_parameters` families;
4. `bounded_work_selection_for_question_family(...)` consumed raw surface args for parameterized families while also selecting the dispatch surface and selected value;
5. existing maps already identified required argument names through `BOUNDED_ASK_REQUIRED_SURFACE_ARGS`;
6. the CLI compatibility messages for missing, extra, or disallowed `--surface-args` were already implementation-backed.

The smallest adjacent recurring responsibility was not dispatch selection itself. It was the narrower pre-selection question:

```text
For this already eligible exact QuestionFamily, are the supplied operator surface args satisfied?
```

## Before

Surface-argument satisfaction was compressed across the CLI bounded ask adapter and bounded work selection:

- `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` rejected `--surface-args` for `eligible_now` families.
- The same function counted required args for `eligible_with_parameters` families.
- The same function emitted the compatibility errors for missing and extra values.
- The same function passed raw tuples into `bounded_work_selection_for_question_family(...)`.
- `bounded_work_selection_for_question_family(...)` then interpreted those raw tuples while also selecting the dispatch surface and selected surface value.

That compression made required-argument satisfaction less observable than exact lookup, eligibility, selected bounded work, dispatch request construction, and dispatch execution.

## After

Surface-argument satisfaction is directly observable as a private implementation handoff:

- `BoundedWorkSurfaceArgsResult` carries validated operator surface args plus the required argument names from eligibility.
- `bounded_work_surface_args_for_eligibility(...)` owns the existing validation rules for permitted `eligible_now` and `eligible_with_parameters` families.
- `apply_bounded_ask_dispatch(...)` consumes the validation helper and keeps the same `parser.error(...)` behavior by forwarding the same message text.
- `bounded_work_selection_for_question_family(...)` now consumes the validated surface-args result for parameterized selection.

## Recovered producer

`seed_runtime/question_surface_inventory.py::bounded_work_surface_args_for_eligibility(...)` now owns the recovered surface-argument satisfaction responsibility.

The producer consumes only:

- exact `question_family` text already admitted upstream;
- `BoundedWorkEligibilityResult` already produced upstream;
- optional operator-supplied `surface_args` from the existing CLI path.

## Recovered artifact/helper

`seed_runtime/question_surface_inventory.py::BoundedWorkSurfaceArgsResult` carries the recovered boundary.

It carries only:

- `question_family`;
- validated `surface_args`;
- `required_surface_args`;
- a local implementation reason.

It intentionally does not carry:

- bounded eligibility permission;
- bounded status ownership;
- dispatch surface;
- selected surface value;
- CLI namespace mutation;
- presentation flags;
- rendered output;
- JSON output;
- event or cluster mutation data.

## Recovered consumer

Two existing implementation-local consumers now consume the recovered handoff:

- `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` consumes the helper result before presentation or dispatch selection.
- `seed_runtime/question_surface_inventory.py::bounded_work_selection_for_question_family(...)` consumes `BoundedWorkSurfaceArgsResult` when constructing parameterized selected bounded work.

## Required questions

1. **What responsibilities were previously compressed?**

   Required surface-argument validation, missing-value refusal, extra-value refusal, disallowed-argument refusal, dispatch surface selection, selected surface-value construction, and CLI namespace mutation were adjacent in the same bounded ask flow.

2. **Which implementation-local ownership boundary became directly observable?**

   Bounded surface argument satisfaction for already eligible exact QuestionFamily invocation became directly observable.

3. **What producer now owns the recovered responsibility?**

   `bounded_work_surface_args_for_eligibility(...)` owns the recovered responsibility.

4. **What artifact or helper carries the recovered boundary, if any?**

   `BoundedWorkSurfaceArgsResult` carries the recovered boundary.

5. **Who consumes it?**

   `apply_bounded_ask_dispatch(...)` consumes the helper result for CLI compatibility handling, and `bounded_work_selection_for_question_family(...)` consumes the artifact for parameterized bounded work selection.

6. **Did any compatibility boundary change?**

   No.

## Compatibility preserved

No public compatibility boundary changed.

- Public CLI behavior is unchanged.
- The existing `--surface-args` error messages are preserved.
- JSON output is unchanged.
- Diagnostic output is unchanged.
- Schema is unchanged.
- Event ledger behavior is unchanged.
- Runtime mutation behavior is unchanged.
- No new diagnostic, audit, probe, operational CLI flag, or recordable output was introduced.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_002.md`

## LOC changed

Implementation/test change before this report:

```text
scripts/seed_local.py                      | 34 +++++++---------
seed_runtime/question_surface_inventory.py | 65 +++++++++++++++++++++++++++++-
tests/test_question_surface_inventory.py   | 48 +++++++++++++++++++++-
3 files changed, 125 insertions(+), 22 deletions(-)
```

This report file is additional documentation for the requested deliverable.

## Tests executed

- `pytest -q tests/test_question_surface_inventory.py` — passed, 51 tests.
- `python scripts/seed_local.py --question-surface-inventory --json >/tmp/question_inventory.json` — passed; exercised the app's question-surface inventory.
- `python scripts/seed_local.py ask --question-family "selection explanation" --surface-args implementation_recovery --json >/tmp/selection_ask.json` — passed; exercised the app's bounded ask path for the selected selection surface.
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 51 tests.

## Remaining compressed responsibilities

This slice intentionally leaves these neighboring responsibilities compressed or only partially separated because recovering them would exceed exactly one implementation-local ownership boundary:

- diagnostic-only refusal ownership;
- not-dispatchable refusal ownership;
- selected / non-selected visibility ownership in `selection_path_audit`;
- exact dispatch surface selection beyond the already existing bounded work selection helper;
- dispatch request and CLI mutation beyond the already existing dispatch request/result helpers;
- presentation override handling;
- compatibility JSON special-casing for `knowledge reachability`;
- surface-local answer composition;
- rendering;
- broader Question Shape recovery.

No framework, engine, registry, dispatcher, scheduler, planner, router, universal selector, Begin function, or Town Clock was introduced.
