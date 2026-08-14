"""One-layer Measurement over the owned recurrence-subject surface."""

from copy import deepcopy

import pytest

from seed_runtime.adjacent_pair_measurement import AdjacentPair
from seed_runtime.assertion_comparison import (
    compare_positional_result_assertions,
    record_positional_result_comparison,
)
from seed_runtime.comparison_result_measurement import (
    record_comparison_result_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.recurrence_subject_measurement import (
    RECURRENCE_SUBJECT_COORDINATES,
    RECURRENCE_SUBJECT_COORDINATES_RECORDED_KIND,
    RecurrenceSubjectMeasurementError,
    _assertion_identity,
    assertions_of_recorded_recurrence_subject_coordinates,
    get_recorded_recurrence_subject_coordinate_assertion,
    measure_recurrence_subject_coordinates,
    record_recurrence_subject_coordinate_layer,
)
from tests.test_positional_result_comparison import _record_following


def _record_compare(ledger, left, right):
    return record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparisons",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    )


def _recurrence_inputs():
    ledger = EventLedger()
    first_pair = AdjacentPair("it", "is")
    first_left = _record_following(
        ledger, "s1", "it is here\n", first_pair
    )
    first_right = _record_following(
        ledger, "s2", "it is there\n", first_pair
    )
    second_pair = AdjacentPair("this", "is")
    second_left = _record_following(
        ledger, "s3", "this is here\n", second_pair
    )
    second_right = _record_following(
        ledger, "s4", "this is there\n", second_pair
    )
    for _ in range(2):
        _record_compare(ledger, first_left, first_right)
        _record_compare(ledger, second_left, second_right)
    record_comparison_result_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("comparisons",),
        recording_session_id="counts",
    )
    return ledger


def test_measurement_emits_exactly_the_validation_owned_immediate_surface():
    ledger = _recurrence_inputs()

    findings = list(
        measure_recurrence_subject_coordinates(
            ledger, workspace_id="w", source_session_ids=("counts",)
        )
    )

    assert findings
    assert all(
        tuple(name for name, _ in finding.coordinates)
        == RECURRENCE_SUBJECT_COORDINATES
        for finding in findings
    )
    compared_subject = dict(findings[0].coordinates)["compared_subject"]
    assert isinstance(compared_subject, dict)
    assert "measurement_form" in compared_subject
    assert all(
        name != "measurement_form"
        for finding in findings
        for name, _ in finding.coordinates
    )


def test_same_exact_coordinate_value_has_one_identity_and_distinct_yields():
    ledger = _recurrence_inputs()
    recorded = record_recurrence_subject_coordinate_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("counts",),
        recording_session_id="coordinate-results",
    )
    events = ledger.list_session("w", "coordinate-results")

    assert recorded == len(events)
    assert recorded > 1
    assert all(
        event.kind == RECURRENCE_SUBJECT_COORDINATES_RECORDED_KIND
        for event in events
    )
    coordinate_results = [
        assertion
        for event in events
        for assertion in assertions_of_recorded_recurrence_subject_coordinates(event)
        if assertion.coordinate == "coordinate"
        and assertion.payload["dimensions"]["content"]["exact_value"] == "standing"
    ]
    assert len(coordinate_results) == 2
    assert len({item.assertion_id for item in coordinate_results}) == 1
    assert len({item.yielding_event_id for item in coordinate_results}) == 2


def test_recording_preserves_one_source_and_three_distinct_results_per_occurrence():
    ledger = _recurrence_inputs()
    record_recurrence_subject_coordinate_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("counts",),
        recording_session_id="coordinate-results",
    )
    event = ledger.list_session("w", "coordinate-results")[0]
    reconstructed = assertions_of_recorded_recurrence_subject_coordinates(event)

    assert len(reconstructed) == 3
    assert {item.coordinate for item in reconstructed} == set(
        RECURRENCE_SUBJECT_COORDINATES
    )
    assert all(
        item.payload["support_basis"]
        == {"assertion_refs": [event.payload["source_assertion_ref"]]}
        for item in reconstructed
    )
    assert all(
        get_recorded_recurrence_subject_coordinate_assertion(
            ledger,
            yielding_event_id=event.id,
            assertion_id=item.assertion_id,
        )
        == item
        for item in reconstructed
    )


def test_validation_refuses_a_coordinate_value_that_disagrees_with_its_source():
    ledger = _recurrence_inputs()
    record_recurrence_subject_coordinate_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("counts",),
        recording_session_id="coordinate-results",
    )
    event = ledger.list_session("w", "coordinate-results")[0]
    assertion = event.payload["assertions"][0]
    assertion["dimensions"]["content"] = {"exact_value": "invented"}
    assertion["dimensions"]["identity"] = _assertion_identity(
        coordinate=assertion["assertion_subject"]["coordinate"],
        value="invented",
        scope=assertion["assertion_scope"],
    )

    with pytest.raises(RecurrenceSubjectMeasurementError):
        get_recorded_recurrence_subject_coordinate_assertion(
            ledger,
            yielding_event_id=event.id,
            assertion_id=assertion["dimensions"]["identity"],
        )


def test_validation_refuses_a_self_consistent_scope_not_carried_by_its_source():
    ledger = _recurrence_inputs()
    record_recurrence_subject_coordinate_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("counts",),
        recording_session_id="coordinate-results",
    )
    event = ledger.list_session("w", "coordinate-results")[0]
    assertion = event.payload["assertions"][0]
    assertion["assertion_scope"] = {
        "workspace_id": "w",
        "source_session_ids": ["different-comparison-session"],
    }
    assertion["dimensions"]["identity"] = _assertion_identity(
        coordinate=assertion["assertion_subject"]["coordinate"],
        value=assertion["dimensions"]["content"]["exact_value"],
        scope=assertion["assertion_scope"],
    )

    with pytest.raises(RecurrenceSubjectMeasurementError):
        get_recorded_recurrence_subject_coordinate_assertion(
            ledger,
            yielding_event_id=event.id,
            assertion_id=assertion["dimensions"]["identity"],
        )


def test_measurement_refuses_a_inputs_with_no_recurrence_assertions():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    left = _record_following(ledger, "s1", "it is here\n", pair)
    right = _record_following(ledger, "s2", "it is there\n", pair)
    _record_compare(ledger, left, right)
    record_comparison_result_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("comparisons",),
        recording_session_id="counts",
    )

    with pytest.raises(RecurrenceSubjectMeasurementError, match="no reconstructed"):
        measure_recurrence_subject_coordinates(
            ledger, workspace_id="w", source_session_ids=("counts",)
        )


def test_structural_validation_refuses_nested_coordinate_promotion():
    ledger = _recurrence_inputs()
    record_recurrence_subject_coordinate_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("counts",),
        recording_session_id="coordinate-results",
    )
    event = ledger.list_session("w", "coordinate-results")[0]
    promoted = deepcopy(event.payload["assertions"][0])
    promoted["assertion_subject"]["coordinate"] = "measurement_form"
    promoted["dimensions"]["content"] = {"exact_value": "following"}
    event.payload["assertions"][0] = promoted

    with pytest.raises(RecurrenceSubjectMeasurementError):
        assertions_of_recorded_recurrence_subject_coordinates(event)
