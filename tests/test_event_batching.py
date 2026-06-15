from datetime import datetime, timezone

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.models import Event, Fact
from seed_runtime.observations import Observation, ObservationIngestor
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def _events() -> list[Event]:
    return [
        Event(
            id="evt_batch_1", kind="batch.first", workspace_id="ws", payload={"n": 1}
        ),
        Event(
            id="evt_batch_2", kind="batch.second", workspace_id="ws", payload={"n": 2}
        ),
        Event(
            id="evt_batch_3", kind="batch.third", workspace_id="ws", payload={"n": 3}
        ),
    ]


def test_append_many_preserves_event_ordering():
    ledger = EventLedger()

    stored = ledger.append_many(_events())

    assert [event.kind for event in stored] == [
        "batch.first",
        "batch.second",
        "batch.third",
    ]
    assert [event.kind for event in ledger.list_events("ws")] == [
        "batch.first",
        "batch.second",
        "batch.third",
    ]


def test_sqlite_append_many_persists_same_events_as_repeated_append(tmp_path):
    batch_db = tmp_path / "batch.db"
    repeated_db = tmp_path / "repeated.db"

    batch = SQLiteEventLedger(str(batch_db))
    repeated = SQLiteEventLedger(str(repeated_db))
    try:
        batch.append_many(_events())
        for event in _events():
            repeated.append(
                event.kind, event.workspace_id, event.payload, actor=event.actor
            )

        batch_events = batch.list_events("ws")
        repeated_events = repeated.list_events("ws")
        assert [
            (event.kind, event.workspace_id, event.payload) for event in batch_events
        ] == [
            (event.kind, event.workspace_id, event.payload) for event in repeated_events
        ]
    finally:
        batch.close()
        repeated.close()


def test_state_projection_after_append_many_replay_matches_repeated_append(tmp_path):
    observed_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    fact = Fact(
        id="fact_batch_runtime",
        subject_id="node115",
        predicate="runtime",
        value="docker",
        evidence_ids=[],
        observed_at=observed_at,
    )
    events = [
        Event(
            id="evt_state_batch_1",
            kind="fact.observed",
            workspace_id="ws",
            payload={"fact": to_plain(fact)},
        )
    ]
    batch = EventLedger()
    repeated = EventLedger()

    batch.append_many(events)
    for event in events:
        repeated.append(
            event.kind, event.workspace_id, event.payload, actor=event.actor
        )

    batch_state = StateProjector(batch).project("ws")
    repeated_state = StateProjector(repeated).project("ws")
    assert batch_state.get_best_fact(
        "node115", "runtime"
    ) == repeated_state.get_best_fact("node115", "runtime")


def test_observation_ingest_keeps_observation_evidence_fact_event_counts():
    ledger = EventLedger()
    observation = Observation(
        id="obs_batch_cpu",
        source_type="provider",
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        subject="node115",
        predicate="cpu.count",
        value=8,
    )

    fact = ObservationIngestor(ledger).ingest(observation, "ws")
    state = StateProjector(ledger).project("ws")

    assert [event.kind for event in ledger.list_events("ws")] == [
        "observation.observed",
        "evidence.observed",
        "fact.observed",
    ]
    assert len(state.observations) == 1
    assert len(state.evidence) == 1
    assert len(state.facts) == 1
    assert fact is not None
    assert fact.id in state.facts


def test_fact_promotion_suppressed_observation_remains_without_fact():
    ledger = EventLedger()
    observation = Observation(
        id="obs_suppressed_uname",
        source_type="provider",
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        subject="node115",
        predicate="os",
        value="linux",
        metadata={
            "fact_promotion_suppressed": True,
            "source_name": "prometheus",
            "prometheus_metric": "node_uname_info",
        },
    )

    fact = ObservationIngestor(ledger).ingest(observation, "ws")
    state = StateProjector(ledger).project("ws")

    assert fact is None
    assert [event.kind for event in ledger.list_events("ws")] == [
        "observation.observed",
        "evidence.observed",
    ]
    assert len(state.observations) == 1
    assert len(state.evidence) == 1
    assert len(state.facts) == 0


def test_sqlite_append_many_uses_one_transaction_for_many_events(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "events.db"))
    statements: list[str] = []
    ledger._connection.set_trace_callback(statements.append)
    try:
        ledger.append_many(_events())
    finally:
        ledger._connection.set_trace_callback(None)
        ledger.close()

    assert sum(1 for statement in statements if statement == "BEGIN ") == 1
    assert sum(1 for statement in statements if statement == "COMMIT") == 1
    assert sum(1 for statement in statements if "INSERT INTO events" in statement) == 3


def _batch_observations() -> list[Observation]:
    return [
        Observation(
            id="obs_batch_cpu_many",
            source_type="provider",
            observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            subject="node115",
            predicate="cpu.count",
            value=8,
        ),
        Observation(
            id="obs_batch_runtime_many",
            source_type="discovery",
            observed_at=datetime(2026, 1, 1, 0, 1, tzinfo=timezone.utc),
            subject="node115",
            predicate="runtime",
            value="docker",
        ),
        Observation(
            id="obs_batch_inferred_many",
            source_type="inferred",
            observed_at=datetime(2026, 1, 1, 0, 2, tzinfo=timezone.utc),
            subject="node115",
            predicate="role",
            value="media",
        ),
    ]


def test_observation_ingest_many_preserves_event_count_and_order():
    ledger = EventLedger()

    facts = ObservationIngestor(ledger).ingest_many(_batch_observations(), "ws")

    assert len(facts) == 3
    assert [event.kind for event in ledger.list_events("ws")] == [
        "observation.observed",
        "evidence.observed",
        "fact.observed",
        "observation.observed",
        "evidence.observed",
        "fact.observed",
        "observation.observed",
        "evidence.observed",
        "fact.inferred",
    ]


def test_observation_ingest_many_projects_same_state_as_repeated_ingest():
    batch = EventLedger()
    repeated = EventLedger()
    observations = _batch_observations()

    ObservationIngestor(batch).ingest_many(observations, "ws")
    repeated_ingestor = ObservationIngestor(repeated)
    for observation in observations:
        repeated_ingestor.ingest(observation, "ws")

    batch_state = StateProjector(batch).project("ws")
    repeated_state = StateProjector(repeated).project("ws")

    assert set(batch_state.observations) == set(repeated_state.observations)
    assert [event.kind for event in batch.list_events("ws")] == [
        event.kind for event in repeated.list_events("ws")
    ]
    assert sorted(
        (fact.subject_id, fact.predicate, fact.value, fact.inferred)
        for fact in batch_state.facts.values()
    ) == sorted(
        (fact.subject_id, fact.predicate, fact.value, fact.inferred)
        for fact in repeated_state.facts.values()
    )


def test_observation_ingest_many_suppressed_promotion_keeps_only_observation_and_evidence():
    ledger = EventLedger()
    observation = Observation(
        id="obs_batch_suppressed_uname",
        source_type="provider",
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        subject="node115",
        predicate="os",
        value="linux",
        metadata={
            "fact_promotion_suppressed": True,
            "source_name": "prometheus",
            "prometheus_metric": "node_uname_info",
        },
    )

    facts = ObservationIngestor(ledger).ingest_many([observation], "ws")

    assert facts == [None]
    assert [event.kind for event in ledger.list_events("ws")] == [
        "observation.observed",
        "evidence.observed",
    ]


def test_observation_ingest_compatibility_uses_batch_path():
    class CountingLedger(EventLedger):
        def __init__(self) -> None:
            super().__init__()
            self.append_many_calls = 0

        def append_many(self, events):  # type: ignore[no-untyped-def]
            self.append_many_calls += 1
            return super().append_many(events)

    ledger = CountingLedger()
    observation = _batch_observations()[0]

    fact = ObservationIngestor(ledger).ingest(observation, "ws")

    assert fact is not None
    assert ledger.append_many_calls == 1
    assert [event.kind for event in ledger.list_events("ws")] == [
        "observation.observed",
        "evidence.observed",
        "fact.observed",
    ]


def test_observation_ingest_many_uses_fewer_sqlite_transactions_than_repeated_ingest(
    tmp_path,
):
    observations = _batch_observations()
    batch = SQLiteEventLedger(str(tmp_path / "batch_observations.db"))
    repeated = SQLiteEventLedger(str(tmp_path / "repeated_observations.db"))
    batch_statements: list[str] = []
    repeated_statements: list[str] = []
    batch._connection.set_trace_callback(batch_statements.append)
    repeated._connection.set_trace_callback(repeated_statements.append)
    try:
        ObservationIngestor(batch).ingest_many(observations, "ws")
        repeated_ingestor = ObservationIngestor(repeated)
        for observation in observations:
            repeated_ingestor.ingest(observation, "ws")
    finally:
        batch._connection.set_trace_callback(None)
        repeated._connection.set_trace_callback(None)
        batch.close()
        repeated.close()

    batch_commits = sum(1 for statement in batch_statements if statement == "COMMIT")
    repeated_commits = sum(
        1 for statement in repeated_statements if statement == "COMMIT"
    )
    assert batch_commits == 1
    assert repeated_commits == len(observations)
    assert batch_commits < repeated_commits


def test_append_many_progress_is_bounded_and_transient():
    from seed_runtime.execution_status import RecordingExecutionStatusConsumer

    ledger = EventLedger()
    events = [
        Event(id=f"evt_write_{index}", kind="batch.progress", workspace_id="ws")
        for index in range(1001)
    ]
    consumer = RecordingExecutionStatusConsumer()

    ledger.append_many(events, status_consumer=consumer)

    progress = [
        status
        for status in consumer.statuses
        if status.phase == "event_persistence"
        and status.current is not None
        and status.total is not None
    ]
    assert [status.current for status in progress] == [0, 1, 501, 1001]
    assert progress[-1].completed is True
    assert [event.id for event in ledger.list_events("ws")] == [
        event.id for event in events
    ]
