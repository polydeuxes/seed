"""Operator material: a Locality relation occurrence."""

from __future__ import annotations

import pytest


from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.material_source import exact_material_result_bytes
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.operator_destination_locality import (
    OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT,
    OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND,
    OperatorDestinationLocalityError,
    get_operator_destination_locality_act_occurrence,
    get_recorded_operator_destination_locality,
    operator_destination_locality_occurrence_references,
    record_operator_destination_locality_act_occurrence,
    record_operator_destination_locality_result,
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
    act = record_operator_destination_locality_act_occurrence(
        ledger,
        operator_material_occurrence_reference=command.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=command.locality_identity
        ),
    )
    result = record_operator_destination_locality_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    return act, result


def test_operator_occurrence_has_a_fresh_destination_locality_relation():
    ledger = EventLedger()
    command = _command(ledger)
    act, result = _relation(ledger, command)
    recorded = get_recorded_operator_destination_locality(ledger, result.identity)

    assert set(act.material) == {
        "act",
        "operator_material_occurrence_reference",
        "operator_through_event_occurrence_identity",
    }
    assert act.kind == OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT
    assert result.kind == OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND
    assert act.locality_identity == result.locality_identity
    assert act.locality_identity != "operator"
    assert all(
        "result_identity" not in occurrence.material
        for occurrence in (act, result)
    )
    assert all(
        "act_occurrence_identity" not in occurrence.material
        for occurrence in (act, result)
    )
    assert all(
        "operator_destination_locality_act_identity" not in occurrence.material
        for occurrence in (act, result)
    )
    assert all(
        "subject_to_act_binding_event_identity" not in occurrence.material
        for occurrence in (act, result)
    )
    assert "destination_locality_identity" not in act.material
    assert "operator_material_result_occurrence_identity" not in act.material
    assert "operator_locality_identity" not in act.material
    assert "exact_act" not in result.material
    assert "operator_material_occurrence_reference" not in result.material
    assert "operator_locality_identity" not in result.material
    assert "destination_locality_identity" not in result.material
    assert all(
        occurrence.kind
        != "operator.destination_locality_subject_to_act_binding_recorded"
        for occurrence in ledger.list_events()
    )
    assert recorded["operator_material_occurrence_reference"] == command.identity
    assert recorded["operator_locality_identity"] == "operator"
    assert recorded["destination_locality_identity"] == result.locality_identity
    assert "locality_relation" not in recorded
    assert operator_destination_locality_occurrence_references(
        ledger, result.identity
    ) == (
        act.identity,
        result.identity,
    )


def test_destination_locality_act_can_precede_its_result():
    ledger = EventLedger()
    command = _command(ledger)
    act = record_operator_destination_locality_act_occurrence(
        ledger,
        operator_material_occurrence_reference=command.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=command.locality_identity
        ),
    )

    assert get_operator_destination_locality_act_occurrence(
        ledger, act.identity
    ) == act
    assert not any(
        event.kind == OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND
        for event in ledger.list_events()
    )


def test_witness_material_occurs_only_in_the_related_locality():
    ledger = EventLedger()
    command = _command(ledger)
    _act, relation = _relation(ledger, command)
    supplied = record_supplied_witness_material_source(
        ledger,
        operator_destination_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"one selected log line\n",
            "invocation output occurrence 0",
        ),
    )

    assert supplied.locality_identity == relation.locality_identity
    assert exact_material_result_bytes(supplied) == b"one selected log line\n"
    assert supplied.material["source_occurrence_references"] == [
        command.identity,
        relation.identity,
    ]
    operator_current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity="operator"
    )
    destination_current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=relation.locality_identity
    )
    assert [
        occurrence["result_occurrence_identity"]
        for occurrence in operator_current_coordinates["material_result_occurrences"]
    ] == [command.identity]
    assert operator_current_coordinates["operator_destination_locality_relations"] == {}
    assert [
        occurrence["result_occurrence_identity"]
        for occurrence in destination_current_coordinates["material_result_occurrences"]
    ] == [supplied.identity]
    assert destination_current_coordinates["operator_destination_locality_relations"] == {
        relation.identity: None
    }
    assert destination_current_coordinates["subject_to_act_binding_occurrences"] == {}


def test_separate_operator_occurrences_have_separate_relation_results():
    ledger = EventLedger()
    first_act, first = _relation(ledger, _command(ledger))
    second_act, second = _relation(ledger, _command(ledger))

    first_recorded = get_recorded_operator_destination_locality(ledger, first.identity)
    second_recorded = get_recorded_operator_destination_locality(
        ledger, second.identity
    )
    assert first.identity != second.identity
    assert first_act.identity != second_act.identity
    assert "result_identity" not in first_recorded
    assert "result_identity" not in second_recorded
    assert "act_occurrence_identity" not in first_recorded
    assert "act_occurrence_identity" not in second_recorded
    assert (
        first_recorded["destination_locality_identity"]
        != second_recorded["destination_locality_identity"]
    )


def test_one_operator_occurrence_cannot_have_two_destination_localities():
    ledger = EventLedger()
    command = _command(ledger)
    _relation(ledger, command)
    with pytest.raises(OperatorDestinationLocalityError, match="already has"):
        record_operator_destination_locality_act_occurrence(
            ledger,
            operator_material_occurrence_reference=command.identity,
            current_coordinates=read_operator_current_coordinates(
                ledger, locality_identity="operator"
            ),
        )


def test_act_requires_exact_current_operator_material():
    ledger = EventLedger()
    command = _command(ledger)
    empty_coordinates = read_operator_current_coordinates(
        ledger, locality_identity="other"
    )
    with pytest.raises(
        OperatorDestinationLocalityError,
        match="current operator material coordinates",
    ):
        record_operator_destination_locality_act_occurrence(
            ledger,
            operator_material_occurrence_reference=command.identity,
            current_coordinates=empty_coordinates,
        )

    not_command = _command(ledger, exact=b"pytest\n")
    with pytest.raises(OperatorDestinationLocalityError, match="material occurrence"):
        record_operator_destination_locality_act_occurrence(
            ledger,
            operator_material_occurrence_reference=not_command.identity,
            current_coordinates=read_operator_current_coordinates(
                ledger, locality_identity="operator"
            ),
        )


def test_one_destination_locality_act_addresses_one_result():
    ledger = EventLedger()
    command = _command(ledger)
    act = record_operator_destination_locality_act_occurrence(
        ledger,
        operator_material_occurrence_reference=command.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity="operator"
        ),
    )
    record_operator_destination_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    with pytest.raises(
        OperatorDestinationLocalityError,
        match="one destination Locality Act occurrence cannot address two results",
    ):
        record_operator_destination_locality_result(
            ledger, act_occurrence_event_identity=act.identity
        )


def test_corrupted_act_and_result_are_refused_independently():
    for coordinate in ("act", "result"):
        ledger = EventLedger()
        act, result = _relation(ledger, _command(ledger))
        event = {"act": act, "result": result}[coordinate]
        exact_coordinate = {
            "act": "act",
            "result": "act_occurrence_event_identity",
        }[coordinate]
        event.material[exact_coordinate] = "changed coordinate"
        reader, identity = {
            "act": (get_operator_destination_locality_act_occurrence, act.identity),
            "result": (get_recorded_operator_destination_locality, result.identity),
        }[coordinate]
        with pytest.raises(OperatorDestinationLocalityError):
            reader(ledger, identity)


def test_destination_locality_act_requires_current_operator_coordinates():
    ledger = EventLedger()
    command = _command(ledger)
    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity="operator"
    )
    without_command = {
        **current_coordinates,
        "exact_result_occurrences": {},
    }
    with pytest.raises(
        OperatorDestinationLocalityError,
        match="current operator material coordinates",
    ):
        record_operator_destination_locality_act_occurrence(
            ledger,
            operator_material_occurrence_reference=command.identity,
            current_coordinates=without_command,
        )


@pytest.mark.parametrize("sqlite", (False, True))
@pytest.mark.parametrize(
    "boundary_case",
    ("absent", "before-command", "different-locality", "corrupted"),
)
def test_invalid_source_cut_refuses_before_the_act(
    tmp_path, monkeypatch, sqlite, boundary_case
):
    ledger = (
        SQLiteEventLedger(tmp_path / f"{boundary_case}.sqlite")
        if sqlite
        else EventLedger()
    )
    prior = (
        _command(ledger, exact=b"!prior\n")
        if boundary_case == "before-command"
        else None
    )
    command = _command(ledger)
    valid_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=command.locality_identity
    )
    boundary = None
    if boundary_case == "absent":
        invalid_boundary = "missing-boundary"
    elif boundary_case == "before-command":
        invalid_boundary = prior.identity
    elif boundary_case == "different-locality":
        invalid_boundary = _command(ledger, locality="other").identity
    else:
        boundary = _command(ledger)
        invalid_boundary = boundary.identity
        integrity_of = ledger.integrity_of
        monkeypatch.setattr(
            ledger,
            "integrity_of",
            lambda identity: (
                CORRUPTED if identity == boundary.identity else integrity_of(identity)
            ),
        )
    invalid_coordinates = {
        **valid_coordinates,
        "through_event_occurrence_identity": invalid_boundary,
    }

    with pytest.raises(OperatorDestinationLocalityError):
        record_operator_destination_locality_act_occurrence(
            ledger,
            operator_material_occurrence_reference=command.identity,
            current_coordinates=invalid_coordinates,
        )

    assert not any(
        event.kind == OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT
        for event in ledger.list_events()
    )
    if boundary_case == "corrupted":
        monkeypatch.setattr(ledger, "integrity_of", integrity_of)
    corrected = record_operator_destination_locality_act_occurrence(
        ledger,
        operator_material_occurrence_reference=command.identity,
        current_coordinates=valid_coordinates,
    )
    assert corrected.kind == OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT
    if isinstance(ledger, SQLiteEventLedger):
        ledger.close()


def test_destination_locality_act_refuses_a_boundary_after_the_act():
    ledger = EventLedger()
    command = _command(ledger)
    act = record_operator_destination_locality_act_occurrence(
        ledger,
        operator_material_occurrence_reference=command.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=command.locality_identity
        ),
    )
    later = _command(ledger)
    act.material["operator_through_event_occurrence_identity"] = later.identity

    with pytest.raises(
        OperatorDestinationLocalityError,
        match="does not follow current material coordinates",
    ):
        get_operator_destination_locality_act_occurrence(ledger, act.identity)


def test_advanced_destination_coordinates_equal_full_replay():
    ledger = EventLedger()
    command = _command(ledger)
    act, relation = _relation(ledger, command)
    locality = relation.locality_identity
    advanced_coordinates = advance_operator_current_coordinates(
        ledger,
        (
            act.identity,
            relation.identity,
        ),
        locality_identity=locality,
    )
    assert advanced_coordinates == read_operator_current_coordinates(
        ledger, locality_identity=locality
    )


def test_destination_locality_relation_reopens_with_exact_current_coordinates(tmp_path):
    database = tmp_path / "operator-destination-locality.db"
    ledger = SQLiteEventLedger(database)
    command = _command(ledger)
    _act, relation = _relation(ledger, command)
    locality = relation.locality_identity
    relation_identity = relation.identity
    ledger.close()

    reopened = SQLiteEventLedger(database)
    try:
        recorded = get_recorded_operator_destination_locality(
            reopened, relation_identity
        )
        current_coordinates = read_operator_current_coordinates(
            reopened, locality_identity=locality
        )
    finally:
        reopened.close()

    assert recorded["destination_locality_identity"] == locality
    assert current_coordinates["operator_destination_locality_relations"] == {
        relation_identity: None
    }
