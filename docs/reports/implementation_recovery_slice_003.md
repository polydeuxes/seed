# Implementation Recovery Slice 003 — Bounded Ask Refusal Boundary

## Selected boundary

This slice recovers the implementation-local boundary for **bounded ask refusal for non-permitted exact QuestionFamily invocation**.

The boundary is intentionally narrow: after exact QuestionFamily lookup and bounded work eligibility have already classified a family as non-permitted, it preserves the existing refusal message and local refusal reason. It does not own exact lookup, eligibility classification, surface-argument satisfaction, selected bounded work, dispatch request construction, dispatch execution, presentation, rendering, JSON shape, schema, diagnostics, event ledger behavior, or cluster mutation.

## Implementation evidence

Implementation evidence immediately adjacent to the recovered Selection implementation showed that `apply_bounded_ask_dispatch(...)` still carried one local non-selection responsibility after eligibility:

1. exact QuestionFamily lookup is already owned by `_lookup_exact_question_family(...)` and `_prepare_question_family_eligibility_input(...)`;
2. bounded work eligibility is already owned by `_bounded_work_eligibility_for_prepared_question_family(...)`;
3. surface-argument satisfaction is already owned by `bounded_work_surface_args_for_eligibility(...)`;
4. selected bounded work is already owned by `bounded_work_selection_for_question_family(...)`;
5. dispatch request preparation is already owned by `bounded_work_dispatch_request_for_selection(...)`;
6. dispatch execution is already owned by `execute_bounded_work_dispatch(...)`;
7. the CLI adapter still embedded the refusal messages for `diagnostic_only` and `not_dispatchable` eligible-but-non-permitted families.

The smallest adjacent recurring responsibility was not dispatch, presentation, or rendering. It was the narrower post-eligibility question:

```text
For this exact QuestionFamily whose bounded eligibility is non-permitted, what existing bounded ask refusal is returned?
```

## Before

Bounded ask refusal was compressed in `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`:

- the CLI adapter checked `eligibility.permitted`;
- the same function distinguished `diagnostic_only` from other non-permitted statuses;
- the same function assembled the compatibility message for diagnostic-only refusal;
- the same function assembled the compatibility message for not-dispatchable refusal;
- those local refusal messages lived beside presentation override handling, selection, dispatch request construction, dispatch execution, and the knowledge-reachability JSON compatibility adjustment.

That compression made refusal less directly observable than exact lookup, eligibility, surface-argument satisfaction, selection, dispatch request construction, and dispatch execution.

## After

Bounded ask refusal is directly observable as a private implementation handoff:

- `BoundedWorkRefusalResult` carries the non-permitted question family, bounded status, compatibility message, and local reason.
- `bounded_work_refusal_for_eligibility(...)` owns the existing refusal messages for non-permitted bounded ask eligibility.
- `apply_bounded_ask_dispatch(...)` consumes the refusal result and preserves existing `parser.error(...)` behavior with the same message text.

## Recovered producer

`seed_runtime/question_surface_inventory.py::bounded_work_refusal_for_eligibility(...)` now owns the recovered bounded ask refusal responsibility.

The producer consumes only `BoundedWorkEligibilityResult` after upstream exact lookup and bounded eligibility have already run.

## Recovered artifact/helper

`seed_runtime/question_surface_inventory.py::BoundedWorkRefusalResult` carries the recovered boundary.

It carries only:

- `question_family`;
- `bounded_status`;
- the existing refusal `message`;
- a local implementation `reason`.

It intentionally does not carry:

- permitted eligibility ownership;
- required surface args;
- selected dispatch surface;
- selected surface value;
- dispatch request data;
- CLI namespace mutation;
- presentation flags;
- rendered output;
- JSON output;
- event or cluster mutation data.

## Recovered consumer

`seed_runtime/question_surface_inventory.py::bounded_work_refusal_for_eligibility(...)` is consumed by `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` when bounded eligibility is non-permitted.

## Required questions

1. **What responsibilities were previously compressed?**

   Non-permitted eligibility refusal, diagnostic-only refusal message construction, not-dispatchable refusal message construction, presentation override handling, selected bounded work construction, dispatch request construction, dispatch execution, and CLI compatibility handling were adjacent in the same bounded ask adapter.

2. **Which implementation-local ownership boundary became directly observable?**

   Bounded ask refusal for non-permitted exact QuestionFamily invocation became directly observable.

3. **What producer now owns the recovered responsibility?**

   `bounded_work_refusal_for_eligibility(...)` owns the recovered responsibility.

4. **What artifact or helper carries the recovered boundary, if any?**

   `BoundedWorkRefusalResult` carries the recovered boundary.

5. **Who consumes it?**

   `apply_bounded_ask_dispatch(...)` consumes the refusal result and passes its preserved message to `parser.error(...)`.

6. **Did any compatibility boundary change?**

   No.

## Compatibility preserved

No public compatibility boundary changed.

- Public CLI behavior is unchanged.
- Existing bounded ask refusal messages are preserved.
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
- `implementation_recovery_slice_003.md`

## LOC changed

Implementation/test change before this report:

```text
scripts/seed_local.py                      | 12 +++------
seed_runtime/question_surface_inventory.py | 43 ++++++++++++++++++++++++++++++
tests/test_question_surface_inventory.py   | 31 +++++++++++++++++++++
3 files changed, 77 insertions(+), 9 deletions(-)
```

This report file is additional documentation for the requested deliverable.

## Tests executed

- `python -m py_compile seed_runtime/question_surface_inventory.py scripts/seed_local.py` — passed.
- `pytest -q tests/test_question_surface_inventory.py` — passed, 52 tests.
- `python scripts/seed_local.py ask --question-family "selection explanation" --surface-args implementation_recovery --json >/tmp/selection_ask.json` — passed; exercised the app's bounded ask path adjacent to the recovered Selection implementation.
- `python scripts/seed_local.py --question-surface-inventory --json >/tmp/question_inventory.json` — passed; exercised the app's question-surface inventory.

## Remaining compressed responsibilities

This slice intentionally leaves these neighboring responsibilities compressed or only partially separated because recovering them would exceed exactly one implementation-local ownership boundary:

- selected / non-selected visibility ownership in `selection_path_audit`;
- presentation override handling;
- compatibility JSON special-casing for `knowledge reachability`;
- surface-local answer composition;
- rendering;
- broader Question Shape recovery;
- dispatch request and CLI mutation beyond their already existing local helpers.

No framework, engine, registry, dispatcher, scheduler, planner, router, universal selector, Begin function, or Town Clock was introduced.
