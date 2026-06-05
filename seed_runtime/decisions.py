"""Decision parsing and validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from seed_runtime.models import Decision
from seed_runtime.registry import ToolRegistry
from seed_runtime.tool_validation import ToolValidationService
from seed_runtime.state import State

_VALID_NAME = re.compile(r"^[a-z][a-z0-9_]{1,63}$")


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: list[str]

    @classmethod
    def valid(cls) -> "ValidationResult":
        return cls(ok=True, errors=[])

    @classmethod
    def invalid(cls, *errors: str) -> "ValidationResult":
        return cls(ok=False, errors=list(errors))


class DecisionValidator:
    """Validate structured model decisions against current runtime state."""

    def __init__(
        self,
        registry: ToolRegistry | None = None,
        tool_validation: ToolValidationService | None = None,
    ) -> None:
        self.registry = registry or ToolRegistry()
        self.tool_validation = tool_validation or ToolValidationService(self.registry)

    def validate(self, decision: Decision, state: State | None = None) -> ValidationResult:
        errors: list[str] = []
        if decision.kind == "answer":
            if not decision.answer:
                errors.append("answer decisions require answer")
        elif decision.kind == "ask_question":
            if not decision.question:
                errors.append("ask_question decisions require question")
        elif decision.kind == "request_tool":
            errors.extend(self._validate_tool_need(decision.tool_need))
        elif decision.kind == "call_tool":
            errors.extend(self._validate_tool_call(decision, state))
        elif decision.kind == "propose_state_patch":
            if not decision.state_patch:
                errors.append("propose_state_patch decisions require state_patch")
        elif decision.kind == "refuse":
            if not decision.reason:
                errors.append("refuse decisions require reason")
        else:
            errors.append(f"unsupported decision kind {decision.kind!r}")
        return ValidationResult(ok=not errors, errors=errors)

    def _validate_tool_need(self, tool_need: dict[str, Any] | None) -> list[str]:
        if not tool_need:
            return ["request_tool decisions require tool_need"]
        errors: list[str] = []
        name = tool_need.get("name")
        if not isinstance(name, str) or not _VALID_NAME.match(name):
            errors.append("tool_need.name must be snake_case and 2-64 characters")
        summary = tool_need.get("summary")
        if not isinstance(summary, str) or len(summary.strip()) < 10:
            errors.append("tool_need.summary must be at least 10 characters")
        capability = tool_need.get("capability")
        if not isinstance(capability, str) or not _VALID_NAME.match(capability):
            errors.append("tool_need.capability is required and must be snake_case")
        return errors

    def _validate_tool_call(self, decision: Decision, state: State | None) -> list[str]:
        if not decision.tool_name:
            return ["call_tool decisions require tool_name"]
        validation = self.tool_validation.validate_tool_input(
            decision.tool_name, decision.tool_arguments, state
        )
        return validation.errors
