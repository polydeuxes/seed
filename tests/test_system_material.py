from __future__ import annotations

from io import BytesIO

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
from seed_runtime.yield_evidence import read_yield_edge_requirements


def _preserve(ledger, material=b"a.txt\nb.txt\n", **differences):
    fields = {
        "locality_id": "locality_000001",
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
    assert occurred.locality_id == "locality_000001"
    assert occurred.payload["byte_count"] == len(exact)
    assert ingested_material_bytes(occurred) == exact
    assert "represented_material" not in occurred.payload


def test_operator_and_system_material_share_one_ingest_road():
    ledger = EventLedger()
    exact = b"\x00\xffsame material\n"
    operator_standing = run_operator_ingest(
        ledger=ledger,
        locality_id="shared",
        boundary_material=operator_boundary_material(BytesIO(exact)),
    )
    operator_ingest = ledger.get(operator_standing["event_ids"][-1])
    system_ingest = preserve_system_material(
        ledger,
        locality_id="shared",
        exact_bytes=exact,
        observed_boundary="system byte boundary",
    )

    assert operator_ingest is not None
    assert operator_ingest.kind == system_ingest.kind == MATERIAL_INGEST_OCCURRED_KIND
    assert set(operator_ingest.payload) == set(system_ingest.payload)
    assert ingested_material_bytes(operator_ingest) == ingested_material_bytes(
        system_ingest
    ) == exact
    assert operator_ingest.payload["source_role"] == "operator"
    assert system_ingest.payload["source_role"] == "system"


def test_ingest_event_binds_exact_act_and_result_evidence():
    ledger = EventLedger()
    ingest = _preserve(ledger)

    assert read_yield_edge_requirements(
        ledger,
        recorded_result_event_id=ingest.id,
        result_evidence_event_id=ingest.payload["yield_evidence_id"],
        responsible_act_evidence_event_id=ingest.payload[
            "responsible_act_evidence_id"
        ],
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def test_system_material_requires_only_material_boundary_and_locality():
    occurred = _preserve(EventLedger(), b"different\n")

    assert occurred.payload["provenance_occurrence_refs"] == []
    assert occurred.payload["dimensions"]["scope_locality"] == "locality:locality_000001"
    assert "invocation" not in str(occurred.payload)


def test_empty_system_material_is_exact_material():
    occurred = _preserve(EventLedger(), b"")

    assert occurred.payload["byte_count"] == 0
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
        _preserve(EventLedger(), locality_id=locality)


def test_ingested_material_bytes_refuses_wrong_or_corrupt_occurrences():
    with pytest.raises(MaterialIngestError, match="only Ingest occurrences"):
        ingested_material_bytes(Event(id="evt_x", kind="something.else", payload={}))
    for payload in ({}, {"exact_bytes_hex": None}, {"exact_bytes_hex": 7}):
        with pytest.raises(MaterialIngestError, match="carries no exact bytes"):
            ingested_material_bytes(
                Event(id="evt_x", kind=MATERIAL_INGEST_OCCURRED_KIND, payload=payload)
            )
    with pytest.raises(MaterialIngestError, match="malformed bytes"):
        ingested_material_bytes(
            Event(
                id="evt_x",
                kind=MATERIAL_INGEST_OCCURRED_KIND,
                payload={"exact_bytes_hex": "zz", "byte_count": 1},
            )
        )
    with pytest.raises(MaterialIngestError, match="byte count differ"):
        ingested_material_bytes(
            Event(
                id="evt_x",
                kind=MATERIAL_INGEST_OCCURRED_KIND,
                payload={"exact_bytes_hex": "6100", "byte_count": 99},
            )
        )


def test_system_material_identity_is_reserved_across_reopen(tmp_path):
    database = str(tmp_path / "reopen.db")
    identities = []
    for index in range(3):
        ledger = SQLiteEventLedger(database)
        try:
            material = preserve_system_material(
                ledger,
                locality_id=f"locality_{index}",
                exact_bytes=f"material {index}".encode(),
                observed_boundary="source boundary",
            )
            identities.append(material.payload["dimensions"]["identity"])
        finally:
            ledger.close()

    assert len(set(identities)) == 3
