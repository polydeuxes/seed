"""Validated registered-tool execution path."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any, Callable

from seed_runtime.events import EventLedger
from seed_runtime.models import RuntimeResponse, ToolSpec
from seed_runtime.policy import PolicyGate
from seed_runtime.registry import ToolRegistry
from seed_runtime.schema import validate_schema_value
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


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

    def execute(
        self,
        workspace_id: str,
        session_id: str | None,
        tool_name: str,
        arguments: dict[str, Any],
        *,
        causation_id: str | None = None,
        scope: str | None = None,
    ) -> RuntimeResponse:
        tool = self.registry.require(tool_name)
        validate_schema_value(tool.input_schema, arguments)
        state = self.projector.project(workspace_id)
        policy = self.policy_gate.evaluate(tool, state, scope=scope)
        if policy.outcome != "allow":
            self.ledger.append(
                "policy.action_gated",
                workspace_id,
                {"tool": tool.name, "policy": to_plain(policy)},
                actor="system",
                session_id=session_id,
                causation_id=causation_id,
            )
            return RuntimeResponse(policy.outcome, policy.reason, {"policy": to_plain(policy)})
        call_event = self.ledger.append(
            "tool.call.started",
            workspace_id,
            {"tool": tool.name, "arguments": arguments},
            actor="tool",
            session_id=session_id,
            causation_id=causation_id,
        )
        fn = self._load(tool)
        output = fn(ToolContext(self.ledger, workspace_id, session_id, tool.name, call_event.id), **arguments)
        validate_schema_value(tool.output_schema, output)
        self.ledger.append(
            "tool.call.completed",
            workspace_id,
            {"tool": tool.name, "output": output},
            actor="tool",
            session_id=session_id,
            causation_id=call_event.id,
        )
        return RuntimeResponse("tool_result", f"Tool {tool.name} completed.", {"output": output})

    def _load(self, tool: ToolSpec) -> Callable[..., dict[str, Any]]:
        module_name, function_name = tool.implementation.split(":", 1)
        module = importlib.import_module(module_name)
        fn = getattr(module, function_name)
        if not callable(fn):
            raise TypeError(f"implementation {tool.implementation!r} is not callable")
        return fn
