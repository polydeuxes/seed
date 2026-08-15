"""Refine exact material under complete witness-pair Measurement."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from decoder_witness_harness import (  # noqa: E402
    ALL,
    MIXED,
    NONE,
    accepts,
    measure_material_pairs,
    material_locality,
    climb,
    refine,
)


def test_one_material_occurrence_cannot_testify_for_every_equal_result():
    """0x80 and 0xff have one equal result earlier and behave apart here.

    A measurement probing one representative would have reported `all` for a
    pair whose material disagrees 13 times out of 77.
    """

    read = material_locality("utf-8", 4)
    refused = next(material for key, material in read.items() if key[0] is None)
    leader = next(material for key, material in read.items() if key[0] == 2)[0]

    accepted = [byte for byte in refused if accepts("utf-8", (leader, byte))]

    assert len(accepted) == 64
    assert len(refused) - len(accepted) == 13
    assert accepts("utf-8", (leader, refused[0]))
    assert not accepts("utf-8", (leader, refused[-1]))


def test_equal_earlier_results_with_disagreeing_material_are_reported_mixed():
    results = measure_material_pairs("utf-8", material_locality("utf-8", 4))

    assert MIXED in results.values()
    assert sorted({ALL, NONE, MIXED} & set(results.values())) == sorted(
        {ALL, NONE, MIXED}
    )


def test_the_climb_ends_exactly_where_nothing_is_mixed():
    """Termination is the measurement having nothing left to separate."""

    localities = climb("utf-8")
    final = measure_material_pairs("utf-8", localities[-1])

    assert MIXED not in final.values()
    assert MIXED in measure_material_pairs("utf-8", localities[0]).values()


def test_refinement_splits_only_where_material_behaved_apart():
    read = material_locality("utf-8", 4)
    refined = refine("utf-8", read)

    assert len(refined) == len(read) + 1
    assert sorted(len(material) for material in refined.values()) == [5, 13, 16, 30, 64, 128]


def test_every_material_locality_carries_the_same_material():
    """Refining differences where the lines fall, never what is being divided."""

    for locality in climb("utf-8"):
        covered = sorted(byte for material in locality.values() for byte in material)
        assert covered == list(range(256))


def _material(locality: dict) -> set[tuple[int, ...]]:
    """The exact material carried by one material Locality."""

    return {tuple(sorted(material)) for material in locality.values()}


def test_each_material_locality_reads_the_one_before_it():
    """Each refinement uses the prior material Locality."""

    localities = climb("utf-8")
    for lower, upper in zip(localities, localities[1:]):
        assert _material(refine("utf-8", lower)) == _material(upper)


def test_witnesses_climb_to_different_heights():
    heights = {name: len(climb(name)) for name in ("ascii", "utf-8", "big5hkscs")}

    assert heights["ascii"] == 1
    assert heights["utf-8"] == 2
    assert heights["big5hkscs"] == 2
    assert len(climb("big5hkscs")[-1]) == 114
