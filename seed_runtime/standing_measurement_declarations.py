"""Record declared Measurements whose exact subjects are carried in Standing.

The declarations in this module do not assign a new Responsibility.  Each
entry names one existing Book-assigned Measurement road.  Discovery chooses
one exact subject at one current Standing boundary, the family records its own
assignment, Act, Yield, and result, and Standing is advanced before discovery
continues.

Ledger writes remain serial and deterministic.  A later implementation may
compute pure discovery findings concurrently, but no two family occurrences
may be appended from one stale Standing boundary.
"""

from __future__ import annotations

from typing import Any, Callable, NamedTuple

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    _record_byte_measurement_responsibility_assignment_from_carried_standing,
    _record_byte_measurement_responsible_act_evidence_from_carried_standing,
    _record_byte_measurement_result_from_carried_act_evidence,
    record_byte_measurement_responsibility_assignment,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _record_byte_pair_occurrence_position_measurement_act_evidence_from_carried_assignment,
    _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_carried_finding,
    _record_byte_pair_occurrence_position_measurement_result_from_carried_act_evidence,
    measure_position_coordinates_of_byte_pair_occurrences,
    record_byte_pair_occurrence_position_measurement_responsibility_assignment,
)
from seed_runtime.material_ingest import read_exact_ingest_result
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    DETERMINATION_RESULT_KIND as ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND,
    _determination_result_reference as _addressed_byte_reference_result_reference,
)
from seed_runtime.measurement_of_source_position_coordinates_carrying_addressed_material import (
    RESPONSIBILITY_ASSIGNMENT_KIND as ADDRESSED_MATERIAL_COORDINATE_ASSIGNMENT_KIND,
    MEASUREMENT_RESULT_KIND as ADDRESSED_MATERIAL_COORDINATE_RESULT_KIND,
    _population_references as _addressed_material_population_references,
    _record_addressed_material_coordinate_measurement_lifecycle_from_carried_standing,
    _subject_is_unmeasured as _addressed_material_subject_is_unmeasured,
)
from seed_runtime.operator_locality_standing import (
    _carry_byte_measurement_assignment_into_standing,
    _carry_byte_pair_occurrence_position_measurement_assignment_into_standing,
    _carry_byte_pair_occurrence_position_measurement_result_into_standing,
    advance_operator_locality_standing,
    read_operator_locality_standing,
)


class StandingMeasurementDeclaration(NamedTuple):
    order: int
    book_clause_identity: str
    assignment_kind: str
    result_kind: str
    discover: Callable[[EventLedger, dict[str, Any], str], str | None]
    record: Callable[
        [EventLedger, dict[str, Any], str, str], tuple[dict[str, Any], Event]
    ]
    record_from_current: Callable[
        [EventLedger, dict[str, Any], str, str], tuple[dict[str, Any], Event]
    ]


class RecordedStandingMeasurements(NamedTuple):
    locality_standing: dict[str, Any]
    result_occurrences: tuple[Event, ...]


def _advance(
    ledger: EventLedger,
    standing: dict[str, Any],
    event_identities: tuple[str, ...],
    *,
    locality_identity: str,
) -> dict[str, Any]:
    return advance_operator_locality_standing(
        ledger,
        event_identities,
        locality_identity=locality_identity,
        prior=standing,
    )


def _require_current_pin(
    ledger: EventLedger,
    standing: dict[str, Any],
    *,
    locality_identity: str,
) -> None:
    if (
        not isinstance(ledger, EventLedger)
        or type(locality_identity) is not str
        or not locality_identity
        or type(standing) is not dict
        or standing.get("locality_identity") != locality_identity
        or type(standing.get("ingest_occurrences")) is not list
        or type(standing.get("measurement_occurrences")) is not dict
        or type(standing.get("responsibility_assignment_occurrences")) is not dict
    ):
        raise ValueError("declared Measurement recording requires exact current Standing")
    boundary = standing.get("through_event_occurrence_identity")
    event = ledger.get(boundary) if type(boundary) is str and boundary else None
    if (
        event is None
        or event.locality_identity != locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("declared Measurement recording requires the current append boundary")


def _ingest_identities(standing: dict[str, Any]) -> tuple[str, ...]:
    identities = []
    for occurrence in standing["ingest_occurrences"]:
        if (
            type(occurrence) is not dict
            or type(occurrence.get("evidence_event_identity")) is not str
            or not occurrence["evidence_event_identity"]
        ):
            raise ValueError("current Standing carries a malformed Ingest occurrence")
        identities.append(occurrence["evidence_event_identity"])
    return tuple(identities)


def _direct_assignment_sources(
    ledger: EventLedger, locality_identity: str
) -> set[str]:
    sources: set[str] = set()
    for assignment in ledger.iter_locality_kind(
        locality_identity, BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND
    ):
        source = assignment.material.get("source_ingest_occurrence_identity")
        if (
            ledger.integrity_of(assignment.identity) == CORRUPTED
            or type(source) is not str
            or not source
        ):
            raise ValueError("recorded direct Measurement assignment is malformed")
        sources.add(source)
    return sources


def _discover_direct_measurement(
    ledger: EventLedger, standing: dict[str, Any], locality_identity: str
) -> str | None:
    assigned = _direct_assignment_sources(ledger, locality_identity)
    for identity in _ingest_identities(standing):
        if identity in assigned:
            continue
        event = ledger.get(identity)
        if event is None or event.locality_identity != locality_identity:
            raise ValueError("current Standing carries an absent Ingest occurrence")
        if not all(
            type(event.material.get(key)) is str and event.material[key]
            for key in (
                "responsible_act_evidence_identity",
                "evidence_of_yield_relation_identity",
            )
        ):
            # Older preserved material can be an Ingest occurrence without an
            # exact Act/Yield result.  It is input to the aggregate byte road,
            # but it is not the exact subject of this direct Measurement.
            continue
        read_exact_ingest_result(ledger, identity)
        return identity
    return None


def _complete_direct_measurement(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    assignment: Event,
    finding,
) -> tuple[dict[str, Any], Event]:
    prior_boundary = standing["through_event_occurrence_identity"]
    standing = _carry_byte_pair_occurrence_position_measurement_assignment_into_standing(
        ledger,
        standing,
        assignment,
        finding,
        prior_through_event_occurrence_identity=prior_boundary,
    )
    act = _record_byte_pair_occurrence_position_measurement_act_evidence_from_carried_assignment(
        ledger,
        responsibility_assignment=assignment,
        finding=finding,
        responsibility_assignment_standing=standing,
    )
    standing = _advance(
        ledger,
        standing,
        (act.identity,),
        locality_identity=locality_identity,
    )
    result = _record_byte_pair_occurrence_position_measurement_result_from_carried_act_evidence(
        ledger,
        responsible_act_evidence=act,
        responsibility_assignment=assignment,
        finding=finding,
    )
    standing = _carry_byte_pair_occurrence_position_measurement_result_into_standing(
        standing,
        result,
        prior_through_event_occurrence_identity=act.identity,
    )
    return standing, result


def _record_direct_measurement(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    source_ingest_occurrence_identity: str,
) -> tuple[dict[str, Any], Event]:
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
    )
    if finding.source_locality_identity != locality_identity:
        raise ValueError("direct Measurement subject belongs to another Locality")
    assignment = _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_carried_finding(
        ledger,
        finding=finding,
        locality_standing=standing,
    )
    return _complete_direct_measurement(
        ledger, standing, locality_identity, assignment, finding
    )


def _record_direct_measurement_from_current(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    source_ingest_occurrence_identity: str,
) -> tuple[dict[str, Any], Event]:
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
    )
    if finding.source_locality_identity != locality_identity:
        raise ValueError("direct Measurement subject belongs to another Locality")
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
        locality_standing=standing,
    )
    return _complete_direct_measurement(
        ledger, standing, locality_identity, assignment, finding
    )


def _byte_assignment_source_sets(
    ledger: EventLedger, locality_identity: str
) -> set[tuple[str, ...]]:
    source_sets: set[tuple[str, ...]] = set()
    for assignment in ledger.iter_locality_kind(
        locality_identity, BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    ):
        references = assignment.material.get("source_occurrence_references")
        if (
            ledger.integrity_of(assignment.identity) == CORRUPTED
            or type(references) is not list
        ):
            raise ValueError("recorded byte Measurement assignment is malformed")
        identities = []
        for reference in references:
            if (
                type(reference) is not dict
                or set(reference) != {"ingest_occurrence_identity"}
                or type(reference["ingest_occurrence_identity"]) is not str
                or not reference["ingest_occurrence_identity"]
            ):
                raise ValueError("recorded byte Measurement source is malformed")
            identities.append(reference["ingest_occurrence_identity"])
        source_sets.add(tuple(identities))
    return source_sets


def _discover_byte_measurement(
    ledger: EventLedger, standing: dict[str, Any], locality_identity: str
) -> str | None:
    current_sources = _ingest_identities(standing)
    if not current_sources:
        return None
    if current_sources in _byte_assignment_source_sets(ledger, locality_identity):
        return None
    return current_sources[-1]


def _complete_byte_measurement(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    assignment: Event,
) -> tuple[dict[str, Any], Event]:
    prior_boundary = standing["through_event_occurrence_identity"]
    standing = _carry_byte_measurement_assignment_into_standing(
        ledger,
        standing,
        assignment,
        prior_through_event_occurrence_identity=prior_boundary,
    )
    act = _record_byte_measurement_responsible_act_evidence_from_carried_standing(
        ledger,
        responsibility_assignment=assignment,
        responsibility_assignment_standing=standing,
    )
    standing = _advance(
        ledger,
        standing,
        (act.identity,),
        locality_identity=locality_identity,
    )
    result = _record_byte_measurement_result_from_carried_act_evidence(
        ledger,
        responsible_act_evidence=act,
        responsibility_assignment=assignment,
        locality_standing=standing,
    )
    standing = _advance(
        ledger,
        standing,
        (
            result.material["evidence_of_yield_relation_identity"],
            result.identity,
        ),
        locality_identity=locality_identity,
    )
    return standing, result


def _record_byte_measurement(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    _subject_identity: str,
) -> tuple[dict[str, Any], Event]:
    assignment = _record_byte_measurement_responsibility_assignment_from_carried_standing(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
        locality_standing=standing,
    )
    return _complete_byte_measurement(
        ledger, standing, locality_identity, assignment
    )


def _record_byte_measurement_from_current(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    _subject_identity: str,
) -> tuple[dict[str, Any], Event]:
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
        locality_standing=standing,
    )
    return _complete_byte_measurement(
        ledger, standing, locality_identity, assignment
    )


def _discover_addressed_material_coordinate_measurement(
    ledger: EventLedger, standing: dict[str, Any], locality_identity: str
) -> str | None:
    measurements = standing["measurement_occurrences"]
    for occurrence_identity in measurements:
        event = ledger.get(occurrence_identity)
        if event is None or event.kind != ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND:
            continue
        if (
            ledger.integrity_of(event.identity) == CORRUPTED
            or event.exact_material is not None
            or measurements[occurrence_identity]
            != _addressed_byte_reference_result_reference(event)
        ):
            raise ValueError("current Standing carries an inexact addressed result")
        source_reference = event.material.get("direct_pair_position_result_reference")
        source_identity = (
            source_reference.get("recorded_occurrence_identity")
            if type(source_reference) is dict
            else None
        )
        if type(source_identity) is not str or not source_identity:
            raise ValueError("addressed Measurement result carries no exact direct source")
        if _addressed_material_subject_is_unmeasured(
                ledger,
                locality_identity=locality_identity,
                addressed_result_identity=occurrence_identity,
                population=_addressed_material_population_references(
                    ledger,
                    standing,
                    locality_identity=locality_identity,
                    excluded_result_identity=source_identity,
                ),
            ):
            return occurrence_identity
    return None


def _record_addressed_material_coordinate_measurement(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    addressed_result_identity: str,
) -> tuple[dict[str, Any], Event]:
    return _record_addressed_material_coordinate_measurement_lifecycle_from_carried_standing(
        ledger,
        addressed_determination_result_event_identity=addressed_result_identity,
        locality_standing=standing,
    )


def _record_addressed_material_coordinate_measurement_from_current(
    ledger: EventLedger,
    standing: dict[str, Any],
    locality_identity: str,
    addressed_result_identity: str,
) -> tuple[dict[str, Any], Event]:
    _require_current_pin(ledger, standing, locality_identity=locality_identity)
    return _record_addressed_material_coordinate_measurement_lifecycle_from_carried_standing(
        ledger,
        addressed_determination_result_event_identity=addressed_result_identity,
        locality_standing=standing,
    )


STANDING_MEASUREMENT_DECLARATIONS = (
    StandingMeasurementDeclaration(
        0,
        "01.Source.D",
        BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        _discover_direct_measurement,
        _record_direct_measurement,
        _record_direct_measurement_from_current,
    ),
    StandingMeasurementDeclaration(
        1,
        "01.Source.D",
        BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        BYTE_MEASUREMENT_RECORDED_KIND,
        _discover_byte_measurement,
        _record_byte_measurement,
        _record_byte_measurement_from_current,
    ),
    StandingMeasurementDeclaration(
        2,
        "01.Source.D",
        ADDRESSED_MATERIAL_COORDINATE_ASSIGNMENT_KIND,
        ADDRESSED_MATERIAL_COORDINATE_RESULT_KIND,
        _discover_addressed_material_coordinate_measurement,
        _record_addressed_material_coordinate_measurement,
        _record_addressed_material_coordinate_measurement_from_current,
    ),
)


def _record_declared_measurements_from_carried_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    *,
    locality_identity: str,
) -> RecordedStandingMeasurements:
    """Record one lawful declaration per exact Standing boundary until quiet."""

    standing = locality_standing
    results: list[Event] = []
    while True:
        _require_current_pin(
            ledger,
            standing,
            locality_identity=locality_identity,
        )
        eligible = []
        for declaration in STANDING_MEASUREMENT_DECLARATIONS:
            subject = declaration.discover(ledger, standing, locality_identity)
            if subject is not None:
                eligible.append((declaration.order, subject, declaration))
        if not eligible:
            return RecordedStandingMeasurements(standing, tuple(results))
        _order, subject, declaration = min(eligible, key=lambda item: item[:2])
        standing, result = declaration.record(
            ledger,
            standing,
            locality_identity,
            subject,
        )
        if result.kind != declaration.result_kind:
            raise ValueError("declared Measurement recorded another result kind")
        results.append(result)


def record_declared_measurements_from_current_standing(
    ledger: EventLedger,
    *,
    locality_identity: str,
) -> RecordedStandingMeasurements:
    """Read one current Locality Standing and record its declared Measurements."""

    standing = read_operator_locality_standing(
        ledger,
        locality_identity=locality_identity,
    )
    eligible = []
    for declaration in STANDING_MEASUREMENT_DECLARATIONS:
        subject = declaration.discover(ledger, standing, locality_identity)
        if subject is not None:
            eligible.append((declaration.order, subject, declaration))
    if not eligible:
        return RecordedStandingMeasurements(standing, ())
    _order, subject, declaration = min(eligible, key=lambda item: item[:2])
    standing, result = declaration.record_from_current(
        ledger,
        standing,
        locality_identity,
        subject,
    )
    remaining = _record_declared_measurements_from_carried_standing(
        ledger,
        standing,
        locality_identity=locality_identity,
    )
    return RecordedStandingMeasurements(
        remaining.locality_standing,
        (result, *remaining.result_occurrences),
    )
