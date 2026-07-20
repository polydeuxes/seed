from seed_runtime.events import EventLedger
from seed_runtime.models import RuntimeResponse
from seed_runtime.runtime import Runtime
from seed_runtime.state import StateProjector


def test_free_text_input_records_no_model_decision_or_runtime_route():
    ledger = EventLedger()
    runtime = Runtime(ledger, StateProjector(ledger))

    response = runtime.handle_user_message("ws", "ses", "free text")

    assert isinstance(response, RuntimeResponse)
    assert response.kind == "unsupported"
    assert response.payload["reason"] == "model_decision_authority_excised"
    event_kinds = [event.kind for event in ledger.list("ws")]
    assert event_kinds == [
        "input.user_message",
        "runtime.decision_authority_unsupported",
    ]
    assert "model.decision.proposed" not in event_kinds
