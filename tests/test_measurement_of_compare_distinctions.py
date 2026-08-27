"""Measurement preserves exact Compare Distinctions."""

from __future__ import annotations

from copy import deepcopy

import pytest

from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
)
from seed_runtime.events import EventLedger
from seed_runtime.measurement_of_compare_distinctions import (
    COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
    get_recorded_compare_distinction_measurement,
    record_compare_distinction_measurement_act_occurrence,
    record_compare_distinction_measurement_result,
    record_compare_distinction_measurement_subject_to_act_binding,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from tests.binary_input import binary_input


LOCALITY = "compare-distinction-measurement"


def _record_measurement(ledger: EventLedger):
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"ab\nac\n"),
    )
    source = next(
        event
        for event in ledger.list()
        if event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    )
    current_coordinates = read_operator_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
    )
    binding = record_compare_distinction_measurement_subject_to_act_binding(
        ledger,
        comparison_result_occurrence_identity=source.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        (binding.identity,),
        locality_identity=LOCALITY,
        prior=current_coordinates,
    )
    act = record_compare_distinction_measurement_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        (act.identity,),
        locality_identity=LOCALITY,
        prior=current_coordinates,
    )
    result = record_compare_distinction_measurement_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        (result.material["yield_relation_identity"], result.identity),
        locality_identity=LOCALITY,
        prior=current_coordinates,
    )
    return source, result, current_coordinates


def test_measurement_records_every_distinction_of_one_current_compare_result():
    ledger = EventLedger()

    source, result, current_coordinates = _record_measurement(ledger)
    reading = get_recorded_compare_distinction_measurement(
        ledger,
        result.identity,
        prior_coordinates=current_coordinates,
    )

    source_findings = source.material["finding"]["relation_findings"]
    expected = tuple(
        (
            relation_finding["path_position_assertion_reference"],
            relation_finding["pair_subject"],
            reference,
        )
        for relation_finding in source_findings
        for reference in relation_finding["comparison_finding_references"]
    )
    measured = tuple(
        (
            finding["path_position_assertion_reference"],
            finding["pair_subject"],
            finding["recorded_finding_reference"],
        )
        for finding in reading["findings"]
    )

    assert measured == expected
    assert reading["source_result_occurrence_identity"] == source.identity
    assert reading["completeness_boundary"] == {
        "source_result_occurrence_identity": source.identity,
        "distinction_count": len(expected),
    }
    assert all(
        finding["ordered_relation_path_assertion_reference"]
        == source.material["finding"]["subject"][
            "ordered_relation_path_assertion_reference"
        ]
        for finding in reading["findings"]
    )
    assert result.identity in current_coordinates["measurement_occurrences"]


def test_changed_measured_distinction_is_refused():
    ledger = EventLedger()
    _source, result, _current_coordinates = _record_measurement(ledger)
    changed = deepcopy(result.material["findings"][0])
    changed["pair_subject"] = [0, 0]
    result.material["findings"][0] = changed

    with pytest.raises(ValueError, match="not exact"):
        get_recorded_compare_distinction_measurement(ledger, result.identity)


def test_later_source_boundary_makes_current_compare_result_measurable():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"ab\nac\nad\n"),
    )

    compare_results = tuple(
        event
        for event in ledger.list()
        if event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    )
    measurements = tuple(
        event
        for event in ledger.list()
        if event.kind == COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND
    )

    assert len(compare_results) == 2
    assert len(measurements) == 1
    assert measurements[0].material["source_result_occurrence_identity"] == (
        compare_results[0].identity
    )
    assert len(measurements[0].material["findings"]) == sum(
        len(finding["comparison_finding_references"])
        for finding in compare_results[0].material["finding"]["relation_findings"]
    )
