from datetime import timedelta

from seed_runtime.capability_catalog import CapabilityRecommendation
from seed_runtime.models import Fact, utc_now
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


def test_registered_provider_outranks_catalog_default():
    registered_tools = {
        "tools": [
            {
                "name": "restart_container",
                "summary": "Restart Docker containers",
                "toolkit_id": "docker_container_lifecycle",
                "policy_action": "docker_container_lifecycle.restart",
            }
        ]
    }

    ranked = RecommendationRanker().rank(
        "service_management",
        _service_recommendations(),
        State(workspace_id="ws"),
        registered_tools=registered_tools,
    )

    assert [recommendation.provider for recommendation in ranked] == [
        "docker_container_lifecycle",
        "systemctl_cli",
    ]
    assert ranked[0].score > ranked[1].score
    assert "+1000 provider already registered" in ranked[0].reasoning


def test_expired_docker_fact_does_not_beat_fresh_systemd_fact():
    now = utc_now()
    expired_docker = Fact(
        id="fact_runtime_docker_expired",
        subject_id="jellyfin",
        predicate="runtime",
        value="docker",
        observed_at=now,
        expires_at=now - timedelta(seconds=1),
    )
    fresh_systemd = Fact(
        id="fact_runtime_systemd_fresh",
        subject_id="jellyfin",
        predicate="runtime",
        value="systemd",
        observed_at=now,
    )
    state = State(
        workspace_id="ws",
        facts={expired_docker.id: expired_docker, fresh_systemd.id: fresh_systemd},
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
    assert any("known runtime: systemd" in reason for reason in ranked[0].reasoning)
    assert not any("known runtime: docker" in reason for reason in ranked[1].reasoning)
