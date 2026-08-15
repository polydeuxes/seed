"""Being readable and being written back the same way are separate properties.

A codec returns results for two probes, and this records where its two results
disagree. Neither result is corrected by the other: a disagreement is a
finding about the pair.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from round_trip_witness_harness import (  # noqa: E402
    DIFFERENT,
    NOT_DECODABLE,
    REFUSED,
    SAME,
    disagreements,
    round_trip,
    survey,
)


def test_bytes_the_witness_refuses_are_not_asked_about():
    """Nothing is measured where nothing was read."""

    assert round_trip("ascii", (0xFF,)) is NOT_DECODABLE
    assert round_trip("utf-8", (0xC2,)) is NOT_DECODABLE


def test_most_witnesses_write_back_what_they_read():
    assert round_trip("ascii", (0x41,)) == SAME
    assert round_trip("utf-8", (0xC2, 0xA9)) == SAME
    assert round_trip("latin_1", (0xFF,)) == SAME


def test_several_byte_sequences_may_read_as_one_thing():
    """cp875 reads four bytes as U+001A and writes a fifth for it.

    So the bytes it writes are not among the bytes it read, and the read
    does not determine what was read from.
    """

    found = {value: written for value, read, written in disagreements("cp875")}

    assert len(found) == 6
    for value in (0x3F, 0xDC, 0xE1, 0xEC):
        assert found[value] == "fd"
        assert bytes([value]).decode("cp875") == "\x1a"
    assert 0xFD not in found


def test_a_witness_may_read_what_it_will_not_write():
    """idna reads 0x2e and writes nothing for what it read."""

    assert round_trip("idna", (0x2E,)) == REFUSED
    assert [value for value, _, written in disagreements("idna") if written == "nothing"] == [0x2E]


def test_a_witness_may_never_write_back_what_it_read():
    """utf_8_sig writes more than it was given, for every input it accepts."""

    results = dict(survey())["utf_8_sig"]

    assert results.get(SAME, 0) == 0
    assert results[DIFFERENT] > 0
    assert round_trip("utf_8_sig", (0x41,)) == DIFFERENT


def test_the_disagreement_is_a_minority_and_is_exact():
    rows = survey()
    uneven = [name for name, results in rows if results.keys() - {SAME}]

    assert len(rows) > 100
    assert 5 < len(uneven) < 20
    assert "mac_arabic" in uneven
    assert "ascii" not in uneven
