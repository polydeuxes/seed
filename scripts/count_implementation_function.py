#!/usr/bin/env python3

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class CountInvocationOccurrence:
    exact_material: bytes
    addressed_material: bytes
    returned_count: int
    returned_material: bytes

    @property
    def coordinates(self) -> tuple[int, bytes]:
        return (self.returned_count, self.returned_material)


def interrogate_count(
    exact_material: bytes, addressed_material: bytes
) -> CountInvocationOccurrence:
    if type(exact_material) is not bytes:
        raise TypeError("exact material must be bytes")
    if type(addressed_material) is not bytes or len(addressed_material) != 1:
        raise TypeError("addressed material must be one byte")
    implementation_function = Counter(exact_material)
    return CountInvocationOccurrence(
        exact_material=exact_material,
        addressed_material=addressed_material,
        returned_count=implementation_function[addressed_material[0]],
        returned_material=bytes(implementation_function),
    )
