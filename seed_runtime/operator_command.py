"""Exact-byte routing for Seed slash commands through divided localities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial


COMMAND_ADDRESSED_KIND = "operator.command.addressed"
COMMAND_UNAVAILABLE_KIND = "operator.command.unavailable"


class OperatorCommandError(ValueError):
    """A slash-command frame or handler result is malformed."""


@dataclass(frozen=True)
class OperatorCommandFrame:
    """The exact parts of one slash-prefixed byte frame."""

    exact_bytes: bytes
    name: bytes
    arguments: bytes


@dataclass(frozen=True)
class AddressedOperatorCommand:
    addressed_event_id: str
    frame: OperatorCommandFrame


OperatorCommandHandler = Callable[[AddressedOperatorCommand], object]


@dataclass(frozen=True)
class OperatorCommandRun:
    addressed: AddressedOperatorCommand
    implementation_result: object


def is_slash_command(material: OperatorBoundaryMaterial) -> bool:
    """Return whether the exact frame addresses the slash-command boundary."""

    return not material.eof and material.exact_bytes.startswith(b"/")


def parse_slash_command(material: OperatorBoundaryMaterial) -> OperatorCommandFrame:
    """Split the slash name from its still-uninterpreted argument bytes."""

    if not is_slash_command(material):
        raise OperatorCommandError("a slash-prefixed frame is required")
    exact = material.exact_bytes
    if exact.endswith(b"\r\n"):
        body = exact[:-2]
    elif exact.endswith(b"\n"):
        body = exact[:-1]
    else:
        body = exact
    addressed = body[1:]
    split_at = next(
        (index for index, byte in enumerate(addressed) if byte in (0x20, 0x09)),
        len(addressed),
    )
    return OperatorCommandFrame(
        exact_bytes=exact,
        name=addressed[:split_at],
        arguments=addressed[split_at + 1 :] if split_at < len(addressed) else b"",
    )


def run_operator_command(
    *,
    ledger: EventLedger,
    locality_id: str,
    addressed_at_representation_event_id: str,
    material: OperatorBoundaryMaterial,
    handlers: Mapping[bytes, OperatorCommandHandler],
) -> OperatorCommandRun:
    """Invoke one exact registered slash name in the supplied locality."""

    frame = parse_slash_command(material)
    if not isinstance(handlers, Mapping) or not all(
        type(name) is bytes and name and callable(handler)
        for name, handler in handlers.items()
    ):
        raise OperatorCommandError("command handlers require exact non-empty byte names")

    command_id = new_id("operator_command")
    addressed = ledger.append(
        COMMAND_ADDRESSED_KIND,
        {
            "command_id": command_id,
            "locality_id": locality_id,
            "addressed_at_representation_event_id": addressed_at_representation_event_id,
            "exact_bytes_hex": frame.exact_bytes.hex(),
            "command_name_hex": frame.name.hex(),
            "argument_bytes_hex": frame.arguments.hex(),
            "authority": "unestablished",
            "unknowns": [
                "operator intent beyond addressing this slash name remains Unknown"
            ],
        },
        locality_id=locality_id,
    )
    ledger.flush()
    addressed_command = AddressedOperatorCommand(
        addressed_event_id=addressed.id,
        frame=frame,
    )
    handler = handlers.get(frame.name)
    if handler is None:
        ledger.append(
            COMMAND_UNAVAILABLE_KIND,
            {
                "command_id": command_id,
                "addressed_event_id": addressed.id,
                "command_name_hex": frame.name.hex(),
                "authority": "unestablished",
            },
            locality_id=locality_id,
        )
        return OperatorCommandRun(
            addressed=addressed_command,
            implementation_result=None,
        )

    implementation_result = handler(addressed_command)
    return OperatorCommandRun(
        addressed=addressed_command,
        implementation_result=implementation_result,
    )
