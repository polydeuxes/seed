import ast
from pathlib import Path

from seed_runtime.api import SeedAPI
from seed_runtime.events import EventLedger
from seed_runtime.policy import PolicyGate
from seed_runtime.projection_store import InMemoryProjectionStore
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime_loop import (
    Decision as LoopDecision,
    EchoTool,
    FakeDecisionProvider,
    RuntimeLoop,
    RuntimeResult,
)
from seed_runtime.state import StateProjector


def make_api(decision: LoopDecision) -> tuple[SeedAPI, EventLedger, FakeDecisionProvider]:
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    provider = FakeDecisionProvider(decision)
    runtime = RuntimeLoop(
        ledger,
        InMemoryProjectionStore(),
        registry,
        PolicyGate(),
        provider,
        {"echo": EchoTool()},
        projector=projector,
    )
    return SeedAPI(runtime, projector, registry), ledger, provider


def test_post_user_message_answer_path_returns_runtime_result():
    api, ledger, provider = make_api(
        LoopDecision(kind="answer", text="done", reason="api answer")
    )

    result = api.post_user_message("ws", "ses", "hello")

    assert isinstance(result, RuntimeResult)
    assert result.decision_kind == "answer"
    assert result.response_text == "done"
    assert result.workspace_id == "ws"
    assert result.error is None
    assert provider.last_context is not None
    assert provider.last_context.current_input == {
        "text": "hello",
        "metadata": {"session_id": "ses"},
    }
    input_event = ledger.list_events("ws")[0]
    assert input_event.kind == "input.user_message"
    assert input_event.payload["metadata"] == {"session_id": "ses"}


def test_post_user_message_request_tool_path_returns_runtime_result():
    api, ledger, _ = make_api(
        LoopDecision(
            kind="request_tool",
            reason="need a new capability",
            tool_need={
                "name": "Weather Lookup",
                "summary": "Look up weather for a location.",
                "capability": "weather lookup",
                "desired_inputs": ["location"],
                "desired_outputs": ["forecast"],
            },
        )
    )

    result = api.post_user_message("ws", "ses", "what is the weather?")

    assert isinstance(result, RuntimeResult)
    assert result.decision_kind == "request_tool"
    assert result.response_text == "Recorded tool need weather_lookup."
    assert result.decision_outcome == "tool_requested"
    assert result.error is None
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "tool_need.created",
        "decision.recorded",
    ]


def test_get_state_returns_projected_workspace_state():
    api, _, _ = make_api(LoopDecision(kind="answer", text="done", reason="api state"))

    state = api.get_state("ws_state")

    assert state["workspace_id"] == "ws_state"
    assert state["last_event_id"] is None


def test_get_tools_returns_registered_tools():
    api, _, _ = make_api(LoopDecision(kind="answer", text="done", reason="api tools"))

    tools = api.get_tools()

    assert tools[0]["name"] == "echo"
    assert tools[0]["toolkit_id"] == "tk_core_echo"


def test_api_migration_does_not_import_old_runtime():
    imports: list[tuple[str | None, str | None]] = []
    tree = ast.parse(Path("seed_runtime/api.py").read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend((alias.name, None) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.extend((node.module, alias.name) for alias in node.names)

    assert ("seed_runtime.runtime", "Runtime") not in imports
    assert any(
        module == "seed_runtime.runtime_loop" and name == "RuntimeLoop"
        for module, name in imports
    )


def test_old_runtime_module_still_exists_for_now():
    from seed_runtime.runtime import Runtime

    assert Runtime.__name__ == "Runtime"
