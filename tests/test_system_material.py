from __future__ import annotations

import sqlite3

import pytest

FIDELITY_SUBJECT = "exact_material_preservation_witness"

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.material_acquisition import (
    MaterialAcquisitionError,
    _append_exact_material_result_occurrence,
    acquired_material_bytes,
    read_exact_material_acquisition_result,
)
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    MaterialIngestError,
    ingest_material,
)
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.evidence_of_yield_relation import RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND, read_requirements_of_yield_relation


def _preserve(ledger, material=b"a.txt\nb.txt\n", **differences):
    fields = {
        "locality_identity": "locality_000001",
        "exact_bytes": material,
        "source_boundary": "source boundary",
    }
    fields.update(differences)
    return ingest_material(
        ledger,
        source_role="system",
        known_loss=(
            "material before the supplied system boundary is not available here",
        ),
        **fields,
    )


def test_system_material_preserves_exact_raw_bytes():
    ledger = EventLedger()
    exact = bytes(range(256)) * 3

    occurred = _preserve(ledger, exact)

    assert occurred.kind == MATERIAL_INGEST_OCCURRED_KIND
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


def test_ingest_preserves_only_exact_intact_provenance_occurrence_references():
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
    with pytest.raises(MaterialIngestError, match="exact intact occurrence"):
        _preserve(
            ledger,
            b"missing",
            provenance_occurrence_references=("missing",),
        )
    assert len(ledger.list()) == before

    ledger.corrupted = source.identity
    with pytest.raises(MaterialIngestError, match="exact intact occurrence"):
        _preserve(
            ledger,
            b"corrupted",
            provenance_occurrence_references=(source.identity,),
        )


def test_durable_ingest_preserves_raw_material_and_evidence_of_yield_relation(tmp_path):
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


def _operator_ingest(ledger, *, locality, exact):
    return ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=exact,
        source_role="operator",
        source_boundary="binary-stream.readline (exact bytes)",
    )


def _ingest_identities(ingest):
    return {
        ingest.identity,
        ingest.material["result_identity"],
        ingest.material["ingest_act_identity"],
        ingest.material["act_occurrence_identity"],
        ingest.material["responsible_act_evidence_identity"],
        ingest.material["evidence_of_yield_relation_identity"],
    }


def _strings(value):
    if isinstance(value, str):
        return {value}
    if isinstance(value, dict):
        return {
            item
            for key, carried in value.items()
            for item in (*_strings(key), *_strings(carried))
        }
    if isinstance(value, (list, tuple)):
        return {item for carried in value for item in _strings(carried)}
    return set()


def _ingest_events(ledger, ingest):
    return tuple(
        ledger.get(identity)
        for identity in (
            ingest.material["responsible_act_evidence_identity"],
            ingest.material["evidence_of_yield_relation_identity"],
            ingest.identity,
        )
    )


def test_operator_and_system_material_use_one_ingest_act_with_distinct_source_roles():
    ledger = EventLedger()
    exact = b"\x00\xffsame material\n"
    operator_ingest = _operator_ingest(ledger, locality="shared", exact=exact)
    system_ingest = _preserve(
        ledger,
        locality_identity="shared",
        exact_bytes=exact,
        source_boundary="system byte boundary",
    )

    assert operator_ingest is not None
    assert operator_ingest.kind == system_ingest.kind == MATERIAL_INGEST_OCCURRED_KIND
    assert set(operator_ingest.material) == set(system_ingest.material)
    assert acquired_material_bytes(operator_ingest) == acquired_material_bytes(
        system_ingest
    ) == exact
    assert operator_ingest.material["source_role"] == "operator"
    assert system_ingest.material["source_role"] == "system"
    assert operator_ingest.material["dimensions"]["source_provenance"] == (
        "binary-stream.readline (exact bytes)"
    )
    assert system_ingest.material["dimensions"]["source_provenance"] == (
        "system byte boundary"
    )


def test_equal_operator_and_system_bytes_keep_distinct_occurrences_results_and_evidence():
    ledger = EventLedger()
    exact = b"same exact material"
    operator_ingest = _operator_ingest(ledger, locality="shared", exact=exact)
    system_ingest = _preserve(
        ledger,
        locality_identity="shared",
        exact_bytes=exact,
        source_boundary="system byte boundary",
    )

    assert operator_ingest is not None
    assert acquired_material_bytes(operator_ingest) == acquired_material_bytes(
        system_ingest
    )
    assert _ingest_identities(operator_ingest).isdisjoint(
        _ingest_identities(system_ingest)
    )
    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=operator_ingest.identity,
        evidence_of_yield_relation_event_identity=system_ingest.material[
            "evidence_of_yield_relation_identity"
        ],
        responsible_act_evidence_event_identity=operator_ingest.material[
            "responsible_act_evidence_identity"
        ],
    ) == {
        "exact_relation": False,
        "occurrence_witness": False,
        "intact_evidence": True,
    }


def test_same_locality_preserves_both_ingest_subjects_without_relation_standing():
    ledger = EventLedger()
    operator_ingest = _operator_ingest(
        ledger, locality="shared", exact=b"operator material\n"
    )
    system_ingest = _preserve(
        ledger,
        locality_identity="shared",
        exact_bytes=b"system material",
        source_boundary="system byte boundary",
    )

    assert operator_ingest is not None
    standing = read_operator_locality_standing(
        ledger, locality_identity="shared"
    )
    assert {
        occurrence["subject_reference"]
        for occurrence in standing["ingest_occurrences"]
    } == {
        operator_ingest.material["result_identity"],
        system_ingest.material["result_identity"],
    }
    assert {
        occurrence["source_role"]
        for occurrence in standing["ingest_occurrences"]
    } == {"operator", "system"}
    assert standing["recorded_relation_Standing"] == {}


def test_operator_and_system_ingest_evidence_do_not_cross_reference():
    ledger = EventLedger()
    operator_ingest = _operator_ingest(
        ledger, locality="shared", exact=b"operator material\n"
    )
    system_ingest = _preserve(
        ledger,
        locality_identity="shared",
        exact_bytes=b"system material",
        source_boundary="system byte boundary",
    )

    assert operator_ingest is not None
    operator_identities = _ingest_identities(operator_ingest)
    system_identities = _ingest_identities(system_ingest)
    operator_material = {
        item
        for event in _ingest_events(ledger, operator_ingest)
        for item in _strings(event.material)
    }
    system_material = {
        item
        for event in _ingest_events(ledger, system_ingest)
        for item in _strings(event.material)
    }

    assert operator_material.isdisjoint(system_identities)
    assert system_material.isdisjoint(operator_identities)


def test_ingest_event_binds_exact_act_and_evidence_of_yield_relation():
    ledger = EventLedger()
    ingest = _preserve(ledger)

    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=ingest.identity,
        evidence_of_yield_relation_event_identity=ingest.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=ingest.material[
            "responsible_act_evidence_identity"
        ],
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def test_changed_ingest_material_cannot_borrow_its_evidence_of_yield_relation():
    ledger = EventLedger()
    ingest = _preserve(ledger, b"first")
    changed = ledger.append(
        MATERIAL_INGEST_OCCURRED_KIND,
        dict(ingest.material),
        exact_material=b"second",
        locality_identity=ingest.locality_identity,
    )

    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=changed.identity,
        evidence_of_yield_relation_event_identity=changed.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=changed.material[
            "responsible_act_evidence_identity"
        ],
    )["exact_relation"] is False


def test_evidence_of_yield_relation_without_exact_material_cannot_certify_an_ingest():
    ledger = EventLedger()
    ingest = _preserve(ledger, b"material")
    evidence = ledger.get(ingest.material["evidence_of_yield_relation_identity"])
    assert evidence is not None
    incomplete_evidence = ledger.append(
        RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
        dict(evidence.material),
        locality_identity=evidence.locality_identity,
    )
    carried = ledger.append(
        MATERIAL_INGEST_OCCURRED_KIND,
        {**ingest.material, "evidence_of_yield_relation_identity": incomplete_evidence.identity},
        exact_material=ingest.exact_material,
        locality_identity=ingest.locality_identity,
    )

    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=carried.identity,
        evidence_of_yield_relation_event_identity=incomplete_evidence.identity,
        responsible_act_evidence_event_identity=carried.material[
            "responsible_act_evidence_identity"
        ],
    )["exact_relation"] is False


def test_equal_material_has_distinct_ingest_occurrences_results_and_yields():
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


def test_system_material_requires_only_material_boundary_and_locality():
    occurred = _preserve(EventLedger(), b"different\n")

    assert occurred.material["provenance_occurrence_references"] == []
    assert occurred.material["dimensions"]["scope_locality"] == "locality:locality_000001"
    assert "invocation" not in str(occurred.material)


def test_empty_system_material_is_exact_material():
    occurred = _preserve(EventLedger(), b"")

    assert acquired_material_bytes(occurred) == b""


def test_generic_material_result_read_refuses_a_changed_source_coordinate():
    ledger = EventLedger()
    occurred = _preserve(ledger, b"exact")
    occurred.material["source_boundary"] = "different boundary"

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
                kind=MATERIAL_INGEST_OCCURRED_KIND,
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
def test_system_material_refuses_non_bytes(material):
    with pytest.raises(MaterialIngestError, match="exact bytes"):
        _preserve(EventLedger(), material)


@pytest.mark.parametrize("boundary", ["", "  ", None, 1, []])
def test_system_material_requires_exact_boundary(boundary):
    with pytest.raises(MaterialIngestError, match="boundary"):
        _preserve(EventLedger(), source_boundary=boundary)


@pytest.mark.parametrize("locality", ["", "  ", None, 1, []])
def test_system_material_requires_exact_locality(locality):
    with pytest.raises(MaterialIngestError, match="locality"):
        _preserve(EventLedger(), locality_identity=locality)


def test_acquired_material_bytes_refuses_wrong_or_corrupt_occurrences():
    with pytest.raises(MaterialAcquisitionError, match="carries no exact bytes"):
        acquired_material_bytes(Event(identity="evt_x", kind="something.else", material={}))
    with pytest.raises(MaterialAcquisitionError, match="carries no exact bytes"):
        acquired_material_bytes(
            Event(identity="evt_x", kind=MATERIAL_INGEST_OCCURRED_KIND)
        )
    corrupt = Event(
        identity="evt_x",
        kind=MATERIAL_INGEST_OCCURRED_KIND,
        exact_material=b"material",
    )
    object.__setattr__(corrupt, "exact_material", "material")
    with pytest.raises(MaterialAcquisitionError, match="carries no exact bytes"):
        acquired_material_bytes(corrupt)


def test_system_material_identity_is_reserved_across_reopen(tmp_path):
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
