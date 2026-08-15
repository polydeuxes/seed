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
class AddedPositionMaterial:
    source_material: bytes
    position: int
    added_material: bytes
    candidate_material: bytes


@dataclass(frozen=True, slots=True)
class CompiledInvocationOccurrence:
    boundary_identity: str
    invocation_position: int
    exact_material: bytes
    implementation_function_identity: str
    returned: bool
    source_coordinate: AddedPositionMaterial | None = None

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
    source_coordinates: tuple[AddedPositionMaterial, ...] | None = None,
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
    candidate_material: bytes,
    added_position: int,
) -> bool:
    if (
        type(source_material) is not bytes
        or type(candidate_material) is not bytes
        or type(added_position) is not int
        or added_position < 0
        or added_position >= len(candidate_material)
        or len(candidate_material) != len(source_material) + 1
    ):
        return False
    return (
        candidate_material[:added_position]
        + candidate_material[added_position + 1 :]
        == source_material
    )


def candidate_material_at_added_positions(
    source_material: tuple[bytes, ...],
    added_material: tuple[int, ...],
) -> tuple[AddedPositionMaterial, ...]:
    if type(source_material) is not tuple or not all(
        type(material) is bytes for material in source_material
    ):
        raise TypeError("source material must be one exact tuple of bytes")
    if type(added_material) is not tuple or not all(
        type(material) is int and 0 <= material <= 255
        for material in added_material
    ):
        raise TypeError("added material must be one exact tuple of byte values")
    return tuple(
        AddedPositionMaterial(
            source_material=source,
            position=position,
            added_material=bytes((added,)),
            candidate_material=bytes(
                (*source[:position], added, *source[position:])
            ),
        )
        for source in source_material
        for position in range(len(source) + 1)
        for added in added_material
    )


def added_position_invocations(
    candidates: tuple[AddedPositionMaterial, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[CompiledImplementationFunction, ...] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(candidates) is not tuple:
        raise TypeError("candidate material must be one exact tuple")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    exact_material = []
    for candidate in candidates:
        if not isinstance(candidate, AddedPositionMaterial):
            raise TypeError("candidate material requires its exact source coordinates")
        source = candidate.source_material
        position = candidate.position
        added = candidate.added_material
        material = candidate.candidate_material
        if (
            type(added) is not bytes
            or len(added) != 1
            or type(material) is not bytes
            or not preserves_original_order(
                source_material=source,
                candidate_material=material,
                added_position=position,
            )
            or material[position : position + 1] != added
        ):
            raise ValueError(
                "candidate material does not preserve its exact source order"
            )
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
        source_coordinates=candidates,
    )
