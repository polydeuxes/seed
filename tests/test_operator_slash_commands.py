"""The console distinguishes exact slash frames from raw operator data."""

from __future__ import annotations

from io import BytesIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_checkpoint import STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
)
from seed_runtime.material_source import (
    exact_material_result_bytes,
    read_exact_material_result,
)


def _run(material: bytes, *, handlers=None):
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="root-locality",
        input_stream=BytesIO(material),
        command_handlers=handlers,
    )
    return ledger


def _bounded_material_bytes(ledger: EventLedger) -> list[bytes]:
    material = []
    for event in ledger.list_locality("root-locality"):
        try:
            result = read_exact_material_result(ledger, event.identity)
        except (TypeError, ValueError):
            continue
        material.append(exact_material_result_bytes(result))
    return material


def _acquired_bytes(ledger: EventLedger) -> list[bytes]:
    return [
        event.exact_material
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
    ]


def test_non_slash_frames_are_exact_operator_material():
    ledger = _run(b"exit\n\xff\x00\n")

    assert _bounded_material_bytes(ledger) == [b"exit\n", b"\xff\x00\n"]
    assert _acquired_bytes(ledger) == [b"exit\n", b"\xff\x00\n"]
    assert not [event for event in ledger.list() if event.kind.startswith("operator.command.")]


def test_eof_ends_input_without_establishing_a_material_result():
    ledger = _run(b"")

    assert _bounded_material_bytes(ledger) == []
    assert _acquired_bytes(ledger) == []


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
    assert _bounded_material_bytes(ledger) == [b"/inspect \xff\x00\n"]
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


def test_checkpoint_records_one_boundary_reference():
    ledger = _run(b"before\n/checkpoint\nafter\n")
    checkpoint = next(
        event for event in ledger.list()
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    )
    assert checkpoint.locality_identity == "root-locality"


def test_checkpoint_does_not_divide_locality():
    ledger = _run(b"before\n/checkpoint\nafter\n")

    assert {event.locality_identity for event in ledger.list()} == {"root-locality"}


def test_repeated_checkpoints_record_distinct_exact_references_without_a_chain():
    ledger = _run(b"/checkpoint\n/checkpoint\n")
    records = [
        event for event in ledger.list()
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    ]

    assert len(records) == 2
    assert records[0].material["result_identity"] != records[1].material[
        "result_identity"
    ]
    assert {record.locality_identity for record in records} == {"root-locality"}


def test_unregistered_slash_name_reaches_the_exact_ingress_road():
    ledger = _run(b"/unregistered\nafter\n")

    assert _bounded_material_bytes(ledger) == [b"/unregistered\n", b"after\n"]
    assert not [
        event for event in ledger.list() if event.kind.startswith("operator.command.")
    ]


def test_exit_is_exact_operator_material():
    ledger = _run(b"/exit\nafter\n")

    assert _bounded_material_bytes(ledger) == [b"/exit\n", b"after\n"]
    assert _acquired_bytes(ledger) == [b"/exit\n", b"after\n"]


def test_exit_does_not_establish_stop():
    ledger = _run(b"/exit\nafter\n")

    assert _bounded_material_bytes(ledger)[-1] == b"after\n"
    assert not [
        event for event in ledger.list() if event.kind.startswith("operator.command.")
    ]


def test_unregistered_binary_slash_material_is_preserved_exactly():
    ledger = _run(b"/\xff\x00 material\n")

    assert _bounded_material_bytes(ledger) == [b"/\xff\x00 material\n"]
