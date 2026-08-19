"""Operator material acquisition, slash commands, Representation, and emission."""

from __future__ import annotations

from typing import BinaryIO, Mapping, TextIO

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    _record_byte_position_pair_count_layer_from_carried_locality_standing,
    get_byte_position_pair_measurement_responsibility_assignment,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    _record_recorded_pair_measurement_comparison_from_carried_measurements,
)
from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.operator_egress import (
    EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    operator_emission_boundary,
)
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.operator_material_acquisition import (
    _record_operator_material_acquire_responsibility_assignment_from_carried_representation,
    _record_operator_material_acquire_responsible_act_evidence_from_assignment,
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
    _record_operator_representation_from_recorded_pair_measurement,
    emit_operator_representation_material,
    read_operator_representation,
    record_operator_representation,
)
from seed_runtime.operator_representation_admission import (
    record_representation_candidate_responsibility_assignment,
    record_representation_candidate_act_evidence,
    record_representation_candidate_result,
    record_exact_material_representation_admission_responsibility_assignment,
    record_exact_material_representation_admission_act_evidence,
    record_exact_material_representation_admission_result,
    exact_material_representation_admission_occurrence_references,
)
from seed_runtime.operator_representation_applicability import (
    record_representation_emission_applicability_act_evidence,
    record_representation_emission_applicability_result,
    representation_emission_applicability_occurrence_references,
)
from seed_runtime.operator_standing_continuation import (
    record_standing_locality_continuation_responsibility_assignment,
    record_standing_locality_continuation_responsible_act_evidence,
    record_standing_locality_continuation_result,
)
from seed_runtime.operator_invocation_locality import (
    record_operator_invocation_locality_responsibility_assignment,
    record_operator_invocation_locality_act_evidence,
    record_operator_invocation_locality_result,
)
from seed_runtime.standing_boundary_locality import (
    record_recorded_standing_boundary_locality_responsibility_assignment,
    record_recorded_standing_boundary_locality_responsible_act_evidence,
    record_recorded_standing_boundary_locality_result,
)
from seed_runtime.operator_locality_standing import (
    _carry_occurrence_position_measurement_assignment_into_standing,
    _carry_occurrence_position_measurement_result_into_standing,
    _carry_operator_material_acquisition_occurrence_into_standing,
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.occurrence_position_measurement import (
    _record_occurrence_position_measurement_responsibility_assignment_from_carried_standing,
    _record_occurrence_position_measurement_responsible_act_evidence_from_carried_standing,
    _record_occurrence_position_measurement_result_from_carried_act_evidence,
    measure_occurrence_position,
)
from seed_runtime.standing_measurement_declarations import (
    _record_declared_measurements_from_carried_standing,
    record_declared_measurements_from_current_standing,
)
from seed_runtime.supplied_invocation_material import (
    OperatorInvocationProvider,
    SuppliedWitnessMaterialOccurrence,
    acquire_supplied_witness_material_occurrence,
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


def _record_representation_candidate(
    ledger,
    standing,
    representation,
    *,
    destination_operator_boundary,
):
    """Carry one addressed Representation into Candidate Standing."""

    locality_identity = representation["locality_identity"]
    candidate_assignment = (
        record_representation_candidate_responsibility_assignment(
            ledger,
            representation_event_identity=representation[
                "representation_event_identity"
            ],
            locality_standing=standing,
            destination_operator_boundary=destination_operator_boundary,
        )
    )
    standing = _advance_over(
        ledger,
        standing,
        (candidate_assignment.identity,),
        locality_identity=locality_identity,
    )
    candidate_act = record_representation_candidate_act_evidence(
        ledger,
        assignment_event_identity=candidate_assignment.identity,
        locality_standing=standing,
    )
    standing = _advance_over(
        ledger,
        standing,
        (candidate_act.identity,),
        locality_identity=locality_identity,
    )
    candidate = record_representation_candidate_result(
        ledger,
        responsible_act_evidence_event_identity=candidate_act.identity,
    )
    standing = _advance_over(
        ledger,
        standing,
        (
            candidate.material["evidence_of_yield_relation_identity"],
            candidate.identity,
        ),
        locality_identity=locality_identity,
    )
    return standing, candidate


def _record_exact_material_representation_admission_and_applicability(
    ledger,
    standing,
    representation,
    *,
    destination_operator_boundary,
):
    """Carry one exact-material Candidate through Admission Standing."""

    locality_identity = representation["locality_identity"]
    standing, candidate = _record_representation_candidate(
        ledger,
        standing,
        representation,
        destination_operator_boundary=destination_operator_boundary,
    )
    admission_assignment = (
        record_exact_material_representation_admission_responsibility_assignment(
            ledger,
            candidate_result_event_identity=candidate.identity,
            locality_standing=standing,
        )
    )
    standing = _advance_over(
        ledger,
        standing,
        (admission_assignment.identity,),
        locality_identity=locality_identity,
    )
    admission_act = record_exact_material_representation_admission_act_evidence(
        ledger,
        assignment_event_identity=admission_assignment.identity,
        locality_standing=standing,
    )
    standing = _advance_over(
        ledger,
        standing,
        (admission_act.identity,),
        locality_identity=locality_identity,
    )
    admission = record_exact_material_representation_admission_result(
        ledger,
        responsible_act_evidence_event_identity=admission_act.identity,
    )
    standing = _advance_over(
        ledger,
        standing,
        (
            admission.material["evidence_of_yield_relation_identity"],
            admission.identity,
        ),
        locality_identity=locality_identity,
    )
    applicability_act = record_representation_emission_applicability_act_evidence(
        ledger,
        admission_result_event_identity=admission.identity,
        locality_standing=standing,
        destination_operator_boundary=destination_operator_boundary,
    )
    standing = _advance_over(
        ledger,
        standing,
        (applicability_act.identity,),
        locality_identity=locality_identity,
    )
    applicability = record_representation_emission_applicability_result(
        ledger,
        responsible_act_evidence_event_identity=applicability_act.identity,
    )
    standing = _advance_over(
        ledger,
        standing,
        (
            applicability.material["evidence_of_yield_relation_identity"],
            applicability.identity,
        ),
        locality_identity=locality_identity,
    )
    return standing, admission, applicability


def _record_occurrence_position_measurement(
    ledger, standing, *, locality_identity
):
    """Record the explicitly triggered position population of this Locality."""

    position_finding = measure_occurrence_position(
        ledger,
        source_locality_identity=locality_identity,
    )
    position_measurement_assignment = (
        _record_occurrence_position_measurement_responsibility_assignment_from_carried_standing(
            ledger,
            recording_locality_identity=locality_identity,
            finding=position_finding,
            locality_standing=standing,
        )
    )
    standing = _carry_occurrence_position_measurement_assignment_into_standing(
        ledger,
        standing,
        position_measurement_assignment,
        position_finding,
        prior_through_event_occurrence_identity=standing[
            "through_event_occurrence_identity"
        ],
    )
    position_measurement_act_evidence = (
        _record_occurrence_position_measurement_responsible_act_evidence_from_carried_standing(
            ledger,
            responsibility_assignment=position_measurement_assignment,
            finding=position_finding,
            responsibility_assignment_standing=standing,
        )
    )
    standing = _advance_over(
        ledger,
        standing,
        (position_measurement_act_evidence.identity,),
        locality_identity=locality_identity,
    )
    position_measurement = (
        _record_occurrence_position_measurement_result_from_carried_act_evidence(
            ledger,
            responsible_act_evidence=position_measurement_act_evidence,
            responsibility_assignment=position_measurement_assignment,
            finding=position_finding,
        )
    )
    standing = _carry_occurrence_position_measurement_result_into_standing(
        ledger,
        standing,
        position_measurement,
        responsible_act_evidence=position_measurement_act_evidence,
        responsibility_assignment=position_measurement_assignment,
        finding=position_finding,
    )
    return standing


def _record_occurrence_position_after_declared_measurements(
    ledger, recorded, *, locality_identity
):
    byte_measurements = tuple(
        event
        for event in recorded.result_occurrences
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    )
    if len(byte_measurements) != 1:
        raise ValueError("one exact-byte Measurement is required after this pin")
    standing = _record_occurrence_position_measurement(
        ledger,
        recorded.locality_standing,
        locality_identity=locality_identity,
    )
    return standing, byte_measurements[0]


def _record_measurements_after_pin(ledger, standing, *, locality_identity):
    """Exhaust declared material acquisition roads, then record the explicit Locality road."""

    recorded = _record_declared_measurements_from_carried_standing(
        ledger,
        standing,
        locality_identity=locality_identity,
    )
    return _record_occurrence_position_after_declared_measurements(
        ledger,
        recorded,
        locality_identity=locality_identity,
    )


def _record_measurements_after_current_pin(ledger, *, locality_identity):
    """Exhaust declarations from independently read current Locality Standing."""

    recorded = record_declared_measurements_from_current_standing(
        ledger,
        locality_identity=locality_identity,
    )
    return _record_occurrence_position_after_declared_measurements(
        ledger,
        recorded,
        locality_identity=locality_identity,
    )


def _record_pair_measurement(
    ledger,
    standing,
    *,
    byte_measurement_event_identity,
    locality_identity,
):
    """Record one pair Measurement only after an exact consumer relation exists."""

    pair_measurement, standing = (
        _record_byte_position_pair_count_layer_from_carried_locality_standing(
            ledger,
            source_measurement_event_identity=byte_measurement_event_identity,
            recording_locality_identity=locality_identity,
            locality_standing=standing,
        )
    )
    return standing, pair_measurement


def _pair_premise_for_existing_material(
    ledger,
    standing,
    *,
    locality_identity,
):
    """Address the latest pair premise, or record one for existing material-acquisition results."""

    if not standing["material_acquisition_result_occurrences"]:
        return standing, None
    current_source_occurrence_references = tuple(
        occurrence["result_occurrence_identity"]
        for occurrence in standing["material_acquisition_result_occurrences"]
    )
    for event_identity in reversed(tuple(standing["measurement_occurrences"])):
        event = ledger.get(event_identity)
        reference = (
            event.material.get("responsibility_assignment_reference")
            if event is not None
            else None
        )
        try:
            assignment = get_byte_position_pair_measurement_responsibility_assignment(
                ledger,
                reference.get("recorded_occurrence_identity")
                if type(reference) is dict
                else None,
            )
        except (TypeError, ValueError):
            assignment = None
        source_occurrence_references = (
            assignment.material.get("source_occurrence_references")
            if assignment is not None
            else None
        )
        if (
            event is not None
            and event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
            and event.locality_identity == locality_identity
            and type(source_occurrence_references) is list
            and tuple(
                reference.get("material_acquisition_occurrence_identity")
                for reference in source_occurrence_references
                if type(reference) is dict
            )
            == current_source_occurrence_references
        ):
            return standing, event
    standing, byte_measurement = _record_measurements_after_current_pin(
        ledger,
        locality_identity=locality_identity,
    )
    return _record_pair_measurement(
        ledger,
        standing,
        byte_measurement_event_identity=byte_measurement.identity,
        locality_identity=locality_identity,
    )


def _representation_source_for_pair_premise(ledger, standing, pair_premise):
    """Recover the Compare that names this exact pair premise, where carried."""

    if pair_premise is None:
        return None
    for comparison_identity in reversed(
        tuple(standing["comparison_result_occurrences"])
    ):
        comparison = ledger.get(comparison_identity)
        assignment_reference = (
            comparison.material.get("responsibility_assignment_reference")
            if comparison is not None
            else None
        )
        assignment = (
            ledger.get(assignment_reference.get("recorded_occurrence_identity"))
            if type(assignment_reference) is dict
            else None
        )
        later_measurement_reference = (
            assignment.material.get("later_measurement_reference")
            if assignment is not None
            else None
        )
        if (
            type(later_measurement_reference) is dict
            and later_measurement_reference.get("recorded_occurrence_identity")
            == pair_premise.identity
        ):
            return comparison_identity
    return pair_premise.identity


def _record_pair_measurement_comparison(
    ledger,
    standing,
    *,
    earlier_pair_measurement,
    later_pair_measurement,
    locality_identity,
):
    """Carry first and second produced pair results into their responsible Compare."""

    if (
        type(earlier_pair_measurement) is not Event
        or type(later_pair_measurement) is not Event
        or earlier_pair_measurement.locality_identity != locality_identity
        or later_pair_measurement.locality_identity != locality_identity
    ):
        raise ValueError("pair Compare requires first and second carried Measurements")
    result, standing = (
        _record_recorded_pair_measurement_comparison_from_carried_measurements(
            ledger,
            earlier_measurement=earlier_pair_measurement,
            later_measurement=later_pair_measurement,
            locality_standing=standing,
        )
    )
    return standing, result


def run_persistent_operator_console(
    *,
    ledger: EventLedger,
    locality_identity: str,
    input_stream: BinaryIO | TextIO,
    output_stream: TextIO,
    command_handlers: Mapping[bytes, OperatorCommandHandler] | None = None,
    raw_output_stream: BinaryIO | None = None,
    operator_invocation_provider: OperatorInvocationProvider | None = None,
) -> None:
    """Repeat exact-byte material acquisition and slash-command occurrences."""
    if operator_invocation_provider is not None and raw_output_stream is None:
        raise ValueError("exact output boundary required")
    operator_egress_boundary_identity = (
        new_identity("operator_egress_boundary")
        if raw_output_stream is not None
        else None
    )

    handlers = dict(command_handlers or {})
    handlers[b"checkpoint"] = request_operator_checkpoint
    handlers[b"checkout"] = request_operator_checkout
    handlers[b"memory"] = request_operator_memory
    handlers[b"locality"] = request_operator_locality
    # Each produced result enters the current Locality Standing.  This
    # Standing is the input of the next interaction.
    locality_standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    locality_standing, pair_premise = _pair_premise_for_existing_material(
        ledger,
        locality_standing,
        locality_identity=locality_identity,
    )
    representation_source = _representation_source_for_pair_premise(
        ledger, locality_standing, pair_premise
    )
    if (
        pair_premise is not None
        and representation_source == pair_premise.identity
        and locality_standing["through_event_occurrence_identity"]
        == pair_premise.identity
    ):
        representation = (
            _record_operator_representation_from_recorded_pair_measurement(
                ledger,
                locality_identity=locality_identity,
                locality_standing=locality_standing,
                pair_measurement=pair_premise,
            )
        )
    else:
        representation = record_operator_representation(
            ledger,
            locality_identity=locality_identity,
            locality_standing=locality_standing,
            source_occurrence_reference=representation_source,
        )
    locality_standing = _advance_over_representation(
        ledger, locality_standing, representation
    )
    while True:
        acquire_assignment = (
            _record_operator_material_acquire_responsibility_assignment_from_carried_representation(
                ledger,
                locality_identity=locality_identity,
                representation=representation,
                locality_standing=locality_standing,
            )
        )
        locality_standing = (
            _carry_operator_material_acquisition_occurrence_into_standing(
                locality_standing,
                acquire_assignment,
                prior_through_event_occurrence_identity=representation[
                    "representation_event_identity"
                ],
            )
        )
        acquire_act_evidence = (
            _record_operator_material_acquire_responsible_act_evidence_from_assignment(
                ledger,
                responsibility_assignment=acquire_assignment,
                responsibility_assignment_standing=locality_standing,
            )
        )
        locality_standing = (
            _carry_operator_material_acquisition_occurrence_into_standing(
                locality_standing,
                acquire_act_evidence,
                prior_through_event_occurrence_identity=(
                    acquire_assignment.identity
                ),
            )
        )
        input_boundary = ledger.append_boundary()
        boundary_material = operator_boundary_material(input_stream)
        if ledger.append_boundary() != input_boundary:
            raise ValueError(
                "operator boundary invocation appended an occurrence before its result"
            )
        if boundary_material.eof:
            return
        acquired_material = record_operator_material_acquire_result(
            ledger,
            responsible_act_evidence_event_identity=acquire_act_evidence.identity,
            boundary_material=boundary_material,
        )
        locality_standing = (
            _carry_operator_material_acquisition_occurrence_into_standing(
                locality_standing,
                acquired_material,
                prior_through_event_occurrence_identity=(
                    acquire_act_evidence.identity
                ),
            )
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
            operator_invocation_provider is not None
            and boundary_material.exact_bytes.startswith(b"!")
        ):
            operator_locality_identity = locality_identity
            with ledger.batched():
                command_occurrence_reference = acquired_material.identity
                locality_standing, _byte_measurement = _record_measurements_after_pin(
                    ledger,
                    locality_standing,
                    locality_identity=locality_identity,
                )
                command_representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                    source_occurrence_reference=command_occurrence_reference,
                )
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, command_representation
                )
                command_material = read_operator_representation(
                    ledger,
                    command_representation["representation_event_identity"],
                )["exact_material"]
                relation_assignment = (
                    record_operator_invocation_locality_responsibility_assignment(
                        ledger,
                        operator_material_occurrence_reference=(
                            command_occurrence_reference
                        ),
                        operator_locality_standing=locality_standing,
                    )
                )
                representation = record_operator_representation(
                    ledger,
                    locality_identity=operator_locality_identity,
                    locality_standing=locality_standing,
                )
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, representation
                )
                invocation_locality_identity = relation_assignment.material[
                    "destination_locality_identity"
                ]
                witness_standing = read_operator_locality_standing(
                    ledger, locality_identity=invocation_locality_identity
                )
                relation_act = record_operator_invocation_locality_act_evidence(
                    ledger,
                    responsibility_assignment_event_identity=(
                        relation_assignment.identity
                    ),
                    responsibility_assignment_standing=witness_standing,
                )
                witness_standing = _advance_over(
                    ledger,
                    witness_standing,
                    (relation_act.identity,),
                    locality_identity=invocation_locality_identity,
                )
                relation_result = record_operator_invocation_locality_result(
                    ledger,
                    responsible_act_evidence_event_identity=relation_act.identity,
                )
                witness_standing = _advance_over(
                    ledger,
                    witness_standing,
                    (
                        relation_result.material[
                            "evidence_of_yield_relation_identity"
                        ],
                        relation_result.identity,
                    ),
                    locality_identity=invocation_locality_identity,
                )
            supplied_boundaries: set[str] = set()
            supplied_occurrence_count = 0
            supplied_occurrence_references: list[str] = []
            provider_boundary = ledger.append_boundary()

            def acquire_witness_material(supplied) -> None:
                nonlocal witness_standing
                nonlocal supplied_occurrence_count
                nonlocal provider_boundary
                if ledger.append_boundary() != provider_boundary:
                    raise ValueError(
                        "provider appended an occurrence outside supplied material"
                    )
                if type(supplied) is not SuppliedWitnessMaterialOccurrence:
                    raise TypeError("exact supplied material required")
                if supplied.source_boundary in supplied_boundaries:
                    raise ValueError("distinct source boundary required")
                supplied_boundaries.add(supplied.source_boundary)
                supplied_occurrence = acquire_supplied_witness_material_occurrence(
                    ledger,
                    operator_invocation_locality_result_event_identity=(
                        relation_result.identity
                    ),
                    command_occurrence_reference=command_occurrence_reference,
                    supplied=supplied,
                    prior_supplied_occurrence_references=tuple(
                        supplied_occurrence_references
                    ),
                )
                supplied_occurrence_references.append(supplied_occurrence.identity)
                supplied_occurrence_count += 1
                witness_standing = _advance_over(
                    ledger,
                    witness_standing,
                    (supplied_occurrence.identity,),
                    locality_identity=invocation_locality_identity,
                )
                witness_standing, _byte_measurement = _record_measurements_after_pin(
                    ledger,
                    witness_standing,
                    locality_identity=invocation_locality_identity,
                )
                provider_boundary = ledger.append_boundary()

            provider_result = operator_invocation_provider(
                command_material,
                acquire_witness_material,
            )
            if ledger.append_boundary() != provider_boundary:
                raise ValueError(
                    "provider appended an occurrence outside supplied material"
                )
            if provider_result is not None or not supplied_occurrence_count:
                raise TypeError("exact supplied material required")
            with ledger.batched():
                witness_representation = record_operator_representation(
                    ledger,
                    locality_identity=invocation_locality_identity,
                    locality_standing=witness_standing,
                )
                witness_standing = _advance_over_representation(
                    ledger, witness_standing, witness_representation
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
                if not request.create_new and not ledger.has_locality(
                    request.locality_identity
                ):
                    raise ValueError("/locality requires an existing Locality")
                locality_identity = request.locality_identity
                locality_standing = read_operator_locality_standing(
                    ledger, locality_identity=locality_identity
                )
                locality_standing, pair_premise = (
                    _pair_premise_for_existing_material(
                        ledger,
                        locality_standing,
                        locality_identity=locality_identity,
                    )
                )
                representation_source = _representation_source_for_pair_premise(
                    ledger, locality_standing, pair_premise
                )
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                    source_occurrence_reference=representation_source,
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
                pair_premise = None
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
                        continuation.material["evidence_of_yield_relation_identity"],
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
                        checkpoint.material["evidence_of_yield_relation_identity"],
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
                pair_premise = None
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
                        relation.material["evidence_of_yield_relation_identity"],
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
            locality_standing, byte_measurement = _record_measurements_after_pin(
                ledger,
                locality_standing,
                locality_identity=locality_identity,
            )
            if pair_premise is None:
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                )
            else:
                locality_standing, later_pair = _record_pair_measurement(
                    ledger,
                    locality_standing,
                    byte_measurement_event_identity=byte_measurement.identity,
                    locality_identity=locality_identity,
                )
                locality_standing, comparison = (
                    _record_pair_measurement_comparison(
                        ledger,
                        locality_standing,
                        earlier_pair_measurement=pair_premise,
                        later_pair_measurement=later_pair,
                        locality_identity=locality_identity,
                    )
                )
                pair_premise = later_pair
                representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                    source_occurrence_reference=comparison.identity,
                )
            locality_standing = _advance_over_representation(
                ledger, locality_standing, representation
            )
