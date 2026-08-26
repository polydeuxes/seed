from seed_runtime.event import Event
from seed_runtime.events import EventLedger, SQLiteEventLedger



def _events() -> list[Event]:
    return [
        Event(
            identity="evt_batch_1", kind="batch.first", material={"n": 1}
        ),
        Event(
            identity="evt_batch_2", kind="batch.second", material={"n": 2}
        ),
        Event(
            identity="evt_batch_3", kind="batch.third", material={"n": 3}
        ),
    ]


def test_append_many_preserves_event_ordering():
    ledger = EventLedger()

    recorded = ledger.append_many(_events())

    assert [event.kind for event in recorded] == [
        "batch.first",
        "batch.second",
        "batch.third",
    ]
    assert [event.kind for event in ledger.list_events()] == [
        "batch.first",
        "batch.second",
        "batch.third",
    ]


def test_append_many_advances_the_process_local_event_identity_number():
    ledger = EventLedger()
    ledger.append_many(
        [Event(identity="evt_000003", kind="supplied.occurrence")]
    )

    assert ledger.append("later.occurrence").identity == "evt_000004"


def test_an_allocated_identity_can_be_carried_by_its_prebuilt_occurrence():
    ledger = EventLedger()

    identity = ledger.allocate_event_identity()
    recorded = ledger.append_many(
        [
            Event(
                identity=identity,
                kind="self.addressed",
                material={"occurrence_identity": identity},
            )
        ]
    )[0]

    assert recorded.material == {"occurrence_identity": recorded.identity}


def test_sqlite_allocated_identity_advances_after_its_occurrence_is_durable(tmp_path):
    database = str(tmp_path / "self-addressed.db")
    ledger = SQLiteEventLedger(database)
    first_identity = ledger.allocate_event_identity()
    first = ledger.append_many(
        [
            Event(
                identity=first_identity,
                kind="self.addressed",
                material={"occurrence_identity": first_identity},
            )
        ]
    )[0]
    ledger.close()

    reopened = SQLiteEventLedger(database)
    try:
        second_identity = reopened.allocate_event_identity()
        second = reopened.append_many(
            [
                Event(
                    identity=second_identity,
                    kind="self.addressed",
                    material={"occurrence_identity": second_identity},
                )
            ]
        )[0]
        assert first.material == {"occurrence_identity": first.identity}
        assert second.material == {"occurrence_identity": second.identity}
        assert second.identity != first.identity
    finally:
        reopened.close()


def test_sqlite_append_many_persists_same_events_as_repeated_append(tmp_path):
    batch = SQLiteEventLedger(str(tmp_path / "batch.db"))
    repeated = SQLiteEventLedger(str(tmp_path / "repeated.db"))
    try:
        batch.append_many(_events())
        for event in _events():
            repeated.append(event.kind, event.material)

        assert [
            (event.kind, event.material)
            for event in batch.list_events()
        ] == [
            (event.kind, event.material)
            for event in repeated.list_events()
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
