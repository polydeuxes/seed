"""Counts over canonical recurrence-subject coordinate Assertions."""

from copy import deepcopy

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.coordinate_assertion_measurement import (
    COORDINATE_ASSERTION_COUNT_RECORDED_KIND,
    CoordinateAssertionMeasurementError,
    _assertion_identity,
    assertions_of_recorded_coordinate_assertion_count,
    get_recorded_coordinate_assertion_count,
    measure_coordinate_assertion_counts,
    record_coordinate_assertion_count_layer,
)
from seed_runtime.recurrence_subject_measurement import (
    record_recurrence_subject_coordinate_layer,
)
from tests.test_recurrence_subject_measurement import _recurrence_population


def _coordinate_population():
    ledger = _recurrence_population()
    record_recurrence_subject_coordinate_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("counts",),
        recording_session_id="coordinate-results",
    )
    return ledger


def test_measurement_groups_only_by_canonical_coordinate_assertion_identity():
    ledger = _coordinate_population()

    findings = list(
        measure_coordinate_assertion_counts(
            ledger,
            workspace_id="w",
            source_session_ids=("coordinate-results",),
        )
    )
    source_assertions = [
        assertion
        for event in ledger.list_session("w", "coordinate-results")
        for assertion in event.payload["assertions"]
    ]

    assert len(findings) == len(
        {assertion["dimensions"]["identity"] for assertion in source_assertions}
    )
    assert sum(finding.count for finding in findings) == len(source_assertions)
    assert all(
        {ref["assertion_id"] for ref in finding.production_refs}
        == {finding.source_assertion_id}
        for finding in findings
    )


def test_recording_preserves_set_count_and_only_evidenced_recurrence():
    ledger = _coordinate_population()
    recorded = record_coordinate_assertion_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("coordinate-results",),
        recording_session_id="coordinate-counts",
    )
    events = ledger.list_session("w", "coordinate-counts")

    assert recorded == len(events)
    assert all(event.kind == COORDINATE_ASSERTION_COUNT_RECORDED_KIND for event in events)
    reconstructed = [
        assertions_of_recorded_coordinate_assertion_count(event) for event in events
    ]
    assert any([item.result for item in group] == ["exact_production_set", "count"] for group in reconstructed)
    assert any(
        [item.result for item in group]
        == ["exact_production_set", "count", "recurrence"]
        for group in reconstructed
    )
    for group in reconstructed:
        by_result = {item.result: item for item in group}
        production_set = by_result["exact_production_set"]
        count = by_result["count"]
        refs = production_set.payload["support_basis"]["assertion_refs"]
        assert count.payload["dimensions"]["content"] == {
            "production_count": len(refs)
        }
        assert count.payload["support_basis"] == {
            "local_assertion_ids": [production_set.assertion_id]
        }
        assert ("recurrence" in by_result) == (len(refs) > 1)
        if "recurrence" in by_result:
            assert by_result["recurrence"].payload["support_basis"] == {
                "local_assertion_ids": [count.assertion_id]
            }


def test_recorded_results_are_occurrence_bound_and_ledger_addressable():
    ledger = _coordinate_population()
    record_coordinate_assertion_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("coordinate-results",),
        recording_session_id="coordinate-counts",
    )
    event = ledger.list_session("w", "coordinate-counts")[0]
    reconstructed = assertions_of_recorded_coordinate_assertion_count(event)

    assert all(
        get_recorded_coordinate_assertion_count(
            ledger,
            producing_event_id=event.id,
            assertion_id=item.assertion_id,
        )
        == item
        for item in reconstructed
    )


def test_validation_refuses_a_self_consistent_invented_production_set():
    ledger = _coordinate_population()
    record_coordinate_assertion_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("coordinate-results",),
        recording_session_id="coordinate-counts",
    )
    event = next(
        item
        for item in ledger.list_session("w", "coordinate-counts")
        if len(item.payload["assertions"][0]["support_basis"]["assertion_refs"])
        > 2
    )
    production_set = event.payload["assertions"][0]
    count = event.payload["assertions"][1]
    recurrence = event.payload["assertions"][2]
    refs = deepcopy(production_set["support_basis"]["assertion_refs"][:-1])
    production_set["support_basis"] = {"assertion_refs": refs}
    production_set["dimensions"]["content"] = {"production_refs": refs}
    set_id = _assertion_identity(
        result="exact_production_set",
        subject=production_set["assertion_subject"],
        scope=production_set["assertion_scope"],
        content=production_set["dimensions"]["content"],
    )
    production_set["dimensions"]["identity"] = set_id
    count["dimensions"]["content"] = {"production_count": len(refs)}
    count_id = _assertion_identity(
        result="count",
        subject=count["assertion_subject"],
        scope=count["assertion_scope"],
        content=count["dimensions"]["content"],
    )
    count["dimensions"]["identity"] = count_id
    count["support_basis"] = {"local_assertion_ids": [set_id]}
    recurrence["support_basis"] = {"local_assertion_ids": [count_id]}

    with pytest.raises(CoordinateAssertionMeasurementError):
        get_recorded_coordinate_assertion_count(
            ledger,
            producing_event_id=event.id,
            assertion_id=set_id,
        )


def test_validation_refuses_self_consistent_content_not_carried_by_source():
    ledger = _coordinate_population()
    record_coordinate_assertion_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("coordinate-results",),
        recording_session_id="coordinate-counts",
    )
    event = ledger.list_session("w", "coordinate-counts")[0]
    production_set, count, *rest = event.payload["assertions"]
    for assertion in event.payload["assertions"]:
        assertion["assertion_subject"] = deepcopy(assertion["assertion_subject"])
        assertion["assertion_subject"]["exact_coordinate_value"] = "invented"
    set_id = _assertion_identity(
        result="exact_production_set",
        subject=production_set["assertion_subject"],
        scope=production_set["assertion_scope"],
        content=production_set["dimensions"]["content"],
    )
    production_set["dimensions"]["identity"] = set_id
    count_id = _assertion_identity(
        result="count",
        subject=count["assertion_subject"],
        scope=count["assertion_scope"],
        content=count["dimensions"]["content"],
    )
    count["dimensions"]["identity"] = count_id
    count["support_basis"] = {"local_assertion_ids": [set_id]}
    if rest:
        recurrence = rest[0]
        recurrence_id = _assertion_identity(
            result="recurrence",
            subject=recurrence["assertion_subject"],
            scope=recurrence["assertion_scope"],
            content=recurrence["dimensions"]["content"],
        )
        recurrence["dimensions"]["identity"] = recurrence_id
        recurrence["support_basis"] = {"local_assertion_ids": [count_id]}

    with pytest.raises(CoordinateAssertionMeasurementError):
        get_recorded_coordinate_assertion_count(
            ledger,
            producing_event_id=event.id,
            assertion_id=set_id,
        )


def test_measurement_refuses_an_absent_declared_source_session():
    ledger = _coordinate_population()
    with pytest.raises(CoordinateAssertionMeasurementError, match="absent"):
        measure_coordinate_assertion_counts(
            ledger,
            workspace_id="w",
            source_session_ids=("missing",),
        )


def test_measurement_refuses_an_empty_coordinate_population_eagerly():
    ledger = EventLedger()
    ledger.append("unrelated", "w", {}, session_id="coordinate-results")

    with pytest.raises(CoordinateAssertionMeasurementError, match="no reconstructed"):
        measure_coordinate_assertion_counts(
            ledger,
            workspace_id="w",
            source_session_ids=("coordinate-results",),
        )
