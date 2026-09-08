# Implementation Recovery Slice 001 — Exact QuestionFamily Lookup Boundary

## Selected boundary

This slice recovers the implementation-local boundary for **exact QuestionFamily lookup for existing registered or audited selection surfaces**.

The boundary is intentionally narrow: it accepts an operator-supplied QuestionFamily string, checks it against the static inventory rows, and produces an exact lookup handoff only when the family exists. It does not own eligibility, required argument handling, diagnostic-only refusal, not-dispatchable refusal, dispatch selection, dispatch execution, rendering, answer composition, event ledger behavior, or schema changes.

## Implementation evidence

The highest implementation-pressure candidate pointed at existing registered or audited selection surfaces. The adjacent code showed these separate responsibilities already compressed in the bounded ask path:

1. static QuestionFamily inventory rows;
2. exact QuestionFamily admission;
3. bounded ask eligibility classification;
4. required surface argument handling;
5. diagnostic-only refusal;
6. not-dispatchable refusal;
7. selected bounded work construction;
8. dispatch request construction;
9. dispatch execution through the existing CLI namespace;
10. selected / non-selected visibility in the selection path audit.

The smallest implementation-backed boundary directly observable in the code was exact family lookup. Before this slice, `_prepare_question_family_eligibility_input(...)` both checked inventory membership and prepared the eligibility input, while `bounded_work_eligibility_for_question_family(...)` could construct eligibility input directly. That made exact inventory admission less explicit than the later eligibility and dispatch handoffs.

This slice adds `ExactQuestionFamilyLookupResult` and `_lookup_exact_question_family(...)` in `seed_runtime/question_surface_inventory.py`. `_prepare_question_family_eligibility_input(...)` now consumes that lookup result before producing eligibility input, and public bounded eligibility now goes through the same exact lookup path.

## Before

Exact QuestionFamily lookup was compressed into eligibility preparation:

- `_prepare_question_family_eligibility_input(...)` built a set of inventory family names, rejected unknown text, and returned `_QuestionFamilyEligibilityInput`.
- `bounded_work_eligibility_for_question_family(...)` created `_QuestionFamilyEligibilityInput` directly instead of consuming the same exact lookup/preparation path.
- Tests proved preparation rejected unknown text, but there was no direct artifact proving lookup was separate from eligibility, dispatch surface selection, or required argument ownership.

## After

Exact lookup is directly observable as its own private handoff:

- `ExactQuestionFamilyLookupResult` carries only the admitted `question_family`.
- `_lookup_exact_question_family(...)` owns exact inventory-backed lookup and unknown-family refusal.
- `_prepare_question_family_eligibility_input(...)` consumes the lookup result and remains responsible only for preparing eligibility input.
- `bounded_work_eligibility_for_question_family(...)` now uses the same lookup/preparation path as the CLI-adjacent bounded ask flow.
- Tests prove the lookup artifact excludes `bounded_status`, `dispatch_surface`, and `required_surface_args`, and that unknown text is rejected before eligibility.

## Recovered producer

`seed_runtime/question_surface_inventory.py::_lookup_exact_question_family(...)` now produces the exact family lookup result.

## Recovered artifact/helper

`seed_runtime/question_surface_inventory.py::ExactQuestionFamilyLookupResult` carries the recovered boundary.

It carries only:

- `question_family`

It intentionally does not carry:

- bounded eligibility status;
- dispatch surface;
- required surface arguments;
- selected surface value;
- diagnostic relationship;
- rendered output;
- event or mutation data.

## Recovered consumer

`seed_runtime/question_surface_inventory.py::_prepare_question_family_eligibility_input(...)` consumes `ExactQuestionFamilyLookupResult` and produces `_QuestionFamilyEligibilityInput` for bounded eligibility evaluation.

The CLI bounded ask path remains a downstream consumer through `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`, which already calls `_prepare_question_family_eligibility_input(...)` before eligibility classification and dispatch selection.

## Required questions

1. **What responsibilities were previously compressed?**

   Exact inventory-backed QuestionFamily lookup, eligibility-input preparation, bounded ask eligibility classification, required-argument handling, diagnostic-only refusal, not-dispatchable refusal, bounded work selection, dispatch request construction, and dispatch execution were adjacent in the same bounded ask selection surface.

2. **Which implementation-local ownership boundary became directly observable?**

   Exact QuestionFamily lookup for existing static inventory rows became directly observable.

3. **What producer now owns the recovered responsibility?**

   `_lookup_exact_question_family(...)` owns the recovered exact lookup responsibility.

4. **What artifact or helper carries the recovered boundary, if any?**

   `ExactQuestionFamilyLookupResult` carries the boundary.

5. **Who consumes it?**

   `_prepare_question_family_eligibility_input(...)` consumes it, and bounded ask consumes the prepared eligibility input downstream.

6. **Did any compatibility boundary change?**

   No.

## Compatibility preserved

No public compatibility boundary changed.

- Public CLI behavior is unchanged.
- JSON output is unchanged.
- Diagnostic output is unchanged.
- Schema is unchanged.
- Event ledger behavior is unchanged.
- Runtime mutation behavior is unchanged.
- No new diagnostic, audit, probe, operational CLI flag, or recordable output was introduced.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_001.md`

## LOC changed

Implementation/test change before this report:

- `seed_runtime/question_surface_inventory.py`: 31 insertions, 6 deletions.
- `tests/test_question_surface_inventory.py`: 19 insertions.
- Total before this report: 50 insertions, 6 deletions.

This report adds the campaign deliverable document.

## Tests and checks executed

- `pytest -q tests/test_question_surface_inventory.py` — passed, 50 tests.
- `python scripts/seed_local.py --question-surface-inventory --json >/tmp/question_inventory.json` — passed; exercised the app's question-surface inventory.
- `python scripts/seed_local.py ask --question-family "selection explanation" --surface-args implementation_recovery --json >/tmp/selection_ask.json` — passed; exercised the app's bounded ask path for the selected selection surface.

## Remaining compressed responsibilities

This slice intentionally leaves these neighboring responsibilities compressed or only partially separated because recovering them would exceed exactly one implementation-local ownership boundary:

- required surface argument ownership;
- diagnostic-only refusal ownership;
- not-dispatchable refusal ownership;
- selected / non-selected visibility ownership in `selection_path_audit`;
- exact dispatch surface selection beyond the already existing bounded work selection helper;
- human/JSON answer presentation boundaries;
- broader Question Shape recovery;
- new Question Family admission.

No framework, engine, registry, dispatcher, scheduler, planner, or universal selector was introduced.
