"""Exact material held while one process holds it."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any



class MaterialAvailabilityError(ValueError):
    """Exact material could not be identified, held, or read as stated."""


def material_digest(exact_bytes: bytes) -> str:
    """A digest identifying exact material independently of holding it.

    **One canonical exact-material digest, shared with the pointer account.**
    `ExactMaterialPointers.sha256` is `sha256` over the read bytes, and
    an earlier revision of this module domain-separated its own, so the same
    body had two values both describable as *the digest of this exact material*.

    The separator earned nothing here. The other domains in this runtime commit
    to composed structures — a chained prefix, a rule with its identities —
    where one structure could otherwise be read as another. This commits to raw
    bytes and nothing else, which is the same subject the pointer account
    commits to, so separating them would have made two names for one thing that
    disagree.

    They now agree exactly, which is what lets a pointer account and a
    material identity for one body be recognised as concerning it without an
    intervening step.
    """

    if type(exact_bytes) is not bytes:
        raise MaterialAvailabilityError(
            f"exact material is bytes, not {type(exact_bytes).__name__}"
        )
    return hashlib.sha256(exact_bytes).hexdigest()


@dataclass(frozen=True)
class MaterialIdentity:
    """What material was, without being the material.

    Carrying this instead of the body is what keeps an occurrence a constant
    size. It identifies; it does not read. Nothing reads material from
    a digest, and a reader holding one knows what to ask for rather than
    what it says.
    """

    digest: str
    byte_count: int

    def __post_init__(self) -> None:
        if type(self.digest) is not str or len(self.digest) != 64:
            raise MaterialAvailabilityError(
                "a material identity requires a 64-character digest"
            )
        try:
            bytes.fromhex(self.digest)
        except ValueError as exc:
            raise MaterialAvailabilityError("a material digest is hexadecimal") from exc
        # bool is an int and True == 1, so it is excluded rather than counted.
        if type(self.byte_count) is not int or self.byte_count < 0:
            raise MaterialAvailabilityError(
                "a material identity requires a non-negative integer byte count"
            )

    @classmethod
    def of(cls, exact_bytes: bytes) -> "MaterialIdentity":
        return cls(digest=material_digest(exact_bytes), byte_count=len(exact_bytes))

    def to_json_dict(self) -> dict[str, Any]:
        return {"digest": self.digest, "byte_count": self.byte_count}

    @classmethod
    def from_json_dict(cls, value: Any) -> "MaterialIdentity":
        if not isinstance(value, dict):
            raise MaterialAvailabilityError("a material identity is not present")
        try:
            return cls(digest=value["digest"], byte_count=value["byte_count"])
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
        self._held[identity.digest] = exact_bytes
        return identity

    def _held_under(self, identity: MaterialIdentity) -> bytes | None:
        """What is held under this exact identity, digest and byte count together.

        Keying on the digest alone made the three answers disagree: an identity
        with the right digest and the wrong byte count reported available, refused
        to read, and — worst — released the material that was genuinely
        held. One identity, one answer.
        """

        held = self._held.get(identity.digest)
        if held is None or len(held) != identity.byte_count:
            return None
        return held

    def is_available(self, identity: MaterialIdentity) -> bool:
        return self._held_under(identity) is not None

    def read(self, identity: MaterialIdentity) -> bytes:
        """The exact material, or a refusal naming what is unavailable.

        The material is not re-digested. It is held *under* its digest, so
        anything found under one reproduces it exactly, and a check that
        cannot fail is not free here: re-digesting was 98% of a 5 MB read
        and 100% of a 50 MB one, at 130 ms each.

        The byte count is still checked, because an identity is supplied by a caller
        and may disagree with what the digest names.
        """

        held = self._held_under(identity)
        if held is None:
            raise MaterialAvailabilityError(
                f"material {identity.digest[:16]}... is not available in this process"
            )
        return held

    def release(self, identity: MaterialIdentity) -> None:
        """Stop holding this exact material. The occurrence of it is untouched.

        An identity that does not name what is held releases nothing. Keying on
        the digest alone meant an identity with the wrong byte count destroyed the
        material it had just been refused.
        """

        if self._held_under(identity) is not None:
            del self._held[identity.digest]

    def release_all(self) -> None:
        self._held.clear()

    @property
    def held_count(self) -> int:
        return len(self._held)
