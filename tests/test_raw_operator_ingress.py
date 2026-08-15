"""Every non-EOF byte frame becomes one preserved operator occurrence."""

from __future__ import annotations

from io import BytesIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material


def _run(material: bytes):
    ledger = EventLedger()
    standing = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        locality_id="s",
        captured_ingress=capture_stdin_material(BytesIO(material)),
    )
    return ledger, standing


def test_arbitrary_bytes_are_preserved_without_a_gate_or_stop():
    material = b"\xff\xfe\x00binary\n"
    ledger, standing = _run(material)
    events = ledger.list_locality("w", "s")

    assert [event.kind for event in events] == [
        "operator.material.raw_captured",
        "operator.material.occurred",
    ]
    assert bytes.fromhex(events[0].payload["exact_bytes_hex"]) == material
    assert events[1].payload["raw_material_event_id"] == events[0].id
    assert events[1].payload["provenance_occurrence_refs"] == [events[0].id]
    assert standing["current_standing"]["interaction_closure"] is None


def test_addressable_material_is_the_exact_byte_sequence():
    material = b"\x00\xff\r\n"
    _, standing = _run(material)
    addressable = standing["addressable_operator_material"]

    exact = addressable["exact_operator_material"]
    assert bytes.fromhex(exact["exact_bytes_hex"]) == material
    assert exact["source_spans"][0]["end"] == len(material)
    assert addressable["provenance"] == (
        addressable["raw_material_event_ref"],
        addressable["ingress_event_ref"],
    )


def test_empty_line_is_material_but_eof_is_not_an_attempt():
    _, standing = _run(b"\n")

    assert standing["current_standing"]["preserved_ingress"] is not None
