from __future__ import annotations

import pytest

import seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings as comparison_module
from seed_runtime.byte_measurement import (
    record_byte_measurement_responsibility_assignment,
    assertions_of_recorded_byte_position_pair_measurement,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result,
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
from seed_runtime.material_ingest import ingest_material
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
        source_ingest_occurrence_identity=source.identity,
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
    earlier_source = ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abcabc",
        source_role="system",
        source_boundary="earlier exact occurrence",
    )
    earlier = _pair_measurement(ledger)
    added = ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abc",
        source_role="system",
        source_boundary="added exact occurrence",
        provenance_occurrence_references=(earlier_source.identity,),
    )
    later = _pair_measurement(ledger)
    comparison = _record_pair_comparison(ledger, earlier, later)
    path_source = added
    if not path_source_is_added:
        path_source = ingest_material(
            ledger,
            locality_identity=LOCALITY,
            exact_bytes=b"abc",
            source_role="system",
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


def test_each_higher_lifecycle_read_validates_large_inputs_once_without_cache(
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


def test_relation_of_relations_survives_sqlite_restart(tmp_path):
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
    reopened.close()


def test_incremental_standing_equals_replay_for_comparison_of_ordered_relation_path_with_recorded_pair_findings():
    ledger, _earlier_source, _added, comparison, path = _inputs()
    prior = _standing(ledger)
    prior_count = len(ledger.list_locality(LOCALITY))
    _record_comparison(ledger, comparison, path)
    later = tuple(
        event.identity for event in ledger.list_locality(LOCALITY)[prior_count:]
    )
    incremental = advance_operator_locality_standing(
        ledger, later, locality_identity=LOCALITY, prior=prior
    )
    assert incremental == _standing(ledger)


def test_relation_of_relations_is_addressable_but_has_no_raw_material():
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
        test_availability_without_both_exact_standings_cannot_assign_comparison,
    ),
    "yield_result_occurrence_evidence": (
        test_one_ordered_relation_path_pair_finding_compare_act_cannot_yield_twice,
        test_changed_input_compare_is_refused_on_later_read,
        test_corrupted_higher_compare_yield_is_refused,
        test_each_higher_lifecycle_read_validates_large_inputs_once_without_cache,
    ),
    "declared_measurement_result": (
        test_relation_of_relations_survives_sqlite_restart,
        test_incremental_standing_equals_replay_for_comparison_of_ordered_relation_path_with_recorded_pair_findings,
    ),
    "representation_source_coordinates": (
        test_relation_of_relations_is_addressable_but_has_no_raw_material,
    ),
}
