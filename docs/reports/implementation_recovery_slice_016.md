# Implementation Recovery Slice 016

## Selected boundary

The selected implementation-local boundary is the bounded-ask presentation handoff for an already admitted and eligible Question Family.

`seed ask --question-family ... --presentation` is diagnostic presentation inside the established `ask --question-family` surface. The local responsibility is to hand off the exact admitted Question Family to the question-family explanation surface. It is not responsible for satisfying dispatch-only surface arguments.

## Implementation evidence

Adjacent implementation evidence selected this seam:

- `scripts/seed_local.py` admits only the exact `ask --question-family <exact-question-family>` CLI shape before bounded-ask processing.
- `seed_runtime/question_surface_inventory.py` prepares exact inventory-backed QuestionFamily text before eligibility.
- `seed_runtime/question_surface_inventory.py` has a dedicated `BoundedWorkPresentationHandoff` artifact whose fields are only `question_family`, `question_family_explanation`, and `reason`.
- `bounded_work_presentation_handoff_for_eligibility(...)` requires permitted eligibility but does not consume dispatch surface, selected surface value, required surface args, dispatch request, execution, rendering, diagnostics, schema, event ledger, or semantic routing.
- `apply_bounded_ask_presentation_handoff(...)` applies that already prepared handoff and clears the bounded ask message.
- Dispatch argument satisfaction remains separately owned by `bounded_work_surface_args_for_eligibility(...)` and is still required for runtime dispatch of parameterized families.

## Fidelity classification

**Unfaithful realization, bounded and correctable.**

Before this slice, `apply_bounded_ask_dispatch(...)` validated `--surface-args` for every permitted family before checking `--presentation`. That made a presentation-only invocation of a parameterized family fail with a dispatch-argument error, even though the presentation handoff artifact does not consume dispatch arguments.

Fidelity required moving presentation handoff ahead of dispatch surface-argument validation after exact lookup and eligibility had already succeeded.

## Before

`seed ask --question-family "derivation explanation" --presentation --json` failed because the CLI demanded dispatch-only `--surface-args` before allowing presentation.

This incorrectly made presentation depend on runtime dispatch argument satisfaction.

## After

`seed ask --question-family "derivation explanation" --presentation --json` now returns the existing composed QuestionFamily explanation JSON for the admitted eligible family without requiring dispatch surface args.

Runtime dispatch remains unchanged: `seed ask --question-family "derivation explanation"` still requires the exact dispatch arguments.

## Recovered or corrected owner

Corrected owner: bounded-ask presentation handoff.

The owner is responsible for turning an already admitted, eligible Question Family into a question-family explanation handoff and for clearing the bounded-ask message after applying that handoff.

It does not own dispatch argument validation or runtime answer dispatch.

## Artifact/helper

Artifact: `BoundedWorkPresentationHandoff`.

Helpers:

- `bounded_work_presentation_handoff_for_eligibility(...)`
- `apply_bounded_work_presentation_handoff(...)`
- `clear_bounded_ask_presentation_message(...)`
- `apply_bounded_ask_presentation_handoff(...)`

No new helper was introduced.

## Consumer

Consumer: `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`.

It now consumes the presentation handoff immediately after exact lookup and permitted eligibility when `--presentation` is present. Dispatch-only surface-argument validation remains consumed only by dispatch selection.

## Negative authority

This boundary does not:

- reclassify, hide, rename, deprecate, or extract `seed ask --question-family`;
- make `ask --question-family` the canonical interactive inquiry road;
- transfer question ownership to the operator;
- establish constitutional Question Family applicability;
- alter `diagnostic_only` status or rejection;
- infer surface args;
- dispatch runtime answer surfaces during presentation;
- write the event ledger;
- mutate cluster truth;
- change diagnostic inventory registration or shape-audit declarations;
- promote Book or presentation vocabulary into implementation knowledge.

## Compatibility and runtime treatment

Preserved:

- exact `ask --question-family` admission;
- unknown-family rejection;
- free-text routing rejection;
- diagnostic-only rejection;
- not-dispatchable rejection;
- dispatch argument requirements for runtime answer dispatch;
- JSON shape for question-family explanation;
- human output for question-family explanation;
- diagnostic inventory and diagnostic shape-audit behavior;
- read-only, no-recording, no-event-ledger, no-cluster-mutation treatment for this path.

Changed only:

- presentation-only invocations for parameterized eligible families no longer require dispatch-only `--surface-args`.

## Files changed

- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_016.md`

## Tests executed

- `python scripts/seed_local.py ask --question-family 'selection explanation' --presentation | head -30`
- `python scripts/seed_local.py ask --question-family 'derivation explanation' --presentation --json | python -m json.tool | head -40`
- `pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

The first full pytest run exposed the existing contrary expectation in `test_bounded_ask_presentation_parameterized_family_still_requires_surface_args`; that test was updated to preserve the corrected boundary.

## Remaining compressed responsibilities

Still compressed nearby:

- broader bounded-ask orchestration in `apply_bounded_ask_dispatch(...)`;
- exact lookup preparation versus public CLI parser errors;
- dispatch request production versus dispatch namespace mutation;
- post-dispatch compatibility handling for knowledge-reachability JSON;
- duplicated-looking presentation/dispatch control flow that remains intentionally not extracted in this slice.

## Preserved Unknowns

Unknown remains preserved for:

- constitutional applicability of any Question Family to an operator goal;
- any canonical interactive inquiry-road implementation;
- future family admission or registration lifecycle;
- whether presentation vocabulary has preserved or projected knowledge standing absent implementation evidence;
- whether broader bounded-ask orchestration should later receive a different local owner.
