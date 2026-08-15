#!/usr/bin/env python3
"""Interrogate Python's compiled parser without adopting its grammar.

The parser is a witness.  It receives exact source bytes and either accepts
them with one exact provider-produced result representation or refuses them
with one exact provider-produced diagnostic representation.  Both outputs are
material attributed to that witness.  Names occurring inside them carry no
Seed Standing merely because the provider emitted them.

This harness deliberately does not inspect returned nodes or assert source
or translate provider labels into claims such as what the source defines.  It
preserves only:

    exact input bytes
    accepted or refused
    exact successful-result bytes, when accepted
    exact diagnostic bytes, when refused

The compiled parser accepts bytes directly. Source decoding remains part of
the witness behavior.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
import subprocess
import warnings


@dataclass(frozen=True)
class ParserWitnessResult:
    """One exact result from one compiled-parser interrogation."""

    exact_material: bytes
    accepted: bool
    result_material: bytes | None
    refusal_material: bytes | None


@dataclass(frozen=True)
class CompiledParserWitness:
    name: str
    arguments: tuple[str, ...]


@dataclass(frozen=True)
class CompiledParserResult:
    exact_material: bytes
    witness: str
    arguments: tuple[str, ...]
    returncode: int
    stdout_bytes: bytes
    stderr_bytes: bytes

    @property
    def accepted(self) -> bool:
        return self.returncode == 0


PYTHON_WITNESS = CompiledParserWitness(
    name="cpython-ast",
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
GCC_WITNESS = CompiledParserWitness(
    name="gcc-c",
    arguments=("gcc", "-x", "c", "-fsyntax-only", "-"),
)
BASH_WITNESS = CompiledParserWitness(
    name="bash",
    arguments=("bash", "--noprofile", "--norc", "-n"),
)
PERL_WITNESS = CompiledParserWitness(
    name="perl",
    arguments=("perl", "-c"),
)
COMPILED_PARSER_WITNESSES = (
    PYTHON_WITNESS,
    GCC_WITNESS,
    BASH_WITNESS,
    PERL_WITNESS,
)


def interrogate_compiled_parser(
    exact_material: bytes,
    witness: CompiledParserWitness,
) -> CompiledParserResult:
    if type(exact_material) is not bytes:
        raise TypeError("parser witness material must be exact bytes")
    if not isinstance(witness, CompiledParserWitness):
        raise TypeError("one compiled parser witness is required")
    completed = subprocess.run(
        witness.arguments,
        input=exact_material,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    return CompiledParserResult(
        exact_material=exact_material,
        witness=witness.name,
        arguments=witness.arguments,
        returncode=completed.returncode,
        stdout_bytes=completed.stdout,
        stderr_bytes=completed.stderr,
    )


def interrogate_across_compiled_parsers(
    exact_materials: tuple[bytes, ...],
    witnesses: tuple[CompiledParserWitness, ...] = COMPILED_PARSER_WITNESSES,
) -> tuple[tuple[CompiledParserResult, ...], ...]:
    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("parser witness inputs must be one exact tuple of bytes")
    if type(witnesses) is not tuple or not witnesses:
        raise TypeError("compiled parser witnesses must be one nonempty tuple")
    return tuple(
        tuple(interrogate_compiled_parser(material, witness) for material in exact_materials)
        for witness in witnesses
    )


def interrogate(exact_material: bytes) -> ParserWitnessResult:
    """Return the compiled parser's exact bounded result for these bytes."""

    if type(exact_material) is not bytes:
        raise TypeError("parser witness material must be exact bytes")
    try:
        # A warning is neither the returned parser result nor a refusal.  It
        # does not revision which of those two results occurred.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            returned = ast.parse(exact_material)
    except (SyntaxError, ValueError) as refusal:
        return ParserWitnessResult(
            exact_material=exact_material,
            accepted=False,
            result_material=None,
            refusal_material=str(refusal).encode("utf-8"),
        )
    return ParserWitnessResult(
        exact_material=exact_material,
        accepted=True,
        result_material=ast.dump(
            returned,
            annotate_fields=True,
            include_attributes=True,
        ).encode("utf-8"),
        refusal_material=None,
    )


def first_probe_family() -> tuple[bytes, ...]:
    """The first small exact family, without names for its distinctions."""

    return (
        b"x",
        b"x=",
        b"x=1",
        b"x=1\n",
        b"def",
        b"def ",
        b"def x",
        b"def x(",
        b"def x():",
        b"def x():\n",
        b"def x():\n pass",
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


def interrogate_many(
    exact_materials: tuple[bytes, ...],
) -> tuple[ParserWitnessResult, ...]:
    """Interrogate each exact supplied material once, in supplied order."""

    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("parser witness inputs must be one exact tuple of bytes")
    return tuple(interrogate(material) for material in exact_materials)
