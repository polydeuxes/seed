"""Deterministic guardrails for model tool-call intent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.models import Decision


@dataclass(frozen=True)
class ToolIntentValidation:
    """Result of checking whether a tool call matches the user's intent."""

    ok: bool
    errors: list[str]


class ToolIntentGuard:
    """Reject schema-valid tool calls that do not match deterministic intent rules.

    The guard is intentionally non-LLM and only applies rules that can be checked
    deterministically from the current input, the proposed decision, and the tools
    visible to the model.
    """

    def validate(
        self,
        current_input_text: str,
        decision: Decision,
        visible_tools: list[dict[str, Any]],
    ) -> ToolIntentValidation:
        if decision.kind != "call_tool":
            return ToolIntentValidation(ok=True, errors=[])

        visible_tool_names = {
            tool.get("name")
            for tool in visible_tools
            if isinstance(tool.get("name"), str)
        }
        if decision.tool_name not in visible_tool_names:
            return ToolIntentValidation(
                ok=False,
                errors=[f"tool {decision.tool_name!r} is not visible to the model"],
            )

        if decision.tool_name == "echo":
            return self._validate_echo(current_input_text, decision)

        return ToolIntentValidation(ok=True, errors=[])

    def _validate_echo(
        self, current_input_text: str, decision: Decision
    ) -> ToolIntentValidation:
        if not current_input_text.startswith("echo "):
            return ToolIntentValidation(
                ok=False,
                errors=["echo tool requires current input to start with 'echo '"],
            )

        expected_message = current_input_text[len("echo ") :]
        actual_message = decision.tool_arguments.get("message")
        if actual_message != expected_message:
            return ToolIntentValidation(
                ok=False,
                errors=["echo tool message must equal text after 'echo '"],
            )

        return ToolIntentValidation(ok=True, errors=[])
