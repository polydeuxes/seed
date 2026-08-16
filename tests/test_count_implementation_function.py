from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import material_admission  # noqa: E402
from compiled_format_invocation import (  # noqa: E402
    ExactMaterialReference,
    added_position_occurrences,
    preserves_original_order,
)
from count_implementation_function import count_invocation  # noqa: E402


def test_absent_material_returns_zero_without_entering_returned_material():
    occurrence = count_invocation(b"a", b"b")

    assert occurrence.exact_material == b"a"
    assert occurrence.addressed_material == b"b"
    assert occurrence.coordinates == (0, b"a")


def test_one_added_position_changes_both_returned_coordinates():
    source = ExactMaterialReference(
        "source-occurrence", "source-assertion", "fixture-locality", b"a"
    )
    added = ExactMaterialReference(
        "added-occurrence", "added-assertion", "fixture-locality", b"b"
    )
    added_occurrences = added_position_occurrences(
        (source,), (added,), boundary_identity="count-addition"
    )
    occurrences = tuple(
        count_invocation(occurrence.result_material, b"b")
        for occurrence in added_occurrences
    )

    assert tuple(occurrence.result_material for occurrence in added_occurrences) == (
        b"ba",
        b"ab",
    )
    assert all(
        preserves_original_order(
            source_material=occurrence.source_material,
            result_material=occurrence.result_material,
            added_position=occurrence.position,
        )
        for occurrence in added_occurrences
    )
    assert tuple(occurrence.coordinates for occurrence in occurrences) == (
        (1, b"ba"),
        (1, b"ab"),
    )


def test_exact_returned_coordinates_perform_admission():
    material = (b"a", b"ba", b"ab")
    admission = material_admission.admission_by(
        lambda exact: count_invocation(exact, b"b").coordinates,
        material,
    )

    assert admission == [(b"a",), (b"ba",), (b"ab",)]


def test_recurrence_changes_count_without_repeating_returned_material():
    once = count_invocation(b"ab", b"b")
    twice = count_invocation(b"abb", b"b")

    assert once.coordinates == (1, b"ab")
    assert twice.coordinates == (2, b"ab")


def test_non_byte_coordinates_are_refused_before_invocation():
    try:
        count_invocation("a", b"b")
    except TypeError as error:
        assert str(error) == "exact material must be bytes"
    else:
        raise AssertionError("non-byte exact material was not refused")

    try:
        count_invocation(b"a", b"bb")
    except TypeError as error:
        assert str(error) == "addressed material must be one byte"
    else:
        raise AssertionError("non-byte addressed material was not refused")
