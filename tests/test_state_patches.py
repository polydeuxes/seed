import pytest

from seed_runtime.events import EventLedger
from seed_runtime.state import StateProjector
from seed_runtime.state_patches import StatePatchError, StatePatchService


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
                        "name": "example_host",
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
                        "summary": "Restore SSH access to example_host",
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
    evidence_event = result.events[1]
    fact_event = result.events[2]
    assert "observed_at" in evidence_event.payload["evidence"]
    assert "observed_at" in fact_event.payload["fact"]
    assert state.evidence["evd_status_1"].workspace_id == "ws"
    assert state.facts["fact_ssh_1"].evidence_ids == ["evd_status_1"]
    assert state.goals["goal_fix_ssh"].created_from_event_id == "evt_decision"


def test_state_patch_service_accepts_legacy_collection_shape():
    ledger = EventLedger()
    service = StatePatchService(ledger, StateProjector(ledger))

    service.apply(
        "ws",
        {
            "entities": [{"id": "ent_1", "kind": "host", "name": "example_host"}],
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


def test_state_patch_service_rejects_non_list_ops():
    ledger = EventLedger()
    service = StatePatchService(ledger, StateProjector(ledger))

    with pytest.raises(StatePatchError, match="state_patch.ops must be a list"):
        service.apply("ws", {"ops": {"op": "upsert_entity"}})


def test_state_patch_service_rejects_non_object_operation():
    ledger = EventLedger()
    service = StatePatchService(ledger, StateProjector(ledger))

    with pytest.raises(
        StatePatchError, match="state_patch operation must be an object"
    ):
        service.apply("ws", {"ops": ["not-an-object"]})


@pytest.mark.parametrize(
    ("operation", "expected_error"),
    [
        (
            {"op": "upsert_entity", "name": "web_service"},
            "entity missing required field\\(s\\): kind",
        ),
        (
            {"op": "upsert_entity", "kind": "service"},
            "entity missing required field\\(s\\): name",
        ),
        (
            {"op": "observe_evidence", "kind": "service.status"},
            "evidence missing required field\\(s\\): source",
        ),
        (
            {"op": "observe_evidence", "source": "user_message"},
            "evidence missing required field\\(s\\): kind",
        ),
        (
            {"op": "observe_fact", "predicate": "service.running", "value": True},
            "fact missing required field\\(s\\): subject_id",
        ),
        (
            {"op": "observe_fact", "subject_id": "ent_1", "value": True},
            "fact missing required field\\(s\\): predicate",
        ),
        (
            {
                "op": "observe_fact",
                "subject_id": "ent_1",
                "predicate": "service.running",
            },
            "fact missing required field\\(s\\): value",
        ),
        ({"op": "create_goal"}, "goal missing required field\\(s\\): summary"),
    ],
)
def test_state_patch_service_rejects_missing_required_fields_after_defaults(
    operation, expected_error
):
    ledger = EventLedger()
    service = StatePatchService(ledger, StateProjector(ledger))

    with pytest.raises(StatePatchError, match=expected_error):
        service.apply("ws", {"ops": [operation]})


def test_state_patch_service_accepts_inline_operation_payloads():
    ledger = EventLedger()
    service = StatePatchService(ledger, StateProjector(ledger))

    result = service.apply(
        "ws",
        {
            "ops": [
                {
                    "op": "upsert_entity",
                    "kind": "service",
                    "name": "web_service",
                }
            ]
        },
    )

    assert [event.kind for event in result.events] == ["entity.upserted"]
    assert [event.kind for event in ledger.list_events("ws")] == ["entity.upserted"]
    entity = result.events[0].payload["entity"]
    assert entity["kind"] == "service"
    assert entity["name"] == "web_service"
    assert entity["id"].startswith("ent_")


def test_state_patch_service_partial_application_is_not_rolled_back():
    ledger = EventLedger()
    service = StatePatchService(ledger, StateProjector(ledger))

    with pytest.raises(StatePatchError, match="unsupported state patch op 'unknown_op'"):
        service.apply(
            "ws",
            {
                "ops": [
                    {"op": "upsert_entity", "kind": "service", "name": "web_service"},
                    {"op": "unknown_op"},
                ]
            },
        )

    events = ledger.list_events("ws")
    assert [event.kind for event in events] == ["entity.upserted"]
    assert events[0].payload["entity"]["name"] == "web_service"
