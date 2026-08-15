from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import shutil
import sys

import pytest

from seed_runtime.byte_measurement import (
    assertions_of_recorded_byte_position_pair_measurement,
    assertions_of_recorded_byte_measurement,
    record_byte_position_pair_count_layer,
    record_byte_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_witness import (  # noqa: E402
    COMPILED_WITNESSES,
    CompiledWitness,
    interrogate,
    interrogate_across,
)
from material_witness_harness import (  # noqa: E402
    MATERIAL_WITNESSES,
    occurrences_across,
    witness_occurrence,
)
from witness_comparison_harness import refines  # noqa: E402


def _witnesses_available():
    return all(
        shutil.which(witness.arguments[0]) is not None
        for witness in MATERIAL_WITNESSES
    )


def _book_paths() -> tuple[Path, ...]:
    return tuple(
        path
        for path in sorted((ROOT / "book_of_seed").rglob("*"))
        if path.is_file()
    )


@pytest.fixture(scope="module")
def measured_book_pairs():
    ledger = EventLedger()
    paths = _book_paths()
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity="book-material",
            exact_bytes=path.read_bytes(),
            source_role="fixture material",
            source_boundary=str(path.relative_to(ROOT)),
        )
        for path in paths
    )
    byte_measurement = record_byte_count_layer(
        ledger,
        source_locality_identities=("book-material",),
        recording_locality_identity="book-byte-measurement",
    )
    pair_measurement = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_measurement.identity,
        recording_locality_identity="book-pair-measurement",
    )
    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair_measurement.identity
    )
    byte_assertions = assertions_of_recorded_byte_measurement(
        ledger, byte_measurement.identity
    )
    pairs = tuple(
        sorted(
            bytes(assertion.representation)
            for assertion in assertions or ()
            if assertion.result == "count" and assertion.representation is not None
        )
    )
    byte_values = tuple(
        sorted(
            assertion.representation
            for assertion in byte_assertions or ()
            if assertion.result == "count" and assertion.representation is not None
        )
    )
    return paths, ingests, assertions, pairs, byte_assertions, byte_values


@pytest.fixture(scope="module")
def book_pair_witness_occurrences(measured_book_pairs):
    return occurrences_across(measured_book_pairs[3])


@pytest.fixture(scope="module")
def book_pair_format_occurrences(measured_book_pairs):
    return interrogate_across(measured_book_pairs[3])


@pytest.fixture(scope="module")
def book_byte_format_comparisons(measured_book_pairs):
    material = measured_book_pairs[5]
    pairs = tuple(bytes((first, second)) for first in material for second in material)
    pair_occurrences = interrogate_across(pairs)
    found = []
    for witness, pair_row in zip(COMPILED_WITNESSES, pair_occurrences):
        pair_returned = {
            tuple(occurrence.exact_material): occurrence.returned
            for occurrence in pair_row
        }
        comparisons = {
            (first, second): (
                tuple(
                    (pair_returned[first, other], pair_returned[second, other])
                    for other in material
                ),
                tuple(
                    (pair_returned[other, first], pair_returned[other, second])
                    for other in material
                ),
            )
            for position, first in enumerate(material)
            for second in material[position + 1 :]
        }
        found.append((witness.identity, pair_returned, comparisons))
    return tuple(found)


@pytest.fixture(scope="module")
def book_three_byte_format_occurrences(
    measured_book_pairs, book_byte_format_comparisons
):
    material = measured_book_pairs[5]
    returned_pairs = frozenset(
        bytes(pair)
        for _, pair_returned, _ in book_byte_format_comparisons
        for pair, returned in pair_returned.items()
        if returned
    )
    candidates = tuple(
        sorted(
            {
                bytes((*pair[:position], item, *pair[position:]))
                for pair in returned_pairs
                for position in range(len(pair) + 1)
                for item in material
            }
        )
    )
    return returned_pairs, candidates, interrogate_across(candidates)


def _material_locality(occurrences, coordinate=lambda occurrence: occurrence.coordinates):
    grouped = defaultdict(set)
    for occurrence in occurrences:
        grouped[coordinate(occurrence)].add(occurrence.exact_material)
    return frozenset(frozenset(material) for material in grouped.values())


def _material_locality_shape(locality):
    return (
        len(locality),
        sum(len(material) == 1 for material in locality),
        max(map(len, locality)),
    )


def _one_byte_apart(first: bytes, second: bytes) -> bool:
    return len(first) == len(second) and sum(
        left != right for left, right in zip(first, second)
    ) == 1


def _return_boundaries(occurrences):
    grouped = defaultdict(list)
    for occurrence in occurrences:
        material = occurrence.exact_material
        for position in range(len(material)):
            grouped[
                (len(material), position, material[:position], material[position + 1 :])
            ].append(occurrence)
    return tuple(
        (first.exact_material, second.exact_material)
        for group in grouped.values()
        for position, first in enumerate(group)
        for second in group[position + 1 :]
        if first.returned != second.returned
    )


WITNESSES_AVAILABLE = _witnesses_available()


def test_every_current_book_material_has_its_own_ingest(measured_book_pairs):
    paths, ingests, _, _, _, _ = measured_book_pairs

    assert len(paths) == len(ingests)
    assert len({ingest.identity for ingest in ingests}) == len(paths)
    assert tuple(ingest.exact_material for ingest in ingests) == tuple(
        path.read_bytes() for path in paths
    )


def test_pair_material_comes_from_the_complete_recorded_measurement(measured_book_pairs):
    _, _, assertions, pairs, _, _ = measured_book_pairs
    recorded = tuple(
        sorted(
            bytes(assertion.representation)
            for assertion in assertions or ()
            if assertion.result == "count" and assertion.representation is not None
        )
    )

    assert pairs
    assert pairs == recorded
    assert len(pairs) == len(set(pairs))
    assert all(len(pair) == 2 for pair in pairs)


def test_byte_material_comes_from_the_complete_recorded_measurement(measured_book_pairs):
    _, _, _, _, assertions, material = measured_book_pairs
    recorded = tuple(
        sorted(
            assertion.representation
            for assertion in assertions or ()
            if assertion.result == "count" and assertion.representation is not None
        )
    )

    assert material
    assert material == recorded
    assert len(material) == len(set(material))


@pytest.mark.skipif(not WITNESSES_AVAILABLE, reason="one material witness is absent")
def test_every_measured_pair_reaches_every_witness(book_pair_witness_occurrences, measured_book_pairs):
    pairs = measured_book_pairs[3]

    assert len(book_pair_witness_occurrences) == len(MATERIAL_WITNESSES)
    assert tuple(
        row[0].witness_identity for row in book_pair_witness_occurrences
    ) == tuple(witness.identity for witness in MATERIAL_WITNESSES)
    assert all(
        tuple(occurrence.exact_material for occurrence in row) == pairs
        for row in book_pair_witness_occurrences
    )
    assert all(
        len({occurrence.exact_material for occurrence in row}) == len(pairs)
        for row in book_pair_witness_occurrences
    )


@pytest.mark.skipif(not WITNESSES_AVAILABLE, reason="one material witness is absent")
def test_distinct_witnesses_expose_their_material_localities(book_pair_witness_occurrences):
    localities = tuple(
        _material_locality(occurrences) for occurrences in book_pair_witness_occurrences
    )
    refinement = {
        (first, second): refines(localities[first], localities[second])
        for first in range(len(localities))
        for second in range(len(localities))
    }

    assert len(set(localities)) > 1
    shapes = tuple(_material_locality_shape(locality) for locality in localities)
    assert all(largest > 1 for _, _, largest in shapes)
    assert all(singletons < blocks for blocks, singletons, _ in shapes)
    assert all(
        refines(locality, frozenset({frozenset().union(*locality)}))
        for locality in localities
    )
    assert any(
        refinement[first, second] != refinement[second, first]
        for first in range(len(localities))
        for second in range(first + 1, len(localities))
    )
    assert any(
        not refinement[first, second] and not refinement[second, first]
        for first in range(len(localities))
        for second in range(first + 1, len(localities))
    )


def test_every_measured_pair_reaches_every_compiled_format_witness(
    book_pair_format_occurrences, measured_book_pairs
):
    pairs = measured_book_pairs[3]

    assert len(book_pair_format_occurrences) == len(COMPILED_WITNESSES)
    assert all(
        tuple(occurrence.exact_material for occurrence in row) == pairs
        for row in book_pair_format_occurrences
    )


def test_compiled_format_witnesses_divide_the_same_material_differently(
    book_pair_format_occurrences,
):
    return_localities = tuple(
        _material_locality(occurrences, lambda occurrence: occurrence.returned)
        for occurrences in book_pair_format_occurrences
    )

    assert len(set(return_localities)) > 1
    assert sum(len(locality) > 1 for locality in return_localities) > 1
    assert all(
        any(len(material) > 1 for material in locality)
        for locality in return_localities
    )


def test_one_byte_differences_expose_compiled_format_boundaries(
    book_pair_format_occurrences,
):
    boundaries = tuple(
        _return_boundaries(occurrences)
        for occurrences in book_pair_format_occurrences
    )

    assert any(boundaries)
    assert all(
        _one_byte_apart(first, second)
        for witness_boundaries in boundaries
        for first, second in witness_boundaries
    )
    assert len({frozenset(witness_boundaries) for witness_boundaries in boundaries}) > 1


def test_every_ordered_pair_is_compared_for_each_compiled_witness(
    book_byte_format_comparisons, measured_book_pairs
):
    material = measured_book_pairs[5]
    expected_pairs = {(first, second) for first in material for second in material}
    expected_comparisons = len(material) * (len(material) - 1) // 2

    for _, pair_returned, comparisons in book_byte_format_comparisons:
        assert set(pair_returned) == expected_pairs
        assert len(comparisons) == expected_comparisons
        assert all(
            len(outgoing) == len(incoming) == len(material)
            for outgoing, incoming in comparisons.values()
        )


def test_compiled_witnesses_establish_different_pairwise_distinctions(
    book_byte_format_comparisons,
):
    distinctions = tuple(
        frozenset(
            pair
            for pair, directions in comparisons.items()
            if any(
                first != second
                for direction in directions
                for first, second in direction
            )
        )
        for _, _, comparisons in book_byte_format_comparisons
    )

    assert len(set(distinctions)) > 1
    assert any(not distinction for distinction in distinctions)
    assert any(distinction for distinction in distinctions)


def test_three_byte_candidates_come_from_measured_bytes_and_witness_returns(
    book_three_byte_format_occurrences, measured_book_pairs
):
    returned_pairs, candidates, _ = book_three_byte_format_occurrences
    material = set(measured_book_pairs[5])

    assert returned_pairs
    assert candidates
    assert len(candidates) == len(set(candidates))
    assert all(len(candidate) == 3 for candidate in candidates)
    assert all(
        any(
            candidate[:position] + candidate[position + 1 :] in returned_pairs
            and candidate[position] in material
            for position in range(len(candidate))
        )
        for candidate in candidates
    )


def test_every_three_byte_candidate_reaches_every_compiled_witness(
    book_three_byte_format_occurrences,
):
    _, candidates, occurrences = book_three_byte_format_occurrences

    assert len(occurrences) == len(COMPILED_WITNESSES)
    assert all(
        tuple(occurrence.exact_material for occurrence in row) == candidates
        for row in occurrences
    )


def test_three_byte_candidates_expose_different_compiled_witness_boundaries(
    book_three_byte_format_occurrences,
):
    _, _, occurrences = book_three_byte_format_occurrences
    localities = tuple(
        _material_locality(row, lambda occurrence: occurrence.returned)
        for row in occurrences
    )
    boundaries = tuple(_return_boundaries(row) for row in occurrences)

    assert len(set(localities)) > 1
    assert any(boundaries)
    assert len({frozenset(found) for found in boundaries}) > 1


def test_compiled_witness_receives_the_exact_material():
    supplied = []

    def competency(material):
        supplied.append(material)

    occurrence = interrogate(
        b"\xff\x00", CompiledWitness(identity="fixture", competency=competency)
    )

    assert supplied == [b"\xff\x00"]
    assert occurrence.exact_material == b"\xff\x00"
    assert occurrence.returned is True


def test_compiled_witness_refusal_and_input_boundary_are_distinct():
    supplied = []

    def competency(material):
        supplied.append(material)
        raise ValueError

    witness = CompiledWitness(identity="fixture", competency=competency)

    occurrence = interrogate(b"\x00", witness)
    with pytest.raises(TypeError, match="exact bytes"):
        interrogate("material", witness)

    assert supplied == [b"\x00"]
    assert occurrence.returned is False


def test_a_non_byte_material_is_refused_before_a_witness_occurs(monkeypatch):
    occurrences = []
    monkeypatch.setattr(
        "material_witness_harness.subprocess.run",
        lambda *args, **kwargs: occurrences.append((args, kwargs)),
    )

    with pytest.raises(TypeError, match="exact bytes"):
        witness_occurrence("material", MATERIAL_WITNESSES[0])

    assert occurrences == []


def test_exact_bytes_reach_the_witness_without_prior_decoding(monkeypatch):
    supplied = []

    class Completed:
        returncode = 0
        stdout = b"provider material"
        stderr = b""

    def compiled_occurrence(*args, **kwargs):
        supplied.append(kwargs["input"])
        return Completed()

    monkeypatch.setattr(
        "material_witness_harness.subprocess.run", compiled_occurrence
    )

    found = witness_occurrence(b"\xff\x00", MATERIAL_WITNESSES[0])

    assert supplied == [b"\xff\x00"]
    assert found.exact_material == b"\xff\x00"
    assert found.stdout_bytes == b"provider material"
