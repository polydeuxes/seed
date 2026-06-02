"""Text-only action plan generation for ranked provider recommendations."""

from __future__ import annotations

from typing import Iterable, cast

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.models import ActionPlan, RiskClass, ToolNeed
from seed_runtime.recommendation_ranker import RankedRecommendation
from seed_runtime.state import State
from seed_runtime.tool_needs import slugify

_MUTATING_RISK_CLASSES: set[str] = {"L3", "L4"}


class ActionPlanService:
    """Create safe proposed next actions from ranked recommendations."""

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
