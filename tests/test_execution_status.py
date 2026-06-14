from datetime import datetime, timezone
from io import StringIO

from seed_runtime.events import EventLedger
from seed_runtime.execution_status import (
    CliExecutionStatusConsumer,
    ExecutionStatus,
    RecordingExecutionStatusConsumer,
)
from seed_runtime.observation_sources import (
    FakeObservationSource,
    ObservationCollectionService,
)
from seed_runtime.observations import Observation, ObservationIngestor
from seed_runtime.projection_store import (
    InMemoryProjectionStore,
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
    snapshot = store.load_snapshot("ws", "state", "state-v1")

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
