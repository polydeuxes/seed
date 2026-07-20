from seed_runtime.context import DecisionInputComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import StaticDecisionProducer, Runtime
from seed_runtime.state import StateProjector
from seed_runtime.tool_intent import ToolIntentGuard
from seed_runtime.tool_needs import ToolNeedService


def make_runtime(decision, *, max_decision_retries=0):
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    model = decision if hasattr(decision, "decide") else StaticDecisionProducer(decision)
    runtime = Runtime(
        ledger,
        projector,
        DecisionInputComposer(registry),
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        model,
        max_decision_retries=max_decision_retries,
    )
    return runtime, ledger, model


def echo_decision(message):
    return Decision(
        kind="call_tool",
        reason="echo requested",
        tool_name="echo",
        tool_arguments={"message": message},
    )


def test_echo_hello_allowed():
    runtime, ledger, _ = make_runtime(echo_decision("hello"))

    response = runtime.handle_user_message("ws", "ses", "echo hello")

    assert response.kind == "tool_result"
    assert response.payload["output"]["message"] == "hello"
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "tool.call.started",
        "tool.call.completed",
        "evidence.observed",
    ]


def test_install_docker_echo_rejected():
    runtime, ledger, _ = make_runtime(echo_decision("install docker"))

    response = runtime.handle_user_message("ws", "ses", "install docker")

    assert response.kind == "invalid_decision"
    assert response.payload == {
        "errors": ["echo tool requires current input to start with 'echo '"]
    }
    events = ledger.list_events("ws")
    assert [event.kind for event in events] == [
        "input.user_message",
        "model.decision.proposed",
        "model.decision.intent_rejected",
    ]
    assert events[-1].payload == {
        "errors": ["echo tool requires current input to start with 'echo '"],
        "attempt": 0,
    }


def test_echo_wrong_message_rejected():
    runtime, ledger, _ = make_runtime(echo_decision("wrong-message"))

    response = runtime.handle_user_message("ws", "ses", "echo hello")

    assert response.kind == "invalid_decision"
    assert response.payload == {
        "errors": ["echo tool message must equal text after 'echo '"]
    }
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "model.decision.intent_rejected",
    ]


def test_guard_rejects_tool_not_visible_to_model():
    result = ToolIntentGuard().validate(
        "echo hello", echo_decision("hello"), visible_tools=[]
    )

    assert result.ok is False
    assert result.errors == ["tool 'echo' is not visible to the model"]
