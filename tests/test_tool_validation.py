from __future__ import annotations

from seed_runtime.events import EventLedger
from seed_runtime.models import ToolSpec, Toolkit
from seed_runtime.registry import ToolRegistry
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
