#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from compiled_format_invocation import (
    added_position_admission_occurrences,
    admission_added_position_occurrences,
)
from compiled_material_invocation import (
    MaterialImplementationFunction,
    admit_invocation_occurrences,
    admit_invocation_return_occurrences,
    compare_added_material_invocations,
    reference_occurrences_across,
)
from compiled_material_measurement_harness import measured_material
from material_admission import compare_admission_result_pairs


def implementation_functions() -> tuple[MaterialImplementationFunction, ...]:
    tests = SCRIPT_DIRECTORY.parent / "tests"
    return (
        MaterialImplementationFunction(
            identity="compiled-0",
            invocation=(
                sys.executable,
                "-I",
                str(tests / "compiled_tic_tac_toe.py"),
            ),
        ),
        MaterialImplementationFunction(
            identity="compiled-1",
            invocation=(
                sys.executable,
                "-I",
                str(tests / "compiled_connect_four.py"),
            ),
        ),
        MaterialImplementationFunction(
            identity="compiled-2",
            invocation=(
                sys.executable,
                "-I",
                str(tests / "compiled_micro_go.py"),
            ),
        ),
        MaterialImplementationFunction(
            identity="compiled-3",
            invocation=("/usr/bin/env", "-i", "/usr/games/hoichess", "-x"),
        ),
        MaterialImplementationFunction(
            identity="compiled-4",
            invocation=("/usr/bin/env", "-i", "/usr/games/hoixiangqi", "-x"),
        ),
    )


def measure_material(implementation_functions, references):
    occurrences = reference_occurrences_across(
        references,
        boundary_identity="game-material-invocation",
        implementation_functions=implementation_functions,
        time_limit_second_count=5.0,
        max_workers=8,
    )
    exact = tuple(
        admit_invocation_occurrences(
            row,
            boundary_identity="game-material-exact-admission",
            occurrence_position=position,
        )
        for position, row in enumerate(occurrences)
    )
    returned = tuple(
        admit_invocation_return_occurrences(
            row,
            boundary_identity="game-material-return-admission",
            occurrence_position=position,
        )
        for position, row in enumerate(occurrences)
    )
    exact_compares = compare_admission_result_pairs(
        tuple(admission.result_reference for admission in exact),
        boundary_identity="game-material-exact-admission-compare",
    )
    return_compares = compare_admission_result_pairs(
        tuple(admission.result_reference for admission in returned),
        boundary_identity="game-material-return-admission-compare",
    )
    return occurrences, exact, returned, exact_compares, return_compares


def measure_added_material(
    implementation_functions,
    references,
    source_occurrences,
    returned_admissions,
):
    additions = tuple(
        addition
        for admission_position, admission in enumerate(returned_admissions)
        for addition in admission_added_position_occurrences(
            admission.result_reference,
            boundary_identity=f"game-material-addition-{admission_position}",
            admitted_material_act_occurrence_count_limit=len(references) ** 2,
        )
    )
    result_occurrences = reference_occurrences_across(
        tuple(addition.result_reference for addition in additions),
        boundary_identity="game-added-material-invocation",
        implementation_functions=implementation_functions,
        time_limit_second_count=5.0,
        max_workers=8,
    )
    result_exact = tuple(
        admit_invocation_occurrences(
            row,
            boundary_identity="game-added-material-exact-admission",
            occurrence_position=position,
        )
        for position, row in enumerate(result_occurrences)
    )
    result_returned = tuple(
        admit_invocation_return_occurrences(
            row,
            boundary_identity="game-added-material-return-admission",
            occurrence_position=position,
        )
        for position, row in enumerate(result_occurrences)
    )
    comparisons = compare_added_material_invocations(
        additions,
        source_occurrences,
        result_occurrences,
        boundary_identity="game-added-material-compare",
    )
    addition_admissions = added_position_admission_occurrences(
        additions,
        comparisons,
        boundary_identity="game-added-material-admission",
    )
    exact_compares = compare_admission_result_pairs(
        tuple(admission.result_reference for admission in result_exact),
        boundary_identity="game-added-material-exact-admission-compare",
    )
    return_compares = compare_admission_result_pairs(
        tuple(admission.result_reference for admission in result_returned),
        boundary_identity="game-added-material-return-admission-compare",
    )
    return (
        additions,
        result_occurrences,
        result_exact,
        result_returned,
        comparisons,
        addition_admissions,
        exact_compares,
        return_compares,
    )


def main() -> int:
    _, references = measured_material()
    functions = implementation_functions()
    for implementation_function in functions:
        if not Path(implementation_function.invocation[0]).is_file():
            return 2
    occurrences, exact, returned, _, _ = measure_material(functions, references)
    additions, _, _, result_returned, _, _, _, _ = measure_added_material(
        functions,
        references,
        occurrences,
        returned,
    )
    print(
        tuple(
            (
                function.identity,
                len(occurrences[position]),
                tuple(len(material) for material in exact[position].admitted_material),
                tuple(
                    len(material) for material in returned[position].admitted_material
                ),
                len(additions),
                tuple(
                    len(material)
                    for material in result_returned[position].admitted_material
                ),
            )
            for position, function in enumerate(functions)
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
