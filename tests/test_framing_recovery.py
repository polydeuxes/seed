"""Whether a byte grouping is recoverable from material that does not state it.

A specimen is bytes. That two of them are one sample, and which of the two
carries the high half, are coordinates the harness knows. These pin what the
material can and cannot supply on its own.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from framing_ladder_harness import (  # noqa: E402
    block,
    position_diversity,
    recovered_width,
)


def test_a_grouping_no_position_distinguishes_is_not_recovered():
    """Material whose magnitudes fill the sample width recovers nothing.

    At amplitude 8000 the high byte takes 64 values, so no candidate width has
    positions that behave markedly differently, and the finding is absence
    rather than a guess.
    """

    assert recovered_width(block(8000)) is None


def test_small_magnitudes_make_the_grouping_recoverable():
    """The high byte carries only sign extension, and the split is the evidence."""

    for amplitude in (2000, 500, 100, 20):
        assert recovered_width(block(amplitude)) == 2, amplitude


def test_the_recovered_width_is_the_one_the_harness_constructed():
    spread = position_diversity(block(100), 2)
    assert spread[1] * 4 <= spread[0], spread
    assert spread[1] == 2


def test_a_width_that_explains_nothing_is_flat():
    """Width 3 divides no sample, so its positions carry a similar spread."""

    spread = position_diversity(block(100), 3)
    assert min(spread.values()) * 4 > max(spread.values()), spread


def test_recovery_does_not_depend_on_the_filename_or_a_declared_period():
    """Only the bytes are consulted."""

    raw = block(100)
    assert recovered_width(raw) == recovered_width(bytes(raw))
    assert recovered_width(raw[:800]) == 2
