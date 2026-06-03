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
        "[nodegroup]\nnode115 ansible_host=192.168.254.115\n", encoding="utf-8"
    )

    observations = AnsibleInventoryObservationSource(inventory_path).collect()

    assert _triples(observations) == {
        ("node115", "hostname", "node115"),
        ("node115", "ansible_host", "192.168.254.115"),
        ("node115", "ip_address", "192.168.254.115"),
        ("node115", "alias", "192.168.254.115"),
        ("node115", "group", "nodegroup"),
    }
    assert {observation.source_type for observation in observations} == {"imported"}
    assert {observation.confidence for observation in observations} == {0.95}
    assert all(
        observation.metadata
        == {
            "source_name": "ansible_inventory",
            "inventory_path": str(inventory_path),
            "inventory_group": "nodegroup",
        }
        for observation in observations
    )


def test_yaml_inventory_emits_authoritative_identity_observations(tmp_path):
    inventory_path = tmp_path / "inventory.yaml"
    inventory_path.write_text(
        """all:
  hosts:
    node115:
      ansible_host: 192.168.254.115
""",
        encoding="utf-8",
    )

    observations = AnsibleInventoryObservationSource(inventory_path).collect()

    assert _triples(observations) == {
        ("node115", "hostname", "node115"),
        ("node115", "ansible_host", "192.168.254.115"),
        ("node115", "ip_address", "192.168.254.115"),
        ("node115", "alias", "192.168.254.115"),
        ("node115", "group", "all"),
    }


def test_yaml_children_inventory_records_each_group_membership(tmp_path):
    inventory_path = tmp_path / "inventory.yml"
    inventory_path.write_text(
        """all:
  children:
    nodegroup:
      hosts:
        node115:
          ansible_host: 192.168.254.115
""",
        encoding="utf-8",
    )

    observations = AnsibleInventoryObservationSource(inventory_path).collect()

    assert ("node115", "group", "nodegroup") in _triples(observations)


def test_unsupported_inventory_format_raises_clear_value_error(tmp_path):
    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match=r"expected \.ini, \.yml, or \.yaml"):
        AnsibleInventoryObservationSource(inventory_path)


def test_inventory_and_prometheus_observations_resolve_by_inventory_hostname(tmp_path):
    inventory_path = tmp_path / "inventory.ini"
    inventory_path.write_text(
        "[nodegroup]\nnode115 ansible_host=192.168.254.115\n", encoding="utf-8"
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
                    subject="192.168.254.115:9100",
                    predicate="up",
                    value=1,
                    confidence=0.95,
                    metadata={
                        "source_name": "prometheus",
                        "nodename": "node115",
                        "instance": "192.168.254.115:9100",
                    },
                )
            ],
            name="prometheus",
        ),
        "ws_ansible",
    )

    state = StateProjector(ledger).project("ws_ansible")

    assert state.alias_resolver.canonical("192.168.254.115") == "node115"
    assert state.alias_resolver.canonical("192.168.254.115:9100") == "node115"
    assert state.get_best_fact("node115", "up").value == 1
    assert any(
        fact.subject_id == "node115"
        and fact.predicate == "prometheus_instance"
        and fact.value == "192.168.254.115:9100"
        for fact in state.facts.values()
    )
