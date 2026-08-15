"""Exact material held while one process holds it."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any



class MaterialAvailabilityError(ValueError):
    """Exact material could not be identified, held, or read as stated."""


def exact_material_identity(exact_bytes: bytes) -> str:
    """Return the implementation representation of one exact material identity."""

    if type(exact_bytes) is not bytes:
        raise MaterialAvailabilityError(
            f"exact material is bytes, not {type(exact_bytes).__name__}"
        )
    return hashlib.sha256(exact_bytes).hexdigest()


@dataclass(frozen=True)
class MaterialIdentity:
    """One exact material identity."""

    identity: str

    def __post_init__(self) -> None:
        if type(self.identity) is not str or len(self.identity) != 64:
            raise MaterialAvailabilityError(
                "a material identity requires one 64-character representation"
            )
        try:
            bytes.fromhex(self.identity)
        except ValueError as exc:
            raise MaterialAvailabilityError(
                "a material identity carries a malformed representation"
            ) from exc
    @classmethod
    def of(cls, exact_bytes: bytes) -> "MaterialIdentity":
        return cls(identity=exact_material_identity(exact_bytes))

    def to_json_dict(self) -> dict[str, Any]:
        return {"identity": self.identity}

    @classmethod
    def from_json_dict(cls, value: Any) -> "MaterialIdentity":
        if not isinstance(value, dict):
            raise MaterialAvailabilityError("a material identity is not present")
        try:
            return cls(identity=value["identity"])
        except KeyError as exc:
            raise MaterialAvailabilityError(
                f"a material identity is incomplete: {exc}"
            ) from exc


class ProcessLocalMaterial:
    """Exact material this process holds, for as long as it holds it.

    Deliberately not durable. There is no spooling, no temporary file, no
    memory mapping and no restart read, because every one of those would be
    Seed preserving material outside itself — an outward Act requiring Authority
    this module does not have and does not ask for.

    A holder answers one distinction: *is this material available here now, and if
    so what is it.* It never answers *was this material ever available*, which is
    what the ledger occurrence is for.
    """

    def __init__(self) -> None:
        self._held: dict[str, bytes] = {}

    def hold(self, exact_bytes: bytes) -> MaterialIdentity:
        """Hold exact material and return what identifies it."""

        identity = MaterialIdentity.of(exact_bytes)
        self._held[identity.identity] = exact_bytes
        return identity

    def _held_under(self, identity: MaterialIdentity) -> bytes | None:
        """Return material held under the exact identity."""

        held = self._held.get(identity.identity)
        return held

    def is_available(self, identity: MaterialIdentity) -> bool:
        return self._held_under(identity) is not None

    def read(self, identity: MaterialIdentity) -> bytes:
        """Return exact material held under the supplied identity."""

        held = self._held_under(identity)
        if held is None:
            raise MaterialAvailabilityError(
                f"material {identity.identity[:16]}... is not available in this process"
            )
        return held

    def release(self, identity: MaterialIdentity) -> None:
        """Stop holding material under the exact supplied identity."""

        if self._held_under(identity) is not None:
            del self._held[identity.identity]

    def release_all(self) -> None:
        self._held.clear()

    @property
    def held_count(self) -> int:
        return len(self._held)
