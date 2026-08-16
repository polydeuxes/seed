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
from seed_runtime.operator_material_acquisition import (
    record_operator_material_acquire_responsibility_assignment,
    record_operator_material_acquire_responsible_act_evidence,
    record_operator_material_acquire_result,
)
from seed_runtime.operator_command import (
    OperatorCommandHandler,
    is_slash_command,
    run_operator_command,
)
from seed_runtime.operator_checkpoint import (
    OperatorCheckpointRequest,
    record_standing_boundary_reference_responsibility_assignment,
    record_standing_boundary_reference_responsible_act_evidence,
    record_standing_boundary_reference_result,
    request_operator_checkpoint,
)
from seed_runtime.operator_checkout import (
    OperatorCheckoutRequest,
    request_operator_checkout,
)
from seed_runtime.operator_memory_command import (
    OperatorMemoryRequest,
    request_operator_memory,
)
from seed_runtime.operator_locality_command import (
    OperatorLocalityRequest,
    request_operator_locality,
)
from seed_runtime.operator_representation import (
    emit_operator_representation_material,
    record_operator_representation,
)
from seed_runtime.operator_standing_continuation import (
    record_standing_locality_continuation_responsibility_assignment,
    record_standing_locality_continuation_responsible_act_evidence,
    record_standing_locality_continuation_result,
)
from seed_runtime.standing_boundary_locality import (
    record_recorded_standing_boundary_locality_responsibility_assignment,
    record_recorded_standing_boundary_locality_responsible_act_evidence,
    record_recorded_standing_boundary_locality_result,
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
from seed_runtime.supplied_invocation_material import (
    SuppliedInvocationProvider,
    ingest_supplied_invocation_material,
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


def _record_acquisition_measurements(ledger, standing, *, locality_identity):
    """Record the live Measurements over the current exact Locality boundary."""

    measurement_act_evidence = record_byte_measurement_responsible_act_evidence(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
    )
    standing = _advance_over(
        ledger,
        standing,
        (measurement_act_evidence.identity,),
        locality_identity=locality_identity,
    )
    measurement = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=measurement_act_evidence.identity,
    )
    standing = _advance_over(
        ledger,
        standing,
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
    standing = _advance_over(
        ledger,
        standing,
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
    return _advance_over(
        ledger,
        standing,
        (
            position_measurement.material["yield_evidence_identity"],
            position_measurement.identity,
        ),
        locality_identity=locality_identity,
    )


def run_persistent_operator_console(
    *,
    ledger: EventLedger,
    locality_identity: str,
    input_stream: BinaryIO | TextIO,
    output_stream: TextIO,
    command_handlers: Mapping[bytes, OperatorCommandHandler] | None = None,
    raw_output_stream: BinaryIO | None = None,
    host_invocation_provider: SuppliedInvocationProvider | None = None,
) -> None:
    """Repeat exact-byte Ingest and slash-command occurrences."""
    if host_invocation_provider is not None and raw_output_stream is None:
        raise ValueError("exact output boundary required")
    handlers = dict(command_handlers or {})
    handlers[b"checkpoint"] = request_operator_checkpoint
    handlers[b"checkout"] = request_operator_checkout
    handlers[b"memory"] = request_operator_memory
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
        acquire_assignment = (
            record_operator_material_acquire_responsibility_assignment(
                ledger,
                locality_identity=locality_identity,
                addressed_representation_event_identity=representation[
                    "representation_event_identity"
                ],
                locality_standing=locality_standing,
            )
        )
        locality_standing = _advance_over(
            ledger,
            locality_standing,
            (acquire_assignment.identity,),
            locality_identity=locality_identity,
        )
        acquire_act_evidence = (
            record_operator_material_acquire_responsible_act_evidence(
                ledger,
                responsibility_assignment_event_identity=(
                    acquire_assignment.identity
                ),
                responsibility_assignment_standing=locality_standing,
            )
        )
        locality_standing = _advance_over(
            ledger,
            locality_standing,
            (acquire_act_evidence.identity,),
            locality_identity=locality_identity,
        )
        boundary_material = operator_boundary_material(input_stream)
        if boundary_material.eof:
            return
        acquired_material = record_operator_material_acquire_result(
            ledger,
            responsible_act_evidence_event_identity=acquire_act_evidence.identity,
            boundary_material=boundary_material,
        )
        locality_standing = _advance_over(
            ledger,
            locality_standing,
            (
                acquired_material.material["yield_evidence_identity"],
                acquired_material.identity,
            ),
            locality_identity=locality_identity,
        )
        representation = record_operator_representation(
            ledger,
            locality_identity=locality_identity,
            locality_standing=locality_standing,
            source_occurrence_reference=acquired_material.identity,
        )
        locality_standing = _advance_over_representation(
            ledger, locality_standing, representation
        )
        if (
            host_invocation_provider is not None
            and boundary_material.exact_bytes.startswith(b"!")
        ):
            with ledger.batched():
                command_record = run_operator_ingest(
                    ledger=ledger,
                    locality_identity=locality_identity,
                    boundary_material=boundary_material,
                    locality_standing=(
                        locality_standing
                        if locality_standing["event_count"]
                        else None
                    ),
                )
                command_occurrence = command_record["current_standing"][
                    "ingest_occurrence"
                ]
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (command_occurrence["evidence_event_identity"],),
                    locality_identity=locality_identity,
                )
                locality_standing = _record_acquisition_measurements(
                    ledger,
                    locality_standing,
                    locality_identity=locality_identity,
                )
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                )
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, representation
                )
            supplied = host_invocation_provider(boundary_material.exact_bytes)
            with ledger.batched():
                supplied_occurrences = ingest_supplied_invocation_material(
                    ledger,
                    locality_identity=locality_identity,
                    command_occurrence_reference=command_occurrence[
                        "evidence_event_identity"
                    ],
                    supplied=supplied,
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    tuple(
                        occurrence.identity
                        for occurrence in supplied_occurrences
                    ),
                    locality_identity=locality_identity,
                )
                locality_standing = _record_acquisition_measurements(
                    ledger,
                    locality_standing,
                    locality_identity=locality_identity,
                )
                for egress_occurrence_position in (
                    supplied.egress_occurrence_positions
                ):
                    supplied_occurrence = supplied_occurrences[
                        egress_occurrence_position
                    ]
                    representation = record_operator_representation(
                        ledger,
                        locality_identity=locality_identity,
                        locality_standing=locality_standing,
                        source_occurrence_reference=supplied_occurrence.identity,
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
            if isinstance(request, OperatorMemoryRequest):
                assignment = (
                    record_standing_locality_continuation_responsibility_assignment(
                        ledger,
                        source_locality_identity=locality_identity,
                        addressed_representation_event_identity=representation[
                            "representation_event_identity"
                        ],
                    )
                )
                locality_identity = assignment.locality_identity
                locality_standing = read_operator_locality_standing(
                    ledger, locality_identity=locality_identity
                )
                assignment_representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                )
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, assignment_representation
                )
                continuation_act_evidence = (
                    record_standing_locality_continuation_responsible_act_evidence(
                        ledger,
                        responsibility_assignment_event_identity=assignment.identity,
                        responsibility_assignment_standing=locality_standing,
                    )
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (continuation_act_evidence.identity,),
                    locality_identity=locality_identity,
                )
                act_evidence_representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                )
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, act_evidence_representation
                )
                continuation = record_standing_locality_continuation_result(
                    ledger,
                    responsible_act_evidence_event_identity=(
                        continuation_act_evidence.identity
                    ),
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (
                        continuation.material["yield_evidence_identity"],
                        continuation.identity,
                    ),
                    locality_identity=locality_identity,
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
            if isinstance(request, OperatorCheckpointRequest):
                assignment = (
                    record_standing_boundary_reference_responsibility_assignment(
                        ledger,
                        addressed_command=command_run.addressed,
                        locality_standing=locality_standing,
                    )
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (assignment.identity,),
                    locality_identity=locality_identity,
                )
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                )
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, representation
                )
                act_evidence = (
                    record_standing_boundary_reference_responsible_act_evidence(
                        ledger,
                        responsibility_assignment_event_identity=assignment.identity,
                        responsibility_assignment_standing=locality_standing,
                    )
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (act_evidence.identity,),
                    locality_identity=locality_identity,
                )
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                )
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, representation
                )
                checkpoint = record_standing_boundary_reference_result(
                    ledger,
                    responsible_act_evidence_event_identity=act_evidence.identity,
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (
                        checkpoint.material["yield_evidence_identity"],
                        checkpoint.identity,
                    ),
                    locality_identity=locality_identity,
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
            if isinstance(request, OperatorCheckoutRequest):
                assignment = (
                    record_recorded_standing_boundary_locality_responsibility_assignment(
                        ledger,
                        source_locality_standing=locality_standing,
                    )
                )
                locality_identity = assignment.locality_identity
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
                act_evidence = (
                    record_recorded_standing_boundary_locality_responsible_act_evidence(
                        ledger,
                        responsibility_assignment_event_identity=assignment.identity,
                        responsibility_assignment_standing=locality_standing,
                    )
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (act_evidence.identity,),
                    locality_identity=locality_identity,
                )
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                )
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, representation
                )
                relation = record_recorded_standing_boundary_locality_result(
                    ledger,
                    responsible_act_evidence_event_identity=act_evidence.identity,
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (
                        relation.material["yield_evidence_identity"],
                        relation.identity,
                    ),
                    locality_identity=locality_identity,
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
            if request is not None or command_run.addressed.frame.name in handlers:
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
            locality_standing = _record_acquisition_measurements(
                ledger,
                locality_standing,
                locality_identity=locality_identity,
            )
            representation = record_operator_representation(
                ledger,
                locality_identity=locality_identity,
                locality_standing=locality_standing,
            )
            locality_standing = _advance_over_representation(
                ledger, locality_standing, representation
            )
