from __future__ import annotations

from copy import deepcopy

import pytest


from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.witness_material_acquisition import record_witness_material_acquisition
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_standing_continuation import (
    STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT,
    STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
    STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    StandingLocalityContinuationError,
    get_recorded_standing_locality_continuation,
    get_standing_locality_continuation_responsibility_assignment,
    record_standing_locality_continuation_responsibility_assignment,
    record_standing_locality_continuation_act_occurrence,
    record_standing_locality_continuation_result,
)
from seed_runtime.yield_relation import read_requirements_of_yield_relation


def _source_boundary(
    ledger: EventLedger, locality_identity: str = "source"
) -> tuple[object, str]:
    source = record_witness_material_acquisition(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"\x00\xffprior\n",
        source_boundary="fixture boundary",
    )
    return source, source.identity


def _assignment(
    ledger: EventLedger,
    boundary: str,
    *,
    source_locality_identity: str = "source",
):
    return record_standing_locality_continuation_responsibility_assignment(
        ledger,
        source_locality_identity=source_locality_identity,
        standing_boundary_event_identity=boundary,
    )


def _act(
    ledger: EventLedger,
    boundary: str,
    *,
    source_locality_identity: str = "source",
):
    assignment = _assignment(
        ledger,
        boundary,
        source_locality_identity=source_locality_identity,
    )
    assignment_standing = read_operator_locality_standing(
        ledger, locality_identity=assignment.locality_identity
    )
    return record_standing_locality_continuation_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=assignment_standing,
    )


def test_three_stage_continuation_records_exact_direct_relation_without_copying_standing():
    ledger = EventLedger()
    source, boundary = _source_boundary(ledger)

    act_occurrence = _act(ledger, boundary)
    destination = act_occurrence.locality_identity
    assignment_reference = act_occurrence.material[
        "responsibility_assignment_reference"
    ]
    assignment = get_standing_locality_continuation_responsibility_assignment(
        ledger, assignment_reference["recorded_occurrence_identity"]
    )
    after_act = read_operator_locality_standing(
        ledger, locality_identity=destination
    )

    assert act_occurrence.kind == STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT
    assert destination != "source"
    assert act_occurrence.exact_material is None
    assert assignment.kind == (
        STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    )
    assert assignment.locality_identity == destination
    assert assignment.material["book_clause_identity"] == "06.Locality.B"
    assert assignment.identity in after_act[
        "responsibility_assignment_occurrences"
    ]
    assert assignment.material["standing_boundary_occurrence_reference"] == boundary
    assert assignment_reference == {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
        "book_clause_identity": "06.Locality.B",
        "result_boundary_identity": assignment.material[
            "result_boundary_identity"
        ],
    }
    assert len(
        {
            assignment.identity,
            assignment.material["assignment_identity"],
            assignment.material["assignment_subject_identity"],
            assignment.material["result_boundary_identity"],
            act_occurrence.material["continuation_act_identity"],
            act_occurrence.material["act_occurrence_identity"],
            act_occurrence.material["locality_relation_occurrence_identity"],
        }
    ) == 7
    assert after_act["event_count"] == 2
    assert after_act["recorded_relation_Standing"] == {}
    assert after_act["responsibility_assignment_occurrences"] == {
        assignment.identity: None
    }
    assert after_act["material_acquisition_result_occurrences"] == []
    assert after_act["measurement_occurrences"] == {}
    assert after_act["exact_result_occurrences"] == {}

    result = record_standing_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    recorded = get_recorded_standing_locality_continuation(
        ledger, result.identity
    )
    source_reference = recorded["source_standing_reference"]

    assert result.kind == STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
    assert result.exact_material is None
    assert source_reference == {
        "source_locality_identity": "source",
        "source_standing_through_event_occurrence_identity": source.identity,
    }
    assert recorded["locality_relation"] == {
        "first_subject": source_reference,
        "second_subject": destination,
        "relation_occurrence_identity": recorded[
            "locality_relation_occurrence_identity"
        ],
    }
    assert recorded["locality_relation_occurrence_identity"] not in {
        recorded["continuation_act_identity"],
        recorded["act_occurrence_identity"],
        recorded["result_identity"],
    }
    assert recorded["result_identity"] == assignment.material[
        "result_boundary_identity"
    ]
    assert result.identity not in {
        recorded["result_identity"],
        recorded["continuation_act_identity"],
        recorded["act_occurrence_identity"],
        recorded["locality_relation_occurrence_identity"],
        assignment.identity,
        assignment.material["assignment_identity"],
        assignment.material["assignment_subject_identity"],
    }
    assert recorded["standing"] == "preserved"
    assert recorded["responsibility_assignment_reference"] == assignment_reference
    assert "applicability" not in recorded
    assert "priority" not in recorded
    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        yield_relation_event_identity=result.material["yield_relation_identity"],
        act_occurrence_event_identity=act_occurrence.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": True,
    }

    carried = advance_operator_locality_standing(
        ledger,
        (result.material["yield_relation_identity"], result.identity),
        locality_identity=destination,
        prior=after_act,
    )
    replayed = read_operator_locality_standing(
        ledger, locality_identity=destination
    )
    assert carried == replayed
    assert replayed["recorded_relation_Standing"] == {result.identity: None}
    assert replayed["responsibility_assignment_occurrences"] == {
        assignment.identity: None
    }
    assert replayed["material_acquisition_result_occurrences"] == []
    assert replayed["measurement_occurrences"] == {}
    assert replayed["exact_result_occurrences"] == {
        result.identity: assignment_reference,
    }


def test_assignment_survives_without_an_act_and_one_later_cut_can_carry_it(
    tmp_path,
):
    path = tmp_path / "continuation.sqlite"
    ledger = SQLiteEventLedger(str(path))
    _source, boundary = _source_boundary(ledger)
    assignment = _assignment(ledger, boundary)
    destination = assignment.locality_identity

    assert [
        event.kind for event in ledger.list_locality(destination)
    ] == [STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND]
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    assignment_standing = read_operator_locality_standing(
        ledger, locality_identity=destination
    )
    assert assignment_standing["responsibility_assignment_occurrences"] == {
        assignment.identity: None
    }
    assert assignment_standing["recorded_relation_Standing"] == {}
    boundary_after_assignment = record_operator_boundary(
        ledger,
        locality_identity=destination,
        locality_standing=assignment_standing,
    )
    carried_assignment_standing = read_operator_locality_standing(
        ledger, locality_identity=destination
    )

    act_occurrence = record_standing_locality_continuation_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=carried_assignment_standing,
    )

    assert boundary_after_assignment[
        "locality_standing_through_event_occurrence_identity"
    ] == assignment.identity
    assert act_occurrence.locality_identity == destination
    assert act_occurrence.material["responsibility_assignment_reference"][
        "recorded_occurrence_identity"
    ] == assignment.identity


def test_act_refuses_an_assignment_that_its_supplied_standing_does_not_carry():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    assignment = _assignment(ledger, boundary)
    source_standing = read_operator_locality_standing(
        ledger, locality_identity="source"
    )

    with pytest.raises(
        StandingLocalityContinuationError, match="prior carried assignment"
    ):
        record_standing_locality_continuation_act_occurrence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=source_standing,
        )


def test_durable_continuation_material_contains_no_operator_shorthand():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    record_standing_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    durable = repr(
        [
            (event.kind, event.material)
            for event in ledger.list_locality(act_occurrence.locality_identity)
        ]
    ).lower()

    for shorthand in ("memory", "important", "command", "cut"):
        assert shorthand not in durable


def test_later_source_occurrences_do_not_move_the_exact_source_cut():
    ledger = EventLedger()
    source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    later = record_witness_material_acquisition(
        ledger,
        locality_identity="source",
        exact_bytes=b"later",
        source_boundary="fixture boundary",
    )

    result = record_standing_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    reference = get_recorded_standing_locality_continuation(
        ledger, result.identity
    )["source_standing_reference"]

    assert reference["source_standing_through_event_occurrence_identity"] == source.identity
    assert reference["source_standing_through_event_occurrence_identity"] != later.identity


def test_exact_empty_source_boundary_remains_empty():
    ledger = EventLedger()
    boundary = record_operator_boundary(
        ledger,
        locality_identity="empty-source",
        locality_standing={"through_event_occurrence_identity": None},
    )
    act_occurrence = _act(
        ledger,
        boundary,
        source_locality_identity="empty-source",
    )
    result = record_standing_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )

    assert get_recorded_standing_locality_continuation(
        ledger, result.identity
    )["source_standing_reference"] == {
        "source_locality_identity": "empty-source",
        "source_standing_through_event_occurrence_identity": None,
        "addressed_boundary_event_identity": boundary[
            "boundary_event_identity"
        ],
    }


def test_continuation_is_direct_and_does_not_carry_an_earlier_relation():
    ledger = EventLedger()
    _source, first_boundary = _source_boundary(ledger, "a")
    first_act = _act(
        ledger, first_boundary, source_locality_identity="a"
    )
    first_result = record_standing_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=first_act.identity,
    )
    first_recorded = get_recorded_standing_locality_continuation(
        ledger, first_result.identity
    )
    first_destination = first_result.locality_identity
    first_standing = read_operator_locality_standing(
        ledger, locality_identity=first_destination
    )
    second_source_boundary = record_operator_boundary(
        ledger,
        locality_identity=first_destination,
        locality_standing=first_standing,
    )
    second_act = _act(
        ledger,
        second_source_boundary,
        source_locality_identity=first_destination,
    )
    second_result = record_standing_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=second_act.identity,
    )
    second_recorded = get_recorded_standing_locality_continuation(
        ledger, second_result.identity
    )

    assert second_recorded["source_standing_reference"] == {
        "source_locality_identity": first_destination,
        "source_standing_through_event_occurrence_identity": first_result.identity,
        "addressed_boundary_event_identity": second_source_boundary[
            "boundary_event_identity"
        ],
    }
    first_source_boundary = first_recorded["source_standing_reference"][
        "addressed_boundary_event_identity"
    ]
    assert first_source_boundary not in repr(second_recorded)
    assert read_operator_locality_standing(
        ledger, locality_identity=second_result.locality_identity
    )["recorded_relation_Standing"] == {second_result.identity: None}


def test_one_continuation_act_cannot_yield_or_record_twice():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    record_standing_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )

    with pytest.raises(
        StandingLocalityContinuationError, match="already carries a Yield"
    ):
        record_standing_locality_continuation_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
        )


def test_missing_different_or_changed_source_coordinates_are_refused():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)

    with pytest.raises(
        StandingLocalityContinuationError, match="different source Locality"
    ):
        _act(ledger, boundary, source_locality_identity="other")
    with pytest.raises(
        StandingLocalityContinuationError, match="intact addressed Standing boundary"
    ):
        record_standing_locality_continuation_responsibility_assignment(
            ledger,
            source_locality_identity="source",
            addressed_boundary_event_identity="missing",
        )

    act_occurrence = _act(ledger, boundary)
    changed = ledger.get(act_occurrence.identity)
    changed.material["source_standing_reference"] = {
        **changed.material["source_standing_reference"],
        "source_standing_through_event_occurrence_identity": "missing-cut",
    }
    with pytest.raises(
        StandingLocalityContinuationError,
        match="intact Act occurrence|source boundary",
    ):
        record_standing_locality_continuation_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "source_standing_reference",
        "destination_locality_identity",
        "participation",
        "locality_relation",
        "act_occurrence_identity",
        "locality_relation_occurrence_identity",
        "responsibility_assignment_reference",
        "act_occurrence_identity",
        "yield_relation_identity",
    ),
)
def test_changed_result_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    result = record_standing_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    changed = ledger.get(result.identity)
    changed.material[coordinate] = "different"

    with pytest.raises(StandingLocalityContinuationError):
        get_recorded_standing_locality_continuation(ledger, result.identity)


def test_equal_source_cuts_keep_distinct_occurrences_and_destinations():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    first_act = _act(ledger, boundary)
    second_act = _act(ledger, boundary)
    first = record_standing_locality_continuation_result(
        ledger, act_occurrence_event_identity=first_act.identity
    )
    second = record_standing_locality_continuation_result(
        ledger, act_occurrence_event_identity=second_act.identity
    )

    assert first_act.identity != second_act.identity
    assert first.locality_identity != second.locality_identity
    assert first.material["act_occurrence_identity"] != second.material[
        "act_occurrence_identity"
    ]
    assert first.material["locality_relation_occurrence_identity"] != second.material[
        "locality_relation_occurrence_identity"
    ]
    assert first.material["result_identity"] != second.material["result_identity"]
    assert first.material["yield_relation_identity"] != second.material[
        "yield_relation_identity"
    ]


def test_incomplete_act_occurrence_is_not_carried_as_a_relation():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)

    standing = read_operator_locality_standing(
        ledger, locality_identity=act_occurrence.locality_identity
    )

    assert standing["recorded_relation_Standing"] == {}
    assignment_identity = act_occurrence.material[
        "responsibility_assignment_reference"
    ]["recorded_occurrence_identity"]
    assert standing["responsibility_assignment_occurrences"] == {
        assignment_identity: None
    }
    assert standing["through_event_occurrence_identity"] == act_occurrence.identity


def test_prior_relation_carrier_must_remain_one_identity_dictionary():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    result = record_standing_locality_continuation_result(
        ledger, act_occurrence_event_identity=act_occurrence.identity
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=result.locality_identity
    )
    broken = deepcopy(standing)
    broken["recorded_relation_Standing"] = [result.identity]

    with pytest.raises(
        ValueError, match="exact recorded relation occurrences"
    ):
        advance_operator_locality_standing(
            ledger,
            (),
            locality_identity=result.locality_identity,
            prior=broken,
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "book_clause_identity",
        "responsible_boundary",
        "source_standing_reference",
        "destination_locality_identity",
        "standing_boundary_occurrence_reference",
        "scope",
        "result_boundary_identity",
        "standing",
        "limits",
        "unknown",
    ),
)
def test_changed_responsibility_assignment_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    assignment_identity = act_occurrence.material[
        "responsibility_assignment_reference"
    ]["recorded_occurrence_identity"]
    assignment = ledger.get(assignment_identity)
    assignment.material[coordinate] = "different"

    with pytest.raises(StandingLocalityContinuationError):
        record_standing_locality_continuation_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
        )


def test_act_occurrence_cannot_cite_another_exact_assignment():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    first = _act(ledger, boundary)
    second = _act(ledger, boundary)
    changed = ledger.get(first.identity)
    changed.material["responsibility_assignment_reference"] = dict(
        second.material["responsibility_assignment_reference"]
    )

    with pytest.raises(StandingLocalityContinuationError):
        record_standing_locality_continuation_result(
            ledger,
            act_occurrence_event_identity=first.identity,
        )


PYTEST_ADMISSION = (
    test_three_stage_continuation_records_exact_direct_relation_without_copying_standing,
    test_assignment_survives_without_an_act_and_one_later_cut_can_carry_it,
    test_act_refuses_an_assignment_that_its_supplied_standing_does_not_carry,
    test_durable_continuation_material_contains_no_operator_shorthand,
    test_later_source_occurrences_do_not_move_the_exact_source_cut,
    test_exact_empty_source_boundary_remains_empty,
    test_continuation_is_direct_and_does_not_carry_an_earlier_relation,
    test_one_continuation_act_cannot_yield_or_record_twice,
    test_missing_different_or_changed_source_coordinates_are_refused,
    test_changed_result_coordinates_are_refused,
    test_equal_source_cuts_keep_distinct_occurrences_and_destinations,
    test_incomplete_act_occurrence_is_not_carried_as_a_relation,
    test_prior_relation_carrier_must_remain_one_identity_dictionary,
    test_changed_responsibility_assignment_coordinates_are_refused,
    test_act_occurrence_cannot_cite_another_exact_assignment,
)
