"""One refinement mechanism, ridden by witnesses that share nothing else.

The material may be bytes or terms; the witness may be a decoder or a corpus.
What the climb requires is a first material Locality and a
witness that returns results for pairs.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import refinement_climb as rc  # noqa: E402
from book_grammar_witness import held_apart, restated, statements  # noqa: E402
from book_grammar_witness import witness as book_witness  # noqa: E402
from decoder_witness_harness import accepts, material_locality  # noqa: E402


def test_complete_pair_coverage_separates_in_one_refinement():
    ordered = rc.climb(rc.one_material_locality(range(16)), lambda a, b: a < b)
    assert rc.heights(ordered) == [1, 16]

    apart = held_apart()
    flat = rc.climb(rc.one_material_locality(apart), book_witness(apart))
    assert rc.heights(flat)[0] == 1
    assert rc.heights(flat)[-1] > 1
    for firsts in flat[-1]:
        for seconds in flat[-1]:
            assert len(
                {book_witness(apart)(a, b) for a in firsts for b in seconds}
            ) == 1


def test_a_nonrepresentative_pair_cannot_hide_inside_a_final_locality():
    material = ("a", "b", "c", "d")

    def witness(first, second):
        return (first, second) == ("b", "d")

    localities = rc.climb([("a", "b"), ("c", "d")], witness)

    assert rc.heights(localities) == [2, 4]
    for firsts in localities[-1]:
        for seconds in localities[-1]:
            assert len({witness(a, b) for a in firsts for b in seconds}) == 1


def test_the_same_engine_climbs_a_decoder_witness():
    read = material_locality("utf-8", 4)
    first = [tuple(material) for material in read.values()]

    localities = rc.climb(first, lambda a, b: accepts("utf-8", (a, b)))

    assert rc.heights(localities) == [5, 6]
    assert sorted(len(material) for material in localities[-1]) == [5, 13, 16, 30, 64, 128]


def test_the_same_engine_climbs_a_corpus_witness():
    apart = held_apart()
    first = rc.by(lambda term: len(apart[term]), apart)

    localities = rc.climb(first, book_witness(apart))

    assert rc.heights(localities)[0] == 5
    assert rc.heights(localities)[-1] > rc.heights(localities)[0]
    for firsts in localities[-1]:
        for seconds in localities[-1]:
            assert len(
                {book_witness(apart)(a, b) for a in firsts for b in seconds}
            ) == 1


def test_the_two_witnesses_establish_different_final_material_localities():
    read = material_locality("big5hkscs", 4)
    codec_rungs = rc.climb(
        [tuple(m) for m in read.values()],
        lambda a, b: accepts("big5hkscs", (a, b)),
    )
    apart = held_apart()
    book_rungs = rc.climb(
        rc.by(lambda term: len(apart[term]), apart), book_witness(apart)
    )

    assert len(codec_rungs) == len(book_rungs) == 2
    assert rc.heights(codec_rungs)[-1] != rc.heights(book_rungs)[-1]


def test_every_material_locality_carries_the_same_material():
    read = material_locality("utf-8", 4)
    localities = rc.climb(
        [tuple(m) for m in read.values()], lambda a, b: accepts("utf-8", (a, b))
    )

    for locality in localities:
        assert sorted(b for material in locality for b in material) == list(range(256))


def test_what_the_witness_could_not_separate_is_reported():
    apart = held_apart()
    localities = rc.climb(
        rc.by(lambda term: len(apart[term]), apart), book_witness(apart)
    )

    left = rc.unseparated(localities)
    assert left
    assert all(len(material) > 1 for material in left)


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
