from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import StateProjector


def test_executes_echo_and_records_events():
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    executor = ToolExecutor(ledger, registry, projector)

    response = executor.execute("ws_1", "ses_1", "echo", {"message": "hello"})

    assert response.kind == "tool_result"
    assert response.payload["output"]["message"] == "hello"
    assert [event.kind for event in ledger.list_events("ws_1")] == ["tool.call.started", "tool.call.completed"]
