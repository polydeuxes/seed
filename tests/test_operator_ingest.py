"""Every non-EOF byte frame becomes one preserved operator occurrence."""

from __future__ import annotations

from io import BytesIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingest import (
    run_operator_ingest,
    update_operator_ingest_standing,
)
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.operator_material_acquisition import (
    record_operator_material_acquire_responsibility_assignment,
    record_operator_material_acquire_responsible_act_evidence,
    record_operator_material_acquire_result,
)
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_representation import record_operator_representation
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


def test_arbitrary_bytes_are_preserved_as_one_operator_occurrence():
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


def test_empty_line_is_exact_operator_material():
    _, standing = _run(b"\n")

    assert standing["current_standing"]["ingest_occurrence"] is not None


def test_eof_is_not_an_operator_material_occurrence():
    with pytest.raises(ValueError, match="must be non-EOF"):
        _run(b"")


def _acquired_operator_material(ledger, material=b"question\n", *, locality="s"):
    representation = record_operator_representation(
        ledger,
        locality_identity=locality,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    assignment = record_operator_material_acquire_responsibility_assignment(
        ledger,
        locality_identity=locality,
        addressed_representation_event_identity=(
            representation["representation_event_identity"]
        ),
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    act = record_operator_material_acquire_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    boundary = operator_boundary_material(BytesIO(material))
    acquired = record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
        boundary_material=boundary,
    )
    return boundary, acquired


def test_operator_ingest_preserves_its_exact_acquisition_occurrence():
    ledger = EventLedger()
    boundary, acquired = _acquired_operator_material(ledger)

    standing = run_operator_ingest(
        ledger=ledger,
        locality_identity="s",
        boundary_material=boundary,
        operator_material_occurrence_reference=acquired.identity,
    )
    ingest = ledger.get(
        standing["current_standing"]["ingest_occurrence"][
            "evidence_event_identity"
        ]
    )

    assert ingest.material["provenance_occurrence_references"] == [
        acquired.identity
    ]


@pytest.mark.parametrize(
    ("locality", "material"),
    (("other", b"question\n"), ("s", b"different\n")),
)
def test_operator_ingest_refuses_a_crossed_acquisition(locality, material):
    ledger = EventLedger()
    _boundary, acquired = _acquired_operator_material(ledger)

    with pytest.raises(ValueError, match="exact acquired material"):
        run_operator_ingest(
            ledger=ledger,
            locality_identity=locality,
            boundary_material=operator_boundary_material(BytesIO(material)),
            operator_material_occurrence_reference=acquired.identity,
        )


def test_ingest_standing_preserves_first_occurrence_order_without_sorting():
    ledger = EventLedger()
    attempts = {}
    first = ledger.append(
        MATERIAL_INGEST_OCCURRED_KIND,
        {
            "source_role": "operator",
            "dimensions": {"identity": "operator-result"},
            "known_loss": ["later", "earlier"],
            "unknown": ["second", "first"],
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
            "unknown": ["third", "second"],
            "conflicts": ["middle", "right"],
        },
        locality_identity="s",
    )

    update_operator_ingest_standing(attempts, first)
    update_operator_ingest_standing(attempts, second)

    standing = attempts["operator-result"]
    assert standing["known_loss"] == ["later", "earlier", "third"]
    assert standing["unknown"] == ["second", "first", "third"]
    assert standing["conflicts"] == ["right", "left", "middle"]


FIDELITY_SUBJECTS = {
    "current_Locality_Standing": (
        test_current_standing_names_the_exact_ingest_occurrence,
        test_ingest_standing_preserves_first_occurrence_order_without_sorting,
    ),
    "operator_material_occurrence": (
        test_arbitrary_bytes_are_preserved_as_one_operator_occurrence,
        test_empty_line_is_exact_operator_material,
        test_eof_is_not_an_operator_material_occurrence,
        test_operator_ingest_preserves_its_exact_acquisition_occurrence,
        test_operator_ingest_refuses_a_crossed_acquisition,
    ),
}
