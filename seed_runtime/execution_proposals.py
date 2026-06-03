"""Concrete, non-executing execution proposal generation."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from seed_runtime.base import SeedModel
from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.models import ActionPlan, RiskClass
from seed_runtime.preconditions import evaluate_preconditions
from seed_runtime.secrets import reject_secret_fields
from seed_runtime.serialization import to_plain
from seed_runtime.state import State


class ExecutionProposal(SeedModel):
    """A proposed concrete tool call that is not executable by itself.

    Execution proposals intentionally stop at the boundary of concrete call
    construction. They do not execute tools, approve tool calls, grant execution
    authorization, or register providers.
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


class ExecutionProposalService:
    """Create concrete tool-call proposals from executable action plans."""

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

    def _tool_call_for_plan(
        self, action_plan: ActionPlan, state: State
    ) -> tuple[str, dict[str, Any]] | None:
        if (
            action_plan.capability != "service_management"
            or action_plan.provider != "docker_container_lifecycle"
        ):
            return None

        host = _find_fact_value(
            state,
            {
                "service.host",
                "service_host",
                "service.host.name",
                "service_host_name",
                "target_host",
                "host",
            },
        )
        container = _find_fact_value(
            state,
            {
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
            },
        )
        if host is None or container is None:
            return None

        return (
            "docker_container_lifecycle",
            {"host": host, "container": container, "action": "restart"},
        )


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
