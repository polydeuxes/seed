from seed_runtime.capability_catalog import CapabilityRecommendation
from seed_runtime.models import Fact, ToolSpec, utc_now
from seed_runtime.recommendation_ranker import RecommendationRanker
from seed_runtime.state import State


def _service_recommendations() -> list[CapabilityRecommendation]:
    return [
        CapabilityRecommendation(
            provider="systemctl_cli",
            summary=(
                "Use systemctl for service lifecycle and status operations on "
                "systemd hosts."
            ),
            kind="local_cli",
            source="systemd",
            risk_class="L3",
        ),
        CapabilityRecommendation(
            provider="docker_container_lifecycle",
            summary=(
                "Use Docker container lifecycle operations for services running "
                "as containers."
            ),
            kind="local_cli",
            source="docker",
            risk_class="L3",
        ),
    ]


def _runtime_fact(value: str) -> Fact:
    return Fact(
        id=f"fact_runtime_{value}",
        subject_id="jellyfin",
        predicate="runtime",
        value=value,
        observed_at=utc_now(),
    )


def _tool(name: str) -> ToolSpec:
    return ToolSpec(
        name=name,
        summary=f"{name} provider",
        toolkit_id=f"toolkit_{name}",
        input_schema={},
        output_schema={},
        policy_action=f"{name}.run",
        implementation=f"toolkits.{name}:run",
        risk_class="L3",
    )


def test_docker_runtime_prefers_docker_container_lifecycle():
    state = State(
        workspace_id="ws",
        facts={"fact_runtime_docker": _runtime_fact("docker")},
    )

    ranked = RecommendationRanker().rank(
        "service_management",
        _service_recommendations(),
        state,
    )

    assert [recommendation.provider for recommendation in ranked] == [
        "docker_container_lifecycle",
        "systemctl_cli",
    ]
    assert ranked[0].score > ranked[1].score
    assert any("known runtime: docker" in reason for reason in ranked[0].reasoning)


def test_systemd_runtime_prefers_systemctl_cli():
    state = State(
        workspace_id="ws",
        facts={"fact_runtime_systemd": _runtime_fact("systemd")},
    )

    ranked = RecommendationRanker().rank(
        "service_management",
        _service_recommendations(),
        state,
    )

    assert [recommendation.provider for recommendation in ranked] == [
        "systemctl_cli",
        "docker_container_lifecycle",
    ]
    assert ranked[0].score > ranked[1].score
    assert any("known runtime: systemd" in reason for reason in ranked[0].reasoning)


def test_no_facts_falls_back_to_catalog_order():
    ranked = RecommendationRanker().rank(
        "service_management",
        _service_recommendations(),
        State(workspace_id="ws"),
    )

    assert [recommendation.provider for recommendation in ranked] == [
        "systemctl_cli",
        "docker_container_lifecycle",
    ]
    assert ranked[0].score >= ranked[1].score
    assert "+5 catalog default priority" in ranked[0].reasoning
    assert "catalog default" in ranked[0].reasons


def test_registered_provider_outranks_unregistered_provider():
    state = State(
        workspace_id="ws",
        tools={"docker_container_lifecycle": _tool("docker_container_lifecycle")},
    )

    ranked = RecommendationRanker().rank(
        "service_management",
        _service_recommendations(),
        state,
    )

    assert [recommendation.provider for recommendation in ranked] == [
        "docker_container_lifecycle",
        "systemctl_cli",
    ]
    assert ranked[0].score > ranked[1].score
    assert "+100 provider already registered" in ranked[0].reasoning
