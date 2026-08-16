"""Exact Locality reads."""

from __future__ import annotations

import sqlite3
from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingested_material_bytes,
)
from seed_runtime.operator_console import run_persistent_operator_console

BODIES = {
    "s1": "a noun is a word\nand a verb is a word\n",
    "s2": "the cat sat on the mat\nthe mat was flat\n",
    "s3": "one two three\nfour five six\n",
}


def _all_locality_occurrences(ledger, *, locality_identity):
    return [
        event
        for event in ledger.list()
        if event.locality_identity == locality_identity
        and event.kind == MATERIAL_INGEST_OCCURRED_KIND
    ]


def _ingest_occurrences(ledger, *, locality_identity):
    return list(
        ledger.iter_locality_kind(
            locality_identity,
            MATERIAL_INGEST_OCCURRED_KIND,
        )
    )


def _fill(ledger):
    for locality_identity, material in BODIES.items():
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity=locality_identity,
            input_stream=binary_input(material + ""),
            output_stream=StringIO(),
        )
    return ledger


@pytest.fixture
def memory_ledger():
    return _fill(EventLedger())


@pytest.fixture
def durable_ledger(tmp_path):
    ledger = _fill(SQLiteEventLedger(str(tmp_path / "seed.db")))
    yield ledger
    ledger.close()


# --------------------------------------------------------------------------
# The result is preserved.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("locality_identity", sorted(BODIES))
def test_the_occurrences_are_identical_in_memory(memory_ledger, locality_identity):
    bounded = _ingest_occurrences(
        memory_ledger, locality_identity=locality_identity
    )
    whole = _all_locality_occurrences(
        memory_ledger, locality_identity=locality_identity
    )
    assert bounded
    assert [e.identity for e in bounded] == [e.identity for e in whole]
    assert [e.material for e in bounded] == [e.material for e in whole]


@pytest.mark.parametrize("locality_identity", sorted(BODIES))
def test_the_occurrences_are_identical_durably(durable_ledger, locality_identity):
    bounded = _ingest_occurrences(
        durable_ledger, locality_identity=locality_identity
    )
    whole = _all_locality_occurrences(
        durable_ledger, locality_identity=locality_identity
    )
    assert bounded
    assert [e.identity for e in bounded] == [e.identity for e in whole]
    assert [e.material for e in bounded] == [e.material for e in whole]


def test_each_body_still_gets_only_its_own_material(durable_ledger):
    held = {
        locality_identity: [
            ingested_material_bytes(event)
            for event in _ingest_occurrences(
                durable_ledger, locality_identity=locality_identity
            )
        ]
        for locality_identity in BODIES
    }
    assert held == {
        locality_identity: [line.encode() for line in material.splitlines(keepends=True)]
        for locality_identity, material in BODIES.items()
    }


def test_an_unrecorded_locality_reads_empty(durable_ledger):
    assert (
        _ingest_occurrences(
            durable_ledger, locality_identity="never-recorded"
        )
        == []
    )


@pytest.mark.parametrize("ledger_name", ("memory_ledger", "durable_ledger"))
def test_one_kind_is_streamed_from_only_one_locality(request, ledger_name):
    ledger = request.getfixturevalue(ledger_name)
    occurrences = ledger.iter_locality_kind(
        "s1",
        MATERIAL_INGEST_OCCURRED_KIND,
    )

    assert iter(occurrences) is occurrences
    events = list(occurrences)
    assert events
    assert {event.locality_identity for event in events} == {"s1"}
    assert {event.kind for event in events} == {MATERIAL_INGEST_OCCURRED_KIND}


@pytest.mark.parametrize("ledger_name", ("memory_ledger", "durable_ledger"))
def test_locality_existence_comes_from_any_recorded_kind(request, ledger_name):
    ledger = request.getfixturevalue(ledger_name)

    assert ledger.has_locality("s1") is True
    assert ledger.has_locality("never-recorded") is False


# --------------------------------------------------------------------------
# The append boundary is bounded.
# --------------------------------------------------------------------------


def test_the_locality_read_seeks_rather_than_scans(durable_ledger):
    connection = sqlite3.connect(durable_ledger.database_path)
    try:
        plan = connection.execute(
            "EXPLAIN QUERY PLAN "
            "SELECT * FROM events WHERE locality_identity = ? "
            "ORDER BY rowid",
            ("s1",),
        ).fetchall()
    finally:
        connection.close()

    detail = " ".join(str(row[-1]) for row in plan)
    assert "SCAN events" not in detail
    assert "idx_events_locality" in detail


def test_the_index_covers_the_locality_boundary(durable_ledger):
    connection = sqlite3.connect(durable_ledger.database_path)
    try:
        sql = connection.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'index' AND name = ?",
            ("idx_events_locality",),
        ).fetchone()
    finally:
        connection.close()

    assert sql is not None
    assert "locality_identity" in sql[0]


def test_the_kind_stream_seeks_by_locality_and_kind(durable_ledger):
    connection = sqlite3.connect(durable_ledger.database_path)
    try:
        plan = connection.execute(
            "EXPLAIN QUERY PLAN "
            "SELECT * FROM events WHERE locality_identity = ? "
            "AND kind = ? ORDER BY rowid",
            ("s1", MATERIAL_INGEST_OCCURRED_KIND),
        ).fetchall()
    finally:
        connection.close()

    detail = " ".join(str(row[-1]) for row in plan)
    assert "SCAN events" not in detail
    assert "idx_events_locality_kind" in detail
