from seed_runtime.context import ContextPacket
from seed_runtime.intent_classifier import (
    DecisionBuilder,
    FakeIntentClassifier,
    IntentClassification,
    IntentDecisionModel,
)


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
