from datetime import datetime, timezone

from seed_runtime.events import EventLedger
from seed_runtime.observation_normalizers import (
    EndpointAliasNormalizer,
    ObservationNormalizationPipeline,
)
from seed_runtime.observation_sources import (
    FakeObservationSource,
    ObservationCollectionService,
)
from seed_runtime.observations import Observation, ObservationIngestor
from seed_runtime.state import StateProjector


OBSERVED_AT = datetime(2026, 1, 1, tzinfo=timezone.utc)
ENDPOINT = "192.168.254.115:9100"


def _observation(
    observation_id: str,
    *,
    subject: str = ENDPOINT,
    predicate: str = "up",
    value: object = 1,
    confidence: float = 0.95,
    metadata: dict[str, object] | None = None,
) -> Observation:
    return Observation(
        id=observation_id,
        source_type="provider",
        observed_at=OBSERVED_AT,
        subject=subject,
        predicate=predicate,
        value=value,
        confidence=confidence,
        metadata=metadata or {},
    )


def _default_pipeline() -> ObservationNormalizationPipeline:
    return ObservationNormalizationPipeline([EndpointAliasNormalizer()])


def test_generic_hostname_and_instance_create_alias_observation():
    original = _observation(
        "obs_generic",
        metadata={"hostname": "node115", "instance": ENDPOINT},
    )

    normalized = _default_pipeline().normalize([original])

    assert normalized[0] is original
    assert len(normalized) == 2
    alias = normalized[1]
    assert (alias.subject, alias.predicate, alias.value) == (
        "node115",
        "alias",
        ENDPOINT,
    )
    assert alias.metadata == {
        "hostname": "node115",
        "instance": ENDPOINT,
        "derived": True,
        "derived_from_observation_id": original.id,
        "normalizer": "endpoint_alias",
        "original_subject": ENDPOINT,
    }


def test_prometheus_nodename_and_instance_create_source_specific_alias():
    original = _observation(
        "obs_prometheus",
        predicate="os",
        value="linux",
        metadata={
            "source_name": "prometheus",
            "nodename": "node115",
            "instance": ENDPOINT,
        },
    )

    alias = _default_pipeline().normalize([original])[1]

    assert (alias.subject, alias.predicate, alias.value) == (
        "node115",
        "prometheus_instance",
        ENDPOINT,
    )


def test_missing_hostname_or_nodename_creates_no_alias():
    original = _observation("obs_no_host", metadata={"instance": ENDPOINT})

    assert _default_pipeline().normalize([original]) == [original]


def test_pipeline_avoids_duplicate_derived_observations():
    alias = _observation("obs_derived_alias", subject="node115", predicate="alias", value=ENDPOINT)

    class DuplicateNormalizer:
        name = "duplicate"

        def normalize(self, observations: list[Observation]) -> list[Observation]:
            return [alias, alias.model_copy(update={"id": "obs_duplicate_alias"})]

    normalized = ObservationNormalizationPipeline([DuplicateNormalizer()]).normalize([])

    assert normalized == [alias]


def test_duplicate_source_observations_create_one_alias_with_provenance():
    first = _observation(
        "obs_up",
        metadata={"hostname": "node115", "instance": ENDPOINT},
    )
    second = _observation(
        "obs_os",
        predicate="os",
        value="linux",
        confidence=0.8,
        metadata={"hostname": "node115", "instance": ENDPOINT},
    )

    normalized = _default_pipeline().normalize([first, second])

    assert normalized[:2] == [first, second]
    assert len(normalized) == 3
    alias = normalized[2]
    assert alias.metadata["derived_from_observation_id"] == first.id
    assert alias.metadata["derived_from_observation_ids"] == [first.id, second.id]
    assert alias.confidence == 0.8


def test_alias_derivation_ingests_originals_and_enables_alias_aware_query():
    original = _observation(
        "obs_alias_query",
        metadata={"hostname": "node115", "instance": ENDPOINT},
    )
    ledger = EventLedger()
    service = ObservationCollectionService(ObservationIngestor(ledger))

    facts = service.collect(FakeObservationSource([original]), "ws_alias_query")
    state = StateProjector(ledger).project("ws_alias_query")

    assert len(facts) == 2
    assert state.observations[original.id].predicate == "up"
    assert state.get_best_fact("node115", "up").value == 1
    assert state.get_best_fact(ENDPOINT, "up").value == 1


def test_collection_can_skip_optional_normalization_pipeline():
    original = _observation(
        "obs_without_pipeline",
        metadata={"hostname": "node115", "instance": ENDPOINT},
    )
    ledger = EventLedger()
    service = ObservationCollectionService(
        ObservationIngestor(ledger), normalization_pipeline=None
    )

    facts = service.collect(FakeObservationSource([original]), "ws_without_pipeline")

    assert len(facts) == 1
    assert facts[0].predicate == "up"


def test_derived_alias_preserves_source_type_and_bounded_confidence():
    original = _observation(
        "obs_provenance",
        confidence=0.73,
        metadata={"hostname": "node115", "endpoint": ENDPOINT},
    )

    alias = _default_pipeline().normalize([original])[1]

    assert alias.source_type == original.source_type
    assert alias.confidence <= original.confidence
    assert alias.metadata["derived"] is True
    assert alias.metadata["derived_from_observation_id"] == original.id
