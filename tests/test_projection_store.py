from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.execution_status import RecordingExecutionStatusConsumer
from seed_runtime.facts import Fact
from seed_runtime.models import Event
from seed_runtime.projection_store import (
    InMemoryProjectionStore,
    ProjectionSnapshot,
    SQLiteProjectionStore,
    STATE_PROJECTION_NAME,
    STATE_PROJECTION_VERSION,
    project_state_with_cache,
    state_from_payload,
    state_to_payload,
)
from seed_runtime.serialization import to_plain
from seed_runtime.state import State, StateProjector


class CountingProjector:
    def __init__(self, ledger):
        self._projector = StateProjector(ledger)
        self.calls = 0
        self.incremental_calls = 0
        self.incremental_event_ids: list[str] = []

    def project(self, workspace_id: str) -> State:
        self.calls += 1
        return self._projector.project(workspace_id)

    def project_from_state(self, state: State, events):
        event_list = list(events)
        self.incremental_calls += 1
        self.incremental_event_ids.extend(event.id for event in event_list)
        return self._projector.project_from_state(state, event_list)


def _append_fact(ledger: EventLedger, workspace_id: str, fact_id: str, value: str):
    fact = Fact(
        id=fact_id,
        subject_id="svc",
        predicate="runtime",
        value=value,
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    return ledger.append(
        "fact.observed",
        workspace_id,
        {"fact": to_plain(fact)},
    )


def test_first_read_only_projection_builds_snapshot():
    ledger = EventLedger()
    event = _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    projector = CountingProjector(ledger)

    state, status = project_state_with_cache(ledger, "ws", store, projector=projector)

    assert status.cache_hit is False
    assert projector.calls == 1
    assert state.get_best_fact("svc", "runtime").value == "docker"
    snapshot = store.load_snapshot(
        "ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
    )
    assert snapshot is not None
    assert snapshot.last_event_id == event.id


def test_second_read_only_projection_reuses_snapshot():
    ledger = EventLedger()
    _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    projector = CountingProjector(ledger)

    project_state_with_cache(ledger, "ws", store, projector=projector)
    state, status = project_state_with_cache(ledger, "ws", store, projector=projector)

    assert status.cache_hit is True
    assert projector.calls == 1
    assert state.get_best_fact("svc", "runtime").value == "docker"


def test_appending_new_event_invalidates_snapshot():
    ledger = EventLedger()
    _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    projector = CountingProjector(ledger)
    project_state_with_cache(ledger, "ws", store, projector=projector)

    event = _append_fact(ledger, "ws", "fact_two", "podman")
    state, status = project_state_with_cache(ledger, "ws", store, projector=projector)

    assert status.cache_hit is False
    assert status.snapshot_last_event_id != event.id
    assert status.current_last_event_id == event.id
    assert projector.calls == 2
    assert projector.incremental_calls == 0
    assert status.incremental_replay is False
    assert set(state.facts) == {"fact_one", "fact_two"}


def test_projection_version_mismatch_invalidates_snapshot():
    ledger = EventLedger()
    event = _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    stale_state = StateProjector(ledger).project("ws")
    store.save_snapshot(
        ProjectionSnapshot(
            workspace_id="ws",
            projection_name=STATE_PROJECTION_NAME,
            projection_version="old-version",
            last_event_id=event.id,
            last_event_created_at=event.timestamp,
            state_payload=state_to_payload(stale_state),
            created_at=datetime.now(timezone.utc),
        )
    )
    projector = CountingProjector(ledger)

    state, status = project_state_with_cache(ledger, "ws", store, projector=projector)

    assert status.cache_hit is False
    assert projector.calls == 1
    assert state.get_best_fact("svc", "runtime").value == "docker"
    assert store.load_snapshot("ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION)


def test_sqlite_projection_store_clear_and_rebuild(tmp_path):
    db_path = tmp_path / "cache.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    store = SQLiteProjectionStore(str(db_path))
    try:
        _append_fact(ledger, "ws", "fact_one", "docker")
        project_state_with_cache(ledger, "ws", store)
        assert store.load_snapshot(
            "ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
        )

        store.clear_snapshot("ws", STATE_PROJECTION_NAME)
        assert (
            store.load_snapshot("ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION)
            is None
        )

        project_state_with_cache(ledger, "ws", store)
        assert store.load_snapshot(
            "ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
        )
        with sqlite3.connect(db_path) as connection:
            columns = {
                row[1]
                for row in connection.execute("PRAGMA table_info(projection_snapshots)")
            }
        assert {
            "workspace_id",
            "projection_name",
            "projection_version",
            "last_event_id",
            "last_event_created_at",
            "state_json",
            "created_at",
        } <= columns
    finally:
        store.close()
        ledger.close()


def test_in_memory_projection_store_works_independently_of_sqlite():
    store = InMemoryProjectionStore()
    snapshot = ProjectionSnapshot(
        workspace_id="ws",
        projection_name="state",
        projection_version="v1",
        last_event_id="evt_000001",
        last_event_created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        state_payload=state_to_payload(State(workspace_id="ws")),
        created_at=datetime.now(timezone.utc),
    )

    store.save_snapshot(snapshot)

    loaded = store.load_snapshot("ws", "state", "v1")
    assert loaded == snapshot
    assert state_from_payload(loaded.state_payload).workspace_id == "ws"
    assert store.load_snapshot("ws", "state", "v2") is None
    store.clear_snapshot("ws")
    assert store.load_snapshot("ws", "state", "v1") is None


def test_event_ledger_api_remains_focused_on_events(tmp_path):
    ledgers = [EventLedger(), SQLiteEventLedger(str(tmp_path / "events.sqlite"))]
    try:
        for ledger in ledgers:
            assert hasattr(ledger, "append")
            assert hasattr(ledger, "list_events")
            assert not hasattr(ledger, "load_snapshot")
            assert not hasattr(ledger, "save_snapshot")
            assert not hasattr(ledger, "clear_snapshot")
    finally:
        ledgers[1].close()


def test_cli_rebuild_state_cache_clears_and_rebuilds(tmp_path, capsys):
    import importlib.util
    import sys
    from pathlib import Path

    spec = importlib.util.spec_from_file_location(
        "seed_local_cache", Path("scripts/seed_local.py")
    )
    seed_local = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = seed_local
    assert spec.loader is not None
    spec.loader.exec_module(seed_local)

    db_path = tmp_path / "cli-cache.sqlite"
    assert (
        seed_local.main(["--db", str(db_path), "--fact", "svc", "runtime", "docker"])
        == 0
    )
    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0
    assert seed_local.main(["--db", str(db_path), "--rebuild-state-cache"]) == 0

    output = capsys.readouterr().out
    assert "rebuilt state cache for workspace 'local'" in output
    store = SQLiteProjectionStore(str(db_path))
    try:
        assert (
            store.load_snapshot(
                "local", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
            )
            is not None
        )
    finally:
        store.close()


def test_summary_cache_hit_matches_summary_rebuilt_from_full_state_projection():
    from seed_runtime.projection_store import (
        STATE_SUMMARY_PROJECTION_NAME,
        STATE_SUMMARY_PROJECTION_VERSION,
        SummaryProjectionSnapshot,
    )
    from seed_runtime.state_summary_views import state_summary
    from seed_runtime.state_views import build_state_summary

    ledger = EventLedger()
    event = _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    state, _status = project_state_with_cache(ledger, "ws", store)
    expected_view = build_state_summary(state)
    expected_operator = state_summary(state)
    store.save_summary_snapshot(
        SummaryProjectionSnapshot(
            workspace_id="ws",
            projection_name=STATE_SUMMARY_PROJECTION_NAME,
            projection_version=STATE_SUMMARY_PROJECTION_VERSION,
            last_event_id=event.id,
            state_projection_version=STATE_PROJECTION_VERSION,
            state_last_event_id=event.id,
            summary_payload={
                "state_view_summary": to_plain(expected_view),
                "operator_summary": expected_operator,
            },
            created_at=datetime.now(timezone.utc),
        )
    )

    snapshot = store.load_summary_snapshot(
        "ws",
        STATE_SUMMARY_PROJECTION_NAME,
        STATE_SUMMARY_PROJECTION_VERSION,
        state_projection_version=STATE_PROJECTION_VERSION,
        state_last_event_id=event.id,
    )

    assert snapshot is not None
    assert snapshot.summary_payload["state_view_summary"] == to_plain(expected_view)
    assert snapshot.summary_payload["operator_summary"] == expected_operator


def test_summary_cache_invalidates_when_projection_last_event_changes():
    from seed_runtime.projection_store import (
        STATE_SUMMARY_PROJECTION_NAME,
        STATE_SUMMARY_PROJECTION_VERSION,
        SummaryProjectionSnapshot,
    )

    ledger = EventLedger()
    first_event = _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    project_state_with_cache(ledger, "ws", store)
    store.save_summary_snapshot(
        SummaryProjectionSnapshot(
            workspace_id="ws",
            projection_name=STATE_SUMMARY_PROJECTION_NAME,
            projection_version=STATE_SUMMARY_PROJECTION_VERSION,
            last_event_id=first_event.id,
            state_projection_version=STATE_PROJECTION_VERSION,
            state_last_event_id=first_event.id,
            summary_payload={"state_view_summary": {}, "operator_summary": {}},
            created_at=datetime.now(timezone.utc),
        )
    )

    second_event = _append_fact(ledger, "ws", "fact_two", "podman")
    project_state_with_cache(ledger, "ws", store)

    assert (
        store.load_summary_snapshot(
            "ws",
            STATE_SUMMARY_PROJECTION_NAME,
            STATE_SUMMARY_PROJECTION_VERSION,
            state_projection_version=STATE_PROJECTION_VERSION,
            state_last_event_id=second_event.id,
        )
        is None
    )


def test_summary_cache_invalidates_on_projection_version_change():
    from seed_runtime.projection_store import (
        STATE_SUMMARY_PROJECTION_NAME,
        STATE_SUMMARY_PROJECTION_VERSION,
        SummaryProjectionSnapshot,
    )

    ledger = EventLedger()
    event = _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    project_state_with_cache(ledger, "ws", store)
    store.save_summary_snapshot(
        SummaryProjectionSnapshot(
            workspace_id="ws",
            projection_name=STATE_SUMMARY_PROJECTION_NAME,
            projection_version=STATE_SUMMARY_PROJECTION_VERSION,
            last_event_id=event.id,
            state_projection_version="old-state-version",
            state_last_event_id=event.id,
            summary_payload={"state_view_summary": {}, "operator_summary": {}},
            created_at=datetime.now(timezone.utc),
        )
    )

    assert (
        store.load_summary_snapshot(
            "ws",
            STATE_SUMMARY_PROJECTION_NAME,
            STATE_SUMMARY_PROJECTION_VERSION,
            state_projection_version=STATE_PROJECTION_VERSION,
            state_last_event_id=event.id,
        )
        is None
    )


def test_sqlite_summary_cache_depends_on_full_state_projection_snapshot(tmp_path):
    from seed_runtime.projection_store import (
        STATE_SUMMARY_PROJECTION_NAME,
        STATE_SUMMARY_PROJECTION_VERSION,
        SummaryProjectionSnapshot,
    )

    db_path = tmp_path / "summary-cache.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    store = SQLiteProjectionStore(str(db_path))
    try:
        event = _append_fact(ledger, "ws", "fact_one", "docker")
        store.save_summary_snapshot(
            SummaryProjectionSnapshot(
                workspace_id="ws",
                projection_name=STATE_SUMMARY_PROJECTION_NAME,
                projection_version=STATE_SUMMARY_PROJECTION_VERSION,
                last_event_id=event.id,
                state_projection_version=STATE_PROJECTION_VERSION,
                state_last_event_id=event.id,
                summary_payload={"state_view_summary": {}, "operator_summary": {}},
                created_at=datetime.now(timezone.utc),
            )
        )

        assert (
            store.load_summary_snapshot(
                "ws",
                STATE_SUMMARY_PROJECTION_NAME,
                STATE_SUMMARY_PROJECTION_VERSION,
                state_projection_version=STATE_PROJECTION_VERSION,
                state_last_event_id=event.id,
            )
            is None
        )

        project_state_with_cache(ledger, "ws", store)
        assert (
            store.load_summary_snapshot(
                "ws",
                STATE_SUMMARY_PROJECTION_NAME,
                STATE_SUMMARY_PROJECTION_VERSION,
                state_projection_version=STATE_PROJECTION_VERSION,
                state_last_event_id=event.id,
            )
            is not None
        )
    finally:
        store.close()
        ledger.close()


def test_cli_state_summary_reuses_summary_read_model_without_deserializing_state(
    monkeypatch, tmp_path, capsys
):
    import importlib.util
    import sys
    from pathlib import Path

    spec = importlib.util.spec_from_file_location(
        "seed_local_summary_cache", Path("scripts/seed_local.py")
    )
    seed_local = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = seed_local
    assert spec.loader is not None
    spec.loader.exec_module(seed_local)

    db_path = tmp_path / "cli-summary-cache.sqlite"
    assert (
        seed_local.main(["--db", str(db_path), "--fact", "svc", "runtime", "docker"])
        == 0
    )
    capsys.readouterr()
    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0
    first_output = capsys.readouterr().out

    def fail_state_load(_payload):
        raise AssertionError(
            "full State snapshot should not be loaded on summary cache hit"
        )

    monkeypatch.setattr(seed_local, "project_state_with_cache", fail_state_load)
    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0
    second_output = capsys.readouterr().out

    assert second_output == first_output


def test_incremental_replay_matches_full_replay_and_preserves_order():
    ledger = EventLedger()
    _append_fact(ledger, "ws", "fact_one", "python")
    store = InMemoryProjectionStore()
    projector = CountingProjector(ledger)
    project_state_with_cache(ledger, "ws", store, projector=projector)

    second = _append_fact(ledger, "ws", "fact_two", "ruby")
    third = _append_fact(ledger, "ws", "fact_three", "go")
    incremental_state, status = project_state_with_cache(
        ledger, "ws", store, projector=projector
    )
    full_state = StateProjector(ledger).project("ws")

    assert state_to_payload(incremental_state) == state_to_payload(full_state)
    assert status.incremental_replay is True
    assert status.events_applied == 2
    assert projector.calls == 1
    assert projector.incremental_calls == 1
    assert projector.incremental_event_ids == [second.id, third.id]


def test_incremental_replay_never_skips_events_after_snapshot():
    ledger = EventLedger()
    first = _append_fact(ledger, "ws", "fact_one", "python")
    second = _append_fact(ledger, "ws", "fact_two", "podman")
    store = InMemoryProjectionStore()
    snapshot_state = StateProjector(ledger).project("ws")
    store.save_snapshot(
        ProjectionSnapshot(
            workspace_id="ws",
            projection_name=STATE_PROJECTION_NAME,
            projection_version=STATE_PROJECTION_VERSION,
            last_event_id=second.id,
            last_event_created_at=second.timestamp,
            state_payload=state_to_payload(snapshot_state),
            created_at=datetime.now(timezone.utc),
        )
    )
    third = _append_fact(ledger, "ws", "fact_three", "containerd")
    fourth = _append_fact(ledger, "ws", "fact_four", "runc")
    projector = CountingProjector(ledger)

    state, status = project_state_with_cache(ledger, "ws", store, projector=projector)

    assert first.id not in projector.incremental_event_ids
    assert second.id not in projector.incremental_event_ids
    assert projector.incremental_event_ids == [third.id, fourth.id]
    assert status.events_applied == 2
    assert set(state.facts) == {"fact_one", "fact_two", "fact_three", "fact_four"}


def test_snapshot_with_unknown_last_event_falls_back_to_full_projection():
    ledger = EventLedger()
    _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    store.save_snapshot(
        ProjectionSnapshot(
            workspace_id="ws",
            projection_name=STATE_PROJECTION_NAME,
            projection_version=STATE_PROJECTION_VERSION,
            last_event_id="evt_missing",
            last_event_created_at=None,
            state_payload=state_to_payload(State(workspace_id="ws")),
            created_at=datetime.now(timezone.utc),
        )
    )
    projector = CountingProjector(ledger)

    state, status = project_state_with_cache(ledger, "ws", store, projector=projector)

    assert status.incremental_replay is False
    assert projector.incremental_calls == 0
    assert projector.calls == 1
    assert state.get_best_fact("svc", "runtime").value == "docker"


def test_corrupted_snapshot_falls_back_to_safe_full_projection():
    ledger = EventLedger()
    event = _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    store.save_snapshot(
        ProjectionSnapshot(
            workspace_id="ws",
            projection_name=STATE_PROJECTION_NAME,
            projection_version=STATE_PROJECTION_VERSION,
            last_event_id=event.id,
            last_event_created_at=event.timestamp,
            state_payload={"workspace_id": "ws", "facts": "not-a-dict"},
            created_at=datetime.now(timezone.utc),
        )
    )
    projector = CountingProjector(ledger)

    state, status = project_state_with_cache(ledger, "ws", store, projector=projector)

    assert status.cache_hit is False
    assert status.incremental_replay is False
    assert projector.calls == 1
    assert state.get_best_fact("svc", "runtime").value == "docker"


def test_incremental_projection_version_mismatch_uses_full_replay_not_snapshot():
    ledger = EventLedger()
    event = _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    store.save_snapshot(
        ProjectionSnapshot(
            workspace_id="ws",
            projection_name=STATE_PROJECTION_NAME,
            projection_version="old-version",
            last_event_id=event.id,
            last_event_created_at=event.timestamp,
            state_payload=state_to_payload(StateProjector(ledger).project("ws")),
            created_at=datetime.now(timezone.utc),
        )
    )
    projector = CountingProjector(ledger)

    _state, status = project_state_with_cache(ledger, "ws", store, projector=projector)

    assert status.incremental_replay is False
    assert projector.incremental_calls == 0
    assert projector.calls == 1


def _load_seed_local_module():
    import importlib.util
    import sys
    from pathlib import Path

    spec = importlib.util.spec_from_file_location(
        "seed_local_cache_status", Path("scripts/seed_local.py")
    )
    seed_local = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = seed_local
    assert spec.loader is not None
    spec.loader.exec_module(seed_local)
    return seed_local


def _state_cache_status_args(db_path, workspace="ws"):
    import argparse

    return argparse.Namespace(db=str(db_path), workspace=workspace)


def _save_sqlite_snapshot(db_path, ledger, workspace, last_event_id):
    store = SQLiteProjectionStore(str(db_path))
    try:
        state = StateProjector(ledger).project(workspace)
        store.save_snapshot(
            ProjectionSnapshot(
                workspace_id=workspace,
                projection_name=STATE_PROJECTION_NAME,
                projection_version=STATE_PROJECTION_VERSION,
                last_event_id=last_event_id,
                last_event_created_at=None,
                state_payload=state_to_payload(state),
                created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            )
        )
    finally:
        store.close()


def test_cli_state_cache_status_does_not_call_project_state_with_cache(
    monkeypatch, tmp_path
):
    seed_local = _load_seed_local_module()
    db_path = tmp_path / "cache-status-no-project-with-cache.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    event = _append_fact(ledger, "ws", "fact_one", "docker")
    ledger.close()

    def fail_project_state_with_cache(*_args, **_kwargs):
        raise AssertionError("cache status must not demand projected state")

    def fail_project(*_args, **_kwargs):
        raise AssertionError("cache status must not replay projection state")

    monkeypatch.setattr(
        seed_local, "project_state_with_cache", fail_project_state_with_cache
    )
    monkeypatch.setattr(seed_local.StateProjector, "project", fail_project)

    output = seed_local.format_state_cache_status_from_args(
        _state_cache_status_args(db_path)
    )

    assert output == "\n".join(
        [
            "cache: miss",
            f"projection_version: {STATE_PROJECTION_VERSION}",
            "snapshot last_event_id: none",
            f"current last_event_id: {event.id}",
        ]
    )


def test_cli_state_cache_status_does_not_rebuild_cache_on_miss(tmp_path):
    seed_local = _load_seed_local_module()
    db_path = tmp_path / "cache-status-miss-no-rebuild.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    event = _append_fact(ledger, "ws", "fact_one", "docker")
    ledger.close()

    output = seed_local.format_state_cache_status_from_args(
        _state_cache_status_args(db_path)
    )

    store = SQLiteProjectionStore(str(db_path))
    try:
        snapshot = store.load_snapshot(
            "ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
        )
    finally:
        store.close()
    assert snapshot is None
    assert "cache: miss" in output
    assert "snapshot last_event_id: none" in output
    assert f"current last_event_id: {event.id}" in output


def test_cli_state_cache_status_miss_reports_no_snapshot(tmp_path):
    seed_local = _load_seed_local_module()
    db_path = tmp_path / "cache-status-miss-report.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    event = _append_fact(ledger, "ws", "fact_one", "docker")
    ledger.close()

    output = seed_local.format_state_cache_status_from_args(
        _state_cache_status_args(db_path)
    )

    assert output == "\n".join(
        [
            "cache: miss",
            f"projection_version: {STATE_PROJECTION_VERSION}",
            "snapshot last_event_id: none",
            f"current last_event_id: {event.id}",
        ]
    )


def test_cli_state_cache_status_hit_reports_matching_snapshot(tmp_path):
    seed_local = _load_seed_local_module()
    db_path = tmp_path / "cache-status-hit.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    event = _append_fact(ledger, "ws", "fact_one", "docker")
    _save_sqlite_snapshot(db_path, ledger, "ws", event.id)
    ledger.close()

    output = seed_local.format_state_cache_status_from_args(
        _state_cache_status_args(db_path)
    )

    assert output == "\n".join(
        [
            "cache: hit",
            f"projection_version: {STATE_PROJECTION_VERSION}",
            f"snapshot last_event_id: {event.id}",
            f"current last_event_id: {event.id}",
        ]
    )


def test_cli_state_cache_status_stale_snapshot_reports_miss_without_modifying_snapshot(
    tmp_path,
):
    seed_local = _load_seed_local_module()
    db_path = tmp_path / "cache-status-stale.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    first = _append_fact(ledger, "ws", "fact_one", "docker")
    _save_sqlite_snapshot(db_path, ledger, "ws", first.id)
    second = _append_fact(ledger, "ws", "fact_two", "podman")
    ledger.close()

    output = seed_local.format_state_cache_status_from_args(
        _state_cache_status_args(db_path)
    )

    store = SQLiteProjectionStore(str(db_path))
    try:
        snapshot = store.load_snapshot(
            "ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
        )
    finally:
        store.close()
    assert snapshot is not None
    assert snapshot.last_event_id == first.id
    assert output == "\n".join(
        [
            "cache: miss",
            f"projection_version: {STATE_PROJECTION_VERSION}",
            f"snapshot last_event_id: {first.id}",
            f"current last_event_id: {second.id}",
        ]
    )


def test_projection_cache_status_surfaces_hit_and_miss_without_changing_state():
    ledger = EventLedger()
    _append_fact(ledger, "ws", "fact_one", "docker")
    store = InMemoryProjectionStore()
    miss_consumer = RecordingExecutionStatusConsumer()
    hit_consumer = RecordingExecutionStatusConsumer()

    missed_state, miss_status = project_state_with_cache(
        ledger, "ws", store, status_consumer=miss_consumer
    )
    hit_state, hit_status = project_state_with_cache(
        ledger, "ws", store, status_consumer=hit_consumer
    )

    assert miss_status.cache_hit is False
    assert hit_status.cache_hit is True
    assert state_to_payload(missed_state) == state_to_payload(hit_state)
    assert any(
        status.message == "State cache: miss" for status in miss_consumer.statuses
    )
    assert any(
        status.message == "Projection replay" for status in miss_consumer.statuses
    )
    assert any(status.message == "State cache: hit" for status in hit_consumer.statuses)


def test_projection_cache_status_surfaces_incremental_replay_without_changing_validity():
    ledger = EventLedger()
    first = _append_fact(ledger, "ws", "fact_one", "python")
    store = InMemoryProjectionStore()
    projector = CountingProjector(ledger)
    project_state_with_cache(ledger, "ws", store, projector=projector)
    _append_fact(ledger, "ws", "fact_two", "ruby")
    consumer = RecordingExecutionStatusConsumer()

    state, status = project_state_with_cache(
        ledger, "ws", store, projector=projector, status_consumer=consumer
    )
    snapshot = store.load_snapshot(
        "ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
    )

    assert status.incremental_replay is True
    assert status.events_applied == 1
    assert status.snapshot_last_event_id == first.id
    assert snapshot is not None
    assert snapshot.last_event_id == state.last_event_id
    assert any(
        status.message == "Incremental replay" for status in consumer.statuses
    )


def test_inspection_cli_emits_projection_status_to_stderr_and_preserves_json_stdout(
    tmp_path, capsys
):
    seed_local = _load_seed_local_module()
    db_path = tmp_path / "inspection-status.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    _append_fact(ledger, "local", "fact_one", "openssh-client")
    ledger.close()

    assert (
        seed_local.main(["--db", str(db_path), "--capability-candidates", "ssh"])
        == 0
    )
    captured = capsys.readouterr()

    assert captured.err.splitlines()[:3] == [
        "Loading projection cache...",
        "State cache: miss",
        "Projection replay: 0 / 1",
    ]
    assert '"boundary": "capability_candidate_preservation_only"' in captured.out
    assert "Loading projection cache" not in captured.out


def test_state_summary_cli_surfaces_summary_cache_hit_and_state_cache_miss(
    tmp_path, capsys
):
    seed_local = _load_seed_local_module()
    db_path = tmp_path / "summary-status.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    _append_fact(ledger, "local", "fact_one", "docker")
    ledger.close()

    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0
    first = capsys.readouterr()
    assert "State-summary cache: miss" in first.err
    assert "State cache: miss" in first.err

    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0
    second = capsys.readouterr()
    assert "State-summary cache: hit" in second.err
    assert "State cache:" not in second.err
    assert first.out == second.out

def test_long_projection_replay_emits_bounded_intermediate_progress():
    ledger = EventLedger()
    events = [
        Event(id=f"evt_progress_{index}", kind="progress.noop", workspace_id="ws")
        for index in range(1001)
    ]
    ledger.append_many(events)
    consumer = RecordingExecutionStatusConsumer()

    with_status, status = project_state_with_cache(
        ledger, "ws", None, status_consumer=consumer
    )
    without_status, _ = project_state_with_cache(ledger, "ws", None)

    progress = [
        item
        for item in consumer.statuses
        if item.phase == "projection_replay"
        and item.current is not None
        and item.total is not None
    ]
    assert [item.current for item in progress] == [0, 1, 501, 1001]
    assert progress[-1].completed is True
    assert status.events_applied == 1001
    assert with_status.last_event_id == without_status.last_event_id
    assert ledger.list_events("ws") == events


def test_short_projection_replay_does_not_spam_progress():
    ledger = EventLedger()
    ledger.append_many(
        [Event(id="evt_short_1", kind="progress.noop", workspace_id="ws")]
    )
    consumer = RecordingExecutionStatusConsumer()

    project_state_with_cache(ledger, "ws", None, status_consumer=consumer)

    progress = [
        item
        for item in consumer.statuses
        if item.phase == "projection_replay"
        and item.current is not None
        and item.total is not None
    ]
    assert [item.current for item in progress] == [0, 1]
    assert progress[-1].completed is True
