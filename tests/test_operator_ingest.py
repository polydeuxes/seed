"""Every non-EOF byte frame becomes one preserved operator occurrence."""

from __future__ import annotations

from io import BytesIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingest import run_operator_ingest
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND


def _run(material: bytes):
    ledger = EventLedger()
    standing = run_operator_ingest(
        ledger=ledger,
        locality_id="s",
        boundary_material=operator_boundary_material(BytesIO(material)),
    )
    return ledger, standing


def test_arbitrary_bytes_are_preserved_without_a_gate_or_stop():
    material = b"\xff\xfe\x00binary\n"
    ledger, standing = _run(material)
    events = ledger.list_locality("s")
    ingests = [event for event in events if event.kind == MATERIAL_INGEST_OCCURRED_KIND]

    assert len(ingests) == 1
    assert bytes.fromhex(ingests[0].payload["exact_bytes_hex"]) == material
    assert ingests[0].payload["source_role"] == "operator"
    assert ingests[0].payload["provenance_occurrence_references"] == []


def test_addressable_material_is_the_exact_byte_sequence():
    material = b"\x00\xff\r\n"
    _, standing = _run(material)
    addressable = standing["addressable_material"]

    exact = addressable["exact_material"]
    assert bytes.fromhex(exact["exact_bytes_hex"]) == material
    assert exact["source_span"]["end"] == len(material)
    assert addressable["provenance"] == (addressable["ingest_event_reference"],)


def test_empty_line_is_material_but_eof_is_not_an_attempt():
    _, standing = _run(b"\n")

    assert standing["current_standing"]["ingest_occurrence"] is not None
