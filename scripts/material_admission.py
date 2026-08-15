#!/usr/bin/env python3
"""Admit material through every ordered implementation-function pair."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Hashable, Iterable, Protocol, Sequence, runtime_checkable

Material = Hashable
Admission = list[tuple[Material, ...]]
ImplementationFunction = Callable[[Material, Material], Hashable]


@runtime_checkable
class AdmissionOccurrenceCoordinates(Protocol):
    @property
    def act_occurrence_identity(self) -> tuple[str, int]: ...

    @property
    def result_identity(self) -> tuple[str, int, str]: ...

    @property
    def source_material(self) -> tuple[Material, ...]: ...

    @property
    def admitted_material(self) -> tuple[tuple[Material, ...], ...]: ...


def _exact_admitted_material(
    admitted_material: tuple[tuple[Material, ...], ...],
) -> tuple[Material, ...]:
    if (
        type(admitted_material) is not tuple
        or not admitted_material
        or any(
            type(material) is not tuple or not material
            for material in admitted_material
        )
    ):
        raise TypeError("Admission result requires exact admitted material tuples")
    material = tuple(item for admitted in admitted_material for item in admitted)
    if len(set(material)) != len(material):
        raise ValueError("one material occurrence entered Admission more than once")
    return material


@dataclass(frozen=True, slots=True)
class AdmissionResultReference:
    admission_occurrence: AdmissionOccurrenceCoordinates

    def __post_init__(self) -> None:
        if not isinstance(
            self.admission_occurrence, AdmissionOccurrenceCoordinates
        ):
            raise TypeError("Admission result requires its exact Act occurrence")

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return self.admission_occurrence.act_occurrence_identity

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return self.admission_occurrence.result_identity

    @property
    def source_material(self) -> tuple[Material, ...]:
        return self.admission_occurrence.source_material

    @property
    def admitted_material(self) -> tuple[tuple[Material, ...], ...]:
        return self.admission_occurrence.admitted_material


@dataclass(frozen=True, slots=True)
class AdmissionOccurrence:
    boundary_identity: str
    occurrence_position: int
    source_material: tuple[Material, ...]
    admitted_material: tuple[tuple[Material, ...], ...]

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact Admission occurrence position is required")
        admitted = _exact_admitted_material(self.admitted_material)
        if (
            type(self.source_material) is not tuple
            or len(set(self.source_material)) != len(self.source_material)
            or frozenset(admitted) != frozenset(self.source_material)
        ):
            raise ValueError("Admission result differs from its exact source material")

    @property
    def act_identity(self) -> tuple[str, str]:
        return (self.boundary_identity, "Admission")

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return (self.boundary_identity, self.occurrence_position)

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return (self.boundary_identity, self.occurrence_position, "result")

    @property
    def result_reference(self) -> AdmissionResultReference:
        return AdmissionResultReference(admission_occurrence=self)


@dataclass(frozen=True, slots=True)
class AdmissionCompareResultReference:
    compare_occurrence: "AdmissionCompareOccurrence"

    def __post_init__(self) -> None:
        if not isinstance(self.compare_occurrence, AdmissionCompareOccurrence):
            raise TypeError("Compare result requires its exact Act occurrence")

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return self.compare_occurrence.act_occurrence_identity

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return self.compare_occurrence.result_identity

    @property
    def first_reference(self) -> AdmissionResultReference:
        return self.compare_occurrence.first_reference

    @property
    def second_reference(self) -> AdmissionResultReference:
        return self.compare_occurrence.second_reference

    @property
    def result(self) -> bool:
        return self.compare_occurrence.result


@dataclass(frozen=True, slots=True)
class AdmissionCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    first_reference: AdmissionResultReference
    second_reference: AdmissionResultReference
    result: bool

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact Compare occurrence position is required")
        if not isinstance(
            self.first_reference, AdmissionResultReference
        ) or not isinstance(self.second_reference, AdmissionResultReference):
            raise TypeError("Compare requires exact Admission result references")
        if self.first_reference == self.second_reference:
            raise ValueError("one Admission result cannot be compared with itself")
        if (
            self.first_reference.source_material
            != self.second_reference.source_material
        ):
            raise ValueError("Compare requires the same exact material occurrences")
        if type(self.result) is not bool or self.result != preserves(
            self.first_reference.admitted_material,
            self.second_reference.admitted_material,
        ):
            raise ValueError("Compare result differs from its exact Admission results")

    @property
    def act_identity(self) -> tuple[str, str]:
        return (self.boundary_identity, "Compare")

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return (self.boundary_identity, self.occurrence_position)

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return (self.boundary_identity, self.occurrence_position, "result")

    @property
    def result_reference(self) -> AdmissionCompareResultReference:
        return AdmissionCompareResultReference(compare_occurrence=self)


def one_admission(material: Iterable[Material]) -> Admission:
    return [tuple(material)]


def admission_by(
    key: Callable[[Material], Hashable], material: Iterable[Material]
) -> Admission:
    same_result: dict[Hashable, list[Material]] = {}
    for item in material:
        same_result.setdefault(key(item), []).append(item)
    return [tuple(found) for found in same_result.values()]


def _admit(
    first: Admission, implementation_function: ImplementationFunction
) -> Admission:
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
            coordinates = (tuple(outgoing[position]), tuple(incoming[position]))
            same_result.setdefault(coordinates, []).append(item)
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


def admission_occurrence(
    admission: Iterable[Iterable[Material]],
    *,
    boundary_identity: str,
    occurrence_position: int = 0,
    source_material: tuple[Material, ...] | None = None,
) -> AdmissionOccurrence:
    admitted_material = tuple(tuple(material) for material in admission)
    return AdmissionOccurrence(
        boundary_identity=boundary_identity,
        occurrence_position=occurrence_position,
        source_material=(
            source_material
            if source_material is not None
            else _exact_admitted_material(admitted_material)
        ),
        admitted_material=admitted_material,
    )


def compare_admission_results(
    first_reference: AdmissionResultReference,
    second_reference: AdmissionResultReference,
    *,
    boundary_identity: str,
    occurrence_position: int = 0,
) -> AdmissionCompareOccurrence:
    return AdmissionCompareOccurrence(
        boundary_identity=boundary_identity,
        occurrence_position=occurrence_position,
        first_reference=first_reference,
        second_reference=second_reference,
        result=preserves(
            first_reference.admitted_material,
            second_reference.admitted_material,
        ),
    )


def compare_admission_result_pairs(
    references: tuple[AdmissionResultReference, ...],
    *,
    boundary_identity: str,
) -> tuple[AdmissionCompareOccurrence, ...]:
    if (
        type(references) is not tuple
        or len(references) < 2
        or any(not isinstance(reference, AdmissionResultReference) for reference in references)
    ):
        raise TypeError("Compare requires exact Admission result references")
    result_identities = tuple(reference.result_identity for reference in references)
    if len(set(result_identities)) != len(result_identities):
        raise ValueError("one Admission result entered Compare twice")
    return tuple(
        compare_admission_results(
            first,
            second,
            boundary_identity=boundary_identity,
            occurrence_position=position,
        )
        for position, (first, second) in enumerate(
            (first, second)
            for first in references
            for second in references
            if first is not second
        )
    )
