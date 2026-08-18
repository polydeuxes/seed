"""Operator Ingest, slash commands, Representation, and emission."""

from __future__ import annotations

from typing import BinaryIO, Mapping, TextIO

from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    _record_recorded_pair_measurement_comparison_from_carried_measurements,
)
from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.operator_ingest import run_operator_ingest
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
from seed_runtime.operator_system_locality import (
    record_operator_system_locality_responsibility_assignment,
    record_operator_system_locality_act_evidence,
    record_operator_system_locality_result,
)
from seed_runtime.standing_boundary_locality import (
    record_recorded_standing_boundary_locality_responsibility_assignment,
    record_recorded_standing_boundary_locality_responsible_act_evidence,
    record_recorded_standing_boundary_locality_result,
)
from seed_runtime.operator_locality_standing import (
    _carry_operator_material_acquisition_occurrence_into_standing,
    _carry_recorded_pair_measurement_into_standing,
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.occurrence_position_measurement import (
    measure_occurrence_position,
    record_occurrence_position_measurement_responsibility_assignment,
    record_occurrence_position_measurement_responsible_act_evidence,
    record_occurrence_position_measurement_result,
)
from seed_runtime.supplied_invocation_material import (
    OperatorInvocationProvider,
    SuppliedSystemMaterialOccurrence,
    ingest_supplied_invocation_occurrence,
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


def _record_acquisition_measurements(ledger, standing, *, locality_identity):
    """Record acquisition Measurements needed before any later relation is known."""

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
            measurement.material["evidence_of_yield_relation_identity"],
            measurement.identity,
        ),
        locality_identity=locality_identity,
    )
    position_finding = measure_occurrence_position(
        ledger,
        source_locality_identity=locality_identity,
    )
    position_measurement_assignment = (
        record_occurrence_position_measurement_responsibility_assignment(
            ledger,
            recording_locality_identity=locality_identity,
            finding=position_finding,
            locality_standing=standing,
        )
    )
    standing = _advance_over(
        ledger,
        standing,
        (position_measurement_assignment.identity,),
        locality_identity=locality_identity,
    )
    position_measurement_act_evidence = (
        record_occurrence_position_measurement_responsible_act_evidence(
            ledger,
            responsibility_assignment_event_identity=(
                position_measurement_assignment.identity
            ),
            responsibility_assignment_standing=standing,
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
        responsible_act_evidence_event_identity=(
            position_measurement_act_evidence.identity
        ),
    )
    standing = _advance_over(
        ledger,
        standing,
        (
            position_measurement.material["evidence_of_yield_relation_identity"],
            position_measurement.identity,
        ),
        locality_identity=locality_identity,
    )
    return standing, measurement


def _record_pair_measurement(
    ledger,
    standing,
    *,
    byte_measurement_event_identity,
    locality_identity,
):
    """Record one pair Measurement only after an exact consumer relation exists."""

    prior_through_event_occurrence_identity = standing[
        "through_event_occurrence_identity"
    ]
    pair_measurement = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_measurement_event_identity,
        recording_locality_identity=locality_identity,
    )
    applicability = ledger.get(
        pair_measurement.material["input_applicability_event_identity"]
    )
    if applicability is None:
        raise ValueError("recorded pair Measurement carries no Applicability")
    standing = _advance_over(
        ledger,
        standing,
        (
            applicability.material["responsible_act_evidence_identity"],
            applicability.material["evidence_of_yield_relation_identity"],
            applicability.identity,
            pair_measurement.material["responsible_act_evidence_identity"],
            pair_measurement.material["evidence_of_yield_relation_identity"],
        ),
        locality_identity=locality_identity,
    )
    standing = _carry_recorded_pair_measurement_into_standing(
        standing,
        pair_measurement,
        prior_through_event_occurrence_identity=(
            prior_through_event_occurrence_identity
        ),
    )
    return standing, pair_measurement


def _pair_premise_for_existing_material(
    ledger,
    standing,
    *,
    locality_identity,
):
    """Address the latest pair premise, or record one for existing Ingests."""

    if not standing["ingest_occurrences"]:
        return standing, None
    current_source_occurrence_references = tuple(
        occurrence["evidence_event_identity"]
        for occurrence in standing["ingest_occurrences"]
    )
    for event_identity in reversed(tuple(standing["measurement_occurrences"])):
        event = ledger.get(event_identity)
        source_occurrence_references = (
            event.material.get("responsibility_assignment_evidence", {}).get(
                "source_occurrence_references"
            )
            if event is not None
            else None
        )
        if (
            event is not None
            and event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
            and event.locality_identity == locality_identity
            and type(source_occurrence_references) is list
            and tuple(
                reference.get("ingest_occurrence_identity")
                for reference in source_occurrence_references
                if type(reference) is dict
            )
            == current_source_occurrence_references
        ):
            return standing, event
    standing, byte_measurement = _record_acquisition_measurements(
        ledger,
        standing,
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
    """Carry two produced pair results into their responsible Compare."""

    if (
        type(earlier_pair_measurement) is not Event
        or type(later_pair_measurement) is not Event
        or earlier_pair_measurement.locality_identity != locality_identity
        or later_pair_measurement.locality_identity != locality_identity
    ):
        raise ValueError("pair Compare requires two carried Measurements")
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
    """Repeat exact-byte Ingest and slash-command occurrences."""
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
    # Standing is carried through the locality rather than re-projected before
    # each interaction. Each responsible act returns the occurrences it
    # recorded, so the console advances over exactly those occurrences.
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
        boundary_material = operator_boundary_material(input_stream)
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
                command_record = run_operator_ingest(
                    ledger=ledger,
                    locality_identity=locality_identity,
                    boundary_material=boundary_material,
                    locality_standing=(
                        locality_standing
                        if locality_standing["event_count"]
                        else None
                    ),
                    operator_material_occurrence_reference=(
                        acquired_material.identity
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
                locality_standing, _byte_measurement = _record_acquisition_measurements(
                    ledger,
                    locality_standing,
                    locality_identity=locality_identity,
                )
                command_representation = record_operator_representation(
                    ledger,
                    locality_identity=locality_identity,
                    locality_standing=locality_standing,
                    source_occurrence_reference=command_occurrence[
                        "evidence_event_identity"
                    ],
                )
                locality_standing = _advance_over_representation(
                    ledger, locality_standing, command_representation
                )
                command_material = read_operator_representation(
                    ledger,
                    command_representation["representation_event_identity"],
                )["exact_material"]
                relation_assignment = (
                    record_operator_system_locality_responsibility_assignment(
                        ledger,
                        operator_material_occurrence_reference=(
                            command_occurrence["evidence_event_identity"]
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
                system_locality_identity = relation_assignment.material[
                    "destination_locality_identity"
                ]
                system_standing = read_operator_locality_standing(
                    ledger, locality_identity=system_locality_identity
                )
                relation_act = record_operator_system_locality_act_evidence(
                    ledger,
                    responsibility_assignment_event_identity=(
                        relation_assignment.identity
                    ),
                    responsibility_assignment_standing=system_standing,
                )
                system_standing = _advance_over(
                    ledger,
                    system_standing,
                    (relation_act.identity,),
                    locality_identity=system_locality_identity,
                )
                relation_result = record_operator_system_locality_result(
                    ledger,
                    responsible_act_evidence_event_identity=relation_act.identity,
                )
                system_standing = _advance_over(
                    ledger,
                    system_standing,
                    (
                        relation_result.material[
                            "evidence_of_yield_relation_identity"
                        ],
                        relation_result.identity,
                    ),
                    locality_identity=system_locality_identity,
                )
            supplied_boundaries: set[str] = set()
            supplied_occurrence_count = 0
            supplied_occurrence_references: list[str] = []
            byte_measurement_by_supplied_occurrence: dict[str, str] = {}
            pair_measurement_by_byte_measurement: dict[str, Event] = {}

            def acquire_system_material(supplied) -> None:
                nonlocal system_standing
                nonlocal supplied_occurrence_count
                if type(supplied) is not SuppliedSystemMaterialOccurrence:
                    raise TypeError("exact supplied material required")
                if supplied.source_boundary in supplied_boundaries:
                    raise ValueError("distinct source boundary required")
                supplied_boundaries.add(supplied.source_boundary)
                supplied_occurrence = ingest_supplied_invocation_occurrence(
                    ledger,
                    operator_invocation_locality_result_event_identity=(
                        relation_result.identity
                    ),
                    command_occurrence_reference=command_occurrence[
                        "evidence_event_identity"
                    ],
                    supplied=supplied,
                    prior_supplied_occurrence_references=tuple(
                        supplied_occurrence_references
                    ),
                )
                supplied_occurrence_references.append(supplied_occurrence.identity)
                supplied_occurrence_count += 1
                system_standing = _advance_over(
                    ledger,
                    system_standing,
                    (supplied_occurrence.identity,),
                    locality_identity=system_locality_identity,
                )
                system_standing, byte_measurement = _record_acquisition_measurements(
                    ledger,
                    system_standing,
                    locality_identity=system_locality_identity,
                )
                byte_measurement_by_supplied_occurrence[
                    supplied_occurrence.identity
                ] = byte_measurement.identity
                prior_position = len(supplied_occurrence_references) - 2
                if prior_position in supplied.provenance_occurrence_positions:
                    prior_reference = supplied_occurrence_references[prior_position]
                    earlier_byte_measurement = byte_measurement_by_supplied_occurrence[
                        prior_reference
                    ]
                    earlier_pair_measurement = (
                        pair_measurement_by_byte_measurement.get(
                            earlier_byte_measurement
                        )
                    )
                    if earlier_pair_measurement is None:
                        system_standing, earlier_pair = _record_pair_measurement(
                            ledger,
                            system_standing,
                            byte_measurement_event_identity=earlier_byte_measurement,
                            locality_identity=system_locality_identity,
                        )
                        earlier_pair_measurement = earlier_pair
                        pair_measurement_by_byte_measurement[
                            earlier_byte_measurement
                        ] = earlier_pair_measurement
                    system_standing, later_pair = _record_pair_measurement(
                        ledger,
                        system_standing,
                        byte_measurement_event_identity=byte_measurement.identity,
                        locality_identity=system_locality_identity,
                    )
                    pair_measurement_by_byte_measurement[
                        byte_measurement.identity
                    ] = later_pair
                    system_standing, comparison = (
                        _record_pair_measurement_comparison(
                            ledger,
                            system_standing,
                            earlier_pair_measurement=earlier_pair_measurement,
                            later_pair_measurement=later_pair,
                            locality_identity=system_locality_identity,
                        )
                    )
                    comparison_representation = record_operator_representation(
                        ledger,
                        locality_identity=system_locality_identity,
                        locality_standing=system_standing,
                        source_occurrence_reference=comparison.identity,
                    )
                    system_standing = _advance_over_representation(
                        ledger, system_standing, comparison_representation
                    )
                    destination_operator_boundary = operator_emission_boundary(
                        raw_output_stream,
                        boundary_identity=operator_egress_boundary_identity,
                        locality_identity=operator_locality_identity,
                        boundary_rule=EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
                    )
                    system_standing, _candidate = _record_representation_candidate(
                        ledger,
                        system_standing,
                        comparison_representation,
                        destination_operator_boundary=(
                            destination_operator_boundary
                        ),
                    )
                if not supplied.egress:
                    return
                system_representation = record_operator_representation(
                    ledger,
                    locality_identity=system_locality_identity,
                    locality_standing=system_standing,
                    source_occurrence_reference=supplied_occurrence.identity,
                )
                base_reference_count = len(
                    system_representation["recorded_occurrence_references"]
                )
                system_standing = _advance_over_representation(
                    ledger, system_standing, system_representation
                )
                destination_operator_boundary = operator_emission_boundary(
                    raw_output_stream,
                    boundary_identity=operator_egress_boundary_identity,
                    locality_identity=operator_locality_identity,
                    boundary_rule=EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
                )
                system_standing, admission, applicability = (
                    _record_exact_material_representation_admission_and_applicability(
                        ledger,
                        system_standing,
                        system_representation,
                        destination_operator_boundary=(
                            destination_operator_boundary
                        ),
                    )
                )
                base_reference_count += len(
                    exact_material_representation_admission_occurrence_references(
                        ledger, admission.identity
                    )
                )
                base_reference_count += len(
                    representation_emission_applicability_occurrence_references(
                        ledger, applicability.identity
                    )
                )
                try:
                    emit_operator_representation_material(
                        ledger,
                        representation=system_representation,
                        admission_result_event_identity=admission.identity,
                        applicability_result_event_identity=(
                            applicability.identity
                        ),
                        locality_standing=system_standing,
                        output_boundary=destination_operator_boundary,
                    )
                finally:
                    emission_references = system_representation[
                        "recorded_occurrence_references"
                    ][base_reference_count:]
                    if emission_references:
                        system_standing = _advance_over_representation(
                            ledger,
                            system_standing,
                            {
                                "locality_identity": system_locality_identity,
                                "recorded_occurrence_references": (
                                    emission_references
                                ),
                            },
                        )

            provider_result = operator_invocation_provider(
                command_material,
                acquire_system_material,
            )
            if provider_result is not None or not supplied_occurrence_count:
                raise TypeError("exact supplied material required")
            with ledger.batched():
                system_representation = record_operator_representation(
                    ledger,
                    locality_identity=system_locality_identity,
                    locality_standing=system_standing,
                )
                system_standing = _advance_over_representation(
                    ledger, system_standing, system_representation
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
            attempt_record = run_operator_ingest(
                ledger=ledger,
                locality_identity=locality_identity,
                boundary_material=boundary_material,
                locality_standing=(
                    locality_standing if locality_standing["event_count"] else None
                ),
                operator_material_occurrence_reference=(
                    acquired_material.identity
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
            locality_standing, byte_measurement = _record_acquisition_measurements(
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
