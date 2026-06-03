"""Text-only action plan generation for ranked provider recommendations."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable, cast

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.models import (
    ActionPlan,
    ActionPlanStatus,
    Actor,
    ExecutionAuthorization,
    RiskClass,
    ToolNeed,
)
from seed_runtime.preconditions import PreconditionReport, evaluate_preconditions
from seed_runtime.recommendation_ranker import RankedRecommendation
from seed_runtime.state import State, StateProjector
from seed_runtime.tool_needs import slugify

_MUTATING_RISK_CLASSES: set[str] = {"L3", "L4"}
_MAX_EXECUTION_AUTHORIZATION_TTL_SECONDS = 900


class ActionPlanNotFoundError(ValueError):
    """Raised when a lifecycle event targets a missing action plan."""


class ActionPlanTransitionError(ValueError):
    """Raised when an action plan lifecycle transition is not allowed."""


_ALLOWED_TRANSITIONS: dict[ActionPlanStatus, set[ActionPlanStatus]] = {
    "proposed": {"accepted", "rejected", "superseded"},
    "accepted": {"superseded"},
    "rejected": set(),
    "superseded": set(),
}


class ActionPlanService:
    """Create and lifecycle-manage safe proposed next actions."""

    def __init__(self, ledger: EventLedger | None = None) -> None:
        self.ledger = ledger

    def create_plan(
        self,
        tool_need: ToolNeed,
        ranked_recommendation: RankedRecommendation,
        state: State | None,
        *,
        session_id: str | None = None,
        causation_id: str | None = None,
    ) -> ActionPlan:
        """Return a text-only, non-executable plan for the chosen provider.

        The supplied state is accepted for future state-aware planning, but this
        implementation is intentionally read-only and never executes, installs,
        or registers anything.
        """
        del state  # Explicitly read-only and currently unused.

        capability = slugify(tool_need.capability)
        provider = slugify(ranked_recommendation.provider)
        risk_class = _normalize_risk_class(
            ranked_recommendation.risk_class or tool_need.risk_hint
        )
        requires_approval = risk_class in _MUTATING_RISK_CLASSES

        plan = ActionPlan(
            id=new_id("plan"),
            tool_need_id=tool_need.id,
            provider=provider,
            capability=capability,
            summary=_plan_summary(tool_need, ranked_recommendation),
            steps=_plan_steps(capability, provider, requires_approval),
            risk_class=risk_class,
            requires_approval=requires_approval,
            executable=False,
        )
        if self.ledger is not None:
            from seed_runtime.serialization import to_plain

            self.ledger.append(
                "action_plan.created",
                tool_need.workspace_id,
                {"action_plan": to_plain(plan)},
                actor="system",
                session_id=session_id,
                causation_id=causation_id,
            )
        return plan

    def precondition_report(
        self, action_plan: ActionPlan, state: State
    ) -> PreconditionReport:
        """Generate an inspect-only execution precondition report.

        Reporting never executes the action plan, invokes tools, registers
        providers, or grants approvals. It only reads the supplied projected
        state and the action plan's declared capability.
        """
        return evaluate_preconditions(action_plan, state)

    def accept_plan(
        self,
        workspace_id: str,
        action_plan_id: str,
        *,
        actor: Actor = "user",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> ActionPlan:
        """Record that a proposed action plan was accepted.

        Acceptance only changes lifecycle state; it does not execute the plan,
        approve tool calls, or register tools.
        """
        plan = self._transition_plan(workspace_id, action_plan_id, "accepted")
        self._require_ledger().append(
            "action_plan.accepted",
            workspace_id,
            {"action_plan_id": action_plan_id, "status": "accepted"},
            actor=actor,
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        return plan.model_copy(
            update={
                "status": "accepted",
                "rejection_reason": None,
                "replacement_plan_id": None,
            }
        )

    def approve_plan(
        self,
        workspace_id: str,
        action_plan_id: str,
        *,
        actor: Actor = "approver",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> ActionPlan:
        """Record approval for an accepted action plan without executing it.

        Plan approval is not execution authorization: it does not change
        lifecycle status, execute the plan, approve pending tool calls, grant
        credentials, or register tools.
        """
        plan = self._require_plan(workspace_id, action_plan_id)
        if plan.status != "accepted":
            raise ActionPlanTransitionError(
                "only accepted action plans can be approved "
                f"({action_plan_id} is {plan.status!r})"
            )
        self._require_ledger().append(
            "action_plan.approved",
            workspace_id,
            {"action_plan_id": action_plan_id},
            actor=actor,
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        return plan

    def grant_execution_authorization(
        self,
        workspace_id: str,
        execution_proposal_id: str,
        *,
        granted_by: str,
        interactive_prompt: bool = False,
        ssh_agent: str | None = None,
        sudo_timestamp: str | None = None,
        external_vault_token_ref: str | None = None,
        session_id: str | None = None,
        ttl_seconds: int = 300,
        actor: Actor = "approver",
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> ExecutionAuthorization:
        """Record a short-lived authorization for one concrete proposal.

        This does not execute anything and does not persist credentials. The
        stored event binds an accepted action plan to an existing execution
        proposal by ID and copies only the proposal's secret-free tool name and
        argument fingerprint. Raw tool arguments are never accepted by this
        authorization path or stored in the authorization event.
        """
        state = StateProjector(self._require_ledger()).project(workspace_id)
        proposal = state.execution_proposals.get(execution_proposal_id)
        if proposal is None:
            raise ValueError(
                f"execution proposal not found in workspace {workspace_id!r}: "
                f"{execution_proposal_id}"
            )
        plan = self._require_plan(workspace_id, proposal.action_plan_id)
        if plan.status != "accepted":
            raise ActionPlanTransitionError(
                "only accepted action plans can receive execution authorization "
                f"({plan.id} is {plan.status!r})"
            )
        if ttl_seconds <= 0:
            raise ValueError("execution authorization ttl_seconds must be positive")
        if ttl_seconds > _MAX_EXECUTION_AUTHORIZATION_TTL_SECONDS:
            raise ValueError(
                "execution authorization ttl_seconds must be <= "
                f"{_MAX_EXECUTION_AUTHORIZATION_TTL_SECONDS}"
            )

        authorization = ExecutionAuthorization(
            id=new_id("auth"),
            execution_proposal_id=proposal.id,
            action_plan_id=proposal.action_plan_id,
            tool_name=proposal.tool_name,
            arguments_fingerprint=proposal.arguments_fingerprint,
            granted_by=granted_by,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds),
            interactive_prompt=interactive_prompt,
            ssh_agent=ssh_agent,
            sudo_timestamp=sudo_timestamp,
            external_vault_token_ref=external_vault_token_ref,
            secret_seen_by_seed=False,
        )
        from seed_runtime.serialization import to_plain

        self._require_ledger().append(
            "execution_authorization.granted",
            workspace_id,
            {"execution_authorization": to_plain(authorization)},
            actor=actor,
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        return authorization

    def reject_plan(
        self,
        workspace_id: str,
        action_plan_id: str,
        reason: str,
        *,
        actor: Actor = "user",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> ActionPlan:
        """Record that an action plan was rejected with a human-readable reason."""
        plan = self._transition_plan(workspace_id, action_plan_id, "rejected")
        self._require_ledger().append(
            "action_plan.rejected",
            workspace_id,
            {
                "action_plan_id": action_plan_id,
                "status": "rejected",
                "reason": reason,
            },
            actor=actor,
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        return plan.model_copy(
            update={
                "status": "rejected",
                "rejection_reason": reason,
                "replacement_plan_id": None,
            }
        )

    def supersede_plan(
        self,
        workspace_id: str,
        action_plan_id: str,
        replacement_plan_id: str,
        *,
        actor: Actor = "user",
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> ActionPlan:
        """Record that an action plan was replaced by another plan."""
        plan = self._transition_plan(workspace_id, action_plan_id, "superseded")
        self._require_ledger().append(
            "action_plan.superseded",
            workspace_id,
            {
                "action_plan_id": action_plan_id,
                "status": "superseded",
                "replacement_plan_id": replacement_plan_id,
            },
            actor=actor,
            session_id=session_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        return plan.model_copy(
            update={
                "status": "superseded",
                "rejection_reason": None,
                "replacement_plan_id": replacement_plan_id,
            }
        )

    def _require_ledger(self) -> EventLedger:
        if self.ledger is None:
            raise RuntimeError("ActionPlanService lifecycle methods require a ledger")
        return self.ledger

    def _require_plan(self, workspace_id: str, action_plan_id: str) -> ActionPlan:
        state = StateProjector(self._require_ledger()).project(workspace_id)
        plan = state.action_plans.get(action_plan_id)
        if plan is None:
            raise ActionPlanNotFoundError(
                f"action plan not found in workspace {workspace_id!r}: {action_plan_id}"
            )
        return plan

    def _transition_plan(
        self,
        workspace_id: str,
        action_plan_id: str,
        target_status: ActionPlanStatus,
    ) -> ActionPlan:
        plan = self._require_plan(workspace_id, action_plan_id)
        if target_status not in _ALLOWED_TRANSITIONS[plan.status]:
            raise ActionPlanTransitionError(
                "invalid action plan transition "
                f"{plan.status!r} -> {target_status!r} for {action_plan_id}"
            )
        return plan



def _normalize_risk_class(value: str | None) -> RiskClass:
    if value in {"L1", "L2", "L3", "L4"}:
        return cast(RiskClass, value)
    return "L1"


def _plan_summary(
    tool_need: ToolNeed, ranked_recommendation: RankedRecommendation
) -> str:
    return (
        f"Propose using {ranked_recommendation.provider} for "
        f"{tool_need.capability}: {ranked_recommendation.summary}"
    )


def _plan_steps(
    capability: str, provider: str, requires_approval: bool
) -> list[str]:
    template = _PLAN_TEMPLATES.get((capability, provider))
    if template is not None:
        return list(template)

    steps = [
        f"Review the requested {capability} capability.",
        f"Confirm {provider} is the intended provider.",
        "Identify required inputs and constraints.",
        "Return the proposed result as Evidence.",
    ]
    if requires_approval:
        steps.append("Request approval before any mutating action.")
    return steps


_PLAN_TEMPLATES: dict[tuple[str, str], Iterable[str]] = {
    ("service_management", "docker_container_lifecycle"): (
        "Identify target host for service.",
        "Confirm container name.",
        "Verify Docker access.",
        "Request approval before restart.",
    ),
    ("weather_lookup", "open_meteo"): (
        "Determine location.",
        "Query Open-Meteo forecast endpoint.",
        "Return result as Evidence.",
    ),
}
