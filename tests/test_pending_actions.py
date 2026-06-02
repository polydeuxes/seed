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


def test_approval_required_tool_does_not_execute(monkeypatch):
    executor, ledger, _projector = make_executor(
        policy_gate=PolicyGate({"echo.run": "L3"})
    )
    called = False

    def echo_would_fail(ctx, message):
        nonlocal called
        called = True
        return operations.echo(ctx, message)

    monkeypatch.setattr(operations, "echo", echo_would_fail)

    result = executor.execute(
        "ws_1", "ses_1", "echo", {"message": "needs approval"}, scope="host_1"
    )

    assert result.kind == "require_approval"
    assert result.status == "require_approval"
    assert called is False
    assert event_kinds(ledger) == [
        "tool.approval.required",
        "pending_action.created",
    ]
    assert result.pending_action is not None
    assert result.pending_action.status == "pending"
    assert result.pending_action.action == "echo.run"
    assert result.pending_action.tool_name == "echo"
    assert result.pending_action.arguments == {"message": "needs approval"}
    assert result.pending_action.scope == "host_1"


def test_pending_action_is_projected_in_state():
    executor, _ledger, projector = make_executor(
        policy_gate=PolicyGate({"echo.run": "L2"})
    )

    result = executor.execute(
        "ws_1", "ses_1", "echo", {"message": "confirm first"}, scope="host_2"
    )

    state = projector.project("ws_1")
    pending_action = state.pending_actions[result.pending_action.id]
    assert pending_action.status == "pending"
    assert pending_action.workspace_id == "ws_1"
    assert pending_action.action == "echo.run"
    assert pending_action.tool_name == "echo"
    assert pending_action.arguments == {"message": "confirm first"}
    assert pending_action.scope == "host_2"
    assert pending_action.created_from_event_id is not None
    assert pending_action.causation_id is None


def test_approval_event_can_mark_pending_action_approved():
    executor, ledger, projector = make_executor(
        policy_gate=PolicyGate({"echo.run": "L3"})
    )
    result = executor.execute(
        "ws_1", "ses_1", "echo", {"message": "approve later"}, scope="host_3"
    )
    service = PendingActionService(ledger, projector)

    approved = service.mark_approved(
        "ws_1", result.pending_action.id, causation_id="approval_evt_1"
    )

    state = projector.project("ws_1")
    assert approved.status == "approved"
    assert state.pending_actions[result.pending_action.id].status == "approved"
    assert event_kinds(ledger) == [
        "tool.approval.required",
        "pending_action.created",
        "pending_action.approved",
    ]
    assert ledger.list_events("ws_1")[-1].actor == "approver"
    assert ledger.list_events("ws_1")[-1].causation_id == "approval_evt_1"
