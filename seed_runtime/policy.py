"""Deterministic policy gate for proposed runtime actions."""

from __future__ import annotations

from seed_runtime.models import PolicyDecision, RiskClass, ToolSpec
from seed_runtime.state import State


class PolicyGate:
    """Map risk and approvals into auditable allow/block decisions."""

    def __init__(self, action_risks: dict[str, RiskClass] | None = None) -> None:
        self.action_risks = action_risks or {}

    def evaluate(self, tool: ToolSpec, state: State, *, scope: str | None = None) -> PolicyDecision:
        risk = self.action_risks.get(tool.policy_action, tool.risk_class)
        if risk == "L1":
            return PolicyDecision("allow", tool.policy_action, "low-risk read-only action", risk)
        if risk == "L2":
            return PolicyDecision("require_confirmation", tool.policy_action, "action requires user confirmation", risk)
        if risk == "L3":
            approval = state.has_approval(tool.policy_action, scope)
            if approval:
                return PolicyDecision("allow", tool.policy_action, "matching approval found", risk, approval.id)
            return PolicyDecision("require_approval", tool.policy_action, "high-risk action requires approval", risk)
        return PolicyDecision("block", tool.policy_action, "critical action is blocked by default", risk)
