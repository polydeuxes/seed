"""Operator Ingest, slash commands, Representation, and emission."""

from __future__ import annotations

from typing import BinaryIO, Mapping, TextIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingest import run_operator_ingest
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.operator_command import (
    OperatorCommandHandler,
    is_slash_command,
    run_operator_command,
)
from seed_runtime.operator_checkpoint import (
    OperatorCheckpointRequest,
    open_operator_checkpoint,
    request_operator_checkpoint,
)
from seed_runtime.operator_material_command import (
    OperatorMaterialRequest,
    request_operator_material,
)
from seed_runtime.operator_locality_command import (
    OperatorLocalityRequest,
    request_operator_locality,
)
from seed_runtime.operator_representation import (
    emit_operator_representation,
    record_operator_representation,
)
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_egress import emit_exact_material


def _advance_over(ledger, standing, event_identities, *, locality_identity):
    """Advance carried Standing over occurrences a responsible act just recorded.

    The identities come from the act that recorded them, so nothing here
    searches the ledger for what happened; the events are retrieved by exact
    identity.
    """

    return advance_operator_locality_standing(
        ledger,
        event_identities,
        locality_identity=locality_identity,
        prior=standing,
    )


def run_persistent_operator_console(
    *,
    ledger: EventLedger,
    locality_identity: str,
    input_stream: BinaryIO | TextIO,
    output_stream: TextIO,
    command_handlers: Mapping[bytes, OperatorCommandHandler] | None = None,
    emit_initial_representation: bool = True,
    raw_output_stream: BinaryIO | None = None,
) -> None:
    """Repeat exact-byte Ingest and slash-command occurrences."""
    handlers = dict(command_handlers or {})
    handlers[b"checkpoint"] = request_operator_checkpoint
    handlers[b"material"] = request_operator_material
    handlers[b"locality"] = request_operator_locality
    # Standing is carried through the locality rather than re-projected before
    # each interaction. Each responsible act returns the occurrences it
    # recorded, so the console advances over exactly those occurrences.
    locality_standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    representation = record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=locality_standing,
    )
    if emit_initial_representation:
        representation = emit_operator_representation(
            ledger, representation=representation, output_stream=output_stream
        )
        locality_standing = _advance_over(
            ledger,
            locality_standing,
            (
                representation["representation_event_identity"],
                representation["emission_attempt_event_identity"],
                representation["emitted_event_identity"],
            ),
            locality_identity=locality_identity,
        )
    while True:
        boundary_material = operator_boundary_material(input_stream)
        if boundary_material.eof:
            return
        if is_slash_command(boundary_material):
            command_run = run_operator_command(
                locality_identity=locality_identity,
                addressed_at_representation_event_identity=representation[
                    "representation_event_identity"
                ],
                material=boundary_material,
                handlers=handlers,
            )
            request = command_run.implementation_result
            if isinstance(request, OperatorLocalityRequest):
                if request.locality_identity is None:
                    output_stream.write(
                        "\n".join(
                            event.locality_identity
                            for event in ledger.list()
                            if event.locality_identity is not None
                        )
                        + "\n"
                    )
                    output_stream.flush()
                    continue
                if not ledger.has_locality(request.locality_identity):
                    raise ValueError("/locality requires an existing Locality")
                locality_identity = request.locality_identity
                locality_standing = read_operator_locality_standing(
                    ledger, locality_identity=locality_identity
                )
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                )
                continue
            if isinstance(request, (OperatorCheckpointRequest, OperatorMaterialRequest)):
                checkpoint = open_operator_checkpoint(ledger, command_run.addressed)
                locality_identity = checkpoint.locality_identity
                locality_standing = read_operator_locality_standing(
                    ledger, locality_identity=locality_identity
                )
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                )
                representation = emit_operator_representation(
                    ledger,
                    representation=representation,
                    output_stream=output_stream,
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (
                        representation["representation_event_identity"],
                        representation["emission_attempt_event_identity"],
                        representation["emitted_event_identity"],
                    ),
                    locality_identity=locality_identity,
                )
            continue
        with ledger.batched():
            # No Representation is attached to this Ingest. Selecting one by
            # recency would assert a relation no occurrence determined.
            attempt_record = run_operator_ingest(
                ledger=ledger,
                locality_identity=locality_identity,
                boundary_material=boundary_material,
                locality_standing=(
                    locality_standing if locality_standing["event_count"] else None
                ),
            )
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                (
                    attempt_record["current_standing"]["ingest_occurrence"][
                        "evidence_event_identity"
                    ],
                ),
                locality_identity=locality_identity,
            )
            if attempt_record["current_standing"]["ingest_occurrence"] is not None:
                if raw_output_stream is not None:
                    emit_exact_material(raw_output_stream, boundary_material.exact_bytes)
                    continue
                # The Representation result and Yield Evidence retain distinct identities. No Compare
                # or Identification is inferred merely from temporal proximity.
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                )
                representation = emit_operator_representation(
                    ledger, representation=representation, output_stream=output_stream
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (
                        representation["representation_event_identity"],
                        representation["emission_attempt_event_identity"],
                        representation["emitted_event_identity"],
                    ),
                    locality_identity=locality_identity,
                )
