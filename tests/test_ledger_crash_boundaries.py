"""What a durable ledger can and cannot lose without saying so.

Losing the tip and corrupting lineage are different failures. A store that
lost its last occurrences still answers every question the remaining ones
support. A store whose chain no longer matches its occurrences answers
nothing safely, and must say so rather than serve a shorter history as if it
were the whole one.

Every crash here is simulated by deleting rows with the refusal triggers
dropped, which is what a lost write leaves behind: a store the triggers never
saw.
"""

from __future__ import annotations

import sqlite3

import pytest

from seed_runtime.events import (
    InvalidLedgerBoundary,
    LedgerIntegrityError,
    SQLiteEventLedger,
    VERIFIED,
)


def _build(path, count=50):
    ledger = SQLiteEventLedger(str(path))
    ids = [
        ledger.append("k", "w", {"i": i}, locality_id="s1").id for i in range(count)
    ]
    return ledger, ids


def _lose(path, *, occurrences=0, commitments=0):
    """Drop the tail of either table, as an unflushed write would."""

    connection = sqlite3.connect(str(path))
    for trigger in ("events_refuse_delete", "prefix_commitments_refuse_delete"):
        connection.execute(f"DROP TRIGGER IF EXISTS {trigger}")
    if occurrences:
        connection.execute(
            "DELETE FROM events WHERE rowid IN"
            " (SELECT rowid FROM events ORDER BY rowid DESC LIMIT ?)",
            (occurrences,),
        )
    if commitments:
        connection.execute(
            "DELETE FROM event_prefix_commitments WHERE position IN"
            " (SELECT position FROM event_prefix_commitments"
            " ORDER BY position DESC LIMIT ?)",
            (commitments,),
        )
    connection.commit()
    connection.close()


def test_losing_the_tip_of_both_leaves_every_remaining_occurrence_intact(tmp_path):
    """A shorter history is still a sound one."""

    path = tmp_path / "e.sqlite"
    ledger, ids = _build(path)
    del ledger

    _lose(path, occurrences=10, commitments=10)

    ledger = SQLiteEventLedger(str(path))
    assert len(ledger.list("w")) == 40
    for event_id in ids[:40]:
        assert ledger.integrity_of(event_id) == VERIFIED


def test_occurrences_lost_without_their_commitments_refuse_to_open(tmp_path):
    """A chain longer than its occurrences is torn, not short."""

    path = tmp_path / "e.sqlite"
    ledger, _ = _build(path)
    del ledger

    _lose(path, occurrences=10)

    with pytest.raises(LedgerIntegrityError):
        SQLiteEventLedger(str(path))


def test_commitments_lost_without_their_occurrences_refuse_to_open(tmp_path):
    """And the tear in the other direction."""

    path = tmp_path / "e.sqlite"
    ledger, _ = _build(path)
    del ledger

    _lose(path, commitments=10)

    with pytest.raises(LedgerIntegrityError):
        SQLiteEventLedger(str(path))


def test_a_retained_boundary_detects_a_tip_that_was_lost(tmp_path):
    """The witness is what makes a silent shortening speak.

    Truncating both tables together leaves a store that is internally
    consistent and cannot tell, alone, that it is shorter than it was. A
    holder of a boundary captured before the loss can.
    """

    path = tmp_path / "e.sqlite"
    ledger, _ = _build(path)
    boundary = ledger.capture_boundary()
    del ledger

    _lose(path, occurrences=10, commitments=10)

    ledger = SQLiteEventLedger(str(path))
    with pytest.raises(InvalidLedgerBoundary):
        ledger.list("w", through=boundary)


def test_only_the_prefix_that_vanished_is_refused(tmp_path):
    """A ledger that refused every boundary would report loss that never happened.

    The refusal above has to be specific to the prefix the store no longer
    holds, so a boundary the surviving store can account for must resolve.
    """

    path = tmp_path / "e.sqlite"
    ledger, _ = _build(path)
    del ledger

    _lose(path, occurrences=10, commitments=10)

    ledger = SQLiteEventLedger(str(path))
    surviving = ledger.capture_boundary()
    assert len(ledger.list("w", through=surviving)) == 40

    ledger.append("k", "w", {"i": "after"}, locality_id="s1")
    assert len(ledger.list("w")) == 41
    assert len(ledger.list("w", through=surviving)) == 40


def test_a_batch_lost_whole_leaves_the_store_sound(tmp_path):
    """The failure a deferred commit can produce is the survivable one.

    Occurrences appended inside one scope are written before any of them is
    committed, so losing the scope loses all of them and leaves a chain
    accounting for exactly the ones it kept. That is the first case above, not
    either tear.
    """

    path = tmp_path / "e.sqlite"
    ledger = SQLiteEventLedger(str(path))
    kept = ledger.append("k", "w", {"i": "committed"}, locality_id="s1")

    with pytest.raises(RuntimeError):
        with ledger.batched():
            for index in range(5):
                ledger.append("k", "w", {"i": index}, locality_id="s1")
            raise RuntimeError("crash mid-batch")
    del ledger

    ledger = SQLiteEventLedger(str(path))
    surviving = ledger.list("w")
    assert [event.id for event in surviving] == [kept.id]
    assert ledger.integrity_of(kept.id) == VERIFIED

    ledger.append("k", "w", {"i": "after"}, locality_id="s1")
    assert len(ledger.list("w")) == 2


def test_a_batch_that_closes_commits_every_occurrence_in_it(tmp_path):
    """Deferring is not discarding."""

    path = tmp_path / "e.sqlite"
    ledger = SQLiteEventLedger(str(path))
    with ledger.batched():
        ids = [
            ledger.append("k", "w", {"i": index}, locality_id="s1").id
            for index in range(5)
        ]
    del ledger

    ledger = SQLiteEventLedger(str(path))
    assert [event.id for event in ledger.list("w")] == ids
    for event_id in ids:
        assert ledger.integrity_of(event_id) == VERIFIED


def test_a_flush_inside_a_batch_makes_what_preceded_it_durable(tmp_path):
    """What an act calls when it must not proceed until an occurrence is durable."""

    path = tmp_path / "e.sqlite"
    ledger = SQLiteEventLedger(str(path))
    with pytest.raises(RuntimeError):
        with ledger.batched():
            before = ledger.append("k", "w", {"i": "before"}, locality_id="s1")
            ledger.flush()
            ledger.append("k", "w", {"i": "after"}, locality_id="s1")
            raise RuntimeError("crash after the flush")
    del ledger

    ledger = SQLiteEventLedger(str(path))
    assert [event.id for event in ledger.list("w")] == [before.id]


def test_the_emission_attempt_is_durable_before_the_output_boundary(tmp_path):
    """A second reader sees the attempt at the moment the stream is written.

    Emission reaches outside Seed. An attempt still sitting in an uncommitted
    batch would let the world receive what no durable occurrence records was
    tried, and no later commit can undo having sent it.

    The reader is a separate connection, so it sees committed rows only.
    """

    from io import StringIO

    from seed_runtime.operator_console import run_persistent_operator_console

    path = tmp_path / "e.sqlite"
    ledger = SQLiteEventLedger(str(path))
    seen: list[int] = []

    class _Watching(StringIO):
        def write(self, value: str) -> int:
            reader = sqlite3.connect(str(path))
            seen.append(
                reader.execute(
                    "SELECT COUNT(*) FROM events WHERE kind = ?",
                    ("operator.representation.emission_attempted",),
                ).fetchone()[0]
            )
            reader.close()
            return super().write(value)

    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        locality_id="s1",
        input_stream=StringIO("one\ntwo\nexit\n"),
        output_stream=_Watching(),
        process_boundary_escape=False,
    )

    assert seen, "no stream write occurred"
    # The nth write is preceded by its own attempt, so at least n attempts are
    # committed by the time it happens. Without the flush this reads
    # [1, 1, 2, 3]: every write but the first reaches the boundary while its
    # own attempt is still uncommitted.
    assert seen == list(range(1, len(seen) + 1)), seen
