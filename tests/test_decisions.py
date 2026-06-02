from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.models import Decision
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import StateProjector


def test_answer_requires_answer():
    validator = DecisionValidator()

    assert validator.validate(Decision(kind="answer", reason="done", answer="hi")).ok
    invalid = validator.validate(Decision(kind="answer", reason="done"))

    assert not invalid.ok
    assert invalid.errors == ["answer decisions require answer"]


def test_ask_question_requires_question():
    validator = DecisionValidator()

    assert validator.validate(
        Decision(kind="ask_question", reason="unclear", question="What should I do?")
    ).ok
    invalid = validator.validate(Decision(kind="ask_question", reason="unclear"))

    assert not invalid.ok
    assert invalid.errors == ["ask_question decisions require question"]


def test_request_tool_requires_tool_need_name_summary_and_capability():
    validator = DecisionValidator()
    decision = Decision(
        kind="request_tool",
        reason="missing",
        tool_need={
            "name": "install_ssh_server",
            "summary": "Install and start an SSH server",
            "capability": "ssh_access",
        },
    )

    assert validator.validate(decision).ok

    invalid = validator.validate(
        Decision(
            kind="request_tool",
            reason="missing",
            tool_need={"name": "install_ssh_server", "summary": "Install SSH"},
        )
    )

    assert not invalid.ok
    assert invalid.errors == ["tool_need.capability is required and must be snake_case"]


def test_request_tool_requires_tool_need_payload():
    validator = DecisionValidator()
    invalid = validator.validate(Decision(kind="request_tool", reason="missing"))

    assert not invalid.ok
    assert invalid.errors == ["request_tool decisions require tool_need"]


def test_call_tool_requires_tool_name():
    validator = DecisionValidator()
    invalid = validator.validate(Decision(kind="call_tool", reason="test"))

    assert not invalid.ok
    assert invalid.errors == ["call_tool decisions require tool_name"]


def test_call_tool_requires_registered_tool_and_schema():
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    state = StateProjector(EventLedger()).project("ws_1")
    validator = DecisionValidator(registry)

    assert validator.validate(
        Decision(
            kind="call_tool",
            reason="test",
            tool_name="echo",
            tool_arguments={"message": "hi"},
        ),
        state,
    ).ok
    invalid = validator.validate(
        Decision(
            kind="call_tool",
            reason="test",
            tool_name="echo",
            tool_arguments={"bad": "hi"},
        ),
        state,
    )
    assert not invalid.ok
    assert "required" in invalid.errors[0]


def test_propose_state_patch_requires_state_patch():
    validator = DecisionValidator()

    assert validator.validate(
        Decision(
            kind="propose_state_patch",
            reason="record observation",
            state_patch={"facts": []},
        )
    ).ok
    invalid = validator.validate(
        Decision(kind="propose_state_patch", reason="record observation")
    )

    assert not invalid.ok
    assert invalid.errors == ["propose_state_patch decisions require state_patch"]


def test_refuse_requires_reason():
    validator = DecisionValidator()

    assert validator.validate(Decision(kind="refuse", reason="unsafe request")).ok
    invalid = validator.validate(Decision(kind="refuse", reason=""))

    assert not invalid.ok
    assert invalid.errors == ["refuse decisions require reason"]
