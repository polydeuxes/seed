from seed_runtime.evaluations import DecisionEvaluator, EvalCase, EvalExpectation
from seed_runtime.models import Decision
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel


def test_evaluator_passes_matching_tool_call_case():
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    model = FakeDecisionModel(Decision(kind="call_tool", reason="safe", tool_name="echo", tool_arguments={"message": "hello"}))
    evaluator = DecisionEvaluator(registry, model)

    run = evaluator.evaluate([
        EvalCase(name="echo hello", user_message="echo hello", expected=EvalExpectation(kind="call_tool", tool_name="echo"))
    ])

    assert run.passed
    assert run.pass_rate == 1.0


def test_evaluator_reports_validation_and_expectation_errors():
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    model = FakeDecisionModel(Decision(kind="call_tool", reason="safe", tool_name="missing", tool_arguments={}))
    result = DecisionEvaluator(registry, model).evaluate_case(
        EvalCase(name="bad call", user_message="do it", expected=EvalExpectation(kind="answer"))
    )

    assert not result.passed
    assert "unknown tool" in result.validation_errors[0]
    assert any("expected kind" in error for error in result.errors)
