from __future__ import annotations

from io import BytesIO
import sqlite3

import pytest

from seed_runtime.event import Event
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    MaterialIngestError,
    ingested_material_bytes,
)
from seed_runtime.operator_ingest import run_operator_ingest
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.system_material import preserve_system_material
from seed_runtime.yield_evidence import YIELD_EVIDENCE_KIND, read_yield_edge_requirements


def _preserve(ledger, material=b"a.txt\nb.txt\n", **differences):
    fields = {
        "locality_identity": "locality_000001",
        "exact_bytes": material,
        "observed_boundary": "source boundary",
    }
    fields.update(differences)
    return preserve_system_material(ledger, **fields)


def test_system_material_preserves_exact_raw_bytes():
    ledger = EventLedger()
    exact = bytes(range(256)) * 3

    occurred = _preserve(ledger, exact)

    assert occurred.kind == MATERIAL_INGEST_OCCURRED_KIND
    assert occurred.locality_identity == "locality_000001"
    assert ingested_material_bytes(occurred) == exact
    assert "represented_material" not in occurred.material


def test_durable_ingest_preserves_raw_material_and_yield_evidence(tmp_path):
    path = str(tmp_path / "material.db")
    exact = b"\x00\xffraw material\n"
    ledger = SQLiteEventLedger(path)
    occurred = _preserve(ledger, exact)
    evidence_identity = occurred.material["yield_evidence_identity"]
    occurred_identity = occurred.identity
    ledger.close()

    connection = sqlite3.connect(path)
    carried = connection.execute(
        "SELECT exact_material, typeof(exact_material) FROM events WHERE identity = ?",
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
        assert read_yield_edge_requirements(
            reopened,
            recorded_result_event_identity=occurred_identity,
            result_evidence_event_identity=evidence_identity,
            responsible_act_evidence_event_identity=read.material[
                "responsible_act_evidence_identity"
            ],
        )["exact_relation"] is True
    finally:
        reopened.close()


def test_operator_and_system_material_share_one_ingest_road():
    ledger = EventLedger()
    exact = b"\x00\xffsame material\n"
    operator_standing = run_operator_ingest(
        ledger=ledger,
        locality_identity="shared",
        boundary_material=operator_boundary_material(BytesIO(exact)),
    )
    operator_ingest = ledger.get(
        operator_standing["current_standing"]["ingest_occurrence"][
            "evidence_event_identity"
        ]
    )
    system_ingest = preserve_system_material(
        ledger,
        locality_identity="shared",
        exact_bytes=exact,
        observed_boundary="system byte boundary",
    )

    assert operator_ingest is not None
    assert operator_ingest.kind == system_ingest.kind == MATERIAL_INGEST_OCCURRED_KIND
    assert set(operator_ingest.material) == set(system_ingest.material)
    assert ingested_material_bytes(operator_ingest) == ingested_material_bytes(
        system_ingest
    ) == exact
    assert operator_ingest.material["source_role"] == "operator"
    assert system_ingest.material["source_role"] == "system"


def test_ingest_event_binds_exact_act_and_result_evidence():
    ledger = EventLedger()
    ingest = _preserve(ledger)

    assert read_yield_edge_requirements(
        ledger,
        recorded_result_event_identity=ingest.identity,
        result_evidence_event_identity=ingest.material["yield_evidence_identity"],
        responsible_act_evidence_event_identity=ingest.material[
            "responsible_act_evidence_identity"
        ],
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def test_changed_ingest_material_cannot_borrow_its_yield_evidence():
    ledger = EventLedger()
    ingest = _preserve(ledger, b"first")
    changed = ledger.append(
        MATERIAL_INGEST_OCCURRED_KIND,
        dict(ingest.material),
        exact_material=b"second",
        locality_identity=ingest.locality_identity,
    )

    assert read_yield_edge_requirements(
        ledger,
        recorded_result_event_identity=changed.identity,
        result_evidence_event_identity=changed.material["yield_evidence_identity"],
        responsible_act_evidence_event_identity=changed.material[
            "responsible_act_evidence_identity"
        ],
    )["exact_relation"] is False


def test_yield_evidence_without_exact_material_cannot_certify_an_ingest():
    ledger = EventLedger()
    ingest = _preserve(ledger, b"material")
    evidence = ledger.get(ingest.material["yield_evidence_identity"])
    assert evidence is not None
    incomplete_evidence = ledger.append(
        YIELD_EVIDENCE_KIND,
        dict(evidence.material),
        locality_identity=evidence.locality_identity,
    )
    carried = ledger.append(
        MATERIAL_INGEST_OCCURRED_KIND,
        {**ingest.material, "yield_evidence_identity": incomplete_evidence.identity},
        exact_material=ingest.exact_material,
        locality_identity=ingest.locality_identity,
    )

    assert read_yield_edge_requirements(
        ledger,
        recorded_result_event_identity=carried.identity,
        result_evidence_event_identity=incomplete_evidence.identity,
        responsible_act_evidence_event_identity=carried.material[
            "responsible_act_evidence_identity"
        ],
    )["exact_relation"] is False


def test_equal_material_has_distinct_ingest_occurrences_results_and_yields():
    ledger = EventLedger()
    first = _preserve(ledger, b"same exact material")
    second = _preserve(ledger, b"same exact material")

    assert ingested_material_bytes(first) == ingested_material_bytes(second)
    assert first.material["act_occurrence_identity"] != second.material["act_occurrence_identity"]
    assert first.material["result_identity"] != second.material["result_identity"]
    assert first.material["yield_evidence_identity"] != second.material["yield_evidence_identity"]
    assert read_yield_edge_requirements(
        ledger,
        recorded_result_event_identity=first.identity,
        result_evidence_event_identity=second.material["yield_evidence_identity"],
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

    assert ingested_material_bytes(occurred) == b""


@pytest.mark.parametrize("material", ["bytes", bytearray(b"x"), memoryview(b"x"), None, 1])
def test_system_material_refuses_non_bytes(material):
    with pytest.raises(MaterialIngestError, match="exact bytes"):
        _preserve(EventLedger(), material)


@pytest.mark.parametrize("boundary", ["", "  ", None, 1, []])
def test_system_material_requires_exact_boundary(boundary):
    with pytest.raises(MaterialIngestError, match="boundary"):
        _preserve(EventLedger(), observed_boundary=boundary)


@pytest.mark.parametrize("locality", ["", "  ", None, 1, []])
def test_system_material_requires_exact_locality(locality):
    with pytest.raises(MaterialIngestError, match="locality"):
        _preserve(EventLedger(), locality_identity=locality)


def test_ingested_material_bytes_refuses_wrong_or_corrupt_occurrences():
    with pytest.raises(MaterialIngestError, match="only Ingest occurrences"):
        ingested_material_bytes(Event(identity="evt_x", kind="something.else", material={}))
    with pytest.raises(MaterialIngestError, match="carries no exact bytes"):
        ingested_material_bytes(
            Event(identity="evt_x", kind=MATERIAL_INGEST_OCCURRED_KIND)
        )
    corrupt = Event(
        identity="evt_x",
        kind=MATERIAL_INGEST_OCCURRED_KIND,
        exact_material=b"material",
    )
    object.__setattr__(corrupt, "exact_material", "material")
    with pytest.raises(MaterialIngestError, match="carries no exact bytes"):
        ingested_material_bytes(corrupt)


def test_system_material_identity_is_reserved_across_reopen(tmp_path):
    database = str(tmp_path / "reopen.db")
    identities = []
    for index in range(3):
        ledger = SQLiteEventLedger(database)
        try:
            material = preserve_system_material(
                ledger,
                locality_identity=f"locality_{index}",
                exact_bytes=f"material {index}".encode(),
                observed_boundary="source boundary",
            )
            identities.append(material.material["dimensions"]["identity"])
        finally:
            ledger.close()

    assert len(set(identities)) == 3
