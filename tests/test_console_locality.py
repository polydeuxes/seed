"""Each console locality remains exact."""

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
from seed_runtime.material_ingest import (
    ingested_material_bytes,
    iter_exact_ingest_results,
)


@pytest.fixture
def db(tmp_path):
    return str(tmp_path / "seed.db")


def _console(monkeypatch, material: str, argv: list[str]) -> None:
    monkeypatch.setattr("sys.stdin", binary_input(material))
    monkeypatch.setattr("sys.stdout", StringIO())
    assert process_entry.main(argv) == 0


def _localities(ledger: EventLedger) -> list[str]:
    seen: list[str] = []
    for event in ledger.list():
        if event.locality_identity is not None and event.locality_identity not in seen:
            seen.append(event.locality_identity)
    return seen


def _ingest_occurrences(ledger, *, locality_identity):
    return list(iter_exact_ingest_results(ledger, locality_identity))


# --------------------------------------------------------------------------
# `--db` reaches the console.
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "argv",
    [[], ["--db", "x"], ["--db=x"]],
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
        assert ledger.list()
    finally:
        ledger.close()


def test_the_bare_console_writes_no_durable_history(db, monkeypatch):
    _console(monkeypatch, "material\n", [])

    ledger = SQLiteEventLedger(db)
    try:
        assert ledger.list() == []
    finally:
        ledger.close()


# --------------------------------------------------------------------------
# Two console Localities.
# --------------------------------------------------------------------------


@pytest.fixture
def two_lifetimes(db, monkeypatch):
    _console(monkeypatch, "first locality\nmore material\n", ["--db", db])
    _console(monkeypatch, "a later locality\n", ["--db", db])
    ledger = SQLiteEventLedger(db)
    yield ledger
    ledger.close()


def test_two_console_lifetimes_receive_different_locality_identities(two_lifetimes):
    Localities = _localities(two_lifetimes)
    assert len(Localities) == 2
    assert Localities[0] != Localities[1]


def test_each_lifetime_holds_only_its_own_ingress(two_lifetimes):
    first, second = _localities(two_lifetimes)

    def material(locality_identity):
        return [
            ingested_material_bytes(event)
            for event in _ingest_occurrences(
                two_lifetimes, locality_identity=locality_identity
            )
        ]

    assert material(first) == [b"first locality\n", b"more material\n"]
    assert material(second) == [b"a later locality\n"]


def test_a_reopened_console_does_not_continue_the_prior_standing(two_lifetimes):
    """The defect, stated as the behaviour it removes.

    This is the test that could not previously be written against the real CLI,
    because two invocations never shared history to continue.
    """
    first, second = _localities(two_lifetimes)
    prior = read_operator_locality_standing(
        two_lifetimes, locality_identity=first
    )
    later = read_operator_locality_standing(
        two_lifetimes, locality_identity=second
    )

    assert len(prior["representations"]) == 5
    assert len(later["representations"]) == 3
    assert set(later["representations"]).isdisjoint(prior["representations"])


def test_the_earlier_lifetime_remains_projectable(two_lifetimes):
    """Bounding the read must not lose what it stopped read."""
    first = _localities(two_lifetimes)[0]
    standing = read_operator_locality_standing(
        two_lifetimes, locality_identity=first
    )
    assert len(standing["representations"]) == 5


# --------------------------------------------------------------------------
# A locality read reads a locality.
# --------------------------------------------------------------------------


def test_a_locality_read_returns_only_that_locality(two_lifetimes):
    first, second = _localities(two_lifetimes)
    for locality_identity in (first, second):
        events = two_lifetimes.list_locality(locality_identity)
        assert events
        assert {e.locality_identity for e in events} == {locality_identity}
    assert len(two_lifetimes.list_locality(first)) + len(
        two_lifetimes.list_locality(second)
    ) == len(two_lifetimes.list())


def test_a_fresh_locality_reads_none_of_the_history(two_lifetimes):
    """The console's startup read, which is the growing read."""
    assert two_lifetimes.list()
    assert two_lifetimes.list_locality("never-recorded") == []
    standing = read_operator_locality_standing(
        two_lifetimes, locality_identity="never-recorded"
    )
    assert standing["representations"] == {}


def test_the_in_memory_ledger_scopes_the_same_way():
    ledger = EventLedger()
    for locality_identity in ("a", "b"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity=locality_identity,
            input_stream=binary_input("material\n"),
            output_stream=StringIO(),
        )
    assert {e.locality_identity for e in ledger.list_locality("a")} == {"a"}
    assert len(ledger.list_locality("a")) < len(ledger.list())


# --------------------------------------------------------------------------
# What did not revision.
# --------------------------------------------------------------------------


def test_a_caller_supplied_locality_identity_remains_exact():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="chosen-by-the-caller",
        input_stream=binary_input("material\n"),
        output_stream=StringIO(),
    )
    assert {event.locality_identity for event in ledger.list()} == {
        "chosen-by-the-caller"
    }


def test_unrecorded_locality_named_list_is_refused_without_direct_output():
    ledger = EventLedger()
    output = StringIO()

    with pytest.raises(ValueError, match="existing Locality"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="current",
            input_stream=binary_input("/locality list\n"),
            output_stream=output,
        )

    assert output.getvalue() == ""


# --------------------------------------------------------------------------
# Separate processes, which is how the console is actually reopened.
# --------------------------------------------------------------------------


def _run_console_process(db: str, material: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "seed_runtime.process_entry", "--db", db],
        input=material + "",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True,
        cwd=str(pathlib.Path(__file__).resolve().parent.parent),
    )


def test_a_reopened_console_process_does_not_abort(db):
    """`new_identity` counts from 1 per process, so durable identities must be reserved.

    Every other test here runs its lifetimes inside one process, where the
    counters keep climbing and no identity is ever reissued. The second real
    `seed --db` invocation aborted on `duplicate representation reference` until
    the console's prefixes were reserved on open.
    """
    for material in ("first process\n", "second process\n", "third process\n"):
        result = _run_console_process(db, material)
        assert result.returncode == 0, result.stderr
        assert "Traceback" not in result.stderr


def test_separate_processes_receive_separate_localities(db):
    for material in ("first process\n", "second process\n", "third process\n"):
        assert _run_console_process(db, material).returncode == 0

    ledger = SQLiteEventLedger(db)
    try:
        Localities = _localities(ledger)
        assert len(Localities) == 3
        held = [
            [
                ingested_material_bytes(event)
                for event in _ingest_occurrences(
                    ledger, locality_identity=locality
                )
            ]
            for locality in Localities
        ]
        assert held == [
            [b"first process\n"],
            [b"second process\n"],
            [b"third process\n"],
        ]
    finally:
        ledger.close()


FIDELITY_SUBJECTS = {
    "operator_entry": (
        test_console_options_alone_select_the_console,
        test_any_other_argument_selects_something_else,
        test_a_db_console_records_into_that_db,
        test_the_bare_console_writes_no_durable_history,
    ),
    "operator_Locality_occurrence": (
        test_two_console_lifetimes_receive_different_locality_identities,
        test_each_lifetime_holds_only_its_own_ingress,
        test_a_reopened_console_does_not_continue_the_prior_standing,
        test_the_earlier_lifetime_remains_projectable,
        test_a_locality_read_returns_only_that_locality,
        test_a_fresh_locality_reads_none_of_the_history,
        test_the_in_memory_ledger_scopes_the_same_way,
        test_a_caller_supplied_locality_identity_remains_exact,
        test_unrecorded_locality_named_list_is_refused_without_direct_output,
        test_a_reopened_console_process_does_not_abort,
        test_separate_processes_receive_separate_localities,
    ),
}
