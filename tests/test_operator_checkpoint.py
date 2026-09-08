"""Operator material: exact occurrence boundary."""

from __future__ import annotations

from io import BytesIO

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_source import exact_material_result_bytes
from seed_runtime.operator_checkpoint import (
    OperatorCheckpointError,
    OperatorCheckpointRequest,
    get_operator_checkpoint_material_occurrence,
    request_operator_checkpoint,
)
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import (
    read_operator_current_coordinates,
    read_operator_current_coordinates_through,
)
from seed_runtime.operator_material_source import OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
from seed_runtime.witness_material_source import record_witness_material_source


def _command(exact: bytes) -> AddressedOperatorCommand:
    return AddressedOperatorCommand(
        locality_identity="source",
        addressed_through_event_occurrence_identity="boundary",
        frame=OperatorCommandFrame(
            exact_bytes=exact,
            name=b"checkpoint",
            arguments=b"",
        ),
    )


def _run(exact: bytes = b"/checkpoint\n", *, ledger=None):
    ledger = ledger or EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(exact),
    )
    occurrence = next(
        event
        for event in ledger.list_locality("source")
        if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        and event.exact_material == exact
    )
    return ledger, occurrence


@pytest.mark.parametrize("exact", (b"/checkpoint", b"/checkpoint\n", b"/checkpoint\r\n"))
def test_checkpoint_request_is_exact_argument_free_operator_control(exact):
    assert request_operator_checkpoint(_command(exact)) == OperatorCheckpointRequest()


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


def test_checkpoint_is_its_exact_operator_material_occurrence():
    ledger, occurrence = _run()

    assert get_operator_checkpoint_material_occurrence(
        ledger, occurrence.identity
    ) == occurrence
    assert exact_material_result_bytes(occurrence) == b"/checkpoint\n"
    assert {event.locality_identity for event in ledger.list()} == {"source"}
    assert not tuple(
        event
        for event in ledger.list()
        if "through_occurrence_boundary_reference" in event.kind
    )
    assert all(
        key not in occurrence.material
        for key in (
            "exact_act_identity",
            "act_occurrence_identity",
            "result_identity",
            "source_reference",
        )
    )


def test_checkpoint_occurrence_itself_is_the_exact_reading_boundary():
    ledger, occurrence = _run()

    reading = read_operator_current_coordinates_through(
        ledger,
        locality_identity="source",
        through_event_occurrence_identity=occurrence.identity,
    )

    assert reading["through_event_occurrence_identity"] == occurrence.identity
    assert reading["material_result_occurrences"] == [
        {
            "subject_reference": occurrence.identity,
            "result_occurrence_identity": occurrence.identity,
        }
    ]
    assert "recorded_through_occurrence_boundary_references" not in reading


def test_checkpoint_occurrence_cut_does_not_drift_when_source_advances():
    ledger, occurrence = _run()
    before = read_operator_current_coordinates_through(
        ledger,
        locality_identity="source",
        through_event_occurrence_identity=occurrence.identity,
    )
    record_witness_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"subsequent\n",
        source_boundary="fixture boundary",
    )
    after = read_operator_current_coordinates_through(
        ledger,
        locality_identity="source",
        through_event_occurrence_identity=occurrence.identity,
    )

    assert after == before


def test_noncheckpoint_and_witness_material_are_not_checkpoint_occurrences():
    ledger, ordinary = _run(b"ordinary\n")
    witness = record_witness_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"/checkpoint\n",
        source_boundary="witness boundary",
    )

    for occurrence in (ordinary, witness):
        with pytest.raises(
            OperatorCheckpointError,
            match="does not supply the exact checkpoint command",
        ):
            get_operator_checkpoint_material_occurrence(ledger, occurrence.identity)


def test_changed_checkpoint_occurrence_is_refused():
    ledger, occurrence = _run()
    ledger.get(occurrence.identity).material["source_boundary"] = "different"

    with pytest.raises(OperatorCheckpointError, match="absent or corrupted"):
        get_operator_checkpoint_material_occurrence(ledger, occurrence.identity)


def test_checkpoint_occurrence_survives_durable_reopen(tmp_path):
    path = tmp_path / "checkpoint.sqlite"
    ledger = SQLiteEventLedger(str(path))
    _ledger, occurrence = _run(ledger=ledger)
    occurrence_identity = occurrence.identity
    ledger.close()

    reopened = SQLiteEventLedger(str(path))
    try:
        occurrence = get_operator_checkpoint_material_occurrence(
            reopened, occurrence_identity
        )
        reading = read_operator_current_coordinates_through(
            reopened,
            locality_identity="source",
            through_event_occurrence_identity=occurrence.identity,
        )
        assert reading["through_event_occurrence_identity"] == occurrence_identity
    finally:
        reopened.close()


def test_current_coordinates_add_no_checkpoint_specific_surface():
    ledger, occurrence = _run()
    current = read_operator_current_coordinates(ledger, locality_identity="source")

    assert occurrence.identity in {
        coordinate["result_occurrence_identity"]
        for coordinate in current["material_result_occurrences"]
    }
    assert "recorded_through_occurrence_boundary_references" not in current
