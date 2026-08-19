from __future__ import annotations

from pathlib import Path
import sys

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
)
from seed_runtime.material_acquisition import acquired_material_bytes
from seed_runtime.witness_material_acquisition import WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND


FIDELITY_SUBJECT = "material_measurement_witness"


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from book_material_measurement import measured_book_material  # noqa: E402


def test_book_material_acquisition_and_measurement_references_keep_their_exact_lineage():
    ledger, pair_references, byte_references = measured_book_material()
    paths = tuple(
        path
        for path in (ROOT / "book_of_seed").rglob("*")
        if path.is_file()
    )
    acquisition_results = tuple(
        occurrence
        for occurrence in ledger.list()
        if occurrence.kind == WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
    )

    assert tuple(acquired_material_bytes(acquisition_result) for acquisition_result in acquisition_results) == tuple(
        path.read_bytes() for path in paths
    )
    assert tuple(acquisition_result.material["source_boundary"] for acquisition_result in acquisition_results) == tuple(
        str(path.relative_to(ROOT)) for path in paths
    )
    assert {acquisition_result.locality_identity for acquisition_result in acquisition_results} == {"book-material"}

    byte_occurrence_identities = {
        reference.recorded_occurrence_identity for reference in byte_references
    }
    pair_occurrence_identities = {
        reference.recorded_occurrence_identity for reference in pair_references
    }
    assert len(byte_occurrence_identities) == len(pair_occurrence_identities) == 1
    byte_occurrence = ledger.get(next(iter(byte_occurrence_identities)))
    pair_occurrence = ledger.get(next(iter(pair_occurrence_identities)))

    assert byte_occurrence is not None
    assert byte_occurrence.kind == BYTE_MEASUREMENT_RECORDED_KIND
    assert byte_occurrence.locality_identity == "book-byte-measurement"
    assert byte_occurrence.material["source_localities"] == ["book-material"]
    assert pair_occurrence is not None
    assert pair_occurrence.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
    assert pair_occurrence.locality_identity == "book-pair-measurement"
    assert pair_occurrence.material["source_localities"] == ["book-material"]
    assert (
        pair_occurrence.material["completeness_boundary"]
        == byte_occurrence.material["completeness_boundary"]
    )
    assert pair_occurrence.material["source_assertion_reference"][
        "recorded_occurrence_identity"
    ] == byte_occurrence.identity

    assert all(
        reference.locality_identity == "book-pair-measurement"
        and reference.locality_movement_event_identity is None
        for reference in pair_references
    )
    assert all(
        reference.locality_identity == "book-pair-measurement"
        and reference.locality_movement_event_identity is not None
        and ledger.get(reference.locality_movement_event_identity).material[
            "source_assertion_reference"
        ]["recorded_occurrence_identity"]
        == byte_occurrence.identity
        and ledger.get(reference.locality_movement_event_identity).material[
            "source_locality"
        ]
        == "book-byte-measurement"
        and ledger.get(reference.locality_movement_event_identity).material[
            "destination_locality"
        ]
        == "book-pair-measurement"
        for reference in byte_references
    )
