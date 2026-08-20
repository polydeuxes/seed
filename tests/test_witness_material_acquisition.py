from __future__ import annotations

import sqlite3

import pytest


from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.material_acquisition import (
    MaterialAcquisitionError,
    _append_exact_material_result_occurrence,
    acquired_material_bytes,
    read_exact_material_acquisition_result,
)
from seed_runtime.witness_material_acquisition import (
    WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
    WitnessMaterialAcquisitionError,
    record_witness_material_acquisition,
)
from seed_runtime.evidence_of_yield_relation import RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND, read_requirements_of_yield_relation


def _preserve(ledger, material=b"a.txt\nb.txt\n", **differences):
    fields = {
        "locality_identity": "locality_000001",
        "exact_bytes": material,
        "source_boundary": "source boundary",
    }
    fields.update(differences)
    return record_witness_material_acquisition(
        ledger,
        known_loss=(
            "material before the supplied Witness boundary is not available here",
        ),
        **fields,
    )


def test_witness_material_preserves_exact_raw_bytes():
    ledger = EventLedger()
    exact = bytes(range(256)) * 3

    occurred = _preserve(ledger, exact)

    assert occurred.kind == WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
    assert occurred.locality_identity == "locality_000001"
    assert acquired_material_bytes(occurred) == exact
    assert "represented_material" not in occurred.material
    assert set(occurred.material["dimensions"]) == {
        "identity",
        "source_provenance",
        "responsibility",
        "authority",
        "evidence_scope",
        "scope_locality",
        "occurrence_preservation",
    }


def test_material_acquisition_preserves_only_exact_intact_provenance_occurrence_references():
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
    with pytest.raises(WitnessMaterialAcquisitionError, match="exact intact occurrence"):
        _preserve(
            ledger,
            b"missing",
            provenance_occurrence_references=("missing",),
        )
    assert len(ledger.list()) == before

    ledger.corrupted = source.identity
    with pytest.raises(WitnessMaterialAcquisitionError, match="exact intact occurrence"):
        _preserve(
            ledger,
            b"corrupted",
            provenance_occurrence_references=(source.identity,),
        )


def test_durable_witness_acquisition_preserves_raw_material_and_evidence_of_yield_relation(tmp_path):
    path = str(tmp_path / "material.db")
    exact = b"\x00\xffraw material\n"
    ledger = SQLiteEventLedger(path)
    occurred = _preserve(ledger, exact)
    evidence_identity = occurred.material["evidence_of_yield_relation_identity"]
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
        evidence = reopened.get(evidence_identity)
        assert read is not None and evidence is not None
        assert read.exact_material == evidence.exact_material == exact
        assert set(evidence.material["dimensions"]) == {
            "identity",
            "exact_act",
            "act_occurrence_identity",
            "responsibility",
            "responsible_boundary",
            "authority",
        }
        assert read_requirements_of_yield_relation(
            reopened,
            recorded_result_event_identity=occurred_identity,
            evidence_of_yield_relation_event_identity=evidence_identity,
            responsible_act_evidence_event_identity=read.material[
                "responsible_act_evidence_identity"
            ],
        )["exact_relation"] is True
    finally:
        reopened.close()


def test_witness_material_acquisition_fixes_its_exact_source_subject():
    occurred = _preserve(EventLedger())

    assert occurred.material["source_role"] == "this Witness"


def test_material_acquisition_event_binds_exact_act_and_evidence_of_yield_relation():
    ledger = EventLedger()
    acquisition_result = _preserve(ledger)

    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=acquisition_result.identity,
        evidence_of_yield_relation_event_identity=acquisition_result.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=acquisition_result.material[
            "responsible_act_evidence_identity"
        ],
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def test_changed_record_witness_material_acquisition_cannot_borrow_its_evidence_of_yield_relation():
    ledger = EventLedger()
    acquisition_result = _preserve(ledger, b"first")
    changed = ledger.append(
        WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
        dict(acquisition_result.material),
        exact_material=b"second",
        locality_identity=acquisition_result.locality_identity,
    )

    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=changed.identity,
        evidence_of_yield_relation_event_identity=changed.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=changed.material[
            "responsible_act_evidence_identity"
        ],
    )["exact_relation"] is False


def test_evidence_of_yield_relation_without_exact_material_cannot_certify_an_acquire():
    ledger = EventLedger()
    acquisition_result = _preserve(ledger, b"material")
    evidence = ledger.get(acquisition_result.material["evidence_of_yield_relation_identity"])
    assert evidence is not None
    incomplete_evidence = ledger.append(
        RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
        dict(evidence.material),
        locality_identity=evidence.locality_identity,
    )
    carried = ledger.append(
        WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
        {**acquisition_result.material, "evidence_of_yield_relation_identity": incomplete_evidence.identity},
        exact_material=acquisition_result.exact_material,
        locality_identity=acquisition_result.locality_identity,
    )

    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=carried.identity,
        evidence_of_yield_relation_event_identity=incomplete_evidence.identity,
        responsible_act_evidence_event_identity=carried.material[
            "responsible_act_evidence_identity"
        ],
    )["exact_relation"] is False


def test_equal_material_has_distinct_material_acquisition_result_occurrences_results_and_yields():
    ledger = EventLedger()
    first = _preserve(ledger, b"same exact material")
    second = _preserve(ledger, b"same exact material")

    assert acquired_material_bytes(first) == acquired_material_bytes(second)
    assert first.material["act_occurrence_identity"] != second.material["act_occurrence_identity"]
    assert first.material["result_identity"] != second.material["result_identity"]
    assert first.material["evidence_of_yield_relation_identity"] != second.material["evidence_of_yield_relation_identity"]
    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=first.identity,
        evidence_of_yield_relation_event_identity=second.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=first.material[
            "responsible_act_evidence_identity"
        ],
    ) == {
        "exact_relation": False,
        "occurrence_witness": False,
        "intact_evidence": True,
    }


def test_witness_material_requires_only_material_boundary_and_locality():
    occurred = _preserve(EventLedger(), b"different\n")

    assert occurred.material["provenance_occurrence_references"] == []
    assert occurred.material["dimensions"]["scope_locality"] == "locality:locality_000001"
    assert "invocation" not in str(occurred.material)


def test_empty_witness_material_is_exact_material():
    occurred = _preserve(EventLedger(), b"")

    assert acquired_material_bytes(occurred) == b""


def test_generic_material_result_read_refuses_a_changed_source_coordinate():
    ledger = EventLedger()
    occurred = _preserve(ledger, b"exact")
    occurred.material["source_boundary"] = "different boundary"

    with pytest.raises(MaterialAcquisitionError, match="absent or corrupted"):
        read_exact_material_acquisition_result(ledger, occurred.identity)


def test_material_acquisition_refuses_a_supplied_representation_coordinate():
    ledger = EventLedger()
    occurred = _preserve(ledger, b"exact")
    occurred.material["represented_material"] = "supplied Representation material"

    with pytest.raises(MaterialAcquisitionError, match="absent or corrupted"):
        read_exact_material_acquisition_result(ledger, occurred.identity)


def test_storage_helper_refuses_unrelated_act_and_yield_before_append():
    ledger = EventLedger()
    act = ledger.append("unrelated.act", locality_identity="s")
    yielded = ledger.append("unrelated.yield", locality_identity="s")
    before = ledger.append_boundary()

    with pytest.raises(MaterialAcquisitionError, match="prior intact Act and Yield"):
        _append_exact_material_result_occurrence(
            ledger,
            result_event=Event(
                identity=ledger.allocate_event_identity(),
                kind=WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
                material={
                    "responsible_act_evidence_identity": act.identity,
                    "evidence_of_yield_relation_identity": yielded.identity,
                },
                exact_material=b"not admitted",
                locality_identity="s",
            ),
        )

    assert ledger.append_boundary() == before


@pytest.mark.parametrize("material", ["bytes", bytearray(b"x"), memoryview(b"x"), None, 1])
def test_witness_material_refuses_non_bytes(material):
    with pytest.raises(WitnessMaterialAcquisitionError, match="exact bytes"):
        _preserve(EventLedger(), material)


@pytest.mark.parametrize("boundary", ["", "  ", None, 1, []])
def test_witness_material_requires_exact_boundary(boundary):
    with pytest.raises(WitnessMaterialAcquisitionError, match="boundary"):
        _preserve(EventLedger(), source_boundary=boundary)


@pytest.mark.parametrize("locality", ["", "  ", None, 1, []])
def test_witness_material_requires_exact_locality(locality):
    with pytest.raises(WitnessMaterialAcquisitionError, match="locality"):
        _preserve(EventLedger(), locality_identity=locality)


def test_acquired_material_bytes_refuses_wrong_or_corrupt_occurrences():
    with pytest.raises(MaterialAcquisitionError, match="carries no exact bytes"):
        acquired_material_bytes(Event(identity="evt_x", kind="something.else", material={}))
    with pytest.raises(MaterialAcquisitionError, match="carries no exact bytes"):
        acquired_material_bytes(
            Event(identity="evt_x", kind=WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND)
        )
    corrupt = Event(
        identity="evt_x",
        kind=WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
        exact_material=b"material",
    )
    object.__setattr__(corrupt, "exact_material", "material")
    with pytest.raises(MaterialAcquisitionError, match="carries no exact bytes"):
        acquired_material_bytes(corrupt)


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
