#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    invocation_occurrence,
)


SURF_IMPLEMENTATION_FUNCTIONS = (
    MaterialImplementationFunction(
        identity="compiled-0",
        invocation=("/usr/bin/surf", "-v"),
    ),
    MaterialImplementationFunction(
        identity="compiled-1",
        invocation=("/usr/bin/surf", "-h"),
    ),
    MaterialImplementationFunction(
        identity="compiled-2",
        invocation=("/usr/bin/surf", "--"),
    ),
    MaterialImplementationFunction(
        identity="compiled-3",
        invocation=(
            "/usr/bin/env",
            "-i",
            "DISPLAY=",
            "/usr/bin/surf",
            "about:blank",
        ),
    ),
)


def surf_invocation_occurrences(exact_material: bytes, *, boundary_identity: str):
    return tuple(
        invocation_occurrence(
            exact_material,
            implementation_function,
            boundary_identity=boundary_identity,
            invocation_position=position,
            time_limit_second_count=2.0,
            material_byte_count_limit=65536,
        )
        for position, implementation_function in enumerate(
            SURF_IMPLEMENTATION_FUNCTIONS
        )
    )
