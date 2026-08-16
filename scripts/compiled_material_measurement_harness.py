#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from seed_runtime.byte_measurement import record_byte_count_layer
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material

from compiled_format_invocation import exact_byte_material_references
from compiled_material_invocation import (
    MaterialImplementationFunction,
    admit_invocation_occurrences,
    admit_invocation_return_occurrences,
    reference_occurrences_across,
)


ROOT = Path(__file__).resolve().parent.parent
COMPILED_EXECUTABLE = ROOT / ".venv" / "bin" / "piper"
COMPILED_MATERIAL = (
    Path.home() / ".local" / "share" / "piper-voices" / "en_US-lessac-medium.onnx"
)


def measured_material():
    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity="compiled-material-source",
        exact_bytes=bytes(range(256)),
        source_role="fixture material",
        source_boundary="fixture-0",
    )
    occurrence = record_byte_count_layer(
        ledger,
        source_locality_identities=("compiled-material-source",),
        recording_locality_identity="compiled-material-measurement",
    )
    return ledger, exact_byte_material_references(ledger, occurrence.identity)


def measure(
    implementation_function: MaterialImplementationFunction,
    references,
    *,
    time_limit_second_count: float,
    max_workers: int,
):
    occurrences = reference_occurrences_across(
        references,
        boundary_identity="compiled-material-invocation",
        implementation_functions=(implementation_function,),
        max_workers=max_workers,
        time_limit_second_count=time_limit_second_count,
    )[0]
    exact = admit_invocation_occurrences(
        occurrences,
        boundary_identity="compiled-material-exact-admission",
    )
    returned = admit_invocation_return_occurrences(
        occurrences,
        boundary_identity="compiled-material-return-admission",
    )
    return occurrences, exact, returned


def main() -> int:
    if not COMPILED_EXECUTABLE.is_file() or not COMPILED_MATERIAL.is_file():
        return 2
    _, references = measured_material()
    occurrences, exact, returned = measure(
        MaterialImplementationFunction(
            identity="compiled-0",
            invocation=(
                str(COMPILED_EXECUTABLE),
                "-m",
                str(COMPILED_MATERIAL),
                "--output-raw",
            ),
        ),
        references,
        time_limit_second_count=31.0,
        max_workers=2,
    )
    print(
        (
            len(occurrences),
            tuple(len(material) for material in exact.admitted_material),
            tuple(len(material) for material in returned.admitted_material),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
