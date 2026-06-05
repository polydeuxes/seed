from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision as RuntimeDecision
from seed_runtime.models import ToolSpec, Toolkit
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel, Runtime
from seed_runtime.runtime_loop import (
    Decision as LoopDecision,
    EchoTool,
    FakeDecisionProvider,
    RuntimeInput,
    RuntimeLoop,
)
from seed_runtime.runtime_loop_decisions import RuntimeLoopDecisionValidator
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


class CountingPolicy:
    def __init__(self):
        self.calls = 0

    def evaluate(self, tool, state, *, scope=None):
        self.calls += 1
        raise AssertionError("policy must not be evaluated for malformed decisions")


def make_registry():
    registry = ToolRegistry()
    registry.register_toolkit(
        Toolkit(
            id="tk_loop_decisions",
            name="loop decisions",
            summary="RuntimeLoop decision test tools.",
            tools=[
                ToolSpec(
                    toolkit_id="tk_loop_decisions",
                    name="echo",
                    summary="Echo a message deterministically.",
                    input_schema={},
                    output_schema={},
                    policy_action="echo.run",
                    implementation="tests:echo",
                    risk_class="L1",
                )
            ],
        )
    )
    return registry


def make_loop(decision, *, policy_engine=None):
    ledger = EventLedger()
    registry = make_registry()
    provider = decision if hasattr(decision, "decide") else FakeDecisionProvider(decision)
    echo_tool = EchoTool()
    runtime = RuntimeLoop(
        ledger,
        None,
        registry,
        policy_engine,
        provider,
        {"echo": echo_tool},
    )
    return runtime, ledger, echo_tool


def make_old_runtime(decision):
    ledger = EventLedger()
    registry = make_registry()
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


def assert_invalid(proposed, expected_error):
    decision, error = RuntimeLoopDecisionValidator().validate_decision(proposed)
    assert decision is None
    assert error == expected_error


def test_runtime_loop_decision_validator_preserves_validation_messages():
    assert_invalid(
        {"kind": "call_tool", "tool_name": "echo"},
        "decision provider must return a runtime_loop.Decision",
    )
    assert_invalid(
        LoopDecision(kind="ask_question", text="Which host?", reason="needs target"),
        "decision kind must be 'answer', 'call_tool', or 'request_tool'",
    )
    assert_invalid(
        LoopDecision(kind="answer", text="done", reason=123),
        "decision reason must be a string",
    )
    assert_invalid(
        LoopDecision(kind="answer", text="", reason="empty"),
        "answer decisions require non-empty text",
    )
    assert_invalid(
        LoopDecision(kind="answer", text="done", tool_name="echo", reason="bad"),
        "answer decisions may not include tool output fields",
    )
    assert_invalid(
        LoopDecision(kind="answer", text="done", tool_need={"name": "n"}, reason="bad"),
        "answer decisions may not include tool_need",
    )
    assert_invalid(
        LoopDecision(kind="call_tool", reason="missing tool"),
        "tool decisions require a non-empty tool_name",
    )
    assert_invalid(
        LoopDecision(kind="call_tool", tool_name="echo", tool_args="bad", reason="bad"),
        "tool decisions require tool_args to be a dict",
    )
    assert_invalid(
        LoopDecision(kind="call_tool", tool_name="echo", text="done", reason="bad"),
        "tool decisions may not include answer text",
    )
    assert_invalid(
        LoopDecision(kind="call_tool", tool_name="echo", tool_need={"name": "n"}, reason="bad"),
        "tool decisions may not include tool_need",
    )
    assert_invalid(
        LoopDecision(kind="request_tool", reason="missing payload"),
        "request_tool decisions require tool_need dict",
    )
    assert_invalid(
        LoopDecision(
            kind="request_tool",
            reason="missing name",
            tool_need={"name": "", "summary": "Summary", "capability": "cap"},
        ),
        "request_tool decisions require non-empty name",
    )
    assert_invalid(
        LoopDecision(
            kind="request_tool",
            reason="missing summary",
            tool_need={"name": "need", "summary": "", "capability": "cap"},
        ),
        "request_tool decisions require non-empty summary",
    )
    assert_invalid(
        LoopDecision(
            kind="request_tool",
            reason="missing capability",
            tool_need={"name": "need", "summary": "Summary", "capability": ""},
        ),
        "request_tool decisions require non-empty capability",
    )
    assert_invalid(
        LoopDecision(
            kind="request_tool",
            reason="forbidden fields",
            tool_name="echo",
            tool_args={"message": "hi"},
            text="no",
            tool_need={"name": "need", "summary": "Summary", "capability": "cap"},
        ),
        "request_tool decisions may not include tool_name, tool_args, or text",
    )


def test_runtime_loop_valid_answer_call_tool_and_request_tool_decisions_still_work():
    answer_runtime, _, _ = make_loop(
        LoopDecision(kind="answer", text="done", reason="valid answer")
    )
    answer = answer_runtime.run(RuntimeInput(workspace_id="ws_answer", user_text="hi"))
    assert answer.decision_kind == "answer"
    assert answer.response_text == "done"
    assert answer.decision_outcome == "answered"

    tool_runtime, _, echo_tool = make_loop(
        LoopDecision(
            kind="call_tool",
            tool_name="echo",
            tool_args={"message": "hello"},
            reason="valid tool",
        )
    )
    tool = tool_runtime.run(RuntimeInput(workspace_id="ws_tool", user_text="echo hello"))
    assert tool.decision_kind == "call_tool"
    assert tool.tool_result == {"ok": True, "message": "hello", "workspace_id": "ws_tool"}
    assert tool.decision_outcome == "tool_succeeded"
    assert echo_tool.calls == [{"message": "hello"}]

    request_runtime, _, _ = make_loop(
        LoopDecision(
            kind="request_tool",
            reason="valid need",
            tool_need={
                "name": "Lookup Service Status",
                "summary": "Look up service status from inventory",
                "capability": "Service Status Lookup",
            },
        )
    )
    requested = request_runtime.run(
        RuntimeInput(workspace_id="ws_request", user_text="check service")
    )
    assert requested.decision_kind == "request_tool"
    assert requested.response_text == "Recorded tool need lookup_service_status."
    assert requested.decision_outcome == "tool_requested"


def test_malformed_runtime_loop_decisions_append_same_events_and_skip_policy_and_tool():
    policy = CountingPolicy()
    runtime, ledger, echo_tool = make_loop(
        {"kind": "call_tool", "tool_name": "echo"},
        policy_engine=policy,
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_bad", user_text="bad"))

    assert result.decision_kind is None
    assert result.policy_allowed is False
    assert result.error == "decision provider must return a runtime_loop.Decision"
    assert result.decision_outcome == "malformed_decision"
    assert policy.calls == 0
    assert echo_tool.calls == []
    events = ledger.list_events("ws_bad")
    assert [event.kind for event in events] == [
        "input.user_message",
        "runtime.decision.rejected",
        "decision.recorded",
    ]
    assert events[1].payload == {
        "error": "decision provider must return a runtime_loop.Decision",
        "decision": {"kind": "call_tool", "tool_name": "echo"},
    }
    journal = events[-1].payload["record"]
    assert journal["outcome"] == "malformed_decision"
    assert journal["error"] == "decision provider must return a runtime_loop.Decision"


def test_old_runtime_behavior_is_untouched_by_runtime_loop_decision_validator():
    runtime, ledger = make_old_runtime(
        RuntimeDecision(kind="answer", reason="ok", answer="done")
    )

    response = runtime.handle_user_message("ws_old", "session", "hi")

    assert response.kind == "answer"
    assert response.message == "done"
    assert [event.kind for event in ledger.list_events("ws_old")] == [
        "input.user_message",
        "model.decision.proposed",
        "response.answer",
    ]
