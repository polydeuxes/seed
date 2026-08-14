"""The occurrence references the ledger indexes, in both directions."""

from __future__ import annotations

import json
from io import StringIO

from seed_runtime.events import SQLiteEventLedger, _payload_references
from seed_runtime.operator_console import run_persistent_operator_console


def _road(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        locality_id="s1",
        input_stream=StringIO("the cat sat\nthe cat ran\nexit\n"),
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


def test_the_index_is_rebuildable_from_the_payloads_it_indexes(tmp_path):
    """Mechanics, not testimony: discarding it loses nothing.

    The payload stays the authority. If the index could hold a relation the
    payloads do not, it would be a second record able to disagree with the
    first, and dropping it would lose an Assertion.
    """

    ledger = _road(tmp_path)
    stored = {
        tuple(row)
        for row in ledger._connection.execute(
            "SELECT source_id, relation, destination_id FROM event_references"
        )
    }

    rebuilt = set()
    for row in ledger._connection.execute("SELECT id FROM events"):
        event = ledger.get(row[0])
        known = {
            other[0] for other in ledger._connection.execute("SELECT id FROM events")
        }
        for relation, destination, _ in dict.fromkeys(
            _payload_references(event.payload)
        ):
            if destination in known:
                rebuilt.add((event.id, relation, destination))

    assert stored == rebuilt


def test_one_reference_restated_in_one_payload_is_indexed_once(tmp_path):
    """A relation held twice in one payload is one relation."""

    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    first = ledger.append("k", "w", {"n": 1}, locality_id="s1")
    ledger.append(
        "k",
        "w",
        {"here": first.id, "and_again": {"here": first.id}},
        locality_id="s1",
    )

    assert ledger.references_to(first.id) == [("here", ledger.list_locality("w", "s1")[1].id)]


def test_references_to_answers_what_the_payload_column_cannot(tmp_path):
    """The direction the index exists for."""

    ledger = _road(tmp_path)
    ingress = [
        event
        for event in ledger.list_locality("w", "s1")
        if event.kind.endswith("raw_material_captured")
    ]
    assert ingress

    referrers = ledger.references_to(ingress[0].id)
    assert referrers
    for relation, source in referrers:
        assert ingress[0].id in json.dumps(ledger.get(source).payload, default=str)
        assert relation


def test_an_unresolvable_id_shaped_string_is_not_an_edge(tmp_path):
    """An edge requires an occurrence, not a string that looks like one."""

    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    ledger.append("k", "w", {"points_at": "evt_999999"}, locality_id="s1")

    assert ledger.references_to("evt_999999") == []
