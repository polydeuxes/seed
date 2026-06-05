from seed_runtime.decision_journal import DecisionJournal
from seed_runtime.events import EventLedger
from seed_runtime.runtime_trace import RuntimeTraceReader, load_runtime_trace


class ExplodingLedger(EventLedger):
    def append(self, *args, **kwargs):  # pragma: no cover - should never be called
        raise AssertionError("trace must not append events")


def record_run(
    ledger: EventLedger,
    *,
    workspace_id: str = "ws",
    input_text: str = "hi",
    decision_kind: str = "answer",
    reason: str = "direct",
    outcome: str = "answered",
    selected_tool_name: str | None = None,
    policy_allowed: bool = True,
    assistant_text: str | None = "done",
    tool_event_kind: str | None = None,
    tool_payload: dict | None = None,
    policy_denied: bool = False,
    error_event_kind: str | None = None,
    error_payload: dict | None = None,
    error: str | None = None,
):
    input_event = ledger.append(
        "input.user_message",
        workspace_id,
        {"text": input_text},
        actor="user",
    )
    run_id = input_event.id
    if assistant_text is not None:
        ledger.append(
            "assistant.answer",
            workspace_id,
            {"text": assistant_text, "reason": reason},
            causation_id=input_event.id,
            correlation_id=run_id,
        )
    if policy_denied:
        ledger.append(
            "runtime.policy.denied",
            workspace_id,
            {"tool_name": selected_tool_name, "error": error},
            causation_id=input_event.id,
            correlation_id=run_id,
        )
    if tool_event_kind is not None:
        payload = dict(tool_payload or {})
        payload.setdefault("tool_name", selected_tool_name)
        ledger.append(
            tool_event_kind,
            workspace_id,
            payload,
            causation_id=input_event.id,
            correlation_id=run_id,
        )
    if error_event_kind is not None:
        ledger.append(
            error_event_kind,
            workspace_id,
            dict(error_payload or {}),
            causation_id=input_event.id,
            correlation_id=run_id,
        )
    DecisionJournal(ledger).append_record(
        workspace_id=workspace_id,
        run_id=run_id,
        decision_kind=decision_kind,
        reason=reason,
        context_hash="ctx123",
        selected_tool_name=selected_tool_name,
        selected_tool_args={},
        policy_allowed=policy_allowed,
        outcome=outcome,
        error=error,
        causation_id=input_event.id,
        correlation_id=run_id,
    )
    return run_id


def test_trace_reconstructs_answer_run():
    ledger = EventLedger()
    run_id = record_run(ledger)

    trace = load_runtime_trace(ledger, "ws", run_id)

    assert trace.user_input_event.event_type == "input.user_message"
    assert trace.assistant_event.event_type == "assistant.answer"
    assert trace.decision_record["outcome"] == "answered"
    assert trace.summary == {
        "found": True,
        "run_id": run_id,
        "input_text": "hi",
        "decision_kind": "answer",
        "decision_reason": "direct",
        "outcome": "answered",
        "selected_tool": None,
        "policy_allowed": True,
        "policy_denied": False,
        "final_response_text": "done",
        "error": None,
    }


def test_trace_reconstructs_successful_tool_run():
    ledger = EventLedger()
    run_id = record_run(
        ledger,
        input_text="echo hi",
        decision_kind="call_tool",
        reason="use echo",
        outcome="tool_succeeded",
        selected_tool_name="echo",
        assistant_text=None,
        tool_event_kind="tool.result",
        tool_payload={"output": {"message": "hi"}},
    )

    trace = load_runtime_trace(ledger, "ws", run_id)

    assert trace.tool_event.event_type == "tool.result"
    assert trace.tool_event.payload["output"]["message"] == "hi"
    assert trace.decision_record["selected_tool_name"] == "echo"
    assert trace.summary["outcome"] == "tool_succeeded"
    assert trace.summary["selected_tool"] == "echo"
    assert trace.summary["policy_allowed"] is True
    assert trace.error_events == []


def test_trace_reconstructs_unknown_tool_run():
    ledger = EventLedger()
    run_id = record_run(
        ledger,
        decision_kind="call_tool",
        outcome="tool_unknown",
        selected_tool_name="missing",
        assistant_text=None,
        tool_event_kind="runtime.tool.unknown",
        tool_payload={"error": "unknown tool: missing"},
        error="unknown tool: missing",
    )

    trace = load_runtime_trace(ledger, "ws", run_id)

    assert trace.tool_event.event_type == "runtime.tool.unknown"
    assert trace.summary["outcome"] == "tool_unknown"
    assert trace.summary["selected_tool"] == "missing"
    assert trace.summary["error"] == "unknown tool: missing"
    assert [event.event_type for event in trace.error_events] == [
        "runtime.tool.unknown",
        "decision.recorded",
    ]


def test_trace_reconstructs_policy_denied_run():
    ledger = EventLedger()
    run_id = record_run(
        ledger,
        input_text="echo hi",
        decision_kind="call_tool",
        reason="echo",
        outcome="policy_denied",
        selected_tool_name="echo",
        policy_allowed=False,
        assistant_text=None,
        policy_denied=True,
        error="policy denied tool echo: block",
    )

    trace = load_runtime_trace(ledger, "ws", run_id)

    assert trace.policy_event.event_type == "runtime.policy.denied"
    assert trace.tool_event is None
    assert trace.summary["policy_allowed"] is False
    assert trace.summary["policy_denied"] is True
    assert trace.summary["outcome"] == "policy_denied"


def test_trace_can_include_provider_failure_error_event():
    ledger = EventLedger()
    run_id = record_run(
        ledger,
        outcome="provider_failed",
        policy_allowed=False,
        assistant_text=None,
        error_event_kind="runtime.decision.provider_failed",
        error_payload={"error": "provider unavailable", "exception_type": "RuntimeError"},
        error="provider unavailable",
    )

    trace = load_runtime_trace(ledger, "ws", run_id)

    assert trace.summary["outcome"] == "provider_failed"
    assert trace.summary["error"] == "provider unavailable"
    assert [event.event_type for event in trace.error_events] == [
        "runtime.decision.provider_failed",
        "decision.recorded",
    ]
    assert trace.error_events[0].payload == {
        "error": "provider unavailable",
        "exception_type": "RuntimeError",
    }


def test_trace_reconstructs_tool_failure_run():
    ledger = EventLedger()
    run_id = record_run(
        ledger,
        input_text="echo hi",
        decision_kind="call_tool",
        reason="echo",
        outcome="tool_failed",
        selected_tool_name="echo",
        assistant_text=None,
        tool_event_kind="tool.failure",
        tool_payload={"error": "tool echo failed: boom"},
        error="tool echo failed: boom",
    )

    trace = load_runtime_trace(ledger, "ws", run_id)

    assert trace.tool_event.event_type == "tool.failure"
    assert trace.summary["outcome"] == "tool_failed"
    assert trace.summary["error"] == "tool echo failed: boom"


def test_trace_preserves_event_ordering():
    ledger = EventLedger()
    run_id = record_run(ledger)

    trace = load_runtime_trace(ledger, "ws", run_id)

    assert [event.event_type for event in trace.events] == [
        "input.user_message",
        "assistant.answer",
        "decision.recorded",
    ]


def test_trace_is_read_only_and_does_not_append_events():
    ledger = EventLedger()
    run_id = record_run(ledger)
    before = ledger.list_events("ws")

    trace = load_runtime_trace(ledger, "ws", run_id)
    trace.events[0].payload["text"] = "mutated snapshot"

    after = ledger.list_events("ws")
    assert [event.id for event in after] == [event.id for event in before]
    assert after[0].payload["text"] == "hi"


def test_trace_does_not_append_events_or_require_runtime_collaborators():
    ledger = ExplodingLedger()
    input_event = EventLedger.append(ledger, "input.user_message", "ws", {"text": "hi"}, actor="user")
    EventLedger.append(
        ledger,
        "assistant.answer",
        "ws",
        {"text": "done", "reason": "direct"},
        causation_id=input_event.id,
        correlation_id=input_event.id,
    )

    trace = RuntimeTraceReader(ledger).trace("ws", input_event.id)

    assert trace.summary["input_text"] == "hi"
    assert trace.summary["final_response_text"] == "done"


def test_missing_run_id_returns_clear_empty_trace():
    ledger = EventLedger()
    ledger.append("input.user_message", "ws", {"text": "other"}, actor="user")

    trace = load_runtime_trace(ledger, "ws", "missing-run")

    assert trace.events == []
    assert trace.user_input_event is None
    assert trace.decision_record is None
    assert trace.error_events == []
    assert trace.summary["found"] is False
    assert trace.summary["run_id"] == "missing-run"
