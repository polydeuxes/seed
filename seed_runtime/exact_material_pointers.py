"""Lossless storage mechanics for exact material recurrence.

This module is deliberately below language and constitutional read.
It establishes only a reversible representation of exact bytes:

    novel bytes        -> literal bytes
    later recurrence   -> reference to an earlier read byte span
    ordered parts      -> the exact original bytes

A reference establishes byte reuse only. It establishes no subject identity,
represented relation, relation, grammar, or standing beyond the exact bytes.

**What this carries is the recurrence its declared pointer_rule found, not the
recurrence present in the material.** The pointer_rule bounds the search, and the
same bytes yield different accounts under different bounds — 60,000 bytes of
prose were 95.8% covered at a three-byte minimum and 52.2% covered at eight, and
changing only the candidate bound moved hundreds of references. So:

```text
  absence of a reference
  !=
  absence of recurrence
```

An absent reference may mean the recurrence is shorter than the minimum, that
its source fell outside the candidate bound, or that an earlier greedy reference
used the bytes it would have matched. The pointer_rule is therefore carried in
the representation, because an account of a bounded search that does not
disclose its bounds reads as a complete one.

Read does not depend on the pointer_rule. The parts alone read
exactly, and the pointer_rule bounds only what the account may be read to mean.

References are backward-only and non-overlapping with the bytes currently being
supplied. Every reference therefore terminates in material that is already fully
addressable from earlier parts; no separate source lookup or brute-force
read is involved.
"""

from __future__ import annotations

from dataclasses import dataclass
import base64
import hashlib
from typing import Any


ENCODING_VERSION = "exact-material-backreference"


class ExactMaterialPointerError(ValueError):
    """An exact-material pointer representation cannot be supplied or read."""


@dataclass(frozen=True)
class LiteralPart:
    exact_bytes: bytes

    def __post_init__(self) -> None:
        if type(self.exact_bytes) is not bytes or not self.exact_bytes:
            raise ExactMaterialPointerError("a literal part requires non-empty exact bytes")


@dataclass(frozen=True)
class ReferencePart:
    start: int
    byte_count: int

    def __post_init__(self) -> None:
        if type(self.start) is not int or self.start < 0:
            raise ExactMaterialPointerError("a reference start must be a non-negative integer")
        if type(self.byte_count) is not int or self.byte_count <= 0:
            raise ExactMaterialPointerError("a reference byte_count must be a positive integer")


ExactMaterialPart = LiteralPart | ReferencePart


@dataclass(frozen=True)
class ExactMaterialPointerRule:
    """The declared bounds of the search that yielded an account.

    Carried so an account of a bounded search discloses its bounds. Two
    accounts of the same material under different pointer_rules are different
    findings rather than contradictory ones, and become comparable subjects.
    """

    minimum_reference_byte_count: int
    candidate_limit: int

    def __post_init__(self) -> None:
        for name in ("minimum_reference_byte_count", "candidate_limit"):
            value = getattr(self, name)
            # `bool` is an `int` and `True == 1`, so it is excluded explicitly.
            if type(value) is not int:
                raise ExactMaterialPointerError(
                    f"{name} must be an integer, not {type(value).__name__}"
                )
        if self.minimum_reference_byte_count < 2:
            raise ExactMaterialPointerError("minimum_reference_byte_count must be at least 2")
        if self.candidate_limit <= 0:
            raise ExactMaterialPointerError("candidate_limit must be positive")

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "minimum_reference_byte_count": self.minimum_reference_byte_count,
            "candidate_limit": self.candidate_limit,
        }

    @classmethod
    def from_json_dict(cls, value: Any) -> "ExactMaterialPointerRule":
        if not isinstance(value, dict):
            raise ExactMaterialPointerError("a pointer_rule must be an object")
        try:
            return cls(
                minimum_reference_byte_count=value["minimum_reference_byte_count"],
                candidate_limit=value["candidate_limit"],
            )
        except KeyError as exc:
            raise ExactMaterialPointerError(f"a pointer_rule is incomplete: {exc}") from exc


@dataclass(frozen=True)
class ExactMaterialPointers:
    """A self-contained, lossless representation of one exact byte sequence."""

    byte_count: int
    sha256: str
    parts: tuple[ExactMaterialPart, ...]
    pointer_rule: ExactMaterialPointerRule
    version: str = ENCODING_VERSION

    def __post_init__(self) -> None:
        if self.version != ENCODING_VERSION:
            raise ExactMaterialPointerError(f"unsupported exact-material encoding: {self.version!r}")
        if type(self.byte_count) is not int or self.byte_count < 0:
            raise ExactMaterialPointerError("byte_count must be a non-negative integer")
        if type(self.sha256) is not str or len(self.sha256) != 64:
            raise ExactMaterialPointerError("sha256 must be a 64-character hexadecimal digest")
        try:
            bytes.fromhex(self.sha256)
        except ValueError as exc:
            raise ExactMaterialPointerError("sha256 must be hexadecimal") from exc
        if type(self.parts) is not tuple:
            raise ExactMaterialPointerError("parts must be an exact tuple")
        if not all(isinstance(part, (LiteralPart, ReferencePart)) for part in self.parts):
            raise ExactMaterialPointerError("parts must contain only literals or references")
        if not isinstance(self.pointer_rule, ExactMaterialPointerRule):
            raise ExactMaterialPointerError(
                "an account must declare the pointer_rule that yielded it"
            )
        read = read_exact_bytes(self, verify=False)
        if len(read) != self.byte_count:
            raise ExactMaterialPointerError("read material does not match byte_count")
        if hashlib.sha256(read).hexdigest() != self.sha256:
            raise ExactMaterialPointerError("read material does not match sha256")

    def to_json_dict(self) -> dict[str, Any]:
        encoded_parts: list[dict[str, Any]] = []
        for part in self.parts:
            if isinstance(part, LiteralPart):
                encoded_parts.append(
                    {
                        "kind": "literal",
                        "bytes_b64": base64.b64encode(part.exact_bytes).decode("ascii"),
                    }
                )
            else:
                encoded_parts.append(
                    {"kind": "reference", "start": part.start, "byte_count": part.byte_count}
                )
        return {
            "version": self.version,
            "byte_count": self.byte_count,
            "sha256": self.sha256,
            "pointer_rule": self.pointer_rule.to_json_dict(),
            "parts": encoded_parts,
        }

    @classmethod
    def from_json_dict(cls, value: Any) -> "ExactMaterialPointers":
        if not isinstance(value, dict):
            raise ExactMaterialPointerError("exact-material pointers must be an object")
        raw_parts = value.get("parts")
        if not isinstance(raw_parts, list):
            raise ExactMaterialPointerError("parts must be a list")
        parts: list[ExactMaterialPart] = []
        for raw in raw_parts:
            if not isinstance(raw, dict):
                raise ExactMaterialPointerError("each part must be an object")
            kind = raw.get("kind")
            if kind == "literal":
                encoded = raw.get("bytes_b64")
                if not isinstance(encoded, str):
                    raise ExactMaterialPointerError("literal bytes_b64 must be a string")
                try:
                    exact = base64.b64decode(encoded.encode("ascii"), validate=True)
                except (ValueError, UnicodeEncodeError) as exc:
                    raise ExactMaterialPointerError("literal bytes_b64 is not valid base64") from exc
                # Canonical, and required explicitly rather than left to the
                # runtime's opinion. `b64decode(validate=True)` accepted
                # "YWJj====" as b"abc" through Python 3.11 and refuses it as
                # excess padding from 3.12, so an account's acceptance depended
                # on the Python process read it. Re-encoding is exact and the
                # same everywhere.
                if base64.b64encode(exact).decode("ascii") != encoded:
                    raise ExactMaterialPointerError(
                        "literal bytes_b64 is not the canonical encoding of its bytes"
                    )
                parts.append(LiteralPart(exact))
            elif kind == "reference":
                parts.append(
                    ReferencePart(start=raw.get("start"), byte_count=raw.get("byte_count"))
                )
            else:
                raise ExactMaterialPointerError(f"unknown exact-material part kind: {kind!r}")
        return cls(
            version=value.get("version"),
            byte_count=value.get("byte_count"),
            sha256=value.get("sha256"),
            pointer_rule=ExactMaterialPointerRule.from_json_dict(value.get("pointer_rule")),
            parts=tuple(parts),
        )


def read_exact_bytes(
    encoded: ExactMaterialPointers, *, verify: bool = True
) -> bytes:
    """Read exact bytes from literals and already-read references."""

    if not isinstance(encoded, ExactMaterialPointers):
        raise ExactMaterialPointerError("encoded material must be ExactMaterialPointers")
    read = bytearray()
    for part in encoded.parts:
        if isinstance(part, LiteralPart):
            read.extend(part.exact_bytes)
            continue
        end = part.start + part.byte_count
        # A reference may point to bytes yielded by an earlier reference, but
        # its complete source span must already exist before this part begins.
        if end > len(read):
            raise ExactMaterialPointerError(
                "a reference must resolve wholly inside already read material"
            )
        read.extend(read[part.start:end])
    result = bytes(read)
    if verify:
        if len(result) != encoded.byte_count:
            raise ExactMaterialPointerError("read material does not match byte_count")
        if hashlib.sha256(result).hexdigest() != encoded.sha256:
            raise ExactMaterialPointerError("read material does not match sha256")
    return result


def represent_exact_material_pointers(
    exact_bytes: bytes,
    *,
    minimum_reference_byte_count: int = 4,
    candidate_limit: int = 64,
) -> ExactMaterialPointers:
    """Greedily find exact backward recurrence within the declared bounds.

    The search is a storage-mechanics experiment, not a Assertion of optimal
    compression, and not a Assertion to find every recurrence. At each position it
    chooses the longest already-complete matching span among the candidates it
    considers.

    `candidate_limit` bounds that consideration to the most recent matching
    source positions, so a tie is resolved to the earliest source **among those
    considered** — which on material recurring more than `candidate_limit`
    times is not the earliest in the material.

    Both bounds are recorded on the result. They do not affect read,
    which is exact under any pointer_rule; they bound what the account may be read
    to mean.
    """

    if type(exact_bytes) is not bytes:
        raise ExactMaterialPointerError("exact_bytes must be exact bytes")
    if type(minimum_reference_byte_count) is not int or minimum_reference_byte_count < 2:
        raise ExactMaterialPointerError("minimum_reference_byte_count must be an integer >= 2")
    if type(candidate_limit) is not int or candidate_limit <= 0:
        raise ExactMaterialPointerError("candidate_limit must be a positive integer")

    pointer_rule = ExactMaterialPointerRule(
        minimum_reference_byte_count=minimum_reference_byte_count,
        candidate_limit=candidate_limit,
    )

    if not exact_bytes:
        return ExactMaterialPointers(
            byte_count=0,
            sha256=hashlib.sha256(b"").hexdigest(),
            parts=(),
            pointer_rule=pointer_rule,
        )

    index: dict[bytes, list[int]] = {}
    parts: list[ExactMaterialPart] = []
    literal = bytearray()
    size = len(exact_bytes)

    def index_position(position: int) -> None:
        if position + minimum_reference_byte_count > size:
            return
        key = exact_bytes[position : position + minimum_reference_byte_count]
        index.setdefault(key, []).append(position)

    def flush_literal() -> None:
        if literal:
            parts.append(LiteralPart(bytes(literal)))
            literal.clear()

    position = 0
    while position < size:
        best_start = -1
        best_byte_count = 0
        if position + minimum_reference_byte_count <= size:
            key = exact_bytes[position : position + minimum_reference_byte_count]
            candidates = index.get(key, ())[-candidate_limit:]
            for start in candidates:
                # The source span must be complete before this part begins.
                max_byte_count = min(size - position, position - start)
                if max_byte_count < minimum_reference_byte_count:
                    continue
                byte_count = minimum_reference_byte_count
                while (
                    byte_count < max_byte_count
                    and exact_bytes[start + byte_count] == exact_bytes[position + byte_count]
                ):
                    byte_count += 1
                if byte_count > best_byte_count or (
                    byte_count == best_byte_count
                    and byte_count >= minimum_reference_byte_count
                    and start < best_start
                ):
                    best_start = start
                    best_byte_count = byte_count

        if best_byte_count >= minimum_reference_byte_count:
            flush_literal()
            parts.append(ReferencePart(start=best_start, byte_count=best_byte_count))
            for indexed_position in range(position, position + best_byte_count):
                index_position(indexed_position)
            position += best_byte_count
        else:
            literal.append(exact_bytes[position])
            index_position(position)
            position += 1

    flush_literal()
    return ExactMaterialPointers(
        byte_count=size,
        sha256=hashlib.sha256(exact_bytes).hexdigest(),
        parts=tuple(parts),
        pointer_rule=pointer_rule,
    )
