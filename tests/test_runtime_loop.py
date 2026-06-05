from seed_runtime.events import EventLedger
from seed_runtime.policy import PolicyGate
from seed_runtime.projection_store import InMemoryProjectionStore, project_state_with_cache
from seed_runtime.runtime_loop import (
    Decision as LoopDecision,
    EchoTool,
    FakeDecisionProvider,
    RuntimeInput,
    RuntimeLoop,
)
from seed_runtime.models import ToolSpec, Toolkit
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import StateProjector

def make_loop(decision, *, policy_engine=None, handlers=None, ledger=None, projector=None):
    ledger = ledger or EventLedger()
    registry = ToolRegistry()
    registry.register_toolkit(
        Toolkit(
            id="tk_loop_echo",
            name="loop echo",
            summary="RuntimeLoop test tools.",
            tools=[
                ToolSpec(
                    toolkit_id="tk_loop_echo",
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
    provider = decision if hasattr(decision, "decide") else FakeDecisionProvider(decision)
    echo_tool = EchoTool()
    runtime = RuntimeLoop(
        ledger,
        InMemoryProjectionStore(),
        registry,
        policy_engine or PolicyGate(),
        provider,
        handlers if handlers is not None else {"echo": echo_tool},
        projector=projector,
    )
    return runtime, ledger, provider, echo_tool


def test_loop_answer_decision_appends_user_and_assistant_events():
    runtime, ledger, provider, _ = make_loop(
        LoopDecision(kind="answer", text="done", reason="deterministic")
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="hello"))

    assert result.decision_kind == "answer"
    assert result.response_text == "done"
    assert result.policy_allowed is True
    assert result.error is None
    assert [event.kind for event in ledger.list_events("ws_loop")] == [
        "input.user_message",
        "assistant.answer",
        "decision.recorded",
    ]
    journal = ledger.list_events("ws_loop")[-1].payload["record"]
    assert journal["decision_kind"] == "answer"
    assert journal["outcome"] == "answered"
    assert result.decision_id == journal["decision_id"]
    assert result.decision_outcome == "answered"
    assert len(result.events_appended) == 3
    assert provider.last_context.current_input["text"] == "hello"
    assert provider.last_context.state.workspace_id == "ws_loop"
    assert provider.last_context.decision_context.projection_version == "v1"
    assert (
        provider.last_context.decision_context.last_event_id
        == result.events_appended[0]
    )


def test_loop_tool_decision_executes_registered_echo_tool_and_appends_result_event():
    runtime, ledger, _, echo_tool = make_loop(
        LoopDecision(
            kind="call_tool",
            tool_name="echo",
            tool_args={"message": "hello"},
            reason="safe registered tool",
        )
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="echo hello"))

    assert result.decision_kind == "call_tool"
    assert result.tool_name == "echo"
    assert result.tool_result == {
        "ok": True,
        "message": "hello",
        "workspace_id": "ws_loop",
    }
    assert result.policy_allowed is True
    assert result.error is None
    assert echo_tool.calls == [{"message": "hello"}]
    assert [event.kind for event in ledger.list_events("ws_loop")] == [
        "input.user_message",
        "tool.result",
        "decision.recorded",
    ]
    assert ledger.list_events("ws_loop")[-2].payload["output"]["message"] == "hello"
    journal = ledger.list_events("ws_loop")[-1].payload["record"]
    assert journal["selected_tool_name"] == "echo"
    assert journal["outcome"] == "tool_succeeded"
    assert result.decision_outcome == "tool_succeeded"


def test_loop_unknown_tool_is_rejected_and_logged_as_event():
    runtime, ledger, _, echo_tool = make_loop(
        LoopDecision(
            kind="call_tool",
            tool_name="missing",
            tool_args={"message": "hello"},
            reason="provider suggested unknown tool",
        )
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="use missing"))

    assert result.tool_name == "missing"
    assert result.policy_allowed is False
    assert result.error == "unknown tool: missing"
    assert echo_tool.calls == []
    assert [event.kind for event in ledger.list_events("ws_loop")] == [
        "input.user_message",
        "runtime.tool.unknown",
        "decision.recorded",
    ]
    journal = ledger.list_events("ws_loop")[-1].payload["record"]
    assert journal["outcome"] == "tool_unknown"
    assert journal["error"] == "unknown tool: missing"
    assert result.decision_outcome == "tool_unknown"


def test_loop_policy_denial_prevents_tool_execution():
    runtime, ledger, _, echo_tool = make_loop(
        LoopDecision(
            kind="call_tool",
            tool_name="echo",
            tool_args={"message": "blocked"},
            reason="policy should block",
        ),
        policy_engine=PolicyGate({"echo.run": "L4"}),
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="echo blocked"))

    assert result.policy_allowed is False
    assert "policy denied tool echo" in result.error
    assert echo_tool.calls == []
    assert [event.kind for event in ledger.list_events("ws_loop")] == [
        "input.user_message",
        "runtime.policy.denied",
        "decision.recorded",
    ]
    assert ledger.list_events("ws_loop")[-2].payload["policy"]["outcome"] == "block"
    journal = ledger.list_events("ws_loop")[-1].payload["record"]
    assert journal["policy_allowed"] is False
    assert journal["outcome"] == "policy_denied"
    assert result.decision_outcome == "policy_denied"


def test_loop_malformed_decision_is_rejected_before_policy_and_tool_execution():
    class CountingPolicy:
        calls = 0

        def evaluate(self, tool, state, *, scope=None):
            self.calls += 1
            return PolicyGate().evaluate(tool, state, scope=scope)

    policy = CountingPolicy()
    runtime, ledger, _, echo_tool = make_loop(
        {"kind": "call_tool", "tool_name": "echo"},
        policy_engine=policy,
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="bad"))

    assert result.decision_kind is None
    assert result.policy_allowed is False
    assert result.error == "decision provider must return a runtime_loop.Decision"
    assert policy.calls == 0
    assert echo_tool.calls == []
    assert [event.kind for event in ledger.list_events("ws_loop")] == [
        "input.user_message",
        "runtime.decision.rejected",
        "decision.recorded",
    ]
    journal = ledger.list_events("ws_loop")[-1].payload["record"]
    assert journal["outcome"] == "malformed_decision"
    assert journal["policy_allowed"] is False
    assert journal["error"] == "decision provider must return a runtime_loop.Decision"
    assert result.decision_outcome == "malformed_decision"




def test_loop_tool_handler_exception_is_caught_and_journaled_as_tool_failed():
    class FailingTool:
        def execute(self, context, arguments):
            raise RuntimeError("boom")

    runtime, ledger, _, _ = make_loop(
        LoopDecision(
            kind="call_tool",
            tool_name="echo",
            tool_args={"message": "explode"},
            reason="registered handler may fail",
        ),
        handlers={"echo": FailingTool()},
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="echo explode"))

    assert result.tool_name == "echo"
    assert result.tool_result is None
    assert result.policy_allowed is True
    assert result.error == "tool echo failed: boom"
    assert result.decision_outcome == "tool_failed"
    assert [event.kind for event in ledger.list_events("ws_loop")] == [
        "input.user_message",
        "tool.failure",
        "decision.recorded",
    ]
    journal = ledger.list_events("ws_loop")[-1].payload["record"]
    assert journal["outcome"] == "tool_failed"
    assert journal["selected_tool_args"] == {"message": "explode"}
    assert journal["error"] == "tool echo failed: boom"


def test_loop_keeps_policy_tool_projection_boundaries_out_of_decision_journal():
    import seed_runtime.decision_journal as decision_journal

    source = open("seed_runtime/decision_journal.py", encoding="utf-8").read()

    assert decision_journal.DecisionJournal.event_kind == "decision.recorded"
    assert "PolicyGate" not in source
    assert "ToolRegistry" not in source
    assert "ProjectionStore" not in source
    assert "execute(" not in source


def test_loop_loads_state_through_projection_path():
    class CountingProjector:
        def __init__(self, ledger):
            self._projector = StateProjector(ledger)
            self.calls = 0

        def project(self, workspace_id):
            self.calls += 1
            return self._projector.project(workspace_id)

    ledger = EventLedger()
    projector = CountingProjector(ledger)
    runtime, _, provider, _ = make_loop(
        LoopDecision(kind="answer", text="projected", reason="ok"),
        ledger=ledger,
        projector=projector,
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="project"))

    assert result.error is None
    assert projector.calls == 1
    assert provider.last_context.state.workspace_id == "ws_loop"
    assert provider.last_context.decision_context.projection_version == "v1"
    assert (
        provider.last_context.decision_context.last_event_id
        == result.events_appended[0]
    )


def test_loop_does_not_add_projection_responsibilities_to_event_ledger():
    assert not hasattr(EventLedger, "project")
    assert not hasattr(EventLedger, "load_snapshot")
    assert not hasattr(EventLedger, "save_snapshot")
    assert project_state_with_cache.__module__ == "seed_runtime.projection_store"


def test_loop_has_no_shell_subprocess_or_network_behavior():
    source = open("seed_runtime/runtime_loop.py", encoding="utf-8").read()

    forbidden_fragments = [
        "import os",
        "import subprocess",
        "from subprocess",
        "socket",
        "requests",
        "urllib",
        "http.client",
        "importlib",
        "exec(",
        "eval(",
    ]
    assert [fragment for fragment in forbidden_fragments if fragment in source] == []
