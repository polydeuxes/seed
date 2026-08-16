#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from compiled_material_invocation import MaterialImplementationFunction
from compiled_material_measurement_harness import measure, measured_material
from compiled_format_invocation import admission_added_position_occurrences
from compiled_material_invocation import compare_added_material_invocations


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
    )


def measure_function(implementation_function, references):
    occurrences, exact, returned = measure(
        implementation_function,
        references,
        time_limit_second_count=5.0,
        max_workers=8,
    )
    additions = admission_added_position_occurrences(
        returned.result_reference,
        boundary_identity=f"{implementation_function.identity}-bounded-addition",
        admitted_material_act_occurrence_count_limit=len(references) ** 2,
    )
    result_occurrences, result_exact, result_returned = measure(
        implementation_function,
        tuple(addition.result_reference for addition in additions),
        time_limit_second_count=5.0,
        max_workers=8,
    )
    comparisons = compare_added_material_invocations(
        additions,
        (occurrences,),
        (result_occurrences,),
        boundary_identity=f"{implementation_function.identity}-bounded-addition-compare",
    )[0]
    return (
        occurrences,
        exact,
        returned,
        additions,
        result_occurrences,
        result_exact,
        result_returned,
        comparisons,
    )


def main() -> int:
    _, references = measured_material()
    found = []
    for implementation_function in implementation_functions():
        if not Path(implementation_function.invocation[0]).is_file():
            return 2
        (
            occurrences,
            exact,
            returned,
            additions,
            _,
            _,
            result_returned,
            _,
        ) = measure_function(implementation_function, references)
        found.append(
            (
                implementation_function.identity,
                len(occurrences),
                tuple(len(material) for material in exact.admitted_material),
                tuple(len(material) for material in returned.admitted_material),
                len(additions),
                tuple(
                    len(material)
                    for material in result_returned.admitted_material
                ),
            )
        )
    print(tuple(found))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
