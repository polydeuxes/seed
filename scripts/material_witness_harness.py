#!/usr/bin/env python3

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import subprocess


@dataclass(frozen=True)
class MaterialWitness:
    identity: str
    arguments: tuple[str, ...]


@dataclass(frozen=True)
class WitnessOccurrence:
    exact_material: bytes
    witness_identity: str
    returncode: int
    stdout_bytes: bytes
    stderr_bytes: bytes

    @property
    def coordinates(self) -> tuple[int, bytes, bytes]:
        return (self.returncode, self.stdout_bytes, self.stderr_bytes)


ASPELL_US = MaterialWitness(
    identity="aspell-en-US",
    arguments=("aspell", "--lang=en_US", "pipe"),
)
ASPELL_GB = MaterialWitness(
    identity="aspell-en-GB",
    arguments=("aspell", "--lang=en_GB", "pipe"),
)
ENCHANT_US = MaterialWitness(
    identity="enchant-en-US",
    arguments=("enchant-2", "-a", "-d", "en_US"),
)
ENCHANT_GB = MaterialWitness(
    identity="enchant-en-GB",
    arguments=("enchant-2", "-a", "-d", "en_GB"),
)
EXTERNAL_MATERIAL_WITNESSES = (
    ASPELL_US,
    ASPELL_GB,
    ENCHANT_US,
    ENCHANT_GB,
)
MATERIAL_WITNESSES = (
    *EXTERNAL_MATERIAL_WITNESSES,
)


def witness_occurrence(
    exact_material: bytes, witness: MaterialWitness
) -> WitnessOccurrence:
    if type(exact_material) is not bytes:
        raise TypeError("witness material must be exact bytes")
    if not isinstance(witness, MaterialWitness):
        raise TypeError("one material witness is required")
    completed = subprocess.run(
        witness.arguments,
        input=exact_material,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    return WitnessOccurrence(
        exact_material=exact_material,
        witness_identity=witness.identity,
        returncode=completed.returncode,
        stdout_bytes=completed.stdout,
        stderr_bytes=completed.stderr,
    )


def occurrences_across(
    exact_materials: tuple[bytes, ...],
    witnesses: tuple[MaterialWitness, ...] = MATERIAL_WITNESSES,
) -> tuple[tuple[WitnessOccurrence, ...], ...]:
    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("witness inputs must be one exact tuple of bytes")
    if type(witnesses) is not tuple or not witnesses:
        raise TypeError("material witnesses must be one nonempty tuple")
    if not exact_materials:
        return tuple(() for _ in witnesses)
    calls = tuple(
        (material, witness)
        for witness in witnesses
        for material in exact_materials
    )
    with ThreadPoolExecutor(max_workers=min(16, len(calls))) as workers:
        occurrences = tuple(
            workers.map(lambda call: witness_occurrence(*call), calls)
        )
    width = len(exact_materials)
    return tuple(
        occurrences[offset : offset + width]
        for offset in range(0, len(occurrences), width)
    )
