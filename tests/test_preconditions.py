from seed_runtime.action_plans import ActionPlanService
from seed_runtime.events import EventLedger
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
        "approval_present",
    ]
    assert [precondition.id for precondition in report.preconditions] == [
        "target_host_known",
        "provider_registered",
        "approval_present",
    ]
    assert [precondition.satisfied for precondition in report.preconditions] == [
        False,
        False,
        False,
    ]


def test_all_satisfied_preconditions_are_executable_without_execution():
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

    assert report.executable is True
    assert report.missing_preconditions == []
    assert [precondition.satisfied for precondition in report.preconditions] == [
        True,
        True,
        True,
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


def test_action_plan_approval_satisfies_approval_present():
    ledger = EventLedger()
    workspace_id = "ws"
    ledger.append("action_plan.approved", workspace_id, {"action_plan_id": "plan_1"})
    state = StateProjector(ledger).project(workspace_id)

    report = ActionPlanService().precondition_report(_plan(), state)

    approval = next(
        precondition
        for precondition in report.preconditions
        if precondition.id == "approval_present"
    )
    assert approval.satisfied is True
    assert "action plan approval is present" in approval.reason
    assert report.executable is False
    assert [precondition.id for precondition in report.missing_preconditions] == [
        "target_host_known",
        "provider_registered",
    ]


def test_executable_becomes_true_only_when_all_preconditions_are_true():
    ledger = EventLedger()
    workspace_id = "ws"
    ledger.append(
        "entity.upserted",
        workspace_id,
        {"entity": to_plain(Entity(id="ent_1", kind="host", name="node-1"))},
    )
    ledger.append("action_plan.approved", workspace_id, {"action_plan_id": "plan_1"})
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
