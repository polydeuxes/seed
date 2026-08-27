"""Measurement preserves exact Compare Distinctions."""

from __future__ import annotations

from copy import deepcopy

import pytest

from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    get_recorded_pair_measurement_comparison,
)
from seed_runtime.events import EventLedger
from seed_runtime.measurement_of_compare_distinctions import (
    COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
    compare_distinction_measurement_subjects_from_current_coordinates,
    get_recorded_compare_distinction_measurement,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates
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
    result = next(
        event
        for event in ledger.list()
        if event.kind == COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND
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


def test_material_slice_measures_its_current_compare_result_before_eof():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"ab\nac\n"),
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

    assert len(compare_results) == 1
    assert len(measurements) == 1
    assert measurements[0].material["source_result_occurrence_identity"] == (
        compare_results[0].identity
    )
    assert len(measurements[0].material["findings"]) == sum(
        len(finding["comparison_finding_references"])
        for finding in compare_results[0].material["finding"]["relation_findings"]
    )


def test_successive_measurements_share_one_exact_pair_measurement():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"ab\nac\nad\n"),
    )
    current_coordinates = read_operator_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
    )
    subjects = compare_distinction_measurement_subjects_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )

    assert len(subjects) == 1
    earlier = ledger.get(subjects[0].earlier_result_occurrence_identity)
    later = ledger.get(subjects[0].later_result_occurrence_identity)
    earlier_source = ledger.get(
        earlier.material["source_result_occurrence_identity"]
    )
    later_source = ledger.get(later.material["source_result_occurrence_identity"])
    earlier_pair_reference = earlier_source.material["finding"]["subject"][
        "recorded_pair_comparison_result_reference"
    ]
    later_pair_reference = later_source.material["finding"]["subject"][
        "recorded_pair_comparison_result_reference"
    ]
    earlier_pair = get_recorded_pair_measurement_comparison(
        ledger,
        earlier_pair_reference["recorded_occurrence_identity"],
    )
    later_pair = get_recorded_pair_measurement_comparison(
        ledger,
        later_pair_reference["recorded_occurrence_identity"],
    )
    earlier_pair_subject = earlier_pair["subject_to_act_binding_reference"][
        "subject_reference"
    ]
    later_pair_subject = later_pair["subject_to_act_binding_reference"][
        "subject_reference"
    ]

    assert subjects[0].shared_measurement_reference == (
        earlier_pair_subject["later_measurement_reference"]
    )
    assert subjects[0].shared_measurement_reference == (
        later_pair_subject["earlier_measurement_reference"]
    )
