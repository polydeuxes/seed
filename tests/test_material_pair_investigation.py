from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import IngestResultReference  # noqa: E402
from material_pair_investigation import (  # noqa: E402
    ExactMaterialPairCompareOccurrence,
    ExactMaterialPairOccurrence,
    ExactRecurrentMaterialPairSubject,
    ExactRecurrentMaterialPairReference,
    compare_pair_occurrences,
    exact_pair_occurrences,
    recurrent_adjacent_pair_subjects,
)


def _source(identity: str, exact: bytes, *, locality: str = "pair-locality"):
    return IngestResultReference(
        recorded_occurrence_identity=f"{identity}-recorded",
        locality_identity=locality,
        act_occurrence_identity=f"{identity}-act",
        result_identity=f"{identity}-result",
        yield_evidence_identity=f"{identity}-yield",
        exact_material=exact,
    )


def _pair(
    identity: str,
    exact: bytes,
    *,
    locality: str = "pair-locality",
    sources: tuple[str, ...] = ("premise-recorded",),
):
    return ExactRecurrentMaterialPairReference(
        recorded_occurrence_identity=f"{identity}-measurement",
        recurrence_assertion_identity=f"{identity}-recurrence-assertion",
        count_assertion_identity=f"{identity}-count-assertion",
        locality_identity=locality,
        source_occurrence_identities=sources,
        completeness_boundary_identity=f"{identity}-boundary",
        exact_material=exact,
    )


@pytest.fixture
def exact_pair():
    subjects = recurrent_adjacent_pair_subjects(
        (_source("premise", b"abxxab"),), (_pair("ab", b"ab"),)
    )
    assert len(subjects) == 1
    return subjects[0]


def test_recurrence_not_adjacency_alone_warrants_one_pair_subject():
    one = _source("one", b"ab")
    two = _source("two", b"abxxab")

    assert recurrent_adjacent_pair_subjects(
        (one,),
        (
            _pair(
                "ab-one",
                b"ab",
                sources=(one.recorded_occurrence_identity,),
            ),
        ),
    ) == ()
    pair = _pair(
        "ab-two",
        b"ab",
        sources=(two.recorded_occurrence_identity,),
    )
    subjects = recurrent_adjacent_pair_subjects(
        (two,), (pair,)
    )

    assert len(subjects) == 1
    subject = subjects[0]
    assert subject.pair_reference == pair
    assert len(subject.premise_occurrences) == 2
    assert {
        occurrence.exact_material for occurrence in subject.premise_occurrences
    } == {b"ab"}


def test_source_order_does_not_select_which_pair_identities_exist():
    first = _source("first", b"ab")
    second = _source("second", b"ab")
    pairs = (
        _pair(
            "ab",
            b"ab",
            sources=(
                first.recorded_occurrence_identity,
                second.recorded_occurrence_identity,
            ),
        ),
    )

    forward = recurrent_adjacent_pair_subjects((first, second), pairs)
    reverse = recurrent_adjacent_pair_subjects((second, first), pairs)

    assert tuple(subject.pair_identity for subject in forward) == tuple(
        subject.pair_identity for subject in reverse
    )


def test_one_pair_identity_survives_before_and_after_displacement(exact_pair):
    current = exact_pair_occurrences(
        exact_pair, _source("current", b"ba---ab")
    )

    assert {occurrence.pair_identity for occurrence in current} == {
        exact_pair.pair_identity
    }
    assert {occurrence.direction for occurrence in current} == {"before", "after"}
    assert {occurrence.displacement for occurrence in current} == {1, 5}
    assert len({occurrence.occurrence_identity for occurrence in current}) == 4


def test_compare_reports_only_the_ordered_coordinate_distinction(exact_pair):
    current = exact_pair_occurrences(
        exact_pair, _source("current", b"ba---ab")
    )
    comparisons = compare_pair_occurrences(
        exact_pair, current, boundary_identity="pair-coordinate-compare"
    )

    assert len(comparisons) == 4
    assert {comparison.distinction for comparison in comparisons} == {False, True}
    assert all(
        comparison.premise_occurrence.pair_identity
        == comparison.current_occurrence.pair_identity
        == exact_pair.pair_identity
        for comparison in comparisons
    )
    assert all(
        not hasattr(comparison, coordinate)
        for comparison in comparisons
        for coordinate in (
            "admitted_material",
            "applicability",
            "meaning",
            "reference",
        )
    )


def test_pair_coordinates_refuse_compression_crossing_and_substitution(exact_pair):
    current = exact_pair_occurrences(
        exact_pair, _source("current", b"ba---ab")
    )
    with pytest.raises(ValueError, match="premise occurrence entered twice"):
        replace(
            exact_pair,
            premise_occurrences=(
                exact_pair.premise_occurrences[0],
                exact_pair.premise_occurrences[0],
            ),
        )
    with pytest.raises(ValueError, match="source crossed its exact Locality"):
        exact_pair_occurrences(
            exact_pair, _source("crossed", b"ab", locality="other-locality")
        )
    with pytest.raises(ValueError, match="yielded source occurrences"):
        recurrent_adjacent_pair_subjects(
            (_source("unrelated", b"abxxab"),),
            (exact_pair.pair_reference,),
        )
    crossed_subject = ExactRecurrentMaterialPairSubject(
        pair_reference=_pair("xy", b"xy", sources=("xy-recorded",)),
        premise_occurrences=recurrent_adjacent_pair_subjects(
            (_source("xy", b"xyxy"),),
            (_pair("xy", b"xy", sources=("xy-recorded",)),),
        )[0].premise_occurrences,
    )
    crossed = exact_pair_occurrences(
        crossed_subject, _source("current-xy", b"xy")
    )[0]
    with pytest.raises(ValueError, match="cannot cross pair identities"):
        ExactMaterialPairCompareOccurrence(
            boundary_identity="crossed-compare",
            occurrence_position=0,
            premise_occurrence=current[0],
            current_occurrence=crossed,
        )


def test_pair_and_compare_carriers_require_exact_types(exact_pair):
    class SubjectSubclass(ExactRecurrentMaterialPairSubject):
        pass

    with pytest.raises(TypeError, match="exact subject"):
        exact_pair_occurrences(
            SubjectSubclass(
                exact_pair.pair_reference,
                exact_pair.premise_occurrences,
            ),
            _source("current", b"ab"),
        )
    with pytest.raises(TypeError, match="exact pair occurrences"):
        compare_pair_occurrences(
            exact_pair,
            [],
            boundary_identity="wrong-carrier-compare",
        )
    with pytest.raises(TypeError, match="exact source reference"):
        exact_pair_occurrences(exact_pair, object())
