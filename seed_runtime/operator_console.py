"""Operator Ingest, slash commands, Representation, and emission."""

from __future__ import annotations

from typing import BinaryIO, Mapping, TextIO

from seed_runtime.byte_measurement import (
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
)
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
    emit_operator_representation_material,
    record_operator_representation,
)
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.occurrence_position_measurement import (
    measure_occurrence_position,
    record_occurrence_position_measurement_responsible_act_evidence,
    record_occurrence_position_measurement_result,
)


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


def _advance_over_representation(ledger, standing, representation):
    """Advance over the exact occurrences returned by one Representation act."""

    return _advance_over(
        ledger,
        standing,
        representation["recorded_occurrence_references"],
        locality_identity=representation["locality_identity"],
    )


def run_persistent_operator_console(
    *,
    ledger: EventLedger,
    locality_identity: str,
    input_stream: BinaryIO | TextIO,
    output_stream: TextIO,
    command_handlers: Mapping[bytes, OperatorCommandHandler] | None = None,
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
    locality_standing = _advance_over_representation(
        ledger, locality_standing, representation
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
                    localities = []
                    seen_localities = set()
                    for event in ledger.list():
                        locality = event.locality_identity
                        if locality is not None and locality not in seen_localities:
                            seen_localities.add(locality)
                            localities.append(locality)
                    output_stream.write("\n".join(localities) + "\n")
                    output_stream.flush()
                    continue
                if not request.create_new and not ledger.has_locality(
                    request.locality_identity
                ):
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
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, representation
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
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, representation
                )
            continue
        with ledger.batched():
            attempt_record = run_operator_ingest(
                ledger=ledger,
                locality_identity=locality_identity,
                boundary_material=boundary_material,
                locality_standing=(
                    locality_standing if locality_standing["event_count"] else None
                ),
            )
            ingest_occurrence = attempt_record["current_standing"][
                "ingest_occurrence"
            ]
            if ingest_occurrence is None:
                continue
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                (ingest_occurrence["evidence_event_identity"],),
                locality_identity=locality_identity,
            )
            measurement_act_evidence = (
                record_byte_measurement_responsible_act_evidence(
                    ledger,
                    source_localities=(locality_identity,),
                    recording_locality_identity=locality_identity,
                )
            )
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                (measurement_act_evidence.identity,),
                locality_identity=locality_identity,
            )
            measurement = record_byte_measurement_result(
                ledger,
                responsible_act_evidence_event_identity=(
                    measurement_act_evidence.identity
                ),
            )
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                (
                    measurement.material["yield_evidence_identity"],
                    measurement.identity,
                ),
                locality_identity=locality_identity,
            )
            position_finding = measure_occurrence_position(
                ledger,
                source_locality_identity=locality_identity,
            )
            position_measurement_act_evidence = (
                record_occurrence_position_measurement_responsible_act_evidence(
                    ledger,
                    recording_locality_identity=locality_identity,
                    finding=position_finding,
                )
            )
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                (position_measurement_act_evidence.identity,),
                locality_identity=locality_identity,
            )
            position_measurement = record_occurrence_position_measurement_result(
                ledger,
                finding=position_finding,
                responsible_act_evidence_event_identity=(
                    position_measurement_act_evidence.identity
                ),
            )
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                (
                    position_measurement.material["yield_evidence_identity"],
                    position_measurement.identity,
                ),
                locality_identity=locality_identity,
            )
            if raw_output_stream is not None:
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                    source_occurrence_reference=ingest_occurrence[
                        "evidence_event_identity"
                    ],
                )
                try:
                    emit_operator_representation_material(
                        ledger,
                        representation=representation,
                        output_stream=raw_output_stream,
                    )
                finally:
                    locality_standing = _advance_over_representation(
                        ledger, locality_standing, representation
                    )
                continue
            representation = record_operator_representation(
                ledger,
                locality_identity=locality_identity,
                locality_standing=locality_standing,
            )
            locality_standing = _advance_over_representation(
                ledger, locality_standing, representation
            )
