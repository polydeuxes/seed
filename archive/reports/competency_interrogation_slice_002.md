# Competency Interrogation Slice 002

## Selected implementation boundary

Evidence Support Assessment != Evaluation Report Composition

The selected boundary is local to the golden-case decision evaluation harness. The harness already validated produced decisions and checked expected decision properties before returning public `EvalResult` records. This slice separates that support assessment from the compatibility report object without changing public evaluation behavior.

## Implementation evidence

`DecisionEvaluator.evaluate_case(...)` previously performed three responsibilities in one method:

1. arrange the evaluation case and obtain a decision;
2. validate the decision and compare it against the expected kind/tool/question/refusal/answer support;
3. compose the public `EvalResult` report.

The support assessment is now carried by `_EvaluationSupportAssessment` and produced by `_assess_evaluation_support(...)`. `evaluate_case(...)` consumes that assessment only to compose the existing `EvalResult` shape.

## Before

`DecisionEvaluator.evaluate_case(...)` directly called `DecisionValidator`, accumulated validation and expectation errors, interpreted pass/fail, and built `EvalResult` in the same block.

## After

`DecisionEvaluator.evaluate_case(...)` still owns case setup, decision production, parse-error report composition, and public `EvalResult` composition. Validation and expectation support checking moved into `_assess_evaluation_support(...)`, which returns the private `_EvaluationSupportAssessment` artifact.

## Recovered producer

`_assess_evaluation_support(...)`

## Recovered artifact/helper

`_EvaluationSupportAssessment`

It carries only assessment fields:

- `errors`
- `validation_errors`
- derived `passed`

It intentionally does not carry public report fields such as `case_name`, `decision`, or `parse_error`.

## Consumer

`DecisionEvaluator.evaluate_case(...)` consumes `_EvaluationSupportAssessment` and composes the unchanged public `EvalResult`.

## Compatibility preserved

Yes. No compatibility boundary changed.

No public CLI, JSON, schema, event-ledger kind, diagnostic registration, diagnostic shape contract, runtime behavior, or public evaluation report shape changed. Existing parse-error handling and `EvalResult` fields are preserved.

## Files changed

- `seed_runtime/evaluations.py`
- `tests/test_evaluations.py`
- `competency_interrogation_slice_002.md`

## LOC changed

From `git diff --stat` at slice completion:

- `seed_runtime/evaluations.py`: 109 changed lines
- `tests/test_evaluations.py`: 33 changed lines
- `competency_interrogation_slice_002.md`: new report

## Tests executed

- `pytest -q tests/test_evaluations.py` — passed, 9 tests.
- `pytest -q` — failed on pre-existing repository-wide generated/inventory expectations unrelated to this slice: architecture generated output stability, storage consumer dependency audit filtering, observation inventory predicate discovery for `up`, and observation utilization predicate filtering. The focused evaluation tests passed.

## Required questions

### 1. Where were evidence/support/authority assessment and report composition previously mixed?

They were mixed in `DecisionEvaluator.evaluate_case(...)`, where decision validation, expectation support checking, pass/fail interpretation, and `EvalResult` construction occurred in one method.

### 2. Which implementation-local boundary became directly observable?

Evidence Support Assessment != Evaluation Report Composition

### 3. What private artifact or helper now carries the assessment, if any?

`_EvaluationSupportAssessment`, produced by `_assess_evaluation_support(...)`.

### 4. Who consumes that artifact/helper?

`DecisionEvaluator.evaluate_case(...)` consumes the assessment to compose the unchanged `EvalResult`.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed competency-interrogation responsibilities

- Parse-error classification remains directly composed as `EvalResult` because this slice recovered only support assessment after a valid decision exists.
- Evaluation run aggregation remains in `EvalRun` properties and `DecisionEvaluator.evaluate(...)`.
- Evaluation recording remains in `DecisionEvaluator.record_run(...)`.
- Seed case construction and small-model MVP fixtures remain unchanged.
- No competency interrogation engine, runtime grammar, methodology framework, planner, scheduler, routing framework, authority framework, capability framework, CLI change, JSON change, schema change, ledger change, or runtime behavior change was introduced.
