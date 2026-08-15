"""Mutation refused by default, and corruption made detectable.

Neither is immutability. A `DROP TRIGGER` followed by a rewrite of both the row
and its material identity defeats all of this, and these tests say so rather than letting
the arrangement be read as tamper-proof storage.

`06.Standing:16` names append-only records permissively, beside projected
material representations. Nothing in active law requires append-only, so this
establishes a storage property Seed chose, not one the Book demanded.
"""

from __future__ import annotations

import json
import random
import sqlite3

import pytest

from tests.binary_input import binary_input

from seed_runtime.event import Event
from seed_runtime.bounded_assertion_comparison import (
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
    event = ledger.append("k", {"a": 1})
    con = _raw(path)
    try:
        with pytest.raises(sqlite3.IntegrityError, match="do not revision"):
            con.execute("UPDATE events SET material = ? WHERE identity = ?",
                        ('{"a": 999}', event.identity))
            con.commit()
    finally:
        con.close()
    assert ledger.get(event.identity).material == {"a": 1}


def test_a_delete_is_refused(ledger, path):
    event = ledger.append("k", {"a": 1})
    con = _raw(path)
    try:
        with pytest.raises(sqlite3.IntegrityError, match="are not removed"):
            con.execute("DELETE FROM events WHERE identity = ?", (event.identity,))
            con.commit()
    finally:
        con.close()
    assert ledger.get(event.identity) is not None


def test_the_refusal_survives_reopening(path):
    led = SQLiteEventLedger(path)
    event = led.append("k", {"a": 1})
    led.close()

    con = _raw(path)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            con.execute("UPDATE events SET kind = 'other' WHERE identity = ?", (event.identity,))
    finally:
        con.close()


# --------------------------------------------------------------------------
# Detectable when bypassed.
# --------------------------------------------------------------------------


def test_a_recorded_occurrence_verifies(ledger):
    event = ledger.append("k", {"a": 1}, locality_identity="s")
    assert ledger.integrity_of(event.identity) == VERIFIED


def test_a_rewrite_that_drops_the_guard_is_detected(ledger, path):
    """The guard is removable. What it leaves behind is evidence."""
    event = ledger.append("k", {"a": 1})
    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    con.execute("UPDATE events SET material = ? WHERE identity = ?", ('{"a": 999}', event.identity))
    con.commit()
    con.close()

    assert SQLiteEventLedger(path).integrity_of(event.identity) == CORRUPTED


def test_moving_an_occurrence_between_sessions_is_detected(ledger, path):
    """`locality_identity` is the boundary keeping bounded localities apart."""
    event = ledger.append("k", {"a": 1}, locality_identity="s1")
    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    con.execute("UPDATE events SET locality_identity = 's2' WHERE identity = ?", (event.identity,))
    con.commit()
    con.close()

    assert SQLiteEventLedger(path).integrity_of(event.identity) == CORRUPTED


@pytest.mark.parametrize(
    "column,value",
    [("identity", "evt_999999"), ("kind", "other"),
     ("timestamp", "1999-01-01T00:00:00")],
)
def test_every_persisted_field_is_covered(ledger, path, column, value):
    event = ledger.append("k", {"a": 1}, locality_identity="s")
    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    con.execute(f"UPDATE events SET {column} = ? WHERE identity = ?", (value, event.identity))
    con.commit()
    con.close()

    reopened = SQLiteEventLedger(path)
    # An altered `identity` is looked up under the value now stored.
    assert reopened.integrity_of(value if column == "identity" else event.identity) == CORRUPTED


# --------------------------------------------------------------------------
# What is not asserted.
# --------------------------------------------------------------------------


def test_rewriting_the_row_and_its_material_identity_together_is_not_detected(ledger, path):
    """Stated as a test so the limit cannot be forgotten.

    Someone able to write arbitrary SQL can drop the guard, rewrite the row,
    and recompute the material identity. Detecting that needs an integrity root outside
    the mutable database, which this does not have and does not Assertion.
    """
    from seed_runtime.events import _occurrence_material_identity

    event = ledger.append("k", {"a": 1}, locality_identity="s")
    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    row = dict(con.execute("SELECT * FROM events WHERE identity = ?", (event.identity,)).fetchone())
    row["material"] = '{"a": 999}'
    con.execute("UPDATE events SET material = ?, occurrence_material_identity = ? WHERE identity = ?",
                (row["material"], _occurrence_material_identity(row), event.identity))
    con.commit()
    con.close()

    assert SQLiteEventLedger(path).integrity_of(event.identity) == VERIFIED
    assert SQLiteEventLedger(path).get(event.identity).material == {"a": 999}


def test_verified_durable_rehydration_still_rejects_nested_secret_fields(path):
    """Row integrity and secret-field admission remain separate boundaries."""
    from seed_runtime.events import _occurrence_material_identity

    ledger = SQLiteEventLedger(path)
    event = ledger.append("k", {"a": 1}, locality_identity="s")
    ledger.close()

    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    row = dict(con.execute("SELECT * FROM events WHERE identity = ?", (event.identity,)).fetchone())
    row["material"] = '{"outer":[[{"token":"not-accepted"}]]}'
    con.execute(
        "UPDATE events SET material = ?, occurrence_material_identity = ? WHERE identity = ?",
        (row["material"], _occurrence_material_identity(row), event.identity),
    )
    con.commit()
    con.close()

    reopened = SQLiteEventLedger(path)
    try:
        assert reopened.integrity_of(event.identity) == VERIFIED
        with pytest.raises(ValueError, match="secret field"):
            reopened.get(event.identity)
    finally:
        reopened.close()


def test_screened_durable_rehydration_still_runs_event_validation(path):
    from seed_runtime.events import _occurrence_material_identity

    ledger = SQLiteEventLedger(path)
    event = ledger.append("k", {"a": 1}, locality_identity="s")
    ledger.close()

    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    row = dict(con.execute("SELECT * FROM events WHERE identity = ?", (event.identity,)).fetchone())
    row["material"] = "[]"
    con.execute(
        "UPDATE events SET material = ?, occurrence_material_identity = ? WHERE identity = ?",
        (row["material"], _occurrence_material_identity(row), event.identity),
    )
    con.commit()
    con.close()

    reopened = SQLiteEventLedger(path)
    try:
        assert reopened.integrity_of(event.identity) == VERIFIED
        with pytest.raises(ValueError, match="material"):
            reopened.get(event.identity)
    finally:
        reopened.close()


def _incomplete_store(path, rows=1):
    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE events (identity TEXT PRIMARY KEY, kind TEXT NOT NULL, "
        "timestamp TEXT NOT NULL, material TEXT NOT NULL, locality_identity TEXT)"
    )
    for i in range(rows):
        con.execute(
            "INSERT INTO events VALUES (?,'k','2026-01-01T00:00:00','{}','s')",
            (f"evt_{i:06d}",),
        )
    con.commit()
    con.close()


@pytest.mark.parametrize("rows", [0, 1, 5])
def test_a_schema_without_occurrence_material_identity_is_refused(path, rows):
    """Seed does not preserve a durable history nobody needs.

    An earlier representation classified rows without this identity as UNVERIFIABLE and input
    them, leaving a supported path on which a durable occurrence carried no
    integrity. A later representation refused populated pre-material identity stores but migrated
    empty ones, which meant a new database was created by running a
    migration over the very shape being rejected.
    """
    _incomplete_store(path, rows=rows)
    with pytest.raises(LedgerIntegrityError, match="current occurrence fields"):
        SQLiteEventLedger(path)


def test_a_nullable_occurrence_material_identity_is_refused(path):
    """Refused for its schema, before any row is counted."""
    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE events (identity TEXT PRIMARY KEY, kind TEXT NOT NULL, "
        "timestamp TEXT NOT NULL, material TEXT NOT NULL, locality_identity TEXT, "
        "occurrence_material_identity TEXT)"
    )
    con.execute(
        "INSERT INTO events VALUES ('evt_000001','k','2026-01-01T00:00:00',"
        "'{}','s',NULL)"
    )
    con.commit()
    con.close()

    with pytest.raises(LedgerIntegrityError, match="declares occurrence_material_identity nullable"):
        SQLiteEventLedger(path)


def test_a_current_store_requires_occurrence_material_identity(path):
    """The schema refuses it before any check has to."""
    led = SQLiteEventLedger(path)
    try:
        event = led.append("k", {"a": 1})
        con = _raw(path)
        con.execute("DROP TRIGGER events_refuse_update")
        with pytest.raises(sqlite3.IntegrityError, match="NOT NULL"):
            con.execute("UPDATE events SET occurrence_material_identity = NULL WHERE identity = ?",
                        (event.identity,))
        con.close()
    finally:
        led.close()


def test_a_new_store_is_born_with_the_integrity_column(path):
    """No ALTER path exists, so opening at all means the schema is current."""
    led = SQLiteEventLedger(path)
    try:
        info = {row["name"]: row["notnull"]
                for row in led._connection.execute("PRAGMA table_info(events)")}
        assert info.get("occurrence_material_identity") == 1
        assert led.integrity_of(led.append("k", {"a": 1}).identity) == VERIFIED
    finally:
        led.close()


def test_no_durable_occurrence_is_ever_unverifiable(ledger):
    """The refusal at open is what makes this true."""
    identities = [ledger.append("k", {"a": i}).identity for i in range(5)]
    assert {ledger.integrity_of(i) for i in identities} == {VERIFIED}


def test_an_in_memory_ledger_reports_unverifiable():
    """Objects, not stored bytes — the one storage shape that cannot verify."""
    led = EventLedger()
    assert led.integrity_of(led.append("k", {"a": 1}).identity) == UNVERIFIABLE


def test_an_absent_occurrence_is_unverifiable(ledger):
    assert ledger.integrity_of("evt_never_recorded") == UNVERIFIABLE


# --------------------------------------------------------------------------
# The Act with participating inputs are where verification happens.
# --------------------------------------------------------------------------


def test_a_comparison_refuses_a_corrupted_input(path, monkeypatch):
    from io import StringIO
    from seed_runtime.adjacency_pair_measurement import measure_after
    from seed_runtime.preserved_material_measurement import (
        ingest_occurrences, record_measurement_finding)
    from tests.material_fixture_console import run_material_fixture_console

    led = SQLiteEventLedger(path)
    for locality_identity in ("s1", "s2"):
        run_material_fixture_console(
            ledger=led, locality_identity=locality_identity,
            input_stream=binary_input("a noun is a word\n"), output_stream=StringIO())
    identities = []
    for locality_identity in ("s1", "s2"):
        occ = ingest_occurrences(led, locality_identity=locality_identity)
        identities.append(record_measurement_finding(
            led, locality_identity=locality_identity,
            finding=measure_after(occ, "a", counting_scope="s")).identity)
    led.close()

    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    con.execute("UPDATE events SET material = ? WHERE identity = ?", ('{"tampered": true}', identities[0]))
    con.commit()
    con.close()

    led = SQLiteEventLedger(path)
    try:
        with pytest.raises(BoundedComparisonError, match="does not match its recorded material identity"):
            compare_preserved_findings(led, identities)
    finally:
        led.close()


def test_a_comparison_checks_each_input_without_copying_storage_integrity(path):
    from io import StringIO
    from seed_runtime.adjacency_pair_measurement import measure_after
    from seed_runtime.preserved_material_measurement import (
        ingest_occurrences, record_measurement_finding)
    from tests.material_fixture_console import run_material_fixture_console

    led = SQLiteEventLedger(path)
    try:
        for locality_identity in ("s1", "s2"):
            run_material_fixture_console(
                ledger=led, locality_identity=locality_identity,
                input_stream=binary_input("a noun is a word\n"),
                output_stream=StringIO())
        identities = []
        for locality_identity in ("s1", "s2"):
            occ = ingest_occurrences(led, locality_identity=locality_identity)
            identities.append(record_measurement_finding(
                led, locality_identity=locality_identity,
                finding=measure_after(occ, "a", counting_scope="s")).identity)
        finding = compare_preserved_findings(led, identities)
        assert [led.integrity_of(identity) for identity in identities] == [
            VERIFIED,
            VERIFIED,
        ]
        assert [item.event_identity for item in finding.inputs] == identities
        assert all("integrity" not in item.to_json_dict() for item in finding.inputs)
    finally:
        led.close()


def test_unverifiable_storage_does_not_become_comparison_result_material():
    from io import StringIO
    from seed_runtime.adjacency_pair_measurement import measure_after
    from seed_runtime.preserved_material_measurement import (
        ingest_occurrences, record_measurement_finding)
    from tests.material_fixture_console import run_material_fixture_console

    led = EventLedger()
    identities = []
    for locality_identity in ("s1", "s2"):
        run_material_fixture_console(
            ledger=led, locality_identity=locality_identity,
            input_stream=binary_input("a noun is a word\n"), output_stream=StringIO())
        occ = ingest_occurrences(led, locality_identity=locality_identity)
        identities.append(record_measurement_finding(
            led, locality_identity=locality_identity,
            finding=measure_after(occ, "a", counting_scope="s")).identity)

    finding = compare_preserved_findings(led, identities)
    assert [led.integrity_of(identity) for identity in identities] == [
        UNVERIFIABLE,
        UNVERIFIABLE,
    ]
    assert [item.event_identity for item in finding.inputs] == identities
    assert all("integrity" not in item.to_json_dict() for item in finding.inputs)


def test_a_nullable_occurrence_material_identity_is_refused_when_populated(path):
    """The column being present is not the invariant.

    `#2426` asserted that opening implies the store was born current, but only
    checked that the column existed and that no row was currently NULL. A store
    created by the withdrawn ALTER path is nullable, and one populated entirely
    with valid material identities would have passed while still admitting an occurrence without one
    occurrence later. Prose asserting a property runtime does not enforce is the
    same defect `#2421` removed from Compare's arity.
    """
    from seed_runtime.events import _occurrence_material_identity

    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE events (identity TEXT PRIMARY KEY, kind TEXT NOT NULL, "
        "timestamp TEXT NOT NULL, material TEXT NOT NULL, locality_identity TEXT, "
        "occurrence_material_identity TEXT)"
    )
    row = {"identity": "evt_000001", "kind": "k",
           "timestamp": "2026-01-01T00:00:00", "material": "{}", "locality_identity": "s",
           }
    con.execute(
        "INSERT INTO events VALUES (?,?,?,?,?,?)",
        tuple(row.values()) + (_occurrence_material_identity(row),),
    )
    con.commit()
    con.close()

    # every row identified, and every material identity correct
    con = _raw(path)
    assert con.execute(
        "SELECT COUNT(*) FROM events WHERE occurrence_material_identity IS NULL"
    ).fetchone()[0] == 0
    con.close()

    with pytest.raises(LedgerIntegrityError, match="declares occurrence_material_identity nullable"):
        SQLiteEventLedger(path)


# --------------------------------------------------------------------------
# Identity counters are kept, not validated.
# --------------------------------------------------------------------------


def test_reservations_are_read_from_the_table_not_from_history(path):
    """`#2414`'s whole-history read, replaced by a durable counter.

    The open cost was linear in stored events — 36.9s at 100,000 — because
    every material was deserialized and walked to read a few integers.
    """
    led = SQLiteEventLedger(path)
    try:
        led.append("k", {"reference": "operator_material_000042"}, locality_identity="locality_000007")
        led.append("k", {"reference": "system_material_000005"})
    finally:
        led.close()

    con = _raw(path)
    try:
        kept = dict(con.execute("SELECT prefix, max_number FROM identity_reservations"))
    finally:
        con.close()
    assert kept["operator_material"] == 42
    assert kept["locality"] == 7
    assert kept["system_material"] == 5


def test_a_reopened_store_does_not_reissue_identifiers(path):
    """The property the reservation exists for, across ledger lifetimes."""
    from seed_runtime.identities import _next_values, new_identity

    led = SQLiteEventLedger(path)
    led.append("k", {"reference": "operator_material_000042"})
    led.close()

    _next_values.clear()          # a fresh process counts from 1
    led = SQLiteEventLedger(path)
    try:
        assert new_identity("operator_material") == "operator_material_000043"
    finally:
        led.close()


def test_a_reservation_only_ever_rises(path):
    led = SQLiteEventLedger(path)
    try:
        led.append("k", {"reference": "operator_material_000042"})
        led.append("k", {"reference": "operator_material_000007"})
    finally:
        led.close()
    con = _raw(path)
    try:
        kept = dict(con.execute("SELECT prefix, max_number FROM identity_reservations"))
    finally:
        con.close()
    assert kept["operator_material"] == 42


def test_the_counter_table_is_not_an_occurrence(path):
    """It records no Assertion, so occurrence mutation refusal does not cover it."""
    led = SQLiteEventLedger(path)
    try:
        event = led.append("k", {"reference": "operator_material_000042"})
    finally:
        led.close()
    con = _raw(path)
    try:
        con.execute("UPDATE identity_reservations SET max_number = 99 WHERE prefix = 'operator_material'")
        con.commit()
    finally:
        con.close()
    led = SQLiteEventLedger(path)
    try:
        assert led.integrity_of(event.identity) == VERIFIED
    finally:
        led.close()


def test_a_batch_commits_its_reservations_with_its_occurrences(path):
    """`#2428`'s invariant, which `append_many` did not satisfy.

    `append` inserts an occurrence and persists its reservations in one
    transaction. `append_many` used two, so a failure between them left durable
    occurrences carrying identities whose counters were stale on reopen —
    exactly the collision `#2428` exists to prevent.
    """
    from seed_runtime.event import Event

    led = SQLiteEventLedger(path)
    commits = []
    led._connection.set_trace_callback(commits.append)
    try:
        led.append_many([
            Event(identity=f"evt_10000{i}", kind="k", material={"reference": f"operator_material_0000{40 + i}"}, locality_identity="locality_000009")
            for i in range(3)
        ])
    finally:
        led._connection.set_trace_callback(None)
        led.close()

    assert sum(1 for q in commits if q.strip().upper() == "COMMIT") == 1

    con = _raw(path)
    try:
        kept = dict(con.execute("SELECT prefix, max_number FROM identity_reservations"))
        stored = con.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    finally:
        con.close()
    assert stored == 3
    assert kept["operator_material"] == 42
    assert kept["locality"] == 9


def test_a_batch_leaves_no_occurrence_without_its_reservation(path):
    """Reopening a batched store does not reissue a batched identity."""
    from seed_runtime.identities import _next_values, new_identity
    from seed_runtime.event import Event

    led = SQLiteEventLedger(path)
    led.append_many([
        Event(identity="evt_100001", kind="k", material={"reference": "operator_material_000077"}, locality_identity="s")
    ])
    led.close()

    _next_values.clear()
    led = SQLiteEventLedger(path)
    try:
        assert new_identity("operator_material") == "operator_material_000078"
    finally:
        led.close()


def test_reservable_suffix_observation_matches_a_per_prefix_scan():
    """One split must find exactly what testing every prefix in turn found.

    A reservable identity is a prefix, an underscore, and digits, so the
    digits begin just after the value's last underscore. This holds the split
    to that equivalence over generated materials rather than over examples,
    because several movement prefixes overlap and a number of
    zero is deliberately not reserved.
    """

    from seed_runtime.events import _numeric_number, _walk_values

    prefixes = tuple(SQLiteEventLedger._RESERVABLE_PREFIXES)

    def per_prefix_scan(event):
        found = {}
        values = list(_walk_values(event.material))
        if event.locality_identity is not None:
            values.append(event.locality_identity)
        for value in values:
            if not isinstance(value, str):
                continue
            for prefix in prefixes:
                number = _numeric_number(value, prefix)
                if number is not None and number > found.get(prefix, 0):
                    found[prefix] = number
        return found

    tokens = list(prefixes) + ["evt", "x", "", "old_fact", "need"]
    rng = random.Random(11)

    def one(values):
        return values[rng.randrange(len(values))]

    def identity():
        token = one(tokens)
        return one([
            f"{token}_{rng.randint(0, 999)}",
            f"{token}_{one(['', 'x', '0a', '007'])}",
            token,
            f"_{rng.randint(0, 99)}",
            f"{token}__{rng.randint(0, 99)}",
        ])

    def value(depth=0):
        roll = rng.random()
        if depth < 3 and roll < 0.3:
            return {identity(): value(depth + 1) for _ in range(rng.randint(0, 4))}
        if depth < 3 and roll < 0.45:
            return [value(depth + 1) for _ in range(rng.randint(0, 4))]
        if roll < 0.75:
            return identity()
        return one([None, True, 7, 3.5])

    ledger = SQLiteEventLedger.__new__(SQLiteEventLedger)
    for index in range(1500):
        material = value()
        if not isinstance(material, dict):
            material = {"k": material}
        event = Event(
            identity=f"evt_{index}",
            kind="k",
            material=material,
            locality_identity=one([None, identity(), f"locality_{rng.randint(0, 9999)}"]),
        )
        assert ledger._observed_numbers(event) == per_prefix_scan(event)


def test_a_reserved_suffix_of_zero_is_not_reserved():
    """`number > found.get(prefix, 0)` deliberately declines zero, and the
    split must decline it too rather than reserve prefix zero."""

    ledger = SQLiteEventLedger.__new__(SQLiteEventLedger)
    event = Event(identity="evt_1", kind="k", material={"a": "operator_material_0"})
    assert ledger._observed_numbers(event) == {}
    event = Event(identity="evt_2", kind="k", material={"a": "operator_material_1"})
    assert ledger._observed_numbers(event) == {"operator_material": 1}


def test_an_overlapping_prefix_reserves_the_longer_match():
    ledger = SQLiteEventLedger.__new__(SQLiteEventLedger)
    event = Event(
        identity="evt_1", kind="k", material={"a": "assertion_locality_movement_act_7", "b": "assertion_locality_movement_4"},
    )
    assert ledger._observed_numbers(event) == {
        "assertion_locality_movement_act": 7,
        "assertion_locality_movement": 4,
    }


def test_a_cache_hit_still_refuses_a_contradictory_support_count():
    """A forged count is refused before and after an exact support read."""

    from seed_runtime.input_support import (
        InputSupport,
        InputSupportError,
        InputSupportValidator,
        declare_input_support,
    )

    ledger = EventLedger()
    ledger.append_many([
        Event(identity=f"evt_{index}", kind="ingest", locality_identity="s")
        for index in range(4)
    ])
    boundary = ledger.append_boundary()
    identities = tuple(ledger.iter_locality_kind_identities("s", "ingest", through=boundary))
    honest = declare_input_support(
        locality_identity="s", occurrence_kind="ingest",
        boundary=boundary, occurrence_references=identities,
    )
    forged = InputSupport(
        locality_identity=honest.locality_identity,
        occurrence_kind=honest.occurrence_kind,
        boundary_identity=honest.boundary_identity,
        support_count=honest.support_count - 1,
    )

    # Refused on a cold validation.
    with pytest.raises(InputSupportError, match="declared count"):
        InputSupportValidator(ledger).validate(forged)

    # And refused after the same inputs has been cached, which is the path
    # that previously returned it.
    validation = InputSupportValidator(ledger)
    assert validation.validate(honest) == identities
    assert validation.reads == 1
    with pytest.raises(InputSupportError, match="declared count"):
        validation.validate(forged)
    assert validation.reuses == 0

    # An honest second reference still reuses the first exact bytes.
    assert validation.validate(honest) == identities
    assert (validation.reads, validation.reuses) == (1, 1)


def test_every_input_support_refusal_can_be_reached():
    """Each input-support refusal has a witness."""

    from seed_runtime.input_support import (
        InputSupport,
        InputSupportError,
    )

    def support(**differences):
        fields = dict(
            locality_identity="s", occurrence_kind="k",
            boundary_identity="b",
            support_count=0,
        )
        fields.update(differences)
        return InputSupport(**fields)

    support()

    for name in ("locality_identity", "occurrence_kind", "boundary_identity"):
        with pytest.raises(InputSupportError, match=f"requires {name}"):
            support(**{name: ""})
        with pytest.raises(InputSupportError, match=f"requires {name}"):
            support(**{name: None})

    with pytest.raises(InputSupportError, match="negative count"):
        support(support_count=-1)

    # A count coordinate must establish that it can be a count. Each of these
    # previously either leaked a raw TypeError from the comparison or was
    # accepted outright.
    for value in ("4", None, True, False, 4.0, [], {}, ()):
        with pytest.raises(InputSupportError, match="integer support count"):
            support(support_count=value)

    # `True` mattered most: it is an int and equals 1, so a support carrying it
    # would have agreed with a one-occurrence inputs.
    assert True == 1

    with pytest.raises(InputSupportError, match="not present"):
        InputSupport.from_json_dict(None)
    with pytest.raises(InputSupportError, match="not present"):
        InputSupport.from_json_dict("not input support")

    complete = support().to_json_dict()
    assert InputSupport.from_json_dict(complete) == support()
    for key in ("scope", "boundary", "support_count"):
        partial = {k: v for k, v in complete.items() if k != key}
        with pytest.raises(InputSupportError, match="incomplete"):
            InputSupport.from_json_dict(partial)


def test_occurrence_material_identity_does_not_move_when_material_is_compressed(tmp_path):
    """The material identity commits to what an occurrence carries, not how it was stored.

    `#2494` put compression below the integrity boundary. If the material identity were
    taken over the stored bytes instead of the canonical string, an occurrence
    would verify differently depending on whether it happened to compress, and
    a store written before compression would verify as CORRUPTED.
    """

    import zlib
    from seed_runtime.events import _occurrence_material_identity, _stored_material, _serialized_material

    material = {"dimensions": {"content": "x" * 4000}, "n": list(range(200))}
    small = {"a": 1}

    for value in (material, small):
        serialized = json.dumps(value)
        row = {
            "identity": "evt_1", "kind": "k",
            "timestamp": "2026-01-01T00:00:00+00:00", "material": serialized,
            "locality_identity": None,
        }
        material_identity = _occurrence_material_identity(row)
        stored = _stored_material(serialized)
        # Whatever the store holds, it reads the canonical string exactly,
        # and identifying that reproduces the same commitment.
        assert _serialized_material(stored) == serialized
        assert (
            _occurrence_material_identity(
                dict(row, material=_serialized_material(stored))
            )
            == material_identity
        )

    # Large materials compress and are stored as bytes; tiny ones do not and are
    # stored as text, because compressing them would cost bytes for nothing.
    assert isinstance(_stored_material(json.dumps(material)), bytes)
    assert isinstance(_stored_material(json.dumps(small)), str)


def test_compressed_and_uncompressed_stores_verify_alike(tmp_path):
    path = str(tmp_path / "ledger.db")
    ledger = SQLiteEventLedger(path)
    material = {"dimensions": {"content": "y" * 5000}, "n": list(range(300))}
    try:
        compressed = ledger.append("k", material)
        plain = ledger.append("k", {"a": 1})
        assert ledger.integrity_of(compressed.identity) == VERIFIED
        assert ledger.integrity_of(plain.identity) == VERIFIED
        assert ledger.get(compressed.identity).material == material
        assert ledger.get(plain.identity).material == {"a": 1}
    finally:
        ledger.close()

    # Stored represents differ; standing does not.
    connection = sqlite3.connect(path)
    stored = {
        row[0]: row[1]
        for row in connection.execute("SELECT identity, material FROM events")
    }
    connection.close()
    assert isinstance(stored[compressed.identity], bytes)
    assert isinstance(stored[plain.identity], str)


def test_damaged_compressed_storage_is_corruption_not_a_compressor_error(tmp_path):

    import zlib
    from seed_runtime.events import InvalidStoredMaterial

    material = {"dimensions": {"content": "q" * 5000}}
    intact = zlib.compress(json.dumps(material).encode("utf-8"), 1)

    damage = {
        "truncated": intact[: len(intact) // 2],
        "bit flipped": intact[:20] + bytes([intact[20] ^ 0xFF]) + intact[21:],
        "empty": b"",
        # Decompresses, and what comes out is not text.
        "not utf-8": zlib.compress(b"\xff\xfe\x00", 1),
    }

    for label, stored in damage.items():
        path = str(tmp_path / f"{label.replace(' ', '_')}.db")
        ledger = SQLiteEventLedger(path)
        try:
            event = ledger.append("k", material)
        finally:
            ledger.close()

        connection = sqlite3.connect(path)
        connection.execute("DROP TRIGGER events_refuse_update")
        connection.execute(
            "UPDATE events SET material = ? WHERE identity = ?", (stored, event.identity)
        )
        connection.commit()
        connection.close()

        ledger = SQLiteEventLedger(path)
        try:
            # Reported, never raised through the caller.
            assert ledger.integrity_of(event.identity) == CORRUPTED, label
            # And a read refuses as a ledger integrity failure rather than
            # exposing the compressor.
            with pytest.raises(InvalidStoredMaterial):
                ledger.get(event.identity)
        finally:
            ledger.close()


def test_a_compressed_material_altered_to_other_valid_content_is_corrupted(tmp_path):
    """The material identity still settles it when the storage reads cleanly."""

    import zlib

    path = str(tmp_path / "swapped.db")
    ledger = SQLiteEventLedger(path)
    try:
        event = ledger.append("k", {"dimensions": {"content": "q" * 5000}})
    finally:
        ledger.close()

    connection = sqlite3.connect(path)
    connection.execute("DROP TRIGGER events_refuse_update")
    connection.execute(
        "UPDATE events SET material = ? WHERE identity = ?",
        (zlib.compress(json.dumps({"dimensions": {"content": "other"}}).encode(), 1), event.identity),
    )
    connection.commit()
    connection.close()

    ledger = SQLiteEventLedger(path)
    try:
        assert ledger.integrity_of(event.identity) == CORRUPTED
    finally:
        ledger.close()


def test_a_stored_material_that_is_not_an_occurrence_is_refused(tmp_path):
    """Read as text is not read as an occurrence.

    A material that decompresses cleanly but is not JSON raised
    `JSONDecodeError` through `get()`, and so did a text material damaged in
    place — reachable before compression existed. It is the same condition as
    one that will not decompress: the stored row no longer carries what it was
    identified from.
    """

    import zlib
    from seed_runtime.events import InvalidStoredMaterial

    material = {"dimensions": {"content": "y" * 5000}}
    damage = {
        "compressed, not json": zlib.compress(b"not json at all", 1),
        "text, not json": "not json at all",
        "text, truncated json": json.dumps(material)[:40],
    }
    for label, stored in damage.items():
        path = str(tmp_path / f"{label.replace(' ', '_').replace(',', '')}.db")
        ledger = SQLiteEventLedger(path)
        try:
            event = ledger.append("k", material)
        finally:
            ledger.close()

        connection = sqlite3.connect(path)
        connection.execute("DROP TRIGGER events_refuse_update")
        connection.execute(
            "UPDATE events SET material = ? WHERE identity = ?", (stored, event.identity)
        )
        connection.commit()
        connection.close()

        ledger = SQLiteEventLedger(path)
        try:
            assert ledger.integrity_of(event.identity) == CORRUPTED, label
            with pytest.raises(InvalidStoredMaterial):
                ledger.get(event.identity)
        finally:
            ledger.close()
