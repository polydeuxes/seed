"""Exact-byte routing for Seed slash commands through divided localities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_ingress_representation import CapturedOperatorMaterial


COMMAND_ADDRESSED_KIND = "operator.command.addressed"
COMMAND_COMPLETED_KIND = "operator.command.completed"
COMMAND_UNAVAILABLE_KIND = "operator.command.unavailable"


class OperatorCommandError(ValueError):
    """A slash-command frame or handler result is malformed."""


@dataclass(frozen=True)
class OperatorCommandFrame:
    """The exact mechanical parts of one slash-prefixed byte frame."""

    exact_bytes: bytes
    name: bytes
    arguments: bytes


@dataclass(frozen=True)
class OperatorCommandContext:
    ledger: EventLedger
    workspace_id: str
    locality_id: str
    command_id: str
    addressed_event_id: str
    addressed_at_representation_event_id: str
    frame: OperatorCommandFrame


OperatorCommandHandler = Callable[[OperatorCommandContext], object]


@dataclass(frozen=True)
class OperatorCommandRun:
    """Mechanical command routing plus an unconstrained implementation result."""

    frame: OperatorCommandFrame
    locality_id: str
    addressed_event_id: str
    implementation_result: object


def is_slash_command(captured: CapturedOperatorMaterial) -> bool:
    """Return whether the exact frame addresses the slash-command boundary."""

    return not captured.eof and captured.exact_bytes.startswith(b"/")


def parse_slash_command(captured: CapturedOperatorMaterial) -> OperatorCommandFrame:
    """Split the slash name from its still-uninterpreted argument bytes."""

    if not is_slash_command(captured):
        raise OperatorCommandError("a slash-prefixed frame is required")
    material = captured.exact_bytes
    if material.endswith(b"\r\n"):
        body = material[:-2]
    elif material.endswith(b"\n"):
        body = material[:-1]
    else:
        body = material
    addressed = body[1:]
    split_at = next(
        (index for index, byte in enumerate(addressed) if byte in (0x20, 0x09)),
        len(addressed),
    )
    return OperatorCommandFrame(
        exact_bytes=material,
        name=addressed[:split_at],
        arguments=addressed[split_at + 1 :] if split_at < len(addressed) else b"",
    )


def run_operator_command(
    *,
    ledger: EventLedger,
    workspace_id: str,
    locality_id: str,
    addressed_at_representation_event_id: str,
    captured: CapturedOperatorMaterial,
    handlers: Mapping[bytes, OperatorCommandHandler],
) -> OperatorCommandRun:
    """Invoke one exact registered slash name in the supplied locality.

    Name selection compares bytes. Argument bytes remain bytes and are supplied
    to the selected implementation function without converting the material.
    Locality division is not implied by the slash prefix; `/checkpoint` owns
    that external operator control explicitly.
    """

    frame = parse_slash_command(captured)
    if not isinstance(handlers, Mapping) or not all(
        type(name) is bytes and name and callable(handler)
        for name, handler in handlers.items()
    ):
        raise OperatorCommandError("command handlers require exact non-empty byte names")

    command_id = new_id("operator_command")
    addressed = ledger.append(
        COMMAND_ADDRESSED_KIND,
        workspace_id,
        {
            "command_id": command_id,
            "locality_id": locality_id,
            "addressed_at_representation_event_id": addressed_at_representation_event_id,
            "exact_bytes_hex": frame.exact_bytes.hex(),
            "command_name_hex": frame.name.hex(),
            "argument_bytes_hex": frame.arguments.hex(),
            "standing": "addressed",
            "authority": "unestablished",
            "unknowns": [
                "operator intent beyond addressing this slash name remains Unknown"
            ],
        },
        locality_id=locality_id,
    )
    ledger.flush()
    handler = handlers.get(frame.name)
    if handler is None:
        ledger.append(
            COMMAND_UNAVAILABLE_KIND,
            workspace_id,
            {
                "command_id": command_id,
                "addressed_event_id": addressed.id,
                "command_name_hex": frame.name.hex(),
                "standing": "no registered implementation function",
                "authority": "unestablished",
            },
            locality_id=locality_id,
        )
        return OperatorCommandRun(
            frame=frame,
            locality_id=locality_id,
            addressed_event_id=addressed.id,
            implementation_result=None,
        )

    implementation_result = handler(
        OperatorCommandContext(
            ledger=ledger,
            workspace_id=workspace_id,
            locality_id=locality_id,
            command_id=command_id,
            addressed_event_id=addressed.id,
            addressed_at_representation_event_id=addressed_at_representation_event_id,
            frame=frame,
        )
    )
    ledger.append(
        COMMAND_COMPLETED_KIND,
        workspace_id,
        {
            "command_id": command_id,
            "addressed_event_id": addressed.id,
            "command_name_hex": frame.name.hex(),
            "standing": "implementation function returned",
            "authority": "unestablished",
        },
        locality_id=locality_id,
    )
    return OperatorCommandRun(
        frame=frame,
        locality_id=locality_id,
        addressed_event_id=addressed.id,
        implementation_result=implementation_result,
    )
