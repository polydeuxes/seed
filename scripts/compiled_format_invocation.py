#!/usr/bin/env python3

from __future__ import annotations

import ast
from dataclasses import dataclass
import io
import json
import plistlib
import tomllib
from typing import Callable, Protocol, runtime_checkable
import xml.etree.ElementTree

from material_admission import (
    AdmissionOccurrence,
    AdmissionResultReference,
    admission_occurrence,
)


@dataclass(frozen=True)
class CompiledImplementationFunction:
    identity: str
    invocation: Callable[[bytes], object]

    def __post_init__(self) -> None:
        if type(self.identity) is not str or not self.identity:
            raise TypeError("one exact implementation function identity is required")
        if not callable(self.invocation):
            raise TypeError("one exact implementation function is required")


@runtime_checkable
class ExactMaterialCoordinates(Protocol):
    exact_material: bytes


@dataclass(frozen=True, slots=True)
class ExactMaterialReference:
    recorded_occurrence_identity: str
    assertion_identity: str
    exact_material: bytes

    def __post_init__(self) -> None:
        if (
            type(self.recorded_occurrence_identity) is not str
            or not self.recorded_occurrence_identity
            or type(self.assertion_identity) is not str
            or not self.assertion_identity
            or type(self.exact_material) is not bytes
        ):
            raise TypeError("exact material requires its occurrence-bound Assertion reference")


@dataclass(frozen=True, slots=True)
class ExactMaterialResultReference:
    act_occurrence_identity: tuple[str, int]
    result_identity: tuple[str, int, str]
    exact_material: bytes

    def __post_init__(self) -> None:
        if (
            type(self.act_occurrence_identity) is not tuple
            or len(self.act_occurrence_identity) != 2
            or type(self.act_occurrence_identity[0]) is not str
            or type(self.act_occurrence_identity[1]) is not int
            or type(self.result_identity) is not tuple
            or len(self.result_identity) != 3
            or self.result_identity[:2] != self.act_occurrence_identity
            or self.result_identity[2] != "result"
            or type(self.exact_material) is not bytes
        ):
            raise TypeError("exact material result requires its Act occurrence and result identity")


@dataclass(frozen=True, slots=True)
class CompiledInvocationResultReference:
    invocation_occurrence: "CompiledInvocationOccurrence"

    def __post_init__(self) -> None:
        if not isinstance(self.invocation_occurrence, CompiledInvocationOccurrence):
            raise TypeError("invocation result requires its exact Act occurrence")

    @property
    def act_occurrence_identity(self) -> tuple[str, str, int]:
        return self.invocation_occurrence.occurrence_identity

    @property
    def result_identity(self) -> tuple[str, str, int, str]:
        return (*self.act_occurrence_identity, "result")

    @property
    def coordinates(self) -> bool:
        return self.invocation_occurrence.returned


@dataclass(frozen=True, slots=True)
class AddedPositionOccurrence:
    boundary_identity: str
    occurrence_position: int
    source_reference: ExactMaterialReference | ExactMaterialResultReference
    position: int
    added_reference: ExactMaterialReference
    result_material: bytes

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact Act occurrence position is required")
        if not isinstance(
            self.source_reference,
            (ExactMaterialReference, ExactMaterialResultReference),
        ):
            raise TypeError("source material requires its exact reference")
        if not isinstance(self.added_reference, ExactMaterialReference):
            raise TypeError("added material requires its exact reference")
        if len(self.added_reference.exact_material) != 1:
            raise ValueError("added material must be exactly one byte")
        if not preserves_original_order(
            source_material=self.source_reference.exact_material,
            result_material=self.result_material,
            added_position=self.position,
        ):
            raise ValueError("result material does not preserve its exact source order")
        if self.result_material[self.position : self.position + 1] != self.added_material:
            raise ValueError("result material does not carry the exact added material")

    @property
    def act_identity(self) -> tuple[str, str]:
        return (self.boundary_identity, "add exact material at exact position")

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return (self.boundary_identity, self.occurrence_position)

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return (self.boundary_identity, self.occurrence_position, "result")

    @property
    def result_reference(self) -> ExactMaterialResultReference:
        return ExactMaterialResultReference(
            act_occurrence_identity=self.act_occurrence_identity,
            result_identity=self.result_identity,
            exact_material=self.result_material,
        )

    @property
    def source_material(self) -> bytes:
        return self.source_reference.exact_material

    @property
    def added_material(self) -> bytes:
        return self.added_reference.exact_material


@dataclass(frozen=True, slots=True)
class RemovedPositionOccurrence:
    boundary_identity: str
    occurrence_position: int
    source_reference: ExactMaterialReference
    position: int
    removed_reference: ExactMaterialReference
    result_material: bytes

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact Act occurrence position is required")
        if not isinstance(self.source_reference, ExactMaterialReference):
            raise TypeError("source material requires its exact reference")
        if not isinstance(self.removed_reference, ExactMaterialReference):
            raise TypeError("removed material requires its exact reference")
        if len(self.removed_reference.exact_material) != 1:
            raise ValueError("removed material must be exactly one byte")
        if (
            type(self.position) is not int
            or self.position < 0
            or self.position >= len(self.source_material)
            or self.source_material[self.position : self.position + 1]
            != self.removed_material
            or self.result_material
            != self.source_material[: self.position]
            + self.source_material[self.position + 1 :]
        ):
            raise ValueError("result material does not preserve the exact removal")

    @property
    def act_identity(self) -> tuple[str, str]:
        return (self.boundary_identity, "remove exact material at exact position")

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return (self.boundary_identity, self.occurrence_position)

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return (self.boundary_identity, self.occurrence_position, "result")

    @property
    def result_reference(self) -> ExactMaterialResultReference:
        return ExactMaterialResultReference(
            act_occurrence_identity=self.act_occurrence_identity,
            result_identity=self.result_identity,
            exact_material=self.result_material,
        )

    @property
    def source_material(self) -> bytes:
        return self.source_reference.exact_material

    @property
    def removed_material(self) -> bytes:
        return self.removed_reference.exact_material


@dataclass(frozen=True, slots=True)
class CompiledInvocationOccurrence:
    boundary_identity: str
    invocation_position: int
    exact_material: bytes
    implementation_function: CompiledImplementationFunction
    returned: bool
    source_coordinate: (
        ExactMaterialCoordinates
        | AddedPositionOccurrence
        | RemovedPositionOccurrence
        | None
    ) = None

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.invocation_position) is not int or self.invocation_position < 0:
            raise TypeError("one exact invocation position is required")
        if type(self.exact_material) is not bytes:
            raise TypeError("implementation function material must be exact bytes")
        if not isinstance(
            self.implementation_function, CompiledImplementationFunction
        ):
            raise TypeError("one exact compiled implementation function is required")
        if type(self.returned) is not bool:
            raise TypeError("returned coordinate must be exact")
        if self.source_coordinate is not None:
            if isinstance(self.source_coordinate, ExactMaterialCoordinates):
                source_material = self.source_coordinate.exact_material
            elif isinstance(
                self.source_coordinate,
                (AddedPositionOccurrence, RemovedPositionOccurrence),
            ):
                source_material = self.source_coordinate.result_material
            else:
                raise TypeError("source material requires its exact reference")
            if source_material != self.exact_material:
                raise ValueError("invocation material differs from its exact source")

    @property
    def implementation_function_identity(self) -> str:
        return self.implementation_function.identity

    @property
    def result_identity(self) -> tuple[str, str, int, str]:
        return (*self.occurrence_identity, "result")

    @property
    def result_reference(self) -> CompiledInvocationResultReference:
        return CompiledInvocationResultReference(invocation_occurrence=self)

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.implementation_function_identity,
            self.invocation_position,
        )

    @property
    def source_material(self) -> bytes | None:
        if isinstance(self.source_coordinate, ExactMaterialCoordinates):
            return self.source_coordinate.exact_material
        if isinstance(self.source_coordinate, AddedPositionOccurrence):
            return self.source_coordinate.source_material
        if isinstance(self.source_coordinate, RemovedPositionOccurrence):
            return self.source_coordinate.source_material
        return None

    @property
    def added_position(self) -> int | None:
        return (
            self.source_coordinate.position
            if isinstance(self.source_coordinate, AddedPositionOccurrence)
            else None
        )

    @property
    def added_material(self) -> bytes | None:
        return (
            self.source_coordinate.added_material
            if isinstance(self.source_coordinate, AddedPositionOccurrence)
            else None
        )


@dataclass(frozen=True, slots=True)
class AddedPositionCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    implementation_function_identity: str
    added_position_act_occurrence_identity: tuple[str, int]
    source_invocation_occurrence_identity: tuple[str, str, int]
    result_invocation_occurrence_identity: tuple[str, str, int]
    source_returned: bool
    result_returned: bool

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.implementation_function_identity,
            self.occurrence_position,
        )

    @property
    def distinction(self) -> bool:
        return self.source_returned != self.result_returned


@dataclass(frozen=True, slots=True)
class AddedPositionPairCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    source_reference: ExactMaterialReference | ExactMaterialResultReference
    added_reference: ExactMaterialReference
    first_position: int
    second_position: int
    first_added_position_act_occurrence_identity: tuple[str, int]
    second_added_position_act_occurrence_identity: tuple[str, int]
    first_compare_occurrence_identities: tuple[tuple[str, str, int], ...]
    second_compare_occurrence_identities: tuple[tuple[str, str, int], ...]
    first_returned_coordinates: tuple[tuple[str, bool, bool], ...]
    second_returned_coordinates: tuple[tuple[str, bool, bool], ...]

    @property
    def occurrence_identity(self) -> tuple[str, int]:
        return (self.boundary_identity, self.occurrence_position)

    @property
    def distinction(self) -> bool:
        return self.first_returned_coordinates != self.second_returned_coordinates


@dataclass(frozen=True, slots=True)
class RemovedPositionCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    implementation_function_identity: str
    removed_position_act_occurrence_identity: tuple[str, int]
    source_invocation_occurrence_identity: tuple[str, str, int]
    result_invocation_occurrence_identity: tuple[str, str, int]
    source_returned: bool
    result_returned: bool

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.implementation_function_identity,
            self.occurrence_position,
        )

    @property
    def distinction(self) -> bool:
        return self.source_returned != self.result_returned


@dataclass(frozen=True, slots=True)
class AddedPositionAdmissionOccurrence:
    admission_occurrence: AdmissionOccurrence
    addition_occurrences: tuple[AddedPositionOccurrence, ...]
    comparison_occurrences: tuple[tuple[AddedPositionCompareOccurrence, ...], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.admission_occurrence, AdmissionOccurrence):
            raise TypeError("addition Admission requires its exact Act occurrence")
        admitted = admit_added_position_occurrences(
            self.addition_occurrences,
            self.comparison_occurrences,
        )
        if self.admission_occurrence.source_material != self.addition_occurrences:
            raise ValueError("addition Admission source differs from its Act occurrences")
        if self.admission_occurrence.admitted_material != admitted:
            raise ValueError("addition Admission differs from its Compare occurrences")

    @property
    def source_material(self):
        return self.admission_occurrence.source_material

    @property
    def admitted_material(self):
        return self.admission_occurrence.admitted_material

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return self.admission_occurrence.act_occurrence_identity

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return self.admission_occurrence.result_identity

    @property
    def result_reference(self) -> AdmissionResultReference:
        return AdmissionResultReference(admission_occurrence=self)


@dataclass(frozen=True, slots=True)
class CompiledAdmissionOccurrence:
    admission_occurrence: AdmissionOccurrence
    invocation_result_references: tuple[CompiledInvocationResultReference, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.admission_occurrence, AdmissionOccurrence):
            raise TypeError("compiled Admission requires its exact Act occurrence")
        if (
            type(self.invocation_result_references) is not tuple
            or not self.invocation_result_references
            or any(
                not isinstance(reference, CompiledInvocationResultReference)
                for reference in self.invocation_result_references
            )
        ):
            raise TypeError("compiled Admission requires exact invocation results")
        invocations = tuple(
            reference.invocation_occurrence
            for reference in self.invocation_result_references
        )
        if len({invocation.implementation_function for invocation in invocations}) != 1:
            raise ValueError("one compiled Admission cannot cross implementation functions")
        source_material = tuple(invocation.source_coordinate for invocation in invocations)
        if any(source is None for source in source_material):
            raise ValueError("compiled Admission requires exact source references")
        if source_material != self.admission_occurrence.source_material:
            raise ValueError("compiled Admission source differs from its invocations")
        same_coordinates = {}
        for invocation in invocations:
            same_coordinates.setdefault(invocation.returned, []).append(
                invocation.source_coordinate
            )
        admitted = tuple(tuple(material) for material in same_coordinates.values())
        if admitted != self.admission_occurrence.admitted_material:
            raise ValueError("compiled Admission differs from its invocation results")

    @property
    def source_material(self):
        return self.admission_occurrence.source_material

    @property
    def admitted_material(self):
        return self.admission_occurrence.admitted_material

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return self.admission_occurrence.act_occurrence_identity

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return self.admission_occurrence.result_identity

    @property
    def result_reference(self) -> AdmissionResultReference:
        return AdmissionResultReference(admission_occurrence=self)


def _added_position_comparisons_by_occurrence(
    occurrences: tuple[AddedPositionOccurrence, ...],
    comparisons: tuple[tuple[AddedPositionCompareOccurrence, ...], ...],
) -> tuple[
    dict[tuple[str, int], AddedPositionOccurrence],
    dict[tuple[str, int], tuple[AddedPositionCompareOccurrence, ...]],
]:
    if type(occurrences) is not tuple or not occurrences:
        raise TypeError("Admission requires exact addition Act occurrences")
    if type(comparisons) is not tuple or not comparisons:
        raise TypeError("Admission requires exact Compare occurrence tuples")

    occurrence_by_identity: dict[tuple[str, int], AddedPositionOccurrence] = {}
    for occurrence in occurrences:
        if not isinstance(occurrence, AddedPositionOccurrence):
            raise TypeError("Admission requires exact addition Act occurrences")
        identity = occurrence.act_occurrence_identity
        if identity in occurrence_by_identity:
            raise ValueError("addition Act occurrence entered Admission twice")
        occurrence_by_identity[identity] = occurrence

    expected_identities = frozenset(occurrence_by_identity)
    comparisons_by_occurrence: dict[
        tuple[str, int], list[AddedPositionCompareOccurrence]
    ] = {
        identity: [] for identity in occurrence_by_identity
    }
    implementation_function_identities = set()
    for row in comparisons:
        if type(row) is not tuple or not row:
            raise TypeError("Admission requires exact Compare occurrence tuples")
        implementation_function_identity = row[0].implementation_function_identity
        if implementation_function_identity in implementation_function_identities:
            raise ValueError("implementation function entered Admission twice")
        implementation_function_identities.add(implementation_function_identity)

        comparison_by_identity = {}
        for comparison in row:
            if not isinstance(comparison, AddedPositionCompareOccurrence):
                raise TypeError("Admission requires exact addition Compare occurrences")
            if (
                comparison.implementation_function_identity
                != implementation_function_identity
            ):
                raise ValueError("one Compare tuple crossed implementation functions")
            identity = comparison.added_position_act_occurrence_identity
            if identity in comparison_by_identity:
                raise ValueError("addition Act occurrence entered one Compare tuple twice")
            if type(comparison.source_returned) is not bool or type(
                comparison.result_returned
            ) is not bool:
                raise TypeError("Compare returned coordinates must be exact booleans")
            comparison_by_identity[identity] = comparison

        if frozenset(comparison_by_identity) != expected_identities:
            raise ValueError("Compare tuple does not carry every addition Act occurrence")
        for identity in occurrence_by_identity:
            comparison = comparison_by_identity[identity]
            comparisons_by_occurrence[identity].append(comparison)

    return occurrence_by_identity, {
        identity: tuple(found)
        for identity, found in comparisons_by_occurrence.items()
    }


def admit_added_position_occurrences(
    occurrences: tuple[AddedPositionOccurrence, ...],
    comparisons: tuple[tuple[AddedPositionCompareOccurrence, ...], ...],
) -> tuple[tuple[AddedPositionOccurrence, ...], ...]:
    occurrence_by_identity, comparisons_by_occurrence = (
        _added_position_comparisons_by_occurrence(occurrences, comparisons)
    )

    same_coordinates: dict[
        tuple[tuple[str, bool, bool], ...], list[AddedPositionOccurrence]
    ] = {}
    for identity, occurrence in occurrence_by_identity.items():
        coordinates = tuple(
            (
                comparison.implementation_function_identity,
                comparison.source_returned,
                comparison.result_returned,
            )
            for comparison in comparisons_by_occurrence[identity]
        )
        same_coordinates.setdefault(coordinates, []).append(occurrence)
    return tuple(tuple(found) for found in same_coordinates.values())


def added_position_admission_occurrence(
    occurrences: tuple[AddedPositionOccurrence, ...],
    comparisons: tuple[tuple[AddedPositionCompareOccurrence, ...], ...],
    *,
    boundary_identity: str,
    occurrence_position: int = 0,
) -> AddedPositionAdmissionOccurrence:
    admitted = admit_added_position_occurrences(occurrences, comparisons)
    admission = admission_occurrence(
        admitted,
        boundary_identity=boundary_identity,
        occurrence_position=occurrence_position,
        source_material=occurrences,
    )
    return AddedPositionAdmissionOccurrence(
        admission_occurrence=admission,
        addition_occurrences=occurrences,
        comparison_occurrences=comparisons,
    )


def compare_added_position_pairs(
    occurrences: tuple[AddedPositionOccurrence, ...],
    comparisons: tuple[tuple[AddedPositionCompareOccurrence, ...], ...],
    *,
    boundary_identity: str,
) -> tuple[AddedPositionPairCompareOccurrence, ...]:
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    occurrence_by_identity, comparisons_by_occurrence = (
        _added_position_comparisons_by_occurrence(occurrences, comparisons)
    )
    same_material = {}
    for occurrence in occurrence_by_identity.values():
        same_material.setdefault(
            (occurrence.source_reference, occurrence.added_reference), []
        ).append(occurrence)

    found = []
    for material_at_positions in same_material.values():
        for first_offset, first in enumerate(material_at_positions):
            for second in material_at_positions[first_offset + 1 :]:
                first_comparisons = comparisons_by_occurrence[
                    first.act_occurrence_identity
                ]
                second_comparisons = comparisons_by_occurrence[
                    second.act_occurrence_identity
                ]
                found.append(
                    AddedPositionPairCompareOccurrence(
                        boundary_identity=boundary_identity,
                        occurrence_position=len(found),
                        source_reference=first.source_reference,
                        added_reference=first.added_reference,
                        first_position=first.position,
                        second_position=second.position,
                        first_added_position_act_occurrence_identity=(
                            first.act_occurrence_identity
                        ),
                        second_added_position_act_occurrence_identity=(
                            second.act_occurrence_identity
                        ),
                        first_compare_occurrence_identities=tuple(
                            comparison.occurrence_identity
                            for comparison in first_comparisons
                        ),
                        second_compare_occurrence_identities=tuple(
                            comparison.occurrence_identity
                            for comparison in second_comparisons
                        ),
                        first_returned_coordinates=tuple(
                            (
                                comparison.implementation_function_identity,
                                comparison.source_returned,
                                comparison.result_returned,
                            )
                            for comparison in first_comparisons
                        ),
                        second_returned_coordinates=tuple(
                            (
                                comparison.implementation_function_identity,
                                comparison.source_returned,
                                comparison.result_returned,
                            )
                            for comparison in second_comparisons
                        ),
                    )
                )
    return tuple(found)


def _a(material: bytes):
    return json.loads(material)


def _b(material: bytes):
    return tomllib.load(io.BytesIO(material))


def _c(material: bytes):
    return xml.etree.ElementTree.fromstring(material)


def _d(material: bytes):
    return ast.parse(material)


def _e(material: bytes):
    return plistlib.loads(material)


COMPILED_IMPLEMENTATION_FUNCTIONS = tuple(
    CompiledImplementationFunction(identity=f"compiled-{index}", invocation=invocation)
    for index, invocation in enumerate((_a, _b, _c, _d, _e))
)


def compiled_invocation(
    exact_material: bytes,
    implementation_function: CompiledImplementationFunction,
    *,
    boundary_identity: str,
    invocation_position: int = 0,
) -> CompiledInvocationOccurrence:
    if type(exact_material) is not bytes:
        raise TypeError("implementation function material must be exact bytes")
    if not isinstance(implementation_function, CompiledImplementationFunction):
        raise TypeError("one compiled implementation function is required")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(invocation_position) is not int or invocation_position < 0:
        raise TypeError("one exact invocation position is required")
    try:
        implementation_function.invocation(exact_material)
    except Exception:
        returned = False
    else:
        returned = True
    return CompiledInvocationOccurrence(
        boundary_identity=boundary_identity,
        invocation_position=invocation_position,
        exact_material=exact_material,
        implementation_function=implementation_function,
        returned=returned,
    )


def compiled_invocations(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[CompiledImplementationFunction, ...] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("implementation function inputs must be one exact tuple of bytes")
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("compiled implementation functions must be one nonempty tuple")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if not all(
        isinstance(implementation_function, CompiledImplementationFunction)
        for implementation_function in implementation_functions
    ):
        raise TypeError("compiled implementation functions must be exact")
    return _compiled_invocations(
        exact_materials,
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
    )


def compiled_reference_invocations(
    references: tuple[ExactMaterialCoordinates, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[
        CompiledImplementationFunction, ...
    ] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(references) is not tuple or not all(
        isinstance(reference, ExactMaterialCoordinates)
        for reference in references
    ):
        raise TypeError("implementation function inputs must carry exact references")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("compiled implementation functions must be one nonempty tuple")
    if not all(
        isinstance(implementation_function, CompiledImplementationFunction)
        for implementation_function in implementation_functions
    ):
        raise TypeError("compiled implementation functions must be exact")
    return _compiled_invocations(
        tuple(reference.exact_material for reference in references),
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
        source_coordinates=references,
    )


def _compiled_invocations(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[CompiledImplementationFunction, ...],
    source_coordinates: tuple[
        ExactMaterialCoordinates
        | AddedPositionOccurrence
        | RemovedPositionOccurrence,
        ...,
    ] | None = None,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    identities = tuple(
        implementation_function.identity
        for implementation_function in implementation_functions
    )
    if len(set(identities)) != len(identities):
        raise ValueError("implementation function identities must be distinct")
    found = []
    for implementation_function in implementation_functions:
        occurrences = []
        for invocation_position, material in enumerate(exact_materials):
            try:
                implementation_function.invocation(material)
            except Exception:
                returned = False
            else:
                returned = True
            occurrences.append(
                CompiledInvocationOccurrence(
                    boundary_identity=boundary_identity,
                    invocation_position=invocation_position,
                    exact_material=material,
                    implementation_function=implementation_function,
                    returned=returned,
                    source_coordinate=(
                        source_coordinates[invocation_position]
                        if source_coordinates is not None
                        else None
                    ),
                )
            )
        found.append(tuple(occurrences))
    return tuple(found)


def admit_compiled_invocation_occurrences(
    occurrences: tuple[CompiledInvocationOccurrence, ...],
    *,
    boundary_identity: str,
    occurrence_position: int = 0,
) -> CompiledAdmissionOccurrence:
    if type(occurrences) is not tuple or not occurrences or any(
        not isinstance(occurrence, CompiledInvocationOccurrence)
        for occurrence in occurrences
    ):
        raise TypeError("compiled Admission requires exact invocation occurrences")
    same_coordinates = {}
    for occurrence in occurrences:
        if occurrence.source_coordinate is None:
            raise ValueError("compiled Admission requires exact source references")
        same_coordinates.setdefault(occurrence.returned, []).append(
            occurrence.source_coordinate
        )
    admission = admission_occurrence(
        tuple(tuple(material) for material in same_coordinates.values()),
        boundary_identity=boundary_identity,
        occurrence_position=occurrence_position,
        source_material=tuple(
            occurrence.source_coordinate for occurrence in occurrences
        ),
    )
    return CompiledAdmissionOccurrence(
        admission_occurrence=admission,
        invocation_result_references=tuple(
            occurrence.result_reference for occurrence in occurrences
        ),
    )


def preserves_original_order(
    *,
    source_material: bytes,
    result_material: bytes,
    added_position: int,
) -> bool:
    if (
        type(source_material) is not bytes
        or type(result_material) is not bytes
        or type(added_position) is not int
        or added_position < 0
        or added_position >= len(result_material)
        or len(result_material) != len(source_material) + 1
    ):
        return False
    return (
        result_material[:added_position]
        + result_material[added_position + 1 :]
        == source_material
    )


def added_position_occurrences(
    source_material: tuple[
        ExactMaterialReference | ExactMaterialResultReference, ...
    ],
    added_material: tuple[ExactMaterialReference, ...],
    *,
    boundary_identity: str,
) -> tuple[AddedPositionOccurrence, ...]:
    if type(source_material) is not tuple or not all(
        isinstance(
            material,
            (ExactMaterialReference, ExactMaterialResultReference),
        )
        for material in source_material
    ):
        raise TypeError("source material must carry exact references")
    if type(added_material) is not tuple or not all(
        isinstance(material, ExactMaterialReference)
        and type(material.exact_material) is bytes
        and len(material.exact_material) == 1
        for material in added_material
    ):
        raise TypeError("added material must carry exact one-byte references")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    return tuple(
        AddedPositionOccurrence(
            boundary_identity=boundary_identity,
            occurrence_position=occurrence_position,
            source_reference=source,
            position=position,
            added_reference=added,
            result_material=bytes(
                (
                    *source.exact_material[:position],
                    *added.exact_material,
                    *source.exact_material[position:],
                )
            ),
        )
        for occurrence_position, (source, position, added) in enumerate(
            (source, position, added)
            for source in source_material
            for position in range(len(source.exact_material) + 1)
            for added in added_material
        )
    )


def added_position_invocations(
    occurrences: tuple[AddedPositionOccurrence, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[CompiledImplementationFunction, ...] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(occurrences) is not tuple:
        raise TypeError("added-position occurrences must be one exact tuple")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    exact_material = []
    for occurrence_position, occurrence in enumerate(occurrences):
        if not isinstance(occurrence, AddedPositionOccurrence):
            raise TypeError("added-position material requires its exact Act occurrence")
        source = occurrence.source_material
        position = occurrence.position
        added = occurrence.added_material
        material = occurrence.result_material
        if (
            occurrence.occurrence_position != occurrence_position
            or type(added) is not bytes
            or len(added) != 1
            or type(material) is not bytes
            or not preserves_original_order(
                source_material=source,
                result_material=material,
                added_position=position,
            )
            or material[position : position + 1] != added
        ):
            raise ValueError("result material does not preserve its exact source order")
        exact_material.append(material)
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("compiled implementation functions must be one nonempty tuple")
    if not all(
        isinstance(implementation_function, CompiledImplementationFunction)
        for implementation_function in implementation_functions
    ):
        raise TypeError("compiled implementation functions must be exact")
    return _compiled_invocations(
        tuple(exact_material),
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
        source_coordinates=occurrences,
    )


def removed_position_occurrences(
    source_material: tuple[ExactMaterialReference, ...],
    removed_material: tuple[ExactMaterialReference, ...],
    *,
    boundary_identity: str,
) -> tuple[RemovedPositionOccurrence, ...]:
    if type(source_material) is not tuple or not all(
        isinstance(material, ExactMaterialReference) for material in source_material
    ):
        raise TypeError("source material must carry exact references")
    if type(removed_material) is not tuple or not all(
        isinstance(material, ExactMaterialReference)
        and len(material.exact_material) == 1
        for material in removed_material
    ):
        raise TypeError("removed material must carry exact one-byte references")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    exact_coordinates = tuple(
        (source, position, removed)
        for source in source_material
        for position in range(len(source.exact_material))
        for removed in removed_material
        if source.exact_material[position : position + 1]
        == removed.exact_material
    )
    return tuple(
        RemovedPositionOccurrence(
            boundary_identity=boundary_identity,
            occurrence_position=occurrence_position,
            source_reference=source,
            position=position,
            removed_reference=removed,
            result_material=(
                source.exact_material[:position]
                + source.exact_material[position + 1 :]
            ),
        )
        for occurrence_position, (source, position, removed) in enumerate(
            exact_coordinates
        )
    )


def removed_position_invocations(
    occurrences: tuple[RemovedPositionOccurrence, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[
        CompiledImplementationFunction, ...
    ] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(occurrences) is not tuple or not all(
        isinstance(occurrence, RemovedPositionOccurrence)
        for occurrence in occurrences
    ):
        raise TypeError("removed-position material requires exact Act occurrences")
    if any(
        occurrence.occurrence_position != position
        for position, occurrence in enumerate(occurrences)
    ):
        raise ValueError("removed-position Act occurrence positions must remain exact")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("compiled implementation functions must be one nonempty tuple")
    if not all(
        isinstance(implementation_function, CompiledImplementationFunction)
        for implementation_function in implementation_functions
    ):
        raise TypeError("compiled implementation functions must be exact")
    return _compiled_invocations(
        tuple(occurrence.result_material for occurrence in occurrences),
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
        source_coordinates=occurrences,
    )


def compare_added_position_invocations(
    source_invocations: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    result_invocations: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
) -> tuple[tuple[AddedPositionCompareOccurrence, ...], ...]:
    if type(source_invocations) is not tuple or type(result_invocations) is not tuple:
        raise TypeError("Compare inputs must be exact invocation tuples")
    if len(source_invocations) != len(result_invocations):
        raise ValueError("Compare inputs require the same implementation functions")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    compared = []
    comparison_position = 0
    for source_row, result_row in zip(source_invocations, result_invocations):
        if not source_row or not result_row:
            raise ValueError("Compare inputs require invocation occurrences")
        implementation_function_identity = source_row[0].implementation_function_identity
        if (
            any(
                occurrence.implementation_function_identity
                != implementation_function_identity
                for occurrence in source_row
            )
            or any(
                occurrence.implementation_function_identity
                != implementation_function_identity
                for occurrence in result_row
            )
        ):
            raise ValueError("Compare inputs require the same implementation function")
        source_by_reference = {}
        for source_invocation in source_row:
            reference = source_invocation.source_coordinate
            if not isinstance(
                reference,
                (ExactMaterialReference, ExactMaterialResultReference),
            ):
                raise ValueError("source invocation requires its exact material reference")
            if reference in source_by_reference:
                raise ValueError("source material reference entered Compare twice")
            source_by_reference[reference] = source_invocation
        row = []
        for result_invocation in result_row:
            addition = result_invocation.source_coordinate
            if not isinstance(addition, AddedPositionOccurrence):
                raise ValueError("result invocation requires its exact addition occurrence")
            source_invocation = source_by_reference.get(addition.source_reference)
            if source_invocation is None:
                raise ValueError("addition occurrence has no exact source invocation")
            if (
                source_invocation.exact_material != addition.source_material
                or result_invocation.exact_material != addition.result_material
            ):
                raise ValueError("invocation material differs from the addition occurrence")
            row.append(
                AddedPositionCompareOccurrence(
                    boundary_identity=boundary_identity,
                    occurrence_position=comparison_position,
                    implementation_function_identity=implementation_function_identity,
                    added_position_act_occurrence_identity=(
                        addition.act_occurrence_identity
                    ),
                    source_invocation_occurrence_identity=(
                        source_invocation.occurrence_identity
                    ),
                    result_invocation_occurrence_identity=(
                        result_invocation.occurrence_identity
                    ),
                    source_returned=source_invocation.returned,
                    result_returned=result_invocation.returned,
                )
            )
            comparison_position += 1
        compared.append(tuple(row))
    return tuple(compared)


def compare_removed_position_invocations(
    source_invocations: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    result_invocations: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
) -> tuple[tuple[RemovedPositionCompareOccurrence, ...], ...]:
    if type(source_invocations) is not tuple or type(result_invocations) is not tuple:
        raise TypeError("Compare inputs must be exact invocation tuples")
    if len(source_invocations) != len(result_invocations):
        raise ValueError("Compare inputs require the same implementation functions")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    compared = []
    comparison_position = 0
    for source_row, result_row in zip(source_invocations, result_invocations):
        if not source_row or not result_row:
            raise ValueError("Compare inputs require invocation occurrences")
        implementation_function_identity = source_row[0].implementation_function_identity
        if (
            any(
                occurrence.implementation_function_identity
                != implementation_function_identity
                for occurrence in source_row
            )
            or any(
                occurrence.implementation_function_identity
                != implementation_function_identity
                for occurrence in result_row
            )
        ):
            raise ValueError("Compare inputs require the same implementation function")
        source_by_reference = {}
        for source_invocation in source_row:
            reference = source_invocation.source_coordinate
            if not isinstance(reference, ExactMaterialReference):
                raise ValueError("source invocation requires its exact material reference")
            if reference in source_by_reference:
                raise ValueError("source material reference entered Compare twice")
            source_by_reference[reference] = source_invocation
        row = []
        for result_invocation in result_row:
            removal = result_invocation.source_coordinate
            if not isinstance(removal, RemovedPositionOccurrence):
                raise ValueError("result invocation requires its exact removal occurrence")
            source_invocation = source_by_reference.get(removal.source_reference)
            if source_invocation is None:
                raise ValueError("removal occurrence has no exact source invocation")
            if (
                source_invocation.exact_material != removal.source_material
                or result_invocation.exact_material != removal.result_material
            ):
                raise ValueError("invocation material differs from the removal occurrence")
            row.append(
                RemovedPositionCompareOccurrence(
                    boundary_identity=boundary_identity,
                    occurrence_position=comparison_position,
                    implementation_function_identity=implementation_function_identity,
                    removed_position_act_occurrence_identity=(
                        removal.act_occurrence_identity
                    ),
                    source_invocation_occurrence_identity=(
                        source_invocation.occurrence_identity
                    ),
                    result_invocation_occurrence_identity=(
                        result_invocation.occurrence_identity
                    ),
                    source_returned=source_invocation.returned,
                    result_returned=result_invocation.returned,
                )
            )
            comparison_position += 1
        compared.append(tuple(row))
    return tuple(compared)
