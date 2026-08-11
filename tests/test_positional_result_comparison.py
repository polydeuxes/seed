"""Literal Compare over exact positional result Assertion productions."""

from io import StringIO

import pytest

from seed_runtime.adjacent_pair_measurement import (
    AdjacentPair,
    assertion_of_recorded_adjacent_pair_result,
    measure_adjacent_pair,
    measure_after,
    record_pair_measurements,
)
from seed_runtime.assertion_comparison import (
    POSITIONAL_RESULT_COORDINATES,
    AssertionComparisonError,
    compare_positional_result_assertions,
)
from seed_runtime.events import EventLedger
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.preserved_material_measurement import (
    preserved_ingress_occurrences,
    record_measurement_finding,
)


def _record_following(ledger, session_id, material, pair=AdjacentPair("it", "is")):
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id=session_id,
        input_stream=StringIO(material + "exit\n"),
        output_stream=StringIO(),
    )
    occurrences = preserved_ingress_occurrences(
        ledger, workspace_id="w", session_id=session_id
    )
    premise = record_measurement_finding(
        ledger,
        workspace_id="w",
        session_id=session_id,
        finding=measure_after(
            occurrences,
            pair.left,
            counting_scope=f"recorded exchange {session_id}",
        ),
    )
    event = record_pair_measurements(
        ledger,
        workspace_id="w",
        session_id=session_id,
        pair=pair,
        findings=measure_adjacent_pair(
            occurrences,
            pair,
            counting_scope=f"recorded exchange {session_id}",
            premise_event_id=premise.id,
        ),
        completeness_boundary=ledger.capture_boundary(),
    )["following"]
    return assertion_of_recorded_adjacent_pair_result(event)


@pytest.fixture
def comparable():
    ledger = EventLedger()
    left = _record_following(ledger, "s1", "it is red\n")
    right = _record_following(ledger, "s2", "it is blue\n")
    return ledger, left, right


def test_same_exact_subject_supplies_a_bounded_compare(comparable):
    ledger, left, right = comparable
    before = tuple(event.id for event in ledger.list("w"))

    comparison = compare_positional_result_assertions(
        ledger, (left.reference, right.reference)
    )
    distinctions = {item.coordinate: item for item in comparison.distinctions}

    assert comparison.act == "Compare"
    assert comparison.owner == "this bounded comparison occurrence"
    assert comparison.subject == left.payload["assertion_subject"]
    assert set(distinctions) == set(POSITIONAL_RESULT_COORDINATES)
    assert distinctions["positions_measured"].same is True
    assert distinctions["occupancies"].same is False
    assert distinctions["occupancies"].present == (True, True)
    assert distinctions["scope"].same is False
    assert distinctions["standing"].same is True
    assert tuple(event.id for event in ledger.list("w")) == before


def test_compare_preserves_exact_occurrence_bound_inputs(comparable):
    ledger, left, right = comparable
    comparison = compare_positional_result_assertions(
        ledger, (left.reference, right.reference)
    )

    assert [item.assertion_id for item in comparison.inputs] == [
        left.assertion_id,
        right.assertion_id,
    ]
    assert [item.producing_event_id for item in comparison.inputs] == [
        left.producing_event_id,
        right.producing_event_id,
    ]


@pytest.mark.parametrize(
    ("coordinate", "field"),
    (
        ("source_provenance", "source_provenance"),
        ("responsibility", "responsibility"),
        ("authority_warrant", "authority_warrant"),
    ),
)
def test_compare_does_not_erase_established_fidelity_coordinates(
    comparable, coordinate, field
):
    ledger, left, right = comparable
    right.payload["dimensions"][field] = f"different {field}"

    comparison = compare_positional_result_assertions(
        ledger, (left.reference, right.reference)
    )
    distinction = {
        item.coordinate: item for item in comparison.distinctions
    }[coordinate]

    assert distinction.present == (True, True)
    assert distinction.same is False
    assert distinction.values[0] != distinction.values[1]


def test_compare_refuses_different_carried_subjects(comparable):
    ledger, left, _ = comparable
    other = _record_following(
        ledger, "s3", "it may change\n", pair=AdjacentPair("it", "may")
    )

    with pytest.raises(AssertionComparisonError, match="one exact carried"):
        compare_positional_result_assertions(
            ledger, (left.reference, other.reference)
        )


@pytest.mark.parametrize("references", [(), ({"producing_event_id": "x", "assertion_id": "y"},)])
def test_compare_requires_exactly_two_inputs(comparable, references):
    ledger, _, _ = comparable
    with pytest.raises(AssertionComparisonError, match="exactly two"):
        compare_positional_result_assertions(ledger, references)


def test_compare_refuses_one_production_twice(comparable):
    ledger, left, _ = comparable
    with pytest.raises(AssertionComparisonError, match="cannot be compared with itself"):
        compare_positional_result_assertions(
            ledger, (left.reference, left.reference)
        )


def test_compare_does_not_claim_relation_recurrence_or_meaning(comparable):
    ledger, left, right = comparable
    comparison = compare_positional_result_assertions(
        ledger, (left.reference, right.reference)
    )
    represented = str(comparison).lower()

    assert "relation=" not in represented
    assert "recurrence=" not in represented
    assert "meaning=" not in represented
    assert "similarity=" not in represented
