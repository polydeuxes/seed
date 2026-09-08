"""Determine each source position, then record available Comparisons."""

from __future__ import annotations

from typing import Any, Iterator, NamedTuple

from seed_runtime.addressed_byte_occurrence_reference_determination import (
    _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_current_coordinates,
)
from seed_runtime.comparison_of_shared_position_source_position_material import (
    yield_shared_position_source_position_material_comparisons,
)
from seed_runtime.event import Event
from seed_runtime.events import EventLedger
import seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences as shared_position
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    source_position_coordinate_references_of_recorded_position_measurement,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    record_shared_position_measurement_act_occurrence_from_addressed_byte_occurrence_reference_determination_result,
)
class SourcePositionDeterminationAndComparison(NamedTuple):
    source_position_coordinate: dict[str, Any]
    determination_result: Event
    shared_position_result: Event | None
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
        if event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND:
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


def _record_shared_position_measurement(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    determination: Event,
) -> tuple[dict[str, Any], Event]:
    """Record the existing shared-position lifecycle from carried coordinates."""

    measurement_act = record_shared_position_measurement_act_occurrence_from_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_result_event_identity=determination.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(ledger, current_coordinates, measurement_act)
    shared_position_result = shared_position.record_shared_position_measurement_result(
        ledger,
        measurement_act_occurrence_event_identity=measurement_act.identity,
        current_coordinates=current_coordinates,
    )
    return _advance(ledger, current_coordinates, shared_position_result), shared_position_result


def _yield_source_position_determinations_and_comparisons(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Iterator[SourcePositionDeterminationAndComparison]:
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
            if len(
                determination.material["ordered_result_position_references"]
            ) != 2:
                shared_position_result = None
            else:
                current_coordinates, shared_position_result = _record_shared_position_measurement(
                    ledger, current_coordinates, determination
                )
        if shared_position_result is None:
            yield SourcePositionDeterminationAndComparison(
                coordinate,
                determination,
                None,
                None,
                current_coordinates,
            )
            continue
        comparisons = yield_shared_position_source_position_material_comparisons(
            ledger,
            shared_position_measurement_result_event_identity=shared_position_result.identity,
            current_coordinates=current_coordinates,
        )
        while True:
            with ledger.batched():
                try:
                    comparison = next(comparisons)
                except StopIteration:
                    break
            current_coordinates = comparison.current_coordinates
            yield SourcePositionDeterminationAndComparison(
                coordinate,
                determination,
                shared_position_result,
                comparison.result_occurrence,
                current_coordinates,
            )


def yield_source_position_determinations_and_comparisons(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Iterator[SourcePositionDeterminationAndComparison]:
    """Yield determinations and available Comparisons for every position."""

    yield from _yield_source_position_determinations_and_comparisons(
        ledger,
        direct_result_event_identity=direct_result_event_identity,
        current_coordinates=current_coordinates,
    )
