"""Exact console control for one Locality continuation request.

``memory`` is operator shorthand only.  The resulting request carries no
priority, importance, represented content, or Seed-native relation name.
"""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.operator_command import AddressedOperatorCommand


@dataclass(frozen=True)
class OperatorMemoryRequest:
    pass


def request_operator_memory(
    addressed: AddressedOperatorCommand,
) -> OperatorMemoryRequest:
    if not isinstance(addressed, AddressedOperatorCommand):
        raise TypeError("memory control requires one addressed command")
    if addressed.frame.exact_bytes not in {
        b"/memory",
        b"/memory\n",
        b"/memory\r\n",
    }:
        raise ValueError("/memory accepts no material")
    return OperatorMemoryRequest()
