"""Compact context packets for model decisions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.models import Event
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import State


@dataclass(frozen=True)
class ContextPacket:
    workspace_id: str
    session_id: str | None
    current_input: dict[str, Any]
    active_goal: dict[str, Any] | None
    entities: list[dict[str, Any]]
    facts: list[dict[str, Any]]
    tools: list[dict[str, Any]]
    open_tool_needs: list[dict[str, Any]]
    decision_schema: dict[str, Any]
    retry_prompt: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class ContextComposer:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def compose(
        self,
        workspace_id: str,
        session_id: str | None,
        input_event: Event,
        state: State,
    ) -> ContextPacket:
        active_goals = [
            goal for goal in state.goals.values() if goal.status == "active"
        ]
        active_goal = (
            min(active_goals, key=lambda goal: goal.id).__dict__
            if active_goals
            else None
        )
        entities = [
            entity.__dict__
            for entity in sorted(
                state.entities.values(), key=lambda entity: entity.name
            )[:20]
        ]
        facts = [
            fact.__dict__
            for fact in sorted(state.facts.values(), key=lambda fact: fact.id)[:30]
        ]
        tools = [
            {
                "name": tool.name,
                "summary": tool.summary,
                "input_schema": tool.input_schema,
                "policy_action": tool.policy_action,
                "risk_class": tool.risk_class,
            }
            for tool in self.registry.list_tools(visible_only=True)
        ]
        open_needs = [
            need.__dict__
            for need in sorted(state.open_tool_needs, key=lambda need: need.name)
        ]
        return ContextPacket(
            workspace_id=workspace_id,
            session_id=session_id,
            current_input={"event_id": input_event.id, **input_event.payload},
            active_goal=active_goal,
            entities=entities,
            facts=facts,
            tools=tools,
            open_tool_needs=open_needs,
            decision_schema={
                "kinds": [
                    "answer",
                    "ask_question",
                    "call_tool",
                    "request_tool",
                    "refuse",
                ]
            },
        )
