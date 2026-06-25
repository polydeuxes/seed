"""Model client contracts, prompt adapters, and strict JSON decision parsing."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from typing import Any, Protocol, Sequence
from urllib import request

from seed_runtime.context import DecisionInputPacket
from seed_runtime.models import Decision
from seed_runtime.serialization import to_plain


class ModelClient(Protocol):
    def complete(self, context: DecisionInputPacket) -> str: ...


class TextCompletionTransport(Protocol):
    """Transport that turns a rendered prompt into raw model text."""

    def complete(self, prompt: str) -> str: ...


def render_decision_prompt(context: DecisionInputPacket) -> str:
    """Render a deterministic compact prompt for one model decision.

    Only fields that help the model choose a runtime decision are included. Runtime
    bookkeeping such as workspace/session ids, event ids, policy actions, and tool
    implementation details are intentionally omitted from the prompt.
    """

    packet = to_plain(context)
    allowed_kinds = packet["decision_schema"].get(
        "kinds",
        [
            "answer",
            "ask_question",
            "call_tool",
            "request_tool",
            "propose_state_patch",
            "refuse",
        ],
    )
    sections = [
        (
            "TASK INSTRUCTION",
            "Choose exactly one decision for the Seed runtime.",
        ),
        ("CURRENT INPUT", _stable_json(_render_current_input(packet["current_input"]))),
        ("RELEVANT STATE SUMMARY", _stable_json(_render_state_summary(packet))),
        ("VISIBLE TOOLS", _stable_json(_render_visible_tools(packet["tools"]))),
        (
            "OPEN TOOL NEEDS",
            _stable_json(_render_open_tool_needs(packet["open_tool_needs"])),
        ),
        (
            "ALLOWED JSON DECISION SHAPES",
            _stable_json(_decision_shapes(allowed_kinds)),
        ),
        (
            "STRICT OUTPUT",
            "Output only one JSON object matching one allowed shape. Do not include prose, markdown, code fences, or multiple objects.",
        ),
    ]
    if packet.get("retry_prompt"):
        sections.append(("CORRECTION REQUIRED", _stable_json(packet["retry_prompt"])))
    return "\n\n".join(f"{heading}\n{body}" for heading, body in sections)


def serialize_decision_prompt(context: DecisionInputPacket) -> str:
    """Backward-compatible alias for :func:`render_decision_prompt`."""

    return render_decision_prompt(context)


def _render_current_input(current_input: dict[str, Any]) -> dict[str, Any]:
    return _without_empty(
        {
            key: value
            for key, value in current_input.items()
            if key not in {"event_id", "workspace_id", "session_id"}
        }
    )


def _render_state_summary(packet: dict[str, Any]) -> dict[str, Any]:
    entities = packet.get("entities", [])
    entity_names = _entity_name_by_id(entities)
    return _without_empty(
        {
            "active_goal": _render_active_goal(packet.get("active_goal")),
            "entities": [_render_entity(entity) for entity in entities],
            "facts": [
                _render_fact(fact, entity_names) for fact in packet.get("facts", [])
            ],
            "evidence": [
                _render_evidence(evidence)
                for evidence in packet.get("evidence", [])
            ],
        }
    )


def _render_active_goal(goal: dict[str, Any] | None) -> dict[str, Any] | None:
    if not goal:
        return None
    return _without_empty(
        {
            "summary": goal.get("summary"),
            "status": goal.get("status"),
            "facts": goal.get("facts"),
            "open_questions": goal.get("open_questions"),
            "related_entities": goal.get("related_entities"),
        }
    )


def _render_entity(entity: dict[str, Any]) -> dict[str, Any]:
    return _without_empty(
        {
            "kind": entity.get("kind"),
            "name": entity.get("name"),
            "aliases": entity.get("aliases"),
            "attributes": entity.get("attributes"),
            "confidence": entity.get("confidence"),
        }
    )


def _render_fact(fact: dict[str, Any], entity_names: dict[str, str]) -> dict[str, Any]:
    return _without_empty(
        {
            "subject": entity_names.get(fact.get("subject_id", "")),
            "predicate": fact.get("predicate"),
            "value": fact.get("value"),
            "confidence": fact.get("confidence"),
            "expires_at": fact.get("expires_at"),
        }
    )


def _render_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    return _without_empty(
        {
            "source": evidence.get("source"),
            "kind": evidence.get("kind"),
            "payload": evidence.get("payload"),
            "confidence": evidence.get("confidence"),
        }
    )


def _entity_name_by_id(entities: list[dict[str, Any]]) -> dict[str, str]:
    return {
        entity["id"]: entity["name"]
        for entity in entities
        if isinstance(entity.get("id"), str) and isinstance(entity.get("name"), str)
    }


def _render_visible_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        _without_empty(
            {
                "name": tool.get("name"),
                "summary": tool.get("summary"),
                "input_schema": tool.get("input_schema"),
                "output_schema": tool.get("output_schema"),
                "risk_class": tool.get("risk_class"),
            }
        )
        for tool in sorted(tools, key=lambda tool: tool.get("name", ""))
    ]


def _render_open_tool_needs(needs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        _without_empty(
            {
                "name": need.get("name"),
                "summary": need.get("summary"),
                "capability": need.get("capability"),
                "reason": need.get("reason"),
                "risk_hint": need.get("risk_hint"),
                "desired_inputs": need.get("desired_inputs"),
                "desired_outputs": need.get("desired_outputs"),
            }
        )
        for need in sorted(needs, key=lambda need: need.get("name", ""))
    ]


def _decision_shapes(allowed_kinds: list[str]) -> list[dict[str, Any]]:
    shapes: dict[str, dict[str, Any]] = {
        "answer": {"kind": "answer", "reason": "...", "answer": "..."},
        "ask_question": {"kind": "ask_question", "reason": "...", "question": "..."},
        "call_tool": {
            "kind": "call_tool",
            "reason": "...",
            "tool_name": "visible_tool_name",
            "tool_arguments": {},
        },
        "request_tool": {
            "kind": "request_tool",
            "reason": "...",
            "tool_need": {
                "name": "snake_case_name",
                "summary": "What the missing tool should do.",
                "capability": "capability_name",
            },
        },
        "propose_state_patch": {
            "kind": "propose_state_patch",
            "reason": "...",
            "state_patch": {},
        },
        "refuse": {"kind": "refuse", "reason": "..."},
    }
    return [shapes[kind] for kind in allowed_kinds if kind in shapes]


def _without_empty(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: item
        for key, item in value.items()
        if item is not None and item != [] and item != {}
    }


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
        http_request = request.Request(
            self.url, data=body, headers=headers, method="POST"
        )
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
    """Concrete ModelClient that renders DecisionInputPacket prompts then delegates transport."""

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
        return cls(
            CommandTransport(command=command, timeout_seconds=timeout_seconds, env=env)
        )

    def complete(self, context: DecisionInputPacket) -> str:
        return self.transport.complete(render_decision_prompt(context))


class DecisionParseError(ValueError):
    """Raised when a model response is not a strict decision object."""


class StrictJSONDecisionParser:
    """Parse model text into a Decision without accepting prose wrappers."""

    def parse(self, text: str) -> Decision:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise DecisionParseError(
                f"model response is not valid JSON: {exc.msg}"
            ) from exc
        if not isinstance(data, dict):
            raise DecisionParseError("model response must be a JSON object")
        if "kind" not in data or "reason" not in data:
            raise DecisionParseError("decision requires kind and reason")
        allowed = {
            "kind",
            "reason",
            "answer",
            "question",
            "tool_name",
            "tool_arguments",
            "tool_need",
            "state_patch",
        }
        extra = sorted(set(data) - allowed)
        if extra:
            raise DecisionParseError(
                f"decision contains unexpected fields: {', '.join(extra)}"
            )
        return Decision(**data)


class ParsedDecisionProducer:
    """DecisionProducer adapter around a text-generating model client."""

    def __init__(
        self, client: ModelClient, parser: StrictJSONDecisionParser | None = None
    ) -> None:
        self.client = client
        self.parser = parser or StrictJSONDecisionParser()

    def decide(self, decision_input: DecisionInputPacket) -> Decision:
        return self.parser.parse(self.client.complete(decision_input))


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


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
