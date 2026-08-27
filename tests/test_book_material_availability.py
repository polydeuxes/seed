"""This Book material is addressed by each declared Measurement."""

from __future__ import annotations

from pathlib import Path
import sys

from seed_runtime.material_source import exact_material_result_bytes
from seed_runtime.witness_material_source import WITNESS_MATERIAL_SOURCE_RECORDED_KIND
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates
from seed_runtime.declared_measurements import (
    record_declared_measurements_from_current_coordinates,
)




ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from book_material_availability import recorded_book_material  # noqa: E402


def test_book_material_locality_exposes_declared_measurements():
    ledger, paths, material_results = recorded_book_material()
    assert tuple(exact_material_result_bytes(result) for result in material_results) == tuple(
        path.read_bytes() for path in paths
    )
    assert tuple(result.material["source_boundary"] for result in material_results) == tuple(
        str(path.relative_to(ROOT)) for path in paths
    )
    assert {result.locality_identity for result in material_results} == {"book-material"}
    assert all(
        result.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND
        for result in material_results
    )
    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity="book-material"
    )
    assert current_coordinates["material_result_occurrences"]
    assert current_coordinates["measurement_occurrences"] == {}
    recorded = record_declared_measurements_from_current_coordinates(
        ledger, locality_identity="book-material"
    )
    assert recorded.result_occurrences
    assert len(recorded.result_occurrences) == len(material_results) + 1
    assert set(recorded.current_coordinates["measurement_occurrences"]) == {
        result.identity for result in recorded.result_occurrences
    }
