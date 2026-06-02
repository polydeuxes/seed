from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.models import Decision
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import StateProjector


def test_validates_answer_and_question_required_fields():
    validator = DecisionValidator()
    assert validator.validate(Decision(kind="answer", reason="done", answer="hi")).ok
    assert not validator.validate(Decision(kind="ask_question", reason="unclear")).ok


def test_validates_tool_need_shape():
    validator = DecisionValidator()
    decision = Decision(kind="request_tool", reason="missing", tool_need={"name": "install_ssh_server", "summary": "Install and start an SSH server", "capability": "ssh_access"})
    assert validator.validate(decision).ok


def test_call_tool_requires_registered_tool_and_schema():
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    state = StateProjector(EventLedger()).project("ws_1")
    validator = DecisionValidator(registry)

    assert validator.validate(Decision(kind="call_tool", reason="test", tool_name="echo", tool_arguments={"message": "hi"}), state).ok
    invalid = validator.validate(Decision(kind="call_tool", reason="test", tool_name="echo", tool_arguments={"bad": "hi"}), state)
    assert not invalid.ok
    assert "required" in invalid.errors[0]
