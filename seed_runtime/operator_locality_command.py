from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.operator_command import AddressedOperatorCommand
from seed_runtime.identities import new_identity


@dataclass(frozen=True)
class OperatorLocalityRequest:
    locality_identity: str


def request_operator_locality(command: AddressedOperatorCommand) -> OperatorLocalityRequest:
    argument = command.frame.arguments
    if argument:
        raise ValueError("/locality accepts no material")
    return OperatorLocalityRequest(locality_identity=new_identity("locality"))
