"""What a durable ledger can and cannot lose without saying so.

Losing the tip and corrupting lineage are different failures. A store that
lost its last occurrences still returns every result the remaining ones
support. A store whose chain no longer matches its occurrences returns
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
    identities = [
        ledger.append("k", {"i": i}, locality_identity="s1").identity for i in range(count)
    ]
    return ledger, identities


def _lose(path, *, occurrences=0, identities=0):
    """Drop the tail of either table, as an unflushed write would."""

    connection = sqlite3.connect(str(path))
    for trigger in ("events_refuse_delete", "prefix_identities_refuse_delete"):
        connection.execute(f"DROP TRIGGER IF EXISTS {trigger}")
    if occurrences:
        connection.execute(
            "DELETE FROM events WHERE rowid IN"
            " (SELECT rowid FROM events ORDER BY rowid DESC LIMIT ?)",
            (occurrences,),
        )
    if identities:
        connection.execute(
            "DELETE FROM event_prefix_identities WHERE position IN"
            " (SELECT position FROM event_prefix_identities"
            " ORDER BY position DESC LIMIT ?)",
            (identities,),
        )
    connection.commit()
    connection.close()


def test_losing_the_tip_of_both_leaves_every_remaining_occurrence_intact(tmp_path):
    """A shorter history is still a sound one."""

    path = tmp_path / "e.sqlite"
    ledger, identities = _build(path)
    del ledger

    _lose(path, occurrences=10, identities=10)

    ledger = SQLiteEventLedger(str(path))
    assert len(ledger.list()) == 40
    for event_identity in identities[:40]:
        assert ledger.integrity_of(event_identity) == VERIFIED


def test_occurrences_lost_without_their_prefix_identities_refuse_to_open(tmp_path):
    """A chain longer than its occurrences is torn, not short."""

    path = tmp_path / "e.sqlite"
    ledger, _ = _build(path)
    del ledger

    _lose(path, occurrences=10)

    with pytest.raises(LedgerIntegrityError):
        SQLiteEventLedger(str(path))


def test_prefix_identities_lost_without_their_occurrences_refuse_to_open(tmp_path):
    """And the tear in the other direction."""

    path = tmp_path / "e.sqlite"
    ledger, _ = _build(path)
    del ledger

    _lose(path, identities=10)

    with pytest.raises(LedgerIntegrityError):
        SQLiteEventLedger(str(path))


def test_a_retained_boundary_detects_a_tip_that_was_lost(tmp_path):
    """The witness is what makes a silent shortening speak.

    Truncating both tables together leaves a store that is internally
    consistent and cannot tell, alone, that it is shorter than it was. A
    holder of a boundary recorded before the loss can.
    """

    path = tmp_path / "e.sqlite"
    ledger, _ = _build(path)
    boundary = ledger.append_boundary()
    del ledger

    _lose(path, occurrences=10, identities=10)

    ledger = SQLiteEventLedger(str(path))
    with pytest.raises(InvalidLedgerBoundary):
        ledger.list(through=boundary)


def test_only_the_prefix_that_vanished_is_refused(tmp_path):
    """A ledger that refused every boundary would report loss that never happened.

    The refusal above has to be specific to the prefix the store no longer
    holds, so a boundary the surviving store can account for must resolve.
    """

    path = tmp_path / "e.sqlite"
    ledger, _ = _build(path)
    del ledger

    _lose(path, occurrences=10, identities=10)

    ledger = SQLiteEventLedger(str(path))
    surviving = ledger.append_boundary()
    assert len(ledger.list(through=surviving)) == 40

    ledger.append("k", {"i": "after"}, locality_identity="s1")
    assert len(ledger.list()) == 41
    assert len(ledger.list(through=surviving)) == 40


def test_a_batch_lost_whole_leaves_the_store_sound(tmp_path):
    """The failure a deferred commit can produce is the survivable one.

    Occurrences appended inside one scope are written before any of them is
    committed, so losing the scope loses all of them and leaves a chain
    accounting for exactly the ones it kept. That is the first case above, not
    either tear.
    """

    path = tmp_path / "e.sqlite"
    ledger = SQLiteEventLedger(str(path))
    kept = ledger.append("k", {"i": "committed"}, locality_identity="s1")

    with pytest.raises(RuntimeError):
        with ledger.batched():
            for index in range(5):
                ledger.append("k", {"i": index}, locality_identity="s1")
            raise RuntimeError("crash mid-batch")
    del ledger

    ledger = SQLiteEventLedger(str(path))
    surviving = ledger.list()
    assert [event.identity for event in surviving] == [kept.identity]
    assert ledger.integrity_of(kept.identity) == VERIFIED

    ledger.append("k", {"i": "after"}, locality_identity="s1")
    assert len(ledger.list()) == 2


def test_a_batch_that_closes_commits_every_occurrence_in_it(tmp_path):
    """Deferring is not discarding."""

    path = tmp_path / "e.sqlite"
    ledger = SQLiteEventLedger(str(path))
    with ledger.batched():
        identities = [
            ledger.append("k", {"i": index}, locality_identity="s1").identity
            for index in range(5)
        ]
    del ledger

    ledger = SQLiteEventLedger(str(path))
    assert [event.identity for event in ledger.list()] == identities
    for event_identity in identities:
        assert ledger.integrity_of(event_identity) == VERIFIED


def test_a_flush_inside_a_batch_makes_what_preceded_it_durable(tmp_path):
    """What an act calls when it must not proceed until an occurrence is durable."""

    path = tmp_path / "e.sqlite"
    ledger = SQLiteEventLedger(str(path))
    with pytest.raises(RuntimeError):
        with ledger.batched():
            before = ledger.append("k", {"i": "before"}, locality_identity="s1")
            ledger.flush()
            ledger.append("k", {"i": "after"}, locality_identity="s1")
            raise RuntimeError("crash after the flush")
    del ledger

    ledger = SQLiteEventLedger(str(path))
    assert [event.identity for event in ledger.list()] == [before.identity]


def test_the_emission_attempt_is_durable_before_the_output_boundary(tmp_path):
    """A second reader sees the attempt at the moment the stream is written.

    Emission reaches outside Seed. An attempt still sitting in an uncommitted
    batch would let the world receive what no durable occurrence records was
    tried, and no later commit can undo having sent it.

    The reader is a separate connection, so it sees committed rows only.
    """

    from io import StringIO

    from seed_runtime.operator_console import run_persistent_operator_console
    from tests.binary_input import binary_input

    path = tmp_path / "e.sqlite"
    ledger = SQLiteEventLedger(str(path))
    seen: list[int] = []

    class _Watching(StringIO):
        def write(self, value: str) -> int:
            reader = sqlite3.connect(str(path))
            seen.append(
                reader.execute(
                    "SELECT COUNT(*) FROM events WHERE kind = ?",
                    ("operator.representation.emission_attempt_recorded",),
                ).fetchone()[0]
            )
            reader.close()
            return super().write(value)

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s1",
        input_stream=binary_input("one\ntwo\n"),
        output_stream=_Watching(),
    )

    assert seen, "no stream write occurred"
    # The nth write is preceded by its own attempt, so at least n attempts are
    # committed by the time it happens. Without the flush this reads
    # [1, 1, 2, 3]: every write but the first reaches the boundary while its
    # own attempt is still uncommitted.
    assert seen == list(range(1, len(seen) + 1)), seen


def test_the_exact_material_attempt_is_durable_before_raw_egress(tmp_path):
    """The byte road exposes no material before its exact attempt is durable."""

    from io import BytesIO

    from seed_runtime.material_ingest import ingest_material
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )
    from seed_runtime.operator_representation import (
        emit_operator_representation_material,
        record_operator_representation,
    )

    path = tmp_path / "raw.sqlite"
    ledger = SQLiteEventLedger(str(path))
    source = ingest_material(
        ledger,
        locality_identity="s1",
        exact_bytes=b"\x00\xffexact",
        source_role="fixture material",
        source_boundary="fixture boundary",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="s1"
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="s1",
        locality_standing=standing,
        source_event_identity=source.identity,
    )
    seen: list[int] = []

    class _Watching(BytesIO):
        def write(self, value: bytes) -> int:
            reader = sqlite3.connect(str(path))
            seen.append(
                reader.execute(
                    "SELECT COUNT(*) FROM events WHERE kind = ?",
                    ("operator.representation.emission_attempt_recorded",),
                ).fetchone()[0]
            )
            reader.close()
            return super().write(value)

    output = _Watching()
    emit_operator_representation_material(
        ledger,
        representation=representation,
        output_stream=output,
    )

    assert seen == [1]
    assert output.getvalue() == source.exact_material
