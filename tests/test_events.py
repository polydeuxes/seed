import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger


def test_append_records_reality_in_order():
    ledger = EventLedger()

    ledger.append("user.message")
    ledger.append("result_condition.recorded")

    assert len(ledger.list()) == 2
    assert ledger.list()[0].kind == "user.message"
    assert ledger.list()[1].kind == "result_condition.recorded"


def test_get_returns_appended_event_by_identity():
    ledger = EventLedger()

    event = ledger.append("user.message")

    assert ledger.get(event.identity) == event


def test_event_ledger_rejects_secret_fields_in_materials():
    ledger = EventLedger()

    for field in ("password", "passphrase", "token", "private_key"):
        try:
            ledger.append("tool.call_requested", {field: "not-accepted"})
        except ValueError as exc:
            assert "secret field" in str(exc)
        else:
            raise AssertionError(f"{field} must be rejected")


@pytest.mark.parametrize(
    "field",
    (
        "TOKEN",
        " token ",
        "PRIVATE-KEY",
        " PassPhrase ",
        "PASSWORD",
    ),
)
def test_event_secret_rejection_preserves_boundary_normalization(field):
    with pytest.raises(ValueError, match="secret field"):
        EventLedger().append("k", {"outer": [{field: "not-accepted"}]})


@pytest.mark.parametrize(
    "material",
    (
        {"token": "not-accepted"},
        {"outer": {"token": "not-accepted"}},
        {"outer": [{"token": "not-accepted"}]},
        {"outer": [[{"token": "not-accepted"}]]},
    ),
)
def test_event_secret_rejection_reaches_every_nested_container(material):
    with pytest.raises(ValueError, match="secret field"):
        EventLedger().append("k", material)


def test_event_secret_rejection_accepts_large_scalar_lists():
    material = {"input_event_identities": [f"evt_{index}" for index in range(10_000)]}

    event = EventLedger().append("k", material)

    assert event.material == material


def test_durable_large_scalar_lists_do_not_repeat_material_traversal(
    tmp_path, monkeypatch
):
    ledger = SQLiteEventLedger(str(tmp_path / "seed.db"))
    material = {"input_event_identities": [f"evt_{index}" for index in range(10_000)]}
    event = ledger.append("k", material)

    def unexpected_second_traversal(*args, **kwargs):
        raise AssertionError("durable material was screened during JSON decoding")

    monkeypatch.setattr(
        "seed_runtime.event._require_preservable_material", unexpected_second_traversal
    )

    assert ledger.get(event.identity).material == material
    ledger.close()
