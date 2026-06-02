"""Local chat model clients for Seed decision models.

These clients intentionally implement the existing runtime DecisionModel shape:
``decide(context: ContextPacket) -> Decision``. They live outside Runtime so local
provider details can be swapped without changing the runtime loop.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Literal
from urllib import request

from seed_runtime.context import ContextPacket
from seed_runtime.model_client import DecisionParseError
from seed_runtime.models import Decision
from seed_runtime.serialization import to_plain


DecisionJSONShape = dict[str, Any]


_ALLOWED_DECISION_SHAPES: list[DecisionJSONShape] = [
    {"kind": "answer", "reason": "...", "answer": "..."},
    {"kind": "ask_question", "reason": "...", "question": "..."},
    {
        "kind": "call_tool",
        "reason": "...",
        "tool_name": "visible_tool_name",
        "tool_arguments": {},
    },
    {
        "kind": "request_tool",
        "reason": "...",
        "tool_need": {
            "name": "snake_case_name",
            "summary": "What the missing tool should do.",
            "capability": "capability_name",
        },
    },
    {
        "kind": "propose_state_patch",
        "reason": "...",
        "state_patch": {},
    },
    {"kind": "refuse", "reason": "..."},
]


_DECISION_FIELDS = {
    "kind",
    "reason",
    "answer",
    "question",
    "tool_name",
    "tool_arguments",
    "tool_need",
    "state_patch",
}


@dataclass(frozen=True)
class LocalChatModel:
    """Base configuration shared by local chat-style model clients."""

    model_name: str
    endpoint_url: str
    timeout: float = 30.0
    temperature: float = 0.0
    max_tokens: int | None = None
    num_predict: int | None = None


class OllamaDecisionModel(LocalChatModel):
    """DecisionModel client for Ollama's local HTTP APIs."""

    def __init__(
        self,
        model_name: str,
        endpoint_url: str = "http://localhost:11434",
        *,
        timeout: float = 30.0,
        temperature: float = 0.0,
        max_tokens: int | None = None,
        num_predict: int | None = None,
        api: Literal["chat", "generate"] = "chat",
    ) -> None:
        if api not in {"chat", "generate"}:
            raise ValueError("api must be 'chat' or 'generate'")
        super().__init__(
            model_name=model_name,
            endpoint_url=endpoint_url,
            timeout=timeout,
            temperature=temperature,
            max_tokens=max_tokens,
            num_predict=num_predict,
        )
        self.api = api

    def decide(self, context: ContextPacket) -> Decision:
        prompt = build_decision_prompt(context)
        if self.api == "generate":
            payload = self._generate_payload(prompt)
            url = _join_url(self.endpoint_url, "/api/generate")
        else:
            payload = self._chat_payload(prompt)
            url = _join_url(self.endpoint_url, "/api/chat")
        response = _post_json(url, payload, timeout=self.timeout)
        return parse_decision_text(_extract_ollama_text(response))

    def _chat_payload(self, prompt: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "format": "json",
            "options": self._ollama_options(),
        }
        return _without_none_or_empty(payload)

    def _generate_payload(self, prompt: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": self._ollama_options(),
        }
        return _without_none_or_empty(payload)

    def _ollama_options(self) -> dict[str, Any]:
        options: dict[str, Any] = {"temperature": self.temperature}
        predict = self.num_predict if self.num_predict is not None else self.max_tokens
        if predict is not None:
            options["num_predict"] = predict
        return options


class LlamaCppDecisionModel(LocalChatModel):
    """DecisionModel client for llama.cpp OpenAI-compatible chat completions."""

    def __init__(
        self,
        model_name: str,
        endpoint_url: str = "http://localhost:8080",
        *,
        timeout: float = 30.0,
        temperature: float = 0.0,
        max_tokens: int | None = None,
        num_predict: int | None = None,
    ) -> None:
        super().__init__(
            model_name=model_name,
            endpoint_url=endpoint_url,
            timeout=timeout,
            temperature=temperature,
            max_tokens=max_tokens,
            num_predict=num_predict,
        )

    def decide(self, context: ContextPacket) -> Decision:
        response = _post_json(
            _join_url(self.endpoint_url, "/v1/chat/completions"),
            self._chat_completions_payload(build_decision_prompt(context)),
            timeout=self.timeout,
        )
        return parse_decision_text(_extract_openai_chat_text(response))

    def _chat_completions_payload(self, prompt: str) -> dict[str, Any]:
        max_tokens = self.max_tokens if self.max_tokens is not None else self.num_predict
        payload: dict[str, Any] = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"},
        }
        return _without_none_or_empty(payload)


def build_decision_prompt(context: ContextPacket) -> str:
    """Build the strict JSON prompt shared by all local decision clients."""

    context_json = _stable_json(to_plain(context.to_dict()))
    shape_json = _stable_json(_allowed_shapes_for_context(context))
    return "\n\n".join(
        [
            "You are choosing exactly one Decision for the Seed runtime.",
            f"CONTEXT JSON\n{context_json}",
            f"ALLOWED DECISION JSON SHAPE\n{shape_json}",
            "Return only JSON, no markdown, no prose.",
        ]
    )


def parse_decision_text(text: str) -> Decision:
    """Parse strict raw JSON model text into a Decision."""

    stripped = text.strip()
    if stripped != text:
        raise DecisionParseError("model response must be a JSON object with no wrapper")
    if stripped.startswith("```") or "```" in stripped:
        raise DecisionParseError("model response must not contain code fences")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise DecisionParseError(f"model response is not valid JSON: {exc.msg}") from exc
        
    if not isinstance(data, dict):
        raise DecisionParseError("model response must be a JSON object")

    # Local-model tolerance
    if "answer" in data and "kind" not in data:
        data["kind"] = "answer"

    if not isinstance(data.get("kind"), str):
        raise DecisionParseError("decision requires string kind")

    if not isinstance(data.get("reason"), str):
        data["reason"] = "local model omitted reason"

    extra = sorted(set(data) - _DECISION_FIELDS)
    if extra:
        raise DecisionParseError(
            f"decision contains unexpected fields: {', '.join(extra)}"
        )
    try:
        return Decision(**data)
    except Exception as exc:  # Pydantic and local compat raise different types.
        raise DecisionParseError(f"decision failed validation: {exc}") from exc


def _allowed_shapes_for_context(context: ContextPacket) -> list[DecisionJSONShape]:
    allowed = set(context.decision_schema.get("kinds", []))
    if not allowed:
        return list(_ALLOWED_DECISION_SHAPES)
    return [shape for shape in _ALLOWED_DECISION_SHAPES if shape["kind"] in allowed]


def _post_json(url: str, payload: dict[str, Any], *, timeout: float) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    http_request = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(http_request, timeout=timeout) as response:
        raw = response.read().decode("utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise DecisionParseError(f"local model response is not valid JSON: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise DecisionParseError("local model response must be a JSON object")
    return data


def _extract_ollama_text(response: dict[str, Any]) -> str:
    message = response.get("message")
    if isinstance(message, dict) and isinstance(message.get("content"), str):
        return message["content"]
    content = response.get("response")
    if isinstance(content, str):
        return content
    raise DecisionParseError("Ollama response did not include decision text")


def _extract_openai_chat_text(response: dict[str, Any]) -> str:
    choices = response.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
            text = first.get("text")
            if isinstance(text, str):
                return text
    raise DecisionParseError("chat completions response did not include decision text")


def _join_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}{path}"


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _without_none_or_empty(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if item is not None and item != {}}
