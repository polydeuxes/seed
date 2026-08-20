"""Continue each addressed source position through path-ordered Compare."""

from __future__ import annotations

from typing import Any, Iterator, NamedTuple

from seed_runtime.addressed_byte_occurrence_reference_determination import (
    _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing,
)
from seed_runtime.comparison_of_ordered_path_source_position_material import (
    yield_ordered_path_source_position_material_comparisons,
)
from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.evidence_of_yield_relation import (
    _record_evidence_of_yield_relation,
)
import seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences as shared_position
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    carried_position_measurement_result_reading,
    source_position_coordinate_references_of_recorded_position_measurement,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
    record_shared_position_responsibility_assignment_from_addressed_byte_occurrence_reference_determination_result,
)
from seed_runtime.operator_locality_standing import (
    _exact_standing_additions,
    _record_distinct,
)


class OrderedPathSourcePositionContinuation(NamedTuple):
    source_position_coordinate: dict[str, Any]
    determination_result: Event
    ordered_path_result: Event | None
    comparison_result: Event | None
    locality_standing: dict[str, Any]


def _advance(
    ledger: EventLedger,
    standing: dict[str, Any],
    *events: Event,
) -> dict[str, Any]:
    locality_identity = standing["locality_identity"]
    prior = standing["through_event_occurrence_identity"]
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
        raise ValueError("source-position continuation left its exact boundary")
    for event in events:
        additions = _exact_standing_additions(
            standing,
            event,
            error_message="source-position continuation Standing is not exact",
        )
        if event.kind == SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND:
            standing["responsibility_assignment_occurrences"][event.identity] = None
        elif event.kind == SHARED_POSITION_APPLICABILITY_RESULT_KIND:
            standing["applicability_result_occurrences"][event.identity] = None
        elif event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND:
            standing["measurement_occurrences"][event.identity] = {
                "recorded_occurrence_identity": event.identity,
                "result_identity": event.material["result_identity"],
                "act_occurrence_identity": event.material["act_occurrence_identity"],
                "responsible_act_evidence_identity": event.material[
                    "responsible_act_evidence_identity"
                ],
                "evidence_of_yield_relation_identity": event.material[
                    "evidence_of_yield_relation_identity"
                ],
            }
        for key, values in additions.items():
            for value in values:
                _record_distinct(standing[key], value)
        standing["through_event_occurrence_identity"] = event.identity
        standing["event_count"] += 1
    return standing


def _record_shared_path(
    ledger: EventLedger,
    standing: dict[str, Any],
    determination: Event,
) -> tuple[dict[str, Any], Event]:
    """Record the existing shared-position lifecycle from carried coordinates."""

    assignment = record_shared_position_responsibility_assignment_from_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_result_event_identity=determination.identity,
        locality_standing=standing,
    )
    _result, inputs = shared_position._d2_result_inputs(
        ledger,
        result_event_identity=determination.identity,
        prior_standing=standing,
    )
    standing = _advance(ledger, standing, assignment)
    applicability_act = ledger.append(
        shared_position.SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND,
        shared_position._applicability_act_material(
            assignment=assignment,
            inputs=inputs,
            standing_boundary_identity=standing[
                "through_event_occurrence_identity"
            ],
        ),
        locality_identity=assignment.locality_identity,
    )
    standing = _advance(ledger, standing, applicability_act)
    applicability_material = shared_position._applicability_result_material(
        act=applicability_act,
        assignment=assignment,
        inputs=inputs,
    )
    applicability_yield = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=assignment.locality_identity,
        exact_act=shared_position.APPLICABILITY_ACT,
        act_occurrence_identity=applicability_act.material[
            "applicability_act_occurrence_identity"
        ],
        responsible_act_evidence_identity=applicability_act.identity,
        result_kind=shared_position.APPLICABILITY_RESULT_KIND,
        result_identity=applicability_material["result_identity"],
        result_content={
            coordinate: value
            for coordinate, value in applicability_material.items()
            if coordinate != "responsible_act_evidence_identity"
        },
        responsibility=shared_position.RESPONSIBILITY,
        occurrence_boundary="shared_pair_position_applicability",
        responsible_boundary="this Seed",
        responsible_act_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
    )
    applicability = ledger.append(
        shared_position.SHARED_POSITION_APPLICABILITY_RESULT_KIND,
        shared_position._recorded_applicability_result_material(
            applicability_material,
            evidence_of_yield_relation_identity=applicability_yield.identity,
        ),
        locality_identity=assignment.locality_identity,
    )
    standing = _advance(
        ledger, standing, applicability_yield, applicability
    )
    measurement_act = ledger.append(
        shared_position.SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND,
        shared_position._measurement_act_material(
            assignment=assignment,
            inputs=inputs,
            applicability=applicability,
            standing_boundary_identity=standing[
                "through_event_occurrence_identity"
            ],
        ),
        locality_identity=assignment.locality_identity,
    )
    standing = _advance(ledger, standing, measurement_act)
    result_material = shared_position._measurement_result_material(
        act=measurement_act,
        assignment=assignment,
        applicability=applicability,
        inputs=inputs,
    )
    path_yield = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=assignment.locality_identity,
        exact_act=shared_position.MEASUREMENT_ACT,
        act_occurrence_identity=measurement_act.material[
            "act_occurrence_identity"
        ],
        responsible_act_evidence_identity=measurement_act.identity,
        result_kind=shared_position.MEASUREMENT_RESULT_KIND,
        result_identity=result_material["result_identity"],
        result_content={
            coordinate: value
            for coordinate, value in result_material.items()
            if coordinate != "responsible_act_evidence_identity"
        },
        responsibility=shared_position.RESPONSIBILITY,
        occurrence_boundary="shared_pair_position_measurement",
        responsible_boundary="this Seed",
    )
    path = ledger.append(
        shared_position.SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        shared_position._recorded_measurement_result_material(
            result_material,
            evidence_of_yield_relation_identity=path_yield.identity,
        ),
        locality_identity=assignment.locality_identity,
    )
    return _advance(ledger, standing, path_yield, path), path


def _yield_ordered_path_source_position_continuations(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Iterator[OrderedPathSourcePositionContinuation]:
    """Yield each bounded source-position continuation before its siblings."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("source-position continuation requires one EventLedger")
    standing = locality_standing
    for coordinate in source_position_coordinate_references_of_recorded_position_measurement(
        ledger, direct_result_event_identity
    ):
        with ledger.batched():
            standing, determination = (
                _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing(
                    ledger,
                    direct_result_event_identity=direct_result_event_identity,
                    addressed_source_byte_position_coordinate_reference=coordinate,
                    locality_standing=standing,
                    mutate_locality_standing=True,
                )
            )
            if len(determination.material["ordered_assertion_references"]) != 2:
                path = None
            else:
                standing, path = _record_shared_path(
                    ledger, standing, determination
                )
        if path is None:
            yield OrderedPathSourcePositionContinuation(
                coordinate,
                determination,
                None,
                None,
                standing,
            )
            continue
        comparisons = yield_ordered_path_source_position_material_comparisons(
            ledger,
            path_result_event_identity=path.identity,
            locality_standing=standing,
        )
        while True:
            with ledger.batched():
                try:
                    comparison = next(comparisons)
                except StopIteration:
                    break
            standing = comparison.locality_standing
            yield OrderedPathSourcePositionContinuation(
                coordinate,
                determination,
                path,
                comparison.result_occurrence,
                standing,
            )


def yield_ordered_path_source_position_continuations(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Iterator[OrderedPathSourcePositionContinuation]:
    """Yield bounded continuations from one validated direct-result reading."""

    with carried_position_measurement_result_reading(
        ledger, direct_result_event_identity
    ):
        yield from _yield_ordered_path_source_position_continuations(
            ledger,
            direct_result_event_identity=direct_result_event_identity,
            locality_standing=locality_standing,
        )
