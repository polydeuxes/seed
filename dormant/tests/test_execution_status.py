from datetime import datetime, timezone
from io import StringIO

from seed_runtime.events import EventLedger
from seed_runtime.execution_status import (
    CliExecutionStatusConsumer,
    ExecutionStatus,
    ExecutionStatusEmitter,
    RecordingExecutionStatusConsumer,
)
from seed_runtime.observation_sources import (
    FakeObservationSource,
    ObservationCollectionService,
)
from seed_runtime.observations import Observation, ObservationIngestor
from seed_runtime.projection_store import (
    InMemoryProjectionStore,
    STATE_PROJECTION_NAME,
    STATE_PROJECTION_VERSION,
    project_state_with_cache,
)
from seed_runtime.state import StateProjector


def _observation(value: str = "value") -> Observation:
    return Observation(
        id=f"obs_{value}",
        source_type="discovery",
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        subject="host",
        predicate="hostname",
        value=value,
    )


def test_status_emitter_exposes_emission_without_consuming_status():
    consumer = RecordingExecutionStatusConsumer()
    emitter = ExecutionStatusEmitter(consumer)

    emitter.emit(
        "projection_replay",
        "Projection replay",
        current=1,
        total=2,
    )

    assert consumer.statuses == [
        ExecutionStatus(
            "projection_replay",
            "Projection replay",
            current=1,
            total=2,
        )
    ]


def test_status_emitter_without_consumer_preserves_noop_behavior():
    ExecutionStatusEmitter(None).emit(
        "projection_cache_load",
        "Loading projection cache...",
    )


def test_execution_status_emitted_during_observation_collection_and_ingestion():
    ledger = EventLedger()
    consumer = RecordingExecutionStatusConsumer()
    service = ObservationCollectionService(ObservationIngestor(ledger))

    service.collect(
        FakeObservationSource(
            [_observation("one"), _observation("two")], source_type="discovery"
        ),
        "ws",
        status_consumer=consumer,
    )

    phases = [status.phase for status in consumer.statuses]
    assert "observation_collection" in phases
    assert "observation_ingestion" in phases
    assert "event_persistence" in phases
    assert any(status.message == "Generating events..." for status in consumer.statuses)
    assert any(status.message == "Writing events" for status in consumer.statuses)


def test_repository_observation_emits_collection_status():
    ledger = EventLedger()
    consumer = RecordingExecutionStatusConsumer()

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource(
            [_observation("repo")],
            name="repository_source",
            source_type="discovery",
        ),
        "ws",
        status_consumer=consumer,
    )

    assert (
        consumer.statuses[0].message == "Collecting repository_source observations..."
    )
    assert any(
        status.message == "Collected 1 observations." and status.completed
        for status in consumer.statuses
    )


def test_repository_observation_emits_ingestion_and_event_writing_after_collection():
    ledger = EventLedger()
    consumer = RecordingExecutionStatusConsumer()

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource(
            [_observation("repo")],
            name="repository_source",
            source_type="discovery",
        ),
        "ws",
        status_consumer=consumer,
    )

    messages = [status.message for status in consumer.statuses]
    assert messages.index("Collected 1 observations.") < messages.index(
        "Generating events..."
    )
    assert any(
        status.phase == "event_persistence"
        and status.message == "Writing events"
        and status.current == 3
        and status.total == 3
        for status in consumer.statuses
    )


def test_local_host_observation_uses_shared_ingestion_status_path():
    ledger = EventLedger()
    consumer = RecordingExecutionStatusConsumer()

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource(
            [_observation("local")],
            name="local-host",
            source_type="discovery",
        ),
        "ws",
        status_consumer=consumer,
    )

    assert any(
        status.message == "Collecting local-host observations..."
        for status in consumer.statuses
    )
    assert any(status.phase == "observation_ingestion" for status in consumer.statuses)
    assert any(status.phase == "event_persistence" for status in consumer.statuses)


def test_cli_consumes_execution_status_as_operator_feedback():
    stream = StringIO()
    consumer = CliExecutionStatusConsumer(stream, progress_interval=1)

    consumer.consume(
        ExecutionStatus("observation_collection", "Collecting observations...")
    )
    consumer.consume(
        ExecutionStatus("event_persistence", "Writing events", current=7, total=10)
    )

    assert stream.getvalue().splitlines() == [
        "Collecting observations...",
        "Writing events: 7 / 10",
    ]


def test_execution_status_is_not_written_to_ledger_observations_or_facts():
    ledger = EventLedger()
    consumer = RecordingExecutionStatusConsumer()
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource([_observation()], source_type="discovery"),
        "ws",
        status_consumer=consumer,
    )

    events = ledger.list_events("ws")
    assert [event.kind for event in events] == [
        "observation.observed",
        "evidence.observed",
        "fact.observed",
    ]
    assert all("execution_status" not in event.kind for event in events)
    assert all("execution_status" not in str(event.payload) for event in events)

    state = StateProjector(ledger).project("ws")
    assert all(
        "execution_status" not in str(obs) for obs in state.observations.values()
    )
    assert all("execution_status" not in str(fact) for fact in state.facts.values())


def test_execution_status_is_not_included_in_projection_cache():
    ledger = EventLedger()
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource([_observation()], source_type="discovery"), "ws"
    )
    store = InMemoryProjectionStore()
    consumer = RecordingExecutionStatusConsumer()

    project_state_with_cache(ledger, "ws", store, status_consumer=consumer)
    snapshot = store.load_snapshot(
        "ws", STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
    )

    assert snapshot is not None
    assert "execution_status" not in str(snapshot.state_payload)
    assert any(status.phase == "projection_cache_save" for status in consumer.statuses)


def test_progress_and_phase_only_statuses_are_supported():
    consumer = RecordingExecutionStatusConsumer()
    ObservationIngestor(EventLedger()).ingest_many(
        [_observation("one"), _observation("two")], "ws", status_consumer=consumer
    )

    assert any(
        status.message == "Generating events"
        and status.current == 2
        and status.total == 2
        for status in consumer.statuses
    )
    assert any(
        status.phase == "event_persistence"
        and status.message == "Writing events"
        and status.current == 6
        and status.total == 6
        for status in consumer.statuses
    )
    assert ExecutionStatus("cache", "Loading projection cache...").total is None


def test_renderer_absence_does_not_affect_execution_behavior():
    ledger_with_status = EventLedger()
    ledger_without_status = EventLedger()

    ObservationCollectionService(ObservationIngestor(ledger_with_status)).collect(
        FakeObservationSource([_observation()], source_type="discovery"),
        "ws",
        status_consumer=RecordingExecutionStatusConsumer(),
    )
    ObservationCollectionService(ObservationIngestor(ledger_without_status)).collect(
        FakeObservationSource([_observation()], source_type="discovery"), "ws"
    )

    assert [event.kind for event in ledger_with_status.list_events("ws")] == [
        event.kind for event in ledger_without_status.list_events("ws")
    ]


def test_execution_status_consumer_cannot_modify_execution_state():
    class MutatingConsumer:
        def consume(self, status: ExecutionStatus) -> None:
            try:
                status.message = "mutated"
            except Exception:
                pass

    ledger = EventLedger()
    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource([_observation()], source_type="discovery"),
        "ws",
        status_consumer=MutatingConsumer(),
    )

    state = StateProjector(ledger).project("ws")
    assert len(state.facts) == 1
    assert next(iter(state.facts.values())).value == "value"


def _lifecycle_messages(consumer: RecordingExecutionStatusConsumer) -> list[str]:
    return [status.message for status in consumer.statuses]


def _lifecycle_phases(consumer: RecordingExecutionStatusConsumer) -> list[str]:
    return [status.phase for status in consumer.statuses]


def test_local_host_observation_uses_shared_observation_producer_lifecycle():
    ledger = EventLedger()
    consumer = RecordingExecutionStatusConsumer()

    ObservationCollectionService(ObservationIngestor(ledger)).collect(
        FakeObservationSource(
            [_observation("local")],
            name="local-host",
            source_type="discovery",
        ),
        "ws",
        status_consumer=consumer,
    )

    messages = _lifecycle_messages(consumer)
    assert messages.index("Collecting local-host observations...") < messages.index(
        "Collected 1 observations."
    )
    assert messages.index("Collected 1 observations.") < messages.index(
        "Normalizing local-host observations..."
    )
    assert messages.index("Normalized 1 observations.") < messages.index(
        "Ingesting local-host observations..."
    )
    assert messages[-1] == "Completed local-host observation lifecycle."
    assert "observation_normalization" in _lifecycle_phases(consumer)
    assert "observation_lifecycle" in _lifecycle_phases(consumer)


def test_repository_source_observation_uses_shared_observation_producer_lifecycle(
    tmp_path,
):
    repo_path = tmp_path / "repo"
    source_dir = repo_path / "seed_runtime"
    source_dir.mkdir(parents=True)
    (source_dir / "state.py").write_text(
        "from seed_runtime.projection_store import project_state_with_cache\n"
        "class StateProjector:\n"
        "    pass\n",
        encoding="utf-8",
    )

    from seed_runtime.observation_sources import RepositorySourceObservationSource

    ledger = EventLedger()
    consumer = RecordingExecutionStatusConsumer()
    facts = ObservationCollectionService(ObservationIngestor(ledger)).collect(
        RepositorySourceObservationSource(repo_path), "ws", status_consumer=consumer
    )

    messages = _lifecycle_messages(consumer)
    assert messages.index(
        "Collecting repository_source observations..."
    ) < messages.index(f"Collected {len(facts)} observations.")
    assert messages.index(
        "Normalizing repository_source observations..."
    ) < messages.index("Ingesting repository_source observations...")
    assert messages[-1] == "Completed repository_source observation lifecycle."
    assert "observation_normalization" in _lifecycle_phases(consumer)
    assert "observation_lifecycle" in _lifecycle_phases(consumer)


def test_shared_observation_lifecycle_preserves_knowledge_output_and_counts():
    observations = [_observation("one"), _observation("two")]
    ledger_with_status = EventLedger()
    ledger_without_status = EventLedger()

    facts_with_status = ObservationCollectionService(
        ObservationIngestor(ledger_with_status)
    ).collect(
        FakeObservationSource(observations, name="local-host", source_type="discovery"),
        "ws",
        status_consumer=RecordingExecutionStatusConsumer(),
    )
    facts_without_status = ObservationCollectionService(
        ObservationIngestor(ledger_without_status)
    ).collect(
        FakeObservationSource(observations, name="local-host", source_type="discovery"),
        "ws",
    )

    events_with_status = ledger_with_status.list_events("ws")
    events_without_status = ledger_without_status.list_events("ws")
    assert len(facts_with_status) == len(facts_without_status) == 2
    assert len(events_with_status) == len(events_without_status) == 6
    assert [event.kind for event in events_with_status] == [
        event.kind for event in events_without_status
    ]
    state_with_status = StateProjector(ledger_with_status).project("ws")
    state_without_status = StateProjector(ledger_without_status).project("ws")
    assert sorted(fact.value for fact in state_with_status.facts.values()) == sorted(
        fact.value for fact in state_without_status.facts.values()
    )
    assert len(state_with_status.observations) == len(state_without_status.observations)


def test_shared_observation_lifecycle_preserves_execution_status_consumer_payload_shape():
    consumer = RecordingExecutionStatusConsumer()
    ObservationCollectionService(ObservationIngestor(EventLedger())).collect(
        FakeObservationSource(
            [_observation()], name="repository_source", source_type="discovery"
        ),
        "ws",
        status_consumer=consumer,
    )

    assert all(isinstance(status, ExecutionStatus) for status in consumer.statuses)
    assert all(isinstance(status.phase, str) for status in consumer.statuses)
    assert all(isinstance(status.message, str) for status in consumer.statuses)
    assert any(
        status.phase == "observation_lifecycle" and status.completed
        for status in consumer.statuses
    )
