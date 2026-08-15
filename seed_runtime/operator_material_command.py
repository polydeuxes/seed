"""Exact `/material` request bytes."""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.operator_command import AddressedOperatorCommand


@dataclass(frozen=True)
class OperatorMaterialRequest:
    path_bytes: bytes


def request_operator_material(
    addressed: AddressedOperatorCommand,
) -> OperatorMaterialRequest:
    if not isinstance(addressed, AddressedOperatorCommand):
        raise TypeError("material control requires one addressed command")
    return OperatorMaterialRequest(path_bytes=addressed.frame.arguments)
