from datetime import datetime, timezone

from seed_runtime import AnsibleInventoryObservationSource
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.models import Entity, Fact
from seed_runtime.observation_sources import (
    FakeObservationSource,
    ObservationCollectionService,
)
from seed_runtime.observations import Observation, ObservationIngestor
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def test_sqlite_ledger_persists_events(tmp_path):
    db = tmp_path / "events.db"
    ledger = SQLiteEventLedger(str(db))
    ledger.append("entity.upserted", "ws", {"entity": to_plain(Entity(id="ent_1", kind="host", name="example_host"))})
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    state = StateProjector(reopened).project("ws")

    assert state.entities["ent_1"].name == "example_host"
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


def test_sqlite_observation_ingest_reopen_projects_current_belief(tmp_path):
    from datetime import datetime, timezone

    from seed_runtime.observations import Observation, ObservationIngestor

    db = tmp_path / "events.db"
    ledger = SQLiteEventLedger(str(db))
    observation = Observation(
        id="obs_example_host_architecture",
        source_type="discovery",
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        subject="example_host",
        predicate="architecture",
        value="x86_64",
        confidence=0.94,
    )
    fact = ObservationIngestor(ledger).ingest(observation, "ws")
    persisted_fact_payload = ledger.list_events("ws")[-1].payload["fact"]
    assert persisted_fact_payload["subject_id"] == "example_host"
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    state = StateProjector(reopened).project("ws")

    assert fact.id in state.facts
    assert any(
        support.subject == "example_host"
        and support.predicate == "architecture"
        and support.value == "x86_64"
        and support.supporting_fact_ids == [fact.id]
        for support in state.fact_supports
    )
    best_fact = state.get_best_fact("example_host", "architecture")
    assert best_fact is not None
    assert best_fact.value == "x86_64"
    reopened.close()


def test_projector_accepts_legacy_fact_observed_subject_payload_after_reopen(tmp_path):
    from datetime import datetime, timezone

    db = tmp_path / "events.db"
    observed_at = datetime(2026, 1, 1, tzinfo=timezone.utc).isoformat()
    ledger = SQLiteEventLedger(str(db))
    ledger.append(
        "fact.observed",
        "ws",
        {
            "fact": {
                "id": "fact_obs_000009",
                "subject": "example_host",
                "predicate": "architecture",
                "value": "x86_64",
                "evidence_ids": [],
                "source_type": "discovery",
                "confidence": 0.94,
                "observed_at": observed_at,
            }
        },
    )
    ledger.append(
        "fact.observed",
        "ws",
        {
            "id": "fact_obs_000010",
            "subject": "example_host",
            "predicate": "kernel",
            "value": "linux",
            "evidence_ids": [],
            "source_type": "discovery",
            "confidence": 0.94,
            "observed_at": observed_at,
        },
    )
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    state = StateProjector(reopened).project("ws")

    architecture = state.get_best_fact("example_host", "architecture")
    assert architecture is not None
    assert architecture.value == "x86_64"
    assert state.get_fact_support("example_host", "architecture") is not None
    kernel = state.get_best_fact("example_host", "kernel")
    assert kernel is not None
    assert kernel.value == "linux"
    assert state.get_fact_support("example_host", "kernel") is not None
    reopened.close()


def test_sqlite_inventory_identity_resolves_endpoint_fact_after_reopen(tmp_path):
    inventory_path = tmp_path / "inventory.ini"
    inventory_path.write_text(
        "[nodes]\nexample_host ansible_host=192.0.2.115\n", encoding="utf-8"
    )
    db = tmp_path / "inventory-endpoint.db"
    workspace_id = "ws_inventory_endpoint"

    ledger = SQLiteEventLedger(str(db))
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        AnsibleInventoryObservationSource(inventory_path), workspace_id
    )
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    ObservationCollectionService(ObservationIngestor(reopened)).collect(
        FakeObservationSource(
            [
                Observation(
                    id="obs_endpoint_availability",
                    source_type="provider",
                    observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    subject="192.0.2.115:9100",
                    predicate="availability_status",
                    value="down",
                    confidence=0.95,
                )
            ]
        ),
        workspace_id,
    )

    state = StateProjector(reopened).project(workspace_id)

    endpoint_aliases = [
        fact
        for fact in state.facts.values()
        if fact.subject_id == "example_host"
        and fact.predicate == "alias"
        and fact.value == "192.0.2.115:9100"
    ]
    assert len(endpoint_aliases) == 1
    assert state.get_best_fact("example_host", "availability_status") is None
    best_fact = state.get_best_fact("192.0.2.115:9100", "availability_status")
    assert best_fact is not None
    assert best_fact.subject_id == "192.0.2.115:9100"
    assert best_fact.value == "down"
    reopened.close()


def test_sqlite_reopen_preserves_entity_type_projection(tmp_path):
    db = tmp_path / "entity-types.db"
    ledger = SQLiteEventLedger(str(db))
    fact = Fact(
        id="fact_example_host_os",
        subject_id="example_host",
        predicate="os",
        value="linux",
        evidence_ids=[],
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    before = StateProjector(ledger).project("ws").entity_type_assertions
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    after = StateProjector(reopened).project("ws").entity_type_assertions

    assert after == before
    assert StateProjector(reopened).project("ws").get_current_entity_types(
        "example_host"
    ) == ["host"]
    reopened.close()


def test_sqlite_reopen_preserves_multi_predicate_cardinality(tmp_path):
    db = tmp_path / "cardinality.db"
    ledger = SQLiteEventLedger(str(db))
    for index, value in enumerate(("example_host:9100", "example_host:9200")):
        fact = Fact(
            id=f"fact_alias_{index}",
            subject_id="example_host",
            predicate="alias",
            value=value,
            source_type="imported",
            confidence=0.9,
            evidence_ids=[],
            observed_at=datetime(2026, 1, index + 1, tzinfo=timezone.utc),
        )
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    state = StateProjector(reopened).project("ws")

    assert [fact.value for fact in state.get_current_facts("example_host", "alias")] == [
        "example_host:9100",
        "example_host:9200",
    ]
    assert state.get_fact_conflicts() == []
    reopened.close()
