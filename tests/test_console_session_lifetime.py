"""A console lifetime is one bounded exchange carrying its exact session id.

`--session` defaulted to the constant `local`, so every console lifetime
addressed the one named session. That could not bite while the ledger was
process-local — the previous lifetime's events were gone before the next opened
— but `--db` makes them survive, and then a reopened console would continue an
exchange that had ended.

`--db` also could not reach the console at all: the console was the no-argument
entry, and `--db` made the argument list non-empty.

These tests pin both halves together, because neither is safe alone.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime import process_entry
from seed_runtime.operator_locality_standing import (
    read_operator_locality_standing,
)
from seed_runtime.preserved_material_measurement import (
    preserved_ingress_occurrences,
)


@pytest.fixture
def db(tmp_path):
    return str(tmp_path / "seed.db")


def _console(monkeypatch, material: str, argv: list[str]) -> None:
    monkeypatch.setattr("sys.stdin", binary_input(material))
    monkeypatch.setattr("sys.stdout", StringIO())
    assert process_entry.main(argv) == 0


def _sessions(ledger: EventLedger, workspace_id: str = "local") -> list[str]:
    seen: list[str] = []
    for event in ledger.list(workspace_id):
        if event.locality_id is not None and event.locality_id not in seen:
            seen.append(event.locality_id)
    return seen


# --------------------------------------------------------------------------
# `--db` reaches the console.
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "argv",
    [[], ["--db", "x"], ["--db=x"], ["--workspace", "w", "--db", "x"]],
)
def test_console_options_alone_select_the_console(argv):
    process_entry.build_parser().parse_args(argv)


@pytest.mark.parametrize(
    "argv",
    [["--show-inference-catalog"], ["--db", "x", "--show-inference-catalog"]],
)
def test_any_other_argument_selects_something_else(argv):
    with pytest.raises(SystemExit, match="2"):
        process_entry.build_parser().parse_args(argv)


def test_a_db_console_records_into_that_db(db, monkeypatch):
    _console(monkeypatch, "material\n", ["--db", db])

    ledger = SQLiteEventLedger(db)
    try:
        assert ledger.list("local")
    finally:
        ledger.close()


def test_the_bare_console_writes_no_durable_history(db, monkeypatch):
    _console(monkeypatch, "material\n", [])

    ledger = SQLiteEventLedger(db)
    try:
        assert ledger.list("local") == []
    finally:
        ledger.close()


# --------------------------------------------------------------------------
# Two lifetimes, one durable workspace.
# --------------------------------------------------------------------------


@pytest.fixture
def two_lifetimes(db, monkeypatch):
    _console(monkeypatch, "first exchange\nmore material\n", ["--db", db])
    _console(monkeypatch, "a later exchange\n", ["--db", db])
    ledger = SQLiteEventLedger(db)
    yield ledger
    ledger.close()


def test_two_console_lifetimes_receive_different_session_ids(two_lifetimes):
    sessions = _sessions(two_lifetimes)
    assert len(sessions) == 2
    assert sessions[0] != sessions[1]


def test_both_lifetimes_share_one_workspace(two_lifetimes):
    assert {e.workspace_id for e in two_lifetimes.list("local")} == {"local"}


def test_each_lifetime_holds_only_its_own_ingress(two_lifetimes):
    first, second = _sessions(two_lifetimes)

    def material(locality_id):
        return [
            bytes.fromhex(
                two_lifetimes.get(event.payload["raw_material_event_id"]).payload[
                    "exact_bytes_hex"
                ]
            )
            for event in preserved_ingress_occurrences(
                two_lifetimes, workspace_id="local", locality_id=locality_id
            )
        ]

    assert material(first) == [b"first exchange\n", b"more material\n"]
    assert material(second) == [b"a later exchange\n"]


def test_a_reopened_console_does_not_continue_the_prior_standing(two_lifetimes):
    """The defect, stated as the behaviour it removes.

    This is the test that could not previously be written against the real CLI,
    because two invocations never shared history to continue.
    """
    first, second = _sessions(two_lifetimes)
    prior = read_operator_locality_standing(
        two_lifetimes, workspace_id="local", locality_id=first
    )
    later = read_operator_locality_standing(
        two_lifetimes, workspace_id="local", locality_id=second
    )

    assert len(prior["representations"]) == 3
    assert len(later["representations"]) == 2
    assert set(later["representations"]).isdisjoint(prior["representations"])


def test_the_earlier_lifetime_remains_projectable(two_lifetimes):
    """Bounding the read must not lose what it stopped reading."""
    first = _sessions(two_lifetimes)[0]
    standing = read_operator_locality_standing(
        two_lifetimes, workspace_id="local", locality_id=first
    )
    assert len(standing["representations"]) == 3


# --------------------------------------------------------------------------
# A session read reads a session.
# --------------------------------------------------------------------------


def test_a_session_read_returns_only_that_session(two_lifetimes):
    first, second = _sessions(two_lifetimes)
    for locality_id in (first, second):
        events = two_lifetimes.list_locality("local", locality_id)
        assert events
        assert {e.locality_id for e in events} == {locality_id}
    assert len(two_lifetimes.list_locality("local", first)) + len(
        two_lifetimes.list_locality("local", second)
    ) == len(two_lifetimes.list("local"))


def test_a_fresh_session_reads_none_of_the_history(two_lifetimes):
    """The console's startup read, which is the growing read."""
    assert two_lifetimes.list("local")
    assert two_lifetimes.list_locality("local", "never-recorded") == []
    standing = read_operator_locality_standing(
        two_lifetimes, workspace_id="local", locality_id="never-recorded"
    )
    assert standing["representations"] == {}


def test_the_in_memory_ledger_scopes_the_same_way():
    ledger = EventLedger()
    for locality_id in ("a", "b"):
        run_persistent_operator_console(
            ledger=ledger,
            workspace_id="w",
            locality_id=locality_id,
            input_stream=binary_input("material\n"),
            output_stream=StringIO(),
        )
    assert {e.locality_id for e in ledger.list_locality("w", "a")} == {"a"}
    assert len(ledger.list_locality("w", "a")) < len(ledger.list("w"))


# --------------------------------------------------------------------------
# What did not change.
# --------------------------------------------------------------------------


def test_a_caller_supplied_session_id_remains_exact():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        locality_id="chosen-by-the-caller",
        input_stream=binary_input("material\n"),
        output_stream=StringIO(),
    )
    assert {event.locality_id for event in ledger.list("w")} == {
        "chosen-by-the-caller"
    }


# --------------------------------------------------------------------------
# Separate processes, which is how the console is actually reopened.
# --------------------------------------------------------------------------


def _run_console_process(db: str, material: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "seed_runtime.process_entry", "--db", db],
        input=material + "",
        capture_output=True,
        text=True,
        cwd=str(pathlib.Path(__file__).resolve().parent.parent),
    )


def test_a_reopened_console_process_does_not_abort(db):
    """`new_id` counts from 1 per process, so durable ids must be reserved.

    Every other test here runs its lifetimes inside one process, where the
    counters keep climbing and no identifier is ever reissued. The second real
    `seed --db` invocation aborted on `duplicate representation reference` until
    the console's prefixes were reserved on open.
    """
    for material in ("first process\n", "second process\n", "third process\n"):
        result = _run_console_process(db, material)
        assert result.returncode == 0, result.stderr
        assert "Traceback" not in result.stderr


def test_separate_processes_receive_separate_sessions(db):
    for material in ("first process\n", "second process\n", "third process\n"):
        assert _run_console_process(db, material).returncode == 0

    ledger = SQLiteEventLedger(db)
    try:
        sessions = _sessions(ledger)
        assert len(sessions) == 3
        held = [
            [
                bytes.fromhex(
                    ledger.get(event.payload["raw_material_event_id"]).payload[
                        "exact_bytes_hex"
                    ]
                )
                for event in preserved_ingress_occurrences(
                    ledger, workspace_id="local", locality_id=session
                )
            ]
            for session in sessions
        ]
        assert held == [
            [b"first process\n"],
            [b"second process\n"],
            [b"third process\n"],
        ]
    finally:
        ledger.close()
