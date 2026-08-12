"""Ledger-owned boundaries recover exact append prefixes without exposing positions."""

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
    first = ledger.append("wanted", "w", {"n": 1}, session_id="s")
    ledger.append("other", "elsewhere", {"n": 2}, session_id="s")
    boundary = ledger.capture_boundary()
    ledger.append("wanted", "w", {"n": 3}, session_id="s")
    ledger.append("wanted", "w", {"n": 4}, session_id="later")

    assert [event.id for event in ledger.list(through=boundary)] == [
        first.id,
        ledger.list()[1].id,
    ]
    assert [event.id for event in ledger.list("w", through=boundary)] == [first.id]
    assert [event.id for event in ledger.list_session(
        "w", "s", through=boundary
    )] == [first.id]
    assert [event.id for event in ledger.iter_session_kind(
        "w", "s", "wanted", through=boundary
    )] == [first.id]
    assert ledger.has_session("w", "s", through=boundary) is True
    assert ledger.has_session("w", "later", through=boundary) is False
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
    boundary = ledger.capture_boundary()
    ledger.append("k", "w")
    assert ledger.list(through=boundary) == []


def test_equal_prefixes_share_a_boundary_and_later_divergence_does_not_break_it():
    events = [
        Event(id="e1", kind="first", workspace_id="w", payload={"n": 1}),
        Event(id="e2", kind="second", workspace_id="w", payload={"n": 2}),
    ]
    left = EventLedger()
    right = EventLedger()
    left.extend(events)
    right.extend(events)
    boundary = left.capture_boundary()

    right.append("later", "w", {"side": "right"})

    assert right.capture_boundary() != boundary
    assert [event.id for event in right.list(through=boundary)] == ["e1", "e2"]


def test_independently_persisted_equal_prefixes_share_a_boundary(tmp_path):
    events = [
        Event(id="e1", kind="first", workspace_id="w", payload={"n": 1}),
        Event(id="e2", kind="second", workspace_id="w", payload={"n": 2}),
    ]
    left = SQLiteEventLedger(str(tmp_path / "left.db"))
    right = SQLiteEventLedger(str(tmp_path / "right.db"))
    try:
        left.extend(events)
        right.extend(events)
        boundary = left.capture_boundary()
        right.append("later", "w")

        assert [event.id for event in right.list(through=boundary)] == ["e1", "e2"]
    finally:
        left.close()
        right.close()


@pytest.mark.parametrize("durable", (False, True))
def test_batched_and_repeated_appends_produce_the_same_boundary(tmp_path, durable):
    events = [
        Event(id="e1", kind="first", workspace_id="w", payload={"n": 1}),
        Event(id="e2", kind="second", workspace_id="w", payload={"n": 2}),
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

        assert batched.capture_boundary() == repeated.capture_boundary()
    finally:
        if durable:
            batched.close()
            repeated.close()


def test_a_boundary_from_a_different_prefix_is_refused():
    left = EventLedger()
    right = EventLedger()
    left.append("k", "w", {"value": "left"})
    right.append("k", "w", {"value": "right"})

    with pytest.raises(InvalidLedgerBoundary):
        right.list(through=left.capture_boundary())


def test_a_durable_boundary_survives_reopen(tmp_path):
    path = str(tmp_path / "ledger.db")
    ledger = SQLiteEventLedger(path)
    first = ledger.append("k", "w", {"n": 1})
    boundary = ledger.capture_boundary()
    ledger.append("k", "w", {"n": 2})
    ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        assert [event.id for event in reopened.list(through=boundary)] == [first.id]
    finally:
        reopened.close()


def test_an_existing_durable_sequence_is_derived_once_without_changing_rows(tmp_path):
    path = str(tmp_path / "ledger.db")
    ledger = SQLiteEventLedger(path)
    events = [ledger.append("k", "w", {"n": n}) for n in range(3)]
    before = ledger.capture_boundary()
    ledger.close()

    connection = sqlite3.connect(path)
    connection.execute("DROP TABLE event_prefix_commitments")
    connection.commit()
    connection.close()

    reopened = SQLiteEventLedger(path)
    try:
        assert reopened.capture_boundary() == before
        assert [event.id for event in reopened.list(through=before)] == [
            event.id for event in events
        ]
    finally:
        reopened.close()


def test_partial_durable_mechanics_are_refused(tmp_path):
    path = str(tmp_path / "ledger.db")
    ledger = SQLiteEventLedger(path)
    ledger.append_many([
        Event(id="e1", kind="k", workspace_id="w"),
        Event(id="e2", kind="k", workspace_id="w"),
    ])
    ledger.close()

    connection = sqlite3.connect(path)
    connection.execute("DROP TRIGGER prefix_commitments_refuse_delete")
    connection.execute("DELETE FROM event_prefix_commitments WHERE position = 2")
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
            "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("foreign", "k", "w", "system", "2026-01-01T00:00:00+00:00",
             "{}", None, None, None, "not-relevant"),
        )
    connection.close()


def test_a_constructed_unknown_boundary_is_refused():
    ledger = EventLedger()
    with pytest.raises(InvalidLedgerBoundary):
        ledger.list(through=EventLedgerBoundary("0" * 64))


def test_a_refused_payload_leaves_the_ledger_unchanged():
    """Whatever is refused, nothing is left half-appended.

    The refusal moved earlier than the serializer: `#2495` refuses a payload a
    durable store could not return unchanged, so an unsupported value is now
    declined by name rather than as a `TypeError` out of `json.dumps`. What this
    test is about is unchanged — the boundary and the history stay exactly as
    they were.
    """

    for payload in (
        {"not_json": object()},
        {"tuple": (1, 2)},
        {"nested": {"deeper": {"key": {1: "x"}}}},
        {"set": {1, 2}},
    ):
        ledger = EventLedger()
        before = ledger.capture_boundary()

        with pytest.raises(ValueError):
            ledger.append("k", "w", payload)

        assert ledger.capture_boundary() == before
        assert ledger.list() == []


def _identity_read_matches_occurrence_read(ledger):
    """An identity read returns exactly the identities the occurrence read does.

    Both ledgers are held to it, and at every boundary, because a caller that
    compares recovered identities against carried ones must not be able to reach
    a different bounded population by reading less.
    """

    boundaries = [None]
    ledger.append_many([
        Event(id="i1", kind="ingress", workspace_id="w", session_id="s"),
        Event(id="i2", kind="other", workspace_id="w", session_id="s"),
        Event(id="i3", kind="ingress", workspace_id="w", session_id="other"),
    ])
    boundaries.append(ledger.capture_boundary())
    ledger.append_many([
        Event(id="i4", kind="ingress", workspace_id="w", session_id="s"),
        Event(id="i5", kind="ingress", workspace_id="other", session_id="s"),
    ])
    boundaries.append(ledger.capture_boundary())

    for boundary in boundaries:
        occurrences = [
            event.id
            for event in ledger.iter_session_kind("w", "s", "ingress", through=boundary)
        ]
        identities = list(
            ledger.iter_session_kind_ids("w", "s", "ingress", through=boundary)
        )
        assert identities == occurrences

    assert list(ledger.iter_session_kind_ids("w", "s", "ingress")) == ["i1", "i4"]
    assert list(ledger.iter_session_kind_ids("w", "s", "ingress",
                                             through=boundaries[1])) == ["i1"]
    assert list(ledger.iter_session_kind_ids("w", "s", "absent")) == []


def test_an_in_memory_identity_read_matches_its_occurrence_read():
    _identity_read_matches_occurrence_read(EventLedger())


def test_a_durable_identity_read_matches_its_occurrence_read(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "ledger.db"))
    try:
        _identity_read_matches_occurrence_read(ledger)
    finally:
        ledger.close()


def test_the_two_ledgers_preserve_the_same_payload(tmp_path):
    """An append must mean the same thing in either ledger.

    They share an API and are used interchangeably, and a durable store silently
    returned `[1, 2]` for a tuple and `{"1": ...}` for an integer key while the
    in-memory ledger returned what the caller passed. The same append produced
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
        in_memory = memory.append("k", "w", preservable)
        stored = durable.append("k", "w", preservable)
        assert memory.get(in_memory.id).payload == preservable
        assert durable.get(stored.id).payload == preservable

        # And what neither can preserve is refused by both, identically.
        for payload in (
            {"tuple": (1, 2)},
            {"nested tuple": {"a": ("x",)}},
            {"int key": {1: "x"}},
            {"nested int key": {"a": {"b": {2: "x"}}}},
            {"bytes": b"raw"},
            {"set": {1}},
        ):
            with pytest.raises(ValueError) as memory_refusal:
                memory.append("k", "w", payload)
            with pytest.raises(ValueError) as durable_refusal:
                durable.append("k", "w", payload)
            assert str(memory_refusal.value) == str(durable_refusal.value)
            # The path is reported, so a nested one is findable.
            assert "payload[" in str(memory_refusal.value)
    finally:
        durable.close()


def test_a_digest_requires_every_recorded_field():
    """An absent field and a null field are different rows."""

    from seed_runtime.events import _content_digest, LedgerIntegrityError

    complete = {
        "id": "e", "kind": "k", "workspace_id": "w", "actor": "system",
        "timestamp": "2026-01-01T00:00:00+00:00", "payload": "{}",
        "session_id": None, "causation_id": None, "correlation_id": None,
    }
    assert _content_digest(complete)

    for field in complete:
        partial = {k: v for k, v in complete.items() if k != field}
        with pytest.raises(LedgerIntegrityError, match=field):
            _content_digest(partial)
