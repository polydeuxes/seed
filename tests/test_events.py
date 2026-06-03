from seed_runtime.events import EventLedger, SQLiteEventLedger


def test_append_records_reality_in_order():
    ledger = EventLedger()

    ledger.append("user.message")
    ledger.append("goal.created")

    assert len(ledger.list()) == 2
    assert ledger.list()[0].kind == "user.message"
    assert ledger.list()[1].kind == "goal.created"


def test_get_returns_appended_event_by_id():
    ledger = EventLedger()

    event = ledger.append("user.message")

    assert ledger.get(event.id) == event


def test_sqlite_execution_authorization_events_are_ephemeral(tmp_path):
    db_path = tmp_path / "events.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    try:
        event = ledger.append(
            "execution_authorization.granted",
            "ws",
            {
                "execution_authorization": {
                    "id": "auth_1",
                    "action_plan_id": "plan_1",
                    "tool_name": "restart_container",
                    "arguments_fingerprint": "abc123",
                    "granted_by": "operator@example.com",
                    "expires_at": "2026-06-03T00:05:00+00:00",
                    "credential_grant_id": "jit_1",
                    "session_id": "ses_1",
                    "metadata": {"reason": "one attempt"},
                }
            },
        )
        assert ledger.get(event.id) is not None
        assert [stored.kind for stored in ledger.list_events("ws")] == [
            "execution_authorization.granted"
        ]
    finally:
        ledger.close()

    reopened = SQLiteEventLedger(str(db_path))
    try:
        assert reopened.list_events("ws") == []
    finally:
        reopened.close()
