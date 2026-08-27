"""An exact material position establishes pair subjects."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import MaterialAcquisitionResultReference  # noqa: E402
from material_pair_investigation import (  # noqa: E402
    ExactCompareOccurrenceOfMaterialPair,
    ExactOccurrenceOfMaterialPair,
    ExactPositionPremiseOfRecurrentMaterialPair,
    ExactSubjectOfRecurrentMaterialPair,
    ExactReferenceToRecurrentMaterialPair,
    compare_occurrences_of_material_pair,
    exact_occurrences_of_material_pair,
    exact_position_premise_of_recurrent_material_pair,
    exact_subjects_of_recurrent_adjacent_material_pairs,
)


def _source(identity: str, exact: bytes, *, locality: str = "pair-locality"):
    return MaterialAcquisitionResultReference(
        recorded_occurrence_identity=f"{identity}-recorded",
        locality_identity=locality,
        act_occurrence_identity=f"{identity}-act",
        result_identity=f"{identity}-result",
        yield_relation_identity=f"{identity}-yield",
        exact_material=exact,
    )


def _pair(
    identity: str,
    exact: bytes,
    *,
    locality: str = "pair-locality",
    sources: tuple[str, ...] = ("premise-recorded",),
):
    return ExactReferenceToRecurrentMaterialPair(
        recorded_occurrence_identity=f"{identity}-measurement",
        recurrence_assertion_position=2,
        count_assertion_position=1,
        locality_identity=locality,
        source_occurrence_identities=sources,
        completeness_boundary_identity=f"{identity}-boundary",
        exact_material=exact,
    )


@pytest.fixture
def exact_pair():
    subjects = exact_subjects_of_recurrent_adjacent_material_pairs(
        (_source("premise", b"abxxab"),), (_pair("ab", b"ab"),)
    )
    assert len(subjects) == 1
    return subjects[0]


def test_recurrence_not_adjacency_alone_warrants_one_pair_subject():
    one = _source("one", b"ab")
    two = _source("two", b"abxxab")

    assert exact_subjects_of_recurrent_adjacent_material_pairs(
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
    subjects = exact_subjects_of_recurrent_adjacent_material_pairs(
        (two,), (pair,)
    )

    assert len(subjects) == 1
    subject = subjects[0]
    assert subject.reference_to_recurrent_material_pair == pair
    assert len(subject.premise_occurrences_of_material_pair) == 2
    assert {
        occurrence.exact_material for occurrence in subject.premise_occurrences_of_material_pair
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

    forward = exact_subjects_of_recurrent_adjacent_material_pairs((first, second), pairs)
    reverse = exact_subjects_of_recurrent_adjacent_material_pairs((second, first), pairs)

    assert tuple(subject.pair_identity for subject in forward) == tuple(
        subject.pair_identity for subject in reverse
    )


def test_pair_subject_order_follows_first_exact_material_positions():
    source = _source("source", b"ba--ba--ab--ab")
    pairs = (
        _pair(
            "ab",
            b"ab",
            sources=(source.recorded_occurrence_identity,),
        ),
        _pair(
            "ba",
            b"ba",
            sources=(source.recorded_occurrence_identity,),
        ),
    )

    subjects = exact_subjects_of_recurrent_adjacent_material_pairs(
        (source,), pairs
    )

    assert tuple(
        subject.reference_to_recurrent_material_pair.exact_material
        for subject in subjects
    ) == (b"ba", b"ab")


def test_one_pair_identity_survives_before_and_after_displacement(exact_pair):
    current = exact_occurrences_of_material_pair(
        exact_pair, _source("current", b"ba---ab")
    )

    assert {occurrence.pair_identity for occurrence in current} == {
        exact_pair.pair_identity
    }
    assert {occurrence.direction for occurrence in current} == {"before", "after"}
    assert {occurrence.displacement for occurrence in current} == {1, 5}
    assert len({occurrence.occurrence_identity for occurrence in current}) == 4


def test_position_premise_of_pair_carries_every_exact_support_occurrence(
    exact_pair,
):
    premise = exact_position_premise_of_recurrent_material_pair(
        exact_pair,
        boundary_identity="position-premise-of-recurrent-material-pair",
    )

    assert type(premise) is ExactPositionPremiseOfRecurrentMaterialPair
    assert premise.subject_of_recurrent_material_pair == exact_pair
    assert premise.relations_of_positions == (("after", 1),)
    assert tuple(
        occurrence.occurrence_identity
        for occurrence in premise.occurrences_supporting_position_premise
    ) == tuple(
        (
            premise.first_reference.source_reference,
            premise.first_reference.position,
            premise.second_reference.position,
        )
        for premise in exact_pair.premise_occurrences_of_material_pair
    )
    assert all(
        occurrence.first_occurrence_reference.source_reference
        .recorded_occurrence_identity
        in exact_pair.reference_to_recurrent_material_pair.source_occurrence_identities
        for occurrence in premise.occurrences_supporting_position_premise
    )


def test_recurrence_and_position_premise_of_pair_discriminate_fresh_material(
    exact_pair,
):
    premise = exact_position_premise_of_recurrent_material_pair(
        exact_pair,
        boundary_identity="position-premise-of-recurrent-material-pair",
    )
    fresh = _source("fresh", b"ab---ba")
    occurrences = exact_occurrences_of_material_pair(exact_pair, fresh)
    comparisons = compare_occurrences_of_material_pair(
        premise,
        occurrences,
        boundary_identity="fresh-pair-coordinate-compare",
    )

    matches = tuple(
        comparison for comparison in comparisons if not comparison.distinction
    )
    conflicts = tuple(
        comparison for comparison in comparisons if comparison.distinction
    )
    assert matches
    assert conflicts
    assert all(
        comparison.matching_support_occurrence_identities
        == tuple(
            occurrence.occurrence_identity
            for occurrence in premise.occurrences_supporting_position_premise
        )
        for comparison in matches
    )
    assert all(
        comparison.matching_support_occurrence_identities == ()
        for comparison in conflicts
    )
    assert all(
        comparison.current_occurrence_of_material_pair.first_occurrence_reference.source_reference
        == fresh
        for comparison in comparisons
    )
    assert fresh.recorded_occurrence_identity not in (
        exact_pair.reference_to_recurrent_material_pair.source_occurrence_identities
    )


def test_position_premise_of_pair_keeps_identity_order_and_distance_distinct(
    exact_pair,
):
    premise = exact_position_premise_of_recurrent_material_pair(
        exact_pair,
        boundary_identity="position-premise-of-recurrent-material-pair",
    )

    same_relation = exact_occurrences_of_material_pair(
        exact_pair, _source("same-relation", b"ab")
    )
    reversed_order = exact_occurrences_of_material_pair(
        exact_pair, _source("reversed-order", b"ba")
    )
    changed_distance = exact_occurrences_of_material_pair(
        exact_pair, _source("changed-distance", b"a---b")
    )

    assert not compare_occurrences_of_material_pair(
        premise, same_relation, boundary_identity="same-relation-compare"
    )[0].distinction
    assert compare_occurrences_of_material_pair(
        premise, reversed_order, boundary_identity="reversed-order-compare"
    )[0].distinction
    assert compare_occurrences_of_material_pair(
        premise, changed_distance, boundary_identity="changed-distance-compare"
    )[0].distinction
    assert exact_occurrences_of_material_pair(
        exact_pair, _source("shuffled-unrelated", b"zz")
    ) == ()

    same_bytes_another_occurrence = exact_occurrences_of_material_pair(
        exact_pair, _source("same-bytes-another-occurrence", b"abxxab")
    )
    assert all(
        occurrence.occurrence_identity
        not in {
            support.occurrence_identity
            for support in premise.occurrences_supporting_position_premise
        }
        for occurrence in same_bytes_another_occurrence
    )
    assert any(
        not comparison.distinction
        for comparison in compare_occurrences_of_material_pair(
            premise,
            same_bytes_another_occurrence,
            boundary_identity="same-bytes-another-occurrence-compare",
        )
    )


def test_compare_reports_only_the_ordered_coordinate_distinction(exact_pair):
    premise = exact_position_premise_of_recurrent_material_pair(
        exact_pair,
        boundary_identity="position-premise-of-recurrent-material-pair",
    )
    current = exact_occurrences_of_material_pair(
        exact_pair, _source("current", b"ba---ab")
    )
    comparisons = compare_occurrences_of_material_pair(
        premise, current, boundary_identity="pair-coordinate-compare"
    )

    assert len(comparisons) == 4
    assert {comparison.distinction for comparison in comparisons} == {False, True}
    assert all(
        comparison.position_premise_of_recurrent_material_pair.pair_identity
        == comparison.current_occurrence_of_material_pair.pair_identity
        == exact_pair.pair_identity
        for comparison in comparisons
    )
    assert all(
        not hasattr(
            comparison.position_premise_of_recurrent_material_pair,
            coordinate,
        )
        for comparison in comparisons
        for coordinate in (
            "candidate",
            "participant",
            "participation",
            "admitted_material",
            "admission",
            "applicability",
            "meaning",
            "reference",
            "standing",
            "yield_relation_identity",
        )
    )
    assert all(
        not hasattr(comparison, coordinate)
        for comparison in comparisons
        for coordinate in (
            "candidate",
            "participant",
            "participation",
            "admitted_material",
            "admission",
            "applicability",
            "meaning",
            "reference",
            "standing",
            "yield_relation_identity",
        )
    )


def test_pair_coordinates_refuse_compression_and_coordinate_substitution(exact_pair):
    current = exact_occurrences_of_material_pair(
        exact_pair, _source("current", b"ba---ab")
    )
    with pytest.raises(ValueError, match="premise occurrence entered twice"):
        replace(
            exact_pair,
            premise_occurrences_of_material_pair=(
                exact_pair.premise_occurrences_of_material_pair[0],
                exact_pair.premise_occurrences_of_material_pair[0],
            ),
        )
    with pytest.raises(ValueError, match="source has a different Locality"):
        exact_occurrences_of_material_pair(
            exact_pair, _source("different", b"ab", locality="other-locality")
        )
    with pytest.raises(ValueError, match="yielded source occurrences"):
        exact_subjects_of_recurrent_adjacent_material_pairs(
            (_source("unrelated", b"abxxab"),),
            (exact_pair.reference_to_recurrent_material_pair,),
        )
    substituted_subject = ExactSubjectOfRecurrentMaterialPair(
        reference_to_recurrent_material_pair=_pair("xy", b"xy", sources=("xy-recorded",)),
        premise_occurrences_of_material_pair=exact_subjects_of_recurrent_adjacent_material_pairs(
            (_source("xy", b"xyxy"),),
            (_pair("xy", b"xy", sources=("xy-recorded",)),),
        )[0].premise_occurrences_of_material_pair,
    )
    substituted = exact_occurrences_of_material_pair(
        substituted_subject, _source("current-xy", b"xy")
    )[0]
    premise = exact_position_premise_of_recurrent_material_pair(
        exact_pair,
        boundary_identity="position-premise-of-recurrent-material-pair",
    )
    with pytest.raises(ValueError, match="cannot cross pair identities"):
        ExactCompareOccurrenceOfMaterialPair(
            boundary_identity="substituted-subject-compare",
            occurrence_position=0,
            position_premise_of_recurrent_material_pair=premise,
            current_occurrence_of_material_pair=substituted,
        )


def test_position_premise_of_pair_refuses_missing_reordered_or_reused_support(
    exact_pair,
):
    premise = exact_position_premise_of_recurrent_material_pair(
        exact_pair,
        boundary_identity="position-premise-of-recurrent-material-pair",
    )
    first, second = premise.occurrences_supporting_position_premise

    with pytest.raises(ValueError, match="entered position premise twice"):
        replace(premise, occurrences_supporting_position_premise=(first, first))
    with pytest.raises(ValueError, match="differs from its exact occurrence support"):
        replace(premise, occurrences_supporting_position_premise=(second, first))
    with pytest.raises(TypeError, match="exact supporting occurrences"):
        replace(premise, occurrences_supporting_position_premise=(first,))
    with pytest.raises(ValueError, match="outside position premise support"):
        compare_occurrences_of_material_pair(
            premise,
            exact_occurrences_of_material_pair(
                exact_pair, _source("premise", b"abxxab")
            ),
            boundary_identity="reused-premise-compare",
        )
    with pytest.raises(ValueError, match="distinct boundaries"):
        compare_occurrences_of_material_pair(
            premise,
            exact_occurrences_of_material_pair(
                exact_pair, _source("later", b"ab")
            ),
            boundary_identity=premise.boundary_identity,
        )


def test_pair_and_compare_carriers_require_exact_types(exact_pair):
    class SubjectSubclass(ExactSubjectOfRecurrentMaterialPair):
        pass

    class PremiseSubclass(ExactPositionPremiseOfRecurrentMaterialPair):
        pass

    class TupleSubclass(tuple):
        pass

    class StrSubclass(str):
        pass

    with pytest.raises(TypeError, match="exact subject"):
        exact_occurrences_of_material_pair(
            SubjectSubclass(
                exact_pair.reference_to_recurrent_material_pair,
                exact_pair.premise_occurrences_of_material_pair,
            ),
            _source("current", b"ab"),
        )
    with pytest.raises(TypeError, match="exact pair occurrences"):
        compare_occurrences_of_material_pair(
            exact_pair,
            [],
            boundary_identity="wrong-carrier-compare",
        )
    premise = exact_position_premise_of_recurrent_material_pair(
        exact_pair,
        boundary_identity="position-premise-of-recurrent-material-pair",
    )
    with pytest.raises(TypeError, match="exact supporting occurrences"):
        replace(
            premise,
            occurrences_supporting_position_premise=TupleSubclass(
                premise.occurrences_supporting_position_premise
            ),
        )
    with pytest.raises(TypeError, match="exact supporting occurrences"):
        exact_position_premise_of_recurrent_material_pair(
            exact_pair,
            boundary_identity=StrSubclass(
                "position-premise-of-recurrent-material-pair"
            ),
        )
    with pytest.raises(TypeError, match="exact pair occurrences"):
        compare_occurrences_of_material_pair(
            PremiseSubclass(
                premise.boundary_identity,
                premise.subject_of_recurrent_material_pair,
                premise.occurrences_supporting_position_premise,
            ),
            exact_occurrences_of_material_pair(exact_pair, _source("later", b"ab")),
            boundary_identity="pair-coordinate-compare",
        )
    with pytest.raises(TypeError, match="exact source reference"):
        exact_occurrences_of_material_pair(exact_pair, object())




WITNESSED_BOOK_COORDINATES = {
    ("book_coordinates", "01.Source.D", "result"): (
        test_recurrence_not_adjacency_alone_warrants_one_pair_subject,
        test_source_order_does_not_select_which_pair_identities_exist,
        test_pair_subject_order_follows_first_exact_material_positions,
        test_one_pair_identity_survives_before_and_after_displacement,
        test_position_premise_of_pair_carries_every_exact_support_occurrence,
        test_recurrence_and_position_premise_of_pair_discriminate_fresh_material,
        test_position_premise_of_pair_keeps_identity_order_and_distance_distinct,
    ),
}
