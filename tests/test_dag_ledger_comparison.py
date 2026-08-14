"""Cross-examine the durable ledger and its edge-indexed witness."""

from seed_runtime.dag_ledger_comparison import DagLedgerComparison
from seed_runtime.events import SQLiteEventLedger


def _cross_examined_stores(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "ledger.sqlite"))
    first = ledger.append("first", "w", {"value": 1}, locality_id="s")
    second = ledger.append(
        "second",
        "w",
        {"source_ref": first.id, "nested": {"source_ref": first.id}},
        locality_id="s",
    )
    third = ledger.append(
        "third",
        "w",
        {"first_ref": first.id, "second_ref": second.id},
        locality_id="s",
    )
    events = ledger.list()
    dag = DagLedgerComparison()
    dag.load(events)
    return ledger, dag, events


def test_sql_and_dag_answer_the_same_reference_relations(tmp_path):
    ledger, dag, events = _cross_examined_stores(tmp_path)

    for event in events:
        assert dag.references_from(event.id) == ledger.references_from(event.id)
        assert dag.references_to(event.id) == ledger.references_to(event.id)


def test_neither_store_turns_a_future_id_string_into_a_relation(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "future.sqlite"))
    future_id = f"evt_{ledger._next_event_number + 1:06d}"
    naming = ledger.append("naming", "w", {"source_ref": future_id}, locality_id="s")
    future = ledger.append("future", "w", {}, locality_id="s")
    assert future.id == future_id

    dag = DagLedgerComparison()
    dag.load(ledger.list())

    assert ledger.references_from(naming.id) == []
    assert dag.references_from(naming.id) == []
    assert ledger.references_to(future.id) == []
    assert dag.references_to(future.id) == []


def test_both_stores_collapse_one_repeated_reference_relation(tmp_path):
    ledger, dag, events = _cross_examined_stores(tmp_path)
    second = events[1]

    assert ledger.references_from(second.id) == [("source_ref", events[0].id)]
    assert dag.references_from(second.id) == [("source_ref", events[0].id)]


def test_both_reference_directions_use_covering_indexes(tmp_path):
    ledger, dag, events = _cross_examined_stores(tmp_path)
    target = events[0].id

    sql_plans = [
        ledger._connection.execute(
            "EXPLAIN QUERY PLAN SELECT relation, destination_id "
            "FROM event_references WHERE source_id = ? "
            "ORDER BY relation, ordinal",
            (target,),
        ).fetchall(),
        ledger._connection.execute(
            "EXPLAIN QUERY PLAN SELECT relation, source_id "
            "FROM event_references WHERE destination_id = ? "
            "ORDER BY relation, source_id",
            (target,),
        ).fetchall(),
    ]
    dag_plans = [
        dag._connection.execute(
            "EXPLAIN QUERY PLAN SELECT relation, destination_id "
            "FROM edges WHERE source_id = ? ORDER BY relation, ordinal",
            (target,),
        ).fetchall(),
        dag._connection.execute(
            "EXPLAIN QUERY PLAN SELECT relation, source_id "
            "FROM edges WHERE destination_id = ? ORDER BY relation, source_id",
            (target,),
        ).fetchall(),
    ]

    for plan in (*sql_plans, *dag_plans):
        assert any("COVERING INDEX" in row[-1] for row in plan), plan
