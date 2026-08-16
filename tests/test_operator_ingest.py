"""Every non-EOF byte frame becomes one preserved operator occurrence."""

from __future__ import annotations

from io import BytesIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingest import (
    run_operator_ingest,
    update_operator_ingest_standing,
)
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingested_material_bytes,
)


def _run(material: bytes):
    ledger = EventLedger()
    standing = run_operator_ingest(
        ledger=ledger,
        locality_identity="s",
        boundary_material=operator_boundary_material(BytesIO(material)),
    )
    return ledger, standing


def test_arbitrary_bytes_are_preserved_without_a_gate_or_stop():
    material = b"\xff\xfe\x00binary\n"
    ledger, standing = _run(material)
    events = ledger.list_locality("s")
    ingests = [event for event in events if event.kind == MATERIAL_INGEST_OCCURRED_KIND]

    assert len(ingests) == 1
    assert ingested_material_bytes(ingests[0]) == material
    assert ingests[0].material["source_role"] == "operator"
    assert ingests[0].material["provenance_occurrence_references"] == []


def test_current_standing_names_the_exact_ingest_occurrence():
    material = b"\x00\xff\r\n"
    ledger, standing = _run(material)
    current = standing["current_standing"]["ingest_occurrence"]
    occurrence = ledger.get(current["evidence_event_identity"])

    assert occurrence is not None
    assert current["subject_reference"] == occurrence.material["result_identity"]
    assert ingested_material_bytes(occurrence) == material
    assert occurrence.material["provenance_occurrence_references"] == []


def test_empty_line_is_material_but_eof_is_not_an_attempt():
    _, standing = _run(b"\n")

    assert standing["current_standing"]["ingest_occurrence"] is not None


def test_ingest_standing_preserves_first_occurrence_order_without_sorting():
    ledger = EventLedger()
    attempts = {}
    first = ledger.append(
        MATERIAL_INGEST_OCCURRED_KIND,
        {
            "source_role": "operator",
            "dimensions": {"identity": "operator-result"},
            "known_loss": ["later", "earlier"],
            "unknowns": ["second", "first"],
            "conflicts": ["right", "left"],
        },
        locality_identity="s",
    )
    second = ledger.append(
        MATERIAL_INGEST_OCCURRED_KIND,
        {
            "source_role": "operator",
            "dimensions": {"identity": "operator-result"},
            "known_loss": ["third", "later"],
            "unknowns": ["third", "second"],
            "conflicts": ["middle", "right"],
        },
        locality_identity="s",
    )

    update_operator_ingest_standing(attempts, first)
    update_operator_ingest_standing(attempts, second)

    standing = attempts["operator-result"]
    assert standing["known_loss"] == ["later", "earlier", "third"]
    assert standing["unknowns"] == ["second", "first", "third"]
    assert standing["conflicts"] == ["right", "left", "middle"]
