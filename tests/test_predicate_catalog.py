import json

from seed_runtime.predicate_catalog import PredicateCatalog


def test_builtin_catalog_defines_canonical_predicates_and_prometheus_mappings():
    catalog = PredicateCatalog.load()

    availability = catalog.get("availability_status")
    assert availability is not None
    assert availability.kind == "measurement"
    assert availability.value_type == "enum"
    assert availability.allowed_values == ["up", "down", "unknown"]
    assert catalog.get("runtime").kind == "durable_fact"
    assert catalog.get("runtime").cardinality == "single"
    assert catalog.get("alias").cardinality == "multi"
    assert catalog.get("group").cardinality == "multi"
    assert catalog.get("ip_address").cardinality == "multi"
    assert catalog.get("network_interface").cardinality == "multi"
    assert catalog.get("interface_operstate").cardinality == "multi"
    assert catalog.get("interface_mac_address").cardinality == "multi"
    assert catalog.get("interface_mtu").cardinality == "multi"
    assert catalog.get("default_gateway").cardinality == "multi"
    assert catalog.get("dns_resolver").cardinality == "multi"
    assert catalog.get("ansible_host").cardinality == "multi"
    assert catalog.get("prometheus_instance").cardinality == "multi"
    local_observation = catalog.get("local_observation_status")
    assert local_observation is not None
    assert local_observation.kind == "measurement"
    assert local_observation.allowed_values == ["observed"]
    assert catalog.get("endpoint_role").kind == "durable_fact"
    assert catalog.get("endpoint_role").cardinality == "multi"
    assert catalog.find_mapping("up", source_name="prometheus").canonical_predicate == (
        "availability_status"
    )
    assert catalog.find_mapping("up", source_name="other") is None


def test_custom_predicate_catalog_can_be_loaded_from_file(tmp_path):
    path = tmp_path / "custom.json"
    path.write_text(
        json.dumps(
            {
                "predicates": [
                    {
                        "predicate": "service_health",
                        "kind": "measurement",
                        "value_type": "enum",
                        "allowed_values": ["healthy", "unhealthy"],
                    }
                ],
                "mappings": [
                    {
                        "source_name": "custom",
                        "predicate": "health",
                        "canonical_predicate": "service_health",
                    }
                ],
            }
        )
    )

    catalog = PredicateCatalog.load(path)

    assert catalog.is_measurement("service_health")
    assert catalog.cardinality("service_health") == "single"
    assert catalog.cardinality("unknown_predicate") == "single"
    assert catalog.find_mapping("health", source_name="custom") is not None


def test_show_predicate_catalog_cli_uses_custom_file(tmp_path, capsys):
    from scripts import seed_local

    path = tmp_path / "custom.json"
    path.write_text(
        json.dumps(
            {
                "predicates": [
                    {
                        "predicate": "service_health",
                        "kind": "measurement",
                        "value_type": "string",
                    }
                ],
                "mappings": [
                    {
                        "predicate": "health",
                        "canonical_predicate": "service_health",
                    }
                ],
            }
        )
    )

    assert seed_local.main(["--predicate-catalog", str(path), "--show-predicate-catalog"]) == 0
    output = capsys.readouterr().out
    assert "service_health: measurement/string/single" in output
    assert "*:health -> service_health" in output
