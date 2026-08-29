"""Operator recording preserves one exact through occurrence boundary."""

from __future__ import annotations

from copy import deepcopy
from io import BytesIO

import pytest


from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_checkpoint import (
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT,
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND,
    OperatorCheckpointError,
    get_recorded_through_occurrence_boundary_reference,
    get_through_occurrence_boundary_reference_act_occurrence,
    record_through_occurrence_boundary_reference_act_occurrence,
    record_through_occurrence_boundary_reference_result,
    request_operator_checkpoint,
)
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.witness_material_source import record_witness_material_source
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.yield_relation import RECORDED_YIELD_RELATION_EVENT


def _command(locality_identity: str, boundary_identity: str) -> AddressedOperatorCommand:
    return AddressedOperatorCommand(
        locality_identity=locality_identity,
        addressed_through_event_occurrence_identity=boundary_identity,
        frame=OperatorCommandFrame(
            exact_bytes=b"/checkpoint\n",
            name=b"checkpoint",
            arguments=b"",
        ),
    )


def _context(ledger, locality_identity="source"):
    standing = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    boundary = record_witness_material_source(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"checkpoint boundary",
        source_boundary="checkpoint source boundary",
    )
    standing = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    return standing, boundary, _command(locality_identity, boundary.identity)


def _act(ledger, current_coordinates, command):
    return record_through_occurrence_boundary_reference_act_occurrence(
        ledger,
        addressed_command=command,
        current_coordinates=current_coordinates,
    )


def test_act_and_result_record_one_exact_bounded_reference_without_movement():
    ledger = EventLedger()
    standing, boundary, command = _context(ledger)
    act = record_through_occurrence_boundary_reference_act_occurrence(
        ledger,
        addressed_command=command,
        current_coordinates=standing,
    )
    before_result = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    result = record_through_occurrence_boundary_reference_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    recorded = get_recorded_through_occurrence_boundary_reference(ledger, result.identity)

    assert act.kind == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT
    assert result.kind == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND
    assert not any(
        event.kind
        == "operator.through_occurrence_boundary_reference_subject_to_act_binding_recorded"
        for event in ledger.list()
    )
    assert {event.locality_identity for event in ledger.list()} == {"source"}
    assert recorded["source_reference"] == {
        "source_locality_identity": "source",
        "through_event_occurrence_identity": boundary.identity,
    }
    assert act.material["subject_reference"] == recorded["source_reference"]
    assert act.material["book_clause_identity"] == "05.Recording.D"
    assert "subject_to_act_binding_reference" not in act.material
    assert "subject_to_act_binding_reference" not in result.material
    assert len(
        {
            act.material["exact_act_identity"],
            act.material["act_occurrence_identity"],
            act.material["result_identity"],
            act.identity,
            result.identity,
        }
    ) == 5
    assert not tuple(
        event
        for event in ledger.iter_locality_kind(
            "source", RECORDED_YIELD_RELATION_EVENT
        )
        if event.material.get("act_occurrence_event_identity") == act.identity
    )
    carried = advance_operator_current_coordinates(
        ledger,
        (result.identity,),
        locality_identity="source",
        prior=before_result,
    )
    replayed = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    assert carried == replayed
    assert replayed["recorded_through_occurrence_boundary_references"] == {
        result.identity: None
    }


def test_console_checkpoint_records_at_current_locality_and_does_not_move():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"/checkpoint\n"),
    )

    assert {event.locality_identity for event in ledger.list()} == {"source"}
    result = next(
        event
        for event in ledger.list()
        if event.kind == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND
    )
    recorded = get_recorded_through_occurrence_boundary_reference(ledger, result.identity)
    boundary = ledger.get(
        recorded["source_reference"]["through_event_occurrence_identity"]
    )
    assert boundary is not None
    assert read_operator_current_coordinates(
        ledger, locality_identity="source"
    )["recorded_through_occurrence_boundary_references"] == {result.identity: None}


@pytest.mark.parametrize("exact", (b"/checkpoint x\n", b"/checkpoint \n"))
def test_checkpoint_operator_shorthand_refuses_payload(exact):
    command = AddressedOperatorCommand(
        locality_identity="source",
        addressed_through_event_occurrence_identity="boundary",
        frame=OperatorCommandFrame(
            exact_bytes=exact,
            name=b"checkpoint",
            arguments=exact.removeprefix(b"/checkpoint ").rstrip(b"\r\n"),
        ),
    )
    with pytest.raises(ValueError, match="accepts no material"):
        request_operator_checkpoint(command)


def test_recorded_reference_does_not_drift_when_the_source_advances():
    ledger = EventLedger()
    standing, _boundary, command = _context(ledger)
    result = record_through_occurrence_boundary_reference_result(
        ledger,
        act_occurrence_event_identity=_act(ledger, standing, command).identity,
    )
    before = get_recorded_through_occurrence_boundary_reference(ledger, result.identity)
    record_witness_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"later\n",
        source_boundary="fixture boundary",
    )
    assert get_recorded_through_occurrence_boundary_reference(ledger, result.identity) == before


def test_act_requires_the_exact_addressed_current_coordinates():
    ledger = EventLedger()
    prior = read_operator_current_coordinates(ledger, locality_identity="source")
    _standing, _boundary, command = _context(ledger)
    with pytest.raises(
        OperatorCheckpointError,
        match="exact addressed through-occurrence boundary",
    ):
        record_through_occurrence_boundary_reference_act_occurrence(
            ledger,
            addressed_command=command,
            current_coordinates=prior,
        )


def test_one_recording_act_cannot_have_two_results():
    ledger = EventLedger()
    standing, _boundary, command = _context(ledger)
    act = _act(ledger, standing, command)
    record_through_occurrence_boundary_reference_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    with pytest.raises(OperatorCheckpointError, match="already has a result"):
        record_through_occurrence_boundary_reference_result(
            ledger, act_occurrence_event_identity=act.identity
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "book_clause_identity",
        "subject_reference",
        "act",
        "exact_act_identity",
        "act_occurrence_identity",
        "result_identity",
    ),
)
def test_changed_act_binding_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    standing, _boundary, command = _context(ledger)
    act = _act(ledger, standing, command)
    changed = ledger.get(act.identity)
    if coordinate in {
        "exact_act_identity",
        "act_occurrence_identity",
        "result_identity",
    }:
        replacement_coordinate = (
            "act_occurrence_identity"
            if coordinate == "result_identity"
            else "result_identity"
        )
        changed.material[coordinate] = changed.material[replacement_coordinate]
    else:
        changed.material[coordinate] = "different"
    with pytest.raises((OperatorCheckpointError, TypeError, ValueError)):
        get_through_occurrence_boundary_reference_act_occurrence(ledger, act.identity)


def test_act_survives_restart_before_result(tmp_path):
    path = tmp_path / "checkpoint.sqlite"
    ledger = SQLiteEventLedger(str(path))
    standing, _boundary, command = _context(ledger)
    act = _act(ledger, standing, command)
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    result = record_through_occurrence_boundary_reference_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    replayed = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    assert replayed["recorded_through_occurrence_boundary_references"] == {
        result.identity: None
    }
    ledger.close()


def test_durable_values_do_not_import_operator_shorthand():
    ledger = EventLedger()
    standing, _boundary, command = _context(ledger)
    result = record_through_occurrence_boundary_reference_result(
        ledger,
        act_occurrence_event_identity=_act(ledger, standing, command).identity,
    )
    durable = repr(
        [
            (event.kind, event.material)
            for event in ledger.list()
            if event.identity in {
                result.identity,
                result.material["act_occurrence_identity"],
            }
            or "through_occurrence_boundary_reference" in event.kind
        ]
    ).lower()
    assert "checkpoint" not in durable
    assert "checkout" not in durable
    assert "memory" not in durable


def test_prior_record_carrier_must_remain_an_identity_dictionary():
    ledger = EventLedger()
    standing, _boundary, command = _context(ledger)
    result = record_through_occurrence_boundary_reference_result(
        ledger,
        act_occurrence_event_identity=_act(ledger, standing, command).identity,
    )
    prior = read_operator_current_coordinates(ledger, locality_identity="source")
    broken = deepcopy(prior)
    broken["recorded_through_occurrence_boundary_references"] = [result.identity]
    with pytest.raises(ValueError, match="through-occurrence boundary references"):
        advance_operator_current_coordinates(
            ledger, (), locality_identity="source", prior=broken
        )
