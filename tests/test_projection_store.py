from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.facts import Fact
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

    def project(self, workspace_id: str) -> State:
        self.calls += 1
        return self._projector.project(workspace_id)


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
    snapshot = store.load_snapshot("ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION)
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
        assert store.load_snapshot("ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION)

        store.clear_snapshot("ws", STATE_PROJECTION_NAME)
        assert store.load_snapshot("ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION) is None

        project_state_with_cache(ledger, "ws", store)
        assert store.load_snapshot("ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION)
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
        assert store.load_snapshot(
            "local", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
        ) is not None
    finally:
        store.close()
