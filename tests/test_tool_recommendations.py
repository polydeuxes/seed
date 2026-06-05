from seed_runtime.capability_catalog import (
    CapabilityCatalog,
    CapabilityCatalogEntry,
    CapabilityRecommendation,
)
from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision, Fact, ToolNeed, ToolSpec, Toolkit, utc_now
from seed_runtime.policy import PolicyGate
from seed_runtime.projection_store import InMemoryProjectionStore
from seed_runtime.recommendation_ranker import RankedRecommendation, RecommendationRanker
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel, Runtime
from seed_runtime.runtime_loop import (
    Decision as LoopDecision,
    EchoTool,
    FakeDecisionProvider,
    RuntimeInput,
    RuntimeLoop,
)
from seed_runtime.serialization import to_plain
from seed_runtime.state import State, StateProjector
from seed_runtime.tool_needs import ToolNeedService
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


def _request_tool_decision() -> Decision:
    return Decision(
        kind="request_tool",
        reason="missing service management capability",
        tool_need={
            "name": "manage_service",
            "summary": "Manage the Jellyfin service",
            "capability": "service_management",
        },
    )


def _tool_need(ledger: EventLedger | None = None) -> ToolNeed:
    ledger = ledger or EventLedger()
    return ToolNeedService(ledger, StateProjector(ledger)).create_from_decision(
        "ws", _request_tool_decision()
    )


def _docker_state() -> State:
    return State(
        workspace_id="ws",
        facts={
            "fact_runtime_docker": Fact(
                id="fact_runtime_docker",
                subject_id="jellyfin",
                predicate="runtime",
                value="docker",
                observed_at=utc_now(),
            )
        },
    )


def _runtime_with_decision(
    decision: Decision, ledger: EventLedger, projector: StateProjector
) -> Runtime:
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    return Runtime(
        ledger,
        projector,
        ContextComposer(registry),
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        FakeDecisionModel(decision),
        capability_catalog=_service_management_catalog(),
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


def test_runtime_request_tool_recommendation_payload_stays_unchanged():
    ledger = EventLedger()
    projector = StateProjector(ledger)
    fact = Fact(
        id="fact_runtime_docker",
        subject_id="jellyfin",
        predicate="runtime",
        value="docker",
        observed_at=utc_now(),
    )
    ledger.append("fact.recorded", "ws", {"fact": to_plain(fact)}, actor="system")
    runtime = _runtime_with_decision(_request_tool_decision(), ledger, projector)

    response = runtime.handle_user_message("ws", "ses", "manage jellyfin")
    projected_state = projector.project("ws")
    tool_need = projected_state.open_tool_needs[0]
    expected_recommendations = [
        {
            "provider": recommendation.provider,
            "score": recommendation.score,
            "reasons": list(recommendation.reasons),
        }
        for recommendation in ToolRecommendationService(
            _service_management_catalog()
        ).recommend_for(tool_need, projected_state)
    ]

    assert response.kind == "tool_need"
    assert response.payload == {
        "tool_need": to_plain(tool_need),
        "recommendations": expected_recommendations,
    }
    assert set(response.payload["recommendations"][0]) == {
        "provider",
        "score",
        "reasons",
    }


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


def test_runtime_loop_request_tool_result_includes_ranked_recommendations():
    ledger = EventLedger()
    projector = StateProjector(ledger)
    fact = Fact(
        id="fact_runtime_docker",
        subject_id="jellyfin",
        predicate="runtime",
        value="docker",
        observed_at=utc_now(),
    )
    ledger.append("fact.observed", "ws_loop", {"fact": to_plain(fact)}, actor="system")
    registry = ToolRegistry()
    recommendation_service = ToolRecommendationService(_service_management_catalog())
    runtime = RuntimeLoop(
        ledger,
        InMemoryProjectionStore(),
        registry,
        PolicyGate(),
        FakeDecisionProvider(
            LoopDecision(
                kind="request_tool",
                reason="missing service management capability",
                tool_need={
                    "name": "Manage Service",
                    "summary": "Manage the Jellyfin service",
                    "capability": "service_management",
                },
            )
        ),
        {},
        projector=projector,
        tool_recommendation_service=recommendation_service,
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="manage jellyfin"))
    events = ledger.list_events("ws_loop")

    assert result.decision_kind == "request_tool"
    assert [recommendation["provider"] for recommendation in result.recommendations] == [
        "docker_container_lifecycle",
        "systemctl_cli",
    ]
    assert set(result.recommendations[0]) == {"provider", "score", "reasons"}
    assert result.recommendations[0]["score"] > result.recommendations[1]["score"]
    assert [event.kind for event in events] == [
        "fact.observed",
        "input.user_message",
        "tool_need.created",
        "decision.recorded",
    ]
    assert set(events[2].payload) == {"tool_need"}


def test_runtime_loop_request_tool_uses_injected_recommendation_service_without_events():
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.register_toolkit(
        Toolkit(
            id="tk_loop_echo",
            name="loop echo",
            summary="RuntimeLoop test tools.",
            tools=[
                ToolSpec(
                    toolkit_id="tk_loop_echo",
                    name="echo",
                    summary="Echo a message deterministically.",
                    input_schema={},
                    output_schema={},
                    policy_action="echo.run",
                    implementation="tests:echo",
                    risk_class="L1",
                )
            ],
        )
    )
    recommendation_service = RecordingToolRecommendationService()
    runtime = RuntimeLoop(
        ledger,
        InMemoryProjectionStore(),
        registry,
        PolicyGate(),
        FakeDecisionProvider(
            LoopDecision(
                kind="request_tool",
                reason="missing capability",
                tool_need={
                    "name": "Lookup Service Status",
                    "summary": "Look up service status from inventory",
                    "capability": "Service Status Lookup",
                },
            )
        ),
        {"echo": EchoTool()},
        tool_recommendation_service=recommendation_service,
    )

    result = runtime.run(RuntimeInput(workspace_id="ws_loop", user_text="check service"))
    events = ledger.list_events("ws_loop")

    assert result.decision_kind == "request_tool"
    assert result.response_text == "Recorded tool need lookup_service_status."
    assert result.recommendations == [
        {
            "provider": "docker_container_lifecycle",
            "score": 50,
            "reasons": ["provider matches known runtime: docker"],
        },
        {
            "provider": "systemctl_cli",
            "score": 15,
            "reasons": ["catalog default"],
        },
    ]
    assert [event.kind for event in events] == [
        "input.user_message",
        "tool_need.created",
        "decision.recorded",
    ]
    assert set(events[1].payload) == {"tool_need"}
    assert "recommendations" not in events[1].payload
    assert len(recommendation_service.calls) == 1
    service_tool_need, service_state = recommendation_service.calls[0]
    assert service_tool_need.name == "lookup_service_status"
    assert service_tool_need.capability == "service_status_lookup"
    assert service_state.open_tool_needs[0].name == "lookup_service_status"
