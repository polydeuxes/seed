"""Operator material acquisition, slash commands, and exact Standing work."""

from __future__ import annotations

from typing import BinaryIO, Mapping, TextIO

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    _record_byte_position_pair_count_layer_from_carried_locality_standing,
    assertions_of_recorded_byte_measurement,
    get_byte_position_pair_measurement_subject_to_act_binding,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    _record_recorded_pair_measurement_comparison_from_carried_measurements,
)
from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.operator_material_boundary import (
    operator_boundary_material,
    operator_material_source_boundary,
)
from seed_runtime.operator_material_source import (
    _record_operator_material_source_subject_to_act_binding_from_current_coordinates,
    _record_operator_material_source_act_occurrence_from_binding,
    record_operator_material_source_result,
)
from seed_runtime.operator_command import (
    OperatorCommandHandler,
    is_slash_command,
    run_operator_command,
)
from seed_runtime.operator_checkpoint import (
    OperatorCheckpointRequest,
    record_standing_boundary_reference_subject_to_act_binding,
    record_standing_boundary_reference_act_occurrence,
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
from seed_runtime.operator_locality_continuation import (
    record_locality_continuation_subject_to_act_binding,
    record_locality_continuation_act_occurrence,
    record_locality_continuation_result,
)
from seed_runtime.operator_invocation_locality import (
    record_operator_invocation_locality_subject_to_act_binding,
    record_operator_invocation_locality_act_occurrence,
    record_operator_invocation_locality_result,
)
from seed_runtime.standing_boundary_locality import (
    record_recorded_standing_boundary_locality_subject_to_act_binding,
    record_recorded_standing_boundary_locality_act_occurrence,
    record_recorded_standing_boundary_locality_result,
)
from seed_runtime.operator_locality_standing import (
    _carry_occurrence_position_measurement_assignment_into_standing,
    _carry_occurrence_position_measurement_result_into_standing,
    _carry_operator_material_source_occurrence_into_standing,
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.occurrence_position_measurement import (
    _record_occurrence_position_measurement_responsibility_assignment_from_carried_standing,
    _record_occurrence_position_measurement_act_occurrence_from_carried_standing,
    _record_occurrence_position_measurement_result_from_carried_act_occurrence,
    measure_occurrence_position,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
)
from seed_runtime.ordered_path_source_position_continuation import (
    yield_ordered_path_source_position_continuations,
)
from seed_runtime.declared_measurement_responsibilities import (
    _record_declared_measurements_from_carried_bounded_locality_replay,
)
from seed_runtime.supplied_invocation_material import (
    OperatorInvocationProvider,
    SuppliedWitnessMaterialOccurrence,
    record_supplied_witness_material_source,
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
    position_measurement_act_occurrence = (
        _record_occurrence_position_measurement_act_occurrence_from_carried_standing(
            ledger,
            responsibility_assignment=position_measurement_assignment,
            finding=position_finding,
            responsibility_assignment_standing=standing,
        )
    )
    standing = _advance_over(
        ledger,
        standing,
        (position_measurement_act_occurrence.identity,),
        locality_identity=locality_identity,
    )
    position_measurement = (
        _record_occurrence_position_measurement_result_from_carried_act_occurrence(
            ledger,
            act_occurrence=position_measurement_act_occurrence,
            responsibility_assignment=position_measurement_assignment,
            finding=position_finding,
        )
    )
    standing = _carry_occurrence_position_measurement_result_into_standing(
        ledger,
        standing,
        position_measurement,
        act_occurrence=position_measurement_act_occurrence,
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
        raise ValueError(
            "one exact-byte Measurement is required after this responsible boundary"
        )
    standing = recorded.bounded_locality_replay
    direct_measurements = tuple(
        event
        for event in recorded.result_occurrences
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    )
    for direct_measurement in direct_measurements:
        for continuation in yield_ordered_path_source_position_continuations(
            ledger,
            direct_result_event_identity=direct_measurement.identity,
            locality_standing=standing,
        ):
            standing = continuation.locality_standing
    standing = _record_occurrence_position_measurement(
        ledger,
        standing,
        locality_identity=locality_identity,
    )
    return standing, byte_measurements[0]


def _record_measurements_from_bounded_locality_replay(
    ledger,
    bounded_locality_replay,
    *,
    locality_identity,
):
    """Record declared Measurements, then the explicit Locality road."""

    recorded = _record_declared_measurements_from_carried_bounded_locality_replay(
        ledger,
        bounded_locality_replay,
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
    """Record the pair Measurement supplied by one exact-byte Measurement."""

    pair_measurement, standing = (
        _record_byte_position_pair_count_layer_from_carried_locality_standing(
            ledger,
            source_measurement_event_identity=byte_measurement_event_identity,
            recording_locality_identity=locality_identity,
            locality_standing=standing,
        )
    )
    return standing, pair_measurement


def _record_pair_measurements_after_declared_measurements(
    ledger,
    recorded,
    *,
    locality_identity,
):
    """Record each pair Measurement whose exact-byte result was just recorded."""

    standing = recorded.bounded_locality_replay
    pair_measurements = []
    for byte_measurement in recorded.result_occurrences:
        if byte_measurement.kind != BYTE_MEASUREMENT_RECORDED_KIND:
            continue
        standing, pair_measurement = _record_pair_measurement(
            ledger,
            standing,
            byte_measurement_event_identity=byte_measurement.identity,
            locality_identity=locality_identity,
        )
        pair_measurements.append(pair_measurement)
    return standing, tuple(pair_measurements)


def _recorded_byte_measurement_material_references(ledger):
    """Read exact-material storage references already measured by this Seed."""

    references = set()
    for event in ledger.list():
        if event.kind != BYTE_MEASUREMENT_RECORDED_KIND:
            continue
        assertions = assertions_of_recorded_byte_measurement(ledger, event.identity)
        source = next(
            (
                assertion
                for assertion in assertions or ()
                if assertion.result == "exact_source_material_set"
            ),
            None,
        )
        if source is None:
            raise ValueError("recorded byte Measurement carries no exact source")
        source_material = source.material["dimensions"]["content"].get(
            "source_material"
        )
        if type(source_material) is not list:
            raise ValueError("recorded byte Measurement source is malformed")
        for occurrence_reference in source_material:
            occurrence_identity = (
                occurrence_reference.get("material_acquisition_occurrence_identity")
                if type(occurrence_reference) is dict
                else None
            )
            reference = (
                ledger._exact_material_reference(occurrence_identity)
                if type(occurrence_identity) is str
                else None
            )
            if reference is None:
                raise ValueError("recorded byte Measurement source has no exact material")
            references.add(reference)
    return references


def _material_measurement_reference(ledger, acquisition_result):
    reference = ledger._exact_material_reference(acquisition_result.identity)
    if reference is None:
        raise ValueError("material acquisition result has no exact material")
    return reference


def _latest_carried_pair_premise(
    ledger,
    standing,
    *,
    locality_identity,
):
    """Address the latest exact pair Measurement already carried here."""

    from seed_runtime.material_source import (
        read_material_locality_relation_requirements,
    )

    for event_identity in reversed(tuple(standing["measurement_occurrences"])):
        event = ledger.get(event_identity)
        if (
            event is None
            or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
            or event.locality_identity != locality_identity
        ):
            continue
        reference = (
            event.material.get("subject_to_act_binding_reference")
            if type(event.material) is dict
            else None
        )
        try:
            assignment = get_byte_position_pair_measurement_subject_to_act_binding(
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
            type(source_occurrence_references) is list
            and source_occurrence_references
            and all(
                type(source_reference) is dict
                and type(
                    source_reference.get(
                        "material_acquisition_occurrence_identity"
                    )
                )
                is str
                for source_reference in source_occurrence_references
            )
            and all(
                all(
                    read_material_locality_relation_requirements(
                        ledger,
                        recorded_result_event_identity=source_reference[
                            "material_acquisition_occurrence_identity"
                        ],
                    ).values()
                )
                for source_reference in source_occurrence_references
            )
        ):
            return standing, event
    return standing, None


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
    command_handlers: Mapping[bytes, OperatorCommandHandler] | None = None,
    operator_invocation_provider: OperatorInvocationProvider | None = None,
) -> None:
    """Repeat exact-byte material acquisition and slash-command occurrences."""
    handlers = dict(command_handlers or {})
    handlers[b"checkpoint"] = request_operator_checkpoint
    handlers[b"checkout"] = request_operator_checkout
    handlers[b"memory"] = request_operator_memory
    # Each produced result enters the current Locality Standing.  This
    # Standing is the input of the next interaction.
    locality_standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    measured_material_references = _recorded_byte_measurement_material_references(
        ledger
    )
    locality_standing, pair_premise = _latest_carried_pair_premise(
        ledger,
        locality_standing,
        locality_identity=locality_identity,
    )
    while True:
        source_prior_boundary = locality_standing[
            "through_event_occurrence_identity"
        ]
        source_boundary = operator_material_source_boundary(input_stream)
        source_binding = (
            _record_operator_material_source_subject_to_act_binding_from_current_coordinates(
                ledger,
                locality_identity=locality_identity,
                current_coordinates=locality_standing,
                source_boundary=source_boundary,
            )
        )
        locality_standing = (
            _carry_operator_material_source_occurrence_into_standing(
                ledger,
                locality_standing,
                source_binding,
                prior_through_event_occurrence_identity=source_prior_boundary,
            )
        )
        source_act_occurrence = (
            _record_operator_material_source_act_occurrence_from_binding(
                ledger,
                subject_to_act_binding=source_binding,
                current_coordinates=locality_standing,
            )
        )
        locality_standing = (
            _carry_operator_material_source_occurrence_into_standing(
                ledger,
                locality_standing,
                source_act_occurrence,
                prior_through_event_occurrence_identity=(
                    source_binding.identity
                ),
            )
        )
        input_boundary = ledger.append_boundary()
        boundary_material = operator_boundary_material(input_stream)
        if boundary_material.material_boundary != source_boundary:
            raise ValueError("operator material crossed its addressed source boundary")
        if ledger.append_boundary() != input_boundary:
            raise ValueError(
                "operator boundary invocation appended an occurrence before its result"
            )
        if boundary_material.eof:
            return
        source_material = record_operator_material_source_result(
            ledger,
            act_occurrence_event_identity=source_act_occurrence.identity,
            boundary_material=boundary_material,
        )
        locality_standing = (
            _carry_operator_material_source_occurrence_into_standing(
                ledger,
                locality_standing,
                source_material,
                prior_through_event_occurrence_identity=(
                    source_act_occurrence.identity
                ),
            )
        )
        if (
            operator_invocation_provider is not None
            and boundary_material.exact_bytes.startswith(b"!")
        ):
            with ledger.batched():
                command_occurrence_reference = source_material.identity
                command_material_reference = _material_measurement_reference(
                    ledger, source_material
                )
                if command_material_reference not in measured_material_references:
                    locality_standing, _byte_measurement = (
                        _record_measurements_from_bounded_locality_replay(
                            ledger,
                            locality_standing,
                            locality_identity=locality_identity,
                        )
                    )
                    measured_material_references.add(command_material_reference)
                command_material = source_material.exact_material
                relation_binding = (
                    record_operator_invocation_locality_subject_to_act_binding(
                        ledger,
                        operator_material_occurrence_reference=(
                            command_occurrence_reference
                        ),
                        current_coordinates=locality_standing,
                    )
                )
                invocation_locality_identity = relation_binding.material[
                    "destination_locality_identity"
                ]
                witness_standing = read_operator_locality_standing(
                    ledger, locality_identity=invocation_locality_identity
                )
                relation_act = record_operator_invocation_locality_act_occurrence(
                    ledger,
                    subject_to_act_binding_event_identity=(
                        relation_binding.identity
                    ),
                    current_coordinates=witness_standing,
                )
                witness_standing = _advance_over(
                    ledger,
                    witness_standing,
                    (relation_act.identity,),
                    locality_identity=invocation_locality_identity,
                )
                relation_result = record_operator_invocation_locality_result(
                    ledger,
                    act_occurrence_event_identity=relation_act.identity,
                )
                witness_standing = _advance_over(
                    ledger,
                    witness_standing,
                    (
                        relation_result.material[
                            "yield_relation_identity"
                        ],
                        relation_result.identity,
                    ),
                    locality_identity=invocation_locality_identity,
                )
            supplied_boundaries: set[str] = set()
            supplied_occurrence_count = 0
            supplied_occurrence_references: list[str] = []
            provider_boundary = ledger.append_boundary()

            def record_witness_material(supplied) -> None:
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
                supplied_occurrence = record_supplied_witness_material_source(
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
                supplied_material_reference = _material_measurement_reference(
                    ledger, supplied_occurrence
                )
                if supplied_material_reference not in measured_material_references:
                    recorded_witness_measurements = (
                        _record_declared_measurements_from_carried_bounded_locality_replay(
                            ledger,
                            witness_standing,
                            locality_identity=invocation_locality_identity,
                        )
                    )
                    witness_standing, _witness_pair_measurements = (
                        _record_pair_measurements_after_declared_measurements(
                            ledger,
                            recorded_witness_measurements,
                            locality_identity=invocation_locality_identity,
                        )
                    )
                    measured_material_references.add(supplied_material_reference)
                provider_boundary = ledger.append_boundary()

            provider_result = operator_invocation_provider(
                command_material,
                record_witness_material,
            )
            if ledger.append_boundary() != provider_boundary:
                raise ValueError(
                    "provider appended an occurrence outside supplied material"
                )
            if provider_result is not None or not supplied_occurrence_count:
                raise TypeError("exact supplied material required")
            continue
        if is_slash_command(boundary_material):
            command_run = run_operator_command(
                locality_identity=locality_identity,
                addressed_at_standing_boundary_event_identity=(
                    source_material.identity
                ),
                material=boundary_material,
                handlers=handlers,
            )
            request = command_run.handler_result
            if isinstance(request, OperatorMemoryRequest):
                binding = (
                    record_locality_continuation_subject_to_act_binding(
                        ledger,
                        source_locality_identity=locality_identity,
                        source_through_event_occurrence_identity=(
                            command_run.addressed.addressed_at_standing_boundary_event_identity
                        ),
                    )
                )
                locality_identity = binding.locality_identity
                pair_premise = None
                locality_standing = read_operator_locality_standing(
                    ledger, locality_identity=locality_identity
                )
                continuation_act_occurrence = (
                    record_locality_continuation_act_occurrence(
                        ledger,
                        subject_to_act_binding_event_identity=binding.identity,
                        current_coordinates=locality_standing,
                    )
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (continuation_act_occurrence.identity,),
                    locality_identity=locality_identity,
                )
                continuation = record_locality_continuation_result(
                    ledger,
                    act_occurrence_event_identity=(
                        continuation_act_occurrence.identity
                    ),
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (
                        continuation.material["yield_relation_identity"],
                        continuation.identity,
                    ),
                    locality_identity=locality_identity,
                )
                continue
            if isinstance(request, OperatorCheckpointRequest):
                binding = (
                    record_standing_boundary_reference_subject_to_act_binding(
                        ledger,
                        addressed_command=command_run.addressed,
                        locality_standing=locality_standing,
                    )
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (binding.identity,),
                    locality_identity=locality_identity,
                )
                act_occurrence = (
                    record_standing_boundary_reference_act_occurrence(
                        ledger,
                        subject_to_act_binding_event_identity=binding.identity,
                        current_coordinates=locality_standing,
                    )
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (act_occurrence.identity,),
                    locality_identity=locality_identity,
                )
                checkpoint = record_standing_boundary_reference_result(
                    ledger,
                    act_occurrence_event_identity=act_occurrence.identity,
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (
                        checkpoint.material["yield_relation_identity"],
                        checkpoint.identity,
                    ),
                    locality_identity=locality_identity,
                )
                continue
            if isinstance(request, OperatorCheckoutRequest):
                binding = (
                    record_recorded_standing_boundary_locality_subject_to_act_binding(
                        ledger,
                        source_locality_standing=locality_standing,
                    )
                )
                locality_identity = binding.locality_identity
                pair_premise = None
                locality_standing = read_operator_locality_standing(
                    ledger, locality_identity=locality_identity
                )
                act_occurrence = (
                    record_recorded_standing_boundary_locality_act_occurrence(
                        ledger,
                        subject_to_act_binding_event_identity=binding.identity,
                        current_coordinates=locality_standing,
                    )
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (act_occurrence.identity,),
                    locality_identity=locality_identity,
                )
                relation = record_recorded_standing_boundary_locality_result(
                    ledger,
                    act_occurrence_event_identity=act_occurrence.identity,
                )
                locality_standing = _advance_over(
                    ledger,
                    locality_standing,
                    (
                        relation.material["yield_relation_identity"],
                        relation.identity,
                    ),
                    locality_identity=locality_identity,
                )
                continue
            if request is not None or command_run.addressed.frame.name in handlers:
                continue
        with ledger.batched():
            source_material_reference = _material_measurement_reference(
                ledger, source_material
            )
            if source_material_reference not in measured_material_references:
                locality_standing, byte_measurement = (
                    _record_measurements_from_bounded_locality_replay(
                        ledger,
                        locality_standing,
                        locality_identity=locality_identity,
                    )
                )
                measured_material_references.add(source_material_reference)
                locality_standing, later_pair = _record_pair_measurement(
                    ledger,
                    locality_standing,
                    byte_measurement_event_identity=byte_measurement.identity,
                    locality_identity=locality_identity,
                )
                if pair_premise is not None:
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
