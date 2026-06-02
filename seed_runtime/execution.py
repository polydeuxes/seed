"""Validated registered-tool execution path."""

from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Any, Callable, Literal

from seed_runtime.base import SeedModel
from seed_runtime.events import EventLedger
from seed_runtime.fact_extraction import FactExtractionService
from seed_runtime.models import PolicyDecision, ToolSpec
from seed_runtime.policy import PolicyGate
from seed_runtime.registry import ToolRegistry
from seed_runtime.schema import SchemaValidationError, validate_schema_value
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


ToolCallStatus = Literal[
    "completed",
    "failed",
    "blocked",
    "require_confirmation",
    "require_approval",
]


class ToolCallResult(SeedModel):
    """Structured result returned by the Seed tool executor."""

    kind: str
    status: ToolCallStatus
    tool_name: str
    message: str
    output: dict[str, Any] | None = None
    error: str | None = None
    policy: dict[str, Any] | None = None
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolContext:
    ledger: EventLedger
    workspace_id: str
    session_id: str | None
    tool_name: str
    call_event_id: str


class ToolExecutor:
    def __init__(
        self,
        ledger: EventLedger,
        registry: ToolRegistry,
        projector: StateProjector,
        policy_gate: PolicyGate | None = None,
    ) -> None:
        self.ledger = ledger
        self.registry = registry
        self.projector = projector
        self.policy_gate = policy_gate or PolicyGate()
        self.fact_extraction = FactExtractionService(ledger)

    def execute(
        self,
        workspace_id: str,
        session_id: str | None,
        tool_name: str,
        arguments: dict[str, Any],
        *,
        causation_id: str | None = None,
        scope: str | None = None,
    ) -> ToolCallResult:
        tool = self.registry.require(tool_name)
        if tool.status != "registered":
            return self._failed(
                workspace_id,
                session_id,
                tool,
                f"tool {tool.name!r} is not registered",
                causation_id=causation_id,
                phase="registration",
            )

        try:
            validate_schema_value(tool.input_schema, arguments)
        except SchemaValidationError as exc:
            return self._failed(
                workspace_id,
                session_id,
                tool,
                str(exc),
                causation_id=causation_id,
                phase="input_validation",
            )

        state = self.projector.project(workspace_id)
        policy = self.policy_gate.evaluate(tool, state, scope=scope)
        if policy.outcome != "allow":
            return self._policy_denied(
                workspace_id,
                session_id,
                tool,
                policy,
                causation_id=causation_id,
            )

        call_event = self.ledger.append(
            "tool.call.started",
            workspace_id,
            {"tool": tool.name, "arguments": arguments},
            actor="tool",
            session_id=session_id,
            causation_id=causation_id,
        )

        try:
            fn = self._load_registered(tool)
            output = fn(
                ToolContext(
                    self.ledger, workspace_id, session_id, tool.name, call_event.id
                ),
                **arguments,
            )
            validate_schema_value(tool.output_schema, output)
        except Exception as exc:
            self.ledger.append(
                "tool.call.failed",
                workspace_id,
                {"tool": tool.name, "error": str(exc), "phase": "execution"},
                actor="tool",
                session_id=session_id,
                causation_id=call_event.id,
            )
            return ToolCallResult(
                kind="tool_failed",
                status="failed",
                tool_name=tool.name,
                message=f"Tool {tool.name} failed.",
                error=str(exc),
                payload={"error": str(exc)},
            )

        completed_event = self.ledger.append(
            "tool.call.completed",
            workspace_id,
            {"tool": tool.name, "output": output},
            actor="tool",
            session_id=session_id,
            causation_id=call_event.id,
        )
        self.fact_extraction.observe_tool_result(completed_event)
        return ToolCallResult(
            kind="tool_result",
            status="completed",
            tool_name=tool.name,
            message=f"Tool {tool.name} completed.",
            output=output,
            payload={"output": output},
        )

    def _policy_denied(
        self,
        workspace_id: str,
        session_id: str | None,
        tool: ToolSpec,
        policy: PolicyDecision,
        *,
        causation_id: str | None,
    ) -> ToolCallResult:
        event_kind = (
            "tool.policy.blocked" if policy.outcome == "block" else "tool.approval.required"
        )
        policy_payload = to_plain(policy)
        self.ledger.append(
            event_kind,
            workspace_id,
            {"tool": tool.name, "policy": policy_payload},
            actor="system",
            session_id=session_id,
            causation_id=causation_id,
        )
        status = "blocked" if policy.outcome == "block" else policy.outcome
        return ToolCallResult(
            kind=policy.outcome,
            status=status,
            tool_name=tool.name,
            message=policy.reason,
            policy=policy_payload,
            payload={"policy": policy_payload},
        )

    def _failed(
        self,
        workspace_id: str,
        session_id: str | None,
        tool: ToolSpec,
        error: str,
        *,
        causation_id: str | None,
        phase: str,
    ) -> ToolCallResult:
        self.ledger.append(
            "tool.call.failed",
            workspace_id,
            {"tool": tool.name, "error": error, "phase": phase},
            actor="tool",
            session_id=session_id,
            causation_id=causation_id,
        )
        return ToolCallResult(
            kind="tool_failed",
            status="failed",
            tool_name=tool.name,
            message=f"Tool {tool.name} failed.",
            error=error,
            payload={"error": error},
        )

    def _load_registered(self, tool: ToolSpec) -> Callable[..., dict[str, Any]]:
        registered = self.registry.get(tool.name)
        if registered is None or registered.implementation != tool.implementation:
            raise ValueError(f"implementation for tool {tool.name!r} is not registered")
        if ":" not in tool.implementation:
            raise ValueError(f"invalid implementation reference {tool.implementation!r}")
        module_name, function_name = tool.implementation.split(":", 1)
        module = importlib.import_module(module_name)
        fn = getattr(module, function_name)
        if not callable(fn):
            raise TypeError(f"implementation {tool.implementation!r} is not callable")
        return fn
