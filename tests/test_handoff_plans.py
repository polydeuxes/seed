import pytest

from seed_runtime.action_plans import ActionPlanService
from seed_runtime.capability_catalog import (
    CapabilityCatalog,
    CapabilityCatalogEntry,
    CapabilityRecommendation,
)
from seed_runtime.events import EventLedger
from seed_runtime.handoff_plans import HandoffPlanService, HandoffPlanStatusError
from seed_runtime.models import HandoffPlan, ToolNeed
from seed_runtime.recommendation_ranker import RankedRecommendation
from seed_runtime.state import State, StateProjector


def test_handoff_plan_is_non_executable():
    plan = HandoffPlan(
        action_plan_id="plan_1",
        provider="awx-prod",
        backend_type="ansible",
        operation="ssh.install",
        target="host:example_host",
        policy_summary="Requires operator approval in AWX.",
        secret_boundary="AWX/Vault/ssh-agent own credentials and job lifecycle.",
        requires_external_approval=True,
        executable=False,
    )

    assert plan.id.startswith("handoff_")
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
            target="host:example_host",
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
            target="host:example_host",
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
                target="host:example_host",
                policy_summary="Requires operator approval in AWX.",
                secret_boundary="AWX/Vault/ssh-agent own credentials and job lifecycle.",
                executable=False,
                **claim,
            )


def test_handoff_service_creates_plan_from_accepted_action_plan_and_catalog_metadata():
    ledger = EventLedger()
    action_service = ActionPlanService(ledger)
    need = ToolNeed(
        id="need_service",
        workspace_id="ws",
        name="restart_web_service",
        capability="service_management",
        summary="Restart web_service",
        reason="User asked",
    )
    recommendation = RankedRecommendation(
        provider="docker_container_lifecycle",
        summary="Use Docker lifecycle operations.",
        kind="local_cli",
        source="docker",
        risk_class="L3",
        notes="Requires approval.",
        score=100,
        reasons=[],
        reasoning=[],
    )
    plan = action_service.create_plan(need, recommendation, State(workspace_id="ws"))
    action_service.accept_plan("ws", plan.id)
    state = StateProjector(ledger).project("ws")
    catalog = CapabilityCatalog(
        [
            CapabilityCatalogEntry(
                capability="service_management",
                summary="Manage services.",
                recommendations=[
                    CapabilityRecommendation(
                        provider="docker_container_lifecycle",
                        summary="Use Docker lifecycle operations.",
                        kind="local_cli",
                        risk_class="L3",
                        backend_type="ansible",
                        operation="service.restart",
                    )
                ],
            )
        ]
    )

    handoff = HandoffPlanService(ledger, catalog).create_handoff_plan(state, plan.id)

    assert handoff.action_plan_id == plan.id
    assert handoff.provider == "docker_container_lifecycle"
    assert handoff.backend_type == "ansible"
    assert handoff.operation == "service.restart"
    assert handoff.requires_external_approval is True
    assert handoff.executable is False
    assert "risk_class=L3" in handoff.policy_summary
    assert "Seed passes only this non-secret plan boundary" in handoff.secret_boundary
    kinds = [event.kind for event in ledger.list_events("ws")]
    assert kinds == [
        "action_plan.created",
        "action_plan.accepted",
        "handoff_plan.created",
    ]
    projected = StateProjector(ledger).project("ws")
    event = ledger.list_events("ws")[-1]
    assert event.kind == "handoff_plan.created"
    assert event.payload["handoff_plan"]["id"] == handoff.id
    assert projected.handoff_plans[handoff.id] == handoff
    assert handoff.action_plan_id not in projected.handoff_plans
    assert "approval.granted" not in kinds
    assert "execution_authorization.granted" not in kinds
    assert projected.approvals == {}
    assert not hasattr(projected, "execution_authorizations")
    assert not hasattr(projected, "execution_proposals")
    assert projected.pending_actions == {}
    assert projected.tools == {}


def test_handoff_service_requires_accepted_action_plan():
    ledger = EventLedger()
    plan = ActionPlanService(ledger).create_plan(
        ToolNeed(
            id="need_weather",
            workspace_id="ws",
            name="weather",
            capability="weather_lookup",
            summary="Weather lookup",
            reason="User asked",
        ),
        RankedRecommendation(
            provider="open_meteo",
            summary="Weather API.",
            kind="public_api",
            source="https://open-meteo.com/",
            risk_class="L1",
            notes=None,
            score=1,
            reasons=[],
            reasoning=[],
        ),
        State(workspace_id="ws"),
    )
    state = StateProjector(ledger).project("ws")

    with pytest.raises(HandoffPlanStatusError, match="only accepted action plans"):
        HandoffPlanService(ledger).create_handoff_plan(state, plan.id)

    assert [event.kind for event in ledger.list_events("ws")] == ["action_plan.created"]
