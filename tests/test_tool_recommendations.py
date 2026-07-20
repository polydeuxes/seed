import pytest
from seed_runtime.capability_catalog import (
    CapabilityCatalog,
    CapabilityCatalogEntry,
    CapabilityRecommendation,
)
from seed_runtime.models import Fact, ToolNeed, ToolSpec, Toolkit, utc_now
from seed_runtime.recommendation_ranker import (
    RankedRecommendation,
    RecommendationRanker,
)
from seed_runtime.registry import ToolRegistry
from seed_runtime.state import State
from seed_runtime.tool_recommendations import ToolRecommendationService


def _service_management_catalog() -> CapabilityCatalog:
    return CapabilityCatalog(
        [
            CapabilityCatalogEntry(
                capability="service_management",
                summary="Manage service lifecycle and status.",
                recommendations=[
                    CapabilityRecommendation(
                        provider="systemctl_cli",
                        summary="Use systemctl on systemd hosts.",
                        kind="local_cli",
                        source="systemd",
                        risk_class="L3",
                    ),
                    CapabilityRecommendation(
                        provider="docker_container_lifecycle",
                        summary="Use Docker container lifecycle operations.",
                        kind="local_cli",
                        source="docker",
                        risk_class="L3",
                    ),
                ],
            )
        ]
    )


def _tool_need() -> ToolNeed:
    return ToolNeed(
        id="need_service_management",
        workspace_id="ws",
        name="manage_service",
        summary="Manage the web_service service",
        capability="service_management",
        reason="missing service management capability",
    )


def _docker_state() -> State:
    return State(
        workspace_id="ws",
        facts={
            "fact_runtime_docker": Fact(
                id="fact_runtime_docker",
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                observed_at=utc_now(),
            )
        },
    )


def test_service_returns_same_ranked_recommendations_as_direct_runtime_logic():
    catalog = _service_management_catalog()
    state = _docker_state()
    need = _tool_need()

    service_recommendations = ToolRecommendationService(catalog).recommend_for(
        need, state
    )
    direct_recommendations = RecommendationRanker().rank(
        need.capability,
        catalog.recommend_for(need),
        state,
    )

    assert service_recommendations == direct_recommendations
    assert [recommendation.provider for recommendation in service_recommendations] == [
        "docker_container_lifecycle",
        "systemctl_cli",
    ]


def test_existing_capability_recommendation_ranking_behavior_remains_intact():
    catalog = _service_management_catalog()
    need = _tool_need()

    ranked = ToolRecommendationService(catalog).recommend_for(
        need, State(workspace_id="ws")
    )

    assert [recommendation.provider for recommendation in ranked] == [
        "systemctl_cli",
        "docker_container_lifecycle",
    ]
    assert "+5 catalog default priority" in ranked[0].reasoning
    assert "catalog default" in ranked[0].reasons


class RecordingToolRecommendationService(ToolRecommendationService):
    def __init__(self) -> None:
        self.calls: list[tuple[ToolNeed, State]] = []

    def recommend_for(
        self, tool_need: ToolNeed, state: State
    ) -> list[RankedRecommendation]:
        self.calls.append((tool_need, state))
        return [
            RankedRecommendation(
                provider="docker_container_lifecycle",
                summary="Use Docker container lifecycle operations.",
                kind="local_cli",
                source="docker",
                risk_class="L3",
                score=50,
                reasons=["provider matches known runtime: docker"],
                reasoning=["+50 provider matches known runtime: docker"],
            ),
            RankedRecommendation(
                provider="systemctl_cli",
                summary="Use systemctl on systemd hosts.",
                kind="local_cli",
                source="systemd",
                risk_class="L3",
                score=15,
                reasons=["catalog default"],
                reasoning=["+5 catalog default priority"],
            ),
        ]
