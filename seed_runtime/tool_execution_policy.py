"""Shared tool validation and policy evaluation service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol

from seed_runtime.models import PolicyDecision, ToolSpec
from seed_runtime.policy import PolicyGate
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import State
from seed_runtime.tool_validation import ToolValidationResult, ToolValidationService


class PolicyEngine(Protocol):
    """Structural protocol for tool policy evaluators."""

    def evaluate(
        self, tool: ToolSpec, state: State, *, scope: str | None = None
    ) -> PolicyDecision: ...


@dataclass(frozen=True)
class RegisteredOperationValidationResult:
    """Result of validating a selected registered operation call.

    This result stops at operation contract validation. It says that the named
    registered operation exists, has executable registration status, and accepts
    the proposed input shape; it does not say policy authorizes execution now.
    """

    tool: ToolSpec | None
    validation: ToolValidationResult
    validation_phase: str | None = None

    @property
    def ok(self) -> bool:
        return self.validation.ok

    @property
    def error(self) -> str | None:
        if self.validation.ok:
            return None
        return "; ".join(self.validation.errors) if self.validation.errors else None


@dataclass(frozen=True)
class ToolExecutionPolicyResult:
    """Result of validating a registered operation and evaluating policy."""

    tool: ToolSpec | None
    validation: ToolValidationResult
    policy: PolicyDecision | None
    allowed_to_execute: bool
    error: str | None
    validation_phase: str | None = None


class ToolExecutionPolicyService:
    """Authorize validated registered operation calls for execution.

    Registered operation validation and policy authorization are intentionally
    separate steps: validation proves the selected operation contract accepts the
    call, while policy decides whether that valid call may execute now. This
    service still returns the historical combined result for compatibility.

    This service intentionally does not execute tools, append events, create
    pending actions, or collapse non-allow policy outcomes.  Callers remain
    responsible for routing the returned validation and policy result according
    to their existing behavior.
    """

    def __init__(
        self,
        registry: ToolRegistry,
        validation_service: ToolValidationService | None = None,
        policy_engine: PolicyEngine | None = None,
    ) -> None:
        self.registry = registry
        self.validation_service = validation_service or ToolValidationService(registry)
        self.policy_engine = policy_engine or PolicyGate()

    def evaluate(
        self,
        *,
        tool_name: str,
        arguments: dict[str, Any],
        state: State,
        scope: str | None = None,
    ) -> ToolExecutionPolicyResult:
        """Validate a selected registered operation, then authorize it."""

        return self._evaluate(
            tool_name=tool_name,
            arguments=arguments,
            state_provider=lambda: state,
            scope=scope,
        )

    def evaluate_with_state_factory(
        self,
        *,
        tool_name: str,
        arguments: dict[str, Any],
        state_factory: Callable[[], State],
        scope: str | None = None,
    ) -> ToolExecutionPolicyResult:
        """Authorize with state projected lazily after validation succeeds."""

        return self._evaluate(
            tool_name=tool_name,
            arguments=arguments,
            state_provider=state_factory,
            scope=scope,
        )

    def _evaluate(
        self,
        *,
        tool_name: str,
        arguments: dict[str, Any],
        state_provider: Callable[[], State],
        scope: str | None,
    ) -> ToolExecutionPolicyResult:
        registered_operation = self._validate_registered_operation_call(
            tool_name, arguments
        )
        if not registered_operation.ok:
            return self._validation_failure(registered_operation)

        return self._authorize_validated_operation(
            registered_operation,
            state_provider=state_provider,
            scope=scope,
        )

    def _validate_registered_operation_call(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> RegisteredOperationValidationResult:
        """Validate the selected registered operation before policy.

        This is the validation boundary: existence, registered status, and input
        schema are checked here; no policy state is projected and no policy
        decision is produced.
        """

        existence = self.validation_service.validate_tool_exists(tool_name)
        if not existence.ok or existence.tool is None:
            return RegisteredOperationValidationResult(
                tool=existence.tool,
                validation=existence,
                validation_phase="existence",
            )
        tool = existence.tool

        status = self.validation_service.validate_tool_status(tool)
        if not status.ok:
            return RegisteredOperationValidationResult(
                tool=status.tool,
                validation=status,
                validation_phase="status",
            )

        input_validation = self.validation_service.validate_input_schema(
            tool, arguments
        )
        if not input_validation.ok:
            return RegisteredOperationValidationResult(
                tool=input_validation.tool,
                validation=input_validation,
                validation_phase="input",
            )

        return RegisteredOperationValidationResult(
            tool=tool,
            validation=input_validation,
            validation_phase=None,
        )

    def _authorize_validated_operation(
        self,
        registered_operation: RegisteredOperationValidationResult,
        *,
        state_provider: Callable[[], State],
        scope: str | None,
    ) -> ToolExecutionPolicyResult:
        """Evaluate policy for a validated registered operation call."""

        if not registered_operation.ok or registered_operation.tool is None:
            raise ValueError(
                "policy authorization requires a validated registered operation"
            )

        policy = self.policy_engine.evaluate(
            registered_operation.tool, state_provider(), scope=scope
        )
        return ToolExecutionPolicyResult(
            tool=registered_operation.tool,
            validation=registered_operation.validation,
            policy=policy,
            allowed_to_execute=policy.outcome == "allow",
            error=None,
            validation_phase=None,
        )

    def _validation_failure(
        self, validation: RegisteredOperationValidationResult
    ) -> ToolExecutionPolicyResult:
        return ToolExecutionPolicyResult(
            tool=validation.tool,
            validation=validation.validation,
            policy=None,
            allowed_to_execute=False,
            error=validation.error,
            validation_phase=validation.validation_phase,
        )
