"""External operator control that begins a fresh locality at one checkpoint."""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.events import CORRUPTED
from seed_runtime.ids import new_id
from seed_runtime.operator_command import OperatorCommandContext


CHECKPOINT_LOCALITY_EVIDENCE_KIND = "operator.checkpoint.locality_evidenced"


class OperatorCheckpointError(ValueError):
    """A fresh locality could not be related to the exact checkpoint."""


@dataclass(frozen=True)
class OperatorCheckpoint:
    locality_id: str
    locality_evidence_event_id: str
    checkpoint_event_id: str


def open_operator_checkpoint(context: OperatorCommandContext) -> OperatorCheckpoint:
    """Begin one fresh locality at the exact emission addressed by the command.

    Argument bytes remain part of the addressed command occurrence. They are
    not interpreted as a goal, desire, relation, Authority, or Standing here.
    The checkpoint occurrence already carries the locality in which it
    occurred, so this relation stores no additional hierarchy field.
    """

    checkpoint = context.ledger.get(context.addressed_at_representation_event_id)
    addressed = context.ledger.get(context.addressed_event_id)
    if (
        checkpoint is None
        or checkpoint.kind != "operator.representation.recorded"
        or checkpoint.workspace_id != context.workspace_id
        or checkpoint.locality_id != context.locality_id
        or context.ledger.integrity_of(checkpoint.id) == CORRUPTED
    ):
        raise OperatorCheckpointError(
            "checkpoint requires one intact Representation occurrence in this locality"
        )
    if (
        addressed is None
        or addressed.kind != "operator.command.addressed"
        or addressed.workspace_id != context.workspace_id
        or addressed.locality_id != context.locality_id
        or addressed.payload.get("command_id") != context.command_id
        or context.ledger.integrity_of(addressed.id) == CORRUPTED
    ):
        raise OperatorCheckpointError(
            "checkpoint requires its intact addressed command occurrence"
        )

    locality_id = new_id("checkpoint_locality")
    evidence = context.ledger.append(
        CHECKPOINT_LOCALITY_EVIDENCE_KIND,
        context.workspace_id,
        {
            "first_subject": context.command_id,
            "second_subject": checkpoint.id,
            "command_id": context.command_id,
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
