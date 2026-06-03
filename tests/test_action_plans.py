import pytest

from seed_runtime.action_plans import (
    ActionPlanService,
    ActionPlanTransitionError,
)
from seed_runtime.events import EventLedger
from seed_runtime.models import ToolNeed
from seed_runtime.recommendation_ranker import RankedRecommendation
from seed_runtime.state import State, StateProjector


def test_creates_text_only_weather_lookup_plan_for_open_meteo():
    need = ToolNeed(
        id="need_weather",
        workspace_id="ws",
        name="weather_lookup",
        capability="weather_lookup",
        summary="Look up a forecast",
        reason="User asked for weather",
    )
    recommendation = RankedRecommendation(
        provider="open_meteo",
        summary=(
            "Public weather API suitable for forecast and current-condition lookup."
        ),
        kind="public_api",
        source="https://open-meteo.com/",
        risk_class="L1",
        notes="Requires explicit integration by a builder or operator before use.",
        score=15,
        reasons=["lower risk class: L1"],
        reasoning=["+10 lower risk class: L1", "+5 catalog default priority"],
    )

    plan = ActionPlanService().create_plan(
        need, recommendation, State(workspace_id="ws")
    )

    assert plan.tool_need_id == "need_weather"
    assert plan.provider == "open_meteo"
    assert plan.capability == "weather_lookup"
    assert plan.risk_class == "L1"
    assert plan.requires_approval is False
    assert plan.executable is False
    assert plan.steps == [
        "Determine location.",
        "Query Open-Meteo forecast endpoint.",
        "Return result as Evidence.",
    ]
    assert "open_meteo" in plan.summary


def test_creates_non_executable_service_management_plan_that_requires_approval():
    need = ToolNeed(
        id="need_service",
        workspace_id="ws",
        name="restart_jellyfin",
        capability="service_management",
        summary="Restart a containerized service",
        reason="User asked to restart Jellyfin",
    )
    recommendation = RankedRecommendation(
        provider="docker_container_lifecycle",
        summary=(
            "Use Docker container lifecycle operations for services running as containers."
        ),
        kind="local_cli",
        source="docker",
        risk_class="L3",
        notes=(
            "Mutating container lifecycle actions require confirmation or approval "
            "according to policy."
        ),
        score=110,
        reasons=["provider matches known runtime: docker"],
        reasoning=["+100 provider matches known runtime: docker"],
    )

    plan = ActionPlanService().create_plan(
        need, recommendation, State(workspace_id="ws")
    )

    assert plan.tool_need_id == "need_service"
    assert plan.provider == "docker_container_lifecycle"
    assert plan.capability == "service_management"
    assert plan.risk_class == "L3"
    assert plan.requires_approval is True
    assert plan.executable is False
    assert plan.steps == [
        "Identify target host for service.",
        "Confirm container name.",
        "Verify Docker access.",
        "Request approval before restart.",
    ]
    assert "docker_container_lifecycle" in plan.summary


def test_create_plan_appends_action_plan_created_event():
    ledger = EventLedger()
    need = ToolNeed(
        id="need_weather",
        workspace_id="ws",
        name="weather_lookup",
        capability="weather_lookup",
        summary="Look up a forecast",
        reason="User asked for weather",
    )
    recommendation = RankedRecommendation(
        provider="open_meteo",
        summary="Public weather API suitable for forecast lookup.",
        kind="public_api",
        source="https://open-meteo.com/",
        risk_class="L1",
        notes="Requires explicit integration.",
        score=15,
        reasons=["lower risk class: L1"],
        reasoning=["+10 lower risk class: L1"],
    )

    plan = ActionPlanService(ledger).create_plan(
        need, recommendation, State(workspace_id="ws"), session_id="ses"
    )

    events = ledger.list_events("ws")
    assert [event.kind for event in events] == ["action_plan.created"]
    assert events[0].payload["action_plan"]["id"] == plan.id
    assert events[0].payload["action_plan"]["executable"] is False
    assert events[0].session_id == "ses"


def test_projected_state_includes_action_plan_by_id_and_remains_non_executable():
    ledger = EventLedger()
    need = ToolNeed(
        id="need_service",
        workspace_id="ws",
        name="restart_jellyfin",
        capability="service_management",
        summary="Restart a containerized service",
        reason="User asked to restart Jellyfin",
    )
    recommendation = RankedRecommendation(
        provider="docker_container_lifecycle",
        summary="Use Docker container lifecycle operations.",
        kind="local_cli",
        source="docker",
        risk_class="L3",
        notes="Mutating actions require approval.",
        score=110,
        reasons=["provider matches known runtime: docker"],
        reasoning=["+100 provider matches known runtime: docker"],
    )

    plan = ActionPlanService(ledger).create_plan(
        need, recommendation, State(workspace_id="ws")
    )

    state = StateProjector(ledger).project("ws")
    assert set(state.action_plans) == {plan.id}
    projected_plan = state.action_plans[plan.id]
    assert projected_plan == plan
    assert projected_plan.executable is False
    assert projected_plan.requires_approval is True


def test_create_plan_does_not_execute_tools_or_register_tools_or_approve():
    ledger = EventLedger()
    need = ToolNeed(
        id="need_service",
        workspace_id="ws",
        name="restart_jellyfin",
        capability="service_management",
        summary="Restart a containerized service",
        reason="User asked to restart Jellyfin",
    )
    recommendation = RankedRecommendation(
        provider="docker_container_lifecycle",
        summary="Use Docker container lifecycle operations.",
        kind="local_cli",
        source="docker",
        risk_class="L3",
        notes="Mutating actions require approval.",
        score=110,
        reasons=["provider matches known runtime: docker"],
        reasoning=["+100 provider matches known runtime: docker"],
    )

    ActionPlanService(ledger).create_plan(
        need, recommendation, State(workspace_id="ws")
    )

    kinds = [event.kind for event in ledger.list_events("ws")]
    assert kinds == ["action_plan.created"]
    assert "tool.call.started" not in kinds
    assert "tool.call.completed" not in kinds
    assert "tool.registered" not in kinds
    assert "approval.granted" not in kinds


def _weather_need() -> ToolNeed:
    return ToolNeed(
        id="need_weather",
        workspace_id="ws",
        name="weather_lookup",
        capability="weather_lookup",
        summary="Look up a forecast",
        reason="User asked for weather",
    )


def _weather_recommendation(provider: str = "open_meteo") -> RankedRecommendation:
    return RankedRecommendation(
        provider=provider,
        summary="Public weather API suitable for forecast lookup.",
        kind="public_api",
        source="https://open-meteo.com/",
        risk_class="L1",
        notes="Requires explicit integration.",
        score=15,
        reasons=["lower risk class: L1"],
        reasoning=["+10 lower risk class: L1"],
    )


def test_created_plan_defaults_to_proposed():
    plan = ActionPlanService().create_plan(
        _weather_need(), _weather_recommendation(), State(workspace_id="ws")
    )

    assert plan.status == "proposed"
    assert plan.rejection_reason is None
    assert plan.replacement_plan_id is None


def test_accept_plan_changes_projected_status_to_accepted():
    ledger = EventLedger()
    service = ActionPlanService(ledger)
    plan = service.create_plan(
        _weather_need(), _weather_recommendation(), State(workspace_id="ws")
    )

    accepted = service.accept_plan("ws", plan.id, session_id="ses")

    assert accepted.status == "accepted"
    events = ledger.list_events("ws")
    assert [event.kind for event in events] == [
        "action_plan.created",
        "action_plan.accepted",
    ]
    assert events[-1].session_id == "ses"
    projected = StateProjector(ledger).project("ws").action_plans[plan.id]
    assert projected.status == "accepted"
    assert projected.executable is False


def test_reject_plan_records_reason_in_event_and_projected_state():
    ledger = EventLedger()
    service = ActionPlanService(ledger)
    plan = service.create_plan(
        _weather_need(), _weather_recommendation(), State(workspace_id="ws")
    )

    rejected = service.reject_plan("ws", plan.id, "Use another provider")

    assert rejected.status == "rejected"
    assert rejected.rejection_reason == "Use another provider"
    event = ledger.list_events("ws")[-1]
    assert event.kind == "action_plan.rejected"
    assert event.payload["reason"] == "Use another provider"
    projected = StateProjector(ledger).project("ws").action_plans[plan.id]
    assert projected.status == "rejected"
    assert projected.rejection_reason == "Use another provider"


def test_supersede_plan_records_replacement_id_in_event_and_projected_state():
    ledger = EventLedger()
    service = ActionPlanService(ledger)
    original = service.create_plan(
        _weather_need(), _weather_recommendation(), State(workspace_id="ws")
    )
    replacement = service.create_plan(
        _weather_need(), _weather_recommendation("weather_api"), State(workspace_id="ws")
    )

    superseded = service.supersede_plan("ws", original.id, replacement.id)

    assert superseded.status == "superseded"
    assert superseded.replacement_plan_id == replacement.id
    event = ledger.list_events("ws")[-1]
    assert event.kind == "action_plan.superseded"
    assert event.payload["replacement_plan_id"] == replacement.id
    projected = StateProjector(ledger).project("ws").action_plans[original.id]
    assert projected.status == "superseded"
    assert projected.replacement_plan_id == replacement.id


def test_lifecycle_unknown_plan_id_raises_clean_error():
    from seed_runtime.action_plans import ActionPlanNotFoundError

    ledger = EventLedger()
    service = ActionPlanService(ledger)

    try:
        service.accept_plan("ws", "plan_missing")
    except ActionPlanNotFoundError as exc:
        assert "action plan not found" in str(exc)
        assert "plan_missing" in str(exc)
    else:
        raise AssertionError("expected ActionPlanNotFoundError")


def _create_projected_plan(
    service: ActionPlanService, provider: str = "open_meteo"
):
    return service.create_plan(
        _weather_need(), _weather_recommendation(provider), State(workspace_id="ws")
    )


def _set_plan_status(service: ActionPlanService, plan_id: str, status: str) -> None:
    if status == "proposed":
        return
    if status == "accepted":
        service.accept_plan("ws", plan_id)
        return
    if status == "rejected":
        service.reject_plan("ws", plan_id, "not this provider")
        return
    if status == "superseded":
        service.supersede_plan("ws", plan_id, "plan_replacement")
        return
    raise AssertionError(f"unknown status: {status}")


def _apply_transition(
    service: ActionPlanService, plan_id: str, target_status: str
):
    if target_status == "accepted":
        return service.accept_plan("ws", plan_id)
    if target_status == "rejected":
        return service.reject_plan("ws", plan_id, "no longer preferred")
    if target_status == "superseded":
        return service.supersede_plan("ws", plan_id, f"replacement_for_{plan_id}")
    raise AssertionError(f"unknown target status: {target_status}")


@pytest.mark.parametrize(
    ("initial_status", "target_status"),
    [
        ("proposed", "accepted"),
        ("proposed", "rejected"),
        ("proposed", "superseded"),
        ("accepted", "superseded"),
    ],
)
def test_action_plan_service_allows_valid_lifecycle_transitions(
    initial_status: str, target_status: str
):
    ledger = EventLedger()
    service = ActionPlanService(ledger)
    plan = _create_projected_plan(service)
    _set_plan_status(service, plan.id, initial_status)

    transitioned = _apply_transition(service, plan.id, target_status)

    assert transitioned.status == target_status
    projected = StateProjector(ledger).project("ws").action_plans[plan.id]
    assert projected.status == target_status


@pytest.mark.parametrize(
    ("initial_status", "target_status"),
    [
        ("accepted", "accepted"),
        ("accepted", "rejected"),
        ("rejected", "accepted"),
        ("rejected", "rejected"),
        ("rejected", "superseded"),
        ("superseded", "accepted"),
        ("superseded", "rejected"),
        ("superseded", "superseded"),
    ],
)
def test_action_plan_service_rejects_invalid_lifecycle_transitions(
    initial_status: str, target_status: str
):
    ledger = EventLedger()
    service = ActionPlanService(ledger)
    plan = _create_projected_plan(service)
    _set_plan_status(service, plan.id, initial_status)
    events_before = ledger.list_events("ws")

    with pytest.raises(ActionPlanTransitionError) as excinfo:
        _apply_transition(service, plan.id, target_status)

    assert f"{initial_status!r} -> {target_status!r}" in str(excinfo.value)
    assert ledger.list_events("ws") == events_before
    projected = StateProjector(ledger).project("ws").action_plans[plan.id]
    assert projected.status == initial_status
