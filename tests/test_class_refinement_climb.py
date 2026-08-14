"""A classification is lawful for the act that established it, and no longer.

Each rung's classes are the material the next rung's measurement reads. Where
that measurement finds a class's members behaving apart, the class decomposes.
The climb ends where a rung establishes nothing the one below it did not.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from decoder_witness_harness import (  # noqa: E402
    ALL,
    MIXED,
    NONE,
    accepts,
    class_adjacency,
    classes,
    climb,
    refine,
)


def test_one_member_cannot_testify_for_its_class():
    """0x80 and 0xff are one class earlier and behave apart here.

    A measurement probing one representative would have reported `all` for a
    pair whose members disagree 13 times out of 77.
    """

    recovered = classes("utf-8", 4)
    refused = next(members for key, members in recovered.items() if key[0] is None)
    leader = next(members for key, members in recovered.items() if key[0] == 2)[0]

    accepted = [byte for byte in refused if accepts("utf-8", (leader, byte))]

    assert len(accepted) == 64
    assert len(refused) - len(accepted) == 13
    assert accepts("utf-8", (leader, refused[0]))
    assert not accepts("utf-8", (leader, refused[-1]))


def test_a_class_whose_members_disagree_is_reported_mixed():
    outcomes = class_adjacency("utf-8", classes("utf-8", 4))

    assert MIXED in outcomes.values()
    assert sorted({ALL, NONE, MIXED} & set(outcomes.values())) == sorted(
        {ALL, NONE, MIXED}
    )


def test_the_climb_ends_exactly_where_nothing_is_mixed():
    """Termination is the measurement having nothing left to separate."""

    rungs = climb("utf-8")
    final = class_adjacency("utf-8", rungs[-1])

    assert MIXED not in final.values()
    assert MIXED in class_adjacency("utf-8", rungs[0]).values()


def test_refinement_splits_only_where_members_behaved_apart():
    recovered = classes("utf-8", 4)
    refined = refine("utf-8", recovered)

    assert len(refined) == len(recovered) + 1
    assert sorted(len(members) for members in refined.values()) == [5, 13, 16, 30, 64, 128]


def test_every_rung_partitions_the_same_material():
    """Refining changes where the lines fall, never what is being divided."""

    for rung in climb("utf-8"):
        covered = sorted(byte for members in rung.values() for byte in members)
        assert covered == list(range(256))


def _members(rung: dict) -> set[tuple[int, ...]]:
    """A rung as the classes it holds, however those classes are keyed."""

    return {tuple(sorted(members)) for members in rung.values()}


def test_each_rung_reads_the_one_below_it():
    """Rung n+1 holds what refining rung n yields, not a fresh measurement."""

    rungs = climb("utf-8")
    for lower, upper in zip(rungs, rungs[1:]):
        assert _members(refine("utf-8", lower)) == _members(upper)


def test_witnesses_climb_to_different_heights():
    """How far the ladder goes is a property of the witness, not the harness."""

    heights = {name: len(climb(name)) for name in ("ascii", "utf-8", "big5hkscs")}

    assert heights["ascii"] == 1
    assert heights["utf-8"] == 2
    assert heights["big5hkscs"] > 4
    assert len(climb("big5hkscs")[-1]) > len(climb("big5hkscs")[0])
