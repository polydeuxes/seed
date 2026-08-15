"""The console distinguishes exact slash frames from raw operator data."""

from __future__ import annotations

from io import BytesIO, StringIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_checkpoint import ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingested_material_bytes,
)


def _run(material: bytes, *, handlers=None):
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="root-locality",
        input_stream=BytesIO(material),
        output_stream=StringIO(),
        command_handlers=handlers,
    )
    return ledger


def _raw_bytes(ledger: EventLedger) -> list[bytes]:
    return [
        ingested_material_bytes(event)
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
    assert addressed_command.locality_identity == "root-locality"
    addressed_representation = ledger.get(
        addressed_command.addressed_at_representation_event_identity
    )
    assert addressed_representation.locality_identity == "root-locality"
    assert _raw_bytes(ledger) == []
    assert not [
        event for event in ledger.list() if event.kind.startswith("operator.command.")
    ]


def test_an_ordinary_command_does_not_divide_locality():
    seen = []
    ledger = _run(b"/inspect\n", handlers={b"inspect": seen.append})
    addressed_command = seen[0]

    assert {event.locality_identity for event in ledger.list()} == {"root-locality"}
    representation_identity = addressed_command.addressed_at_representation_event_identity
    assert ledger.get(representation_identity).kind == "operator.representation.recorded"
    assert ledger.get(representation_identity).locality_identity == "root-locality"


def test_checkpoint_alone_divides_locality_at_the_last_representation():
    ledger = _run(b"before\n/checkpoint\nafter\n")
    evidence = next(
        event for event in ledger.list()
        if event.kind == ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND
    )
    checkpoint = ledger.get(evidence.material["second_subject"])

    assert evidence.locality_identity != "root-locality"
    assert checkpoint.kind == "operator.representation.recorded"
    assert checkpoint.locality_identity == "root-locality"
    assert isinstance(evidence.material["first_subject"], str)
    assert evidence.material["second_subject"] == checkpoint.identity
    assert not any("emission" in key for key in evidence.material)
    assert _raw_bytes(ledger) == [b"before\n"]
    assert [
        ingested_material_bytes(event)
        for event in ledger.list_locality(evidence.locality_identity)
        if event.kind == MATERIAL_INGEST_OCCURRED_KIND
    ] == [b"after\n"]


def test_repeated_checkpoints_preserve_one_exact_checkpoint_chain():
    ledger = _run(b"/checkpoint\n/checkpoint\n")
    evidence = [
        event for event in ledger.list()
        if event.kind == ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND
    ]

    assert len(evidence) == 2
    first_checkpoint = ledger.get(evidence[0].material["second_subject"])
    second_checkpoint = ledger.get(evidence[1].material["second_subject"])
    assert first_checkpoint.locality_identity == "root-locality"
    assert second_checkpoint.locality_identity == evidence[0].locality_identity
    assert evidence[1].locality_identity not in {
        "root-locality", evidence[0].locality_identity
    }


def test_unregistered_slash_name_is_not_silently_reclassified_as_data():
    ledger = _run(b"/unregistered\nafter\n")

    assert _raw_bytes(ledger) == [b"after\n"]
    assert not [
        event for event in ledger.list() if event.kind.startswith("operator.command.")
    ]


def test_exit_has_no_console_wrapper():
    ledger = _run(b"/exit\nafter\n")

    assert _raw_bytes(ledger) == [b"after\n"]
    assert not [
        event for event in ledger.list() if event.kind.startswith("operator.command.")
    ]
