from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import shutil
import sys

import pytest

from seed_runtime.byte_measurement import (
    assertions_of_recorded_adjacent_byte_pair_measurement,
    record_adjacent_byte_pair_count_layer,
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
    pair_measurement = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_measurement.identity,
        recording_locality_identity="book-pair-measurement",
    )
    assertions = assertions_of_recorded_adjacent_byte_pair_measurement(
        ledger, pair_measurement.identity
    )
    pairs = tuple(
        sorted(
            bytes(assertion.representation)
            for assertion in assertions or ()
            if assertion.result == "count" and assertion.representation is not None
        )
    )
    return paths, ingests, assertions, pairs


@pytest.fixture(scope="module")
def book_pair_witness_occurrences(measured_book_pairs):
    return occurrences_across(measured_book_pairs[3])


@pytest.fixture(scope="module")
def book_pair_format_occurrences(measured_book_pairs):
    return interrogate_across(measured_book_pairs[3])


def _partition(occurrences, coordinate=lambda occurrence: occurrence.coordinates):
    grouped = defaultdict(set)
    for occurrence in occurrences:
        grouped[coordinate(occurrence)].add(occurrence.exact_material)
    return frozenset(frozenset(members) for members in grouped.values())


def _partition_shape(partition):
    return (
        len(partition),
        sum(len(block) == 1 for block in partition),
        max(map(len, partition)),
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
    paths, ingests, _, _ = measured_book_pairs

    assert len(paths) == len(ingests)
    assert len({ingest.identity for ingest in ingests}) == len(paths)
    assert tuple(ingest.exact_material for ingest in ingests) == tuple(
        path.read_bytes() for path in paths
    )


def test_pair_material_comes_from_the_complete_recorded_measurement(measured_book_pairs):
    _, _, assertions, pairs = measured_book_pairs
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
def test_distinct_witnesses_expose_their_partitions(book_pair_witness_occurrences):
    partitions = tuple(
        _partition(occurrences) for occurrences in book_pair_witness_occurrences
    )
    refinement = {
        (first, second): refines(partitions[first], partitions[second])
        for first in range(len(partitions))
        for second in range(len(partitions))
    }

    assert len(set(partitions)) > 1
    shapes = tuple(_partition_shape(partition) for partition in partitions)
    assert all(largest > 1 for _, _, largest in shapes)
    assert all(singletons < blocks for blocks, singletons, _ in shapes)
    assert all(
        refines(partition, frozenset({frozenset().union(*partition)}))
        for partition in partitions
    )
    assert any(
        refinement[first, second] != refinement[second, first]
        for first in range(len(partitions))
        for second in range(first + 1, len(partitions))
    )
    assert any(
        not refinement[first, second] and not refinement[second, first]
        for first in range(len(partitions))
        for second in range(first + 1, len(partitions))
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
    return_partitions = tuple(
        _partition(occurrences, lambda occurrence: occurrence.returned)
        for occurrences in book_pair_format_occurrences
    )

    assert len(set(return_partitions)) > 1
    assert sum(len(partition) > 1 for partition in return_partitions) > 1
    assert all(
        any(len(block) > 1 for block in partition)
        for partition in return_partitions
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
