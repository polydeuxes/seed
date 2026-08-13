"""Material returned by the system, and who asked for it.

A third boundary, distinct from the two that exist:

```text
  operator -> Seed    operator-origin    testimony and instruction
  Seed -> system      Seed-origin        the emission occurrence
  system -> Seed      system-origin      here
```

**This is what a second eye sees.** Material attributed to the system — a
directory listing, a file's contents, a program's output, a process exiting, a
file changing, a device delivering something. It is the first Evidence available
to Seed that neither the operator supplied nor Seed produced.

**No invocation is required.** An earlier revision of this module made system
material inherently the answer to an invocation, carried the invocation's
identity as a coordinate of the material, and named the occurrence "returned".
That is too narrow — the system produces material without anyone asking — and it
is the shape this repository has repeatedly refused: a relation between two
preserved subjects is its own bounded subject, not a coordinate of one
participant. An invocation and the material that followed it are two
occurrences; whether one is the answer to the other is a third thing, and is not
established here.

**It is not Seed observing itself.** Seed's own emission is an act Seed
performed and an occurrence already recorded directly; discovering it through an
observer would manufacture a second testimony path about something Seed knows
first-hand. `#2490` recorded the reason attribution comes first: Seed's account
of a fire must never become material asserting a fire, and separating
system-origin from Seed-origin is what keeps that separate.

## Nothing here invokes anything, and nothing here establishes that anyone did

**A declaration records that an invocation was declared.** It does not record
that it was performed. This function receives a supplied declaration and cannot
observe an act, so an earlier revision saying the named party *performed* the
invocation, in the same occurrence that recorded the performance as Unknown, was
carrying two contradictory Standings at once.

What a caller may establish about performance is what the caller itself did. A
harness that ran a subprocess can attest to running it; it cannot attest on
behalf of a party it merely names.

So no record here says Seed invoked anything. When Seed may invoke on its own
authority, that is a separate recovery, and only the production occurrence of the invoking
Act changes — the eye does not.

## The exchange is declared, not derived from an invocation

A caller supplies the bounded exchange, as everywhere else. Material that
nobody asked for still occurs somewhere, and deriving the exchange from an
invocation would have made unprompted material unrecordable.

## The material is whole

Unlike the console, this boundary is not line-framed, so exact material arrives
entire. A zip or an ELF crossing here is not cut at its first `0x0A`. The text
representation is a later examination exactly as in `#2490`, and its absence
does not make the material absent.

**Provisional.** This is a harness for separating the authority lines while the
operator performs invocations on Seed's behalf. It is expected to be replaced,
and what should survive it is the distinction it records, not its mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id

SYSTEM_ORIGIN = "system"

SYSTEM_INVOCATION_DECLARED_KIND = "system.invocation.declared"
SYSTEM_MATERIAL_OCCURRED_KIND = "system.material.occurred"


class SystemMaterialError(ValueError):
    """System material could not be declared or preserved as stated."""


@dataclass(frozen=True)
class DeclaredInvocation:
    """What was invoked, who declares having performed it, and on whose behalf.

    `declared_performer` is not decoration. An operator running a command so Seed
    can consume the result has not made Seed the invoker, and a record saying
    otherwise would grant Seed a capability it does not hold.

    It is *declared*, not established. Nothing here observed an act, so the
    coordinate carries an attribution a caller supplied and the occurrence says
    so in its own warrant.
    """

    invocation: str
    declared_performer: str
    on_behalf_of: str

    def __post_init__(self) -> None:
        for name in ("invocation", "declared_performer", "on_behalf_of"):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise SystemMaterialError(
                    f"a declared invocation requires {name} as an exact representation"
                )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "invocation": self.invocation,
            "declared_performer": self.declared_performer,
            "on_behalf_of": self.on_behalf_of,
        }


def _text_representation(exact_bytes: bytes) -> dict[str, Any]:
    """Whether these bytes have a text representation, and under what.

    The same shape `#2490` established at the operator boundary. A decoder
    outcome is recorded either way; material without a text representation is
    material, not absence.
    """

    try:
        exact_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        return {
            "available": False,
            "decoder_outcome": "bytes_rejected",
            "decoder_mechanism": "utf-8",
            "decoder_failure": f"{type(exc).__name__}: {exc}",
        }
    return {
        "available": True,
        "decoder_outcome": "decoded",
        "decoder_mechanism": "utf-8",
        "decoder_failure": None,
    }


def declare_invocation(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    declared: DeclaredInvocation,
) -> Event:
    """Record that an invocation was declared, and by whom it is attributed.

    Not that it was performed. Nothing here observed an act, and the warrant
    says so rather than the payload asserting a performance the function cannot
    establish.
    """

    _require_exchange(session_id)
    return ledger.append_many([
        Event(
            id=new_id("evt"),
            kind=SYSTEM_INVOCATION_DECLARED_KIND,
            workspace_id=workspace_id,
            session_id=session_id,
            payload={
                "dimensions": {
                    "identity": new_id("system_invocation"),
                    "content": declared.invocation,
                    "standing": "declared",
                    "source_provenance": (
                        f"attributed to {declared.declared_performer} by the declaring caller"
                    ),
                    "responsibility": "declared-system-invocation",
                    "authority_warrant": (
                        "records that an invocation was declared; establishes no "
                        "performance of it, and no capability of this Seed to invoke"
                    ),
                    "scope_locality": f"workspace:{workspace_id};session:{session_id}",
                    "occurrence_preservation": "declaration durably recorded",
                },
                "declared_invocation": declared.to_json_dict(),
                # No `seed_invoked` coordinate. That it is not established that
                # Seed invoked is not the same as its being established that
                # Seed did not, and a caller may declare Seed as the performer.
                # The warrant and the Unknowns carry exactly what is known.
                "unknowns": [
                    "whether the declared performer performed this remains Unknown",
                    "whether this Seed invoked anything remains Unknown",
                    "what the invocation names remains Unknown",
                ],
                "mutates_cluster": False,
                "lineage": [],
            },
        )
    ])[0]


def preserve_system_material(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    exact_bytes: bytes,
    observed_boundary: str,
) -> Event:
    """Record that exact system-attributed material occurred.

    No invocation is required or referenced. Material the system produced
    because someone asked, and material it produced because a process exited or
    a file changed, are the same kind of occurrence here. Whether some
    particular material followed some particular invocation is a relation
    between two preserved subjects, which is its own bounded subject and is not
    established by placing one inside the other.
    """

    if type(exact_bytes) is not bytes:
        raise SystemMaterialError("system material must be exact bytes")
    if type(observed_boundary) is not str or not observed_boundary.strip():
        raise SystemMaterialError("system material requires the boundary it was observed at")
    _require_exchange(session_id)

    return ledger.append_many([
        Event(
            id=new_id("evt"),
            kind=SYSTEM_MATERIAL_OCCURRED_KIND,
            workspace_id=workspace_id,
            session_id=session_id,
            payload={
                "dimensions": {
                    "identity": new_id("system_material"),
                    "content": f"exact material, {len(exact_bytes)} bytes",
                    "standing": "occurred",
                    "source_provenance": observed_boundary,
                    "responsibility": "system-material-occurrence",
                    "authority_warrant": "occurrence-only; meaning Unknown",
                    "scope_locality": f"workspace:{workspace_id};session:{session_id}",
                    "occurrence_preservation": "exact material durably recorded",
                },
                "material_origin": SYSTEM_ORIGIN,
                "observed_boundary": observed_boundary,
                "exact_bytes_hex": exact_bytes.hex(),
                "byte_count": len(exact_bytes),
                "text_representation": _text_representation(exact_bytes),
                "known_loss": [
                    "material existing before this boundary is not observable here",
                ],
                "unknowns": [
                    "what this material represents remains Unknown",
                    "what produced it remains Unknown",
                ],
                "mutates_cluster": False,
                "lineage": [],
            },
        )
    ])[0]


def _require_exchange(session_id: str) -> None:
    if type(session_id) is not str or not session_id.strip():
        raise SystemMaterialError("system occurrences require an exact bounded exchange")


def system_material_bytes(event: Event) -> bytes:
    """The exact bytes an occurrence preserved."""

    if event.kind != SYSTEM_MATERIAL_OCCURRED_KIND:
        raise SystemMaterialError(
            f"only system material occurrences carry exact bytes: {event.kind}"
        )
    encoded = event.payload.get("exact_bytes_hex")
    if type(encoded) is not str:
        raise SystemMaterialError("system material carries no exact bytes")
    try:
        recovered = bytes.fromhex(encoded)
    except ValueError as exc:
        raise SystemMaterialError("system material is not exact bytes") from exc
    if len(recovered) != event.payload.get("byte_count"):
        raise SystemMaterialError("system material does not match its byte count")
    return recovered
