"""Exact operator control selecting one bounded branch creation."""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.operator_command import AddressedOperatorCommand


@dataclass(frozen=True)
class OperatorCheckoutRequest:
    pass


def request_operator_checkout(
    addressed: AddressedOperatorCommand,
) -> OperatorCheckoutRequest:
    if not isinstance(addressed, AddressedOperatorCommand):
        raise TypeError("checkout control requires one addressed command")
    if addressed.frame.exact_bytes not in {
        b"/checkout",
        b"/checkout\n",
        b"/checkout\r\n",
    }:
        raise ValueError("/checkout accepts no material")
    return OperatorCheckoutRequest()
