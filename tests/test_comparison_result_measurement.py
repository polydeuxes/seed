from copy import deepcopy
from collections.abc import Iterator

import pytest

from seed_runtime.adjacent_pair_measurement import AdjacentPair
from seed_runtime.assertion_comparison import (
    compare_positional_result_assertions,
    record_positional_result_comparison,
)
from seed_runtime.comparison_result_measurement import (
    ComparisonResultMeasurementError,
    measure_comparison_result_counts,
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
        list(
            measure_comparison_result_counts(
                ledger, workspace_id="w", source_session_ids=("missing",)
            )
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
