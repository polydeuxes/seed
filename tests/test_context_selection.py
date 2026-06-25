from datetime import timedelta

from seed_runtime.context import DecisionInputComposer
from seed_runtime.context_budget import ContextBudget, ENTITIES, RECENT_EVIDENCE, RECENT_FACTS
from seed_runtime.evidence import Evidence
from seed_runtime.facts import Fact
from seed_runtime.models import Entity, Event, Goal, utc_now
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import State


def _fact(
    fact_id: str,
    observed_at,
    *,
    confidence: float,
    expires_at=None,
) -> Fact:
    return Fact(
        id=fact_id,
        subject_id="ent_subject",
        predicate="status",
        value=fact_id,
        observed_at=observed_at,
        expires_at=expires_at,
        confidence=confidence,
    )


def test_decision_input_composer_orders_facts_before_budget_truncation():
    now = utc_now()
    state = State(workspace_id="ws")
    facts = [
        _fact(
            "fact_expired_newest",
            now + timedelta(minutes=10),
            confidence=1.0,
            expires_at=now - timedelta(minutes=1),
        ),
        _fact("fact_fresh_newer_low_confidence", now + timedelta(minutes=4), confidence=0.1),
        _fact("fact_fresh_same_time_high_confidence", now + timedelta(minutes=2), confidence=0.9),
        _fact("fact_fresh_same_time_low_confidence", now + timedelta(minutes=2), confidence=0.4),
        _fact("fact_fresh_older_high_confidence", now + timedelta(minutes=1), confidence=1.0),
    ]
    state.facts = {fact.id: fact for fact in facts}
    input_event = Event(id="evt_input", kind="input.user_message", payload={"text": "go"})

    packet = DecisionInputComposer(
        ToolRegistry(), budget=ContextBudget(section_limits={RECENT_FACTS: 4})
    ).compose("ws", None, input_event, state)

    assert [fact["id"] for fact in packet.facts] == [
        "fact_fresh_newer_low_confidence",
        "fact_fresh_same_time_high_confidence",
        "fact_fresh_same_time_low_confidence",
        "fact_fresh_older_high_confidence",
    ]
    assert packet.context_budget["dropped_counts"][RECENT_FACTS] == 1


def test_decision_input_composer_orders_evidence_before_budget_truncation():
    now = utc_now()
    state = State(workspace_id="ws")
    evidence = [
        Evidence(
            id="evd_older_high_confidence",
            workspace_id="ws",
            source="test",
            kind="status",
            observed_at=now + timedelta(minutes=1),
            confidence=1.0,
        ),
        Evidence(
            id="evd_same_time_low_confidence",
            workspace_id="ws",
            source="test",
            kind="status",
            observed_at=now + timedelta(minutes=2),
            confidence=0.2,
        ),
        Evidence(
            id="evd_newer_low_confidence",
            workspace_id="ws",
            source="test",
            kind="status",
            observed_at=now + timedelta(minutes=3),
            confidence=0.1,
        ),
        Evidence(
            id="evd_same_time_high_confidence",
            workspace_id="ws",
            source="test",
            kind="status",
            observed_at=now + timedelta(minutes=2),
            confidence=0.8,
        ),
    ]
    state.evidence = {item.id: item for item in evidence}
    input_event = Event(id="evt_input", kind="input.user_message", payload={"text": "go"})

    packet = DecisionInputComposer(
        ToolRegistry(), budget=ContextBudget(section_limits={RECENT_EVIDENCE: 3})
    ).compose("ws", None, input_event, state)

    assert [item["id"] for item in packet.evidence] == [
        "evd_newer_low_confidence",
        "evd_same_time_high_confidence",
        "evd_same_time_low_confidence",
    ]
    assert packet.context_budget["dropped_counts"][RECENT_EVIDENCE] == 1


def test_decision_input_composer_orders_goals_and_entities_before_budget_truncation():
    state = State(workspace_id="ws")
    state.goals = {
        "goal_001_blocked": Goal(
            id="goal_001_blocked", workspace_id="ws", summary="Blocked", status="blocked"
        ),
        "goal_002_active": Goal(
            id="goal_002_active", workspace_id="ws", summary="Active", status="active"
        ),
    }
    entities = [
        Entity(id="ent_low", kind="host", name="aaa", confidence=0.1),
        Entity(id="ent_high_z", kind="host", name="zzz", confidence=0.9),
        Entity(id="ent_mid_2", kind="host", name="same", confidence=0.8),
        Entity(id="ent_mid_1", kind="host", name="same", confidence=0.8),
    ]
    state.entities = {entity.id: entity for entity in entities}
    input_event = Event(id="evt_input", kind="input.user_message", payload={"text": "go"})

    packet = DecisionInputComposer(
        ToolRegistry(), budget=ContextBudget(section_limits={ENTITIES: 3})
    ).compose("ws", None, input_event, state)

    assert packet.active_goal["id"] == "goal_002_active"
    assert [entity["id"] for entity in packet.entities] == [
        "ent_high_z",
        "ent_mid_1",
        "ent_mid_2",
    ]
    assert packet.context_budget["dropped_counts"][ENTITIES] == 1
