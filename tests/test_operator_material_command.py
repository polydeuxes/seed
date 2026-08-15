"""`/material` reads bounded filesystem material in the current locality."""

from __future__ import annotations

from io import BytesIO, StringIO
import os

from seed_runtime.events import EventLedger
from seed_runtime.material_availability import (
    MATERIAL_OCCURRED_KIND,
    ProcessLocalMaterial,
    identity_of_occurrence,
)
from seed_runtime.operator_checkpoint import CHECKPOINT_LOCALITY_EVIDENCE_KIND
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_material_command import (
    MATERIAL_REFUSED_KIND,
    MATERIAL_RELATED_KIND,
    MATERIAL_TARGET_READ_KIND,
    OperatorMaterialCommand,
)


def _run(material: bytes, command: OperatorMaterialCommand) -> EventLedger:
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        locality_id="root-locality",
        input_stream=BytesIO(material),
        output_stream=StringIO(),
        material_command=command,
    )
    return ledger


def test_regular_file_is_held_whole_without_putting_its_body_in_the_ledger(tmp_path):
    exact = b"\x00audio\xffvideo\nbook"
    path = tmp_path / "material.bin"
    path.write_bytes(exact)
    holder = ProcessLocalMaterial()
    command = OperatorMaterialCommand(holder=holder, file_byte_bound=len(exact))

    ledger = _run(b"/material " + os.fsencode(path) + b"\n", command)
    occurred = next(event for event in ledger.list("w") if event.kind == MATERIAL_OCCURRED_KIND)
    identity = identity_of_occurrence(occurred)

    assert holder.reconstruct(identity) == exact
    assert identity.byte_count == len(exact)
    assert occurred.payload["material_origin"] == "system"
    assert exact.hex() not in str(occurred.payload)
    read = next(
        event for event in ledger.list("w")
        if event.kind == MATERIAL_TARGET_READ_KIND
    )
    related = next(
        event for event in ledger.list("w") if event.kind == MATERIAL_RELATED_KIND
    )
    assert related.payload["first_subject"] == read.id
    assert related.payload["second_subject"] == occurred.id


def test_directory_read_is_shallow_and_bounded(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()
    (folder / "one").write_bytes(b"one")
    (folder / "two").write_bytes(b"two")
    (folder / "three").write_bytes(b"three")
    nested = folder / "nested"
    nested.mkdir()
    (nested / "not-read").write_bytes(b"not read")
    command = OperatorMaterialCommand(directory_entry_bound=2)

    ledger = _run(b"/material " + os.fsencode(folder) + b"\n", command)
    read = next(
        event for event in ledger.list("w")
        if event.kind == MATERIAL_TARGET_READ_KIND
    )

    assert read.payload["target_kind"] == "directory"
    assert read.payload["recursive"] is False
    assert len(read.payload["entries_read"]) == 2
    assert read.payload["complete_under_entry_bound"] is False
    assert not [event for event in ledger.list("w") if event.kind == MATERIAL_OCCURRED_KIND]


def test_oversized_file_is_not_partially_held_or_represented_as_whole(tmp_path):
    path = tmp_path / "large.bin"
    path.write_bytes(b"0123456789")
    holder = ProcessLocalMaterial()
    command = OperatorMaterialCommand(holder=holder, file_byte_bound=4)

    ledger = _run(b"/material " + os.fsencode(path) + b"\n", command)
    refused = next(event for event in ledger.list("w") if event.kind == MATERIAL_REFUSED_KIND)

    assert refused.payload["target_byte_count"] == 10
    assert holder.held_count == 0
    assert not [event for event in ledger.list("w") if event.kind == MATERIAL_OCCURRED_KIND]
    assert not [event for event in ledger.list("w") if event.kind == MATERIAL_RELATED_KIND]


def test_symbolic_link_is_not_followed(tmp_path):
    target = tmp_path / "target"
    target.write_bytes(b"material")
    link = tmp_path / "link"
    link.symlink_to(target)
    holder = ProcessLocalMaterial()

    ledger = _run(
        b"/material " + os.fsencode(link) + b"\n",
        OperatorMaterialCommand(holder=holder),
    )
    refused = next(event for event in ledger.list("w") if event.kind == MATERIAL_REFUSED_KIND)

    assert "symbolic_link" in refused.payload["reason"]
    assert holder.held_count == 0


def test_material_occurs_in_the_locality_selected_by_checkpoint(tmp_path):
    path = tmp_path / "book.bin"
    path.write_bytes(b"book bytes")
    ledger = _run(
        b"/checkpoint\n/material " + os.fsencode(path) + b"\n",
        OperatorMaterialCommand(),
    )
    checkpoint = next(
        event for event in ledger.list("w")
        if event.kind == CHECKPOINT_LOCALITY_EVIDENCE_KIND
    )
    material = next(event for event in ledger.list("w") if event.kind == MATERIAL_OCCURRED_KIND)

    assert material.locality_id == checkpoint.locality_id
    assert material.locality_id != "root-locality"
