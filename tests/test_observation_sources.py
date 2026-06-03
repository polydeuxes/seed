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
