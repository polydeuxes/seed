#!/usr/bin/env python3

from __future__ import annotations

import ast
from dataclasses import dataclass
import io
import json
import plistlib
import tomllib
from typing import Callable
import xml.etree.ElementTree


@dataclass(frozen=True)
class CompiledImplementationFunction:
    identity: str
    invocation: Callable[[bytes], object]


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
class AddedPositionOccurrence:
    boundary_identity: str
    occurrence_position: int
    source_reference: ExactMaterialReference
    position: int
    added_reference: ExactMaterialReference
    result_material: bytes

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact Act occurrence position is required")
        if not isinstance(self.source_reference, ExactMaterialReference):
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
    def source_material(self) -> bytes:
        return self.source_reference.exact_material

    @property
    def added_material(self) -> bytes:
        return self.added_reference.exact_material


@dataclass(frozen=True, slots=True)
class CompiledInvocationOccurrence:
    boundary_identity: str
    invocation_position: int
    exact_material: bytes
    implementation_function_identity: str
    returned: bool
    source_coordinate: AddedPositionOccurrence | None = None

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.implementation_function_identity,
            self.invocation_position,
        )

    @property
    def source_material(self) -> bytes | None:
        return (
            self.source_coordinate.source_material
            if self.source_coordinate is not None
            else None
        )

    @property
    def added_position(self) -> int | None:
        return (
            self.source_coordinate.position
            if self.source_coordinate is not None
            else None
        )

    @property
    def added_material(self) -> bytes | None:
        return (
            self.source_coordinate.added_material
            if self.source_coordinate is not None
            else None
        )


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
        implementation_function_identity=implementation_function.identity,
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


def _compiled_invocations(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[CompiledImplementationFunction, ...],
    source_coordinates: tuple[AddedPositionOccurrence, ...] | None = None,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
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
                    implementation_function_identity=implementation_function.identity,
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
    source_material: tuple[ExactMaterialReference, ...],
    added_material: tuple[ExactMaterialReference, ...],
    *,
    boundary_identity: str,
) -> tuple[AddedPositionOccurrence, ...]:
    if type(source_material) is not tuple or not all(
        isinstance(material, ExactMaterialReference) for material in source_material
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
