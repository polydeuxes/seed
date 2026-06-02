from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.policy import PolicyGate
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import StateProjector
from toolkits.core.echo import operations


def make_executor(*, policy_gate=None):
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    executor = ToolExecutor(ledger, registry, projector, policy_gate=policy_gate)
    return executor, ledger


def event_kinds(ledger):
    return [event.kind for event in ledger.list_events("ws_1")]


def test_successful_echo_tool_execution():
    executor, ledger = make_executor()

    result = executor.execute("ws_1", "ses_1", "echo", {"message": "hello"})

    assert result.kind == "tool_result"
    assert result.status == "completed"
    assert result.payload["output"] == {
        "ok": True,
        "message": "hello",
        "workspace_id": "ws_1",
    }
    assert event_kinds(ledger) == ["tool.call.started", "tool.call.completed"]


def test_invalid_input_schema_fails_before_execution(monkeypatch):
    executor, ledger = make_executor()
    called = False

    def echo_would_fail(ctx, message):
        nonlocal called
        called = True
        return operations.echo(ctx, message)

    monkeypatch.setattr(operations, "echo", echo_would_fail)

    result = executor.execute("ws_1", "ses_1", "echo", {"message": 123})

    assert result.kind == "tool_failed"
    assert result.status == "failed"
    assert result.error == "$.message must be a string"
    assert called is False
    assert event_kinds(ledger) == ["tool.call.failed"]
    assert ledger.list_events("ws_1")[0].payload["phase"] == "input_validation"


def test_policy_block_prevents_execution(monkeypatch):
    policy_gate = PolicyGate({"echo.run": "L4"})
    executor, ledger = make_executor(policy_gate=policy_gate)
    called = False

    def echo_would_fail(ctx, message):
        nonlocal called
        called = True
        return operations.echo(ctx, message)

    monkeypatch.setattr(operations, "echo", echo_would_fail)

    result = executor.execute("ws_1", "ses_1", "echo", {"message": "blocked"})

    assert result.kind == "block"
    assert result.status == "blocked"
    assert called is False
    assert event_kinds(ledger) == ["tool.policy.blocked"]
    assert ledger.list_events("ws_1")[0].payload["policy"]["outcome"] == "block"


def test_output_schema_validation_failure_records_failed_event(monkeypatch):
    executor, ledger = make_executor()

    def invalid_echo(ctx, message):
        return {"ok": "yes", "message": message, "workspace_id": ctx.workspace_id}

    monkeypatch.setattr(operations, "echo", invalid_echo)

    result = executor.execute("ws_1", "ses_1", "echo", {"message": "bad output"})

    assert result.kind == "tool_failed"
    assert result.status == "failed"
    assert "$.ok must be a boolean" in result.error
    assert event_kinds(ledger) == ["tool.call.started", "tool.call.failed"]
    assert ledger.list_events("ws_1")[-1].payload["phase"] == "execution"


def test_completed_tool_call_appends_tool_call_completed():
    executor, ledger = make_executor()

    executor.execute("ws_1", "ses_1", "echo", {"message": "done"})

    completed = ledger.list_events("ws_1")[-1]
    assert completed.kind == "tool.call.completed"
    assert completed.payload["tool"] == "echo"
    assert completed.payload["output"]["message"] == "done"
