from __future__ import annotations

from io import BytesIO, StringIO
import os

from seed_runtime.events import EventLedger
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_checkpoint import (
    ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingested_material_bytes,
)
from seed_runtime.operator_material_command import (
    OperatorMaterialRequest,
    request_operator_material,
)


def test_material_request_preserves_exact_argument_bytes():
    addressed = AddressedOperatorCommand(
        command_identity="command",
        locality_identity="locality",
        addressed_at_representation_event_identity="representation",
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
        locality_identity="root-locality",
        input_stream=BytesIO(b"/material " + os.fsencode(path) + b"\n"),
        output_stream=StringIO(),
    )

    assert not [
        event for event in ledger.list() if event.kind.startswith("operator.command.")
    ]


def test_material_request_begins_a_fresh_locality_at_the_addressed_representation():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="root-locality",
        input_stream=BytesIO(b"/material fixture\nafter\n"),
        output_stream=StringIO(),
    )

    evidence = next(
        event
        for event in ledger.list()
        if event.kind == ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND
    )
    addressed = ledger.get(evidence.material["second_subject"])
    ingests = [
        event for event in ledger.list() if event.kind == MATERIAL_INGEST_OCCURRED_KIND
    ]

    assert evidence.locality_identity != "root-locality"
    assert addressed.locality_identity == "root-locality"
    assert ingested_material_bytes(ingests[0]) == b"after\n"
    assert ingests[0].locality_identity == evidence.locality_identity


def test_each_material_request_begins_another_fresh_locality():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="root-locality",
        input_stream=BytesIO(b"/material first\n/material second\n"),
        output_stream=StringIO(),
    )

    evidence = [
        event
        for event in ledger.list()
        if event.kind == ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND
    ]
    first_addressed = ledger.get(evidence[0].material["second_subject"])
    second_addressed = ledger.get(evidence[1].material["second_subject"])

    assert len(evidence) == 2
    assert first_addressed.locality_identity == "root-locality"
    assert second_addressed.locality_identity == evidence[0].locality_identity
    assert evidence[1].locality_identity not in {
        "root-locality",
        evidence[0].locality_identity,
    }
