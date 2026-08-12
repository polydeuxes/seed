"""Lossless storage mechanics for exact material recurrence.

This module is deliberately below language and constitutional interpretation.
It establishes only a reversible representation of exact bytes:

    novel bytes        -> literal bytes
    later recurrence   -> reference to an earlier reconstructed byte span
    ordered parts      -> the exact original bytes

A reference establishes byte reuse only. It establishes no subject identity,
meaning, relation, grammar, or standing beyond exact reconstruction.

References are backward-only and non-overlapping with the bytes currently being
formed. Every reference therefore terminates in material that is already fully
reconstructable from earlier parts; no external source lookup or brute-force
recovery is involved.
"""

from __future__ import annotations

from dataclasses import dataclass
import base64
import hashlib
from typing import Any


ENCODING_VERSION = "exact-material-backreference-v1"


class ExactMaterialPointerError(ValueError):
    """An exact-material pointer representation cannot be formed or recovered."""


@dataclass(frozen=True)
class LiteralPart:
    exact_bytes: bytes

    def __post_init__(self) -> None:
        if type(self.exact_bytes) is not bytes or not self.exact_bytes:
            raise ExactMaterialPointerError("a literal part requires non-empty exact bytes")


@dataclass(frozen=True)
class ReferencePart:
    start: int
    length: int

    def __post_init__(self) -> None:
        if type(self.start) is not int or self.start < 0:
            raise ExactMaterialPointerError("a reference start must be a non-negative integer")
        if type(self.length) is not int or self.length <= 0:
            raise ExactMaterialPointerError("a reference length must be a positive integer")


ExactMaterialPart = LiteralPart | ReferencePart


@dataclass(frozen=True)
class ExactMaterialPointers:
    """A self-contained, lossless representation of one exact byte sequence."""

    byte_count: int
    sha256: str
    parts: tuple[ExactMaterialPart, ...]
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
        recovered = reconstruct_exact_bytes(self, verify=False)
        if len(recovered) != self.byte_count:
            raise ExactMaterialPointerError("reconstructed material does not match byte_count")
        if hashlib.sha256(recovered).hexdigest() != self.sha256:
            raise ExactMaterialPointerError("reconstructed material does not match sha256")

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
                    {"kind": "reference", "start": part.start, "length": part.length}
                )
        return {
            "version": self.version,
            "byte_count": self.byte_count,
            "sha256": self.sha256,
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
                parts.append(LiteralPart(exact))
            elif kind == "reference":
                parts.append(ReferencePart(start=raw.get("start"), length=raw.get("length")))
            else:
                raise ExactMaterialPointerError(f"unknown exact-material part kind: {kind!r}")
        return cls(
            version=value.get("version"),
            byte_count=value.get("byte_count"),
            sha256=value.get("sha256"),
            parts=tuple(parts),
        )


def reconstruct_exact_bytes(
    encoded: ExactMaterialPointers, *, verify: bool = True
) -> bytes:
    """Reconstruct exact bytes from literals and already-reconstructed references."""

    if not isinstance(encoded, ExactMaterialPointers):
        raise ExactMaterialPointerError("encoded material must be ExactMaterialPointers")
    recovered = bytearray()
    for part in encoded.parts:
        if isinstance(part, LiteralPart):
            recovered.extend(part.exact_bytes)
            continue
        end = part.start + part.length
        # A reference may point to bytes produced by an earlier reference, but
        # its complete source span must already exist before this part begins.
        if end > len(recovered):
            raise ExactMaterialPointerError(
                "a reference must resolve wholly inside already reconstructed material"
            )
        recovered.extend(recovered[part.start:end])
    result = bytes(recovered)
    if verify:
        if len(result) != encoded.byte_count:
            raise ExactMaterialPointerError("reconstructed material does not match byte_count")
        if hashlib.sha256(result).hexdigest() != encoded.sha256:
            raise ExactMaterialPointerError("reconstructed material does not match sha256")
    return result


def form_exact_material_pointers(
    exact_bytes: bytes,
    *,
    minimum_reference_length: int = 4,
    candidate_limit: int = 64,
) -> ExactMaterialPointers:
    """Greedily replace exact recurrences with deterministic backward references.

    The search is intentionally a storage-mechanics experiment, not a claim of
    optimal compression. At each position it chooses the longest already-complete
    matching span. Ties choose the earliest source position. `candidate_limit`
    bounds work on highly repetitive material without changing reconstruction.
    """

    if type(exact_bytes) is not bytes:
        raise ExactMaterialPointerError("exact_bytes must be exact bytes")
    if type(minimum_reference_length) is not int or minimum_reference_length < 2:
        raise ExactMaterialPointerError("minimum_reference_length must be an integer >= 2")
    if type(candidate_limit) is not int or candidate_limit <= 0:
        raise ExactMaterialPointerError("candidate_limit must be a positive integer")

    if not exact_bytes:
        return ExactMaterialPointers(
            byte_count=0,
            sha256=hashlib.sha256(b"").hexdigest(),
            parts=(),
        )

    index: dict[bytes, list[int]] = {}
    parts: list[ExactMaterialPart] = []
    literal = bytearray()
    size = len(exact_bytes)

    def index_position(position: int) -> None:
        if position + minimum_reference_length > size:
            return
        key = exact_bytes[position : position + minimum_reference_length]
        index.setdefault(key, []).append(position)

    def flush_literal() -> None:
        if literal:
            parts.append(LiteralPart(bytes(literal)))
            literal.clear()

    position = 0
    while position < size:
        best_start = -1
        best_length = 0
        if position + minimum_reference_length <= size:
            key = exact_bytes[position : position + minimum_reference_length]
            candidates = index.get(key, ())[-candidate_limit:]
            for start in candidates:
                # The source span must be complete before this part begins.
                max_length = min(size - position, position - start)
                if max_length < minimum_reference_length:
                    continue
                length = minimum_reference_length
                while (
                    length < max_length
                    and exact_bytes[start + length] == exact_bytes[position + length]
                ):
                    length += 1
                if length > best_length or (
                    length == best_length and length >= minimum_reference_length and start < best_start
                ):
                    best_start = start
                    best_length = length

        if best_length >= minimum_reference_length:
            flush_literal()
            parts.append(ReferencePart(start=best_start, length=best_length))
            for indexed_position in range(position, position + best_length):
                index_position(indexed_position)
            position += best_length
        else:
            literal.append(exact_bytes[position])
            index_position(position)
            position += 1

    flush_literal()
    return ExactMaterialPointers(
        byte_count=size,
        sha256=hashlib.sha256(exact_bytes).hexdigest(),
        parts=tuple(parts),
    )
