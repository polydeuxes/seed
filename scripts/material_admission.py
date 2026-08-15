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
    results = {
        (first, second): implementation_function(first, second)
        for first in material
        for second in material
    }
    admitted: Admission = []
    for material_at_one_coordinate in first:
        same_result: dict[Hashable, list[Material]] = {}
        for item in material_at_one_coordinate:
            complete = (
                tuple(results[item, other] for other in material),
                tuple(results[other, item] for other in material),
            )
            same_result.setdefault(complete, []).append(item)
        admitted.extend(tuple(found) for found in same_result.values())
    return admitted


def admit(first: Admission, implementation_function: ImplementationFunction) -> list[Admission]:
    admitted = _admit(first, implementation_function)
    return [first] if len(admitted) == len(first) else [first, admitted]


def admission_counts(admissions: Sequence[Admission]) -> list[int]:
    return [len(admission) for admission in admissions]


def not_distinguished(admissions: Sequence[Admission]) -> list[tuple[Material, ...]]:
    return [material for material in admissions[-1] if len(material) > 1]
