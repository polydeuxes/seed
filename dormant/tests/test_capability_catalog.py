from pathlib import Path

from seed_runtime.capability_catalog import CapabilityCatalog


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
    weather_recommendations = catalog.get("weather_lookup").recommendations
    assert [recommendation.provider for recommendation in weather_recommendations] == [
        "open_meteo",
        "wttr",
    ]
    assert catalog.get("custom_workflow") is None


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
