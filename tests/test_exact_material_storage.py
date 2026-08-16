from __future__ import annotations

from collections import Counter
import sqlite3

import pytest

import seed_runtime.events as events
from seed_runtime.events import (
    VERIFIED,
    InvalidStoredMaterial,
    LedgerIntegrityError,
    SQLiteEventLedger,
)
from seed_runtime.material_ingest import ingest_material


def _ingest(ledger, exact_material: bytes, position: int):
    return ingest_material(
        ledger,
        locality_identity="material-storage",
        exact_bytes=exact_material,
        source_role="system",
        source_boundary=f"boundary-{position}",
    )


def test_equal_material_has_one_physical_reference_and_distinct_occurrences(tmp_path):
    ledger = SQLiteEventLedger(tmp_path / "material.db")
    first_material = bytes(bytearray(b"tatatata"))
    second_material = bytes(bytearray(b"tatatata"))
    assert first_material == second_material and first_material is not second_material

    first = _ingest(ledger, first_material, 0)
    second = _ingest(ledger, second_material, 1)
    exact_occurrences = (
        ledger.get(first.material["evidence_of_yield_relation_identity"]),
        ledger.get(first.identity),
        ledger.get(second.material["evidence_of_yield_relation_identity"]),
        ledger.get(second.identity),
    )
    references = tuple(
        ledger._exact_material_reference(occurrence.identity)
        for occurrence in exact_occurrences
    )

    assert len({occurrence.identity for occurrence in exact_occurrences}) == 4
    assert Counter(references) == {references[0]: 4}
    assert ledger._read_exact_material_reference(references[0]) == b"tatatata"
    assert all(occurrence.exact_material == b"tatatata" for occurrence in exact_occurrences)
    assert all(not hasattr(occurrence, "exact_material_identity") for occurrence in exact_occurrences)
    assert {
        ledger.integrity_of(occurrence.identity)
        for occurrence in exact_occurrences
    } == {VERIFIED}
    ledger.close()

    reopened = SQLiteEventLedger(tmp_path / "material.db")
    try:
        assert Counter(
            reopened._exact_material_reference(occurrence.identity)
            for occurrence in exact_occurrences
        ) == {references[0]: 4}
        assert reopened._read_exact_material_reference(references[0]) == b"tatatata"
    finally:
        reopened.close()


def test_absent_empty_and_distinct_exact_material_have_distinct_storage(tmp_path):
    ledger = SQLiteEventLedger(tmp_path / "material.db")
    absent = ledger.append("absent")
    empty = ledger.append("empty", exact_material=b"")
    first = ledger.append("first", exact_material=b"a")
    second = ledger.append("second", exact_material=b"b")

    references = tuple(
        ledger._exact_material_reference(event.identity)
        for event in (absent, empty, first, second)
    )

    assert references[0] is None
    assert all(type(reference) is str for reference in references[1:])
    assert len(set(references[1:])) == 3
    assert ledger._read_exact_material_reference(references[1]) == b""
    assert ledger.get(absent.identity).exact_material is None
    assert ledger.get(empty.identity).exact_material == b""
    ledger.close()


def test_an_exact_material_identity_collision_is_refused_atomically(
    monkeypatch, tmp_path
):
    ledger = SQLiteEventLedger(tmp_path / "material.db")
    fixed_identity = "0" * 64
    monkeypatch.setattr(events, "_exact_material_identity", lambda exact: fixed_identity)
    first = ledger.append("first", exact_material=b"first")
    boundary = ledger.append_boundary()

    with pytest.raises(LedgerIntegrityError, match="different bytes"):
        ledger.append("second", exact_material=b"second")

    assert ledger.append_boundary() == boundary
    assert ledger.list() == [first]
    assert ledger._read_exact_material_reference(fixed_identity) == b"first"
    ledger.close()


def test_exact_material_storage_refuses_revision_and_removal(tmp_path):
    path = tmp_path / "material.db"
    ledger = SQLiteEventLedger(path)
    event = ledger.append("exact", exact_material=b"material")
    reference = ledger._exact_material_reference(event.identity)
    ledger.close()

    connection = sqlite3.connect(path)
    try:
        with pytest.raises(sqlite3.IntegrityError, match="does not revision"):
            connection.execute(
                "UPDATE event_exact_materials SET exact_material = ? "
                "WHERE material_identity = ?",
                (b"changed", reference),
            )
        with pytest.raises(sqlite3.IntegrityError, match="is not removed"):
            connection.execute(
                "DELETE FROM event_exact_materials WHERE material_identity = ?",
                (reference,),
            )
    finally:
        connection.close()


def test_changed_exact_material_is_detected_through_every_reference(tmp_path):
    path = tmp_path / "material.db"
    ledger = SQLiteEventLedger(path)
    first = ledger.append("first", exact_material=b"shared")
    second = ledger.append("second", exact_material=bytes(bytearray(b"shared")))
    reference = ledger._exact_material_reference(first.identity)
    ledger.close()

    connection = sqlite3.connect(path)
    connection.execute("DROP TRIGGER event_exact_materials_refuse_update")
    connection.execute(
        "UPDATE event_exact_materials SET exact_material = ? "
        "WHERE material_identity = ?",
        (b"changed", reference),
    )
    connection.commit()
    connection.close()

    with pytest.raises(LedgerIntegrityError, match="append-prefix identity"):
        SQLiteEventLedger(path)


def test_changed_event_pointer_is_not_a_changed_occurrence_material(tmp_path):
    path = tmp_path / "material.db"
    ledger = SQLiteEventLedger(path)
    first = ledger.append("first", exact_material=b"first")
    second = ledger.append("second", exact_material=b"second")
    first_reference = ledger._exact_material_reference(first.identity)
    second_reference = ledger._exact_material_reference(second.identity)
    ledger.close()

    connection = sqlite3.connect(path)
    connection.execute("DROP TRIGGER events_refuse_update")
    connection.execute(
        "UPDATE events SET exact_material_identity = ? WHERE identity = ?",
        (second_reference, first.identity),
    )
    connection.commit()
    connection.close()

    assert first_reference != second_reference
    with pytest.raises(LedgerIntegrityError, match="append-prefix identity"):
        SQLiteEventLedger(path)


def test_missing_exact_material_cannot_be_rehydrated_and_is_corrupted(tmp_path):
    path = tmp_path / "material.db"
    ledger = SQLiteEventLedger(path)
    event = ledger.append("exact", exact_material=b"material")
    reference = ledger._exact_material_reference(event.identity)
    ledger.close()

    connection = sqlite3.connect(path)
    connection.execute("DROP TRIGGER event_exact_materials_refuse_delete")
    connection.execute(
        "DELETE FROM event_exact_materials WHERE material_identity = ?",
        (reference,),
    )
    connection.commit()
    connection.close()

    with pytest.raises(InvalidStoredMaterial, match="not available"):
        SQLiteEventLedger(path)
