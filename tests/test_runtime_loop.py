from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.model_client import DecisionParseError
from seed_runtime.models import Decision
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
    assert response.kind == "tool_result"
    assert response.payload["output"]["message"] == "hi"


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
