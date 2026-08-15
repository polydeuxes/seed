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
class CompiledWitness:
    identity: str
    competency: Callable[[bytes], object]


@dataclass(frozen=True)
class CompiledWitnessOccurrence:
    exact_material: bytes
    witness_identity: str
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


COMPILED_WITNESSES = tuple(
    CompiledWitness(identity=f"compiled-{index}", competency=competency)
    for index, competency in enumerate((_a, _b, _c, _d, _e))
)


def interrogate(
    exact_material: bytes, witness: CompiledWitness
) -> CompiledWitnessOccurrence:
    if type(exact_material) is not bytes:
        raise TypeError("witness material must be exact bytes")
    if not isinstance(witness, CompiledWitness):
        raise TypeError("one compiled witness is required")
    try:
        witness.competency(exact_material)
    except Exception:
        returned = False
    else:
        returned = True
    return CompiledWitnessOccurrence(
        exact_material=exact_material,
        witness_identity=witness.identity,
        returned=returned,
    )


def interrogate_across(
    exact_materials: tuple[bytes, ...],
    witnesses: tuple[CompiledWitness, ...] = COMPILED_WITNESSES,
) -> tuple[tuple[CompiledWitnessOccurrence, ...], ...]:
    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("witness inputs must be one exact tuple of bytes")
    if type(witnesses) is not tuple or not witnesses:
        raise TypeError("compiled witnesses must be one nonempty tuple")
    return tuple(
        tuple(interrogate(material, witness) for material in exact_materials)
        for witness in witnesses
    )
