from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel, Runtime
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


def make_runtime(decision):
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    runtime = Runtime(
        ledger,
        projector,
        ContextComposer(registry),
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        FakeDecisionModel(decision),
    )
    return runtime, ledger


def test_routes_answer():
    runtime, ledger = make_runtime(Decision(kind="answer", reason="ok", answer="done"))
    response = runtime.handle_user_message("ws", "ses", "hi")
    assert response.kind == "answer"
    assert ledger.list_events("ws")[-1].kind == "response.answer"


def test_routes_question():
    runtime, _ = make_runtime(Decision(kind="ask_question", reason="need", question="Which host?"))
    assert runtime.handle_user_message("ws", "ses", "install ssh").kind == "question"


def test_routes_request_tool():
    decision = Decision(kind="request_tool", reason="missing", tool_need={"name": "install_ssh_server", "summary": "Install and start SSH server", "capability": "ssh_access"})
    runtime, ledger = make_runtime(decision)
    response = runtime.handle_user_message("ws", "ses", "install ssh")
    assert response.kind == "tool_need"
    assert "tool_need.created" in [event.kind for event in ledger.list_events("ws")]


def test_routes_call_tool():
    runtime, _ = make_runtime(Decision(kind="call_tool", reason="safe", tool_name="echo", tool_arguments={"message": "hi"}))
    response = runtime.handle_user_message("ws", "ses", "echo hi")
    assert response.kind == "tool_result"
    assert response.payload["output"]["message"] == "hi"
