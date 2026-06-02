"""Model client contracts, prompt adapters, and strict JSON decision parsing."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from typing import Any, Protocol, Sequence
from urllib import request

from seed_runtime.context import ContextPacket
from seed_runtime.models import Decision
from seed_runtime.serialization import to_plain


class ModelClient(Protocol):
    def complete(self, context: ContextPacket) -> str:
        ...


class TextCompletionTransport(Protocol):
    """Transport that turns a rendered prompt into raw model text."""

    def complete(self, prompt: str) -> str:
        ...


def serialize_decision_prompt(context: ContextPacket) -> str:
    """Serialize a ContextPacket into the stable small-model decision form.

    The format intentionally uses fixed section headings and JSON bodies so a
    small model sees the same structure every turn while the parser still owns
    strict output validation.
    """

    packet = to_plain(context)
    state = {
        "workspace_id": packet["workspace_id"],
        "session_id": packet["session_id"],
        "active_goal": packet["active_goal"],
        "entities": packet["entities"],
        "facts": packet["facts"],
        "open_tool_needs": packet["open_tool_needs"],
    }
    output_schema = {
        "instruction": "Return only one JSON object. Do not include prose, markdown, or code fences.",
        "required_fields": ["kind", "reason"],
        "allowed_kinds": packet["decision_schema"].get(
            "kinds",
            ["answer", "ask_question", "call_tool", "request_tool", "propose_state_patch", "refuse"],
        ),
        "allowed_fields": [
            "kind",
            "reason",
            "answer",
            "question",
            "tool_name",
            "tool_arguments",
            "tool_need",
            "state_patch",
        ],
        "examples": {
            "answer": {"kind": "answer", "reason": "The context contains the answer.", "answer": "..."},
            "ask_question": {"kind": "ask_question", "reason": "A required field is missing.", "question": "..."},
            "call_tool": {
                "kind": "call_tool",
                "reason": "A visible tool can satisfy the request.",
                "tool_name": "tool_name",
                "tool_arguments": {},
            },
            "request_tool": {
                "kind": "request_tool",
                "reason": "No visible safe tool can satisfy the request.",
                "tool_need": {"name": "snake_case_name", "summary": "What the missing tool should do.", "capability": "capability_name"},
            },
            "refuse": {"kind": "refuse", "reason": "The request is unsafe or unsupported."},
        },
    }
    sections = [
        ("TASK", "Choose one decision for the Seed runtime."),
        ("CURRENT INPUT", _stable_json(packet["current_input"])),
        ("STATE", _stable_json(state)),
        ("TOOLS", _stable_json(packet["tools"])),
        ("OUTPUT JSON SCHEMA", _stable_json(output_schema)),
    ]
    return "\n\n".join(f"{heading}\n{body}" for heading, body in sections)


@dataclass(frozen=True)
class EndpointTransport:
    """POST prompts to a small/local HTTP model endpoint.

    The endpoint receives JSON with a configurable prompt field and may return
    either plain text or common JSON completion shapes such as ``text``,
    ``completion``, ``response``, or OpenAI-style ``choices``.
    """

    url: str
    prompt_field: str = "prompt"
    timeout_seconds: float = 30.0
    extra_payload: dict[str, Any] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)

    def complete(self, prompt: str) -> str:
        payload = {**self.extra_payload, self.prompt_field: prompt}
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json", **self.headers}
        http_request = request.Request(self.url, data=body, headers=headers, method="POST")
        with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
            raw = response.read().decode("utf-8")
        return _extract_model_text(raw)


@dataclass(frozen=True)
class CommandTransport:
    """Run a local model command, writing the prompt to stdin."""

    command: Sequence[str]
    timeout_seconds: float = 60.0
    env: dict[str, str] | None = None

    def complete(self, prompt: str) -> str:
        completed = subprocess.run(
            list(self.command),
            input=prompt,
            text=True,
            capture_output=True,
            timeout=self.timeout_seconds,
            check=True,
            env=self.env,
        )
        return completed.stdout


class DecisionPromptModelClient:
    """Concrete ModelClient that renders ContextPacket prompts then delegates transport."""

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
    ) -> "DecisionPromptModelClient":
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
    ) -> "DecisionPromptModelClient":
        return cls(CommandTransport(command=command, timeout_seconds=timeout_seconds, env=env))

    def complete(self, context: ContextPacket) -> str:
        return self.transport.complete(serialize_decision_prompt(context))


class DecisionParseError(ValueError):
    """Raised when a model response is not a strict decision object."""


class StrictJSONDecisionParser:
    """Parse model text into a Decision without accepting prose wrappers."""

    def parse(self, text: str) -> Decision:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise DecisionParseError(f"model response is not valid JSON: {exc.msg}") from exc
        if not isinstance(data, dict):
            raise DecisionParseError("model response must be a JSON object")
        if "kind" not in data or "reason" not in data:
            raise DecisionParseError("decision requires kind and reason")
        allowed = {"kind", "reason", "answer", "question", "tool_name", "tool_arguments", "tool_need", "state_patch"}
        extra = sorted(set(data) - allowed)
        if extra:
            raise DecisionParseError(f"decision contains unexpected fields: {', '.join(extra)}")
        return Decision(**data)


class ParsedDecisionModel:
    """DecisionModel adapter around a text-generating model client."""

    def __init__(self, client: ModelClient, parser: StrictJSONDecisionParser | None = None) -> None:
        self.client = client
        self.parser = parser or StrictJSONDecisionParser()

    def decide(self, context: ContextPacket) -> Decision:
        return self.parser.parse(self.client.complete(context))


def _stable_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, separators=(",", ": "))


def _extract_model_text(raw: str) -> str:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    if isinstance(data, str):
        return data
    if not isinstance(data, dict):
        return raw
    for key in ("text", "completion", "response", "content"):
        value = data.get(key)
        if isinstance(value, str):
            return value
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            text = first.get("text")
            if isinstance(text, str):
                return text
            message = first.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
    return raw
