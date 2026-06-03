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
) -> Fact:
    return Fact(
        id=fact_id,
        subject_id="svc_ssh",
        predicate=predicate,
        value=value,
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
        support for support in state.fact_supports if support.value == "docker_container_lifecycle"
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
    assert state.get_best_fact(
        "svc_ssh", "service.running", include_expired=True
    ) == expired


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
