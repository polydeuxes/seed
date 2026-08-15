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
from seed_runtime.operator_material_command import request_operator_material
from seed_runtime.operator_representation import (
    emit_operator_representation,
    record_operator_representation,
)
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)


def _advance_over(ledger, standing, event_ids, *, locality_id):
    """Advance carried Standing over occurrences a responsible act just recorded.

    The identifiers come from the act that recorded them, so nothing here
    searches the ledger for what happened; the events are retrieved by exact
    identifier.
    """

    return advance_operator_locality_standing(
        [ledger.get(event_id) for event_id in event_ids],
        locality_id=locality_id,
        prior=standing,
    )


def run_persistent_operator_console(
    *,
    ledger: EventLedger,
    locality_id: str,
    input_stream: BinaryIO | TextIO,
    output_stream: TextIO,
    command_handlers: Mapping[bytes, OperatorCommandHandler] | None = None,
) -> None:
    """Repeat exact-byte Ingest and slash-command occurrences."""
    handlers = dict(command_handlers or {})
    handlers[b"checkpoint"] = request_operator_checkpoint
    handlers[b"material"] = request_operator_material
    # Standing is carried through the locality rather than re-projected before
    # each interaction. Each responsible act returns the occurrences it
    # recorded, so the console advances over exactly those occurrences.
    locality_standing = read_operator_locality_standing(
        ledger, locality_id=locality_id
    )
    representation = record_operator_representation(
        ledger,
        locality_id=locality_id,
        locality_standing=locality_standing,
    )
    representation = emit_operator_representation(
        ledger, representation=representation, output_stream=output_stream
    )
    locality_standing = _advance_over(
        ledger,
        locality_standing,
        (
            representation["representation_event_id"],
            representation["emission_attempt_event_id"],
            representation["emitted_event_id"],
        ),
        locality_id=locality_id,
    )
    while True:
        boundary_material = operator_boundary_material(input_stream)
        if boundary_material.eof:
            return
        if is_slash_command(boundary_material):
            command_run = run_operator_command(
                ledger=ledger,
                locality_id=locality_id,
                addressed_at_representation_event_id=representation[
                    "representation_event_id"
                ],
                material=boundary_material,
                handlers=handlers,
            )
            request = command_run.implementation_result
            if isinstance(request, OperatorCheckpointRequest):
                checkpoint = open_operator_checkpoint(ledger, command_run.addressed)
                locality_id = checkpoint.locality_id
                locality_standing = read_operator_locality_standing(
                    ledger, locality_id=locality_id
                )
                representation = record_operator_representation(
                    ledger,
                    locality_id=locality_id,
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
                        representation["representation_event_id"],
                        representation["emission_attempt_event_id"],
                        representation["emitted_event_id"],
                    ),
                    locality_id=locality_id,
                )
            continue
        with ledger.batched():
            # No Representation is attached to this Ingest. Selecting one by
            # recency would assert a relation no occurrence determined.
            attempt_record = run_operator_ingest(
                ledger=ledger,
                locality_id=locality_id,
                boundary_material=boundary_material,
                locality_standing=(
                    locality_standing if locality_standing["event_count"] else None
                ),
            )
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                attempt_record["event_ids"],
                locality_id=locality_id,
            )
            if attempt_record["current_standing"]["ingest_occurrence"] is not None:
                # The yielded Representation is preserved independently. No Compare
                # or Identification is inferred merely from temporal proximity.
                representation = record_operator_representation(
                    ledger,
                    locality_id=locality_id,
                    locality_standing=locality_standing,
                )
                representation = emit_operator_representation(
                    ledger, representation=representation, output_stream=output_stream
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (
                        representation["representation_event_id"],
                        representation["emission_attempt_event_id"],
                        representation["emitted_event_id"],
                    ),
                    locality_id=locality_id,
                )
