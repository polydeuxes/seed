#!/usr/bin/env python3

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import subprocess


@dataclass(frozen=True)
class MaterialImplementationFunction:
    identity: str
    invocation: tuple[str, ...]


@dataclass(frozen=True)
class InvocationOccurrence:
    exact_material: bytes
    implementation_function_identity: str
    returncode: int
    stdout_bytes: bytes
    stderr_bytes: bytes

    @property
    def coordinates(self) -> tuple[int, bytes, bytes]:
        return (self.returncode, self.stdout_bytes, self.stderr_bytes)


ASPELL_US = MaterialImplementationFunction(
    identity="aspell-en-US",
    invocation=("aspell", "--lang=en_US", "pipe"),
)
ASPELL_GB = MaterialImplementationFunction(
    identity="aspell-en-GB",
    invocation=("aspell", "--lang=en_GB", "pipe"),
)
ENCHANT_US = MaterialImplementationFunction(
    identity="enchant-en-US",
    invocation=("enchant-2", "-a", "-d", "en_US"),
)
ENCHANT_GB = MaterialImplementationFunction(
    identity="enchant-en-GB",
    invocation=("enchant-2", "-a", "-d", "en_GB"),
)
MATERIAL_IMPLEMENTATION_FUNCTIONS = (
    ASPELL_US,
    ASPELL_GB,
    ENCHANT_US,
    ENCHANT_GB,
)
def invocation_occurrence(
    exact_material: bytes, implementation_function: MaterialImplementationFunction
) -> InvocationOccurrence:
    if type(exact_material) is not bytes:
        raise TypeError("implementation function material must be exact bytes")
    if not isinstance(implementation_function, MaterialImplementationFunction):
        raise TypeError("one material implementation function is required")
    completed = subprocess.run(
        implementation_function.invocation,
        input=exact_material,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    return InvocationOccurrence(
        exact_material=exact_material,
        implementation_function_identity=implementation_function.identity,
        returncode=completed.returncode,
        stdout_bytes=completed.stdout,
        stderr_bytes=completed.stderr,
    )


def occurrences_across(
    exact_materials: tuple[bytes, ...],
    implementation_functions: tuple[MaterialImplementationFunction, ...] = MATERIAL_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[InvocationOccurrence, ...], ...]:
    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("implementation function inputs must be one exact tuple of bytes")
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("material implementation functions must be one nonempty tuple")
    if not exact_materials:
        return tuple(() for _ in implementation_functions)
    calls = tuple(
        (material, implementation_function)
        for implementation_function in implementation_functions
        for material in exact_materials
    )
    with ThreadPoolExecutor(max_workers=min(16, len(calls))) as workers:
        occurrences = tuple(
            workers.map(lambda call: invocation_occurrence(*call), calls)
        )
    width = len(exact_materials)
    return tuple(
        occurrences[offset : offset + width]
        for offset in range(0, len(occurrences), width)
    )
