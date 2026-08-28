"""Determine each source position, then record available path Comparisons."""

from __future__ import annotations

from typing import Any, Iterator, NamedTuple

from seed_runtime.addressed_byte_occurrence_reference_determination import (
    _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_current_coordinates,
)
from seed_runtime.comparison_of_ordered_path_source_position_material import (
    yield_ordered_path_source_position_material_comparisons,
)
from seed_runtime.event import Event
from seed_runtime.events import EventLedger
import seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences as shared_position
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    source_position_coordinate_references_of_recorded_position_measurement,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result,
)
class SourcePositionDeterminationPathAndComparison(NamedTuple):
    source_position_coordinate: dict[str, Any]
    determination_result: Event
    ordered_path_result: Event | None
    comparison_result: Event | None
    current_coordinates: dict[str, Any]


def _advance(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    *events: Event,
) -> dict[str, Any]:
    locality_identity = current_coordinates["locality_identity"]
    prior = current_coordinates["through_event_occurrence_identity"]
    ordered = ledger.occurrences_in_append_order(
        (prior, *(event.identity for event in events)),
        locality_identity=locality_identity,
    )
    if (
        tuple(event.identity for event in ordered)
        != (prior, *(event.identity for event in events))
        or ledger.append_boundary_through_occurrence(events[-1].identity)
        != ledger.append_boundary()
    ):
        raise ValueError(
            "source-position determination and comparison left its exact boundary"
        )
    for event in events:
        if event.kind in {
            SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        }:
            current_coordinates["subject_to_act_binding_occurrences"][
                event.identity
            ] = None
        elif event.kind == SHARED_POSITION_APPLICABILITY_RESULT_KIND:
            current_coordinates["applicability_result_occurrences"][
                event.identity
            ] = None
        elif event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND:
            current_coordinates["measurement_occurrences"][event.identity] = {
                "recorded_occurrence_identity": event.identity,
                "result_identity": event.material["result_identity"],
                "act_occurrence_identity": event.material["act_occurrence_identity"],
                "act_occurrence_event_identity": event.material[
                    "act_occurrence_event_identity"
                ],
            }
        current_coordinates["through_event_occurrence_identity"] = event.identity
        current_coordinates["event_count"] += 1
    return current_coordinates


def _record_shared_path(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    determination: Event,
) -> tuple[dict[str, Any], Event]:
    """Record the existing shared-position lifecycle from carried coordinates."""

    measurement_binding = record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_result_event_identity=determination.identity,
        current_coordinates=current_coordinates,
    )
    _result, inputs = shared_position._d2_result_inputs(
        ledger,
        result_event_identity=determination.identity,
        prior_coordinates=current_coordinates,
    )
    current_coordinates = _advance(
        ledger, current_coordinates, measurement_binding
    )
    applicability_identities = shared_position._mint_applicability_identities(ledger)
    applicability_binding = ledger.append(
        shared_position.SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        shared_position._applicability_binding_material(
            inputs=inputs,
            through_event_occurrence_identity=current_coordinates[
                "through_event_occurrence_identity"
            ],
            measurement_act_identity=measurement_binding.material[
                "exact_act_identity"
            ],
            identities=applicability_identities,
            determination_result_reference=measurement_binding.material.get(
                shared_position.D2_RESULT_REFERENCE_COORDINATE
            ),
        ),
        locality_identity=measurement_binding.locality_identity,
    )
    current_coordinates = _advance(
        ledger, current_coordinates, applicability_binding
    )
    applicability_act = ledger.append(
        shared_position.SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT,
        shared_position._applicability_act_material(
            binding=applicability_binding,
            inputs=inputs,
            through_event_occurrence_identity=current_coordinates[
                "through_event_occurrence_identity"
            ],
        ),
        locality_identity=measurement_binding.locality_identity,
    )
    current_coordinates = _advance(ledger, current_coordinates, applicability_act)
    applicability_material = shared_position._applicability_result_material(
        ledger=ledger,
        act=applicability_act,
        binding=applicability_binding,
        inputs=inputs,
    )
    applicability = ledger.append(
        shared_position.SHARED_POSITION_APPLICABILITY_RESULT_KIND,
        shared_position._recorded_applicability_result_material(
            applicability_material,
        ),
        locality_identity=measurement_binding.locality_identity,
    )
    current_coordinates = _advance(
        ledger, current_coordinates, applicability
    )
    measurement_act = ledger.append(
        shared_position.SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT,
        shared_position._measurement_act_material(
            binding=measurement_binding,
            inputs=inputs,
            applicability=applicability,
            through_event_occurrence_identity=current_coordinates[
                "through_event_occurrence_identity"
            ],
        ),
        locality_identity=measurement_binding.locality_identity,
    )
    current_coordinates = _advance(ledger, current_coordinates, measurement_act)
    result_material = shared_position._measurement_result_material(
        act=measurement_act,
        binding=measurement_binding,
        applicability=applicability,
        inputs=inputs,
    )
    path = ledger.append(
        shared_position.SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        shared_position._recorded_measurement_result_material(result_material),
        locality_identity=measurement_binding.locality_identity,
    )
    return _advance(ledger, current_coordinates, path), path


def _yield_source_position_determinations_paths_and_comparisons(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Iterator[SourcePositionDeterminationPathAndComparison]:
    """Yield each source-position result before results for later positions."""

    if not isinstance(ledger, EventLedger):
        raise TypeError(
            "source-position determination and comparison requires one EventLedger"
        )
    for coordinate in source_position_coordinate_references_of_recorded_position_measurement(
        ledger,
        direct_result_event_identity,
        prior_coordinates=current_coordinates,
    ):
        with ledger.batched():
            current_coordinates, determination = (
                _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_current_coordinates(
                    ledger,
                    direct_result_event_identity=direct_result_event_identity,
                    addressed_source_byte_position_coordinate_reference=coordinate,
                    current_coordinates=current_coordinates,
                    mutate_current_coordinates=True,
                )
            )
            if len(determination.material["ordered_assertion_references"]) != 2:
                path = None
            else:
                current_coordinates, path = _record_shared_path(
                    ledger, current_coordinates, determination
                )
        if path is None:
            yield SourcePositionDeterminationPathAndComparison(
                coordinate,
                determination,
                None,
                None,
                current_coordinates,
            )
            continue
        comparisons = yield_ordered_path_source_position_material_comparisons(
            ledger,
            path_result_event_identity=path.identity,
            current_coordinates=current_coordinates,
        )
        while True:
            with ledger.batched():
                try:
                    comparison = next(comparisons)
                except StopIteration:
                    break
            current_coordinates = comparison.current_coordinates
            yield SourcePositionDeterminationPathAndComparison(
                coordinate,
                determination,
                path,
                comparison.result_occurrence,
                current_coordinates,
            )


def yield_source_position_determinations_paths_and_comparisons(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Iterator[SourcePositionDeterminationPathAndComparison]:
    """Yield determinations and available path Comparisons for every position."""

    yield from _yield_source_position_determinations_paths_and_comparisons(
        ledger,
        direct_result_event_identity=direct_result_event_identity,
        current_coordinates=current_coordinates,
    )
