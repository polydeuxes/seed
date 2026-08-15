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


@dataclass(frozen=True)
class CompiledInvocationOccurrence:
    exact_material: bytes
    implementation_function_identity: str
    returned: bool


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


def interrogate(
    exact_material: bytes, implementation_function: CompiledImplementationFunction
) -> CompiledInvocationOccurrence:
    if type(exact_material) is not bytes:
        raise TypeError("implementation function material must be exact bytes")
    if not isinstance(implementation_function, CompiledImplementationFunction):
        raise TypeError("one compiled implementation function is required")
    try:
        implementation_function.invocation(exact_material)
    except Exception:
        returned = False
    else:
        returned = True
    return CompiledInvocationOccurrence(
        exact_material=exact_material,
        implementation_function_identity=implementation_function.identity,
        returned=returned,
    )


def interrogate_across(
    exact_materials: tuple[bytes, ...],
    implementation_functions: tuple[CompiledImplementationFunction, ...] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("implementation function inputs must be one exact tuple of bytes")
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("compiled implementation functions must be one nonempty tuple")
    return tuple(
        tuple(interrogate(material, implementation_function) for material in exact_materials)
        for implementation_function in implementation_functions
    )


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
) -> tuple[dict[str, object], ...]:
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
        {
            "source_material": source,
            "position": position,
            "added_material": bytes((added,)),
            "candidate_material": bytes(
                (*source[:position], added, *source[position:])
            ),
        }
        for source in source_material
        for position in range(len(source) + 1)
        for added in added_material
    )


def interrogate_added_positions(
    candidates: tuple[dict[str, object], ...],
    implementation_functions: tuple[CompiledImplementationFunction, ...] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(candidates) is not tuple:
        raise TypeError("candidate material must be one exact tuple")
    exact_material = []
    for candidate in candidates:
        if type(candidate) is not dict or set(candidate) != {
            "source_material",
            "position",
            "added_material",
            "candidate_material",
        }:
            raise TypeError("candidate material requires its exact source coordinates")
        source = candidate["source_material"]
        position = candidate["position"]
        added = candidate["added_material"]
        material = candidate["candidate_material"]
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
    return interrogate_across(tuple(exact_material), implementation_functions)
