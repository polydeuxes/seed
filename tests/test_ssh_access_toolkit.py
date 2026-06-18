from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import StateProjector


def make_executor():
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/generated/ssh_access/toolkit.yaml")
    projector = StateProjector(ledger)
    return ToolExecutor(ledger, registry, projector), ledger, registry


def test_verify_ssh_access_is_stubbed_and_does_not_mutate_or_network():
    executor, ledger, registry = make_executor()

    result = executor.execute("ws", "ses", "verify_ssh_access", {"host": "example_host"})

    assert result.kind == "tool_result"
    assert result.status == "completed"
    assert result.payload["output"] == {
        "ok": True,
        "host": "example_host",
        "access_status": "not_checked",
        "method": "stub_no_network",
        "summary": "SSH access for example_host was not checked because network SSH is not enabled in this prototype.",
    }
    assert registry.require("verify_ssh_access").risk_class == "L1"
    assert [event.kind for event in ledger.list_events("ws")] == [
        "tool.call.started",
        "tool.call.completed",
        "evidence.observed",
    ]


def test_plan_ssh_install_returns_non_mutating_steps_only():
    executor, ledger, registry = make_executor()

    result = executor.execute("ws", "ses", "plan_ssh_install", {"host": "example_host"})

    assert result.kind == "tool_result"
    assert result.status == "completed"
    output = result.payload["output"]
    assert output["host"] == "example_host"
    assert output["plan_only"] is True
    assert output["mutation_allowed"] is False
    assert len(output["steps"]) >= 4
    assert all(isinstance(step, str) for step in output["steps"])
    assert registry.require("plan_ssh_install").risk_class == "L1"
    assert "host_note.added" not in [event.kind for event in ledger.list_events("ws")]


def test_ssh_access_toolkit_exposes_no_mutating_install_tool():
    _, _, registry = make_executor()

    tool_names = [tool.name for tool in registry.list_tools()]
    visible_tool_names = [tool.name for tool in registry.list_tools(visible_only=True)]

    assert tool_names == ["plan_ssh_install", "verify_ssh_access"]
    assert visible_tool_names == ["plan_ssh_install", "verify_ssh_access"]
    assert registry.get("install_ssh_server") is None
