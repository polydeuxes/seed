from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_game_measurement_harness import (  # noqa: E402
    implementation_functions,
    measure_added_material,
    measure_material,
)
from material_fixture_measurement import measured_one_byte_material  # noqa: E402


def test_each_game_function_receives_every_exact_one_byte_material():
    _, references = measured_one_byte_material()
    functions = implementation_functions()
    occurrences, exact, returned, exact_compares, return_compares = measure_material(
        functions, references
    )

    assert len(occurrences) == len(exact) == len(returned) == len(functions) == 4
    for position in range(len(functions)):
        assert tuple(
            occurrence.source_reference for occurrence in occurrences[position]
        ) == (
            references
        )
        assert (
            exact[position].source_material
            == returned[position].source_material
            == references
        )
    assert len(exact_compares) == len(return_compares) == 12
    assert {comparison.first_reference for comparison in exact_compares} == {
        admission.result_reference for admission in exact
    }
    assert {comparison.first_reference for comparison in return_compares} == {
        admission.result_reference for admission in returned
    }
    assert all(len(admission.admitted_material) > 1 for admission in returned)

    (
        additions,
        result_occurrences,
        result_exact,
        result_returned,
        comparisons,
        addition_admissions,
        result_exact_compares,
        result_return_compares,
    ) = measure_added_material(functions, references, occurrences, returned)

    assert len({addition.act_occurrence_identity for addition in additions}) == len(
        additions
    )
    assert {
        addition.source_admission_result_reference for addition in additions
    } == {admission.result_reference for admission in returned}
    assert len(result_occurrences) == len(comparisons) == len(functions)
    for position in range(len(functions)):
        assert len(comparisons[position]) == len(additions)
        assert tuple(
            occurrence.source_reference
            for occurrence in result_occurrences[position]
        ) == tuple(
            addition.result_reference for addition in additions
        )
        assert (
            result_exact[position].source_material
            == result_returned[position].source_material
            == tuple(addition.result_reference for addition in additions)
        )
    assert len(addition_admissions) == len(functions) + 1
    assert len(addition_admissions[-1].comparison_occurrences) == len(functions)
    assert len(result_exact_compares) == len(result_return_compares) == 12
