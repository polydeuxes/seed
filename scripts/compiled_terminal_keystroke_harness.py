#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material

from compiled_material_invocation import (
    IngestResultReference,
    MaterialAdmissionOccurrence,
    MaterialImplementationFunction,
    MaterialInvocationOccurrence,
    admit_invocation_occurrences,
    ingest_result_reference,
    reference_occurrences_across,
)


PTY_READLINE_IMPLEMENTATION_FUNCTION = MaterialImplementationFunction(
    identity="compiled-pty-readline-0",
    invocation=(
        "/usr/bin/env",
        "-i",
        "TERM=dumb",
        "HOME=/tmp",
        "PS1=",
        "PS2=",
        "/usr/bin/script",
        "-qefc",
        "/bin/bash --noprofile --norc -i",
        "/dev/null",
    ),
)


@dataclass(frozen=True, slots=True)
class TerminalMaterialAcquisition:
    ledger: EventLedger
    ingest_occurrences: tuple[Event, ...]
    source_references: tuple[IngestResultReference, ...]
    implementation_function: MaterialImplementationFunction
    invocation_occurrences: tuple[MaterialInvocationOccurrence, ...]
    admission_occurrence: MaterialAdmissionOccurrence


def acquire_terminal_material(
    exact_material: tuple[bytes, ...],
    *,
    boundary_identity: str,
    material_occurrence_count_limit: int,
    time_limit_second_count: float,
    output_material_byte_count_limit: int,
) -> TerminalMaterialAcquisition:
    if (
        type(exact_material) is not tuple
        or not exact_material
        or any(type(material) is not bytes for material in exact_material)
    ):
        raise TypeError("terminal source requires one nonempty exact tuple of bytes")
    if (
        type(material_occurrence_count_limit) is not int
        or material_occurrence_count_limit < 1
    ):
        raise TypeError("one exact positive material occurrence count limit is required")
    if len(exact_material) > material_occurrence_count_limit:
        raise ValueError("terminal material exceeds its exact occurrence count limit")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")

    ledger = EventLedger()
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity=f"{boundary_identity}-source",
            exact_bytes=material,
            source_role="operator supplied material",
            source_boundary=f"{boundary_identity}-source-{position}",
        )
        for position, material in enumerate(exact_material)
    )
    references = tuple(
        ingest_result_reference(ledger, occurrence.identity)
        for occurrence in ingests
    )
    occurrences = reference_occurrences_across(
        references,
        boundary_identity=f"{boundary_identity}-invocation",
        implementation_functions=(PTY_READLINE_IMPLEMENTATION_FUNCTION,),
        max_workers=1,
        time_limit_second_count=time_limit_second_count,
        material_byte_count_limit=output_material_byte_count_limit,
    )[0]
    admission = admit_invocation_occurrences(
        occurrences,
        boundary_identity=f"{boundary_identity}-admission",
    )
    return TerminalMaterialAcquisition(
        ledger=ledger,
        ingest_occurrences=ingests,
        source_references=references,
        implementation_function=PTY_READLINE_IMPLEMENTATION_FUNCTION,
        invocation_occurrences=occurrences,
        admission_occurrence=admission,
    )
