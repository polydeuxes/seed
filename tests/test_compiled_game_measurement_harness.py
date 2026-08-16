from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_game_measurement_harness import (  # noqa: E402
    implementation_functions,
    measure_function,
)
from material_fixture_measurement import measured_one_byte_material  # noqa: E402


def test_each_game_function_receives_every_exact_one_byte_material():
    _, references = measured_one_byte_material()
    found = []
    for function in implementation_functions():
        (
            occurrences,
            exact,
            returned,
            additions,
            result_occurrences,
            _,
            result_returned,
            comparisons,
        ) = measure_function(function, references)
        assert tuple(occurrence.source_reference for occurrence in occurrences) == (
            references
        )
        assert exact.source_material == returned.source_material == references
        found.append(returned.admitted_material)
        assert len(comparisons) == len(additions) == len(result_occurrences)
        assert result_returned.source_material == tuple(
            addition.result_reference for addition in additions
        )

    assert len(found) == 4
    assert all(len(admitted_material) > 1 for admitted_material in found)
