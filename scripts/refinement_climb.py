#!/usr/bin/env python3
"""Refine one material Locality through complete ordered-pair witness coverage."""

from __future__ import annotations

from typing import Callable, Hashable, Iterable, Sequence

Material = Hashable
MaterialLocality = list[tuple[Material, ...]]
Witness = Callable[[Material, Material], Hashable]


def one_material_locality(material: Iterable[Material]) -> MaterialLocality:
    return [tuple(material)]


def by(key: Callable[[Material], Hashable], material: Iterable[Material]) -> MaterialLocality:
    grouped: dict[Hashable, list[Material]] = {}
    for item in material:
        grouped.setdefault(key(item), []).append(item)
    return [tuple(material) for material in grouped.values()]


def refine(locality: MaterialLocality, witness: Witness) -> MaterialLocality:
    material = tuple(other for found in locality for other in found)
    observed = {
        (first, second): witness(first, second)
        for first in material
        for second in material
    }
    refined: MaterialLocality = []
    for material_at_one_coordinate in locality:
        grouped: dict[Hashable, list[Material]] = {}
        for item in material_at_one_coordinate:
            complete = (
                tuple(observed[item, other] for other in material),
                tuple(observed[other, item] for other in material),
            )
            grouped.setdefault(complete, []).append(item)
        refined.extend(tuple(split) for split in grouped.values())
    return refined


def climb(first: MaterialLocality, witness: Witness) -> list[MaterialLocality]:
    nxt = refine(first, witness)
    return [first] if len(nxt) == len(first) else [first, nxt]


def heights(localities: Sequence[MaterialLocality]) -> list[int]:
    return [len(locality) for locality in localities]


def unseparated(localities: Sequence[MaterialLocality]) -> list[tuple[Material, ...]]:
    return [material for material in localities[-1] if len(material) > 1]
