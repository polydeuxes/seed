"""One Measurement standing on another across implementation functions.

One implementation function yields a material admission. The pair Measurement reads that admission. The second is
handed the first's finding rather than recomputing it, so it measures over
whatever material admission it is given and reports nothing without one.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from decoder_measurement import (  # noqa: E402
    MIXED,
    NONE,
    measure_material_pairs,
    first_admission,
    decoding_implementation_functions,
)


def test_the_second_measurement_takes_the_first_as_input_rather_than_repeating_it():
    """Handed another material admission, it reports ordered pairs within it."""

    read = first_admission("utf-8", 4)
    supplied = {("everything",): list(range(256))}

    over_read = measure_material_pairs("utf-8", read)
    over_supplied = measure_material_pairs("utf-8", supplied)

    assert len(over_read) == len(read) ** 2
    assert len(over_supplied) == 1
    assert measure_material_pairs("utf-8", {}) == {}


def test_complete_pairs_name_a_distinction_the_first_admission_did_not():
    """Material sharing one refused result does not share pair results.

    The first material admission records 0x80-0xff as refused, which is about first bytes.
    The pair Measurement finds that the material does not agree about following a
    two-byte first byte, which the earlier measurement had no way to state.
    """

    read = first_admission("utf-8", 4)
    pair_results = measure_material_pairs("utf-8", read)

    refused = next(key for key in read if key[0] is None)
    pair_leader = next(key for key in read if key[0] == 2)

    assert pair_results[(pair_leader, refused)] == MIXED
    assert pair_results[(refused, refused)] == NONE


def test_every_implementation_function_returns_both_admissions():
    names = decoding_implementation_functions()
    assert len(names) > 90

    for name in names[:12]:
        read = first_admission(name, 4)
        assert sum(len(material) for material in read.values()) == 256
        assert len(measure_material_pairs(name, read)) == len(read) ** 2


def test_implementation_functions_disagree_about_the_boundaries():
    """The fan-out is a range of results, not one result repeated."""

    counts = {
        len(first_admission(name, 4))
        for name in ("ascii", "utf-8", "big5", "shift_jis_2004", "latin_1")
    }
    assert len(counts) > 2


def test_an_implementation_function_that_accepts_every_byte_alone_has_one_result_coordinate():
    read = first_admission("latin_1", 4)

    assert len(read) == 1
    assert next(iter(read)) == (1, None)


PYTEST_ADMISSION = (
    test_the_second_measurement_takes_the_first_as_input_rather_than_repeating_it,
    test_complete_pairs_name_a_distinction_the_first_admission_did_not,
    test_every_implementation_function_returns_both_admissions,
    test_implementation_functions_disagree_about_the_boundaries,
    test_an_implementation_function_that_accepts_every_byte_alone_has_one_result_coordinate,
)
