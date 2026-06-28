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


@dataclass(frozen=True)
class OperationSelectionResult:
    """Result of resolving one selected registered operation.

    Operation selection consumes an already-selected operation name from a
    ``call_tool`` decision. It does not rank capability recommendations, inspect
    handoff metadata, or choose between providers.
    """

    ok: bool
    errors: list[str]
    operation: ToolSpec | None = None

    @classmethod
    def selected(cls, operation: ToolSpec) -> "OperationSelectionResult":
        return cls(ok=True, errors=[], operation=operation)

    @classmethod
    def rejected(cls, *errors: str) -> "OperationSelectionResult":
        return cls(ok=False, errors=list(errors), operation=None)


class ToolValidationService:
    """Validate registered tool calls using Seed's existing validation rules.

    The service keeps operation selection separate from capability
    recommendation: recommendation surfaces bounded possibilities in the
    request_tool path, while operation selection resolves the single registered
    operation named by an already-formed call_tool decision.
    """

    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.registry = registry or ToolRegistry()

    def require_tool(self, tool_name: str) -> ToolSpec:
        """Return a registered tool or raise the registry's existing error."""

        return self.registry.require(tool_name)

    def select_operation(
        self, operation_name: str, state: State | None = None
    ) -> OperationSelectionResult:
        """Resolve the single registered operation named by a call_tool decision.

        This preserves the existing registry/state lookup behavior and only
        names the boundary explicitly: selection starts from an operation name,
        not from catalog provider recommendations or capability handoff metadata.
        """

        operation = self.registry.get(operation_name)
        if operation is None and state is not None:
            operation = state.tools.get(operation_name)
        if operation is None:
            return OperationSelectionResult.rejected(
                f"unknown tool {operation_name!r}"
            )
        return OperationSelectionResult.selected(operation)

    def validate_tool_exists(
        self, tool_name: str, state: State | None = None
    ) -> ToolValidationResult:
        selection = self.select_operation(tool_name, state)
        if not selection.ok or selection.operation is None:
            return ToolValidationResult.invalid(*selection.errors)
        return ToolValidationResult.valid(selection.operation)

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
        selection = self.select_operation(tool_name)
        if not selection.ok or selection.operation is None:
            # Preserve the historical execution-path exception for unknown tools.
            self.require_tool(tool_name)
        tool = selection.operation
        status = self.validate_tool_status(tool)
        if not status.ok:
            return status
        return self.validate_input_schema(tool, arguments)
