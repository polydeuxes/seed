"""Exact material held for as long as this process holds it, and no longer.

Three things wore one coat, and separating them is the whole of this module:

```text
  material occurred            a durable occurrence, permanent
  material is available now    a distinction with a present-tense answer
  material is durably retained not this; that is an outward Act
```

**An occurrence records that material occurred. It does not record that the
material is available.** Availability differences without anything being recorded —
a process exits and every byte it held is gone — so a payload asserting
`available` would be stating present-tense Standing in a permanent record, and
would be wrong the moment the process ended while still read as true. Current
availability is asked of the holder, never read from the ledger.

What the occurrence records is what stays true: material with this digest and
this byte count occurred, and at that occurrence **this process held it**.

**That says nothing about anything else holding it.** Bytes read from a file are
process-locally held and separately located at the same moment, so recording the
first establishes nothing about the second. No locator recorded is not no
separate source — the same rule that made a filename source label rather than
truth. This module does not know whether another source exists and does not
Assertion to.

**The body is not in the ledger.** The occurrence carries identity and byte count;
the bytes live in a process-local holder. `#2491` measured the alternative on a
74 KB archive: the occurrence was 149,241 bytes, 99.3% of it hex, while identity
and byte count are about 1 KB regardless of size.

**Nothing here writes anything anywhere.** Holding bytes in memory is retention
without an outward act. Writing them to disk is Seed changing the world outside
itself, which is an Authority distinction this module deliberately does not touch —
no temp files, no spooling, no memory mapping, no restart read. When the
process ends the bytes are gone, and that is honest rather than a defect.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id

MATERIAL_OCCURRED_KIND = "material.transient.occurred"


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


def record_transient_material(
    ledger: EventLedger,
    *,
    locality_id: str,
    holder: ProcessLocalMaterial,
    identity: MaterialIdentity,
    occurrence_boundary: str,
) -> Event:
    """Record that exact material occurred, without recording the material.

    The occurrence carries no availability coordinate. Availability is a
    present-tense answer that differences without anything being recorded, so a
    payload asserting it would read as true after it stopped being so. What is
    recorded is that at this occurrence this process held the material.

    **The holder is required, and is asked.** Taking only an identity let a
    caller record that material was held process-locally when nothing had ever
    held it — a permanent record asserting something the function could not
    establish. No re-digest is involved; the holder is asked whether it holds this
    exact identity, which is the thing being asserted.
    """

    for name, value in (("occurrence_boundary", occurrence_boundary),
                        ("locality_id", locality_id)):
        if type(value) is not str or not value.strip():
            raise MaterialAvailabilityError(
                f"transient material requires {name} as an exact representation"
            )
    if not isinstance(identity, MaterialIdentity):
        raise MaterialAvailabilityError(
            "transient material requires the identity of what occurred"
        )
    if not isinstance(holder, ProcessLocalMaterial):
        raise MaterialAvailabilityError(
            "recording that material was held requires the holder that held it"
        )
    if not holder.is_available(identity):
        raise MaterialAvailabilityError(
            "the supplied holder does not hold this material, so this occurrence "
            "cannot record that it was held"
        )

    return ledger.append_many([
        Event(
            id=new_id("evt"),
            kind=MATERIAL_OCCURRED_KIND,
            locality_id=locality_id,
            payload={
                "dimensions": {
                    "identity": new_id("transient_material"),
                    "content": f"exact material, {identity.byte_count} bytes",
                    "standing": "occurred",
                    "source_provenance": occurrence_boundary,
                    "responsibility": "transient-material-occurrence",
                    "authority": "unestablished",
                    "evidence_scope": (
                        "occurrence-only; represented relation Unknown. Records that material "
                        "occurred, never that it is available now"
                    ),
                    "scope_locality": f"locality:{locality_id}",
                    "occurrence_preservation": (
                        "identity and byte count durably recorded; the material itself "
                        "was held process-locally and is not preserved here"
                    ),
                },
                "occurrence_boundary": occurrence_boundary,
                "material_identity": identity.to_json_dict(),
                "held_at_occurrence": "process-local",
                "known_loss": [
                    "the material itself is not preserved by this occurrence",
                    "material held process-locally does not survive the process",
                ],
                "unknowns": [
                    "what this material represents remains Unknown",
                    "whether it is available now is not answerable from this record",
                    "whether any other source holds this material remains Unknown",
                ],
                "mutates_cluster": False,
                "provenance_occurrence_refs": [],
            },
        )
    ])[0]


def identity_of_occurrence(event: Event) -> MaterialIdentity:
    """What an occurrence says the material was."""

    if event.kind != MATERIAL_OCCURRED_KIND:
        raise MaterialAvailabilityError(
            f"only transient material occurrences carry an identity: {event.kind}"
        )
    return MaterialIdentity.from_json_dict(event.payload.get("material_identity"))
