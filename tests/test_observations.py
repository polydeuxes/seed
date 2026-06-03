from datetime import datetime, timedelta, timezone

from seed_runtime.events import EventLedger
from seed_runtime.observations import Observation, ObservationIngestor
from seed_runtime.state import StateProjector


BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_observation_becomes_fact():
    ledger = EventLedger()
    observation = Observation(
        id="obs_cpu",
        source_type="provider",
        observed_at=BASE_TIME,
        subject="node115",
        predicate="cpu.count",
        value=8,
        confidence=0.82,
    )

    fact = ObservationIngestor(ledger).ingest(observation, "ws_obs")
    state = StateProjector(ledger).project("ws_obs")

    assert fact.id in state.facts
    projected = state.facts[fact.id]
    assert projected.subject_id == "node115"
    assert projected.predicate == "cpu.count"
    assert projected.value == 8
    assert projected.observed_at == BASE_TIME


def test_observation_provenance_preserved():
    ledger = EventLedger()
    observation = Observation(
        id="obs_runtime",
        source_type="discovery",
        observed_at=BASE_TIME,
        subject="jellyfin",
        predicate="runtime",
        value="docker",
        confidence=0.91,
        metadata={"scanner": "inventory"},
    )

    fact = ObservationIngestor(ledger).ingest(observation, "ws_obs")
    state = StateProjector(ledger).project("ws_obs")

    assert observation.id in state.observations
    projected_fact = state.facts[fact.id]
    evidence = state.evidence[projected_fact.evidence_ids[0]]
    assert projected_fact.source_type == "discovery"
    assert evidence.source == "observation:discovery"
    assert evidence.kind == "observation"
    assert evidence.payload["observation_id"] == observation.id
    assert evidence.payload["source_type"] == "discovery"
    assert evidence.payload["metadata"] == {"scanner": "inventory"}


def test_observation_confidence_preserved():
    ledger = EventLedger()
    observation = Observation(
        id="obs_confidence",
        source_type="imported",
        observed_at=BASE_TIME,
        subject="service-a",
        predicate="owner",
        value="team-platform",
        confidence=0.37,
    )

    fact = ObservationIngestor(ledger).ingest(observation, "ws_obs")
    state = StateProjector(ledger).project("ws_obs")

    projected_fact = state.facts[fact.id]
    evidence = state.evidence[projected_fact.evidence_ids[0]]
    assert projected_fact.confidence == 0.37
    assert evidence.confidence == 0.37


def test_observation_support_aggregation_still_works():
    ledger = EventLedger()
    first = Observation(
        id="obs_provider",
        source_type="provider",
        observed_at=BASE_TIME,
        subject="svc_ssh",
        predicate="service.running",
        value=True,
        confidence=0.70,
    )
    second = Observation(
        id="obs_discovery",
        source_type="discovery",
        observed_at=BASE_TIME + timedelta(minutes=1),
        subject="svc_ssh",
        predicate="service.running",
        value=True,
        confidence=0.60,
    )

    first_fact = ObservationIngestor(ledger).ingest(first, "ws_obs")
    second_fact = ObservationIngestor(ledger).ingest(second, "ws_obs")
    state = StateProjector(ledger).project("ws_obs")

    support = state.get_fact_support("svc_ssh", "service.running")
    assert support is not None
    assert support.value is True
    assert support.supporting_fact_ids == [first_fact.id, second_fact.id]
    assert support.source_types == ["provider", "discovery"]
    assert support.confidence > first.confidence
    assert support.confidence > second.confidence
    assert support.observed_at == first.observed_at
    assert support.latest_observed_at == second.observed_at
