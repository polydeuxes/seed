from datetime import datetime, timedelta, timezone

from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact, FactSupport
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector

BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _fact(
    fact_id: str,
    value: object,
    *,
    source_type: str = "provider",
    confidence: float | None = None,
    observed_offset: int = 0,
    evidence_ids: list[str] | None = None,
    predicate: str = "service.running",
    expires_at: datetime | None = None,
    subject_id: str = "svc_ssh",
    dimensions: dict[str, str] | None = None,
) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject_id,
        predicate=predicate,
        value=value,
        dimensions=dimensions or {},
        source_type=source_type,
        confidence=confidence,
        evidence_ids=evidence_ids or [f"evd_{fact_id}"],
        observed_at=BASE_TIME + timedelta(minutes=observed_offset),
        expires_at=expires_at,
        inferred=source_type == "inferred",
    )


def _project(*facts: Fact):
    ledger = EventLedger()
    workspace_id = "ws_support"
    for fact in facts:
        kind = "fact.inferred" if fact.inferred else "fact.observed"
        ledger.append(kind, workspace_id, {"fact": to_plain(fact)})
    return StateProjector(ledger).project(workspace_id)


def test_two_sources_supporting_same_value_raise_aggregate_confidence():
    first = _fact("fact_provider", True, source_type="provider", confidence=0.70)
    second = _fact(
        "fact_discovery",
        True,
        source_type="discovery",
        confidence=0.60,
        observed_offset=1,
    )

    state = _project(first, second)

    support = state.get_fact_support("svc_ssh", "service.running")
    assert isinstance(support, FactSupport)
    assert support.value is True
    assert support.confidence > first.confidence
    assert support.confidence > second.confidence
    assert support.supporting_fact_ids == [first.id, second.id]
    assert support.source_types == ["provider", "discovery"]
    assert support.observed_at == first.observed_at
    assert support.latest_observed_at == second.observed_at


def test_conflicting_value_with_lower_support_loses():
    true_provider = _fact(
        "fact_provider", True, source_type="provider", confidence=0.68
    )
    true_discovery = _fact(
        "fact_discovery",
        True,
        source_type="discovery",
        confidence=0.55,
        observed_offset=1,
    )
    false_user = _fact("fact_user", False, source_type="user", confidence=0.72)

    state = _project(true_provider, true_discovery, false_user)

    best = state.get_best_fact("svc_ssh", "service.running")
    assert best is not None
    assert best.value is True
    assert state.fact_conflicts[0].best_fact_id in {true_provider.id, true_discovery.id}
    assert state.fact_conflicts[0].conflicting_fact_ids == [false_user.id]


def test_conflicting_value_with_higher_confidence_and_support_wins():
    true_provider = _fact(
        "fact_provider_true", True, source_type="provider", confidence=0.70
    )
    false_provider = _fact(
        "fact_provider_false", False, source_type="provider", confidence=0.80
    )
    false_discovery = _fact(
        "fact_discovery_false",
        False,
        source_type="discovery",
        confidence=0.75,
        observed_offset=1,
    )

    state = _project(true_provider, false_provider, false_discovery)

    best_support = state.get_fact_support("svc_ssh", "service.running")
    best = state.get_best_fact("svc_ssh", "service.running")
    assert best_support is not None
    assert best_support.value is False
    assert best is not None
    assert best.value is False
    assert state.fact_conflicts[0].conflicting_fact_ids == [true_provider.id]


def test_inferred_only_support_is_weaker_than_observed_provider_support():
    inferred = _fact(
        "fact_inferred",
        "docker_container_lifecycle",
        source_type="inferred",
        confidence=0.95,
        predicate="managed_by",
    )
    provider = _fact(
        "fact_provider",
        "systemctl_cli",
        source_type="provider",
        confidence=0.55,
        predicate="managed_by",
    )

    state = _project(inferred, provider)

    inferred_support = next(
        support
        for support in state.fact_supports
        if support.value == "docker_container_lifecycle"
    )
    provider_support = next(
        support for support in state.fact_supports if support.value == "systemctl_cli"
    )
    best = state.get_best_fact("svc_ssh", "managed_by")
    assert inferred_support.confidence < provider_support.confidence
    assert best is not None
    assert best.value == "systemctl_cli"


def test_fact_support_preserves_provenance_without_verified_stamp():
    first = _fact("fact_provider", True, source_type="provider", confidence=0.70)
    second = _fact(
        "fact_discovery",
        True,
        source_type="discovery",
        confidence=0.60,
        observed_offset=1,
        evidence_ids=["evd_discovery_a", "evd_discovery_b"],
    )

    state = _project(first, second)

    support = state.get_fact_support("svc_ssh", "service.running")
    assert support is not None
    assert support.supporting_fact_ids == [first.id, second.id]
    assert set(state.facts[first.id].evidence_ids) == {"evd_fact_provider"}
    assert set(state.facts[second.id].evidence_ids) == {
        "evd_discovery_a",
        "evd_discovery_b",
    }
    assert not hasattr(support, "verified")
    assert not hasattr(state.facts[first.id], "verified")


def test_unexpired_fact_still_counts():
    unexpired = _fact(
        "fact_unexpired",
        True,
        confidence=0.70,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
    )

    state = _project(unexpired)

    support = state.get_fact_support("svc_ssh", "service.running")
    assert support is not None
    assert support.value is True
    assert support.supporting_fact_ids == [unexpired.id]
    assert state.get_best_fact("svc_ssh", "service.running") == unexpired


def test_expired_support_is_visible_only_when_include_expired_true():
    expired = _fact(
        "fact_expired",
        True,
        confidence=0.70,
        expires_at=datetime.now(timezone.utc) - timedelta(seconds=1),
    )

    state = _project(expired)

    assert state.get_fact_supports("svc_ssh", "service.running") == []
    assert state.get_fact_support("svc_ssh", "service.running") is None
    assert state.get_best_fact("svc_ssh", "service.running") is None

    supports = state.get_fact_supports(
        "svc_ssh", "service.running", include_expired=True
    )
    assert len(supports) == 1
    assert supports[0].value is True
    assert supports[0].supporting_fact_ids == [expired.id]
    assert (
        state.get_best_fact("svc_ssh", "service.running", include_expired=True)
        == expired
    )


def test_conflicts_ignore_expired_facts_by_default():
    expired_docker = _fact(
        "fact_expired_docker",
        "docker",
        predicate="runtime",
        expires_at=datetime.now(timezone.utc) - timedelta(seconds=1),
    )
    fresh_systemd = _fact(
        "fact_fresh_systemd",
        "systemd",
        predicate="runtime",
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
    )

    state = _project(expired_docker, fresh_systemd)

    assert state.fact_conflicts == []
    assert state.get_best_fact("svc_ssh", "runtime") == fresh_systemd
    supports = state.get_fact_supports("svc_ssh", "runtime", include_expired=True)
    assert {support.value for support in supports} == {"docker", "systemd"}


def test_measurement_up_old_zero_new_one_prefers_latest_sample():
    old_down = _fact("fact_up_old_down", 0, predicate="up", observed_offset=0)
    new_up = _fact("fact_up_new_up", 1, predicate="up", observed_offset=1)

    state = _project(old_down, new_up)

    best = state.get_best_fact("svc_ssh", "up")
    support = state.get_fact_support("svc_ssh", "up")
    assert best == new_up
    assert support is not None
    assert support.value == 1
    assert support.predicate_semantics == "measurement"
    assert support.support_kind == "current_sample"
    assert support.supporting_fact_ids == [new_up.id]


def test_measurement_up_old_one_new_zero_prefers_latest_sample():
    old_up = _fact("fact_up_old_up", 1, predicate="up", observed_offset=0)
    new_down = _fact("fact_up_new_down", 0, predicate="up", observed_offset=1)

    state = _project(old_up, new_down)

    best = state.get_best_fact("svc_ssh", "up")
    support = state.get_fact_support("svc_ssh", "up")
    assert best == new_down
    assert support is not None
    assert support.value == 0
    assert support.predicate_semantics == "measurement"
    assert support.support_kind == "current_sample"
    assert support.supporting_fact_ids == [new_down.id]


def test_measurement_repeated_values_do_not_strengthen_confidence_like_durable_facts():
    first = _fact("fact_up_first", 1, predicate="up", confidence=0.70)
    second = _fact(
        "fact_up_second",
        1,
        predicate="up",
        confidence=0.60,
        observed_offset=1,
    )

    state = _project(first, second)

    support = state.get_fact_support("svc_ssh", "up")
    assert support is not None
    assert support.confidence == second.confidence
    assert support.supporting_fact_ids == [second.id]


def test_runtime_docker_repeated_observations_still_aggregate_support():
    first = _fact("fact_runtime_first", "docker", predicate="runtime", confidence=0.70)
    second = _fact(
        "fact_runtime_second",
        "docker",
        predicate="runtime",
        confidence=0.60,
        observed_offset=1,
    )

    state = _project(first, second)

    support = state.get_fact_support("svc_ssh", "runtime")
    assert support is not None
    assert support.predicate_semantics == "durable"
    assert support.support_kind == "aggregate"
    assert support.confidence > first.confidence
    assert support.confidence > second.confidence
    assert support.supporting_fact_ids == [first.id, second.id]


def test_canonical_measurement_uses_current_sample_across_alias_component():
    first_alias = _fact(
        "fact_alias_9100",
        "192.168.254.115:9100",
        predicate="alias",
        subject_id="node115",
    )
    second_alias = _fact(
        "fact_alias_9200",
        "192.168.254.115:9200",
        predicate="alias",
        subject_id="node115",
    )
    endpoint_up = _fact(
        "fact_endpoint_up",
        "up",
        predicate="availability_status",
        subject_id="192.168.254.115:9200",
    )
    endpoint_down = _fact(
        "fact_endpoint_z_down",
        "down",
        predicate="availability_status",
        subject_id="192.168.254.115:9100",
    )

    state = _project(first_alias, second_alias, endpoint_up, endpoint_down)

    best = state.get_best_fact("node115", "availability_status")
    support = state.get_fact_support("node115", "availability_status")
    assert best == endpoint_down
    assert support is not None
    assert support.subject == "node115"
    assert support.value == "down"
    assert support.supporting_fact_ids == [endpoint_down.id]
    assert (
        state.get_best_fact("node115", "availability_status", resolve_aliases=False)
        is None
    )


def test_alias_resolution_still_works_for_measurements():
    alias = _fact(
        "fact_alias",
        "node.example.com:9100",
        predicate="alias",
        subject_id="node",
    )
    old_down = _fact(
        "fact_node_old_down",
        0,
        predicate="up",
        subject_id="node.example.com:9100",
    )
    new_up = _fact(
        "fact_node_new_up",
        1,
        predicate="up",
        subject_id="node.example.com:9100",
        observed_offset=1,
    )

    state = _project(alias, old_down, new_up)

    best = state.get_best_fact("node", "up")
    support = state.get_fact_support("node", "up")
    assert best == new_up
    assert support is not None
    assert support.subject == "node"
    assert support.value == 1
    assert support.support_kind == "current_sample"


def test_default_projection_retains_only_latest_measurement_fact_and_all_events():
    old = _fact("fact_old", 10, predicate="filesystem_avail_bytes")
    current = _fact(
        "fact_current", 20, predicate="filesystem_avail_bytes", observed_offset=1
    )
    ledger = EventLedger()
    for fact in (old, current):
        ledger.append("fact.observed", "ws_retention", {"fact": to_plain(fact)})

    state = StateProjector(ledger).project("ws_retention")

    assert set(state.facts) == {current.id}
    assert len(ledger.list_events("ws_retention")) == 2


def test_requested_measurement_debug_history_retains_recent_n_but_current_is_latest():
    samples = [
        _fact(f"fact_{offset}", offset, predicate="up", observed_offset=offset)
        for offset in range(4)
    ]
    ledger = EventLedger()
    for fact in samples:
        ledger.append("fact.observed", "ws_history", {"fact": to_plain(fact)})

    state = StateProjector(ledger, measurement_history_limit=3).project("ws_history")

    assert set(state.facts) == {"fact_1", "fact_2", "fact_3"}
    assert state.get_fact_support("svc_ssh", "up").supporting_fact_ids == ["fact_3"]


def test_measurement_retention_is_per_alias_component_predicate_and_dimensions():
    alias = _fact("fact_alias", "node:9100", predicate="alias", subject_id="node")
    root_old = _fact(
        "fact_root_old",
        10,
        predicate="filesystem_avail_bytes",
        subject_id="node",
        dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
    )
    root_new = _fact(
        "fact_root_new",
        20,
        predicate="filesystem_avail_bytes",
        subject_id="node:9100",
        observed_offset=1,
        dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
    )
    data = _fact(
        "fact_data",
        30,
        predicate="filesystem_avail_bytes",
        subject_id="node:9100",
        dimensions={"mountpoint": "/data", "device": "/dev/sdb1", "fstype": "xfs"},
    )

    state = _project(alias, root_old, root_new, data)

    assert set(state.facts) == {alias.id, root_new.id, data.id}
    root = state.get_fact_support(
        "node",
        "filesystem_avail_bytes",
        dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
    )
    assert root is not None
    assert root.value == 20
    assert len(state.get_fact_supports("node", "filesystem_avail_bytes")) == 2


def test_durable_fact_history_still_aggregates_after_projection():
    first = _fact("fact_first", "linux", predicate="os", confidence=0.6)
    second = _fact(
        "fact_second", "linux", predicate="os", confidence=0.7, observed_offset=1
    )

    state = _project(first, second)

    assert set(state.facts) == {first.id, second.id}
    assert state.get_fact_support("svc_ssh", "os").supporting_fact_ids == [
        first.id,
        second.id,
    ]


def test_measurement_history_limit_must_be_positive():
    import pytest

    with pytest.raises(ValueError, match="at least 1"):
        StateProjector(EventLedger(), measurement_history_limit=0)


def test_measurement_projection_prunes_old_observation_provenance_not_events():
    from seed_runtime.observations import Observation, ObservationIngestor

    ledger = EventLedger()
    ingestor = ObservationIngestor(ledger)
    for offset, value in enumerate((0, 1)):
        ingestor.ingest(
            Observation(
                id=f"obs_{offset}",
                source_type="provider",
                observed_at=BASE_TIME + timedelta(minutes=offset),
                subject="node",
                predicate="up",
                value=value,
            ),
            "ws_provenance_retention",
        )

    state = StateProjector(ledger).project("ws_provenance_retention")

    assert set(state.observations) == {"obs_1"}
    assert len(state.evidence) == 1
    assert len(state.facts) == 1
    assert len(ledger.list_events("ws_provenance_retention")) == 6
