#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from compiled_material_invocation import MaterialImplementationFunction
from compiled_material_measurement_harness import measure
from compiled_format_invocation import exact_byte_pair_material_references
from seed_runtime.byte_measurement import (
    record_byte_count_layer,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


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


def measured_material():
    ledger = EventLedger()
    paths = tuple(
        path
        for path in sorted((SCRIPT_DIRECTORY.parent / "book_of_seed").rglob("*"))
        if path.is_file()
    )
    for path in paths:
        ingest_material(
            ledger,
            locality_identity="book-material",
            exact_bytes=path.read_bytes(),
            source_role="fixture material",
            source_boundary=str(path.relative_to(SCRIPT_DIRECTORY.parent)),
        )
    byte_occurrence = record_byte_count_layer(
        ledger,
        source_locality_identities=("book-material",),
        recording_locality_identity="book-byte-measurement",
    )
    pair_occurrence = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_occurrence.identity,
        recording_locality_identity="book-pair-measurement",
    )
    return (
        ledger,
        exact_byte_pair_material_references(ledger, pair_occurrence.identity),
    )
def main() -> int:
    if not EXECUTABLE.is_file():
        return 2
    _, references = measured_material()
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
