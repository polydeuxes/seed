import json

import pytest

from seed_runtime.context import ContextPacket
from seed_runtime.intent_classifier import (
    DecisionBuilder,
    FakeIntentClassifier,
    IntentClassification,
    IntentDecisionModel,
    TextIntentClassifier,
    build_intent_prompt,
)
from seed_runtime.model_client import DecisionParseError


class FakeModelClient:
    def __init__(self, response: str) -> None:
        self.response = response
        self.last_context: ContextPacket | None = None

    def complete(self, context: ContextPacket) -> str:
        self.last_context = context
        return self.response


def context_for(text: str) -> ContextPacket:
    return ContextPacket(
        workspace_id="workspace-1",
        session_id="session-1",
        current_input={"event_id": "event-1", "text": text},
        active_goal=None,
        entities=[],
        facts=[],
        tools=[],
        open_tool_needs=[],
        decision_schema={
            "kinds": ["answer", "ask_question", "call_tool", "request_tool", "refuse"]
        },
    )


def test_echo_prefix_uses_deterministic_fallback_without_model():
    classifier = FakeIntentClassifier(
        IntentClassification(
            intent="refuse",
            reason="This classifier should not be called for deterministic echo.",
            arguments={},
        )
    )
    model = IntentDecisionModel(classifier)

    decision = model.decide(context_for("echo hello"))

    assert decision.kind == "call_tool"
    assert decision.tool_name == "echo"
    assert decision.tool_arguments == {"message": "hello"}
    assert classifier.last_context is None


def test_missing_tool_intent_requests_install_docker_tool():
    classifier = FakeIntentClassifier(
        IntentClassification(
            intent="missing_tool",
            reason="No registered tool can install Docker.",
            arguments={
                "name": "install_docker",
                "summary": "Install Docker on the requested system.",
                "capability": "install_docker",
            },
        )
    )
    model = IntentDecisionModel(classifier)

    decision = model.decide(context_for("install docker"))

    assert decision.kind == "request_tool"
    assert decision.tool_need == {
        "name": "install_docker",
        "summary": "Install Docker on the requested system.",
        "capability": "install_docker",
    }


def test_clarify_intent_asks_question_for_unknown_vague_input():
    decision = DecisionBuilder().build(
        context_for("unknown vague input"),
        IntentClassification(
            intent="clarify",
            reason="The request is too vague to act on.",
            arguments={"question": "What outcome do you want?"},
        ),
    )

    assert decision.kind == "ask_question"
    assert decision.question == "What outcome do you want?"


def test_build_intent_prompt_renders_context_and_intent_only_shape():
    prompt = build_intent_prompt(context_for("what is the weather?"))

    assert "You are classifying the user's intent for the Seed runtime." in prompt
    assert '"text":"what is the weather?"' in prompt
    assert '"intent":"echo|answer|missing_tool|clarify|refuse"' in prompt
    assert '"reason":"..."' in prompt
    assert '"arguments":{}' in prompt
    assert "Return only JSON, no markdown, no prose." in prompt
    assert '"kind":"call_tool"' not in prompt


def test_text_intent_classifier_wraps_model_client_and_parses_intent():
    client = FakeModelClient(
        json.dumps(
            {
                "intent": "missing_tool",
                "reason": "No registered tool can check weather.",
                "arguments": {"name": "weather_lookup"},
            },
            separators=(",", ":"),
        )
    )
    classifier = TextIntentClassifier(client)
    context = context_for("what is the weather?")

    classification = classifier.classify(context)

    assert client.last_context is context
    assert classification.intent == "missing_tool"
    assert classification.reason == "No registered tool can check weather."
    assert classification.arguments == {"name": "weather_lookup"}


def test_text_intent_classifier_uses_strict_json_intent_parser():
    client = FakeModelClient(
        json.dumps(
            {
                "intent": "answer",
                "reason": "Can answer directly.",
                "arguments": {},
                "kind": "answer",
            }
        )
    )
    classifier = TextIntentClassifier(client)

    with pytest.raises(DecisionParseError, match="unexpected fields: kind"):
        classifier.classify(context_for("hello"))
