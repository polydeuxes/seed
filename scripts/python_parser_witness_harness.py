#!/usr/bin/env python3
"""Interrogate Python's compiled parser without adopting its grammar.

The parser is a witness.  It receives exact source bytes and either accepts
them with one exact provider-produced result representation or refuses them
with one exact provider-produced diagnostic representation.  Both outputs are
material attributed to that witness.  Names occurring inside them carry no
Seed Standing merely because the provider emitted them.

This harness deliberately does not inspect returned nodes, classify source,
or translate provider labels into claims such as what the source defines.  It
preserves only:

    exact input bytes
    accepted or refused
    exact successful-result bytes, when accepted
    exact diagnostic bytes, when refused

The compiled parser accepts bytes directly.  Source decoding, when required by
that parser, therefore remains part of the witness behavior rather than a
developer reconstruction performed before the interrogation.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
import warnings


@dataclass(frozen=True)
class ParserWitnessOutcome:
    """One exact answer from one compiled-parser interrogation."""

    exact_material: bytes
    accepted: bool
    result_material: bytes | None
    refusal_material: bytes | None


def interrogate(exact_material: bytes) -> ParserWitnessOutcome:
    """Return the compiled parser's exact bounded answer for these bytes."""

    if type(exact_material) is not bytes:
        raise TypeError("parser witness material must be exact bytes")
    try:
        # A warning is neither the returned parser result nor a refusal.  It
        # does not change which of those two outcomes occurred.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            returned = ast.parse(exact_material)
    except (SyntaxError, ValueError) as refusal:
        return ParserWitnessOutcome(
            exact_material=exact_material,
            accepted=False,
            result_material=None,
            refusal_material=str(refusal).encode("utf-8"),
        )
    return ParserWitnessOutcome(
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
    """Every distinct same-length material differing at exactly one byte."""

    if type(exact_material) is not bytes:
        raise TypeError("one-byte substitutions require exact bytes")
    changed = []
    for position, original in enumerate(exact_material):
        for replacement in range(256):
            if replacement == original:
                continue
            candidate = bytearray(exact_material)
            candidate[position] = replacement
            changed.append(bytes(candidate))
    return tuple(changed)


def interrogate_many(
    exact_materials: tuple[bytes, ...],
) -> tuple[ParserWitnessOutcome, ...]:
    """Interrogate each exact supplied material once, in supplied order."""

    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("parser witness inputs must be one exact tuple of bytes")
    return tuple(interrogate(material) for material in exact_materials)
