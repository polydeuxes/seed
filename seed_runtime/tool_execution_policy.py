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
class ToolExecutionPolicyResult:
    """Result of resolving, validating, and policy-checking a tool call."""

    tool: ToolSpec | None
    validation: ToolValidationResult
    policy: PolicyDecision | None
    allowed_to_execute: bool
    error: str | None
    validation_phase: str | None = None


class ToolExecutionPolicyService:
    """Validate a tool call and preserve the raw policy decision for callers.

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
        """Resolve and validate a tool call, then evaluate policy if valid."""

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
        """Evaluate with state projected lazily after validation succeeds."""

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
        existence = self.validation_service.validate_tool_exists(tool_name)
        if not existence.ok or existence.tool is None:
            return self._validation_failure(existence, phase="existence")
        tool = existence.tool

        status = self.validation_service.validate_tool_status(tool)
        if not status.ok:
            return self._validation_failure(status, phase="status")

        input_validation = self.validation_service.validate_input_schema(
            tool, arguments
        )
        if not input_validation.ok:
            return self._validation_failure(input_validation, phase="input")

        policy = self.policy_engine.evaluate(tool, state_provider(), scope=scope)
        return ToolExecutionPolicyResult(
            tool=tool,
            validation=input_validation,
            policy=policy,
            allowed_to_execute=policy.outcome == "allow",
            error=None,
            validation_phase=None,
        )

    def _validation_failure(
        self, validation: ToolValidationResult, *, phase: str
    ) -> ToolExecutionPolicyResult:
        return ToolExecutionPolicyResult(
            tool=validation.tool,
            validation=validation,
            policy=None,
            allowed_to_execute=False,
            error="; ".join(validation.errors) if validation.errors else None,
            validation_phase=phase,
        )
