"""Validated registered-tool execution path."""

from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Any, Callable, Literal

from seed_runtime.base import SeedModel
from seed_runtime.events import EventLedger
from seed_runtime.fact_extraction import FactExtractionService
from seed_runtime.models import PendingAction, PolicyDecision, ToolSpec
from seed_runtime.pending_actions import PendingActionService
from seed_runtime.policy import PolicyGate
from seed_runtime.registry import ToolRegistry
from seed_runtime.tool_validation import ToolValidationService
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
    pending_action: PendingAction | None = None
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolContext:
    ledger: EventLedger
    workspace_id: str
    session_id: str | None
    tool_name: str
    call_event_id: str
    registry: ToolRegistry | None = None


class ToolExecutor:
    def __init__(
        self,
        ledger: EventLedger,
        registry: ToolRegistry,
        projector: StateProjector,
        policy_gate: PolicyGate | None = None,
        tool_validation: ToolValidationService | None = None,
    ) -> None:
        self.ledger = ledger
        self.registry = registry
        self.projector = projector
        self.policy_gate = policy_gate or PolicyGate()
        self.tool_validation = tool_validation or ToolValidationService(registry)
        self.fact_extraction = FactExtractionService(ledger)
        self.pending_actions = PendingActionService(ledger, projector)

    def execute(
        self,
        workspace_id: str,
        session_id: str | None,
        tool_name: str,
        arguments: dict[str, Any],
        *,
        causation_id: str | None = None,
        correlation_id: str | None = None,
        scope: str | None = None,
    ) -> ToolCallResult:
        tool = self.tool_validation.require_tool(tool_name)
        status_validation = self.tool_validation.validate_tool_status(tool)
        if not status_validation.ok:
            return self._failed(
                workspace_id,
                session_id,
                tool,
                status_validation.errors[0],
                causation_id=causation_id,
                correlation_id=correlation_id,
                phase="registration",
            )

        input_validation = self.tool_validation.validate_input_schema(tool, arguments)
        if not input_validation.ok:
            return self._failed(
                workspace_id,
                session_id,
                tool,
                input_validation.errors[0],
                causation_id=causation_id,
                correlation_id=correlation_id,
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
                arguments=arguments,
                scope=scope,
                causation_id=causation_id,
                correlation_id=correlation_id,
            )

        return self._execute_allowed_tool_call(
            workspace_id,
            session_id,
            tool,
            arguments,
            scope=scope,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )

    def resume_approved_tool_call(
        self,
        workspace_id: str,
        pending_action_id: str,
        session_id: str | None = None,
    ) -> ToolCallResult:
        """Execute an approved pending action's stored tool call exactly once."""
        state = self.projector.project(workspace_id)
        if pending_action_id not in state.pending_actions:
            raise ValueError(f"unknown pending action: {pending_action_id}")

        pending_action = state.pending_actions[pending_action_id]
        if pending_action.status != "approved":
            raise ValueError(
                "pending action "
                f"{pending_action_id} has status {pending_action.status!r}; "
                "only approved pending actions can be resumed"
            )

        causation_id, correlation_id = self._resume_event_context(
            workspace_id, pending_action
        )
        tool = self.registry.require(pending_action.tool_name)
        result = self._execute_allowed_tool_call(
            workspace_id,
            session_id,
            tool,
            pending_action.arguments,
            scope=pending_action.scope,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        if result.status == "completed":
            self.pending_actions.mark_completed(
                workspace_id,
                pending_action_id,
                session_id=session_id,
                causation_id=result.payload.get("completed_event_id") or causation_id,
                correlation_id=correlation_id,
            )
        return result

    def _execute_allowed_tool_call(
        self,
        workspace_id: str,
        session_id: str | None,
        tool: ToolSpec,
        arguments: dict[str, Any],
        *,
        scope: str | None,
        causation_id: str | None,
        correlation_id: str | None,
    ) -> ToolCallResult:
        started_payload = {"tool": tool.name, "arguments": to_plain(arguments)}
        if scope is not None:
            started_payload["scope"] = scope
        call_event = self.ledger.append(
            "tool.call.started",
            workspace_id,
            started_payload,
            actor="tool",
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )

        try:
            fn = self._load_registered(tool)
            output = fn(
                ToolContext(
                    self.ledger,
                    workspace_id,
                    session_id,
                    tool.name,
                    call_event.id,
                    self.registry,
                ),
                **arguments,
            )
            output_validation = self.tool_validation.validate_output_schema(tool, output)
            if not output_validation.ok:
                raise ValueError(output_validation.errors[0])
        except Exception as exc:
            failed_event = self.ledger.append(
                "tool.call.failed",
                workspace_id,
                {"tool": tool.name, "error": str(exc), "phase": "execution"},
                actor="tool",
                session_id=session_id,
                causation_id=call_event.id,
                correlation_id=correlation_id,
            )
            return ToolCallResult(
                kind="tool_failed",
                status="failed",
                tool_name=tool.name,
                message=f"Tool {tool.name} failed.",
                error=str(exc),
                payload={"error": str(exc), "failed_event_id": failed_event.id},
            )

        completed_event = self.ledger.append(
            "tool.call.completed",
            workspace_id,
            {"tool": tool.name, "output": output},
            actor="tool",
            session_id=session_id,
            causation_id=call_event.id,
            correlation_id=correlation_id,
        )
        self.fact_extraction.observe_tool_result(completed_event)
        return ToolCallResult(
            kind="tool_result",
            status="completed",
            tool_name=tool.name,
            message=f"Tool {tool.name} completed.",
            output=output,
            payload={"output": output, "completed_event_id": completed_event.id},
        )

    def _policy_denied(
        self,
        workspace_id: str,
        session_id: str | None,
        tool: ToolSpec,
        policy: PolicyDecision,
        *,
        arguments: dict[str, Any],
        scope: str | None,
        causation_id: str | None,
        correlation_id: str | None,
    ) -> ToolCallResult:
        event_kind = (
            "tool.policy.blocked" if policy.outcome == "block" else "tool.approval.required"
        )
        policy_payload = to_plain(policy)
        policy_event = self.ledger.append(
            event_kind,
            workspace_id,
            {"tool": tool.name, "policy": policy_payload},
            actor="system",
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        status = "blocked" if policy.outcome == "block" else policy.outcome
        pending_action = None
        payload = {"policy": policy_payload}
        if policy.outcome in {"require_confirmation", "require_approval"}:
            pending_action = self.pending_actions.create_tool_call(
                workspace_id,
                action=policy.action,
                tool_name=tool.name,
                arguments=arguments,
                scope=scope,
                session_id=session_id,
                created_from_event_id=policy_event.id,
                causation_id=causation_id,
                correlation_id=correlation_id,
            )
            payload["pending_action"] = to_plain(pending_action)
        return ToolCallResult(
            kind=policy.outcome,
            status=status,
            tool_name=tool.name,
            message=policy.reason,
            policy=policy_payload,
            pending_action=pending_action,
            payload=payload,
        )

    def _failed(
        self,
        workspace_id: str,
        session_id: str | None,
        tool: ToolSpec,
        error: str,
        *,
        causation_id: str | None,
        correlation_id: str | None,
        phase: str,
    ) -> ToolCallResult:
        self.ledger.append(
            "tool.call.failed",
            workspace_id,
            {"tool": tool.name, "error": error, "phase": phase},
            actor="tool",
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        return ToolCallResult(
            kind="tool_failed",
            status="failed",
            tool_name=tool.name,
            message=f"Tool {tool.name} failed.",
            error=error,
            payload={"error": error},
        )

    def _resume_event_context(
        self, workspace_id: str, pending_action: PendingAction
    ) -> tuple[str | None, str | None]:
        causation_id = pending_action.created_from_event_id or pending_action.causation_id
        correlation_id = None
        created_event = None

        for event in reversed(self.ledger.list_events(workspace_id)):
            if event.kind == "pending_action.created":
                event_action = event.payload.get("pending_action", {})
                if event_action.get("id") == pending_action.id:
                    created_event = event
                    if correlation_id is None:
                        correlation_id = event.correlation_id
                    continue

            if event.kind not in {
                "pending_action.approved",
                "pending_action.status_changed",
            }:
                continue
            if event.payload.get("pending_action_id") != pending_action.id:
                continue
            if event.payload.get("status", "approved") != "approved":
                continue
            causation_id = event.id
            correlation_id = event.correlation_id or correlation_id
            break

        if correlation_id is None and created_event is not None:
            correlation_id = created_event.correlation_id
        if correlation_id is None and pending_action.created_from_event_id is not None:
            source_event = self.ledger.get(pending_action.created_from_event_id)
            if source_event is not None:
                correlation_id = source_event.correlation_id
        if correlation_id is None and pending_action.causation_id is not None:
            source_event = self.ledger.get(pending_action.causation_id)
            if source_event is not None:
                correlation_id = source_event.correlation_id

        return causation_id, correlation_id

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
