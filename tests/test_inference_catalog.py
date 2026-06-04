import json
from datetime import datetime, timezone

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.inference_catalog import InferenceCatalog, InferenceRule
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def test_builtin_inference_catalog_contains_deterministic_rules():
    catalog = InferenceCatalog.load()

    assert [rule.id for rule in catalog.list_inference_rules()] == [
        "runtime_docker_managed_by_container_lifecycle",
        "runtime_systemd_managed_by_systemctl",
    ]
    assert [rule.id for rule in catalog.for_source_predicate("runtime")] == [
        "runtime_docker_managed_by_container_lifecycle",
        "runtime_systemd_managed_by_systemctl",
    ]


def test_inference_catalog_requires_unique_rule_ids():
    rule = InferenceRule(
        id="duplicate",
        source_predicate="a",
        source_value="one",
        target_predicate="b",
        target_value="two",
    )

    with pytest.raises(ValueError, match="IDs must be unique"):
        InferenceCatalog([rule, rule])


def test_inference_catalog_validates_confidence_cap(tmp_path):
    path = tmp_path / "inference.json"
    path.write_text(
        json.dumps(
            {
                "inference_rules": [
                    {
                        "id": "bad",
                        "source_predicate": "a",
                        "source_value": "one",
                        "target_predicate": "b",
                        "target_value": "two",
                        "confidence_cap": 1.1,
                    }
                ]
            }
        )
    )

    with pytest.raises(ValueError, match="confidence_cap"):
        InferenceCatalog.load(path)


def test_custom_inference_catalog_drives_projection():
    catalog = InferenceCatalog(
        [
            InferenceRule(
                id="a_to_b",
                source_predicate="a",
                source_value="one",
                target_predicate="b",
                target_value="two",
                confidence_cap=0.5,
            )
        ]
    )
    source = Fact(
        id="fact_source",
        subject_id="entity",
        predicate="a",
        value="one",
        observed_at=datetime(2026, 6, 4, tzinfo=timezone.utc),
        confidence=0.9,
    )
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(source)})

    state = StateProjector(ledger, inference_catalog=catalog).project("ws")

    inferred = state.get_best_fact("entity", "b")
    assert inferred is not None
    assert inferred.value == "two"
    assert inferred.inference_rule_id == "a_to_b"
    assert inferred.source_fact_id == source.id
    assert inferred.confidence == 0.5
    assert inferred.confidence_cap == 0.5
