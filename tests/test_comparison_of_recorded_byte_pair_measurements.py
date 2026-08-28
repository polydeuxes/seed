"""Earlier and later pair results are exact Compare subjects."""

from copy import deepcopy

import pytest

from tests.binary_input import binary_input
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)

import seed_runtime.byte_measurement as byte_measurement_module
import seed_runtime.comparison_of_recorded_byte_pair_measurements as comparison_module
from seed_runtime.byte_measurement import (
    record_byte_measurement_subject_to_act_binding,
    record_byte_measurement_act_occurrence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
    result_positions_of_recorded_byte_position_pair_measurement,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    RecordedPairMeasurementComparisonError,
    get_recorded_pair_measurement_comparison,
    record_recorded_pair_measurement_comparison_subject_to_act_binding,
    record_recorded_pair_measurement_comparison_applicability_subject_to_act_binding,
    record_recorded_pair_measurement_comparison_applicability_act_occurrence,
    record_recorded_pair_measurement_comparison_applicability_result,
    record_recorded_pair_measurement_comparison_act_occurrence,
    record_recorded_pair_measurement_comparison_result,
    _record_recorded_pair_measurement_comparison_from_carried_measurements,
)
from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.witness_material_source import record_witness_material_source
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates
from seed_runtime.operator_console import (
    _latest_carried_pair_premise,
    run_persistent_operator_console,
)
from seed_runtime.supplied_invocation_material import SuppliedWitnessMaterialOccurrence


LOCALITY = "recorded-pair-comparison-locality"
def _pair_measurement(ledger):
    binding = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=(LOCALITY,),
        recording_locality_identity=LOCALITY,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=LOCALITY
        ),
    )
    act = record_byte_measurement_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=LOCALITY
        ),
    )
    byte_result = record_byte_measurement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    return record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_result.identity,
        recording_locality_identity=LOCALITY,
    )


def _witness_compare_input_testimony(monkeypatch):
    ledger = EventLedger()
    earlier_source = record_witness_material_source(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abab",
        source_boundary="earlier supplied occurrence",
    )
    earlier = ledger.append(
        "operator.measurement.byte_position_pair_counts_recorded",
        {"test_subject": "earlier recorded pair Measurement"},
        locality_identity=LOCALITY,
    )
    added = record_witness_material_source(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abac",
        source_boundary="later supplied occurrence",
        source_occurrence_references=(earlier_source.identity,),
    )
    later = ledger.append(
        "operator.measurement.byte_position_pair_counts_recorded",
        {"test_subject": "later recorded pair Measurement"},
        locality_identity=LOCALITY,
    )
    earlier_binding = Event(
        identity="earlier-binding",
        kind="test.recorded_pair_measurement_binding",
        material={
            "source_occurrence_references": [
                {
                    "material_result_occurrence_identity": (
                        earlier_source.identity
                    )
                }
            ]
        },
        exact_material=None,
        locality_identity=LOCALITY,
    )
    later_binding = Event(
        identity="later-binding",
        kind="test.recorded_pair_measurement_binding",
        material={
            "source_occurrence_references": [
                {
                    "material_result_occurrence_identity": (
                        earlier_source.identity
                    )
                },
                {"material_result_occurrence_identity": added.identity},
            ]
        },
        exact_material=None,
        locality_identity=LOCALITY,
    )

    def measurement_and_findings(_ledger, event_identity, **_coordinates):
        if event_identity == earlier.identity:
            return earlier, (), earlier_binding
        if event_identity == later.identity:
            return later, (), later_binding
        raise AssertionError("unexpected recorded pair Measurement")

    monkeypatch.setattr(
        comparison_module, "_measurement_and_findings", measurement_and_findings
    )
    monkeypatch.setattr(
        comparison_module,
        "_source_occurrence_references",
        lambda _ledger, event, *, prior_coordinates=None: (
            earlier_source.identity,
            added.identity,
        )
        if event.identity == later.identity
        else (),
    )
    current_coordinates = {
        "locality_identity": LOCALITY,
        "through_event_occurrence_identity": later.identity,
        "measurement_occurrences": {earlier.identity: {}, later.identity: {}},
        "exact_result_occurrences": {},
        "representations": {},
    }
    return ledger, earlier_source, added, earlier, later, current_coordinates


def _inputs():
    ledger, earlier_source, _acquired, added, earlier, later = _operator_inputs()
    return ledger, earlier_source, added, earlier, later


def _comparison():
    ledger, earlier_source, added, earlier, later = _inputs()
    current_coordinates = read_operator_current_coordinates(ledger, locality_identity=LOCALITY)
    binding = record_recorded_pair_measurement_comparison_subject_to_act_binding(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = read_operator_current_coordinates(ledger, locality_identity=LOCALITY)
    applicability_binding = (
        record_recorded_pair_measurement_comparison_applicability_subject_to_act_binding(
            ledger,
            comparison_binding_event_identity=binding.identity,
            current_coordinates=current_coordinates,
        )
    )
    current_coordinates = read_operator_current_coordinates(ledger, locality_identity=LOCALITY)
    applicability_act = (
        record_recorded_pair_measurement_comparison_applicability_act_occurrence(
            ledger,
            applicability_binding_event_identity=applicability_binding.identity,
            current_coordinates=current_coordinates,
        )
    )
    applicability = record_recorded_pair_measurement_comparison_applicability_result(
        ledger,
        act_occurrence_event_identity=applicability_act.identity,
    )
    current_coordinates = read_operator_current_coordinates(ledger, locality_identity=LOCALITY)
    compare_act = record_recorded_pair_measurement_comparison_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=current_coordinates,
    )
    result = record_recorded_pair_measurement_comparison_result(
        ledger, act_occurrence_event_identity=compare_act.identity
    )
    return ledger, earlier_source, added, earlier, later, binding, applicability, result


def test_changed_pair_between_coordinate_read_and_recording_cannot_enter_compare_current_coordinates():
    ledger, _earlier_source, _added, earlier, later = _inputs()
    current_coordinates = read_operator_current_coordinates(ledger, locality_identity=LOCALITY)
    coordinates_before = deepcopy(current_coordinates)
    event_count_before = len(ledger.list())
    earlier.material["result_positions"][0]["dimensions"]["content"]["count"] += 1

    with pytest.raises(
        (RecordedPairMeasurementComparisonError, ValueError),
    ):
        _record_recorded_pair_measurement_comparison_from_carried_measurements(
            ledger,
            earlier_measurement=earlier,
            later_measurement=later,
            current_coordinates=current_coordinates,
        )

    assert current_coordinates == coordinates_before
    assert len(ledger.list()) == event_count_before


def _operator_source(ledger, exact_bytes):
    return record_operator_material_occurrence(
        ledger,
        locality_identity=LOCALITY,
        exact=exact_bytes,
    )


def _operator_inputs(*, source_before_earlier_measurement=False):
    ledger = EventLedger()
    bootstrap = record_witness_material_source(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"bootstrap",
        source_boundary="Witness bootstrap occurrence",
    )

    earlier_source = _operator_source(ledger, b"abab\n")
    if source_before_earlier_measurement:
        source_event = _operator_source(ledger, b"abac\n")
        earlier = _pair_measurement(ledger)
    else:
        earlier = _pair_measurement(ledger)
        source_event = _operator_source(ledger, b"abac\n")
    added = source_event
    later = _pair_measurement(ledger)
    return ledger, earlier_source, source_event, added, earlier, later


def test_operator_source_carries_the_prior_pair_measurement_into_compare():
    ledger, _source, source_event, added, earlier, later = _operator_inputs()
    current_coordinates = read_operator_current_coordinates(ledger, locality_identity=LOCALITY)

    binding = record_recorded_pair_measurement_comparison_subject_to_act_binding(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        current_coordinates=current_coordinates,
    )

    assert binding.material["added_occurrence_reference"] == added.identity
    assert binding.material[
        "operator_material_source_result_event_identity"
    ] == source_event.identity
    assert binding.material[
        "operator_material_source_current_coordinate_reference"
    ] == source_event.material["current_coordinate_reference"]
    assert binding.material["destination_operator_locality_identity"] == LOCALITY


def test_carried_measurements_record_one_complete_comparison():
    ledger, _source, _source_event, _added, earlier, later = _operator_inputs()
    result, current_coordinates = (
        _record_recorded_pair_measurement_comparison_from_carried_measurements(
            ledger,
            earlier_measurement=earlier,
            later_measurement=later,
            current_coordinates=read_operator_current_coordinates(
                ledger, locality_identity=LOCALITY
            ),
        )
    )

    reading = get_recorded_pair_measurement_comparison(ledger, result.identity)
    assert reading["result_identity"] == result.material["result_identity"]
    assert result.identity in current_coordinates["comparison_result_occurrences"]


def test_witness_source_references_do_not_establish_a_recorded_pair_compare_input(monkeypatch):
    ledger, earlier_source, added, earlier, later, current_coordinates = (
        _witness_compare_input_testimony(monkeypatch)
    )

    assert added.material["source_occurrence_references"] == [
        earlier_source.identity
    ]

    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="Witness source references establish no recorded-pair Compare input",
    ):
        record_recorded_pair_measurement_comparison_subject_to_act_binding(
            ledger,
            earlier_result_event_identity=earlier.identity,
            later_result_event_identity=later.identity,
            current_coordinates=current_coordinates,
        )


def test_operator_source_before_the_premise_cannot_supply_compare():
    ledger, _source, _acquired, _added, earlier, later = _operator_inputs(
        source_before_earlier_measurement=True
    )

    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="later Measurement must extend the earlier exact source sequence once",
    ):
        record_recorded_pair_measurement_comparison_subject_to_act_binding(
            ledger,
            earlier_result_event_identity=earlier.identity,
            later_result_event_identity=later.identity,
            current_coordinates=read_operator_current_coordinates(
                ledger, locality_identity=LOCALITY
            ),
        )


def test_produced_measurements_enter_one_compare():
    ledger, earlier_source, added, earlier, later, binding, applicability, result = (
        _comparison()
    )
    recorded = get_recorded_pair_measurement_comparison(ledger, result.identity)
    applicability_binding = ledger.get(
        applicability.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
    )

    assert applicability_binding is not None
    assert applicability_binding.identity != binding.identity
    assert "comparison_act_identity" not in binding.material
    assert "applicability_act_identity" not in applicability_binding.material
    assert applicability_binding.material["addressed_act_identity"] == (
        binding.material["exact_act_identity"]
    )
    assert binding.material["earlier_measurement_reference"][
        "recorded_occurrence_identity"
    ] == earlier.identity
    assert binding.material["later_measurement_reference"][
        "recorded_occurrence_identity"
    ] == later.identity
    assert binding.material["added_occurrence_reference"] == added.identity
    assert applicability.material["applicability"] == "applicable"
    assert recorded["subject_to_act_binding_reference"][
        "recorded_occurrence_identity"
    ] == binding.identity

    findings = recorded["findings"]
    count_ab = next(
        item
        for item in findings["conflicting_findings"]
        if item["subject"] == {"result": "count", "content": [97, 98]}
    )
    assert count_ab["earlier_content"] == {
        "input_count": 2,
        "occurrences_carrying": 1,
        "count": 2,
    }
    assert count_ab["later_content"] == {
        "input_count": 3,
        "occurrences_carrying": 2,
        "count": 3,
    }
    assert any(
        item["subject"] == {"result": "recurrence", "content": [97, 98]}
        for item in findings["same_content_findings"]
    )
    assert any(
        item["subject"] == {"result": "count", "content": [97, 99]}
        for item in findings["findings_of_later_result"]
    )

    current_coordinates = read_operator_current_coordinates(ledger, locality_identity=LOCALITY)
    assert result.identity in current_coordinates["comparison_result_occurrences"]


def test_same_content_finding_labels_do_not_hide_changed_content():
    ledger, *_rest, result = _comparison()
    findings = get_recorded_pair_measurement_comparison(ledger, result.identity)[
        "findings"
    ]
    conflicting_subjects = {
        (item["subject"]["result"], tuple(item["subject"]["content"]))
        for item in findings["conflicting_findings"]
    }
    assert ("count", (97, 98)) in conflicting_subjects


def test_witness_source_references_do_not_supply_the_carried_compare_rung(monkeypatch):
    ledger, earlier_source, added, earlier, later, current_coordinates = (
        _witness_compare_input_testimony(monkeypatch)
    )
    coordinates_before = deepcopy(current_coordinates)
    event_count_before = len(ledger.list())

    assert added.material["source_occurrence_references"] == [
        earlier_source.identity
    ]
    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="Witness source references establish no recorded-pair Compare input",
    ):
        _record_recorded_pair_measurement_comparison_from_carried_measurements(
            ledger,
            earlier_measurement=earlier,
            later_measurement=later,
            current_coordinates=current_coordinates,
        )

    assert current_coordinates == coordinates_before
    assert len(ledger.list()) == event_count_before


def test_measurement_availability_without_current_coordinates_cannot_supply_compare():
    ledger, _source, _added, earlier, later = _inputs()
    current_coordinates = read_operator_current_coordinates(ledger, locality_identity=LOCALITY)
    current_coordinates["measurement_occurrences"].pop(earlier.identity)
    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="each exact Measurement result in current coordinates",
    ):
        record_recorded_pair_measurement_comparison_subject_to_act_binding(
            ledger,
            earlier_result_event_identity=earlier.identity,
            later_result_event_identity=later.identity,
            current_coordinates=current_coordinates,
        )


def test_corrupted_compare_yield_is_refused():
    ledger, *_rest, result = _comparison()
    yield_relation = ledger.get(result.material["yield_relation_identity"])
    assert yield_relation is not None
    yield_relation.material["result_identity"] = "changed-result"
    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="exact Yield",
    ):
        get_recorded_pair_measurement_comparison(ledger, result.identity)


def test_one_result_read_validates_each_pair_measurement_once(monkeypatch):
    ledger, _first_source, _added, earlier, later, *_middle, result = _comparison()
    original = comparison_module._measurement_and_findings
    calls = []

    def counted(ledger, event_identity, **coordinates):
        calls.append(event_identity)
        return original(ledger, event_identity, **coordinates)

    monkeypatch.setattr(comparison_module, "_measurement_and_findings", counted)

    get_recorded_pair_measurement_comparison(ledger, result.identity)
    assert calls == [earlier.identity, later.identity]

    get_recorded_pair_measurement_comparison(ledger, result.identity)
    assert calls == [
        earlier.identity,
        later.identity,
        earlier.identity,
        later.identity,
    ]


def test_result_reader_preserves_its_exact_binding_and_public_getter_delegates(
    monkeypatch,
):
    ledger, *_inputs, binding, _applicability, result = _comparison()
    material, binding_reading = (
        comparison_module._recorded_pair_measurement_comparison_reading(
            ledger, result.identity
        )
    )

    assert material == result.material
    assert binding_reading[0] == binding

    calls = []
    original = comparison_module._recorded_pair_measurement_comparison_reading

    def witnessed(ledger, event_identity):
        calls.append(event_identity)
        return original(ledger, event_identity)

    monkeypatch.setattr(
        comparison_module,
        "_recorded_pair_measurement_comparison_reading",
        witnessed,
    )
    assert get_recorded_pair_measurement_comparison(
        ledger, result.identity
    ) == result.material
    assert calls == [result.identity]


def test_interleaved_comparisons_remain_distinct_in_current_coordinates():
    ledger, _source, _added, earlier, later = _inputs()
    first = record_recorded_pair_measurement_comparison_subject_to_act_binding(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=LOCALITY
        ),
    )
    second = record_recorded_pair_measurement_comparison_subject_to_act_binding(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=LOCALITY
        ),
    )

    def finish(binding):
        applicability_binding = (
            record_recorded_pair_measurement_comparison_applicability_subject_to_act_binding(
                ledger,
                comparison_binding_event_identity=binding.identity,
                current_coordinates=read_operator_current_coordinates(
                    ledger, locality_identity=LOCALITY
                ),
            )
        )
        applicability_act = record_recorded_pair_measurement_comparison_applicability_act_occurrence(
            ledger,
            applicability_binding_event_identity=applicability_binding.identity,
            current_coordinates=read_operator_current_coordinates(
                ledger, locality_identity=LOCALITY
            ),
        )
        applicability = record_recorded_pair_measurement_comparison_applicability_result(
            ledger,
            act_occurrence_event_identity=applicability_act.identity,
        )
        act = record_recorded_pair_measurement_comparison_act_occurrence(
            ledger,
            subject_to_act_binding_event_identity=binding.identity,
            applicability_result_event_identity=applicability.identity,
            current_coordinates=read_operator_current_coordinates(
                ledger, locality_identity=LOCALITY
            ),
        )
        return record_recorded_pair_measurement_comparison_result(
            ledger, act_occurrence_event_identity=act.identity
        )

    results = (finish(first), finish(second))
    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=LOCALITY
    )

    assert all(
        result.identity in current_coordinates["comparison_result_occurrences"]
        for result in results
    )


def test_compare_reads_exact_findings_without_rebuilding_full_result_position_readers(
    monkeypatch,
):
    ledger, *_rest, result = _comparison()

    def full_carrier_is_not_a_compare_input(*args, **kwargs):
        raise AssertionError("Compare rebuilt one full result position carrier")

    monkeypatch.setattr(
        byte_measurement_module,
        "RecordedBytePairResultPosition",
        full_carrier_is_not_a_compare_input,
    )

    recorded = get_recorded_pair_measurement_comparison(ledger, result.identity)
    assert recorded["findings"]["conflicting_findings"]


def test_later_result_read_revalidates_changed_pair_measurement_yield_relation():
    ledger, _first_source, _added, earlier, _later, *_middle, result = _comparison()
    get_recorded_pair_measurement_comparison(ledger, result.identity)
    yield_relation = ledger.get(earlier.material["yield_relation_identity"])
    assert yield_relation is not None
    yield_relation.material["result_identity"] = "changed-pair-result"

    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="intact recorded byte-position-pair Measurement",
    ):
        get_recorded_pair_measurement_comparison(ledger, result.identity)


def test_supplied_local_material_records_pair_measurements():
    ledger = EventLedger()

    def provider(command, supply):
        assert command == b"!\n"
        supply(
            SuppliedWitnessMaterialOccurrence(
                exact_bytes=b"a",
                source_boundary="first opaque occurrence",
            )
        )
        supply(
            SuppliedWitnessMaterialOccurrence(
                exact_bytes=b"b",
                source_boundary="second opaque occurrence",
            )
        )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="operator-locality",
        input_stream=binary_input(b"!\n"),
        operator_invocation_provider=provider,
    )

    kinds = tuple(event.kind for event in ledger.list())
    assert kinds.count("operator.measurement.byte_counts_recorded") == 3
    assert kinds.count("operator.measurement.byte_position_pair_counts_recorded") == 2


def test_pair_premise_remains_carried_across_the_prior_compare_result():
    ledger, _first_source, _added, _first, second, *_middle, first_compare = (
        _comparison()
    )
    third_source = _operator_source(ledger, b"abad\n")
    third = _pair_measurement(ledger)

    second_binding = (
        record_recorded_pair_measurement_comparison_subject_to_act_binding(
            ledger,
            earlier_result_event_identity=second.identity,
            later_result_event_identity=third.identity,
            current_coordinates=read_operator_current_coordinates(
                ledger, locality_identity=LOCALITY
            ),
        )
    )

    assert third_source.material["current_coordinate_reference"] == {
        "locality_identity": LOCALITY,
        "through_event_occurrence_identity": first_compare.identity,
    }
    assert second_binding.material["earlier_measurement_reference"][
        "recorded_occurrence_identity"
    ] == second.identity
    assert second_binding.material["earlier_measurement_reference"][
        "result_identity"
    ] == second.material["result_identity"]


def test_console_addresses_the_latest_carried_pair_after_a_compare_result():
    ledger, _first_source, _added, _first, second, *_middle, _comparison_result = (
        _comparison()
    )
    current = read_operator_current_coordinates(ledger, locality_identity=LOCALITY)

    carried, premise = _latest_carried_pair_premise(
        ledger,
        current,
        locality_identity=LOCALITY,
    )

    assert carried == current
    assert premise == second


@pytest.mark.parametrize(
    ("exact_material", "exact_pair", "exact_pair_count", "has_recurrence"),
    (
        (b"ab", b"ab", 1, False),
        (b"aaa", b"aa", 2, True),
    ),
)
def test_first_exact_material_records_pair_counts(
    exact_material, exact_pair, exact_pair_count, has_recurrence
):
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(exact_material),
    )

    pair_measurements = tuple(
        event
        for event in ledger.list()
        if event.kind == "operator.measurement.byte_position_pair_counts_recorded"
    )
    assert len(pair_measurements) == 1
    result_positions = result_positions_of_recorded_byte_position_pair_measurement(
        ledger, pair_measurements[0].identity
    )
    pair_result_positions = tuple(
        result_position
        for result_position in result_positions or ()
        if result_position.content == tuple(exact_pair)
    )
    count_result_position = next(
        result_position for result_position in pair_result_positions if result_position.result == "count"
    )
    assert (
        count_result_position.material["dimensions"]["content"]["count"]
        == exact_pair_count
    )
    assert any(
        result_position.result == "recurrence" for result_position in pair_result_positions
    ) is has_recurrence


def test_compare_requires_prior_and_later_pair_results():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"\na\n"),
    )

    pair_results = tuple(
        event
        for event in ledger.list()
        if event.kind == "operator.measurement.byte_position_pair_counts_recorded"
    )
    compare_results = tuple(
        event
        for event in ledger.list()
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
    )

    assert len(pair_results) == 2
    assert len(compare_results) == 1
    reading = get_recorded_pair_measurement_comparison(
        ledger,
        compare_results[0].identity,
    )
    binding = ledger.get(
        reading["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
    )
    assert binding is not None
    assert (
        binding.material["earlier_measurement_reference"][
            "recorded_occurrence_identity"
        ]
        == pair_results[0].identity
    )
    assert (
        binding.material["later_measurement_reference"][
            "recorded_occurrence_identity"
        ]
        == pair_results[1].identity
    )


def test_pair_compare_uses_supplied_coordinates_with_ordered_paths(monkeypatch):
    ledger = EventLedger()

    def historical_pair_coordinates_are_not_read(*_args, **_coordinates):
        raise AssertionError(
            "pair Compare must use the exact current coordinates already supplied"
        )

    monkeypatch.setattr(
        byte_measurement_module,
        "_prior_coordinates_for_pair_subject_to_act_binding",
        historical_pair_coordinates_are_not_read,
    )
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"ab\nac\n"),
    )

    pair_results = tuple(
        event
        for event in ledger.list()
        if event.kind == "operator.measurement.byte_position_pair_counts_recorded"
    )
    compare_results = tuple(
        event
        for event in ledger.list()
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
    )
    assert len(pair_results) == 2
    assert len(compare_results) == 1
    binding_reference = compare_results[0].material[
        "subject_to_act_binding_reference"
    ]
    binding = ledger.get(binding_reference["recorded_occurrence_identity"])
    assert binding is not None
    assert binding.material["earlier_measurement_reference"][
        "recorded_occurrence_identity"
    ] == pair_results[0].identity
    assert binding.material["later_measurement_reference"][
        "recorded_occurrence_identity"
    ] == pair_results[1].identity
