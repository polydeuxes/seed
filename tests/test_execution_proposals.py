from dataclasses import replace
from datetime import timedelta

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.execution_proposals import (
    ExecutionProposal,
    ExecutionProposalService,
    fingerprint_tool_call,
)
from seed_runtime.facts import Fact
from seed_runtime.models import (
    ActionPlan,
    Entity,
    ExecutionAuthorization,
    ToolSpec,
    utc_now,
)
from seed_runtime.serialization import to_plain
from seed_runtime.state import State, StateProjector


def _plan() -> ActionPlan:
    return ActionPlan(
        id="plan_1",
        tool_need_id="need_1",
        provider="docker_container_lifecycle",
        capability="service_management",
        summary="Restart the web container.",
        steps=["Build a proposal only."],
        risk_class="L3",
        requires_approval=True,
        executable=False,
    )


def _tool() -> ToolSpec:
    return ToolSpec(
        name="docker_container_lifecycle",
        summary="Manage Docker containers.",
        toolkit_id="docker_container_lifecycle",
        input_schema={},
        output_schema={},
        policy_action="service_management.docker_container_lifecycle",
        implementation="toolkits.generated.docker.operations:restart",
        risk_class="L3",
    )


def _authorization() -> ExecutionAuthorization:
    return ExecutionAuthorization(
        id="auth_1",
        action_plan_id="plan_1",
        tool_name="docker_container_lifecycle",
        arguments_fingerprint=fingerprint_tool_call(
            "docker_container_lifecycle",
            {"host": "node-1", "container": "web", "action": "restart"},
        ),
        granted_by="operator@example.com",
        expires_at=utc_now() + timedelta(days=1),
        secret_seen_by_seed=False,
    )


def _fact(fact_id: str, predicate: str, value):
    return Fact(
        id=fact_id,
        subject_id="service_1",
        predicate=predicate,
        value=value,
        observed_at=utc_now(),
    )


def _executable_state() -> State:
    ledger = EventLedger()
    workspace_id = "ws"
    ledger.append(
        "entity.upserted",
        workspace_id,
        {"entity": to_plain(Entity(id="ent_1", kind="host", name="node-1"))},
    )
    ledger.append("tool.registered", workspace_id, {"tool": to_plain(_tool())})
    ledger.append(
        "execution_authorization.granted",
        workspace_id,
        {"execution_authorization": to_plain(_authorization())},
    )
    ledger.append(
        "fact.observed",
        workspace_id,
        {"fact": to_plain(_fact("fact_host", "service.host", "node-1"))},
    )
    ledger.append(
        "fact.observed",
        workspace_id,
        {"fact": to_plain(_fact("fact_container", "service.container", "web"))},
    )
    return StateProjector(ledger).project(workspace_id)


def test_no_proposal_if_preconditions_missing():
    ledger = EventLedger()
    proposal = ExecutionProposalService(ledger).create_proposal(
        _plan(), State(workspace_id="ws")
    )

    assert proposal is None
    assert ledger.list_events("ws") == []


def test_docker_service_plan_creates_proposal_from_facts():
    ledger = EventLedger()

    proposal = ExecutionProposalService(ledger).create_proposal(
        _plan(), _executable_state(), session_id="ses_1", causation_id="evt_1"
    )

    assert proposal is not None
    assert proposal.action_plan_id == "plan_1"
    assert proposal.provider == "docker_container_lifecycle"
    assert proposal.tool_name == "docker_container_lifecycle"
    assert proposal.tool_arguments == {
        "host": "node-1",
        "container": "web",
        "action": "restart",
    }
    assert proposal.risk_class == "L3"
    assert proposal.executable is False
    events = ledger.list_events("ws")
    assert [event.kind for event in events] == ["execution_proposal.created"]
    assert events[0].payload["execution_proposal"]["id"] == proposal.id
    assert events[0].session_id == "ses_1"
    assert events[0].causation_id == "evt_1"


def test_proposal_stores_fingerprint():
    proposal = ExecutionProposalService().create_proposal(_plan(), _executable_state())

    assert proposal is not None
    assert proposal.arguments_fingerprint == fingerprint_tool_call(
        "docker_container_lifecycle",
        {"host": "node-1", "container": "web", "action": "restart"},
    )
    assert proposal.arguments_fingerprint.startswith("sha256:")


def test_secrets_rejected():
    with pytest.raises(ValueError, match="secret field"):
        ExecutionProposal(
            id="eprop_secret",
            action_plan_id="plan_1",
            provider="docker_container_lifecycle",
            tool_name="docker_container_lifecycle",
            tool_arguments={"host": "node-1", "container": "web", "token": "raw"},
            arguments_fingerprint="sha256:placeholder",
            risk_class="L3",
            executable=False,
        )

    state = replace(
        _executable_state(),
        facts={
            "fact_host": _fact("fact_host", "service.host", "node-1"),
            "fact_container": _fact(
                "fact_container",
                "service.container",
                {"name": "web", "password": "raw"},
            ),
        },
    )
    with pytest.raises(ValueError, match="secret field"):
        ExecutionProposalService().create_proposal(_plan(), state)


def test_no_tool_execution_occurs():
    ledger = EventLedger()

    ExecutionProposalService(ledger).create_proposal(_plan(), _executable_state())

    kinds = [event.kind for event in ledger.list_events("ws")]
    assert kinds == ["execution_proposal.created"]
    assert "tool.call.started" not in kinds
    assert "tool.call.completed" not in kinds
    assert "pending_action.approved" not in kinds
    assert "approval.granted" not in kinds
    assert "tool.registered" not in kinds
