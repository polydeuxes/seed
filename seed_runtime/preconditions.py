"""Execution precondition reporting for action plans.

This module is intentionally inspect-only: it derives whether a future
execution path would have the declared prerequisites, without invoking tools,
registering providers, or granting approvals.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone

from seed_runtime.base import SeedModel
from seed_runtime.models import ActionPlan
from seed_runtime.state import State


class Precondition(SeedModel):
    """A single prerequisite required before an action plan can execute."""

    id: str
    name: str
    satisfied: bool
    reason: str


class PreconditionReport(SeedModel):
    """Inspect-only execution readiness report for an action plan."""

    action_plan_id: str
    executable: bool
    missing_preconditions: list[Precondition]


CheckFn = Callable[[ActionPlan, State], tuple[bool, str]]


_PRECONDITION_NAMES: dict[str, str] = {
    "target_host_known": "Target host known",
    "provider_registered": "Provider registered",
    "approval_present": "Approval present",
}


_CAPABILITY_PRECONDITIONS: dict[str, tuple[str, ...]] = {
    "service_management": (
        "target_host_known",
        "provider_registered",
        "approval_present",
    ),
    "weather_lookup": ("provider_registered",),
    "installation": ("target_host_known", "approval_present"),
}


class PreconditionEvaluator:
    """Evaluate declared action-plan preconditions against projected state."""

    def report(self, action_plan: ActionPlan, state: State) -> PreconditionReport:
        """Return missing preconditions and executability for an action plan.

        Unknown capabilities currently have no declared preconditions and are
        therefore reported as executable from the precondition framework's point
        of view. This does not execute anything and does not change state.
        """
        preconditions = [
            self._evaluate(precondition_id, action_plan, state)
            for precondition_id in _CAPABILITY_PRECONDITIONS.get(
                action_plan.capability, ()
            )
        ]
        missing = [
            precondition
            for precondition in preconditions
            if not precondition.satisfied
        ]
        return PreconditionReport(
            action_plan_id=action_plan.id,
            executable=not missing,
            missing_preconditions=missing,
        )

    def _evaluate(
        self, precondition_id: str, action_plan: ActionPlan, state: State
    ) -> Precondition:
        check = _CHECKS.get(precondition_id)
        if check is None:
            satisfied = False
            reason = "precondition is declared but has no evaluator"
        else:
            satisfied, reason = check(action_plan, state)
        return Precondition(
            id=precondition_id,
            name=_PRECONDITION_NAMES.get(precondition_id, precondition_id),
            satisfied=satisfied,
            reason=reason,
        )


def declared_preconditions(capability: str) -> tuple[str, ...]:
    """Return the precondition IDs declared for a capability."""
    return _CAPABILITY_PRECONDITIONS.get(capability, ())


def evaluate_preconditions(
    action_plan: ActionPlan, state: State
) -> PreconditionReport:
    """Convenience wrapper for evaluating action-plan preconditions."""
    return PreconditionEvaluator().report(action_plan, state)


def _target_host_known(_action_plan: ActionPlan, state: State) -> tuple[bool, str]:
    for entity in state.entities.values():
        if entity.kind == "host":
            return True, f"host entity is known: {entity.id}"

    for fact in state.facts.values():
        if fact.predicate in {"target_host", "target_host_known"} and bool(fact.value):
            return True, f"target host fact is present: {fact.id}"

    return False, "no host entity or target host fact is present"


def _provider_registered(action_plan: ActionPlan, state: State) -> tuple[bool, str]:
    provider = action_plan.provider
    capability = action_plan.capability
    for tool in state.tools.values():
        if tool.status != "registered":
            continue
        if tool.name in {provider, capability}:
            return True, f"registered tool is available: {tool.name}"
        if tool.toolkit_id == provider:
            return True, f"registered provider toolkit is available: {tool.toolkit_id}"

    return False, f"provider is not registered: {provider}"


def _approval_present(action_plan: ActionPlan, state: State) -> tuple[bool, str]:
    now = datetime.now(timezone.utc)
    for approval in state.approvals.values():
        if approval.expires_at is not None and approval.expires_at < now:
            continue
        if approval.action in {
            action_plan.capability,
            action_plan.provider,
            f"{action_plan.capability}.{action_plan.provider}",
        }:
            return True, f"matching approval is present: {approval.id}"
        return True, f"approval is present: {approval.id}"

    return False, "no current approval is present"


_CHECKS: dict[str, CheckFn] = {
    "target_host_known": _target_host_known,
    "provider_registered": _provider_registered,
    "approval_present": _approval_present,
}
