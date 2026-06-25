"""Compact context packets for model decisions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from seed_runtime.context_budget import (
    ACTIVE_GOALS,
    CURRENT_INPUT,
    ENTITIES,
    OPEN_TOOL_NEEDS,
    RECENT_EVIDENCE,
    RECENT_FACTS,
    ContextBudget,
)
from seed_runtime.context_selection import (
    order_entities,
    order_evidence,
    order_facts,
    order_goals,
)
from seed_runtime.models import Event
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import State


@dataclass(frozen=True)
class DecisionInputPacket:
    workspace_id: str
    session_id: str | None
    current_input: dict[str, Any]
    active_goal: dict[str, Any] | None
    entities: list[dict[str, Any]]
    facts: list[dict[str, Any]]
    tools: list[dict[str, Any]]
    open_tool_needs: list[dict[str, Any]]
    decision_schema: dict[str, Any]
    evidence: list[dict[str, Any]] = field(default_factory=list)
    retry_prompt: dict[str, Any] | None = None
    context_budget: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class DecisionInputComposer:
    def __init__(
        self, registry: ToolRegistry, budget: ContextBudget | None = None
    ) -> None:
        self.registry = registry
        self.budget = budget or ContextBudget()

    def compose(
        self,
        workspace_id: str,
        session_id: str | None,
        input_event: Event,
        state: State,
    ) -> DecisionInputPacket:
        ordered_goals = order_goals(state.goals.values())
        ordered_entities = order_entities(state.entities.values())
        ordered_facts = order_facts(state.facts.values())
        ordered_evidence = order_evidence(state.evidence.values())
        open_needs_by_name = sorted(state.open_tool_needs, key=lambda need: need.name)
        budgeted = self.budget.select_sections(
            {
                CURRENT_INPUT: [{"event_id": input_event.id, **input_event.payload}],
                ACTIVE_GOALS: ordered_goals,
                OPEN_TOOL_NEEDS: open_needs_by_name,
                RECENT_FACTS: ordered_facts,
                RECENT_EVIDENCE: ordered_evidence,
                ENTITIES: ordered_entities,
            }
        )

        active_goal = (
            budgeted.sections[ACTIVE_GOALS][0].__dict__
            if budgeted.sections[ACTIVE_GOALS]
            else None
        )
        entities = [entity.__dict__ for entity in budgeted.sections[ENTITIES]]
        selected_evidence_ids = {
            item.id for item in budgeted.sections[RECENT_EVIDENCE]
        }
        facts = []
        for fact in budgeted.sections[RECENT_FACTS]:
            fact_payload = fact.__dict__.copy()
            if not fact.inferred:
                fact_payload.pop("source_fact_id", None)
                fact_payload.pop("inference_rule_id", None)
            fact_payload["evidence"] = [
                state.evidence[evidence_id].__dict__
                for evidence_id in fact.evidence_ids
                if evidence_id in selected_evidence_ids
                and evidence_id in state.evidence
            ]
            facts.append(fact_payload)
        evidence = [item.__dict__ for item in budgeted.sections[RECENT_EVIDENCE]]
        tools = [
            {
                "name": tool.name,
                "summary": tool.summary,
                "input_schema": tool.input_schema,
                "output_schema": tool.output_schema,
                "policy_action": tool.policy_action,
                "risk_class": tool.risk_class,
            }
            for tool in self.registry.list_tools(visible_only=True)
        ]
        open_needs = [need.__dict__ for need in budgeted.sections[OPEN_TOOL_NEEDS]]
        return DecisionInputPacket(
            workspace_id=workspace_id,
            session_id=session_id,
            current_input=(
                budgeted.sections[CURRENT_INPUT][0]
                if budgeted.sections[CURRENT_INPUT]
                else {}
            ),
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
            evidence=evidence,
            context_budget=budgeted.trace.to_dict(),
        )


# Compatibility aliases for the former public runtime decision-input names.
ContextPacket = DecisionInputPacket
ContextComposer = DecisionInputComposer
