"""State projection from append-only events."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from seed_runtime.events import EventLedger
from seed_runtime.models import Approval, Entity, Event, Fact, Goal, ToolNeed, ToolSpec


def _parse_dt(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


@dataclass
class State:
    workspace_id: str
    entities: dict[str, Entity] = field(default_factory=dict)
    facts: dict[str, Fact] = field(default_factory=dict)
    goals: dict[str, Goal] = field(default_factory=dict)
    tool_needs: dict[str, ToolNeed] = field(default_factory=dict)
    approvals: dict[str, Approval] = field(default_factory=dict)
    tools: dict[str, ToolSpec] = field(default_factory=dict)

    @property
    def open_tool_needs(self) -> list[ToolNeed]:
        closed = {"registered", "rejected"}
        return [need for need in self.tool_needs.values() if need.status not in closed]

    def has_approval(self, action: str, scope: str | None = None) -> Approval | None:
        now = datetime.now().astimezone()
        for approval in self.approvals.values():
            if approval.action != action:
                continue
            if scope is not None and approval.scope != scope:
                continue
            if approval.expires_at is not None and approval.expires_at < now:
                continue
            return approval
        return None


class StateProjector:
    """Rebuild current inspectable state from ledger events."""

    def __init__(self, ledger: EventLedger) -> None:
        self.ledger = ledger

    def project(self, workspace_id: str) -> State:
        state = State(workspace_id=workspace_id)
        for event in self.ledger.list_events(workspace_id):
            self.apply(state, event)
        return state

    def apply(self, state: State, event: Event) -> None:
        payload = event.payload
        if event.kind == "entity.upserted":
            data = payload.get("entity", payload)
            entity = Entity(**data)
            state.entities[entity.id] = entity
        elif event.kind == "fact.observed":
            data = payload.get("fact", payload).copy()
            data["observed_at"] = _parse_dt(data.get("observed_at")) or event.timestamp
            data["expires_at"] = _parse_dt(data.get("expires_at"))
            fact = Fact(**data)
            state.facts[fact.id] = fact
        elif event.kind == "goal.created":
            data = payload.get("goal", payload)
            goal = Goal(**data)
            state.goals[goal.id] = goal
        elif event.kind == "tool_need.created":
            data = payload.get("tool_need", payload)
            need = ToolNeed(**data)
            state.tool_needs[need.id] = need
        elif event.kind == "tool_need.status_changed":
            need_id = payload["tool_need_id"]
            if need_id in state.tool_needs:
                current = state.tool_needs[need_id]
                state.tool_needs[need_id] = ToolNeed(
                    **{**current.__dict__, "status": payload["status"]}
                )
        elif event.kind == "approval.granted":
            data = payload.get("approval", payload).copy()
            data["expires_at"] = _parse_dt(data.get("expires_at"))
            approval = Approval(**data)
            state.approvals[approval.id] = approval
        elif event.kind == "tool.registered":
            data = payload.get("tool", payload)
            tool = ToolSpec(**data)
            state.tools[tool.name] = tool
