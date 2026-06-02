from seed_runtime.context import ContextComposer
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.fact_extraction import FactExtractionError, ToolResultFactExtractor
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import StateProjector


def make_executor():
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    return ToolExecutor(ledger, registry, projector), ledger, registry, projector


def test_completed_tool_call_extracts_tool_output_evidence_into_state_and_context():
    executor, ledger, registry, projector = make_executor()

    executor.execute("ws_1", "ses_1", "echo", {"message": "hello"})

    events = ledger.list_events("ws_1")
    assert [event.kind for event in events] == [
        "tool.call.started",
        "tool.call.completed",
        "evidence.observed",
    ]
    completed = events[1]
    observed = events[2]
    assert observed.causation_id == completed.id
    assert observed.payload["evidence"]["source"] == "tool:echo"
    assert observed.payload["evidence"]["kind"] == "tool.output"
    assert observed.payload["evidence"]["observed_at"] == completed.timestamp.isoformat()
    assert observed.payload["evidence"]["payload"] == {
        "tool": "echo",
        "output": {"ok": True, "message": "hello", "workspace_id": "ws_1"},
        "tool_call_event_id": completed.id,
    }

    state = projector.project("ws_1")
    evidence = next(iter(state.evidence.values()))
    assert evidence.source == "tool:echo"
    assert state.facts == {}

    input_event = ledger.append("input.user_message", "ws_1", {"text": "what happened?"})
    context = ContextComposer(registry).compose("ws_1", "ses_1", input_event, state)
    assert context.evidence == [evidence.__dict__]


def test_tool_result_fact_extractor_rejects_non_completed_tool_events():
    ledger = EventLedger()
    event = ledger.append("tool.call.failed", "ws_1", {"tool": "echo"})

    try:
        ToolResultFactExtractor(ledger).observe_tool_result(event)
    except FactExtractionError as exc:
        assert str(exc) == "can only extract facts from tool.call.completed"
    else:
        raise AssertionError("expected FactExtractionError")
