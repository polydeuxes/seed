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
        addressed_at_representation_event_identity="representation",
        frame=OperatorCommandFrame(b"/locality " + arguments, b"locality", arguments),
    )


def test_locality_command_preserves_one_exact_identity():
    request = request_operator_locality(_command(b"session_123"))
    assert request.locality_identity == "session_123"


def test_locality_list_is_a_separate_command_result():
    assert request_operator_locality(_command(b"list")).locality_identity is None


@pytest.mark.parametrize("arguments", (b"", b"a b", b"\xff"))
def test_locality_command_refuses_non_exact_identity(arguments):
    with pytest.raises(ValueError):
        request_operator_locality(_command(arguments))
