"""Tests for catalog-driven deterministic inference projection."""

from datetime import datetime, timezone

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.facts import Fact
from seed_runtime.inference_catalog import InferenceCatalog, InferenceRule
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


OBSERVED_AT = datetime(2026, 6, 4, tzinfo=timezone.utc)


def _fact(
    fact_id: str,
    subject: str,
    predicate: str,
    value: str,
    *,
    confidence: float = 1.0,
) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject,
        predicate=predicate,
        value=value,
        observed_at=OBSERVED_AT,
        source_type="provider",
        confidence=confidence,
    )


def _project(*facts: Fact):
    ledger = EventLedger()
    for fact in facts:
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    return StateProjector(ledger).project("ws")


def test_core_catalog_loads_initial_deterministic_rules():
    catalog = InferenceCatalog.load()

    assert [rule.id for rule in catalog.list_rules()] == [
        "availability_down_health_degraded",
        "availability_up_health_ok",
        "docker_runtime_managed_by",
        "systemd_runtime_managed_by",
    ]
    assert catalog.get("docker_runtime_managed_by").then_value == (
        "docker_container_lifecycle"
    )


def test_runtime_docker_infers_managed_by_with_provenance():
    state = _project(_fact("fact_runtime", "jellyfin", "runtime", "docker"))

    inferred = state.get_best_fact("jellyfin", "managed_by")
    assert inferred is not None
    assert inferred.value == "docker_container_lifecycle"
    assert inferred.source_type == "inferred"
    assert inferred.inferred is True
    assert inferred.source_fact_id == "fact_runtime"
    assert inferred.inference_rule_id == "docker_runtime_managed_by"
    assert inferred.confidence == 0.60


def test_runtime_systemd_infers_managed_by():
    state = _project(_fact("fact_runtime", "sshd", "runtime", "systemd"))

    assert state.get_best_fact("sshd", "managed_by").value == "systemctl_cli"


def test_ambiguous_runtime_docker_systemd_infers_no_managed_by():
    state = _project(
        _fact("fact_docker", "service", "runtime", "docker"),
        _fact("fact_systemd", "service", "runtime", "systemd"),
    )

    assert state.get_best_fact("service", "runtime") is None
    assert state.get_current_facts("service", "managed_by") == []


def test_availability_down_infers_health_degraded():
    state = _project(
        _fact("fact_availability", "node115", "availability_status", "down")
    )

    assert state.get_best_fact("node115", "health_status").value == "degraded"


def test_availability_up_infers_health_ok():
    state = _project(
        _fact("fact_availability", "node115", "availability_status", "up")
    )

    assert state.get_best_fact("node115", "health_status").value == "ok"


def test_inferred_confidence_is_capped_by_source_confidence():
    state = _project(
        _fact(
            "fact_availability",
            "node115",
            "availability_status",
            "down",
            confidence=0.31,
        )
    )

    inferred = state.get_best_fact("node115", "health_status")
    assert inferred.confidence == 0.31


def test_observed_managed_by_beats_inferred_managed_by():
    state = _project(
        _fact("fact_runtime", "jellyfin", "runtime", "docker"),
        _fact("fact_manager", "jellyfin", "managed_by", "custom_cli"),
    )

    manager = state.get_best_fact("jellyfin", "managed_by")
    assert manager.id == "fact_manager"
    assert manager.value == "custom_cli"
    assert manager.inferred is False
    assert not any(
        fact.predicate == "managed_by" for fact in state.inferred_facts.values()
    )



def test_single_cardinality_target_suppresses_conflicting_rule_outputs():
    catalog = InferenceCatalog(
        [
            InferenceRule(
                id="primary_alias_manager",
                name="Primary alias manager",
                when_predicate="alias",
                when_value="primary",
                then_predicate="managed_by",
                then_value="primary_cli",
                confidence=0.8,
                reason="fixture",
            ),
            InferenceRule(
                id="secondary_alias_manager",
                name="Secondary alias manager",
                when_predicate="alias",
                when_value="secondary",
                then_predicate="managed_by",
                then_value="secondary_cli",
                confidence=0.8,
                reason="fixture",
            ),
        ]
    )
    ledger = EventLedger()
    for fact in (
        _fact("fact_primary", "service", "alias", "primary"),
        _fact("fact_secondary", "service", "alias", "secondary"),
    ):
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})

    state = StateProjector(ledger, inference_catalog=catalog).project("ws")

    assert state.get_current_facts("service", "managed_by") == []


def test_sqlite_reopen_preserves_inferred_projection(tmp_path):
    db = tmp_path / "events.db"
    ledger = SQLiteEventLedger(str(db))
    source = _fact("fact_runtime", "jellyfin", "runtime", "docker")
    ledger.append("fact.observed", "ws", {"fact": to_plain(source)})
    first = StateProjector(ledger).project("ws").get_best_fact(
        "jellyfin", "managed_by"
    )
    ledger.close()

    reopened = SQLiteEventLedger(str(db))
    second = StateProjector(reopened).project("ws").get_best_fact(
        "jellyfin", "managed_by"
    )
    reopened.close()

    assert second == first
    assert second.source_fact_id == source.id
    assert second.inference_rule_id == "docker_runtime_managed_by"
