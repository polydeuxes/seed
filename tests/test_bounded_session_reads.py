"""A read bounded in what it answers must also be bounded in what it reads.

`#2414` measured two places where it was not. `preserved_ingress_occurrences`
loaded a whole workspace and filtered by session in Python, and the SQLite
session read scanned every row because no index covered its selection boundary.
Both returned correct answers, which is why neither was visible until the
workspace held sixteen co-resident bodies.

These tests pin the extent, not only the answer. The identical-results tests
matter as much as the plan test: a bounded read that changes what it returns has
not been made cheaper, it has been broken.
"""

from __future__ import annotations

import sqlite3
from io import StringIO

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.preserved_material_measurement import (
    INGRESS_OCCURRED_KIND,
    preserved_ingress_occurrences,
)
from scripts import seed_local

BODIES = {
    "s1": "a noun is a word\nand a verb is a word\n",
    "s2": "the cat sat on the mat\nthe mat was flat\n",
    "s3": "one two three\nfour five six\n",
}


def _whole_workspace_read(ledger, *, workspace_id, session_id):
    """What `preserved_ingress_occurrences` did before `#2416`."""
    return [
        event
        for event in ledger.list(workspace_id)
        if event.session_id == session_id and event.kind == INGRESS_OCCURRED_KIND
    ]


def _fill(ledger):
    for session_id, material in BODIES.items():
        seed_local.run_persistent_operator_console(
            ledger=ledger,
            workspace_id="w",
            session_id=session_id,
            input_stream=StringIO(material + "exit\n"),
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
# The answer is unchanged.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("session_id", sorted(BODIES))
def test_the_occurrences_are_identical_in_memory(memory_ledger, session_id):
    bounded = preserved_ingress_occurrences(
        memory_ledger, workspace_id="w", session_id=session_id
    )
    whole = _whole_workspace_read(
        memory_ledger, workspace_id="w", session_id=session_id
    )
    assert bounded
    assert [e.id for e in bounded] == [e.id for e in whole]
    assert [e.payload for e in bounded] == [e.payload for e in whole]


@pytest.mark.parametrize("session_id", sorted(BODIES))
def test_the_occurrences_are_identical_durably(durable_ledger, session_id):
    bounded = preserved_ingress_occurrences(
        durable_ledger, workspace_id="w", session_id=session_id
    )
    whole = _whole_workspace_read(
        durable_ledger, workspace_id="w", session_id=session_id
    )
    assert bounded
    assert [e.id for e in bounded] == [e.id for e in whole]
    assert [e.payload for e in bounded] == [e.payload for e in whole]


def test_each_body_still_gets_only_its_own_material(durable_ledger):
    held = {
        session_id: [
            event.payload["decoded_text"]
            for event in preserved_ingress_occurrences(
                durable_ledger, workspace_id="w", session_id=session_id
            )
        ]
        for session_id in BODIES
    }
    assert held == {
        session_id: material.splitlines(keepends=True)
        for session_id, material in BODIES.items()
    }


def test_an_unrecorded_session_reads_empty(durable_ledger):
    assert (
        preserved_ingress_occurrences(
            durable_ledger, workspace_id="w", session_id="never-recorded"
        )
        == []
    )


# --------------------------------------------------------------------------
# The extent is bounded.
# --------------------------------------------------------------------------


def test_the_session_read_seeks_rather_than_scans(durable_ledger):
    connection = sqlite3.connect(durable_ledger.database_path)
    try:
        plan = connection.execute(
            "EXPLAIN QUERY PLAN "
            "SELECT * FROM events WHERE workspace_id = ? AND session_id = ? "
            "ORDER BY rowid",
            ("w", "s1"),
        ).fetchall()
    finally:
        connection.close()

    detail = " ".join(str(row[-1]) for row in plan)
    assert "SCAN events" not in detail
    assert "idx_events_workspace_session" in detail


def test_the_index_covers_the_boundary_sessions_are_selected_by(durable_ledger):
    connection = sqlite3.connect(durable_ledger.database_path)
    try:
        sql = connection.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'index' AND name = ?",
            ("idx_events_workspace_session",),
        ).fetchone()
    finally:
        connection.close()

    assert sql is not None
    assert "workspace_id" in sql[0]
    assert "session_id" in sql[0]


def test_the_index_is_created_on_an_existing_ledger(tmp_path):
    """A ledger written before `#2416` gains the index when next opened."""
    path = str(tmp_path / "prior.db")
    connection = sqlite3.connect(path)
    connection.execute(
        "CREATE TABLE events (id TEXT PRIMARY KEY, kind TEXT NOT NULL, "
        "workspace_id TEXT NOT NULL, actor TEXT NOT NULL, timestamp TEXT "
        "NOT NULL, payload TEXT NOT NULL, session_id TEXT, causation_id TEXT, "
        "correlation_id TEXT)"
    )
    connection.commit()
    connection.close()

    ledger = SQLiteEventLedger(path)
    try:
        connection = sqlite3.connect(path)
        names = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'index'"
            )
        }
        connection.close()
        assert "idx_events_workspace_session" in names
    finally:
        ledger.close()
