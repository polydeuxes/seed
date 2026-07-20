from __future__ import annotations

from seed_runtime.context import DecisionInputComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision, ToolSpec, Toolkit
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import StaticDecisionProducer, Runtime
from seed_runtime.state import StateProjector
from seed_runtime.tool_intent import ToolIntentValidation
from seed_runtime.tool_needs import ToolNeedService
from seed_runtime.tool_validation import ToolValidationService
from toolkits.core.echo import operations


def make_registry(*, tool_status: str = "registered") -> ToolRegistry:
    registry = ToolRegistry()
    registry.register_toolkit(
        Toolkit(
            id="tk_validation_echo",
            name="validation echo",
            summary="Tool validation test operations.",
            tools=[
                ToolSpec(
                    toolkit_id="tk_validation_echo",
                    name="echo",
                    summary="Echo a message deterministically.",
                    input_schema={
                        "type": "object",
                        "properties": {"message": {"type": "string"}},
                        "required": ["message"],
                    },
                    output_schema={
                        "type": "object",
                        "properties": {"ok": {"type": "boolean"}},
                        "required": ["ok"],
                    },
                    policy_action="echo.run",
                    implementation="toolkits.core.echo.operations:echo",
                    risk_class="L1",
                    status=tool_status,
                )
            ],
        )
    )
    return registry


def make_runtime(decision: Decision, registry: ToolRegistry | None = None):
    ledger = EventLedger()
    registry = registry or make_registry()
    projector = StateProjector(ledger)
    runtime = Runtime(
        ledger,
        projector,
        DecisionInputComposer(registry),
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        StaticDecisionProducer(decision),
    )
    return runtime, ledger


def event_kinds(ledger: EventLedger, workspace_id: str = "ws") -> list[str]:
    return [event.kind for event in ledger.list_events(workspace_id)]


def test_shared_service_preserves_tool_existence_and_input_schema_rules():
    registry = make_registry()
    service = ToolValidationService(registry)

    missing = service.validate_tool_exists("missing")
    invalid_input = service.validate_tool_input("echo", {"message": 123})
    valid_input = service.validate_tool_input("echo", {"message": "hello"})

    assert missing.ok is False
    assert missing.errors == ["unknown tool 'missing'"]
    assert invalid_input.ok is False
    assert invalid_input.errors == ["$.message must be a string"]
    assert valid_input.ok is True
    assert valid_input.tool is registry.require("echo")


def test_shared_service_preserves_tool_status_validation_rule():
    registry = make_registry(tool_status="disabled")
    service = ToolValidationService(registry)
    tool = registry.require("echo")

    validation = service.validate_tool_status(tool)

    assert validation.ok is False
    assert validation.errors == ["tool 'echo' is not registered"]
    assert validation.tool is tool


def test_shared_service_preserves_output_schema_validation_rule():
    registry = make_registry()
    service = ToolValidationService(registry)
    tool = registry.require("echo")

    validation = service.validate_output_schema(tool, {"ok": "yes"})

    assert validation.ok is False
    assert validation.errors == ["$.ok must be a boolean"]
    assert validation.tool is tool


def test_runtime_still_rejects_unknown_tool_during_decision_validation():
    runtime, ledger = make_runtime(
        Decision(
            kind="call_tool",
            reason="bad tool",
            tool_name="missing",
            tool_arguments={},
        )
    )

    response = runtime.handle_user_message("ws", "ses", "run missing")

    assert response.kind == "invalid_decision"
    assert response.payload == {"errors": ["unknown tool 'missing'"]}
    assert event_kinds(ledger) == [
        "input.user_message",
        "model.decision.proposed",
        "model.decision.invalid",
        "model.decision.proposed",
        "model.decision.invalid",
    ]


def test_runtime_still_rejects_invalid_input_schema_before_execution(monkeypatch):
    called = False

    def echo_would_fail(ctx, message):
        nonlocal called
        called = True
        return operations.echo(ctx, message)

    monkeypatch.setattr(operations, "echo", echo_would_fail)
    runtime, ledger = make_runtime(
        Decision(
            kind="call_tool",
            reason="bad args",
            tool_name="echo",
            tool_arguments={"message": 123},
        )
    )

    response = runtime.handle_user_message("ws", "ses", "echo bad")

    assert response.kind == "invalid_decision"
    assert response.payload == {"errors": ["$.message must be a string"]}
    assert called is False
    assert "tool.call.started" not in event_kinds(ledger)


def test_runtime_still_rejects_unregistered_tool_status_before_execution(monkeypatch):
    called = False

    def echo_would_fail(ctx, message):
        nonlocal called
        called = True
        return operations.echo(ctx, message)

    monkeypatch.setattr(operations, "echo", echo_would_fail)
    runtime, ledger = make_runtime(
        Decision(
            kind="call_tool",
            reason="disabled",
            tool_name="echo",
            tool_arguments={"message": "hello"},
        ),
        registry=make_registry(tool_status="disabled"),
    )

    runtime.tool_intent_guard.validate = (
        lambda current_input_text, decision, visible_tools: ToolIntentValidation(
            ok=True, errors=[]
        )
    )

    response = runtime.handle_user_message("ws", "ses", "echo hello")

    assert response.kind == "tool_failed"
    assert response.message == "Tool echo failed."
    assert response.payload["error"] == "tool 'echo' is not registered"
    assert called is False
    assert event_kinds(ledger) == [
        "input.user_message",
        "model.decision.proposed",
        "tool.call.failed",
    ]
    assert ledger.list_events("ws")[-1].payload["phase"] == "registration"


def test_runtime_still_rejects_invalid_output_schema_after_start(monkeypatch):
    def invalid_echo(ctx, message):
        return {"ok": "yes"}

    monkeypatch.setattr(operations, "echo", invalid_echo)
    runtime, ledger = make_runtime(
        Decision(
            kind="call_tool",
            reason="bad output",
            tool_name="echo",
            tool_arguments={"message": "hello"},
        )
    )

    response = runtime.handle_user_message("ws", "ses", "echo hello")

    assert response.kind == "tool_failed"
    assert response.payload["error"] == "$.ok must be a boolean"
    assert event_kinds(ledger) == [
        "input.user_message",
        "model.decision.proposed",
        "tool.call.started",
        "tool.call.failed",
    ]
    assert ledger.list_events("ws")[-1].payload["phase"] == "execution"


def test_operation_selection_resolves_one_registered_operation_without_recommendations():
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    service = ToolValidationService(registry)

    selection = service.select_operation("echo")

    assert selection.ok is True
    assert selection.errors == []
    assert selection.operation is not None
    assert selection.operation.name == "echo"


def test_operation_selection_preserves_unknown_tool_error_message():
    service = ToolValidationService(ToolRegistry())

    selection = service.select_operation("missing_tool")
    validation = service.validate_tool_input("missing_tool", {})

    assert selection.ok is False
    assert selection.errors == ["unknown tool 'missing_tool'"]
    assert validation.errors == ["unknown tool 'missing_tool'"]
