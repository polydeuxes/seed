"""Admit exact material under complete implementation-function pair Measurement."""

from __future__ import annotations

import sys
from pathlib import Path



sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from decoder_measurement import (  # noqa: E402
    ALL,
    MIXED,
    NONE,
    accepts,
    measure_material_pairs,
    first_admission,
    admit,
    admit_pairs,
)


def test_one_material_occurrence_cannot_testify_for_every_equal_result():
    """0x80 and 0xff have one equal result earlier and behave apart here.

    A measurement probing one representative would have reported `all` for a
    pair whose material disagrees 13 times out of 77.
    """

    read = first_admission("utf-8", 4)
    refused = next(material for key, material in read.items() if key[0] is None)
    leader = next(material for key, material in read.items() if key[0] == 2)[0]

    accepted = [byte for byte in refused if accepts("utf-8", (leader, byte))]

    assert len(accepted) == 64
    assert len(refused) - len(accepted) == 13
    assert accepts("utf-8", (leader, refused[0]))
    assert not accepts("utf-8", (leader, refused[-1]))


def test_equal_earlier_results_with_disagreeing_material_are_reported_mixed():
    results = measure_material_pairs("utf-8", first_admission("utf-8", 4))

    assert MIXED in results.values()
    assert sorted({ALL, NONE, MIXED} & set(results.values())) == sorted(
        {ALL, NONE, MIXED}
    )


def test_admission_stops_exactly_where_nothing_is_mixed():
    """Termination is the measurement having nothing left to separate."""

    admissions = admit("utf-8")
    final = measure_material_pairs("utf-8", admissions[-1])

    assert MIXED not in final.values()
    assert MIXED in measure_material_pairs("utf-8", admissions[0]).values()


def test_admission_separates_only_where_material_behaved_apart():
    read = first_admission("utf-8", 4)
    admitted = admit_pairs("utf-8", read)

    assert len(admitted) == len(read) + 1
    assert sorted(len(material) for material in admitted.values()) == [
        5,
        13,
        16,
        30,
        64,
        128,
    ]


def test_every_admission_carries_the_same_material():
    """Refining differences where the lines fall, never what is being divided."""

    for admission in admit("utf-8"):
        covered = sorted(byte for material in admission.values() for byte in material)
        assert covered == list(range(256))


def _material(admission: dict) -> set[tuple[int, ...]]:
    """The exact material carried by one material admission."""

    return {tuple(sorted(material)) for material in admission.values()}


def test_each_admission_uses_the_one_before_it():

    admissions = admit("utf-8")
    for lower, upper in zip(admissions, admissions[1:]):
        assert _material(admit_pairs("utf-8", lower)) == _material(upper)


def test_decoder_functions_establish_different_admission_counts():
    counts = {name: len(admit(name)) for name in ("ascii", "utf-8", "big5hkscs")}

    assert counts["ascii"] == 1
    assert counts["utf-8"] == 2
    assert counts["big5hkscs"] == 2
    assert len(admit("big5hkscs")[-1]) == 114


PYTEST_ADMISSION = (
    test_one_material_occurrence_cannot_testify_for_every_equal_result,
    test_equal_earlier_results_with_disagreeing_material_are_reported_mixed,
    test_admission_stops_exactly_where_nothing_is_mixed,
    test_admission_separates_only_where_material_behaved_apart,
    test_every_admission_carries_the_same_material,
    test_each_admission_uses_the_one_before_it,
    test_decoder_functions_establish_different_admission_counts,
)
