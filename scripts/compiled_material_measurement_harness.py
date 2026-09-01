#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from seed_runtime.byte_measurement import (
    record_byte_measurement_subject_to_act_binding,
    record_byte_measurement_act_occurrence,
    record_byte_measurement_result,
)
from seed_runtime.events import EventLedger
from seed_runtime.witness_material_source import (
    record_witness_material_source,
)
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates

from compiled_format_invocation import (
    admission_result_added_position_occurrences,
    exact_byte_material_references,
)
from compiled_material_invocation import (
    MaterialImplementationFunction,
    admit_invocation_occurrences,
    admit_invocation_rows,
    admit_invocation_return_occurrences,
    compare_added_material_invocations,
    reference_occurrences_across,
)


ROOT = Path(__file__).resolve().parent.parent
COMPILED_EXECUTABLE = ROOT / ".venv" / "bin" / "piper"
COMPILED_MATERIAL = (
    Path.home() / ".local" / "share" / "piper-voices" / "en_US-lessac-medium.onnx"
)


def measured_material():
    ledger = EventLedger()
    record_witness_material_source(
        ledger,
        locality_identity="compiled-material-source",
        exact_bytes=bytes(range(256)),
        source_boundary="one-byte material test boundary",
    )
    binding = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=("compiled-material-source",),
        recording_locality_identity="compiled-material-measurement",
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity="compiled-material-measurement"
        ),
    )
    act_occurrence = record_byte_measurement_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity="compiled-material-measurement"
        ),
    )
    occurrence = record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    return ledger, exact_byte_material_references(ledger, occurrence.identity)


def measure(
    implementation_function: MaterialImplementationFunction,
    references,
    *,
    time_boundary_second_count: float,
    max_workers: int,
):
    occurrences = reference_occurrences_across(
        references,
        boundary_identity="compiled-material-invocation",
        implementation_functions=(implementation_function,),
        max_workers=max_workers,
        time_boundary_second_count=time_boundary_second_count,
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


def measure_functions(
    implementation_functions: tuple[MaterialImplementationFunction, ...],
    references,
    *,
    boundary_identity: str,
    time_boundary_second_count: float,
    max_workers: int,
    material_byte_count_boundary: int,
):
    occurrences = reference_occurrences_across(
        references,
        boundary_identity=f"{boundary_identity}-invocation",
        implementation_functions=implementation_functions,
        max_workers=max_workers,
        time_boundary_second_count=time_boundary_second_count,
        material_byte_count_boundary=material_byte_count_boundary,
    )
    admission = admit_invocation_rows(
        occurrences,
        boundary_identity=f"{boundary_identity}-admission",
    )
    return occurrences, admission


def measure_added_material(
    implementation_functions: tuple[MaterialImplementationFunction, ...],
    source_references,
    added_references,
    *,
    boundary_identity: str,
    time_boundary_second_count: float,
    max_workers: int,
    material_byte_count_boundary: int,
    act_occurrence_count_boundary: int,
):
    source_occurrences, source_admission = measure_functions(
        implementation_functions,
        source_references,
        boundary_identity=f"{boundary_identity}-source",
        time_boundary_second_count=time_boundary_second_count,
        max_workers=max_workers,
        material_byte_count_boundary=material_byte_count_boundary,
    )
    _, added_admission = measure_functions(
        implementation_functions,
        added_references,
        boundary_identity=f"{boundary_identity}-added",
        time_boundary_second_count=time_boundary_second_count,
        max_workers=max_workers,
        material_byte_count_boundary=material_byte_count_boundary,
    )
    additions = admission_result_added_position_occurrences(
        source_admission.result_reference,
        added_admission.result_reference,
        boundary_identity=f"{boundary_identity}-addition",
        admitted_material_act_occurrence_count_boundary=act_occurrence_count_boundary,
    )
    result_occurrences = reference_occurrences_across(
        tuple(addition.result_reference for addition in additions),
        boundary_identity=f"{boundary_identity}-result",
        implementation_functions=implementation_functions,
        max_workers=max_workers,
        time_boundary_second_count=time_boundary_second_count,
        material_byte_count_boundary=material_byte_count_boundary,
    )
    comparisons = compare_added_material_invocations(
        additions,
        source_occurrences,
        result_occurrences,
        boundary_identity=f"{boundary_identity}-compare",
    )
    return additions, source_occurrences, result_occurrences, comparisons


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
        time_boundary_second_count=31.0,
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
