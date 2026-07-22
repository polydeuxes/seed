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


def test_event_ledger_rejects_secret_fields_in_payloads():
    ledger = EventLedger()

    for field in ("password", "passphrase", "token", "private_key"):
        try:
            ledger.append("tool.call_requested", "ws", {field: "not-accepted"})
        except ValueError as exc:
            assert "secret field" in str(exc)
        else:
            raise AssertionError(f"{field} must be rejected")


def test_sqlite_persisted_id_prefixes_exclude_deleted_planning_artifacts():
    assert "plan" not in SQLiteEventLedger._PERSISTED_ID_PREFIXES
    assert "handoff" not in SQLiteEventLedger._PERSISTED_ID_PREFIXES
    assert "auth" not in SQLiteEventLedger._PERSISTED_ID_PREFIXES
    assert SQLiteEventLedger._PERSISTED_ID_PREFIXES == (
        "obs",
        "obs_local_host",
        "evd",
        "evd_obs",
        "fact",
        "fact_obs",
        "need",
    )
