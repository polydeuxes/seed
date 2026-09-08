"""Operator shorthand addressing its exact material-result occurrence."""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.material_source import (
    exact_material_result_bytes,
    read_exact_material_result,
)
from seed_runtime.operator_command import AddressedOperatorCommand
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
)


_OPERATOR_CHECKPOINT_MATERIALS = {
    b"/checkpoint",
    b"/checkpoint\n",
    b"/checkpoint\r\n",
}


class OperatorCheckpointError(ValueError):
    """One exact operator checkpoint-command occurrence could not be read."""


def is_operator_checkpoint_material(exact_material: object) -> bool:
    """Return whether exact bytes supply the operator checkpoint command."""

    return (
        type(exact_material) is bytes
        and exact_material in _OPERATOR_CHECKPOINT_MATERIALS
    )


@dataclass(frozen=True)
class OperatorCheckpointRequest:
    pass


def request_operator_checkpoint(
    addressed: AddressedOperatorCommand,
) -> OperatorCheckpointRequest:
    if not isinstance(addressed, AddressedOperatorCommand):
        raise TypeError("checkpoint control requires one addressed command")
    if addressed.frame.exact_bytes not in _OPERATOR_CHECKPOINT_MATERIALS:
        raise ValueError("/checkpoint accepts no material")
    return OperatorCheckpointRequest()


def get_operator_checkpoint_material_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    """Read one exact operator material occurrence supplying `/checkpoint`."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("checkpoint occurrence requires one EventLedger")
    if type(event_identity) is not str or not event_identity:
        raise OperatorCheckpointError(
            "checkpoint occurrence requires one exact occurrence identity"
        )
    try:
        event = read_exact_material_result(ledger, event_identity)
    except (TypeError, ValueError) as error:
        raise OperatorCheckpointError(
            "checkpoint occurrence is absent or corrupted"
        ) from error
    if (
        event.kind != OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        or exact_material_result_bytes(event) not in _OPERATOR_CHECKPOINT_MATERIALS
    ):
        raise OperatorCheckpointError(
            "occurrence does not supply the exact checkpoint command"
        )
    return event
