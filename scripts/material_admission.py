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
