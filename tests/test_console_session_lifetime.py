"""A console lifetime is one bounded exchange, and owns its own session id.

`--session` defaulted to the constant `local`, so every console lifetime
addressed the one named session. Reopening the console continued the previous
exchange's Standing, because as far as the projection was concerned it was the
previous exchange.

These tests pin the boundary: two lifetimes in one workspace and one ledger
receive different session ids, each keeps its own C0 and ingress, and the second
does not inherit the first's Standing.

They also pin what did **not** change. `--session` still exists for the
subcommands, which address a session that already exists, and a caller passing
`session_id` directly still owns that choice.
"""

from __future__ import annotations

from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_session_standing import (
    project_operator_session_standing,
)
from seed_runtime.preserved_material_measurement import (
    preserved_ingress_occurrences,
)
from scripts import seed_local


@pytest.fixture
def shared_ledger(monkeypatch):
    """One ledger across console lifetimes, which the CLI cannot supply itself.

    The bare console constructs `EventLedger()` and never consults `--db`, so
    two real invocations never share history. That is recorded as a finding
    rather than repaired here; this fixture supplies what the CLI does not so
    the session boundary can be observed at all.
    """
    ledger = EventLedger()
    monkeypatch.setattr(seed_local, "EventLedger", lambda: ledger)
    return ledger


def _console(monkeypatch, material: str) -> None:
    monkeypatch.setattr("sys.stdin", StringIO(material + "exit\n"))
    monkeypatch.setattr("sys.stdout", StringIO())
    assert seed_local.main([]) == 0


def _sessions(ledger: EventLedger) -> list[str]:
    seen: list[str] = []
    for event in ledger.list("local"):
        if event.session_id is not None and event.session_id not in seen:
            seen.append(event.session_id)
    return seen


# --------------------------------------------------------------------------
# Two lifetimes, one workspace.
# --------------------------------------------------------------------------


def test_two_console_lifetimes_receive_different_session_ids(
    shared_ledger, monkeypatch
):
    _console(monkeypatch, "first exchange\n")
    _console(monkeypatch, "second exchange\n")

    sessions = _sessions(shared_ledger)
    assert len(sessions) == 2
    assert sessions[0] != sessions[1]


def test_neither_lifetime_uses_the_constant_default(shared_ledger, monkeypatch):
    _console(monkeypatch, "an exchange\n")
    assert seed_local.DEFAULT_SESSION not in _sessions(shared_ledger)


def test_both_lifetimes_share_one_workspace(shared_ledger, monkeypatch):
    _console(monkeypatch, "first exchange\n")
    _console(monkeypatch, "second exchange\n")

    assert {event.workspace_id for event in shared_ledger.list("local")} == {"local"}


# --------------------------------------------------------------------------
# Each lifetime keeps its own occurrences.
# --------------------------------------------------------------------------


def test_each_lifetime_holds_only_its_own_ingress(shared_ledger, monkeypatch):
    _console(monkeypatch, "first exchange\n")
    _console(monkeypatch, "second exchange\n")
    first, second = _sessions(shared_ledger)

    def material(session_id):
        return [
            event.payload["decoded_text"]
            for event in preserved_ingress_occurrences(
                shared_ledger, workspace_id="local", session_id=session_id
            )
        ]

    assert material(first) == ["first exchange\n"]
    assert material(second) == ["second exchange\n"]


def test_each_lifetime_forms_its_own_c0(shared_ledger, monkeypatch):
    _console(monkeypatch, "first exchange\n")
    _console(monkeypatch, "second exchange\n")
    first, second = _sessions(shared_ledger)

    def presentations(session_id):
        return project_operator_session_standing(
            shared_ledger, workspace_id="local", session_id=session_id
        )["presentations"]

    assert presentations(first)
    assert presentations(second)
    assert set(presentations(first)).isdisjoint(presentations(second))


def test_a_reopened_console_does_not_continue_the_prior_standing(
    shared_ledger, monkeypatch
):
    """The defect this fixes, stated as the behaviour it removes."""
    _console(monkeypatch, "first exchange\nsecond material\n")
    _console(monkeypatch, "a later exchange\n")
    first, second = _sessions(shared_ledger)

    prior = project_operator_session_standing(
        shared_ledger, workspace_id="local", session_id=first
    )
    later = project_operator_session_standing(
        shared_ledger, workspace_id="local", session_id=second
    )

    # The first lifetime held two interactions plus C0; the second holds C0 and
    # one.  A continued session would show the second carrying all of them.
    assert len(prior["presentations"]) == 3
    assert len(later["presentations"]) == 2
    assert set(later["presentations"]).isdisjoint(prior["presentations"])


# --------------------------------------------------------------------------
# What did not change.
# --------------------------------------------------------------------------


def test_a_caller_supplying_a_session_id_still_owns_it():
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="chosen-by-the-caller",
        input_stream=StringIO("material\nexit\n"),
        output_stream=StringIO(),
    )
    assert {event.session_id for event in ledger.list("w")} == {
        "chosen-by-the-caller"
    }


def test_the_session_argument_remains_for_the_subcommands():
    args = seed_local.build_parser().parse_args([])
    assert args.session == seed_local.DEFAULT_SESSION
