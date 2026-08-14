"""One refinement mechanism, ridden by witnesses that share nothing else.

The subjects may be bytes or terms; the witness may be a decoder or a corpus.
What the climb requires is a first classification that carries something and a
witness that answers about pairs.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import refinement_climb as rc  # noqa: E402
from book_grammar_witness import held_apart, restated, statements  # noqa: E402
from book_grammar_witness import witness as book_witness  # noqa: E402
from decoder_witness_harness import accepts, classes  # noqa: E402


def test_whether_a_first_classification_must_carry_something_is_the_witness():
    """What one class costs is how fast the witness separates from it.

    An ordering witness halves against its representative and climbs quickly.
    The Book's witness answers `False` for almost every pair, so from one class
    it peels a single term per rung.
    """

    ordered = rc.climb(rc.one_class(range(16)), lambda a, b: a < b)
    assert rc.heights(ordered)[0] == 1
    assert rc.heights(ordered)[-1] > 1

    apart = held_apart()
    flat = rc.climb(rc.one_class(apart), book_witness(apart), limit=40)
    assert rc.heights(flat)[:4] == [1, 2, 3, 4]


def test_the_same_engine_climbs_a_decoder_witness():
    recovered = classes("utf-8", 4)
    first = [tuple(members) for members in recovered.values()]

    rungs = rc.climb(first, lambda a, b: accepts("utf-8", (a, b)))

    assert rc.heights(rungs) == [5, 6]
    assert sorted(len(members) for members in rungs[-1]) == [5, 13, 16, 30, 64, 128]


def test_the_same_engine_climbs_a_corpus_witness():
    apart = held_apart()
    first = rc.by(lambda term: len(apart[term]), apart)

    rungs = rc.climb(first, book_witness(apart), limit=400)

    assert len(rungs) > 100
    assert rc.heights(rungs)[0] < rc.heights(rungs)[-1]


def test_the_two_witnesses_climb_differently():
    """A codec splits many classes per rung; the Book splits about one.

    Both reach a rung that separates nothing further. How long that takes is a
    property of the witness, and these differ by more than an order.
    """

    recovered = classes("big5hkscs", 4)
    codec_rungs = rc.climb(
        [tuple(m) for m in recovered.values()],
        lambda a, b: accepts("big5hkscs", (a, b)),
    )
    apart = held_apart()
    book_rungs = rc.climb(
        rc.by(lambda term: len(apart[term]), apart), book_witness(apart), limit=400
    )

    assert len(codec_rungs) < 12
    assert len(book_rungs) > 100
    assert len(book_rungs) > 8 * len(codec_rungs)


def test_every_rung_partitions_the_same_subjects():
    recovered = classes("utf-8", 4)
    rungs = rc.climb(
        [tuple(m) for m in recovered.values()], lambda a, b: accepts("utf-8", (a, b))
    )

    for rung in rungs:
        assert sorted(b for members in rung for b in members) == list(range(256))


def test_what_the_witness_could_not_separate_is_reported():
    apart = held_apart()
    rungs = rc.climb(
        rc.by(lambda term: len(apart[term]), apart), book_witness(apart), limit=400
    )

    left = rc.unseparated(rungs)
    assert left
    assert all(len(members) > 1 for members in left)


def test_each_repeated_distinction_crosses_chapters():
    """Each crosses chapters, so restatement rather than duplication."""

    again = restated()

    assert again
    assert ("material", "evidence") in again
    for pair, at in again.items():
        assert len({place.split(":")[0] for place in at}) > 1, pair


def test_no_distinction_is_stated_in_both_directions():
    said = {(first, second) for _, _, first, second in statements()}

    assert not [(a, b) for a, b in said if (b, a) in said]
