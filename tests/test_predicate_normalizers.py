import json
from datetime import datetime, timezone

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.observation_normalizers import DEFAULT_OBSERVATION_NORMALIZATION_PIPELINE
from seed_runtime.observation_sources import FakeObservationSource, ObservationCollectionService
from seed_runtime.observations import Observation, ObservationIngestor
from seed_runtime.predicate_catalog import PredicateCatalog
from seed_runtime.predicate_normalizers import PredicateNormalizer
from seed_runtime.state import StateProjector


OBSERVED_AT = datetime(2026, 1, 1, tzinfo=timezone.utc)
ENDPOINT = "192.168.254.115:9100"


def _prometheus(predicate: str, value: object, *, metadata=None) -> Observation:
    return Observation(
        id=f"obs_{predicate}_{value}",
        source_type="provider",
        observed_at=OBSERVED_AT,
        subject=ENDPOINT,
        predicate=predicate,
        value=value,
        confidence=0.95,
        metadata={"source_name": "prometheus", **(metadata or {})},
    )


@pytest.mark.parametrize("raw, canonical", [(1, "up"), (0, "down")])
def test_prometheus_up_is_normalized_to_availability_status(raw, canonical):
    original = _prometheus("up", raw)

    normalized = PredicateNormalizer().normalize([original])

    assert len(normalized) == 1
    derived = normalized[0]
    assert (derived.predicate, derived.value) == ("availability_status", canonical)
    assert derived.metadata["derived"] is True
    assert derived.metadata["normalizer"] == "predicate"
    assert derived.metadata["original_predicate"] == "up"
    assert derived.metadata["canonical_predicate"] == "availability_status"
    assert derived.metadata["original_value"] == raw


@pytest.mark.parametrize(
    ("raw", "canonical"),
    [
        ("filesystem_avail_bytes", "filesystem_free_bytes"),
        ("node_filesystem_avail_bytes", "filesystem_free_bytes"),
        ("filesystem_size_bytes", "filesystem_total_bytes"),
        ("node_filesystem_size_bytes", "filesystem_total_bytes"),
    ],
)
def test_prometheus_filesystem_predicates_are_normalized(raw, canonical):
    derived = PredicateNormalizer().normalize([_prometheus(raw, 1024)])[0]

    assert (derived.predicate, derived.value) == (canonical, 1024)


def test_default_pipeline_preserves_original_and_adds_canonical_observation():
    original = _prometheus("up", 1)

    normalized = DEFAULT_OBSERVATION_NORMALIZATION_PIPELINE.normalize([original])

    assert normalized[0] is original
    assert {(item.predicate, item.value) for item in normalized} == {
        ("up", 1),
        ("availability_status", "up"),
    }


def test_unknown_predicate_passes_through_unchanged():
    original = _prometheus("provider_specific_metric", 7)

    assert DEFAULT_OBSERVATION_NORMALIZATION_PIPELINE.normalize([original]) == [original]


def test_canonical_availability_is_measurement_and_endpoint_scoped():
    original = _prometheus(
        "up", 1, metadata={"hostname": "node115", "instance": ENDPOINT}
    )
    ledger = EventLedger()

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource([original]), "ws_predicates"
    )
    state = StateProjector(ledger).project("ws_predicates")

    assert state.get_best_fact("node115", "availability_status") is None
    assert state.get_best_fact(ENDPOINT, "availability_status").value == "up"
    support = state.get_fact_support(ENDPOINT, "availability_status")
    assert support.predicate_semantics == "measurement"


def test_custom_catalog_drives_normalization(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text(
        json.dumps(
            {
                "predicates": [
                    {
                        "predicate": "service_health",
                        "kind": "measurement",
                        "value_type": "enum",
                        "allowed_values": ["healthy"],
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
    observation = _prometheus("health", "healthy").model_copy(
        update={"metadata": {"source_name": "custom"}}
    )

    derived = PredicateNormalizer(PredicateCatalog.load(path)).normalize([observation])

    assert [(item.predicate, item.value) for item in derived] == [
        ("service_health", "healthy")
    ]
