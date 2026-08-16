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
    compare_added_material_return_invocations,
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
        MaterialImplementationFunction(
            identity="compiled-5",
            invocation=("/usr/bin/env", "-i", "/usr/games/gnugo", "--mode", "gtp"),
        ),
        MaterialImplementationFunction(
            identity="compiled-6",
            invocation=("/usr/bin/env", "-i", "/usr/games/stockfish"),
        ),
        MaterialImplementationFunction(
            identity="compiled-7",
            invocation=("/usr/bin/env", "-i", "/usr/games/fairy-stockfish"),
        ),
        MaterialImplementationFunction(
            identity="compiled-8",
            invocation=("/usr/bin/env", "-i", "/usr/games/ethereal-chess"),
        ),
        MaterialImplementationFunction(
            identity="compiled-9",
            invocation=("/usr/bin/env", "-i", "/usr/games/glaurung"),
        ),
        MaterialImplementationFunction(
            identity="compiled-10",
            invocation=("/usr/bin/env", "-i", "/usr/games/gtp-rhino"),
        ),
        MaterialImplementationFunction(
            identity="compiled-11",
            invocation=(
                "/usr/bin/env",
                "-i",
                "/usr/bin/qqwing",
                "--solve",
                "--one-line",
            ),
        ),
        MaterialImplementationFunction(
            identity="compiled-12",
            invocation=("/usr/bin/env", "-i", "/usr/games/mancala", "0"),
        ),
        MaterialImplementationFunction(
            identity="compiled-13",
            invocation=("/usr/bin/env", "-i", "/usr/games/backgammon"),
        ),
        MaterialImplementationFunction(
            identity="compiled-14",
            invocation=("/usr/bin/env", "-i", "/usr/bin/bc", "-q"),
        ),
        MaterialImplementationFunction(
            identity="compiled-15",
            invocation=("/usr/bin/env", "-i", "/usr/games/nbcheckers"),
        ),
        MaterialImplementationFunction(
            identity="compiled-16",
            invocation=(
                "/usr/bin/env",
                "-i",
                "/usr/bin/script",
                "-qefc",
                "/usr/games/nbcheckers",
                "/dev/null",
            ),
        ),
        MaterialImplementationFunction(
            identity="compiled-17",
            invocation=(
                "/usr/bin/env",
                "-i",
                "TERM=dumb",
                "/usr/bin/script",
                "-qefc",
                "/usr/games/nbcheckers",
                "/dev/null",
            ),
        ),
        MaterialImplementationFunction(
            identity="compiled-18",
            invocation=(
                "/usr/bin/env",
                "-i",
                "TERM=xterm",
                "/usr/bin/script",
                "-qefc",
                "/usr/games/nbcheckers",
                "/dev/null",
            ),
        ),
    )


def measure_material(
    implementation_functions,
    references,
    *,
    boundary_identity,
    time_limit_second_count,
):
    occurrences = reference_occurrences_across(
        references,
        boundary_identity=f"{boundary_identity}-invocation",
        implementation_functions=implementation_functions,
        time_limit_second_count=time_limit_second_count,
        material_byte_count_limit=4096,
        max_workers=8,
    )
    exact = tuple(
        admit_invocation_occurrences(
            row,
            boundary_identity=f"{boundary_identity}-exact-admission",
            occurrence_position=position,
        )
        for position, row in enumerate(occurrences)
    )
    returned = tuple(
        admit_invocation_return_occurrences(
            row,
            boundary_identity=f"{boundary_identity}-return-admission",
            occurrence_position=position,
        )
        for position, row in enumerate(occurrences)
    )
    return occurrences, exact, returned


def measure_material_time_counts(
    implementation_functions,
    references,
    time_limit_second_counts,
):
    if (
        type(time_limit_second_counts) is not tuple
        or len(time_limit_second_counts) < 2
        or len(set(time_limit_second_counts)) != len(time_limit_second_counts)
        or any(
            type(second_count) is not float or second_count <= 0
            for second_count in time_limit_second_counts
        )
    ):
        raise TypeError("distinct positive time limit second counts are required")
    measurements = tuple(
        (
            second_count,
            *measure_material(
                implementation_functions,
                references,
                boundary_identity=f"compiled-material-{position}",
                time_limit_second_count=second_count,
            ),
        )
        for position, second_count in enumerate(time_limit_second_counts)
    )
    exact_references = tuple(
        admission.result_reference
        for _, _, exact, _ in measurements
        for admission in exact
    )
    return_references = tuple(
        admission.result_reference
        for _, _, _, returned in measurements
        for admission in returned
    )
    exact_compares = compare_admission_result_pairs(
        exact_references,
        boundary_identity="compiled-material-time-exact-admission-compare",
    )
    return_compares = compare_admission_result_pairs(
        return_references,
        boundary_identity="compiled-material-time-return-admission-compare",
    )
    return measurements, exact_compares, return_compares


def measure_added_material(
    implementation_functions,
    references,
    source_occurrences,
    returned_admissions,
    *,
    time_limit_second_count,
    act_occurrence_count_limit,
):
    if (
        type(act_occurrence_count_limit) is not int
        or act_occurrence_count_limit < 1
    ):
        raise TypeError("one exact positive Act occurrence count limit is required")
    found_additions = []
    for admission_position, admission in enumerate(returned_admissions):
        found = admission_added_position_occurrences(
            admission.result_reference,
            boundary_identity=f"compiled-material-addition-{admission_position}",
            admitted_material_act_occurrence_count_limit=act_occurrence_count_limit,
        )
        if len(found_additions) + len(found) > act_occurrence_count_limit:
            raise ValueError("addition Act occurrences exceed their exact count limit")
        found_additions.extend(found)
    additions = tuple(found_additions)
    result_occurrences = reference_occurrences_across(
        tuple(addition.result_reference for addition in additions),
        boundary_identity="compiled-added-material-invocation",
        implementation_functions=implementation_functions,
        time_limit_second_count=time_limit_second_count,
        material_byte_count_limit=4096,
        max_workers=8,
    )
    result_exact = tuple(
        admit_invocation_occurrences(
            row,
            boundary_identity="compiled-added-material-exact-admission",
            occurrence_position=position,
        )
        for position, row in enumerate(result_occurrences)
    )
    result_returned = tuple(
        admit_invocation_return_occurrences(
            row,
            boundary_identity="compiled-added-material-return-admission",
            occurrence_position=position,
        )
        for position, row in enumerate(result_occurrences)
    )
    comparisons = compare_added_material_invocations(
        additions,
        source_occurrences,
        result_occurrences,
        boundary_identity="compiled-added-material-compare",
    )
    return_comparisons = compare_added_material_return_invocations(
        additions,
        source_occurrences,
        result_occurrences,
        boundary_identity="compiled-added-material-return-compare",
    )
    addition_admissions = added_position_admission_occurrences(
        additions,
        comparisons,
        boundary_identity="compiled-added-material-admission",
    )
    return_addition_admissions = added_position_admission_occurrences(
        additions,
        return_comparisons,
        boundary_identity="compiled-added-material-return-admission",
    )
    exact_compares = compare_admission_result_pairs(
        tuple(admission.result_reference for admission in result_exact),
        boundary_identity="compiled-added-material-exact-admission-compare",
    )
    return_compares = compare_admission_result_pairs(
        tuple(admission.result_reference for admission in result_returned),
        boundary_identity="compiled-added-material-return-admission-compare",
    )
    return (
        additions,
        result_occurrences,
        result_exact,
        result_returned,
        comparisons,
        return_comparisons,
        addition_admissions,
        return_addition_admissions,
        exact_compares,
        return_compares,
    )


def measure_material_and_act_results(
    implementation_functions,
    references,
    additions,
    *,
    time_limit_second_count,
):
    all_references = references + tuple(
        addition.result_reference for addition in additions
    )
    occurrences, exact, returned = measure_material(
        implementation_functions,
        all_references,
        boundary_identity="compiled-material-and-act-results",
        time_limit_second_count=time_limit_second_count,
    )
    exact_compares = compare_admission_result_pairs(
        tuple(admission.result_reference for admission in exact),
        boundary_identity="compiled-material-and-act-results-exact-compare",
    )
    return_compares = compare_admission_result_pairs(
        tuple(admission.result_reference for admission in returned),
        boundary_identity="compiled-material-and-act-results-return-compare",
    )
    return (
        all_references,
        occurrences,
        exact,
        returned,
        exact_compares,
        return_compares,
    )


def main() -> int:
    _, references = measured_material()
    functions = implementation_functions()
    for implementation_function in functions:
        if not Path(implementation_function.invocation[0]).is_file():
            return 2
    measurements, _, _ = measure_material_time_counts(
        functions,
        references,
        (0.0078125, 0.03125, 0.25),
    )
    second_count, source_occurrences, _, _ = measurements[0]
    _, occurrences, exact, returned = measurements[-1]
    (
        additions,
        _,
        _,
        result_returned,
        _,
        _,
        _,
        return_addition_admissions,
        _,
        _,
    ) = measure_added_material(
        functions,
        references,
        source_occurrences,
        returned,
        time_limit_second_count=second_count,
        act_occurrence_count_limit=len(references) * len(functions),
    )
    measure_material_and_act_results(
        functions,
        references,
        additions,
        time_limit_second_count=second_count,
    )
    print(
        (
            tuple(
                (
                    function.identity,
                    len(occurrences[position]),
                    tuple(
                        len(material)
                        for material in exact[position].admitted_material
                    ),
                    tuple(
                        len(material)
                        for material in returned[position].admitted_material
                    ),
                    len(additions),
                    tuple(
                        len(material)
                        for material in result_returned[position].admitted_material
                    ),
                )
                for position, function in enumerate(functions)
            ),
            tuple(
                len(material)
                for material in return_addition_admissions[-1].admitted_material
            ),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
