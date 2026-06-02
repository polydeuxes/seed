from pathlib import Path

from seed_runtime.capability_catalog import CapabilityCatalog
from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Decision
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import FakeDecisionModel, Runtime
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService


def test_loads_checked_in_catalog_entries():
    catalog = CapabilityCatalog.load("capability_catalog")

    capabilities = [entry.capability for entry in catalog.list_entries()]

    assert capabilities == [
        "disk_inspection",
        "docker_inspection",
        "docker_installation",
        "documentation_lookup",
        "finance_lookup",
        "knowledge_lookup",
        "prometheus_query",
        "service_management",
        "weather_lookup",
        "web_search",
    ]
    assert catalog.get("weather_lookup").recommendations[0].provider == "open_meteo"


def test_recommend_for_matches_tool_need_capability():
    ledger = EventLedger()
    service = ToolNeedService(ledger, StateProjector(ledger))
    need = service.create_from_decision(
        "ws",
        Decision(
            kind="request_tool",
            reason="missing current weather",
            tool_need={
                "name": "weather_lookup",
                "summary": "Look up the current weather for a location",
                "capability": "weather_lookup",
            },
        ),
    )

    recommendations = CapabilityCatalog.load("capability_catalog").recommend_for(need)

    assert [recommendation.provider for recommendation in recommendations] == [
        "open_meteo"
    ]
    assert recommendations[0].kind == "public_api"


def test_returns_no_recommendations_for_unknown_capability():
    ledger = EventLedger()
    service = ToolNeedService(ledger, StateProjector(ledger))
    need = service.create_from_decision(
        "ws",
        Decision(
            kind="request_tool",
            reason="missing custom workflow",
            tool_need={
                "name": "custom_workflow",
                "summary": "Run a custom workflow that is not in the catalog",
                "capability": "custom_workflow",
            },
        ),
    )

    assert CapabilityCatalog.load("capability_catalog").recommend_for(need) == []


def test_runtime_tool_need_response_includes_recommendations_without_registering_tools():
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    runtime = Runtime(
        ledger,
        projector,
        ContextComposer(registry),
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        FakeDecisionModel(
            Decision(
                kind="request_tool",
                reason="missing weather capability",
                tool_need={
                    "name": "weather_lookup",
                    "summary": "Look up the current weather for a location",
                    "capability": "weather_lookup",
                },
            )
        ),
        capability_catalog=CapabilityCatalog.load("capability_catalog"),
    )

    response = runtime.handle_user_message("ws", "ses", "what is the weather?")

    assert response.kind == "tool_need"
    assert response.payload["recommendations"][0]["provider"] == "open_meteo"
    assert [tool.name for tool in registry.list_tools()] == ["echo"]
    assert projector.project("ws").tools == {}


def test_loads_yaml_catalog_entries_from_supplied_directory(tmp_path: Path):
    catalog_file = tmp_path / "example.yml"
    catalog_file.write_text(
        "\n".join(
            [
                "capability: Example Capability",
                "summary: Example lookup capability.",
                "recommendations:",
                "  - provider: example_provider",
                "    summary: Example provider recommendation.",
                "    kind: local_service",
                "    risk_class: L1",
            ]
        )
    )

    catalog = CapabilityCatalog.load(tmp_path)

    entry = catalog.get("example_capability")
    assert entry is not None
    assert entry.recommendations[0].provider == "example_provider"
