"""Compare requires exact ordered path findings."""

from __future__ import annotations

from copy import deepcopy

import pytest

import seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings as comparison_module
import seed_runtime.comparison_of_recorded_byte_pair_measurements as recorded_pair_comparison_module
from seed_runtime.byte_measurement import (
    _record_byte_measurement_act_occurrence_from_current_coordinates,
    _record_byte_measurement_result_from_current_coordinates,
    _record_byte_measurement_subject_to_act_binding_from_current_coordinates,
    assertions_of_recorded_byte_position_pair_measurement,
    _record_byte_position_pair_count_layer_from_current_coordinates,
)
from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    OrderedPathPairFindingCompareSubject,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability,
    move_recorded_path_comparison_finding_assertion_to_locality,
    recorded_distinction_pins_from_current_coordinates,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_subject_to_act_binding,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result,
    record_ordered_path_pair_finding_compare_bindings_from_current_coordinates,
    record_ordered_path_pair_finding_compare_applicability_from_current_coordinates,
    record_applicable_ordered_path_pair_finding_compare_act_occurrence_from_current_coordinates,
    record_ordered_path_pair_finding_compare_results_from_current_coordinates,
    unbound_ordered_path_pair_finding_compare_subjects_in_current_coordinates,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
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
    _record_recurrent_pair_position_measurement_binding_from_current_coordinates,
    measure_positions_for_recurrent_byte_pair_assertions,
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
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
    record_operator_material_occurrence_from_current_coordinates,
)


LOCALITY = "ordered-relation-path-pair-finding-comparison"


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
    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger,
        pair_measurement.identity,
        prior_coordinates=current_coordinates,
    )
    recurrence = {
        assertion.content: assertion.assertion_position
        for assertion in assertions or ()
        if assertion.result == "recurrence"
        and assertion.content in {(97, 98), (98, 99)}
    }
    findings = measure_positions_for_recurrent_byte_pair_assertions(
        ledger,
        pair_measurement_occurrence_identity=pair_measurement.identity,
        recurrence_assertion_positions=(recurrence[(97, 98)], recurrence[(98, 99)]),
        source_material_result_occurrence_identity=source.identity,
        occurrence_count_boundary=16,
        through=ledger.append_boundary(),
        prior_coordinates=current_coordinates,
    )
    results = []
    for finding in findings:
        prior_count = len(ledger.list_locality(LOCALITY))
        binding = _record_recurrent_pair_position_measurement_binding_from_current_coordinates(
            ledger,
            finding=finding,
            current_coordinates=current_coordinates,
        )
        current_coordinates = _advance_since(ledger, current_coordinates, prior_count)
        prior_count = len(ledger.list_locality(LOCALITY))
        act = _record_recurrent_pair_position_measurement_act_from_current_coordinates(
            ledger,
            binding=binding,
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
        first_assertion_address=first.assertion_address,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_assertion_address=second.assertion_address,
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
    path_source_is_added=True,
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
    path_source = added
    if not path_source_is_added:
        path_source, current_coordinates = (
            record_operator_material_occurrence_from_current_coordinates(
                ledger,
                locality_identity=LOCALITY,
                exact=b"abc",
                source_boundary="unrelated exact occurrence",
                current_coordinates=current_coordinates,
            )
        )
    path, current_coordinates = _record_path(
        ledger, earlier, path_source, current_coordinates
    )
    return ledger, earlier_source, added, comparison, path, current_coordinates


def _record_inputs(ledger, *, path_source_is_added=True):
    recorded = _record_inputs_with_coordinates(
        ledger,
        path_source_is_added=path_source_is_added,
    )
    return recorded[:-1]


def _inputs(*, ledger=None, path_source_is_added=True):
    return _record_inputs(
        ledger if ledger is not None else EventLedger(),
        path_source_is_added=path_source_is_added,
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
            reading = record_ordered_path_pair_finding_compare_bindings_from_current_coordinates(
                ledger,
                locality_identity=LOCALITY,
                current_coordinates=current_coordinates,
            )
            results = reading.binding_occurrences
        elif story_floor == 2:
            reading = record_ordered_path_pair_finding_compare_applicability_from_current_coordinates(
                ledger,
                locality_identity=LOCALITY,
                current_coordinates=current_coordinates,
            )
            results = reading.applicability_result_occurrences
        elif story_floor == 3:
            reading = record_applicable_ordered_path_pair_finding_compare_act_occurrence_from_current_coordinates(
                ledger,
                locality_identity=LOCALITY,
                current_coordinates=current_coordinates,
            )
            results = reading.compare_act_occurrence_occurrences
        else:
            reading = record_ordered_path_pair_finding_compare_results_from_current_coordinates(
                ledger,
                locality_identity=LOCALITY,
                current_coordinates=current_coordinates,
            )
            results = reading.compare_result_occurrences
        current_coordinates = reading.current_coordinates
    return ledger, tuple(results), current_coordinates


def _record_comparison(ledger, comparison, path):
    binding = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=comparison.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_binding = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_subject_to_act_binding(
        ledger,
        comparison_binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence(
        ledger,
        applicability_binding_event_identity=applicability_binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
        ledger, act_occurrence_event_identity=applicability_act.identity
    )
    act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    result = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    return binding, applicability, act, result


def test_yielded_path_meets_complete_findings_of_the_same_added_occurrence():
    ledger, _earlier_source, added, comparison, path = _inputs()
    binding, applicability, act, result = _record_comparison(
        ledger, comparison, path
    )

    applicable = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability(
        ledger, applicability.identity
    )
    assert applicable["applicability"] == "applicable"
    assert applicable["dimensions"]["content"]["same_source_occurrence"] is True
    assert all(
        count > 0
        for count in applicable["dimensions"]["content"][
            "path_relation_finding_counts"
        ]
    )

    reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        ledger, result.identity
    )
    assert result.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    assert binding.material["path_source_occurrence_identity"] == added.identity
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
            "subject",
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
        if reference["subject"]["result"] == "count"
    )
    first_count = recorded_comparison["findings"][
        first_count_reference["finding_category"]
    ][first_count_reference["finding_position"]]
    assert first_count["earlier_content"]["count"] == 2
    assert first_count["later_content"]["count"] == 3
    assert result.exact_material is None


def test_result_local_position_addresses_finding_movement():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
    )

    moved = move_recorded_path_comparison_finding_assertion_to_locality(
        ledger,
        comparison_result_occurrence_identity=result.identity,
        destination_locality="finding-destination",
    )

    assert moved.source_assertion_reference == {
        "recorded_occurrence_identity": result.identity,
        "assertion_position": 0,
    }
    with pytest.raises(ValueError, match="exact source coordinates"):
        comparison_module._recorded_path_comparison_finding_assertion_coordinates_for_locality_movement(
            ledger,
            result_event_identity=result.identity,
            assertion_position=1,
        )


def test_unassigned_exact_compare_subject_read_records_nothing():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    boundary_before_read = ledger.append_boundary()

    assert unbound_ordered_path_pair_finding_compare_subjects_in_current_coordinates(
        ledger, locality_identity=LOCALITY
    ) == (
        OrderedPathPairFindingCompareSubject(
            path_result_event_identity=path.identity,
            comparison_result_event_identity=comparison.identity,
        ),
    )
    assert ledger.append_boundary() == boundary_before_read

    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=comparison.identity,
        current_coordinates=_current_coordinates(ledger),
    )

    assert (
        unbound_ordered_path_pair_finding_compare_subjects_in_current_coordinates(
            ledger, locality_identity=LOCALITY
        )
        == ()
    )


def test_unassigned_exact_compare_subject_read_after_restart(tmp_path):
    database = str(tmp_path / "ordered-path-compare-subject.sqlite")
    source, _earlier_source, _added, comparison, path = _inputs()
    subjects = (
        OrderedPathPairFindingCompareSubject(
            path_result_event_identity=path.identity,
            comparison_result_event_identity=comparison.identity,
        ),
    )
    ledger = SQLiteEventLedger(database)
    ledger.append_many(source.list())
    ledger.close()

    durable = SQLiteEventLedger(database)
    try:
        assert unbound_ordered_path_pair_finding_compare_subjects_in_current_coordinates(
            durable, locality_identity=LOCALITY
        ) == subjects
    finally:
        durable.close()


def test_unassigned_exact_compare_subject_read_returns_every_path_and_comparison_pair():
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
        OrderedPathPairFindingCompareSubject(
            path_result_event_identity=path.identity,
            comparison_result_event_identity=comparison.identity,
        )
        for path in (first_path, second_path)
        for comparison in (first_comparison, second_comparison)
    )

    assert unbound_ordered_path_pair_finding_compare_subjects_in_current_coordinates(
        ledger, locality_identity=LOCALITY
    ) == subjects

    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        path_result_event_identity=first_path.identity,
        comparison_result_event_identity=second_comparison.identity,
        current_coordinates=_current_coordinates(ledger),
    )

    assert unbound_ordered_path_pair_finding_compare_subjects_in_current_coordinates(
        ledger, locality_identity=LOCALITY
    ) == tuple(
        subject
        for subject in subjects
        if subject
        != OrderedPathPairFindingCompareSubject(
            path_result_event_identity=first_path.identity,
            comparison_result_event_identity=second_comparison.identity,
        )
    )


def test_every_current_compare_subject_records_one_serial_binding():
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
        OrderedPathPairFindingCompareSubject(
            path_result_event_identity=path_identity,
            comparison_result_event_identity=comparison_identity,
        )
        for path_identity in (first_path.identity, second_path.identity)
        for comparison_identity in (
            first_comparison.identity,
            second_comparison.identity,
        )
    )

    recorded = (
        record_ordered_path_pair_finding_compare_bindings_from_current_coordinates(
            ledger, locality_identity=LOCALITY
        )
    )
    bindings = recorded.binding_occurrences

    assert len(bindings) == len(subjects) == 4
    assert tuple(
        OrderedPathPairFindingCompareSubject(
            path_result_event_identity=binding.material[
                "path_result_reference"
            ]["recorded_occurrence_identity"],
            comparison_result_event_identity=binding.material[
                "comparison_result_reference"
            ]["recorded_occurrence_identity"],
        )
        for binding in bindings
    ) == subjects
    assert tuple(
        binding.material["through_event_occurrence_identity"]
        for binding in bindings
    ) == (
        coordinates_before["through_event_occurrence_identity"],
        bindings[0].identity,
        bindings[1].identity,
        bindings[2].identity,
    )
    assert recorded.current_coordinates["through_event_occurrence_identity"] == (
        bindings[-1].identity
    )
    assert all(
        binding.identity
        in recorded.current_coordinates["subject_to_act_binding_occurrences"]
        for binding in bindings
    )
    assert recorded.current_coordinates["applicability_result_occurrences"] == (
        coordinates_before["applicability_result_occurrences"]
    )
    assert (
        unbound_ordered_path_pair_finding_compare_subjects_in_current_coordinates(
            ledger, locality_identity=LOCALITY
        )
        == ()
    )

def test_every_current_compare_binding_records_one_separate_applicability_result():
    ledger, bindings, _current_coordinates_read = _ledger_at_story_floor(1)
    recorded = (
        record_ordered_path_pair_finding_compare_applicability_from_current_coordinates(
            ledger, locality_identity=LOCALITY
        )
    )
    results = recorded.applicability_result_occurrences

    assert len(results) == len(bindings) == 4
    assert tuple(result.material["applicability"] for result in results) == (
        "applicable",
        "inapplicable",
        "inapplicable",
        "applicable",
    )
    applicability_bindings = tuple(
        ledger.get(
            result.material["subject_to_act_binding_reference"][
                "recorded_occurrence_identity"
            ]
        )
        for result in results
    )
    assert tuple(
        binding.material["addressed_act_identity"]
        for binding in applicability_bindings
    ) == tuple(binding.material["exact_act_identity"] for binding in bindings)
    assert tuple(
        binding.material["compare_subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
        for binding in applicability_bindings
    ) == tuple(binding.identity for binding in bindings)
    assert all(
        result.identity
        in recorded.current_coordinates["applicability_result_occurrences"]
        for result in results
    )


def test_applicability_binding_refuses_a_substituted_compare_binding_reference():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    current_coordinates = _current_coordinates(ledger)
    compare_binding = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=comparison.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_since(
        ledger,
        current_coordinates,
        len(ledger.list_locality(LOCALITY)) - 1,
    )
    applicability_binding = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_subject_to_act_binding(
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
    ledger, applicability_results, _current_coordinates_read = _ledger_at_story_floor(2)
    bindings = tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            comparison_module.COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
        )
    )
    recorded = record_applicable_ordered_path_pair_finding_compare_act_occurrence_from_current_coordinates(
        ledger, locality_identity=LOCALITY
    )
    acts = recorded.compare_act_occurrence_occurrences

    assert len(acts) == 2
    assert tuple(
        act.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
        for act in acts
    ) == (bindings[0].identity, bindings[3].identity)
    assert tuple(
        act.material["applicability_result_event_identity"] for act in acts
    ) == (applicability_results[0].identity, applicability_results[3].identity)
    assert all(
        set(binding.material["subject_reference"])
        == {"path_result_reference", "comparison_result_reference"}
        for binding in (bindings[0], bindings[3])
    )
    assert tuple(
        result.material["addressed_act_occurrence_identity"]
        for result in applicability_results
        if result.material["applicability"] == "inapplicable"
    ) == (None, None)
    assert recorded.current_coordinates["through_event_occurrence_identity"] == (
        acts[-1].identity
    )
def test_every_current_compare_act_records_one_separate_yield_and_result():
    ledger, acts, _current_coordinates_read = _ledger_at_story_floor(3)

    recorded = record_ordered_path_pair_finding_compare_results_from_current_coordinates(
        ledger, locality_identity=LOCALITY
    )
    results = recorded.compare_result_occurrences

    assert len(results) == len(acts) == 2
    assert tuple(
            result.material["act_occurrence_event_identity"] for result in results
    ) == tuple(act.identity for act in acts)
    assert len(
        {
            result.material["yield_relation_identity"]
            for result in results
        }
    ) == len(results)
    assert all(
        ledger.get(result.material["yield_relation_identity"])
        is not None
        for result in results
    )
    assert all(
        result.identity
        in recorded.current_coordinates["comparison_result_occurrences"]
        for result in results
    )
    assert tuple(
        result.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
        for result in results
    ) == tuple(
        act.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
        for act in acts
    )
    for result in results:
        path_reference = result.material["finding"]["subject"][
            "ordered_relation_path_assertion_reference"
        ]
        path_result = ledger.get(path_reference["recorded_occurrence_identity"])
        path_subject = path_result.material["assertions"][0]["assertion_subject"]
        assert tuple(
            finding["path_position_assertion_reference"]
            for finding in result.material["finding"]["relation_findings"]
        ) == (
            path_subject["first_position_assertion_reference"],
            path_subject["second_position_assertion_reference"],
        )
    assert recorded.current_coordinates["through_event_occurrence_identity"] == (
        results[-1].identity
    )

def test_current_coordinates_fans_one_comparison_into_exact_distinction_pins():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
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
    path_subject = path.material["assertions"][0]["assertion_subject"]
    assert tuple(pin.path_position_assertion_reference for pin in pins) == (
        path_subject["first_position_assertion_reference"],
        path_subject["first_position_assertion_reference"],
        path_subject["second_position_assertion_reference"],
        path_subject["second_position_assertion_reference"],
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


def test_every_current_compare_result_exposes_every_exact_finding_reference_branch():
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
        set(pin.path_position_assertion_reference)
        == {"recorded_occurrence_identity", "assertion_position"}
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
                pin.path_position_assertion_reference[
                    "recorded_occurrence_identity"
                ],
                pin.path_position_assertion_reference["assertion_position"],
                pin.recorded_finding_reference["finding_category"],
                pin.recorded_finding_reference["finding_position"],
            )
            for pin in pins
        }
    ) == len(pins)
    assert all(pin.through_event_occurrence_identity == results[-1].identity for pin in pins)
    assert ledger.append_boundary() == boundary


def test_pair_findings_and_path_do_not_authorize_distinction_fanout_by_presence():
    ledger, _earlier_source, _added, _comparison, _path = _inputs()
    boundary = ledger.append_boundary()

    assert recorded_distinction_pins_from_current_coordinates(
        ledger, locality_identity=LOCALITY
    ) == ()
    assert ledger.append_boundary() == boundary


def test_distinction_fanout_keeps_one_locality_pin_after_another_locality_append():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
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
    ledger, _earlier_source, _added, comparison, path = _inputs(
        path_source_is_added=False
    )
    binding = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=comparison.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_binding = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_subject_to_act_binding(
        ledger,
        comparison_binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence(
        ledger,
        applicability_binding_event_identity=applicability_binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
        ledger, act_occurrence_event_identity=applicability_act.identity
    )
    reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability(
        ledger, applicability.identity
    )
    assert reading["applicability"] == "inapplicable"
    assert reading["dimensions"]["content"]["same_source_occurrence"] is False
    with pytest.raises(ValueError, match="not applicable"):
        record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence(
            ledger,
            subject_to_act_binding_event_identity=binding.identity,
            applicability_result_event_identity=applicability.identity,
            current_coordinates=_current_coordinates(ledger),
        )


def test_availability_without_both_exact_current_coordinates_cannot_assign_comparison():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    current_coordinates = _current_coordinates(ledger)
    current_coordinates["comparison_result_occurrences"].pop(comparison.identity)
    with pytest.raises(
        ValueError, match="each exact result in current coordinates"
    ):
        record_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding(
            ledger,
            path_result_event_identity=path.identity,
            comparison_result_event_identity=comparison.identity,
            current_coordinates=current_coordinates,
        )


def test_one_ordered_relation_path_pair_finding_compare_act_cannot_yield_twice():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _binding, _applicability, act, _result = _record_comparison(
        ledger, comparison, path
    )
    with pytest.raises(ValueError, match="cannot Yield twice"):
        record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
            ledger, act_occurrence_event_identity=act.identity
        )


def test_changed_input_compare_is_refused_on_later_read():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
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
        get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
            ledger, result.identity
        )


def test_higher_input_preserves_the_exact_comparison_binding(monkeypatch):
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
    assert reading["binding_event_identity"] == binding_identity
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


def test_corrupted_higher_compare_yield_is_refused():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
    )
    yield_relation = ledger.get(result.material["yield_relation_identity"])
    assert yield_relation is not None
    yield_relation.material["result_identity"] = "crossed-result"

    with pytest.raises(ValueError, match="exact Yield relation"):
        get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
            ledger, result.identity
        )


def test_each_higher_lifecycle_read_validates_large_inputs_once_without_retained_read(
    monkeypatch,
):
    ledger, _earlier_source, _added, comparison, path = _inputs()
    binding = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=comparison.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_binding = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_subject_to_act_binding(
        ledger,
        comparison_binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability_act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence(
        ledger,
        applicability_binding_event_identity=applicability_binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    applicability = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
        ledger, act_occurrence_event_identity=applicability_act.identity
    )
    current_coordinates = _current_coordinates(ledger)
    original = comparison_module._inputs
    calls = []

    def counted(ledger, **identities):
        calls.append(
            (
                identities["path_result_event_identity"],
                identities["comparison_result_event_identity"],
            )
        )
        return original(ledger, **identities)

    monkeypatch.setattr(comparison_module, "_inputs", counted)
    call_coordinates = (path.identity, comparison.identity)

    act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=current_coordinates,
    )
    assert calls == [call_coordinates]

    result = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    assert calls == [call_coordinates, call_coordinates]

    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        ledger, result.identity
    )
    assert calls == [call_coordinates, call_coordinates, call_coordinates]

    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        ledger, result.identity
    )
    assert calls == [call_coordinates] * 4


def test_ordered_path_and_recorded_findings_are_read_from_sqlite(tmp_path):
    database = tmp_path / "ordered-relation-path-pair-finding-comparison.sqlite"
    source, _earlier_source, _added, comparison, path = _inputs()
    _binding, _applicability, _act, result = _record_comparison(
        source, comparison, path
    )
    result_identity = result.identity
    ledger = SQLiteEventLedger(str(database))
    ledger.append_many(source.list())
    ledger.close()

    durable = SQLiteEventLedger(str(database))
    reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        durable, result_identity
    )
    assert reading["finding"]["relation_findings"]
    assert result_identity in _current_coordinates(durable)["comparison_result_occurrences"]
    assert recorded_distinction_pins_from_current_coordinates(
        durable, locality_identity=LOCALITY
    )
    durable.close()


def test_advanced_current_coordinates_equal_replay_for_comparison_of_ordered_relation_path_with_recorded_pair_findings():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    prior = _current_coordinates(ledger)
    prior_count = len(ledger.list_locality(LOCALITY))
    _record_comparison(ledger, comparison, path)
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
        test_ordered_path_and_recorded_findings_are_read_from_sqlite,
        test_advanced_current_coordinates_equal_replay_for_comparison_of_ordered_relation_path_with_recorded_pair_findings,
    ),
}
