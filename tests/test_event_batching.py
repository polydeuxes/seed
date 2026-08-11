from seed_runtime.event import Event
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.execution_status import RecordingExecutionStatusConsumer


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
    batch = SQLiteEventLedger(str(tmp_path / "batch.db"))
    repeated = SQLiteEventLedger(str(tmp_path / "repeated.db"))
    try:
        batch.append_many(_events())
        for event in _events():
            repeated.append(
                event.kind, event.workspace_id, event.payload, actor=event.actor
            )

        assert [
            (event.kind, event.workspace_id, event.payload)
            for event in batch.list_events("ws")
        ] == [
            (event.kind, event.workspace_id, event.payload)
            for event in repeated.list_events("ws")
        ]
    finally:
        batch.close()
        repeated.close()


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
    reopened = SQLiteEventLedger(str(tmp_path / "events.db"))
    try:
        assert len(reopened.list()) == 3
    finally:
        reopened.close()


def test_append_many_progress_is_bounded_and_transient():
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
