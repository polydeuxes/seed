"""Operator control that begins a fresh locality at one checkpoint."""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_command import AddressedOperatorCommand


ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND = "operator.addressed_representation.locality_evidenced"
EVENT_KIND_RESPONSIBILITIES = {
    ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND: "06.Standing.B",
}


class OperatorCheckpointError(ValueError):
    """A fresh locality could not be related to the exact checkpoint."""


@dataclass(frozen=True)
class OperatorCheckpoint:
    locality_id: str
    locality_evidence_event_id: str
    representation_reference: str


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
    not classified as a goal, desire, relation, Authority, or Standing here.
    The checkpoint occurrence already carries the locality in which it
    occurred, so this relation stores no additional hierarchy field.
    """

    if not isinstance(addressed_command, AddressedOperatorCommand):
        raise TypeError("checkpoint requires one addressed command")
    checkpoint_id = addressed_command.addressed_at_representation_event_id
    checkpoint = ledger.get(checkpoint_id) if isinstance(checkpoint_id, str) else None
    if (
        checkpoint is None
        or checkpoint.kind != "operator.representation.recorded"
        or checkpoint.locality_id != addressed_command.locality_id
        or ledger.integrity_of(checkpoint.id) == CORRUPTED
    ):
        raise OperatorCheckpointError(
            "checkpoint requires one intact Representation occurrence in this locality"
        )
    command_id = addressed_command.command_id
    if not isinstance(command_id, str):
        raise OperatorCheckpointError("checkpoint requires one exact command identity")

    locality_id = new_id("checkpoint_locality")
    evidence = ledger.append(
        ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND,
        {
            "first_subject": command_id,
            "second_subject": checkpoint.id,
            "addressed_identity": command_id,
            "representation_reference": checkpoint.id,
            "authority": "unestablished",
            "evidence_scope": (
                "this exact addressed-identity-to-Representation Locality relation only"
            ),
            "unknowns": [
                "what the addressed argument material represents remains Unknown"
            ],
        },
        locality_id=locality_id,
    )
    return OperatorCheckpoint(
        locality_id=locality_id,
        locality_evidence_event_id=evidence.id,
        representation_reference=checkpoint.id,
    )
