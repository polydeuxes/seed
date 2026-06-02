"""Text-only action plan generation for ranked provider recommendations."""

from __future__ import annotations

from typing import Iterable, Literal, cast

from seed_runtime.base import SeedModel
from seed_runtime.ids import new_id
from seed_runtime.models import RiskClass, ToolNeed
from seed_runtime.recommendation_ranker import RankedRecommendation
from seed_runtime.state import State
from seed_runtime.tool_needs import slugify

_MUTATING_RISK_CLASSES: set[str] = {"L3", "L4"}


class ActionPlan(SeedModel):
    """A safe, non-executable proposal for satisfying a tool need.

    Action plans deliberately contain only text. They describe a proposed next
    action for the recommended provider, but they do not carry callable code,
    executable arguments, or any authority to mutate state or external systems.
    """

    id: str
    tool_need_id: str
    provider: str
    capability: str
    summary: str
    steps: list[str]
    risk_class: RiskClass
    requires_approval: bool
    executable: Literal[False] = False


class ActionPlanService:
    """Create safe proposed next actions from ranked recommendations."""

    def create_plan(
        self,
        tool_need: ToolNeed,
        ranked_recommendation: RankedRecommendation,
        state: State | None,
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

        return ActionPlan(
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
