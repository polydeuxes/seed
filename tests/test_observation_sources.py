import json
from datetime import datetime, timezone

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.observation_sources import (
    FakeObservationSource,
    JsonObservationSource,
    ObservationCollectionService,
)
from seed_runtime.observations import Observation, ObservationIngestor
from seed_runtime.state import StateProjector

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
              "subject": "jellyfin",
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
    assert fact.subject_id == "jellyfin"
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
              "subject": "jellyfin",
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
              "subject": "jellyfin",
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
        subject="jellyfin",
        predicate="runtime",
        value="docker",
    )
    second = Observation(
        id="obs_roundtrip_discovery",
        source_type="discovery",
        observed_at=BASE_TIME,
        subject="jellyfin",
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

    support = imported_state.get_fact_support("jellyfin", "runtime")
    assert support is not None
    assert support.value == "docker"
    assert len(support.supporting_fact_ids) == 2
    assert support.source_types == ["provider", "discovery"]
    assert sorted(
        (fact.subject_id, fact.predicate, fact.value, fact.source_type, fact.confidence)
        for fact in imported_state.observed_facts.values()
    ) == [
        ("jellyfin", "runtime", "docker", "discovery", 0.74),
        ("jellyfin", "runtime", "docker", "provider", 0.86),
    ]


def test_export_observations_json_includes_expired_fact_expires_at():
    ledger = EventLedger()
    expired_at = datetime(2025, 1, 1, tzinfo=timezone.utc)
    observation = Observation(
        id="obs_expired_export",
        source_type="provider",
        observed_at=BASE_TIME,
        subject="jellyfin",
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
            subject="jellyfin",
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

    assert "fact_inferred_jellyfin_managed_by_docker_container_lifecycle" in (
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
    monkeypatch.setattr(sources.shutil, "disk_usage", lambda path: DiskUsage())

    observations = LocalHostObservationSource().collect()

    assert [(obs.subject, obs.predicate, obs.value) for obs in observations] == [
        ("node-a", "os", "linux"),
        ("node-a", "architecture", "x86_64"),
        ("node-a", "disk_total_bytes", 1000),
        ("node-a", "disk_free_bytes", 250),
    ]
    assert {obs.source_type for obs in observations} == {"discovery"}
    assert all(obs.metadata["shell_execution"] is False for obs in observations)


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
                "result": [{"metric": {"instance": "node-a:9100"}, "value": [1, "1"]}],
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
        ("node-a:9100", "up", 1),
        ("node-a:9100", "os", "linux"),
        ("node-a:9100", "filesystem_avail_bytes", 512),
        ("node-a:9100", "filesystem_size_bytes", 1024),
    ]
    assert observations[0].dimensions == {}
    assert observations[2].dimensions == {
        "mountpoint": "/",
        "device": "/dev/sda1",
        "fstype": "ext4",
    }
    assert observations[3].dimensions == observations[2].dimensions
    assert {obs.source_type for obs in observations} == {"provider"}
    assert {obs.metadata["source_name"] for obs in observations} == {"prometheus"}
    assert [method for _, method, _ in requested_urls] == ["GET"] * 4
    assert [timeout for _, _, timeout in requested_urls] == [2.5] * 4
    assert [url.rsplit("query=", 1)[1] for url, _, _ in requested_urls] == list(
        PrometheusObservationSource.SAFE_QUERIES
    )


def test_prometheus_source_unreachable_fails_gracefully(monkeypatch):
    from seed_runtime import observation_sources as sources
    from seed_runtime.observation_sources import PrometheusObservationSource

    def fake_urlopen(request, timeout):
        raise OSError("network unreachable")

    monkeypatch.setattr(sources, "urlopen", fake_urlopen)

    source = PrometheusObservationSource("http://prom.example:9090", timeout_seconds=1)

    assert source.collect() == []
    assert "network unreachable" in (source.last_error or "")


def test_collection_normalized_alias_resolves_best_fact_by_stable_name():
    ledger = EventLedger()
    source = FakeObservationSource(
        [
            _observation(
                "obs_generic_up",
                subject="192.168.254.115:9100",
                predicate="up",
                value=1,
                metadata={
                    "hostname": "node115",
                    "instance": "192.168.254.115:9100",
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
    assert state.get_best_fact("node115", "up").value == 1
    assert any(
        fact.subject_id == "node115"
        and fact.predicate == "generic_instance"
        and fact.value == "192.168.254.115:9100"
        for fact in state.facts.values()
    )


def test_prometheus_nodename_creates_prometheus_instance_alias_via_normalizer(
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
        metric = {"instance": "192.168.254.115:9100"}
        if query == "node_uname_info":
            metric.update({"nodename": "node115", "sysname": "Linux"})
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
    assert aliases[0].subject_id == "node115"
    assert aliases[0].value == "192.168.254.115:9100"
    assert state.get_best_fact("node115", "up").value == 1
