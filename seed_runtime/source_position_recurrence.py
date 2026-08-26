"""Measure recurrence across consecutive source positions and carried material.

This is the smallest live proof of two separate declared Measurements:

* recurrence of all same-content/difference findings for consecutive source
  positions;
* material recurrence at corresponding exact source positions across the
  exact source-position results carried by the first recurrence result.

The public producer begins with all complete adjacent coordinates and records
another source coordinate only while exact recurrent results make that
coordinate addressable. No caller chooses the final coordinate count. Each Act
has an exact preceding subject-to-Act binding. The later Measurement accepts
the complete recurrence result, not a selected recurrence finding, source
position, or value. The explicit call from the recurrence result to that
Measurement remains visible: this module does not claim a general result-uptake
dispatcher.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Iterator, NamedTuple

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.yield_relation import (
    _record_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    source_position_coordinate_references_of_recorded_position_measurement,
)


COMPARE_APPLICABILITY_ACT_KIND = (
    "operator.source_position_compare.applicability_act_recorded"
)
COMPARE_APPLICABILITY_RESULT_KIND = (
    "operator.source_position_compare.applicability_result_recorded"
)
COMPARE_ACT_KIND = "operator.source_position_compare.act_recorded"
COMPARE_RESULT_KIND = "operator.source_position_compare.result_recorded"
SOURCE_POSITION_MEASUREMENT_ACT_KIND = "operator.source_position.measurement_act_recorded"
SOURCE_POSITION_MEASUREMENT_RESULT_KIND = "operator.source_position.measurement_result_recorded"
RECURRENCE_MEASUREMENT_ACT_KIND = (
    "operator.source_position_recurrence.measurement_act_recorded"
)
RECURRENCE_MEASUREMENT_RESULT_KIND = (
    "operator.source_position_recurrence.measurement_result_recorded"
)
COORDINATE_MEASUREMENT_ACT_KIND = (
    "operator.recurrence_corresponding_source_position_material.measurement_act_recorded"
)
COORDINATE_MEASUREMENT_RESULT_KIND = (
    "operator.recurrence_corresponding_source_position_material.measurement_result_recorded"
)
RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT_KIND = (
    "operator.recurrent_result_exact_material.measurement_act_recorded"
)
RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESULT_KIND = (
    "operator.recurrent_result_exact_material.measurement_result_recorded"
)

COMPARE_APPLICABILITY_RESPONSIBILITY_KIND = (
    "operator.source_position_compare.applicability_responsibility_recorded"
)
COMPARE_RESPONSIBILITY_KIND = (
    "operator.source_position_compare.responsibility_recorded"
)
SOURCE_POSITION_MEASUREMENT_RESPONSIBILITY_KIND = (
    "operator.source_position.measurement_responsibility_recorded"
)
RECURRENCE_MEASUREMENT_RESPONSIBILITY_KIND = (
    "operator.source_position_recurrence.measurement_responsibility_recorded"
)
COORDINATE_MEASUREMENT_RESPONSIBILITY_KIND = (
    "operator.recurrence_corresponding_source_position_material."
    "measurement_responsibility_recorded"
)
RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESPONSIBILITY_KIND = (
    "operator.recurrent_result_exact_material.measurement_responsibility_recorded"
)

EVENT_KIND_RESPONSIBILITIES = {
    COMPARE_APPLICABILITY_ACT_KIND: "02.Acts.A",
    COMPARE_APPLICABILITY_RESULT_KIND: "01.Current.E.1",
    COMPARE_ACT_KIND: "02.Acts.A",
    COMPARE_RESULT_KIND: "04.Compare",
    SOURCE_POSITION_MEASUREMENT_ACT_KIND: "02.Acts.A",
    SOURCE_POSITION_MEASUREMENT_RESULT_KIND: "01.Source.D",
    RECURRENCE_MEASUREMENT_ACT_KIND: "02.Acts.A",
    RECURRENCE_MEASUREMENT_RESULT_KIND: "01.Source.D",
    COORDINATE_MEASUREMENT_ACT_KIND: "02.Acts.A",
    COORDINATE_MEASUREMENT_RESULT_KIND: "01.Source.D",
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT_KIND: "02.Acts.A",
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESULT_KIND: "01.Source.D",
}

_ACT_RESPONSIBILITY_KINDS = {
    COMPARE_APPLICABILITY_ACT_KIND: COMPARE_APPLICABILITY_RESPONSIBILITY_KIND,
    COMPARE_ACT_KIND: COMPARE_RESPONSIBILITY_KIND,
    SOURCE_POSITION_MEASUREMENT_ACT_KIND: SOURCE_POSITION_MEASUREMENT_RESPONSIBILITY_KIND,
    RECURRENCE_MEASUREMENT_ACT_KIND: RECURRENCE_MEASUREMENT_RESPONSIBILITY_KIND,
    COORDINATE_MEASUREMENT_ACT_KIND: COORDINATE_MEASUREMENT_RESPONSIBILITY_KIND,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT_KIND: (
        RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESPONSIBILITY_KIND
    ),
}
COMPARE_APPLICABILITY_ACT = (
    "Applicability of exact source-position coordinates to Compare"
)
COMPARE_APPLICABILITY_RULE = (
    "the exact carried source-position coordinates address this exact Compare Act"
)
COMPARE_ACT = "Compare exact material at two exact source positions"
COMPARE_RULE = (
    "same-content exactly when the two exact source-position materials are equal; "
    "difference otherwise"
)
SOURCE_POSITION_MEASUREMENT_ACT = "Measure the complete Compare result"
SOURCE_POSITION_MEASUREMENT_RULE = (
    "preserve one Compare result for every distinct pair of exact consecutive "
    "source positions carried by the subject"
)
RECURRENCE_MEASUREMENT_ACT = (
    "Measure recurrence of complete internal Compare results"
)
RECURRENCE_MEASUREMENT_RULE = (
    "group exact source-position results only when their complete Compare findings "
    "are equal; recurrence requires more than one exact result"
)
COORDINATE_MEASUREMENT_ACT = (
    "Measure corresponding carried material across exact recurrence support results"
)
COORDINATE_MEASUREMENT_RULE = (
    "measure the exact material at each corresponding source position carried by "
    "every exact result of one recurrence finding"
)
RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT = (
    "Measure exact material shared by every exact recurrent result"
)
RECURRENT_RESULT_MATERIAL_MEASUREMENT_RULE = (
    "one exact material at every corresponding source position across exactly the same "
    "results, each carrying consecutive source positions"
)

_EXACT_ACT_RULES = {
    COMPARE_APPLICABILITY_ACT: COMPARE_APPLICABILITY_RULE,
    COMPARE_ACT: COMPARE_RULE,
    SOURCE_POSITION_MEASUREMENT_ACT: SOURCE_POSITION_MEASUREMENT_RULE,
    RECURRENCE_MEASUREMENT_ACT: RECURRENCE_MEASUREMENT_RULE,
    COORDINATE_MEASUREMENT_ACT: COORDINATE_MEASUREMENT_RULE,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT: (
        RECURRENT_RESULT_MATERIAL_MEASUREMENT_RULE
    ),
}

COMPARE_APPLICABILITY_BOUNDARY = "source_position_compare_applicability"
COMPARE_BOUNDARY = "source_position_compare"
SOURCE_POSITION_MEASUREMENT_BOUNDARY = "source_position_measurement"
RECURRENCE_MEASUREMENT_BOUNDARY = "source_position_recurrence_measurement"
COORDINATE_MEASUREMENT_BOUNDARY = (
    "recurrence_corresponding_source_position_material_measurement"
)
RECURRENT_RESULT_MATERIAL_MEASUREMENT_BOUNDARY = (
    "recurrent_result_exact_material_measurement"
)


class SourcePositionMeasurementStep(NamedTuple):
    coordinate_count: int
    source_position_result_occurrences: tuple[Event, ...]
    recurrence_result_occurrence: Event
    new_event_count: int


class SourcePositionMeasurements(NamedTuple):
    direct_result_event_identity: str
    steps: tuple[SourcePositionMeasurementStep, ...]
    exhausted: bool
    current_coordinates: dict[str, Any]


class CorrespondingCoordinateMeasurement(NamedTuple):
    recurrence_finding_reference: str
    result_occurrence: Event


class CorrespondingCoordinateMeasurements(NamedTuple):
    measurements: tuple[CorrespondingCoordinateMeasurement, ...]
    current_coordinates: dict[str, Any]


class RecurrentResultMaterialMeasurement(NamedTuple):
    recurrence_finding_reference: str
    result_occurrence: Event


class RecurrentResultMaterialMeasurements(NamedTuple):
    measurements: tuple[RecurrentResultMaterialMeasurement, ...]
    current_coordinates: dict[str, Any]


def _exact_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _digest(prefix: str, value: Any) -> str:
    return prefix + ":" + hashlib.sha256(_exact_json(value).encode("utf-8")).hexdigest()


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(message)
    return value


def _recorded_occurrence(ledger: EventLedger, identity: Any, *, message: str) -> Event:
    event = ledger.get(_identity(identity, message))
    if (
        event is None
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError(message)
    return event


def _result_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_reference": event.identity,
        "result_reference": event.material["result_identity"],
    }


def _coordinates(material: dict[str, Any]) -> dict[str, Any]:
    coordinates = material.get("coordinates")
    if type(coordinates) is not dict:
        raise ValueError("source-position occurrence carries no exact coordinates")
    return coordinates


def _require_preserved_result(
    ledger: EventLedger,
    result: Event,
    *,
    exact_act: str,
    occurrence_boundary: str,
) -> tuple[Event, dict[str, Any]]:
    """Read one exact produced result without replaying its input history."""

    act = _require_yield(
        ledger,
        result,
        exact_act=exact_act,
        occurrence_boundary=occurrence_boundary,
    )
    coordinates = deepcopy(_coordinates(result.material))
    if _coordinates(act.material).get("subject") != coordinates:
        raise ValueError("recorded result does not preserve its exact Act subject")
    return act, {**deepcopy(result.material), **coordinates}


def _require_coordinate(coordinate: Any, *, locality_identity: str) -> dict[str, Any]:
    keys = {
        "source_material_result_occurrence_identity",
        "locality_identity",
        "completeness_boundary_identity",
        "position",
        "exact_material",
    }
    if (
        type(coordinate) is not dict
        or set(coordinate) != keys
        or type(coordinate.get("source_material_result_occurrence_identity"))
        is not str
        or not coordinate["source_material_result_occurrence_identity"]
        or coordinate.get("locality_identity") != locality_identity
        or type(coordinate.get("completeness_boundary_identity")) is not str
        or not coordinate["completeness_boundary_identity"]
        or type(coordinate.get("position")) is not int
        or coordinate["position"] < 0
        or type(coordinate.get("exact_material")) is not list
        or len(coordinate["exact_material"]) != 1
        or type(coordinate["exact_material"][0]) is not int
        or not 0 <= coordinate["exact_material"][0] <= 255
    ):
        raise ValueError("source-position requires an exact source coordinate")
    return coordinate


def _direct_coordinates(
    ledger: EventLedger,
    direct_result_event_identity: str,
    *,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> tuple[dict[str, Any], ...]:
    cache_key = ("direct_coordinates", direct_result_event_identity)
    if _validated is not None and cache_key in _validated:
        return _validated[cache_key]
    coordinates = tuple(
        source_position_coordinate_references_of_recorded_position_measurement(
            ledger, direct_result_event_identity
        )
    )
    if len(coordinates) < 2:
        raise ValueError("source-position requires at least two source coordinates")
    locality_identity = coordinates[0]["locality_identity"]
    source_identity = coordinates[0][
        "source_material_result_occurrence_identity"
    ]
    completeness_boundary = coordinates[0]["completeness_boundary_identity"]
    for position, coordinate in enumerate(coordinates):
        _require_coordinate(coordinate, locality_identity=locality_identity)
        if (
            coordinate["position"] != position
            or coordinate["source_material_result_occurrence_identity"]
            != source_identity
            or coordinate["completeness_boundary_identity"]
            != completeness_boundary
        ):
            raise ValueError("direct result carries no exact source positions")
    if _validated is not None:
        _validated[cache_key] = coordinates
    return coordinates


def _preserved_act_material(material):
    return {
        "book_reference": material["book_reference"],
        "result_identity": material["result_identity"],
        "act_identity": material["act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "responsibility_assignment_reference": deepcopy(
            material["responsibility_assignment_reference"]
        ),
        "act": material["act"],
        "coordinates": deepcopy(material["coordinates"]),
    }


def _preserved_result_material(material):
    return {
        "book_reference": material["book_reference"],
        "result_identity": material["result_identity"],
        "act_identity": material["act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act_occurrence_event_identity": material[
            "act_occurrence_event_identity"
        ],
        "coordinates": deepcopy(material["coordinates"]),
        "yield_relation_identity": material[
            "yield_relation_identity"
        ],
    }


def _preserved_responsibility_material(material):
    return {
        "book_clause_identity": material["book_clause_identity"],
        "result_boundary_identity": material["result_boundary_identity"],
        "through_event_occurrence_identity": material[
            "through_event_occurrence_identity"
        ],
        "exact_act_identity": material["act_identity"],
        "act_identity": material["act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": material["exact_act"],
        "rule": material["rule"],
        "subject": deepcopy(material["subject"]),
        "subject_reference": deepcopy(material["subject"]),
        "scope": deepcopy(material["scope"]),
        "conflicts": deepcopy(material["conflicts"]),
        "unknown": deepcopy(material["unknown"]),
    }


def _append_responsibility(ledger, label, material, locality_identity):
    return ledger.append(
        label,
        _preserved_responsibility_material(material),
        locality_identity=locality_identity,
    )


def _append_compare_applicability_act(ledger, material, locality_identity):
    return ledger.append(
        COMPARE_APPLICABILITY_ACT_KIND,
        _preserved_act_material(material),
        locality_identity=locality_identity,
    )


def _append_compare_applicability_result(ledger, material, locality_identity):
    return ledger.append(
        COMPARE_APPLICABILITY_RESULT_KIND,
        _preserved_result_material(material),
        locality_identity=locality_identity,
    )


def _append_compare_act(ledger, material, locality_identity):
    return ledger.append(
        COMPARE_ACT_KIND,
        _preserved_act_material(material),
        locality_identity=locality_identity,
    )


def _append_compare_result(ledger, material, locality_identity):
    return ledger.append(
        COMPARE_RESULT_KIND,
        _preserved_result_material(material),
        locality_identity=locality_identity,
    )


def _append_source_position_measurement_act(ledger, material, locality_identity):
    return ledger.append(
        SOURCE_POSITION_MEASUREMENT_ACT_KIND,
        _preserved_act_material(material),
        locality_identity=locality_identity,
    )


def _append_source_position_measurement_result(ledger, material, locality_identity):
    return ledger.append(
        SOURCE_POSITION_MEASUREMENT_RESULT_KIND,
        _preserved_result_material(material),
        locality_identity=locality_identity,
    )


def _append_recurrence_measurement_act(ledger, material, locality_identity):
    return ledger.append(
        RECURRENCE_MEASUREMENT_ACT_KIND,
        _preserved_act_material(material),
        locality_identity=locality_identity,
    )


def _append_recurrence_measurement_result(ledger, material, locality_identity):
    return ledger.append(
        RECURRENCE_MEASUREMENT_RESULT_KIND,
        _preserved_result_material(material),
        locality_identity=locality_identity,
    )


def _append_coordinate_measurement_act(ledger, material, locality_identity):
    return ledger.append(
        COORDINATE_MEASUREMENT_ACT_KIND,
        _preserved_act_material(material),
        locality_identity=locality_identity,
    )


def _append_coordinate_measurement_result(ledger, material, locality_identity):
    return ledger.append(
        COORDINATE_MEASUREMENT_RESULT_KIND,
        _preserved_result_material(material),
        locality_identity=locality_identity,
    )


def _append_recurrent_result_material_measurement_act(ledger, material, locality_identity):
    return ledger.append(
        RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT_KIND,
        _preserved_act_material(material),
        locality_identity=locality_identity,
    )


def _append_recurrent_result_material_measurement_result(
    ledger, material, locality_identity
):
    exact_material = material.get("coordinates", {}).get("exact_material")
    if (
        type(exact_material) is not list
        or any(type(value) is not int or not 0 <= value <= 255 for value in exact_material)
    ):
        raise ValueError("exact-material Measurement requires exact material")
    return ledger.append(
        RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESULT_KIND,
        _preserved_result_material(material),
        exact_material=bytes(exact_material),
        locality_identity=locality_identity,
    )


_EVENT_APPENDERS = {
    COMPARE_APPLICABILITY_ACT_KIND: _append_compare_applicability_act,
    COMPARE_APPLICABILITY_RESULT_KIND: _append_compare_applicability_result,
    COMPARE_ACT_KIND: _append_compare_act,
    COMPARE_RESULT_KIND: _append_compare_result,
    SOURCE_POSITION_MEASUREMENT_ACT_KIND: _append_source_position_measurement_act,
    SOURCE_POSITION_MEASUREMENT_RESULT_KIND: _append_source_position_measurement_result,
    RECURRENCE_MEASUREMENT_ACT_KIND: _append_recurrence_measurement_act,
    RECURRENCE_MEASUREMENT_RESULT_KIND: _append_recurrence_measurement_result,
    COORDINATE_MEASUREMENT_ACT_KIND: _append_coordinate_measurement_act,
    COORDINATE_MEASUREMENT_RESULT_KIND: _append_coordinate_measurement_result,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT_KIND: (
        _append_recurrent_result_material_measurement_act
    ),
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESULT_KIND: (
        _append_recurrent_result_material_measurement_result
    ),
}

def _responsibility_reference(assignment: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "book_clause_identity": assignment.material["book_clause_identity"],
        "exact_act_identity": assignment.material["act_identity"],
        "subject_reference": deepcopy(assignment.material["subject"]),
        "result_boundary_identity": assignment.material["result_boundary_identity"],
    }


def _record_responsibility(
    ledger: EventLedger,
    *,
    act_kind: str,
    exact_act: str,
    rule: str,
    book_reference: str,
    locality_identity: str,
    through_event_occurrence_identity: str,
    act_identity: str,
    act_occurrence_identity: str,
    result_identity: str,
    subject: dict[str, Any],
) -> Event:
    return _append_responsibility(
        ledger,
        _ACT_RESPONSIBILITY_KINDS[act_kind],
        {
            "book_clause_identity": book_reference,
            "result_boundary_identity": result_identity,
            "through_event_occurrence_identity": through_event_occurrence_identity,
            "act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "exact_act": exact_act,
            "rule": rule,
            "subject": subject,
            "scope": {
                "locality_identity": locality_identity,
            },
            "conflicts": [],
            "unknown": [],
        },
        locality_identity,
    )


def _record_yielded_result(
    ledger: EventLedger,
    *,
    act_kind: str,
    result_kind: str,
    exact_act: str,
    book_reference: str,
    occurrence_boundary: str,
    locality_identity: str,
    act_payload: dict[str, Any],
    result_payload: dict[str, Any],
    identity_prefix: str,
    result_exact_material: bytes | None = None,
) -> tuple[Event, Event]:
    latest_locality_event = ledger.latest_locality_event(locality_identity)
    if latest_locality_event is None:
        raise ValueError("source-position work requires an exact Locality boundary")
    through_event_occurrence_identity = latest_locality_event.identity
    act_identity = new_identity(identity_prefix + "_act")
    act_occurrence_identity = new_identity(identity_prefix + "_act_occurrence")
    result_identity = new_identity(identity_prefix + "_result")
    subject = act_payload.get("subject")
    if type(subject) is not dict:
        raise ValueError("source-position Responsibility requires one exact subject")
    assignment = _record_responsibility(
        ledger,
        act_kind=act_kind,
        exact_act=exact_act,
        rule=_EXACT_ACT_RULES[exact_act],
        book_reference=book_reference,
        locality_identity=locality_identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
        act_identity=act_identity,
        act_occurrence_identity=act_occurrence_identity,
        result_identity=result_identity,
        subject=subject,
    )
    assignment_reference = _responsibility_reference(assignment)
    act = _EVENT_APPENDERS[act_kind](
        ledger,
        {
            "book_reference": book_reference,
            "act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "result_identity": result_identity,
            "act": exact_act,
            "responsibility_assignment_reference": assignment_reference,
            "coordinates": {
                "through_event_occurrence_identity": through_event_occurrence_identity,
                **deepcopy(act_payload),
            },
        },
        locality_identity,
    )
    content = {
        "book_reference": book_reference,
        "result_identity": result_identity,
        "act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "act_occurrence_event_identity": act.identity,
        "coordinates": deepcopy(result_payload),
    }
    yielded = _record_yield_relation(
        ledger,
        locality_identity=locality_identity,
        exact_act=exact_act,
        act_occurrence_identity=act_occurrence_identity,
        act_occurrence_event_identity=act.identity,
        result_kind=result_kind,
        result_identity=result_identity,
        result_content=content,
        occurrence_boundary=occurrence_boundary,
        result_exact_material=result_exact_material,
    )
    result = _EVENT_APPENDERS[result_kind](
        ledger,
        {**content, "yield_relation_identity": yielded.identity},
        locality_identity,
    )
    return act, result


def _require_yield(
    ledger: EventLedger,
    result: Event,
    *,
    exact_act: str,
    occurrence_boundary: str,
) -> Event:
    act = _recorded_occurrence(
        ledger,
        result.material.get("act_occurrence_event_identity"),
        message="recorded result carries no exact responsible Act occurrence",
    )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        yield_relation_event_identity=result.material.get(
            "yield_relation_identity"
        ),
        act_occurrence_event_identity=act.identity,
    )
    yielded = ledger.get(result.material.get("yield_relation_identity"))
    if (
        result.locality_identity != act.locality_identity
        or act.material.get("act") != exact_act
        or yielded is None
        or yielded.material.get("occurrence_boundary") != occurrence_boundary
        or not all(requirements.values())
    ):
        raise ValueError("recorded result carries no exact Yield relation")
    _require_act_boundary(ledger, act)
    _require_responsibility(ledger, act, result)
    return act


def _require_act_boundary(ledger: EventLedger, act: Event) -> None:
    boundary_identity = _coordinates(act.material).get(
        "through_event_occurrence_identity"
    )
    if type(boundary_identity) is not str or not boundary_identity:
        raise ValueError("source-position Act carries no exact through-occurrence boundary")
    occurrences = ledger.occurrences_in_append_order(
        (boundary_identity, act.identity),
        locality_identity=act.locality_identity,
    )
    if tuple(event.identity for event in occurrences) != (
        boundary_identity,
        act.identity,
    ):
        raise ValueError("source-position Act carries no exact through-occurrence boundary")


def _require_responsibility(
    ledger: EventLedger, act: Event, result: Event | None = None
) -> Event:
    reference = act.material.get("responsibility_assignment_reference")
    if type(reference) is not dict or set(reference) != {
        "recorded_occurrence_identity",
        "book_clause_identity",
        "exact_act_identity",
        "subject_reference",
        "result_boundary_identity",
    }:
        raise ValueError("source-position Act carries no exact Responsibility")
    assignment = ledger.get(reference.get("recorded_occurrence_identity"))
    if (
        assignment is None
        or assignment.locality_identity != act.locality_identity
        or ledger.integrity_of(assignment.identity) == CORRUPTED
        or reference != _responsibility_reference(assignment)
        or assignment.material.get("act_identity") != act.material.get("act_identity")
        or assignment.material.get("act_occurrence_identity")
        != act.material.get("act_occurrence_identity")
        or assignment.material.get("exact_act") != act.material.get("act")
        or assignment.material.get("rule")
        != _EXACT_ACT_RULES.get(act.material.get("act"))
        or assignment.material.get("subject")
        != _coordinates(act.material).get("subject")
        or assignment.material.get("through_event_occurrence_identity")
        != _coordinates(act.material).get("through_event_occurrence_identity")
        or type(assignment.material.get("scope")) is not dict
        or type(assignment.material.get("conflicts")) is not list
        or type(assignment.material.get("unknown")) is not list
    ):
        raise ValueError("source-position Act carries no exact Responsibility")
    occurrences = ledger.occurrences_in_append_order(
        (assignment.identity, act.identity),
        locality_identity=act.locality_identity,
    )
    if tuple(event.identity for event in occurrences) != (
        assignment.identity,
        act.identity,
    ):
        raise ValueError("source-position Responsibility does not precede its Act")
    if (
        result is not None
        and assignment.material.get("result_boundary_identity")
        != result.material.get("result_identity")
    ):
        raise ValueError("source-position Responsibility owns no exact result")
    return assignment


def _require_recorded_responsibility(
    ledger: EventLedger, event: Event
) -> Event:
    material = event.material
    if (
        event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
        or type(material) is not dict
        or type(material.get("book_clause_identity")) is not str
        or not material["book_clause_identity"]
        or type(material.get("result_boundary_identity")) is not str
        or not material["result_boundary_identity"]
        or type(material.get("through_event_occurrence_identity")) is not str
        or not material["through_event_occurrence_identity"]
        or type(material.get("act_identity")) is not str
        or not material["act_identity"]
        or type(material.get("act_occurrence_identity")) is not str
        or not material["act_occurrence_identity"]
        or type(material.get("exact_act")) is not str
        or not material["exact_act"]
        or material.get("rule") != _EXACT_ACT_RULES.get(material.get("exact_act"))
        or type(material.get("subject")) is not dict
        or type(material.get("scope")) is not dict
        or type(material.get("conflicts")) is not list
        or type(material.get("unknown")) is not list
    ):
        raise ValueError("source-position Responsibility is not exact")
    boundary = ledger.get(material["through_event_occurrence_identity"])
    if (
        boundary is None
        or boundary.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary.identity) == CORRUPTED
        or tuple(
            occurrence.identity
            for occurrence in ledger.occurrences_in_append_order(
                (boundary.identity, event.identity),
                locality_identity=event.locality_identity,
            )
        )
        != (boundary.identity, event.identity)
    ):
        raise ValueError("source-position Responsibility has no exact prior boundary")
    return event


def _require_current_measurement_subject(
    ledger: EventLedger,
    *,
    locality_identity: str,
    measurement_result_event_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from seed_runtime.operator_current_coordinates import read_operator_current_coordinates

    current_coordinates = (
        read_operator_current_coordinates(ledger, locality_identity=locality_identity)
        if current_coordinates is None
        else current_coordinates
    )
    locality_events = ledger.list_locality(locality_identity)
    if (
        type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity") != locality_identity
        or not locality_events
        or current_coordinates.get("through_event_occurrence_identity")
        != locality_events[-1].identity
        or measurement_result_event_identity
        not in current_coordinates.get("measurement_occurrences", {})
    ):
        raise ValueError("current coordinates carry no exact Measurement subject")
    return current_coordinates


def _carry_recorded_events(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    events: tuple[Event, ...],
) -> dict[str, Any]:
    """Advance current coordinates through the exact recorded occurrences.

    Current coordinates do not include every durable lifecycle occurrence.
    Keeping a second partial reader here made the coordinates agree with replay
    while the boundary count did not. The bounded advance is the exact contract
    and does not read the earlier Locality again.
    """

    from seed_runtime.operator_current_coordinates import (
        advance_operator_current_coordinates,
    )

    if not events:
        return current_coordinates
    return advance_operator_current_coordinates(
        ledger,
        (event.identity for event in events),
        locality_identity=events[0].locality_identity,
        prior=current_coordinates,
    )


def _pair_subject(
    coordinates: tuple[dict[str, Any], ...], pair: tuple[int, int]
) -> dict[str, Any]:
    first_number, second_number = pair
    if (
        type(first_number) is not int
        or type(second_number) is not int
        or first_number < 0
        or second_number <= first_number
        or second_number >= len(coordinates)
    ):
        raise ValueError("source-position Compare requires two exact source positions")
    return {
        "first_source_position_coordinate": coordinates[first_number],
        "second_source_position_coordinate": coordinates[second_number],
    }


def _coordinate_numbers(
    coordinates: tuple[dict[str, Any], ...], subject: dict[str, Any]
) -> tuple[int, int]:
    first = subject.get("first_source_position_coordinate")
    second = subject.get("second_source_position_coordinate")
    try:
        first_number = coordinates.index(first)
        second_number = coordinates.index(second)
    except ValueError as error:
        raise ValueError("Compare subjects are not exact source positions") from error
    pair = (first_number, second_number)
    if _pair_subject(coordinates, pair) != subject:
        raise ValueError("Compare subjects are not exact source positions")
    return pair


def _record_compare(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    coordinates: tuple[dict[str, Any], ...],
    pair: tuple[int, int],
    prior_result_reference: dict[str, str] | None,
) -> Event:
    subject = _pair_subject(coordinates, pair)
    locality_identity = coordinates[0]["locality_identity"]
    applicability_subject = {
        "direct_position_result_occurrence": direct_result_event_identity,
        "source_position_coordinates": list(coordinates),
        "compare_subject": subject,
        "prior_result_reference": prior_result_reference,
    }
    _applicability_act, applicability = _record_yielded_result(
        ledger,
        act_kind=COMPARE_APPLICABILITY_ACT_KIND,
        result_kind=COMPARE_APPLICABILITY_RESULT_KIND,
        exact_act=COMPARE_APPLICABILITY_ACT,
        book_reference="01.Current.E.1",
        occurrence_boundary=COMPARE_APPLICABILITY_BOUNDARY,
        locality_identity=locality_identity,
        act_payload={"subject": applicability_subject},
        result_payload={
            "subject": applicability_subject,
            "applicability": "applicable",
        },
        identity_prefix="source_position_compare_applicability",
    )
    finding = (
        "same-content"
        if subject["first_source_position_coordinate"]["exact_material"]
        == subject["second_source_position_coordinate"]["exact_material"]
        else "difference"
    )
    compare_subject = {
        **applicability_subject,
        "applicability_result_reference": _result_reference(applicability),
    }
    _compare_act, result = _record_yielded_result(
        ledger,
        act_kind=COMPARE_ACT_KIND,
        result_kind=COMPARE_RESULT_KIND,
        exact_act=COMPARE_ACT,
        book_reference="04.Compare",
        occurrence_boundary=COMPARE_BOUNDARY,
        locality_identity=locality_identity,
        act_payload={
            "subject": compare_subject,
            "participation_relations": [
                {
                    "first_subject": subject["first_source_position_coordinate"],
                    "relation": "participation",
                    "second_subject": {"role": "first subject"},
                },
                {
                    "first_subject": subject["second_source_position_coordinate"],
                    "relation": "participation",
                    "second_subject": {"role": "second subject"},
                },
            ],
        },
        result_payload={
            "subject": compare_subject,
            "finding": {
                "subject": subject,
                "result": finding,
            },
        },
        identity_prefix="source_position_compare",
    )
    return result


def get_recorded_source_position_compare(
    ledger: EventLedger,
    result_event_identity: str,
    *,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> dict[str, Any]:
    cache_key = ("compare_result", result_event_identity)
    if _validated is not None and cache_key in _validated:
        return _validated[cache_key]
    result = _recorded_occurrence(
        ledger,
        result_event_identity,
        message="source-position Compare result is not exact",
    )
    act = _require_yield(
        ledger,
        result,
        exact_act=COMPARE_ACT,
        occurrence_boundary=COMPARE_BOUNDARY,
    )
    result_coordinates = _coordinates(result.material)
    subject = result_coordinates.get("subject")
    if type(subject) is not dict:
        raise ValueError("source-position Compare carries no exact subject")
    direct_identity = subject.get("direct_position_result_occurrence")
    direct_coordinates = _direct_coordinates(
        ledger, direct_identity, _validated=_validated
    )
    coordinates = subject.get("source_position_coordinates")
    compare_subject = subject.get("compare_subject")
    if type(coordinates) is not list or type(compare_subject) is not dict:
        raise ValueError("source-position Compare carries no exact subject positions")
    coordinate_tuple = tuple(coordinates)
    expected_source = tuple(
        direct_coordinates[coordinate["position"]] for coordinate in coordinate_tuple
    )
    pair = _coordinate_numbers(coordinate_tuple, compare_subject)
    expected_pair_subject = _pair_subject(coordinate_tuple, pair)
    applicability = _recorded_occurrence(
        ledger,
        subject.get("applicability_result_reference", {}).get(
            "recorded_occurrence_reference"
        ),
        message="source-position Compare carries no exact Applicability result",
    )
    applicability_act = _require_yield(
        ledger,
        applicability,
        exact_act=COMPARE_APPLICABILITY_ACT,
        occurrence_boundary=COMPARE_APPLICABILITY_BOUNDARY,
    )
    finding = result_coordinates.get("finding")
    expected_result = (
        "same-content"
        if expected_pair_subject["first_source_position_coordinate"]["exact_material"]
        == expected_pair_subject["second_source_position_coordinate"]["exact_material"]
        else "difference"
    )
    expected_applicability_subject = {
        key: deepcopy(value)
        for key, value in subject.items()
        if key != "applicability_result_reference"
    }
    prior_reference = subject.get("prior_result_reference")
    if prior_reference is None:
        exact_prior = len(coordinate_tuple) == 2
    elif type(prior_reference) is dict:
        prior = get_recorded_source_position_measurement(
            ledger,
            prior_reference.get("recorded_occurrence_reference"),
            _validated=_validated,
        )
        exact_prior = (
            prior_reference.get("result_reference") == prior["result_identity"]
            and prior["source_position_coordinates"] == list(coordinate_tuple[:-1])
            and pair[1] == len(coordinate_tuple) - 1
        )
    else:
        exact_prior = False
    participation = _coordinates(act.material).get("participation_relations")
    exact_participation = (
        type(participation) is list
        and len(participation) == 2
        and tuple(item.get("relation") for item in participation)
        == ("participation", "participation")
        and tuple(item.get("first_subject") for item in participation)
        == (
            expected_pair_subject["first_source_position_coordinate"],
            expected_pair_subject["second_source_position_coordinate"],
        )
        and tuple(item.get("second_subject") for item in participation)
        == ({"role": "first subject"}, {"role": "second subject"})
    )
    if (
        coordinate_tuple != expected_source
        or not exact_prior
        or subject["applicability_result_reference"]
        != _result_reference(applicability)
        or _coordinates(applicability.material).get("subject")
        != expected_applicability_subject
        or _coordinates(applicability.material).get("applicability")
        != "applicable"
        or _coordinates(applicability_act.material).get("subject")
        != expected_applicability_subject
        or _coordinates(act.material).get("subject") != subject
        or not exact_participation
        or type(finding) is not dict
        or finding.get("subject") != expected_pair_subject
        or finding.get("result") != expected_result
    ):
        raise ValueError("source-position Compare result is not exact")
    reading = {**deepcopy(result.material), **deepcopy(result_coordinates)}
    if _validated is not None:
        _validated[cache_key] = reading
    return reading


def _complete_pairs(length: int) -> tuple[tuple[int, int], ...]:
    # Established comparisons remain the exact prefix when the source-position count grows.
    # Only comparisons introduced by the new final source position are appended.
    return tuple(
        (first, second)
        for second in range(1, length)
        for first in range(second)
    )


def _record_source_position_result(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    coordinates: tuple[dict[str, Any], ...],
    compare_results: tuple[Event, ...],
    newly_introduced_compare_results: tuple[Event, ...],
    prior_source_position_result: Event | None,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> Event:
    readings = tuple(
        get_recorded_source_position_compare(
            ledger, event.identity, _validated=_validated
        )
        for event in compare_results
    )
    pairs = tuple(
        _coordinate_numbers(coordinates, reading["finding"]["subject"])
        for reading in readings
    )
    if pairs != _complete_pairs(len(coordinates)):
        raise ValueError("coordinate result requires all internal Compare results")
    signature = [reading["finding"]["result"] for reading in readings]
    prior_reference = (
        _result_reference(prior_source_position_result)
        if prior_source_position_result is not None
        else None
    )
    payload = {
        "direct_position_result_occurrence": direct_result_event_identity,
        "coordinate_count": len(coordinates),
        "source_position_coordinates": list(coordinates),
        "compare_result_references": [
            _result_reference(event) for event in compare_results
        ],
        "new_compare_result_references": [
            _result_reference(event) for event in newly_introduced_compare_results
        ],
        "prior_result_reference": prior_reference,
        "complete_compare_findings": signature,
    }
    _act, result = _record_yielded_result(
        ledger,
        act_kind=SOURCE_POSITION_MEASUREMENT_ACT_KIND,
        result_kind=SOURCE_POSITION_MEASUREMENT_RESULT_KIND,
        exact_act=SOURCE_POSITION_MEASUREMENT_ACT,
        book_reference="01.Source.D",
        occurrence_boundary=SOURCE_POSITION_MEASUREMENT_BOUNDARY,
        locality_identity=coordinates[0]["locality_identity"],
        act_payload={"subject": payload},
        result_payload=payload,
        identity_prefix="source_position_measurement",
    )
    return result


def get_recorded_source_position_measurement(
    ledger: EventLedger,
    result_event_identity: str,
    *,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> dict[str, Any]:
    cache_key = ("source_position_result", result_event_identity)
    if _validated is not None and cache_key in _validated:
        return _validated[cache_key]
    result = _recorded_occurrence(
        ledger,
        result_event_identity,
        message="source-position result is not exact",
    )
    act = _require_yield(
        ledger,
        result,
        exact_act=SOURCE_POSITION_MEASUREMENT_ACT,
        occurrence_boundary=SOURCE_POSITION_MEASUREMENT_BOUNDARY,
    )
    material = _coordinates(result.material)
    direct_coordinates = _direct_coordinates(
        ledger,
        material.get("direct_position_result_occurrence"),
        _validated=_validated,
    )
    coordinates = material.get("source_position_coordinates")
    references = material.get("compare_result_references")
    new_references = material.get("new_compare_result_references")
    length = material.get("coordinate_count")
    if (
        type(length) is not int
        or length < 2
        or type(coordinates) is not list
        or len(coordinates) != length
        or type(references) is not list
        or type(new_references) is not list
    ):
        raise ValueError("source-position result carries no exact results")
    start = coordinates[0].get("position")
    if (
        type(start) is not int
        or tuple(coordinates) != direct_coordinates[start : start + length]
        or tuple(coordinate["position"] for coordinate in coordinates)
        != tuple(range(start, start + length))
    ):
        raise ValueError("source-position result carries no exact source-position coordinates")
    readings = []
    for reference in references:
        if type(reference) is not dict:
            raise ValueError("source-position result carries no exact Compare reference")
        reading = get_recorded_source_position_compare(
            ledger,
            reference.get("recorded_occurrence_reference"),
            _validated=_validated,
        )
        if reference.get("result_reference") != reading["result_identity"]:
            raise ValueError("source-position result carries no exact Compare reference")
        readings.append(reading)
    coordinate_tuple = tuple(coordinates)
    pairs = tuple(
        _coordinate_numbers(coordinate_tuple, reading["finding"]["subject"])
        for reading in readings
    )
    expected_surface = [reading["finding"]["result"] for reading in readings]
    prior_reference = material.get("prior_result_reference")
    if prior_reference is None:
        expected_new = references
        prior_material = None
    else:
        if type(prior_reference) is not dict:
            raise ValueError("source-position result carries no exact prior result")
        prior_material = get_recorded_source_position_measurement(
            ledger,
            prior_reference.get("recorded_occurrence_reference"),
            _validated=_validated,
        )
        if (
            prior_reference.get("result_reference") != prior_material["result_identity"]
            or prior_material["source_position_coordinates"] != coordinates[:-1]
            or prior_material["compare_result_references"]
            != references[: len(prior_material["compare_result_references"])]
        ):
            raise ValueError("source-position result carries no exact prior result")
        expected_new = references[len(prior_material["compare_result_references"]) :]
    if (
        pairs != _complete_pairs(length)
        or material.get("complete_compare_findings") != expected_surface
        or new_references != expected_new
        or _coordinates(act.material).get("subject")
        != {
            key: deepcopy(value)
            for key, value in material.items()
            if key
            not in {
                "book_reference",
                "result_identity",
                "act_identity",
                "act_occurrence_identity",
                "act_occurrence_identity",
                "yield_relation_identity",
            }
        }
    ):
        raise ValueError("source-position result is not exact")
    reading = {**deepcopy(result.material), **deepcopy(material)}
    if _validated is not None:
        _validated[cache_key] = reading
    return reading


def _source_position_results_at_boundary(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    coordinate_count: int,
    boundary: EventLedgerBoundary,
    locality_identity: str,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> tuple[Event, ...]:
    events = []
    for event in ledger.list(through=boundary):
        coordinates = event.material.get("coordinates")
        if (
            event.locality_identity == locality_identity
            and type(coordinates) is dict
            and coordinates.get("direct_position_result_occurrence")
            == direct_result_event_identity
            and coordinates.get("coordinate_count") == coordinate_count
            and type(coordinates.get("source_position_coordinates")) is list
            and type(coordinates.get("compare_result_references")) is list
            and type(event.material.get("act_occurrence_event_identity")) is str
            and type(event.material.get("yield_relation_identity")) is str
        ):
            get_recorded_source_position_measurement(
                ledger, event.identity, _validated=_validated
            )
            events.append(event)
    return tuple(events)


def _recurrence_findings(source_position_results: tuple[Event, ...]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Event]] = {}
    surfaces: dict[str, list[dict[str, Any]]] = {}
    for event in source_position_results:
        event_coordinates = _coordinates(event.material)
        surface = event_coordinates["complete_compare_findings"]
        key = _exact_json(surface)
        grouped.setdefault(key, []).append(event)
        surfaces[key] = surface
    groups = []
    for key in sorted(grouped):
        productions = grouped[key]
        support = [_result_reference(event) for event in productions]
        subject = {
            "coordinate_count": _coordinates(productions[0].material)["coordinate_count"],
            "complete_compare_findings": deepcopy(surfaces[key]),
        }
        identity = _digest(
            "source-position-results",
            {"subject": subject, "support": support},
        )
        group = {
            "finding_reference": identity,
            "subject": subject,
            "support_result_references": support,
            "count": len(productions),
        }
        if len(productions) > 1:
            group["recurrence"] = {
                "finding_reference": _digest(
                    "source-position-recurrence",
                    {"count_finding_reference": identity, "count": len(productions)},
                ),
                "count_finding_reference": identity,
            }
        groups.append(group)
    return groups


def _record_recurrence_measurement(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    coordinate_count: int,
    locality_identity: str,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> Event:
    boundary = ledger.append_boundary()
    source_position_results = _source_position_results_at_boundary(
        ledger,
        direct_result_event_identity=direct_result_event_identity,
        coordinate_count=coordinate_count,
        boundary=boundary,
        locality_identity=locality_identity,
        _validated=_validated,
    )
    if not source_position_results:
        raise ValueError("recurrence Measurement requires exact source-position results")
    groups = _recurrence_findings(source_position_results)
    payload = {
        "direct_position_result_occurrence": direct_result_event_identity,
        "coordinate_count": coordinate_count,
        "completeness_boundary_reference": boundary.identity,
        "source_position_result_references": [
            _result_reference(event) for event in source_position_results
        ],
        "findings": groups,
    }
    _act, result = _record_yielded_result(
        ledger,
        act_kind=RECURRENCE_MEASUREMENT_ACT_KIND,
        result_kind=RECURRENCE_MEASUREMENT_RESULT_KIND,
        exact_act=RECURRENCE_MEASUREMENT_ACT,
        book_reference="01.Source.D",
        occurrence_boundary=RECURRENCE_MEASUREMENT_BOUNDARY,
        locality_identity=locality_identity,
        act_payload={"subject": payload},
        result_payload=payload,
        identity_prefix="source_position_recurrence_measurement",
    )
    return result


def get_recorded_source_position_recurrence(
    ledger: EventLedger,
    result_event_identity: str,
    *,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> dict[str, Any]:
    cache_key = ("recurrence_result", result_event_identity)
    if _validated is not None and cache_key in _validated:
        return _validated[cache_key]
    result = _recorded_occurrence(
        ledger,
        result_event_identity,
        message="source-position recurrence result is not exact",
    )
    act = _require_yield(
        ledger,
        result,
        exact_act=RECURRENCE_MEASUREMENT_ACT,
        occurrence_boundary=RECURRENCE_MEASUREMENT_BOUNDARY,
    )
    material = _coordinates(result.material)
    boundary_identity = material.get("completeness_boundary_reference")
    if type(boundary_identity) is not str or not boundary_identity:
        raise ValueError("recurrence result carries no exact completeness boundary")
    source_position_results = _source_position_results_at_boundary(
        ledger,
        direct_result_event_identity=material.get(
            "direct_position_result_occurrence"
        ),
        coordinate_count=material.get("coordinate_count"),
        boundary=EventLedgerBoundary(boundary_identity),
        locality_identity=result.locality_identity,
        _validated=_validated,
    )
    expected_payload = {
        "direct_position_result_occurrence": material[
            "direct_position_result_occurrence"
        ],
        "coordinate_count": material["coordinate_count"],
        "completeness_boundary_reference": boundary_identity,
        "source_position_result_references": [
            _result_reference(event) for event in source_position_results
        ],
        "findings": _recurrence_findings(source_position_results),
    }
    carried_payload = {
        key: deepcopy(value)
        for key, value in material.items()
        if key
        not in {
            "book_reference",
            "result_identity",
            "act_identity",
            "act_occurrence_identity",
            "act_occurrence_identity",
            "yield_relation_identity",
        }
    }
    if (
        carried_payload != expected_payload
        or _coordinates(act.material).get("subject") != expected_payload
    ):
        raise ValueError("source-position recurrence result is not exact")
    reading = {**deepcopy(result.material), **deepcopy(material)}
    if _validated is not None:
        _validated[cache_key] = reading
    return reading


def _extend_recurrent_source_positions(
    ledger: EventLedger,
    *,
    recurrence_result: Event,
    direct_coordinates: tuple[dict[str, Any], ...],
    _validated: dict[tuple[str, str], Any] | None = None,
) -> tuple[Event, ...]:
    recurrence = get_recorded_source_position_recurrence(
        ledger, recurrence_result.identity, _validated=_validated
    )
    extended = []
    for finding in recurrence["findings"]:
        if "recurrence" not in finding:
            continue
        for reference in finding["support_result_references"]:
            prior_event = _recorded_occurrence(
                ledger,
                reference["recorded_occurrence_reference"],
                message="recurrence carries no exact producing source-position result",
            )
            prior = get_recorded_source_position_measurement(
                ledger, prior_event.identity, _validated=_validated
            )
            if reference["result_reference"] != prior["result_identity"]:
                raise ValueError("recurrence carries no exact producing source-position result")
            prior_coordinates = tuple(prior["source_position_coordinates"])
            next_position = prior_coordinates[-1]["position"] + 1
            if next_position >= len(direct_coordinates):
                continue
            coordinates = (*prior_coordinates, direct_coordinates[next_position])
            prior_compare_events = tuple(
                _recorded_occurrence(
                    ledger,
                    compare_reference["recorded_occurrence_reference"],
                    message="prior source-position result carries no exact Compare result",
                )
                for compare_reference in prior["compare_result_references"]
            )
            new_results = tuple(
                _record_compare(
                    ledger,
                    direct_result_event_identity=recurrence[
                        "direct_position_result_occurrence"
                    ],
                    coordinates=coordinates,
                    pair=(coordinate_number, len(coordinates) - 1),
                    prior_result_reference=_result_reference(prior_event),
                )
                for coordinate_number in range(len(coordinates) - 1)
            )
            extended.append(
                _record_source_position_result(
                    ledger,
                    direct_result_event_identity=recurrence[
                        "direct_position_result_occurrence"
                    ],
                    coordinates=coordinates,
                    compare_results=(*prior_compare_events, *new_results),
                    newly_introduced_compare_results=new_results,
                    prior_source_position_result=prior_event,
                    _validated=_validated,
                )
            )
    return tuple(extended)


def _record_source_position_measurements(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
) -> SourcePositionMeasurements:
    """Record consecutive source positions until recurrence is exhausted."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("source-position recording requires an EventLedger")
    validated: dict[tuple[str, str], Any] = {}
    direct_coordinates = _direct_coordinates(
        ledger, direct_result_event_identity, _validated=validated
    )
    locality_identity = direct_coordinates[0]["locality_identity"]
    current_coordinates = _require_current_measurement_subject(
        ledger,
        locality_identity=locality_identity,
        measurement_result_event_identity=direct_result_event_identity,
    )
    locality_event_count = len(ledger.list_locality(locality_identity))
    steps = []

    before = len(ledger.list())
    minimal = []
    for start in range(len(direct_coordinates) - 1):
        coordinates = direct_coordinates[start : start + 2]
        compare = _record_compare(
            ledger,
            direct_result_event_identity=direct_result_event_identity,
            coordinates=coordinates,
            pair=(0, 1),
            prior_result_reference=None,
        )
        minimal.append(
            _record_source_position_result(
                ledger,
                direct_result_event_identity=direct_result_event_identity,
                coordinates=coordinates,
                compare_results=(compare,),
                newly_introduced_compare_results=(compare,),
                prior_source_position_result=None,
                _validated=validated,
            )
        )
    recurrence = _record_recurrence_measurement(
        ledger,
        direct_result_event_identity=direct_result_event_identity,
        coordinate_count=2,
        locality_identity=locality_identity,
        _validated=validated,
    )
    steps.append(
        SourcePositionMeasurementStep(2, tuple(minimal), recurrence, len(ledger.list()) - before)
    )

    while True:
        before = len(ledger.list())
        source_position_results = _extend_recurrent_source_positions(
            ledger,
            recurrence_result=recurrence,
            direct_coordinates=direct_coordinates,
            _validated=validated,
        )
        if not source_position_results:
            break
        coordinate_count = _coordinates(source_position_results[0].material)["coordinate_count"]
        recurrence = _record_recurrence_measurement(
            ledger,
            direct_result_event_identity=direct_result_event_identity,
            coordinate_count=coordinate_count,
            locality_identity=locality_identity,
            _validated=validated,
        )
        steps.append(
            SourcePositionMeasurementStep(
                coordinate_count,
                source_position_results,
                recurrence,
                len(ledger.list()) - before,
            )
        )
    new_events = tuple(ledger.list_locality(locality_identity)[locality_event_count:])
    return SourcePositionMeasurements(
        direct_result_event_identity,
        tuple(steps),
        True,
        _carry_recorded_events(ledger, current_coordinates, new_events),
    )


def record_source_position_measurements(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
) -> SourcePositionMeasurements:
    """Record the source-exhausted proof road in a durable mechanics boundary."""

    with ledger.batched():
        return _record_source_position_measurements(
            ledger,
            direct_result_event_identity=direct_result_event_identity,
        )


def _coordinate_findings(
    ledger: EventLedger,
    recurrence_group: dict[str, Any],
    *,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> list[dict[str, Any]]:
    productions = []
    for reference in recurrence_group["support_result_references"]:
        material = get_recorded_source_position_measurement(
            ledger,
            reference["recorded_occurrence_reference"],
            _validated=_validated,
        )
        if reference["result_reference"] != material["result_identity"]:
            raise ValueError("coordinate Measurement carries no exact production")
        productions.append((reference, material))
    coordinate_count = recurrence_group["subject"]["coordinate_count"]
    if any(production[1]["coordinate_count"] != coordinate_count for production in productions):
        raise ValueError("coordinate Measurement results carry different source positions")
    findings = []
    for corresponding_coordinates in zip(
        *(
            production["source_position_coordinates"]
            for _reference, production in productions
        ),
        strict=True,
    ):
        grouped: dict[int, list[dict[str, Any]]] = {}
        coordinates: dict[int, list[dict[str, Any]]] = {}
        for (reference, _production), coordinate in zip(
            productions, corresponding_coordinates, strict=True
        ):
            value = coordinate["exact_material"][0]
            grouped.setdefault(value, []).append(deepcopy(reference))
            coordinates.setdefault(value, []).append(deepcopy(coordinate))
        for value in sorted(grouped):
            subject = {
                "recurrence_finding_reference": recurrence_group[
                    "finding_reference"
                ],
                "exact_material": [value],
            }
            support = [
                {
                    "support_result_reference": reference,
                    "source_position_coordinate": coordinate,
                }
                for reference, coordinate in zip(
                    grouped[value], coordinates[value], strict=True
                )
            ]
            identity = _digest(
                "recurrence-corresponding-source-position-material",
                {"subject": subject, "support": support},
            )
            finding = {
                "finding_reference": identity,
                "subject": subject,
                "support": support,
                "count": len(support),
            }
            if len(support) > 1:
                finding["recurrence"] = {
                    "finding_reference": _digest(
                        "recurrence-corresponding-source-position-material-recurrence",
                        {"count_finding_reference": identity, "count": len(support)},
                    ),
                    "count_finding_reference": identity,
                }
            findings.append(finding)
    return findings


def _record_corresponding_coordinate_material_measurements(
    ledger: EventLedger,
    *,
    recurrence_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> CorrespondingCoordinateMeasurements:
    """Measure material at every corresponding exact source position."""

    recurrence_event = _recorded_occurrence(
        ledger,
        recurrence_result_event_identity,
        message="coordinate Measurement requires an exact recurrence result",
    )
    locality_identity = recurrence_event.locality_identity
    current_coordinates = _require_current_measurement_subject(
        ledger,
        locality_identity=locality_identity,
        measurement_result_event_identity=recurrence_result_event_identity,
        current_coordinates=current_coordinates,
    )
    locality_event_count = len(ledger.list_locality(locality_identity))
    validated: dict[tuple[str, str], Any] = {}
    recurrence = get_recorded_source_position_recurrence(
        ledger, recurrence_result_event_identity, _validated=validated
    )
    recorded = []
    for group in recurrence["findings"]:
        if "recurrence" not in group:
            continue
        payload = {
            "source_recurrence_result_reference": {
                "recorded_occurrence_reference": recurrence_result_event_identity,
                "result_reference": recurrence["result_identity"],
            },
            "source_recurrence_finding_reference": group["finding_reference"],
            "support_result_references": group["support_result_references"],
            "completeness_boundary_reference": recurrence[
                "completeness_boundary_reference"
            ],
            "findings": _coordinate_findings(
                ledger, group, _validated=validated
            ),
        }
        _act, result = _record_yielded_result(
            ledger,
            act_kind=COORDINATE_MEASUREMENT_ACT_KIND,
            result_kind=COORDINATE_MEASUREMENT_RESULT_KIND,
            exact_act=COORDINATE_MEASUREMENT_ACT,
            book_reference="01.Source.D.1",
            occurrence_boundary=COORDINATE_MEASUREMENT_BOUNDARY,
            locality_identity=locality_identity,
            act_payload={"subject": payload},
            result_payload=payload,
            identity_prefix="recurrence_corresponding_source_position_material_measurement",
        )
        recorded.append(
            CorrespondingCoordinateMeasurement(group["finding_reference"], result)
        )
    new_events = tuple(ledger.list_locality(locality_identity)[locality_event_count:])
    return CorrespondingCoordinateMeasurements(
        tuple(recorded),
        _carry_recorded_events(ledger, current_coordinates, new_events),
    )


def record_corresponding_coordinate_material_measurements(
    ledger: EventLedger,
    *,
    recurrence_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> CorrespondingCoordinateMeasurements:
    """Record all corresponding-coordinate Measurement results."""

    with ledger.batched():
        return _record_corresponding_coordinate_material_measurements(
            ledger,
            recurrence_result_event_identity=recurrence_result_event_identity,
            current_coordinates=current_coordinates,
        )


def get_recorded_corresponding_coordinate_material_measurement(
    ledger: EventLedger,
    result_event_identity: str,
    *,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> dict[str, Any]:
    cache_key = ("coordinate_result", result_event_identity)
    if _validated is not None and cache_key in _validated:
        return _validated[cache_key]
    result = _recorded_occurrence(
        ledger,
        result_event_identity,
        message="corresponding-coordinate Measurement result is not exact",
    )
    act = _require_yield(
        ledger,
        result,
        exact_act=COORDINATE_MEASUREMENT_ACT,
        occurrence_boundary=COORDINATE_MEASUREMENT_BOUNDARY,
    )
    material = _coordinates(result.material)
    source_reference = material.get("source_recurrence_result_reference")
    if type(source_reference) is not dict:
        raise ValueError("coordinate Measurement carries no exact recurrence result")
    recurrence = get_recorded_source_position_recurrence(
        ledger,
        source_reference.get("recorded_occurrence_reference"),
        _validated=_validated,
    )
    if source_reference.get("result_reference") != recurrence["result_identity"]:
        raise ValueError("coordinate Measurement carries no exact recurrence result")
    matching = tuple(
        group
        for group in recurrence["findings"]
        if group["finding_reference"]
        == material.get("source_recurrence_finding_reference")
        and "recurrence" in group
    )
    if len(matching) != 1:
        raise ValueError("coordinate Measurement carries no exact recurrence group")
    group = matching[0]
    payload = {
        "source_recurrence_result_reference": deepcopy(source_reference),
        "source_recurrence_finding_reference": group["finding_reference"],
        "support_result_references": deepcopy(
            group["support_result_references"]
        ),
        "completeness_boundary_reference": recurrence[
            "completeness_boundary_reference"
        ],
        "findings": _coordinate_findings(
            ledger, group, _validated=_validated
        ),
    }
    carried_payload = {
        key: deepcopy(value)
        for key, value in material.items()
        if key
        not in {
            "book_reference",
            "result_identity",
            "act_identity",
            "act_occurrence_identity",
            "act_occurrence_identity",
            "yield_relation_identity",
        }
    }
    if carried_payload != payload or _coordinates(act.material).get("subject") != payload:
        raise ValueError("corresponding-coordinate Measurement result is not exact")
    reading = {**deepcopy(result.material), **deepcopy(material)}
    if _validated is not None:
        _validated[cache_key] = reading
    return reading


def _support_references(
    finding: dict[str, Any],
) -> tuple[dict[str, str], ...]:
    support = finding.get("support")
    if type(support) is not list:
        raise ValueError("exact-material Measurement carries no exact support")
    references = []
    for occurrence in support:
        if type(occurrence) is not dict or type(
            occurrence.get("support_result_reference")
        ) is not dict:
            raise ValueError("exact-material Measurement carries no exact support")
        references.append(deepcopy(occurrence["support_result_reference"]))
    return tuple(references)


def _recurrent_result_material_payload(
    ledger: EventLedger,
    *,
    recurrence_event: Event,
    recurrence: dict[str, Any],
    recurrence_group: dict[str, Any],
    coordinate_event: Event,
    coordinate_measurement: dict[str, Any],
) -> dict[str, Any] | None:
    """Return exact material common to every recurrent result, or no result."""

    support_references = recurrence_group.get("support_result_references")
    coordinate_count = recurrence_group.get("subject", {}).get("coordinate_count")
    coordinate_source = coordinate_measurement.get(
        "source_recurrence_result_reference"
    )
    if (
        type(support_references) is not list
        or len(support_references) < 2
        or type(coordinate_count) is not int
        or coordinate_count < 2
        or type(coordinate_source) is not dict
        or coordinate_source.get("recorded_occurrence_reference")
        != recurrence_event.identity
        or coordinate_source.get("result_reference")
        != recurrence.get("result_identity")
        or coordinate_measurement.get("source_recurrence_finding_reference")
        != recurrence_group.get("finding_reference")
        or coordinate_measurement.get("support_result_references")
        != support_references
        or coordinate_measurement.get("completeness_boundary_reference")
        != recurrence.get("completeness_boundary_reference")
    ):
        raise ValueError("exact-material Measurement carries no exact recurrence support")

    support_occurrences = []
    for support_reference in support_references:
        if type(support_reference) is not dict:
            raise ValueError("exact-material Measurement carries no exact result")
        production_event = _recorded_occurrence(
            ledger,
            support_reference.get("recorded_occurrence_reference"),
            message="exact-material Measurement carries no exact result",
        )
        _production_act, production = _require_preserved_result(
            ledger,
            production_event,
            exact_act=SOURCE_POSITION_MEASUREMENT_ACT,
            occurrence_boundary=SOURCE_POSITION_MEASUREMENT_BOUNDARY,
        )
        coordinates = production.get("source_position_coordinates")
        if (
            support_reference.get("result_reference")
            != production.get("result_identity")
            or production.get("coordinate_count") != coordinate_count
            or type(coordinates) is not list
            or len(coordinates) != coordinate_count
            or tuple(coordinate.get("position") for coordinate in coordinates)
            != tuple(
                range(
                    coordinates[0]["position"],
                    coordinates[0]["position"] + coordinate_count,
                )
            )
        ):
            raise ValueError(
                "exact-material Measurement cannot recover consecutive source positions"
            )
        support_occurrences.append(
            {
                "support_result_reference": deepcopy(support_reference),
                "source_position_coordinates": deepcopy(coordinates),
            }
        )

    findings = coordinate_measurement.get("findings")
    if type(findings) is not list:
        raise ValueError("exact-material Measurement carries no exact findings")
    exact_support = tuple(support_references)
    complete_findings = []
    for finding in findings:
        if type(finding) is not dict or type(finding.get("subject")) is not dict:
            raise ValueError("exact-material Measurement carries no exact finding")
        material = finding["subject"].get("exact_material")
        if (
            type(material) is not list
            or len(material) != 1
            or type(material[0]) is not int
            or not 0 <= material[0] <= 255
        ):
            raise ValueError("exact-material Measurement carries no exact material")
        finding_support = _support_references(finding)
        if any(reference not in exact_support for reference in finding_support):
            raise ValueError("exact-material Measurement carries different support")
        if (
            finding_support == exact_support
            and finding.get("count") == len(exact_support)
            and type(finding.get("recurrence")) is dict
        ):
            complete_findings.append(finding)

    exact_material = []
    consumed_findings = []
    for corresponding_coordinates in zip(
        *(
            support["source_position_coordinates"]
            for support in support_occurrences
        ),
        strict=True,
    ):
        complete = []
        for finding in complete_findings:
            carried_coordinates = tuple(
                occurrence["source_position_coordinate"]
                for occurrence in finding["support"]
            )
            if carried_coordinates == corresponding_coordinates:
                complete.append(finding)
        if not complete:
            return None
        if len(complete) != 1:
            raise ValueError("exact-material Measurement carries more than one material")
        exact_material.append(complete[0]["subject"]["exact_material"][0])
        consumed_findings.append(deepcopy(complete[0]))

    measured_material = bytes(exact_material)
    for support in support_occurrences:
        if bytes(
            coordinate["exact_material"][0]
            for coordinate in support["source_position_coordinates"]
        ) != measured_material:
            raise ValueError("exact-material Measurement support carries different material")

    coordinate_result_reference = _result_reference(coordinate_event)
    recurrence_result_reference = _result_reference(recurrence_event)
    subject = {
        "coordinate_measurement_result_reference": coordinate_result_reference,
        "recurrence_result_reference": recurrence_result_reference,
        "recurrence_finding_reference": recurrence_group["finding_reference"],
        "support_result_references": deepcopy(support_references),
        "coordinate_count": coordinate_count,
    }
    return {
        "subject": subject,
        "measurement_rule": RECURRENT_RESULT_MATERIAL_MEASUREMENT_RULE,
        "exact_material": exact_material,
        "coordinate_material_findings": consumed_findings,
        "support_result_references": deepcopy(support_references),
        "support_occurrences": support_occurrences,
        "completeness_boundary_reference": recurrence[
            "completeness_boundary_reference"
        ],
        "scope": {
            "locality_identity": recurrence_event.locality_identity,
            "recurrence_result_reference": recurrence_result_reference,
            "recurrence_finding_reference": recurrence_group["finding_reference"],
            "support_result_references": deepcopy(support_references),
            "completeness_boundary_reference": recurrence[
                "completeness_boundary_reference"
            ],
        },
        "locality": {"locality_identity": recurrence_event.locality_identity},
        "conflicts": [],
        "unknown": [
            "what the exact material means beyond this Measurement: Unknown"
        ],
    }


def _coordinate_measurements_for_recurrence(
    ledger: EventLedger,
    *,
    recurrence_event: Event,
    recurrence: dict[str, Any],
    current_coordinates: dict[str, Any],
    _validated: dict[tuple[str, str], Any] | None = None,
) -> dict[str, tuple[Event, dict[str, Any]]]:
    recurrent_groups = {
        finding["finding_reference"]: finding
        for finding in recurrence["findings"]
        if "recurrence" in finding
    }
    carried_measurements = current_coordinates.get("measurement_occurrences")
    if type(carried_measurements) is not dict:
        raise ValueError("exact-material Measurement requires current Measurement results")
    found: dict[str, tuple[Event, dict[str, Any]]] = {}
    for event in ledger.list_locality(recurrence_event.locality_identity):
        coordinates = event.material.get("coordinates")
        if type(coordinates) is not dict:
            continue
        source = coordinates.get("source_recurrence_result_reference")
        if (
            type(source) is not dict
            or source.get("recorded_occurrence_reference") != recurrence_event.identity
            or type(coordinates.get("source_recurrence_finding_reference")) is not str
            or type(coordinates.get("findings")) is not list
            or type(event.material.get("act_occurrence_event_identity")) is not str
            or type(event.material.get("yield_relation_identity")) is not str
        ):
            continue
        if event.identity not in carried_measurements:
            raise ValueError("exact-material Measurement input is not current")
        measurement = get_recorded_corresponding_coordinate_material_measurement(
            ledger, event.identity, _validated=_validated
        )
        reference = measurement["source_recurrence_finding_reference"]
        if reference not in recurrent_groups or reference in found:
            raise ValueError("exact-material Measurements are not exact")
        found[reference] = (event, measurement)
    if tuple(sorted(found)) != tuple(sorted(recurrent_groups)):
        raise ValueError("exact-material Measurements are incomplete")
    return found


def _record_recurrent_result_material_measurements(
    ledger: EventLedger,
    *,
    recurrence_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> RecurrentResultMaterialMeasurements:
    recurrence_event = _recorded_occurrence(
        ledger,
        recurrence_result_event_identity,
        message="exact-material Measurement requires one exact recurrence result",
    )
    current_coordinates = _require_current_measurement_subject(
        ledger,
        locality_identity=recurrence_event.locality_identity,
        measurement_result_event_identity=recurrence_event.identity,
        current_coordinates=current_coordinates,
    )
    validated: dict[tuple[str, str], Any] = {}
    recurrence = get_recorded_source_position_recurrence(
        ledger, recurrence_event.identity, _validated=validated
    )
    coordinate_measurements = _coordinate_measurements_for_recurrence(
        ledger,
        recurrence_event=recurrence_event,
        recurrence=recurrence,
        current_coordinates=current_coordinates,
        _validated=validated,
    )
    for event in ledger.list_locality(recurrence_event.locality_identity):
        coordinates = event.material.get("coordinates")
        if type(coordinates) is not dict or type(event.exact_material) is not bytes:
            continue
        subject = coordinates.get("subject")
        source = (
            subject.get("recurrence_result_reference")
            if type(subject) is dict
            else None
        )
        if (
            type(source) is dict
            and source.get("recorded_occurrence_reference")
            == recurrence_event.identity
        ):
            raise ValueError("exact-material Measurement was already recorded")

    locality_event_count = len(ledger.list_locality(recurrence_event.locality_identity))
    recorded = []
    for group in recurrence["findings"]:
        if "recurrence" not in group:
            continue
        coordinate_event, coordinate_measurement = coordinate_measurements[
            group["finding_reference"]
        ]
        payload = _recurrent_result_material_payload(
            ledger,
            recurrence_event=recurrence_event,
            recurrence=recurrence,
            recurrence_group=group,
            coordinate_event=coordinate_event,
            coordinate_measurement=coordinate_measurement,
        )
        if payload is None:
            continue
        _act, result = _record_yielded_result(
            ledger,
            act_kind=RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT_KIND,
            result_kind=RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESULT_KIND,
            exact_act=RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT,
            book_reference="01.Source.D",
            occurrence_boundary=RECURRENT_RESULT_MATERIAL_MEASUREMENT_BOUNDARY,
            locality_identity=recurrence_event.locality_identity,
            act_payload={"subject": payload["subject"]},
            result_payload=payload,
            identity_prefix="recurrent_result_exact_material_measurement",
            result_exact_material=bytes(payload["exact_material"]),
        )
        recorded.append(
            RecurrentResultMaterialMeasurement(group["finding_reference"], result)
        )
    new_events = tuple(
        ledger.list_locality(recurrence_event.locality_identity)[
            locality_event_count:
        ]
    )
    return RecurrentResultMaterialMeasurements(
        tuple(recorded),
        _carry_recorded_events(ledger, current_coordinates, new_events),
    )


def record_recurrent_result_material_measurements(
    ledger: EventLedger,
    *,
    recurrence_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> RecurrentResultMaterialMeasurements:
    """Measure exact material shared by every exact recurrent result."""

    with ledger.batched():
        return _record_recurrent_result_material_measurements(
            ledger,
            recurrence_result_event_identity=recurrence_result_event_identity,
            current_coordinates=current_coordinates,
        )


def get_recorded_recurrent_result_material_measurement(
    ledger: EventLedger,
    result_event_identity: str,
    *,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> dict[str, Any]:
    cache_key = ("recurrent_result_material_result", result_event_identity)
    if _validated is not None and cache_key in _validated:
        return _validated[cache_key]
    result = ledger.get(
        _identity(result_event_identity, "exact-material Measurement requires one result")
    )
    if (
        result is None
        or type(result.exact_material) is not bytes
        or ledger.integrity_of(result.identity) == CORRUPTED
    ):
        raise ValueError("exact-material Measurement result is not exact")
    act = _require_yield(
        ledger,
        result,
        exact_act=RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT,
        occurrence_boundary=RECURRENT_RESULT_MATERIAL_MEASUREMENT_BOUNDARY,
    )
    material = _coordinates(result.material)
    subject = material.get("subject")
    if type(subject) is not dict:
        raise ValueError("exact-material Measurement carries no exact subject")
    recurrence_reference = subject.get("recurrence_result_reference")
    coordinate_reference = subject.get("coordinate_measurement_result_reference")
    if type(recurrence_reference) is not dict or type(coordinate_reference) is not dict:
        raise ValueError("exact-material Measurement carries no exact source results")
    recurrence_event = _recorded_occurrence(
        ledger,
        recurrence_reference.get("recorded_occurrence_reference"),
        message="exact-material Measurement carries no exact recurrence result",
    )
    _recurrence_act, recurrence = _require_preserved_result(
        ledger,
        recurrence_event,
        exact_act=RECURRENCE_MEASUREMENT_ACT,
        occurrence_boundary=RECURRENCE_MEASUREMENT_BOUNDARY,
    )
    if recurrence_reference.get("result_reference") != recurrence["result_identity"]:
        raise ValueError("exact-material Measurement carries no exact recurrence result")
    matching = tuple(
        group
        for group in recurrence["findings"]
        if group.get("finding_reference")
        == subject.get("recurrence_finding_reference")
        and "recurrence" in group
    )
    if len(matching) != 1:
        raise ValueError("exact-material Measurement carries no exact recurrence finding")
    coordinate_event = _recorded_occurrence(
        ledger,
        coordinate_reference.get("recorded_occurrence_reference"),
        message="exact-material Measurement carries no exact coordinate result",
    )
    _coordinate_act, coordinate_measurement = _require_preserved_result(
        ledger,
        coordinate_event,
        exact_act=COORDINATE_MEASUREMENT_ACT,
        occurrence_boundary=COORDINATE_MEASUREMENT_BOUNDARY,
    )
    if coordinate_reference.get("result_reference") != coordinate_measurement[
        "result_identity"
    ]:
        raise ValueError("exact-material Measurement carries no exact coordinate result")
    expected = _recurrent_result_material_payload(
        ledger,
        recurrence_event=recurrence_event,
        recurrence=recurrence,
        recurrence_group=matching[0],
        coordinate_event=coordinate_event,
        coordinate_measurement=coordinate_measurement,
    )
    carried = deepcopy(material)
    if (
        expected is None
        or carried != expected
        or _coordinates(act.material).get("subject") != expected["subject"]
        or result.exact_material != bytes(expected["exact_material"])
    ):
        raise ValueError("exact-material Measurement result is not exact")
    reading = {**deepcopy(result.material), **deepcopy(material)}
    if _validated is not None:
        _validated[cache_key] = reading
    return reading


def validate_source_position_recurrence_event(
    ledger: EventLedger,
    event_identity: str,
    *,
    _validated: dict[tuple[str, str], Any] | None = None,
) -> Event:
    """Validate every occurrence exposed by the source-position proof road."""

    event = ledger.get(event_identity)
    if event is None or ledger.integrity_of(event.identity) == CORRUPTED:
        raise ValueError("source-position occurrence is not exact")
    material = event.material
    if type(material) is not dict:
        raise ValueError("source-position occurrence is not exact")
    if event.kind in set(_ACT_RESPONSIBILITY_KINDS.values()):
        return _require_recorded_responsibility(ledger, event)
    if "yield_relation_identity" in material:
        act = ledger.get(material.get("act_occurrence_event_identity"))
        exact_act = (
            act.material.get("act")
            if act is not None and type(act.material) is dict
            else None
        )
        result_readings = {
            RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT: (
                get_recorded_recurrent_result_material_measurement
            ),
            COMPARE_ACT: get_recorded_source_position_compare,
            SOURCE_POSITION_MEASUREMENT_ACT: get_recorded_source_position_measurement,
            RECURRENCE_MEASUREMENT_ACT: get_recorded_source_position_recurrence,
            COORDINATE_MEASUREMENT_ACT: (
                get_recorded_corresponding_coordinate_material_measurement
            ),
        }
        reading = result_readings.get(exact_act)
        if reading is not None:
            reading(ledger, event.identity, _validated=_validated)
            return event
        if exact_act != COMPARE_APPLICABILITY_ACT:
            raise ValueError("source-position result carries no exact Act")
        act = _require_yield(
            ledger,
            event,
            exact_act=COMPARE_APPLICABILITY_ACT,
            occurrence_boundary=COMPARE_APPLICABILITY_BOUNDARY,
        )
        coordinates = _coordinates(event.material)
        subject = coordinates.get("subject")
        if (
            type(subject) is not dict
            or coordinates.get("applicability") != "applicable"
            or _coordinates(act.material).get("subject") != subject
        ):
            raise ValueError("source-position Applicability result is not exact")
        direct = _direct_coordinates(
            ledger,
            subject.get("direct_position_result_occurrence"),
            _validated=_validated,
        )
        coordinates = subject.get("source_position_coordinates")
        compare_subject = subject.get("compare_subject")
        if (
            type(coordinates) is not list
            or type(compare_subject) is not dict
            or tuple(coordinates)
            != tuple(direct[coordinate["position"]] for coordinate in coordinates)
            or subject.get("compare_subject")
            != _pair_subject(
                tuple(coordinates),
                _coordinate_numbers(tuple(coordinates), compare_subject),
            )
        ):
            raise ValueError("source-position Applicability result is not exact")
        return event
    if "act" not in material:
        raise ValueError("source-position occurrence is not exact")
    act_readings = {
        COMPARE_APPLICABILITY_ACT: (COMPARE_APPLICABILITY_ACT, "subject"),
        COMPARE_ACT: (COMPARE_ACT, "subject"),
        SOURCE_POSITION_MEASUREMENT_ACT: (
            SOURCE_POSITION_MEASUREMENT_ACT,
            "subject",
        ),
        RECURRENCE_MEASUREMENT_ACT: (RECURRENCE_MEASUREMENT_ACT, "subject"),
        COORDINATE_MEASUREMENT_ACT: (COORDINATE_MEASUREMENT_ACT, "subject"),
        RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT: (
            RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT,
            "subject",
        ),
    }
    reading = act_readings.get(material.get("act"))
    if reading is None:
        raise ValueError("source-position Act occurrence is not exact")
    exact_act, required_coordinate = reading
    exact = _recorded_occurrence(
        ledger,
        event.identity,
        message="source-position Act occurrence is not exact",
    )
    _require_act_boundary(ledger, exact)
    if (
        exact.material.get("act") != exact_act
        or type(_coordinates(exact.material).get(required_coordinate)) is not dict
    ):
        raise ValueError("source-position Act occurrence is not exact")
    _require_responsibility(ledger, exact)
    return event


def iter_recurrent_coordinate_material_findings(
    ledger: EventLedger,
    measurements: tuple[CorrespondingCoordinateMeasurement, ...],
) -> Iterator[dict[str, Any]]:
    """Yield exact material recurrence findings from all corresponding Measurements."""

    for measurement in measurements:
        material = get_recorded_corresponding_coordinate_material_measurement(
            ledger, measurement.result_occurrence.identity
        )
        for finding in material["findings"]:
            if "recurrence" in finding:
                yield deepcopy(finding)
