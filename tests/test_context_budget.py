from datetime import timedelta

from seed_runtime.context import DecisionInputComposer
from seed_runtime.context_budget import (
    ACTIVE_GOALS,
    CURRENT_INPUT,
    ENTITIES,
    OPEN_TOOL_NEEDS,
    RECENT_FACTS,
    ContextBudget,
)
from seed_runtime.evidence import Evidence
from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.models import Entity, Goal, ToolNeed, utc_now
from seed_runtime.registry import ToolRegistry
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def test_context_budget_selects_higher_priority_sections_first():
    budget = ContextBudget(max_items=3)

    selected = budget.select_sections(
        {
            ENTITIES: ["entity"],
            RECENT_FACTS: ["fact"],
            OPEN_TOOL_NEEDS: ["need"],
            ACTIVE_GOALS: ["goal"],
            CURRENT_INPUT: ["input"],
        }
    )

    assert selected.sections[CURRENT_INPUT] == ["input"]
    assert selected.sections[ACTIVE_GOALS] == ["goal"]
    assert selected.sections[OPEN_TOOL_NEEDS] == ["need"]
    assert selected.sections[RECENT_FACTS] == []
    assert selected.sections[ENTITIES] == []
    assert selected.trace.section_order == [
        CURRENT_INPUT,
        ACTIVE_GOALS,
        OPEN_TOOL_NEEDS,
        RECENT_FACTS,
        ENTITIES,
    ]
    assert selected.trace.dropped_counts[RECENT_FACTS] == 1


def test_context_budget_applies_section_limits_without_token_counting():
    budget = ContextBudget(section_limits={RECENT_FACTS: 2})

    selected = budget.select_sections({RECENT_FACTS: ["new", "middle", "old"]})

    assert selected.sections[RECENT_FACTS] == ["new", "middle"]
    assert selected.trace.selected_counts[RECENT_FACTS] == 2
    assert selected.trace.dropped_counts[RECENT_FACTS] == 1


def test_decision_input_composer_uses_budget_for_priority_and_recency_selection():
    ledger = EventLedger()
    workspace_id = "ws_budget"
    base_time = utc_now()
    ledger.append(
        "goal.created",
        workspace_id,
        {
            "goal": to_plain(
                Goal(id="goal_1", workspace_id=workspace_id, summary="Fix SSH")
            )
        },
    )
    ledger.append(
        "tool_need.created",
        workspace_id,
        {
            "tool_need": to_plain(
                ToolNeed(
                    id="need_1",
                    workspace_id=workspace_id,
                    name="install_ssh",
                    summary="Install SSH",
                    capability="ssh_access",
                    reason="missing",
                )
            )
        },
    )
    ledger.append(
        "entity.upserted",
        workspace_id,
        {"entity": to_plain(Entity(id="ent_1", kind="host", name="example_host"))},
    )
    for index in range(3):
        observed_at = base_time + timedelta(minutes=index)
        evidence = Evidence(
            id=f"evd_{index}",
            workspace_id=workspace_id,
            source="test",
            kind="status",
            observed_at=observed_at,
            payload={"index": index},
        )
        fact = Fact(
            id=f"fact_{index}",
            subject_id="ent_1",
            predicate="ssh.running",
            value=bool(index),
            evidence_ids=[evidence.id],
            observed_at=observed_at,
        )
        ledger.append(
            "evidence.observed", workspace_id, {"evidence": to_plain(evidence)}
        )
        ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})
    input_event = ledger.append(
        "input.user_message", workspace_id, {"text": "what matters?"}
    )
    state = StateProjector(ledger).project(workspace_id)

    packet = DecisionInputComposer(ToolRegistry(), budget=ContextBudget(max_items=4)).compose(
        workspace_id, None, input_event, state
    )

    assert packet.current_input["text"] == "what matters?"
    assert packet.active_goal["summary"] == "Fix SSH"
    assert [need["name"] for need in packet.open_tool_needs] == ["install_ssh"]
    assert [fact["id"] for fact in packet.facts] == ["fact_2"]
    assert packet.evidence == []
    assert packet.entities == []
    assert packet.context_budget["selected_counts"][RECENT_FACTS] == 1
    assert packet.context_budget["dropped_counts"][ENTITIES] == 1
