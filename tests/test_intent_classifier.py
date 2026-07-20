import json

import pytest

from seed_runtime.context import DecisionInputPacket
from seed_runtime.context_views import (
    ContextCapability,
    ContextFact,
    ContextIssue,
    ContextRequirement,
    ContextSummary,
    DecisionContextView,
)
from seed_runtime.intent_classifier import (
    IntentClassification,
    IntentPromptModelClient,
    StrictJSONIntentParser,
    TextIntentClassifier,
    build_intent_prompt,
)
from seed_runtime.model_client import DecisionParseError
from seed_runtime.state import State


class FakeTransport:
    def __init__(self, response: str) -> None:
        self.response = response
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


def context_for(text: str) -> DecisionInputPacket:
    return DecisionInputPacket(
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


def test_build_intent_prompt_renders_context_and_intent_only_shape():
    prompt = build_intent_prompt(context_for("what is the weather?"))

    assert "Classify only the user's intent for the Seed runtime." in prompt
    assert '"text":"what is the weather?"' in prompt
    assert '"intent": "echo|answer|missing_tool|clarify|refuse"' in prompt
    assert '"reason": "..."' in prompt
    assert '"arguments": {}' in prompt
    assert "Return only JSON, no markdown, no prose." in prompt
    assert "kind" not in prompt
    assert "call_tool" not in prompt
    assert "ALLOWED JSON DECISION SHAPES" not in prompt


def test_build_intent_prompt_explains_answer_and_missing_tool_boundaries():
    prompt = build_intent_prompt(context_for("install docker"))

    assert (
        "Use answer only for conversational replies or questions that can be answered "
        "directly from the provided context."
    ) in prompt
    assert (
        "Use missing_tool when the user requests an action, lookup, installation, "
        "search, system operation, file operation, network operation, weather lookup, "
        "external information retrieval, observations of the world, or any capability "
        "that cannot be satisfied by visible tools."
    ) in prompt
    assert "Never pretend to perform an action." in prompt
    assert "Never answer with the requested action text." in prompt
    assert "Never invent tool names." in prompt
    assert "If no visible tool can satisfy the request, prefer missing_tool." in prompt


def test_build_intent_prompt_includes_general_missing_capability_examples():
    prompt = build_intent_prompt(context_for("check disk usage"))

    assert 'User: "echo hello"\n-> intent: echo' in prompt
    assert 'User: "what tools do you have?"\n-> intent: answer' in prompt
    assert 'User: "What is Docker?"\n-> intent: answer' in prompt
    assert 'User: "Explain Kubernetes."\n-> intent: answer' in prompt
    assert 'User: "install docker"\n-> intent: missing_tool' in prompt
    assert 'User: "check disk usage"\n-> intent: missing_tool' in prompt
    assert (
        'User: "what is the weather in Jacksonville?"\n-> intent: missing_tool'
        in prompt
    )


def test_text_intent_classifier_uses_intent_prompt_client_and_parses_intent():
    transport = FakeTransport(
        json.dumps(
            {
                "intent": "missing_tool",
                "reason": "needs weather tool",
                "arguments": {"name": "weather_lookup"},
            },
            separators=(",", ":"),
        )
    )
    client = IntentPromptModelClient(transport)
    classifier = TextIntentClassifier(client)
    context = context_for("what is the weather?")

    classification = classifier.classify(context)

    assert len(transport.prompts) == 1
    assert '"text":"what is the weather?"' in transport.prompts[0]
    assert classification.intent == "missing_tool"
    assert classification.reason == "needs weather tool"
    assert classification.arguments == {"name": "weather_lookup"}


def test_strict_json_intent_parser_defaults_missing_arguments_to_empty_dict():
    classification = StrictJSONIntentParser().parse(
        json.dumps({"intent": "answer", "reason": "Can answer directly."})
    )

    assert classification.arguments == {}


def test_strict_json_intent_parser_defaults_null_arguments_to_empty_dict():
    classification = StrictJSONIntentParser().parse(
        json.dumps(
            {
                "intent": "clarify",
                "reason": "Need more detail.",
                "arguments": None,
            }
        )
    )

    assert classification.arguments == {}


def test_strict_json_intent_parser_rejects_non_object_arguments():
    with pytest.raises(DecisionParseError, match="arguments must be a JSON object"):
        StrictJSONIntentParser().parse(
            json.dumps(
                {
                    "intent": "answer",
                    "reason": "Can answer directly.",
                    "arguments": [],
                }
            )
        )


def test_strict_json_intent_parser_wraps_invalid_intent_validation():
    with pytest.raises(
        DecisionParseError, match="intent classification failed validation"
    ):
        StrictJSONIntentParser().parse(
            json.dumps(
                {
                    "intent": "invalid",
                    "reason": "Unsupported intent label.",
                    "arguments": {},
                }
            )
        )


def test_text_intent_classifier_uses_strict_json_intent_parser():
    transport = FakeTransport(
        json.dumps(
            {
                "intent": "answer",
                "reason": "Can answer directly.",
                "arguments": {},
                "kind": "answer",
            }
        )
    )
    client = IntentPromptModelClient(transport)
    classifier = TextIntentClassifier(client)

    with pytest.raises(DecisionParseError, match="unexpected fields: kind"):
        classifier.classify(context_for("hello"))

def test_context_packet_prompt_still_uses_legacy_context_shape():
    prompt = build_intent_prompt(context_for("hello"))

    assert '"input":{"text":"hello"}' in prompt
    assert '"decision_context"' not in prompt
    assert '"metadata"' not in prompt
