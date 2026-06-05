"""Shared registered-tool validation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.models import ToolSpec
from seed_runtime.registry import ToolRegistry
from seed_runtime.schema import SchemaValidationError, validate_schema_value
from seed_runtime.state import State


@dataclass(frozen=True)
class ToolValidationResult:
    """Result of validating a tool lookup or schema check."""

    ok: bool
    errors: list[str]
    tool: ToolSpec | None = None

    @classmethod
    def valid(cls, tool: ToolSpec | None = None) -> "ToolValidationResult":
        return cls(ok=True, errors=[], tool=tool)

    @classmethod
    def invalid(
        cls, *errors: str, tool: ToolSpec | None = None
    ) -> "ToolValidationResult":
        return cls(ok=False, errors=list(errors), tool=tool)


class ToolValidationService:
    """Validate registered tool calls using Seed's existing validation rules."""

    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.registry = registry or ToolRegistry()

    def require_tool(self, tool_name: str) -> ToolSpec:
        """Return a registered tool or raise the registry's existing error."""

        return self.registry.require(tool_name)

    def validate_tool_exists(
        self, tool_name: str, state: State | None = None
    ) -> ToolValidationResult:
        tool = self.registry.get(tool_name)
        if tool is None and state is not None:
            tool = state.tools.get(tool_name)
        if tool is None:
            return ToolValidationResult.invalid(f"unknown tool {tool_name!r}")
        return ToolValidationResult.valid(tool)

    def validate_tool_status(self, tool: ToolSpec) -> ToolValidationResult:
        if tool.status != "registered":
            return ToolValidationResult.invalid(
                f"tool {tool.name!r} is not registered", tool=tool
            )
        return ToolValidationResult.valid(tool)

    def validate_input_schema(
        self, tool: ToolSpec, arguments: dict[str, Any]
    ) -> ToolValidationResult:
        try:
            validate_schema_value(tool.input_schema, arguments)
        except SchemaValidationError as exc:
            return ToolValidationResult.invalid(str(exc), tool=tool)
        return ToolValidationResult.valid(tool)

    def validate_output_schema(
        self, tool: ToolSpec, output: Any
    ) -> ToolValidationResult:
        try:
            validate_schema_value(tool.output_schema, output)
        except SchemaValidationError as exc:
            return ToolValidationResult.invalid(str(exc), tool=tool)
        return ToolValidationResult.valid(tool)

    def validate_tool_input(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        state: State | None = None,
    ) -> ToolValidationResult:
        existence = self.validate_tool_exists(tool_name, state)
        if not existence.ok or existence.tool is None:
            return existence
        return self.validate_input_schema(existence.tool, arguments)

    def validate_executable_tool_call(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> ToolValidationResult:
        tool = self.require_tool(tool_name)
        status = self.validate_tool_status(tool)
        if not status.ok:
            return status
        return self.validate_input_schema(tool, arguments)
