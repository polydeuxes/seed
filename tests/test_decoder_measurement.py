"""What a decoder's refusals establish, and what they do not.

A decoder returns whether it accepts exact bytes. That result is testimony
about the decoder. These pin the exact Measurement, without taking
the decoder's vocabulary along with its results.
"""

from __future__ import annotations

import sys
from pathlib import Path


FIDELITY_SUBJECT = "material_measurement_witness"

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from decoder_measurement import accepts, admissible_followers, first_admission  # noqa: E402


def _spans(codec: str) -> dict[tuple[int, int], tuple[object, int]]:
    return {
        (material[0], material[-1]): (key[0], len(material))
        for key, material in first_admission(codec).items()
    }


def test_one_implementation_function_places_every_byte_exactly_once():
    same_result = first_admission("utf-8")
    covered = sorted(byte for material in same_result.values() for byte in material)

    assert covered == list(range(256))
    assert len(same_result) == 5


def test_the_boundaries_the_implementation_function_refused_at():
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


def test_a_second_implementation_function_places_the_same_bytes_differently():
    """Two decoders, one material, different refusals.

    They agree exactly on the bytes each accepts alone, and differ on
    everything after. Neither agreement nor difference is explained here.
    """

    utf8 = first_admission("utf-8")
    ascii_ = first_admission("ascii", max_byte_count=2)

    assert len(ascii_) == 2
    accepted_alone = {
        tuple(material) for key, material in utf8.items() if key[0] == 1
    }
    assert accepted_alone == {
        tuple(material) for key, material in ascii_.items() if key[0] == 1
    }


def test_the_implementation_function_refuses_more_than_a_leading_bit_rule_predicts():
    """The surplus is recorded, not explained.

    A read by leading bits alone would admit 0xc0, 0xc1 and 0xf5-0xff as
    first bytes. This implementation function refuses them, so its refusals carry something
    beyond that read. What that something is is not established here.
    """

    refused = next(
        material for key, material in first_admission("utf-8").items() if key[0] is None
    )

    for byte in (0xC0, 0xC1, *range(0xF5, 0x100)):
        assert byte in refused, hex(byte)


def test_an_accepted_sequence_is_not_thereby_meaningful():
    """Acceptance is the whole of what was measured."""

    assert accepts("utf-8", (0x41,))
    assert accepts("utf-8", (0xC2, 0xA9))
    assert not accepts("utf-8", (0xC2,))
    assert not accepts("utf-8", (0xA9,))
