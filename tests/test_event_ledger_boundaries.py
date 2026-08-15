"""Ledger-bound occurrences read exact append prefixes without exposing positions."""

from __future__ import annotations

import sqlite3

import pytest

from seed_runtime.events import (
    EventLedger,
    EventLedgerBoundary,
    InvalidLedgerBoundary,
    LedgerIntegrityError,
    SQLiteEventLedger,
)
from seed_runtime.event import Event


def _exercise_scoped_reads(ledger):
    first = ledger.append("wanted", {"n": 1}, locality_identity="s")
    ledger.append("other", {"n": 2}, locality_identity="s")
    boundary = ledger.append_boundary()
    ledger.append("wanted", {"n": 3}, locality_identity="s")
    ledger.append("wanted", {"n": 4}, locality_identity="later")

    assert [event.identity for event in ledger.list(through=boundary)] == [
        first.identity,
        ledger.list()[1].identity,
    ]
    assert [event.identity for event in ledger.list(through=boundary)] == [
        first.identity,
        ledger.list()[1].identity,
    ]
    assert [event.identity for event in ledger.list_locality(
        "s", through=boundary
    )] == [first.identity, ledger.list()[1].identity]
    assert [event.identity for event in ledger.iter_locality_kind(
        "s", "wanted", through=boundary
    )] == [first.identity]
    assert ledger.has_locality("s", through=boundary) is True
    assert ledger.has_locality("later", through=boundary) is False
    return boundary


@pytest.mark.parametrize("durable", (False, True))
def test_one_boundary_constrains_every_ordered_reader(tmp_path, durable):
    ledger = (
        SQLiteEventLedger(str(tmp_path / "ledger.db"))
        if durable
        else EventLedger()
    )
    try:
        _exercise_scoped_reads(ledger)
    finally:
        if durable:
            ledger.close()


def test_empty_boundary_excludes_later_occurrences():
    ledger = EventLedger()
    boundary = ledger.append_boundary()
    ledger.append("k")
    assert ledger.list(through=boundary) == []


def test_equal_prefixes_share_a_boundary_and_later_divergence_does_not_break_it():
    events = [
        Event(identity="e1", kind="first", material={"n": 1}),
        Event(identity="e2", kind="second", material={"n": 2}),
    ]
    left = EventLedger()
    right = EventLedger()
    left.extend(events)
    right.extend(events)
    boundary = left.append_boundary()

    right.append("later", {"side": "right"})

    assert right.append_boundary() != boundary
    assert [event.identity for event in right.list(through=boundary)] == ["e1", "e2"]


def test_exact_material_participates_in_the_append_boundary():
    left = EventLedger()
    right = EventLedger()
    left.extend([Event(identity="e1", kind="k", exact_material=b"left")])
    right.extend([Event(identity="e1", kind="k", exact_material=b"right")])

    assert left.append_boundary() != right.append_boundary()


@pytest.mark.parametrize(
    "value",
    ("material", bytearray(b"material"), memoryview(b"material"), 1),
)
def test_event_exact_material_requires_raw_bytes(value):
    with pytest.raises(ValueError, match="exact bytes or absent"):
        Event(identity="e1", kind="k", exact_material=value)


def test_independently_persisted_equal_prefixes_share_a_boundary(tmp_path):
    events = [
        Event(identity="e1", kind="first", material={"n": 1}),
        Event(identity="e2", kind="second", material={"n": 2}),
    ]
    left = SQLiteEventLedger(str(tmp_path / "left.db"))
    right = SQLiteEventLedger(str(tmp_path / "right.db"))
    try:
        left.extend(events)
        right.extend(events)
        boundary = left.append_boundary()
        right.append("later")

        assert [event.identity for event in right.list(through=boundary)] == ["e1", "e2"]
    finally:
        left.close()
        right.close()


@pytest.mark.parametrize("durable", (False, True))
def test_batched_and_repeated_appends_yield_the_same_boundary(tmp_path, durable):
    events = [
        Event(identity="e1", kind="first", material={"n": 1}),
        Event(identity="e2", kind="second", material={"n": 2}),
    ]
    if durable:
        batched = SQLiteEventLedger(str(tmp_path / "batched.db"))
        repeated = SQLiteEventLedger(str(tmp_path / "repeated.db"))
    else:
        batched = EventLedger()
        repeated = EventLedger()
    try:
        batched.append_many(events)
        for event in events:
            repeated.extend([event])

        assert batched.append_boundary() == repeated.append_boundary()
    finally:
        if durable:
            batched.close()
            repeated.close()


def test_a_boundary_from_a_different_prefix_is_refused():
    left = EventLedger()
    right = EventLedger()
    left.append("k", {"value": "left"})
    right.append("k", {"value": "right"})

    with pytest.raises(InvalidLedgerBoundary):
        right.list(through=left.append_boundary())


def test_a_durable_boundary_survives_reopen(tmp_path):
    path = str(tmp_path / "ledger.db")
    ledger = SQLiteEventLedger(path)
    first = ledger.append("k", {"n": 1})
    boundary = ledger.append_boundary()
    ledger.append("k", {"n": 2})
    ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        assert [event.identity for event in reopened.list(through=boundary)] == [first.identity]
    finally:
        reopened.close()


def test_an_existing_durable_sequence_is_derived_once_without_changing_rows(tmp_path):
    path = str(tmp_path / "ledger.db")
    ledger = SQLiteEventLedger(path)
    events = [ledger.append("k", {"n": n}) for n in range(3)]
    before = ledger.append_boundary()
    ledger.close()

    connection = sqlite3.connect(path)
    connection.execute("DROP TABLE event_prefix_identities")
    connection.commit()
    connection.close()

    reopened = SQLiteEventLedger(path)
    try:
        assert reopened.append_boundary() == before
        assert [event.identity for event in reopened.list(through=before)] == [
            event.identity for event in events
        ]
    finally:
        reopened.close()


def test_partial_durable_mechanics_are_refused(tmp_path):
    path = str(tmp_path / "ledger.db")
    ledger = SQLiteEventLedger(path)
    ledger.append_many([
        Event(identity="e1", kind="k"),
        Event(identity="e2", kind="k"),
    ])
    ledger.close()

    connection = sqlite3.connect(path)
    connection.execute("DROP TRIGGER prefix_identities_refuse_delete")
    connection.execute("DELETE FROM event_prefix_identities WHERE position = 2")
    connection.commit()
    connection.close()

    with pytest.raises(LedgerIntegrityError, match="incomplete"):
        SQLiteEventLedger(path)


def test_a_writer_without_prefix_maintenance_is_refused(tmp_path):
    path = str(tmp_path / "ledger.db")
    SQLiteEventLedger(path).close()

    connection = sqlite3.connect(path)
    with pytest.raises(sqlite3.OperationalError, match="seed_prefix_writer"):
        connection.execute(
            "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("foreign", "k", "2026-01-01T00:00:00+00:00", "{}",
             None, None, "not-relevant"),
        )
    connection.close()


def test_a_formed_unknown_boundary_is_refused():
    ledger = EventLedger()
    with pytest.raises(InvalidLedgerBoundary):
        ledger.list(through=EventLedgerBoundary("0" * 64))


def test_a_refused_material_leaves_the_ledger_unchanged():
    """Whatever is refused, nothing is left half-appended.

    The refusal moved earlier than the serializer: `#2495` refuses a material a
    durable store could not return preserved, so an unsupported value is now
    declined by name rather than as a `TypeError` out of `json.dumps`. What this
    test is about is preserved — the boundary and the history stay exactly as
    they were.
    """

    for material in (
        {"not_json": object()},
        {"tuple": (1, 2)},
        {"nested": {"deeper": {"key": {1: "x"}}}},
        {"set": {1, 2}},
    ):
        ledger = EventLedger()
        before = ledger.append_boundary()

        with pytest.raises(ValueError):
            ledger.append("k", material)

        assert ledger.append_boundary() == before
        assert ledger.list() == []


def _identity_read_matches_occurrence_read(ledger):
    """An identity read returns exactly the identities the occurrence read does.

    Both ledgers are held to it, and at every boundary, because a caller that
    compares read identities against carried ones must not be able to reach
    a different bounded inputs by read less.
    """

    boundaries = [None]
    ledger.append_many([
        Event(identity="i1", kind="ingest", locality_identity="s"),
        Event(identity="i2", kind="other", locality_identity="s"),
        Event(identity="i3", kind="ingest", locality_identity="other"),
    ])
    boundaries.append(ledger.append_boundary())
    ledger.append_many([
        Event(identity="i4", kind="ingest", locality_identity="s"),
        Event(identity="i5", kind="ingest", locality_identity="other"),
    ])
    boundaries.append(ledger.append_boundary())

    for boundary in boundaries:
        occurrences = [
            event.identity
            for event in ledger.iter_locality_kind("s", "ingest", through=boundary)
        ]
        identities = list(
            ledger.iter_locality_kind_identities("s", "ingest", through=boundary)
        )
        assert identities == occurrences

    assert list(ledger.iter_locality_kind_identities("s", "ingest")) == ["i1", "i4"]
    assert list(ledger.iter_locality_kind_identities("s", "ingest",
                                             through=boundaries[1])) == ["i1"]
    assert list(ledger.iter_locality_kind_identities("s", "absent")) == []


def test_an_in_memory_identity_read_matches_its_occurrence_read():
    _identity_read_matches_occurrence_read(EventLedger())


def test_a_durable_identity_read_matches_its_occurrence_read(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "ledger.db"))
    try:
        _identity_read_matches_occurrence_read(ledger)
    finally:
        ledger.close()


def test_the_two_ledgers_preserve_the_same_material(tmp_path):
    """An append must mean the same thing in either ledger.

    They share an API and are used interchangeably, and a durable store silently
    returned `[1, 2]` for a tuple and `{"1": ...}` for an integer key while the
    in-memory ledger returned what the caller passed. The same append yielded
    two different occurrences depending on which ledger held it, with nothing
    recorded to say so.
    """

    memory = EventLedger()
    durable = SQLiteEventLedger(str(tmp_path / "both.db"))
    try:
        preservable = {
            "text": "the cat", "list": [1, 2], "nested": {"a": {"b": [1, {"c": None}]}},
            "numbers": [1, 1.5, True, False, None],
        }
        in_memory = memory.append("k", preservable)
        stored = durable.append("k", preservable)
        assert memory.get(in_memory.identity).material == preservable
        assert durable.get(stored.identity).material == preservable

        # And what neither can preserve is refused by both, identically.
        for material in (
            {"tuple": (1, 2)},
            {"nested tuple": {"a": ("x",)}},
            {"int key": {1: "x"}},
            {"nested int key": {"a": {"b": {2: "x"}}}},
            {"bytes": b"raw"},
            {"set": {1}},
        ):
            with pytest.raises(ValueError) as memory_refusal:
                memory.append("k", material)
            with pytest.raises(ValueError) as durable_refusal:
                durable.append("k", material)
            assert str(memory_refusal.value) == str(durable_refusal.value)
            # The path is reported, so a nested one is findable.
            assert "material[" in str(memory_refusal.value)
    finally:
        durable.close()


def test_occurrence_material_identity_requires_every_recorded_field():
    """An absent field and a null field are different rows."""

    from seed_runtime.events import _occurrence_material_identity, LedgerIntegrityError

    complete = {
        "identity": "e", "kind": "k",
        "timestamp": "2026-01-01T00:00:00+00:00", "material": "{}",
        "exact_material": None,
        "locality_identity": None,
    }
    assert _occurrence_material_identity(complete)

    for field in complete:
        partial = {k: v for k, v in complete.items() if k != field}
        with pytest.raises(LedgerIntegrityError, match=field):
            _occurrence_material_identity(partial)


def test_a_material_carrying_a_non_json_number_is_refused(tmp_path):
    """`NaN` and the infinities are not JSON, whatever Python's encoder allows.

    `NaN` never equals itself and so cannot round-trip at all. The infinities do
    round-trip, but only under Python's own permissive encoder — no strict
    reader accepts `NaN` or `Infinity`, so a store holding one is readable by
    nothing else. `#2492` was this exact lesson at the base64 boundary: a
    durable representation must not depend on one runtime's leniency.
    """

    memory = EventLedger()
    durable = SQLiteEventLedger(str(tmp_path / "numbers.db"))
    try:
        for value in (float("nan"), float("inf"), float("-inf")):
            with pytest.raises(ValueError, match="not a JSON number"):
                memory.append("k", {"a": value})
            with pytest.raises(ValueError, match="not a JSON number"):
                durable.append("k", {"a": value})
            with pytest.raises(ValueError, match=r"material\['a'\]\['b'\]\[0\]"):
                memory.append("k", {"a": {"b": [value]}})

        # Ordinary numbers, including the awkward ones, still pass.
        finite = {"large": 1e308, "small": 5e-324, "negative zero": -0.0,
                  "int": 0, "negative": -5, "bool": True}
        in_memory = memory.append("k", finite)
        stored = durable.append("k", finite)
        assert memory.get(in_memory.identity).material == durable.get(stored.identity).material
    finally:
        durable.close()


def test_a_python_subclass_does_not_survive_the_store_and_is_refused(tmp_path):
    """The boundary is JSON value identity, held by exact type.

    A durable store returns the JSON type, so an `IntEnum` came back as `int`, a
    `str` subclass as `str`, a `list` subclass as `list`. That is the same
    divergence a tuple caused, and an `isinstance` gate admitted every one of
    them — the rule was stated as one thing and enforced as another.
    """

    import enum

    class Colour(enum.IntEnum):
        RED = 1

    class Name(str):
        pass

    class Rows(list):
        pass

    class Table(dict):
        pass

    memory = EventLedger()
    durable = SQLiteEventLedger(str(tmp_path / "subclasses.db"))
    try:
        for material in (
            {"a": Colour.RED},
            {"a": Name("x")},
            {"a": Rows([1])},
            {"a": Table({"b": 1})},
            {"a": {"b": [Colour.RED]}},
            {Name("key"): 1},
        ):
            with pytest.raises(ValueError) as from_memory:
                memory.append("k", material)
            with pytest.raises(ValueError) as from_durable:
                durable.append("k", material)
            assert str(from_memory.value) == str(from_durable.value)

        # bool is an int subclass and must remain admissible.
        both = {"true": True, "false": False, "int": 1}
        in_memory = memory.append("k", both)
        stored = durable.append("k", both)
        assert memory.get(in_memory.identity).material == both
        assert durable.get(stored.identity).material == both
        assert type(durable.get(stored.identity).material["true"]) is bool
    finally:
        durable.close()
