from __future__ import annotations

import pytest


from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_source import exact_material_result_bytes
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_invocation_locality import (
    OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT,
    OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND,
    OPERATOR_INVOCATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    OperatorInvocationLocalityError,
    get_operator_invocation_locality_act_occurrence,
    get_operator_invocation_locality_subject_to_act_binding,
    get_recorded_operator_invocation_locality,
    operator_invocation_locality_occurrence_references,
    record_operator_invocation_locality_act_occurrence,
    record_operator_invocation_locality_subject_to_act_binding,
    record_operator_invocation_locality_result,
)
from seed_runtime.supplied_invocation_material import (
    SuppliedWitnessMaterialOccurrence,
    record_supplied_witness_material_source,
)


def _command(ledger, *, exact=b"!pytest\n", locality="operator"):
    return record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
    )


def _relation(ledger, command):
    binding = record_operator_invocation_locality_subject_to_act_binding(
        ledger,
        operator_material_occurrence_reference=command.identity,
        current_coordinates=read_operator_locality_standing(
            ledger, locality_identity=command.locality_identity
        ),
    )
    act = record_operator_invocation_locality_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=read_operator_locality_standing(
            ledger, locality_identity=binding.locality_identity
        ),
    )
    result = record_operator_invocation_locality_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    return binding, act, result


def test_operator_occurrence_establishes_one_fresh_direct_locality_relation():
    ledger = EventLedger()
    command = _command(ledger)
    binding, act, result = _relation(ledger, command)
    recorded = get_recorded_operator_invocation_locality(ledger, result.identity)

    assert binding.kind == (
        OPERATOR_INVOCATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    )
    assert binding.locality_identity == recorded[
        "destination_locality_identity"
    ]
    assert act.kind == OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT
    assert result.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
    assert act.locality_identity == result.locality_identity
    assert act.locality_identity == binding.locality_identity
    assert act.locality_identity != "operator"
    assert recorded["operator_material_occurrence_reference"] == command.identity
    assert recorded["locality_relation"] == {
        "first_subject": "operator",
        "second_subject": result.locality_identity,
        "relation_occurrence_identity": recorded[
            "relation_occurrence_identity"
        ],
    }
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
    binding, _act, relation = _relation(ledger, command)
    supplied = record_supplied_witness_material_source(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"one selected log line\n",
            "invocation output occurrence 0",
        ),
    )

    assert supplied.locality_identity == relation.locality_identity
    assert exact_material_result_bytes(supplied) == b"one selected log line\n"
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
    assert binding.identity not in operator_standing[
        "subject_to_act_binding_occurrences"
    ]
    assert [
        occurrence["result_occurrence_identity"]
        for occurrence in witness_standing["material_acquisition_result_occurrences"]
    ] == [supplied.identity]
    assert witness_standing["operator_invocation_locality_relations"] == {
        relation.identity: None
    }
    assert witness_standing["subject_to_act_binding_occurrences"] == {
        binding.identity: None
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
        record_operator_invocation_locality_subject_to_act_binding(
            ledger,
            operator_material_occurrence_reference=command.identity,
            current_coordinates=read_operator_locality_standing(
                ledger, locality_identity="operator"
            ),
        )


def test_binding_requires_a_carried_exact_operator_invocation():
    ledger = EventLedger()
    command = _command(ledger)
    empty_coordinates = read_operator_locality_standing(
        ledger, locality_identity="other"
    )
    with pytest.raises(
        OperatorInvocationLocalityError,
        match="current operator material coordinates",
    ):
        record_operator_invocation_locality_subject_to_act_binding(
            ledger,
            operator_material_occurrence_reference=command.identity,
            current_coordinates=empty_coordinates,
        )

    not_invocation = _command(ledger, exact=b"pytest\n")
    with pytest.raises(OperatorInvocationLocalityError, match="material occurrence"):
        record_operator_invocation_locality_subject_to_act_binding(
            ledger,
            operator_material_occurrence_reference=not_invocation.identity,
            current_coordinates=read_operator_locality_standing(
                ledger, locality_identity="operator"
            ),
        )


def test_one_invocation_locality_act_cannot_yield_twice():
    ledger = EventLedger()
    command = _command(ledger)
    binding = record_operator_invocation_locality_subject_to_act_binding(
        ledger,
        operator_material_occurrence_reference=command.identity,
        current_coordinates=read_operator_locality_standing(
            ledger, locality_identity="operator"
        ),
    )
    act = record_operator_invocation_locality_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=read_operator_locality_standing(
            ledger, locality_identity=binding.locality_identity
        ),
    )
    record_operator_invocation_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    with pytest.raises(OperatorInvocationLocalityError, match="already carries a Yield"):
        record_operator_invocation_locality_result(
            ledger, act_occurrence_event_identity=act.identity
        )


def test_corrupted_binding_act_and_result_are_refused_independently():
    for coordinate in ("binding", "act", "result"):
        ledger = EventLedger()
        binding, act, result = _relation(ledger, _command(ledger))
        event = {"binding": binding, "act": act, "result": result}[
            coordinate
        ]
        event.material["unknown"] = ["crossed"]
        reader, identity = {
            "binding": (
                get_operator_invocation_locality_subject_to_act_binding,
                binding.identity,
            ),
            "act": (get_operator_invocation_locality_act_occurrence, act.identity),
            "result": (get_recorded_operator_invocation_locality, result.identity),
        }[coordinate]
        with pytest.raises(OperatorInvocationLocalityError):
            reader(ledger, identity)


def test_invocation_locality_act_requires_binding_in_current_destination_coordinates():
    ledger = EventLedger()
    command = _command(ledger)
    binding = record_operator_invocation_locality_subject_to_act_binding(
        ledger,
        operator_material_occurrence_reference=command.identity,
        current_coordinates=read_operator_locality_standing(
            ledger, locality_identity="operator"
        ),
    )
    destination_coordinates_without_binding = {
        **read_operator_locality_standing(
            ledger, locality_identity=binding.locality_identity
        ),
        "subject_to_act_binding_occurrences": {},
    }

    for current_coordinates in (
        read_operator_locality_standing(ledger, locality_identity="operator"),
        destination_coordinates_without_binding,
    ):
        with pytest.raises(OperatorInvocationLocalityError, match="carried binding"):
            record_operator_invocation_locality_act_occurrence(
                ledger,
                subject_to_act_binding_event_identity=binding.identity,
                current_coordinates=current_coordinates,
            )


def test_carried_witness_standing_equals_full_replay():
    ledger = EventLedger()
    command = _command(ledger)
    binding, act, relation = _relation(ledger, command)
    locality = relation.locality_identity
    carried = advance_operator_locality_standing(
        ledger,
        (
            binding.identity,
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
    _binding, _act, relation = _relation(ledger, command)
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
