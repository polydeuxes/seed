"""What positional support measures, and what it does not select.

A specimen is bytes. Beginning a material Locality at each offset under a candidate stride is
exact, and so are the resulting value sets. Which stride, if any, frames the
material is a further distinction these do not establish.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from framing_ladder_harness import (  # noqa: E402
    block,
    position_diversity,
    position_support,
)


def test_support_is_the_exact_set_of_values_at_each_offset():
    raw = block(100)
    support = position_support(raw, 2)

    assert support[0] == frozenset(raw[0::2])
    assert support[1] == frozenset(raw[1::2])
    assert position_diversity(raw, 2) == {0: len(support[0]), 1: len(support[1])}


def test_one_offset_carries_two_values_where_another_carries_many():
    """The measurement, stated as the comparison it is.

    What the two values are about is not measured here. Read them as a high
    half, or as sign extension, is a claim about why, and no occurrence
    established it.
    """

    diversity = position_diversity(block(100), 2)

    assert diversity[0] == 201
    assert diversity[1] == 2
    assert diversity[0] != diversity[1]


def test_support_sizes_differ_under_every_stride_so_inequality_selects_nothing():
    """Why the earlier fourfold ratio was doing all the work.

    An earlier revision selected a stride where one offset's support was four
    times another's. Inequality alone admits every stride at every amplitude,
    so the count, not the material, was choosing.
    """

    for amplitude in (8000, 2000, 500, 100, 20):
        raw = block(amplitude)
        for stride in (2, 3, 4):
            sizes = set(position_diversity(raw, stride).values())
            assert len(sizes) > 1, (amplitude, stride, sizes)


def test_a_stride_and_its_multiple_carry_the_same_distinction():
    """Stride 4 agrees with stride 2 because it is two of them.

    The Measurement establishes no distinction between a primitive candidate
    and a composite candidate.
    """

    diversity = position_diversity(block(100), 4)

    assert diversity[1] == diversity[3] == position_diversity(block(100), 2)[1]


def test_no_module_level_name_states_a_read_framing():
    """The verdict is withdrawn, not renamed."""

    import framing_ladder_harness as harness

    assert not hasattr(harness, "read_width")
    assert not [name for name in dir(harness) if "sample_width" in name]


def test_a_stride_does_not_say_where_a_group_begins():
    """The same material read from byte one gives the same material tuples in reversed places.

    A material Locality starts somewhere, and starting at byte zero is this harness's
    determination. Positional recurrence at some stride is compatible with either
    phase, so it does not establish a boundary.
    """

    raw = block(100)
    at_zero = position_support(raw, 2, phase=0)
    at_one = position_support(raw, 2, phase=1)

    assert at_zero[0] == at_one[1]
    assert at_zero[1] == at_one[0]
    assert at_zero[0] != at_zero[1]


def test_the_reversal_is_exact_rather_than_approximate():
    raw = block(100)
    at_zero = position_support(raw, 2, phase=0)
    at_one = position_support(raw, 2, phase=1)

    assert not at_zero[0] ^ at_one[1]
    assert not at_zero[1] ^ at_one[0]
    assert [len(v) for v in at_zero.values()] == [201, 2]
    assert [len(v) for v in at_one.values()] == [2, 201]


def test_phase_defaults_to_a_choice_and_not_a_finding():
    """Read from byte zero is what the default does, and only that."""

    raw = block(100)
    assert position_support(raw, 2) == position_support(raw, 2, phase=0)
    assert position_support(raw, 2) != position_support(raw, 2, phase=1)


def test_the_materials_own_byte_count_is_not_an_internal_boundary():
    """An occurrence begins at its first byte. Nothing inside it does.

    A material Locality read from byte zero starts where the material starts, which
    says something about the Locality. Promoting it to "a unit also begins
    here" would take the occurrence's exact byte count as evidence about the
    occurrence's contents.
    """

    raw = block(100)

    # The byte count is exact and available.
    assert len(raw) == 1600

    # And it is compatible with either Locality phase, which is what makes it
    # no evidence for one: the material tuples trade places rather than one disagreeing.
    at_zero = position_support(raw, 2, phase=0)
    at_one = position_support(raw, 2, phase=1)
    assert {frozenset(at_zero.values())} == {frozenset(at_one.values())}


def test_phase_zero_is_not_privileged_by_the_material():
    """Every phase under a stride carries the same material exactly."""

    raw = block(100)
    seen = [
        frozenset(position_support(raw, 2, phase=phase).values())
        for phase in (0, 1)
    ]
    assert seen[0] == seen[1]
