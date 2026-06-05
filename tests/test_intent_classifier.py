from seed_runtime.context_views import DecisionContextView
from seed_runtime.intent_classifier import (
    DecisionBuilder,
    FakeIntentClassifier,
    IntentClassification,
    IntentDecisionModel,
    build_intent_prompt,
)
from seed_runtime.runtime_loop import RuntimeContext
from seed_runtime.state import State


def context_for(text: str) -> RuntimeContext:
    return RuntimeContext(
        workspace_id="ws",
        run_id="run",
        state=State(workspace_id="ws"),
        current_input={"text": text},
        tools=[{"name": "echo", "summary": "Echo text."}],
        decision_context=DecisionContextView(projection_version="v1"),
    )


def test_echo_fallback_builds_runtime_loop_tool_decision():
    decision = IntentDecisionModel().decide(context_for("echo hello"))

    assert decision.kind == "call_tool"
    assert decision.tool_name == "echo"
    assert decision.tool_args == {"message": "hello"}


def test_informational_questions_become_answers_without_classifier():
    classifier = FakeIntentClassifier(
        IntentClassification(
            intent="missing_tool",
            reason="Small model incorrectly requested a tool.",
            arguments={"name": "what_is_docker"},
        )
    )
    model = IntentDecisionModel(classifier)

    for text, topic in (
        ("What is Docker?", "Docker"),
        ("who is Grace Hopper", "Grace Hopper"),
        ("Explain Kubernetes.", "Kubernetes"),
        ("define containerization", "containerization"),
    ):
        decision = model.decide(context_for(text))

        assert decision.kind == "answer"
        assert topic in (decision.text or "")

    assert classifier.last_context is None


def test_missing_tool_intent_is_answered_with_visible_tool_boundary():
    classifier = FakeIntentClassifier(
        IntentClassification(
            intent="missing_tool",
            reason="No registered tool can install Docker.",
            arguments={"capability": "docker_installation"},
        )
    )
    decision = IntentDecisionModel(classifier).decide(context_for("install docker"))

    assert decision.kind == "answer"
    assert "docker_installation" in (decision.text or "")


def test_clarify_intent_becomes_answer_text_for_runtime_loop():
    decision = DecisionBuilder().build(
        context_for("unknown vague input"),
        IntentClassification(
            intent="clarify",
            reason="The request is too vague to act on.",
            arguments={"question": "What outcome do you want?"},
        ),
    )

    assert decision.kind == "answer"
    assert decision.text == "What outcome do you want?"


def test_build_intent_prompt_renders_runtime_context_and_intent_only_shape():
    prompt = build_intent_prompt(context_for("what is the weather?"))

    assert "Classify only the user's intent for the Seed runtime." in prompt
    assert '"text":"what is the weather?"' in prompt
    assert '"intent": "echo|answer|missing_tool|clarify|refuse"' in prompt
    assert '"reason": "..."' in prompt
    assert '"arguments": {}' in prompt
