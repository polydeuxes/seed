from __future__ import annotations

from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_surf_invocation import (  # noqa: E402
    SURF_IMPLEMENTATION_FUNCTIONS,
    surf_invocation_occurrences,
)


FIDELITY_SUBJECT = "compiled_material_invocation_witness"

pytestmark = pytest.mark.skipif(
    not Path("/usr/bin/surf").is_file(),
    reason="one compiled implementation function is absent",
)


def test_exact_material_reaches_each_surf_invocation_occurrence():
    exact_material = b"\x00surf\xff"

    occurrences = surf_invocation_occurrences(
        exact_material,
        boundary_identity="surf-first-invocations",
    )

    assert len(occurrences) == len(SURF_IMPLEMENTATION_FUNCTIONS)
    assert len({occurrence.occurrence_identity for occurrence in occurrences}) == len(
        occurrences
    )
    assert all(occurrence.exact_material == exact_material for occurrence in occurrences)
    assert len({occurrence.coordinates for occurrence in occurrences}) > 1


def test_surf_invocations_preserve_equal_and_different_result_coordinates():
    occurrences = surf_invocation_occurrences(
        b"",
        boundary_identity="surf-result-coordinates",
    )

    coordinates = tuple(occurrence.coordinates for occurrence in occurrences)
    assert 1 < len(set(coordinates)) < len(coordinates)
    assert all(
        occurrence.time_limit_second_count == 2.0
        and occurrence.material_byte_count_limit == 65536
        for occurrence in occurrences
    )
