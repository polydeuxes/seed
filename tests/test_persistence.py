from seed_runtime.events import SQLiteEventLedger
from seed_runtime.models import Entity
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def test_sqlite_ledger_persists_events(tmp_path):
    db = tmp_path / "events.db"
    ledger = SQLiteEventLedger(str(db))
    ledger.append("entity.upserted", "ws", {"entity": to_plain(Entity(id="ent_1", kind="host", name="node-1"))})
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    state = StateProjector(reopened).project("ws")

    assert state.entities["ent_1"].name == "node-1"
    reopened.close()


def test_sqlite_ledger_continues_event_ids_after_reopen(tmp_path):
    db = tmp_path / "events.db"
    ledger = SQLiteEventLedger(str(db))
    first = ledger.append("test.first", "ws")
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    second = reopened.append("test.second", "ws")

    assert first.id == "evt_000001"
    assert second.id == "evt_000002"
    assert second.id != first.id
    assert [event.id for event in reopened.list_events("ws")] == [
        "evt_000001",
        "evt_000002",
    ]
    reopened.close()


def test_sqlite_ledger_reserves_persisted_domain_id_counters(tmp_path):
    from seed_runtime.action_plans import ActionPlanService
    from seed_runtime.ids import new_id
    from seed_runtime.models import ToolNeed
    from seed_runtime.recommendation_ranker import RankedRecommendation
    from seed_runtime.state import State

    db = tmp_path / "events.db"
    ledger = SQLiteEventLedger(str(db))
    ledger.append(
        "tool_need.created",
        "ws",
        {
            "tool_need": {
                "id": "need_000004",
                "workspace_id": "ws",
                "name": "weather",
                "summary": "lookup weather",
                "capability": "weather_lookup",
                "reason": "test",
                "status": "proposed",
                "desired_inputs": [],
                "desired_outputs": [],
            }
        },
    )
    first_timestamp = ledger.list_events("ws")[-1].timestamp.isoformat()
    ledger.append(
        "evidence.observed",
        "ws",
        {
            "evidence": {
                "id": "evd_000005",
                "workspace_id": "ws",
                "source": "test",
                "kind": "fixture",
                "observed_at": first_timestamp,
                "payload": {},
                "confidence": 1.0,
            }
        },
    )
    ledger.append(
        "fact.observed",
        "ws",
        {
            "fact": {
                "id": "fact_000006",
                "subject_id": "host",
                "predicate": "runtime",
                "value": "docker",
                "evidence_ids": ["evd_000005"],
                "observed_at": first_timestamp,
                "confidence": 1.0,
            }
        },
    )
    ledger.append(
        "action_plan.created",
        "ws",
        {
            "action_plan": {
                "id": "plan_000007",
                "tool_need_id": "need_000004",
                "provider": "open_meteo",
                "capability": "weather_lookup",
                "summary": "fixture",
                "steps": ["Determine location."],
                "risk_class": "L1",
                "requires_approval": False,
                "status": "proposed",
                "rejection_reason": None,
                "replacement_plan_id": None,
                "executable": False,
            }
        },
    )
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    assert int(new_id("need").removeprefix("need_")) > 4
    assert int(new_id("evd").removeprefix("evd_")) > 5
    assert int(new_id("fact").removeprefix("fact_")) > 6

    plan = ActionPlanService(reopened).create_plan(
        ToolNeed(
            id="need_000005",
            workspace_id="ws",
            name="forecast",
            summary="lookup forecast",
            capability="weather_lookup",
            reason="test",
        ),
        RankedRecommendation(
            provider="open_meteo",
            summary="Open-Meteo forecast",
            score=1,
            reasons=[],
            reasoning=[],
        ),
        State(workspace_id="ws"),
    )

    assert int(plan.id.removeprefix("plan_")) > 7
    assert plan.id != "plan_000007"
    reopened.close()
