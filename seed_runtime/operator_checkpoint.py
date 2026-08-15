"""External operator control that begins a fresh locality at one checkpoint."""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_command import AddressedOperatorCommand


CHECKPOINT_LOCALITY_EVIDENCE_KIND = "operator.checkpoint.locality_evidenced"


class OperatorCheckpointError(ValueError):
    """A fresh locality could not be related to the exact checkpoint."""


@dataclass(frozen=True)
class OperatorCheckpoint:
    locality_id: str
    locality_evidence_event_id: str
    checkpoint_event_id: str


@dataclass(frozen=True)
class OperatorCheckpointRequest:
    pass


def request_operator_checkpoint(
    addressed: AddressedOperatorCommand,
) -> OperatorCheckpointRequest:
    if not isinstance(addressed, AddressedOperatorCommand):
        raise TypeError("checkpoint control requires one addressed command")
    return OperatorCheckpointRequest()


def open_operator_checkpoint(
    ledger: EventLedger,
    addressed_command: AddressedOperatorCommand,
) -> OperatorCheckpoint:
    """Begin one fresh locality at the exact Representation addressed by the command.

    Argument bytes remain part of the addressed command occurrence. They are
    not interpreted as a goal, desire, relation, Authority, or Standing here.
    The checkpoint occurrence already carries the locality in which it
    occurred, so this relation stores no additional hierarchy field.
    """

    if not isinstance(addressed_command, AddressedOperatorCommand):
        raise TypeError("checkpoint requires one addressed command")
    addressed = ledger.get(addressed_command.addressed_event_id)
    if (
        addressed is None
        or addressed.kind != "operator.command.addressed"
        or ledger.integrity_of(addressed.id) == CORRUPTED
    ):
        raise OperatorCheckpointError(
            "checkpoint requires its intact addressed command occurrence"
        )
    checkpoint_id = addressed.payload.get("addressed_at_representation_event_id")
    checkpoint = ledger.get(checkpoint_id) if isinstance(checkpoint_id, str) else None
    if (
        checkpoint is None
        or checkpoint.kind != "operator.representation.recorded"
        or checkpoint.workspace_id != addressed.workspace_id
        or checkpoint.locality_id != addressed.locality_id
        or ledger.integrity_of(checkpoint.id) == CORRUPTED
    ):
        raise OperatorCheckpointError(
            "checkpoint requires one intact Representation occurrence in this locality"
        )
    command_id = addressed.payload.get("command_id")
    if not isinstance(command_id, str):
        raise OperatorCheckpointError("checkpoint requires one exact command identity")

    locality_id = new_id("checkpoint_locality")
    evidence = ledger.append(
        CHECKPOINT_LOCALITY_EVIDENCE_KIND,
        addressed.workspace_id,
        {
            "first_subject": command_id,
            "second_subject": checkpoint.id,
            "command_id": command_id,
            "addressed_event_id": addressed.id,
            "checkpoint_event_id": checkpoint.id,
            "standing": "local",
            "authority": "unestablished",
            "evidence_scope": (
                "this exact command-to-checkpoint Locality relation only"
            ),
            "unknowns": [
                "what the command argument material represents remains Unknown"
            ],
        },
        locality_id=locality_id,
    )
    return OperatorCheckpoint(
        locality_id=locality_id,
        locality_evidence_event_id=evidence.id,
        checkpoint_event_id=checkpoint.id,
    )
