#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from typing import Hashable

from compiled_material_invocation import (
    MaterialImplementationFunction,
    MaterialInvocationOccurrence,
    reference_occurrences_across,
)


def piper_implementation_function(
    *,
    executable: Path,
    model: Path,
    identity: str,
) -> MaterialImplementationFunction:
    if not executable.is_file():
        raise ValueError("Piper implementation function is unavailable")
    if not model.is_file():
        raise ValueError("Piper material is unavailable")
    return MaterialImplementationFunction(
        identity=identity,
        invocation=(
            str(executable),
            "-m",
            str(model),
            "--output-raw",
        ),
    )


def piper_invocations(
    references: tuple[Hashable, ...],
    implementation_functions: tuple[MaterialImplementationFunction, ...],
    *,
    boundary_identity: str,
) -> tuple[tuple[MaterialInvocationOccurrence, ...], ...]:
    return reference_occurrences_across(
        references,
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
        max_workers=1,
    )
