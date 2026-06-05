from seed_runtime.events import EventLedger
from seed_runtime.models import PolicyDecision
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime_loop import (
    Decision,
    EchoTool,
    FakeDecisionProvider,
    RuntimeInput,
    RuntimeLoop,
)
from seed_runtime.runtime_trace import RuntimeTraceReader, load_runtime_trace


class DenyPolicy:
    def __init__(self):
        self.calls = 0

    def evaluate(self, tool, state, *, scope=None):
        self.calls += 1
        return PolicyDecision(
            outcome="block",
            action=tool.policy_action,
            reason="blocked in test",
            risk_class=tool.risk_class,
        )


class FailingTool:
    def __init__(self):
        self.calls = 0

    def execute(self, context, arguments):
        self.calls += 1
        raise RuntimeError("boom")


class RaisingProvider:
    def decide(self, context):
        raise RuntimeError("provider unavailable")


class ExplodingLedger(EventLedger):
    def append(self, *args, **kwargs):  # pragma: no cover - should never be called
        raise AssertionError("trace must not append events")


class ExplodingProvider:
    def decide(self, context):  # pragma: no cover - should never be called
        raise AssertionError("trace must not call provider")


class ExplodingPolicy:
    def evaluate(self, tool, state, *, scope=None):  # pragma: no cover
        raise AssertionError("trace must not call policy")


class ExplodingTool:
    def execute(self, context, arguments):  # pragma: no cover
        raise AssertionError("trace must not execute operation implementations")


def make_loop(decision, *, policy_engine=None, tool_handlers=None):
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    runtime = RuntimeLoop(
        ledger,
        None,
        registry,
        policy_engine,
        FakeDecisionProvider(decision),
        tool_handlers or {},
    )
    return runtime, ledger


def trace_for(result, ledger):
    return load_runtime_trace(ledger, result.workspace_id, result.run_id)


def test_trace_reconstructs_answer_run():
    runtime, ledger = make_loop(Decision(kind="answer", text="done", reason="direct"))
    result = runtime.run(RuntimeInput("ws", "hi"))

    trace = trace_for(result, ledger)

    assert trace.user_input_event.event_type == "input.user_message"
    assert trace.assistant_event.event_type == "assistant.answer"
    assert trace.decision_record["outcome"] == "answered"
    assert trace.summary == {
        "found": True,
        "run_id": result.run_id,
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
    runtime, ledger = make_loop(
        Decision(
            kind="call_tool",
            tool_name="echo",
            tool_args={"message": "hi"},
            reason="use echo",
        ),
        tool_handlers={"echo": EchoTool()},
    )
    result = runtime.run(RuntimeInput("ws", "echo hi"))

    trace = trace_for(result, ledger)

    assert trace.tool_event.event_type == "tool.result"
    assert trace.tool_event.payload["output"]["message"] == "hi"
    assert trace.decision_record["selected_tool_name"] == "echo"
    assert trace.summary["outcome"] == "tool_succeeded"
    assert trace.summary["selected_tool"] == "echo"
    assert trace.summary["policy_allowed"] is True
    assert trace.error_events == []


def test_trace_reconstructs_unknown_tool_run():
    runtime, ledger = make_loop(
        Decision(kind="call_tool", tool_name="missing", tool_args={}, reason="try missing")
    )
    result = runtime.run(RuntimeInput("ws", "missing"))

    trace = trace_for(result, ledger)

    assert trace.tool_event.event_type == "runtime.tool.unknown"
    assert trace.summary["outcome"] == "tool_unknown"
    assert trace.summary["selected_tool"] == "missing"
    assert trace.summary["error"] == "unknown tool: missing"
    assert [event.event_type for event in trace.error_events] == [
        "runtime.tool.unknown",
        "decision.recorded",
    ]


def test_trace_reconstructs_policy_denied_run():
    policy = DenyPolicy()
    runtime, ledger = make_loop(
        Decision(
            kind="call_tool",
            tool_name="echo",
            tool_args={"message": "hi"},
            reason="echo",
        ),
        policy_engine=policy,
        tool_handlers={"echo": EchoTool()},
    )
    result = runtime.run(RuntimeInput("ws", "echo hi"))

    trace = trace_for(result, ledger)

    assert policy.calls == 1
    assert trace.policy_event.event_type == "runtime.policy.denied"
    assert trace.tool_event is None
    assert trace.summary["policy_allowed"] is False
    assert trace.summary["policy_denied"] is True
    assert trace.summary["outcome"] == "policy_denied"


def test_trace_reconstructs_malformed_decision_run():
    runtime, ledger = make_loop({"kind": "answer", "text": "not a Decision"})
    result = runtime.run(RuntimeInput("ws", "hi"))

    trace = trace_for(result, ledger)

    assert trace.summary["outcome"] == "malformed_decision"
    assert trace.summary["error"] == "decision provider must return a runtime_loop.Decision"
    assert [event.event_type for event in trace.error_events] == [
        "runtime.decision.rejected",
        "decision.recorded",
    ]


def test_trace_can_include_provider_failure_error_event():
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    runtime = RuntimeLoop(
        ledger,
        None,
        registry,
        ExplodingPolicy(),
        RaisingProvider(),
        {"echo": ExplodingTool()},
    )
    result = runtime.run(RuntimeInput("ws", "hi"))

    trace = trace_for(result, ledger)

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
    failing_tool = FailingTool()
    runtime, ledger = make_loop(
        Decision(
            kind="call_tool",
            tool_name="echo",
            tool_args={"message": "hi"},
            reason="echo",
        ),
        tool_handlers={"echo": failing_tool},
    )
    result = runtime.run(RuntimeInput("ws", "echo hi"))

    trace = trace_for(result, ledger)

    assert failing_tool.calls == 1
    assert trace.tool_event.event_type == "tool.failure"
    assert trace.summary["outcome"] == "tool_failed"
    assert trace.summary["error"] == "tool echo failed: boom"


def test_trace_preserves_event_ordering():
    runtime, ledger = make_loop(Decision(kind="answer", text="done", reason="direct"))
    result = runtime.run(RuntimeInput("ws", "hi"))

    trace = trace_for(result, ledger)

    assert [event.event_id for event in trace.events] == result.events_appended
    assert [event.event_type for event in trace.events] == [
        "input.user_message",
        "assistant.answer",
        "decision.recorded",
    ]


def test_trace_is_read_only_and_does_not_append_events():
    runtime, ledger = make_loop(Decision(kind="answer", text="done", reason="direct"))
    result = runtime.run(RuntimeInput("ws", "hi"))
    before = ledger.list_events("ws")

    trace = trace_for(result, ledger)
    trace.events[0].payload["text"] = "mutated snapshot"

    after = ledger.list_events("ws")
    assert [event.id for event in after] == [event.id for event in before]
    assert after[0].payload["text"] == "hi"


def test_trace_does_not_call_provider_policy_or_tools():
    ledger = ExplodingLedger()
    input_event = EventLedger.append(ledger, "input.user_message", "ws", {"text": "hi"}, actor="user")
    EventLedger.append(
        ledger,
        "assistant.answer",
        "ws",
        {"text": "done", "reason": "direct"},
        causation_id=input_event.id,
    )
    runtime = RuntimeLoop(
        ledger,
        None,
        ToolRegistry(),
        ExplodingPolicy(),
        ExplodingProvider(),
        {"echo": ExplodingTool()},
    )

    trace = RuntimeTraceReader(runtime.ledger).trace("ws", input_event.id)

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
