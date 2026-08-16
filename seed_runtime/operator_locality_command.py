from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.operator_command import AddressedOperatorCommand
from seed_runtime.identities import new_identity


@dataclass(frozen=True)
class OperatorLocalityRequest:
    locality_identity: str | None
    create_new: bool = False


def request_operator_locality(command: AddressedOperatorCommand) -> OperatorLocalityRequest:
    argument = command.frame.arguments
    if not argument:
        return OperatorLocalityRequest(
            locality_identity=new_identity("locality"),
            create_new=True,
        )
    if argument == b"list":
        return OperatorLocalityRequest(locality_identity=None)
    try:
        locality_identity = argument.decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError("/locality requires an ASCII Locality identity") from error
    if not locality_identity or any(byte in locality_identity for byte in " \t\r\n"):
        raise ValueError("/locality requires one exact Locality identity")
    return OperatorLocalityRequest(locality_identity=locality_identity)
