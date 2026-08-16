#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from compiled_material_invocation import MaterialImplementationFunction
from compiled_material_measurement_harness import measure, measured_material


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


def main() -> int:
    _, references = measured_material()
    found = []
    for implementation_function in implementation_functions():
        if not Path(implementation_function.invocation[0]).is_file():
            return 2
        occurrences, exact, returned = measure(
            implementation_function,
            references,
            time_limit_second_count=5.0,
            max_workers=8,
        )
        found.append(
            (
                implementation_function.identity,
                len(occurrences),
                tuple(len(material) for material in exact.admitted_material),
                tuple(len(material) for material in returned.admitted_material),
            )
        )
    print(tuple(found))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
