import pytest
from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.context_views import DecisionContextView
from seed_runtime.events import EventLedger
from seed_runtime.evidence import Evidence
from seed_runtime.execution import ToolExecutor
from seed_runtime.model_client import DecisionParseError
from seed_runtime.models import Decision, Fact, RuntimeResponse, utc_now
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel, Runtime
from seed_runtime.serialization import to_plain
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


def test_runtime_rejects_propose_action_plan_decision():
    runtime, ledger, _ = make_runtime(
        Decision(
            kind="propose_action_plan",
            reason="legacy planning side path",
            action_plan={"summary": "Plan something outside current core."},
        ),
        max_decision_retries=0,
    )

    response = runtime.handle_user_message("ws", "ses", "make a plan")

    assert response.kind == "invalid_decision"
    assert response.payload == {
        "errors": ["unsupported decision kind 'propose_action_plan'"]
    }
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "model.decision.invalid",
    ]
    assert "action_plan.created" not in [
        event.kind for event in ledger.list_events("ws")
    ]


def test_runtime_rejects_propose_handoff_plan_decision():
    runtime, ledger, _ = make_runtime(
        Decision(
            kind="propose_handoff_plan",
            reason="legacy handoff side path",
            handoff_plan={"operation": "legacy.side_path", "executable": False},
        ),
        max_decision_retries=0,
    )

    response = runtime.handle_user_message("ws", "ses", "handoff this")

    assert response.kind == "invalid_decision"
    assert response.payload == {
        "errors": ["unsupported decision kind 'propose_handoff_plan'"]
    }
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "model.decision.invalid",
    ]
    assert "handoff_plan.created" not in [
        event.kind for event in ledger.list_events("ws")
    ]

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
from seed_runtime.intent_classifier import (
    FakeIntentClassifier,
    IntentClassification,
    IntentDecisionModel,
)
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
            summary="RuntimeLoop test operations.",
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


class RaisingLoopDecisionProvider:
    def __init__(self, exc):
        self.exc = exc
        self.contexts = []

    def decide(self, context):
        self.contexts.append(context)
        raise self.exc


class ExplodingLoopPolicy:
    def evaluate(self, tool, state, *, scope=None):  # pragma: no cover - failure path
        raise AssertionError("policy must not be evaluated")


class ExplodingLoopTool:
    def execute(self, context, arguments):  # pragma: no cover - failure path
        raise AssertionError("operation implementation must not be executed")


@pytest.mark.experimental_runtime_loop
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


@pytest.mark.experimental_runtime_loop
def test_loop_provider_exception_returns_failure_result_and_journals_event():
    provider = RaisingLoopDecisionProvider(RuntimeError("provider exploded"))
    runtime, ledger, provider, _ = make_loop(
        provider,
        policy_engine=ExplodingLoopPolicy(),
        handlers={"echo": ExplodingLoopTool()},
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="hello"))

    assert result.decision_kind is None
    assert result.response_text is None
    assert result.policy_allowed is False
    assert result.error == "provider exploded"
    assert result.decision_outcome == "provider_failed"
    assert result.decision_id is not None
    assert result.context_hash is not None
    assert result.decision_reason == ""
    assert len(provider.contexts) == 1
    assert [event.kind for event in ledger.list_events("ws_loop")] == [
        "input.user_message",
        "runtime.decision.provider_failed",
        "decision.recorded",
    ]
    assert result.events_appended == [
        event.id for event in ledger.list_events("ws_loop")
    ]
    provider_failed = ledger.list_events("ws_loop")[1]
    assert provider_failed.payload == {
        "error": "provider exploded",
        "exception_type": "RuntimeError",
    }
    assert provider_failed.causation_id == ledger.list_events("ws_loop")[0].id
    journal = ledger.list_events("ws_loop")[-1].payload["record"]
    assert journal["decision_id"] == result.decision_id
    assert journal["decision_kind"] is None
    assert journal["reason"] == ""
    assert journal["context_hash"] == result.context_hash
    assert journal["policy_allowed"] is False
    assert journal["outcome"] == "provider_failed"
    assert journal["error"] == "provider exploded"
    assert ledger.list_events("ws_loop")[-1].causation_id == provider_failed.id
    assert (
        ledger.list_events("ws_loop")[-1].correlation_id
        == ledger.list_events("ws_loop")[0].id
    )


@pytest.mark.experimental_runtime_loop
def test_loop_provider_exception_does_not_append_decision_rejected():
    runtime, ledger, _, _ = make_loop(
        RaisingLoopDecisionProvider(ValueError("bad provider")),
        policy_engine=ExplodingLoopPolicy(),
        handlers={"echo": ExplodingLoopTool()},
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="hello"))

    assert result.decision_outcome == "provider_failed"
    assert "runtime.decision.rejected" not in [
        event.kind for event in ledger.list_events("ws_loop")
    ]


@pytest.mark.experimental_runtime_loop
def test_loop_malformed_returned_decision_still_uses_decision_rejected():
    runtime, ledger, _, echo_tool = make_loop(
        {"kind": "answer", "text": "not a Decision"}
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="hello"))

    assert result.decision_outcome == "malformed_decision"
    assert result.error == "decision provider must return a runtime_loop.Decision"
    assert echo_tool.calls == []
    assert [event.kind for event in ledger.list_events("ws_loop")] == [
        "input.user_message",
        "runtime.decision.rejected",
        "decision.recorded",
    ]
    assert ledger.list_events("ws_loop")[-1].payload["record"]["outcome"] == (
        "malformed_decision"
    )


@pytest.mark.experimental_runtime_loop
def test_old_runtime_parse_retry_behavior_remains_unchanged():
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
    assert model.contexts[1].retry_prompt["instruction"].startswith(
        "Your previous output was not valid strict JSON."
    )


@pytest.mark.experimental_runtime_loop
@pytest.mark.skip(reason="RuntimeLoop intent-model adaptation is quarantined; Runtime is canonical")
def test_loop_clarify_intent_is_answered_and_journaled_as_answer():
    question = "Which host should I inspect?"
    provider = IntentDecisionModel(
        FakeIntentClassifier(
            IntentClassification(
                intent="clarify",
                reason="needs target host",
                arguments={"question": question},
            )
        )
    )
    runtime, ledger, _, _ = make_loop(provider)

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="check ssh"))

    assert result.decision_kind == "answer"
    assert question in (result.response_text or "")
    assert result.policy_allowed is True
    assert result.decision_outcome == "answered"
    events = ledger.list_events("ws_loop")
    assert [event.kind for event in events] == [
        "input.user_message",
        "assistant.answer",
        "decision.recorded",
    ]
    assert events[1].payload["text"] == question
    journal = events[-1].payload["record"]
    assert journal["decision_kind"] == "answer"
    assert journal["outcome"] == "answered"


@pytest.mark.experimental_runtime_loop
@pytest.mark.skip(reason="RuntimeLoop intent-model adaptation is quarantined; Runtime is canonical")
def test_loop_refuse_intent_is_answered_and_journaled_as_answer():
    refusal = "I can’t help with that unsafe request."
    provider = IntentDecisionModel(
        FakeIntentClassifier(
            IntentClassification(
                intent="refuse",
                reason="unsafe request",
                arguments={"refusal": refusal},
            )
        )
    )
    runtime, ledger, _, _ = make_loop(provider)

    result = runtime.run(
        RuntimeInput(workspace_id="ws_loop", user_text="disable all safety controls")
    )

    assert result.decision_kind == "answer"
    assert refusal in (result.response_text or "")
    assert result.policy_allowed is True
    assert result.decision_outcome == "answered"
    events = ledger.list_events("ws_loop")
    assert [event.kind for event in events] == [
        "input.user_message",
        "assistant.answer",
        "decision.recorded",
    ]
    assert events[1].payload["text"] == refusal
    journal = events[-1].payload["record"]
    assert journal["decision_kind"] == "answer"
    assert journal["outcome"] == "answered"


@pytest.mark.experimental_runtime_loop
def test_loop_provider_receives_decision_context_without_changing_existing_fields():
    runtime, _, provider, _ = make_loop(
        LoopDecision(kind="answer", text="done", reason="context available")
    )

    runtime_input = RuntimeInput(
        workspace_id="ws_loop",
        user_text="hello",
        metadata={"request_id": "req-1"},
    )

    runtime.run(runtime_input)

    assert isinstance(provider.last_context.decision_context, DecisionContextView)
    assert provider.last_context.state.workspace_id == "ws_loop"
    assert provider.last_context.current_input == {
        "text": "hello",
        "metadata": {"request_id": "req-1"},
    }
    assert provider.last_context.tools == [
        {
            "name": "echo",
            "summary": "Echo a message deterministically.",
            "policy_action": "echo.run",
            "risk_class": "L1",
        }
    ]


@pytest.mark.experimental_runtime_loop
def test_loop_decision_context_is_built_from_projected_state_for_run():
    ledger = EventLedger()
    evidence = Evidence(
        id="evd_runtime_loop",
        workspace_id="ws_loop",
        source="test",
        kind="user_input",
        observed_at=utc_now(),
        payload={"summary": "service status"},
        confidence=1.0,
    )
    ledger.append(
        "evidence.observed",
        "ws_loop",
        {"evidence": to_plain(evidence)},
    )
    fact = Fact(
        id="fact_runtime_loop",
        subject_id="service-a",
        predicate="status",
        value="active",
        evidence_ids=["evd_runtime_loop"],
        observed_at=utc_now(),
        confidence=0.95,
    )
    ledger.append("fact.observed", "ws_loop", {"fact": to_plain(fact)})
    runtime, _, provider, _ = make_loop(
        LoopDecision(kind="answer", text="projected", reason="state view"),
        ledger=ledger,
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="status?"))

    assert result.error is None
    assert provider.last_context.state.last_event_id == result.events_appended[0]
    assert provider.last_context.decision_context.last_event_id == result.events_appended[0]
    assert [fact.fact_id for fact in provider.last_context.decision_context.facts] == [
        "fact_runtime_loop"
    ]
    assert provider.last_context.decision_context.summary.facts_count == 1


@pytest.mark.experimental_runtime_loop
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
        "evidence.observed",
        "decision.recorded",
    ]
    assert ledger.list_events("ws_loop")[-3].payload["output"]["message"] == "hello"
    journal = ledger.list_events("ws_loop")[-1].payload["record"]
    assert journal["selected_tool_name"] == "echo"
    assert journal["outcome"] == "tool_succeeded"
    assert result.decision_outcome == "tool_succeeded"


@pytest.mark.experimental_runtime_loop
def test_loop_tool_decision_records_projected_evidence_from_extractable_output():
    runtime, ledger, _, _ = make_loop(
        LoopDecision(
            kind="call_tool",
            tool_name="echo",
            tool_args={"message": "project me"},
            reason="record tool output evidence",
        )
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="echo evidence"))
    projected_state = StateProjector(ledger).project("ws_loop")

    assert result.error is None
    assert "evidence.observed" in [event.kind for event in ledger.list_events("ws_loop")]
    assert len(projected_state.evidence) == 1
    evidence = next(iter(projected_state.evidence.values()))
    assert evidence.source == "tool:echo"
    assert evidence.kind == "tool.output"
    assert evidence.payload == {
        "ok": True,
        "message": "project me",
        "workspace_id": "ws_loop",
    }


@pytest.mark.experimental_runtime_loop
def test_loop_request_tool_decision_appends_tool_need_and_journal():
    runtime, ledger, _, _ = make_loop(
        LoopDecision(
            kind="request_tool",
            reason="missing capability",
            tool_need={
                "name": "Lookup Service Status",
                "summary": "Look up service status from inventory",
                "capability": "Service Status Lookup",
            },
        )
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="check service"))

    assert result.decision_kind == "request_tool"
    assert result.response_text == "Recorded tool need lookup_service_status."
    assert result.policy_allowed is True
    assert result.error is None
    assert result.decision_outcome == "tool_requested"
    assert [event.kind for event in ledger.list_events("ws_loop")] == [
        "input.user_message",
        "tool_need.created",
        "decision.recorded",
    ]
    need_payload = ledger.list_events("ws_loop")[-2].payload["tool_need"]
    assert need_payload["name"] == "lookup_service_status"
    assert need_payload["summary"] == "Look up service status from inventory"
    assert need_payload["capability"] == "service_status_lookup"
    journal = ledger.list_events("ws_loop")[-1].payload["record"]
    assert journal["decision_kind"] == "request_tool"
    assert journal["outcome"] == "tool_requested"
    assert journal["policy_allowed"] is True
    assert result.decision_id == journal["decision_id"]

@pytest.mark.experimental_runtime_loop
def test_loop_request_tool_projects_open_tool_need():
    runtime, ledger, _, _ = make_loop(
        LoopDecision(
            kind="request_tool",
            reason="missing lookup",
            tool_need={
                "name": "lookup_service_status",
                "summary": "Look up service status from inventory",
                "capability": "service_status_lookup",
            },
        )
    )

    runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="check service"))
    projected_state = StateProjector(ledger).project("ws_loop")

    assert [need.name for need in projected_state.open_tool_needs] == [
        "lookup_service_status"
    ]

@pytest.mark.experimental_runtime_loop
def test_loop_request_tool_rejects_missing_tool_need_payload():
    runtime, ledger, _, _ = make_loop(
        LoopDecision(kind="request_tool", reason="missing payload")
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="need tool"))

    assert result.decision_kind is None
    assert result.error == "request_tool decisions require tool_need dict"
    assert [event.kind for event in ledger.list_events("ws_loop")] == [
        "input.user_message",
        "runtime.decision.rejected",
        "decision.recorded",
    ]
    assert (
        ledger.list_events("ws_loop")[-1].payload["record"]["outcome"]
        == "malformed_decision"
    )

@pytest.mark.experimental_runtime_loop
def test_loop_request_tool_rejects_malformed_payload_and_forbidden_fields():
    cases = [
        (
            LoopDecision(
                kind="request_tool",
                reason="missing name",
                tool_need={"name": "", "summary": "Summary", "capability": "cap"},
            ),
            "request_tool decisions require non-empty name",
        ),
        (
            LoopDecision(
                kind="request_tool",
                reason="missing summary",
                tool_need={"name": "need", "summary": "", "capability": "cap"},
            ),
            "request_tool decisions require non-empty summary",
        ),
        (
            LoopDecision(
                kind="request_tool",
                reason="missing capability",
                tool_need={"name": "need", "summary": "Summary", "capability": ""},
            ),
            "request_tool decisions require non-empty capability",
        ),
        (
            LoopDecision(
                kind="request_tool",
                reason="forbidden tool fields",
                tool_name="echo",
                tool_args={"message": "hi"},
                text="no",
                tool_need={"name": "need", "summary": "Summary", "capability": "cap"},
            ),
            "request_tool decisions may not include tool_name, tool_args, or text",
        ),
    ]

    for decision, expected_error in cases:
        runtime, _, _, _ = make_loop(decision)
        result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="need tool"))
        assert result.error == expected_error
        assert result.decision_outcome == "malformed_decision"


@pytest.mark.experimental_runtime_loop
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


@pytest.mark.experimental_runtime_loop
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


@pytest.mark.experimental_runtime_loop
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


@pytest.mark.experimental_runtime_loop
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


@pytest.mark.experimental_runtime_loop
def test_loop_keeps_policy_tool_projection_boundaries_out_of_decision_journal():
    import seed_runtime.decision_journal as decision_journal

    source = open("seed_runtime/decision_journal.py", encoding="utf-8").read()

    assert decision_journal.DecisionJournal.event_kind == "decision.recorded"
    assert "PolicyGate" not in source
    assert "ToolRegistry" not in source
    assert "ProjectionStore" not in source
    assert "execute(" not in source


@pytest.mark.experimental_runtime_loop
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


@pytest.mark.experimental_runtime_loop
def test_loop_does_not_add_projection_responsibilities_to_event_ledger():
    assert not hasattr(EventLedger, "project")
    assert not hasattr(EventLedger, "load_snapshot")
    assert not hasattr(EventLedger, "save_snapshot")
    assert project_state_with_cache.__module__ == "seed_runtime.projection_store"


@pytest.mark.experimental_runtime_loop
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


@pytest.mark.experimental_runtime_loop
def test_loop_rejects_direct_ask_question_decision_kind_as_malformed():
    runtime, ledger, _, echo_tool = make_loop(
        LoopDecision(kind="ask_question", text="Which host?", reason="needs target")
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="check ssh"))

    assert result.decision_kind is None
    assert result.response_text is None
    assert result.policy_allowed is False
    assert result.decision_outcome == "malformed_decision"
    assert (
        result.error
        == "decision kind must be 'answer', 'call_tool', or 'request_tool'"
    )
    assert echo_tool.calls == []
    events = ledger.list_events("ws_loop")
    assert [event.kind for event in events] == [
        "input.user_message",
        "runtime.decision.rejected",
        "decision.recorded",
    ]
    assert events[1].payload["decision"]["kind"] == "ask_question"
    assert events[-1].payload["record"]["decision_kind"] == "ask_question"
    assert events[-1].payload["record"]["outcome"] == "malformed_decision"


@pytest.mark.experimental_runtime_loop
def test_loop_rejects_direct_refuse_decision_kind_as_malformed():
    runtime, ledger, _, echo_tool = make_loop(
        LoopDecision(kind="refuse", text="I can’t help with that.", reason="unsafe")
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="unsafe"))

    assert result.decision_kind is None
    assert result.response_text is None
    assert result.policy_allowed is False
    assert result.decision_outcome == "malformed_decision"
    assert (
        result.error
        == "decision kind must be 'answer', 'call_tool', or 'request_tool'"
    )
    assert echo_tool.calls == []
    events = ledger.list_events("ws_loop")
    assert [event.kind for event in events] == [
        "input.user_message",
        "runtime.decision.rejected",
        "decision.recorded",
    ]
    assert events[1].payload["decision"]["kind"] == "refuse"
    assert events[-1].payload["record"]["decision_kind"] == "refuse"
    assert events[-1].payload["record"]["outcome"] == "malformed_decision"


@pytest.mark.experimental_runtime_loop
def test_loop_rejects_state_patch_decision_kind_as_malformed():
    runtime, ledger, _, echo_tool = make_loop(
        LoopDecision(
            kind="propose_state_patch", reason="runtime loop does not patch state"
        )
    )

    result = runtime.run(
        RuntimeInput(workspace_id="ws_loop", user_text="remember state")
    )

    assert result.decision_kind is None
    assert result.decision_outcome == "malformed_decision"
    assert result.policy_allowed is False
    assert (
        result.error
        == "decision kind must be 'answer', 'call_tool', or 'request_tool'"
    )
    assert echo_tool.calls == []
    events = ledger.list_events("ws_loop")
    assert [event.kind for event in events] == [
        "input.user_message",
        "runtime.decision.rejected",
        "decision.recorded",
    ]
    assert events[1].payload == {
        "error": "decision kind must be 'answer', 'call_tool', or 'request_tool'",
        "decision": {
            "kind": "propose_state_patch",
            "text": None,
            "tool_name": None,
            "tool_args": {},
            "tool_need": None,
            "reason": "runtime loop does not patch state",
        },
    }
    assert events[-1].payload["record"]["outcome"] == "malformed_decision"
