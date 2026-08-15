"""Admission under complete pair implementation-function coverage."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import material_admission  # noqa: E402
from book_grammar_witness import held_apart, restated, statements  # noqa: E402
from book_grammar_witness import implementation_function as book_implementation_function  # noqa: E402
from decoder_measurement import accepts, first_admission  # noqa: E402


def test_complete_pair_coverage_separates_in_one_admission():
    ordered = material_admission.admit(material_admission.one_admission(range(16)), lambda a, b: a < b)
    assert material_admission.admission_counts(ordered) == [1, 16]

    apart = held_apart()
    flat = material_admission.admit(material_admission.one_admission(apart), book_implementation_function(apart))
    assert material_admission.admission_counts(flat)[0] == 1
    assert material_admission.admission_counts(flat)[-1] > 1
    for firsts in flat[-1]:
        for seconds in flat[-1]:
            assert len(
                {book_implementation_function(apart)(a, b) for a in firsts for b in seconds}
            ) == 1


def test_a_nonrepresentative_pair_cannot_hide_inside_a_final_admission():
    material = ("a", "b", "c", "d")

    def implementation_function(first, second):
        return (first, second) == ("b", "d")

    admissions = material_admission.admit([("a", "b"), ("c", "d")], implementation_function)

    assert material_admission.admission_counts(admissions) == [2, 4]
    for firsts in admissions[-1]:
        for seconds in admissions[-1]:
            assert len({implementation_function(a, b) for a in firsts for b in seconds}) == 1


def test_the_same_admission_uses_a_decoder_witness():
    read = first_admission("utf-8", 4)
    first = [tuple(material) for material in read.values()]

    admissions = material_admission.admit(first, lambda a, b: accepts("utf-8", (a, b)))

    assert material_admission.admission_counts(admissions) == [5, 6]
    assert sorted(len(material) for material in admissions[-1]) == [5, 13, 16, 30, 64, 128]


def test_the_same_admission_uses_a_book_implementation_function():
    apart = held_apart()
    first = material_admission.admission_by(lambda term: len(apart[term]), apart)

    admissions = material_admission.admit(first, book_implementation_function(apart))

    assert material_admission.admission_counts(admissions)[0] == 5
    assert material_admission.admission_counts(admissions)[-1] > material_admission.admission_counts(admissions)[0]
    for firsts in admissions[-1]:
        for seconds in admissions[-1]:
            assert len(
                {book_implementation_function(apart)(a, b) for a in firsts for b in seconds}
            ) == 1


def test_the_two_witnesses_establish_different_final_admissions():
    read = first_admission("big5hkscs", 4)
    codec_admissions = material_admission.admit(
        [tuple(m) for m in read.values()],
        lambda a, b: accepts("big5hkscs", (a, b)),
    )
    apart = held_apart()
    book_admissions = material_admission.admit(
        material_admission.admission_by(lambda term: len(apart[term]), apart), book_implementation_function(apart)
    )

    assert len(codec_admissions) == len(book_admissions) == 2
    assert material_admission.admission_counts(codec_admissions)[
        -1
    ] != material_admission.admission_counts(book_admissions)[-1]


def test_every_admission_carries_the_same_material():
    read = first_admission("utf-8", 4)
    admissions = material_admission.admit(
        [tuple(m) for m in read.values()], lambda a, b: accepts("utf-8", (a, b))
    )

    for admission in admissions:
        assert sorted(b for material in admission for b in material) == list(range(256))


def test_what_the_implementation_function_could_not_separate_is_reported():
    apart = held_apart()
    admissions = material_admission.admit(
        material_admission.admission_by(lambda term: len(apart[term]), apart), book_implementation_function(apart)
    )

    left = material_admission.not_distinguished(admissions)
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
