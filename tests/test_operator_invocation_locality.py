from __future__ import annotations

import pytest


from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_acquisition import acquired_material_bytes
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_invocation_locality import (
    OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT,
    OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND,
    OPERATOR_INVOCATION_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OperatorInvocationLocalityError,
    get_operator_invocation_locality_act_occurrence,
    get_operator_invocation_locality_responsibility_assignment,
    get_recorded_operator_invocation_locality,
    operator_invocation_locality_occurrence_references,
    record_operator_invocation_locality_act_occurrence,
    record_operator_invocation_locality_responsibility_assignment,
    record_operator_invocation_locality_result,
)
from seed_runtime.supplied_invocation_material import (
    SuppliedWitnessMaterialOccurrence,
    acquire_supplied_witness_material_occurrence,
)


def _command(ledger, *, exact=b"!pytest\n", locality="operator"):
    return record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
    )


def _relation(ledger, command):
    assignment = record_operator_invocation_locality_responsibility_assignment(
        ledger,
        operator_material_occurrence_reference=command.identity,
        operator_locality_standing=read_operator_locality_standing(
            ledger, locality_identity=command.locality_identity
        ),
    )
    act = record_operator_invocation_locality_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=assignment.locality_identity
        ),
    )
    result = record_operator_invocation_locality_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    return assignment, act, result


def test_operator_authority_establishes_one_fresh_direct_locality_relation():
    ledger = EventLedger()
    command = _command(ledger)
    assignment, act, result = _relation(ledger, command)
    recorded = get_recorded_operator_invocation_locality(ledger, result.identity)

    assert assignment.kind == (
        OPERATOR_INVOCATION_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    )
    assert assignment.locality_identity == recorded[
        "destination_locality_identity"
    ]
    assert act.kind == OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT
    assert result.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
    assert act.locality_identity == result.locality_identity
    assert act.locality_identity == assignment.locality_identity
    assert act.locality_identity != "operator"
    assert recorded["operator_material_occurrence_reference"] == command.identity
    assert recorded["locality_relation"] == {
        "first_subject": "operator",
        "second_subject": result.locality_identity,
        "relation_occurrence_identity": recorded[
            "relation_occurrence_identity"
        ],
    }
    assert recorded["negative_authority"] == [
        "the relation carries no operator Standing into the destination Locality",
        "the relation establishes no enclosure or hierarchy",
    ]
    assert operator_invocation_locality_occurrence_references(
        ledger, result.identity
    ) == (
        act.identity,
        result.material["yield_relation_identity"],
        result.identity,
    )


def test_witness_material_occurs_only_in_the_related_locality():
    ledger = EventLedger()
    command = _command(ledger)
    assignment, _act, relation = _relation(ledger, command)
    supplied = acquire_supplied_witness_material_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"one selected log line\n",
            "invocation output occurrence 0",
        ),
    )

    assert supplied.locality_identity == relation.locality_identity
    assert acquired_material_bytes(supplied) == b"one selected log line\n"
    assert supplied.material["provenance_occurrence_references"] == [
        command.identity,
        relation.identity,
    ]
    operator_standing = read_operator_locality_standing(
        ledger, locality_identity="operator"
    )
    witness_standing = read_operator_locality_standing(
        ledger, locality_identity=relation.locality_identity
    )
    assert [
        occurrence["result_occurrence_identity"]
        for occurrence in operator_standing["material_acquisition_result_occurrences"]
    ] == [command.identity]
    assert operator_standing["operator_invocation_locality_relations"] == {}
    assert assignment.identity not in operator_standing[
        "responsibility_assignment_occurrences"
    ]
    assert [
        occurrence["result_occurrence_identity"]
        for occurrence in witness_standing["material_acquisition_result_occurrences"]
    ] == [supplied.identity]
    assert witness_standing["operator_invocation_locality_relations"] == {
        relation.identity: None
    }
    assert witness_standing["responsibility_assignment_occurrences"] == {
        assignment.identity: None
    }


def test_each_operator_occurrence_establishes_distinct_relation_identities():
    ledger = EventLedger()
    first = _relation(ledger, _command(ledger))[2]
    second = _relation(ledger, _command(ledger))[2]

    first_recorded = get_recorded_operator_invocation_locality(ledger, first.identity)
    second_recorded = get_recorded_operator_invocation_locality(
        ledger, second.identity
    )
    coordinates = (
        "result_identity",
        "operator_invocation_locality_act_identity",
        "act_occurrence_identity",
        "relation_occurrence_identity",
        "destination_locality_identity",
    )
    assert all(
        first_recorded[coordinate] != second_recorded[coordinate]
        for coordinate in coordinates
    )


def test_one_operator_occurrence_cannot_assign_two_invocation_localities():
    ledger = EventLedger()
    command = _command(ledger)
    _relation(ledger, command)
    with pytest.raises(OperatorInvocationLocalityError, match="already carries"):
        record_operator_invocation_locality_responsibility_assignment(
            ledger,
            operator_material_occurrence_reference=command.identity,
            operator_locality_standing=read_operator_locality_standing(
                ledger, locality_identity="operator"
            ),
        )


def test_assignment_requires_a_carried_exact_operator_invocation():
    ledger = EventLedger()
    command = _command(ledger)
    empty_standing = read_operator_locality_standing(
        ledger, locality_identity="other"
    )
    with pytest.raises(OperatorInvocationLocalityError, match="material Standing"):
        record_operator_invocation_locality_responsibility_assignment(
            ledger,
            operator_material_occurrence_reference=command.identity,
            operator_locality_standing=empty_standing,
        )

    not_invocation = _command(ledger, exact=b"pytest\n")
    with pytest.raises(OperatorInvocationLocalityError, match="material occurrence"):
        record_operator_invocation_locality_responsibility_assignment(
            ledger,
            operator_material_occurrence_reference=not_invocation.identity,
            operator_locality_standing=read_operator_locality_standing(
                ledger, locality_identity="operator"
            ),
        )


def test_one_invocation_locality_act_cannot_yield_twice():
    ledger = EventLedger()
    command = _command(ledger)
    assignment = record_operator_invocation_locality_responsibility_assignment(
        ledger,
        operator_material_occurrence_reference=command.identity,
        operator_locality_standing=read_operator_locality_standing(
            ledger, locality_identity="operator"
        ),
    )
    act = record_operator_invocation_locality_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=assignment.locality_identity
        ),
    )
    record_operator_invocation_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    with pytest.raises(OperatorInvocationLocalityError, match="already carries a Yield"):
        record_operator_invocation_locality_result(
            ledger, act_occurrence_event_identity=act.identity
        )


def test_corrupted_assignment_act_and_result_are_refused_independently():
    for coordinate in ("assignment", "act", "result"):
        ledger = EventLedger()
        assignment, act, result = _relation(ledger, _command(ledger))
        event = {"assignment": assignment, "act": act, "result": result}[
            coordinate
        ]
        event.material["unknown"] = ["crossed"]
        reader, identity = {
            "assignment": (
                get_operator_invocation_locality_responsibility_assignment,
                assignment.identity,
            ),
            "act": (get_operator_invocation_locality_act_occurrence, act.identity),
            "result": (get_recorded_operator_invocation_locality, result.identity),
        }[coordinate]
        with pytest.raises(OperatorInvocationLocalityError):
            reader(ledger, identity)


def test_invocation_locality_act_requires_assignment_standing_in_destination():
    ledger = EventLedger()
    command = _command(ledger)
    assignment = record_operator_invocation_locality_responsibility_assignment(
        ledger,
        operator_material_occurrence_reference=command.identity,
        operator_locality_standing=read_operator_locality_standing(
            ledger, locality_identity="operator"
        ),
    )
    destination_standing_without_assignment = {
        **read_operator_locality_standing(
            ledger, locality_identity=assignment.locality_identity
        ),
        "responsibility_assignment_occurrences": {},
    }

    for standing in (
        read_operator_locality_standing(ledger, locality_identity="operator"),
        destination_standing_without_assignment,
    ):
        with pytest.raises(OperatorInvocationLocalityError, match="carried assignment"):
            record_operator_invocation_locality_act_occurrence(
                ledger,
                responsibility_assignment_event_identity=assignment.identity,
                responsibility_assignment_standing=standing,
            )


def test_carried_witness_standing_equals_full_replay():
    ledger = EventLedger()
    command = _command(ledger)
    _assignment, act, relation = _relation(ledger, command)
    locality = relation.locality_identity
    carried = advance_operator_locality_standing(
        ledger,
        (
            _assignment.identity,
            act.identity,
            relation.material["yield_relation_identity"],
            relation.identity,
        ),
        locality_identity=locality,
    )
    assert carried == read_operator_locality_standing(
        ledger, locality_identity=locality
    )


def test_invocation_locality_relation_reopens_with_exact_standing(tmp_path):
    database = tmp_path / "operator-invocation-locality.db"
    ledger = SQLiteEventLedger(database)
    command = _command(ledger)
    _assignment, _act, relation = _relation(ledger, command)
    locality = relation.locality_identity
    relation_identity = relation.identity
    ledger.close()

    reopened = SQLiteEventLedger(database)
    try:
        recorded = get_recorded_operator_invocation_locality(
            reopened, relation_identity
        )
        standing = read_operator_locality_standing(
            reopened, locality_identity=locality
        )
    finally:
        reopened.close()

    assert recorded["destination_locality_identity"] == locality
    assert standing["operator_invocation_locality_relations"] == {
        relation_identity: None
    }


PYTEST_ADMISSION = (
    test_operator_authority_establishes_one_fresh_direct_locality_relation,
    test_witness_material_occurs_only_in_the_related_locality,
    test_each_operator_occurrence_establishes_distinct_relation_identities,
    test_one_operator_occurrence_cannot_assign_two_invocation_localities,
    test_assignment_requires_a_carried_exact_operator_invocation,
    test_one_invocation_locality_act_cannot_yield_twice,
    test_corrupted_assignment_act_and_result_are_refused_independently,
    test_invocation_locality_act_requires_assignment_standing_in_destination,
    test_carried_witness_standing_equals_full_replay,
    test_invocation_locality_relation_reopens_with_exact_standing,
)
