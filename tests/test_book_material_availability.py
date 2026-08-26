from __future__ import annotations

from pathlib import Path
import sys

from seed_runtime.material_source import exact_material_result_bytes
from seed_runtime.witness_material_source import WITNESS_MATERIAL_SOURCE_RECORDED_KIND
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates
from seed_runtime.declared_measurements import (
    record_declared_measurements_from_current_bounded_locality_replay,
)




ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from book_material_availability import acquired_book_material  # noqa: E402


def test_book_material_acquisition_locality_exposes_declared_measurements():
    ledger, paths, acquisition_results = acquired_book_material()
    assert tuple(exact_material_result_bytes(acquisition_result) for acquisition_result in acquisition_results) == tuple(
        path.read_bytes() for path in paths
    )
    assert tuple(acquisition_result.material["source_boundary"] for acquisition_result in acquisition_results) == tuple(
        str(path.relative_to(ROOT)) for path in paths
    )
    assert {acquisition_result.locality_identity for acquisition_result in acquisition_results} == {"book-material"}
    assert all(
        result.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND
        for result in acquisition_results
    )
    bounded_replay = read_operator_current_coordinates(
        ledger, locality_identity="book-material"
    )
    assert bounded_replay["material_locality_relation_occurrences"]
    assert bounded_replay["measurement_occurrences"] == {}
    recorded = record_declared_measurements_from_current_bounded_locality_replay(
        ledger, locality_identity="book-material"
    )
    assert recorded.result_occurrences
    assert len(recorded.result_occurrences) == len(acquisition_results) + 1
    assert set(recorded.bounded_locality_replay["measurement_occurrences"]) == {
        result.identity for result in recorded.result_occurrences
    }
