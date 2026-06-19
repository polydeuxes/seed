import json
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.observation_sources import (
    FakeObservationSource,
    JsonObservationSource,
    ObservationCollectionService,
    RepositorySourceObservationSource,
)
from seed_runtime.observations import Observation, ObservationIngestor
from seed_runtime.state import StateProjector
from seed_runtime.state_views import build_fact_view

BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _observation(
    observation_id: str = "obs_fake",
    *,
    subject: str = "service-a",
    predicate: str = "runtime",
    value: object = "docker",
    metadata: dict[str, object] | None = None,
) -> Observation:
    return Observation(
        id=observation_id,
        source_type="provider",
        observed_at=BASE_TIME,
        subject=subject,
        predicate=predicate,
        value=value,
        confidence=0.86,
        metadata=metadata or {},
    )


def test_fake_source_emits_observations():
    observation = _observation()
    source = FakeObservationSource([observation], name="fake-provider")

    assert source.name == "fake-provider"
    assert source.source_type == "provider"
    assert source.collect() == [observation]


def test_collection_ingests_facts():
    ledger = EventLedger()
    source = FakeObservationSource([_observation()], name="fake-provider")

    facts = ObservationCollectionService(ObservationIngestor(ledger)).collect(
        source, "ws_sources"
    )
    state = StateProjector(ledger).project("ws_sources")

    assert len(facts) == 1
    assert facts[0].id in state.facts
    fact = state.facts[facts[0].id]
    assert fact.subject_id == "service-a"
    assert fact.predicate == "runtime"
    assert fact.value == "docker"


def test_repository_source_discovers_and_observes_python_files(tmp_path):
    source_file = tmp_path / "seed_runtime" / "projection_store.py"
    source_file.parent.mkdir()
    source_file.write_text(
        "from seed_runtime.state import StateProjector\n"
        "class SQLiteProjectionStore:\n"
        "    pass\n"
        "def project_state_with_cache():\n"
        "    pass\n",
        encoding="utf-8",
    )
    ignored = tmp_path / "docs" / "ignored.py"
    ignored.parent.mkdir()
    ignored.write_text("import os\n", encoding="utf-8")

    source = RepositorySourceObservationSource(tmp_path, observed_at=BASE_TIME)
    observations = source.collect()

    assert source.discover_source_files() == ["seed_runtime/projection_store.py"]
    assert {(obs.subject, obs.predicate, obs.value) for obs in observations} == {
        ("seed_runtime.projection_store", "imports", "StateProjector"),
        (
            "seed_runtime.projection_store",
            "defines",
            "seed_runtime.projection_store.SQLiteProjectionStore",
        ),
        (
            "seed_runtime.projection_store",
            "defines",
            "seed_runtime.projection_store.project_state_with_cache",
        ),
    }
    assert all(obs.source_type == "discovery" for obs in observations)
    assert all(
        obs.metadata["source_name"] == "repository_source" for obs in observations
    )
    assert all("calls" not in obs.predicate for obs in observations)


def test_repository_source_ingests_through_projection_without_grep_or_behavior(
    tmp_path,
):
    source_file = tmp_path / "seed_runtime" / "state.py"
    source_file.parent.mkdir()
    source_file.write_text(
        "from seed_runtime.projection_store import project_state_with_cache\n"
        "class StateProjector:\n"
        "    def project(self):\n"
        "        pass\n",
        encoding="utf-8",
    )
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_state.py").write_text(
        "from seed_runtime.state import StateProjector\n",
        encoding="utf-8",
    )
    ledger = EventLedger()

    facts = ObservationCollectionService(
        ObservationIngestor(ledger), normalization_pipeline=None
    ).collect(
        RepositorySourceObservationSource(tmp_path, observed_at=BASE_TIME),
        "ws_repository",
    )
    state = StateProjector(ledger).project("ws_repository")

    assert facts
    assert [
        fact.value for fact in state.get_current_facts("seed_runtime.state", "imports")
    ] == ["project_state_with_cache"]
    assert [
        fact.value for fact in state.get_current_facts("seed_runtime.state", "defines")
    ] == ["seed_runtime.state.StateProjector"]
    assert [
        fact.value for fact in state.get_current_facts("tests.test_state", "imports")
    ] == ["StateProjector"]
    assert not state.get_current_facts("seed_runtime.state", "calls")
    assert not state.get_current_facts("seed_runtime.state", "entrypoints")
    assert all(fact.predicate in {"imports", "defines"} for fact in facts)


def test_repeated_repository_observation_preserves_history_but_stabilizes_current_claims(
    tmp_path,
):
    source_file = tmp_path / "seed_runtime" / "state.py"
    source_file.parent.mkdir()
    source_file.write_text(
        "import os\n"
        "from seed_runtime.projection_store import project_state_with_cache\n"
        "class StateProjector:\n"
        "    pass\n"
        "def entrypoints():\n"
        "    pass\n",
        encoding="utf-8",
    )
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_state.py").write_text(
        "from seed_runtime.state import StateProjector\n"
        "def test_state_projector():\n"
        "    pass\n",
        encoding="utf-8",
    )
    ledger = EventLedger()
    service = ObservationCollectionService(
        ObservationIngestor(ledger), normalization_pipeline=None
    )
    source = RepositorySourceObservationSource(tmp_path, observed_at=BASE_TIME)

    first_facts = service.collect(source, "ws_repository")
    first_state = StateProjector(ledger).project("ws_repository")
    first_views = build_fact_view(first_state)
    first_durable_count = len(first_views)
    first_observation_count = len(first_state.observations)
    first_evidence_count = len(first_state.evidence)
    first_ledger_fact_count = len(first_state.facts)

    second_facts = service.collect(source, "ws_repository")
    second_state = StateProjector(ledger).project("ws_repository")
    second_views = build_fact_view(second_state)

    assert len(first_facts) == len(second_facts)
    assert len(second_views) == first_durable_count
    assert len(second_state.observations) == first_observation_count * 2
    assert len(second_state.evidence) == first_evidence_count * 2
    assert len(second_state.facts) == first_ledger_fact_count * 2

    for predicate in ("imports", "defines", "entrypoints"):
        values = [
            view.object
            for view in second_views
            if view.subject == "seed_runtime.state" and view.predicate == predicate
        ]
        assert values == sorted(set(values))

    support = next(
        support
        for support in second_state.get_fact_supports(
            "seed_runtime.state",
            "defines",
            dimensions={"path": "seed_runtime/state.py"},
        )
        if support.value == "seed_runtime.state.StateProjector"
    )
    assert len(support.supporting_fact_ids) == 2

    import_support = next(
        support
        for support in second_state.get_fact_supports(
            "seed_runtime.state",
            "imports",
            dimensions={"path": "seed_runtime/state.py"},
        )
        if support.value == "os"
    )
    assert len(import_support.supporting_fact_ids) == 2

    assert all(
        view.predicate not in {"filesystem_free_bytes", "availability_status", "up"}
        for view in second_views
    )


def test_collection_preserves_provenance():
    ledger = EventLedger()
    observation = _observation(metadata={"scanner": "dev-fixture"})
    source = FakeObservationSource([observation], name="fake-provider")

    facts = ObservationCollectionService(ObservationIngestor(ledger)).collect(
        source, "ws_sources"
    )
    state = StateProjector(ledger).project("ws_sources")

    projected_observation = state.observations[observation.id]
    projected_fact = state.facts[facts[0].id]
    evidence = state.evidence[projected_fact.evidence_ids[0]]

    assert projected_observation.source_type == "provider"
    assert projected_observation.metadata == {
        "observation_source": "fake-provider",
        "scanner": "dev-fixture",
    }
    assert projected_fact.source_type == "provider"
    assert evidence.source == "observation:provider"
    assert evidence.payload["observation_id"] == observation.id
    assert evidence.payload["source_type"] == "provider"
    assert evidence.payload["metadata"] == projected_observation.metadata


def test_bad_source_failure_does_not_partially_corrupt_state():
    class BadSource:
        name = "bad-source"
        source_type = "provider"

        def collect(self):
            yield _observation("obs_before_failure")
            raise RuntimeError("source failed")

    ledger = EventLedger()
    service = ObservationCollectionService(ObservationIngestor(ledger))

    with pytest.raises(RuntimeError, match="source failed"):
        service.collect(BadSource(), "ws_sources")

    state = StateProjector(ledger).project("ws_sources")
    assert state.observations == {}
    assert state.evidence == {}
    assert state.facts == {}
    assert ledger.list_events("ws_sources") == []


def test_json_source_valid_file_ingests_observations(tmp_path):
    json_path = tmp_path / "observations.json"
    json_path.write_text(
        """
        {
          "observations": [
            {
              "id": "obs_json_fixture",
              "subject": "web_service",
              "predicate": "runtime",
              "value": "docker",
              "confidence": 0.95,
              "observed_at": "2026-01-01T00:00:00+00:00"
            }
          ]
        }
        """,
        encoding="utf-8",
    )
    ledger = EventLedger()
    source = JsonObservationSource(json_path)

    facts = ObservationCollectionService(ObservationIngestor(ledger)).collect(
        source, "ws_json"
    )
    state = StateProjector(ledger).project("ws_json")

    assert source.source_type == "imported"
    assert len(facts) == 1
    fact = facts[0]
    assert fact.id in state.facts
    assert fact.subject_id == "web_service"
    assert fact.predicate == "runtime"
    assert fact.value == "docker"
    assert fact.source_type == "imported"
    assert fact.confidence == 0.95


def test_json_source_malformed_file_fails_without_partial_ingest(tmp_path):
    json_path = tmp_path / "observations.json"
    json_path.write_text(
        """
        {
          "observations": [
            {
              "id": "obs_valid_before_bad",
              "subject": "web_service",
              "predicate": "runtime",
              "value": "docker"
            },
            {
              "id": "obs_bad_missing_predicate",
              "subject": "plex",
              "value": "systemd"
            }
          ]
        }
        """,
        encoding="utf-8",
    )
    ledger = EventLedger()

    with pytest.raises(ValueError, match="observations\\[1\\] missing"):
        ObservationCollectionService(ObservationIngestor(ledger)).collect(
            JsonObservationSource(json_path), "ws_json"
        )

    state = StateProjector(ledger).project("ws_json")
    assert state.observations == {}
    assert state.evidence == {}
    assert state.facts == {}
    assert ledger.list_events("ws_json") == []


def test_json_source_provenance_and_source_metadata_preserved(tmp_path):
    json_path = tmp_path / "observations.json"
    json_path.write_text(
        """
        {
          "observations": [
            {
              "id": "obs_json_provenance",
              "subject": "web_service",
              "predicate": "runtime",
              "value": "docker",
              "metadata": {"scanner": "inventory-export"}
            }
          ]
        }
        """,
        encoding="utf-8",
    )
    ledger = EventLedger()

    facts = ObservationCollectionService(ObservationIngestor(ledger)).collect(
        JsonObservationSource(json_path, name="json-inventory"), "ws_json"
    )
    state = StateProjector(ledger).project("ws_json")

    projected_observation = state.observations["obs_json_provenance"]
    projected_fact = state.facts[facts[0].id]
    evidence = state.evidence[projected_fact.evidence_ids[0]]

    assert projected_observation.source_type == "imported"
    assert projected_observation.metadata == {
        "scanner": "inventory-export",
        "json_path": str(json_path),
        "observation_source": "json-inventory",
    }
    assert projected_fact.source_type == "imported"
    assert evidence.source == "observation:imported"
    assert evidence.payload["observation_id"] == "obs_json_provenance"
    assert evidence.payload["source_type"] == "imported"
    assert evidence.payload["metadata"] == projected_observation.metadata


def test_export_observations_json_round_trip_preserves_facts_and_support(tmp_path):
    ledger = EventLedger()
    first = _observation(
        "obs_roundtrip_provider",
        subject="web_service",
        predicate="runtime",
        value="docker",
    )
    second = Observation(
        id="obs_roundtrip_discovery",
        source_type="discovery",
        observed_at=BASE_TIME,
        subject="web_service",
        predicate="runtime",
        value="docker",
        confidence=0.74,
    )
    ingestor = ObservationIngestor(ledger)
    ingestor.ingest(first, "ws_export")
    ingestor.ingest(second, "ws_export")
    state = StateProjector(ledger).project("ws_export")

    from seed_runtime.observation_sources import export_observations_json

    payload = export_observations_json(state)
    export_path = tmp_path / "exported-observations.json"
    export_path.write_text(json.dumps(payload), encoding="utf-8")

    imported_ledger = EventLedger()
    ObservationCollectionService(ObservationIngestor(imported_ledger)).collect(
        JsonObservationSource(export_path), "ws_imported"
    )
    imported_state = StateProjector(imported_ledger).project("ws_imported")

    support = imported_state.get_fact_support("web_service", "runtime")
    assert support is not None
    assert support.value == "docker"
    assert len(support.supporting_fact_ids) == 2
    assert support.source_types == ["provider", "discovery"]
    assert sorted(
        (fact.subject_id, fact.predicate, fact.value, fact.source_type, fact.confidence)
        for fact in imported_state.observed_facts.values()
    ) == [
        ("web_service", "runtime", "docker", "discovery", 0.74),
        ("web_service", "runtime", "docker", "provider", 0.86),
    ]


def test_export_observations_json_includes_expired_fact_expires_at():
    ledger = EventLedger()
    expired_at = datetime(2025, 1, 1, tzinfo=timezone.utc)
    observation = Observation(
        id="obs_expired_export",
        source_type="provider",
        observed_at=BASE_TIME,
        subject="web_service",
        predicate="runtime",
        value="docker",
        confidence=0.86,
        expires_at=expired_at,
    )
    ObservationIngestor(ledger).ingest(observation, "ws_export_expired")
    state = StateProjector(ledger).project("ws_export_expired")

    from seed_runtime.observation_sources import export_observations_json

    payload = export_observations_json(state)

    assert payload["observations"][0]["expires_at"] == expired_at.isoformat()


def test_export_observations_json_excludes_inferred_facts_by_default(tmp_path):
    ledger = EventLedger()
    ObservationIngestor(ledger).ingest(
        _observation(
            "obs_runtime_for_inference",
            subject="web_service",
            predicate="runtime",
            value="docker",
        ),
        "ws_export_inferred",
    )
    state = StateProjector(ledger).project("ws_export_inferred")

    from seed_runtime.observation_sources import export_observations_json

    default_payload = export_observations_json(state)
    with_inferred_payload = export_observations_json(state, include_inferred=True)

    assert [entry["predicate"] for entry in default_payload["observations"]] == [
        "runtime"
    ]
    assert [entry["predicate"] for entry in with_inferred_payload["observations"]] == [
        "runtime",
        "managed_by",
    ]
    assert with_inferred_payload["observations"][1]["source_type"] == "inferred"

    export_path = tmp_path / "exported-with-inferred.json"
    export_path.write_text(json.dumps(with_inferred_payload), encoding="utf-8")
    imported_ledger = EventLedger()
    ObservationCollectionService(ObservationIngestor(imported_ledger)).collect(
        JsonObservationSource(export_path), "ws_imported_inferred"
    )
    imported_state = StateProjector(imported_ledger).project("ws_imported_inferred")

    assert "fact_inferred_web_service_managed_by_docker_container_lifecycle" in (
        imported_state.inferred_facts
    )


def test_diff_observations_json_matching_inventory_reports_matching():
    ledger = EventLedger()
    observation = _observation("obs_existing")
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource([observation], name="fake-provider"), "ws_diff"
    )
    state = StateProjector(ledger).project("ws_diff")

    from seed_runtime.observation_sources import (
        diff_observations_json,
        export_observations_json,
    )

    diff = diff_observations_json(state, export_observations_json(state))

    assert len(diff.matching_facts) == 1
    assert diff.matching_facts[0].observation["subject"] == "service-a"
    assert diff.new_facts == []
    assert diff.changed_facts == []
    assert diff.expired_incoming == []
    assert diff.conflicts_introduced == []


def test_diff_observations_json_new_observation_reports_new_facts():
    state = StateProjector(EventLedger()).project("ws_diff")

    from seed_runtime.observation_sources import diff_observations_json

    diff = diff_observations_json(
        state,
        {
            "observations": [
                {
                    "subject": "new-service",
                    "predicate": "runtime",
                    "value": "docker",
                }
            ]
        },
    )

    assert len(diff.new_facts) == 1
    assert diff.new_facts[0].observation["subject"] == "new-service"
    assert diff.matching_facts == []
    assert diff.conflicts_introduced == []


def test_diff_observations_json_conflicting_value_reports_conflicts_introduced():
    ledger = EventLedger()
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource([_observation("obs_existing", value="docker")]),
        "ws_diff",
    )
    state = StateProjector(ledger).project("ws_diff")

    from seed_runtime.observation_sources import diff_observations_json

    diff = diff_observations_json(
        state,
        {
            "observations": [
                {
                    "subject": "service-a",
                    "predicate": "runtime",
                    "value": "systemd",
                }
            ]
        },
    )

    assert len(diff.changed_facts) == 1
    assert len(diff.conflicts_introduced) == 1
    conflict = diff.conflicts_introduced[0]
    assert conflict.subject == "service-a"
    assert conflict.predicate == "runtime"
    assert conflict.values == ["docker", "systemd"]


def test_diff_observations_json_expired_incoming_reported_separately():
    state = StateProjector(EventLedger()).project("ws_diff")

    from seed_runtime.observation_sources import diff_observations_json

    diff = diff_observations_json(
        state,
        {
            "observations": [
                {
                    "subject": "old-service",
                    "predicate": "runtime",
                    "value": "docker",
                    "expires_at": "2000-01-01T00:00:00+00:00",
                }
            ]
        },
    )

    assert len(diff.expired_incoming) == 1
    assert diff.expired_incoming[0].observation["subject"] == "old-service"
    assert diff.new_facts == []
    assert diff.matching_facts == []
    assert diff.changed_facts == []
    assert diff.conflicts_introduced == []


def test_diff_observations_json_does_not_append_events():
    ledger = EventLedger()
    state = StateProjector(ledger).project("ws_diff")

    from seed_runtime.observation_sources import diff_observations_json

    diff_observations_json(
        state,
        {
            "observations": [
                {
                    "subject": "new-service",
                    "predicate": "runtime",
                    "value": "docker",
                }
            ]
        },
    )

    assert ledger.list_events("ws_diff") == []
    assert state.facts == {}


def test_local_host_source_emits_read_only_host_observations(monkeypatch):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.os, "cpu_count", lambda: 4)
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_storage_observations",
        lambda self, observed_at, hostname, metadata: [],
    )
    missing = Path("/definitely/missing/seed-local-identity")

    observations = LocalHostObservationSource(
        proc_root=missing,
        etc_hostname=missing,
        machine_id=missing,
        etc_hosts=missing,
        etc_passwd=missing,
        etc_group=missing,
        dpkg_status=missing,
    ).collect()

    assert [(obs.subject, obs.predicate, obs.value) for obs in observations] == [
        ("node-a", "local_observation_status", "observed"),
        ("node-a", "os", "linux"),
        ("node-a", "architecture", "x86_64"),
        ("node-a", "disk_total_bytes", 1000),
        ("node-a", "disk_free_bytes", 250),
        ("node-a", "cpu_count", 4),
    ]
    assert {obs.source_type for obs in observations} == {"discovery"}
    assert all(obs.metadata["shell_execution"] is False for obs in observations)
    local_status = observations[0]
    assert local_status.metadata["network_reachability_asserted"] is False
    assert local_status.metadata["provider_visibility_asserted"] is False
    assert local_status.metadata["availability_asserted"] is False


def test_local_host_source_emits_hosts_file_mapping_observations(tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    hosts = tmp_path / "hosts"
    hosts.write_text(
        "\n"
        "# comment-only line\n"
        "127.0.0.1 localhost localhost.localdomain # inline comment\n"
        "2001:db8::10 node-v6 node-v6-alias\n"
        "# another comment\n",
        encoding="utf-8",
    )

    observations = LocalHostObservationSource(
        etc_hosts=hosts
    )._collect_hosts_file_observations(
        BASE_TIME, "node-a", {"collector": "LocalHostObservationSource"}
    )

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert ("node-a", "hosts_file_address_mapping", "127.0.0.1") in triples
    assert ("node-a", "hosts_file_name", "localhost") in triples
    assert ("node-a", "hosts_file_alias", "localhost.localdomain") in triples
    assert ("node-a", "hosts_file_address_mapping", "2001:db8::10") in triples
    assert ("node-a", "hosts_file_name", "node-v6") in triples
    assert ("node-a", "hosts_file_alias", "node-v6-alias") in triples
    assert len(observations) == 6

    ipv4_alias = next(
        obs for obs in observations if obs.value == "localhost.localdomain"
    )
    assert ipv4_alias.dimensions == {
        "source": "/etc/hosts",
        "line_number": "3",
        "address": "127.0.0.1",
        "canonical_name": "localhost",
        "name_index": "1",
        "name_role": "alias",
    }

    ipv6_mapping = next(
        obs
        for obs in observations
        if obs.predicate == "hosts_file_address_mapping" and obs.value == "2001:db8::10"
    )
    assert ipv6_mapping.dimensions["line_number"] == "4"
    assert ipv6_mapping.dimensions["canonical_name"] == "node-v6"
    assert ipv6_mapping.dimensions["names"] == "node-v6 node-v6-alias"


def test_local_host_hosts_file_metadata_preserves_observation_boundaries(tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    hosts = tmp_path / "hosts"
    hosts.write_text("192.0.2.10 node-a node-a-alias\n", encoding="utf-8")

    observations = LocalHostObservationSource(
        etc_hosts=hosts
    )._collect_hosts_file_observations(
        BASE_TIME, "observer-node", {"collector": "LocalHostObservationSource"}
    )

    assert observations
    for obs in observations:
        assert obs.metadata["source"] == "/etc/hosts"
        assert obs.metadata["source_path"] == str(hosts)
        assert obs.metadata["question_answered"] == (
            "What local hosts-file name/address mappings are configured?"
        )
        assert obs.metadata["dns_validity_asserted"] is False
        assert obs.metadata["dns_resolution_asserted"] is False
        assert obs.metadata["network_reachability_asserted"] is False
        assert obs.metadata["availability_asserted"] is False
        assert obs.metadata["host_ownership_asserted"] is False
        assert obs.metadata["host_uniqueness_asserted"] is False
        assert obs.metadata["alias_equivalence_asserted"] is False
        assert obs.metadata["endpoint_identity_asserted"] is False
        assert obs.metadata["host_identity_asserted"] is False

    emitted_predicates = {obs.predicate for obs in observations}
    assert "alias" not in emitted_predicates
    assert "hostname" not in emitted_predicates
    assert "fqdn" not in emitted_predicates


def test_local_host_hosts_file_oversized_input_is_skipped(tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    hosts = tmp_path / "hosts"
    hosts.write_text("x" * (1024 * 1024 + 1), encoding="utf-8")
    source = LocalHostObservationSource(etc_hosts=hosts)

    assert (
        source._collect_hosts_file_observations(
            BASE_TIME, "node-a", {"collector": "LocalHostObservationSource"}
        )
        == []
    )


def test_local_host_observation_fact_does_not_assert_availability_or_network(
    monkeypatch,
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observations import ObservationIngestor
    from seed_runtime.observation_sources import (
        LocalHostObservationSource,
        ObservationCollectionService,
    )
    from seed_runtime.state import StateProjector

    class DiskUsage:
        total = 1000
        free = 250

    def fail_network(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError("local host observation must not make network calls")

    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(sources, "urlopen", fail_network)
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    ledger = EventLedger()
    facts = ObservationCollectionService(ObservationIngestor(ledger)).collect(
        LocalHostObservationSource(), "ws_local_observable"
    )
    state = StateProjector(ledger).project("ws_local_observable")

    assert ("local_observation_status", "observed") in {
        (fact.predicate, fact.value) for fact in facts
    }
    assert state.get_best_fact("node-a", "local_observation_status").value == "observed"
    assert state.get_best_fact("node-a", "availability_status") is None


def _write_local_network_fixture(tmp_path):
    proc = tmp_path / "proc"
    sys_net = tmp_path / "sys" / "class" / "net"
    resolv_conf = tmp_path / "resolv.conf"
    (proc / "net").mkdir(parents=True)
    (sys_net / "eth0").mkdir(parents=True)
    (sys_net / "lo").mkdir(parents=True)
    (proc / "net" / "dev").write_text(
        "Inter-| Receive\n face |bytes\n"
        "  lo: 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0\n"
        "eth0: 2 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0\n",
        encoding="utf-8",
    )
    (proc / "net" / "route").write_text(
        "Iface\tDestination\tGateway\tFlags\tRefCnt\tUse\tMetric\t"
        "Mask\tMTU\tWindow\tIRTT\n"
        "eth0\t00000000\t0102A8C0\t0003\t0\t0\t100\t"
        "00000000\t0\t0\t0\n",
        encoding="utf-8",
    )
    (proc / "net" / "if_inet6").write_text(
        "00000000000000000000000000000001 01 80 10 80 lo\n"
        "20010db8000000000000000000000005 02 40 00 80 eth0\n",
        encoding="utf-8",
    )
    for interface, operstate, address, mtu in [
        ("eth0", "up", "aa:bb:cc:dd:ee:ff", "1500"),
        ("lo", "unknown", "00:00:00:00:00:00", "65536"),
    ]:
        (sys_net / interface / "operstate").write_text(
            operstate + "\n", encoding="utf-8"
        )
        (sys_net / interface / "address").write_text(address + "\n", encoding="utf-8")
        (sys_net / interface / "mtu").write_text(mtu + "\n", encoding="utf-8")
        (sys_net / interface / "ifindex").write_text(
            ("2" if interface == "eth0" else "1") + "\n", encoding="utf-8"
        )
    resolv_conf.write_text(
        "# local resolver configuration\n"
        "nameserver 1.1.1.1\n"
        "nameserver 2001:4860:4860::8888\n",
        encoding="utf-8",
    )
    return proc, sys_net, resolv_conf


def test_local_host_source_emits_local_network_configuration(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc, sys_net, resolv_conf = _write_local_network_fixture(tmp_path)
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        sources.socket, "if_nameindex", lambda: [(1, "lo"), (2, "eth0")]
    )
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_ipv4_address_for_interface",
        lambda self, interface: {
            "eth0": "192.168.2.5",
            "lo": "127.0.0.1",
        }.get(interface),
    )

    observations = LocalHostObservationSource(
        proc_root=proc, sys_class_net=sys_net, resolv_conf=resolv_conf
    ).collect()

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert ("node-a", "network_interface", "eth0") in triples
    assert ("node-a", "interface_operstate", "up") in triples
    assert ("node-a", "interface_mac_address", "aa:bb:cc:dd:ee:ff") in triples
    assert ("node-a", "interface_mtu", 1500) in triples
    assert ("node-a", "ip_address", "192.168.2.5") in triples
    assert ("node-a", "ip_address", "2001:db8::5") in triples
    assert ("node-a", "default_gateway", "192.168.2.1") in triples
    assert ("node-a", "interface_role", "primary") in triples
    assert ("node-a", "interface_role", "loopback") in triples
    assert ("node-a", "dns_resolver", "1.1.1.1") in triples
    assert ("node-a", "dns_resolver", "2001:4860:4860::8888") in triples
    eth0_ip = next(
        obs
        for obs in observations
        if obs.predicate == "ip_address" and obs.value == "192.168.2.5"
    )
    assert eth0_ip.dimensions == {"interface": "eth0", "address_family": "ipv4"}
    assert eth0_ip.metadata["local_only"] is True
    assert eth0_ip.metadata["network_probe"] is False
    assert eth0_ip.metadata["network_connection"] is False
    assert eth0_ip.metadata["subprocess_execution"] is False
    assert eth0_ip.metadata["privilege_escalation"] is False


def test_local_host_source_distinguishes_systemd_resolved_stub_and_upstream(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc, sys_net, resolv_conf = _write_local_network_fixture(tmp_path)
    resolv_conf.write_text("nameserver 127.0.0.53\n", encoding="utf-8")
    systemd_resolv = tmp_path / "run" / "systemd" / "resolve" / "resolv.conf"
    systemd_resolv.parent.mkdir(parents=True)
    systemd_resolv.write_text(
        "nameserver 1.1.1.1\nnameserver 2001:4860:4860::8888\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        sources.socket, "if_nameindex", lambda: [(1, "lo"), (2, "eth0")]
    )
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_ipv4_address_for_interface",
        lambda self, interface: None,
    )

    observations = LocalHostObservationSource(
        proc_root=proc,
        sys_class_net=sys_net,
        resolv_conf=resolv_conf,
        systemd_resolv_conf=systemd_resolv,
    ).collect()

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert ("node-a", "dns_resolver", "127.0.0.53") in triples
    assert ("node-a", "dns_resolver_stub", "127.0.0.53") in triples
    assert ("node-a", "dns_resolver_upstream", "1.1.1.1") in triples
    assert ("node-a", "dns_resolver_upstream", "2001:4860:4860::8888") in triples
    for obs in observations:
        if obs.predicate in {"dns_resolver_stub", "dns_resolver_upstream"}:
            assert obs.metadata["network_probe"] is False
            assert obs.metadata["network_connection"] is False
            assert obs.metadata["subprocess_execution"] is False
            assert obs.metadata["dns_resolution_asserted"] is False


def test_local_host_source_stub_only_has_no_upstream_fact(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc, sys_net, resolv_conf = _write_local_network_fixture(tmp_path)
    resolv_conf.write_text("nameserver 127.0.0.53\n", encoding="utf-8")
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        sources.socket, "if_nameindex", lambda: [(1, "lo"), (2, "eth0")]
    )
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_ipv4_address_for_interface",
        lambda self, interface: None,
    )

    observations = LocalHostObservationSource(
        proc_root=proc,
        sys_class_net=sys_net,
        resolv_conf=resolv_conf,
        systemd_resolv_conf=tmp_path / "missing-resolv.conf",
    ).collect()

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert ("node-a", "dns_resolver_stub", "127.0.0.53") in triples
    assert not [obs for obs in observations if obs.predicate == "dns_resolver_upstream"]


def test_local_host_source_keeps_container_interfaces_as_facts(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc, sys_net, resolv_conf = _write_local_network_fixture(tmp_path)
    for interface in ("docker0", "vethabc123"):
        (sys_net / interface).mkdir(parents=True)
        (sys_net / interface / "operstate").write_text("up\n", encoding="utf-8")
        (sys_net / interface / "address").write_text(
            "02:42:ac:11:00:02\n", encoding="utf-8"
        )
        (sys_net / interface / "mtu").write_text("1500\n", encoding="utf-8")
        (sys_net / interface / "ifindex").write_text("10\n", encoding="utf-8")
    (proc / "net" / "dev").write_text(
        "Inter-| Receive\n face |bytes\n"
        "  lo: 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0\n"
        "eth0: 2 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0\n"
        "docker0: 3 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0\n"
        "vethabc123: 4 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        sources.socket,
        "if_nameindex",
        lambda: [(1, "lo"), (2, "eth0"), (3, "docker0"), (4, "vethabc123")],
    )
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_ipv4_address_for_interface",
        lambda self, interface: {
            "eth0": "192.168.2.5",
            "lo": "127.0.0.1",
            "docker0": "172.17.0.1",
            "vethabc123": "169.254.1.10",
        }.get(interface),
    )

    observations = LocalHostObservationSource(
        proc_root=proc, sys_class_net=sys_net, resolv_conf=resolv_conf
    ).collect()

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert ("node-a", "network_interface", "docker0") in triples
    assert ("node-a", "network_interface", "vethabc123") in triples
    assert ("node-a", "ip_address", "172.17.0.1") in triples
    assert ("node-a", "ip_address", "169.254.1.10") in triples
    assert [
        obs.value
        for obs in observations
        if obs.predicate == "interface_role"
        and obs.dimensions.get("interface") in {"docker0", "vethabc123"}
    ] == ["container", "container"]


def test_local_host_source_emits_dhcp_only_with_explicit_lease_evidence(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc, sys_net, resolv_conf = _write_local_network_fixture(tmp_path)
    lease_dir = tmp_path / "run" / "systemd" / "netif" / "leases"
    lease_dir.mkdir(parents=True)
    (lease_dir / "2").write_text(
        "# systemd-networkd lease\nADDRESS=192.168.2.5\nROUTER=192.168.2.1\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(sources.socket, "if_nameindex", lambda: [(2, "eth0")])
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_ipv4_address_for_interface",
        lambda self, interface: "192.168.2.5",
    )

    observations = LocalHostObservationSource(
        proc_root=proc,
        sys_class_net=sys_net,
        resolv_conf=resolv_conf,
        systemd_lease_dir=lease_dir,
    ).collect()

    assignment = next(
        obs for obs in observations if obs.predicate == "address_assignment_method"
    )
    assert assignment.value == "dhcp"
    assert assignment.dimensions == {"interface": "eth0", "address_family": "ipv4"}
    assert assignment.metadata["source"] == "systemd_netif_lease"


def test_local_network_configuration_projects_without_availability(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observations import ObservationIngestor
    from seed_runtime.observation_sources import (
        LocalHostObservationSource,
        ObservationCollectionService,
    )
    from seed_runtime.state import StateProjector

    class DiskUsage:
        total = 1000
        free = 250

    proc, sys_net, resolv_conf = _write_local_network_fixture(tmp_path)
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(sources.socket, "if_nameindex", lambda: [(2, "eth0")])
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_ipv4_address_for_interface",
        lambda self, interface: "192.168.2.5",
    )

    ledger = EventLedger()
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        LocalHostObservationSource(
            proc_root=proc, sys_class_net=sys_net, resolv_conf=resolv_conf
        ),
        "ws_local_network",
    )
    state = StateProjector(ledger).project("ws_local_network")

    assert state.get_current_facts("node-a", "network_interface")
    assert state.get_current_facts("node-a", "ip_address")
    assert state.get_current_facts("node-a", "default_gateway")
    assert state.get_current_facts("node-a", "dns_resolver")
    assert state.get_best_fact("node-a", "availability_status") is None


def test_local_network_observation_is_deterministic(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc, sys_net, resolv_conf = _write_local_network_fixture(tmp_path)
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        sources.socket, "if_nameindex", lambda: [(2, "eth0"), (1, "lo")]
    )
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_ipv4_address_for_interface",
        lambda self, interface: {
            "eth0": "192.168.2.5",
            "lo": "127.0.0.1",
        }.get(interface),
    )

    source = LocalHostObservationSource(
        proc_root=proc, sys_class_net=sys_net, resolv_conf=resolv_conf
    )
    first = [
        (obs.subject, obs.predicate, obs.value, obs.dimensions)
        for obs in source.collect()
    ]
    second = [
        (obs.subject, obs.predicate, obs.value, obs.dimensions)
        for obs in source.collect()
    ]

    assert first == second


def test_local_network_observation_does_not_probe_or_escalate(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    def fail_forbidden(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError(
            "local network observation must not probe, execute, or escalate"
        )

    proc, sys_net, resolv_conf = _write_local_network_fixture(tmp_path)
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(sources.socket, "if_nameindex", lambda: [(2, "eth0")])
    monkeypatch.setattr(sources.socket, "create_connection", fail_forbidden)
    monkeypatch.setattr(sources.socket, "getaddrinfo", fail_forbidden)
    monkeypatch.setattr(sources.socket, "gethostbyname", fail_forbidden)
    monkeypatch.setattr(sources, "urlopen", fail_forbidden)
    monkeypatch.setattr(os, "system", fail_forbidden)
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_ipv4_address_for_interface",
        lambda self, interface: "192.168.2.5",
    )

    observations = LocalHostObservationSource(
        proc_root=proc, sys_class_net=sys_net, resolv_conf=resolv_conf
    ).collect()

    assert observations
    assert all(obs.metadata["local_only"] is True for obs in observations)
    assert all(obs.metadata["shell_execution"] is False for obs in observations)
    assert all(obs.metadata["subprocess_execution"] is False for obs in observations)
    assert all(obs.metadata["privilege_escalation"] is False for obs in observations)
    assert all(obs.metadata["network_probe"] is False for obs in observations)


def _write_host_description_fixture(proc: Path) -> Path:
    (proc / "sys" / "kernel").mkdir(parents=True, exist_ok=True)
    (proc / "sys" / "kernel" / "osrelease").write_text(
        "6.8.0-seed-test\n", encoding="utf-8"
    )
    (proc / "version").write_text(
        "Linux version 6.8.0-seed-test (builder@seed) #1 SMP PREEMPT_DYNAMIC\n",
        encoding="utf-8",
    )
    (proc / "cpuinfo").write_text(
        "processor\t: 0\n"
        "model name\t: Seed Test CPU 9000\n"
        "\n"
        "processor\t: 1\n"
        "model name\t: Seed Test CPU 9000\n",
        encoding="utf-8",
    )
    (proc / "meminfo").write_text("MemTotal:       16384 kB\n", encoding="utf-8")
    return proc


def test_local_host_read_text_reads_no_more_than_configured_bound():
    import stat

    from seed_runtime.observation_sources import LocalHostObservationSource

    class FakeStat:
        st_mode = stat.S_IFCHR
        st_size = 0

    class FakeHandle:
        def __init__(self) -> None:
            self.read_sizes: list[int] = []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self, size: int) -> bytes:
            self.read_sizes.append(size)
            return b"bounded"

    class FakePath:
        def __init__(self) -> None:
            self.handle = FakeHandle()

        def stat(self) -> FakeStat:
            return FakeStat()

        def open(self, mode: str):
            assert mode == "rb"
            return self.handle

    path = FakePath()

    assert LocalHostObservationSource()._read_text(path, max_bytes=8) == "bounded"
    assert path.handle.read_sizes == [8]


def test_local_host_read_text_skips_oversized_regular_file(tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    oversized = tmp_path / "oversized-proc-file"
    oversized.write_text("x" * 17, encoding="utf-8")

    assert LocalHostObservationSource()._read_text(oversized, max_bytes=16) is None


def test_local_host_source_emits_kernel_cpu_memory_observations(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc = _write_host_description_fixture(tmp_path / "proc")
    missing = tmp_path / "missing"
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.os, "cpu_count", lambda: 99)
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    observations = LocalHostObservationSource(
        proc_root=proc, sys_class_net=missing, resolv_conf=missing
    ).collect()

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert ("node-a", "kernel_release", "6.8.0-seed-test") in triples
    assert (
        "node-a",
        "kernel_version",
        "Linux version 6.8.0-seed-test (builder@seed) #1 SMP PREEMPT_DYNAMIC",
    ) in triples
    assert ("node-a", "cpu_model", "Seed Test CPU 9000") in triples
    assert ("node-a", "cpu_count", 2) in triples
    assert ("node-a", "memory_total_bytes", 16_777_216) in triples
    assert not [
        obs for obs in observations if obs.predicate == "memory_available_bytes"
    ]

    cpu_count = next(obs for obs in observations if obs.predicate == "cpu_count")
    assert cpu_count.metadata["source"] == "/proc/cpuinfo"
    assert (
        cpu_count.metadata["question_answered"] == "How many CPUs are visible locally?"
    )
    assert cpu_count.metadata["local_only"] is True
    assert cpu_count.metadata["shell_execution"] is False
    assert cpu_count.metadata["subprocess_execution"] is False
    assert cpu_count.metadata["privilege_escalation"] is False
    assert cpu_count.metadata["network_probe"] is False
    assert cpu_count.metadata["network_connection"] is False
    assert cpu_count.metadata["availability_asserted"] is False
    assert cpu_count.metadata["health_asserted"] is False
    assert cpu_count.metadata["performance_adequacy_asserted"] is False
    assert cpu_count.metadata["memory_pressure_asserted"] is False
    assert cpu_count.metadata["supportability_asserted"] is False


def test_kernel_cpu_memory_observation_skips_oversized_procfs_without_crashing(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc = tmp_path / "proc"
    (proc / "sys" / "kernel").mkdir(parents=True, exist_ok=True)
    (proc / "sys" / "kernel" / "osrelease").write_text(
        "6.8.0-seed-test\n", encoding="utf-8"
    )
    (proc / "version").write_text("Linux version 6.8.0-seed-test\n", encoding="utf-8")
    (proc / "cpuinfo").write_text(
        "processor\t: 0\nmodel name\t: Misleading Partial CPU\n"
        + ("padding\n" * 140_000),
        encoding="utf-8",
    )
    (proc / "meminfo").write_text(
        "MemTotal:       999999 kB\n" + ("padding\n" * 140_000),
        encoding="utf-8",
    )
    missing = tmp_path / "missing"
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.os, "cpu_count", lambda: 8)
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    observations = LocalHostObservationSource(
        proc_root=proc, sys_class_net=missing, resolv_conf=missing
    ).collect()

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert ("node-a", "kernel_release", "6.8.0-seed-test") in triples
    assert ("node-a", "cpu_model", "Misleading Partial CPU") not in triples
    assert ("node-a", "memory_total_bytes", 1_023_998_976) not in triples
    assert ("node-a", "cpu_count", 8) in triples


def test_kernel_cpu_memory_observation_skips_truncated_oversized_partial_input(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc = tmp_path / "proc"
    proc.mkdir(parents=True, exist_ok=True)
    (proc / "cpuinfo").write_text(
        "model name\t: Truncated CPU Without Complete Bounded Evidence"
        + ("x" * (1024 * 1024 + 1)),
        encoding="utf-8",
    )
    (proc / "meminfo").write_text(
        "MemTotal:       424242 kB" + ("x" * (1024 * 1024 + 1)),
        encoding="utf-8",
    )
    missing = tmp_path / "missing"
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.os, "cpu_count", lambda: None)
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    observations = LocalHostObservationSource(
        proc_root=proc, sys_class_net=missing, resolv_conf=missing
    ).collect()

    predicates = {obs.predicate for obs in observations}
    assert "cpu_model" not in predicates
    assert "cpu_count" not in predicates
    assert "memory_total_bytes" not in predicates


def test_kernel_cpu_memory_observation_projects_only_direct_facts(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observations import ObservationIngestor
    from seed_runtime.observation_sources import (
        LocalHostObservationSource,
        ObservationCollectionService,
    )
    from seed_runtime.state import StateProjector

    class DiskUsage:
        total = 1000
        free = 250

    proc = _write_host_description_fixture(tmp_path / "proc")
    missing = tmp_path / "missing"
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    ledger = EventLedger()
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        LocalHostObservationSource(
            proc_root=proc, sys_class_net=missing, resolv_conf=missing
        ),
        "ws_host_description",
    )
    state = StateProjector(ledger).project("ws_host_description")

    assert state.get_best_fact("node-a", "kernel_release").value == "6.8.0-seed-test"
    assert state.get_best_fact("node-a", "cpu_model").value == "Seed Test CPU 9000"
    assert state.get_best_fact("node-a", "cpu_count").value == 2
    assert state.get_best_fact("node-a", "memory_total_bytes").value == 16_777_216
    assert state.get_best_fact("node-a", "memory_available_bytes") is None
    assert state.get_best_fact("node-a", "availability_status") is None
    assert state.get_best_fact("node-a", "health_status") is None
    assert state.get_best_fact("node-a", "reachability_status") is None


def test_kernel_cpu_memory_observation_avoids_execution_root_network_and_providers(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    def fail_forbidden(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError(
            "kernel/cpu/memory observation must not execute, escalate, network, or call providers"
        )

    proc = _write_host_description_fixture(tmp_path / "proc")
    missing = tmp_path / "missing"
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(sources.socket, "create_connection", fail_forbidden)
    monkeypatch.setattr(sources.socket, "getaddrinfo", fail_forbidden)
    monkeypatch.setattr(sources.socket, "gethostbyname", fail_forbidden)
    monkeypatch.setattr(sources, "urlopen", fail_forbidden)
    monkeypatch.setattr(os, "system", fail_forbidden)
    monkeypatch.setattr(subprocess, "Popen", fail_forbidden)
    monkeypatch.setattr(subprocess, "run", fail_forbidden)
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    observations = LocalHostObservationSource(
        proc_root=proc, sys_class_net=missing, resolv_conf=missing
    ).collect()
    host_description = [
        obs
        for obs in observations
        if obs.predicate
        in {
            "kernel_release",
            "kernel_version",
            "cpu_model",
            "cpu_count",
            "memory_total_bytes",
        }
    ]

    assert host_description
    assert all(obs.source_type == "discovery" for obs in host_description)
    assert all(obs.metadata["local_only"] is True for obs in host_description)
    assert all(obs.metadata["shell_execution"] is False for obs in host_description)
    assert all(
        obs.metadata["subprocess_execution"] is False for obs in host_description
    )
    assert all(
        obs.metadata["privilege_escalation"] is False for obs in host_description
    )
    assert all(obs.metadata["network_probe"] is False for obs in host_description)
    assert all(obs.metadata["network_connection"] is False for obs in host_description)


def _write_listener_fixture(proc: Path) -> Path:
    net = proc / "net"
    net.mkdir(parents=True, exist_ok=True)
    (net / "tcp").write_text(
        "  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode\n"
        "   0: 00000000:0016 00000000:0000 0A 00000000:00000000 00:00000000 00000000 0 0 1\n"
        "   1: 0100007F:2386 00000000:0000 0A 00000000:00000000 00:00000000 00000000 0 0 2\n"
        "   2: 0100007F:0050 00000000:0000 01 00000000:00000000 00:00000000 00000000 0 0 3\n",
        encoding="utf-8",
    )
    (net / "udp").write_text(
        "  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode\n"
        "   0: 00000000:0035 00000000:0000 07 00000000:00000000 00:00000000 00000000 0 0 4\n",
        encoding="utf-8",
    )
    (net / "tcp6").write_text(
        "  sl  local_address                         remote_address                        st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode\n"
        "   0: 00000000000000000000000000000000:01BB 00000000000000000000000000000000:0000 0A 00000000:00000000 00:00000000 00000000 0 0 5\n"
        "   1: 00000000000000000000000001000000:1F90 00000000000000000000000000000000:0000 0A 00000000:00000000 00:00000000 00000000 0 0 6\n",
        encoding="utf-8",
    )
    (net / "udp6").write_text(
        "  sl  local_address                         remote_address                        st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode\n"
        "   0: 00000000000000000000000000000000:04D2 00000000000000000000000000000000:0000 07 00000000:00000000 00:00000000 00000000 0 0 7\n",
        encoding="utf-8",
    )
    return proc


def _patch_listener_host(monkeypatch):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_mount_observations",
        lambda self, observed_at, hostname, metadata: [],
    )
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_storage_observations",
        lambda self, observed_at, hostname, metadata: [],
    )


def test_local_host_source_emits_tcp_udp_listener_observations(monkeypatch, tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    proc = _write_listener_fixture(tmp_path / "proc")
    _patch_listener_host(monkeypatch)

    observations = LocalHostObservationSource(proc_root=proc).collect()

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert ("node-a", "listening_endpoint", "tcp 0.0.0.0:22") in triples
    assert ("node-a", "listening_endpoint", "tcp 127.0.0.1:9094") in triples
    assert ("node-a", "listening_endpoint", "udp 0.0.0.0:53") in triples
    assert ("node-a", "listening_endpoint", "tcp [::]:443") in triples
    assert ("node-a", "listening_endpoint", "tcp [::1]:8080") in triples
    assert ("node-a", "listening_endpoint", "udp [::]:1234") in triples
    assert ("node-a", "listening_protocol", "tcp") in triples
    assert ("node-a", "listening_protocol", "udp") in triples
    assert ("node-a", "listening_address", "0.0.0.0") in triples
    assert ("node-a", "listening_address", "::1") in triples
    assert ("node-a", "listening_port", 22) in triples
    assert ("node-a", "listening_port", 53) in triples
    assert ("node-a", "listening_endpoint", "tcp 127.0.0.1:80") not in triples
    endpoint = next(obs for obs in observations if obs.value == "tcp 0.0.0.0:22")
    assert endpoint.dimensions == {
        "protocol": "tcp",
        "address": "0.0.0.0",
        "port": "22",
        "address_family": "ipv4",
    }
    assert endpoint.metadata["source"] == "/proc/net/tcp"
    assert endpoint.metadata["question_answered"] == (
        "What protocol/address/port endpoints are bound locally?"
    )


def test_listening_port_observation_is_deterministic(monkeypatch, tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    proc = _write_listener_fixture(tmp_path / "proc")
    _patch_listener_host(monkeypatch)
    source = LocalHostObservationSource(proc_root=proc)

    first = [
        (obs.subject, obs.predicate, obs.value, obs.dimensions)
        for obs in source.collect()
        if obs.predicate.startswith("listening_")
    ]
    second = [
        (obs.subject, obs.predicate, obs.value, obs.dimensions)
        for obs in source.collect()
        if obs.predicate.startswith("listening_")
    ]

    assert first == second


def test_listening_port_observation_projects_without_availability_reachability_health_or_ownership(
    monkeypatch, tmp_path
):
    from seed_runtime.observations import ObservationIngestor
    from seed_runtime.observation_sources import (
        LocalHostObservationSource,
        ObservationCollectionService,
    )
    from seed_runtime.state import StateProjector

    proc = _write_listener_fixture(tmp_path / "proc")
    _patch_listener_host(monkeypatch)
    ledger = EventLedger()
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        LocalHostObservationSource(proc_root=proc), "ws_listeners"
    )
    state = StateProjector(ledger).project("ws_listeners")

    assert state.get_current_facts("node-a", "listening_endpoint")
    assert state.get_current_facts("node-a", "listening_port")
    assert state.get_current_facts("node-a", "listening_protocol")
    assert state.get_current_facts("node-a", "listening_address")
    for forbidden in (
        "availability_status",
        "reachability_status",
        "endpoint_health",
        "listener_health",
        "process_owner",
        "service_owner",
        "application_owner",
        "service_status",
    ):
        assert state.get_best_fact("node-a", forbidden) is None


def test_listening_port_observation_avoids_execution_root_network_dns_and_providers(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    def fail_forbidden(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError(
            "listener observation must not execute, escalate, network, DNS, or call providers"
        )

    proc = _write_listener_fixture(tmp_path / "proc")
    _patch_listener_host(monkeypatch)
    monkeypatch.setattr(sources.socket, "create_connection", fail_forbidden)
    monkeypatch.setattr(sources.socket, "getaddrinfo", fail_forbidden)
    monkeypatch.setattr(sources.socket, "gethostbyname", fail_forbidden)
    monkeypatch.setattr(sources, "urlopen", fail_forbidden)
    monkeypatch.setattr(os, "system", fail_forbidden)
    monkeypatch.setattr(subprocess, "Popen", fail_forbidden)
    monkeypatch.setattr(subprocess, "run", fail_forbidden)

    observations = LocalHostObservationSource(proc_root=proc).collect()
    listeners = [obs for obs in observations if obs.predicate.startswith("listening_")]

    assert listeners
    assert all(obs.metadata["local_only"] is True for obs in listeners)
    assert all(obs.metadata["shell_execution"] is False for obs in listeners)
    assert all(obs.metadata["subprocess_execution"] is False for obs in listeners)
    assert all(obs.metadata["privilege_escalation"] is False for obs in listeners)
    assert all(obs.metadata["network_probe"] is False for obs in listeners)
    assert all(obs.metadata["network_connection"] is False for obs in listeners)
    assert all(obs.metadata["availability_asserted"] is False for obs in listeners)
    assert all(obs.metadata["reachability_asserted"] is False for obs in listeners)
    assert all(obs.metadata["endpoint_health_asserted"] is False for obs in listeners)
    assert all(obs.metadata["process_owner_asserted"] is False for obs in listeners)
    assert all(obs.metadata["service_owner_asserted"] is False for obs in listeners)


def test_listening_port_observation_uses_bounded_reads_and_skips_truncated_inputs(
    monkeypatch, tmp_path
):
    from seed_runtime.observation_sources import LocalHostObservationSource

    proc = _write_listener_fixture(tmp_path / "proc")
    (proc / "net" / "tcp").write_text(
        "  sl  local_address rem_address   st\n" "   0: 00000000:0016 00000000:0000\n",
        encoding="utf-8",
    )
    (proc / "net" / "udp").write_text("x" * (1024 * 1024 + 1), encoding="utf-8")
    _patch_listener_host(monkeypatch)

    observations = LocalHostObservationSource(proc_root=proc).collect()
    endpoints = [
        obs.value for obs in observations if obs.predicate == "listening_endpoint"
    ]

    assert "tcp 0.0.0.0:22" not in endpoints
    assert "udp 0.0.0.0:53" not in endpoints
    assert "tcp [::]:443" in endpoints
    assert "udp [::]:1234" in endpoints


def _write_mount_fixture(proc: Path) -> Path:
    proc.mkdir(parents=True, exist_ok=True)
    (proc / "mounts").write_text(
        "/dev/sda1 / ext4 rw,relatime 0 0\n"
        "tmpfs /run tmpfs rw,nosuid,nodev,mode=755 0 0\n"
        "/dev/disk/by-label/My\\040Data /mnt/My\\040Data xfs ro,relatime 0 0\n",
        encoding="utf-8",
    )
    return proc


def test_local_host_source_emits_mount_observations(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc = _write_mount_fixture(tmp_path / "proc")
    missing = tmp_path / "missing"
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    observations = LocalHostObservationSource(
        proc_root=proc, sys_class_net=missing, resolv_conf=missing
    ).collect()

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert ("node-a", "mount_point", "/") in triples
    assert ("node-a", "mount_point", "/mnt/My Data") in triples
    assert ("node-a", "filesystem_type", "ext4") in triples
    assert ("node-a", "filesystem_type", "xfs") in triples
    assert ("node-a", "mounted_device", "/dev/sda1") in triples
    assert ("node-a", "mounted_device", "/dev/disk/by-label/My Data") in triples
    assert ("node-a", "mount_option", "ro") in triples
    mount_point = next(
        obs
        for obs in observations
        if obs.predicate == "mount_point" and obs.value == "/"
    )
    assert mount_point.dimensions == {"mount_point": "/"}
    assert mount_point.metadata["source"] == "/proc/mounts"
    assert (
        mount_point.metadata["question_answered"]
        == "What mount points currently exist?"
    )
    assert mount_point.metadata["availability_asserted"] is False
    assert mount_point.metadata["reachability_asserted"] is False
    assert mount_point.metadata["network_reachability_asserted"] is False
    assert mount_point.metadata["health_asserted"] is False
    assert mount_point.metadata["writability_asserted"] is False


def test_mount_observation_projection_is_deterministic(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc = _write_mount_fixture(tmp_path / "proc")
    missing = tmp_path / "missing"
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )
    source = LocalHostObservationSource(
        proc_root=proc, sys_class_net=missing, resolv_conf=missing
    )

    first = [
        (obs.subject, obs.predicate, obs.value, obs.dimensions)
        for obs in source.collect()
        if obs.predicate
        in {"mount_point", "filesystem_type", "mounted_device", "mount_option"}
    ]
    second = [
        (obs.subject, obs.predicate, obs.value, obs.dimensions)
        for obs in source.collect()
        if obs.predicate
        in {"mount_point", "filesystem_type", "mounted_device", "mount_option"}
    ]

    assert first == second


def test_mount_observation_projects_without_availability_or_reachability(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observations import ObservationIngestor
    from seed_runtime.observation_sources import (
        LocalHostObservationSource,
        ObservationCollectionService,
    )
    from seed_runtime.state import StateProjector

    class DiskUsage:
        total = 1000
        free = 250

    proc = _write_mount_fixture(tmp_path / "proc")
    missing = tmp_path / "missing"
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    ledger = EventLedger()
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        LocalHostObservationSource(
            proc_root=proc, sys_class_net=missing, resolv_conf=missing
        ),
        "ws_mount",
    )
    state = StateProjector(ledger).project("ws_mount")

    assert state.get_current_facts("node-a", "mount_point")
    assert state.get_current_facts("node-a", "filesystem_type")
    assert state.get_current_facts("node-a", "mounted_device")
    assert state.get_current_facts("node-a", "mount_option")
    assert state.get_best_fact("node-a", "availability_status") is None
    assert state.get_best_fact("node-a", "reachability_status") is None


def test_mount_observation_does_not_probe_execute_or_escalate(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    def fail_forbidden(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError("mount observation must not probe, execute, or escalate")

    proc = _write_mount_fixture(tmp_path / "proc")
    missing = tmp_path / "missing"
    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(sources.socket, "create_connection", fail_forbidden)
    monkeypatch.setattr(sources.socket, "getaddrinfo", fail_forbidden)
    monkeypatch.setattr(sources.socket, "gethostbyname", fail_forbidden)
    monkeypatch.setattr(sources, "urlopen", fail_forbidden)
    monkeypatch.setattr(os, "system", fail_forbidden)
    monkeypatch.setattr(subprocess, "Popen", fail_forbidden)
    monkeypatch.setattr(subprocess, "run", fail_forbidden)
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    observations = LocalHostObservationSource(
        proc_root=proc, sys_class_net=missing, resolv_conf=missing
    ).collect()
    mount_observations = [
        obs
        for obs in observations
        if obs.predicate
        in {"mount_point", "filesystem_type", "mounted_device", "mount_option"}
    ]

    assert mount_observations
    assert all(obs.metadata["local_only"] is True for obs in mount_observations)
    assert all(obs.metadata["shell_execution"] is False for obs in mount_observations)
    assert all(
        obs.metadata["subprocess_execution"] is False for obs in mount_observations
    )
    assert all(
        obs.metadata["privilege_escalation"] is False for obs in mount_observations
    )
    assert all(obs.metadata["network_probe"] is False for obs in mount_observations)
    assert all(
        obs.metadata["network_connection"] is False for obs in mount_observations
    )


def test_prometheus_source_uses_safe_get_queries_and_converts_observations(
    monkeypatch,
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import PrometheusObservationSource

    requested_urls = []

    class Response:
        def __init__(self, payload):
            self.payload = payload

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps(self.payload).encode("utf-8")

    payloads = {
        "up": {
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": [
                    {
                        "metric": {"instance": "node-a:9100", "job": "node-exporter"},
                        "value": [1, "1"],
                    }
                ],
            },
        },
        "node_uname_info": {
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": [
                    {
                        "metric": {"instance": "node-a:9100", "sysname": "Linux"},
                        "value": [1, "1"],
                    }
                ],
            },
        },
        "node_filesystem_avail_bytes": {
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": [
                    {
                        "metric": {
                            "instance": "node-a:9100",
                            "mountpoint": "/",
                            "device": "/dev/sda1",
                            "fstype": "ext4",
                        },
                        "value": [1, "512"],
                    }
                ],
            },
        },
        "node_filesystem_size_bytes": {
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": [
                    {
                        "metric": {
                            "instance": "node-a:9100",
                            "mountpoint": "/",
                            "device": "/dev/sda1",
                            "fstype": "ext4",
                        },
                        "value": [1, "1024"],
                    }
                ],
            },
        },
    }

    def fake_urlopen(request, timeout):
        requested_urls.append((request.full_url, request.get_method(), timeout))
        query = request.full_url.rsplit("query=", 1)[1]
        return Response(payloads[query])

    monkeypatch.setattr(sources, "urlopen", fake_urlopen)

    source = PrometheusObservationSource(
        "http://prom.example:9090", timeout_seconds=2.5
    )
    observations = source.collect()

    assert [(obs.subject, obs.predicate, obs.value) for obs in observations] == [
        ("node-a:9100", "endpoint_role", "node-exporter"),
        ("node-a:9100", "up", 1),
        ("node-a:9100", "os", "linux"),
        ("node-a:9100", "filesystem_avail_bytes", 512),
        ("node-a:9100", "filesystem_size_bytes", 1024),
    ]
    assert observations[0].dimensions == {}
    assert observations[3].dimensions == {
        "mountpoint": "/",
        "device": "/dev/sda1",
        "fstype": "ext4",
    }
    assert observations[4].dimensions == observations[3].dimensions
    assert {obs.source_type for obs in observations} == {"provider"}
    assert {obs.metadata["source_name"] for obs in observations} == {"prometheus"}
    assert [method for _, method, _ in requested_urls] == ["GET"] * 4
    assert [timeout for _, _, timeout in requested_urls] == [2.5] * 4
    assert [url.rsplit("query=", 1)[1] for url, _, _ in requested_urls] == list(
        PrometheusObservationSource.SAFE_QUERIES
    )


def test_prometheus_node_uname_os_endpoint_evidence_is_preserved_without_fact_promotion(
    monkeypatch,
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import PrometheusObservationSource

    class Response:
        def __init__(self, payload):
            self.payload = payload

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps(self.payload).encode("utf-8")

    def fake_urlopen(request, timeout):
        query = request.full_url.rsplit("query=", 1)[1]
        metric = {"instance": "192.0.2.115:9100"}
        if query == "up":
            metric["job"] = "node-exporter"
        if query == "node_uname_info":
            metric.update({"nodename": "example_host", "sysname": "Linux"})
        if query.startswith("node_filesystem_"):
            metric.update({"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"})
        return Response(
            {
                "status": "success",
                "data": {
                    "resultType": "vector",
                    "result": [{"metric": metric, "value": [1, "1"]}],
                },
            }
        )

    monkeypatch.setattr(sources, "urlopen", fake_urlopen)
    source = PrometheusObservationSource("http://prom.example:9090", name="prometheus")

    raw = source.collect()
    raw_os = [obs for obs in raw if obs.predicate == "os"]
    assert len(raw_os) == 1
    assert raw_os[0].subject == "192.0.2.115:9100"
    assert raw_os[0].value == "linux"
    assert raw_os[0].metadata["source_name"] == "prometheus"
    assert raw_os[0].metadata["prometheus_metric"] == "node_uname_info"
    assert raw_os[0].metadata["metric_labels"] == {
        "instance": "192.0.2.115:9100",
        "nodename": "example_host",
        "sysname": "Linux",
    }
    assert raw_os[0].metadata["instance"] == "192.0.2.115:9100"
    assert raw_os[0].metadata["nodename"] == "example_host"
    assert raw_os[0].metadata["fact_promotion_suppressed"] is True

    ledger = EventLedger()
    facts = ObservationCollectionService(ObservationIngestor(ledger)).collect(
        source, "ws_prometheus_os_endpoint"
    )
    state = StateProjector(ledger).project("ws_prometheus_os_endpoint")

    assert state.get_best_fact("192.0.2.115:9100", "os") is None
    assert state.get_best_fact("example_host", "os") is None
    assert state.get_best_fact("example_host", "prometheus_instance").value == (
        "192.0.2.115:9100"
    )
    assert state.get_best_fact("192.0.2.115:9100", "up").value == 1
    assert state.get_best_fact("192.0.2.115:9100", "availability_status").value == "up"
    assert state.get_best_fact("192.0.2.115:9100", "filesystem_avail_bytes").value == 1
    assert state.get_best_fact("192.0.2.115:9100", "filesystem_free_bytes").value == 1
    assert state.get_best_fact("192.0.2.115:9100", "filesystem_size_bytes").value == 1
    assert state.get_best_fact("192.0.2.115:9100", "filesystem_total_bytes").value == 1
    assert not any(
        fact.subject_id == "192.0.2.115:9100" and fact.predicate == "os"
        for fact in facts
    )

    observation_events = [
        event
        for event in ledger.list("ws_prometheus_os_endpoint")
        if event.kind == "observation.observed"
    ]
    evidence_events = [
        event
        for event in ledger.list("ws_prometheus_os_endpoint")
        if event.kind == "evidence.observed"
    ]
    fact_events = [
        event
        for event in ledger.list("ws_prometheus_os_endpoint")
        if event.kind == "fact.observed"
    ]
    observed_os_payloads = [
        event.payload["observation"]
        for event in observation_events
        if event.payload["observation"]["predicate"] == "os"
    ]
    evidence_os_payloads = [
        event.payload["evidence"]["payload"]
        for event in evidence_events
        if event.payload["evidence"]["payload"]["predicate"] == "os"
    ]
    fact_os_payloads = [
        event.payload["fact"]
        for event in fact_events
        if event.payload["fact"]["predicate"] == "os"
    ]
    assert len(observed_os_payloads) == 1
    assert observed_os_payloads[0]["metadata"]["prometheus_metric"] == "node_uname_info"
    assert observed_os_payloads[0]["metadata"]["nodename"] == "example_host"
    assert len(evidence_os_payloads) == 1
    assert evidence_os_payloads[0]["metadata"]["prometheus_metric"] == "node_uname_info"
    assert evidence_os_payloads[0]["metadata"]["nodename"] == "example_host"
    assert fact_os_payloads == []


def test_non_prometheus_os_observation_still_promotes_to_fact():
    ledger = EventLedger()
    source = FakeObservationSource(
        [
            _observation(
                "obs_local_os",
                subject="192.0.2.115:9100",
                predicate="os",
                value="linux",
                metadata={"source_name": "local_inventory"},
            )
        ],
        name="local_inventory",
    )

    facts = ObservationCollectionService(ObservationIngestor(ledger)).collect(
        source, "ws_non_prometheus_os"
    )
    state = StateProjector(ledger).project("ws_non_prometheus_os")

    assert [(fact.subject_id, fact.predicate, fact.value) for fact in facts] == [
        ("192.0.2.115:9100", "os", "linux")
    ]
    assert state.get_best_fact("192.0.2.115:9100", "os").value == "linux"


class _PrometheusResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def _prometheus_vector_payload(result):
    return {"status": "success", "data": {"resultType": "vector", "result": result}}


def _patch_prometheus_payloads(monkeypatch, payloads_by_query):
    from seed_runtime import observation_sources as sources

    def fake_urlopen(request, timeout):
        query = request.full_url.rsplit("query=", 1)[1]
        return _PrometheusResponse(
            payloads_by_query.get(query, _prometheus_vector_payload([]))
        )

    monkeypatch.setattr(sources, "urlopen", fake_urlopen)


def test_prometheus_vector_sample_timestamp_and_value_are_preserved(monkeypatch):
    from seed_runtime.observation_sources import PrometheusObservationSource

    _patch_prometheus_payloads(
        monkeypatch,
        {
            "up": _prometheus_vector_payload(
                [
                    {
                        "metric": {"instance": "node-a:9100"},
                        "value": ["1718123456.789", "1"],
                    }
                ]
            )
        },
    )
    before = datetime.now(timezone.utc)

    observations = PrometheusObservationSource("http://prom.example:9090").collect()

    after = datetime.now(timezone.utc)
    assert len(observations) == 1
    observation = observations[0]
    sample_time = datetime.fromisoformat("2024-06-11T16:30:56.789000+00:00")
    assert observation.observed_at == sample_time
    assert observation.value == 1
    assert (
        observation.metadata["prometheus_sample_timestamp"] == sample_time.isoformat()
    )
    assert observation.metadata["prometheus_sample_timestamp_raw"] == "1718123456.789"
    assert observation.metadata["source_observed_at"] == sample_time.isoformat()
    assert observation.metadata["source_time_kind"] == "sample_time"
    assert observation.metadata["source_time_authority"] == "prometheus"
    assert observation.metadata["seed_collection_time_authority"] == "seed_local_clock"
    assert observation.metadata["query_temporal_intent"] == "current_instant"
    seed_collected_at = datetime.fromisoformat(
        observation.metadata["seed_collected_at"]
    )
    assert before <= seed_collected_at <= after
    assert seed_collected_at != observation.observed_at


def test_prometheus_malformed_sample_timestamp_is_skipped(monkeypatch):
    from seed_runtime.observation_sources import PrometheusObservationSource

    _patch_prometheus_payloads(
        monkeypatch,
        {
            "up": _prometheus_vector_payload(
                [
                    {
                        "metric": {"instance": "bad-node:9100"},
                        "value": ["not-a-unix-timestamp", "1"],
                    },
                    {
                        "metric": {"instance": "good-node:9100"},
                        "value": [1718123456, "0"],
                    },
                ]
            )
        },
    )

    observations = PrometheusObservationSource("http://prom.example:9090").collect()

    assert [(obs.subject, obs.value) for obs in observations] == [("good-node:9100", 0)]
    assert observations[0].observed_at == datetime.fromtimestamp(
        1718123456, timezone.utc
    )


def test_prometheus_event_timestamp_remains_independent_from_sample_time(monkeypatch):
    from seed_runtime.observation_sources import PrometheusObservationSource

    _patch_prometheus_payloads(
        monkeypatch,
        {
            "up": _prometheus_vector_payload(
                [
                    {
                        "metric": {"instance": "node-a:9100"},
                        "value": [1718123456, "1"],
                    }
                ]
            )
        },
    )
    source = PrometheusObservationSource("http://prom.example:9090")
    ledger = EventLedger()

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        source, "ws_prom_time"
    )

    observed_event = ledger.list("ws_prom_time")[0]
    sample_time = datetime.fromtimestamp(1718123456, timezone.utc)
    assert observed_event.kind == "observation.observed"
    assert observed_event.timestamp != sample_time
    assert (
        observed_event.payload["observation"]["observed_at"] == sample_time.isoformat()
    )
    assert (
        observed_event.payload["observation"]["metadata"]["seed_collected_at"]
        != sample_time.isoformat()
    )


def test_prometheus_measurement_latest_current_uses_sample_time(monkeypatch):
    from seed_runtime.observation_sources import PrometheusObservationSource

    older_time = 1718123456
    newer_time = 1718124456
    _patch_prometheus_payloads(
        monkeypatch,
        {
            "up": _prometheus_vector_payload(
                [
                    {
                        "metric": {"instance": "node-a:9100"},
                        "value": [newer_time, "1"],
                    },
                    {
                        "metric": {"instance": "node-a:9100"},
                        "value": [older_time, "0"],
                    },
                ]
            )
        },
    )
    ledger = EventLedger()

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        PrometheusObservationSource("http://prom.example:9090"), "ws_prom_latest"
    )
    state = StateProjector(ledger).project("ws_prom_latest")

    best = state.get_best_fact("node-a:9100", "up")
    assert best is not None
    assert best.value == 1
    assert best.observed_at == datetime.fromtimestamp(newer_time, timezone.utc)


def test_prometheus_source_unreachable_fails_gracefully(monkeypatch):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import PrometheusObservationSource

    def fake_urlopen(request, timeout):
        raise OSError("network unreachable")

    monkeypatch.setattr(sources, "urlopen", fake_urlopen)

    source = PrometheusObservationSource("http://prom.example:9090", timeout_seconds=1)

    assert source.collect() == []
    assert "network unreachable" in (source.last_error or "")


def test_collection_normalized_endpoint_instance_keeps_best_fact_endpoint_scoped():
    ledger = EventLedger()
    source = FakeObservationSource(
        [
            _observation(
                "obs_generic_up",
                subject="192.0.2.115:9100",
                predicate="up",
                value=1,
                metadata={
                    "hostname": "example_host",
                    "instance": "192.0.2.115:9100",
                    "source": "generic",
                },
            )
        ],
        name="generic",
    )

    facts = ObservationCollectionService(ObservationIngestor(ledger)).collect(
        source, "ws_generic_alias"
    )
    state = StateProjector(ledger).project("ws_generic_alias")

    assert len(facts) == 2
    assert state.get_best_fact("example_host", "up") is None
    assert state.get_best_fact("192.0.2.115:9100", "up").value == 1
    assert any(
        fact.subject_id == "example_host"
        and fact.predicate == "generic_instance"
        and fact.value == "192.0.2.115:9100"
        for fact in state.facts.values()
    )


def test_prometheus_nodename_preserves_prometheus_instance_without_aliasing_endpoint(
    monkeypatch,
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import PrometheusObservationSource

    class Response:
        def __init__(self, payload):
            self.payload = payload

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps(self.payload).encode("utf-8")

    def fake_urlopen(request, timeout):
        query = request.full_url.rsplit("query=", 1)[1]
        metric = {"instance": "192.0.2.115:9100"}
        if query == "node_uname_info":
            metric.update({"nodename": "example_host", "sysname": "Linux"})
        return Response(
            {
                "status": "success",
                "data": {
                    "resultType": "vector",
                    "result": [{"metric": metric, "value": [1, "1"]}],
                },
            }
        )

    monkeypatch.setattr(sources, "urlopen", fake_urlopen)
    source = PrometheusObservationSource("http://prom.example:9090", name="prometheus")

    raw = source.collect()
    assert all("nodename" not in obs.metadata for obs in raw if obs.predicate != "os")
    assert all("instance" not in obs.metadata for obs in raw if obs.predicate != "os")

    ledger = EventLedger()
    facts = ObservationCollectionService(ObservationIngestor(ledger)).collect(
        source, "ws_prometheus_alias"
    )
    state = StateProjector(ledger).project("ws_prometheus_alias")

    canonical = {(fact.predicate, fact.value) for fact in facts}
    assert ("availability_status", "up") in canonical
    assert ("filesystem_free_bytes", 1) in canonical
    assert ("filesystem_total_bytes", 1) in canonical
    aliases = [fact for fact in facts if fact.predicate == "prometheus_instance"]
    assert len(aliases) == 1
    assert aliases[0].subject_id == "example_host"
    assert aliases[0].value == "192.0.2.115:9100"
    assert state.get_best_fact("example_host", "up") is None
    assert state.get_best_fact("192.0.2.115:9100", "up").value == 1
    assert not any(
        relationship.relationship == "monitored_by"
        for relationship in state.get_relationships()
    )


def _write_local_identity_fixture(tmp_path, hostname="example_host", *, fqdn=False):
    proc = tmp_path / "proc"
    etc_hostname = tmp_path / "hostname"
    machine_id = tmp_path / "machine-id"
    (proc / "sys" / "kernel" / "random").mkdir(parents=True)
    if fqdn:
        hostname = "example_host.example.test"
    etc_hostname.write_text(hostname + "\n", encoding="utf-8")
    (proc / "sys" / "kernel" / "hostname").write_text(
        "ignored-proc-host\n", encoding="utf-8"
    )
    machine_id.write_text("0123456789abcdef0123456789abcdef\n", encoding="utf-8")
    (proc / "sys" / "kernel" / "random" / "boot_id").write_text(
        "11111111-2222-3333-4444-555555555555\n", encoding="utf-8"
    )
    return proc, etc_hostname, machine_id


def test_local_host_source_emits_identity_observations(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc, etc_hostname, machine_id = _write_local_identity_fixture(tmp_path)
    monkeypatch.setattr(sources.platform, "node", lambda: "")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    observations = LocalHostObservationSource(
        proc_root=proc, etc_hostname=etc_hostname, machine_id=machine_id
    ).collect()

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert ("example_host", "hostname", "example_host") in triples
    assert ("example_host", "machine_id", "0123456789abcdef0123456789abcdef") in triples
    assert (
        "example_host",
        "boot_id",
        "11111111-2222-3333-4444-555555555555",
    ) in triples
    assert not [obs for obs in observations if obs.predicate == "fqdn"]
    for obs in observations:
        if obs.predicate in {"hostname", "machine_id", "boot_id"}:
            assert obs.metadata["local_only"] is True
            assert obs.metadata["shell_execution"] is False
            assert obs.metadata["subprocess_execution"] is False
            assert obs.metadata["privilege_escalation"] is False
            assert obs.metadata["network_probe"] is False
            assert obs.metadata["network_connection"] is False
            assert obs.metadata["dns_resolution_asserted"] is False
            assert obs.metadata["network_reachability_asserted"] is False
            assert obs.metadata["availability_asserted"] is False


def test_local_host_source_emits_fqdn_only_when_locally_configured(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc, etc_hostname, machine_id = _write_local_identity_fixture(tmp_path, fqdn=True)
    monkeypatch.setattr(sources.platform, "node", lambda: "")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )

    observations = LocalHostObservationSource(
        proc_root=proc, etc_hostname=etc_hostname, machine_id=machine_id
    ).collect()

    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}
    assert (
        "example_host.example.test",
        "hostname",
        "example_host.example.test",
    ) in triples
    assert ("example_host.example.test", "fqdn", "example_host.example.test") in triples


def test_local_identity_projection_is_deterministic(monkeypatch, tmp_path):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    proc, etc_hostname, machine_id = _write_local_identity_fixture(tmp_path)
    monkeypatch.setattr(sources.platform, "node", lambda: "")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )
    source = LocalHostObservationSource(
        proc_root=proc, etc_hostname=etc_hostname, machine_id=machine_id
    )

    first = [
        (obs.subject, obs.predicate, obs.value, obs.dimensions)
        for obs in source.collect()
    ]
    second = [
        (obs.subject, obs.predicate, obs.value, obs.dimensions)
        for obs in source.collect()
    ]

    assert first == second


def test_local_identity_does_not_infer_availability_or_reachability(
    monkeypatch, tmp_path
):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observations import ObservationIngestor
    from seed_runtime.observation_sources import (
        LocalHostObservationSource,
        ObservationCollectionService,
    )
    from seed_runtime.state import StateProjector

    class DiskUsage:
        total = 1000
        free = 250

    proc, etc_hostname, machine_id = _write_local_identity_fixture(tmp_path)
    monkeypatch.setattr(sources.platform, "node", lambda: "")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )
    ledger = EventLedger()
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        LocalHostObservationSource(
            proc_root=proc, etc_hostname=etc_hostname, machine_id=machine_id
        ),
        "ws_identity",
    )
    state = StateProjector(ledger).project("ws_identity")

    assert state.get_best_fact("example_host", "hostname").value == "example_host"
    assert state.get_best_fact("example_host", "availability_status") is None
    assert state.get_best_fact("example_host", "reachability_status") is None


def test_local_identity_observation_avoids_network_dns_execution_and_escalation(
    monkeypatch, tmp_path
):
    import subprocess
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    def fail_forbidden(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError(
            "identity observation must not use network, DNS, shell, subprocess, or sudo"
        )

    proc, etc_hostname, machine_id = _write_local_identity_fixture(tmp_path)
    monkeypatch.setattr(sources.platform, "node", lambda: "")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(
        LocalHostObservationSource,
        "_collect_network_observations",
        lambda self, observed_at, hostname, metadata: [],
    )
    monkeypatch.setattr(sources.socket, "create_connection", fail_forbidden)
    monkeypatch.setattr(sources.socket, "getaddrinfo", fail_forbidden)
    monkeypatch.setattr(sources.socket, "getfqdn", fail_forbidden)
    monkeypatch.setattr(sources.socket, "gethostbyname", fail_forbidden)
    monkeypatch.setattr(sources, "urlopen", fail_forbidden)
    monkeypatch.setattr(os, "system", fail_forbidden)
    monkeypatch.setattr(subprocess, "run", fail_forbidden)
    monkeypatch.setattr(subprocess, "Popen", fail_forbidden)

    observations = LocalHostObservationSource(
        proc_root=proc, etc_hostname=etc_hostname, machine_id=machine_id
    ).collect()

    assert {
        (obs.predicate, obs.value)
        for obs in observations
        if obs.predicate in {"hostname", "machine_id", "boot_id"}
    } == {
        ("hostname", "example_host"),
        ("machine_id", "0123456789abcdef0123456789abcdef"),
        ("boot_id", "11111111-2222-3333-4444-555555555555"),
    }


def _write_storage_fixture(tmp_path):
    proc = tmp_path / "proc"
    sys_block = tmp_path / "sys" / "block"
    sys_class_block = tmp_path / "sys" / "class" / "block"
    proc.mkdir(parents=True)
    sys_block.mkdir(parents=True)
    sys_class_block.mkdir(parents=True)
    (proc / "partitions").write_text(
        "major minor  #blocks  name\n\n   8        0   20971520 sda\n   8        1    1048576 sda1\n 259        0   41943040 nvme0n1\n 259        1    2097152 nvme0n1p1\n"
    )
    for device, sectors, rotational, removable, model, vendor in (
        ("sda", "41943040\n", "1\n", "0\n", "Fast Disk\n", "SEED\n"),
        ("nvme0n1", "83886080\n", "0\n", "0\n", "NVMe Disk\n", "NVMECO\n"),
    ):
        root = sys_block / device
        (root / "queue").mkdir(parents=True)
        (root / "device").mkdir()
        (root / "size").write_text(sectors)
        (root / "queue" / "rotational").write_text(rotational)
        (root / "removable").write_text(removable)
        (root / "device" / "model").write_text(model)
        (root / "device" / "vendor").write_text(vendor)
    for parent, partition, sectors in (
        ("sda", "sda1", "2097152\n"),
        ("nvme0n1", "nvme0n1p1", "4194304\n"),
    ):
        part_root = sys_block / parent / partition
        part_root.mkdir()
        (part_root / "partition").write_text("1\n")
        class_root = sys_class_block / partition
        class_root.mkdir()
        (class_root / "size").write_text(sectors)
    return proc, sys_block, sys_class_block


def test_local_host_source_observes_storage_topology_block_devices_and_partitions(
    tmp_path,
):
    from seed_runtime.observation_sources import LocalHostObservationSource

    proc, sys_block, sys_class_block = _write_storage_fixture(tmp_path)
    source = LocalHostObservationSource(
        proc_root=proc, sys_block=sys_block, sys_class_block=sys_class_block
    )

    observations = source._collect_storage_observations(BASE_TIME, "example_host", {})
    triples = {(obs.predicate, obs.value) for obs in observations}

    assert ("block_device", "sda") in triples
    assert ("block_device", "nvme0n1") in triples
    assert ("partition", "sda1") in triples
    assert ("partition", "nvme0n1p1") in triples


def test_local_host_source_observes_storage_size_markers_model_vendor_and_parent(
    tmp_path,
):
    from seed_runtime.observation_sources import LocalHostObservationSource

    proc, sys_block, sys_class_block = _write_storage_fixture(tmp_path)
    source = LocalHostObservationSource(
        proc_root=proc, sys_block=sys_block, sys_class_block=sys_class_block
    )

    observations = source._collect_storage_observations(BASE_TIME, "example_host", {})
    by_predicate = {}
    for obs in observations:
        by_predicate.setdefault(obs.predicate, []).append(obs)

    assert any(
        obs.value == 41943040 * 512 and obs.dimensions == {"device": "sda"}
        for obs in by_predicate["block_device_size_bytes"]
    )
    assert any(
        obs.value == 2097152 * 512
        and obs.dimensions == {"device": "sda1", "parent": "sda"}
        for obs in by_predicate["block_device_size_bytes"]
    )
    assert ("block_device_rotational", "true") in {
        (obs.predicate, obs.value) for obs in observations
    }
    assert ("block_device_removable", "false") in {
        (obs.predicate, obs.value) for obs in observations
    }
    assert ("block_device_model", "Fast Disk") in {
        (obs.predicate, obs.value) for obs in observations
    }
    assert ("block_device_vendor", "SEED") in {
        (obs.predicate, obs.value) for obs in observations
    }
    assert any(
        obs.predicate == "block_device_parent"
        and obs.value == "sda"
        and obs.dimensions == {"device": "sda1", "parent": "sda"}
        for obs in observations
    )


def test_local_storage_projection_is_deterministic(tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    proc, sys_block, sys_class_block = _write_storage_fixture(tmp_path)
    source = LocalHostObservationSource(
        proc_root=proc, sys_block=sys_block, sys_class_block=sys_class_block
    )

    first = [
        (obs.subject, obs.predicate, obs.value, obs.dimensions)
        for obs in source._collect_storage_observations(BASE_TIME, "example_host", {})
    ]
    second = [
        (obs.subject, obs.predicate, obs.value, obs.dimensions)
        for obs in source._collect_storage_observations(BASE_TIME, "example_host", {})
    ]

    assert first == second


def test_local_storage_current_facts_and_no_health_or_availability_inference(tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    proc, sys_block, sys_class_block = _write_storage_fixture(tmp_path)
    ledger = EventLedger()
    source = LocalHostObservationSource(
        proc_root=proc, sys_block=sys_block, sys_class_block=sys_class_block
    )
    observations = source._collect_storage_observations(BASE_TIME, "example_host", {})

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource(observations, source_type="discovery"), "ws_storage"
    )
    state = StateProjector(ledger).project("ws_storage")

    assert state.get_current_facts("example_host", "block_device")
    assert state.get_current_facts("example_host", "partition")
    assert state.get_current_facts("example_host", "block_device_size_bytes")
    assert state.get_best_fact("example_host", "availability_status") is None
    assert state.get_best_fact("example_host", "health_status") is None
    assert state.get_best_fact("example_host", "filesystem_health") is None
    assert state.get_best_fact("example_host", "storage_health") is None


def test_local_storage_observation_avoids_shell_subprocess_sudo_network_and_dns(
    monkeypatch, tmp_path
):
    import subprocess
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    def fail_forbidden(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError(
            "storage observation must not use shell, subprocess, sudo, network, or DNS"
        )

    proc, sys_block, sys_class_block = _write_storage_fixture(tmp_path)
    monkeypatch.setattr(sources.socket, "create_connection", fail_forbidden)
    monkeypatch.setattr(sources.socket, "getaddrinfo", fail_forbidden)
    monkeypatch.setattr(sources.socket, "getfqdn", fail_forbidden)
    monkeypatch.setattr(sources.socket, "gethostbyname", fail_forbidden)
    monkeypatch.setattr(sources, "urlopen", fail_forbidden)
    monkeypatch.setattr(os, "system", fail_forbidden)
    monkeypatch.setattr(subprocess, "run", fail_forbidden)
    monkeypatch.setattr(subprocess, "Popen", fail_forbidden)

    observations = LocalHostObservationSource(
        proc_root=proc, sys_block=sys_block, sys_class_block=sys_class_block
    )._collect_storage_observations(BASE_TIME, "example_host", {})

    assert any(obs.predicate == "block_device" for obs in observations)


def test_local_bounded_first_line_skips_possibly_truncated_stream():
    from io import BytesIO

    from seed_runtime.observation_sources import _read_bounded_first_line

    class FullBoundStreamPath:
        def stat(self):
            raise OSError("unknown pseudo-file size")

        def open(self, mode):
            return BytesIO(b"x" * 8)

    assert _read_bounded_first_line(FullBoundStreamPath(), max_bytes=8) is None


def test_local_storage_bounded_reads_skip_oversized_or_truncated_inputs(tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    proc, sys_block, sys_class_block = _write_storage_fixture(tmp_path)
    (sys_block / "sda" / "device" / "model").write_text("x" * (1024 * 1024 + 1))
    source = LocalHostObservationSource(
        proc_root=proc, sys_block=sys_block, sys_class_block=sys_class_block
    )

    observations = source._collect_storage_observations(BASE_TIME, "example_host", {})

    assert ("block_device_model", "Fast Disk") not in {
        (obs.predicate, obs.value) for obs in observations
    }
    assert any(obs.predicate == "block_device_vendor" for obs in observations)


def _write_local_users_fixture(tmp_path: Path) -> tuple[Path, Path]:
    passwd = tmp_path / "passwd"
    group = tmp_path / "group"
    passwd.write_text(
        "root:x:0:0:root:/root:/bin/bash\n"
        "john:x:1000:1000:John:/home/john:/bin/bash\n"
        "nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin\n",
        encoding="utf-8",
    )
    group.write_text(
        "sudo:x:27:john\n" "docker:x:999:john\n" "john:x:1000:\n",
        encoding="utf-8",
    )
    return passwd, group


def test_local_users_observation_emits_fixture_passwd_and_group_facts(tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    passwd, group = _write_local_users_fixture(tmp_path)
    source = LocalHostObservationSource(etc_passwd=passwd, etc_group=group)

    observations = source._collect_local_user_observations(
        BASE_TIME, "example_host", {}
    )
    triples = {(obs.subject, obs.predicate, obs.value) for obs in observations}

    assert ("example_host", "user_account", "john") in triples
    assert ("example_host", "user_uid", 1000) in triples
    assert ("example_host", "user_primary_gid", 1000) in triples
    assert ("example_host", "user_home_directory", "/home/john") in triples
    assert ("example_host", "user_shell", "/bin/bash") in triples
    assert ("example_host", "group_account", "sudo") in triples
    assert ("example_host", "group_gid", 27) in triples
    assert ("example_host", "group_member", "john") in triples

    user_account = next(
        obs
        for obs in observations
        if obs.predicate == "user_account" and obs.value == "john"
    )
    assert user_account.dimensions == {"username": "john", "uid": "1000"}
    assert user_account.metadata["source"] == "/etc/passwd"
    assert user_account.metadata["source_file"] == "/etc/passwd"
    assert user_account.metadata["read_only"] is True
    assert user_account.metadata["question_answered"] == (
        "Which local user accounts are declared on this host?"
    )

    group_member = next(obs for obs in observations if obs.predicate == "group_member")
    assert group_member.dimensions == {
        "groupname": "docker",
        "gid": "999",
        "username": "john",
    }
    assert group_member.metadata["source"] == "/etc/group"
    assert group_member.metadata["source_file"] == "/etc/group"
    assert group_member.metadata["sudo_access_asserted"] is False
    assert group_member.metadata["privilege_asserted"] is False


def test_local_users_current_facts_fact_support_and_no_boundary_inference(tmp_path):
    from seed_runtime.observation_sources import LocalHostObservationSource

    passwd, group = _write_local_users_fixture(tmp_path)
    ledger = EventLedger()
    source = LocalHostObservationSource(etc_passwd=passwd, etc_group=group)
    observations = source._collect_local_user_observations(
        BASE_TIME, "example_host", {"read_only": True, "local_only": True}
    )

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource(observations, source_type="discovery"), "ws_local_users"
    )
    state = StateProjector(ledger).project("ws_local_users")

    assert state.get_current_facts("example_host", "user_account")
    assert state.get_current_facts("example_host", "user_uid")
    assert state.get_current_facts("example_host", "user_primary_gid")
    assert state.get_current_facts("example_host", "user_home_directory")
    assert state.get_current_facts("example_host", "user_shell")
    assert state.get_current_facts("example_host", "group_account")
    assert state.get_current_facts("example_host", "group_gid")
    assert state.get_current_facts("example_host", "group_member")

    support = state.get_fact_support(
        "example_host",
        "group_member",
        dimensions={"groupname": "sudo", "gid": "27", "username": "john"},
    )
    assert support is not None
    assert support.value == "john"
    assert support.source_types == ["discovery"]

    forbidden_predicates = {
        "active_login_session",
        "ssh_access",
        "sudo_access",
        "sudoers_rule",
        "user_privileged",
        "account_safe",
        "account_enabled",
        "password_status",
        "availability_status",
    }
    emitted_predicates = {obs.predicate for obs in observations}
    assert emitted_predicates.isdisjoint(forbidden_predicates)
    for predicate in forbidden_predicates:
        assert state.get_best_fact("example_host", predicate) is None


def test_local_users_observation_avoids_forbidden_activity_privilege_sources(
    monkeypatch, tmp_path
):
    import subprocess
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    def fail_forbidden(*args, **kwargs):  # pragma: no cover - guard callback
        raise AssertionError(
            "local user observation must not execute, network, inspect login state, or inspect privilege sources"
        )

    passwd, group = _write_local_users_fixture(tmp_path)
    forbidden_paths = {
        "/etc/shadow",
        "/etc/sudoers",
        "/etc/sudoers.d",
        "authorized_keys",
        "pam.d",
        "utmp",
        "wtmp",
    }
    original_read_text = LocalHostObservationSource._read_text

    def guarded_read_text(self, path, *args, **kwargs):
        path_text = str(path)
        assert not any(forbidden in path_text for forbidden in forbidden_paths)
        return original_read_text(self, path, *args, **kwargs)

    monkeypatch.setattr(LocalHostObservationSource, "_read_text", guarded_read_text)
    monkeypatch.setattr(sources.socket, "create_connection", fail_forbidden)
    monkeypatch.setattr(sources.socket, "getaddrinfo", fail_forbidden)
    monkeypatch.setattr(sources, "urlopen", fail_forbidden)
    monkeypatch.setattr(os, "system", fail_forbidden)
    monkeypatch.setattr(subprocess, "run", fail_forbidden)
    monkeypatch.setattr(subprocess, "Popen", fail_forbidden)

    observations = LocalHostObservationSource(
        etc_passwd=passwd, etc_group=group
    )._collect_local_user_observations(BASE_TIME, "example_host", {})

    assert any(obs.predicate == "user_account" for obs in observations)
    assert any(obs.predicate == "group_member" for obs in observations)
    assert all(obs.metadata["shadow_inspected"] is False for obs in observations)
    assert all(obs.metadata["sudoers_inspected"] is False for obs in observations)
    assert all(
        obs.metadata["authorized_keys_inspected"] is False for obs in observations
    )
    assert all(obs.metadata["pam_inspected"] is False for obs in observations)
    assert all(obs.metadata["utmp_wtmp_inspected"] is False for obs in observations)
    assert all(obs.metadata["loginctl_inspected"] is False for obs in observations)



def test_local_host_observation_includes_systemd_source(monkeypatch):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import LocalHostObservationSource

    class DiskUsage:
        total = 1000
        free = 250

    class FakeSystemdSource:
        def __init__(self, *, observed_at, hostname):
            self.observed_at = observed_at
            self.hostname = hostname

        def collect(self):
            return [
                Observation(
                    id="obs_systemd_local",
                    source_type="discovery",
                    observed_at=self.observed_at,
                    subject=self.hostname,
                    predicate="systemd_unit",
                    value="nginx.service",
                    confidence=1.0,
                    metadata={"collector": "SystemdObservationSource"},
                    dimensions={"unit": "nginx.service"},
                )
            ]

    monkeypatch.setattr(sources.platform, "node", lambda: "node-a")
    monkeypatch.setattr(sources.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sources.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())
    monkeypatch.setattr(sources, "SystemdObservationSource", FakeSystemdSource)

    observations = LocalHostObservationSource().collect()

    assert ("node-a", "systemd_unit", "nginx.service") in {
        (obs.subject, obs.predicate, obs.value) for obs in observations
    }


def test_systemd_observations_flow_through_local_host_collection_and_projection():
    from seed_runtime.observation_sources import LocalHostObservationSource

    class FakeSystemdSource:
        def collect(self):
            return [
                Observation(
                    id="obs_systemd_unit_local",
                    source_type="discovery",
                    observed_at=BASE_TIME,
                    subject="node-a",
                    predicate="systemd_unit",
                    value="nginx.service",
                    confidence=1.0,
                    metadata={"collector": "SystemdObservationSource"},
                    dimensions={"unit": "nginx.service"},
                ),
                Observation(
                    id="obs_systemd_active_local",
                    source_type="discovery",
                    observed_at=BASE_TIME,
                    subject="node-a",
                    predicate="systemd_active_state",
                    value="active",
                    confidence=1.0,
                    metadata={"collector": "SystemdObservationSource"},
                    dimensions={"unit": "nginx.service"},
                ),
            ]

    source = LocalHostObservationSource(systemd_source=FakeSystemdSource())
    observations = source._collect_systemd_observations(BASE_TIME, "node-a")
    assert {obs.predicate for obs in observations} == {
        "systemd_unit",
        "systemd_active_state",
    }

    ledger = EventLedger()
    facts = ObservationCollectionService(
        ObservationIngestor(ledger), normalization_pipeline=None
    ).collect(source, "ws_local_host_systemd")
    state = StateProjector(ledger).project("ws_local_host_systemd")

    assert {fact.predicate for fact in facts} >= {
        "systemd_unit",
        "systemd_active_state",
    }
    assert (
        state.get_best_fact(
            "node-a", "systemd_active_state", dimensions={"unit": "nginx.service"}
        ).value
        == "active"
    )
    fact_view = build_fact_view(state)
    assert ("node-a", "systemd_unit", "nginx.service") in {
        (fact.subject, fact.predicate, fact.object) for fact in fact_view
    }

def test_systemd_observations_normalize_and_project_reported_states():
    from seed_runtime.observation_sources import SystemdObservationSource

    commands: list[tuple[str, ...]] = []

    def runner(command: list[str]) -> str:
        commands.append(tuple(command))
        if command[:2] == ["systemctl", "list-units"]:
            return json.dumps(
                [
                    {
                        "unit": "nginx.service",
                        "load": "loaded",
                        "active": "active",
                        "sub": "running",
                    },
                    {
                        "unit": "cron.service",
                        "load": "loaded",
                        "active": "inactive",
                        "sub": "dead",
                    },
                ]
            )
        if command[:2] == ["systemctl", "list-unit-files"]:
            return json.dumps(
                [
                    {"unit_file": "nginx.service", "state": "enabled"},
                    {"unit_file": "cron.service", "state": "disabled"},
                ]
            )
        raise AssertionError(command)

    observations = SystemdObservationSource(
        observed_at=BASE_TIME, command_runner=runner, hostname="node-a"
    ).collect()
    triples = {
        (obs.subject, obs.predicate, obs.value, obs.dimensions["unit"])
        for obs in observations
    }

    assert ("node-a", "systemd_unit", "nginx.service", "nginx.service") in triples
    assert ("node-a", "systemd_active_state", "active", "nginx.service") in triples
    assert ("node-a", "systemd_sub_state", "running", "nginx.service") in triples
    assert ("node-a", "systemd_unit_file_state", "enabled", "nginx.service") in triples
    assert ("node-a", "systemd_unit", "cron.service", "cron.service") in triples
    assert ("node-a", "systemd_active_state", "inactive", "cron.service") in triples
    assert ("node-a", "systemd_sub_state", "dead", "cron.service") in triples
    assert ("node-a", "systemd_unit_file_state", "disabled", "cron.service") in triples
    assert commands == [
        (
            "systemctl",
            "list-units",
            "--all",
            "--output=json",
            "--no-pager",
            "--plain",
        ),
        (
            "systemctl",
            "list-unit-files",
            "--output=json",
            "--no-pager",
            "--plain",
        ),
    ]
    assert all(obs.metadata["service_health_asserted"] is False for obs in observations)

    ledger = EventLedger()
    facts = ObservationCollectionService(
        ObservationIngestor(ledger), normalization_pipeline=None
    ).collect(
        FakeObservationSource(observations, name="systemd", source_type="discovery"),
        "ws_systemd",
    )
    state = StateProjector(ledger).project("ws_systemd")

    assert [
        (fact.value, fact.dimensions)
        for fact in state.get_current_facts(
            "node-a", "systemd_active_state", dimensions={"unit": "nginx.service"}
        )
    ] == [("active", {"unit": "nginx.service"})]
    assert (
        state.get_best_fact(
            "node-a", "systemd_sub_state", dimensions={"unit": "nginx.service"}
        ).value
        == "running"
    )
    assert (
        state.get_best_fact(
            "node-a", "systemd_unit_file_state", dimensions={"unit": "nginx.service"}
        ).value
        == "enabled"
    )
    assert {fact.predicate for fact in facts} == {
        "systemd_unit",
        "systemd_active_state",
        "systemd_sub_state",
        "systemd_unit_file_state",
    }


def test_systemd_missing_fields_are_safe_and_projection_is_deterministic():
    from seed_runtime.observation_sources import SystemdObservationSource

    def runner(command: list[str]) -> str:
        if command[:2] == ["systemctl", "list-units"]:
            return json.dumps(
                [
                    {"unit": "partial.service", "active": "activating"},
                    {"load": "loaded", "active": "failed", "sub": "failed"},
                ]
            )
        if command[:2] == ["systemctl", "list-unit-files"]:
            return json.dumps(
                [
                    {"unit_file": "partial.service"},
                    {"unit_file": "generated.service", "state": "generated"},
                ]
            )
        raise AssertionError(command)

    source = SystemdObservationSource(
        observed_at=BASE_TIME, command_runner=runner, hostname="node-a"
    )
    first = source.collect()
    second = source.collect()

    def stable(observations):
        return [
            (obs.subject, obs.predicate, obs.value, obs.dimensions)
            for obs in observations
        ]

    assert stable(first) == stable(second)
    assert stable(first) == [
        ("node-a", "systemd_unit", "generated.service", {"unit": "generated.service"}),
        (
            "node-a",
            "systemd_unit_file_state",
            "generated",
            {"unit": "generated.service"},
        ),
        ("node-a", "systemd_unit", "partial.service", {"unit": "partial.service"}),
        (
            "node-a",
            "systemd_active_state",
            "activating",
            {"unit": "partial.service"},
        ),
    ]

    ledger = EventLedger()
    ObservationCollectionService(
        ObservationIngestor(ledger), normalization_pipeline=None
    ).collect(
        FakeObservationSource(first, name="systemd", source_type="discovery"),
        "ws_systemd_missing",
    )
    state = StateProjector(ledger).project("ws_systemd_missing")

    assert (
        state.get_best_fact(
            "node-a", "systemd_sub_state", dimensions={"unit": "partial.service"}
        )
        is None
    )
    assert (
        state.get_best_fact(
            "node-a", "systemd_unit_file_state", dimensions={"unit": "partial.service"}
        )
        is None
    )
    assert (
        state.get_best_fact(
            "node-a",
            "systemd_unit_file_state",
            dimensions={"unit": "generated.service"},
        ).value
        == "generated"
    )
