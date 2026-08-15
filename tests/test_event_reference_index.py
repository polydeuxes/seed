"""The occurrence references the ledger indexes, in both directions."""

from __future__ import annotations

import json
from tests.binary_input import binary_input
from io import StringIO

from seed_runtime.events import SQLiteEventLedger, _material_references
from seed_runtime.operator_console import run_persistent_operator_console


def _road(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s1",
        input_stream=binary_input("the cat sat\nthe cat ran\n"),
        output_stream=StringIO(),
    )
    return ledger


def test_the_index_restates_only_references_the_material_carries(tmp_path):
    """Every indexed reference pair is readable from its material."""

    ledger = _road(tmp_path)
    rows = [
        tuple(row)
        for row in ledger._connection.execute(
            "SELECT source_identity, relation, destination_identity FROM event_references"
        )
    ]
    assert rows

    for source_identity, relation, destination_identity in rows:
        material = ledger.get(source_identity).material
        carried = json.dumps(material, default=str)
        assert destination_identity in carried, (
            f"{source_identity} is indexed as referencing {destination_identity} under "
            f"{relation}, and its material does not carry that identity"
        )


def _rebuild(ledger) -> set[tuple[str, str, str]]:
    """The index recomputed from the materials, in the order they occurred.

    Occurrence order is part of the rebuild, not a detail of it. An occurrence
    may only reference one that already existed, so a rebuild consulting every
    identity present now would credit relations to materials written before their
    destination occurred.
    """

    rebuilt: set[tuple[str, str, str]] = set()
    existing: set[str] = set()
    for row in ledger._connection.execute("SELECT identity FROM events ORDER BY rowid"):
        event = ledger.get(row[0])
        for relation, destination, _ in dict.fromkeys(
            _material_references(event.material)
        ):
            if destination in existing:
                rebuilt.add((event.identity, relation, destination))
        existing.add(event.identity)
    return rebuilt


def _stored(ledger) -> set[tuple[str, str, str]]:
    return {
        tuple(row)
        for row in ledger._connection.execute(
            "SELECT source_identity, relation, destination_identity FROM event_references"
        )
    }


def test_the_index_is_rebuildable_from_the_materials_it_indexes(tmp_path):
    """Mechanics, not testimony: discarding it loses nothing.

    The material stays the authority. If the index could hold a relation the
    materials do not, it would be a second record able to disagree with the
    first, and dropping it would lose an Assertion.
    """

    ledger = _road(tmp_path)
    assert _stored(ledger) == _rebuild(ledger)


def test_naming_an_identity_before_its_occurrence_is_not_a_reference(tmp_path):
    """Co-presence does not establish the relation.

    A material may hold a string that later becomes some occurrence's exact identity.
    `grammar.json` holds that endpoint presence does not establish a relation,
    and `02.Standing:55` that co-presence does not establish participation. An
    occurrence that could not have referenced its destination did not.

    Read it the other way would also let a caller name an identity it has not seen
    and acquire a reference to whatever later takes that identity.
    """

    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    naming = ledger.append("k", {"points_at": "evt_000002"}, locality_identity="s1")
    taking = ledger.append("k", {"i": 2}, locality_identity="s1")

    assert taking.identity == "evt_000002"
    assert ledger.references_to(taking.identity) == []
    assert ledger.references_from(naming.identity) == []
    assert "evt_000002" in json.dumps(ledger.get(naming.identity).material)


def test_the_rebuild_agrees_with_the_index_across_that_case(tmp_path):
    """The invariant has to survive the case that exposed it."""

    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    ledger.append("k", {"points_at": "evt_000002"}, locality_identity="s1")
    second = ledger.append("k", {"i": 2}, locality_identity="s1")
    ledger.append("k", {"points_at": second.identity}, locality_identity="s1")

    assert _stored(ledger) == _rebuild(ledger)
    assert len(_stored(ledger)) == 1


def test_one_reference_restated_in_one_material_is_indexed_once(tmp_path):
    """A relation held twice in one material is one relation."""

    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    first = ledger.append("k", {"n": 1}, locality_identity="s1")
    ledger.append(
        "k",
        {"here": first.identity, "and_again": {"here": first.identity}},
        locality_identity="s1",
    )

    assert ledger.references_to(first.identity) == [("here", ledger.list_locality("s1")[1].identity)]


def test_references_to_answers_what_the_material_column_cannot(tmp_path):
    """The direction the index exists for."""

    ledger = _road(tmp_path)
    ingest = [
        event
        for event in ledger.list_locality("s1")
        if event.kind == "material.ingest.occurred"
    ]
    assert ingest

    referrers = ledger.references_to(ingest[0].identity)
    assert referrers
    for relation, source in referrers:
        assert ingest[0].identity in json.dumps(ledger.get(source).material, default=str)
        assert relation


def test_an_unresolvable_identity_shaped_string_is_not_a_reference(tmp_path):
    """A reference requires an occurrence, not a string that looks like one."""

    ledger = SQLiteEventLedger(str(tmp_path / "e.sqlite"))
    ledger.append("k", {"points_at": "evt_999999"}, locality_identity="s1")

    assert ledger.references_to("evt_999999") == []
