import pytest
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
from seed_runtime.recommendation_ranker import (
    RankedRecommendation,
    RecommendationRanker,
)
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel, Runtime
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
            "summary": "Manage the web_service service",
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
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                observed_at=utc_now(),
            )
        },
    )


def _runtime_with_decision(
    decision: Decision,
    ledger: EventLedger,
    projector: StateProjector,
    *,
    registry: ToolRegistry | None = None,
    capability_catalog: CapabilityCatalog | None = None,
    tool_executor: ToolExecutor | None = None,
) -> Runtime:
    registry = registry or ToolRegistry()
    if registry.get("echo") is None:
        registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    return Runtime(
        ledger,
        projector,
        ContextComposer(registry),
        DecisionValidator(registry),
        tool_executor or ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        FakeDecisionModel(decision),
        capability_catalog=capability_catalog or _service_management_catalog(),
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
        subject_id="web_service",
        predicate="runtime",
        value="docker",
        observed_at=utc_now(),
    )
    ledger.append("fact.recorded", "ws", {"fact": to_plain(fact)}, actor="system")
    runtime = _runtime_with_decision(_request_tool_decision(), ledger, projector)

    response = runtime.handle_user_message("ws", "ses", "manage web_service")
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
        "capability_resolution": {
            "known_capability": True,
            "registered_operations": [],
            "provider_recommendations": expected_recommendations,
            "handoff_candidates": [],
        },
    }
    assert set(response.payload["recommendations"][0]) == {
        "provider",
        "score",
        "reasons",
    }


def _ssh_access_catalog(operation: str = "verify_ssh_access") -> CapabilityCatalog:
    return CapabilityCatalog(
        [
            CapabilityCatalogEntry(
                capability="ssh_access",
                summary="Inspect SSH access availability.",
                recommendations=[
                    CapabilityRecommendation(
                        provider="ansible_ssh",
                        summary="Use an external Ansible handoff for SSH checks.",
                        kind="handoff",
                        source="ansible",
                        risk_class="L2",
                        backend_type="ansible",
                        operation=operation,
                    )
                ],
            )
        ]
    )


def _ssh_access_decision() -> Decision:
    return Decision(
        kind="request_tool",
        reason="missing SSH access capability",
        tool_need={
            "name": "verify_ssh_access",
            "summary": "Verify whether SSH access is available",
            "capability": "ssh_access",
        },
    )


def _registry_with_ssh_tools() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register_toolkit(
        Toolkit(
            id="tk_generated_ssh_access",
            name="Generated SSH access",
            summary="Generated SSH access operations.",
            tools=[
                ToolSpec(
                    toolkit_id="tk_generated_ssh_access",
                    name="verify_ssh_access",
                    summary="Verify whether SSH access is available.",
                    input_schema={},
                    output_schema={},
                    policy_action="ssh_access.verify",
                    implementation="tests:verify_ssh_access",
                    risk_class="L1",
                    capabilities=["ssh_access"],
                ),
                ToolSpec(
                    toolkit_id="tk_generated_ssh_access",
                    name="hidden_ssh_access",
                    summary="Hidden SSH access operation.",
                    input_schema={},
                    output_schema={},
                    policy_action="ssh_access.hidden",
                    implementation="tests:hidden_ssh_access",
                    risk_class="L1",
                    visibility="hidden",
                    capabilities=["ssh_access"],
                ),
                ToolSpec(
                    toolkit_id="tk_generated_ssh_access",
                    name="draft_ssh_access",
                    summary="Draft SSH access operation.",
                    input_schema={},
                    output_schema={},
                    policy_action="ssh_access.draft",
                    implementation="tests:draft_ssh_access",
                    risk_class="L1",
                    status="draft",
                    capabilities=["ssh_access"],
                ),
            ],
        )
    )
    return registry


class RecordingToolExecutor(ToolExecutor):
    def __init__(
        self, ledger: EventLedger, registry: ToolRegistry, projector: StateProjector
    ) -> None:
        super().__init__(ledger, registry, projector)
        self.calls: list[tuple[object, ...]] = []

    def execute(self, *args: object, **kwargs: object):  # type: ignore[no-untyped-def]
        self.calls.append(args)
        return super().execute(*args, **kwargs)


def test_runtime_request_tool_response_includes_read_only_capability_resolution():
    ledger = EventLedger()
    projector = StateProjector(ledger)
    registry = _registry_with_ssh_tools()
    runtime = _runtime_with_decision(
        _ssh_access_decision(),
        ledger,
        projector,
        registry=registry,
        capability_catalog=_ssh_access_catalog(),
    )

    response = runtime.handle_user_message("ws", "ses", "check ssh access")

    resolution = response.payload["capability_resolution"]
    assert resolution["known_capability"] is True
    assert resolution["registered_operations"] == [
        {
            "name": "verify_ssh_access",
            "summary": "Verify whether SSH access is available.",
            "toolkit_id": "tk_generated_ssh_access",
            "policy_action": "ssh_access.verify",
            "risk_class": "L1",
            "visibility": "model_visible",
            "status": "registered",
            "capabilities": ["ssh_access"],
        }
    ]
    assert resolution["provider_recommendations"] == response.payload["recommendations"]
    assert resolution["provider_recommendations"][0]["provider"] == "ansible_ssh"
    assert resolution["handoff_candidates"] == [
        {
            "provider": "ansible_ssh",
            "backend_type": "ansible",
            "operation": "verify_ssh_access",
        }
    ]
    assert [event.kind for event in ledger.list_events("ws")].count(
        "tool_need.created"
    ) == 1


def test_runtime_request_tool_unknown_catalog_can_still_report_registry_candidates():
    ledger = EventLedger()
    projector = StateProjector(ledger)
    runtime = _runtime_with_decision(
        _ssh_access_decision(),
        ledger,
        projector,
        registry=_registry_with_ssh_tools(),
        capability_catalog=CapabilityCatalog(),
    )

    response = runtime.handle_user_message("ws", "ses", "check ssh access")

    resolution = response.payload["capability_resolution"]
    assert resolution["known_capability"] is False
    assert [operation["name"] for operation in resolution["registered_operations"]] == [
        "verify_ssh_access"
    ]
    assert resolution["provider_recommendations"] == []
    assert resolution["handoff_candidates"] == []


def test_runtime_request_tool_registered_operations_come_only_from_registry_capability_lookup():
    ledger = EventLedger()
    projector = StateProjector(ledger)
    registry = ToolRegistry()
    registry.register_toolkit(
        Toolkit(
            id="tk_catalog_operation_name",
            name="Catalog operation name",
            summary="Registered operation without matching capability.",
            tools=[
                ToolSpec(
                    toolkit_id="tk_catalog_operation_name",
                    name="catalog_named_operation",
                    summary="Name matches catalog metadata only.",
                    input_schema={},
                    output_schema={},
                    policy_action="catalog.operation",
                    implementation="tests:catalog_named_operation",
                    capabilities=[],
                )
            ],
        )
    )
    runtime = _runtime_with_decision(
        _ssh_access_decision(),
        ledger,
        projector,
        registry=registry,
        capability_catalog=_ssh_access_catalog(operation="catalog_named_operation"),
    )

    response = runtime.handle_user_message("ws", "ses", "check ssh access")

    resolution = response.payload["capability_resolution"]
    assert resolution["registered_operations"] == []
    assert resolution["handoff_candidates"] == [
        {
            "provider": "ansible_ssh",
            "backend_type": "ansible",
            "operation": "catalog_named_operation",
        }
    ]


def test_runtime_request_tool_resolution_does_not_call_tool_executor():
    ledger = EventLedger()
    projector = StateProjector(ledger)
    registry = _registry_with_ssh_tools()
    executor = RecordingToolExecutor(ledger, registry, projector)
    runtime = _runtime_with_decision(
        _ssh_access_decision(),
        ledger,
        projector,
        registry=registry,
        capability_catalog=_ssh_access_catalog(),
        tool_executor=executor,
    )

    response = runtime.handle_user_message("ws", "ses", "check ssh access")

    assert response.kind == "tool_need"
    assert executor.calls == []
    assert [event.kind for event in ledger.list_events("ws")] == [
        "input.user_message",
        "model.decision.proposed",
        "tool_need.created",
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
