"""What a decoder's refusals establish, and what they do not.

A decoder answers whether it accepts exact bytes. That answer is testimony
about the decoder. These pin what one interrogation measured, without taking
the decoder's vocabulary along with its answers.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from decoder_witness_harness import accepts, admissible_followers, classes  # noqa: E402


def _spans(codec: str) -> dict[tuple[int, int], tuple[object, int]]:
    return {
        (members[0], members[-1]): (key[0], len(members))
        for key, members in classes(codec).items()
    }


def test_one_witness_partitions_every_byte_exactly_once():
    grouped = classes("utf-8")
    covered = sorted(byte for members in grouped.values() for byte in members)

    assert covered == list(range(256))
    assert len(grouped) == 5


def test_the_boundaries_the_witness_refused_at():
    assert _spans("utf-8") == {
        (0x00, 0x7F): (1, 128),
        (0xC2, 0xDF): (2, 30),
        (0xE0, 0xEF): (3, 16),
        (0xF0, 0xF4): (4, 5),
        (0x80, 0xFF): (None, 77),
    }


def test_the_only_admissible_followers_are_one_contiguous_range():
    followers = admissible_followers("utf-8", 0xC2)

    assert followers == list(range(0x80, 0xC0))
    assert len(followers) == 64


def test_a_second_witness_partitions_the_same_bytes_differently():
    """Two decoders, one material, different refusals.

    They agree exactly on the bytes each accepts alone, and differ on
    everything after. Neither agreement nor difference is explained here.
    """

    utf8 = classes("utf-8")
    ascii_ = classes("ascii", max_length=2)

    assert len(ascii_) == 2
    accepted_alone = {
        tuple(members) for key, members in utf8.items() if key[0] == 1
    }
    assert accepted_alone == {
        tuple(members) for key, members in ascii_.items() if key[0] == 1
    }


def test_the_witness_refuses_more_than_a_leading_bit_rule_predicts():
    """The surplus is recorded, not explained.

    A reading by leading bits alone would admit 0xc0, 0xc1 and 0xf5-0xff as
    first bytes. This witness refuses them, so its refusals carry something
    beyond that reading. What that something is is not established here.
    """

    refused = next(
        members for key, members in classes("utf-8").items() if key[0] is None
    )

    for byte in (0xC0, 0xC1, *range(0xF5, 0x100)):
        assert byte in refused, hex(byte)


def test_an_accepted_sequence_is_not_thereby_meaningful():
    """Acceptance is the whole of what was measured."""

    assert accepts("utf-8", (0x41,))
    assert accepts("utf-8", (0xC2, 0xA9))
    assert not accepts("utf-8", (0xC2,))
    assert not accepts("utf-8", (0xA9,))
