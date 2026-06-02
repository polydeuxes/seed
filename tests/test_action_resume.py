import pytest

from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.pending_actions import PendingActionService
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
    return executor, ledger, projector


def event_kinds(ledger):
    return [event.kind for event in ledger.list_events("ws_1")]


def create_approved_echo_action(message="resume me", *, scope="host_1"):
    executor, ledger, projector = make_executor(
        policy_gate=PolicyGate({"echo.run": "L3"})
    )
    result = executor.execute(
        "ws_1",
        "ses_request",
        "echo",
        {"message": message},
        scope=scope,
        correlation_id="corr_1",
    )
    pending_action = result.pending_action
    assert pending_action is not None
    service = PendingActionService(ledger, projector)
    service.mark_approved(
        "ws_1",
        pending_action.id,
        session_id="ses_approve",
        causation_id="approval_request_evt",
        correlation_id="corr_1",
    )
    return executor, ledger, projector, pending_action


def test_approved_pending_action_resumes_echo_tool():
    executor, ledger, projector, pending_action = create_approved_echo_action()

    result = executor.resume_approved_tool_call(
        "ws_1", pending_action.id, session_id="ses_resume"
    )

    assert result.kind == "tool_result"
    assert result.status == "completed"
    assert result.output == {
        "ok": True,
        "message": "resume me",
        "workspace_id": "ws_1",
    }
    assert projector.project("ws_1").pending_actions[pending_action.id].status == (
        "completed"
    )
    assert event_kinds(ledger) == [
        "tool.approval.required",
        "pending_action.created",
        "pending_action.approved",
        "tool.call.started",
        "tool.call.completed",
        "evidence.observed",
        "pending_action.completed",
    ]
    started_event = ledger.list_events("ws_1")[3]
    approved_event = ledger.list_events("ws_1")[2]
    assert started_event.payload == {
        "tool": "echo",
        "arguments": {"message": "resume me"},
        "scope": "host_1",
    }
    assert started_event.causation_id == approved_event.id
    assert started_event.correlation_id == "corr_1"
    assert ledger.list_events("ws_1")[-1].correlation_id == "corr_1"


def test_pending_action_cannot_resume_before_approval(monkeypatch):
    executor, ledger, _projector = make_executor(
        policy_gate=PolicyGate({"echo.run": "L3"})
    )
    result = executor.execute("ws_1", "ses_1", "echo", {"message": "wait"})
    called = False

    def echo_would_fail(ctx, message):
        nonlocal called
        called = True
        return operations.echo(ctx, message)

    monkeypatch.setattr(operations, "echo", echo_would_fail)

    with pytest.raises(ValueError, match="only approved"):
        executor.resume_approved_tool_call("ws_1", result.pending_action.id)

    assert called is False
    assert event_kinds(ledger) == [
        "tool.approval.required",
        "pending_action.created",
    ]


def test_completed_action_cannot_resume_twice(monkeypatch):
    executor, ledger, _projector, pending_action = create_approved_echo_action(
        "once only"
    )
    call_count = 0
    original_echo = operations.echo

    def counting_echo(ctx, message):
        nonlocal call_count
        call_count += 1
        return original_echo(ctx, message)

    monkeypatch.setattr(operations, "echo", counting_echo)

    first_result = executor.resume_approved_tool_call("ws_1", pending_action.id)
    with pytest.raises(ValueError, match="'completed'"):
        executor.resume_approved_tool_call("ws_1", pending_action.id)

    assert first_result.status == "completed"
    assert call_count == 1
    assert event_kinds(ledger).count("tool.call.started") == 1
    assert event_kinds(ledger).count("pending_action.completed") == 1


def test_failed_resumed_tool_does_not_mark_completed(monkeypatch):
    executor, ledger, projector, pending_action = create_approved_echo_action("boom")

    def failing_echo(ctx, message):
        raise RuntimeError(f"failed echo: {message}")

    monkeypatch.setattr(operations, "echo", failing_echo)

    result = executor.resume_approved_tool_call("ws_1", pending_action.id)

    assert result.kind == "tool_failed"
    assert result.status == "failed"
    assert result.error == "failed echo: boom"
    assert projector.project("ws_1").pending_actions[pending_action.id].status == (
        "approved"
    )
    assert event_kinds(ledger) == [
        "tool.approval.required",
        "pending_action.created",
        "pending_action.approved",
        "tool.call.started",
        "tool.call.failed",
    ]
    assert "pending_action.completed" not in event_kinds(ledger)
