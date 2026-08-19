"""Binary console streams for tests whose source witness is written as text."""

from __future__ import annotations

from io import BytesIO


class BinaryBoundaryInput(BytesIO):
    """Exact bytes plus the developer-written material supplied to the boundary."""

    def __init__(self, exact_bytes: bytes, supplied_material: str | None) -> None:
        super().__init__(exact_bytes)
        self.supplied_material = supplied_material


def binary_input(material: str | bytes) -> BinaryBoundaryInput:
    """Encode developer-written test material before it reaches the live boundary."""

    supplied_material = material if isinstance(material, str) else None
    if supplied_material is not None:
        material = supplied_material.encode("utf-8")
    return BinaryBoundaryInput(material, supplied_material)
