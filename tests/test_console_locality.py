"""Operator Locality is exact."""

from __future__ import annotations

import pathlib
import subprocess
import sys
from io import BytesIO
from types import SimpleNamespace

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime import process_entry
from seed_runtime.operator_current_coordinates import (
    read_operator_current_coordinates,
)
from seed_runtime.material_source import (
    exact_material_result_bytes,
    iter_exact_material_results,
)


@pytest.fixture
def db(tmp_path):
    return str(tmp_path / "seed.db")


@pytest.fixture(autouse=True)
def _skip_unrelated_measurement_work(monkeypatch):
    monkeypatch.setattr(
        "seed_runtime.operator_console._record_declared_measurements_from_carried_current_coordinates",
        lambda _ledger, current_coordinates, *, locality_identity: SimpleNamespace(
            current_coordinates=current_coordinates,
            result_occurrences=(),
        ),
    )


def _console(monkeypatch, material: bytes, argv: list[str]) -> None:
    monkeypatch.setattr("sys.stdin", BytesIO(material))
    assert process_entry.main(argv) == 0


def _localities(ledger: EventLedger) -> list[str]:
    seen: list[str] = []
    for event in ledger.list():
        if event.locality_identity is not None and event.locality_identity not in seen:
            seen.append(event.locality_identity)
    return seen


def _acquisition_results(ledger, *, locality_identity):
    return list(iter_exact_material_results(ledger, locality_identity))


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
    _console(monkeypatch, b"material\n", ["--db", db])

    ledger = SQLiteEventLedger(db)
    try:
        assert ledger.list()
    finally:
        ledger.close()


def test_the_bare_console_writes_no_durable_history(db, monkeypatch):
    _console(monkeypatch, b"material\n", [])

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
    _console(monkeypatch, b"first\nmore\n", ["--db", db])
    _console(monkeypatch, b"later\n", ["--db", db])
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
            exact_material_result_bytes(event)
            for event in _acquisition_results(
                two_lifetimes, locality_identity=locality_identity
            )
        ]

    assert material(first) == [b"first\n", b"more\n"]
    assert material(second) == [b"later\n"]


def test_a_reopened_console_has_distinct_current_coordinates(two_lifetimes):
    first, second = _localities(two_lifetimes)
    prior = read_operator_current_coordinates(
        two_lifetimes, locality_identity=first
    )
    later = read_operator_current_coordinates(
        two_lifetimes, locality_identity=second
    )

    assert prior["exact_result_occurrences"]
    assert later["exact_result_occurrences"]
    assert set(later["exact_result_occurrences"]).isdisjoint(
        prior["exact_result_occurrences"]
    )


def test_the_earlier_lifetime_remains_readable(two_lifetimes):
    first = _localities(two_lifetimes)[0]
    assert [
        exact_material_result_bytes(event)
        for event in _acquisition_results(
            two_lifetimes, locality_identity=first
        )
    ] == [b"first\n", b"more\n"]


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
    current = read_operator_current_coordinates(
        two_lifetimes, locality_identity="never-recorded"
    )
    assert current["exact_result_occurrences"] == {}


def test_the_in_memory_ledger_scopes_the_same_way():
    ledger = EventLedger()
    for locality_identity in ("a", "b"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity=locality_identity,
            input_stream=BytesIO(b"material\n"),
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
        input_stream=BytesIO(b"material\n"),
    )
    assert {event.locality_identity for event in ledger.list()} == {
        "chosen-by-the-caller"
    }


# --------------------------------------------------------------------------
# Separate processes, which is how the console is actually reopened.
# --------------------------------------------------------------------------


def _run_console_process(db: str, material: bytes) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "seed_runtime.process_entry", "--db", db],
        input=material,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        cwd=str(pathlib.Path(__file__).resolve().parent.parent),
    )


def test_a_reopened_console_process_does_not_abort(db):
    """A reopened durable Ledger does not reissue an existing identity."""
    for material in (b"a", b"b", b"c"):
        result = _run_console_process(db, material)
        assert result.returncode == 0, result.stderr
        assert b"Traceback" not in result.stderr


def test_separate_processes_receive_separate_localities(db):
    for material in (b"a", b"b", b"c"):
        assert _run_console_process(db, material).returncode == 0

    ledger = SQLiteEventLedger(db)
    try:
        Localities = _localities(ledger)
        assert len(Localities) == 3
        held = [
            [
                exact_material_result_bytes(event)
                for event in _acquisition_results(
                    ledger, locality_identity=locality
                )
            ]
            for locality in Localities
        ]
        assert held == [
            [b"a"],
            [b"b"],
            [b"c"],
        ]
    finally:
        ledger.close()
