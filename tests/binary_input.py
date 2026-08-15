"""Binary console streams for tests whose fixture source is written as text."""

from __future__ import annotations

from io import BytesIO


class BinaryFixtureInput(BytesIO):
    """Exact bytes plus the developer-written material that formed the fixture."""

    def __init__(self, exact_bytes: bytes, supplied_material: str | None) -> None:
        super().__init__(exact_bytes)
        self.supplied_material = supplied_material


def binary_input(material: str | bytes) -> BinaryFixtureInput:
    """Encode developer-written fixture text before it reaches the live boundary."""

    supplied_material = material if isinstance(material, str) else None
    if supplied_material is not None:
        material = supplied_material.encode("utf-8")
    return BinaryFixtureInput(material, supplied_material)
