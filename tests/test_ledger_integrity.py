"""Mutation refused by default, and corruption made detectable.

Neither is immutability. A `DROP TRIGGER` followed by a rewrite of both the row
and its digest defeats all of this, and these tests say so rather than letting
the arrangement be read as tamper-proof storage.

`06.Standing:16` names append-only records permissively, beside projected
material and context views. Nothing in active law requires append-only, so this
establishes a storage property Seed chose, not one the Book demanded.
"""

from __future__ import annotations

import sqlite3

import pytest

from seed_runtime.bounded_testimony_comparison import (
    BoundedComparisonError,
    compare_preserved_findings,
)
from seed_runtime.events import (
    CORRUPTED,
    UNVERIFIABLE,
    VERIFIED,
    EventLedger,
    LedgerIntegrityError,
    SQLiteEventLedger,
)


@pytest.fixture
def path(tmp_path):
    return str(tmp_path / "seed.db")


@pytest.fixture
def ledger(path):
    led = SQLiteEventLedger(path)
    yield led
    led.close()


def _raw(path):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con


# --------------------------------------------------------------------------
# Refused by default.
# --------------------------------------------------------------------------


def test_an_update_is_refused(ledger, path):
    event = ledger.append("k", "w", {"a": 1})
    con = _raw(path)
    try:
        with pytest.raises(sqlite3.IntegrityError, match="do not change"):
            con.execute("UPDATE events SET payload = ? WHERE id = ?",
                        ('{"a": 999}', event.id))
            con.commit()
    finally:
        con.close()
    assert ledger.get(event.id).payload == {"a": 1}


def test_a_delete_is_refused(ledger, path):
    event = ledger.append("k", "w", {"a": 1})
    con = _raw(path)
    try:
        with pytest.raises(sqlite3.IntegrityError, match="are not removed"):
            con.execute("DELETE FROM events WHERE id = ?", (event.id,))
            con.commit()
    finally:
        con.close()
    assert ledger.get(event.id) is not None


def test_the_refusal_survives_reopening(path):
    led = SQLiteEventLedger(path)
    event = led.append("k", "w", {"a": 1})
    led.close()

    con = _raw(path)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            con.execute("UPDATE events SET kind = 'other' WHERE id = ?", (event.id,))
    finally:
        con.close()


# --------------------------------------------------------------------------
# Detectable when bypassed.
# --------------------------------------------------------------------------


def test_a_recorded_occurrence_verifies(ledger):
    event = ledger.append("k", "w", {"a": 1}, session_id="s")
    assert ledger.integrity_of(event.id) == VERIFIED


def test_a_rewrite_that_drops_the_guard_is_detected(ledger, path):
    """The guard is removable. What it leaves behind is evidence."""
    event = ledger.append("k", "w", {"a": 1})
    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    con.execute("UPDATE events SET payload = ? WHERE id = ?", ('{"a": 999}', event.id))
    con.commit()
    con.close()

    assert SQLiteEventLedger(path).integrity_of(event.id) == CORRUPTED


def test_moving_an_occurrence_between_sessions_is_detected(ledger, path):
    """`session_id` is the boundary keeping bounded exchanges apart."""
    event = ledger.append("k", "w", {"a": 1}, session_id="s1")
    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    con.execute("UPDATE events SET session_id = 's2' WHERE id = ?", (event.id,))
    con.commit()
    con.close()

    assert SQLiteEventLedger(path).integrity_of(event.id) == CORRUPTED


@pytest.mark.parametrize(
    "column,value",
    [("id", "evt_999999"), ("kind", "other"), ("workspace_id", "elsewhere"),
     ("actor", "someone"), ("timestamp", "1999-01-01T00:00:00"),
     ("causation_id", "evt_x"), ("correlation_id", "evt_y")],
)
def test_every_persisted_field_is_covered(ledger, path, column, value):
    event = ledger.append("k", "w", {"a": 1}, session_id="s")
    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    con.execute(f"UPDATE events SET {column} = ? WHERE id = ?", (value, event.id))
    con.commit()
    con.close()

    reopened = SQLiteEventLedger(path)
    # An altered `id` is looked up under the value now stored.
    assert reopened.integrity_of(value if column == "id" else event.id) == CORRUPTED


# --------------------------------------------------------------------------
# What is not claimed.
# --------------------------------------------------------------------------


def test_rewriting_the_row_and_its_digest_together_is_not_detected(ledger, path):
    """Stated as a test so the limit cannot be forgotten.

    Someone able to write arbitrary SQL can drop the guard, rewrite the row,
    and recompute the digest. Detecting that needs an integrity root outside
    the mutable database, which this does not have and does not claim.
    """
    from seed_runtime.events import _content_digest

    event = ledger.append("k", "w", {"a": 1}, session_id="s")
    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    row = dict(con.execute("SELECT * FROM events WHERE id = ?", (event.id,)).fetchone())
    row["payload"] = '{"a": 999}'
    con.execute("UPDATE events SET payload = ?, content_hash = ? WHERE id = ?",
                (row["payload"], _content_digest(row), event.id))
    con.commit()
    con.close()

    assert SQLiteEventLedger(path).integrity_of(event.id) == VERIFIED
    assert SQLiteEventLedger(path).get(event.id).payload == {"a": 999}


def _legacy_store(path, rows=1):
    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE events (id TEXT PRIMARY KEY, kind TEXT NOT NULL, "
        "workspace_id TEXT NOT NULL, actor TEXT NOT NULL, timestamp TEXT NOT NULL, "
        "payload TEXT NOT NULL, session_id TEXT, causation_id TEXT, correlation_id TEXT)"
    )
    for i in range(rows):
        con.execute(
            "INSERT INTO events VALUES (?,'k','w','system',"
            "'2026-01-01T00:00:00','{}','s',NULL,NULL)", (f"evt_{i:06d}",))
    con.commit()
    con.close()


@pytest.mark.parametrize("rows", [0, 1, 5])
def test_a_pre_digest_schema_is_refused_whether_or_not_it_holds_rows(path, rows):
    """Seed does not preserve a durable history nobody needs.

    An earlier form classified undigested rows as UNVERIFIABLE and consumed
    them, leaving a supported path on which a durable occurrence carried no
    integrity. A later form refused populated pre-digest stores but migrated
    empty ones, which meant a new database was created by running a
    compatibility migration over the very shape being rejected.
    """
    _legacy_store(path, rows=rows)
    with pytest.raises(LedgerIntegrityError, match="without content_hash"):
        SQLiteEventLedger(path)


def test_a_nullable_schema_holding_an_undigested_row_is_refused(path):
    """Refused for its schema, before any row is counted."""
    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE events (id TEXT PRIMARY KEY, kind TEXT NOT NULL, "
        "workspace_id TEXT NOT NULL, actor TEXT NOT NULL, timestamp TEXT NOT NULL, "
        "payload TEXT NOT NULL, session_id TEXT, causation_id TEXT, "
        "correlation_id TEXT, content_hash TEXT)"
    )
    con.execute(
        "INSERT INTO events VALUES ('evt_000001','k','w','system',"
        "'2026-01-01T00:00:00','{}','s',NULL,NULL,NULL)"
    )
    con.commit()
    con.close()

    with pytest.raises(LedgerIntegrityError, match="declares content_hash nullable"):
        SQLiteEventLedger(path)


def test_a_current_store_cannot_hold_an_undigested_occurrence(path):
    """The schema refuses it before any check has to."""
    led = SQLiteEventLedger(path)
    try:
        event = led.append("k", "w", {"a": 1})
        con = _raw(path)
        con.execute("DROP TRIGGER events_refuse_update")
        with pytest.raises(sqlite3.IntegrityError, match="NOT NULL"):
            con.execute("UPDATE events SET content_hash = NULL WHERE id = ?",
                        (event.id,))
        con.close()
    finally:
        led.close()


def test_a_new_store_is_born_with_the_integrity_column(path):
    """No ALTER path exists, so opening at all means the schema is current."""
    led = SQLiteEventLedger(path)
    try:
        info = {row["name"]: row["notnull"]
                for row in led._connection.execute("PRAGMA table_info(events)")}
        assert info.get("content_hash") == 1
        assert led.integrity_of(led.append("k", "w", {"a": 1}).id) == VERIFIED
    finally:
        led.close()


def test_no_durable_occurrence_is_ever_unverifiable(ledger):
    """The refusal at open is what makes this true."""
    ids = [ledger.append("k", "w", {"a": i}).id for i in range(5)]
    assert {ledger.integrity_of(i) for i in ids} == {VERIFIED}


def test_an_in_memory_ledger_reports_unverifiable():
    """Objects, not stored bytes — the one storage shape that cannot verify."""
    led = EventLedger()
    assert led.integrity_of(led.append("k", "w", {"a": 1}).id) == UNVERIFIABLE


def test_an_absent_occurrence_is_unverifiable(ledger):
    assert ledger.integrity_of("evt_never_recorded") == UNVERIFIABLE


# --------------------------------------------------------------------------
# The consuming act is where verification happens.
# --------------------------------------------------------------------------


def test_a_comparison_refuses_a_corrupted_input(path, monkeypatch):
    from io import StringIO
    from seed_runtime.adjacent_pair_measurement import measure_after
    from seed_runtime.preserved_material_measurement import (
        preserved_ingress_occurrences, record_measurement_finding)
    from scripts import seed_local

    led = SQLiteEventLedger(path)
    for session_id in ("s1", "s2"):
        seed_local.run_persistent_operator_console(
            ledger=led, workspace_id="w", session_id=session_id,
            input_stream=StringIO("a noun is a word\nexit\n"), output_stream=StringIO())
    ids = []
    for session_id in ("s1", "s2"):
        occ = preserved_ingress_occurrences(led, workspace_id="w", session_id=session_id)
        ids.append(record_measurement_finding(
            led, workspace_id="w", session_id=session_id,
            finding=measure_after(occ, "a", counting_scope="s")).id)
    led.close()

    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    con.execute("UPDATE events SET payload = ? WHERE id = ?", ('{"tampered": true}', ids[0]))
    con.commit()
    con.close()

    led = SQLiteEventLedger(path)
    try:
        with pytest.raises(BoundedComparisonError, match="does not match its recorded digest"):
            compare_preserved_findings(led, ids)
    finally:
        led.close()


def test_a_comparison_records_each_input_s_integrity(path):
    from io import StringIO
    from seed_runtime.adjacent_pair_measurement import measure_after
    from seed_runtime.preserved_material_measurement import (
        preserved_ingress_occurrences, record_measurement_finding)
    from scripts import seed_local

    led = SQLiteEventLedger(path)
    try:
        for session_id in ("s1", "s2"):
            seed_local.run_persistent_operator_console(
                ledger=led, workspace_id="w", session_id=session_id,
                input_stream=StringIO("a noun is a word\nexit\n"),
                output_stream=StringIO())
        ids = []
        for session_id in ("s1", "s2"):
            occ = preserved_ingress_occurrences(led, workspace_id="w", session_id=session_id)
            ids.append(record_measurement_finding(
                led, workspace_id="w", session_id=session_id,
                finding=measure_after(occ, "a", counting_scope="s")).id)
        finding = compare_preserved_findings(led, ids)
        assert [i.integrity for i in finding.inputs] == [VERIFIED, VERIFIED]
    finally:
        led.close()


def test_an_unverifiable_input_is_recorded_rather_than_refused():
    """In-memory findings are lawfully unverifiable, and comparison proceeds."""
    from io import StringIO
    from seed_runtime.adjacent_pair_measurement import measure_after
    from seed_runtime.preserved_material_measurement import (
        preserved_ingress_occurrences, record_measurement_finding)
    from scripts import seed_local

    led = EventLedger()
    ids = []
    for session_id in ("s1", "s2"):
        seed_local.run_persistent_operator_console(
            ledger=led, workspace_id="w", session_id=session_id,
            input_stream=StringIO("a noun is a word\nexit\n"), output_stream=StringIO())
        occ = preserved_ingress_occurrences(led, workspace_id="w", session_id=session_id)
        ids.append(record_measurement_finding(
            led, workspace_id="w", session_id=session_id,
            finding=measure_after(occ, "a", counting_scope="s")).id)

    finding = compare_preserved_findings(led, ids)
    assert [i.integrity for i in finding.inputs] == [UNVERIFIABLE, UNVERIFIABLE]


def test_a_nullable_digest_schema_is_refused_even_when_fully_digested(path):
    """The column being present is not the invariant.

    `#2426` claimed that opening implies the store was born current, but only
    checked that the column existed and that no row was currently NULL. A store
    created by the withdrawn ALTER path is nullable, and one populated entirely
    with valid digests would have passed while still admitting an undigested
    occurrence later. Prose claiming a property runtime does not enforce is the
    same defect `#2421` removed from Compare's arity.
    """
    from seed_runtime.events import _content_digest

    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE events (id TEXT PRIMARY KEY, kind TEXT NOT NULL, "
        "workspace_id TEXT NOT NULL, actor TEXT NOT NULL, timestamp TEXT NOT NULL, "
        "payload TEXT NOT NULL, session_id TEXT, causation_id TEXT, "
        "correlation_id TEXT, content_hash TEXT)"
    )
    row = {"id": "evt_000001", "kind": "k", "workspace_id": "w", "actor": "system",
           "timestamp": "2026-01-01T00:00:00", "payload": "{}", "session_id": "s",
           "causation_id": None, "correlation_id": None}
    con.execute(
        "INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?)",
        tuple(row.values()) + (_content_digest(row),),
    )
    con.commit()
    con.close()

    # every row digested, and every digest correct
    con = _raw(path)
    assert con.execute(
        "SELECT COUNT(*) FROM events WHERE content_hash IS NULL"
    ).fetchone()[0] == 0
    con.close()

    with pytest.raises(LedgerIntegrityError, match="declares content_hash nullable"):
        SQLiteEventLedger(path)
