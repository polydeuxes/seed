"""Deterministic policy gate for proposed runtime actions."""

from __future__ import annotations

from seed_runtime.models import PolicyDecision, RiskClass, ToolSpec
from seed_runtime.state import State


class PolicyGate:
    """Map risk and approvals into auditable allow/block decisions."""

    def __init__(self, action_risks: dict[str, RiskClass] | None = None) -> None:
        self.action_risks = action_risks or {}

    def evaluate(
        self, tool: ToolSpec, state: State, *, scope: str | None = None
    ) -> PolicyDecision:
        risk = self.action_risks.get(tool.policy_action, tool.risk_class)
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
            approval = state.has_approval(tool.policy_action, scope)
            if approval:
                return PolicyDecision(
                    outcome="allow",
                    action=tool.policy_action,
                    reason="matching approval found",
                    risk_class=risk,
                    approval_id=approval.id,
                )
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
