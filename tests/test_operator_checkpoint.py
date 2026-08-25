from __future__ import annotations

from copy import deepcopy
from io import BytesIO

import pytest


from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_checkpoint import (
    STANDING_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT,
    STANDING_BOUNDARY_REFERENCE_RECORDED_KIND,
    STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OperatorCheckpointError,
    get_recorded_standing_boundary_reference,
    get_standing_boundary_reference_responsibility_assignment,
    record_standing_boundary_reference_responsibility_assignment,
    record_standing_boundary_reference_act_occurrence,
    record_standing_boundary_reference_result,
    request_operator_checkpoint,
)
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.witness_material_source import record_witness_material_source
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.yield_relation import read_requirements_of_yield_relation


def _command(locality_identity: str, boundary_identity: str) -> AddressedOperatorCommand:
    return AddressedOperatorCommand(
        command_identity="fixture-command",
        locality_identity=locality_identity,
        addressed_at_standing_boundary_event_identity=boundary_identity,
        frame=OperatorCommandFrame(
            exact_bytes=b"/checkpoint\n",
            name=b"checkpoint",
            arguments=b"",
        ),
    )


def _context(ledger, locality_identity="source"):
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    boundary = record_witness_material_source(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"checkpoint boundary",
        source_boundary="checkpoint source boundary",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    return standing, boundary, _command(locality_identity, boundary.identity)


def _assignment(ledger, standing, command):
    return record_standing_boundary_reference_responsibility_assignment(
        ledger,
        addressed_command=command,
        locality_standing=standing,
    )


def _act(ledger, assignment):
    standing = read_operator_locality_standing(
        ledger, locality_identity=assignment.locality_identity
    )
    return record_standing_boundary_reference_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing,
    )


def test_three_stages_record_one_exact_bounded_reference_without_movement():
    ledger = EventLedger()
    standing, boundary, command = _context(ledger)
    assignment = _assignment(ledger, standing, command)
    after_assignment = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    act = record_standing_boundary_reference_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=after_assignment,
    )
    before_result = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    result = record_standing_boundary_reference_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    recorded = get_recorded_standing_boundary_reference(ledger, result.identity)

    assert assignment.kind == (
        STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    )
    assert act.kind == STANDING_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT
    assert result.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    assert {event.locality_identity for event in ledger.list()} == {"source"}
    assert recorded["source_reference"] == {
        "source_locality_identity": "source",
        "standing_boundary_event_identity": boundary.identity,
    }
    assert len(
        {
            assignment.identity,
            assignment.material["assignment_identity"],
            assignment.material["assignment_subject_identity"],
            assignment.material["recording_act_identity"],
            assignment.material["act_occurrence_identity"],
            assignment.material["result_identity"],
            assignment.material["scope"]["scope_identity"],
            act.identity,
            result.identity,
            result.material["yield_relation_identity"],
        }
    ) == 10
    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        yield_relation_event_identity=result.material["yield_relation_identity"],
        act_occurrence_event_identity=act.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": True,
    }
    carried = advance_operator_locality_standing(
        ledger,
        (result.material["yield_relation_identity"], result.identity),
        locality_identity="source",
        prior=before_result,
    )
    replayed = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    assert carried == replayed
    assert replayed["recorded_standing_boundary_references"] == {
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
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    )
    recorded = get_recorded_standing_boundary_reference(ledger, result.identity)
    boundary = ledger.get(
        recorded["source_reference"]["standing_boundary_event_identity"]
    )
    assert boundary is not None
    assert read_operator_locality_standing(
        ledger, locality_identity="source"
    )["recorded_standing_boundary_references"] == {result.identity: None}


@pytest.mark.parametrize("exact", (b"/checkpoint x\n", b"/checkpoint \n"))
def test_checkpoint_operator_shorthand_refuses_payload(exact):
    command = AddressedOperatorCommand(
        command_identity="command",
        locality_identity="source",
        addressed_at_standing_boundary_event_identity="boundary",
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
    result = record_standing_boundary_reference_result(
        ledger,
        act_occurrence_event_identity=_act(
            ledger, _assignment(ledger, standing, command)
        ).identity,
    )
    before = get_recorded_standing_boundary_reference(ledger, result.identity)
    record_witness_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"later\n",
        source_boundary="fixture boundary",
    )
    assert get_recorded_standing_boundary_reference(ledger, result.identity) == before


def test_act_requires_the_exact_carried_assignment():
    ledger = EventLedger()
    standing, _boundary, command = _context(ledger)
    assignment = _assignment(ledger, standing, command)
    with pytest.raises(OperatorCheckpointError, match="carried assignment"):
        record_standing_boundary_reference_act_occurrence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=standing,
        )


def test_one_recording_act_cannot_yield_twice():
    ledger = EventLedger()
    standing, _boundary, command = _context(ledger)
    act = _act(ledger, _assignment(ledger, standing, command))
    record_standing_boundary_reference_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    with pytest.raises(OperatorCheckpointError, match="already carries a Yield"):
        record_standing_boundary_reference_result(
            ledger, act_occurrence_event_identity=act.identity
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "assignment_identity",
        "assignment_subject_identity",
        "book_clause_identity",
        "recording_act_identity",
        "act_occurrence_identity",
        "result_identity",
        "source_reference",
        "scope",
        "unknown",
    ),
)
def test_changed_assignment_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    standing, _boundary, command = _context(ledger)
    assignment = _assignment(ledger, standing, command)
    changed = ledger.get(assignment.identity)
    if coordinate in {
        "assignment_identity",
        "assignment_subject_identity",
        "recording_act_identity",
        "act_occurrence_identity",
        "result_identity",
    }:
        changed.material[coordinate] = changed.material["scope"]["scope_identity"]
    else:
        changed.material[coordinate] = "different"
    with pytest.raises((OperatorCheckpointError, TypeError, ValueError)):
        get_standing_boundary_reference_responsibility_assignment(
            ledger, assignment.identity
        )


def test_assignment_and_act_survive_restart_before_result(tmp_path):
    path = tmp_path / "checkpoint.sqlite"
    ledger = SQLiteEventLedger(str(path))
    standing, _boundary, command = _context(ledger)
    assignment = _assignment(ledger, standing, command)
    act = _act(ledger, assignment)
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    result = record_standing_boundary_reference_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    replayed = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    assert replayed["recorded_standing_boundary_references"] == {
        result.identity: None
    }
    ledger.close()


def test_durable_values_do_not_import_operator_shorthand():
    ledger = EventLedger()
    standing, _boundary, command = _context(ledger)
    result = record_standing_boundary_reference_result(
        ledger,
        act_occurrence_event_identity=_act(
            ledger, _assignment(ledger, standing, command)
        ).identity,
    )
    durable = repr(
        [
            (event.kind, event.material)
            for event in ledger.list()
            if event.identity in {
                result.identity,
                result.material["act_occurrence_identity"],
                result.material["yield_relation_identity"],
            }
            or "standing_boundary_reference" in event.kind
        ]
    ).lower()
    assert "checkpoint" not in durable
    assert "checkout" not in durable
    assert "memory" not in durable


def test_prior_record_carrier_must_remain_an_identity_dictionary():
    ledger = EventLedger()
    standing, _boundary, command = _context(ledger)
    result = record_standing_boundary_reference_result(
        ledger,
        act_occurrence_event_identity=_act(
            ledger, _assignment(ledger, standing, command)
        ).identity,
    )
    prior = read_operator_locality_standing(ledger, locality_identity="source")
    broken = deepcopy(prior)
    broken["recorded_standing_boundary_references"] = [result.identity]
    with pytest.raises(ValueError, match="Standing boundary references"):
        advance_operator_locality_standing(
            ledger, (), locality_identity="source", prior=broken
        )
