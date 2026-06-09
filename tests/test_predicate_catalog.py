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
    assert catalog.get("interface_role").cardinality == "multi"
    assert catalog.get("interface_role").allowed_values == [
        "primary",
        "secondary",
        "loopback",
        "virtual",
        "container",
        "vpn",
    ]
    assert catalog.get("address_assignment_method").allowed_values == [
        "dhcp",
        "static",
        "unknown",
    ]
    assert catalog.get("interface_mac_address").cardinality == "multi"
    assert catalog.get("interface_mtu").cardinality == "multi"
    assert catalog.get("default_gateway").cardinality == "multi"
    assert catalog.get("dns_resolver").cardinality == "multi"
    assert catalog.get("dns_resolver_stub").cardinality == "multi"
    assert catalog.get("dns_resolver_upstream").cardinality == "multi"
    for predicate in (
        "listening_address",
        "listening_endpoint",
        "listening_port",
        "listening_protocol",
    ):
        definition = catalog.get(predicate)
        assert definition is not None
        assert definition.kind == "durable_fact"
        assert definition.cardinality == "multi"
    assert catalog.get("listening_port").value_type == "integer"
    assert catalog.get("listening_protocol").allowed_values == ["tcp", "udp"]
    assert catalog.get("ansible_host").cardinality == "multi"
    assert catalog.get("prometheus_instance").cardinality == "multi"
    local_observation = catalog.get("local_observation_status")
    assert local_observation is not None
    assert local_observation.kind == "measurement"
    assert local_observation.allowed_values == ["observed"]
    assert catalog.get("endpoint_role").kind == "durable_fact"
    assert catalog.get("endpoint_role").cardinality == "multi"
    for predicate in (
        "kernel_release",
        "kernel_version",
        "cpu_model",
        "cpu_count",
        "memory_total_bytes",
    ):
        definition = catalog.get(predicate)
        assert definition is not None
        assert definition.kind == "durable_fact"
        assert definition.cardinality == "single"
    assert catalog.get("cpu_count").value_type == "integer"
    assert catalog.get("memory_total_bytes").value_type == "integer"
    for predicate in (
        "block_device",
        "partition",
        "block_device_model",
        "block_device_vendor",
        "block_device_parent",
    ):
        definition = catalog.get(predicate)
        assert definition is not None
        assert definition.kind == "durable_fact"
        assert definition.value_type == "string"
        assert definition.cardinality == "multi"
    assert catalog.get("block_device_size_bytes").value_type == "integer"
    assert catalog.get("block_device_size_bytes").cardinality == "multi"
    assert catalog.get("block_device_rotational").allowed_values == [
        "true",
        "false",
    ]
    assert catalog.get("block_device_removable").allowed_values == [
        "true",
        "false",
    ]
    for predicate in (
        "package_installed",
        "package_version",
        "package_architecture",
        "package_manager",
    ):
        definition = catalog.get(predicate)
        assert definition is not None
        assert definition.kind == "durable_fact"
        assert definition.value_type == "string"
        assert definition.cardinality == "multi"
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

    assert (
        seed_local.main(["--predicate-catalog", str(path), "--show-predicate-catalog"])
        == 0
    )
    output = capsys.readouterr().out
    assert "service_health: measurement/string/single" in output
    assert "*:health -> service_health" in output
