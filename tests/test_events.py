from seed_runtime.events import EventLedger


def test_append_and_list_events_by_workspace():
    ledger = EventLedger()
    first = ledger.append("input.user_message", "ws_1", {"text": "hello"}, actor="user", session_id="ses_1")
    ledger.append("input.user_message", "ws_2", {"text": "other"}, actor="user")

    events = ledger.list_events("ws_1")

    assert [event.id for event in events] == [first.id]
    assert events[0].payload == {"text": "hello"}
    assert events[0].session_id == "ses_1"
