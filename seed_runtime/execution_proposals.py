"""Experimental concrete-call proposal generation; not on the core path."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from seed_runtime.base import SeedModel
from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.models import ActionPlan, RiskClass
from seed_runtime.preconditions import PreconditionReport, evaluate_preconditions
from seed_runtime.secrets import reject_secret_fields
from seed_runtime.serialization import to_plain
from seed_runtime.state import State


class ExecutionProposal(SeedModel):
    """Experimental concrete-call shape that is not executable by itself.

    ExecutionProposal is not part of Seed's core path yet. Prefer HandoffPlan for
    external-provider handoff, and do not use this model to add internal
    execution lifecycle, credentials, retries, scheduling, or long-running jobs.
    """

    def __init__(self, **data: Any) -> None:
        reject_secret_fields(data, "execution_proposal")
        super().__init__(**data)

    id: str
    action_plan_id: str
    provider: str
    tool_name: str
    tool_arguments: dict[str, Any]
    arguments_fingerprint: str
    risk_class: RiskClass
    authorized: bool = False
    executable: bool = False


class ExecutionProposalFailure(SeedModel):
    """Diagnostic for why a concrete execution proposal cannot be built."""

    action_plan_id: str
    missing_reason: str
    detail: str | None = None


class ExecutionProposalService:
    """Experimental helper for concrete-call proposals, outside the core path."""

    def __init__(self, ledger: EventLedger | None = None) -> None:
        self.ledger = ledger

    def create_proposal(
        self,
        action_plan: ActionPlan,
        state: State,
        *,
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> ExecutionProposal | None:
        """Create a concrete proposal only when preconditions are executable.

        The method only reads the supplied state and optionally appends an
        ``execution_proposal.created`` event. It never invokes tools, grants
        approvals or execution authorizations, or registers tools.
        """
        report = evaluate_preconditions(action_plan, state)
        if not report.plan_ready:
            return None

        tool_call = self._tool_call_for_plan(action_plan, state)
        if tool_call is None:
            return None
        tool_name, tool_arguments = tool_call
        reject_secret_fields(tool_arguments, "tool_arguments")

        proposal = ExecutionProposal(
            id=new_id("eprop"),
            action_plan_id=action_plan.id,
            provider=action_plan.provider,
            tool_name=tool_name,
            tool_arguments=tool_arguments,
            arguments_fingerprint=fingerprint_tool_call(tool_name, tool_arguments),
            risk_class=action_plan.risk_class,
            authorized=False,
            executable=False,
        )

        if self.ledger is not None:
            self.ledger.append(
                "execution_proposal.created",
                state.workspace_id,
                {"execution_proposal": to_plain(proposal)},
                actor="system",
                session_id=session_id,
                causation_id=causation_id,
                correlation_id=correlation_id,
            )
        return proposal

    def diagnose_failure(
        self, action_plan: ActionPlan, state: State
    ) -> ExecutionProposalFailure | None:
        """Return a stable, CLI-friendly reason proposal generation would fail."""
        report = evaluate_preconditions(action_plan, state)
        if not report.plan_ready:
            return ExecutionProposalFailure(
                action_plan_id=action_plan.id,
                missing_reason=_precondition_failure_reason(report),
                detail=_precondition_failure_detail(report),
            )

        tool_call_failure = _tool_call_failure_reason(action_plan, state)
        if tool_call_failure is not None:
            reason, detail = tool_call_failure
            return ExecutionProposalFailure(
                action_plan_id=action_plan.id, missing_reason=reason, detail=detail
            )
        return None

    def _tool_call_for_plan(
        self, action_plan: ActionPlan, state: State
    ) -> tuple[str, dict[str, Any]] | None:
        if (
            action_plan.capability != "service_management"
            or action_plan.provider != "docker_container_lifecycle"
        ):
            return None

        host = _find_fact_value(state, _SERVICE_HOST_PREDICATES)
        container = _find_fact_value(state, _SERVICE_CONTAINER_PREDICATES)
        if host is None or container is None:
            return None

        return (
            "docker_container_lifecycle",
            {"host": host, "container": container, "action": "restart"},
        )


def _precondition_failure_reason(report: PreconditionReport) -> str:
    missing_ids = {precondition.id for precondition in report.missing_preconditions}
    if "provider_registered" in missing_ids:
        return "provider/tool not registered"
    return "preconditions missing"


def _precondition_failure_detail(report: PreconditionReport) -> str | None:
    if not report.missing_preconditions:
        return None
    return ", ".join(
        f"{precondition.id}: {precondition.reason}"
        for precondition in report.missing_preconditions
    )


def _tool_call_failure_reason(
    action_plan: ActionPlan, state: State
) -> tuple[str, str | None] | None:
    if (
        action_plan.capability != "service_management"
        or action_plan.provider != "docker_container_lifecycle"
    ):
        detail = (
            "no proposal builder is available for "
            f"{action_plan.capability}/{action_plan.provider}"
        )
        return "provider unsupported", detail

    host = _find_fact_value(state, _SERVICE_HOST_PREDICATES)
    if host is None:
        return (
            "service host missing",
            "no service host fact is present for the action plan",
        )

    container = _find_fact_value(state, _SERVICE_CONTAINER_PREDICATES)
    if container is None:
        return (
            "container name missing",
            "no service container name fact is present for the action plan",
        )

    return None


_SERVICE_HOST_PREDICATES = {
    "service.host",
    "service_host",
    "service.host.name",
    "service_host_name",
    "target_host",
    "host",
}


_SERVICE_CONTAINER_PREDICATES = {
    "service.container",
    "service_container",
    "service.container.name",
    "service_container_name",
    "container",
    "container.name",
    "container_name",
    "service.name",
    "service_name",
    "service",
}


def fingerprint_tool_call(tool_name: str, arguments: dict[str, Any]) -> str:
    """Return a deterministic fingerprint for a proposed concrete tool call."""
    payload = {"tool_name": tool_name, "arguments": arguments}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _find_fact_value(state: State, predicates: set[str]) -> str | None:
    normalized_predicates = {_normalize_predicate(predicate) for predicate in predicates}
    for fact in state.facts.values():
        if _normalize_predicate(fact.predicate) not in normalized_predicates:
            continue
        value = _secret_free_fact_value(fact.value, fact.predicate)
        if value is not None:
            return value
    return None


def _secret_free_fact_value(value: Any, predicate: str) -> str | None:
    reject_secret_fields(value, f"fact.{predicate}.value")
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, dict):
        for key in ("name", "value", "host", "container"):
            nested = value.get(key)
            if isinstance(nested, str) and nested.strip():
                return nested.strip()
    return None


def _normalize_predicate(predicate: str) -> str:
    normalized = predicate.strip().lower()
    for separator in ("-", "/", " "):
        normalized = normalized.replace(separator, "_")
    return normalized
