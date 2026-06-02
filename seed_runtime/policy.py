"""Deterministic policy gate for proposed runtime actions."""

from __future__ import annotations

from seed_runtime.models import PolicyDecision, RiskClass, ToolSpec
from seed_runtime.state import State


class PolicyGate:
    """Map risk and approvals into auditable allow/block decisions.

    When ``action_risks`` is provided, it acts as the policy's known-action
    table. Actions absent from that table are blocked even if the tool manifest
    declares a low risk class. When no table is provided, the gate trusts the
    tool's declared ``risk_class`` so core/generated manifests can still be
    exercised by the prototype runtime.
    """

    def __init__(self, action_risks: dict[str, RiskClass] | None = None) -> None:
        self.action_risks = action_risks

    def evaluate(
        self, tool: ToolSpec, state: State, *, scope: str | None = None
    ) -> PolicyDecision:
        if (
            self.action_risks is not None
            and tool.policy_action not in self.action_risks
        ):
            return PolicyDecision(
                outcome="block",
                action=tool.policy_action,
                reason="unknown policy action is blocked by default",
                risk_class=tool.risk_class,
            )

        risk = self._risk_for(tool)
        approval = state.has_approval(tool.policy_action, scope)
        if approval:
            return PolicyDecision(
                outcome="allow",
                action=tool.policy_action,
                reason="matching approval found",
                risk_class=risk,
                approval_id=approval.id,
            )

        if risk == "L1":
            return PolicyDecision(
                outcome="allow",
                action=tool.policy_action,
                reason="low-risk read-only action",
                risk_class=risk,
            )
        if risk == "L2":
            return PolicyDecision(
                outcome="require_confirmation",
                action=tool.policy_action,
                reason="action requires user confirmation",
                risk_class=risk,
            )
        if risk == "L3":
            return PolicyDecision(
                outcome="require_approval",
                action=tool.policy_action,
                reason="high-risk action requires approval",
                risk_class=risk,
            )
        return PolicyDecision(
            outcome="block",
            action=tool.policy_action,
            reason="critical action is blocked by default",
            risk_class=risk,
        )

    def _risk_for(self, tool: ToolSpec) -> RiskClass:
        if self.action_risks is None:
            return tool.risk_class
        return self.action_risks[tool.policy_action]
