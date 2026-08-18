import json
from pathlib import Path
import sqlite3

import pytest

from scripts.reference_pair_comparison import ReferencePairComparison
from seed_runtime.events import EventLedgerBoundary, SQLiteEventLedger


def _cross_examined_store(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "ledger.sqlite"))
    first = ledger.append("first", {"value": 1}, locality_identity="s")
    second = ledger.append(
        "second",
        {
            "source_reference": first.identity,
            "nested": {"source_reference": first.identity},
        },
        locality_identity="s",
    )
    third = ledger.append(
        "third",
        {
            "first_reference": first.identity,
            "second_reference": second.identity,
        },
        locality_identity="s",
    )
    boundary = ledger.append_boundary()
    comparison = ReferencePairComparison()
    comparison.load(ledger, through=boundary)
    return ledger, comparison, (first, second, third), boundary


def test_bounded_comparison_reads_both_reference_directions(tmp_path):
    _, comparison, events, _ = _cross_examined_store(tmp_path)
    first, second, third = events

    assert comparison.references_from(first.identity) == []
    assert comparison.references_from(second.identity) == [
        ("source_reference", first.identity)
    ]
    assert comparison.references_from(third.identity) == [
        ("first_reference", first.identity),
        ("second_reference", second.identity),
    ]
    assert comparison.references_to(first.identity) == [
        ("first_reference", third.identity),
        ("source_reference", second.identity),
    ]


def test_bounded_comparison_does_not_turn_a_future_name_into_a_relation(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "future.sqlite"))
    future_identity = f"evt_{ledger._next_event_number + 1:06d}"
    naming = ledger.append("naming", {"source_reference": future_identity})
    future = ledger.append("future", {})
    assert future.identity == future_identity
    comparison = ReferencePairComparison()

    comparison.load(ledger, through=ledger.append_boundary())

    assert comparison.references_from(naming.identity) == []
    assert comparison.references_to(future.identity) == []


def test_one_repeated_reference_relation_is_collected_once(tmp_path):
    _, comparison, events, _ = _cross_examined_store(tmp_path)
    assert comparison.references_from(events[1].identity) == [
        ("source_reference", events[0].identity)
    ]
    grammar = json.loads(
        (Path(__file__).resolve().parents[1] / "book_of_seed/grammar.json").read_text(
            encoding="utf-8"
        )
    )
    assert grammar["clause_coordinates"]["01.Source.D.1"][
        "repeated_reference_to_one_occurrence"
    ] == {
        "standing_not_established": [
            {
                "first_subject": "repeated_reference_to_one_occurrence",
                "relation": "create",
                "second_subject": "another_occurrence",
                "standing": "not_established",
            },
            {
                "first_subject": "repeated_reference_to_one_occurrence",
                "relation": "establishes",
                "second_subject": "another_occurrence_reference_in_count_finding",
                "standing": "not_established",
            },
        ]
    }


def test_collection_stays_at_its_exact_boundary_after_the_ledger_advances(tmp_path):
    ledger, comparison, events, boundary = _cross_examined_store(tmp_path)
    later = ledger.append(
        "later", {"source_reference": events[0].identity}, locality_identity="s"
    )
    pair_count = comparison.load(ledger, through=boundary)

    assert pair_count == 3
    assert comparison.references_from(later.identity) == []
    assert comparison._connection.execute(
        "SELECT identity FROM collection_boundary"
    ).fetchone()[0] == boundary.identity


def test_persisted_collection_refuses_a_different_boundary(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "ledger.sqlite"))
    ledger.append("first")
    first_boundary = ledger.append_boundary()
    path = str(tmp_path / "comparison.sqlite")
    ReferencePairComparison(path).load(ledger, through=first_boundary)
    ledger.append("second")

    reopened = ReferencePairComparison(path)
    with pytest.raises(ValueError, match="different boundaries"):
        reopened.load(ledger, through=ledger.append_boundary())

    assert reopened._connection.execute(
        "SELECT identity FROM collection_boundary"
    ).fetchone()[0] == first_boundary.identity


def test_load_requires_the_ledger_and_exact_boundary(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "ledger.sqlite"))
    boundary = ledger.append_boundary()
    comparison = ReferencePairComparison()

    with pytest.raises(TypeError, match="EventLedger"):
        comparison.load([], through=boundary)
    with pytest.raises(TypeError, match="exact boundary"):
        comparison.load(ledger, through=object())
    with pytest.raises(TypeError, match="exact boundary"):
        comparison.load(
            ledger,
            through=type("BoundarySubclass", (EventLedgerBoundary,), {})(
                boundary.identity
            ),
        )


def test_unbounded_legacy_comparison_is_refused(tmp_path):
    path = str(tmp_path / "comparison.sqlite")
    connection = sqlite3.connect(path)
    connection.execute("CREATE TABLE occurrences (identity TEXT)")
    connection.execute("INSERT INTO occurrences VALUES ('unbounded')")
    connection.commit()
    connection.close()

    ledger = SQLiteEventLedger(str(tmp_path / "ledger.sqlite"))
    with pytest.raises(ValueError, match="without their exact collection boundary"):
        ReferencePairComparison(path).load(
            ledger, through=ledger.append_boundary()
        )


def test_reference_directions_use_covering_indexes(tmp_path):
    _, comparison, events, _ = _cross_examined_store(tmp_path)
    target = events[0].identity
    plans = [
        comparison._connection.execute(
            "EXPLAIN QUERY PLAN SELECT relation, destination_identity "
            "FROM reference_pairs WHERE source_identity = ? "
            "ORDER BY relation, position",
            (target,),
        ).fetchall(),
        comparison._connection.execute(
            "EXPLAIN QUERY PLAN SELECT relation, source_identity "
            "FROM reference_pairs WHERE destination_identity = ? "
            "ORDER BY relation, source_identity",
            (target,),
        ).fetchall(),
    ]

    for plan in plans:
        assert any("COVERING INDEX" in row[-1] for row in plan), plan


FIDELITY_SUBJECTS = {
    "reference_pair_comparison": (
        test_bounded_comparison_reads_both_reference_directions,
    ),
    "later_reference_relation_distinction": (
        test_bounded_comparison_does_not_turn_a_future_name_into_a_relation,
    ),
    "repeated_reference_relation": (
        test_one_repeated_reference_relation_is_collected_once,
    ),
    "reference_collection_boundary": (
        test_collection_stays_at_its_exact_boundary_after_the_ledger_advances,
    ),
    "persistent_reference_collection_boundary": (
        test_persisted_collection_refuses_a_different_boundary,
    ),
    "reference_collection_exact_boundary": (
        test_load_requires_the_ledger_and_exact_boundary,
    ),
    "reference_collection_without_boundary_refusal": (
        test_unbounded_legacy_comparison_is_refused,
    ),
    "reference_indexing": (test_reference_directions_use_covering_indexes,),
}
