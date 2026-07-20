import ast
from pathlib import Path

from seed_runtime.api import SeedAPI
from seed_runtime.events import EventLedger
from seed_runtime.models import RuntimeResponse
from seed_runtime.runtime import Runtime
from seed_runtime.state import StateProjector


def make_api() -> tuple[SeedAPI, EventLedger]:
    ledger = EventLedger()
    projector = StateProjector(ledger)
    runtime = Runtime(ledger, projector)
    return SeedAPI(runtime, projector), ledger


def test_post_user_message_returns_input_boundary_response():
    api, ledger = make_api()

    result = api.post_user_message("ws", "ses", "hello")

    assert isinstance(result, RuntimeResponse)
    assert result.kind == "unsupported"
    assert result.payload["reason"] == "model_decision_authority_excised"
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "runtime.decision_authority_unsupported",
    ]


def test_get_state_returns_projected_workspace_state():
    api, _ = make_api()

    state = api.get_state("ws_state")

    assert state["workspace_id"] == "ws_state"
    assert state["last_event_id"] is None


def test_api_uses_canonical_runtime_not_runtime_loop():
    imports: list[tuple[str | None, str | None]] = []
    tree = ast.parse(Path("seed_runtime/api.py").read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend((alias.name, None) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.extend((node.module, alias.name) for alias in node.names)

    assert ("seed_runtime.runtime", "Runtime") in imports
    assert not any(module == "seed_runtime.runtime_loop" for module, _name in imports)


def test_runtime_module_is_canonical():
    from seed_runtime.runtime import Runtime

    assert Runtime.__name__ == "Runtime"
