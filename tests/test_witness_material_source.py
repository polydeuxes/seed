"""This Witness preserves exact supplied material and boundary results."""

from __future__ import annotations

import sqlite3

import pytest


from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.material_source import (
    MaterialSourceError,
    exact_material_result_bytes,
    read_exact_material_result,
)
from seed_runtime.witness_material_source import (
    WITNESS_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
    WitnessMaterialSourceError,
    record_witness_material_source,
)
from seed_runtime.yield_relation import RECORDED_YIELD_RELATION_EVENT


def _preserve(ledger, material=b"a.txt\nb.txt\n", **differences):
    fields = {
        "locality_identity": "locality_000001",
        "exact_bytes": material,
        "source_boundary": "source boundary",
    }
    fields.update(differences)
    return record_witness_material_source(ledger, **fields)


def test_source_result_preserves_each_exact_byte_value_without_interpretation():
    ledger = EventLedger()
    exact = bytes(range(256)) * 3

    occurred = _preserve(ledger, exact)

    assert occurred.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND
    assert occurred.locality_identity == "locality_000001"
    assert exact_material_result_bytes(occurred) == exact
    assert occurred.locality_identity == "locality_000001"
    assert "locality_relation" not in occurred.material


def test_source_result_preserves_exact_external_invocation_boundary_outcomes():
    ledger = EventLedger()
    occurred = _preserve(
        ledger,
        b"partial output",
        time_boundary_reached=True,
        output_byte_count_boundary_reached=False,
        error_byte_count_boundary_reached=True,
    )

    assert read_exact_material_result(ledger, occurred.identity) == occurred
    assert occurred.material["time_boundary_reached"] is True
    assert occurred.material["output_byte_count_boundary_reached"] is False
    assert occurred.material["error_byte_count_boundary_reached"] is True


def test_material_source_preserves_only_exact_intact_source_occurrence_references():
    class CorruptedReferenceLedger(EventLedger):
        corrupted = None

        def integrity_of(self, event_identity):
            if event_identity == self.corrupted:
                return CORRUPTED
            return super().integrity_of(event_identity)

    ledger = CorruptedReferenceLedger()
    source = _preserve(ledger, b"source")
    occurred = _preserve(
        ledger,
        b"result",
        source_occurrence_references=(source.identity,),
    )

    assert occurred.material["source_occurrence_references"] == [
        source.identity
    ]

    before = len(ledger.list())
    with pytest.raises(WitnessMaterialSourceError, match="exact intact occurrence"):
        _preserve(
            ledger,
            b"missing",
            source_occurrence_references=("missing",),
        )
    assert len(ledger.list()) == before

    ledger.corrupted = source.identity
    with pytest.raises(WitnessMaterialSourceError, match="exact intact occurrence"):
        _preserve(
            ledger,
            b"corrupted",
            source_occurrence_references=(source.identity,),
        )


def test_durable_witness_source_preserves_raw_material_and_exact_act(tmp_path):
    path = str(tmp_path / "material.db")
    exact = b"\x00\xffraw material\n"
    ledger = SQLiteEventLedger(path)
    occurred = _preserve(ledger, exact)
    act_occurrence_identity = occurred.material["act_occurrence_event_identity"]
    occurred_identity = occurred.identity
    ledger.close()

    connection = sqlite3.connect(path)
    stored = connection.execute(
        "SELECT event_exact_materials.exact_material, "
        "typeof(event_exact_materials.exact_material) FROM events "
        "JOIN event_exact_materials ON event_exact_materials.material_identity = "
        "events.exact_material_identity WHERE events.identity = ?",
        (occurred_identity,),
    ).fetchone()
    connection.close()
    assert stored == (exact, "blob")

    reopened = SQLiteEventLedger(path)
    try:
        read = read_exact_material_result(reopened, occurred_identity)
        act_occurrence = reopened.get(act_occurrence_identity)
        assert act_occurrence is not None
        assert read.exact_material == exact
        assert "yield_relation_identity" not in read.material
    finally:
        reopened.close()


def test_witness_material_source_fixes_its_exact_source_subject():
    ledger = EventLedger()
    occurred = _preserve(ledger)

    assert occurred.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND
    reference = occurred.material["subject_to_act_binding_reference"]
    binding = ledger.get(reference["recorded_occurrence_identity"])
    act_occurrence = ledger.get(
        occurred.material["act_occurrence_event_identity"]
    )
    assert binding is not None and act_occurrence is not None
    assert binding.kind == (
        WITNESS_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    )
    assert binding.material["subject_reference"] == {
        "source_boundary": "source boundary",
    }
    assert tuple(sorted(binding.material)) == (
        "act",
        "act_occurrence_identity",
        "book_clause_identity",
        "exact_act_identity",
        "result_identity",
        "subject_reference",
    )
    assert "result_identity" not in reference
    assert binding.material["result_identity"] == occurred.material["result_identity"]
    assert act_occurrence.material[
        "subject_to_act_binding_reference"
    ] == reference
    assert [
        event.identity
        for event in ledger.occurrences_in_append_order(
            (
                binding.identity,
                act_occurrence.identity,
                occurred.identity,
            ),
            locality_identity=occurred.locality_identity,
        )
    ] == [
        binding.identity,
        act_occurrence.identity,
        occurred.identity,
    ]


def test_witness_material_result_preserves_source_occurrences_and_locality():
    ledger = EventLedger()
    command = ledger.append(
        "operator.command.recorded",
        {"command": "cat"},
        locality_identity="operator-locality",
    )

    occurred = _preserve(
        ledger,
        b"hello",
        locality_identity="invocation-locality",
        source_boundary="stdout",
        source_occurrence_references=(command.identity,),
    )

    assert occurred.locality_identity == "invocation-locality"
    assert occurred.exact_material == b"hello"
    assert occurred.material["source_boundary"] == "stdout"
    assert occurred.material["source_occurrence_references"] == [
        command.identity
    ]
    assert read_exact_material_result(ledger, occurred.identity) == occurred
    assert not any(
        event.exact_material == b"hello"
        for event in ledger.list_locality("operator-locality")
    )


def test_witness_material_result_refuses_a_mismatched_locality():
    ledger = EventLedger()
    occurred = _preserve(ledger, b"hello")
    forged = ledger.append(
        WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
        dict(occurred.material),
        exact_material=occurred.exact_material,
        locality_identity="another-locality",
    )

    with pytest.raises(MaterialSourceError, match="absent or corrupted"):
        read_exact_material_result(ledger, forged.identity)


def test_material_source_event_binds_exact_act_to_one_result():
    ledger = EventLedger()
    source_result = _preserve(ledger)

    act_identity = source_result.material["act_occurrence_event_identity"]
    assert [
        event.identity
        for event in ledger.occurrences_in_append_order(
            (act_identity, source_result.identity),
            locality_identity=source_result.locality_identity,
        )
    ] == [act_identity, source_result.identity]
    assert not tuple(
        event
        for event in ledger.iter_locality_kind(
            source_result.locality_identity,
            RECORDED_YIELD_RELATION_EVENT,
        )
        if event.material.get("act_occurrence_event_identity") == act_identity
    )


def test_changed_witness_material_result_cannot_borrow_its_act_occurrence():
    ledger = EventLedger()
    source_result = _preserve(ledger, b"first")
    changed = ledger.append(
        WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
        dict(source_result.material),
        exact_material=b"second",
        locality_identity=source_result.locality_identity,
    )

    with pytest.raises(MaterialSourceError, match="single exact result"):
        read_exact_material_result(ledger, changed.identity)


def test_added_yield_coordinate_does_not_certify_a_source_occurrence():
    ledger = EventLedger()
    source_result = _preserve(ledger, b"material")
    source_result.material["yield_relation_identity"] = "not established"

    with pytest.raises(MaterialSourceError, match="absent or corrupted"):
        read_exact_material_result(ledger, source_result.identity)


def test_equal_material_has_distinct_source_act_and_result_occurrences():
    ledger = EventLedger()
    first = _preserve(ledger, b"same exact material")
    second = _preserve(ledger, b"same exact material")

    assert exact_material_result_bytes(first) == exact_material_result_bytes(second)
    assert first.material["act_occurrence_identity"] != second.material["act_occurrence_identity"]
    assert first.material["result_identity"] != second.material["result_identity"]
    assert first.material["act_occurrence_event_identity"] != second.material[
        "act_occurrence_event_identity"
    ]
    assert "yield_relation_identity" not in first.material
    assert "yield_relation_identity" not in second.material
    assert read_exact_material_result(ledger, first.identity) == first
    assert read_exact_material_result(ledger, second.identity) == second


def test_witness_material_requires_only_material_boundary_and_locality():
    ledger = EventLedger()
    occurred = _preserve(ledger, b"different\n")

    assert occurred.material["source_occurrence_references"] == []
    reference = occurred.material["subject_to_act_binding_reference"]
    binding = ledger.get(reference["recorded_occurrence_identity"])
    assert binding.material["result_identity"] == occurred.material[
        "result_identity"
    ]
    assert "invocation" not in str(occurred.material)


def test_empty_witness_material_is_exact_material():
    occurred = _preserve(EventLedger(), b"")

    assert exact_material_result_bytes(occurred) == b""


def test_material_result_read_refuses_a_changed_source_coordinate():
    ledger = EventLedger()
    occurred = _preserve(ledger, b"exact")
    occurred.material["source_boundary"] = "different boundary"

    with pytest.raises(MaterialSourceError, match="absent or corrupted"):
        read_exact_material_result(ledger, occurred.identity)


def test_material_source_refuses_a_supplied_representation_coordinate():
    ledger = EventLedger()
    occurred = _preserve(ledger, b"exact")
    occurred.material["represented_material"] = "supplied Representation material"

    with pytest.raises(MaterialSourceError, match="absent or corrupted"):
        read_exact_material_result(ledger, occurred.identity)


@pytest.mark.parametrize("material", ["bytes", bytearray(b"x"), memoryview(b"x"), None, 1])
def test_witness_material_refuses_non_bytes(material):
    with pytest.raises(WitnessMaterialSourceError, match="exact bytes"):
        _preserve(EventLedger(), material)


@pytest.mark.parametrize("boundary", ["", "  ", None, 1, []])
def test_witness_material_requires_exact_boundary(boundary):
    with pytest.raises(WitnessMaterialSourceError, match="boundary"):
        _preserve(EventLedger(), source_boundary=boundary)


@pytest.mark.parametrize("locality", ["", "  ", None, 1, []])
def test_witness_material_requires_exact_locality(locality):
    with pytest.raises(WitnessMaterialSourceError, match="locality"):
        _preserve(EventLedger(), locality_identity=locality)


def test_exact_material_result_bytes_refuses_wrong_or_corrupt_occurrences():
    with pytest.raises(MaterialSourceError, match="carries no exact bytes"):
        exact_material_result_bytes(Event(identity="evt_x", kind="something.else", material={}))
    with pytest.raises(MaterialSourceError, match="carries no exact bytes"):
        exact_material_result_bytes(
            Event(identity="evt_x", kind=WITNESS_MATERIAL_SOURCE_RECORDED_KIND)
        )
    corrupt = Event(
        identity="evt_x",
        kind=WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
        exact_material=b"material",
    )
    object.__setattr__(corrupt, "exact_material", "material")
    with pytest.raises(MaterialSourceError, match="carries no exact bytes"):
        exact_material_result_bytes(corrupt)


def test_witness_material_identity_is_reserved_across_reopen(tmp_path):
    database = str(tmp_path / "reopen.db")
    identities = []
    for index in range(3):
        ledger = SQLiteEventLedger(database)
        try:
            material = _preserve(
                ledger,
                locality_identity=f"locality_{index}",
                exact_bytes=f"material {index}".encode(),
                source_boundary="source boundary",
            )
            identities.append(material.material["result_identity"])
        finally:
            ledger.close()

    assert len(set(identities)) == 3
