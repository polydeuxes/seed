from datetime import datetime, timezone

from seed_runtime.events import EventLedger
from seed_runtime.observation_sources import SeedRuntimeObservationSource
from seed_runtime.observations import ObservationIngestor
from seed_runtime.state import StateProjector


def test_observation_ingestor_accepts_seed_runtime_observations_without_special_path(
    tmp_path,
):
    proc_dir = tmp_path / "1234"
    proc_dir.mkdir()
    (proc_dir / "status").write_text("VmRSS:\t1 kB\nThreads:\t2\n", encoding="utf-8")
    source = SeedRuntimeObservationSource(
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        process_id=1234,
        proc_root=tmp_path,
    )
    observations = source.collect()
    ledger = EventLedger()

    facts = ObservationIngestor(ledger).ingest_many(observations, "ws_ingestor")
    state = StateProjector(ledger).project("ws_ingestor")

    assert len(facts) == 2
    assert [event.kind for event in ledger.list_events("ws_ingestor")] == [
        "observation.observed",
        "evidence.observed",
        "fact.observed",
        "observation.observed",
        "evidence.observed",
        "fact.observed",
    ]
    assert {fact.predicate for fact in facts if fact is not None} == {
        "seed_process_resident_memory_bytes",
        "seed_process_thread_count",
    }
    assert {evidence.source for evidence in state.evidence.values()} == {
        "observation:discovery"
    }
