from datetime import datetime, timezone

import pytest

from seed_runtime import AnsibleInventoryObservationSource
from seed_runtime.events import EventLedger
from seed_runtime.observation_sources import FakeObservationSource, ObservationCollectionService
from seed_runtime.observations import Observation, ObservationIngestor
from seed_runtime.state import StateProjector


def _triples(observations):
    return {(observation.subject, observation.predicate, observation.value) for observation in observations}


def test_ini_inventory_emits_authoritative_identity_observations(tmp_path):
    inventory_path = tmp_path / "inventory.ini"
    inventory_path.write_text(
        "[nodegroup]\nexample_host ansible_host=192.0.2.115\n", encoding="utf-8"
    )

    observations = AnsibleInventoryObservationSource(inventory_path).collect()

    assert _triples(observations) == {
        ("example_host", "hostname", "example_host"),
        ("example_host", "ansible_host", "192.0.2.115"),
        ("example_host", "ip_address", "192.0.2.115"),
        ("example_host", "alias", "192.0.2.115"),
        ("example_host", "group", "nodegroup"),
    }
    assert {observation.source_type for observation in observations} == {"imported"}
    assert {observation.confidence for observation in observations} == {0.95}
    assert all(
        observation.metadata["source_name"] == "ansible_inventory"
        and observation.metadata["inventory_path"] == str(inventory_path)
        and observation.metadata["inventory_group"] == "nodegroup"
        and observation.metadata["input_path"] == str(inventory_path)
        and observation.metadata["input_detected_format"] == "ini"
        and observation.metadata["input_warnings"] == []
        and len(observation.metadata["input_sha256"]) == 64
        for observation in observations
    )


def test_yaml_inventory_emits_authoritative_identity_observations(tmp_path):
    inventory_path = tmp_path / "inventory.yaml"
    inventory_path.write_text(
        """all:
  hosts:
    example_host:
      ansible_host: 192.0.2.115
""",
        encoding="utf-8",
    )

    observations = AnsibleInventoryObservationSource(inventory_path).collect()

    assert _triples(observations) == {
        ("example_host", "hostname", "example_host"),
        ("example_host", "ansible_host", "192.0.2.115"),
        ("example_host", "ip_address", "192.0.2.115"),
        ("example_host", "alias", "192.0.2.115"),
        ("example_host", "group", "all"),
    }


def test_yaml_children_inventory_records_each_group_membership(tmp_path):
    inventory_path = tmp_path / "inventory.yml"
    inventory_path.write_text(
        """all:
  children:
    nodegroup:
      hosts:
        example_host:
          ansible_host: 192.0.2.115
""",
        encoding="utf-8",
    )

    observations = AnsibleInventoryObservationSource(inventory_path).collect()

    assert ("example_host", "group", "nodegroup") in _triples(observations)


def test_ini_extension_containing_yaml_uses_yaml_parser(tmp_path):
    inventory_path = tmp_path / "inventory.ini"
    inventory_path.write_text(
        """all:
  children:
    servers:
      hosts:
        example_host:
          ansible_host: 192.0.2.115
""",
        encoding="utf-8",
    )

    observations = AnsibleInventoryObservationSource(inventory_path).collect()

    assert ("example_host", "group", "servers") in _triples(observations)
    assert {
        observation.metadata["input_detected_format"] for observation in observations
    } == {"yaml"}
    assert all(
        "extension_mismatch:.ini!=yaml" in observation.metadata["input_warnings"]
        for observation in observations
    )


def test_yaml_extension_containing_ini_uses_ini_parser(tmp_path):
    inventory_path = tmp_path / "inventory.yml"
    inventory_path.write_text(
        "[servers]\nexample_host ansible_host=192.0.2.115\n", encoding="utf-8"
    )

    observations = AnsibleInventoryObservationSource(inventory_path).collect()

    assert ("example_host", "group", "servers") in _triples(observations)
    assert {
        observation.metadata["input_detected_format"] for observation in observations
    } == {"ini"}
    assert all(
        "extension_mismatch:.yml!=ini" in observation.metadata["input_warnings"]
        for observation in observations
    )


def test_unsupported_inventory_format_raises_clear_value_error(tmp_path):
    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match=r"^unsupported Ansible inventory format: json$"):
        AnsibleInventoryObservationSource(inventory_path).collect()


def test_secret_inventory_vars_are_ignored(tmp_path):
    inventory_path = tmp_path / "inventory.yaml"
    inventory_path.write_text(
        """all:
  hosts:
    example_host:
      ansible_host: 192.0.2.115
      ansible_password: do-not-ingest
      ansible_become_password: do-not-ingest
      ansible_ssh_private_key_file: /secret/key
      password: do-not-ingest
      passphrase: do-not-ingest
      token: do-not-ingest
      private_key: do-not-ingest
""",
        encoding="utf-8",
    )

    observations = AnsibleInventoryObservationSource(inventory_path).collect()

    serialized = repr([observation.model_dump() for observation in observations])
    assert "do-not-ingest" not in serialized
    assert "/secret/key" not in serialized
    assert _triples(observations) == {
        ("example_host", "hostname", "example_host"),
        ("example_host", "ansible_host", "192.0.2.115"),
        ("example_host", "ip_address", "192.0.2.115"),
        ("example_host", "alias", "192.0.2.115"),
        ("example_host", "group", "all"),
    }


def test_inventory_and_prometheus_observations_keep_endpoint_availability_scoped(tmp_path):
    inventory_path = tmp_path / "inventory.ini"
    inventory_path.write_text(
        "[nodegroup]\nexample_host ansible_host=192.0.2.115\n", encoding="utf-8"
    )
    ledger = EventLedger()
    service = ObservationCollectionService(ObservationIngestor(ledger))
    service.collect(AnsibleInventoryObservationSource(inventory_path), "ws_ansible")
    service.collect(
        FakeObservationSource(
            [
                Observation(
                    id="obs_prometheus_up",
                    source_type="provider",
                    observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    subject="192.0.2.115:9100",
                    predicate="up",
                    value=1,
                    confidence=0.95,
                    metadata={
                        "source_name": "prometheus",
                        "nodename": "example_host",
                        "instance": "192.0.2.115:9100",
                    },
                )
            ],
            name="prometheus",
        ),
        "ws_ansible",
    )

    state = StateProjector(ledger).project("ws_ansible")

    assert state.alias_resolver.canonical("192.0.2.115") == "example_host"
    assert state.alias_resolver.canonical("192.0.2.115:9100") == "192.0.2.115:9100"
    assert state.get_best_fact("example_host", "up") is None
    assert state.get_best_fact("192.0.2.115:9100", "up").value == 1
    assert any(
        fact.subject_id == "example_host"
        and fact.predicate == "prometheus_instance"
        and fact.value == "192.0.2.115:9100"
        for fact in state.facts.values()
    )
