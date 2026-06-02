"""Intent-classifier adapter for small/local decision models.

Small models can return a compact intent label plus lightweight arguments. Seed then
builds the full runtime Decision deterministically so the model does not have to
hand-author every Decision field.
"""

from __future__ import annotations

import json
import re
from importlib.util import find_spec
from typing import Any, Literal, Protocol, Sequence

from seed_runtime.base import SeedModel
from seed_runtime.context import ContextPacket
from seed_runtime.model_client import (
    CommandTransport,
    DecisionParseError,
    EndpointTransport,
    TextCompletionTransport,
)
from seed_runtime.models import Decision
from seed_runtime.serialization import to_plain

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field

IntentLabel = Literal["echo", "answer", "missing_tool", "clarify", "refuse"]

_VALID_TOOL_NAME_CHARS = re.compile(r"[^a-z0-9]+")
_CATEGORY_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\b(weather|forecast|temperature)\b", re.IGNORECASE), "weather_lookup"),
    (re.compile(r"\b(install|setup|set\s+up)\b", re.IGNORECASE), "installation"),
    (re.compile(r"\b(check|status|inspect)\b", re.IGNORECASE), "inspection"),
)


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


class IntentPromptModelClient:
    """Render intent-only prompts and delegate completion to a text transport."""

    def __init__(self, transport: TextCompletionTransport) -> None:
        self.transport = transport

    @classmethod
    def for_endpoint(
        cls,
        url: str,
        *,
        prompt_field: str = "prompt",
        timeout_seconds: float = 30.0,
        extra_payload: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> "IntentPromptModelClient":
        return cls(
            EndpointTransport(
                url=url,
                prompt_field=prompt_field,
                timeout_seconds=timeout_seconds,
                extra_payload=extra_payload or {},
                headers=headers or {},
            )
        )

    @classmethod
    def for_command(
        cls,
        command: Sequence[str],
        *,
        timeout_seconds: float = 60.0,
        env: dict[str, str] | None = None,
    ) -> "IntentPromptModelClient":
        return cls(
            CommandTransport(command=command, timeout_seconds=timeout_seconds, env=env)
        )

    def complete(self, context: ContextPacket) -> str:
        return self.transport.complete(build_intent_prompt(context))


class TextIntentClassifier:
    """IntentClassifier adapter around an intent-prompt model client."""

    def __init__(
        self,
        client: IntentPromptModelClient,
        parser: StrictJSONIntentParser | None = None,
    ) -> None:
        self.client = client
        self.parser = parser or StrictJSONIntentParser()

    @classmethod
    def for_transport(
        cls,
        transport: TextCompletionTransport,
        parser: StrictJSONIntentParser | None = None,
    ) -> "TextIntentClassifier":
        return cls(IntentPromptModelClient(transport), parser=parser)

    @classmethod
    def for_endpoint(
        cls,
        url: str,
        *,
        prompt_field: str = "prompt",
        timeout_seconds: float = 30.0,
        extra_payload: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        parser: StrictJSONIntentParser | None = None,
    ) -> "TextIntentClassifier":
        return cls(
            IntentPromptModelClient.for_endpoint(
                url=url,
                prompt_field=prompt_field,
                timeout_seconds=timeout_seconds,
                extra_payload=extra_payload,
                headers=headers,
            ),
            parser=parser,
        )

    @classmethod
    def for_command(
        cls,
        command: Sequence[str],
        *,
        timeout_seconds: float = 60.0,
        env: dict[str, str] | None = None,
        parser: StrictJSONIntentParser | None = None,
    ) -> "TextIntentClassifier":
        return cls(
            IntentPromptModelClient.for_command(
                command=command, timeout_seconds=timeout_seconds, env=env
            ),
            parser=parser,
        )

    def classify(self, context: ContextPacket) -> IntentClassification:
        return self.parser.parse(self.client.complete(context))


ParsedIntentClassifier = TextIntentClassifier


def build_intent_prompt(context: ContextPacket) -> str:
    """Build a provider-neutral prompt for intent-only classification."""

    context_json = _stable_json(_render_intent_context(to_plain(context)))
    shape_json = json.dumps(
        {
            "intent": "echo|answer|missing_tool|clarify|refuse",
            "reason": "...",
            "arguments": {},
        },
        indent=2,
    )
    return "\n\n".join(
        [
            "TASK INSTRUCTION\nClassify only the user's intent for the Seed runtime.",
            "INTENTS\necho, answer, missing_tool, clarify, refuse",
            "GUIDANCE\nUse answer only for conversational replies or questions that can be answered directly from the provided context.",
            "Use missing_tool when the user requests an action, lookup, installation, search, system operation, file operation, network operation, weather lookup, external information retrieval, or any capability that cannot be satisfied by visible tools.",
            "Never pretend to perform an action.",
            "Never answer with the requested action text.",
            "Never invent tool names.",
            "If no visible tool can satisfy the request, prefer missing_tool.",
            "EXAMPLES",
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


def _render_intent_context(packet: dict[str, Any]) -> dict[str, Any]:
    active_goal = packet.get("active_goal") or {}
    input_text = packet.get("current_input", {}).get("text")
    return _without_empty(
        {
            "input": {"text": input_text} if isinstance(input_text, str) else {},
            "goal": _without_empty(
                {
                    "summary": active_goal.get("summary"),
                    "status": active_goal.get("status"),
                    "open_questions": active_goal.get("open_questions"),
                }
            ),
            "entity_names": [
                entity["name"]
                for entity in packet.get("entities", [])
                if isinstance(entity.get("name"), str)
            ],
            "facts": [
                _without_empty(
                    {
                        "predicate": fact.get("predicate"),
                        "value": fact.get("value"),
                    }
                )
                for fact in packet.get("facts", [])
            ],
            "tools": [
                _without_empty(
                    {
                        "name": tool.get("name"),
                        "summary": tool.get("summary"),
                    }
                )
                for tool in sorted(
                    packet.get("tools", []), key=lambda tool: tool.get("name", "")
                )
            ],
            "open_tool_needs": [
                _without_empty(
                    {
                        "name": need.get("name"),
                        "summary": need.get("summary"),
                        "capability": need.get("capability"),
                    }
                )
                for need in packet.get("open_tool_needs", [])
            ],
        }
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
            tool_need = _normalize_tool_need(arguments, _input_text(context))
            return Decision(
                kind="request_tool",
                reason=reason,
                tool_need=tool_need,
            )
        if classification.intent == "clarify":
            question = str(arguments.get("question") or "What would you like me to do?")
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


def _normalize_tool_need(arguments: dict[str, Any], text: str) -> dict[str, str]:
    name = _tool_name(arguments, text)
    summary = str(arguments.get("summary") or _tool_summary(name, text))
    capability = _snake_name(str(arguments.get("capability") or name))
    return {"name": name, "summary": summary, "capability": capability}


def _tool_name(arguments: dict[str, Any], text: str) -> str:
    for key in ("name", "tool_name"):
        value = arguments.get(key)
        if isinstance(value, str) and value.strip():
            return _snake_name(value)
    category = _tool_need_category(text)
    if category == "weather_lookup":
        return category
    if category == "installation":
        install_target = _imperative_target(text, ("install", "setup", "set up"))
        if install_target:
            action = (
                "setup"
                if text.strip().lower().startswith(("setup", "set up"))
                else "install"
            )
            return _snake_name(f"{action} {install_target}")
        return category
    if category == "inspection":
        inspect_target = _imperative_target(text, ("check", "status", "inspect"))
        if inspect_target:
            action = "inspect" if text.strip().lower().startswith("inspect") else "check"
            return _snake_name(f"{action} {inspect_target}")
        return category
    return _snake_name(text) or "missing_tool"


def _tool_summary(name: str, text: str) -> str:
    category = _tool_need_category(text)
    if category == "weather_lookup":
        return "Look up weather information."
    if category == "installation" and name == category:
        return "Provide installation or setup support."
    if category == "inspection" and name == category:
        return "Inspect or check the requested status."
    source = text.strip() or name
    return f"Provide the missing capability for: {source}."


def _tool_need_category(text: str) -> str | None:
    for pattern, category in _CATEGORY_PATTERNS:
        if pattern.search(text):
            return category
    return None


def _imperative_target(text: str, verbs: tuple[str, ...]) -> str:
    stripped = text.strip()
    for verb in sorted(verbs, key=len, reverse=True):
        match = re.match(
            rf"^{re.escape(verb)}\b[\s:,-]*(?P<target>.+)$",
            stripped,
            re.IGNORECASE,
        )
        if match:
            return match.group("target").strip()
    return ""


def _snake_name(value: str) -> str:
    stripped = value.strip().lower()
    name = _VALID_TOOL_NAME_CHARS.sub("_", stripped).strip("_")
    return name[:64] or "missing_tool"


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _without_empty(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: item
        for key, item in value.items()
        if item is not None and item != [] and item != {}
    }
