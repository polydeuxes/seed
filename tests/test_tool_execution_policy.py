from __future__ import annotations

from seed_runtime.events import EventLedger
from seed_runtime.models import ToolSpec, Toolkit
from seed_runtime.policy import PolicyGate
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import State, StateProjector
from seed_runtime.tool_execution_policy import ToolExecutionPolicyService


def make_tool(name: str, risk_class: str, *, status: str = "registered") -> ToolSpec:
    return ToolSpec(
        toolkit_id="tk_policy",
        name=name,
        summary=f"{name} tool.",
        input_schema={
            "type": "object",
            "required": ["message"],
            "properties": {"message": {"type": "string"}},
            "additionalProperties": False,
        },
        output_schema={"type": "object"},
        policy_action=f"{name}.run",
        implementation="toolkits.core.echo.operations:echo",
        status=status,
        risk_class=risk_class,
    )


def make_registry(*tools: ToolSpec) -> ToolRegistry:
    registry = ToolRegistry()
    registry.register_toolkit(
        Toolkit(
            id="tk_policy",
            name="policy tools",
            summary="Policy test tools.",
            tools=list(tools),
        )
    )
    return registry


def projected_state(workspace_id: str = "ws") -> State:
    return StateProjector(EventLedger()).project(workspace_id)


def make_service(registry: ToolRegistry) -> ToolExecutionPolicyService:
    return ToolExecutionPolicyService(registry, policy_engine=PolicyGate())


def test_unknown_tool_returns_validation_failure_and_no_policy():
    service = make_service(make_registry(make_tool("safe", "L1")))

    result = service.evaluate(
        tool_name="missing", arguments={"message": "hello"}, state=projected_state()
    )

    assert result.tool is None
    assert result.validation.ok is False
    assert result.validation.errors == ["unknown tool 'missing'"]
    assert result.validation_phase == "existence"
    assert result.policy is None
    assert result.allowed_to_execute is False
    assert result.error == "unknown tool 'missing'"


def test_disabled_unregistered_tool_returns_validation_failure_and_no_policy():
    disabled = make_tool("disabled", "L1", status="disabled")
    service = make_service(make_registry(disabled))

    result = service.evaluate(
        tool_name="disabled", arguments={"message": "hello"}, state=projected_state()
    )

    assert result.tool is disabled
    assert result.validation.ok is False
    assert result.validation.errors == ["tool 'disabled' is not registered"]
    assert result.validation_phase == "status"
    assert result.policy is None
    assert result.allowed_to_execute is False
    assert result.error == "tool 'disabled' is not registered"


def test_invalid_input_returns_validation_failure_and_no_policy():
    tool = make_tool("safe", "L1")
    service = make_service(make_registry(tool))

    result = service.evaluate(
        tool_name="safe", arguments={"message": 123}, state=projected_state()
    )

    assert result.tool is tool
    assert result.validation.ok is False
    assert result.validation.errors == ["$.message must be a string"]
    assert result.validation_phase == "input"
    assert result.policy is None
    assert result.allowed_to_execute is False
    assert result.error == "$.message must be a string"


def test_valid_input_returns_policy_result():
    tool = make_tool("safe", "L1")
    service = make_service(make_registry(tool))

    result = service.evaluate(
        tool_name="safe", arguments={"message": "hello"}, state=projected_state()
    )

    assert result.tool is tool
    assert result.validation.ok is True
    assert result.policy is not None
    assert result.policy.action == "safe.run"
    assert result.validation_phase is None
    assert result.error is None


def test_l1_tool_returns_allow():
    tool = make_tool("safe", "L1")
    service = make_service(make_registry(tool))

    result = service.evaluate(
        tool_name="safe", arguments={"message": "hello"}, state=projected_state()
    )

    assert result.policy is not None
    assert result.policy.outcome == "allow"
    assert result.allowed_to_execute is True


def test_l2_tool_returns_require_confirmation():
    tool = make_tool("confirm", "L2")
    service = make_service(make_registry(tool))

    result = service.evaluate(
        tool_name="confirm", arguments={"message": "hello"}, state=projected_state()
    )

    assert result.policy is not None
    assert result.policy.outcome == "require_confirmation"
    assert result.allowed_to_execute is False


def test_l3_tool_returns_require_approval():
    tool = make_tool("approve", "L3")
    service = make_service(make_registry(tool))

    result = service.evaluate(
        tool_name="approve", arguments={"message": "hello"}, state=projected_state()
    )

    assert result.policy is not None
    assert result.policy.outcome == "require_approval"
    assert result.allowed_to_execute is False


def test_l4_tool_returns_block():
    tool = make_tool("block", "L4")
    service = make_service(make_registry(tool))

    result = service.evaluate(
        tool_name="block", arguments={"message": "hello"}, state=projected_state()
    )

    assert result.policy is not None
    assert result.policy.outcome == "block"
    assert result.allowed_to_execute is False


def test_service_appends_no_events():
    ledger = EventLedger()
    registry = make_registry(make_tool("safe", "L1"))
    service = ToolExecutionPolicyService(registry, policy_engine=PolicyGate())
    state = StateProjector(ledger).project("ws")

    result = service.evaluate(
        tool_name="safe", arguments={"message": "hello"}, state=state
    )

    assert result.policy is not None
    assert ledger.list_events("ws") == []
