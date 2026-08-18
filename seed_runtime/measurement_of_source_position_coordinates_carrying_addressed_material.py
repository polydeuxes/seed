"""Measure source-position coordinates carrying one addressed byte material.

The value used by this exact Measurement rule comes only from one exact D.2
addressed source-byte coordinate.  The Measurement scans the intact direct
pair-position results carried by the same current Locality Standing and
returns every distinct source-position coordinate carrying that exact
one-byte material.  It establishes neither occurrence identity across
sources nor any represented relation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, NamedTuple

from seed_runtime.addressed_byte_occurrence_reference_determination import (
    DETERMINATION_RESULT_KIND as ADDRESSED_REFERENCE_RESULT_KIND,
    _determination_result_reference as _addressed_result_reference,
    _read_determination_result as _read_addressed_result,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    FindingOfPositionCoordinatesOfBytePairOccurrences,
    ReferenceToRecordedPositionOfBytePairOccurrence,
    _read_result as _read_direct_result,
    _recorded_position_reference,
)


RESPONSIBILITY_ASSIGNMENT_KIND = (
    "operator.measurement_of_source_position_coordinates_carrying_addressed_material."
    "responsibility_assignment_recorded"
)
APPLICABILITY_ACT_EVIDENCE_KIND = (
    "operator.measurement_of_source_position_coordinates_carrying_addressed_material."
    "applicability_act_evidenced"
)
APPLICABILITY_RESULT_KIND = (
    "operator.measurement_of_source_position_coordinates_carrying_addressed_material."
    "applicability_recorded"
)
MEASUREMENT_ACT_EVIDENCE_KIND = (
    "operator.measurement_of_source_position_coordinates_carrying_addressed_material."
    "measurement_act_evidenced"
)
MEASUREMENT_RESULT_KIND = (
    "operator.measurement_of_source_position_coordinates_carrying_addressed_material."
    "measurement_recorded"
)

BOOK_CLAUSE = "01.Source.D"
RESPONSIBILITY = (
    "Measurement of every distinct source-position coordinate reference carrying the "
    "exact one-byte material of one addressed source-byte coordinate"
)
APPLICABILITY_ACT = (
    "addressed-material source-position coordinate Measurement Applicability"
)
MEASUREMENT_ACT = (
    "exact Measurement of source-position coordinate references carrying "
    "the exact one-byte material of one addressed coordinate"
)
MEASUREMENT_RULE = (
    "every distinct source-position coordinate reference in the carried direct "
    "pair-position results that carry the exact one-byte material of the addressed "
    "coordinate, in direct-result and source-coordinate "
    "order"
)
APPLICABILITY_RESULT_NAME = (
    "addressed-material source-position coordinate Applicability result"
)
MEASUREMENT_RESULT_NAME = (
    "result of exact Measurement of source-position coordinate references "
    "carrying addressed exact material"
)
APPLICABILITY_BOUNDARY = (
    "source_position_coordinates_carrying_addressed_material_applicability"
)
MEASUREMENT_BOUNDARY = (
    "measurement_of_source_position_coordinates_carrying_addressed_material"
)
LIMITS = [
    "bounded to one exact D.2 result, one current Locality Standing boundary, "
    "and its ordered collection of intact direct pair-position results",
    "same exact one-byte material establishes no same occurrence and no "
    "same position",
    "establishes no represented relation, recurrence, shared position relation, "
    "or downstream Applicability",
]
UNKNOWN = [
    "what the addressed byte occurrence represents remains Unknown",
    "what each measured source-position coordinate represents remains Unknown",
]

EVENT_KIND_RESPONSIBILITIES = {
    RESPONSIBILITY_ASSIGNMENT_KIND: "01.Source.D",
    APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    APPLICABILITY_RESULT_KIND: "01.Standing.E.1",
    MEASUREMENT_ACT_EVIDENCE_KIND: "02.Acts.A",
    MEASUREMENT_RESULT_KIND: "01.Source.D",
}


class AddressedMaterialCoordinateMeasurementError(ValueError):
    """One addressed-material coordinate Measurement is not exact."""


class MeasuredAddressedMaterialCoordinate(NamedTuple):
    direct_pair_position_result_reference: dict[str, str]
    pair_position_assertion_reference: dict[str, str]
    coordinate_role: str
    source_position_coordinate_reference: dict[str, Any]


_IDENTITY_COORDINATES = (
    "assignment_identity",
    "assignment_subject_identity",
    "applicability_act_identity",
    "applicability_act_occurrence_identity",
    "applicability_result_identity",
    "measurement_act_identity",
    "measurement_act_occurrence_identity",
    "measurement_result_identity",
)


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise AddressedMaterialCoordinateMeasurementError(message)
    return value


def _assignment_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "assignment_identity": event.material["assignment_identity"],
        "assignment_subject_identity": event.material[
            "assignment_subject_identity"
        ],
    }


def _applicability_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material[
            "applicability_act_occurrence_identity"
        ],
        "responsible_act_evidence_identity": event.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": event.material[
            "evidence_of_yield_relation_identity"
        ],
    }


def measurement_result_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material[
            "measurement_act_occurrence_identity"
        ],
        "responsible_act_evidence_identity": event.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": event.material[
            "evidence_of_yield_relation_identity"
        ],
    }


def _direct_result_reference(event: Event) -> dict[str, str]:
    return {
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


def _coordinate_is_exact(value: Any) -> bool:
    return (
        type(value) is dict
        and set(value)
        == {
            "identity",
            "source_ingest_occurrence_identity",
            "locality_identity",
            "completeness_boundary_identity",
            "position",
            "exact_material",
        }
        and type(value.get("identity")) is str
        and bool(value["identity"])
        and type(value.get("source_ingest_occurrence_identity")) is str
        and bool(value["source_ingest_occurrence_identity"])
        and type(value.get("locality_identity")) is str
        and bool(value["locality_identity"])
        and type(value.get("completeness_boundary_identity")) is str
        and bool(value["completeness_boundary_identity"])
        and type(value.get("position")) is int
        and value["position"] >= 0
        and type(value.get("exact_material")) is list
        and len(value["exact_material"]) == 1
        and type(value["exact_material"][0]) is int
        and 0 <= value["exact_material"][0] <= 255
    )


def _addressed_source(
    ledger: EventLedger,
    result_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any]]:
    try:
        result, _act, _applicability, _assignment, _source, _references = (
            _read_addressed_result(
                ledger, result_identity, prior_standing=prior_standing
            )
        )
    except (TypeError, ValueError) as error:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement requires one intact D.2 result"
        ) from error
    coordinate = result.material.get(
        "addressed_source_byte_position_coordinate_reference"
    )
    if (
        result.kind != ADDRESSED_REFERENCE_RESULT_KIND
        or not _coordinate_is_exact(coordinate)
        or result.locality_identity != coordinate["locality_identity"]
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement requires one exact addressed coordinate"
        )
    return result, deepcopy(coordinate)


def _direct_result(
    ledger: EventLedger, reference: dict[str, Any], *, locality_identity: str
) -> tuple[Event, FindingOfPositionCoordinatesOfBytePairOccurrences]:
    identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    event = ledger.get(identity) if type(identity) is str else None
    if (
        event is None
        or event.kind != BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        or event.locality_identity != locality_identity
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
        or reference != _direct_result_reference(event)
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement requires intact direct results"
        )
    try:
        read_event, finding, _assertions = _read_direct_result(ledger, event.identity)
    except (TypeError, ValueError) as error:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement requires intact direct results"
        ) from error
    if read_event != event:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement requires intact direct results"
        )
    return event, finding


def _population_references(
    ledger: EventLedger,
    standing: dict[str, Any],
    *,
    locality_identity: str,
) -> tuple[dict[str, str], ...]:
    measurements = standing.get("measurement_occurrences")
    if type(measurements) is not dict:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement requires exact current Standing"
        )
    found = []
    for identity, carried in measurements.items():
        event = ledger.get(identity)
        if event is None or event.kind != BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
            continue
        reference = _direct_result_reference(event)
        if carried != reference:
            raise AddressedMaterialCoordinateMeasurementError(
                "current Standing carries a malformed direct result"
            )
        found.append(reference)
    return tuple(found)


def _measured_coordinates(
    ledger: EventLedger,
    *,
    direct_result_references: tuple[dict[str, str], ...],
    addressed_coordinate: dict[str, Any],
    locality_identity: str,
) -> tuple[MeasuredAddressedMaterialCoordinate, ...]:
    target = addressed_coordinate["exact_material"]
    seen: set[str] = set()
    measured = []
    for direct_reference in direct_result_references:
        event, finding = _direct_result(
            ledger, direct_reference, locality_identity=locality_identity
        )
        for first_position in range(max(0, len(finding.exact_material) - 1)):
            second_position = first_position + 1
            reference = _recorded_position_reference(
                event,
                finding,
                exact_pair=finding.exact_material[first_position : second_position + 1],
                first_position=first_position,
                second_position=second_position,
            )
            for role, coordinate in (
                ("first_position_coordinate", reference.first_position_coordinate_reference),
                ("second_position_coordinate", reference.second_position_coordinate_reference),
            ):
                identity = coordinate["identity"]
                if coordinate["exact_material"] != target or identity in seen:
                    continue
                seen.add(identity)
                measured.append(
                    MeasuredAddressedMaterialCoordinate(
                        _direct_result_reference(event),
                        reference.assertion_reference,
                        role,
                        deepcopy(coordinate),
                    )
                )
    return tuple(measured)


def _standing_source(
    ledger: EventLedger,
    *,
    standing: dict[str, Any],
    addressed_result_identity: str,
    required_boundary_identity: str,
) -> tuple[Event, dict[str, Any], tuple[dict[str, str], ...]]:
    if type(standing) is not dict:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement requires exact current Standing"
        )
    locality = standing.get("locality_identity")
    through = standing.get("through_event_occurrence_identity")
    measurements = standing.get("measurement_occurrences")
    if (
        type(locality) is not str
        or not locality
        or type(through) is not str
        or not through
        or type(required_boundary_identity) is not str
        or not required_boundary_identity
        or type(measurements) is not dict
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement requires exact current Standing"
        )
    addressed_result, coordinate = _addressed_source(
        ledger, addressed_result_identity, prior_standing=standing
    )
    if (
        addressed_result.locality_identity != locality
        or measurements.get(addressed_result.identity)
        != _addressed_result_reference(addressed_result)
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "current Standing carries no exact D.2 result"
        )
    population = _population_references(
        ledger,
        standing,
        locality_identity=locality,
    )
    source_identities = (
        addressed_result.identity,
        *(item["recorded_occurrence_identity"] for item in population),
    )
    try:
        if len(population) > 1:
            ledger.occurrences_in_append_order(
                tuple(item["recorded_occurrence_identity"] for item in population),
                locality_identity=locality,
            )
        for identity in source_identities:
            if identity != required_boundary_identity:
                ledger.occurrences_in_append_order(
                    (identity, required_boundary_identity),
                    locality_identity=locality,
                )
        required_through = tuple(dict.fromkeys((required_boundary_identity, through)))
        events = ledger.occurrences_in_append_order(
            required_through, locality_identity=locality
        )
    except (TypeError, ValueError) as error:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement Standing order is false"
        ) from error
    if tuple(event.identity for event in events) != required_through:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement Standing order is false"
        )
    return addressed_result, coordinate, population


def _require_tip(ledger: EventLedger, event: Event | None, message: str) -> None:
    if (
        event is None
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise AddressedMaterialCoordinateMeasurementError(message)


def _require_current_standing(
    ledger: EventLedger,
    *,
    locality_standing: dict[str, Any],
    addressed_result_identity: str,
) -> tuple[dict[str, Any], Event, dict[str, Any], tuple[dict[str, str], ...]]:
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    locality = (
        locality_standing.get("locality_identity")
        if type(locality_standing) is dict
        else None
    )
    current = read_operator_locality_standing(
        ledger,
        locality_identity=_identity(
            locality, "addressed-material Measurement requires one Locality"
        ),
    )
    if locality_standing != current:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement requires exact current Standing"
        )
    boundary = current["through_event_occurrence_identity"]
    addressed, coordinate, population = _standing_source(
        ledger,
        standing=current,
        addressed_result_identity=addressed_result_identity,
        required_boundary_identity=boundary,
    )
    _require_tip(
        ledger,
        ledger.get(boundary),
        "addressed-material Measurement requires Standing at the append tip",
    )
    return current, addressed, coordinate, population


def _authority() -> dict[str, str]:
    return {
        "source": "this Book",
        "book_clause_identity": BOOK_CLAUSE,
        "authority_limit": "bounded",
        "act": MEASUREMENT_ACT,
        "negative_authority": (
            "establish no occurrence identity of different source occurrences and no represented relation"
        ),
    }


def _scope(
    *, locality_identity: str, standing_boundary_identity: str
) -> dict[str, str]:
    return {
        "locality_identity": locality_identity,
        "completeness_boundary_identity": standing_boundary_identity,
    }


def _assignment_material(
    *,
    addressed_result: Event,
    addressed_coordinate: dict[str, Any],
    population: tuple[dict[str, str], ...],
    standing_boundary_identity: str,
    identities: dict[str, str],
) -> dict[str, Any]:
    return {
        "assignment_identity": identities["assignment_identity"],
        "assignment_subject_identity": identities["assignment_subject_identity"],
        "applicability_act_identity": identities["applicability_act_identity"],
        "applicability_act_occurrence_identity": identities[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": identities[
            "applicability_result_identity"
        ],
        "measurement_act_identity": identities["measurement_act_identity"],
        "measurement_act_occurrence_identity": identities[
            "measurement_act_occurrence_identity"
        ],
        "measurement_result_identity": identities["measurement_result_identity"],
        "book_clause_identity": BOOK_CLAUSE,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "addressed_determination_result_reference": _addressed_result_reference(
            addressed_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            addressed_coordinate
        ),
        "direct_pair_position_result_references": deepcopy(list(population)),
        "measurement_rule": MEASUREMENT_RULE,
        "standing_boundary_identity": standing_boundary_identity,
        "scope": _scope(
            locality_identity=addressed_result.locality_identity,
            standing_boundary_identity=standing_boundary_identity,
        ),
        "authority": _authority(),
        "limits": list(LIMITS),
        "unknown": list(UNKNOWN),
    }


def _subject_key(material: dict[str, Any]) -> tuple[str, tuple[str, ...]] | None:
    addressed = material.get("addressed_determination_result_reference")
    population = material.get("direct_pair_position_result_references")
    if type(addressed) is not dict or type(population) is not list:
        return None
    addressed_identity = addressed.get("recorded_occurrence_identity")
    direct_identities = tuple(
        item.get("recorded_occurrence_identity")
        for item in population
        if type(item) is dict
    )
    if (
        type(addressed_identity) is not str
        or not addressed_identity
        or len(direct_identities) != len(population)
        or any(type(identity) is not str or not identity for identity in direct_identities)
    ):
        return None
    return addressed_identity, direct_identities


def _refuse_existing_subject(
    ledger: EventLedger, *, locality_identity: str, key: tuple[str, tuple[str, ...]]
) -> None:
    for kind in (RESPONSIBILITY_ASSIGNMENT_KIND, MEASUREMENT_RESULT_KIND):
        for event in ledger.iter_locality_kind(locality_identity, kind):
            if ledger.integrity_of(event.identity) == CORRUPTED:
                raise AddressedMaterialCoordinateMeasurementError(
                    "addressed-material Measurement history is corrupted"
                )
            if _subject_key(event.material) == key:
                raise AddressedMaterialCoordinateMeasurementError(
                    "addressed-material Measurement subject is already assigned or measured"
                )


def _new_identities() -> dict[str, str]:
    prefixes = {
        "assignment_identity": "addressed_material_coordinate_assignment",
        "assignment_subject_identity": "addressed_material_coordinate_assignment_subject",
        "applicability_act_identity": "addressed_material_coordinate_applicability_act",
        "applicability_act_occurrence_identity": "addressed_material_coordinate_applicability_act_occurrence",
        "applicability_result_identity": "addressed_material_coordinate_applicability_result",
        "measurement_act_identity": "addressed_material_coordinate_measurement_act",
        "measurement_act_occurrence_identity": "addressed_material_coordinate_measurement_act_occurrence",
        "measurement_result_identity": "addressed_material_coordinate_measurement_result",
    }
    identities = {key: new_identity(prefix) for key, prefix in prefixes.items()}
    if len(set(identities.values())) != len(identities):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement lifecycle identities collapsed"
        )
    return identities


def _append_assignment(
    ledger: EventLedger,
    *,
    standing: dict[str, Any],
    addressed_result: Event,
    addressed_coordinate: dict[str, Any],
    population: tuple[dict[str, str], ...],
    expected_global_boundary: Any | None = None,
) -> Event:
    boundary = standing["through_event_occurrence_identity"]
    expected_material = _assignment_material(
        addressed_result=addressed_result,
        addressed_coordinate=addressed_coordinate,
        population=population,
        standing_boundary_identity=boundary,
        identities=_new_identities(),
    )
    _refuse_existing_subject(
        ledger,
        locality_identity=addressed_result.locality_identity,
        key=_subject_key(expected_material),
    )
    if expected_global_boundary is None:
        _require_tip(
            ledger,
            ledger.get(boundary),
            "addressed-material Measurement source left the append tip",
        )
    elif ledger.append_boundary() != expected_global_boundary:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material global recording boundary changed before assignment"
        )
    event = ledger.append(
        RESPONSIBILITY_ASSIGNMENT_KIND,
        _assignment_material(
            addressed_result=addressed_result,
            addressed_coordinate=addressed_coordinate,
            population=population,
            standing_boundary_identity=boundary,
            identities={
                key: expected_material[key] for key in _IDENTITY_COORDINATES
            },
        ),
        locality_identity=addressed_result.locality_identity,
    )
    if event.material != expected_material:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material assignment changed while it was recorded"
        )
    return event


def record_addressed_material_coordinate_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    addressed_determination_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    if not isinstance(ledger, EventLedger):
        raise TypeError("addressed-material assignment requires an EventLedger")
    current, addressed, coordinate, population = _require_current_standing(
        ledger,
        locality_standing=locality_standing,
        addressed_result_identity=_identity(
            addressed_determination_result_event_identity,
            "addressed-material assignment requires one D.2 result",
        ),
    )
    _measured_coordinates(
        ledger,
        direct_result_references=population,
        addressed_coordinate=coordinate,
        locality_identity=addressed.locality_identity,
    )
    return _append_assignment(
        ledger,
        standing=current,
        addressed_result=addressed,
        addressed_coordinate=coordinate,
        population=population,
    )


def _record_addressed_material_coordinate_measurement_assignment_from_carried_standing(
    ledger: EventLedger,
    *,
    addressed_determination_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    boundary = (
        locality_standing.get("through_event_occurrence_identity")
        if type(locality_standing) is dict
        else None
    )
    _require_tip(
        ledger,
        ledger.get(boundary) if type(boundary) is str else None,
        "addressed-material Measurement requires carried Standing at the append tip",
    )
    addressed, coordinate, population = _standing_source(
        ledger,
        standing=locality_standing,
        addressed_result_identity=addressed_determination_result_event_identity,
        required_boundary_identity=boundary,
    )
    _measured_coordinates(
        ledger,
        direct_result_references=population,
        addressed_coordinate=coordinate,
        locality_identity=addressed.locality_identity,
    )
    return _append_assignment(
        ledger,
        standing=locality_standing,
        addressed_result=addressed,
        addressed_coordinate=coordinate,
        population=population,
    )


def _read_assignment(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, Event, dict[str, Any], tuple[dict[str, str], ...]]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != RESPONSIBILITY_ASSIGNMENT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material assignment is absent or corrupted"
        )
    material = event.material
    addressed_reference = material.get("addressed_determination_result_reference")
    addressed_identity = (
        addressed_reference.get("recorded_occurrence_identity")
        if type(addressed_reference) is dict
        else None
    )
    population_material = material.get("direct_pair_position_result_references")
    boundary = material.get("standing_boundary_identity")
    if (
        type(population_material) is not list
        or type(boundary) is not str
        or not boundary
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material assignment coordinates are not exact"
        )
    if prior_standing is None:
        from seed_runtime.operator_locality_standing import (
            read_operator_locality_standing_through,
        )

        prior_standing = read_operator_locality_standing_through(
            ledger,
            locality_identity=event.locality_identity,
            through_event_occurrence_identity=boundary,
        )
    addressed, coordinate, population = _standing_source(
        ledger,
        standing=prior_standing,
        addressed_result_identity=addressed_identity,
        required_boundary_identity=boundary,
    )
    _measured_coordinates(
        ledger,
        direct_result_references=population,
        addressed_coordinate=coordinate,
        locality_identity=addressed.locality_identity,
    )
    identities = {key: material.get(key) for key in _IDENTITY_COORDINATES}
    expected = _assignment_material(
        addressed_result=addressed,
        addressed_coordinate=coordinate,
        population=population,
        standing_boundary_identity=boundary,
        identities=identities,
    )
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or addressed_reference != _addressed_result_reference(addressed)
        or population_material != list(population)
        or event.locality_identity != addressed.locality_identity
        or material != expected
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material assignment coordinates are not exact"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (boundary, event.identity), locality_identity=event.locality_identity
        )
    except ValueError as error:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material assignment order is false"
        ) from error
    if tuple(item.identity for item in ordered) != (boundary, event.identity):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material assignment order is false"
        )
    return event, addressed, coordinate, population


def get_addressed_material_coordinate_measurement_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_assignment(ledger, event_identity)[0].material)


def _stage_standing(
    ledger: EventLedger,
    *,
    standing: dict[str, Any],
    assignment: Event,
    required_tip: Event,
    require_applicability: bool = False,
) -> None:
    locality = assignment.locality_identity
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    current = read_operator_locality_standing(ledger, locality_identity=locality)
    assignments = current.get("responsibility_assignment_occurrences")
    applicability = current.get("applicability_result_occurrences")
    if (
        standing != current
        or current.get("through_event_occurrence_identity") != required_tip.identity
        or type(assignments) is not dict
        or assignments.get(assignment.identity, object()) is not None
        or (
            require_applicability
            and (
                type(applicability) is not dict
                or applicability.get(required_tip.identity, object()) is not None
            )
        )
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "current Standing carries no exact addressed-material Measurement stage"
        )
    _require_tip(
        ledger,
        required_tip,
        "addressed-material Measurement stage left the append tip",
    )


def _refuse_act(ledger: EventLedger, assignment: Event, kind: str, coordinate: str) -> None:
    for event in ledger.iter_locality_kind(assignment.locality_identity, kind):
        if (
            event.material.get(coordinate) == assignment.material[coordinate]
            or event.material.get("responsibility_assignment_reference")
            == _assignment_reference(assignment)
        ):
            raise AddressedMaterialCoordinateMeasurementError(
                "addressed-material assignment already carries this Act"
            )


def _applicability_act_material(assignment: Event) -> dict[str, Any]:
    return {
        "applicability_act_identity": assignment.material["applicability_act_identity"],
        "applicability_act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "act": APPLICABILITY_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "addressed_determination_result_reference": deepcopy(
            assignment.material["addressed_determination_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            assignment.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "direct_pair_position_result_references": deepcopy(
            assignment.material["direct_pair_position_result_references"]
        ),
        "measurement_rule": MEASUREMENT_RULE,
        "downstream_act_identity": assignment.material["measurement_act_identity"],
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "evidence_scope": "Evidence for this exact Applicability Act occurrence",
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def record_addressed_material_coordinate_measurement_applicability_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    assignment, _addressed, _coordinate, _population = _read_assignment(
        ledger, responsibility_assignment_event_identity
    )
    _stage_standing(
        ledger,
        standing=responsibility_assignment_standing,
        assignment=assignment,
        required_tip=assignment,
    )
    _refuse_act(
        ledger,
        assignment,
        APPLICABILITY_ACT_EVIDENCE_KIND,
        "applicability_act_occurrence_identity",
    )
    _require_tip(ledger, assignment, "Applicability assignment left the append tip")
    return ledger.append(
        APPLICABILITY_ACT_EVIDENCE_KIND,
        _applicability_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def _read_applicability_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, Event, Event, dict[str, Any], tuple[dict[str, str], ...]]:
    event = ledger.get(event_identity)
    reference = (
        event.material.get("responsibility_assignment_reference")
        if event is not None and type(event.material) is dict
        else None
    )
    assignment_identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    assignment, addressed, coordinate, population = _read_assignment(
        ledger, assignment_identity, prior_standing=prior_standing
    )
    if (
        event is None
        or event.kind != APPLICABILITY_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
        or reference != _assignment_reference(assignment)
        or event.locality_identity != assignment.locality_identity
        or event.material != _applicability_act_material(assignment)
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Applicability Act is absent or inexact"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (assignment.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Applicability Act order is false"
        ) from error
    if tuple(item.identity for item in ordered) != (assignment.identity, event.identity):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Applicability Act order is false"
        )
    return event, assignment, addressed, coordinate, population


def get_addressed_material_coordinate_measurement_applicability_act_evidence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_act(ledger, event_identity)[0].material)


def _applicability_result_material(act: Event, assignment: Event) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["applicability_result_identity"],
        "exact_act": APPLICABILITY_ACT,
        "applicability_act_identity": assignment.material["applicability_act_identity"],
        "applicability_act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "downstream_act_identity": assignment.material["measurement_act_identity"],
        "downstream_act_occurrence_identity": assignment.material[
            "measurement_act_occurrence_identity"
        ],
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "addressed_determination_result_reference": deepcopy(
            assignment.material["addressed_determination_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            assignment.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "direct_pair_position_result_references": deepcopy(
            assignment.material["direct_pair_position_result_references"]
        ),
        "measurement_rule": MEASUREMENT_RULE,
        "applicability_finding": {
            "first_subject": {
                "addressed_determination_result_reference": deepcopy(
                    assignment.material["addressed_determination_result_reference"]
                ),
                "direct_pair_position_result_references": deepcopy(
                    assignment.material["direct_pair_position_result_references"]
                ),
            },
            "relation": "applicable_to",
            "second_subject": {
                "exact_act": MEASUREMENT_ACT,
                "act_identity": assignment.material["measurement_act_identity"],
                "act_occurrence_identity": assignment.material[
                    "measurement_act_occurrence_identity"
                ],
                "result_identity": assignment.material["measurement_result_identity"],
            },
            "responsibility_assignment_reference": _assignment_reference(assignment),
        },
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def _refuse_result(
    ledger: EventLedger, *, act: Event, result_kind: str, occurrence_coordinate: str
) -> None:
    occurrence = act.material[occurrence_coordinate]
    for evidence in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ):
        if (
            evidence.material.get("responsible_act_evidence_identity") == act.identity
            or evidence.material.get("dimensions", {}).get("act_occurrence_identity")
            == occurrence
        ):
            raise AddressedMaterialCoordinateMeasurementError(
                "addressed-material Act already carries a Yield"
            )
    for result in ledger.iter_locality_kind(act.locality_identity, result_kind):
        if (
            result.material.get("responsible_act_evidence_identity") == act.identity
            or result.material.get(occurrence_coordinate) == occurrence
        ):
            raise AddressedMaterialCoordinateMeasurementError(
                "addressed-material Act already carries a result"
            )


def _record_applicability_yield_and_result(
    ledger: EventLedger, *, act: Event, assignment: Event
) -> Event:
    material = _applicability_result_material(act, assignment)
    _refuse_result(
        ledger,
        act=act,
        result_kind=APPLICABILITY_RESULT_KIND,
        occurrence_coordinate="applicability_act_occurrence_identity",
    )
    _require_tip(ledger, act, "Applicability result requires its Act at the append tip")
    evidence = _record_applicability_yield_evidence(
        ledger, act=act, result_material=material
    )
    _require_tip(
        ledger,
        evidence,
        "addressed-material result requires Yield Evidence at the append tip",
    )
    return _append_addressed_material_applicability_result(
        ledger, act=act, assignment=assignment, evidence=evidence
    )


def _record_applicability_yield_evidence(
    ledger: EventLedger, *, act: Event, result_material: dict[str, Any]
) -> Event:
    return _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=act.material["act"],
        act_occurrence_identity=act.material["applicability_act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=APPLICABILITY_RESULT_NAME,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        responsibility=RESPONSIBILITY,
        occurrence_boundary="source_position_coordinates_carrying_addressed_material_applicability",
        responsible_boundary="this Seed",
        responsible_act_occurrence_coordinate="applicability_act_occurrence_identity",
    )


def _append_addressed_material_applicability_result(
    ledger: EventLedger, *, act: Event, assignment: Event, evidence: Event
) -> Event:
    return ledger.append(
        APPLICABILITY_RESULT_KIND,
        {
            **_applicability_result_material(act, assignment),
            "responsible_act_evidence_identity": act.identity,
            "evidence_of_yield_relation_identity": evidence.identity,
        },
        locality_identity=act.locality_identity,
    )


def _record_measurement_yield_and_result(
    ledger: EventLedger,
    *,
    act: Event,
    applicability: Event,
    assignment: Event,
    coordinate: dict[str, Any],
    population: tuple[dict[str, str], ...],
    measured: tuple[MeasuredAddressedMaterialCoordinate, ...],
) -> Event:
    material = _measurement_result_material(
        act=act,
        applicability=applicability,
        assignment=assignment,
        coordinate=coordinate,
        population=population,
        measured=measured,
    )
    _refuse_result(
        ledger,
        act=act,
        result_kind=MEASUREMENT_RESULT_KIND,
        occurrence_coordinate="measurement_act_occurrence_identity",
    )
    _require_tip(ledger, act, "Measurement result requires its Act at the append tip")
    evidence = _record_measurement_yield_evidence(
        ledger, act=act, result_material=material
    )
    _require_tip(
        ledger,
        evidence,
        "addressed-material result requires Yield Evidence at the append tip",
    )
    return _append_addressed_material_measurement_result(
        ledger,
        act=act,
        applicability=applicability,
        assignment=assignment,
        coordinate=coordinate,
        population=population,
        measured=measured,
        evidence=evidence,
    )


def _record_measurement_yield_evidence(
    ledger: EventLedger, *, act: Event, result_material: dict[str, Any]
) -> Event:
    return _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=act.material["act"],
        act_occurrence_identity=act.material["measurement_act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=MEASUREMENT_RESULT_NAME,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        responsibility=RESPONSIBILITY,
        occurrence_boundary="measurement_of_source_position_coordinates_carrying_addressed_material",
        responsible_boundary="this Seed",
        responsible_act_occurrence_coordinate="measurement_act_occurrence_identity",
    )


def _append_addressed_material_measurement_result(
    ledger: EventLedger,
    *,
    act: Event,
    applicability: Event,
    assignment: Event,
    coordinate: dict[str, Any],
    population: tuple[dict[str, str], ...],
    measured: tuple[MeasuredAddressedMaterialCoordinate, ...],
    evidence: Event,
) -> Event:
    return ledger.append(
        MEASUREMENT_RESULT_KIND,
        {
            **_measurement_result_material(
                act=act,
                applicability=applicability,
                assignment=assignment,
                coordinate=coordinate,
                population=population,
                measured=measured,
            ),
            "responsible_act_evidence_identity": act.identity,
            "evidence_of_yield_relation_identity": evidence.identity,
        },
        locality_identity=act.locality_identity,
    )
def record_addressed_material_coordinate_measurement_applicability_result(
    ledger: EventLedger, *, applicability_act_evidence_event_identity: str
) -> Event:
    act, assignment, _addressed, _coordinate, _population = _read_applicability_act(
        ledger, applicability_act_evidence_event_identity
    )
    material = _applicability_result_material(act, assignment)
    _require_tip(ledger, act, "Applicability Act left the append tip")
    return _record_applicability_yield_and_result(
        ledger, act=act, assignment=assignment
    )


def _require_yield(
    ledger: EventLedger,
    *,
    event: Event,
    act: Event,
    occurrence_coordinate: str,
    boundary: str,
    result_name: str,
) -> None:
    evidence_identity = event.material.get("evidence_of_yield_relation_identity")
    evidence = ledger.get(evidence_identity) if type(evidence_identity) is str else None
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=evidence_identity,
            responsible_act_evidence_event_identity=act.identity,
            recorded_result_occurrence_coordinate=occurrence_coordinate,
            responsible_act_occurrence_coordinate=occurrence_coordinate,
        )
    except (TypeError, ValueError):
        requirements = {}
    if (
        evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("occurrence_boundary") != boundary
        or evidence.material.get("result_kind") != result_name
        or not all(requirements.values())
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material result carries no exact Yield"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, evidence.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Yield order is false"
        ) from error
    if tuple(item.identity for item in ordered) != (
        act.identity,
        evidence.identity,
        event.identity,
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Yield order is false"
        )


def _read_applicability_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, Event, Event, Event, dict[str, Any], tuple[dict[str, str], ...]]:
    event = ledger.get(event_identity)
    act_identity = (
        event.material.get("responsible_act_evidence_identity")
        if event is not None and type(event.material) is dict
        else None
    )
    act, assignment, addressed, coordinate, population = _read_applicability_act(
        ledger, act_identity, prior_standing=prior_standing
    )
    expected = {
        **_applicability_result_material(act, assignment),
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": event.material.get(
            "evidence_of_yield_relation_identity"
        ) if event is not None else None,
    }
    if (
        event is None
        or event.kind != APPLICABILITY_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != act.locality_identity
        or event.material != expected
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Applicability result is absent or inexact"
        )
    _require_yield(
        ledger,
        event=event,
        act=act,
        occurrence_coordinate="applicability_act_occurrence_identity",
        boundary=APPLICABILITY_BOUNDARY,
        result_name=APPLICABILITY_RESULT_NAME,
    )
    return event, act, assignment, addressed, coordinate, population


def get_recorded_addressed_material_coordinate_measurement_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_result(ledger, event_identity)[0].material)


def _measurement_act_material(assignment: Event, applicability: Event) -> dict[str, Any]:
    return {
        "measurement_act_identity": assignment.material["measurement_act_identity"],
        "measurement_act_occurrence_identity": assignment.material[
            "measurement_act_occurrence_identity"
        ],
        "act": MEASUREMENT_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_result_reference": _applicability_reference(applicability),
        "addressed_determination_result_reference": deepcopy(
            assignment.material["addressed_determination_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            assignment.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "direct_pair_position_result_references": deepcopy(
            assignment.material["direct_pair_position_result_references"]
        ),
        "measurement_rule": MEASUREMENT_RULE,
        "result_identity": assignment.material["measurement_result_identity"],
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "evidence_scope": "Evidence for this exact Measurement Act occurrence",
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def record_addressed_material_coordinate_measurement_act_evidence(
    ledger: EventLedger,
    *,
    applicability_result_event_identity: str,
    applicability_standing: dict[str, Any],
) -> Event:
    applicability, _app_act, assignment, _addressed, _coordinate, _population = (
        _read_applicability_result(ledger, applicability_result_event_identity)
    )
    _stage_standing(
        ledger,
        standing=applicability_standing,
        assignment=assignment,
        required_tip=applicability,
        require_applicability=True,
    )
    _refuse_act(
        ledger,
        assignment,
        MEASUREMENT_ACT_EVIDENCE_KIND,
        "measurement_act_occurrence_identity",
    )
    _require_tip(ledger, applicability, "Applicability result left the append tip")
    return ledger.append(
        MEASUREMENT_ACT_EVIDENCE_KIND,
        _measurement_act_material(assignment, applicability),
        locality_identity=assignment.locality_identity,
    )


def _read_measurement_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    Event,
    dict[str, Any],
    tuple[dict[str, str], ...],
]:
    event = ledger.get(event_identity)
    applicability_reference = (
        event.material.get("applicability_result_reference")
        if event is not None and type(event.material) is dict
        else None
    )
    applicability_identity = (
        applicability_reference.get("recorded_occurrence_identity")
        if type(applicability_reference) is dict
        else None
    )
    applicability, _app_act, assignment, addressed, coordinate, population = (
        _read_applicability_result(
            ledger, applicability_identity, prior_standing=prior_standing
        )
    )
    if (
        event is None
        or event.kind != MEASUREMENT_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
        or applicability_reference != _applicability_reference(applicability)
        or event.locality_identity != assignment.locality_identity
        or event.material != _measurement_act_material(assignment, applicability)
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement Act is absent or inexact"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (applicability.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement Act order is false"
        ) from error
    if tuple(item.identity for item in ordered) != (applicability.identity, event.identity):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement Act order is false"
        )
    return event, applicability, assignment, addressed, coordinate, population


def get_addressed_material_coordinate_measurement_act_evidence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_measurement_act(ledger, event_identity)[0].material)


def _coordinate_material(item: MeasuredAddressedMaterialCoordinate) -> dict[str, Any]:
    return {
        "direct_pair_position_result_reference": deepcopy(
            item.direct_pair_position_result_reference
        ),
        "pair_position_assertion_reference": deepcopy(
            item.pair_position_assertion_reference
        ),
        "coordinate_role": item.coordinate_role,
        "source_position_coordinate_reference": deepcopy(
            item.source_position_coordinate_reference
        ),
    }


def _measurement_result_material(
    *,
    act: Event,
    applicability: Event,
    assignment: Event,
    coordinate: dict[str, Any],
    population: tuple[dict[str, str], ...],
    measured: tuple[MeasuredAddressedMaterialCoordinate, ...],
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["measurement_result_identity"],
        "exact_act": MEASUREMENT_ACT,
        "measurement_act_identity": assignment.material["measurement_act_identity"],
        "measurement_act_occurrence_identity": assignment.material[
            "measurement_act_occurrence_identity"
        ],
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_result_reference": _applicability_reference(applicability),
        "addressed_determination_result_reference": deepcopy(
            assignment.material["addressed_determination_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(coordinate),
        "direct_pair_position_result_references": deepcopy(list(population)),
        "measurement_rule": MEASUREMENT_RULE,
        "completeness_boundary": {
            "identity": assignment.material["standing_boundary_identity"]
        },
        "ordered_source_position_coordinate_findings": [
            _coordinate_material(item) for item in measured
        ],
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def record_addressed_material_coordinate_measurement_result(
    ledger: EventLedger, *, measurement_act_evidence_event_identity: str
) -> Event:
    act, applicability, assignment, _addressed, coordinate, population = (
        _read_measurement_act(ledger, measurement_act_evidence_event_identity)
    )
    _require_tip(ledger, act, "Measurement result requires its Act at the append tip")
    measured = _measured_coordinates(
        ledger,
        direct_result_references=population,
        addressed_coordinate=coordinate,
        locality_identity=assignment.locality_identity,
    )
    _require_tip(ledger, act, "Measurement source changed before Yield")
    material = _measurement_result_material(
        act=act,
        applicability=applicability,
        assignment=assignment,
        coordinate=coordinate,
        population=population,
        measured=measured,
    )
    return _record_measurement_yield_and_result(
        ledger,
        act=act,
        applicability=applicability,
        assignment=assignment,
        coordinate=coordinate,
        population=population,
        measured=measured,
    )


def _read_measurement_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, tuple[MeasuredAddressedMaterialCoordinate, ...]]:
    event = ledger.get(event_identity)
    act_identity = (
        event.material.get("responsible_act_evidence_identity")
        if event is not None and type(event.material) is dict
        else None
    )
    act, applicability, assignment, _addressed, coordinate, population = (
        _read_measurement_act(ledger, act_identity, prior_standing=prior_standing)
    )
    measured = _measured_coordinates(
        ledger,
        direct_result_references=population,
        addressed_coordinate=coordinate,
        locality_identity=assignment.locality_identity,
    )
    expected = {
        **_measurement_result_material(
            act=act,
            applicability=applicability,
            assignment=assignment,
            coordinate=coordinate,
            population=population,
            measured=measured,
        ),
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": event.material.get(
            "evidence_of_yield_relation_identity"
        ) if event is not None else None,
    }
    if (
        event is None
        or event.kind != MEASUREMENT_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != assignment.locality_identity
        or event.material != expected
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement result is absent or inexact"
        )
    _require_yield(
        ledger,
        event=event,
        act=act,
        occurrence_coordinate="measurement_act_occurrence_identity",
        boundary=MEASUREMENT_BOUNDARY,
        result_name=MEASUREMENT_RESULT_NAME,
    )
    return event, measured


def get_recorded_addressed_material_coordinate_measurement(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_measurement_result(ledger, event_identity)[0].material)


def _carry_produced_occurrence(
    ledger: EventLedger,
    standing: dict[str, Any],
    event: Event,
    *,
    expected_material: dict[str, Any],
    required_prior_identity: str,
) -> dict[str, Any]:
    """Carry one just-produced exact family occurrence without durable replay."""

    from seed_runtime.operator_locality_standing import (
        _exact_standing_additions,
        _record_distinct,
    )

    assignments = standing.get("responsibility_assignment_occurrences")
    applicability = standing.get("applicability_result_occurrences")
    measurements = standing.get("measurement_occurrences")
    prior = standing.get("through_event_occurrence_identity")
    event_count = standing.get("event_count")
    if (
        type(standing) is not dict
        or type(assignments) is not dict
        or type(applicability) is not dict
        or type(measurements) is not dict
        or type(event_count) is not int
        or prior != required_prior_identity
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != standing.get("locality_identity")
        or event.material != expected_material
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "produced addressed-material occurrence is not exact"
        )
    if event.kind == RESPONSIBILITY_ASSIGNMENT_KIND:
        lawful = (
            event.material.get("standing_boundary_identity") == prior
            and event.identity not in assignments
        )
    elif event.kind == APPLICABILITY_ACT_EVIDENCE_KIND:
        assignment_identity = event.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
        lawful = assignment_identity == prior and assignment_identity in assignments
    elif event.kind == APPLICABILITY_RESULT_KIND:
        assignment_identity = event.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
        lawful = (
            event.material.get("responsible_act_evidence_identity") == prior
            and assignment_identity in assignments
            and event.identity not in applicability
        )
    elif event.kind == MEASUREMENT_ACT_EVIDENCE_KIND:
        applicability_identity = event.material["applicability_result_reference"][
            "recorded_occurrence_identity"
        ]
        assignment_identity = event.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
        lawful = (
            applicability_identity == prior
            and applicability_identity in applicability
            and assignment_identity in assignments
        )
    elif event.kind == MEASUREMENT_RESULT_KIND:
        applicability_identity = event.material["applicability_result_reference"][
            "recorded_occurrence_identity"
        ]
        assignment_identity = event.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
        lawful = (
            event.material.get("responsible_act_evidence_identity") == prior
            and applicability_identity in applicability
            and assignment_identity in assignments
            and event.identity not in measurements
        )
    else:
        lawful = False
    if not lawful:
        raise AddressedMaterialCoordinateMeasurementError(
            "produced addressed-material occurrence has false Standing"
        )
    additions = _exact_standing_additions(
        standing,
        event,
        error_message="produced addressed-material Standing is not exact",
    )
    if event.kind == RESPONSIBILITY_ASSIGNMENT_KIND:
        assignments[event.identity] = None
    elif event.kind == APPLICABILITY_RESULT_KIND:
        applicability[event.identity] = None
    elif event.kind == MEASUREMENT_RESULT_KIND:
        measurements[event.identity] = measurement_result_reference(event)
    for key, added in additions.items():
        for value in added:
            _record_distinct(standing[key], value)
    standing["through_event_occurrence_identity"] = event.identity
    standing["event_count"] = event_count + 1
    return standing


def _record_addressed_material_coordinate_measurement_lifecycle_from_carried_standing(
    ledger: EventLedger,
    *,
    addressed_determination_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> tuple[dict[str, Any], Event]:
    """Produce and carry one exact lifecycle from one validated Standing pin."""

    boundary = locality_standing.get("through_event_occurrence_identity")
    working_standing = deepcopy(locality_standing)
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    locality_events = (
        ledger.list_locality(locality_standing.get("locality_identity"))
        if boundary_event is not None
        else ()
    )
    if (
        boundary_event is None
        or not locality_events
        or locality_events[-1].identity != boundary_event.identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement requires exact current Locality Standing"
        )
    initial_global_boundary = ledger.append_boundary()
    addressed, coordinate, population = _standing_source(
        ledger,
        standing=locality_standing,
        addressed_result_identity=addressed_determination_result_event_identity,
        required_boundary_identity=boundary,
    )
    addressed_material_snapshot = deepcopy(addressed.material)
    source_material_snapshots = {
        reference["recorded_occurrence_identity"]: deepcopy(
            ledger.get(reference["recorded_occurrence_identity"]).material
        )
        for reference in population
    }
    measured = _measured_coordinates(
        ledger,
        direct_result_references=population,
        addressed_coordinate=coordinate,
        locality_identity=addressed.locality_identity,
    )
    for identity, material_snapshot in source_material_snapshots.items():
        source_event = ledger.get(identity)
        if (
            source_event is None
            or source_event.material != material_snapshot
            or ledger.integrity_of(identity) == CORRUPTED
        ):
            raise AddressedMaterialCoordinateMeasurementError(
                "addressed-material Measurement source changed during derivation"
            )
    if addressed.material != addressed_material_snapshot:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material addressed result changed during derivation"
        )
    assignment = _append_assignment(
        ledger,
        standing=locality_standing,
        addressed_result=addressed,
        addressed_coordinate=coordinate,
        population=population,
        expected_global_boundary=initial_global_boundary,
    )
    assignment_material_snapshot = deepcopy(assignment.material)
    standing = _carry_produced_occurrence(
        ledger,
        working_standing,
        assignment,
        expected_material=assignment_material_snapshot,
        required_prior_identity=boundary,
    )
    applicability_act_material = _applicability_act_material(assignment)
    applicability_act = ledger.append(
        APPLICABILITY_ACT_EVIDENCE_KIND,
        _applicability_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )
    standing = _carry_produced_occurrence(
        ledger,
        standing,
        applicability_act,
        expected_material=applicability_act_material,
        required_prior_identity=assignment.identity,
    )
    applicability_material = _applicability_result_material(
        applicability_act, assignment
    )
    applicability_result = _record_applicability_yield_and_result(
        ledger, act=applicability_act, assignment=assignment
    )
    standing = _carry_produced_occurrence(
        ledger,
        standing,
        applicability_result,
        expected_material={
            **applicability_material,
            "responsible_act_evidence_identity": applicability_act.identity,
            "evidence_of_yield_relation_identity": applicability_result.material[
                "evidence_of_yield_relation_identity"
            ],
        },
        required_prior_identity=applicability_act.identity,
    )
    measurement_act_material = _measurement_act_material(
        assignment, applicability_result
    )
    measurement_act = ledger.append(
        MEASUREMENT_ACT_EVIDENCE_KIND,
        _measurement_act_material(assignment, applicability_result),
        locality_identity=assignment.locality_identity,
    )
    standing = _carry_produced_occurrence(
        ledger,
        standing,
        measurement_act,
        expected_material=measurement_act_material,
        required_prior_identity=applicability_result.identity,
    )
    if (
        ledger.get(addressed.identity) is None
        or ledger.get(addressed.identity).material != addressed_material_snapshot
        or ledger.integrity_of(addressed.identity) == CORRUPTED
        or any(
            ledger.get(identity) is None
            or ledger.get(identity).material != material_snapshot
            or ledger.integrity_of(identity) == CORRUPTED
            for identity, material_snapshot in source_material_snapshots.items()
        )
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement source changed before Yield"
        )
    result_material = _measurement_result_material(
        act=measurement_act,
        applicability=applicability_result,
        assignment=assignment,
        coordinate=coordinate,
        population=population,
        measured=measured,
    )
    result = _record_measurement_yield_and_result(
        ledger,
        act=measurement_act,
        applicability=applicability_result,
        assignment=assignment,
        coordinate=coordinate,
        population=population,
        measured=measured,
    )
    standing = _carry_produced_occurrence(
        ledger,
        standing,
        result,
        expected_material={
            **result_material,
            "responsible_act_evidence_identity": measurement_act.identity,
            "evidence_of_yield_relation_identity": result.material[
                "evidence_of_yield_relation_identity"
            ],
        },
        required_prior_identity=measurement_act.identity,
    )
    return standing, result


def _events_for_addressed_material_assignment(
    ledger: EventLedger,
    *,
    assignment: Event,
    kind: str,
) -> tuple[Event, ...]:
    events = []
    for event in ledger.iter_locality_kind(assignment.locality_identity, kind):
        reference = event.material.get("responsibility_assignment_reference")
        if (
            type(reference) is dict
            and reference.get("recorded_occurrence_identity") == assignment.identity
        ):
            if ledger.integrity_of(event.identity) == CORRUPTED:
                raise AddressedMaterialCoordinateMeasurementError(
                    "addressed-material partial lifecycle is corrupted"
                )
            events.append(event)
    if len(events) > 1:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material partial lifecycle is ambiguous"
        )
    return tuple(events)


def _addressed_material_yield_for_act(
    ledger: EventLedger,
    *,
    act: Event,
) -> Event | None:
    events = []
    for event in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ):
        if event.material.get("responsible_act_evidence_identity") == act.identity:
            if ledger.integrity_of(event.identity) == CORRUPTED:
                raise AddressedMaterialCoordinateMeasurementError(
                    "addressed-material partial Yield is corrupted"
                )
            events.append(event)
    if len(events) > 1:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material partial Yield is ambiguous"
        )
    return events[0] if events else None


def _require_addressed_material_partial_yield(
    ledger: EventLedger,
    *,
    evidence: Event,
    act: Event,
    result_material: dict[str, Any],
    result_kind: str,
    result_name: str,
    occurrence_boundary: str,
    act_occurrence_coordinate: str,
) -> None:
    expected = {
        "responsible_act_evidence_identity": act.identity,
        "result_identity": result_material["result_identity"],
        "dimensions": {
            "identity": (
                f"yield-evidence:{act.material[act_occurrence_coordinate]}:"
                f"{result_material['result_identity']}"
            ),
            "exact_act": act.material["act"],
            "act_occurrence_identity": act.material[act_occurrence_coordinate],
            "responsibility": RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": "unestablished",
        },
        "coordinates_of_carried_result": list(result_material),
        "result": deepcopy(result_material),
        "coordinates_of_recorded_result": {
            coordinate: [coordinate] for coordinate in result_material
        },
        "result_kind": result_name,
        "occurrence_boundary": occurrence_boundary,
    }
    if (
        evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or evidence.exact_material is not None
        or evidence.locality_identity != act.locality_identity
        or evidence.material != expected
        or ledger.get(evidence.identity) != evidence
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or not ledger.list_locality(act.locality_identity)
        or ledger.list_locality(act.locality_identity)[-1].identity
        != evidence.identity
        or any(
            event.material.get("responsible_act_evidence_identity") == act.identity
            for event in ledger.iter_locality_kind(act.locality_identity, result_kind)
        )
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material partial Yield cannot be continued"
        )


def _addressed_material_continuation_write_snapshot(
    ledger: EventLedger, *, prior: Event
) -> tuple[Any, int]:
    locality_events = ledger.list_locality(prior.locality_identity)
    if (
        ledger.get(prior.identity) != prior
        or ledger.integrity_of(prior.identity) == CORRUPTED
        or not locality_events
        or locality_events[-1].identity != prior.identity
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material continuation prior phase is not Locality-current"
        )
    return ledger.append_boundary(), len(ledger.list())


def _require_addressed_material_serialized_append(
    ledger: EventLedger,
    *,
    snapshot: tuple[Any, int],
    event: Event,
) -> None:
    _boundary, count = snapshot
    events = ledger.list()
    if (
        len(events) != count + 1
        or events[-1] != event
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material continuation write was not globally serialized"
        )


def _continue_addressed_material_coordinate_measurement_lifecycle(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    locality_standing: dict[str, Any],
) -> tuple[dict[str, Any], Event]:
    """Continue one exact intact recorded lifecycle prefix after reopen."""

    from seed_runtime.operator_locality_standing import (
        advance_operator_locality_standing,
    )

    assignment, _addressed, coordinate, population = _read_assignment(
        ledger, responsibility_assignment_event_identity
    )
    if (
        locality_standing.get("locality_identity") != assignment.locality_identity
        or assignment.identity
        not in locality_standing.get("responsibility_assignment_occurrences", {})
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material continuation requires its exact current Standing"
        )

    def advance(standing: dict[str, Any], event: Event) -> dict[str, Any]:
        return advance_operator_locality_standing(
            ledger,
            (event.identity,),
            locality_identity=assignment.locality_identity,
            prior=standing,
        )

    applicability_acts = _events_for_addressed_material_assignment(
        ledger, assignment=assignment, kind=APPLICABILITY_ACT_EVIDENCE_KIND
    )
    applicability_results = _events_for_addressed_material_assignment(
        ledger, assignment=assignment, kind=APPLICABILITY_RESULT_KIND
    )
    measurement_acts = _events_for_addressed_material_assignment(
        ledger, assignment=assignment, kind=MEASUREMENT_ACT_EVIDENCE_KIND
    )
    measurement_results = _events_for_addressed_material_assignment(
        ledger, assignment=assignment, kind=MEASUREMENT_RESULT_KIND
    )
    if measurement_results:
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material lifecycle is already complete"
        )
    if (
        (applicability_results and not applicability_acts)
        or (measurement_acts and not applicability_results)
    ):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material partial lifecycle order is false"
        )

    if applicability_acts:
        applicability_act = applicability_acts[0]
        _read_applicability_act(ledger, applicability_act.identity)
    else:
        _refuse_act(
            ledger,
            assignment,
            APPLICABILITY_ACT_EVIDENCE_KIND,
            "applicability_act_occurrence_identity",
        )
        snapshot = _addressed_material_continuation_write_snapshot(
            ledger, prior=assignment
        )
        applicability_act = ledger.append(
            APPLICABILITY_ACT_EVIDENCE_KIND,
            _applicability_act_material(assignment),
            locality_identity=assignment.locality_identity,
        )
        _require_addressed_material_serialized_append(
            ledger, snapshot=snapshot, event=applicability_act
        )
        locality_standing = advance(locality_standing, applicability_act)

    if applicability_results:
        applicability = applicability_results[0]
        _read_applicability_result(ledger, applicability.identity)
    else:
        applicability_material = _applicability_result_material(
            applicability_act, assignment
        )
        applicability_yield = _addressed_material_yield_for_act(
            ledger, act=applicability_act
        )
        if applicability_yield is None:
            _refuse_result(
                ledger,
                act=applicability_act,
                result_kind=APPLICABILITY_RESULT_KIND,
                occurrence_coordinate="applicability_act_occurrence_identity",
            )
            snapshot = _addressed_material_continuation_write_snapshot(
                ledger, prior=applicability_act
            )
            applicability_yield = _record_applicability_yield_evidence(
                ledger,
                act=applicability_act,
                result_material=applicability_material,
            )
            _require_addressed_material_serialized_append(
                ledger, snapshot=snapshot, event=applicability_yield
            )
            snapshot = _addressed_material_continuation_write_snapshot(
                ledger, prior=applicability_yield
            )
            applicability = _append_addressed_material_applicability_result(
                ledger,
                act=applicability_act,
                assignment=assignment,
                evidence=applicability_yield,
            )
            _require_addressed_material_serialized_append(
                ledger, snapshot=snapshot, event=applicability
            )
        else:
            _require_addressed_material_partial_yield(
                ledger,
                evidence=applicability_yield,
                act=applicability_act,
                result_material=applicability_material,
                result_kind=APPLICABILITY_RESULT_KIND,
                result_name=APPLICABILITY_RESULT_NAME,
                occurrence_boundary=APPLICABILITY_BOUNDARY,
                act_occurrence_coordinate="applicability_act_occurrence_identity",
            )
            snapshot = _addressed_material_continuation_write_snapshot(
                ledger, prior=applicability_yield
            )
            applicability = _append_addressed_material_applicability_result(
                ledger,
                act=applicability_act,
                assignment=assignment,
                evidence=applicability_yield,
            )
            _require_addressed_material_serialized_append(
                ledger, snapshot=snapshot, event=applicability
            )
        locality_standing = advance(locality_standing, applicability)

    if measurement_acts:
        measurement_act = measurement_acts[0]
        _read_measurement_act(ledger, measurement_act.identity)
    else:
        _refuse_act(
            ledger,
            assignment,
            MEASUREMENT_ACT_EVIDENCE_KIND,
            "measurement_act_occurrence_identity",
        )
        snapshot = _addressed_material_continuation_write_snapshot(
            ledger, prior=applicability
        )
        measurement_act = ledger.append(
            MEASUREMENT_ACT_EVIDENCE_KIND,
            _measurement_act_material(assignment, applicability),
            locality_identity=assignment.locality_identity,
        )
        _require_addressed_material_serialized_append(
            ledger, snapshot=snapshot, event=measurement_act
        )
        locality_standing = advance(locality_standing, measurement_act)

    measured = _measured_coordinates(
        ledger,
        direct_result_references=population,
        addressed_coordinate=coordinate,
        locality_identity=assignment.locality_identity,
    )
    result_material = _measurement_result_material(
        act=measurement_act,
        applicability=applicability,
        assignment=assignment,
        coordinate=coordinate,
        population=population,
        measured=measured,
    )
    measurement_yield = _addressed_material_yield_for_act(
        ledger, act=measurement_act
    )
    if measurement_yield is None:
        _refuse_result(
            ledger,
            act=measurement_act,
            result_kind=MEASUREMENT_RESULT_KIND,
            occurrence_coordinate="measurement_act_occurrence_identity",
        )
        snapshot = _addressed_material_continuation_write_snapshot(
            ledger, prior=measurement_act
        )
        measurement_yield = _record_measurement_yield_evidence(
            ledger,
            act=measurement_act,
            result_material=result_material,
        )
        _require_addressed_material_serialized_append(
            ledger, snapshot=snapshot, event=measurement_yield
        )
        snapshot = _addressed_material_continuation_write_snapshot(
            ledger, prior=measurement_yield
        )
        result = _append_addressed_material_measurement_result(
            ledger,
            act=measurement_act,
            applicability=applicability,
            assignment=assignment,
            coordinate=coordinate,
            population=population,
            measured=measured,
            evidence=measurement_yield,
        )
        _require_addressed_material_serialized_append(
            ledger, snapshot=snapshot, event=result
        )
    else:
        _require_addressed_material_partial_yield(
            ledger,
            evidence=measurement_yield,
            act=measurement_act,
            result_material=result_material,
            result_kind=MEASUREMENT_RESULT_KIND,
            result_name=MEASUREMENT_RESULT_NAME,
            occurrence_boundary=MEASUREMENT_BOUNDARY,
            act_occurrence_coordinate="measurement_act_occurrence_identity",
        )
        snapshot = _addressed_material_continuation_write_snapshot(
            ledger, prior=measurement_yield
        )
        result = _append_addressed_material_measurement_result(
            ledger,
            act=measurement_act,
            applicability=applicability,
            assignment=assignment,
            coordinate=coordinate,
            population=population,
            measured=measured,
            evidence=measurement_yield,
        )
        _require_addressed_material_serialized_append(
            ledger, snapshot=snapshot, event=result
        )
    locality_standing = advance(locality_standing, result)
    return locality_standing, result


def _subject_is_unmeasured(
    ledger: EventLedger,
    *,
    locality_identity: str,
    addressed_result_identity: str,
    population: tuple[dict[str, str], ...],
) -> bool:
    key = (
        addressed_result_identity,
        tuple(item["recorded_occurrence_identity"] for item in population),
    )
    for kind in (RESPONSIBILITY_ASSIGNMENT_KIND, MEASUREMENT_RESULT_KIND):
        for event in ledger.iter_locality_kind(locality_identity, kind):
            if ledger.integrity_of(event.identity) == CORRUPTED:
                raise AddressedMaterialCoordinateMeasurementError(
                    "addressed-material Measurement history is corrupted"
                )
            if _subject_key(event.material) == key:
                return False
    return True


def _incomplete_assignment_for_subject(
    ledger: EventLedger,
    *,
    locality_identity: str,
    addressed_result_identity: str,
    population: tuple[dict[str, str], ...],
) -> Event | None:
    key = (
        addressed_result_identity,
        tuple(item["recorded_occurrence_identity"] for item in population),
    )
    assignments = []
    for event in ledger.iter_locality_kind(
        locality_identity, RESPONSIBILITY_ASSIGNMENT_KIND
    ):
        if ledger.integrity_of(event.identity) == CORRUPTED:
            raise AddressedMaterialCoordinateMeasurementError(
                "addressed-material Measurement history is corrupted"
            )
        if _subject_key(event.material) == key:
            assignments.append(event)
    results = []
    for event in ledger.iter_locality_kind(locality_identity, MEASUREMENT_RESULT_KIND):
        if ledger.integrity_of(event.identity) == CORRUPTED:
            raise AddressedMaterialCoordinateMeasurementError(
                "addressed-material Measurement history is corrupted"
            )
        if _subject_key(event.material) == key:
            results.append(event)
    if len(assignments) > 1 or len(results) > 1 or (results and not assignments):
        raise AddressedMaterialCoordinateMeasurementError(
            "addressed-material Measurement history is ambiguous"
        )
    return assignments[0] if assignments and not results else None
