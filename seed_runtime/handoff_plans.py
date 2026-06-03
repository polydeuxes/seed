"""Non-executable handoff plan generation for accepted action plans."""

from __future__ import annotations

from seed_runtime.capability_catalog import CapabilityCatalog, CapabilityRecommendation
from seed_runtime.events import EventLedger
from seed_runtime.models import ActionPlan, HandoffBackendType, HandoffPlan
from seed_runtime.serialization import to_plain
from seed_runtime.state import State
from seed_runtime.tool_needs import slugify


class HandoffPlanNotFoundError(ValueError):
    """Raised when a requested handoff source action plan is missing."""


class HandoffPlanStatusError(ValueError):
    """Raised when an action plan is not eligible for handoff."""


class HandoffPlanService:
    """Create non-executable provider handoffs from accepted action plans.

    Handoff planning is a boundary description only: it does not execute the
    provider, approve the action plan, authorize execution, register tools, ask
    for credentials, or manage provider jobs.
    """

    def __init__(
        self,
        ledger: EventLedger | None = None,
        capability_catalog: CapabilityCatalog | None = None,
    ) -> None:
        self.ledger = ledger
        self.capability_catalog = capability_catalog or CapabilityCatalog.load()

    def create_handoff_plan(
        self,
        state: State,
        action_plan_id: str,
        *,
        session_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> HandoffPlan:
        """Create a non-executable handoff for an accepted stored action plan."""

        action_plan = state.action_plans.get(action_plan_id)
        if action_plan is None:
            raise HandoffPlanNotFoundError(
                f"action plan not found in workspace {state.workspace_id!r}: "
                f"{action_plan_id}"
            )
        if action_plan.status != "accepted":
            raise HandoffPlanStatusError(
                "only accepted action plans can produce handoff plans "
                f"({action_plan_id} is {action_plan.status!r})"
            )

        recommendation = self._catalog_recommendation(action_plan)
        backend_type = _backend_type_from_metadata(recommendation)
        handoff_plan = HandoffPlan(
            action_plan_id=action_plan.id,
            provider=action_plan.provider,
            backend_type=backend_type,
            operation=_operation_for(action_plan, recommendation),
            target=_target_for(action_plan, state),
            policy_summary=_policy_summary(action_plan),
            secret_boundary=_secret_boundary(action_plan.provider, backend_type),
            requires_external_approval=action_plan.requires_approval,
            executable=False,
        )

        if self.ledger is not None:
            self.ledger.append(
                "handoff_plan.created",
                state.workspace_id,
                {"handoff_plan": to_plain(handoff_plan)},
                actor="system",
                session_id=session_id,
                causation_id=causation_id or action_plan.id,
                correlation_id=correlation_id,
            )
        return handoff_plan

    def _catalog_recommendation(
        self, action_plan: ActionPlan
    ) -> CapabilityRecommendation | None:
        entry = self.capability_catalog.get(action_plan.capability)
        if entry is None:
            return None
        provider = slugify(action_plan.provider)
        for recommendation in entry.recommendations:
            if slugify(recommendation.provider) == provider:
                return recommendation
        return None


def _backend_type_from_metadata(
    recommendation: CapabilityRecommendation | None,
) -> HandoffBackendType:
    if recommendation is not None and recommendation.backend_type is not None:
        return recommendation.backend_type
    return "manual"


def _operation_for(
    action_plan: ActionPlan, recommendation: CapabilityRecommendation | None
) -> str:
    if recommendation is not None and recommendation.operation:
        return recommendation.operation
    return action_plan.capability


def _target_for(action_plan: ActionPlan, state: State) -> str:
    target_parts: list[str] = []
    for fact in state.facts.values():
        predicate = fact.predicate.strip().lower().replace("_", ".")
        value = fact.value
        if predicate in {"host", "service.host", "target.host"} and isinstance(
            value, str
        ):
            target_parts.append(f"host:{value.strip()}")
        elif predicate in {
            "container",
            "service.container",
            "container.name",
        } and isinstance(value, str):
            target_parts.append(f"container:{value.strip()}")
        elif predicate in {"service", "service.name"} and isinstance(value, str):
            target_parts.append(f"service:{value.strip()}")
    if target_parts:
        return " ".join(dict.fromkeys(part for part in target_parts if part))

    need = state.tool_needs.get(action_plan.tool_need_id)
    if need is not None:
        return f"tool_need:{need.id}"
    return f"action_plan:{action_plan.id}"


def _policy_summary(action_plan: ActionPlan) -> str:
    approval = (
        "external approval required"
        if action_plan.requires_approval
        else "no Seed approval granted"
    )
    return (
        f"risk_class={action_plan.risk_class}; {approval}; "
        "handoff is non-executable and does not authorize execution"
    )


def _secret_boundary(provider: str, backend_type: HandoffBackendType) -> str:
    return (
        f"Seed passes only this non-secret plan boundary; {provider} via "
        f"{backend_type} owns credentials, approvals, execution, retries, and job state."
    )
