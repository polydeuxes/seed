from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.model_client import DecisionParseError
from seed_runtime.models import Decision, RuntimeResponse
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel, Runtime
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


class SequenceDecisionModel:
    def __init__(self, decisions):
        self.decisions = list(decisions)
        self.contexts = []

    def decide(self, context):
        self.contexts.append(context)
        return self.decisions.pop(0)


def make_runtime(decision, *, max_decision_retries=1):
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    model = decision if hasattr(decision, "decide") else FakeDecisionModel(decision)
    runtime = Runtime(
        ledger,
        projector,
        ContextComposer(registry),
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        model,
        max_decision_retries=max_decision_retries,
    )
    return runtime, ledger, model


def test_routes_answer():
    runtime, ledger, _ = make_runtime(
        Decision(kind="answer", reason="ok", answer="done")
    )
    response = runtime.handle_user_message("ws", "ses", "hi")
    assert response.kind == "answer"
    assert ledger.list_events("ws")[-1].kind == "response.answer"


def test_routes_question():
    runtime, _, _ = make_runtime(
        Decision(kind="ask_question", reason="need", question="Which host?")
    )
    assert runtime.handle_user_message("ws", "ses", "install ssh").kind == "question"


def test_routes_request_tool():
    decision = Decision(
        kind="request_tool",
        reason="missing",
        tool_need={
            "name": "install_ssh_server",
            "summary": "Install and start SSH server",
            "capability": "ssh_access",
        },
    )
    runtime, ledger, _ = make_runtime(decision)
    response = runtime.handle_user_message("ws", "ses", "install ssh")
    assert response.kind == "tool_need"
    assert "tool_need.created" in [event.kind for event in ledger.list_events("ws")]


def test_routes_call_tool():
    runtime, _, _ = make_runtime(
        Decision(
            kind="call_tool",
            reason="safe",
            tool_name="echo",
            tool_arguments={"message": "hi"},
        )
    )
    response = runtime.handle_user_message("ws", "ses", "echo hi")
    assert isinstance(response, RuntimeResponse)
    assert response.kind == "tool_result"
    assert response.payload["output"]["message"] == "hi"


def test_routes_refuse():
    runtime, ledger, _ = make_runtime(
        Decision(kind="refuse", reason="unsafe request")
    )

    response = runtime.handle_user_message("ws", "ses", "do unsafe thing")

    assert response.kind == "refusal"
    assert response.message == "unsafe request"
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "response.refusal",
    ]
    assert ledger.list_events("ws")[-1].payload == {"reason": "unsafe request"}


def test_mvp_echo_loop_records_result_event_and_projects_tool_output_evidence():
    runtime, ledger, model = make_runtime(
        Decision(
            kind="call_tool",
            reason="safe deterministic echo",
            tool_name="echo",
            tool_arguments={"message": "hello"},
        )
    )

    response = runtime.handle_user_message("ws", "ses", "echo hello")
    projected_state = runtime.projector.project("ws")

    assert response.kind == "tool_result"
    assert response.payload["output"] == {
        "ok": True,
        "message": "hello",
        "workspace_id": "ws",
    }
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "tool.call.started",
        "tool.call.completed",
        "evidence.observed",
    ]
    assert model.last_context.current_input["text"] == "echo hello"
    assert [tool["name"] for tool in model.last_context.tools] == ["echo"]
    assert projected_state.workspace_id == "ws"
    assert projected_state.open_tool_needs == []
    assert len(projected_state.evidence) == 1
    assert next(iter(projected_state.evidence.values())).source == "tool:echo"


def test_mvp_request_tool_loop_records_need_and_projects_open_state():
    runtime, ledger, model = make_runtime(
        Decision(
            kind="request_tool",
            reason="missing safe capability",
            tool_need={
                "name": "lookup_service_status",
                "summary": "Look up service status from recorded host inventory",
                "capability": "service_status_lookup",
            },
        )
    )

    response = runtime.handle_user_message("ws", "ses", "check service")
    projected_state = runtime.projector.project("ws")

    assert response.kind == "tool_need"
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "tool_need.created",
    ]
    assert model.last_context.current_input["text"] == "check service"
    assert [need.name for need in projected_state.open_tool_needs] == [
        "lookup_service_status"
    ]


def test_retries_invalid_first_decision_with_corrected_valid_decision():
    model = SequenceDecisionModel(
        [
            Decision(kind="answer", reason="missing answer"),
            Decision(kind="answer", reason="corrected", answer="done"),
        ]
    )
    runtime, ledger, model = make_runtime(model)

    response = runtime.handle_user_message("ws", "ses", "hi")

    assert response.kind == "answer"
    assert response.message == "done"
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "model.decision.invalid",
        "model.decision.proposed",
        "response.answer",
    ]
    assert model.contexts[0].retry_prompt is None
    assert model.contexts[1].retry_prompt == {
        "instruction": "Return exactly one corrected JSON decision that satisfies the decision_schema.",
        "retry_number": 1,
        "max_retries": 1,
        "invalid_event_id": ledger.list_events("ws")[2].id,
        "validation_errors": ["answer decisions require answer"],
        "invalid_decision": {
            "kind": "answer",
            "reason": "missing answer",
            "answer": None,
            "question": None,
            "tool_name": None,
            "tool_arguments": {},
            "tool_need": None,
            "action_plan": None,
            "handoff_plan": None,
            "state_patch": None,
        },
    }


def test_invalid_first_and_second_decision_returns_invalid_decision():
    model = SequenceDecisionModel(
        [
            Decision(kind="answer", reason="missing answer"),
            Decision(kind="ask_question", reason="missing question"),
        ]
    )
    runtime, ledger, _ = make_runtime(model)

    response = runtime.handle_user_message("ws", "ses", "hi")

    assert response.kind == "invalid_decision"
    assert response.payload == {"errors": ["ask_question decisions require question"]}
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "model.decision.invalid",
        "model.decision.proposed",
        "model.decision.invalid",
    ]


def test_decision_and_invalid_decision_events_are_recorded_deterministically():
    model = SequenceDecisionModel(
        [
            Decision(kind="answer", reason="missing answer"),
            Decision(kind="ask_question", reason="missing question"),
        ]
    )
    runtime, ledger, _ = make_runtime(model, max_decision_retries=1)

    runtime.handle_user_message("ws", "ses", "hi")

    events = ledger.list_events("ws")
    first_proposed = events[1]
    first_invalid = events[2]
    second_proposed = events[3]
    second_invalid = events[4]
    assert first_proposed.payload["attempt"] == 0
    assert first_invalid.payload == {
        "errors": ["answer decisions require answer"],
        "attempt": 0,
    }
    assert first_invalid.causation_id == first_proposed.id
    assert second_proposed.payload["attempt"] == 1
    assert second_invalid.payload == {
        "errors": ["ask_question decisions require question"],
        "attempt": 1,
    }
    assert second_invalid.causation_id == second_proposed.id


class SequenceParseDecisionModel:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.contexts = []

    def decide(self, context):
        self.contexts.append(context)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, DecisionParseError):
            raise outcome
        return outcome


def test_retries_parse_failed_first_decision_with_valid_decision():
    model = SequenceParseDecisionModel(
        [
            DecisionParseError("model response is not valid JSON: Expecting value"),
            Decision(kind="answer", reason="corrected", answer="done"),
        ]
    )
    runtime, ledger, model = make_runtime(model)

    response = runtime.handle_user_message("ws", "ses", "hi")

    assert response.kind == "answer"
    assert response.message == "done"
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.parse_failed",
        "model.decision.proposed",
        "response.answer",
    ]
    parse_failed = ledger.list_events("ws")[1]
    assert parse_failed.payload == {
        "attempt": 0,
        "parse_error": "model response is not valid JSON: Expecting value",
    }
    assert parse_failed.causation_id == ledger.list_events("ws")[0].id
    assert model.contexts[0].retry_prompt is None
    assert model.contexts[1].retry_prompt == {
        "instruction": "Your previous output was not valid strict JSON. Return only one JSON decision object matching the decision_schema, with no prose, markdown, code fences, or extra text.",
        "retry_number": 1,
        "max_retries": 1,
        "invalid_event_id": parse_failed.id,
        "parse_error": "model response is not valid JSON: Expecting value",
    }


def test_exhausted_parse_failures_return_invalid_decision_and_record_events():
    first_error = DecisionParseError("model response must be a JSON object")
    second_error = DecisionParseError("decision requires kind and reason")
    second_error.raw_failure_classification = "missing_required_fields"
    model = SequenceParseDecisionModel([first_error, second_error])
    runtime, ledger, _ = make_runtime(model, max_decision_retries=1)

    response = runtime.handle_user_message("ws", "ses", "hi")

    assert response.kind == "invalid_decision"
    assert response.message == "Model decision failed parsing."
    assert response.payload == {"errors": ["decision requires kind and reason"]}
    events = ledger.list_events("ws")
    assert [event.kind for event in events] == [
        "input.user_message",
        "model.decision.parse_failed",
        "model.decision.parse_failed",
    ]
    assert events[1].payload == {
        "attempt": 0,
        "parse_error": "model response must be a JSON object",
    }
    assert events[1].causation_id == events[0].id
    assert events[2].payload == {
        "attempt": 1,
        "parse_error": "decision requires kind and reason",
        "raw_failure_classification": "missing_required_fields",
    }
    assert events[2].causation_id == events[0].id

# RuntimeLoop v1 deterministic execution tests
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
