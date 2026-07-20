from seed_runtime.events import EventLedger
from seed_runtime.models import RuntimeResponse
from seed_runtime.runtime import Runtime
from seed_runtime.state import StateProjector


def make_runtime():
    ledger = EventLedger()
    projector = StateProjector(ledger)
    return Runtime(ledger, projector), ledger


def test_runtime_input_boundary_returns_unsupported_without_model_route():
    runtime, ledger = make_runtime()

    response = runtime.handle_user_message("ws", "ses", "hello")

    assert isinstance(response, RuntimeResponse)
    assert response.kind == "unsupported"
    assert response.message == "No Seed-owned runtime decision authority is configured for free-text input."
    assert response.payload["reason"] == "model_decision_authority_excised"
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "runtime.decision_authority_unsupported",
    ]


def test_runtime_projects_input_boundary_events_without_cluster_mutation():
    runtime, ledger = make_runtime()

    runtime.handle_user_message("ws", "ses", "hello")
    projected_state = runtime.projector.project("ws")

    assert projected_state.workspace_id == "ws"
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "runtime.decision_authority_unsupported",
    ]
    assert projected_state.open_tool_needs == []
    assert projected_state.evidence == {}
    assert projected_state.facts == {}
