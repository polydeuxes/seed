"""Same-position Measurement findings are Compare subjects."""

from __future__ import annotations

from copy import deepcopy

import pytest

import seed_runtime.comparison_of_shared_position_measurement_with_recorded_pair_findings as comparison_module
import seed_runtime.comparison_of_recorded_byte_pair_measurements as recorded_pair_comparison_module
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    _record_byte_measurement_act_occurrence_from_current_coordinates,
    _record_byte_measurement_result_from_current_coordinates,
    _record_byte_measurement_subject_to_act_binding_from_current_coordinates,
    result_positions_of_recorded_byte_position_pair_measurement,
    _record_byte_position_pair_count_layer_from_current_coordinates,
)
from seed_runtime.comparison_of_shared_position_measurement_with_recorded_pair_findings import (
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
    SharedPositionMeasurementPairFindingCompareSubject,
    get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings,
    get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability,
    move_recorded_shared_position_comparison_finding_result_content_to_locality,
    recorded_distinction_pins_from_current_coordinates,
    record_comparison_of_shared_position_measurement_with_recorded_pair_findings_act_occurrence,
    record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_act_occurrence,
    record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_subject_to_act_binding,
    record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_result,
    record_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding,
    record_comparison_of_shared_position_measurement_with_recorded_pair_findings_result,
    record_shared_position_measurement_pair_finding_compare_bindings_from_current_coordinates,
    record_shared_position_measurement_pair_finding_compare_applicability_act_occurrences_from_current_coordinates,
    record_shared_position_measurement_pair_finding_compare_applicability_from_current_coordinates,
    record_applicable_shared_position_measurement_pair_finding_compare_act_occurrence_from_current_coordinates,
    record_shared_position_measurement_pair_finding_compare_results_from_current_coordinates,
    read_shared_position_measurement_pair_finding_compare_applicability_results_and_acts,
    unbound_shared_position_measurement_pair_finding_compare_subjects_in_current_coordinates,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    get_recorded_pair_measurement_comparison,
    record_recorded_pair_measurement_comparison_act_occurrence,
    record_recorded_pair_measurement_comparison_applicability_subject_to_act_binding,
    record_recorded_pair_measurement_comparison_applicability_act_occurrence,
    record_recorded_pair_measurement_comparison_applicability_result,
    record_recorded_pair_measurement_comparison_subject_to_act_binding,
    record_recorded_pair_measurement_comparison_result,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    _record_recurrent_pair_position_measurement_act_from_current_coordinates,
    measure_positions_for_recurrent_byte_pair_result_positions,
    record_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
    references_to_recorded_recurrent_byte_pair_occurrence_positions,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    record_shared_position_applicability_act_occurrence,
    record_shared_position_applicability_result,
    record_shared_position_measurement_act_occurrence,
    record_shared_position_measurement_result,
    record_shared_position_subject_to_act_binding,
)
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.yield_relation import RECORDED_YIELD_RELATION_EVENT
from tests.binary_input import binary_input
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
    record_operator_material_occurrence_from_current_coordinates,
)


LOCALITY = "shared-position-measurement-pair-finding-comparison"


def test_compare_requires_current_shared_position_and_pair_results():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"ab\nac\n"),
    )

    applicability_results = tuple(
        event
        for event in ledger.list()
        if event.kind
        == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND
    )
    compare_acts = tuple(
        event
        for event in ledger.list()
        if event.kind
        == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT
    )
    compare_results = tuple(
        event
        for event in ledger.list()
        if event.kind
        == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    )

    assert tuple(
        result.material["applicability"] for result in applicability_results
    ) == ("inapplicable", "applicable")
    assert len(compare_acts) == len(compare_results) == 1
    assert compare_acts[0].material["applicability_result_event_identity"] == (
        applicability_results[1].identity
    )
    assert compare_results[0].material["act_occurrence_event_identity"] == (
        compare_acts[0].identity
    )
    assert len(compare_results[0].material["finding"]["relation_findings"]) == 2
    assert tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
        )
    ) == ()
    assert tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
        )
    ) == ()
    assert all(
        "subject_to_act_binding_reference" not in event.material
        for event in (*applicability_results, *compare_acts, *compare_results)
    )


def test_each_later_pair_result_has_one_prior_pair_result_for_compare():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"ab\nac\nad\n"),
    )

    pair_results = tuple(
        event
        for event in ledger.list()
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
    )
    applicability_results = tuple(
        event
        for event in ledger.list()
        if event.kind
        == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND
    )
    compare_acts = tuple(
        event
        for event in ledger.list()
        if event.kind
        == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT
    )
    compare_results = tuple(
        event
        for event in ledger.list()
        if event.kind
        == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    )

    assert len(pair_results) == 2
    assert tuple(
        result.material["applicability"] for result in applicability_results
    ) == (
        "inapplicable",
        "applicable",
        "inapplicable",
        "inapplicable",
        "inapplicable",
        "applicable",
    )
    assert len(compare_acts) == len(compare_results) == 2
    assert tuple(
        result.material["act_occurrence_event_identity"]
        for result in compare_results
    ) == tuple(act.identity for act in compare_acts)
    assert tuple(
        len(result.material["finding"]["relation_findings"])
        for result in compare_results
    ) == (2, 2)


def test_compare_requires_equal_material_from_separate_source_occurrences():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"ab\nab\n"),
    )

    byte_measurements = tuple(
        event
        for event in ledger.list()
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    )
    pair_measurements = tuple(
        event
        for event in ledger.list()
        if event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
    )
    pair_results = tuple(
        event
        for event in ledger.list()
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
    )

    assert len(byte_measurements) == len(pair_measurements) == 2
    assert len(pair_results) == 1
    assert [
        finding["subject"]["content"]
        for finding in pair_results[0].material["findings"][
            "conflicting_findings"
        ]
    ] == [[97, 98], [98, 10]]


def _current_coordinates(ledger):
    return read_operator_current_coordinates(
        ledger, locality_identity=LOCALITY
    )


def _advance_since(ledger, current_coordinates, prior_count):
    occurrences = ledger.list_locality(LOCALITY)[prior_count:]
    return advance_operator_current_coordinates(
        ledger,
        tuple(occurrence.identity for occurrence in occurrences),
        locality_identity=LOCALITY,
        prior=current_coordinates,
    )


def _pair_measurement(ledger, current_coordinates):
    prior_count = len(ledger.list_locality(LOCALITY))
    binding = _record_byte_measurement_subject_to_act_binding_from_current_coordinates(
        ledger,
        source_localities=(LOCALITY,),
        recording_locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    act = _record_byte_measurement_act_occurrence_from_current_coordinates(
        ledger,
        subject_to_act_binding=binding,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    byte_result = _record_byte_measurement_result_from_current_coordinates(
        ledger,
        act_occurrence=act,
        subject_to_act_binding=binding,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    result, current_coordinates = (
        _record_byte_position_pair_count_layer_from_current_coordinates(
            ledger,
            source_measurement_event_identity=byte_result.identity,
            recording_locality_identity=LOCALITY,
            current_coordinates=current_coordinates,
        )
    )
    return result, current_coordinates


def _record_pair_comparison(ledger, earlier, later, current_coordinates):
    prior_count = len(ledger.list_locality(LOCALITY))
    binding = record_recorded_pair_measurement_comparison_subject_to_act_binding(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    applicability_binding = (
        record_recorded_pair_measurement_comparison_applicability_subject_to_act_binding(
            ledger,
            comparison_binding_event_identity=binding.identity,
            current_coordinates=current_coordinates,
        )
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    applicability_act = (
        record_recorded_pair_measurement_comparison_applicability_act_occurrence(
            ledger,
            applicability_binding_event_identity=applicability_binding.identity,
            current_coordinates=current_coordinates,
        )
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    applicability = record_recorded_pair_measurement_comparison_applicability_result(
        ledger,
        act_occurrence_event_identity=applicability_act.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    act = record_recorded_pair_measurement_comparison_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    result = record_recorded_pair_measurement_comparison_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        current_coordinates=current_coordinates,
    )
    return result, _advance_since(ledger, current_coordinates, prior_count)


def _record_path(ledger, pair_measurement, source, current_coordinates):
    result_positions = result_positions_of_recorded_byte_position_pair_measurement(
        ledger,
        pair_measurement.identity,
        prior_coordinates=current_coordinates,
    )
    recurrence = {
        result_position.content: result_position.result_position
        for result_position in result_positions or ()
        if result_position.result == "recurrence"
        and result_position.content in {(97, 98), (98, 99)}
    }
    findings = measure_positions_for_recurrent_byte_pair_result_positions(
        ledger,
        pair_measurement_occurrence_identity=pair_measurement.identity,
        recurrence_result_positions=(recurrence[(97, 98)], recurrence[(98, 99)]),
        source_material_result_occurrence_identity=source.identity,
        occurrence_count_boundary=16,
        through=ledger.append_boundary(),
        prior_coordinates=current_coordinates,
    )
    results = []
    for finding in findings:
        prior_count = len(ledger.list_locality(LOCALITY))
        act = _record_recurrent_pair_position_measurement_act_from_current_coordinates(
            ledger,
            finding=finding,
            current_coordinates=current_coordinates,
        )
        current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
        prior_count = len(ledger.list_locality(LOCALITY))
        result = record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            act_occurrence_event_identity=act.identity,
            current_coordinates=current_coordinates,
        )
        results.append(result)
        current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    references = tuple(
        reference
        for result in results
        for reference in references_to_recorded_recurrent_byte_pair_occurrence_positions(
            ledger,
            result_occurrence_identity=result.identity,
            prior_coordinates=current_coordinates,
        )
    )
    first = next(reference for reference in references if reference.exact_pair == b"ab")
    second = next(reference for reference in references if reference.exact_pair == b"bc")
    prior_count = len(ledger.list_locality(LOCALITY))
    binding = record_shared_position_subject_to_act_binding(
        ledger,
        first_result_occurrence_identity=first.recorded_occurrence_identity,
        first_result_position=first.result_position,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_result_position=second.result_position,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    applicability_act = record_shared_position_applicability_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=applicability_act.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    act = record_shared_position_measurement_act_occurrence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
    prior_count = len(ledger.list_locality(LOCALITY))
    result = record_shared_position_measurement_result(
        ledger,
        measurement_act_occurrence_event_identity=act.identity,
        current_coordinates=current_coordinates,
    )
    return result, _advance_since(ledger, current_coordinates, prior_count)


def _record_inputs_with_coordinates(
    ledger,
    *,
    shared_position_source_is_added=True,
    current_coordinates=None,
):
    if current_coordinates is None:
        current_coordinates = _current_coordinates(ledger)
    earlier_source, current_coordinates = (
        record_operator_material_occurrence_from_current_coordinates(
            ledger,
            locality_identity=LOCALITY,
            exact=b"abcabc",
            source_boundary="earlier exact occurrence",
            current_coordinates=current_coordinates,
        )
    )
    earlier, current_coordinates = _pair_measurement(ledger, current_coordinates)
    added, current_coordinates = (
        record_operator_material_occurrence_from_current_coordinates(
            ledger,
            locality_identity=LOCALITY,
            exact=b"abc",
            source_boundary="added exact occurrence",
            current_coordinates=current_coordinates,
        )
    )
    later, current_coordinates = _pair_measurement(ledger, current_coordinates)
    comparison, current_coordinates = _record_pair_comparison(
        ledger, earlier, later, current_coordinates
    )
    shared_position_source = added
    if not shared_position_source_is_added:
        shared_position_source, current_coordinates = (
            record_operator_material_occurrence_from_current_coordinates(
                ledger,
                locality_identity=LOCALITY,
                exact=b"abc",
                source_boundary="unrelated exact occurrence",
                current_coordinates=current_coordinates,
            )
        )
    shared_position, current_coordinates = _record_path(
        ledger, earlier, shared_position_source, current_coordinates
    )
    return ledger, earlier_source, added, comparison, shared_position, current_coordinates


def _record_inputs(ledger, *, shared_position_source_is_added=True):
    recorded = _record_inputs_with_coordinates(
        ledger,
        shared_position_source_is_added=shared_position_source_is_added,
    )
    return recorded[:-1]


def _inputs(*, ledger=None, shared_position_source_is_added=True):
    return _record_inputs(
        ledger if ledger is not None else EventLedger(),
        shared_position_source_is_added=shared_position_source_is_added,
    )


def _two_inputs():
    ledger, *first, current_coordinates = _record_inputs_with_coordinates(
        EventLedger()
    )
    ledger, *second, _current_coordinates_read = _record_inputs_with_coordinates(
        ledger,
        current_coordinates=current_coordinates,
    )
    return ledger, *first, *second


def _two_inputs_with_coordinates():
    ledger, *first, current_coordinates = _record_inputs_with_coordinates(
        EventLedger()
    )
    ledger, *second, current_coordinates = _record_inputs_with_coordinates(
        ledger,
        current_coordinates=current_coordinates,
    )
    return ledger, *first, *second, current_coordinates


def _ledger_at_story_floor(floor):
    if floor not in range(5):
        raise ValueError("the exact story floor is absent")
    ledger, *_inputs_reading, current_coordinates = _two_inputs_with_coordinates()
    results = ()
    for story_floor in range(1, floor + 1):
        if story_floor == 1:
            reading = record_shared_position_measurement_pair_finding_compare_applicability_act_occurrences_from_current_coordinates(
                ledger,
                locality_identity=LOCALITY,
                current_coordinates=current_coordinates,
            )
            results = reading.applicability_act_occurrence_occurrences
        elif story_floor == 2:
            reading = record_shared_position_measurement_pair_finding_compare_applicability_from_current_coordinates(
                ledger,
                locality_identity=LOCALITY,
                current_coordinates=current_coordinates,
            )
            results = reading.applicability_result_occurrences
        elif story_floor == 3:
            reading = record_applicable_shared_position_measurement_pair_finding_compare_act_occurrence_from_current_coordinates(
                ledger,
                locality_identity=LOCALITY,
                current_coordinates=current_coordinates,
            )
            results = reading.compare_act_occurrence_occurrences
        else:
            reading = record_shared_position_measurement_pair_finding_compare_results_from_current_coordinates(
                ledger,
                locality_identity=LOCALITY,
                current_coordinates=current_coordinates,
            )
            results = reading.compare_result_occurrences
        current_coordinates = reading.current_coordinates
    return ledger, tuple(results), current_coordinates


def _record_comparison(ledger, comparison, shared_position):
    binding = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        shared_position_measurement_result_event_identity=shared_position.identity,
        comparison_result_event_identity=comparison.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_binding = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_subject_to_act_binding(
        ledger,
        comparison_binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_act = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_act_occurrence(
        ledger,
        applicability_binding_event_identity=applicability_binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_result(
        ledger, act_occurrence_event_identity=applicability_act.identity
    )
    act = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    result = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    return binding, applicability, act, result


def test_shared_position_result_meets_complete_findings_of_the_same_added_occurrence():
    ledger, _earlier_source, added, comparison, shared_position = _inputs()
    binding, applicability, act, result = _record_comparison(
        ledger, comparison, shared_position
    )

    applicable = get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability(
        ledger, applicability.identity
    )
    assert applicable["applicability"] == "applicable"
    assert applicable["dimensions"]["content"]["same_source_occurrence"] is True
    assert all(
        count > 0
        for count in applicable["dimensions"]["content"][
                "pair_finding_counts"
        ]
    )

    reading = get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
        ledger, result.identity
    )
    assert result.kind == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    assert (
        binding.material["source_material_result_occurrence_identity"]
        == added.identity
    )
    assert act.material["subject_to_act_binding_reference"][
        "recorded_occurrence_identity"
    ] == binding.identity
    relation_findings = reading["finding"]["relation_findings"]
    assert [finding["pair_subject"] for finding in relation_findings] == [
        [97, 98],
        [98, 99],
    ]
    assert all(
        finding["comparison_finding_references"]
        for finding in relation_findings
    )
    assert all(
        set(reference)
        == {
            "recorded_comparison_occurrence_identity",
            "finding_category",
            "finding_position",
        }
        for finding in relation_findings
        for reference in finding["comparison_finding_references"]
    )
    assert {
        reference["finding_category"]
        for finding in relation_findings
        for reference in finding["comparison_finding_references"]
    } <= {
        "same_content_findings",
        "conflicting_findings",
        "findings_of_earlier_result",
        "findings_of_later_result",
    }
    recorded_comparison = get_recorded_pair_measurement_comparison(
        ledger, comparison.identity
    )
    first_count_reference = next(
        reference
        for reference in relation_findings[0]["comparison_finding_references"]
        if recorded_comparison["findings"][reference["finding_category"]][
            reference["finding_position"]
        ]["subject"]["result"]
        == "count"
    )
    first_count = recorded_comparison["findings"][
        first_count_reference["finding_category"]
    ][first_count_reference["finding_position"]]
    assert first_count["earlier_content"]["count"] == 2
    assert first_count["later_content"]["count"] == 3
    assert result.exact_material is None


def test_result_local_position_addresses_finding_movement():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        ledger, comparison, shared_position
    )

    moved = move_recorded_shared_position_comparison_finding_result_content_to_locality(
        ledger,
        comparison_result_occurrence_identity=result.identity,
        destination_locality="finding-destination",
    )

    assert {
        "recorded_occurrence_identity": moved["recorded_occurrence_identity"],
        "result_position": moved["result_position"],
    } == {
        "recorded_occurrence_identity": result.identity,
        "result_position": 0,
    }
    with pytest.raises(ValueError, match="exact source coordinates"):
        comparison_module._recorded_shared_position_comparison_finding_result_content_for_locality_movement(
            ledger,
            result_event_identity=result.identity,
            result_position=1,
        )


def test_unassigned_exact_compare_subject_read_records_nothing():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    boundary_before_read = ledger.append_boundary()

    assert unbound_shared_position_measurement_pair_finding_compare_subjects_in_current_coordinates(
        ledger, locality_identity=LOCALITY
    ) == (
        SharedPositionMeasurementPairFindingCompareSubject(
            shared_position_measurement_result_event_identity=shared_position.identity,
            comparison_result_event_identity=comparison.identity,
        ),
    )
    assert ledger.append_boundary() == boundary_before_read

    record_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        shared_position_measurement_result_event_identity=shared_position.identity,
        comparison_result_event_identity=comparison.identity,
        current_coordinates=_current_coordinates(ledger),
    )

    assert (
        unbound_shared_position_measurement_pair_finding_compare_subjects_in_current_coordinates(
            ledger, locality_identity=LOCALITY
        )
        == ()
    )


def test_unassigned_exact_compare_subject_read_after_restart(tmp_path):
    database = str(tmp_path / "shared-position-compare-subject.sqlite")
    source, _earlier_source, _added, comparison, shared_position = _inputs()
    subjects = (
        SharedPositionMeasurementPairFindingCompareSubject(
            shared_position_measurement_result_event_identity=shared_position.identity,
            comparison_result_event_identity=comparison.identity,
        ),
    )
    ledger = SQLiteEventLedger(database)
    ledger.append_many(source.list())
    ledger.close()

    durable = SQLiteEventLedger(database)
    try:
        assert unbound_shared_position_measurement_pair_finding_compare_subjects_in_current_coordinates(
            durable, locality_identity=LOCALITY
        ) == subjects
    finally:
        durable.close()


def test_unassigned_exact_compare_subject_read_returns_every_shared_position_and_comparison_pair():
    (
        ledger,
        _first_source,
        _first_added,
        first_comparison,
        first_path,
        _second_source,
        _second_added,
        second_comparison,
        second_path,
    ) = _two_inputs()
    subjects = tuple(
        SharedPositionMeasurementPairFindingCompareSubject(
            shared_position_measurement_result_event_identity=shared_position.identity,
            comparison_result_event_identity=comparison.identity,
        )
        for shared_position in (first_path, second_path)
        for comparison in (first_comparison, second_comparison)
    )

    assert unbound_shared_position_measurement_pair_finding_compare_subjects_in_current_coordinates(
        ledger, locality_identity=LOCALITY
    ) == subjects

    record_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        shared_position_measurement_result_event_identity=first_path.identity,
        comparison_result_event_identity=second_comparison.identity,
        current_coordinates=_current_coordinates(ledger),
    )

    assert unbound_shared_position_measurement_pair_finding_compare_subjects_in_current_coordinates(
        ledger, locality_identity=LOCALITY
    ) == tuple(
        subject
        for subject in subjects
        if subject
        != SharedPositionMeasurementPairFindingCompareSubject(
            shared_position_measurement_result_event_identity=first_path.identity,
            comparison_result_event_identity=second_comparison.identity,
        )
    )


def test_every_exact_cross_set_member_receives_one_applicability_act():
    (
        ledger,
        _first_source,
        _first_added,
        first_comparison,
        first_path,
        _second_source,
        _second_added,
        second_comparison,
        second_path,
    ) = _two_inputs()
    coordinates_before = _current_coordinates(ledger)
    boundary_before = ledger.append_boundary()
    assert boundary_before.identity != coordinates_before[
        "through_event_occurrence_identity"
    ]
    subjects = tuple(
        SharedPositionMeasurementPairFindingCompareSubject(
            shared_position_measurement_result_event_identity=shared_position_identity,
            comparison_result_event_identity=comparison_identity,
        )
        for shared_position_identity in (first_path.identity, second_path.identity)
        for comparison_identity in (
            first_comparison.identity,
            second_comparison.identity,
        )
    )

    recorded = record_shared_position_measurement_pair_finding_compare_applicability_act_occurrences_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
    )
    acts = recorded.applicability_act_occurrence_occurrences

    assert len(acts) == len(subjects) == 4
    assert tuple(
        SharedPositionMeasurementPairFindingCompareSubject(
            shared_position_measurement_result_event_identity=act.material[
                "subject_reference"
            ]["shared_position_input"]["subject"]["recorded_occurrence_identity"],
            comparison_result_event_identity=act.material["subject_reference"][
                "comparison_input"
            ]["subject"]["recorded_occurrence_identity"],
        )
        for act in acts
    ) == subjects
    assert tuple(
        act.material["through_event_occurrence_identity"] for act in acts
    ) == (
        coordinates_before["through_event_occurrence_identity"],
        acts[0].identity,
        acts[1].identity,
        acts[2].identity,
    )
    assert recorded.current_coordinates["through_event_occurrence_identity"] == (
        acts[-1].identity
    )
    assert tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
        )
    ) == ()
    assert tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
        )
    ) == ()
    assert tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
        )
    ) == ()
    assert tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
        )
    ) == ()
    assert recorded.current_coordinates["applicability_result_occurrences"] == (
        coordinates_before["applicability_result_occurrences"]
    )
    assert all("subject_to_act_binding_reference" not in act.material for act in acts)


def test_no_applicability_occurrence_is_not_inapplicable():
    ledger_before_binding, _results, _current_coordinates_read = (
        _ledger_at_story_floor(0)
    )

    assert len(
        unbound_shared_position_measurement_pair_finding_compare_subjects_in_current_coordinates(
            ledger_before_binding, locality_identity=LOCALITY
        )
    ) == 4
    assert tuple(
        ledger_before_binding.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
        )
    ) == ()
    assert tuple(
        ledger_before_binding.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
        )
    ) == ()

    ledger_after_applicability, results, _current_coordinates_read = (
        _ledger_at_story_floor(2)
    )

    assert tuple(
        ledger_after_applicability.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
        )
    ) == ()
    assert tuple(
        ledger_after_applicability.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
        )
    ) == ()
    assert tuple(result.material["applicability"] for result in results) == (
        "applicable",
        "inapplicable",
        "inapplicable",
        "applicable",
    )


def test_every_current_applicability_act_records_one_result():
    ledger, acts, _current_coordinates_read = _ledger_at_story_floor(1)
    recorded = (
        record_shared_position_measurement_pair_finding_compare_applicability_from_current_coordinates(
            ledger, locality_identity=LOCALITY
        )
    )
    results = recorded.applicability_result_occurrences

    assert len(results) == len(acts) == 4
    assert tuple(result.material["applicability"] for result in results) == (
        "applicable",
        "inapplicable",
        "inapplicable",
        "applicable",
    )
    assert tuple(
        result.material["act_occurrence_event_identity"] for result in results
    ) == tuple(act.identity for act in acts)
    assert tuple(result.material["subject_reference"] for result in results) == tuple(
        act.material["subject_reference"] for act in acts
    )
    assert all(
        "subject_to_act_binding_reference" not in result.material
        for result in results
    )
    assert all(
        result.identity
        in recorded.current_coordinates["applicability_result_occurrences"]
        for result in results
    )
    assert all(
        "yield_relation_identity" not in result.material for result in results
    )
    assert not tuple(
        event
        for event in ledger.iter_locality_kind(
            LOCALITY, RECORDED_YIELD_RELATION_EVENT
        )
        if event.material.get("occurrence_boundary")
        == "comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability"
    )
    with pytest.raises(ValueError, match="already has a result"):
        record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_result(
            ledger,
            act_occurrence_event_identity=results[0].material[
                "act_occurrence_event_identity"
            ],
        )


def test_holding_one_input_exact_does_not_determine_applicability():
    ledger, acts, _current_coordinates_read = _ledger_at_story_floor(1)
    results = (
        record_shared_position_measurement_pair_finding_compare_applicability_from_current_coordinates(
            ledger,
            locality_identity=LOCALITY,
        ).applicability_result_occurrences
    )
    subjects = tuple(act.material["subject_reference"] for act in acts)

    assert subjects[0]["shared_position_input"]["subject"] == subjects[1][
        "shared_position_input"
    ]["subject"]
    assert subjects[0]["comparison_input"]["subject"] != subjects[1][
        "comparison_input"
    ]["subject"]
    assert tuple(result.material["applicability"] for result in results[:2]) == (
        "applicable",
        "inapplicable",
    )

    assert subjects[0]["comparison_input"]["subject"] == subjects[2][
        "comparison_input"
    ]["subject"]
    assert subjects[0]["shared_position_input"]["subject"] != subjects[2][
        "shared_position_input"
    ]["subject"]
    assert (results[0].material["applicability"], results[2].material["applicability"]) == (
        "applicable",
        "inapplicable",
    )


def test_applicability_binding_refuses_a_substituted_compare_binding_reference():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    current_coordinates = _current_coordinates(ledger)
    compare_binding = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        shared_position_measurement_result_event_identity=shared_position.identity,
        comparison_result_event_identity=comparison.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(
        ledger,
        current_coordinates,
        len(ledger.list_locality(LOCALITY)) - 1,
    )
    applicability_binding = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_subject_to_act_binding(
        ledger,
        comparison_binding_event_identity=compare_binding.identity,
        current_coordinates=current_coordinates,
    )
    applicability_binding.material[
        "compare_subject_to_act_binding_reference"
    ]["recorded_occurrence_identity"] = "substituted-binding"

    with pytest.raises(ValueError):
        comparison_module._read_applicability_binding(
            ledger,
            applicability_binding.identity,
            prior_coordinates=current_coordinates,
        )


def test_only_applicable_current_compare_results_record_act_occurrence():
    ledger, applicability_results, current_coordinates = _ledger_at_story_floor(2)
    before = read_shared_position_measurement_pair_finding_compare_applicability_results_and_acts(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )
    assert before.applicable_result_occurrence_identities == (
        applicability_results[0].identity,
        applicability_results[3].identity,
    )
    assert before.inapplicable_result_occurrence_identities == (
        applicability_results[1].identity,
        applicability_results[2].identity,
    )
    assert before.act_occurrences_by_applicability_result == ()
    assert before.applicable_result_occurrence_identities_without_act_occurrence == (
        before.applicable_result_occurrence_identities
    )

    recorded = record_applicable_shared_position_measurement_pair_finding_compare_act_occurrence_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )
    acts = recorded.compare_act_occurrence_occurrences

    assert len(acts) == 2
    assert tuple(
        act.material["applicability_result_event_identity"] for act in acts
    ) == (applicability_results[0].identity, applicability_results[3].identity)
    assert all(
        set(act.material["subject_reference"])
        == {"shared_position_measurement_result_reference", "comparison_result_reference"}
        for act in acts
    )
    assert all("subject_to_act_binding_reference" not in act.material for act in acts)
    assert all(
        "addressed_act_occurrence_identity" not in result.material
        for result in applicability_results
    )
    assert all(
        "addressed_act_occurrence_identity" not in applicability_act.material
        and "compare_result_identity" not in applicability_act.material
        and "applicability_act_identity" not in applicability_act.material
        and "applicability_act_occurrence_identity"
        not in applicability_act.material
        and "result_identity" not in applicability_act.material
        and "addressed_act_identity" not in applicability_act.material
        and applicability_act.material["addressed_act"]
        == comparison_module.COMPARE_ACT
        and all(
            subject["addressed_act"] == comparison_module.COMPARE_ACT
            and "addressed_act_identity" not in subject
            for subject in applicability_act.material["subject_reference"].values()
        )
        for applicability_act in (
            ledger.get(result.material["act_occurrence_event_identity"])
            for result in applicability_results
        )
    )
    assert all(
        "result_identity" not in result.material
        and "applicability_act_identity" not in result.material
        and "applicability_act_occurrence_identity" not in result.material
        and "addressed_act_identity" not in result.material
        and result.material["addressed_act"] == comparison_module.COMPARE_ACT
        and set(result.material["dimensions"]) == {"content"}
        for result in applicability_results
    )
    assert all(
        "act_occurrence_identity" not in act.material
        and "result_identity" not in act.material
        and "compare_act_identity" not in act.material
        for act in acts
    )
    assert recorded.current_coordinates["through_event_occurrence_identity"] == (
        acts[-1].identity
    )
    historical = read_shared_position_measurement_pair_finding_compare_applicability_results_and_acts(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )
    assert historical == before

    after = read_shared_position_measurement_pair_finding_compare_applicability_results_and_acts(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=recorded.current_coordinates,
    )
    assert after.applicable_result_occurrence_identities == (
        before.applicable_result_occurrence_identities
    )
    assert after.inapplicable_result_occurrence_identities == (
        before.inapplicable_result_occurrence_identities
    )
    assert after.act_occurrences_by_applicability_result == (
        (applicability_results[0].identity, acts[0].identity),
        (applicability_results[3].identity, acts[1].identity),
    )
    assert (
        after.applicable_result_occurrence_identities_without_act_occurrence == ()
    )

    repeated = record_applicable_shared_position_measurement_pair_finding_compare_act_occurrence_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=recorded.current_coordinates,
    )
    assert repeated.compare_act_occurrence_occurrences == ()
    assert repeated.current_coordinates == recorded.current_coordinates


def test_every_current_compare_act_records_one_result():
    ledger, acts, _current_coordinates_read = _ledger_at_story_floor(3)

    recorded = record_shared_position_measurement_pair_finding_compare_results_from_current_coordinates(
        ledger, locality_identity=LOCALITY
    )
    results = recorded.compare_result_occurrences

    assert len(results) == len(acts) == 2
    assert tuple(
            result.material["act_occurrence_event_identity"] for result in results
    ) == tuple(act.identity for act in acts)
    assert all(
        "yield_relation_identity" not in result.material
        for result in results
    )
    assert all(
        result.identity
        in recorded.current_coordinates["comparison_result_occurrences"]
        for result in results
    )
    assert tuple(
        result.material["subject_reference"] for result in results
    ) == tuple(act.material["subject_reference"] for act in acts)
    assert all(
        "subject_to_act_binding_reference" not in result.material
        for result in results
    )
    assert all(
        "act_occurrence_identity" not in result.material
        and "result_identity" not in result.material
        and "compare_act_identity" not in result.material
        for result in results
    )
    for result in results:
        shared_position_reference = result.material["finding"]["subject"][
            "shared_position_result_position_reference"
        ]
        shared_position_result = ledger.get(shared_position_reference["recorded_occurrence_identity"])
        shared_position_subject = shared_position_result.material["result_positions"][0]["subject"]
        assert tuple(
            finding["pair_position_result_reference"]
            for finding in result.material["finding"]["relation_findings"]
        ) == (
            shared_position_subject["first_position_result_reference"],
            shared_position_subject["second_position_result_reference"],
        )
    assert recorded.current_coordinates["through_event_occurrence_identity"] == (
        results[-1].identity
    )

def test_current_coordinates_fans_one_comparison_into_exact_distinction_pins():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        ledger, comparison, shared_position
    )
    boundary = ledger.append_boundary()
    through_occurrence = _current_coordinates(ledger)[
        "through_event_occurrence_identity"
    ]

    pins = recorded_distinction_pins_from_current_coordinates(
        ledger, locality_identity=LOCALITY
    )

    assert ledger.append_boundary() == boundary
    assert all(
        pin.comparison_result_occurrence_identity == result.identity for pin in pins
    )
    assert all(pin.through_event_occurrence_identity == through_occurrence for pin in pins)
    shared_position_subject = shared_position.material["result_positions"][0]["subject"]
    assert tuple(pin.pair_position_result_reference for pin in pins) == (
        shared_position_subject["first_position_result_reference"],
        shared_position_subject["first_position_result_reference"],
        shared_position_subject["second_position_result_reference"],
        shared_position_subject["second_position_result_reference"],
    )
    assert tuple(pin.pair_subject for pin in pins) == (
        b"ab",
        b"ab",
        b"bc",
        b"bc",
    )
    assert tuple(
        pin.recorded_finding_reference["finding_category"] for pin in pins
    ) == (
        "same_content_findings",
        "conflicting_findings",
        "same_content_findings",
        "conflicting_findings",
    )
    pins[0].recorded_finding_reference["finding_category"] = "changed copy"
    assert recorded_distinction_pins_from_current_coordinates(
        ledger, locality_identity=LOCALITY
    )[0].recorded_finding_reference["finding_category"] == "same_content_findings"


def test_every_current_compare_result_reads_every_exact_finding_reference_branch():
    ledger, results, current_coordinates = _ledger_at_story_floor(4)
    boundary = ledger.append_boundary()

    pins = recorded_distinction_pins_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
        current_coordinates=current_coordinates,
    )

    assert len(results) == 2
    assert tuple(pin.comparison_result_occurrence_identity for pin in pins) == tuple(
        result.identity for result in results for _ in range(4)
    )
    assert all(
        set(pin.pair_position_result_reference)
        == {"recorded_occurrence_identity", "result_position"}
        for pin in pins
    )
    assert tuple(pin.pair_subject for pin in pins) == (
        b"ab",
        b"ab",
        b"bc",
        b"bc",
    ) * len(results)
    assert tuple(
        pin.recorded_finding_reference["finding_category"] for pin in pins
    ) == (
        "same_content_findings",
        "conflicting_findings",
        "same_content_findings",
        "conflicting_findings",
    ) * len(results)
    assert len(
        {
            (
                pin.comparison_result_occurrence_identity,
                pin.pair_position_result_reference[
                    "recorded_occurrence_identity"
                ],
                    pin.pair_position_result_reference["result_position"],
                pin.recorded_finding_reference["finding_category"],
                pin.recorded_finding_reference["finding_position"],
            )
            for pin in pins
        }
    ) == len(pins)
    assert all(pin.through_event_occurrence_identity == results[-1].identity for pin in pins)
    assert ledger.append_boundary() == boundary


def test_pair_findings_and_shared_position_do_not_authorize_distinction_fanout_by_presence():
    ledger, _earlier_source, _added, _comparison, _path = _inputs()
    boundary = ledger.append_boundary()

    assert recorded_distinction_pins_from_current_coordinates(
        ledger, locality_identity=LOCALITY
    ) == ()
    assert ledger.append_boundary() == boundary


def test_distinction_fanout_keeps_one_locality_pin_after_another_locality_append():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        ledger, comparison, shared_position
    )
    ledger.append("test.occurrence", {"unknown": []}, locality_identity="other")
    boundary = ledger.append_boundary()

    pins = recorded_distinction_pins_from_current_coordinates(
        ledger, locality_identity=LOCALITY
    )

    assert pins
    assert all(pin.comparison_result_occurrence_identity == result.identity for pin in pins)
    assert ledger.append_boundary() == boundary


def test_another_source_occurrence_is_inapplicable_and_cannot_participate():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs(
        shared_position_source_is_added=False
    )
    binding = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        shared_position_measurement_result_event_identity=shared_position.identity,
        comparison_result_event_identity=comparison.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_binding = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_subject_to_act_binding(
        ledger,
        comparison_binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_act = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_act_occurrence(
        ledger,
        applicability_binding_event_identity=applicability_binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_result(
        ledger, act_occurrence_event_identity=applicability_act.identity
    )
    reading = get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability(
        ledger, applicability.identity
    )
    assert reading["applicability"] == "inapplicable"
    assert reading["dimensions"]["content"]["same_source_occurrence"] is False
    with pytest.raises(ValueError, match="not applicable"):
        record_comparison_of_shared_position_measurement_with_recorded_pair_findings_act_occurrence(
            ledger,
            subject_to_act_binding_event_identity=binding.identity,
            applicability_result_event_identity=applicability.identity,
            current_coordinates=_current_coordinates(ledger),
        )


def test_availability_without_both_exact_current_coordinates_cannot_assign_comparison():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    current_coordinates = _current_coordinates(ledger)
    current_coordinates["comparison_result_occurrences"].pop(comparison.identity)
    with pytest.raises(
        ValueError, match="each exact result in current coordinates"
    ):
        record_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding(
            ledger,
            shared_position_measurement_result_event_identity=shared_position.identity,
            comparison_result_event_identity=comparison.identity,
            current_coordinates=current_coordinates,
        )


def test_one_shared_position_measurement_pair_finding_compare_act_cannot_record_two_results():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    _binding, _applicability, act, _result = _record_comparison(
        ledger, comparison, shared_position
    )
    with pytest.raises(ValueError, match="cannot record two results"):
        record_comparison_of_shared_position_measurement_with_recorded_pair_findings_result(
            ledger, act_occurrence_event_identity=act.identity
        )


def test_changed_input_compare_is_refused_on_later_read():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        ledger, comparison, shared_position
    )
    count_finding = next(
        finding
        for findings in comparison.material["findings"].values()
        for finding in findings
        if type(finding.get("later_content")) is dict
        and "count" in finding["later_content"]
    )
    count_finding["later_content"]["count"] += 1
    with pytest.raises(ValueError):
        get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
            ledger, result.identity
        )


def test_higher_input_reads_the_exact_authored_comparison_binding(monkeypatch):
    ledger, _earlier_source, _added, comparison, _path = _inputs()
    binding_reads = []
    original = recorded_pair_comparison_module._binding_reading

    def witnessed(ledger, event_identity, **coordinates):
        binding_reads.append(event_identity)
        return original(ledger, event_identity, **coordinates)

    monkeypatch.setattr(
        recorded_pair_comparison_module, "_binding_reading", witnessed
    )
    reading = comparison_module._comparison_input(ledger, comparison.identity)

    binding_identity = comparison.material[
        "subject_to_act_binding_reference"
    ]["recorded_occurrence_identity"]
    assert binding_reads == [binding_identity]


def test_higher_input_handoff_refuses_changed_comparison_binding():
    ledger, _earlier_source, _added, comparison, _path = _inputs()
    binding = ledger.get(
        comparison.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
    )
    binding.material["comparison_result_identity"] = "changed-result"

    with pytest.raises(ValueError):
        comparison_module._comparison_input(ledger, comparison.identity)


def test_changed_higher_compare_result_is_refused_without_yield():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        ledger, comparison, shared_position
    )
    assert "yield_relation_identity" not in result.material
    result.material["result_identity"] = "crossed-result"

    with pytest.raises(ValueError, match="not exact"):
        get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
            ledger, result.identity
        )


def test_each_higher_lifecycle_read_validates_large_inputs_once_without_retained_read(
    monkeypatch,
):
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    binding = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        shared_position_measurement_result_event_identity=shared_position.identity,
        comparison_result_event_identity=comparison.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_binding = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_subject_to_act_binding(
        ledger,
        comparison_binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_act = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_act_occurrence(
        ledger,
        applicability_binding_event_identity=applicability_binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_result(
        ledger, act_occurrence_event_identity=applicability_act.identity
    )
    current_coordinates = _current_coordinates(ledger)
    original = comparison_module._inputs
    calls = []

    def counted(ledger, **identities):
        calls.append(
            (
                identities["shared_position_measurement_result_event_identity"],
                identities["comparison_result_event_identity"],
            )
        )
        return original(ledger, **identities)

    monkeypatch.setattr(comparison_module, "_inputs", counted)
    call_coordinates = (shared_position.identity, comparison.identity)

    act = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=current_coordinates,
    )
    assert calls == [call_coordinates]

    result = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    assert calls == [call_coordinates, call_coordinates]

    get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
        ledger, result.identity
    )
    assert calls == [call_coordinates, call_coordinates, call_coordinates]

    get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
        ledger, result.identity
    )
    assert calls == [call_coordinates] * 4


def test_shared_position_and_recorded_findings_are_read_from_sqlite(tmp_path):
    database = tmp_path / "shared-position-measurement-pair-finding-comparison.sqlite"
    source, _earlier_source, _added, comparison, shared_position = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        source, comparison, shared_position
    )
    result_identity = result.identity
    ledger = SQLiteEventLedger(str(database))
    ledger.append_many(source.list())
    ledger.close()

    durable = SQLiteEventLedger(str(database))
    reading = get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
        durable, result_identity
    )
    assert reading["finding"]["relation_findings"]
    assert result_identity in _current_coordinates(durable)["comparison_result_occurrences"]
    assert recorded_distinction_pins_from_current_coordinates(
        durable, locality_identity=LOCALITY
    )
    result_act_reading = (
        read_shared_position_measurement_pair_finding_compare_applicability_results_and_acts(
            durable,
            locality_identity=LOCALITY,
        )
    )
    assert len(result_act_reading.applicable_result_occurrence_identities) == 1
    assert len(
        result_act_reading.act_occurrences_by_applicability_result
    ) == 1
    assert (
        result_act_reading.applicable_result_occurrence_identities_without_act_occurrence
        == ()
    )
    durable.close()


def test_advanced_current_coordinates_equal_replay_for_comparison_of_shared_position_measurement_with_recorded_pair_findings():
    ledger, _earlier_source, _added, comparison, shared_position = _inputs()
    prior = _current_coordinates(ledger)
    prior_count = len(ledger.list_locality(LOCALITY))
    _record_comparison(ledger, comparison, shared_position)
    later = tuple(
        event.identity for event in ledger.list_locality(LOCALITY)[prior_count:]
    )
    advanced = advance_operator_current_coordinates(
        ledger, later, locality_identity=LOCALITY, prior=prior
    )
    assert advanced == _current_coordinates(ledger)




WITNESSED_BOOK_COORDINATES = {
    ("book_coordinates", "01.Current.E.1", "Applicability", "result"): (
        test_another_source_occurrence_is_inapplicable_and_cannot_participate,
    ),
    ("book_coordinates", "01.Source.D", "result"): (
        test_shared_position_and_recorded_findings_are_read_from_sqlite,
        test_advanced_current_coordinates_equal_replay_for_comparison_of_shared_position_measurement_with_recorded_pair_findings,
    ),
}
