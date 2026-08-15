"""One measurement standing on another, across every witness on this machine.

Class read reads bytes. Class adjacency reads classes. The second is
handed the first's finding rather than recomputing it, so it measures over
whatever classes it is given and reports nothing without them.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from decoder_witness_harness import (  # noqa: E402
    MIXED,
    NONE,
    class_adjacency,
    classes,
    decoding_witnesses,
)


def test_the_second_measurement_takes_the_first_as_input_rather_than_repeating_it():
    """Handed other classes, it reports adjacency among those."""

    read = classes("utf-8", 4)
    supplied = {("everything",): list(range(256))}

    over_read = class_adjacency("utf-8", read)
    over_supplied = class_adjacency("utf-8", supplied)

    assert len(over_read) == len(read) ** 2
    assert len(over_supplied) == 1
    assert class_adjacency("utf-8", {}) == {}


def test_adjacency_names_a_pair_class_read_could_not():
    """A class refused as a first byte still admits followers.

    Class read reports 0x80-0xff as refused, which is about first bytes.
    Adjacency finds that the subjects do not agree about following a
    two-byte first byte, which the earlier measurement had no way to state.
    """

    read = classes("utf-8", 4)
    adjacency = class_adjacency("utf-8", read)

    refused = next(key for key in read if key[0] is None)
    pair_leader = next(key for key in read if key[0] == 2)

    assert adjacency[(pair_leader, refused)] == MIXED
    assert adjacency[(refused, refused)] == NONE


def test_every_witness_on_this_machine_answers_both_ladders():
    names = decoding_witnesses()
    assert len(names) > 90

    for name in names[:12]:
        read = classes(name, 4)
        assert sum(len(subjects) for subjects in read.values()) == 256
        assert len(class_adjacency(name, read)) == len(read) ** 2


def test_witnesses_disagree_about_where_the_boundaries_are():
    """The fan-out is a range of answers, not one answer repeated."""

    shapes = {
        len(classes(name, 4))
        for name in ("ascii", "utf-8", "big5", "shift_jis_2004", "latin_1")
    }
    assert len(shapes) > 2


def test_a_witness_that_accepts_every_byte_alone_has_one_class():
    read = classes("latin_1", 4)

    assert len(read) == 1
    assert next(iter(read)) == (1, None)
