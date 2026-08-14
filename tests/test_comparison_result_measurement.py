from copy import deepcopy
from collections.abc import Iterator
from dataclasses import replace

import pytest

from seed_runtime.adjacent_pair_measurement import AdjacentPair
from seed_runtime.assertion_comparison import (
    compare_positional_result_assertions,
    record_positional_result_comparison,
)
from seed_runtime.comparison_result_measurement import (
    COMPARISON_RESULT_COUNT_RECORDED_KIND,
    ComparisonResultMeasurementError,
    assertions_of_recorded_comparison_result_count,
    assertions_from_comparison_result_count,
    get_recorded_comparison_result_count_assertion,
    measure_comparison_result_counts,
    record_comparison_result_count,
    record_comparison_result_count_layer,
)
from seed_runtime.events import EventLedger
from tests.test_positional_result_comparison import _record_following


def _record_compare(ledger, *, session_id, left, right):
    return record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id=session_id,
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    )


def test_measurement_counts_exact_results_without_collapsing_difference():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    c = _record_following(ledger, "s3", "it is elsewhere\n", pair)
    first = _record_compare(ledger, session_id="comparisons", left=a, right=b)
    second = _record_compare(ledger, session_id="comparisons", left=a, right=c)

    measured = measure_comparison_result_counts(
        ledger, workspace_id="w", source_session_ids=("comparisons",)
    )
    assert isinstance(measured, Iterator)
    findings = list(measured)
    occupancy = [item for item in findings if item.coordinate == "occupancies"]

    assert len(occupancy) == 2
    assert {item.result_content["same"] for item in occupancy} == {False}
    assert {item.count for item in occupancy} == {1}
    assert {
        item.production_refs[0]["producing_event_id"] for item in occupancy
    } == {first.id, second.id}


def test_measurement_groups_only_identical_complete_result_content():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    first = _record_compare(ledger, session_id="comparisons", left=a, right=b)
    second = _record_compare(ledger, session_id="comparisons", left=a, right=b)

    findings = list(
        measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )
    )
    occupancy = [item for item in findings if item.coordinate == "occupancies"]

    assert len(occupancy) == 1
    assert occupancy[0].count == 2
    assert occupancy[0].production_refs == (
        {
            "producing_event_id": first.id,
            "assertion_id": first.payload["assertions"][1]["dimensions"]["identity"],
        },
        {
            "producing_event_id": second.id,
            "assertion_id": second.payload["assertions"][1]["dimensions"]["identity"],
        },
    )


def test_measurement_boundary_excludes_later_comparison(monkeypatch):
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    c = _record_following(ledger, "s3", "it is elsewhere\n", pair)
    first = _record_compare(ledger, session_id="comparisons", left=a, right=b)
    captured = ledger.capture_boundary()
    original_capture = ledger.capture_boundary

    def capture_then_append():
        _record_compare(ledger, session_id="comparisons", left=a, right=c)
        return captured

    monkeypatch.setattr(ledger, "capture_boundary", capture_then_append)
    findings = list(
        measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )
    )

    refs = {
        reference["producing_event_id"]
        for finding in findings
        for reference in finding.production_refs
    }
    assert refs == {first.id}
    assert all(finding.completeness_boundary == captured for finding in findings)
    monkeypatch.setattr(ledger, "capture_boundary", original_capture)


def test_measurement_requires_declared_established_population():
    ledger = EventLedger()
    with pytest.raises(ComparisonResultMeasurementError, match="absent"):
        measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("missing",)
        )


def test_measurement_refuses_an_empty_comparison_population_eagerly():
    ledger = EventLedger()
    ledger.append("unrelated", "w", {}, session_id="comparisons")

    with pytest.raises(ComparisonResultMeasurementError, match="no recorded"):
        measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )


def test_measurement_replays_the_recorded_compare_before_counting():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    event = _record_compare(ledger, session_id="comparisons", left=a, right=b)
    event.payload["assertions"][0] = deepcopy(event.payload["assertions"][0])
    event.payload["assertions"][0]["dimensions"]["standing"] = "warranted"

    with pytest.raises(ValueError):
        list(
            measure_comparison_result_counts(
                ledger, workspace_id="w", source_session_ids=("comparisons",)
            )
        )


def test_digest_collision_does_not_establish_exact_result_equality(monkeypatch):
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    c = _record_following(ledger, "s3", "it is elsewhere\n", pair)
    _record_compare(ledger, session_id="comparisons", left=a, right=b)
    _record_compare(ledger, session_id="comparisons", left=a, right=c)
    monkeypatch.setattr(
        "seed_runtime.comparison_result_measurement._digest", lambda value: "collision"
    )

    findings = list(
        measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )
    )
    occupancy = [item for item in findings if item.coordinate == "occupancies"]

    assert len(occupancy) == 2
    assert all(item.count == 1 for item in occupancy)


def test_population_validates_each_reused_input_once(monkeypatch):
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    c = _record_following(ledger, "s3", "it is elsewhere\n", pair)
    d = _record_following(ledger, "s4", "it is present\n", pair)
    _record_compare(ledger, session_id="comparisons", left=a, right=b)
    _record_compare(ledger, session_id="comparisons", left=a, right=c)
    _record_compare(ledger, session_id="comparisons", left=a, right=d)

    calls = []
    from seed_runtime import assertion_comparison

    original = assertion_comparison._validate_result_assertion_ingress

    def counted(*args, **kwargs):
        calls.append(args[1].id)
        return original(*args, **kwargs)

    monkeypatch.setattr(
        assertion_comparison, "_validate_result_assertion_ingress", counted
    )

    list(
        measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )
    )

    assert len(calls) == 4
    assert set(calls) == {
        a.producing_event_id,
        b.producing_event_id,
        c.producing_event_id,
        d.producing_event_id,
    }


def test_recording_preserves_exact_set_and_derived_count_separately():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    first = _record_compare(ledger, session_id="comparisons", left=a, right=b)
    second = _record_compare(ledger, session_id="comparisons", left=a, right=b)
    finding = next(
        item
        for item in measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )
        if item.coordinate == "occupancies"
    )

    event = record_comparison_result_count(
        ledger,
        workspace_id="w",
        session_id="counts",
        finding=finding,
    )
    production_set, count, recurrence = event.payload["assertions"]

    assert event.kind == COMPARISON_RESULT_COUNT_RECORDED_KIND
    assert "result_content" not in event.payload
    assert production_set["result"] == "exact_production_set"
    assert production_set["support_basis"]["assertion_refs"] == [
        {
            "producing_event_id": first.id,
            "assertion_id": first.payload["assertions"][1]["dimensions"]["identity"],
        },
        {
            "producing_event_id": second.id,
            "assertion_id": second.payload["assertions"][1]["dimensions"]["identity"],
        },
    ]
    assert production_set["completeness_boundary"] == {
        "commitment": finding.completeness_boundary.commitment
    }
    assert count["result"] == "count"
    assert count["dimensions"]["content"] == {"production_count": 2}
    assert count["support_basis"] == {
        "local_assertion_ids": [production_set["dimensions"]["identity"]]
    }
    assert "completeness_boundary" not in count
    assert recurrence["result"] == "recurrence"
    assert recurrence["dimensions"]["content"] == {
        "recurrence_established": True
    }
    assert "no recurrence" not in recurrence["dimensions"][
        "authority"
    ].lower()
    assert recurrence["support_basis"] == {
        "local_assertion_ids": [count["dimensions"]["identity"]]
    }
    assert "completeness_boundary" not in recurrence
    recovered = assertions_of_recorded_comparison_result_count(event)
    assert [item.result for item in recovered] == [
        "exact_production_set",
        "count",
        "recurrence",
    ]
    assert (
        get_recorded_comparison_result_count_assertion(
            ledger,
            producing_event_id=event.id,
            assertion_id=recurrence["dimensions"]["identity"],
        ).result
        == "recurrence"
    )


def test_count_one_is_recorded_without_a_recurrence_assertion():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    _record_compare(ledger, session_id="comparisons", left=a, right=b)
    finding = next(
        item
        for item in measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )
        if item.coordinate == "occupancies"
    )

    assertions = assertions_from_comparison_result_count(finding)

    assert finding.count == 1
    assert [item["result"] for item in assertions] == [
        "exact_production_set",
        "count",
    ]
    assert all(item["result"] != "recurrence" for item in assertions)


def test_recording_layer_writes_one_event_per_exact_result():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    _record_compare(ledger, session_id="comparisons", left=a, right=b)

    recorded = record_comparison_result_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("comparisons",),
        recording_session_id="counts",
    )
    events = ledger.list_session("w", "counts")

    assert recorded == 12
    assert len(events) == 12
    assert all(event.kind == COMPARISON_RESULT_COUNT_RECORDED_KIND for event in events)
    assert all(len(event.payload["assertions"]) == 2 for event in events)


def test_recorded_assertions_are_occurrence_bound_and_ledger_recoverable():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    _record_compare(ledger, session_id="comparisons", left=a, right=b)
    finding = next(
        item
        for item in measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )
        if item.coordinate == "occupancies"
    )
    event = record_comparison_result_count(
        ledger, workspace_id="w", session_id="counts", finding=finding
    )

    recovered = assertions_of_recorded_comparison_result_count(event)

    assert [item.result for item in recovered] == ["exact_production_set", "count"]
    assert all(item.producing_event_id == event.id for item in recovered)
    assert all(
        get_recorded_comparison_result_count_assertion(
            ledger,
            producing_event_id=event.id,
            assertion_id=item.assertion_id,
        )
        == item
        for item in recovered
    )


def test_recovery_refuses_changed_local_dependency():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    _record_compare(ledger, session_id="comparisons", left=a, right=b)
    finding = next(
        item
        for item in measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )
        if item.coordinate == "occupancies"
    )
    event = record_comparison_result_count(
        ledger, workspace_id="w", session_id="counts", finding=finding
    )
    event.payload["assertions"][1]["support_basis"] = {
        "local_assertion_ids": ["some-other-Assertion"]
    }

    with pytest.raises(ComparisonResultMeasurementError, match="noncanonical"):
        assertions_of_recorded_comparison_result_count(event)


def test_ledger_recovery_refuses_an_incomplete_production_set():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    _record_compare(ledger, session_id="comparisons", left=a, right=b)
    _record_compare(ledger, session_id="comparisons", left=a, right=b)
    finding = next(
        item
        for item in measure_comparison_result_counts(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )
        if item.coordinate == "occupancies"
    )
    event = record_comparison_result_count(
        ledger,
        workspace_id="w",
        session_id="counts",
        finding=replace(finding, production_refs=finding.production_refs[:1]),
    )
    count = event.payload["assertions"][1]

    with pytest.raises(ComparisonResultMeasurementError):
        get_recorded_comparison_result_count_assertion(
            ledger,
            producing_event_id=event.id,
            assertion_id=count["dimensions"]["identity"],
        )
