#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from typing import Hashable

from compiled_material_invocation import (
    MaterialAdmissionOccurrence,
    MaterialImplementationFunction,
    MaterialInvocationOccurrence,
    admit_invocation_occurrences,
    reference_occurrences_across,
)


def piper_implementation_function(
    executable: Path,
    compiled_material: Path,
    *,
    identity: str,
) -> MaterialImplementationFunction:
    return MaterialImplementationFunction(
        identity=identity,
        invocation=(
            str(executable),
            "-m",
            str(compiled_material),
            "--output-raw",
        ),
    )


def piper_material_occurrences(
    references: tuple[Hashable, ...],
    implementation_function: MaterialImplementationFunction,
    *,
    boundary_identity: str,
    time_limit_second_count: float,
    material_byte_count_limit: int,
    max_workers: int,
) -> tuple[
    tuple[MaterialInvocationOccurrence, ...],
    MaterialAdmissionOccurrence,
]:
    rows = reference_occurrences_across(
        references,
        boundary_identity=f"{boundary_identity}-invocation",
        implementation_functions=(implementation_function,),
        time_limit_second_count=time_limit_second_count,
        material_byte_count_limit=material_byte_count_limit,
        max_workers=max_workers,
    )
    occurrences = rows[0]
    admission = admit_invocation_occurrences(
        occurrences,
        boundary_identity=f"{boundary_identity}-admission",
    )
    return occurrences, admission
