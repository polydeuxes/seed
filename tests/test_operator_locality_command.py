from __future__ import annotations

import pytest


from seed_runtime.operator_command import (
    AddressedOperatorCommand,
    OperatorCommandFrame,
)
from seed_runtime.operator_locality_command import request_operator_locality


def _command(arguments: bytes) -> AddressedOperatorCommand:
    return AddressedOperatorCommand(
        command_identity="command",
        locality_identity="current",
        addressed_at_standing_boundary_event_identity="boundary",
        frame=OperatorCommandFrame(b"/locality " + arguments, b"locality", arguments),
    )


def test_locality_without_an_argument_creates_one():
    request = request_operator_locality(_command(b""))
    assert request.locality_identity.startswith("locality_")


@pytest.mark.parametrize("arguments", (b"session_123", b"list", b"a b", b"\xff"))
def test_locality_command_refuses_supplied_material(arguments):
    with pytest.raises(ValueError, match="accepts no material"):
        request_operator_locality(_command(arguments))
