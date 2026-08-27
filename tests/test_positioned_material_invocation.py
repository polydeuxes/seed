from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.witness_material_source import record_witness_material_source


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    exact_position_material_references,
    exact_position_pair_material_references,
)
from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    admit_invocation_occurrences,
    admit_invocation_return_occurrences,
    material_acquisition_result_reference,
    reference_occurrences_across,
)


def _source(ledger, locality_identity, material):
    event = record_witness_material_source(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=material,
        source_boundary=locality_identity,
    )
    return material_acquisition_result_reference(ledger, event.identity)


def test_equal_material_at_different_positions_keeps_each_occurrence():
    ledger = EventLedger()
    source = _source(ledger, "position-source", b"aaa")
    positions = exact_position_material_references(source)
    pairs = exact_position_pair_material_references(positions)

    assert tuple(reference.position for reference in positions) == (0, 1, 2)
    assert tuple(reference.exact_material for reference in positions) == (
        b"a",
        b"a",
        b"a",
    )
    assert len({reference.occurrence_identity for reference in positions}) == 3
    assert tuple(reference.exact_material for reference in pairs) == (b"aa", b"aa")
    assert len({reference.occurrence_identity for reference in pairs}) == 2
    assert {reference.locality_identity for reference in (*positions, *pairs)} == {
        source.locality_identity
    }


def test_exact_position_pairs_pair_again_at_the_exact_next_position():
    ledger = EventLedger()
    source = _source(ledger, "position-source", b"abcde")
    positions = exact_position_material_references(source)
    pairs = exact_position_pair_material_references(positions)
    paired_pairs = exact_position_pair_material_references(pairs)

    assert tuple(reference.exact_material for reference in pairs) == (
        b"ab",
        b"bc",
        b"cd",
        b"de",
    )
    assert tuple(reference.exact_material for reference in paired_pairs) == (
        b"abcd",
        b"bcde",
    )
    assert tuple(reference.first_position for reference in paired_pairs) == (0, 1)
    assert tuple(reference.last_position for reference in paired_pairs) == (3, 4)
    assert len({reference.occurrence_identity for reference in paired_pairs}) == 2
    assert all(reference.source_reference == source for reference in paired_pairs)


def test_position_pair_refuses_reordered_or_cross_locality_material():
    ledger = EventLedger()
    first_source = _source(ledger, "position-source-a", b"aaa")
    second_source = _source(ledger, "position-source-b", b"aaa")
    first = exact_position_material_references(first_source)
    second = exact_position_material_references(second_source)
    pair = exact_position_pair_material_references(first)[0]

    with pytest.raises(ValueError, match="exact source order"):
        replace(pair, second_reference=first[2])
    with pytest.raises(ValueError, match="cross source material"):
        replace(pair, second_reference=second[1])


def test_position_pair_admission_preserves_equal_occurrence_references():
    ledger = EventLedger()
    source = _source(ledger, "position-source", b"aaa")
    pairs = exact_position_pair_material_references(
        exact_position_material_references(source)
    )
    occurrences = reference_occurrences_across(
        pairs,
        boundary_identity="position-pair-invocation",
        implementation_functions=(
            MaterialImplementationFunction(
                identity="compiled-0",
                invocation=("/bin/cat",),
            ),
        ),
        max_workers=1,
    )[0]
    exact = admit_invocation_occurrences(
        occurrences,
        boundary_identity="position-pair-exact-admission",
    )
    returned = admit_invocation_return_occurrences(
        occurrences,
        boundary_identity="position-pair-return-admission",
    )

    assert tuple(occurrence.source_reference for occurrence in occurrences) == pairs
    assert exact.admitted_material == returned.admitted_material == (pairs,)
    assert len({reference.occurrence_identity for reference in pairs}) == len(pairs)




WITNESSED_BOOK_COORDINATES = {
    ("book_coordinates", "01.Source.D", "result"): (
        test_equal_material_at_different_positions_keeps_each_occurrence,
        test_exact_position_pairs_pair_again_at_the_exact_next_position,
    ),
}
