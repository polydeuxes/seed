from __future__ import annotations

from datetime import datetime, timezone

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.execution_status import RecordingExecutionStatusConsumer
from seed_runtime.fact_index import build_fact_index, load_or_build_fact_index
from seed_runtime.facts import Fact
from seed_runtime.models import Event
from seed_runtime.projection_store import (
    FACT_INDEX_NAME,
    FACT_INDEX_VERSION,
    InMemoryProjectionStore,
    SQLiteProjectionStore,
    STATE_PROJECTION_NAME,
    STATE_PROJECTION_VERSION,
    project_state_with_cache,
)
from seed_runtime.serialization import to_plain
from scripts.seed_local import format_current_facts


def _fact(fact_id: str, subject: str, predicate: str, value: str) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject,
        predicate=predicate,
        value=value,
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


def _append_fact(ledger: EventLedger, workspace_id: str, fact: Fact):
    return ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})


def _projected_state_with_store():
    ledger = EventLedger()
    event = _append_fact(
        ledger, "ws", _fact("fact_runtime", "svc", "runtime", "docker")
    )
    _append_fact(
        ledger,
        "ws",
        _fact("fact_package", "node", "package_installed", "openssh-client"),
    )
    store = InMemoryProjectionStore()
    state, _status = project_state_with_cache(ledger, "ws", store)
    return ledger, store, state, event


def test_derived_fact_index_builds_from_projected_state():
    _ledger, _store, state, _event = _projected_state_with_store()

    index = build_fact_index(state, workspace_id="ws")

    assert index.current_facts(state, "svc", "runtime") == state.get_current_facts(
        "svc", "runtime", resolve_aliases=False
    )
    assert index.fact_ids_by_subject_predicate["node"]["package_installed"] == [
        "fact_package"
    ]


def test_derived_fact_index_saved_with_projection_dependency_metadata():
    _ledger, store, state, _event = _projected_state_with_store()

    index = load_or_build_fact_index(state, workspace_id="ws", store=store)
    snapshot = store.load_derived_index_snapshot(
        "ws",
        FACT_INDEX_NAME,
        FACT_INDEX_VERSION,
        state_projection_version=STATE_PROJECTION_VERSION,
        state_last_event_id=state.last_event_id,
    )

    assert snapshot is not None
    assert snapshot.workspace_id == "ws"
    assert snapshot.index_name == FACT_INDEX_NAME
    assert snapshot.index_version == FACT_INDEX_VERSION
    assert snapshot.state_projection_version == STATE_PROJECTION_VERSION
    assert snapshot.state_last_event_id == state.last_event_id
    assert snapshot.created_at == index.created_at


def test_derived_fact_index_cache_hits_only_for_matching_projection_version_and_event():
    _ledger, store, state, _event = _projected_state_with_store()
    load_or_build_fact_index(state, workspace_id="ws", store=store)

    matching = store.load_derived_index_snapshot(
        "ws",
        FACT_INDEX_NAME,
        FACT_INDEX_VERSION,
        state_projection_version=STATE_PROJECTION_VERSION,
        state_last_event_id=state.last_event_id,
    )
    wrong_projection_version = "state-v0"
    assert wrong_projection_version != STATE_PROJECTION_VERSION

    wrong_version = store.load_derived_index_snapshot(
        "ws",
        FACT_INDEX_NAME,
        FACT_INDEX_VERSION,
        state_projection_version=wrong_projection_version,
        state_last_event_id=state.last_event_id,
    )
    wrong_event = store.load_derived_index_snapshot(
        "ws",
        FACT_INDEX_NAME,
        FACT_INDEX_VERSION,
        state_projection_version=STATE_PROJECTION_VERSION,
        state_last_event_id="evt_other",
    )

    assert matching is not None
    assert wrong_version is None
    assert wrong_event is None


def test_stale_fact_index_cache_misses_when_last_event_id_changes():
    ledger, store, state, _event = _projected_state_with_store()
    load_or_build_fact_index(state, workspace_id="ws", store=store)
    _append_fact(ledger, "ws", _fact("fact_new", "svc", "runtime", "podman"))
    new_state, _status = project_state_with_cache(ledger, "ws", store)

    stale = store.load_derived_index_snapshot(
        "ws",
        FACT_INDEX_NAME,
        FACT_INDEX_VERSION,
        state_projection_version=STATE_PROJECTION_VERSION,
        state_last_event_id=new_state.last_event_id,
    )

    assert stale is None


def test_indexed_current_facts_lookup_matches_existing_path():
    _ledger, store, state, _event = _projected_state_with_store()
    index = load_or_build_fact_index(state, workspace_id="ws", store=store)

    assert format_current_facts(
        state, "svc", "runtime", fact_index=index
    ) == format_current_facts(state, "svc", "runtime")


def test_derived_index_creation_does_not_append_events_or_create_observations_or_facts():
    ledger, store, state, _event = _projected_state_with_store()
    event_count = len(ledger.list_events("ws"))
    observation_count = len(state.observations)
    fact_count = len(state.facts)

    load_or_build_fact_index(state, workspace_id="ws", store=store)

    assert len(ledger.list_events("ws")) == event_count
    assert len(state.observations) == observation_count
    assert len(state.facts) == fact_count


def test_fact_index_status_reporting_does_not_alter_output():
    _ledger, store, state, _event = _projected_state_with_store()
    consumer = RecordingExecutionStatusConsumer()

    index = load_or_build_fact_index(
        state, workspace_id="ws", store=store, status_consumer=consumer
    )

    assert format_current_facts(state, "svc", "runtime", fact_index=index) == "docker"
    assert any(
        status.message == "Fact index cache: miss" for status in consumer.statuses
    )
    assert any(
        status.message == "Saving fact index cache..." for status in consumer.statuses
    )


def test_fact_index_does_not_change_projection_cache_semantics():
    ledger, store, state, _event = _projected_state_with_store()
    before = store.load_snapshot("ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION)

    load_or_build_fact_index(state, workspace_id="ws", store=store)
    after = store.load_snapshot("ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION)

    assert before == after
    assert len(ledger.list_events("ws")) == 2


def test_long_fact_index_build_emits_intermediate_progress_without_mutating_state():
    ledger = EventLedger()
    events = [
        Event(
            id=f"evt_fact_index_{index}",
            kind="fact.observed",
            workspace_id="ws",
            payload={
                "fact": to_plain(
                    _fact(f"fact_index_{index}", f"svc_{index}", "runtime", "docker")
                )
            },
        )
        for index in range(1001)
    ]
    ledger.append_many(events)
    state, _status = project_state_with_cache(ledger, "ws", None)
    fact_count = len(state.facts)
    observation_count = len(state.observations)
    consumer = RecordingExecutionStatusConsumer()

    index = load_or_build_fact_index(
        state, workspace_id="ws", store=None, status_consumer=consumer
    )

    progress = [
        status
        for status in consumer.statuses
        if status.phase == "fact_index_build"
        and status.current is not None
        and status.total is not None
    ]
    assert [status.current for status in progress] == [1, 501, 1001]
    assert progress[-1].completed is True
    assert len(index.fact_ids_by_subject_predicate) == 1001
    assert len(state.facts) == fact_count
    assert len(state.observations) == observation_count
    assert len(ledger.list_events("ws")) == 1001


def test_fact_index_build_starts_from_read_model_construction_inputs(monkeypatch):
    from seed_runtime import fact_index
    from seed_runtime.read_model_ownership import ReadModelConstructionInputs

    _ledger, _store, state, _event = _projected_state_with_store()
    observed = []

    def capture_inputs(visible_state):
        observed.append(visible_state)
        return ReadModelConstructionInputs(visible_state=visible_state)

    monkeypatch.setattr(fact_index, "read_model_construction_inputs", capture_inputs)

    index = fact_index.build_fact_index(state, workspace_id="ws")

    assert observed == [state]
    assert index.state_last_event_id == state.last_event_id


def test_sqlite_fact_index_cache_requires_bounded_source_projection(tmp_path):
    db_path = tmp_path / "fact-index-source-boundary.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    store = SQLiteProjectionStore(str(db_path))
    try:
        _append_fact(ledger, "ws", _fact("fact_runtime", "svc", "runtime", "docker"))
        state, _status = project_state_with_cache(ledger, "ws", store)
        first = load_or_build_fact_index(state, workspace_id="ws", store=store)
        cached = store.load_derived_index_snapshot(
            "ws",
            FACT_INDEX_NAME,
            FACT_INDEX_VERSION,
            state_projection_version=STATE_PROJECTION_VERSION,
            state_last_event_id=state.last_event_id,
        )
        assert cached is not None

        store._connection.execute(
            "UPDATE projection_snapshots SET consumer_limit = 'cluster_truth' WHERE workspace_id = ?",
            ("ws",),
        )
        store._connection.commit()

        assert (
            store.load_derived_index_snapshot(
                "ws",
                FACT_INDEX_NAME,
                FACT_INDEX_VERSION,
                state_projection_version=STATE_PROJECTION_VERSION,
                state_last_event_id=state.last_event_id,
            )
            is None
        )
        rebuilt = load_or_build_fact_index(state, workspace_id="ws", store=store)
    finally:
        store.close()
        ledger.close()

    assert first.fact_ids_by_subject_predicate == rebuilt.fact_ids_by_subject_predicate


def test_sqlite_fact_index_cache_requires_own_derived_boundary(tmp_path):
    db_path = tmp_path / "fact-index-own-boundary.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    store = SQLiteProjectionStore(str(db_path))
    try:
        _append_fact(ledger, "ws", _fact("fact_runtime", "svc", "runtime", "docker"))
        state, _status = project_state_with_cache(ledger, "ws", store)
        before_events = ledger.list_events("ws")
        first = load_or_build_fact_index(state, workspace_id="ws", store=store)
        cached = store.load_derived_index_snapshot(
            "ws",
            FACT_INDEX_NAME,
            FACT_INDEX_VERSION,
            state_projection_version=STATE_PROJECTION_VERSION,
            state_last_event_id=state.last_event_id,
        )
        assert cached is not None
        assert cached.boundary.consumer_limit == "fact_index_cache_only"

        store._connection.execute(
            "UPDATE derived_index_snapshots SET consumer_limit = 'cluster_truth', mutates_cluster = 1 WHERE workspace_id = ?",
            ("ws",),
        )
        store._connection.commit()

        assert (
            store.load_derived_index_snapshot(
                "ws",
                FACT_INDEX_NAME,
                FACT_INDEX_VERSION,
                state_projection_version=STATE_PROJECTION_VERSION,
                state_last_event_id=state.last_event_id,
            )
            is None
        )
        rebuilt = load_or_build_fact_index(state, workspace_id="ws", store=store)
        after_events = ledger.list_events("ws")
    finally:
        store.close()
        ledger.close()

    assert first.fact_ids_by_subject_predicate == rebuilt.fact_ids_by_subject_predicate
    assert [event.id for event in after_events] == [event.id for event in before_events]
