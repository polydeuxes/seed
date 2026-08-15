"""The occurrence references the ledger indexes, in both directions."""

from __future__ import annotations

import json
from tests.binary_input import binary_input
from io import StringIO

from seed_runtime.events import SQLiteEventLedger, _payload_references
from seed_runtime.operator_console import run_persistent_operator_console


def _road(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    run_persistent_operator_console(
        ledger=ledger,
        locality_id="s1",
        input_stream=binary_input("the cat sat\nthe cat ran\n"),
        output_stream=StringIO(),
    )
    return ledger


def test_the_index_restates_only_references_the_payload_carries(tmp_path):
    """Every indexed edge is readable back out of the payload it came from."""

    ledger = _road(tmp_path)
    rows = [
        tuple(row)
        for row in ledger._connection.execute(
            "SELECT source_id, relation, destination_id FROM event_references"
        )
    ]
    assert rows

    for source_id, relation, destination_id in rows:
        payload = ledger.get(source_id).payload
        carried = json.dumps(payload, default=str)
        assert destination_id in carried, (
            f"{source_id} is indexed as referencing {destination_id} under "
            f"{relation}, and its payload does not carry that id"
        )


def _rebuild(ledger) -> set[tuple[str, str, str]]:
    """The index recomputed from the payloads, in the order they occurred.

    Occurrence order is part of the rebuild, not a detail of it. An occurrence
    may only reference one that already existed, so a rebuild consulting every
    id present now would credit relations to payloads written before their
    destination occurred.
    """

    rebuilt: set[tuple[str, str, str]] = set()
    existing: set[str] = set()
    for row in ledger._connection.execute("SELECT id FROM events ORDER BY rowid"):
        event = ledger.get(row[0])
        for relation, destination, _ in dict.fromkeys(
            _payload_references(event.payload)
        ):
            if destination in existing:
                rebuilt.add((event.id, relation, destination))
        existing.add(event.id)
    return rebuilt


def _stored(ledger) -> set[tuple[str, str, str]]:
    return {
        tuple(row)
        for row in ledger._connection.execute(
            "SELECT source_id, relation, destination_id FROM event_references"
        )
    }


def test_the_index_is_rebuildable_from_the_payloads_it_indexes(tmp_path):
    """Mechanics, not testimony: discarding it loses nothing.

    The payload stays the authority. If the index could hold a relation the
    payloads do not, it would be a second record able to disagree with the
    first, and dropping it would lose an Assertion.
    """

    ledger = _road(tmp_path)
    assert _stored(ledger) == _rebuild(ledger)


def test_naming_an_id_before_its_occurrence_is_not_a_reference(tmp_path):
    """Co-presence does not establish the relation.

    A payload may hold a string that later becomes some occurrence's exact id.
    `grammar.json` holds that endpoint presence does not establish a relation,
    and `02.Standing:55` that co-presence does not establish participation. An
    occurrence that could not have referenced its destination did not.

    Read it the other way would also let a caller name an id it has not seen
    and acquire an edge to whatever later takes that id.
    """

    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    naming = ledger.append("k", {"points_at": "evt_000002"}, locality_id="s1")
    taking = ledger.append("k", {"i": 2}, locality_id="s1")

    assert taking.id == "evt_000002"
    assert ledger.references_to(taking.id) == []
    assert ledger.references_from(naming.id) == []
    assert "evt_000002" in json.dumps(ledger.get(naming.id).payload)


def test_the_rebuild_agrees_with_the_index_across_that_case(tmp_path):
    """The invariant has to survive the case that exposed it."""

    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    ledger.append("k", {"points_at": "evt_000002"}, locality_id="s1")
    second = ledger.append("k", {"i": 2}, locality_id="s1")
    ledger.append("k", {"points_at": second.id}, locality_id="s1")

    assert _stored(ledger) == _rebuild(ledger)
    assert len(_stored(ledger)) == 1


def test_one_reference_restated_in_one_payload_is_indexed_once(tmp_path):
    """A relation held twice in one payload is one relation."""

    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    first = ledger.append("k", {"n": 1}, locality_id="s1")
    ledger.append(
        "k",
        {"here": first.id, "and_again": {"here": first.id}},
        locality_id="s1",
    )

    assert ledger.references_to(first.id) == [("here", ledger.list_locality("s1")[1].id)]


def test_references_to_answers_what_the_payload_column_cannot(tmp_path):
    """The direction the index exists for."""

    ledger = _road(tmp_path)
    ingest = [
        event
        for event in ledger.list_locality("s1")
        if event.kind == "material.ingest.occurred"
    ]
    assert ingest

    referrers = ledger.references_to(ingest[0].id)
    assert referrers
    for relation, source in referrers:
        assert ingest[0].id in json.dumps(ledger.get(source).payload, default=str)
        assert relation


def test_an_unresolvable_id_shaped_string_is_not_an_edge(tmp_path):
    """An edge requires an occurrence, not a string that looks like one."""

    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    ledger.append("k", {"points_at": "evt_999999"}, locality_id="s1")

    assert ledger.references_to("evt_999999") == []
