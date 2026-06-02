from seed_runtime.action_plans import ActionPlanService
from seed_runtime.models import ToolNeed
from seed_runtime.recommendation_ranker import RankedRecommendation
from seed_runtime.state import State


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
