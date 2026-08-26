"""Exact-byte routing for Seed slash commands through divided localities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from seed_runtime.identities import new_identity
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial


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
    command_identity: str
    locality_identity: str
    addressed_through_event_occurrence_identity: str
    frame: OperatorCommandFrame


OperatorCommandHandler = Callable[[AddressedOperatorCommand], object]


@dataclass(frozen=True)
class OperatorCommandRun:
    addressed: AddressedOperatorCommand
    handler_result: object


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
    locality_identity: str,
    addressed_through_event_occurrence_identity: str,
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

    command_identity = new_identity("operator_command")
    addressed_command = AddressedOperatorCommand(
        command_identity=command_identity,
        locality_identity=locality_identity,
        addressed_through_event_occurrence_identity=(
            addressed_through_event_occurrence_identity
        ),
        frame=frame,
    )
    handler = handlers.get(frame.name)
    if handler is None:
        return OperatorCommandRun(
            addressed=addressed_command,
            handler_result=None,
        )

    handler_result = handler(addressed_command)
    return OperatorCommandRun(
        addressed=addressed_command,
        handler_result=handler_result,
    )
