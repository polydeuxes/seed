import ast
from pathlib import Path

from seed_runtime.api import SeedAPI
from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision, RuntimeResponse
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel, Runtime
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


def make_api(decision: Decision) -> tuple[SeedAPI, EventLedger, FakeDecisionModel]:
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    provider = FakeDecisionModel(decision)
    runtime = Runtime(
        ledger,
        projector,
        ContextComposer(registry),
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        provider,
    )
    return SeedAPI(runtime, projector, registry), ledger, provider


def test_post_user_message_answer_path_returns_runtime_response():
    api, ledger, provider = make_api(
        Decision(kind="answer", answer="done", reason="api answer")
    )

    result = api.post_user_message("ws", "ses", "hello")

    assert isinstance(result, RuntimeResponse)
    assert result.kind == "answer"
    assert result.message == "done"
    assert provider.last_context is not None
    assert provider.last_context.current_input["text"] == "hello"
    input_event = ledger.list_events("ws")[0]
    assert input_event.kind == "input.user_message"
    assert input_event.session_id == "ses"


def test_post_user_message_request_tool_path_returns_runtime_response():
    api, ledger, _ = make_api(
        Decision(
            kind="request_tool",
            reason="need a new capability",
            tool_need={
                "name": "weather_lookup",
                "summary": "Look up weather for a location.",
                "capability": "weather_lookup",
                "desired_inputs": ["location"],
                "desired_outputs": ["forecast"],
            },
        )
    )

    result = api.post_user_message("ws", "ses", "what is the weather?")

    assert isinstance(result, RuntimeResponse)
    assert result.kind == "tool_need"
    assert result.message == "Recorded tool need weather_lookup."
    assert result.payload["tool_need"]["capability"] == "weather_lookup"
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "tool_need.created",
    ]


def test_get_state_returns_projected_workspace_state():
    api, _, _ = make_api(Decision(kind="answer", answer="done", reason="api state"))

    state = api.get_state("ws_state")

    assert state["workspace_id"] == "ws_state"
    assert state["last_event_id"] is None


def test_get_tools_returns_registered_tools():
    api, _, _ = make_api(Decision(kind="answer", answer="done", reason="api tools"))

    tools = api.get_tools()

    assert tools[0]["name"] == "echo"
    assert tools[0]["toolkit_id"] == "tk_core_echo"


def test_api_uses_canonical_runtime_not_runtime_loop():
    imports: list[tuple[str | None, str | None]] = []
    tree = ast.parse(Path("seed_runtime/api.py").read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend((alias.name, None) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.extend((node.module, alias.name) for alias in node.names)

    assert ("seed_runtime.runtime", "Runtime") in imports
    assert not any(
        module == "seed_runtime.runtime_loop" for module, _name in imports
    )


def test_runtime_module_is_canonical():
    from seed_runtime.runtime import Runtime

    assert Runtime.__name__ == "Runtime"
