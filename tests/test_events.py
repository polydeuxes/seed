import pytest

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


def test_durable_actor_is_a_preserved_label_not_a_closed_grammar(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "seed.db"))

    event = ledger.append("k", "w", actor="source-local-label")

    assert ledger.get(event.id).actor == "source-local-label"
    ledger.close()


def test_event_ledger_rejects_secret_fields_in_payloads():
    ledger = EventLedger()

    for field in ("password", "passphrase", "token", "private_key"):
        try:
            ledger.append("tool.call_requested", "ws", {field: "not-accepted"})
        except ValueError as exc:
            assert "secret field" in str(exc)
        else:
            raise AssertionError(f"{field} must be rejected")


@pytest.mark.parametrize(
    "payload",
    (
        {"token": "not-accepted"},
        {"outer": {"token": "not-accepted"}},
        {"outer": [{"token": "not-accepted"}]},
        {"outer": [[{"token": "not-accepted"}]]},
    ),
)
def test_event_secret_rejection_reaches_every_nested_container(payload):
    with pytest.raises(ValueError, match="secret field"):
        EventLedger().append("k", "w", payload)


def test_event_secret_rejection_accepts_large_scalar_lists():
    payload = {"consumed_event_ids": [f"evt_{index}" for index in range(10_000)]}

    event = EventLedger().append("k", "w", payload)

    assert event.payload == payload


def test_durable_large_scalar_lists_do_not_repeat_secret_traversal(
    tmp_path, monkeypatch
):
    ledger = SQLiteEventLedger(str(tmp_path / "seed.db"))
    payload = {"consumed_event_ids": [f"evt_{index}" for index in range(10_000)]}
    event = ledger.append("k", "w", payload)

    def unexpected_second_traversal(*args, **kwargs):
        raise AssertionError("durable payload was screened during JSON decoding")

    monkeypatch.setattr(
        "seed_runtime.event.reject_secret_fields", unexpected_second_traversal
    )

    assert ledger.get(event.id).payload == payload
    ledger.close()


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
        # Added by `#2413`, which gave the console a durable ledger. They are
        # here because the console persists them and a later process mints
        # them again, not because they were found nearby.
        "operator_presentation",
        "operator_ingress_attempt",
        "operator_material",
        "session",
    )
