from copy import deepcopy

import pytest

from tests.binary_input import binary_input
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)

import seed_runtime.byte_measurement as byte_measurement_module
import seed_runtime.comparison_of_recorded_byte_pair_measurements as comparison_module
import seed_runtime.operator_locality_standing as operator_standing_module
from seed_runtime.byte_measurement import (
    record_byte_measurement_subject_to_act_binding,
    record_byte_measurement_act_occurrence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
    assertions_of_recorded_byte_position_pair_measurement,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RecordedPairMeasurementComparisonError,
    get_recorded_pair_measurement_comparison,
    record_recorded_pair_measurement_comparison_responsibility_assignment,
    record_recorded_pair_measurement_comparison_applicability_act_occurrence,
    record_recorded_pair_measurement_comparison_applicability_result,
    record_recorded_pair_measurement_comparison_act_occurrence,
    record_recorded_pair_measurement_comparison_result,
    _record_recorded_pair_measurement_comparison_from_carried_measurements,
)
from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.witness_material_source import record_witness_material_source
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_console import (
    _latest_carried_pair_premise,
    run_persistent_operator_console,
)
from seed_runtime.supplied_invocation_material import SuppliedWitnessMaterialOccurrence


LOCALITY = "recorded-pair-comparison-locality"
def _pair_measurement(ledger):
    assignment = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=(LOCALITY,),
        recording_locality_identity=LOCALITY,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        ),
    )
    act = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
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
        provenance_occurrence_references=(earlier_source.identity,),
    )
    later = ledger.append(
        "operator.measurement.byte_position_pair_counts_recorded",
        {"test_subject": "later recorded pair Measurement"},
        locality_identity=LOCALITY,
    )
    earlier_assignment = Event(
        identity="earlier-assignment",
        kind="test.recorded_pair_measurement_assignment",
        material={
            "source_occurrence_references": [
                {
                    "material_acquisition_occurrence_identity": (
                        earlier_source.identity
                    )
                }
            ]
        },
        exact_material=None,
        locality_identity=LOCALITY,
    )
    later_assignment = Event(
        identity="later-assignment",
        kind="test.recorded_pair_measurement_assignment",
        material={
            "source_occurrence_references": [
                {
                    "material_acquisition_occurrence_identity": (
                        earlier_source.identity
                    )
                },
                {"material_acquisition_occurrence_identity": added.identity},
            ]
        },
        exact_material=None,
        locality_identity=LOCALITY,
    )

    def measurement_and_findings(_ledger, event_identity):
        if event_identity == earlier.identity:
            return earlier, (), earlier_assignment
        if event_identity == later.identity:
            return later, (), later_assignment
        raise AssertionError("unexpected recorded pair Measurement")

    monkeypatch.setattr(
        comparison_module, "_measurement_and_findings", measurement_and_findings
    )
    monkeypatch.setattr(
        comparison_module,
        "_source_occurrence_references",
        lambda _ledger, event: (
            earlier_source.identity,
            added.identity,
        )
        if event.identity == later.identity
        else (),
    )
    standing = {
        "locality_identity": LOCALITY,
        "through_event_occurrence_identity": later.identity,
        "measurement_occurrences": {earlier.identity: {}, later.identity: {}},
        "exact_result_occurrences": {},
        "representations": {},
    }
    return ledger, earlier_source, added, earlier, later, standing


def _inputs():
    ledger, earlier_source, _acquired, added, earlier, later = _operator_inputs()
    return ledger, earlier_source, added, earlier, later


def _comparison():
    ledger, earlier_source, added, earlier, later = _inputs()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    assignment = record_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        locality_standing=standing,
    )
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    applicability_act = (
        record_recorded_pair_measurement_comparison_applicability_act_occurrence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            locality_standing=standing,
        )
    )
    applicability = record_recorded_pair_measurement_comparison_applicability_result(
        ledger,
        act_occurrence_event_identity=applicability_act.identity,
    )
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    compare_act = record_recorded_pair_measurement_comparison_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
    )
    result = record_recorded_pair_measurement_comparison_result(
        ledger, act_occurrence_event_identity=compare_act.identity
    )
    return ledger, earlier_source, added, earlier, later, assignment, applicability, result


def test_changed_pair_crossing_a_callback_cannot_enter_compare_standing():
    ledger, _earlier_source, _added, earlier, later = _inputs()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    standing_before = deepcopy(standing)
    event_count_before = len(ledger.list())
    earlier.material["assertions"][0]["dimensions"]["content"]["count"] += 1

    with pytest.raises(
        (RecordedPairMeasurementComparisonError, ValueError),
    ):
        _record_recorded_pair_measurement_comparison_from_carried_measurements(
            ledger,
            earlier_measurement=earlier,
            later_measurement=later,
            locality_standing=standing,
        )

    assert standing == standing_before
    assert len(ledger.list()) == event_count_before


def _operator_acquisition(ledger, exact_bytes):
    return record_operator_material_occurrence(
        ledger,
        locality_identity=LOCALITY,
        exact=exact_bytes,
    )


def _operator_inputs(*, acquisition_before_earlier_measurement=False):
    ledger = EventLedger()
    bootstrap = record_witness_material_source(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"bootstrap",
        source_boundary="Witness bootstrap occurrence",
    )

    earlier_source = _operator_acquisition(ledger, b"abab\n")
    if acquisition_before_earlier_measurement:
        acquired = _operator_acquisition(ledger, b"abac\n")
        earlier = _pair_measurement(ledger)
    else:
        earlier = _pair_measurement(ledger)
        acquired = _operator_acquisition(ledger, b"abac\n")
    added = acquired
    later = _pair_measurement(ledger)
    return ledger, earlier_source, acquired, added, earlier, later


def test_operator_acquisition_carries_the_prior_pair_measurement_into_compare():
    ledger, _source, acquired, added, earlier, later = _operator_inputs()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)

    assignment = record_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        locality_standing=standing,
    )

    assert assignment.material["added_occurrence_reference"] == added.identity
    assert assignment.material["input_relation"] == (
        "operator material source occurrence after prior coordinates"
    )
    assert assignment.material[
        "operator_material_source_result_event_identity"
    ] == acquired.identity
    assert assignment.material[
        "operator_material_source_current_coordinate_reference"
    ] == acquired.material["current_coordinate_reference"]
    assert assignment.material["destination_operator_locality_identity"] == LOCALITY


def test_witness_provenance_does_not_establish_a_compare_input_relation(monkeypatch):
    ledger, earlier_source, added, earlier, later, standing = (
        _witness_compare_input_testimony(monkeypatch)
    )

    assert added.material["provenance_occurrence_references"] == [
        earlier_source.identity
    ]

    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="Witness provenance establishes no comparison input relation",
    ):
        record_recorded_pair_measurement_comparison_responsibility_assignment(
            ledger,
            earlier_result_event_identity=earlier.identity,
            later_result_event_identity=later.identity,
            locality_standing=standing,
        )


def test_operator_acquisition_before_the_premise_cannot_supply_compare():
    ledger, _source, _acquired, _added, earlier, later = _operator_inputs(
        acquisition_before_earlier_measurement=True
    )

    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="later Measurement must extend the earlier exact source sequence once",
    ):
        record_recorded_pair_measurement_comparison_responsibility_assignment(
            ledger,
            earlier_result_event_identity=earlier.identity,
            later_result_event_identity=later.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=LOCALITY
            ),
        )


def test_produced_measurements_enter_one_responsible_compare():
    ledger, earlier_source, added, earlier, later, assignment, applicability, result = (
        _comparison()
    )
    recorded = get_recorded_pair_measurement_comparison(ledger, result.identity)

    assert assignment.material["earlier_measurement_reference"][
        "recorded_occurrence_identity"
    ] == earlier.identity
    assert assignment.material["later_measurement_reference"][
        "recorded_occurrence_identity"
    ] == later.identity
    assert assignment.material["added_occurrence_reference"] == added.identity
    assert assignment.material["prior_provenance_occurrence_references"] == []
    assert applicability.material["standing"] == "applicable"
    assert len(recorded["participation_of_input_in_compare"]) == 2

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
    assert findings["unknown_findings"] == []

    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    assert result.identity in standing["comparison_result_occurrences"]


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


def test_witness_provenance_does_not_supply_the_carried_compare_rung(monkeypatch):
    ledger, earlier_source, added, earlier, later, standing = (
        _witness_compare_input_testimony(monkeypatch)
    )
    standing_before = deepcopy(standing)
    event_count_before = len(ledger.list())

    assert added.material["provenance_occurrence_references"] == [
        earlier_source.identity
    ]
    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="Witness provenance establishes no comparison input relation",
    ):
        _record_recorded_pair_measurement_comparison_from_carried_measurements(
            ledger,
            earlier_measurement=earlier,
            later_measurement=later,
            locality_standing=standing,
        )

    assert standing == standing_before
    assert len(ledger.list()) == event_count_before


def test_measurement_availability_without_standing_cannot_supply_compare():
    ledger, _source, _added, earlier, later = _inputs()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    standing["measurement_occurrences"].pop(earlier.identity)
    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="each exact Measurement result in current Standing",
    ):
        record_recorded_pair_measurement_comparison_responsibility_assignment(
            ledger,
            earlier_result_event_identity=earlier.identity,
            later_result_event_identity=later.identity,
            locality_standing=standing,
        )


def test_corrupted_compare_yield_is_refused():
    ledger, *_rest, result = _comparison()
    yield_relation = ledger.get(result.material["yield_relation_identity"])
    assert yield_relation is not None
    yield_relation.material["result_identity"] = "crossed-result"
    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="exact Yield",
    ):
        get_recorded_pair_measurement_comparison(ledger, result.identity)


def test_one_result_read_validates_each_pair_measurement_once(monkeypatch):
    ledger, _first_source, _added, earlier, later, *_middle, result = _comparison()
    original = comparison_module._measurement_and_findings
    calls = []

    def counted(ledger, event_identity):
        calls.append(event_identity)
        return original(ledger, event_identity)

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


def test_result_reader_preserves_its_exact_assignment_and_public_getter_delegates(
    monkeypatch,
):
    ledger, *_inputs, assignment, _applicability, result = _comparison()
    material, assignment_reading = (
        comparison_module._recorded_pair_measurement_comparison_reading(
            ledger, result.identity
        )
    )

    assert material == result.material
    assert assignment_reading[0] == assignment

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


def test_standing_replay_carries_one_validated_assignment_across_comparison_stages(
    monkeypatch,
):
    ledger, *_rest, result = _comparison()
    calls = []
    original = (
        operator_standing_module._recorded_pair_comparison_assignment_reading
    )

    def witnessed(ledger, event_identity):
        calls.append(event_identity)
        return original(ledger, event_identity)

    monkeypatch.setattr(
        operator_standing_module,
        "_recorded_pair_comparison_assignment_reading",
        witnessed,
    )
    monkeypatch.setattr(comparison_module, "_assignment_reading", witnessed)

    standing = read_operator_locality_standing(
        ledger, locality_identity=LOCALITY
    )
    assignment_identity = result.material[
        "responsibility_assignment_reference"
    ]["recorded_occurrence_identity"]
    assert result.identity in standing["comparison_result_occurrences"]
    assert calls == [assignment_identity]

    get_recorded_pair_measurement_comparison(ledger, result.identity)
    assert calls == [assignment_identity, assignment_identity]


@pytest.mark.parametrize("callback", ("assignment", "input", "append"))
def test_standing_replay_carry_refuses_callback_change_and_leaks_no_state(
    monkeypatch, callback
):
    ledger, _source, _added, earlier, _later, assignment, _applicability, _result = (
        _comparison()
    )
    assignment_material = deepcopy(assignment.material)
    earlier_material = deepcopy(earlier.material)
    original = (
        operator_standing_module._recorded_pair_comparison_applicability_act_reading
    )
    callback_crossed = False

    def cross_after_assignment(*args, **kwargs):
        nonlocal callback_crossed
        if not callback_crossed:
            callback_crossed = True
            if callback == "assignment":
                assignment.material["responsibility"] = "changed after validation"
            elif callback == "input":
                earlier.material["measurement_rule"] = "changed after validation"
            else:
                ledger.append(
                    "test.unrelated_callback",
                    {"unknown": ["append after comparison assignment validation"]},
                    locality_identity="unrelated-callback",
                )
        return original(*args, **kwargs)

    monkeypatch.setattr(
        operator_standing_module,
        "_recorded_pair_comparison_applicability_act_reading",
        cross_after_assignment,
    )
    with pytest.raises(RecordedPairMeasurementComparisonError):
        read_operator_locality_standing(ledger, locality_identity=LOCALITY)

    assignment.material.clear()
    assignment.material.update(assignment_material)
    earlier.material.clear()
    earlier.material.update(earlier_material)
    assert read_operator_locality_standing(
        ledger, locality_identity=LOCALITY
    )["comparison_result_occurrences"]


def test_interleaved_comparisons_keep_distinct_ephemeral_assignment_readings(
    monkeypatch,
):
    ledger, _source, _added, earlier, later = _inputs()
    first = record_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        ),
    )
    second = record_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        ),
    )

    def finish(assignment):
        applicability_act = record_recorded_pair_measurement_comparison_applicability_act_occurrence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=LOCALITY
            ),
        )
        applicability = record_recorded_pair_measurement_comparison_applicability_result(
            ledger,
            act_occurrence_event_identity=applicability_act.identity,
        )
        act = record_recorded_pair_measurement_comparison_act_occurrence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=LOCALITY
            ),
        )
        return record_recorded_pair_measurement_comparison_result(
            ledger, act_occurrence_event_identity=act.identity
        )

    results = (finish(first), finish(second))
    calls = []
    original = (
        operator_standing_module._recorded_pair_comparison_assignment_reading
    )

    def witnessed(ledger, event_identity):
        calls.append(event_identity)
        return original(ledger, event_identity)

    monkeypatch.setattr(
        operator_standing_module,
        "_recorded_pair_comparison_assignment_reading",
        witnessed,
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=LOCALITY
    )

    assert all(
        result.identity in standing["comparison_result_occurrences"]
        for result in results
    )
    assert calls == [first.identity, second.identity]


def test_compare_reads_exact_findings_without_rebuilding_full_assertion_carriers(
    monkeypatch,
):
    ledger, *_rest, result = _comparison()

    def full_carrier_is_not_a_compare_input(*args, **kwargs):
        raise AssertionError("Compare rebuilt one full Assertion carrier")

    monkeypatch.setattr(
        byte_measurement_module,
        "RecordedBytePairAssertion",
        full_carrier_is_not_a_compare_input,
    )

    recorded = get_recorded_pair_measurement_comparison(ledger, result.identity)
    assert recorded["findings"]["conflicting_findings"]


def test_later_result_read_revalidates_changed_pair_measurement_yield_relation():
    ledger, _first_source, _added, earlier, _later, *_middle, result = _comparison()
    get_recorded_pair_measurement_comparison(ledger, result.identity)
    yield_relation = ledger.get(earlier.material["yield_relation_identity"])
    assert yield_relation is not None
    yield_relation.material["result_identity"] = "crossed-pair-result"

    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="intact recorded byte-position-pair Measurement",
    ):
        get_recorded_pair_measurement_comparison(ledger, result.identity)


def test_supplied_local_material_records_pair_measurements():
    ledger = EventLedger()

    def provider(command, supply):
        assert command == b"!opaque\n"
        supply(
            SuppliedWitnessMaterialOccurrence(
                exact_bytes=b"first",
                source_boundary="first opaque occurrence",
            )
        )
        supply(
            SuppliedWitnessMaterialOccurrence(
                exact_bytes=b"second",
                source_boundary="second opaque occurrence",
            )
        )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="operator-locality",
        input_stream=binary_input(b"!opaque\n"),
        operator_invocation_provider=provider,
    )

    kinds = tuple(event.kind for event in ledger.list())
    assert kinds.count("operator.measurement.byte_counts_recorded") == 3
    assert kinds.count("operator.measurement.byte_position_pair_counts_recorded") == 2


def test_pair_premise_remains_carried_across_the_prior_compare_result():
    ledger, _first_source, _added, _first, second, *_middle, first_compare = (
        _comparison()
    )
    third_source = _operator_acquisition(ledger, b"abad\n")
    third = _pair_measurement(ledger)

    second_binding = (
        record_recorded_pair_measurement_comparison_responsibility_assignment(
            ledger,
            earlier_result_event_identity=second.identity,
            later_result_event_identity=third.identity,
            locality_standing=read_operator_locality_standing(
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
    current = read_operator_locality_standing(ledger, locality_identity=LOCALITY)

    carried, premise = _latest_carried_pair_premise(
        ledger,
        current,
        locality_identity=LOCALITY,
    )

    assert carried == current
    assert premise == second


@pytest.mark.parametrize(
    ("exact_material", "exact_ab_count", "has_recurrence"),
    (
        (b"ab", 1, False),
        (b"abxxab", 2, True),
    ),
)
def test_first_exact_material_records_pair_counts(
    exact_material, exact_ab_count, has_recurrence
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
    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair_measurements[0].identity
    )
    ab_assertions = tuple(
        assertion
        for assertion in assertions or ()
        if assertion.content == (ord("a"), ord("b"))
    )
    count_assertion = next(
        assertion for assertion in ab_assertions if assertion.result == "count"
    )
    assert (
        count_assertion.material["dimensions"]["content"]["count"]
        == exact_ab_count
    )
    assert any(
        assertion.result == "recurrence" for assertion in ab_assertions
    ) is has_recurrence
