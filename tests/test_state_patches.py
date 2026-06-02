from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel, Runtime
from seed_runtime.state import StateProjector
from seed_runtime.state_patches import StatePatchError, StatePatchService
from seed_runtime.tool_needs import ToolNeedService


def make_runtime(decision):
    ledger = EventLedger()
    registry = ToolRegistry()
    projector = StateProjector(ledger)
    runtime = Runtime(
        ledger,
        projector,
        ContextComposer(registry),
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        FakeDecisionModel(decision),
    )
    return runtime, ledger


def test_state_patch_service_applies_minimum_supported_ops():
    ledger = EventLedger()
    projector = StateProjector(ledger)
    service = StatePatchService(ledger, projector)

    result = service.apply(
        "ws",
        {
            "ops": [
                {
                    "op": "upsert_entity",
                    "entity": {
                        "id": "ent_node_1",
                        "kind": "host",
                        "name": "node-1",
                        "attributes": {"os": "linux"},
                    },
                },
                {
                    "op": "observe_evidence",
                    "evidence": {
                        "id": "evd_status_1",
                        "source": "user_message",
                        "kind": "host.status",
                        "payload": {"ssh_running": False},
                        "confidence": 0.8,
                    },
                },
                {
                    "op": "observe_fact",
                    "fact": {
                        "id": "fact_ssh_1",
                        "subject_id": "ent_node_1",
                        "predicate": "ssh.running",
                        "value": False,
                        "evidence_ids": ["evd_status_1"],
                        "confidence": 0.8,
                    },
                },
                {
                    "op": "create_goal",
                    "goal": {
                        "id": "goal_fix_ssh",
                        "summary": "Restore SSH access to node-1",
                        "related_entities": ["ent_node_1"],
                    },
                },
            ]
        },
        session_id="ses",
        causation_id="evt_decision",
    )

    assert [event.kind for event in result.events] == [
        "entity.upserted",
        "evidence.observed",
        "fact.observed",
        "goal.created",
    ]
    assert [event.causation_id for event in result.events] == ["evt_decision"] * 4

    state = projector.project("ws")
    assert state.entities["ent_node_1"].attributes == {"os": "linux"}
    assert state.evidence["evd_status_1"].workspace_id == "ws"
    assert state.facts["fact_ssh_1"].evidence_ids == ["evd_status_1"]
    assert state.goals["goal_fix_ssh"].created_from_event_id == "evt_decision"


def test_state_patch_service_accepts_legacy_collection_shape():
    ledger = EventLedger()
    service = StatePatchService(ledger, StateProjector(ledger))

    service.apply(
        "ws",
        {
            "entities": [{"id": "ent_1", "kind": "host", "name": "node-1"}],
            "facts": [
                {
                    "id": "fact_1",
                    "subject_id": "ent_1",
                    "predicate": "host.status",
                    "value": "known",
                }
            ],
        },
    )

    assert [event.kind for event in ledger.list_events("ws")] == [
        "entity.upserted",
        "fact.observed",
    ]


def test_state_patch_service_rejects_unknown_op():
    ledger = EventLedger()
    service = StatePatchService(ledger, StateProjector(ledger))

    try:
        service.apply("ws", {"ops": [{"op": "delete_everything"}]})
    except StatePatchError as exc:
        assert str(exc) == "unsupported state patch op 'delete_everything'"
    else:
        raise AssertionError("expected StatePatchError")

    assert ledger.list_events("ws") == []


def test_runtime_routes_propose_state_patch_to_state_updated_response():
    runtime, ledger = make_runtime(
        Decision(
            kind="propose_state_patch",
            reason="remember host status",
            state_patch={
                "ops": [
                    {
                        "op": "upsert_entity",
                        "entity": {
                            "id": "ent_node_1",
                            "kind": "host",
                            "name": "node-1",
                        },
                    },
                    {
                        "op": "create_goal",
                        "goal": {
                            "id": "goal_check_ssh",
                            "summary": "Check SSH status on node-1",
                        },
                    },
                ]
            },
        )
    )

    response = runtime.handle_user_message("ws", "ses", "remember node-1")

    assert response.kind == "state_updated"
    assert response.message == "Applied 2 state patch operation(s)."
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "entity.upserted",
        "goal.created",
    ]
    state = runtime.projector.project("ws")
    assert state.entities["ent_node_1"].name == "node-1"
    assert state.goals["goal_check_ssh"].summary == "Check SSH status on node-1"
