from __future__ import annotations

import sqlite3

import pytest


from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.material_source import (
    MaterialSourceError,
    _append_exact_material_result_occurrence,
    exact_material_result_bytes,
    read_exact_material_result,
    read_material_locality_relation_requirements,
)
from seed_runtime.witness_material_source import (
    WITNESS_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
    WitnessMaterialSourceError,
    record_witness_material_source,
    read_witness_material_source_locality_relation_requirements,
)
from seed_runtime.yield_relation import RECORDED_YIELD_RELATION_EVENT, read_requirements_of_yield_relation


def _preserve(ledger, material=b"a.txt\nb.txt\n", **differences):
    fields = {
        "locality_identity": "locality_000001",
        "exact_bytes": material,
        "source_boundary": "source boundary",
    }
    fields.update(differences)
    return record_witness_material_source(
        ledger,
        known_loss=(
            "material before the supplied Witness boundary is not available here",
        ),
        **fields,
    )


def test_source_result_preserves_each_exact_byte_value_without_interpretation():
    ledger = EventLedger()
    exact = bytes(range(256)) * 3

    occurred = _preserve(ledger, exact)

    assert occurred.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND
    assert occurred.locality_identity == "locality_000001"
    assert exact_material_result_bytes(occurred) == exact
    assert occurred.material["locality_relation"] == {
        "first_subject": {
            "recorded_occurrence_identity": occurred.identity,
            "coordinate": "exact_material",
        },
        "relation": "locality",
        "second_subject": "this Seed",
        "relation_occurrence_identity": occurred.identity,
    }


def test_material_source_preserves_only_exact_intact_provenance_occurrence_references():
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
        provenance_occurrence_references=(source.identity,),
    )

    assert occurred.material["provenance_occurrence_references"] == [
        source.identity
    ]

    before = len(ledger.list())
    with pytest.raises(WitnessMaterialSourceError, match="exact intact occurrence"):
        _preserve(
            ledger,
            b"missing",
            provenance_occurrence_references=("missing",),
        )
    assert len(ledger.list()) == before

    ledger.corrupted = source.identity
    with pytest.raises(WitnessMaterialSourceError, match="exact intact occurrence"):
        _preserve(
            ledger,
            b"corrupted",
            provenance_occurrence_references=(source.identity,),
        )


def test_durable_witness_source_preserves_raw_material_and_yield_relation(tmp_path):
    path = str(tmp_path / "material.db")
    exact = b"\x00\xffraw material\n"
    ledger = SQLiteEventLedger(path)
    occurred = _preserve(ledger, exact)
    yield_relation_identity = occurred.material["yield_relation_identity"]
    occurred_identity = occurred.identity
    ledger.close()

    connection = sqlite3.connect(path)
    carried = connection.execute(
        "SELECT event_exact_materials.exact_material, "
        "typeof(event_exact_materials.exact_material) FROM events "
        "JOIN event_exact_materials ON event_exact_materials.material_identity = "
        "events.exact_material_identity WHERE events.identity = ?",
        (occurred_identity,),
    ).fetchone()
    connection.close()
    assert carried == (exact, "blob")

    reopened = SQLiteEventLedger(path)
    try:
        read = reopened.get(occurred_identity)
        yield_relation = reopened.get(yield_relation_identity)
        assert read is not None and yield_relation is not None
        assert read.exact_material == yield_relation.exact_material == exact
        assert set(yield_relation.material["dimensions"]) == {
            "identity",
            "exact_act",
            "act_occurrence_identity",
        }
        assert read_requirements_of_yield_relation(
            reopened,
            recorded_result_event_identity=occurred_identity,
            yield_relation_event_identity=yield_relation_identity,
            act_occurrence_event_identity=read.material[
                "act_occurrence_event_identity"
            ],
        )["exact_relation"] is True
    finally:
        reopened.close()


def test_witness_material_source_fixes_its_exact_source_subject():
    ledger = EventLedger()
    occurred = _preserve(ledger)

    assert occurred.material["source_role"] == "this Witness"
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
        "source_role": "this Witness",
        "source_boundary": "source boundary",
    }
    assert binding.material["scope"] == {
        "source_boundary": "source boundary",
        "locality_identity": "locality_000001",
        "result_identity": occurred.material["result_identity"],
    }
    assert reference["result_boundary_identity"] == occurred.material[
        "result_identity"
    ]
    assert act_occurrence.material[
        "subject_to_act_binding_reference"
    ] == reference
    assert [
        event.identity
        for event in ledger.occurrences_in_append_order(
            (
                binding.identity,
                act_occurrence.identity,
                occurred.material["yield_relation_identity"],
                occurred.identity,
            ),
            locality_identity=occurred.locality_identity,
        )
    ] == [
        binding.identity,
        act_occurrence.identity,
        occurred.material["yield_relation_identity"],
        occurred.identity,
    ]


def test_witness_material_locality_relation_preserves_invocation_and_provenance():
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
        provenance_occurrence_references=(command.identity,),
    )

    assert occurred.locality_identity == "invocation-locality"
    assert occurred.exact_material == b"hello"
    assert occurred.material["source_role"] == "this Witness"
    assert occurred.material["source_boundary"] == "stdout"
    assert occurred.material["provenance_occurrence_references"] == [
        command.identity
    ]
    assert all(
        read_witness_material_source_locality_relation_requirements(
            ledger,
            recorded_result_event_identity=occurred.identity,
        ).values()
    )
    assert all(
        read_material_locality_relation_requirements(
            ledger,
            recorded_result_event_identity=occurred.identity,
        ).values()
    )
    assert not any(
        event.exact_material == b"hello"
        for event in ledger.list_locality("operator-locality")
    )


def test_witness_material_locality_relation_refuses_mismatched_coordinates():
    ledger = EventLedger()
    occurred = _preserve(ledger, b"hello")
    forged_relation = dict(occurred.material["locality_relation"])
    forged_relation["second_subject"] = "another boundary"
    forged = ledger.append(
        WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
        {**occurred.material, "locality_relation": forged_relation},
        exact_material=occurred.exact_material,
        locality_identity=occurred.locality_identity,
    )

    assert read_witness_material_source_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=forged.identity,
    ) == {
        "exact_relation": False,
        "relation_occurrence": False,
        "intact_source_occurrence": False,
    }
    with pytest.raises(MaterialSourceError, match="absent or corrupted"):
        read_exact_material_result(ledger, forged.identity)


def test_material_source_event_binds_exact_act_and_yield_relation():
    ledger = EventLedger()
    source_result = _preserve(ledger)

    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=source_result.identity,
        yield_relation_event_identity=source_result.material["yield_relation_identity"],
        act_occurrence_event_identity=source_result.material[
            "act_occurrence_event_identity"
        ],
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": True,
    }


def test_changed_record_witness_material_source_cannot_borrow_its_yield_relation():
    ledger = EventLedger()
    source_result = _preserve(ledger, b"first")
    changed = ledger.append(
        WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
        dict(source_result.material),
        exact_material=b"second",
        locality_identity=source_result.locality_identity,
    )

    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=changed.identity,
        yield_relation_event_identity=changed.material["yield_relation_identity"],
        act_occurrence_event_identity=changed.material[
            "act_occurrence_event_identity"
        ],
    )["exact_relation"] is False


def test_yield_relation_without_exact_material_cannot_certify_a_source_occurrence():
    ledger = EventLedger()
    source_result = _preserve(ledger, b"material")
    yield_relation = ledger.get(source_result.material["yield_relation_identity"])
    assert yield_relation is not None
    incomplete_yield_relation = ledger.append(
        RECORDED_YIELD_RELATION_EVENT,
        dict(yield_relation.material),
        locality_identity=yield_relation.locality_identity,
    )
    carried = ledger.append(
        WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
        {
            **source_result.material,
            "yield_relation_identity": incomplete_yield_relation.identity,
        },
        exact_material=source_result.exact_material,
        locality_identity=source_result.locality_identity,
    )

    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=carried.identity,
        yield_relation_event_identity=incomplete_yield_relation.identity,
        act_occurrence_event_identity=carried.material[
            "act_occurrence_event_identity"
        ],
    )["exact_relation"] is False


def test_equal_material_has_distinct_material_source_result_occurrences_results_and_yields():
    ledger = EventLedger()
    first = _preserve(ledger, b"same exact material")
    second = _preserve(ledger, b"same exact material")

    assert exact_material_result_bytes(first) == exact_material_result_bytes(second)
    assert first.material["act_occurrence_identity"] != second.material["act_occurrence_identity"]
    assert first.material["result_identity"] != second.material["result_identity"]
    assert first.material["yield_relation_identity"] != second.material["yield_relation_identity"]
    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=first.identity,
        yield_relation_event_identity=second.material["yield_relation_identity"],
        act_occurrence_event_identity=first.material[
            "act_occurrence_event_identity"
        ],
    ) == {
        "exact_relation": False,
        "occurrence_witness": False,
        "intact_occurrence": True,
    }


def test_witness_material_requires_only_material_boundary_and_locality():
    occurred = _preserve(EventLedger(), b"different\n")

    assert occurred.material["provenance_occurrence_references"] == []
    assert occurred.material["dimensions"]["scope_locality"] == "locality:locality_000001"
    assert "invocation" not in str(occurred.material)


def test_empty_witness_material_is_exact_material():
    occurred = _preserve(EventLedger(), b"")

    assert exact_material_result_bytes(occurred) == b""


def test_generic_material_result_read_refuses_a_changed_source_coordinate():
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


def test_storage_helper_refuses_unrelated_act_and_yield_before_append():
    ledger = EventLedger()
    act = ledger.append("unrelated.act", locality_identity="s")
    yielded = ledger.append("unrelated.yield", locality_identity="s")
    before = ledger.append_boundary()

    with pytest.raises(MaterialSourceError, match="prior intact Act and Yield"):
        _append_exact_material_result_occurrence(
            ledger,
            result_event=Event(
                identity=ledger.allocate_event_identity(),
                kind=WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
                material={
                    "act_occurrence_event_identity": act.identity,
                    "yield_relation_identity": yielded.identity,
                },
                exact_material=b"not admitted",
                locality_identity="s",
            ),
        )

    assert ledger.append_boundary() == before


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
            identities.append(material.material["dimensions"]["identity"])
        finally:
            ledger.close()

    assert len(set(identities)) == 3
