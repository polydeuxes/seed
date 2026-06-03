import pytest

from seed_runtime.models import HandoffPlan


def test_handoff_plan_is_non_executable():
    plan = HandoffPlan(
        action_plan_id="plan_1",
        provider="awx-prod",
        backend_type="ansible",
        operation="ssh.install",
        target="host:node-1",
        policy_summary="Requires operator approval in AWX.",
        secret_boundary="AWX/Vault/ssh-agent own credentials and job lifecycle.",
        requires_external_approval=True,
        executable=False,
    )

    assert plan.action_plan_id == "plan_1"
    assert plan.backend_type == "ansible"
    assert plan.requires_external_approval is True
    assert plan.executable is False


def test_handoff_plan_rejects_executable_true():
    with pytest.raises(ValueError, match="executable must be false"):
        HandoffPlan(
            action_plan_id="plan_1",
            provider="awx-prod",
            backend_type="ansible",
            operation="ssh.install",
            target="host:node-1",
            policy_summary="Requires operator approval in AWX.",
            secret_boundary="AWX/Vault/ssh-agent own credentials and job lifecycle.",
            executable=True,
        )


def test_handoff_plan_rejects_secret_fields():
    with pytest.raises(ValueError, match="secret field"):
        HandoffPlan(
            action_plan_id="plan_1",
            provider="awx-prod",
            backend_type="ansible",
            operation="ssh.install",
            target="host:node-1",
            policy_summary="Requires operator approval in AWX.",
            secret_boundary="AWX/Vault/ssh-agent own credentials and job lifecycle.",
            token="raw",
            executable=False,
        )


def test_handoff_plan_does_not_imply_approval_or_provider_trust():
    blocked_claims = [
        {"approved": True},
        {"user_approval": "appr_1"},
        {"execution_authorization_id": "auth_1"},
        {"credentials_available": True},
        {"provider_trusted": True},
        {"tool_registered": True},
    ]

    for claim in blocked_claims:
        with pytest.raises(
            ValueError,
            match=(
                "may not imply approval, execution authorization, "
                "credential availability, provider trust, or tool registration"
            ),
        ):
            HandoffPlan(
                action_plan_id="plan_1",
                provider="awx-prod",
                backend_type="ansible",
                operation="ssh.install",
                target="host:node-1",
                policy_summary="Requires operator approval in AWX.",
                secret_boundary="AWX/Vault/ssh-agent own credentials and job lifecycle.",
                executable=False,
                **claim,
            )
