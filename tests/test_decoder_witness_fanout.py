"""One measurement standing on another, across every witness on this machine.

Class recovery reads bytes. Class adjacency reads classes. The second is
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

    recovered = classes("utf-8", 4)
    supplied = {("everything",): list(range(256))}

    over_recovered = class_adjacency("utf-8", recovered)
    over_supplied = class_adjacency("utf-8", supplied)

    assert len(over_recovered) == len(recovered) ** 2
    assert len(over_supplied) == 1
    assert class_adjacency("utf-8", {}) == {}


def test_adjacency_names_a_pair_class_recovery_could_not():
    """A class refused as a first byte still admits followers.

    Class recovery reports 0x80-0xff as refused, which is about first bytes.
    Adjacency finds that class's members do not agree about following a
    length-two first byte, which the earlier measurement had no way to state.
    """

    recovered = classes("utf-8", 4)
    adjacency = class_adjacency("utf-8", recovered)

    refused = next(key for key in recovered if key[0] is None)
    pair_leader = next(key for key in recovered if key[0] == 2)

    assert adjacency[(pair_leader, refused)] == MIXED
    assert adjacency[(refused, refused)] == NONE


def test_every_witness_on_this_machine_answers_both_ladders():
    names = decoding_witnesses()
    assert len(names) > 90

    for name in names[:12]:
        recovered = classes(name, 4)
        assert sum(len(members) for members in recovered.values()) == 256
        assert len(class_adjacency(name, recovered)) == len(recovered) ** 2


def test_witnesses_disagree_about_where_the_boundaries_are():
    """The fan-out is a range of answers, not one answer repeated."""

    shapes = {
        len(classes(name, 4))
        for name in ("ascii", "utf-8", "big5", "shift_jis_2004", "latin_1")
    }
    assert len(shapes) > 2


def test_a_witness_that_accepts_every_byte_alone_has_one_class():
    recovered = classes("latin_1", 4)

    assert len(recovered) == 1
    assert next(iter(recovered)) == (1, None)
