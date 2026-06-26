from datetime import datetime, timezone

from seed_runtime.events import EventLedger
from seed_runtime.observation_sources import (
    ObservationCollectionService,
    SeedRuntimeObservationSource,
)
from seed_runtime.observations import ObservationIngestor
from seed_runtime.state import StateProjector

BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _proc_status(root, pid=1234, text="VmRSS:\t42 kB\nThreads:\t7\n"):
    proc_dir = root / str(pid)
    proc_dir.mkdir(parents=True)
    (proc_dir / "status").write_text(text, encoding="utf-8")


def test_seed_runtime_source_emits_deterministic_read_only_observations(tmp_path):
    _proc_status(tmp_path)
    sqlite_db = tmp_path / "seed.sqlite"
    sqlite_db.write_bytes(b"abc")
    event_ledger = tmp_path / "events.sqlite"
    event_ledger.write_bytes(b"abcdef")

    observations = SeedRuntimeObservationSource(
        observed_at=BASE_TIME,
        process_id=1234,
        proc_root=tmp_path,
        started_at_monotonic=10.0,
        monotonic_fn=lambda: 12.5,
        sqlite_database_path=sqlite_db,
        event_ledger_path=event_ledger,
    ).collect()

    values = {observation.predicate: observation.value for observation in observations}
    assert values == {
        "seed_process_resident_memory_bytes": 42 * 1024,
        "seed_process_thread_count": 7,
        "seed_runtime_duration_seconds": 2.5,
        "seed_sqlite_database_size_bytes": 3,
        "seed_event_ledger_size_bytes": 6,
    }
    assert {observation.subject for observation in observations} == {"Seed"}
    assert all(observation.source_type == "discovery" for observation in observations)
    assert all(observation.observed_at == BASE_TIME for observation in observations)
    assert all(
        observation.metadata["read_only"] is True for observation in observations
    )
    assert all(
        observation.metadata["mutates_cluster"] is False for observation in observations
    )
    assert all(
        observation.metadata["scheduler"] is False for observation in observations
    )
    assert all(
        observation.metadata["runtime_governance"] is False
        for observation in observations
    )


def test_seed_runtime_observations_flow_through_existing_ingestion_to_projection(
    tmp_path,
):
    _proc_status(tmp_path)
    ledger = EventLedger()
    source = SeedRuntimeObservationSource(
        observed_at=BASE_TIME,
        process_id=1234,
        proc_root=tmp_path,
        started_at_monotonic=1.0,
        monotonic_fn=lambda: 4.0,
    )

    facts = ObservationCollectionService(
        ObservationIngestor(ledger), normalization_pipeline=None
    ).collect(source, "ws_seed_runtime")
    state = StateProjector(ledger).project("ws_seed_runtime")

    assert [event.kind for event in ledger.list_events("ws_seed_runtime")] == [
        kind
        for _ in facts
        for kind in ("observation.observed", "evidence.observed", "fact.observed")
    ]
    assert len(state.observations) == 3
    assert len(state.evidence) == 3
    assert len(state.facts) == 3
    assert {fact.predicate: fact.value for fact in state.facts.values()} == {
        "seed_process_resident_memory_bytes": 42 * 1024,
        "seed_process_thread_count": 7,
        "seed_runtime_duration_seconds": 3.0,
    }
    assert state.get_current_facts("Seed", "seed_process_thread_count")[0].value == 7


def test_seed_runtime_collection_succeeds_when_optional_metrics_unavailable(tmp_path):
    _proc_status(tmp_path, text="Name:\tpython\n")

    observations = SeedRuntimeObservationSource(
        observed_at=BASE_TIME,
        process_id=1234,
        proc_root=tmp_path,
        sqlite_database_path=tmp_path / "missing.sqlite",
        event_ledger_path=tmp_path / "missing-events.sqlite",
    ).collect()

    assert observations == []
