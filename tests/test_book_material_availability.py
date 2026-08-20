from __future__ import annotations

from pathlib import Path
import sys

from seed_runtime.material_acquisition import acquired_material_bytes
from seed_runtime.witness_material_acquisition import WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.standing_measurement_declarations import (
    record_declared_measurements_from_current_standing,
)


FIDELITY_SUBJECT = "material_measurement_witness"


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from book_material_availability import acquired_book_material  # noqa: E402


def test_book_material_acquisition_keeps_exact_lineage_without_measurement_pressure():
    ledger, paths, acquisition_results = acquired_book_material()
    assert tuple(acquired_material_bytes(acquisition_result) for acquisition_result in acquisition_results) == tuple(
        path.read_bytes() for path in paths
    )
    assert tuple(acquisition_result.material["source_boundary"] for acquisition_result in acquisition_results) == tuple(
        str(path.relative_to(ROOT)) for path in paths
    )
    assert {acquisition_result.locality_identity for acquisition_result in acquisition_results} == {"book-material"}
    assert all(
        result.kind == WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
        for result in acquisition_results
    )
    bounded_replay = read_operator_locality_standing(
        ledger, locality_identity="book-material"
    )
    assert bounded_replay["operator_material_locality_relation_occurrences"] == {}
    assert bounded_replay["measurement_occurrences"] == {}
    boundary = ledger.append_boundary()
    recorded = record_declared_measurements_from_current_standing(
        ledger, locality_identity="book-material"
    )
    assert recorded.result_occurrences == ()
    assert ledger.append_boundary() == boundary
