from __future__ import annotations

import pytest

import seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings as comparison_module
import seed_runtime.comparison_of_recorded_byte_pair_measurements as recorded_pair_comparison_module
from seed_runtime.byte_measurement import (
    record_byte_measurement_responsibility_assignment,
    assertions_of_recorded_byte_position_pair_measurement,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.candidate_standing_from_exact_result_assertions import (
    get_recorded_candidate_standing,
    record_one_source_and_ordered_pair_candidate_standings,
    source_assertion_references_for_candidate_standing,
)
from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    OrderedPathPairFindingCompareAssignmentSubject,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability,
    recorded_distinction_pins_from_current_standing,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result,
    record_ordered_path_pair_finding_compare_assignments_from_current_standing,
    record_ordered_path_pair_finding_compare_applicability_from_current_standing,
    record_applicable_ordered_path_pair_finding_compare_act_evidence_from_current_standing,
    record_ordered_path_pair_finding_compare_results_from_current_standing,
    unassigned_ordered_path_pair_finding_compare_subjects_in_current_standing,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    get_recorded_pair_measurement_comparison,
    record_recorded_pair_measurement_comparison_act_evidence,
    record_recorded_pair_measurement_comparison_applicability_act_evidence,
    record_recorded_pair_measurement_comparison_applicability_result,
    record_recorded_pair_measurement_comparison_responsibility_assignment,
    record_recorded_pair_measurement_comparison_result,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.witness_material_acquisition import record_witness_material_acquisition
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    measure_positions_for_recurrent_byte_pair_assertions,
    record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position,
    record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position,
    record_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
    references_to_recorded_recurrent_byte_pair_occurrence_positions,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    record_shared_position_applicability_act_evidence,
    record_shared_position_applicability_result,
    record_shared_position_measurement_act_evidence,
    record_shared_position_measurement_result,
    record_shared_position_responsibility_assignment,
)
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_representation import (
    read_operator_representation,
    record_operator_representation,
)


LOCALITY = "ordered-relation-path-pair-finding-comparison"


def _standing(ledger):
    return read_operator_locality_standing(
        ledger, locality_identity=LOCALITY
    )


def _pair_measurement(ledger):
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=(LOCALITY,),
        recording_locality_identity=LOCALITY,
        locality_standing=_standing(ledger),
    )
    act = record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger),
    )
    byte_result = record_byte_measurement_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    return record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_result.identity,
        recording_locality_identity=LOCALITY,
    )


def _record_pair_comparison(ledger, earlier, later):
    assignment = record_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        locality_standing=_standing(ledger),
    )
    applicability_act = (
        record_recorded_pair_measurement_comparison_applicability_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            locality_standing=_standing(ledger),
        )
    )
    applicability = record_recorded_pair_measurement_comparison_applicability_result(
        ledger,
        responsible_act_evidence_event_identity=applicability_act.identity,
    )
    act = record_recorded_pair_measurement_comparison_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=_standing(ledger),
    )
    return record_recorded_pair_measurement_comparison_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )


def _record_path(ledger, pair_measurement, source):
    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair_measurement.identity
    )
    recurrence = {
        assertion.representation: assertion.assertion_identity
        for assertion in assertions or ()
        if assertion.result == "recurrence"
        and assertion.representation in {(97, 98), (98, 99)}
    }
    findings = measure_positions_for_recurrent_byte_pair_assertions(
        ledger,
        pair_measurement_occurrence_identity=pair_measurement.identity,
        recurrence_assertion_identities=(recurrence[(97, 98)], recurrence[(98, 99)]),
        source_material_acquisition_occurrence_identity=source.identity,
        occurrence_limit=16,
        through=ledger.append_boundary(),
    )
    results = []
    for finding in findings:
        assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            finding=finding,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=LOCALITY
            ),
        )
        act = record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=read_operator_locality_standing(
                ledger, locality_identity=LOCALITY
            ),
        )
        results.append(
            record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
                ledger, responsible_act_evidence_event_identity=act.identity
            )
        )
    references = tuple(
        reference
        for result in results
        for reference in references_to_recorded_recurrent_byte_pair_occurrence_positions(
            ledger, result_occurrence_identity=result.identity
        )
    )
    first = next(reference for reference in references if reference.exact_pair == b"ab")
    second = next(reference for reference in references if reference.exact_pair == b"bc")
    assignment = record_shared_position_responsibility_assignment(
        ledger,
        first_result_occurrence_identity=first.recorded_occurrence_identity,
        first_assertion_identity=first.assertion_identity,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_assertion_identity=second.assertion_identity,
        locality_standing=_standing(ledger),
    )
    applicability_act = record_shared_position_applicability_act_evidence(
        ledger,
        assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger),
    )
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_evidence_event_identity=applicability_act.identity,
    )
    act = record_shared_position_measurement_act_evidence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        locality_standing=_standing(ledger),
    )
    return record_shared_position_measurement_result(
        ledger, measurement_act_evidence_event_identity=act.identity
    )


def _inputs(*, ledger=None, path_source_is_added=True):
    if ledger is None:
        ledger = EventLedger()
    earlier_source = record_witness_material_acquisition(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abcabc",
        source_boundary="earlier exact occurrence",
    )
    earlier = _pair_measurement(ledger)
    added = record_witness_material_acquisition(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abc",
        source_boundary="added exact occurrence",
        provenance_occurrence_references=(earlier_source.identity,),
    )
    later = _pair_measurement(ledger)
    comparison = _record_pair_comparison(ledger, earlier, later)
    path_source = added
    if not path_source_is_added:
        path_source = record_witness_material_acquisition(
            ledger,
            locality_identity=LOCALITY,
            exact_bytes=b"abc",
            source_boundary="unrelated exact occurrence",
            provenance_occurrence_references=(earlier_source.identity,),
        )
    path = _record_path(ledger, earlier, path_source)
    return ledger, earlier_source, added, comparison, path


def _record_comparison(ledger, comparison, path):
    assignment = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=comparison.identity,
        locality_standing=_standing(ledger),
    )
    applicability_act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger),
    )
    applicability = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
        ledger, responsible_act_evidence_event_identity=applicability_act.identity
    )
    act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=_standing(ledger),
    )
    result = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    return assignment, applicability, act, result


def test_yielded_path_meets_complete_findings_of_the_same_added_occurrence():
    ledger, _earlier_source, added, comparison, path = _inputs()
    assignment, applicability, act, result = _record_comparison(
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
    assert assignment.material["path_source_occurrence_identity"] == added.identity
    assert len(act.material["participation_of_input_in_compare"]) == 2
    roles = reading["finding"]["relation_findings"]
    assert [role["pair_subject"] for role in roles] == [[97, 98], [98, 99]]
    assert all(role["comparison_finding_references"] for role in roles)
    assert all(
        set(reference)
        == {
            "recorded_comparison_occurrence_identity",
            "finding_category",
            "finding_position",
            "subject",
        }
        for role in roles
        for reference in role["comparison_finding_references"]
    )
    assert {
        reference["finding_category"]
        for role in roles
        for reference in role["comparison_finding_references"]
    } <= {
        "same_content_findings",
        "conflicting_findings",
        "findings_of_earlier_result",
        "findings_of_later_result",
        "unknown_findings",
    }
    recorded_comparison = get_recorded_pair_measurement_comparison(
        ledger, comparison.identity
    )
    first_count_reference = next(
        reference
        for reference in roles[0]["comparison_finding_references"]
        if reference["subject"]["result"] == "count"
    )
    first_count = recorded_comparison["findings"][
        first_count_reference["finding_category"]
    ][first_count_reference["finding_position"]]
    assert first_count["earlier_content"]["count"] == 2
    assert first_count["later_content"]["count"] == 3
    assert result.exact_material is None


def test_unassigned_exact_compare_subject_read_records_nothing():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    boundary_before_read = ledger.append_boundary()

    assert unassigned_ordered_path_pair_finding_compare_subjects_in_current_standing(
        ledger, locality_identity=LOCALITY
    ) == (
        OrderedPathPairFindingCompareAssignmentSubject(
            path_result_event_identity=path.identity,
            comparison_result_event_identity=comparison.identity,
        ),
    )
    assert ledger.append_boundary() == boundary_before_read

    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=comparison.identity,
        locality_standing=_standing(ledger),
    )

    assert (
        unassigned_ordered_path_pair_finding_compare_subjects_in_current_standing(
            ledger, locality_identity=LOCALITY
        )
        == ()
    )


def test_unassigned_exact_compare_subject_read_replays_after_restart(tmp_path):
    database = str(tmp_path / "ordered-path-compare-subject.sqlite")
    ledger = SQLiteEventLedger(database)
    ledger, _earlier_source, _added, comparison, path = _inputs(ledger=ledger)
    expected = (
        OrderedPathPairFindingCompareAssignmentSubject(
            path_result_event_identity=path.identity,
            comparison_result_event_identity=comparison.identity,
        ),
    )
    assert unassigned_ordered_path_pair_finding_compare_subjects_in_current_standing(
        ledger, locality_identity=LOCALITY
    ) == expected
    ledger.close()

    reopened = SQLiteEventLedger(database)
    try:
        assert unassigned_ordered_path_pair_finding_compare_subjects_in_current_standing(
            reopened, locality_identity=LOCALITY
        ) == expected
    finally:
        reopened.close()


def test_unassigned_exact_compare_subject_read_returns_every_path_and_comparison_pair():
    ledger, _first_source, _first_added, first_comparison, first_path = _inputs()
    ledger, _second_source, _second_added, second_comparison, second_path = _inputs(
        ledger=ledger
    )
    expected = tuple(
        OrderedPathPairFindingCompareAssignmentSubject(
            path_result_event_identity=path.identity,
            comparison_result_event_identity=comparison.identity,
        )
        for path in (first_path, second_path)
        for comparison in (first_comparison, second_comparison)
    )

    assert unassigned_ordered_path_pair_finding_compare_subjects_in_current_standing(
        ledger, locality_identity=LOCALITY
    ) == expected

    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
        ledger,
        path_result_event_identity=first_path.identity,
        comparison_result_event_identity=second_comparison.identity,
        locality_standing=_standing(ledger),
    )

    assert unassigned_ordered_path_pair_finding_compare_subjects_in_current_standing(
        ledger, locality_identity=LOCALITY
    ) == tuple(
        subject
        for subject in expected
        if subject
        != OrderedPathPairFindingCompareAssignmentSubject(
            path_result_event_identity=first_path.identity,
            comparison_result_event_identity=second_comparison.identity,
        )
    )


def test_every_current_compare_subject_records_one_serial_responsibility_assignment():
    ledger, _first_source, _first_added, first_comparison, first_path = _inputs()
    ledger, _second_source, _second_added, second_comparison, second_path = _inputs(
        ledger=ledger
    )
    standing_before = _standing(ledger)
    boundary_before = ledger.append_boundary()
    assert boundary_before.identity != standing_before[
        "through_event_occurrence_identity"
    ]
    expected_subjects = tuple(
        OrderedPathPairFindingCompareAssignmentSubject(
            path_result_event_identity=path.identity,
            comparison_result_event_identity=comparison.identity,
        )
        for path in (first_path, second_path)
        for comparison in (first_comparison, second_comparison)
    )

    recorded = (
        record_ordered_path_pair_finding_compare_assignments_from_current_standing(
            ledger, locality_identity=LOCALITY
        )
    )
    assignments = recorded.assignment_occurrences

    assert len(assignments) == len(expected_subjects) == 4
    assert tuple(
        OrderedPathPairFindingCompareAssignmentSubject(
            path_result_event_identity=assignment.material[
                "path_result_reference"
            ]["recorded_occurrence_identity"],
            comparison_result_event_identity=assignment.material[
                "comparison_result_reference"
            ]["recorded_occurrence_identity"],
        )
        for assignment in assignments
    ) == expected_subjects
    assert tuple(
        assignment.material["standing_boundary_identity"]
        for assignment in assignments
    ) == (
        standing_before["through_event_occurrence_identity"],
        assignments[0].identity,
        assignments[1].identity,
        assignments[2].identity,
    )
    assert recorded.locality_standing["through_event_occurrence_identity"] == (
        assignments[-1].identity
    )
    assert all(
        assignment.identity
        in recorded.locality_standing["responsibility_assignment_occurrences"]
        for assignment in assignments
    )
    assert recorded.locality_standing["applicability_result_occurrences"] == (
        standing_before["applicability_result_occurrences"]
    )
    assert (
        unassigned_ordered_path_pair_finding_compare_subjects_in_current_standing(
            ledger, locality_identity=LOCALITY
        )
        == ()
    )

    boundary_after = ledger.append_boundary()
    repeated = (
        record_ordered_path_pair_finding_compare_assignments_from_current_standing(
            ledger, locality_identity=LOCALITY
        )
    )
    assert repeated.assignment_occurrences == ()
    assert repeated.locality_standing == recorded.locality_standing
    assert ledger.append_boundary() == boundary_after


def test_every_current_compare_assignment_records_one_separate_applicability_result():
    ledger, _first_source, _first_added, _first_comparison, _first_path = _inputs()
    ledger, _second_source, _second_added, _second_comparison, _second_path = (
        _inputs(ledger=ledger)
    )
    assignments = (
        record_ordered_path_pair_finding_compare_assignments_from_current_standing(
            ledger, locality_identity=LOCALITY
        ).assignment_occurrences
    )
    compare_results_before = tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        )
    )

    recorded = (
        record_ordered_path_pair_finding_compare_applicability_from_current_standing(
            ledger, locality_identity=LOCALITY
        )
    )
    results = recorded.applicability_result_occurrences

    assert len(results) == len(assignments) == 4
    assert tuple(result.material["applicability"] for result in results) == (
        "applicable",
        "inapplicable",
        "inapplicable",
        "applicable",
    )
    assert tuple(
        result.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
        for result in results
    ) == tuple(assignment.identity for assignment in assignments)
    assert all(
        result.identity
        in recorded.locality_standing["applicability_result_occurrences"]
        for result in results
    )
    assert all(
        "participation_of_input_in_compare" not in result.material
        for result in results
    )
    assert tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        )
    ) == compare_results_before

    boundary_after = ledger.append_boundary()
    repeated = (
        record_ordered_path_pair_finding_compare_applicability_from_current_standing(
            ledger, locality_identity=LOCALITY
        )
    )
    assert repeated.applicability_result_occurrences == ()
    assert repeated.locality_standing == recorded.locality_standing
    assert ledger.append_boundary() == boundary_after


def test_only_applicable_current_compare_results_record_participation_and_act_evidence():
    ledger, _first_source, _first_added, _first_comparison, _first_path = _inputs()
    ledger, _second_source, _second_added, _second_comparison, _second_path = (
        _inputs(ledger=ledger)
    )
    assignments = (
        record_ordered_path_pair_finding_compare_assignments_from_current_standing(
            ledger, locality_identity=LOCALITY
        ).assignment_occurrences
    )
    applicability_results = (
        record_ordered_path_pair_finding_compare_applicability_from_current_standing(
            ledger, locality_identity=LOCALITY
        ).applicability_result_occurrences
    )
    compare_results_before = tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        )
    )

    recorded = record_applicable_ordered_path_pair_finding_compare_act_evidence_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    acts = recorded.compare_act_evidence_occurrences

    assert len(acts) == 2
    assert tuple(
        act.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
        for act in acts
    ) == (assignments[0].identity, assignments[3].identity)
    assert tuple(
        act.material["applicability_result_event_identity"] for act in acts
    ) == (applicability_results[0].identity, applicability_results[3].identity)
    assert all(
        tuple(
            participation["role"]
            for participation in act.material["participation_of_input_in_compare"]
        )
        == ("ordered relation path", "recorded pair comparison result")
        for act in acts
    )
    assert all(
        len(act.material["participation_of_input_in_compare"]) == 2
        for act in acts
    )
    assert tuple(
        result.material["addressed_act_occurrence_identity"]
        for result in applicability_results
        if result.material["applicability"] == "inapplicable"
    ) == (None, None)
    assert recorded.locality_standing["through_event_occurrence_identity"] == (
        acts[-1].identity
    )
    assert tuple(
        ledger.iter_locality_kind(
            LOCALITY,
            COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        )
    ) == compare_results_before

    boundary_after = ledger.append_boundary()
    repeated = record_applicable_ordered_path_pair_finding_compare_act_evidence_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    assert repeated.compare_act_evidence_occurrences == ()
    assert repeated.locality_standing == recorded.locality_standing
    assert ledger.append_boundary() == boundary_after


def test_every_current_compare_act_records_one_separate_yield_and_result():
    ledger, _first_source, _first_added, _first_comparison, _first_path = _inputs()
    ledger, _second_source, _second_added, _second_comparison, _second_path = (
        _inputs(ledger=ledger)
    )
    record_ordered_path_pair_finding_compare_assignments_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    record_ordered_path_pair_finding_compare_applicability_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    acts = record_applicable_ordered_path_pair_finding_compare_act_evidence_from_current_standing(
        ledger, locality_identity=LOCALITY
    ).compare_act_evidence_occurrences

    recorded = record_ordered_path_pair_finding_compare_results_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    results = recorded.compare_result_occurrences

    assert len(results) == len(acts) == 2
    assert tuple(
        result.material["responsible_act_evidence_identity"] for result in results
    ) == tuple(act.identity for act in acts)
    assert len(
        {
            result.material["evidence_of_yield_relation_identity"]
            for result in results
        }
    ) == len(results)
    assert all(
        ledger.get(result.material["evidence_of_yield_relation_identity"])
        is not None
        for result in results
    )
    assert all(
        result.identity
        in recorded.locality_standing["comparison_result_occurrences"]
        for result in results
    )
    assert all(
        result.material["participation_of_input_in_compare"]
        == act.material["participation_of_input_in_compare"]
        for result, act in zip(results, acts)
    )
    assert all(result.exact_material is None for result in results)
    assert all(
        tuple(
            role["role"] for role in result.material["finding"]["relation_findings"]
        )
        == ("first_path_relation", "second_path_relation")
        for result in results
    )
    assert all("exact_material" not in result.material["finding"] for result in results)
    assert all(
        "represented_relation" not in result.material["finding"]
        for result in results
    )
    assert recorded.locality_standing["through_event_occurrence_identity"] == (
        results[-1].identity
    )

    boundary_after = ledger.append_boundary()
    repeated = record_ordered_path_pair_finding_compare_results_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    assert repeated.compare_result_occurrences == ()
    assert repeated.locality_standing == recorded.locality_standing
    assert ledger.append_boundary() == boundary_after


def test_complete_compare_lifecycle_advances_each_carried_read(monkeypatch):
    ledger, _first_source, _first_added, _first_comparison, _first_path = _inputs()
    ledger, _second_source, _second_added, _second_comparison, _second_path = (
        _inputs(ledger=ledger)
    )
    import seed_runtime.operator_locality_standing as standing_module

    read = standing_module.read_operator_locality_standing
    reads = 0

    def counted_read(*args, **kwargs):
        nonlocal reads
        reads += 1
        return read(*args, **kwargs)

    monkeypatch.setattr(
        standing_module, "read_operator_locality_standing", counted_read
    )

    assignments = record_ordered_path_pair_finding_compare_assignments_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    applicability = record_ordered_path_pair_finding_compare_applicability_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    acts = record_applicable_ordered_path_pair_finding_compare_act_evidence_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    results = record_ordered_path_pair_finding_compare_results_from_current_standing(
        ledger, locality_identity=LOCALITY
    )

    assert reads == 4
    assert assignments.locality_standing["through_event_occurrence_identity"] == (
        assignments.assignment_occurrences[-1].identity
    )
    assert applicability.locality_standing["through_event_occurrence_identity"] == (
        applicability.applicability_result_occurrences[-1].identity
    )
    assert acts.locality_standing["through_event_occurrence_identity"] == (
        acts.compare_act_evidence_occurrences[-1].identity
    )
    assert results.locality_standing == read(
        ledger, locality_identity=LOCALITY
    )


def test_current_standing_fans_one_comparison_into_exact_distinction_pins():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _assignment, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
    )
    boundary = ledger.append_boundary()
    standing_boundary = _standing(ledger)["through_event_occurrence_identity"]

    pins = recorded_distinction_pins_from_current_standing(
        ledger, locality_identity=LOCALITY
    )

    assert ledger.append_boundary() == boundary
    assert all(
        pin.comparison_result_occurrence_identity == result.identity for pin in pins
    )
    assert all(pin.standing_boundary_identity == standing_boundary for pin in pins)
    assert tuple(pin.path_role for pin in pins) == (
        "first_path_relation",
        "first_path_relation",
        "second_path_relation",
        "second_path_relation",
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
    assert recorded_distinction_pins_from_current_standing(
        ledger, locality_identity=LOCALITY
    )[0].recorded_finding_reference["finding_category"] == "same_content_findings"


def test_every_current_compare_result_exposes_every_exact_finding_reference_branch():
    ledger, _first_source, _first_added, _first_comparison, _first_path = _inputs()
    ledger, _second_source, _second_added, _second_comparison, _second_path = (
        _inputs(ledger=ledger)
    )
    record_ordered_path_pair_finding_compare_assignments_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    record_ordered_path_pair_finding_compare_applicability_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    record_applicable_ordered_path_pair_finding_compare_act_evidence_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    results = record_ordered_path_pair_finding_compare_results_from_current_standing(
        ledger, locality_identity=LOCALITY
    ).compare_result_occurrences
    boundary = ledger.append_boundary()

    pins = recorded_distinction_pins_from_current_standing(
        ledger, locality_identity=LOCALITY
    )

    assert len(results) == 2
    assert tuple(pin.comparison_result_occurrence_identity for pin in pins) == tuple(
        result.identity for result in results for _ in range(4)
    )
    assert tuple(pin.path_role for pin in pins) == (
        "first_path_relation",
        "first_path_relation",
        "second_path_relation",
        "second_path_relation",
    ) * len(results)
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
                pin.path_role,
                pin.recorded_finding_reference["finding_category"],
                pin.recorded_finding_reference["finding_position"],
            )
            for pin in pins
        }
    ) == len(pins)
    assert all(pin.standing_boundary_identity == results[-1].identity for pin in pins)
    assert ledger.append_boundary() == boundary


def test_every_current_compare_result_and_finding_enter_later_candidate_source_read():
    ledger, _first_source, _first_added, _first_comparison, _first_path = _inputs()
    ledger, _second_source, _second_added, _second_comparison, _second_path = (
        _inputs(ledger=ledger)
    )
    record_ordered_path_pair_finding_compare_assignments_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    record_ordered_path_pair_finding_compare_applicability_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    record_applicable_ordered_path_pair_finding_compare_act_evidence_from_current_standing(
        ledger, locality_identity=LOCALITY
    )
    results = record_ordered_path_pair_finding_compare_results_from_current_standing(
        ledger, locality_identity=LOCALITY
    ).compare_result_occurrences
    boundary = ledger.append_boundary()

    references = source_assertion_references_for_candidate_standing(
        ledger, source_append_boundary=boundary
    )
    result_identities = {result.identity for result in results}
    comparison_references = tuple(
        reference
        for reference in references
        if reference["recorded_result_occurrence_identity"] in result_identities
    )

    assert len(results) == 2
    assert tuple(
        (
            reference["recorded_result_occurrence_identity"],
            reference["assertion_coordinate"],
        )
        for reference in comparison_references
    ) == tuple(
        (result.identity, coordinate)
        for result in results
        for coordinate in ("result", "finding")
    )
    assert tuple(
        reference["assertion_identity"] for reference in comparison_references
    ) == tuple(
        identity
        for result in results
        for identity in (
            result.material["result_identity"],
            result.material["finding"]["identity"],
        )
    )
    assert all(
        reference["source_standing_coordinate"]
        == "comparison_result_occurrences"
        for reference in comparison_references
    )
    assert all(
        reference["source_standing_through_event_occurrence_identity"]
        == results[-1].identity
        for reference in comparison_references
    )
    assert ledger.append_boundary() == boundary


def test_compare_result_and_finding_enter_both_complete_later_candidate_productions():
    ledger, _source, _added, comparison, path = _inputs()
    _assignment, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
    )
    source_boundary = ledger.append_boundary()
    source_references = source_assertion_references_for_candidate_standing(
        ledger, source_append_boundary=source_boundary
    )
    compare_references = tuple(
        reference
        for reference in source_references
        if reference["recorded_result_occurrence_identity"] == result.identity
    )
    assert tuple(
        reference["assertion_coordinate"] for reference in compare_references
    ) == ("result", "finding")
    comparison_count_before = sum(
        event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
        for event in ledger.list()
    )

    one_source_result, ordered_pair_result = (
        record_one_source_and_ordered_pair_candidate_standings(
            ledger,
            source_append_boundary=source_boundary,
            one_source_recording_locality_identity="ordered-path-unary-candidates",
            ordered_pair_recording_locality_identity="ordered-path-pair-candidates",
        )
    )
    one_source = get_recorded_candidate_standing(
        ledger, one_source_result.identity
    )
    ordered_pair = get_recorded_candidate_standing(
        ledger, ordered_pair_result.identity
    )

    assert tuple(
        candidate["assertion_subject"]["source_assertion_reference"]
        for candidate in one_source["candidate_assertions"]
    ) == tuple(source_references)
    assert tuple(
        candidate["assertion_subject"]["source_assertion_reference"]
        for candidate in one_source["candidate_assertions"]
        if candidate["assertion_subject"]["source_assertion_reference"]
        in compare_references
    ) == compare_references
    assert all(
        candidate["represented_relation"] == "Unknown"
        for candidate in one_source["candidate_assertions"]
    )

    candidate_pairs = tuple(
        (
            candidate["assertion_subject"]["first_source_assertion_reference"],
            candidate["assertion_subject"]["second_source_assertion_reference"],
        )
        for candidate in ordered_pair["candidate_assertions"]
    )
    expected_compare_pairs = tuple(
        (first, second)
        for first_position, first in enumerate(source_references)
        for second_position, second in enumerate(source_references)
        if first_position != second_position
        and (first in compare_references or second in compare_references)
    )
    assert tuple(
        pair
        for pair in candidate_pairs
        if pair[0] in compare_references or pair[1] in compare_references
    ) == expected_compare_pairs
    assert len(expected_compare_pairs) == (
        len(compare_references)
        * (2 * len(source_references) - len(compare_references) - 1)
    )
    assert all(
        candidate["represented_relation"] == "Unknown"
        for candidate in ordered_pair["candidate_assertions"]
    )
    assert one_source_result.locality_identity == "ordered-path-unary-candidates"
    assert ordered_pair_result.locality_identity == "ordered-path-pair-candidates"
    assert all(
        reference["source_locality_identity"] == LOCALITY
        for reference in compare_references
    )
    assert sum(
        event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
        for event in ledger.list()
    ) == comparison_count_before


def test_pair_findings_and_path_do_not_authorize_distinction_fanout_by_presence():
    ledger, _earlier_source, _added, _comparison, _path = _inputs()
    boundary = ledger.append_boundary()

    assert recorded_distinction_pins_from_current_standing(
        ledger, locality_identity=LOCALITY
    ) == ()
    assert ledger.append_boundary() == boundary


def test_distinction_fanout_keeps_one_locality_pin_after_another_locality_append():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _assignment, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
    )
    ledger.append("test.occurrence", {"unknown": []}, locality_identity="other")
    boundary = ledger.append_boundary()

    pins = recorded_distinction_pins_from_current_standing(
        ledger, locality_identity=LOCALITY
    )

    assert pins
    assert all(pin.comparison_result_occurrence_identity == result.identity for pin in pins)
    assert ledger.append_boundary() == boundary


def test_another_source_occurrence_is_inapplicable_and_cannot_participate():
    ledger, _earlier_source, _added, comparison, path = _inputs(
        path_source_is_added=False
    )
    assignment = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=comparison.identity,
        locality_standing=_standing(ledger),
    )
    applicability_act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger),
    )
    applicability = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
        ledger, responsible_act_evidence_event_identity=applicability_act.identity
    )
    reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability(
        ledger, applicability.identity
    )
    assert reading["applicability"] == "inapplicable"
    assert reading["dimensions"]["content"]["same_source_occurrence"] is False
    with pytest.raises(ValueError, match="not applicable"):
        record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=_standing(ledger),
        )


def test_availability_without_both_exact_standings_cannot_assign_comparison():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    standing = _standing(ledger)
    standing["comparison_result_occurrences"].pop(comparison.identity)
    with pytest.raises(
        ValueError, match="each exact result in current Standing"
    ):
        record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
            ledger,
            path_result_event_identity=path.identity,
            comparison_result_event_identity=comparison.identity,
            locality_standing=standing,
        )


def test_one_ordered_relation_path_pair_finding_compare_act_cannot_yield_twice():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _assignment, _applicability, act, _result = _record_comparison(
        ledger, comparison, path
    )
    with pytest.raises(ValueError, match="cannot Yield twice"):
        record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
            ledger, responsible_act_evidence_event_identity=act.identity
        )


def test_changed_input_compare_is_refused_on_later_read():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _assignment, _applicability, _act, result = _record_comparison(
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


def test_higher_input_preserves_the_validated_comparison_assignment(monkeypatch):
    ledger, _earlier_source, _added, comparison, _path = _inputs()
    assignment_reads = []
    original = recorded_pair_comparison_module._assignment_reading

    def witnessed(ledger, event_identity):
        assignment_reads.append(event_identity)
        return original(ledger, event_identity)

    monkeypatch.setattr(
        recorded_pair_comparison_module, "_assignment_reading", witnessed
    )
    reading = comparison_module._comparison_input(ledger, comparison.identity)

    assignment_identity = comparison.material[
        "responsibility_assignment_reference"
    ]["recorded_occurrence_identity"]
    assert reading["assignment_event_identity"] == assignment_identity
    assert assignment_reads == [assignment_identity]


def test_higher_input_handoff_still_refuses_comparison_assignment_corruption():
    ledger, _earlier_source, _added, comparison, _path = _inputs()
    assignment = ledger.get(
        comparison.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
    )
    assignment.material["comparison_result_identity"] = "crossed-result"

    with pytest.raises(ValueError):
        comparison_module._comparison_input(ledger, comparison.identity)


def test_corrupted_higher_compare_yield_is_refused():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _assignment, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
    )
    evidence = ledger.get(result.material["evidence_of_yield_relation_identity"])
    assert evidence is not None
    evidence.material["result_identity"] = "crossed-result"

    with pytest.raises(ValueError, match="exact Evidence of Yield"):
        get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
            ledger, result.identity
        )


def test_each_higher_lifecycle_read_validates_large_inputs_once_without_retained_read(
    monkeypatch,
):
    ledger, _earlier_source, _added, comparison, path = _inputs()
    assignment = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=comparison.identity,
        locality_standing=_standing(ledger),
    )
    applicability_act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger),
    )
    applicability = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
        ledger, responsible_act_evidence_event_identity=applicability_act.identity
    )
    standing = _standing(ledger)
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
    expected_call = (path.identity, comparison.identity)

    act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
    )
    assert calls == [expected_call]

    result = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    assert calls == [expected_call, expected_call]

    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        ledger, result.identity
    )
    assert calls == [expected_call, expected_call, expected_call]

    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        ledger, result.identity
    )
    assert calls == [expected_call] * 4


def test_ordered_path_and_recorded_findings_survive_sqlite_restart(tmp_path):
    database = tmp_path / "ordered-relation-path-pair-finding-comparison.sqlite"
    ledger = SQLiteEventLedger(str(database))
    ledger, _earlier_source, _added, comparison, path = _inputs(ledger=ledger)
    _assignment, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
    )
    result_identity = result.identity
    ledger.close()

    reopened = SQLiteEventLedger(str(database))
    reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        reopened, result_identity
    )
    assert reading["finding"]["relation_findings"]
    assert result_identity in _standing(reopened)["comparison_result_occurrences"]
    assert recorded_distinction_pins_from_current_standing(
        reopened, locality_identity=LOCALITY
    )
    reopened.close()


def test_carried_standing_equals_replay_for_comparison_of_ordered_relation_path_with_recorded_pair_findings():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    prior = _standing(ledger)
    prior_count = len(ledger.list_locality(LOCALITY))
    _record_comparison(ledger, comparison, path)
    later = tuple(
        event.identity for event in ledger.list_locality(LOCALITY)[prior_count:]
    )
    carried = advance_operator_locality_standing(
        ledger, later, locality_identity=LOCALITY, prior=prior
    )
    assert carried == _standing(ledger)


def test_ordered_path_and_recorded_findings_are_addressable_without_exact_material():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    _assignment, _applicability, _act, result = _record_comparison(
        ledger, comparison, path
    )
    representation = record_operator_representation(
        ledger,
        locality_identity=LOCALITY,
        locality_standing=_standing(ledger),
        source_occurrence_reference=result.identity,
    )
    recorded = ledger.get(representation["representation_event_identity"])
    reading = read_operator_representation(ledger, recorded.identity)
    assert reading["source_occurrence_reference"] == result.identity
    assert recorded.exact_material is None
    assert "representation_rule" not in recorded.material


FIDELITY_SUBJECTS = {
    "applicability_determination": (
        test_another_source_occurrence_is_inapplicable_and_cannot_participate,
    ),
    "relation_required_coordinates": (
        test_yielded_path_meets_complete_findings_of_the_same_added_occurrence,
        test_unassigned_exact_compare_subject_read_records_nothing,
        test_unassigned_exact_compare_subject_read_replays_after_restart,
        test_unassigned_exact_compare_subject_read_returns_every_path_and_comparison_pair,
        test_every_current_compare_subject_records_one_serial_responsibility_assignment,
        test_every_current_compare_assignment_records_one_separate_applicability_result,
        test_only_applicable_current_compare_results_record_participation_and_act_evidence,
        test_every_current_compare_act_records_one_separate_yield_and_result,
        test_current_standing_fans_one_comparison_into_exact_distinction_pins,
        test_every_current_compare_result_exposes_every_exact_finding_reference_branch,
        test_every_current_compare_result_and_finding_enter_later_candidate_source_read,
        test_compare_result_and_finding_enter_both_complete_later_candidate_productions,
        test_pair_findings_and_path_do_not_authorize_distinction_fanout_by_presence,
        test_distinction_fanout_keeps_one_locality_pin_after_another_locality_append,
        test_availability_without_both_exact_standings_cannot_assign_comparison,
    ),
    "yield_result_occurrence_evidence": (
        test_one_ordered_relation_path_pair_finding_compare_act_cannot_yield_twice,
        test_changed_input_compare_is_refused_on_later_read,
        test_higher_input_preserves_the_validated_comparison_assignment,
        test_higher_input_handoff_still_refuses_comparison_assignment_corruption,
        test_corrupted_higher_compare_yield_is_refused,
        test_each_higher_lifecycle_read_validates_large_inputs_once_without_retained_read,
    ),
    "declared_measurement_result": (
        test_ordered_path_and_recorded_findings_survive_sqlite_restart,
        test_carried_standing_equals_replay_for_comparison_of_ordered_relation_path_with_recorded_pair_findings,
    ),
    "representation_source_coordinates": (
        test_ordered_path_and_recorded_findings_are_addressable_without_exact_material,
    ),
}
