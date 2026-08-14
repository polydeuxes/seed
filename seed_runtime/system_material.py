"""Material returned by the system, and who asked for it.

A third boundary, distinct from the two that exist:

```text
  operator -> Seed    operator-origin    source role and instruction
  Seed -> system      Seed-origin        the emission occurrence
  system -> Seed      system-origin      here
```

**This is what a second eye sees.** System-origin material — a
directory listing, a file's contents, a program's output, a process exiting, a
file changing, a device sending something. It is the first Evidence available
to Seed that neither the operator supplied nor Seed yielded.

**No invocation is required.** An earlier revision of this module made system
material inherently the answer to an invocation, carried the invocation's
identity as a coordinate of the material, and named the occurrence "returned".
That is too narrow — the system yields material without anyone asking — and it
is the shape this repository has repeatedly refused: a relation between two
preserved subjects is its own bounded subject, not a coordinate of one
participant. An invocation and the material that followed it are two
occurrences; whether one is the answer to the other is a third thing, and is not
established here.

**It is not Seed observing itself.** Seed's own emission is an act Seed
performed and an occurrence already recorded directly; discovering it through an
observer would manufacture a second source path about something Seed knows
first-hand. `#2490` recorded the reason source identity comes first: Seed's account
of a fire must never become material asserting a fire, and separating
system-origin from Seed-origin is what keeps that separate.

## Nothing here invokes anything, and nothing here establishes that anyone did

**A declaration records that an invocation was declared.** It does not record
that it was performed. This function receives a supplied declaration and cannot
observe an act, so an earlier revision saying the named party *performed* the
invocation, in the same occurrence that recorded that act as Unknown, was
carrying two contradictory Standings at once.

What a caller may establish is what the caller itself did. A
harness that ran a subprocess can attest to running it; it cannot attest on
behalf of a party it merely names.

So no record here says Seed invoked anything. When Seed may invoke on its own
authority, that is a separate reconstruction, and only Standing concerning the
exact invoking Act occurrence changes — the eye does not.

## The exchange is declared, not derived from an invocation

A caller supplies the bounded exchange, as everywhere else. Material that
nobody asked for still occurs somewhere, and deriving the exchange from an
invocation would have made unprompted material unrecordable.

## The material is whole

Unlike the console, this boundary is not line-framed, so exact material arrives
entire. A zip or an ELF crossing here is not cut at its first `0x0A`. The text
representation is a later decoder outcome exactly as in `#2490`, and its absence
does not make the material absent.

**Provisional.** This is a harness for separating the authority lines while the
operator performs invocations on Seed's behalf. It is expected to be replaced,
and what should survive it is the distinction it records, not its mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.process_boundary import ProcessBoundaryError, run_process_boundary

SYSTEM_ORIGIN = "system"

SYSTEM_INVOCATION_DECLARED_KIND = "system.invocation.declared"
SYSTEM_MATERIAL_OCCURRED_KIND = "system.material.occurred"
SYSTEM_INVOCATION_ARGUMENTS_RELATED_KIND = "system.invocation.arguments_related"
SYSTEM_INVOCATION_ATTEMPTED_KIND = "system.invocation.attempted"
SYSTEM_INVOCATION_OCCURRED_KIND = "system.invocation.occurred"
SYSTEM_INVOCATION_FAILED_KIND = "system.invocation.failed"
SYSTEM_INVOCATION_MATERIAL_RELATED_KIND = "system.invocation.material_related"


class SystemMaterialError(ValueError):
    """System material could not be declared or preserved as stated."""


@dataclass(frozen=True)
class DeclaredInvocation:
    """What was invoked, who declares having performed it, and on whose behalf.

    `declared_performer` is not decoration. An operator running a command so Seed
    can have as input the result has not made Seed the invoker, and a record saying
    otherwise would grant Seed Authority or mechanism Evidence it does not hold.

    It is *declared*, not established. Nothing here observed an act, so the
    coordinate carries a source role a caller supplied and the occurrence says
    so in its own support.
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


@dataclass(frozen=True)
class SystemInvocationRun:
    """Exact records preserved around one no-shell system invocation."""

    arguments_relation: Event
    attempt: Event
    occurrence: Event
    stdout_material: Event
    stderr_material: Event
    stdout_relation: Event
    stderr_relation: Event


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
    locality_id: str,
    declared: DeclaredInvocation,
) -> Event:
    """Record that an invocation was declared, and with which declared source role.

    Not that it was performed. Nothing here observed an act, and the support
    says so rather than the payload asserting an act the function cannot
    establish.
    """

    _require_exchange(locality_id)
    return ledger.append_many([
        Event(
            id=new_id("evt"),
            kind=SYSTEM_INVOCATION_DECLARED_KIND,
            workspace_id=workspace_id,
            locality_id=locality_id,
            payload={
                "dimensions": {
                    "identity": new_id("system_invocation"),
                    "content": declared.invocation,
                    "standing": "declared",
                    "source_provenance": (
                        f"source role {declared.declared_performer} supplied by the declaring caller"
                    ),
                    "responsibility": "declared-system-invocation",
                    "authority": "unestablished",
                    "evidence_scope": (
                        "records that an invocation was declared; establishes no "
                        "act of it, and no Evidence or Authority for this Seed to invoke"
                    ),
                    "scope_locality": f"workspace:{workspace_id};locality:{locality_id}",
                    "occurrence_preservation": "declaration durably recorded",
                },
                "declared_invocation": declared.to_json_dict(),
                # No `seed_invoked` coordinate. That it is not established that
                # Seed invoked is not the same as its being established that
                # Seed did not, and a caller may declare Seed as the performer.
                # The support and the Unknowns carry exactly what is known.
                "unknowns": [
                    "whether the declared performer performed this remains Unknown",
                    "whether this Seed invoked anything remains Unknown",
                    "what the invocation names remains Unknown",
                ],
                "mutates_cluster": False,
                "provenance_occurrence_refs": [],
            },
        )
    ])[0]


def preserve_system_material(
    ledger: EventLedger,
    *,
    workspace_id: str,
    locality_id: str,
    exact_bytes: bytes,
    observed_boundary: str,
) -> Event:
    """Record that exact system-origin material occurred.

    No invocation is required or referenced. Material the system yielded
    because someone asked, and material it yielded because a process exited or
    a file changed, are the same kind of occurrence here. Whether some
    particular material followed some particular invocation is a relation
    between two preserved subjects, which is its own bounded subject and is not
    established by placing one inside the other.
    """

    if type(exact_bytes) is not bytes:
        raise SystemMaterialError("system material must be exact bytes")
    if type(observed_boundary) is not str or not observed_boundary.strip():
        raise SystemMaterialError("system material requires the boundary it was observed at")
    _require_exchange(locality_id)

    return ledger.append_many([
        Event(
            id=new_id("evt"),
            kind=SYSTEM_MATERIAL_OCCURRED_KIND,
            workspace_id=workspace_id,
            locality_id=locality_id,
            payload={
                "dimensions": {
                    "identity": new_id("system_material"),
                    "content": f"exact material, {len(exact_bytes)} bytes",
                    "standing": "occurred",
                    "source_provenance": observed_boundary,
                    "responsibility": "system-material-occurrence",
                    "authority": "unestablished",
                    "evidence_scope": "occurrence only; represented relation Unknown",
                    "scope_locality": f"workspace:{workspace_id};locality:{locality_id}",
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
                    "what yielded it remains Unknown",
                ],
                "mutates_cluster": False,
                "provenance_occurrence_refs": [],
            },
        )
    ])[0]


def _exact_arguments(argv: tuple[str, ...]) -> tuple[str, ...]:
    if not argv or not all(type(part) is str and part for part in argv):
        raise SystemMaterialError("a system invocation requires exact non-empty arguments")
    return argv


def invoke_system(
    ledger: EventLedger,
    *,
    workspace_id: str,
    locality_id: str,
    command_representation: str,
    argv: tuple[str, ...],
    cwd: str | Path,
    timeout_seconds: float = 60.0,
    max_output_bytes: int = 1_000_000,
) -> SystemInvocationRun:
    """Run one explicitly related representation and argv without a shell.

    ``command_representation`` is never parsed. The caller supplies the exact
    argv relation separately, so ``/ls`` does not silently become ``ls``. The
    attempt is flushed before the process boundary. Returned stream material
    and its relation to the exact process occurrence are recorded separately.
    """

    _require_exchange(locality_id)
    if type(command_representation) is not str or not command_representation:
        raise SystemMaterialError("a system invocation requires an exact representation")
    if type(argv) is not tuple:
        raise SystemMaterialError("a system invocation requires an exact argv tuple")
    exact_argv = _exact_arguments(argv)
    if isinstance(timeout_seconds, bool) or not isinstance(
        timeout_seconds, (int, float)
    ) or timeout_seconds <= 0:
        raise SystemMaterialError("a system invocation timeout must be positive")
    if type(max_output_bytes) is not int or max_output_bytes < 0:
        raise SystemMaterialError(
            "a system invocation output boundary must be non-negative"
        )
    try:
        exact_cwd = Path(cwd).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise SystemMaterialError("a system invocation requires an exact directory") from exc
    root_stat = exact_cwd.stat()
    if not exact_cwd.is_dir():
        raise SystemMaterialError("a system invocation directory must be a directory")

    invocation_id = new_id("system_invocation")
    arguments_relation = ledger.append(
        SYSTEM_INVOCATION_ARGUMENTS_RELATED_KIND,
        workspace_id,
        {
            "invocation_id": invocation_id,
            "command_representation": command_representation,
            "argv": list(exact_argv),
            "standing": "supplied",
            "evidence_scope": (
                "the caller supplied this exact representation-to-argv relation; "
                "no parsing or wider command-language relation is established"
            ),
        },
        locality_id=locality_id,
    )
    attempt = ledger.append(
        SYSTEM_INVOCATION_ATTEMPTED_KIND,
        workspace_id,
        {
            "invocation_id": invocation_id,
            "arguments_relation_event_id": arguments_relation.id,
            "command_representation": command_representation,
            "argv": list(exact_argv),
            "cwd": str(exact_cwd),
            "cwd_device": root_stat.st_dev,
            "cwd_inode": root_stat.st_ino,
            "timeout_seconds": float(timeout_seconds),
            "max_output_bytes": max_output_bytes,
            "standing": "attempt recorded; process outcome Unknown",
            "unknowns": [
                "whether a process occurrence follows remains Unknown",
                "stdout, stderr, and return code remain Unknown",
            ],
        },
        locality_id=locality_id,
    )
    ledger.flush()

    try:
        result = run_process_boundary(
            exact_cwd,
            exact_argv,
            timeout_seconds=timeout_seconds,
            max_output_bytes=max_output_bytes,
        )
    except (OSError, ProcessBoundaryError) as exc:
        ledger.append(
            SYSTEM_INVOCATION_FAILED_KIND,
            workspace_id,
            {
                "invocation_id": invocation_id,
                "attempt_event_id": attempt.id,
                "arguments_relation_event_id": arguments_relation.id,
                "process_occurrence_id": None,
                "standing": "process occurrence not established",
                "failure_type": type(exc).__name__,
                "failure_representation": str(exc),
                "unknowns": [
                    "whether effects occurred beyond this process boundary remains Unknown"
                ],
            },
            locality_id=locality_id,
        )
        raise SystemMaterialError("the declared system invocation did not start") from exc

    process_occurrence_id = new_id("system_invocation_occurrence")
    occurrence = ledger.append(
        SYSTEM_INVOCATION_OCCURRED_KIND,
        workspace_id,
        {
            "invocation_id": invocation_id,
            "process_occurrence_id": process_occurrence_id,
            "attempt_event_id": attempt.id,
            "arguments_relation_event_id": arguments_relation.id,
            "command_representation": command_representation,
            "argv": list(result.argv),
            "cwd": result.cwd,
            "returncode": result.returncode,
            "timed_out": result.timed_out,
            "stdout_total_bytes": result.stdout_total_bytes,
            "stderr_total_bytes": result.stderr_total_bytes,
            "stdout_complete": result.stdout_complete,
            "stderr_complete": result.stderr_complete,
            "standing": "occurred",
            "unknowns": (
                ["return code remains Unknown because the exact timeout elapsed"]
                if result.timed_out
                else []
            ),
        },
        locality_id=locality_id,
    )
    stdout_material = preserve_system_material(
        ledger,
        workspace_id=workspace_id,
        locality_id=locality_id,
        exact_bytes=result.stdout,
        observed_boundary=f"process occurrence {process_occurrence_id}, stdout",
    )
    stderr_material = preserve_system_material(
        ledger,
        workspace_id=workspace_id,
        locality_id=locality_id,
        exact_bytes=result.stderr,
        observed_boundary=f"process occurrence {process_occurrence_id}, stderr",
    )

    def relate(stream_name: str, material: Event, total_bytes: int, complete: bool) -> Event:
        return ledger.append(
            SYSTEM_INVOCATION_MATERIAL_RELATED_KIND,
            workspace_id,
            {
                "invocation_id": invocation_id,
                "process_occurrence_id": process_occurrence_id,
                "process_event_id": occurrence.id,
                "material_occurrence_id": material.id,
                "stream_role": stream_name,
                "preserved_byte_count": material.payload["byte_count"],
                "total_byte_count": total_bytes,
                "complete": complete,
                "standing": "related",
                "evidence_scope": (
                    "this exact process-occurrence-to-stream-material relation only"
                ),
            },
            locality_id=locality_id,
        )

    stdout_relation = relate(
        "stdout", stdout_material, result.stdout_total_bytes, result.stdout_complete
    )
    stderr_relation = relate(
        "stderr", stderr_material, result.stderr_total_bytes, result.stderr_complete
    )
    return SystemInvocationRun(
        arguments_relation=arguments_relation,
        attempt=attempt,
        occurrence=occurrence,
        stdout_material=stdout_material,
        stderr_material=stderr_material,
        stdout_relation=stdout_relation,
        stderr_relation=stderr_relation,
    )


def _require_exchange(locality_id: str) -> None:
    if type(locality_id) is not str or not locality_id.strip():
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
        reconstructed = bytes.fromhex(encoded)
    except ValueError as exc:
        raise SystemMaterialError("system material is not exact bytes") from exc
    if len(reconstructed) != event.payload.get("byte_count"):
        raise SystemMaterialError("system material does not match its byte count")
    return reconstructed
