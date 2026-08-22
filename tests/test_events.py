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


# Prefixes minted for use inside one process and never written into a durable
# material. Reservation is about a *later* process reissuing an identity, so a
# genuinely process-local one does not need it — but it has to be declared here
# rather than assumed, because that is the judgement someone has to make.
PROCESS_LOCAL_ID_PREFIXES: frozenset = frozenset()


def test_every_minted_prefix_is_reserved_or_declared_process_local():
    """The invariant, held at one boundary instead of one pocket at a time.

    What requires reservation is narrower than "every `new_identity` call": an
    identity must be minted, written into a durable material, and mintable again
    by a later process. `new_identity` promises process uniqueness and nothing more,
    so a genuinely process-local identity should not be dragged into durable
    ledger mechanics merely because it shares a helper.

    Rather than infer which calls are durable — which is the kind of inference
    that allowed this defect three times — every minted prefix must be either
    reserved or **declared** process-local above. Adding a prefix forces that
    decision into the open instead of leaving it to whoever reads the diff.

    """

    import glob
    import os
    import re

    reserved = set(SQLiteEventLedger._RESERVABLE_PREFIXES)
    # `evt` is issued by the durable ledger from its own numbering.
    reserved.add("evt")
    reserved |= PROCESS_LOCAL_ID_PREFIXES

    minted = {}
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pattern = re.compile(r"new_identity\(\s*[\"']([a-z][a-z_]*)[\"']")
    for path in glob.glob(os.path.join(root, "seed_runtime", "*.py")):
        source = open(path, encoding="utf-8").read()
        for match in pattern.finditer(source):
            minted.setdefault(match.group(1), set()).add(os.path.basename(path))

    assert minted, "no minted prefixes were found, so this would pass vacuously"
    undeclared = {
        prefix: sorted(files)
        for prefix, files in minted.items()
        if prefix not in reserved
    }
    assert not undeclared, (
        "these identity prefixes are minted but neither reserved nor declared "
        "process-local, so if any reaches a durable material it restarts at one "
        f"in every process: {undeclared}"
    )


PYTEST_ADMISSION = (
    test_append_records_reality_in_order,
    test_get_returns_appended_event_by_identity,
    test_event_ledger_rejects_secret_fields_in_materials,
    test_event_secret_rejection_preserves_boundary_normalization,
    test_event_secret_rejection_reaches_every_nested_container,
    test_event_secret_rejection_accepts_large_scalar_lists,
    test_durable_large_scalar_lists_do_not_repeat_material_traversal,
    test_every_minted_prefix_is_reserved_or_declared_process_local,
)
