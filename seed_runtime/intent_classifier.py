"""Intent-classifier adapter for small/local decision models.

Small models can return a compact intent label plus lightweight arguments. Seed then
builds the full runtime Decision deterministically so the model does not have to
hand-author every Decision field.
"""

from __future__ import annotations

import json
import re
from importlib.util import find_spec
from typing import Any, Literal, Protocol

from seed_runtime.base import SeedModel
from seed_runtime.context import ContextPacket
from seed_runtime.model_client import DecisionParseError, ModelClient
from seed_runtime.models import Decision
from seed_runtime.serialization import to_plain

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field

IntentLabel = Literal["echo", "answer", "missing_tool", "clarify", "refuse"]

_VALID_TOOL_NAME_CHARS = re.compile(r"[^a-z0-9]+")


class IntentClassification(SeedModel):
    """Compact model output for intent-first decision making."""

    intent: IntentLabel
    reason: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class IntentClassifier(Protocol):
    """Classify a context packet into one compact intent label."""

    def classify(self, context: ContextPacket) -> IntentClassification: ...


class FakeIntentClassifier:
    """Test helper that returns a preconfigured intent classification."""

    def __init__(self, classification: IntentClassification) -> None:
        self.classification = classification
        self.last_context: ContextPacket | None = None

    def classify(self, context: ContextPacket) -> IntentClassification:
        self.last_context = context
        return self.classification


class StrictJSONIntentParser:
    """Parse strict raw JSON model text into an IntentClassification."""

    def parse(self, text: str) -> IntentClassification:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise DecisionParseError(
                f"model response is not valid JSON intent classification: {exc.msg}"
            ) from exc
        if not isinstance(data, dict):
            raise DecisionParseError("intent classification must be a JSON object")
        if "intent" not in data or "reason" not in data:
            raise DecisionParseError("intent classification requires intent and reason")
        allowed = {"intent", "reason", "arguments"}
        extra = sorted(set(data) - allowed)
        if extra:
            raise DecisionParseError(
                "intent classification contains unexpected fields: " + ", ".join(extra)
            )
        return IntentClassification(**data)


class TextIntentClassifier:
    """IntentClassifier adapter around any text-generating ModelClient."""

    def __init__(
        self, client: ModelClient, parser: StrictJSONIntentParser | None = None
    ) -> None:
        self.client = client
        self.parser = parser or StrictJSONIntentParser()

    def classify(self, context: ContextPacket) -> IntentClassification:
        return self.parser.parse(self.client.complete(context))


ParsedIntentClassifier = TextIntentClassifier


def build_intent_prompt(context: ContextPacket) -> str:
    """Build a provider-neutral prompt for intent-only classification."""

    context_json = _stable_json(to_plain(context.to_dict()))
    shape_json = json.dumps(
        {
            "intent": "echo|answer|missing_tool|clarify|refuse",
            "reason": "...",
            "arguments": {},
        },
        separators=(",", ":"),
    )
    return "\n\n".join(
        [
            "You are classifying the user's intent for the Seed runtime.",
            "Choose exactly one intent: echo, answer, missing_tool, clarify, refuse.",
            "Use answer only for conversational replies or questions that can be answered directly from the provided context.",
            "Use missing_tool when the user requests an action, lookup, installation, search, system operation, file operation, network operation, weather lookup, external information retrieval, or any capability that cannot be satisfied by visible tools.",
            "Never pretend to perform an action.",
            "Never answer with the requested action text.",
            "Never invent tool names.",
            "If no visible tool can satisfy the request, prefer missing_tool.",
            "FEW-SHOT EXAMPLES",
            'User: "echo hello"\n-> intent: echo',
            'User: "what tools do you have?"\n-> intent: answer',
            'User: "install docker"\n-> intent: missing_tool',
            'User: "check disk usage"\n-> intent: missing_tool',
            'User: "what is the weather in Jacksonville?"\n-> intent: missing_tool',
            f"CONTEXT JSON\n{context_json}",
            f"REQUIRED JSON OUTPUT\n{shape_json}",
            "Return only JSON, no markdown, no prose.",
        ]
    )


class DecisionBuilder:
    """Build full runtime decisions from compact intent classifications."""

    def build(
        self, context: ContextPacket, classification: IntentClassification
    ) -> Decision:
        arguments = classification.arguments
        reason = classification.reason or f"classified as {classification.intent}"
        if classification.intent == "echo":
            message = str(arguments.get("message") or _echo_message(_input_text(context)))
            return Decision(
                kind="call_tool",
                reason=reason,
                tool_name="echo",
                tool_arguments={"message": message},
            )
        if classification.intent == "answer":
            answer = str(arguments.get("answer") or arguments.get("message") or "")
            return Decision(kind="answer", reason=reason, answer=answer)
        if classification.intent == "missing_tool":
            name = _tool_name(arguments, _input_text(context))
            summary = str(
                arguments.get("summary")
                or f"Provide the missing capability for: {_input_text(context) or name}."
            )
            capability = _snake_name(str(arguments.get("capability") or name))
            return Decision(
                kind="request_tool",
                reason=reason,
                tool_need={
                    "name": name,
                    "summary": summary,
                    "capability": capability,
                },
            )
        if classification.intent == "clarify":
            question = str(
                arguments.get("question")
                or "What would you like me to do?"
            )
            return Decision(kind="ask_question", reason=reason, question=question)
        if classification.intent == "refuse":
            return Decision(kind="refuse", reason=reason)
        raise ValueError(f"unsupported intent {classification.intent!r}")


class IntentDecisionModel:
    """DecisionModel that asks for an intent label, then builds a Decision locally."""

    def __init__(
        self,
        classifier: IntentClassifier | None = None,
        builder: DecisionBuilder | None = None,
    ) -> None:
        self.classifier = classifier
        self.builder = builder or DecisionBuilder()

    def decide(self, context: ContextPacket) -> Decision:
        classification = deterministic_intent_fallback(context)
        if classification is None:
            if self.classifier is None:
                classification = IntentClassification(
                    intent="clarify",
                    reason="No intent classifier was configured and no deterministic fallback matched.",
                    arguments={"question": "What would you like me to do?"},
                )
            else:
                classification = self.classifier.classify(context)
        return self.builder.build(context, classification)


def deterministic_intent_fallback(
    context: ContextPacket,
) -> IntentClassification | None:
    """Classify trivial echo requests without calling a model."""

    text = _input_text(context)
    if text.lower().startswith("echo "):
        return IntentClassification(
            intent="echo",
            reason="Input starts with the deterministic echo prefix.",
            arguments={"message": text[5:]},
        )
    return None


def _input_text(context: ContextPacket) -> str:
    text = context.current_input.get("text")
    return text if isinstance(text, str) else ""


def _echo_message(text: str) -> str:
    return text[5:] if text.lower().startswith("echo ") else text


def _tool_name(arguments: dict[str, Any], text: str) -> str:
    for key in ("name", "tool_name"):
        value = arguments.get(key)
        if isinstance(value, str) and value.strip():
            return _snake_name(value)
    return _snake_name(text) or "missing_tool"


def _snake_name(value: str) -> str:
    stripped = value.strip().lower()
    name = _VALID_TOOL_NAME_CHARS.sub("_", stripped).strip("_")
    return name[:64] or "missing_tool"


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))
