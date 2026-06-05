"""Shared model transport utilities for canonical RuntimeLoop providers.

The canonical provider-facing input is ``seed_runtime.runtime_loop.RuntimeContext``.
This module intentionally contains only transport/error helpers used by local
intent-classifier adapters; it no longer renders or parses legacy context-packet prompts.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from typing import Protocol, Sequence
from urllib import request


class TextCompletionTransport(Protocol):
    """Transport that turns a rendered prompt into raw model text."""

    def complete(self, prompt: str) -> str: ...


class DecisionParseError(ValueError):
    """Raised when a model response is not strict JSON for the expected shape."""


@dataclass(frozen=True)
class EndpointTransport:
    """POST prompts to a small/local HTTP model endpoint."""

    url: str
    prompt_field: str = "prompt"
    timeout_seconds: float = 30.0
    extra_payload: dict[str, object] = field(default_factory=dict)
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
