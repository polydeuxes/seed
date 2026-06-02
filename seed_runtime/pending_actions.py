"""Pending actions for tool calls awaiting human approval or confirmation."""

from __future__ import annotations

from typing import Any

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.models import PendingAction, PendingActionStatus
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


class PendingActionService:
    """Append and update pending tool-call actions in the event ledger."""

    def __init__(self, ledger: EventLedger, projector: StateProjector) -> None:
        self.ledger = ledger
        self.projector = projector

    def create_tool_call(
        self,
        workspace_id: str,
        *,
        action: str,
        tool_name: str,
        arguments: dict[str, Any],
        scope: str | None = None,
        session_id: str | None = None,
        created_from_event_id: str | None = None,
        causation_id: str | None = None,
    ) -> PendingAction:
        """Create a pending action for a tool call that must not execute yet."""
        pending_action = PendingAction(
            id=new_id("pa"),
            workspace_id=workspace_id,
            action=action,
            tool_name=tool_name,
            arguments=to_plain(arguments),
            scope=scope,
            status="pending",
            created_from_event_id=created_from_event_id,
            causation_id=causation_id,
        )
        self.ledger.append(
            "pending_action.created",
            workspace_id,
            {"pending_action": to_plain(pending_action)},
            actor="system",
            session_id=session_id,
            causation_id=created_from_event_id or causation_id,
        )
        return pending_action

    def mark_approved(
        self,
        workspace_id: str,
        pending_action_id: str,
        *,
        session_id: str | None = None,
        causation_id: str | None = None,
    ) -> PendingAction:
        """Mark a projected pending action as approved without resuming it."""
        return self._set_status(
            workspace_id,
            pending_action_id,
            "approved",
            session_id=session_id,
            causation_id=causation_id,
        )

    def mark_completed(
        self,
        workspace_id: str,
        pending_action_id: str,
        *,
        session_id: str | None = None,
        causation_id: str | None = None,
    ) -> PendingAction:
        """Mark a projected pending action as completed after external execution."""
        return self._set_status(
            workspace_id,
            pending_action_id,
            "completed",
            session_id=session_id,
            causation_id=causation_id,
        )

    def _set_status(
        self,
        workspace_id: str,
        pending_action_id: str,
        status: PendingActionStatus,
        *,
        session_id: str | None,
        causation_id: str | None,
    ) -> PendingAction:
        state = self.projector.project(workspace_id)
        if pending_action_id not in state.pending_actions:
            raise ValueError(f"unknown pending action: {pending_action_id}")

        pending_action = state.pending_actions[pending_action_id].model_copy(
            update={"status": status}
        )
        event_kind = f"pending_action.{status}"
        self.ledger.append(
            event_kind,
            workspace_id,
            {"pending_action_id": pending_action_id, "status": status},
            actor="approver" if status == "approved" else "system",
            session_id=session_id,
            causation_id=causation_id,
        )
        return pending_action
