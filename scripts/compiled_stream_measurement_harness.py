#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from compiled_material_invocation import MaterialImplementationFunction
from book_material_measurement import measured_book_material
from compiled_material_measurement_harness import (
    measure,
    measure_added_material,
    measure_functions,
)


EXECUTABLE = Path("/usr/bin/ffmpeg")


def implementation_functions() -> tuple[MaterialImplementationFunction, ...]:
    common = (
        str(EXECUTABLE),
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-protocol_whitelist",
        "pipe,data",
    )
    stream_functions = tuple(
        MaterialImplementationFunction(
            identity=f"compiled-{position}",
            invocation=(
                *common,
                *(("-f", material_kind) if material_kind is not None else ()),
                "-i",
                "pipe:0",
                "-f",
                "null",
                "-",
            ),
        )
        for position, material_kind in enumerate((None, "mpegts", "hls", "dash"))
    )
    caca = MaterialImplementationFunction(
        identity=f"compiled-{len(stream_functions)}",
        invocation=(
            "/bin/sh",
            "-c",
            "/usr/bin/ffmpeg -nostdin -hide_banner -loglevel error "
            "-protocol_whitelist pipe,data -i pipe:0 -vf format=rgb24 "
            "-frames:v 1 -f caca - | head -c 2048",
        ),
    )
    return (*stream_functions, caca)


def main() -> int:
    if not EXECUTABLE.is_file():
        return 2
    _, references, _ = measured_book_material()
    found = []
    for implementation_function in implementation_functions():
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
