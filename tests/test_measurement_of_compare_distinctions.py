"""Measurement preserves exact Compare Distinctions."""

from __future__ import annotations

from copy import deepcopy

import pytest

import seed_runtime.byte_measurement as byte_measurement
from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    get_recorded_pair_measurement_comparison,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.measurement_of_compare_distinctions import (
    COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
    compare_distinction_measurement_references_from_current_coordinates,
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
            relation_finding["path_position_result_reference"],
            reference,
        )
        for relation_finding in source_findings
        for reference in relation_finding["comparison_finding_references"]
    )
    measured = tuple(
        (
            finding["path_position_result_reference"],
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
        finding["ordered_relation_path_result_position_reference"]
        == source.material["finding"]["subject"][
            "ordered_relation_path_result_position_reference"
        ]
        for finding in reading["findings"]
    )
    assert result.identity in current_coordinates["measurement_occurrences"]


def test_changed_measured_distinction_is_refused():
    ledger = EventLedger()
    _source, result, _current_coordinates = _record_measurement(ledger)
    changed = deepcopy(result.material["findings"][0])
    changed["recorded_finding_reference"]["subject"]["content"] = [0, 0]
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


def test_material_slice_measures_every_current_compare_result():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"a\nab\nabc\n"),
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

    assert len(compare_results) == 3
    assert tuple(
        measurement.material["source_result_occurrence_identity"]
        for measurement in measurements
    ) == tuple(result.identity for result in compare_results)


def test_material_slice_preserves_current_coordinates_through_pair_measurement(
    monkeypatch,
):
    ledger = EventLedger()
    original = byte_measurement._read_byte_measurement_subject_to_act_binding
    reads = 0

    def require_current_coordinates(*args, **kwargs):
        nonlocal reads
        reads += 1
        assert kwargs.get("prior_coordinates") is not None
        return original(*args, **kwargs)

    monkeypatch.setattr(
        byte_measurement,
        "_read_byte_measurement_subject_to_act_binding",
        require_current_coordinates,
    )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"a\nab\nabc\n"),
    )

    assert reads > 0


def test_exact_measurement_reference_addresses_the_two_results():
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
    references = compare_distinction_measurement_references_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )

    assert len(references) == 1
    earlier = ledger.get(references[0].earlier_result_occurrence_identity)
    later = ledger.get(references[0].later_result_occurrence_identity)
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

    assert references[0].exact_measurement_reference == (
        earlier_pair_subject["later_measurement_reference"]
    )
    assert references[0].exact_measurement_reference == (
        later_pair_subject["earlier_measurement_reference"]
    )


def test_one_exact_measurement_reference_can_address_multiple_results_on_each_side():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"a\nab\nabc\nabcd\n"),
    )
    current_coordinates = read_operator_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
    )
    references = compare_distinction_measurement_references_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )

    result_occurrences_by_measurement: dict[str, tuple[set[str], set[str]]] = {}
    for reference in references:
        measurement_occurrence_identity = reference.exact_measurement_reference[
            "recorded_occurrence_identity"
        ]
        earlier, later = result_occurrences_by_measurement.setdefault(
            measurement_occurrence_identity,
            (set(), set()),
        )
        earlier.add(reference.earlier_result_occurrence_identity)
        later.add(reference.later_result_occurrence_identity)

    assert sorted(
        (len(earlier), len(later))
        for earlier, later in result_occurrences_by_measurement.values()
    ) == [(1, 2), (2, 3)]


def test_exact_measurement_references_are_reconstructed_after_restart(tmp_path):
    database = tmp_path / "compare-distinction-measurements.sqlite"
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
    before = compare_distinction_measurement_references_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )
    durable = SQLiteEventLedger(str(database))
    durable.append_many(ledger.list())
    durable.close()

    reopened = SQLiteEventLedger(str(database))
    after = compare_distinction_measurement_references_from_current_coordinates(
        reopened,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )

    assert after == before


def test_measurement_reference_does_not_depend_on_projection_order():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"a\nab\nabc\nabcd\n"),
    )
    current_coordinates = read_operator_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
    )
    expected = compare_distinction_measurement_references_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )
    reordered_coordinates = deepcopy(current_coordinates)
    reordered_coordinates["measurement_occurrences"] = dict(
        reversed(tuple(current_coordinates["measurement_occurrences"].items()))
    )

    observed = compare_distinction_measurement_references_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=reordered_coordinates,
    )

    def exact_references(reference):
        return (
            reference.earlier_result_occurrence_identity,
            reference.later_result_occurrence_identity,
            reference.exact_measurement_reference[
                "recorded_occurrence_identity"
            ],
        )

    assert sorted(map(exact_references, observed)) == sorted(
        map(exact_references, expected)
    )


def test_separate_occurrences_can_carry_equal_measured_content():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"ab\nab\nab\nab\n"),
    )
    current_coordinates = read_operator_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
    )
    references = compare_distinction_measurement_references_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )

    def measured_content(reading):
        return tuple(
            (
                    finding["path_position_result_reference"][
                        "result_position"
                    ],
                finding["recorded_finding_reference"]["subject"]["content"],
                finding["recorded_finding_reference"]["finding_category"],
                finding["recorded_finding_reference"]["subject"],
            )
            for finding in reading["findings"]
        )

    readings = tuple(
        (
            get_recorded_compare_distinction_measurement(
                ledger,
                reference.earlier_result_occurrence_identity,
                prior_coordinates=current_coordinates,
            ),
            get_recorded_compare_distinction_measurement(
                ledger,
                reference.later_result_occurrence_identity,
                prior_coordinates=current_coordinates,
            ),
        )
        for reference in references
    )

    assert len(readings) == 2
    assert measured_content(readings[0][0]) != measured_content(readings[0][1])
    assert readings[1][0]["findings"] != readings[1][1]["findings"]
    assert measured_content(readings[1][0]) == measured_content(readings[1][1])
    assert (
        readings[1][0]["source_result_occurrence_identity"]
        != readings[1][1]["source_result_occurrence_identity"]
    )
