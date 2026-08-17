"""Interrogate fixed Surf argv forms without claiming presentation.

This is the `8e8a2557` experiment restored outside Seed Fidelity.  An external
process result can distinguish invocation forms; it does not establish display
access, a rendered frame, or material accepted by an operator boundary.
"""

from __future__ import annotations

from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    invocation_occurrence,
)


IMPLEMENTATION_FUNCTIONS = (
    MaterialImplementationFunction(
        identity="material-witness-surf-version",
        invocation=("/usr/bin/surf", "-v"),
    ),
    MaterialImplementationFunction(
        identity="material-witness-surf-help",
        invocation=("/usr/bin/surf", "-h"),
    ),
    MaterialImplementationFunction(
        identity="material-witness-surf-empty-option",
        invocation=("/usr/bin/surf", "--"),
    ),
    MaterialImplementationFunction(
        identity="material-witness-surf-no-display",
        invocation=(
            "/usr/bin/env",
            "-i",
            "DISPLAY=",
            "/usr/bin/surf",
            "about:blank",
        ),
    ),
)


pytestmark = pytest.mark.skipif(
    not Path("/usr/bin/surf").is_file(),
    reason="the external Surf implementation function is absent",
)


def _observations(exact_material: bytes):
    return tuple(
        invocation_occurrence(
            exact_material,
            implementation_function,
            boundary_identity="surf-material-witness",
            invocation_position=position,
            time_limit_second_count=2.0,
            material_byte_count_limit=65536,
        )
        for position, implementation_function in enumerate(IMPLEMENTATION_FUNCTIONS)
    )


def test_equal_exact_material_reaches_each_external_invocation():
    exact_material = b"\x00surf\xff"
    observations = _observations(exact_material)

    assert len(observations) == len(IMPLEMENTATION_FUNCTIONS)
    assert all(observation.exact_material == exact_material for observation in observations)
    assert len({observation.occurrence_identity for observation in observations}) == len(
        observations
    )


def test_external_results_preserve_equal_and_different_coordinates():
    observations = _observations(b"")
    coordinates = tuple(observation.coordinates for observation in observations)

    assert 1 < len(set(coordinates)) < len(coordinates)
    assert all(
        observation.time_limit_second_count == 2.0
        and observation.material_byte_count_limit == 65536
        for observation in observations
    )
