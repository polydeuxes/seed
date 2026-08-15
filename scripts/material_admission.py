#!/usr/bin/env python3
"""Admit material through complete ordered-pair implementation-function coverage."""

from __future__ import annotations

from typing import Callable, Hashable, Iterable, Sequence

Material = Hashable
Admission = list[tuple[Material, ...]]
ImplementationFunction = Callable[[Material, Material], Hashable]


def one_admission(material: Iterable[Material]) -> Admission:
    return [tuple(material)]


def admission_by(
    key: Callable[[Material], Hashable], material: Iterable[Material]
) -> Admission:
    same_result: dict[Hashable, list[Material]] = {}
    for item in material:
        same_result.setdefault(key(item), []).append(item)
    return [tuple(found) for found in same_result.values()]


def _admit(first: Admission, implementation_function: ImplementationFunction) -> Admission:
    material = tuple(other for found in first for other in found)
    outgoing: list[list[Hashable]] = [[] for _ in material]
    incoming: list[list[Hashable]] = [[] for _ in material]
    for first_position, first_material in enumerate(material):
        for second_position, second_material in enumerate(material):
            result = implementation_function(first_material, second_material)
            outgoing[first_position].append(result)
            incoming[second_position].append(result)
    admitted: Admission = []
    position = 0
    for material_at_one_coordinate in first:
        same_result: dict[Hashable, list[Material]] = {}
        for item in material_at_one_coordinate:
            complete = (tuple(outgoing[position]), tuple(incoming[position]))
            same_result.setdefault(complete, []).append(item)
            position += 1
        admitted.extend(tuple(found) for found in same_result.values())
    return admitted


def admit(first: Admission, implementation_function: ImplementationFunction) -> list[Admission]:
    admitted = _admit(first, implementation_function)
    return [first] if len(admitted) == len(first) else [first, admitted]


def admission_counts(admissions: Sequence[Admission]) -> list[int]:
    return [len(admission) for admission in admissions]


def not_distinguished(admissions: Sequence[Admission]) -> list[tuple[Material, ...]]:
    return [material for material in admissions[-1] if len(material) > 1]


def preserves(
    first: Iterable[Iterable[Material]], second: Iterable[Iterable[Material]]
) -> bool:
    second_coordinates = tuple(tuple(material) for material in second)
    coordinates_by_material: dict[Material, set[int]] = {}
    for coordinate, material in enumerate(second_coordinates):
        for item in material:
            coordinates_by_material.setdefault(item, set()).add(coordinate)

    for material in first:
        possible: set[int] | None = None
        for item in material:
            item_coordinates = coordinates_by_material.get(item)
            if not item_coordinates:
                return False
            if possible is None:
                possible = set(item_coordinates)
            else:
                possible.intersection_update(item_coordinates)
            if not possible:
                return False
        if possible is None and not second_coordinates:
            return False
    return True
