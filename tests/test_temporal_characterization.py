from __future__ import annotations

from datetime import datetime, timedelta, timezone

from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.models import Entity, Event
from seed_runtime.projection_store import (
    InMemoryProjectionStore,
    STATE_PROJECTION_NAME,
    STATE_PROJECTION_VERSION,
    project_state_with_cache,
    state_from_payload,
)
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector

BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)
WORKSPACE = "ws_temporal_characterization"


def _fact(
    fact_id: str,
    value: object,
    *,
    predicate: str = "runtime",
    subject_id: str = "svc",
    observed_offset: int = 0,
    source_type: str = "provider",
    confidence: float | None = None,
    evidence_ids: list[str] | None = None,
    expires_at: datetime | None = None,
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
        evidence_ids=evidence_ids if evidence_ids is not None else [f"evd_{fact_id}"],
        observed_at=BASE_TIME + timedelta(minutes=observed_offset),
        expires_at=expires_at,
    )


def _append_fact(ledger: EventLedger, fact: Fact, workspace_id: str = WORKSPACE):
    return ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})


def _entity_event(
    event_id: str, name: str, *, event_timestamp: datetime, workspace_id: str = WORKSPACE
) -> Event:
    return Event(
        id=event_id,
        kind="entity.upserted",
        workspace_id=workspace_id,
        timestamp=event_timestamp,
        payload={
            "entity": to_plain(
                Entity(id="ent_node", kind="host", name=name, aliases=[])
            )
        },
    )


# Part 1 — Event-order characterization


def test_temporal_characterization_projection_follows_append_order_for_updates():
    ledger = EventLedger()
    first = ledger.append(
        "entity.upserted",
        WORKSPACE,
        {"entity": to_plain(Entity(id="ent_node", kind="host", name="node-old"))},
    )
    second = ledger.append(
        "entity.upserted",
        WORKSPACE,
        {"entity": to_plain(Entity(id="ent_node", kind="host", name="node-current"))},
    )

    state = StateProjector(ledger).project(WORKSPACE)

    assert [event.id for event in ledger.list_events(WORKSPACE)] == [first.id, second.id]
    assert state.last_event_id == second.id
    assert state.entities["ent_node"].name == "node-current"


def test_temporal_characterization_out_of_order_event_timestamps_do_not_reorder_projection():
    ledger = EventLedger()
    ledger.extend(
        [
            _entity_event(
                "evt_temporal_newer_timestamp",
                "node-first-appended",
                event_timestamp=BASE_TIME + timedelta(days=1),
            ),
            _entity_event(
                "evt_temporal_older_timestamp",
                "node-second-appended",
                event_timestamp=BASE_TIME,
            ),
        ]
    )

    state = StateProjector(ledger).project(WORKSPACE)

    assert [event.id for event in ledger.list_events(WORKSPACE)] == [
        "evt_temporal_newer_timestamp",
        "evt_temporal_older_timestamp",
    ]
    assert state.last_event_id == "evt_temporal_older_timestamp"
    assert state.entities["ent_node"].name == "node-second-appended"


def test_temporal_characterization_projection_remains_deterministic():
    ledger = EventLedger()
    _append_fact(
        ledger,
        _fact(
            "fact_runtime_docker_a",
            "docker",
            observed_offset=2,
            source_type="discovery",
            confidence=0.70,
        ),
    )
    _append_fact(
        ledger,
        _fact("fact_runtime_systemd", "systemd", observed_offset=1, confidence=0.60),
    )
    _append_fact(
        ledger,
        _fact(
            "fact_runtime_docker_b",
            "docker",
            observed_offset=0,
            source_type="discovery",
            confidence=0.70,
        ),
    )

    first = StateProjector(ledger).project(WORKSPACE)
    second = StateProjector(ledger).project(WORKSPACE)

    assert first == second
    assert first.get_best_fact("svc", "runtime").value == "docker"
    assert first.get_fact_support("svc", "runtime").supporting_fact_ids == [
        "fact_runtime_docker_b",
        "fact_runtime_docker_a",
    ]


# Part 2 — Durable fact characterization


def test_temporal_characterization_durable_current_belief_selection_is_support_based():
    ledger = EventLedger()
    docker_old = _fact(
        "fact_runtime_docker_old",
        "docker",
        observed_offset=0,
        source_type="discovery",
        confidence=0.70,
        evidence_ids=["evd_discovery_old"],
    )
    systemd_newer = _fact(
        "fact_runtime_systemd_newer",
        "systemd",
        observed_offset=10,
        source_type="user",
        confidence=0.90,
        evidence_ids=["evd_user_newer"],
    )
    docker_later_support = _fact(
        "fact_runtime_docker_later_support",
        "docker",
        observed_offset=1,
        source_type="provider",
        confidence=0.70,
        evidence_ids=["evd_provider_later"],
    )
    for fact in (docker_old, systemd_newer, docker_later_support):
        _append_fact(ledger, fact)

    state = StateProjector(ledger).project(WORKSPACE)

    support = state.get_fact_support("svc", "runtime")
    best = state.get_best_fact("svc", "runtime")
    assert support is not None
    assert support.value == "docker"
    assert support.supporting_fact_ids == [docker_old.id, docker_later_support.id]
    assert best is not None
    assert best.value == "docker"


def test_temporal_characterization_older_durable_facts_remain_retained():
    ledger = EventLedger()
    facts = [
        _fact("fact_os_old", "linux", predicate="os", observed_offset=0),
        _fact("fact_os_middle", "freebsd", predicate="os", observed_offset=1),
        _fact("fact_os_current_support", "linux", predicate="os", observed_offset=2),
    ]
    for fact in facts:
        _append_fact(ledger, fact)

    state = StateProjector(ledger).project(WORKSPACE)

    assert set(state.facts) == {fact.id for fact in facts}
    assert state.facts["fact_os_old"].value == "linux"
    assert state.facts["fact_os_middle"].value == "freebsd"


def test_temporal_characterization_durable_support_and_provenance_are_preserved():
    ledger = EventLedger()
    first = _fact(
        "fact_os_first",
        "linux",
        predicate="os",
        observed_offset=0,
        evidence_ids=["evd_os_scan", "evd_host_inventory"],
    )
    second = _fact(
        "fact_os_second",
        "linux",
        predicate="os",
        observed_offset=5,
        evidence_ids=["evd_provider_report"],
    )
    for fact in (first, second):
        _append_fact(ledger, fact)

    state = StateProjector(ledger).project(WORKSPACE)

    support = state.get_fact_support("svc", "os")
    assert support is not None
    assert support.supporting_fact_ids == [first.id, second.id]
    assert support.observed_at == first.observed_at
    assert support.latest_observed_at == second.observed_at
    assert state.facts[first.id].evidence_ids == ["evd_os_scan", "evd_host_inventory"]
    assert state.facts[second.id].evidence_ids == ["evd_provider_report"]


# Part 3 — Measurement characterization


def test_temporal_characterization_measurement_latest_current_uses_observed_time_not_append_order():
    ledger = EventLedger()
    latest_by_observation = _fact("fact_up_observed_later", 1, predicate="up", observed_offset=10)
    appended_later_but_older = _fact("fact_up_observed_older", 0, predicate="up", observed_offset=1)
    _append_fact(ledger, latest_by_observation)
    _append_fact(ledger, appended_later_but_older)

    state = StateProjector(ledger).project(WORKSPACE)

    assert set(state.facts) == {latest_by_observation.id}
    support = state.get_fact_support("svc", "up")
    assert support is not None
    assert support.value == 1
    assert support.support_kind == "current_sample"
    assert support.supporting_fact_ids == [latest_by_observation.id]


def test_temporal_characterization_measurement_debug_history_keeps_recent_samples_only():
    ledger = EventLedger()
    samples = [
        _fact(f"fact_up_{offset}", offset, predicate="up", observed_offset=offset)
        for offset in range(4)
    ]
    for fact in samples:
        _append_fact(ledger, fact)

    state = StateProjector(ledger, measurement_history_limit=3).project(WORKSPACE)

    assert set(state.facts) == {"fact_up_1", "fact_up_2", "fact_up_3"}
    assert state.get_best_fact("svc", "up") == samples[3]
    assert state.get_fact_support("svc", "up").supporting_fact_ids == ["fact_up_3"]


def test_temporal_characterization_measurement_retention_prunes_projection_not_ledger():
    ledger = EventLedger()
    for offset in range(3):
        _append_fact(
            ledger,
            _fact(f"fact_up_retention_{offset}", offset, predicate="up", observed_offset=offset),
        )

    state = StateProjector(ledger).project(WORKSPACE)

    assert set(state.facts) == {"fact_up_retention_2"}
    assert [
        event.payload["fact"]["id"] for event in ledger.list_events(WORKSPACE)
    ] == ["fact_up_retention_0", "fact_up_retention_1", "fact_up_retention_2"]


# Part 4 — Staleness characterization


def test_temporal_characterization_expired_facts_are_retained_but_filtered_by_default():
    ledger = EventLedger()
    expired = _fact(
        "fact_runtime_expired",
        "docker",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    )
    _append_fact(ledger, expired)

    state = StateProjector(ledger).project(WORKSPACE)

    assert set(state.facts) == {expired.id}
    assert state.get_fact_support("svc", "runtime") is None
    assert state.get_best_fact("svc", "runtime") is None
    assert state.get_fact_support("svc", "runtime", include_expired=True).value == "docker"
    assert state.get_best_fact("svc", "runtime", include_expired=True) == expired


def test_temporal_characterization_stale_recommendations_are_read_only_and_deterministic():
    ledger = EventLedger()
    runtime = _fact(
        "fact_runtime_stale",
        "docker",
        predicate="runtime",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    )
    weather = _fact(
        "fact_weather_stale",
        "rain",
        predicate="weather",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=2),
    )
    for fact in (runtime, weather):
        _append_fact(ledger, fact)

    state = StateProjector(ledger).project(WORKSPACE)

    recommendations = state.get_stale_fact_refresh_recommendations()
    assert [recommendation.fact_id for recommendation in recommendations] == [
        weather.id,
        runtime.id,
    ]
    assert [
        recommendation.recommended_capability for recommendation in recommendations
    ] == ["weather_lookup", "service_inspection"]
    assert [event.kind for event in ledger.list_events(WORKSPACE)] == [
        "fact.observed",
        "fact.observed",
    ]


def test_temporal_characterization_stale_facts_do_not_drive_current_state_when_fresh_support_exists():
    ledger = EventLedger()
    expired_docker = _fact(
        "fact_runtime_expired_docker",
        "docker",
        observed_offset=0,
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
        confidence=0.50,
    )
    fresh_systemd = _fact(
        "fact_runtime_fresh_systemd", "systemd", observed_offset=1, confidence=0.95
    )
    for fact in (expired_docker, fresh_systemd):
        _append_fact(ledger, fact)

    state = StateProjector(ledger).project(WORKSPACE)

    assert state.get_best_fact("svc", "runtime") == fresh_systemd
    assert state.get_fact_conflicts() == []
    assert state.get_fact_conflicts(include_expired=True)[0].winning_value == "systemd"
    assert [fact.id for fact in state.get_stale_facts()] == [expired_docker.id]


# Part 5 — ProjectionStore characterization


def test_temporal_characterization_projection_store_caches_latest_current_state_only():
    ledger = EventLedger()
    first_event = _append_fact(ledger, _fact("fact_runtime_initial", "docker"))
    store = InMemoryProjectionStore()
    first_state, first_status = project_state_with_cache(ledger, WORKSPACE, store)
    first_snapshot = store.load_snapshot(
        WORKSPACE, STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
    )

    second_event = _append_fact(
        ledger, _fact("fact_runtime_second", "systemd", observed_offset=1)
    )
    second_state, second_status = project_state_with_cache(ledger, WORKSPACE, store)
    second_snapshot = store.load_snapshot(
        WORKSPACE, STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
    )

    assert first_status.current_last_event_id == first_event.id
    assert first_state.last_event_id == first_event.id
    assert second_status.cache_hit is False
    assert second_status.current_last_event_id == second_event.id
    assert second_snapshot is not None
    assert first_snapshot is not None
    assert second_snapshot.last_event_id == second_event.id
    assert state_from_payload(second_snapshot.state_payload).last_event_id == second_event.id
    assert set(second_state.facts) == {"fact_runtime_initial", "fact_runtime_second"}


def test_temporal_characterization_projection_store_invalidation_follows_latest_event_id():
    ledger = EventLedger()
    store = InMemoryProjectionStore()
    _append_fact(ledger, _fact("fact_runtime_initial", "docker"))
    project_state_with_cache(ledger, WORKSPACE, store)

    next_event = _append_fact(
        ledger, _fact("fact_runtime_added", "docker", observed_offset=1)
    )
    state, status = project_state_with_cache(ledger, WORKSPACE, store)

    assert status.cache_hit is False
    assert status.current_last_event_id == next_event.id
    assert status.snapshot_last_event_id != status.current_last_event_id
    assert state.last_event_id == next_event.id


def test_temporal_characterization_projection_store_has_no_historical_as_of_api():
    store = InMemoryProjectionStore()

    assert not hasattr(store, "load_as_of_event")
    assert not hasattr(store, "load_as_of_timestamp")
    assert not hasattr(store, "project_as_of_event")
    assert not hasattr(store, "project_as_of_timestamp")


def test_temporal_characterization_projection_store_does_not_change_temporal_semantics():
    ledger = EventLedger()
    latest_by_observation = _fact("fact_up_latest_observation", 1, predicate="up", observed_offset=5)
    appended_later_but_older = _fact("fact_up_appended_later", 0, predicate="up", observed_offset=1)
    _append_fact(ledger, latest_by_observation)
    _append_fact(ledger, appended_later_but_older)
    direct_state = StateProjector(ledger).project(WORKSPACE)
    store = InMemoryProjectionStore()

    cached_state, status = project_state_with_cache(ledger, WORKSPACE, store)
    cached_state_again, cache_hit_status = project_state_with_cache(ledger, WORKSPACE, store)

    assert status.cache_hit is False
    assert cache_hit_status.cache_hit is True
    assert cached_state == direct_state
    assert cached_state_again == direct_state
    assert cached_state_again.get_fact_support("svc", "up").supporting_fact_ids == [
        latest_by_observation.id
    ]


def test_book_temporal_view_disclosure_amendment_preserves_current_view_limits():
    amendment = (
        __import__("pathlib")
        .Path("book_of_seed/temporal_standing_and_view_disclosure_amendment_001.md")
        .read_text()
    )

    assert "Latest support or latest measurement sample is not sufficient" in amendment
    assert "not a complete current-standing View by itself" in amendment
    assert "observation navigation index" in amendment
    assert "A View must disclose temporal distinctions constitutive" in amendment
