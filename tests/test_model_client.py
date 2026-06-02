import pytest

from seed_runtime.model_client import DecisionParseError, StrictJSONDecisionParser


def test_strict_json_decision_parser_accepts_decision_object():
    decision = StrictJSONDecisionParser().parse('{"kind":"answer","reason":"done","answer":"hello"}')
    assert decision.kind == "answer"
    assert decision.answer == "hello"


def test_strict_json_decision_parser_rejects_prose():
    with pytest.raises(DecisionParseError):
        StrictJSONDecisionParser().parse('Here is the decision: {"kind":"answer"}')
