#!/usr/bin/env python3
"""Exact compiled-parser invocation occurrences."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import subprocess
import warnings


@dataclass(frozen=True, slots=True)
class PythonParserInvocation:
    boundary_identity: str
    invocation_position: int
    exact_material: bytes
    returned: bool
    result_material: bytes | None
    refusal_material: bytes | None

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            "cpython-ast-direct",
            self.invocation_position,
        )


@dataclass(frozen=True, slots=True)
class CompiledParserFunction:
    identity: str
    arguments: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CompiledParserInvocation:
    boundary_identity: str
    invocation_position: int
    exact_material: bytes
    implementation_function_identity: str
    arguments: tuple[str, ...]
    returncode: int
    stdout_bytes: bytes
    stderr_bytes: bytes

    @property
    def returned(self) -> bool:
        return self.returncode == 0

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.implementation_function_identity,
            self.invocation_position,
        )


PYTHON_FUNCTION = CompiledParserFunction(
    identity="cpython-ast",
    arguments=(
        "python3.11",
        "-c",
        (
            "import ast,sys;"
            "b=sys.stdin.buffer.read();"
            "t=ast.parse(b);"
            "sys.stdout.buffer.write(ast.dump(t,annotate_fields=True,"
            "include_attributes=True).encode())"
        ),
    ),
)
GCC_FUNCTION = CompiledParserFunction(
    identity="gcc-c",
    arguments=("gcc", "-x", "c", "-fsyntax-only", "-"),
)
BASH_FUNCTION = CompiledParserFunction(
    identity="bash",
    arguments=("bash", "--noprofile", "--norc", "-n"),
)
PERL_FUNCTION = CompiledParserFunction(
    identity="perl",
    arguments=("perl", "-c"),
)
COMPILED_PARSER_FUNCTIONS = (
    PYTHON_FUNCTION,
    GCC_FUNCTION,
    BASH_FUNCTION,
    PERL_FUNCTION,
)


def compiled_parser_invocation(
    exact_material: bytes,
    implementation_function: CompiledParserFunction,
    *,
    boundary_identity: str,
    invocation_position: int = 0,
) -> CompiledParserInvocation:
    if type(exact_material) is not bytes:
        raise TypeError("compiled parser material must be exact bytes")
    if not isinstance(implementation_function, CompiledParserFunction):
        raise TypeError("one compiled parser function is required")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(invocation_position) is not int or invocation_position < 0:
        raise TypeError("one exact invocation position is required")
    completed = subprocess.run(
        implementation_function.arguments,
        input=exact_material,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    return CompiledParserInvocation(
        boundary_identity=boundary_identity,
        invocation_position=invocation_position,
        exact_material=exact_material,
        implementation_function_identity=implementation_function.identity,
        arguments=implementation_function.arguments,
        returncode=completed.returncode,
        stdout_bytes=completed.stdout,
        stderr_bytes=completed.stderr,
    )


def compiled_parser_invocations(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[CompiledParserFunction, ...] = COMPILED_PARSER_FUNCTIONS,
) -> tuple[tuple[CompiledParserInvocation, ...], ...]:
    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("compiled parser inputs must be one exact tuple of bytes")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("compiled parser functions must be one nonempty tuple")
    if not all(
        isinstance(function, CompiledParserFunction)
        for function in implementation_functions
    ):
        raise TypeError("compiled parser functions must be exact")
    return tuple(
        tuple(
            compiled_parser_invocation(
                material,
                implementation_function,
                boundary_identity=boundary_identity,
                invocation_position=position,
            )
            for position, material in enumerate(exact_materials)
        )
        for implementation_function in implementation_functions
    )


def python_parser_invocation(
    exact_material: bytes,
    *,
    boundary_identity: str,
    invocation_position: int = 0,
) -> PythonParserInvocation:
    if type(exact_material) is not bytes:
        raise TypeError("compiled parser material must be exact bytes")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(invocation_position) is not int or invocation_position < 0:
        raise TypeError("one exact invocation position is required")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            returned = ast.parse(exact_material)
    except (SyntaxError, ValueError) as refusal:
        return PythonParserInvocation(
            boundary_identity=boundary_identity,
            invocation_position=invocation_position,
            exact_material=exact_material,
            returned=False,
            result_material=None,
            refusal_material=str(refusal).encode("utf-8"),
        )
    return PythonParserInvocation(
        boundary_identity=boundary_identity,
        invocation_position=invocation_position,
        exact_material=exact_material,
        returned=True,
        result_material=ast.dump(
            returned,
            annotate_fields=True,
            include_attributes=True,
        ).encode("utf-8"),
        refusal_material=None,
    )


def one_byte_substitutions(exact_material: bytes) -> tuple[bytes, ...]:
    """Every distinct material with the same byte count differing at exactly one byte."""

    if type(exact_material) is not bytes:
        raise TypeError("one-byte substitutions require exact bytes")
    different = []
    for position, original in enumerate(exact_material):
        for replacement in range(256):
            if replacement == original:
                continue
            candidate = bytearray(exact_material)
            candidate[position] = replacement
            different.append(bytes(candidate))
    return tuple(different)


def python_parser_invocations(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
) -> tuple[PythonParserInvocation, ...]:
    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("compiled parser inputs must be one exact tuple of bytes")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    return tuple(
        python_parser_invocation(
            material,
            boundary_identity=boundary_identity,
            invocation_position=position,
        )
        for position, material in enumerate(exact_materials)
    )
