from datetime import datetime, timedelta, timezone

from seed_runtime.action_plans import ActionPlanService
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.models import ActionPlan, Approval, Entity, ToolSpec
from seed_runtime.serialization import to_plain
from seed_runtime.state import State, StateProjector


def _plan(capability: str = "service_management") -> ActionPlan:
    return ActionPlan(
        id="plan_1",
        tool_need_id="need_1",
        provider="docker_container_lifecycle",
        capability=capability,
        summary="Propose a future action.",
        steps=["Inspect readiness only."],
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


def test_missing_preconditions_are_not_executable():
    report = ActionPlanService().precondition_report(
        _plan(), State(workspace_id="ws")
    )

    assert report.action_plan_id == "plan_1"
    assert report.executable is False
    assert [precondition.id for precondition in report.missing_preconditions] == [
        "target_host_known",
        "provider_registered",
        "execution_authorization_present",
    ]
    assert [precondition.id for precondition in report.preconditions] == [
        "target_host_known",
        "provider_registered",
        "execution_authorization_present",
    ]
    assert [precondition.satisfied for precondition in report.preconditions] == [
        False,
        False,
        False,
    ]


def test_legacy_approval_no_longer_satisfies_mutating_preconditions():
    ledger = EventLedger()
    workspace_id = "ws"
    ledger.append(
        "entity.upserted",
        workspace_id,
        {"entity": to_plain(Entity(id="ent_1", kind="host", name="node-1"))},
    )
    ledger.append("tool.registered", workspace_id, {"tool": to_plain(_tool())})
    ledger.append(
        "approval.granted",
        workspace_id,
        {
            "approval": to_plain(
                Approval(
                    id="appr_1",
                    action="service_management.docker_container_lifecycle",
                    scope="ent_1",
                    approved_by="user",
                )
            )
        },
    )
    state = StateProjector(ledger).project(workspace_id)

    report = ActionPlanService().precondition_report(_plan(), state)

    assert report.executable is False
    assert [precondition.id for precondition in report.missing_preconditions] == [
        "execution_authorization_present",
    ]
    assert [precondition.satisfied for precondition in report.preconditions] == [
        True,
        True,
        False,
    ]
    assert [event.kind for event in ledger.list_events(workspace_id)] == [
        "entity.upserted",
        "tool.registered",
        "approval.granted",
    ]


def test_unknown_capability_is_handled_gracefully():
    report = ActionPlanService().precondition_report(
        _plan(capability="unknown_capability"), State(workspace_id="ws")
    )

    assert report.action_plan_id == "plan_1"
    assert report.executable is True
    assert report.missing_preconditions == []


def test_action_plan_approval_does_not_satisfy_mutating_authorization():
    ledger = EventLedger()
    workspace_id = "ws"
    ledger.append("action_plan.approved", workspace_id, {"action_plan_id": "plan_1"})
    state = StateProjector(ledger).project(workspace_id)

    report = ActionPlanService().precondition_report(_plan(), state)

    approval = next(
        precondition
        for precondition in report.preconditions
        if precondition.id == "execution_authorization_present"
    )
    assert approval.satisfied is False
    assert "no current execution authorization" in approval.reason
    assert report.executable is False
    assert [precondition.id for precondition in report.missing_preconditions] == [
        "target_host_known",
        "provider_registered",
        "execution_authorization_present",
    ]


def test_executable_becomes_true_only_when_all_preconditions_are_true():
    ledger = EventLedger()
    workspace_id = "ws"
    ledger.append(
        "entity.upserted",
        workspace_id,
        {"entity": to_plain(Entity(id="ent_1", kind="host", name="node-1"))},
    )
    plan = _plan().model_copy(update={"status": "accepted"})
    ledger.append(
        "action_plan.created", workspace_id, {"action_plan": to_plain(plan)}
    )
    ActionPlanService(ledger).grant_execution_authorization(
        workspace_id,
        "plan_1",
        tool_name="docker_container_lifecycle",
        tool_arguments={"container": "web", "operation": "restart"},
        granted_by="operator@example.com",
    )
    missing_provider = ActionPlanService().precondition_report(
        _plan(), StateProjector(ledger).project(workspace_id)
    )

    assert missing_provider.executable is False
    assert [precondition.id for precondition in missing_provider.missing_preconditions] == [
        "provider_registered",
    ]

    ledger.append("tool.registered", workspace_id, {"tool": to_plain(_tool())})
    complete = ActionPlanService().precondition_report(
        _plan(), StateProjector(ledger).project(workspace_id)
    )

    assert complete.executable is True
    assert complete.missing_preconditions == []
    assert [precondition.satisfied for precondition in complete.preconditions] == [
        True,
        True,
        True,
    ]


def test_mutating_plan_approval_does_not_satisfy_execution_authorization():
    ledger = EventLedger()
    workspace_id = "ws"
    ledger.append("action_plan.approved", workspace_id, {"action_plan_id": "plan_1"})
    state = StateProjector(ledger).project(workspace_id)

    report = ActionPlanService().precondition_report(_plan(), state)

    authorization = next(
        precondition
        for precondition in report.preconditions
        if precondition.id == "execution_authorization_present"
    )
    assert authorization.satisfied is False
    assert [precondition.id for precondition in report.missing_preconditions] == [
        "target_host_known",
        "provider_registered",
        "execution_authorization_present",
    ]


def test_low_risk_read_only_plan_can_use_action_plan_approval():
    ledger = EventLedger()
    workspace_id = "ws"
    ledger.append("action_plan.approved", workspace_id, {"action_plan_id": "plan_1"})
    state = StateProjector(ledger).project(workspace_id)
    plan = _plan()
    plan = plan.model_copy(update={"risk_class": "L1", "requires_approval": False})

    report = ActionPlanService().precondition_report(plan, state)

    approval = next(
        precondition
        for precondition in report.preconditions
        if precondition.id == "approval_present"
    )
    assert approval.satisfied is True
    assert "action plan approval is present" in approval.reason
    assert "execution_authorization_present" not in [
        precondition.id for precondition in report.preconditions
    ]


def test_sqlite_execution_authorization_survives_reopen_for_preconditions(tmp_path):
    db_path = tmp_path / "events.sqlite"
    workspace_id = "ws"
    plan = _plan().model_copy(update={"status": "accepted"})
    ledger = SQLiteEventLedger(str(db_path))
    try:
        ledger.append(
            "action_plan.created", workspace_id, {"action_plan": to_plain(plan)}
        )
        ledger.append(
            "entity.upserted",
            workspace_id,
            {"entity": to_plain(Entity(id="ent_1", kind="host", name="node-1"))},
        )
        ledger.append("tool.registered", workspace_id, {"tool": to_plain(_tool())})
        authorization = ActionPlanService(ledger).grant_execution_authorization(
            workspace_id,
            "plan_1",
            tool_name="docker_container_lifecycle",
            tool_arguments={"container": "web", "operation": "restart"},
            granted_by="operator@example.com",
            ttl_seconds=300,
        )
        assert authorization.id.startswith("auth_")
    finally:
        ledger.close()

    reopened = SQLiteEventLedger(str(db_path))
    try:
        state = StateProjector(reopened).project(workspace_id)
        report = ActionPlanService().precondition_report(plan, state)

        assert report.executable is True
        assert report.missing_preconditions == []
        authorization_precondition = next(
            precondition
            for precondition in report.preconditions
            if precondition.id == "execution_authorization_present"
        )
        assert authorization_precondition.satisfied is True
        assert "execution authorization is present" in authorization_precondition.reason
    finally:
        reopened.close()


def test_expired_execution_authorization_does_not_satisfy_precondition():
    ledger = EventLedger()
    workspace_id = "ws"
    plan = _plan().model_copy(update={"status": "accepted"})
    ledger.append(
        "action_plan.created", workspace_id, {"action_plan": to_plain(plan)}
    )
    ledger.append(
        "entity.upserted",
        workspace_id,
        {"entity": to_plain(Entity(id="ent_1", kind="host", name="node-1"))},
    )
    ledger.append("tool.registered", workspace_id, {"tool": to_plain(_tool())})
    ledger.append(
        "execution_authorization.granted",
        workspace_id,
        {
            "execution_authorization": {
                "id": "auth_expired",
                "action_plan_id": "plan_1",
                "tool_name": "docker_container_lifecycle",
                "arguments_fingerprint": "sha256:expired",
                "granted_by": "operator@example.com",
                "expires_at": (
                    datetime.now(timezone.utc) - timedelta(seconds=1)
                ).isoformat(),
                "secret_seen_by_seed": False,
            }
        },
    )

    report = ActionPlanService().precondition_report(
        plan, StateProjector(ledger).project(workspace_id)
    )

    assert report.executable is False
    assert [precondition.id for precondition in report.missing_preconditions] == [
        "execution_authorization_present"
    ]
    authorization_precondition = next(
        precondition
        for precondition in report.preconditions
        if precondition.id == "execution_authorization_present"
    )
    assert authorization_precondition.satisfied is False
    assert "no current execution authorization" in authorization_precondition.reason


def test_execution_authorization_satisfies_mutating_plan_without_storing_arguments():
    ledger = EventLedger()
    workspace_id = "ws"
    plan = _plan().model_copy(update={"status": "accepted"})
    ledger.append(
        "action_plan.created", workspace_id, {"action_plan": to_plain(plan)}
    )
    ledger.append(
        "entity.upserted",
        workspace_id,
        {"entity": to_plain(Entity(id="ent_1", kind="host", name="node-1"))},
    )
    ledger.append("tool.registered", workspace_id, {"tool": to_plain(_tool())})

    authorization = ActionPlanService(ledger).grant_execution_authorization(
        workspace_id,
        "plan_1",
        tool_name="docker_container_lifecycle",
        tool_arguments={"container": "web", "operation": "restart"},
        granted_by="operator@example.com",
        interactive_prompt=True,
        ssh_agent="SSH_AUTH_SOCK",
        sudo_timestamp="host-sudo-cache",
        external_vault_token_ref="vault://seed/jit/session-1",
        session_id="ses_1",
    )
    state = StateProjector(ledger).project(workspace_id)

    report = ActionPlanService().precondition_report(plan, state)

    assert report.executable is True
    assert report.missing_preconditions == []
    assert state.execution_authorizations[authorization.id].tool_name == (
        "docker_container_lifecycle"
    )
    event = ledger.get(
        next(
            event.id
            for event in ledger.list_events(workspace_id)
            if event.kind == "execution_authorization.granted"
        )
    )
    assert event is not None
    payload = event.payload["execution_authorization"]
    assert "tool_arguments" not in payload
    assert "arguments_fingerprint" in payload
    assert payload["interactive_prompt"] is True
    assert payload["ssh_agent"] == "SSH_AUTH_SOCK"
    assert payload["sudo_timestamp"] == "host-sudo-cache"
    assert payload["external_vault_token_ref"] == "vault://seed/jit/session-1"
    assert payload["secret_seen_by_seed"] is False


def test_execution_authorization_rejects_common_secret_fields():
    ledger = EventLedger()
    workspace_id = "ws"
    plan = _plan().model_copy(update={"status": "accepted"})
    ledger.append(
        "action_plan.created", workspace_id, {"action_plan": to_plain(plan)}
    )

    for field in ("password", "passphrase", "token", "private_key"):
        try:
            ActionPlanService(ledger).grant_execution_authorization(
                workspace_id,
                "plan_1",
                tool_name="docker_container_lifecycle",
                tool_arguments={field: "not-stored"},
                granted_by="operator@example.com",
            )
        except ValueError as exc:
            assert "secret field" in str(exc)
        else:
            raise AssertionError(f"{field} fields must be rejected")
