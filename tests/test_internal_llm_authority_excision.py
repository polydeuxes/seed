from seed_runtime.events import EventLedger
from seed_runtime.runtime import Runtime
from seed_runtime.state import StateProjector


def test_model_decision_corridor_dependencies_are_absent_from_runtime_boundary():
    ledger = EventLedger()
    runtime = Runtime(ledger, StateProjector(ledger))

    response = runtime.handle_user_message("ws", "ses", "free text")

    assert response.kind == "unsupported"
    for name in (
        "decision_input_composer",
        "decision_validator",
        "tool_executor",
        "tool_need_service",
        "capability_catalog",
        "decision_producer",
        "recommendation_ranker",
    ):
        assert not hasattr(runtime, name)
    assert [event.kind for event in ledger.list("ws")] == [
        "input.user_message",
        "runtime.decision_authority_unsupported",
    ]
