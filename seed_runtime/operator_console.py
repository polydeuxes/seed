"""Operator material, slash commands, and exact current-coordinate work."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, BinaryIO, Mapping, TextIO

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    _record_byte_position_pair_count_layer_from_current_coordinates,
    result_positions_of_recorded_byte_measurement,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    _record_recorded_pair_measurement_comparison_from_carried_measurements,
)
from seed_runtime.comparison_of_shared_position_measurement_with_recorded_pair_findings import (
    record_applicable_shared_position_measurement_pair_finding_compare_act_occurrence_from_current_coordinates,
    record_shared_position_measurement_pair_finding_compare_applicability_from_current_coordinates,
    record_shared_position_measurement_pair_finding_compare_bindings_from_current_coordinates,
    record_shared_position_measurement_pair_finding_compare_results_from_current_coordinates,
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
    record_through_occurrence_boundary_reference_act_occurrence,
    record_through_occurrence_boundary_reference_result,
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
from seed_runtime.operator_destination_locality import (
    record_operator_destination_locality_subject_to_act_binding,
    record_operator_destination_locality_act_occurrence,
    record_operator_destination_locality_result,
)
from seed_runtime.recorded_boundary_locality import (
    record_recorded_boundary_locality_subject_to_act_binding,
    record_recorded_boundary_locality_act_occurrence,
    record_recorded_boundary_locality_result,
)
from seed_runtime.operator_current_coordinates import (
    _carry_occurrence_position_measurement_binding_into_current_coordinates,
    _carry_occurrence_position_measurement_result_into_current_coordinates,
    _advance_current_coordinates_with_operator_material_source_occurrence,
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.occurrence_position_measurement import (
    _record_occurrence_position_measurement_subject_to_act_binding_from_current_coordinates,
    _record_occurrence_position_measurement_act_occurrence_from_current_coordinates,
    _record_occurrence_position_measurement_result_from_carried_act_occurrence,
    measure_occurrence_position,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
)
from seed_runtime.source_position_determination_and_comparison import (
    yield_source_position_determinations_and_comparisons,
)
from seed_runtime.declared_measurements import (
    _record_declared_measurements_from_carried_current_coordinates,
)
from seed_runtime.supplied_invocation_material import (
    OperatorInvocationProvider,
    SuppliedWitnessMaterialOccurrence,
    record_supplied_witness_material_source,
)


def _advance_over(ledger, current_coordinates, event_identities, *, locality_identity):
    """Advance current coordinates through exact recorded occurrences.

    The identities come from the act that recorded them, so nothing here
    searches the ledger for what happened; the events are retrieved by exact
    identity.
    """

    return advance_operator_current_coordinates(
        ledger,
        event_identities,
        locality_identity=locality_identity,
        prior=current_coordinates,
    )


def _record_occurrence_position_measurement(
    ledger, current_coordinates, *, locality_identity
):
    """Record exact occurrence positions in this Locality."""

    position_finding = measure_occurrence_position(
        ledger,
        source_locality_identity=locality_identity,
    )
    position_measurement_binding = (
        _record_occurrence_position_measurement_subject_to_act_binding_from_current_coordinates(
            ledger,
            recording_locality_identity=locality_identity,
            finding=position_finding,
            current_coordinates=current_coordinates,
        )
    )
    current_coordinates = _carry_occurrence_position_measurement_binding_into_current_coordinates(
        ledger,
        current_coordinates,
        position_measurement_binding,
        position_finding,
        prior_through_event_occurrence_identity=current_coordinates[
            "through_event_occurrence_identity"
        ],
    )
    position_measurement_act_occurrence = (
        _record_occurrence_position_measurement_act_occurrence_from_current_coordinates(
            ledger,
            binding=position_measurement_binding,
            finding=position_finding,
            current_coordinates=current_coordinates,
        )
    )
    current_coordinates = _advance_over(
        ledger,
        current_coordinates,
        (position_measurement_act_occurrence.identity,),
        locality_identity=locality_identity,
    )
    position_measurement = (
        _record_occurrence_position_measurement_result_from_carried_act_occurrence(
            ledger,
            act_occurrence=position_measurement_act_occurrence,
            binding=position_measurement_binding,
            finding=position_finding,
        )
    )
    current_coordinates = _carry_occurrence_position_measurement_result_into_current_coordinates(
        ledger,
        current_coordinates,
        position_measurement,
        act_occurrence=position_measurement_act_occurrence,
        binding=position_measurement_binding,
        finding=position_finding,
    )
    return current_coordinates


def _record_occurrence_position_after_declared_measurements(
    ledger, recorded, *, locality_identity
):
    byte_measurements = tuple(
        event
        for event in recorded.result_occurrences
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    )
    if len(byte_measurements) > 1:
        raise ValueError(
            "one exact-byte Measurement is required through this occurrence boundary"
        )
    current_coordinates = recorded.current_coordinates
    if not byte_measurements:
        return current_coordinates, None
    direct_measurements = tuple(
        event
        for event in recorded.result_occurrences
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    )
    for direct_measurement in direct_measurements:
        for result in yield_source_position_determinations_and_comparisons(
            ledger,
            direct_result_event_identity=direct_measurement.identity,
            current_coordinates=current_coordinates,
        ):
            current_coordinates = result.current_coordinates
    current_coordinates = _record_occurrence_position_measurement(
        ledger,
        current_coordinates,
        locality_identity=locality_identity,
    )
    return current_coordinates, byte_measurements[0]


def _record_measurements_from_current_coordinates(
    ledger,
    current_coordinates,
    *,
    locality_identity,
):
    """Record declared Measurements, then occurrence-position Measurement."""

    recorded = _record_declared_measurements_from_carried_current_coordinates(
        ledger,
        current_coordinates,
        locality_identity=locality_identity,
    )
    return _record_occurrence_position_after_declared_measurements(
        ledger,
        recorded,
        locality_identity=locality_identity,
    )


def _record_pair_measurement(
    ledger,
    current_coordinates,
    *,
    byte_measurement_event_identity,
    locality_identity,
):
    """Record the pair Measurement supplied by one exact-byte Measurement."""

    pair_measurement, current_coordinates = (
        _record_byte_position_pair_count_layer_from_current_coordinates(
            ledger,
            source_measurement_event_identity=byte_measurement_event_identity,
            recording_locality_identity=locality_identity,
            current_coordinates=current_coordinates,
        )
    )
    return current_coordinates, pair_measurement


def _record_pair_measurements_after_declared_measurements(
    ledger,
    recorded,
    *,
    locality_identity,
):
    """Record each pair Measurement whose exact-byte result was just recorded."""

    current_coordinates = recorded.current_coordinates
    pair_measurements = []
    for byte_measurement in recorded.result_occurrences:
        if byte_measurement.kind != BYTE_MEASUREMENT_RECORDED_KIND:
            continue
        current_coordinates, pair_measurement = _record_pair_measurement(
            ledger,
            current_coordinates,
            byte_measurement_event_identity=byte_measurement.identity,
            locality_identity=locality_identity,
        )
        pair_measurements.append(pair_measurement)
    return current_coordinates, tuple(pair_measurements)


def _latest_carried_pair_premise(
    ledger,
    current_coordinates,
    *,
    locality_identity,
):
    """Address the latest exact pair Measurement already carried here."""

    from seed_runtime.material_source import (
        MaterialSourceError,
        read_exact_material_result,
    )

    for event_identity in reversed(
        tuple(current_coordinates["measurement_occurrences"])
    ):
        event = ledger.get(event_identity)
        if (
            event is None
            or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
            or event.locality_identity != locality_identity
        ):
            continue
        source_reference = event.material.get("source_result_position_reference")
        source_positions = (
            result_positions_of_recorded_byte_measurement(
                ledger,
                source_reference.get("recorded_occurrence_identity"),
                prior_coordinates=current_coordinates,
            )
            if type(source_reference) is dict
            else None
        )
        source_position = (
            next(
                (
                    position
                    for position in source_positions
                    if position.get("dimensions", {}).get("position")
                    == source_reference.get("result_position")
                ),
                None,
            )
            if type(source_positions) is tuple
            else None
        )
        source_content = (
            source_position.get("dimensions", {}).get("content")
            if type(source_position) is dict
            else None
        )
        source_occurrence_references = (
            source_content.get("source_material")
            if type(source_content) is dict
            else None
        )
        if (
            type(source_occurrence_references) is not list
            or not source_occurrence_references
        ):
            continue
        if not all(
            type(source_reference) is dict
            and type(
                source_reference.get("material_result_occurrence_identity")
            )
            is str
            for source_reference in source_occurrence_references
        ):
            continue
        try:
            for source_reference in source_occurrence_references:
                read_exact_material_result(
                    ledger,
                    source_reference["material_result_occurrence_identity"],
                )
        except (MaterialSourceError, TypeError):
            continue
        return current_coordinates, event
    return current_coordinates, None


def _record_pair_measurement_comparison(
    ledger,
    current_coordinates,
    *,
    earlier_pair_measurement,
    later_pair_measurement,
    locality_identity,
):
    """Carry first and second produced pair results into their Compare."""

    if (
        type(earlier_pair_measurement) is not Event
        or type(later_pair_measurement) is not Event
        or earlier_pair_measurement.locality_identity != locality_identity
        or later_pair_measurement.locality_identity != locality_identity
    ):
        raise ValueError("pair Compare requires first and second carried Measurements")
    result, current_coordinates = (
        _record_recorded_pair_measurement_comparison_from_carried_measurements(
            ledger,
            earlier_measurement=earlier_pair_measurement,
            later_measurement=later_pair_measurement,
            current_coordinates=current_coordinates,
        )
    )
    return current_coordinates, result


def _record_shared_position_measurement_pair_finding_compare(
    ledger,
    current_coordinates,
    *,
    locality_identity,
):
    """Record each exact shared-position Compare in current coordinates."""

    bindings = record_shared_position_measurement_pair_finding_compare_bindings_from_current_coordinates(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=current_coordinates,
    )
    applicability = record_shared_position_measurement_pair_finding_compare_applicability_from_current_coordinates(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=bindings.current_coordinates,
    )
    acts = record_applicable_shared_position_measurement_pair_finding_compare_act_occurrence_from_current_coordinates(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=applicability.current_coordinates,
    )
    results = record_shared_position_measurement_pair_finding_compare_results_from_current_coordinates(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=acts.current_coordinates,
    )
    return results.current_coordinates


def run_persistent_operator_console(
    *,
    ledger: EventLedger,
    locality_identity: str,
    input_stream: BinaryIO | TextIO,
    command_handlers: Mapping[bytes, OperatorCommandHandler] | None = None,
    operator_invocation_provider: OperatorInvocationProvider | None = None,
) -> dict[str, Any]:
    """Repeat exact-byte material and slash-command occurrences."""
    handlers = dict(command_handlers or {})
    handlers[b"checkpoint"] = request_operator_checkpoint
    handlers[b"checkout"] = request_operator_checkout
    handlers[b"memory"] = request_operator_memory
    # Each produced result enters the current coordinates used by the next
    # interaction.
    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    current_coordinates, pair_premise = _latest_carried_pair_premise(
        ledger,
        current_coordinates,
        locality_identity=locality_identity,
    )
    while True:
        source_prior_boundary = current_coordinates[
            "through_event_occurrence_identity"
        ]
        source_boundary = operator_material_source_boundary(input_stream)
        source_binding = (
            _record_operator_material_source_subject_to_act_binding_from_current_coordinates(
                ledger,
                locality_identity=locality_identity,
                current_coordinates=current_coordinates,
                source_boundary=source_boundary,
            )
        )
        current_coordinates = (
            _advance_current_coordinates_with_operator_material_source_occurrence(
                ledger,
                current_coordinates,
                source_binding,
                prior_through_event_occurrence_identity=source_prior_boundary,
            )
        )
        source_act_occurrence = (
            _record_operator_material_source_act_occurrence_from_binding(
                ledger,
                subject_to_act_binding=source_binding,
                current_coordinates=current_coordinates,
            )
        )
        current_coordinates = (
            _advance_current_coordinates_with_operator_material_source_occurrence(
                ledger,
                current_coordinates,
                source_act_occurrence,
                prior_through_event_occurrence_identity=(
                    source_binding.identity
                ),
            )
        )
        input_boundary = ledger.append_boundary()
        boundary_material = operator_boundary_material(input_stream)
        if boundary_material.material_boundary != source_boundary:
            raise ValueError("operator material differs from its addressed source boundary")
        if ledger.append_boundary() != input_boundary:
            raise ValueError(
                "operator boundary invocation appended an occurrence before its result"
            )
        if boundary_material.eof:
            return deepcopy(current_coordinates)
        source_material = record_operator_material_source_result(
            ledger,
            act_occurrence_event_identity=source_act_occurrence.identity,
            boundary_material=boundary_material,
        )
        current_coordinates = (
            _advance_current_coordinates_with_operator_material_source_occurrence(
                ledger,
                current_coordinates,
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
                current_coordinates, _byte_measurement = (
                    _record_measurements_from_current_coordinates(
                        ledger,
                        current_coordinates,
                        locality_identity=locality_identity,
                    )
                )
                command_material = source_material.exact_material
                relation_binding = (
                    record_operator_destination_locality_subject_to_act_binding(
                        ledger,
                        operator_material_occurrence_reference=(
                            command_occurrence_reference
                        ),
                        current_coordinates=current_coordinates,
                    )
                )
                destination_locality_identity = relation_binding.material[
                    "destination_locality_identity"
                ]
                witness_current_coordinates = read_operator_current_coordinates(
                    ledger, locality_identity=destination_locality_identity
                )
                relation_act = record_operator_destination_locality_act_occurrence(
                    ledger,
                    subject_to_act_binding_event_identity=(
                        relation_binding.identity
                    ),
                    current_coordinates=witness_current_coordinates,
                )
                witness_current_coordinates = _advance_over(
                    ledger,
                    witness_current_coordinates,
                    (relation_act.identity,),
                    locality_identity=destination_locality_identity,
                )
                relation_result = record_operator_destination_locality_result(
                    ledger,
                    act_occurrence_event_identity=relation_act.identity,
                )
                witness_current_coordinates = _advance_over(
                    ledger,
                    witness_current_coordinates,
                    (relation_result.identity,),
                    locality_identity=destination_locality_identity,
                )
            supplied_boundaries: set[str] = set()
            supplied_occurrence_count = 0
            supplied_occurrence_references: list[str] = []
            provider_boundary = ledger.append_boundary()

            def record_witness_material(supplied) -> None:
                nonlocal witness_current_coordinates
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
                    operator_destination_locality_result_event_identity=(
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
                recorded_occurrences = ledger.locality_occurrence_interval(
                    locality_identity=destination_locality_identity,
                    after_occurrence_identity=witness_current_coordinates[
                        "through_event_occurrence_identity"
                    ],
                    through_occurrence_identity=supplied_occurrence.identity,
                )
                witness_current_coordinates = _advance_over(
                    ledger,
                    witness_current_coordinates,
                    tuple(event.identity for event in recorded_occurrences),
                    locality_identity=destination_locality_identity,
                )
                recorded_witness_measurements = (
                    _record_declared_measurements_from_carried_current_coordinates(
                        ledger,
                        witness_current_coordinates,
                        locality_identity=destination_locality_identity,
                    )
                )
                witness_current_coordinates, _witness_pair_measurements = (
                    _record_pair_measurements_after_declared_measurements(
                        ledger,
                        recorded_witness_measurements,
                        locality_identity=destination_locality_identity,
                    )
                )
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
                addressed_through_event_occurrence_identity=(
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
                            command_run.addressed.addressed_through_event_occurrence_identity
                        ),
                    )
                )
                locality_identity = binding.locality_identity
                pair_premise = None
                current_coordinates = read_operator_current_coordinates(
                    ledger, locality_identity=locality_identity
                )
                continuation_act_occurrence = (
                    record_locality_continuation_act_occurrence(
                        ledger,
                        subject_to_act_binding_event_identity=binding.identity,
                        current_coordinates=current_coordinates,
                    )
                )
                current_coordinates = _advance_over(
                    ledger,
                    current_coordinates,
                    (continuation_act_occurrence.identity,),
                    locality_identity=locality_identity,
                )
                continuation = record_locality_continuation_result(
                    ledger,
                    act_occurrence_event_identity=(
                        continuation_act_occurrence.identity
                    ),
                )
                current_coordinates = _advance_over(
                    ledger,
                    current_coordinates,
                    (continuation.identity,),
                    locality_identity=locality_identity,
                )
                continue
            if isinstance(request, OperatorCheckpointRequest):
                act_occurrence = (
                    record_through_occurrence_boundary_reference_act_occurrence(
                        ledger,
                        addressed_command=command_run.addressed,
                        current_coordinates=current_coordinates,
                    )
                )
                current_coordinates = _advance_over(
                    ledger,
                    current_coordinates,
                    (act_occurrence.identity,),
                    locality_identity=locality_identity,
                )
                checkpoint = record_through_occurrence_boundary_reference_result(
                    ledger,
                    act_occurrence_event_identity=act_occurrence.identity,
                )
                current_coordinates = _advance_over(
                    ledger,
                    current_coordinates,
                    (checkpoint.identity,),
                    locality_identity=locality_identity,
                )
                continue
            if isinstance(request, OperatorCheckoutRequest):
                binding = (
                    record_recorded_boundary_locality_subject_to_act_binding(
                        ledger,
                        source_current_coordinates=current_coordinates,
                    )
                )
                locality_identity = binding.locality_identity
                pair_premise = None
                current_coordinates = read_operator_current_coordinates(
                    ledger, locality_identity=locality_identity
                )
                act_occurrence = (
                    record_recorded_boundary_locality_act_occurrence(
                        ledger,
                        subject_to_act_binding_event_identity=binding.identity,
                        current_coordinates=current_coordinates,
                    )
                )
                current_coordinates = _advance_over(
                    ledger,
                    current_coordinates,
                    (act_occurrence.identity,),
                    locality_identity=locality_identity,
                )
                relation = record_recorded_boundary_locality_result(
                    ledger,
                    act_occurrence_event_identity=act_occurrence.identity,
                )
                current_coordinates = _advance_over(
                    ledger,
                    current_coordinates,
                    (relation.identity,),
                    locality_identity=locality_identity,
                )
                continue
            if request is not None or command_run.addressed.frame.name in handlers:
                continue
        with ledger.batched():
            current_coordinates, byte_measurement = (
                _record_measurements_from_current_coordinates(
                    ledger,
                    current_coordinates,
                    locality_identity=locality_identity,
                )
            )
            if byte_measurement is None:
                continue
            current_coordinates, later_pair = _record_pair_measurement(
                ledger,
                current_coordinates,
                byte_measurement_event_identity=byte_measurement.identity,
                locality_identity=locality_identity,
            )
            if pair_premise is not None:
                current_coordinates, comparison = (
                    _record_pair_measurement_comparison(
                        ledger,
                        current_coordinates,
                        earlier_pair_measurement=pair_premise,
                        later_pair_measurement=later_pair,
                        locality_identity=locality_identity,
                    )
                )
                current_coordinates = _record_shared_position_measurement_pair_finding_compare(
                    ledger,
                    current_coordinates,
                    locality_identity=locality_identity,
                )
                current_coordinates = (
                    _record_declared_measurements_from_carried_current_coordinates(
                        ledger,
                        current_coordinates,
                        locality_identity=locality_identity,
                    ).current_coordinates
                )
            pair_premise = later_pair
