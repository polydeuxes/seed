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
        # Added by `#2491` on the same criterion. A durable store persists these
        # subject identities and a later process mints them again, so before
        # they were reserved two independent subjects claimed
        # `system_material_000001` across a reopen.
        "system_invocation",
        "system_material",
        # `#2496` on the same criterion again.
        "transient_material",
        # `#2497` found these by sweeping instead of waiting for a fourth.
        "operator_response_comparison",
        "operator_alternative_identification",
        "presented_alternative",
        # The exact pair-Measurement Act identity is carried durably by its
        # Applicability, responsible-Act Evidence, and result occurrence.
        "adjacent_byte_pair_measurement_act",
        # The performed occurrence is distinct from the proposed exact Act and
        # is likewise carried durably by its Evidence and result.
        "adjacent_byte_pair_measurement_occurrence",
        # Seed-native byte Measurement and pair-input Applicability likewise
        # preserve exact Act identities separately from their occurrences.
        "byte_measurement_act",
        "byte_measurement_occurrence",
        "byte_pair_applicability_act",
        "byte_pair_applicability_occurrence",
    )


# Prefixes minted for use inside one process and never written into a durable
# payload. Reservation is about a *later* process reissuing an identity, so a
# genuinely process-local one does not need it — but it has to be declared here
# rather than assumed, because that is the judgement someone has to make.
PROCESS_LOCAL_ID_PREFIXES: frozenset = frozenset()


def test_every_minted_prefix_is_reserved_or_declared_process_local():
    """The invariant, held mechanically instead of one pocket at a time.

    What requires reservation is narrower than "every `new_id` call": an
    identity must be minted, written into a durable payload, and mintable again
    by a later process. `new_id` promises process uniqueness and nothing more,
    so a genuinely process-local identity should not be dragged into durable
    ledger mechanics merely because it shares a helper.

    Rather than infer which calls are durable — which is the kind of inference
    that produced this defect three times — every minted prefix must be either
    reserved or **declared** process-local above. Adding a prefix forces that
    decision into the open instead of leaving it to whoever reads the diff.

    Answered locally three times before this existed: `system_material` in
    `#2491`, an exchange identity in `#2493`, `transient_material` in `#2496`.
    """

    import glob
    import os
    import re

    reserved = set(SQLiteEventLedger._RESERVABLE_PREFIXES)
    reserved |= set(SQLiteEventLedger._PERSISTED_ID_PREFIXES)
    # `evt` is issued by the durable ledger from its own numbering.
    reserved.add("evt")
    reserved |= PROCESS_LOCAL_ID_PREFIXES

    minted = {}
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pattern = re.compile(r"new_id\(\s*[\"']([a-z][a-z_]*)[\"']")
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
        "process-local, so if any reaches a durable payload it restarts at one "
        f"in every process: {undeclared}"
    )
