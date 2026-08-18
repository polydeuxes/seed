from copy import deepcopy

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_ingest import ingest_material
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences_whose_difference_is_one import (
    POSITION_DIFFERENCE_ONE_RESULT_KIND,
    get_position_difference_one_measurement_act_evidence,
    get_position_difference_one_measurement_responsibility_assignment,
    get_recorded_position_difference_one_measurement,
    measure_position_coordinates_of_byte_pair_occurrences_whose_difference_is_one,
    record_position_difference_one_measurement_act_evidence,
    record_position_difference_one_measurement_responsibility_assignment,
    record_position_difference_one_measurement_result,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences_whose_difference_is_one,
)
from seed_runtime.operator_locality_standing import (
    _carry_position_difference_one_measurement_result_into_standing,
    read_operator_locality_standing,
)


def _standing(ledger, locality):
    return read_operator_locality_standing(ledger, locality_identity=locality)


def _source(ledger, exact=b"2+2=5\n", locality="position-difference-one"):
    return ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=exact,
        source_role="exact supplied material",
        source_boundary="exact supplied material boundary",
    )


def _record(ledger, exact=b"2+2=5\n", locality="position-difference-one"):
    source = _source(ledger, exact, locality)
    assignment = record_position_difference_one_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
    )
    act = record_position_difference_one_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    result = record_position_difference_one_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )
    return source, assignment, act, result


def test_each_input_pair_has_two_exact_position_coordinates_whose_difference_is_one():
    ledger = EventLedger()
    source = _source(ledger)

    finding = measure_position_coordinates_of_byte_pair_occurrences_whose_difference_is_one(
        ledger,
        source_ingest_occurrence_identity=source.identity,
    )

    assert finding.occurrences == (
        (b"2+", 0, 1),
        (b"+2", 1, 2),
        (b"2=", 2, 3),
        (b"=5", 3, 4),
        (b"5\n", 4, 5),
    )
    assert finding.source_ingest_occurrence_identity == source.identity
    assert finding.completeness_boundary == (
        ledger.append_boundary_through_occurrence(source.identity)
    )


def test_equal_pair_bytes_at_two_position_coordinates_remain_two_occurrences():
    ledger = EventLedger()
    source = _source(ledger, b"aaa")

    finding = measure_position_coordinates_of_byte_pair_occurrences_whose_difference_is_one(
        ledger,
        source_ingest_occurrence_identity=source.identity,
    )

    assert finding.occurrences == ((b"aa", 0, 1), (b"aa", 1, 2))


@pytest.mark.parametrize("exact", (b"", b"x"))
def test_material_without_two_position_coordinates_yields_an_exact_empty_result(exact):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, exact)

    finding = get_recorded_position_difference_one_measurement(
        ledger, result.identity
    )

    assert finding.occurrences == ()
    assert result.material["assertions"]["occurrences"] == 0


def test_assignment_act_yield_and_result_enter_current_standing():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_position_difference_one_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
    )
    assert assignment.identity in _standing(
        ledger, locality
    )["responsibility_assignment_occurrences"]

    act = record_position_difference_one_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    result = record_position_difference_one_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )
    standing = _standing(ledger, locality)

    assert get_position_difference_one_measurement_responsibility_assignment(
        ledger, assignment.identity
    ) == assignment
    assert get_position_difference_one_measurement_act_evidence(
        ledger, act.identity
    ) == act
    assert result.identity in standing["measurement_occurrences"]
    assert result.material["evidence_of_yield_relation_identity"] == (
        standing["measurement_occurrences"][result.identity][
            "evidence_of_yield_relation_identity"
        ]
    )


def test_act_requires_current_standing_that_carries_exact_assignment():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    before_assignment = _standing(ledger, locality)
    assignment = record_position_difference_one_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=before_assignment,
    )

    with pytest.raises(ValueError, match="current Locality Standing"):
        record_position_difference_one_measurement_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=before_assignment,
        )


def test_one_assignment_records_one_act_and_one_result():
    ledger = EventLedger()
    _source_event, assignment, act, _result = _record(ledger)

    with pytest.raises(ValueError, match="already carries an Act"):
        record_position_difference_one_measurement_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=_standing(
                ledger, assignment.locality_identity
            ),
        )
    with pytest.raises(ValueError, match="already carries a Yield"):
        record_position_difference_one_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act.identity,
        )


def test_result_refuses_changed_assertion_coordinates():
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger)
    result.material["assertions"]["dimensions"]["content"][
        "second_position"
    ] = "position"

    with pytest.raises(ValueError, match="coordinates are not exact"):
        get_recorded_position_difference_one_measurement(ledger, result.identity)


def test_references_preserve_every_exact_pair_occurrence():
    ledger = EventLedger()
    source, _assignment, _act, result = _record(ledger, b"aaa")

    references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences_whose_difference_is_one(
            ledger, result.identity
        )
    )

    assert tuple(
        (reference.exact_pair, reference.first_position, reference.second_position)
        for reference in references
    ) == ((b"aa", 0, 1), (b"aa", 1, 2))
    assert len({reference.assertion_identity for reference in references}) == 2
    assert all(
        reference.source_ingest_occurrence_identity == source.identity
        and reference.recorded_occurrence_identity == result.identity
        for reference in references
    )


def test_assignment_act_and_result_survive_separate_restarts(tmp_path):
    path = tmp_path / "position-difference-one.sqlite"
    ledger = SQLiteEventLedger(path)
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_position_difference_one_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
    )
    assignment_identity = assignment.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    assignment = get_position_difference_one_measurement_responsibility_assignment(
        ledger, assignment_identity
    )
    act = record_position_difference_one_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    act_identity = act.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    try:
        result = record_position_difference_one_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act_identity,
        )
        assert get_recorded_position_difference_one_measurement(
            ledger, result.identity
        ).occurrences[0] == (b"2+", 0, 1)
    finally:
        ledger.close()


def test_same_call_result_carry_equals_full_standing_replay():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_position_difference_one_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
    )
    act = record_position_difference_one_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    before_result = _standing(ledger, locality)
    result = record_position_difference_one_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )

    incremental = _carry_position_difference_one_measurement_result_into_standing(
        before_result,
        result,
        prior_through_event_occurrence_identity=act.identity,
    )

    assert incremental == _standing(ledger, locality)


def test_refused_same_call_result_does_not_change_prior_standing():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_position_difference_one_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
    )
    act = record_position_difference_one_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    prior = _standing(ledger, locality)
    unchanged = deepcopy(prior)
    result = record_position_difference_one_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )
    malformed = deepcopy(result)
    malformed.material["unknown"] = "not one exact list"

    with pytest.raises(ValueError, match="Standing is not exact"):
        _carry_position_difference_one_measurement_result_into_standing(
            prior,
            malformed,
            prior_through_event_occurrence_identity=act.identity,
        )

    assert prior == unchanged


def test_result_carries_only_its_declared_measurement_coordinates():
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger)

    assert result.kind == POSITION_DIFFERENCE_ONE_RESULT_KIND
    assert set(result.material) == {
        "result_identity",
        "downstream_act_identity",
        "act_occurrence_identity",
        "exact_act",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_reference",
        "input_applicability",
        "measurement_rule",
        "source_localities",
        "source_ingest_occurrence_identity",
        "completeness_boundary",
        "assertions",
        "unknown",
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    }


FIDELITY_SUBJECTS = {
    "act_evidence_responsibility_boundary_occurrence_authority_scope": (
        test_assignment_act_yield_and_result_enter_current_standing,
        test_act_requires_current_standing_that_carries_exact_assignment,
        test_one_assignment_records_one_act_and_one_result,
        test_assignment_act_and_result_survive_separate_restarts,
        test_same_call_result_carry_equals_full_standing_replay,
        test_refused_same_call_result_does_not_change_prior_standing,
    ),
    "declared_measurement_result": (
        test_each_input_pair_has_two_exact_position_coordinates_whose_difference_is_one,
        test_equal_pair_bytes_at_two_position_coordinates_remain_two_occurrences,
        test_material_without_two_position_coordinates_yields_an_exact_empty_result,
        test_result_refuses_changed_assertion_coordinates,
        test_references_preserve_every_exact_pair_occurrence,
        test_result_carries_only_its_declared_measurement_coordinates,
    ),
}
