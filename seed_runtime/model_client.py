"""Model client contracts and strict JSON decision parsing."""

from __future__ import annotations

import json
from typing import Protocol

from seed_runtime.context import ContextPacket
from seed_runtime.models import Decision


class ModelClient(Protocol):
    def complete(self, context: ContextPacket) -> str:
        ...


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
