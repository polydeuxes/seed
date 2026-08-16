from __future__ import annotations

from copy import deepcopy

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_ingest import ingest_material
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_representation import record_operator_representation
from seed_runtime.operator_standing_continuation import (
    STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND,
    STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
    STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    StandingLocalityContinuationError,
    get_recorded_standing_locality_continuation,
    get_standing_locality_continuation_responsibility_assignment,
    record_standing_locality_continuation_responsibility_assignment,
    record_standing_locality_continuation_responsible_act_evidence,
    record_standing_locality_continuation_result,
)
from seed_runtime.evidence_of_yield_relation import read_requirements_of_yield_relation


def _source_representation(
    ledger: EventLedger, locality_identity: str = "source"
) -> tuple[object, dict]:
    source = ingest_material(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"\x00\xffprior\n",
        source_role="fixture material",
        source_boundary="fixture boundary",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    representation = record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=standing,
    )
    return source, representation


def _assignment(
    ledger: EventLedger,
    representation: dict,
    *,
    source_locality_identity: str = "source",
):
    return record_standing_locality_continuation_responsibility_assignment(
        ledger,
        source_locality_identity=source_locality_identity,
        addressed_representation_event_identity=representation[
            "representation_event_identity"
        ],
    )


def _act(
    ledger: EventLedger,
    representation: dict,
    *,
    source_locality_identity: str = "source",
):
    assignment = _assignment(
        ledger,
        representation,
        source_locality_identity=source_locality_identity,
    )
    assignment_standing = read_operator_locality_standing(
        ledger, locality_identity=assignment.locality_identity
    )
    return record_standing_locality_continuation_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=assignment_standing,
    )


def test_three_stage_continuation_records_exact_direct_relation_without_copying_standing():
    ledger = EventLedger()
    source, representation = _source_representation(ledger)

    act_evidence = _act(ledger, representation)
    destination = act_evidence.locality_identity
    assignment_reference = act_evidence.material[
        "responsibility_assignment_reference"
    ]
    assignment = get_standing_locality_continuation_responsibility_assignment(
        ledger, assignment_reference["recorded_occurrence_identity"]
    )
    after_act = read_operator_locality_standing(
        ledger, locality_identity=destination
    )

    assert act_evidence.kind == STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND
    assert destination != "source"
    assert act_evidence.exact_material is None
    assert assignment.kind == (
        STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    )
    assert assignment.locality_identity == destination
    assert assignment.material["book_clause_identity"] == "06.Locality.B"
    assert assignment.material["standing"] == "assigned"
    assert assignment.material["evidence_occurrence_reference"] == representation[
        "representation_event_identity"
    ]
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
            act_evidence.material["continuation_act_identity"],
            act_evidence.material["act_occurrence_identity"],
            act_evidence.material["locality_relation_occurrence_identity"],
        }
    ) == 7
    assert after_act["event_count"] == 2
    assert after_act["recorded_relation_standings"] == {}
    assert after_act["responsibility_assignment_occurrences"] == {
        assignment.identity: None
    }
    assert after_act["ingest_occurrences"] == []
    assert after_act["measurement_occurrences"] == {}
    assert after_act["exact_result_occurrences"] == {}
    assert after_act["representations"] == {}

    result = record_standing_locality_continuation_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    recorded = get_recorded_standing_locality_continuation(
        ledger, result.identity
    )
    source_reference = recorded["source_standing_reference"]

    assert result.kind == STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
    assert result.exact_material is None
    assert source_reference == {
        "source_locality_identity": "source",
        "source_standing_as_of_event_identity": source.identity,
        "addressed_representation_event_identity": representation[
            "representation_event_identity"
        ],
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
        evidence_of_yield_relation_event_identity=result.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=act_evidence.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }

    incremental = advance_operator_locality_standing(
        ledger,
        (result.material["evidence_of_yield_relation_identity"], result.identity),
        locality_identity=destination,
        prior=after_act,
    )
    replayed = read_operator_locality_standing(
        ledger, locality_identity=destination
    )
    assert incremental == replayed
    assert replayed["recorded_relation_standings"] == {result.identity: None}
    assert replayed["responsibility_assignment_occurrences"] == {
        assignment.identity: None
    }
    assert replayed["ingest_occurrences"] == []
    assert replayed["measurement_occurrences"] == {}
    assert replayed["exact_result_occurrences"] == {}
    assert replayed["representations"] == {}


def test_assignment_survives_without_an_act_and_one_later_cut_can_carry_it(
    tmp_path,
):
    path = tmp_path / "continuation.sqlite"
    ledger = SQLiteEventLedger(str(path))
    _source, representation = _source_representation(ledger)
    assignment = _assignment(ledger, representation)
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
    assert assignment_standing["recorded_relation_standings"] == {}
    representation_after_assignment = record_operator_representation(
        ledger,
        locality_identity=destination,
        locality_standing=assignment_standing,
    )
    carried_assignment_standing = read_operator_locality_standing(
        ledger, locality_identity=destination
    )

    act_evidence = record_standing_locality_continuation_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=carried_assignment_standing,
    )

    assert representation_after_assignment[
        "locality_standing_as_of_event_identity"
    ] == assignment.identity
    assert act_evidence.locality_identity == destination
    assert act_evidence.material["responsibility_assignment_reference"][
        "recorded_occurrence_identity"
    ] == assignment.identity


def test_act_refuses_an_assignment_that_its_supplied_standing_does_not_carry():
    ledger = EventLedger()
    _source, representation = _source_representation(ledger)
    assignment = _assignment(ledger, representation)
    source_standing = read_operator_locality_standing(
        ledger, locality_identity="source"
    )

    with pytest.raises(
        StandingLocalityContinuationError, match="prior carried assignment"
    ):
        record_standing_locality_continuation_responsible_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=source_standing,
        )


def test_durable_continuation_material_contains_no_operator_shorthand():
    ledger = EventLedger()
    _source, representation = _source_representation(ledger)
    act_evidence = _act(ledger, representation)
    record_standing_locality_continuation_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    durable = repr(
        [
            (event.kind, event.material)
            for event in ledger.list_locality(act_evidence.locality_identity)
        ]
    ).lower()

    for shorthand in ("memory", "important", "command", "cut"):
        assert shorthand not in durable


def test_later_source_occurrences_do_not_move_the_exact_source_cut():
    ledger = EventLedger()
    source, representation = _source_representation(ledger)
    act_evidence = _act(ledger, representation)
    later = ingest_material(
        ledger,
        locality_identity="source",
        exact_bytes=b"later",
        source_role="fixture material",
        source_boundary="fixture boundary",
    )

    result = record_standing_locality_continuation_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    reference = get_recorded_standing_locality_continuation(
        ledger, result.identity
    )["source_standing_reference"]

    assert reference["source_standing_as_of_event_identity"] == source.identity
    assert reference["source_standing_as_of_event_identity"] != later.identity


def test_exact_empty_source_boundary_remains_empty():
    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="empty-source",
        locality_standing={"as_of_event_identity": None},
    )
    act_evidence = _act(
        ledger,
        representation,
        source_locality_identity="empty-source",
    )
    result = record_standing_locality_continuation_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )

    assert get_recorded_standing_locality_continuation(
        ledger, result.identity
    )["source_standing_reference"] == {
        "source_locality_identity": "empty-source",
        "source_standing_as_of_event_identity": None,
        "addressed_representation_event_identity": representation[
            "representation_event_identity"
        ],
    }


def test_continuation_is_direct_and_does_not_carry_an_earlier_relation():
    ledger = EventLedger()
    _source, first_representation = _source_representation(ledger, "a")
    first_act = _act(
        ledger, first_representation, source_locality_identity="a"
    )
    first_result = record_standing_locality_continuation_result(
        ledger,
        responsible_act_evidence_event_identity=first_act.identity,
    )
    first_recorded = get_recorded_standing_locality_continuation(
        ledger, first_result.identity
    )
    first_destination = first_result.locality_identity
    first_standing = read_operator_locality_standing(
        ledger, locality_identity=first_destination
    )
    second_source_representation = record_operator_representation(
        ledger,
        locality_identity=first_destination,
        locality_standing=first_standing,
    )
    second_act = _act(
        ledger,
        second_source_representation,
        source_locality_identity=first_destination,
    )
    second_result = record_standing_locality_continuation_result(
        ledger,
        responsible_act_evidence_event_identity=second_act.identity,
    )
    second_recorded = get_recorded_standing_locality_continuation(
        ledger, second_result.identity
    )

    assert second_recorded["source_standing_reference"] == {
        "source_locality_identity": first_destination,
        "source_standing_as_of_event_identity": first_result.identity,
        "addressed_representation_event_identity": second_source_representation[
            "representation_event_identity"
        ],
    }
    first_source_representation = first_recorded["source_standing_reference"][
        "addressed_representation_event_identity"
    ]
    assert first_source_representation not in repr(second_recorded)
    assert read_operator_locality_standing(
        ledger, locality_identity=second_result.locality_identity
    )["recorded_relation_standings"] == {second_result.identity: None}


def test_one_continuation_act_cannot_yield_or_record_twice():
    ledger = EventLedger()
    _source, representation = _source_representation(ledger)
    act_evidence = _act(ledger, representation)
    record_standing_locality_continuation_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )

    with pytest.raises(
        StandingLocalityContinuationError, match="already carries a Yield"
    ):
        record_standing_locality_continuation_result(
            ledger,
            responsible_act_evidence_event_identity=act_evidence.identity,
        )


def test_missing_different_or_changed_source_coordinates_are_refused():
    ledger = EventLedger()
    _source, representation = _source_representation(ledger)

    with pytest.raises(
        StandingLocalityContinuationError, match="different source Locality"
    ):
        _act(ledger, representation, source_locality_identity="other")
    with pytest.raises(
        StandingLocalityContinuationError, match="intact addressed Representation"
    ):
        record_standing_locality_continuation_responsibility_assignment(
            ledger,
            source_locality_identity="source",
            addressed_representation_event_identity="missing",
        )

    act_evidence = _act(ledger, representation)
    changed = ledger.get(act_evidence.identity)
    changed.material["source_standing_reference"] = {
        **changed.material["source_standing_reference"],
        "source_standing_as_of_event_identity": "missing-cut",
    }
    with pytest.raises(
        StandingLocalityContinuationError,
        match="intact Act Evidence|source boundary",
    ):
        record_standing_locality_continuation_result(
            ledger,
            responsible_act_evidence_event_identity=act_evidence.identity,
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
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    ),
)
def test_changed_result_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    _source, representation = _source_representation(ledger)
    act_evidence = _act(ledger, representation)
    result = record_standing_locality_continuation_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    changed = ledger.get(result.identity)
    changed.material[coordinate] = "different"

    with pytest.raises(StandingLocalityContinuationError):
        get_recorded_standing_locality_continuation(ledger, result.identity)


def test_equal_source_cuts_keep_distinct_occurrences_and_destinations():
    ledger = EventLedger()
    _source, representation = _source_representation(ledger)
    first_act = _act(ledger, representation)
    second_act = _act(ledger, representation)
    first = record_standing_locality_continuation_result(
        ledger, responsible_act_evidence_event_identity=first_act.identity
    )
    second = record_standing_locality_continuation_result(
        ledger, responsible_act_evidence_event_identity=second_act.identity
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
    assert first.material["evidence_of_yield_relation_identity"] != second.material[
        "evidence_of_yield_relation_identity"
    ]


def test_incomplete_act_evidence_is_not_projected_as_a_relation():
    ledger = EventLedger()
    _source, representation = _source_representation(ledger)
    act_evidence = _act(ledger, representation)

    standing = read_operator_locality_standing(
        ledger, locality_identity=act_evidence.locality_identity
    )

    assert standing["recorded_relation_standings"] == {}
    assignment_identity = act_evidence.material[
        "responsibility_assignment_reference"
    ]["recorded_occurrence_identity"]
    assert standing["responsibility_assignment_occurrences"] == {
        assignment_identity: None
    }
    assert standing["as_of_event_identity"] == act_evidence.identity


def test_prior_relation_carrier_must_remain_one_identity_dictionary():
    ledger = EventLedger()
    _source, representation = _source_representation(ledger)
    act_evidence = _act(ledger, representation)
    result = record_standing_locality_continuation_result(
        ledger, responsible_act_evidence_event_identity=act_evidence.identity
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=result.locality_identity
    )
    broken = deepcopy(standing)
    broken["recorded_relation_standings"] = [result.identity]

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
        "evidence_occurrence_reference",
        "authority",
        "scope",
        "result_boundary_identity",
        "standing",
        "limits",
        "unknowns",
    ),
)
def test_changed_responsibility_assignment_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    _source, representation = _source_representation(ledger)
    act_evidence = _act(ledger, representation)
    assignment_identity = act_evidence.material[
        "responsibility_assignment_reference"
    ]["recorded_occurrence_identity"]
    assignment = ledger.get(assignment_identity)
    assignment.material[coordinate] = "different"

    with pytest.raises(StandingLocalityContinuationError):
        record_standing_locality_continuation_result(
            ledger,
            responsible_act_evidence_event_identity=act_evidence.identity,
        )


def test_act_evidence_cannot_cite_another_exact_assignment():
    ledger = EventLedger()
    _source, representation = _source_representation(ledger)
    first = _act(ledger, representation)
    second = _act(ledger, representation)
    changed = ledger.get(first.identity)
    changed.material["responsibility_assignment_reference"] = dict(
        second.material["responsibility_assignment_reference"]
    )

    with pytest.raises(StandingLocalityContinuationError):
        record_standing_locality_continuation_result(
            ledger,
            responsible_act_evidence_event_identity=first.identity,
        )
