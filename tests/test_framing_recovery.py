"""What positional support measures, and what it does not select.

A specimen is bytes. Partitioning them by offset under a candidate stride is
exact, and so are the resulting value sets. Which stride, if any, frames the
material is a further question these do not answer.
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

    What the two values are about is not measured here. Reading them as a high
    half, or as sign extension, is an interpretation of why, and no occurrence
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
    so the threshold, not the material, was choosing.
    """

    for amplitude in (8000, 2000, 500, 100, 20):
        raw = block(amplitude)
        for stride in (2, 3, 4):
            sizes = set(position_diversity(raw, stride).values())
            assert len(sizes) > 1, (amplitude, stride, sizes)


def test_a_stride_and_its_multiple_carry_the_same_distinction():
    """Stride 4 agrees with stride 2 because it is two of them.

    Separating a primitive candidate from a composite one is what a selection
    rule would have to do, and no rule here does it.
    """

    diversity = position_diversity(block(100), 4)

    assert diversity[1] == diversity[3] == position_diversity(block(100), 2)[1]


def test_no_module_level_name_states_a_recovered_framing():
    """The verdict is withdrawn, not renamed."""

    import framing_ladder_harness as harness

    assert not hasattr(harness, "recovered_width")
    assert not [name for name in dir(harness) if "sample_width" in name]
