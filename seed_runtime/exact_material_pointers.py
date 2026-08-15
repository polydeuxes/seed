"""Lossless exact-material storage using literals and backward references."""

from __future__ import annotations

from dataclasses import dataclass
import base64
from typing import Any

from seed_runtime.material_availability import exact_material_identity


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
    source_position: int
    count: int

    def __post_init__(self) -> None:
        if type(self.source_position) is not int or self.source_position < 0:
            raise ExactMaterialPointerError("a reference source_position must be a non-negative integer")
        if type(self.count) is not int or self.count <= 0:
            raise ExactMaterialPointerError("a reference count must be a positive integer")


ExactMaterialPart = LiteralPart | ReferencePart


@dataclass(frozen=True)
class ExactMaterialReferenceLimits:
    """The declared bounds of one reference search."""

    reference_count_limit: int
    candidate_limit: int

    def __post_init__(self) -> None:
        for name in ("reference_count_limit", "candidate_limit"):
            value = getattr(self, name)
            # `bool` is an `int` and `True == 1`, so it is excluded explicitly.
            if type(value) is not int:
                raise ExactMaterialPointerError(
                    f"{name} must be an integer, not {type(value).__name__}"
                )
        if self.reference_count_limit < 2:
            raise ExactMaterialPointerError("reference_count_limit must be at least 2")
        if self.candidate_limit <= 0:
            raise ExactMaterialPointerError("candidate_limit must be positive")

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "reference_count_limit": self.reference_count_limit,
            "candidate_limit": self.candidate_limit,
        }

    @classmethod
    def from_json_dict(cls, value: Any) -> "ExactMaterialReferenceLimits":
        if not isinstance(value, dict):
            raise ExactMaterialPointerError("reference limits must be an object")
        try:
            return cls(
                reference_count_limit=value["reference_count_limit"],
                candidate_limit=value["candidate_limit"],
            )
        except KeyError as exc:
            raise ExactMaterialPointerError(f"reference limits are incomplete: {exc}") from exc


@dataclass(frozen=True)
class ExactMaterialPointers:
    """A self-contained, lossless representation of one exact byte sequence."""

    count: int
    material_identity: str
    material: tuple[ExactMaterialPart, ...]
    reference_limits: ExactMaterialReferenceLimits

    def __post_init__(self) -> None:
        if type(self.count) is not int or self.count < 0:
            raise ExactMaterialPointerError("count must be a non-negative integer")
        if type(self.material_identity) is not str or len(self.material_identity) != 64:
            raise ExactMaterialPointerError(
                "material_identity must be one 64-character hexadecimal representation"
            )
        try:
            bytes.fromhex(self.material_identity)
        except ValueError as exc:
            raise ExactMaterialPointerError("material_identity must be hexadecimal") from exc
        if type(self.material) is not tuple:
            raise ExactMaterialPointerError("material must be an exact tuple")
        if not all(isinstance(part, (LiteralPart, ReferencePart)) for part in self.material):
            raise ExactMaterialPointerError("material must contain only literals or references")
        if not isinstance(self.reference_limits, ExactMaterialReferenceLimits):
            raise ExactMaterialPointerError(
                "an account must declare its reference limits"
            )
        read = read_exact_bytes(self, verify=False)
        if len(read) != self.count:
            raise ExactMaterialPointerError("read material does not match count")
        if exact_material_identity(read) != self.material_identity:
            raise ExactMaterialPointerError("read material does not match material_identity")

    def to_json_dict(self) -> dict[str, Any]:
        represented_material: list[dict[str, Any]] = []
        for part in self.material:
            if isinstance(part, LiteralPart):
                represented_material.append(
                    {
                        "kind": "literal",
                        "representation": base64.b64encode(part.exact_bytes).decode("ascii"),
                    }
                )
            else:
                represented_material.append(
                    {"kind": "reference", "source_position": part.source_position, "count": part.count}
                )
        return {
            "count": self.count,
            "material_identity": self.material_identity,
            "reference_limits": self.reference_limits.to_json_dict(),
            "material": represented_material,
        }

    @classmethod
    def from_json_dict(cls, value: Any) -> "ExactMaterialPointers":
        if not isinstance(value, dict):
            raise ExactMaterialPointerError("exact-material pointers must be an object")
        raw_material = value.get("material")
        if not isinstance(raw_material, list):
            raise ExactMaterialPointerError("material must be a list")
        material: list[ExactMaterialPart] = []
        for raw in raw_material:
            if not isinstance(raw, dict):
                raise ExactMaterialPointerError("each part must be an object")
            kind = raw.get("kind")
            if kind == "literal":
                encoded = raw.get("representation")
                if not isinstance(encoded, str):
                    raise ExactMaterialPointerError("literal representation must be a string")
                try:
                    exact = base64.b64decode(encoded.encode("ascii"), validate=True)
                except (ValueError, UnicodeEncodeError) as exc:
                    raise ExactMaterialPointerError("literal representation is not valid base64") from exc
                # Canonical, and required explicitly rather than left to the
                # runtime's opinion. `b64decode(validate=True)` accepted
                # "YWJj====" as b"abc" through Python 3.11 and refuses it as
                # excess padding from 3.12, so an account's acceptance depended
                # on the Python process read it. Re-encoding is exact and the
                # same everywhere.
                if base64.b64encode(exact).decode("ascii") != encoded:
                    raise ExactMaterialPointerError(
                        "literal representation is not the canonical encoding of its bytes"
                    )
                material.append(LiteralPart(exact))
            elif kind == "reference":
                material.append(
                    ReferencePart(source_position=raw.get("source_position"), count=raw.get("count"))
                )
            else:
                raise ExactMaterialPointerError(f"unknown exact-material part kind: {kind!r}")
        return cls(
            count=value.get("count"),
            material_identity=value.get("material_identity"),
            reference_limits=ExactMaterialReferenceLimits.from_json_dict(value.get("reference_limits")),
            material=tuple(material),
        )


def read_exact_bytes(
    encoded: ExactMaterialPointers, *, verify: bool = True
) -> bytes:
    """Read exact bytes from literals and already-read references."""

    if not isinstance(encoded, ExactMaterialPointers):
        raise ExactMaterialPointerError("encoded material must be ExactMaterialPointers")
    read = bytearray()
    for part in encoded.material:
        if isinstance(part, LiteralPart):
            read.extend(part.exact_bytes)
            continue
        end = part.source_position + part.count
        # A reference may point to bytes appended by an earlier reference, but
        # its complete source span must already exist before this part begins.
        if end > len(read):
            raise ExactMaterialPointerError(
                "a reference must resolve wholly inside already read material"
            )
        read.extend(read[part.source_position:end])
    result = bytes(read)
    if verify:
        if len(result) != encoded.count:
            raise ExactMaterialPointerError("read material does not match count")
        if exact_material_identity(result) != encoded.material_identity:
            raise ExactMaterialPointerError("read material does not match material_identity")
    return result


def represent_exact_material_pointers(
    exact_bytes: bytes,
    *,
    reference_count_limit: int = 4,
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
    which is exact under any reference_limits; they bound what the account may be read
    to mean.
    """

    if type(exact_bytes) is not bytes:
        raise ExactMaterialPointerError("exact_bytes must be exact bytes")
    if type(reference_count_limit) is not int or reference_count_limit < 2:
        raise ExactMaterialPointerError("reference_count_limit must be an integer >= 2")
    if type(candidate_limit) is not int or candidate_limit <= 0:
        raise ExactMaterialPointerError("candidate_limit must be a positive integer")

    reference_limits = ExactMaterialReferenceLimits(
        reference_count_limit=reference_count_limit,
        candidate_limit=candidate_limit,
    )

    if not exact_bytes:
        return ExactMaterialPointers(
            count=0,
            material_identity=exact_material_identity(b""),
            material=(),
            reference_limits=reference_limits,
        )

    index: dict[bytes, list[int]] = {}
    material: list[ExactMaterialPart] = []
    literal = bytearray()
    size = len(exact_bytes)

    def index_position(position: int) -> None:
        if position + reference_count_limit > size:
            return
        key = exact_bytes[position : position + reference_count_limit]
        index.setdefault(key, []).append(position)

    def flush_literal() -> None:
        if literal:
            material.append(LiteralPart(bytes(literal)))
            literal.clear()

    position = 0
    while position < size:
        reference_source_position = -1
        reference_count = 0
        if position + reference_count_limit <= size:
            key = exact_bytes[position : position + reference_count_limit]
            candidates = index.get(key, ())[-candidate_limit:]
            for source_position in candidates:
                # The source span must be complete before this part begins.
                available_count = min(size - position, position - source_position)
                if available_count < reference_count_limit:
                    continue
                count = reference_count_limit
                while (
                    count < available_count
                    and exact_bytes[source_position + count] == exact_bytes[position + count]
                ):
                    count += 1
                if count > reference_count or (
                    count == reference_count
                    and count >= reference_count_limit
                    and source_position < reference_source_position
                ):
                    reference_source_position = source_position
                    reference_count = count

        if reference_count >= reference_count_limit:
            flush_literal()
            material.append(
                ReferencePart(
                    source_position=reference_source_position,
                    count=reference_count,
                )
            )
            for indexed_position in range(position, position + reference_count):
                index_position(indexed_position)
            position += reference_count
        else:
            literal.append(exact_bytes[position])
            index_position(position)
            position += 1

    flush_literal()
    return ExactMaterialPointers(
        count=size,
        material_identity=exact_material_identity(exact_bytes),
        material=tuple(material),
        reference_limits=reference_limits,
    )
