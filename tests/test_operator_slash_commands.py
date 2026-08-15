"""The console distinguishes exact slash frames from raw operator data."""

from __future__ import annotations

from io import BytesIO, StringIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_command import (
    COMMAND_ADDRESSED_KIND,
    COMMAND_UNAVAILABLE_KIND,
)
from seed_runtime.operator_checkpoint import CHECKPOINT_LOCALITY_EVIDENCE_KIND
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND


def _run(material: bytes, *, handlers=None):
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_id="root-locality",
        input_stream=BytesIO(material),
        output_stream=StringIO(),
        command_handlers=handlers,
    )
    return ledger


def _raw_bytes(ledger: EventLedger) -> list[bytes]:
    return [
        bytes.fromhex(event.payload["exact_bytes_hex"])
        for event in ledger.list_locality("root-locality")
        if event.kind == MATERIAL_INGEST_OCCURRED_KIND
    ]


def test_non_slash_frames_are_raw_data_and_eof_ends_the_loop():
    ledger = _run(b"exit\n\xff\x00\n")

    assert _raw_bytes(ledger) == [b"exit\n", b"\xff\x00\n"]
    assert not [event for event in ledger.list() if event.kind.startswith("operator.command.")]


def test_slash_frame_invokes_the_exact_registered_implementation_function():
    received = []

    def inspect(addressed_command):
        received.append(addressed_command)
        return {"return shape is not constrained": object()}

    ledger = _run(b"/inspect \xff\x00\n", handlers={b"inspect": inspect})

    assert len(received) == 1
    addressed_command = received[0]
    assert addressed_command.frame.name == b"inspect"
    assert addressed_command.frame.arguments == b"\xff\x00"
    assert addressed_command.frame.exact_bytes == b"/inspect \xff\x00\n"
    addressed = ledger.get(addressed_command.addressed_event_id)
    assert addressed.locality_id == "root-locality"
    assert _raw_bytes(ledger) == []
    assert [event.kind for event in ledger.list_locality(addressed.locality_id)
            if event.kind.startswith("operator.command.")] == [
        COMMAND_ADDRESSED_KIND,
    ]


def test_an_ordinary_command_does_not_divide_locality():
    seen = []
    ledger = _run(b"/inspect\n", handlers={b"inspect": seen.append})
    addressed_command = seen[0]
    addressed = ledger.get(addressed_command.addressed_event_id)

    assert {event.locality_id for event in ledger.list()} == {"root-locality"}
    representation_id = addressed.payload["addressed_at_representation_event_id"]
    assert ledger.get(representation_id).kind == "operator.representation.recorded"
    assert ledger.get(representation_id).locality_id == "root-locality"


def test_checkpoint_alone_divides_locality_at_the_last_representation():
    ledger = _run(b"before\n/checkpoint\nafter\n")
    evidence = next(
        event for event in ledger.list()
        if event.kind == CHECKPOINT_LOCALITY_EVIDENCE_KIND
    )
    checkpoint = ledger.get(evidence.payload["checkpoint_event_id"])
    addressed = ledger.get(evidence.payload["addressed_event_id"])

    assert evidence.locality_id != "root-locality"
    assert checkpoint.kind == "operator.representation.recorded"
    assert checkpoint.locality_id == "root-locality"
    assert evidence.payload["first_subject"] == addressed.payload["command_id"]
    assert evidence.payload["second_subject"] == checkpoint.id
    assert not any("emission" in key for key in evidence.payload)
    assert not any("emission" in key for key in addressed.payload)
    assert _raw_bytes(ledger) == [b"before\n"]
    assert [
        bytes.fromhex(event.payload["exact_bytes_hex"])
        for event in ledger.list_locality(evidence.locality_id)
        if event.kind == MATERIAL_INGEST_OCCURRED_KIND
    ] == [b"after\n"]


def test_repeated_checkpoints_preserve_one_exact_checkpoint_chain():
    ledger = _run(b"/checkpoint\n/checkpoint\n")
    evidence = [
        event for event in ledger.list()
        if event.kind == CHECKPOINT_LOCALITY_EVIDENCE_KIND
    ]

    assert len(evidence) == 2
    first_checkpoint = ledger.get(evidence[0].payload["checkpoint_event_id"])
    second_checkpoint = ledger.get(evidence[1].payload["checkpoint_event_id"])
    assert first_checkpoint.locality_id == "root-locality"
    assert second_checkpoint.locality_id == evidence[0].locality_id
    assert evidence[1].locality_id not in {
        "root-locality", evidence[0].locality_id
    }


def test_unregistered_slash_name_is_not_silently_reclassified_as_data():
    ledger = _run(b"/unregistered\nafter\n")

    assert _raw_bytes(ledger) == [b"after\n"]
    unavailable = [event for event in ledger.list() if event.kind == COMMAND_UNAVAILABLE_KIND]
    assert len(unavailable) == 1
    assert bytes.fromhex(unavailable[0].payload["command_name_hex"]) == b"unregistered"


def test_exit_has_no_console_wrapper():
    ledger = _run(b"/exit\nafter\n")

    assert _raw_bytes(ledger) == [b"after\n"]
    assert [event for event in ledger.list() if event.kind == COMMAND_UNAVAILABLE_KIND]
