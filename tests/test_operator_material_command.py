from __future__ import annotations

from io import BytesIO, StringIO
import os

from seed_runtime.events import EventLedger
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_material_command import (
    OperatorMaterialRequest,
    request_operator_material,
)


def test_material_request_preserves_exact_argument_bytes():
    addressed = AddressedOperatorCommand(
        command_id="command",
        locality_id="locality",
        addressed_at_representation_event_id="representation",
        frame=OperatorCommandFrame(
            exact_bytes=b"/material \xff\x00\n",
            name=b"material",
            arguments=b"\xff\x00",
        ),
    )

    request = request_operator_material(addressed)

    assert request == OperatorMaterialRequest(path_bytes=b"\xff\x00")


def test_material_request_does_not_cross_the_filesystem(monkeypatch, tmp_path):
    path = tmp_path / "book.bin"
    path.write_bytes(b"book bytes")

    def refuse_crossing(*args, **kwargs):
        raise AssertionError((args, kwargs))

    monkeypatch.setattr(os, "lstat", refuse_crossing)
    monkeypatch.setattr(os, "open", refuse_crossing)
    monkeypatch.setattr(os, "scandir", refuse_crossing)
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_id="root-locality",
        input_stream=BytesIO(b"/material " + os.fsencode(path) + b"\n"),
        output_stream=StringIO(),
    )

    assert not [
        event for event in ledger.list() if event.kind.startswith("operator.command.")
    ]
