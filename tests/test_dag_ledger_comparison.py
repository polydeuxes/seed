"""Cross-examine the durable ledger and its reference-pair witness."""

from seed_runtime.dag_ledger_comparison import DagLedgerComparison
from seed_runtime.events import SQLiteEventLedger


def _cross_examined_stores(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "ledger.sqlite"))
    first = ledger.append("first", {"value": 1}, locality_identity="s")
    second = ledger.append(
        "second",
        {"source_reference": first.identity, "nested": {"source_reference": first.identity}},
        locality_identity="s",
    )
    third = ledger.append(
        "third",
        {"first_reference": first.identity, "second_reference": second.identity},
        locality_identity="s",
    )
    events = ledger.list()
    dag = DagLedgerComparison()
    dag.load(events)
    return ledger, dag, events


def test_sql_and_dag_answer_the_same_reference_relations(tmp_path):
    ledger, dag, events = _cross_examined_stores(tmp_path)

    for event in events:
        assert dag.references_from(event.identity) == ledger.references_from(event.identity)
        assert dag.references_to(event.identity) == ledger.references_to(event.identity)


def test_neither_store_turns_a_future_identity_string_into_a_relation(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "future.sqlite"))
    future_identity = f"evt_{ledger._next_event_number + 1:06d}"
    naming = ledger.append("naming", {"source_reference": future_identity}, locality_identity="s")
    future = ledger.append("future", {}, locality_identity="s")
    assert future.identity == future_identity

    dag = DagLedgerComparison()
    dag.load(ledger.list())

    assert ledger.references_from(naming.identity) == []
    assert dag.references_from(naming.identity) == []
    assert ledger.references_to(future.identity) == []
    assert dag.references_to(future.identity) == []


def test_both_stores_collapse_one_repeated_reference_relation(tmp_path):
    ledger, dag, events = _cross_examined_stores(tmp_path)
    second = events[1]

    assert ledger.references_from(second.identity) == [("source_reference", events[0].identity)]
    assert dag.references_from(second.identity) == [("source_reference", events[0].identity)]


def test_both_reference_directions_use_covering_indexes(tmp_path):
    ledger, dag, events = _cross_examined_stores(tmp_path)
    target = events[0].identity

    sql_plans = [
        ledger._connection.execute(
            "EXPLAIN QUERY PLAN SELECT relation, destination_identity "
            "FROM event_references WHERE source_identity = ? "
            "ORDER BY relation, ordinal",
            (target,),
        ).fetchall(),
        ledger._connection.execute(
            "EXPLAIN QUERY PLAN SELECT relation, source_identity "
            "FROM event_references WHERE destination_identity = ? "
            "ORDER BY relation, source_identity",
            (target,),
        ).fetchall(),
    ]
    dag_plans = [
        dag._connection.execute(
            "EXPLAIN QUERY PLAN SELECT relation, destination_identity "
            "FROM reference_pairs WHERE source_identity = ? ORDER BY relation, ordinal",
            (target,),
        ).fetchall(),
        dag._connection.execute(
            "EXPLAIN QUERY PLAN SELECT relation, source_identity "
            "FROM reference_pairs WHERE destination_identity = ? ORDER BY relation, source_identity",
            (target,),
        ).fetchall(),
    ]

    for plan in (*sql_plans, *dag_plans):
        assert any("COVERING INDEX" in row[-1] for row in plan), plan
