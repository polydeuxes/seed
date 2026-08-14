"""Mutation refused by default, and corruption made detectable.

Neither is immutability. A `DROP TRIGGER` followed by a rewrite of both the row
and its digest defeats all of this, and these tests say so rather than letting
the arrangement be read as tamper-proof storage.

`06.Standing:16` names append-only records permissively, beside projected
material and context representations. Nothing in active law requires append-only, so this
establishes a storage property Seed chose, not one the Book demanded.
"""

from __future__ import annotations

import json
import random
import sqlite3

import pytest

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
# What is not asserted.
# --------------------------------------------------------------------------


def test_rewriting_the_row_and_its_digest_together_is_not_detected(ledger, path):
    """Stated as a test so the limit cannot be forgotten.

    Someone able to write arbitrary SQL can drop the guard, rewrite the row,
    and recompute the digest. Detecting that needs an integrity root outside
    the mutable database, which this does not have and does not Assertion.
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


def test_verified_durable_rehydration_still_rejects_nested_secret_fields(path):
    """Row integrity and secret-field admission remain separate boundaries."""
    from seed_runtime.events import _content_digest

    ledger = SQLiteEventLedger(path)
    event = ledger.append("k", "w", {"a": 1}, session_id="s")
    ledger.close()

    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    row = dict(con.execute("SELECT * FROM events WHERE id = ?", (event.id,)).fetchone())
    row["payload"] = '{"outer":[[{"token":"not-accepted"}]]}'
    con.execute(
        "UPDATE events SET payload = ?, content_hash = ? WHERE id = ?",
        (row["payload"], _content_digest(row), event.id),
    )
    con.commit()
    con.close()

    reopened = SQLiteEventLedger(path)
    try:
        assert reopened.integrity_of(event.id) == VERIFIED
        with pytest.raises(ValueError, match="secret field"):
            reopened.get(event.id)
    finally:
        reopened.close()


def test_screened_durable_rehydration_still_runs_event_validation(path):
    from seed_runtime.events import _content_digest

    ledger = SQLiteEventLedger(path)
    event = ledger.append("k", "w", {"a": 1}, session_id="s")
    ledger.close()

    con = _raw(path)
    con.execute("DROP TRIGGER events_refuse_update")
    row = dict(con.execute("SELECT * FROM events WHERE id = ?", (event.id,)).fetchone())
    row["payload"] = "[]"
    con.execute(
        "UPDATE events SET payload = ?, content_hash = ? WHERE id = ?",
        (row["payload"], _content_digest(row), event.id),
    )
    con.commit()
    con.close()

    reopened = SQLiteEventLedger(path)
    try:
        assert reopened.integrity_of(event.id) == VERIFIED
        with pytest.raises(ValueError, match="payload"):
            reopened.get(event.id)
    finally:
        reopened.close()


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

    An earlier form classified undigested rows as UNVERIFIABLE and input
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
# The Act with participating inputs are where verification happens.
# --------------------------------------------------------------------------


def test_a_comparison_refuses_a_corrupted_input(path, monkeypatch):
    from io import StringIO
    from seed_runtime.adjacent_pair_measurement import measure_after
    from seed_runtime.preserved_material_measurement import (
        preserved_ingress_occurrences, record_measurement_finding)
    from seed_runtime.operator_console import run_persistent_operator_console

    led = SQLiteEventLedger(path)
    for session_id in ("s1", "s2"):
        run_persistent_operator_console(
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
    from seed_runtime.operator_console import run_persistent_operator_console

    led = SQLiteEventLedger(path)
    try:
        for session_id in ("s1", "s2"):
            run_persistent_operator_console(
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
    from seed_runtime.operator_console import run_persistent_operator_console

    led = EventLedger()
    ids = []
    for session_id in ("s1", "s2"):
        run_persistent_operator_console(
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

    `#2426` asserted that opening implies the store was born current, but only
    checked that the column existed and that no row was currently NULL. A store
    created by the withdrawn ALTER path is nullable, and one populated entirely
    with valid digests would have passed while still admitting an undigested
    occurrence later. Prose asserting a property runtime does not enforce is the
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


# --------------------------------------------------------------------------
# Identifier counters are kept, not validated.
# --------------------------------------------------------------------------


def test_reservations_are_read_from_the_table_not_from_history(path):
    """`#2414`'s whole-history read, replaced by a durable counter.

    The open cost was linear in stored events — 36.9s at 100,000 — because
    every payload was deserialized and walked to reconstruct a few integers.
    """
    led = SQLiteEventLedger(path)
    try:
        led.append("k", "w", {"ref": "operator_material_000042"}, session_id="session_000007")
        led.append("k", "w", {"ref": "system_material_000005"})
    finally:
        led.close()

    con = _raw(path)
    try:
        kept = dict(con.execute("SELECT prefix, max_suffix FROM id_reservations"))
    finally:
        con.close()
    assert kept["operator_material"] == 42
    assert kept["session"] == 7
    assert kept["system_material"] == 5


def test_a_reopened_store_does_not_reissue_identifiers(path):
    """The property the reservation exists for, across ledger lifetimes."""
    from seed_runtime.ids import _next_values, new_id

    led = SQLiteEventLedger(path)
    led.append("k", "w", {"ref": "operator_material_000042"})
    led.close()

    _next_values.clear()          # a fresh process counts from 1
    led = SQLiteEventLedger(path)
    try:
        assert new_id("operator_material") == "operator_material_000043"
    finally:
        led.close()


def test_a_reservation_only_ever_rises(path):
    led = SQLiteEventLedger(path)
    try:
        led.append("k", "w", {"ref": "operator_material_000042"})
        led.append("k", "w", {"ref": "operator_material_000007"})
    finally:
        led.close()
    con = _raw(path)
    try:
        kept = dict(con.execute("SELECT prefix, max_suffix FROM id_reservations"))
    finally:
        con.close()
    assert kept["operator_material"] == 42


def test_the_counter_table_is_not_an_occurrence(path):
    """It records no Assertion, so occurrence mutation refusal does not cover it."""
    led = SQLiteEventLedger(path)
    try:
        event = led.append("k", "w", {"ref": "operator_material_000042"})
    finally:
        led.close()
    con = _raw(path)
    try:
        con.execute("UPDATE id_reservations SET max_suffix = 99 WHERE prefix = 'operator_material'")
        con.commit()
    finally:
        con.close()
    led = SQLiteEventLedger(path)
    try:
        assert led.integrity_of(event.id) == VERIFIED
    finally:
        led.close()


def test_a_batch_commits_its_reservations_with_its_occurrences(path):
    """`#2428`'s invariant, which `append_many` did not satisfy.

    `append` inserts an occurrence and persists its reservations in one
    transaction. `append_many` used two, so a failure between them left durable
    occurrences carrying identifiers whose counters were stale on reopen —
    exactly the collision `#2428` exists to prevent.
    """
    from seed_runtime.event import Event

    led = SQLiteEventLedger(path)
    commits = []
    led._connection.set_trace_callback(commits.append)
    try:
        led.append_many([
            Event(id=f"evt_10000{i}", kind="k", workspace_id="w",
                  payload={"ref": f"operator_material_0000{40 + i}"}, session_id="session_000009")
            for i in range(3)
        ])
    finally:
        led._connection.set_trace_callback(None)
        led.close()

    assert sum(1 for q in commits if q.strip().upper() == "COMMIT") == 1

    con = _raw(path)
    try:
        kept = dict(con.execute("SELECT prefix, max_suffix FROM id_reservations"))
        stored = con.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    finally:
        con.close()
    assert stored == 3
    assert kept["operator_material"] == 42
    assert kept["session"] == 9


def test_a_batch_leaves_no_occurrence_without_its_reservation(path):
    """Reopening a batched store does not reissue a batched identifier."""
    from seed_runtime.ids import _next_values, new_id
    from seed_runtime.event import Event

    led = SQLiteEventLedger(path)
    led.append_many([
        Event(id="evt_100001", kind="k", workspace_id="w",
              payload={"ref": "operator_material_000077"}, session_id="s")
    ])
    led.close()

    _next_values.clear()
    led = SQLiteEventLedger(path)
    try:
        assert new_id("operator_material") == "operator_material_000078"
    finally:
        led.close()


def test_reservable_suffix_observation_matches_a_per_prefix_scan():
    """One split must find exactly what testing every prefix in turn found.

    A reservable identifier is a prefix, an underscore, and digits, so the
    digits begin just after the value's last underscore. This holds the split
    to that equivalence over generated payloads rather than over examples,
    because several movement prefixes overlap and a suffix of
    zero is deliberately not reserved.
    """

    from seed_runtime.events import _numeric_suffix, _walk_values

    prefixes = tuple(SQLiteEventLedger._RESERVABLE_PREFIXES)

    def per_prefix_scan(event):
        found = {}
        values = list(_walk_values(event.payload))
        if event.session_id is not None:
            values.append(event.session_id)
        for value in values:
            if not isinstance(value, str):
                continue
            for prefix in prefixes:
                suffix = _numeric_suffix(value, prefix)
                if suffix is not None and suffix > found.get(prefix, 0):
                    found[prefix] = suffix
        return found

    tokens = list(prefixes) + ["evt", "x", "", "retired_fact", "need"]
    rng = random.Random(11)

    def identifier():
        token = rng.choice(tokens)
        return rng.choice([
            f"{token}_{rng.randint(0, 999)}",
            f"{token}_{rng.choice(['', 'x', '0a', '007'])}",
            token,
            f"_{rng.randint(0, 99)}",
            f"{token}__{rng.randint(0, 99)}",
        ])

    def value(depth=0):
        roll = rng.random()
        if depth < 3 and roll < 0.3:
            return {identifier(): value(depth + 1) for _ in range(rng.randint(0, 4))}
        if depth < 3 and roll < 0.45:
            return [value(depth + 1) for _ in range(rng.randint(0, 4))]
        if roll < 0.75:
            return identifier()
        return rng.choice([None, True, 7, 3.5])

    ledger = SQLiteEventLedger.__new__(SQLiteEventLedger)
    for index in range(1500):
        payload = value()
        if not isinstance(payload, dict):
            payload = {"k": payload}
        event = Event(
            id=f"evt_{index}",
            kind="k",
            workspace_id="w",
            payload=payload,
            session_id=rng.choice([None, identifier(), f"session_{rng.randint(0, 9999)}"]),
        )
        assert ledger._observed_suffixes(event) == per_prefix_scan(event)


def test_a_reserved_suffix_of_zero_is_not_reserved():
    """`suffix > found.get(prefix, 0)` deliberately declines zero, and the
    split must decline it too rather than reserve prefix zero."""

    ledger = SQLiteEventLedger.__new__(SQLiteEventLedger)
    event = Event(id="evt_1", kind="k", workspace_id="w", payload={"a": "operator_material_0"})
    assert ledger._observed_suffixes(event) == {}
    event = Event(id="evt_2", kind="k", workspace_id="w", payload={"a": "operator_material_1"})
    assert ledger._observed_suffixes(event) == {"operator_material": 1}


def test_an_overlapping_prefix_reserves_the_longer_match():
    ledger = SQLiteEventLedger.__new__(SQLiteEventLedger)
    event = Event(
        id="evt_1", kind="k", workspace_id="w",
        payload={"a": "assertion_locality_movement_act_7", "b": "assertion_locality_movement_4"},
    )
    assert ledger._observed_suffixes(event) == {
        "assertion_locality_movement_act": 7,
        "assertion_locality_movement": 4,
    }


def test_a_cache_hit_still_refuses_a_contradictory_support_count():
    """A forged count must be refused whichever validation reaches it first.

    `SupportValidator` keys on the commitment, not the count, so a second basis
    committing to the same inputs reaches a cached result. Curator found
    that the count check then never ran, which made catching a forged count
    depend on what the act happened to have validated earlier.
    """

    from seed_runtime.support_basis import (
        SupportBasis,
        SupportBasisError,
        SupportValidator,
        declare_complete_inputs,
    )

    ledger = EventLedger()
    ledger.append_many([
        Event(id=f"evt_{index}", kind="ingress", workspace_id="w", session_id="s")
        for index in range(4)
    ])
    boundary = ledger.capture_boundary()
    identities = tuple(ledger.iter_session_kind_ids("w", "s", "ingress", through=boundary))
    honest = declare_complete_inputs(
        workspace_id="w", session_id="s", occurrence_kind="ingress",
        boundary=boundary, identities=identities,
    )
    forged = SupportBasis(
        workspace_id=honest.workspace_id,
        session_id=honest.session_id,
        occurrence_kind=honest.occurrence_kind,
        boundary_commitment=honest.boundary_commitment,
        selection_rule=honest.selection_rule,
        commitment=honest.commitment,
        support_count=honest.support_count - 1,
    )

    # Refused on a cold validation.
    with pytest.raises(SupportBasisError, match="declared count"):
        SupportValidator(ledger).validate(forged)

    # And refused after the same inputs has been cached, which is the path
    # that previously returned it.
    validation = SupportValidator(ledger)
    assert validation.validate(honest) == identities
    assert validation.reads == 1
    with pytest.raises(SupportBasisError, match="declared count"):
        validation.validate(forged)
    assert validation.reuses == 0

    # An honest second reference still reuses rather than re-reading.
    assert validation.validate(honest) == identities
    assert (validation.reads, validation.reuses) == (1, 1)


def test_every_support_basis_refusal_can_be_reached():
    """Each refusal a support basis declares must actually fire.

    A refusal no test has triggered is a refusal nobody has verified, and this
    module's refusals are what stand in for the enumeration it no longer
    carries.
    """

    from seed_runtime.support_basis import (
        COMPLETE_INGRESS_INPUTS,
        SupportBasis,
        SupportBasisError,
        support_commitment,
    )

    def basis(**changes):
        fields = dict(
            workspace_id="w", session_id="s", occurrence_kind="k",
            boundary_commitment="b", selection_rule=COMPLETE_INGRESS_INPUTS,
            commitment=support_commitment(COMPLETE_INGRESS_INPUTS, ()),
            support_count=0,
        )
        fields.update(changes)
        return SupportBasis(**fields)

    basis()  # the honest one is constructible

    with pytest.raises(SupportBasisError, match="recognised selection"):
        basis(selection_rule="a selection nobody established")

    # A selection rule is established as a representation before it is looked
    # up, because frozenset membership hashes its argument. `[]` and `{}` leaked
    # a raw TypeError; `set()` did not, only because CPython converts a set
    # argument to a frozenset before testing membership. Both outcomes are held
    # so neither depends on that quirk.
    for value in ([], {}, set(), None, 1, True, b"x", ("a",)):
        with pytest.raises(SupportBasisError, match="recognised selection"):
            basis(selection_rule=value)
        with pytest.raises(SupportBasisError):
            SupportBasis.from_json_dict(dict(basis().to_json_dict(), selection_rule=value))

    for name in ("workspace_id", "session_id", "occurrence_kind",
                 "boundary_commitment", "commitment"):
        with pytest.raises(SupportBasisError, match=f"requires {name}"):
            basis(**{name: ""})
        with pytest.raises(SupportBasisError, match=f"requires {name}"):
            basis(**{name: None})

    with pytest.raises(SupportBasisError, match="negative count"):
        basis(support_count=-1)

    # A count coordinate must establish that it can be a count. Each of these
    # previously either leaked a raw TypeError from the comparison or was
    # accepted outright.
    for value in ("4", None, True, False, 4.0, [], {}, ()):
        with pytest.raises(SupportBasisError, match="integer support count"):
            basis(support_count=value)

    # `True` mattered most: it is an int and equals 1, so a basis carrying it
    # would have agreed with a one-occurrence inputs.
    assert True == 1

    with pytest.raises(SupportBasisError, match="not present"):
        SupportBasis.from_json_dict(None)
    with pytest.raises(SupportBasisError, match="not present"):
        SupportBasis.from_json_dict("a string is not a basis")

    complete = basis().to_json_dict()
    assert SupportBasis.from_json_dict(complete) == basis()
    for key in ("scope", "boundary", "selection_rule", "commitment", "support_count"):
        partial = {k: v for k, v in complete.items() if k != key}
        with pytest.raises(SupportBasisError, match="incomplete"):
            SupportBasis.from_json_dict(partial)


def test_a_commitment_distinguishes_order_and_rule_not_only_membership():
    """Two selections returning the same identities in a different order, or
    under a different rule, must not commit to the same digest."""

    from seed_runtime.support_basis import (
        COMPLETE_INGRESS_INPUTS, support_commitment,
    )

    ordered = support_commitment(COMPLETE_INGRESS_INPUTS, ("a", "b", "c"))
    assert ordered != support_commitment(COMPLETE_INGRESS_INPUTS, ("a", "c", "b"))
    assert ordered != support_commitment("another rule", ("a", "b", "c"))
    assert ordered != support_commitment(COMPLETE_INGRESS_INPUTS, ("a", "b"))
    assert support_commitment(COMPLETE_INGRESS_INPUTS, ("ab", "c")) != \
           support_commitment(COMPLETE_INGRESS_INPUTS, ("a", "bc"))

    # The parts must be unambiguous when a part contains whatever divides them.
    # An earlier encoding separated parts with a NUL, which held only while no
    # identity carried one — and nothing constrains an Event.id. Both of these
    # produced one digest for two different inputss.
    assert support_commitment(COMPLETE_INGRESS_INPUTS, ("a", "b\0c")) != \
           support_commitment(COMPLETE_INGRESS_INPUTS, ("a\0b", "c"))
    assert support_commitment("a", ("b",)) != support_commitment("a\0b", ())

    # And the same requirement under the length prefix that replaced it.
    assert support_commitment("a", ("b",)) != support_commitment("ab", ())
    assert support_commitment(COMPLETE_INGRESS_INPUTS, ("", "ab")) != \
           support_commitment(COMPLETE_INGRESS_INPUTS, ("a", "b"))
    assert support_commitment(COMPLETE_INGRESS_INPUTS, ("",)) != \
           support_commitment(COMPLETE_INGRESS_INPUTS, ())
    # Multi-byte identities are committed by encoded length, not character count.
    assert support_commitment(COMPLETE_INGRESS_INPUTS, ("é",)) != \
           support_commitment(COMPLETE_INGRESS_INPUTS, ("ab",))

    # A part that is not a representation is refused rather than leaking from
    # the encode. The rule is a part too, and is held to the same requirement.
    from seed_runtime.support_basis import SupportBasisError as _E
    for bad in (1, None, b"bytes", ["a"]):
        with pytest.raises(_E, match="must be a representation"):
            support_commitment(COMPLETE_INGRESS_INPUTS, (bad,))
        with pytest.raises(_E, match="must be a representation"):
            support_commitment(bad, ("a",))


def test_a_digest_does_not_move_when_a_payload_is_compressed(tmp_path):
    """The digest commits to what an occurrence carries, not how it was stored.

    `#2494` put compression below the integrity boundary. If the digest were
    taken over the stored bytes instead of the canonical string, an occurrence
    would verify differently depending on whether it happened to compress, and
    a store written before compression would verify as CORRUPTED.
    """

    import zlib
    from seed_runtime.events import _content_digest, _stored_payload, _serialized_payload

    payload = {"dimensions": {"content": "x" * 4000}, "n": list(range(200))}
    small = {"a": 1}

    for value in (payload, small):
        serialized = json.dumps(value)
        row = {
            "id": "evt_1", "kind": "k", "workspace_id": "w", "actor": "system",
            "timestamp": "2026-01-01T00:00:00+00:00", "payload": serialized,
            "session_id": None, "causation_id": None, "correlation_id": None,
        }
        digest = _content_digest(row)
        stored = _stored_payload(serialized)
        # Whatever the store holds, it reconstructs the canonical string exactly,
        # and digesting that reproduces the same commitment.
        assert _serialized_payload(stored) == serialized
        assert _content_digest(dict(row, payload=_serialized_payload(stored))) == digest

    # Large payloads compress and are stored as bytes; tiny ones do not and are
    # stored as text, because compressing them would cost bytes for nothing.
    assert isinstance(_stored_payload(json.dumps(payload)), bytes)
    assert isinstance(_stored_payload(json.dumps(small)), str)


def test_compressed_and_uncompressed_stores_verify_alike(tmp_path):
    path = str(tmp_path / "ledger.db")
    ledger = SQLiteEventLedger(path)
    payload = {"dimensions": {"content": "y" * 5000}, "n": list(range(300))}
    try:
        compressed = ledger.append("k", "w", payload)
        plain = ledger.append("k", "w", {"a": 1})
        assert ledger.integrity_of(compressed.id) == VERIFIED
        assert ledger.integrity_of(plain.id) == VERIFIED
        assert ledger.get(compressed.id).payload == payload
        assert ledger.get(plain.id).payload == {"a": 1}
    finally:
        ledger.close()

    # Stored forms differ; standing does not.
    connection = sqlite3.connect(path)
    stored = {
        row[0]: row[1]
        for row in connection.execute("SELECT id, payload FROM events")
    }
    connection.close()
    assert isinstance(stored[compressed.id], bytes)
    assert isinstance(stored[plain.id], str)


def test_a_store_written_before_compression_still_reads_and_verifies(tmp_path):
    """Text payloads predate `#2494` and must not become unreadable or corrupt."""

    path = str(tmp_path / "legacy.db")
    ledger = SQLiteEventLedger(path)
    payload = {"dimensions": {"content": "z" * 5000}}
    try:
        event = ledger.append("k", "w", payload)
    finally:
        ledger.close()

    # Rewrite the row as an older store would have held it: canonical text, and
    # the same digest, since the digest never covered the stored form.
    connection = sqlite3.connect(path)
    connection.execute("DROP TRIGGER events_refuse_update")
    connection.execute(
        "UPDATE events SET payload = ? WHERE id = ?",
        (json.dumps(payload), event.id),
    )
    connection.commit()
    connection.close()

    ledger = SQLiteEventLedger(path)
    try:
        assert ledger.get(event.id).payload == payload
        assert ledger.integrity_of(event.id) == VERIFIED
    finally:
        ledger.close()


def test_damaged_compressed_storage_is_corruption_not_a_compressor_error(tmp_path):
    """Damage the compressed bytes, not the row's type.

    An earlier version of this test replaced the BLOB with `json.dumps(...)`,
    which SQLite returns as `str`, so `zlib.decompress` was never reached and
    the test passed through the ordinary text path while asserting to exercise
    compressed corruption. Curator caught it. Damaged compressed bytes had been
    leaking raw `zlib.error` and `UnicodeDecodeError` through `integrity_of`.
    """

    import zlib
    from seed_runtime.events import InvalidStoredPayload

    payload = {"dimensions": {"content": "q" * 5000}}
    intact = zlib.compress(json.dumps(payload).encode("utf-8"), 1)

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
            event = ledger.append("k", "w", payload)
        finally:
            ledger.close()

        connection = sqlite3.connect(path)
        connection.execute("DROP TRIGGER events_refuse_update")
        connection.execute(
            "UPDATE events SET payload = ? WHERE id = ?", (stored, event.id)
        )
        connection.commit()
        connection.close()

        ledger = SQLiteEventLedger(path)
        try:
            # Reported, never raised through the caller.
            assert ledger.integrity_of(event.id) == CORRUPTED, label
            # And a read refuses as a ledger integrity failure rather than
            # exposing the compressor.
            with pytest.raises(InvalidStoredPayload):
                ledger.get(event.id)
        finally:
            ledger.close()


def test_a_compressed_payload_altered_to_other_valid_content_is_corrupted(tmp_path):
    """The digest still settles it when the storage reconstructs cleanly."""

    import zlib

    path = str(tmp_path / "swapped.db")
    ledger = SQLiteEventLedger(path)
    try:
        event = ledger.append("k", "w", {"dimensions": {"content": "q" * 5000}})
    finally:
        ledger.close()

    connection = sqlite3.connect(path)
    connection.execute("DROP TRIGGER events_refuse_update")
    connection.execute(
        "UPDATE events SET payload = ? WHERE id = ?",
        (zlib.compress(json.dumps({"dimensions": {"content": "other"}}).encode(), 1), event.id),
    )
    connection.commit()
    connection.close()

    ledger = SQLiteEventLedger(path)
    try:
        assert ledger.integrity_of(event.id) == CORRUPTED
    finally:
        ledger.close()


def test_a_stored_payload_that_is_not_an_occurrence_is_refused(tmp_path):
    """Reconstructing as text is not reconstructing as an occurrence.

    A payload that decompresses cleanly but is not JSON raised
    `JSONDecodeError` through `get()`, and so did a text payload damaged in
    place — reachable before compression existed. It is the same condition as
    one that will not decompress: the stored row no longer carries what it was
    digested from.
    """

    import zlib
    from seed_runtime.events import InvalidStoredPayload

    payload = {"dimensions": {"content": "y" * 5000}}
    damage = {
        "compressed, not json": zlib.compress(b"not json at all", 1),
        "text, not json": "not json at all",
        "text, truncated json": json.dumps(payload)[:40],
    }
    for label, stored in damage.items():
        path = str(tmp_path / f"{label.replace(' ', '_').replace(',', '')}.db")
        ledger = SQLiteEventLedger(path)
        try:
            event = ledger.append("k", "w", payload)
        finally:
            ledger.close()

        connection = sqlite3.connect(path)
        connection.execute("DROP TRIGGER events_refuse_update")
        connection.execute(
            "UPDATE events SET payload = ? WHERE id = ?", (stored, event.id)
        )
        connection.commit()
        connection.close()

        ledger = SQLiteEventLedger(path)
        try:
            assert ledger.integrity_of(event.id) == CORRUPTED, label
            with pytest.raises(InvalidStoredPayload):
                ledger.get(event.id)
        finally:
            ledger.close()
