"""Grow recurrent ordered extents and measure corresponding carried material.

This is the smallest live proof of two separate declared Measurements:

* recurrence of the complete same-content/difference surface inside each
  ordered source extent;
* literal recurrence at corresponding source-coordinate roles across the
  exact extent results carried by the first recurrence result.

The public producer grows by a caller-declared number of successive extents;
it has no extent-three or extent-four entry point.  The consumer accepts the
complete recurrence result, not a selected recurrence group, role, or value.
The explicit call from producer result to consumer is deliberately left
visible: this module does not claim a general result-uptake dispatcher.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Iterator, NamedTuple

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.evidence_of_yield_relation import (
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    source_position_coordinate_references_of_recorded_position_measurement,
)


COMPARE_APPLICABILITY_ACT_KIND = (
    "operator.ordered_coordinate_set_compare.applicability_act_recorded"
)
COMPARE_APPLICABILITY_RESULT_KIND = (
    "operator.ordered_coordinate_set_compare.applicability_result_recorded"
)
COMPARE_ACT_KIND = "operator.ordered_coordinate_set_compare.act_recorded"
COMPARE_RESULT_KIND = "operator.ordered_coordinate_set_compare.result_recorded"
EXTENT_MEASUREMENT_ACT_KIND = "operator.ordered_coordinate_set.measurement_act_recorded"
EXTENT_MEASUREMENT_RESULT_KIND = "operator.ordered_coordinate_set.measurement_result_recorded"
RECURRENCE_MEASUREMENT_ACT_KIND = (
    "operator.ordered_coordinate_set_recurrence.measurement_act_recorded"
)
RECURRENCE_MEASUREMENT_RESULT_KIND = (
    "operator.ordered_coordinate_set_recurrence.measurement_result_recorded"
)
COORDINATE_MEASUREMENT_ACT_KIND = (
    "operator.recurrence_ordered_coordinate_material.measurement_act_recorded"
)
COORDINATE_MEASUREMENT_RESULT_KIND = (
    "operator.recurrence_ordered_coordinate_material.measurement_result_recorded"
)

EVENT_KIND_RESPONSIBILITIES = {
    COMPARE_APPLICABILITY_ACT_KIND: "02.Acts.A",
    COMPARE_APPLICABILITY_RESULT_KIND: "01.Standing.E.1",
    COMPARE_ACT_KIND: "02.Acts.A",
    COMPARE_RESULT_KIND: "04.Compare",
    EXTENT_MEASUREMENT_ACT_KIND: "02.Acts.A",
    EXTENT_MEASUREMENT_RESULT_KIND: "01.Source.D",
    RECURRENCE_MEASUREMENT_ACT_KIND: "02.Acts.A",
    RECURRENCE_MEASUREMENT_RESULT_KIND: "01.Source.D",
    COORDINATE_MEASUREMENT_ACT_KIND: "02.Acts.A",
    COORDINATE_MEASUREMENT_RESULT_KIND: "01.Source.D",
}

COMPARE_RESPONSIBILITY = "compare exact material at two ordered coordinate roles"
COMPARE_APPLICABILITY_ACT = (
    "Applicability of exact ordered coordinates to Compare"
)
COMPARE_ACT = "Compare exact material at two ordered coordinate roles"
EXTENT_MEASUREMENT_RESPONSIBILITY = (
    "preserve the complete Compare result of an exact ordered coordinate set"
)
EXTENT_MEASUREMENT_ACT = "Measure the complete Compare result"
RECURRENCE_MEASUREMENT_RESPONSIBILITY = (
    "measure exact recurrence of complete internal Compare results"
)
RECURRENCE_MEASUREMENT_ACT = (
    "Measure recurrence of complete internal Compare results"
)
COORDINATE_MEASUREMENT_RESPONSIBILITY = (
    "measure corresponding carried material across exact recurrence support results"
)
COORDINATE_MEASUREMENT_ACT = (
    "Measure corresponding carried material across exact recurrence support results"
)

COMPARE_APPLICABILITY_BOUNDARY = "ordered_coordinate_set_compare_applicability"
COMPARE_BOUNDARY = "ordered_coordinate_set_compare"
EXTENT_MEASUREMENT_BOUNDARY = "ordered_coordinate_set_measurement"
RECURRENCE_MEASUREMENT_BOUNDARY = "ordered_coordinate_set_recurrence_measurement"
COORDINATE_MEASUREMENT_BOUNDARY = (
    "recurrence_ordered_coordinate_material_measurement"
)


class VariableExtentStep(NamedTuple):
    coordinate_count: int
    extent_result_occurrences: tuple[Event, ...]
    recurrence_result_occurrence: Event
    new_event_count: int


class VariableExtentRun(NamedTuple):
    direct_result_event_identity: str
    steps: tuple[VariableExtentStep, ...]
    locality_standing: dict[str, Any]


class CorrespondingCoordinateMeasurement(NamedTuple):
    recurrence_finding_reference: str
    result_occurrence: Event


class CorrespondingCoordinateMeasurementRun(NamedTuple):
    measurements: tuple[CorrespondingCoordinateMeasurement, ...]
    locality_standing: dict[str, Any]


def _canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _digest(prefix: str, value: Any) -> str:
    return prefix + ":" + hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(message)
    return value


def _event(
    ledger: EventLedger, identity: Any, *, kind: str, message: str
) -> Event:
    event = ledger.get(_identity(identity, message))
    if (
        event is None
        or event.kind != kind
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
        raise ValueError("variable extent occurrence carries no exact coordinates")
    return coordinates


def _require_coordinate(coordinate: Any, *, locality_identity: str) -> dict[str, Any]:
    keys = {
        "identity",
        "source_material_acquisition_occurrence_identity",
        "locality_identity",
        "completeness_boundary_identity",
        "position",
        "exact_material",
    }
    if (
        type(coordinate) is not dict
        or set(coordinate) != keys
        or type(coordinate.get("identity")) is not str
        or not coordinate["identity"]
        or type(coordinate.get("source_material_acquisition_occurrence_identity"))
        is not str
        or not coordinate["source_material_acquisition_occurrence_identity"]
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
        raise ValueError("variable extent requires an exact source coordinate")
    return coordinate


def _direct_coordinates(
    ledger: EventLedger, direct_result_event_identity: str
) -> tuple[dict[str, Any], ...]:
    coordinates = tuple(
        source_position_coordinate_references_of_recorded_position_measurement(
            ledger, direct_result_event_identity
        )
    )
    if len(coordinates) < 2:
        raise ValueError("variable extent requires at least two source coordinates")
    locality_identity = coordinates[0]["locality_identity"]
    source_identity = coordinates[0][
        "source_material_acquisition_occurrence_identity"
    ]
    completeness_boundary = coordinates[0]["completeness_boundary_identity"]
    for position, coordinate in enumerate(coordinates):
        _require_coordinate(coordinate, locality_identity=locality_identity)
        if (
            coordinate["position"] != position
            or coordinate["source_material_acquisition_occurrence_identity"]
            != source_identity
            or coordinate["completeness_boundary_identity"]
            != completeness_boundary
        ):
            raise ValueError("direct result carries no exact ordered source population")
    return coordinates


def _preserved_act_material(material):
    return {
        "book_reference": material["book_reference"],
        "result_identity": material["result_identity"],
        "act_identity": material["act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "responsibility": material["responsibility"],
        "responsible_boundary": material["responsible_boundary"],
        "act": material["act"],
        "coordinates": deepcopy(material["coordinates"]),
    }


def _preserved_result_material(material):
    return {
        "book_reference": material["book_reference"],
        "result_identity": material["result_identity"],
        "act_identity": material["act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "responsible_act_evidence_identity": material[
            "responsible_act_evidence_identity"
        ],
        "responsibility": material["responsibility"],
        "responsible_boundary": material["responsible_boundary"],
        "coordinates": deepcopy(material["coordinates"]),
        "evidence_of_yield_relation_identity": material[
            "evidence_of_yield_relation_identity"
        ],
    }


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


def _append_extent_measurement_act(ledger, material, locality_identity):
    return ledger.append(
        EXTENT_MEASUREMENT_ACT_KIND,
        _preserved_act_material(material),
        locality_identity=locality_identity,
    )


def _append_extent_measurement_result(ledger, material, locality_identity):
    return ledger.append(
        EXTENT_MEASUREMENT_RESULT_KIND,
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


_EVENT_APPENDERS = {
    COMPARE_APPLICABILITY_ACT_KIND: _append_compare_applicability_act,
    COMPARE_APPLICABILITY_RESULT_KIND: _append_compare_applicability_result,
    COMPARE_ACT_KIND: _append_compare_act,
    COMPARE_RESULT_KIND: _append_compare_result,
    EXTENT_MEASUREMENT_ACT_KIND: _append_extent_measurement_act,
    EXTENT_MEASUREMENT_RESULT_KIND: _append_extent_measurement_result,
    RECURRENCE_MEASUREMENT_ACT_KIND: _append_recurrence_measurement_act,
    RECURRENCE_MEASUREMENT_RESULT_KIND: _append_recurrence_measurement_result,
    COORDINATE_MEASUREMENT_ACT_KIND: _append_coordinate_measurement_act,
    COORDINATE_MEASUREMENT_RESULT_KIND: _append_coordinate_measurement_result,
}


def _record_yielded_result(
    ledger: EventLedger,
    *,
    act_kind: str,
    result_kind: str,
    exact_act: str,
    responsibility: str,
    book_reference: str,
    occurrence_boundary: str,
    locality_identity: str,
    act_payload: dict[str, Any],
    result_payload: dict[str, Any],
    identity_prefix: str,
) -> tuple[Event, Event]:
    locality_events = ledger.list_locality(locality_identity)
    if not locality_events:
        raise ValueError("variable extent work requires an exact Locality boundary")
    standing_boundary_occurrence_reference = locality_events[-1].identity
    act_identity = new_identity(identity_prefix + "_act")
    act_occurrence_identity = new_identity(identity_prefix + "_act_occurrence")
    result_identity = new_identity(identity_prefix + "_result")
    act = _EVENT_APPENDERS[act_kind](
        ledger,
        {
            "book_reference": book_reference,
            "act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "result_identity": result_identity,
            "act": exact_act,
            "responsibility": responsibility,
            "responsible_boundary": "this Seed",
            "coordinates": {
                "standing_boundary_occurrence_reference": (
                    standing_boundary_occurrence_reference
                ),
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
        "responsible_act_evidence_identity": act.identity,
        "responsibility": responsibility,
        "responsible_boundary": "this Seed",
        "coordinates": deepcopy(result_payload),
    }
    yielded = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=locality_identity,
        exact_act=exact_act,
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=act.identity,
        result_kind=result_kind,
        result_identity=result_identity,
        result_content=content,
        responsibility=responsibility,
        occurrence_boundary=occurrence_boundary,
        responsible_boundary="this Seed",
    )
    result = _EVENT_APPENDERS[result_kind](
        ledger,
        {**content, "evidence_of_yield_relation_identity": yielded.identity},
        locality_identity,
    )
    return act, result


def _require_yield(
    ledger: EventLedger,
    result: Event,
    *,
    act_kind: str,
    exact_act: str,
    responsibility: str,
    occurrence_boundary: str,
) -> Event:
    act = _event(
        ledger,
        result.material.get("responsible_act_evidence_identity"),
        kind=act_kind,
        message="recorded result carries no exact responsible Act occurrence",
    )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        evidence_of_yield_relation_event_identity=result.material.get(
            "evidence_of_yield_relation_identity"
        ),
        responsible_act_evidence_event_identity=act.identity,
    )
    yielded = ledger.get(result.material.get("evidence_of_yield_relation_identity"))
    if (
        result.locality_identity != act.locality_identity
        or act.material.get("act") != exact_act
        or act.material.get("responsibility") != responsibility
        or result.material.get("responsibility") != responsibility
        or yielded is None
        or yielded.material.get("occurrence_boundary") != occurrence_boundary
        or not all(requirements.values())
    ):
        raise ValueError("recorded result carries no exact Yield relation")
    _require_act_boundary(ledger, act)
    return act


def _require_act_boundary(ledger: EventLedger, act: Event) -> None:
    boundary_identity = _coordinates(act.material).get(
        "standing_boundary_occurrence_reference"
    )
    if type(boundary_identity) is not str or not boundary_identity:
        raise ValueError("variable extent Act carries no exact Standing boundary")
    ordered = ledger.occurrences_in_append_order(
        (boundary_identity, act.identity),
        locality_identity=act.locality_identity,
    )
    if tuple(event.identity for event in ordered) != (
        boundary_identity,
        act.identity,
    ):
        raise ValueError("variable extent Act carries no exact Standing boundary")


def _require_current_measurement_subject(
    ledger: EventLedger,
    *,
    locality_identity: str,
    measurement_result_event_identity: str,
    locality_standing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    standing = (
        read_operator_locality_standing(ledger, locality_identity=locality_identity)
        if locality_standing is None
        else locality_standing
    )
    locality_events = ledger.list_locality(locality_identity)
    if (
        type(standing) is not dict
        or standing.get("locality_identity") != locality_identity
        or not locality_events
        or standing.get("through_event_occurrence_identity")
        != locality_events[-1].identity
        or measurement_result_event_identity
        not in standing.get("measurement_occurrences", {})
    ):
        raise ValueError("current Standing carries no exact Measurement subject")
    return standing


def _carry_recorded_events(
    ledger: EventLedger,
    standing: dict[str, Any],
    events: tuple[Event, ...],
) -> dict[str, Any]:
    """Advance through the exact new occurrences using the Standing reader.

    Standing deliberately does not count every durable lifecycle occurrence.
    Keeping a second partial implementation here made its carried coordinates
    agree with replay while its boundary count did not.  The existing bounded
    advance is the exact contract and does not reread the earlier Locality.
    """

    from seed_runtime.operator_locality_standing import (
        advance_operator_locality_standing,
    )

    if not events:
        return standing
    return advance_operator_locality_standing(
        ledger,
        (event.identity for event in events),
        locality_identity=events[0].locality_identity,
        prior=standing,
    )


def _pair_subject(
    coordinates: tuple[dict[str, Any], ...], pair: tuple[int, int]
) -> dict[str, Any]:
    first_role, second_role = pair
    if (
        type(first_role) is not int
        or type(second_role) is not int
        or first_role < 0
        or second_role <= first_role
        or second_role >= len(coordinates)
    ):
        raise ValueError("extent Compare requires an exact ordered role pair")
    return {
        "first_role": first_role,
        "second_role": second_role,
        "first_source_position_coordinate": deepcopy(coordinates[first_role]),
        "second_source_position_coordinate": deepcopy(coordinates[second_role]),
    }


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
        "ordered_coordinates": deepcopy(list(coordinates)),
        "ordered_role_pair": list(pair),
        "compare_subject": deepcopy(subject),
        "prior_result_reference": deepcopy(prior_result_reference),
    }
    _applicability_act, applicability = _record_yielded_result(
        ledger,
        act_kind=COMPARE_APPLICABILITY_ACT_KIND,
        result_kind=COMPARE_APPLICABILITY_RESULT_KIND,
        exact_act=COMPARE_APPLICABILITY_ACT,
        responsibility=COMPARE_RESPONSIBILITY,
        book_reference="01.Standing.E.1",
        occurrence_boundary=COMPARE_APPLICABILITY_BOUNDARY,
        locality_identity=locality_identity,
        act_payload={"subject": deepcopy(applicability_subject)},
        result_payload={
            "subject": deepcopy(applicability_subject),
            "applicability": "applicable",
        },
        identity_prefix="ordered_coordinate_set_compare_applicability",
    )
    first_participation_identity = new_identity(
        "ordered_coordinate_set_compare_first_participation"
    )
    second_participation_identity = new_identity(
        "ordered_coordinate_set_compare_second_participation"
    )
    finding = (
        "same-content"
        if subject["first_source_position_coordinate"]["exact_material"]
        == subject["second_source_position_coordinate"]["exact_material"]
        else "difference"
    )
    compare_subject = {
        **deepcopy(applicability_subject),
        "applicability_result_reference": _result_reference(applicability),
    }
    _compare_act, result = _record_yielded_result(
        ledger,
        act_kind=COMPARE_ACT_KIND,
        result_kind=COMPARE_RESULT_KIND,
        exact_act=COMPARE_ACT,
        responsibility=COMPARE_RESPONSIBILITY,
        book_reference="04.Compare",
        occurrence_boundary=COMPARE_BOUNDARY,
        locality_identity=locality_identity,
        act_payload={
            "subject": deepcopy(compare_subject),
            "participation_relations": [
                {
                    "first_subject": deepcopy(
                        subject["first_source_position_coordinate"]
                    ),
                    "relation": "participation",
                    "second_subject": {"role": pair[0]},
                    "relation_occurrence_reference": first_participation_identity,
                },
                {
                    "first_subject": deepcopy(
                        subject["second_source_position_coordinate"]
                    ),
                    "relation": "participation",
                    "second_subject": {"role": pair[1]},
                    "relation_occurrence_reference": second_participation_identity,
                },
            ],
        },
        result_payload={
            "subject": deepcopy(compare_subject),
            "finding": {
                "finding_reference": _digest(
                    "ordered-coordinate-set-compare",
                    {"subject": subject, "result": finding},
                ),
                "subject": deepcopy(subject),
                "result": finding,
            },
        },
        identity_prefix="ordered_coordinate_set_compare",
    )
    return result


def get_recorded_ordered_coordinate_set_compare(
    ledger: EventLedger, result_event_identity: str
) -> dict[str, Any]:
    result = _event(
        ledger,
        result_event_identity,
        kind=COMPARE_RESULT_KIND,
        message="variable extent Compare result is not exact",
    )
    act = _require_yield(
        ledger,
        result,
        act_kind=COMPARE_ACT_KIND,
        exact_act=COMPARE_ACT,
        responsibility=COMPARE_RESPONSIBILITY,
        occurrence_boundary=COMPARE_BOUNDARY,
    )
    result_coordinates = _coordinates(result.material)
    subject = result_coordinates.get("subject")
    if type(subject) is not dict:
        raise ValueError("variable extent Compare carries no exact subject")
    direct_identity = subject.get("direct_position_result_occurrence")
    direct_coordinates = _direct_coordinates(ledger, direct_identity)
    coordinates = subject.get("ordered_coordinates")
    pair = subject.get("ordered_role_pair")
    if (
        type(coordinates) is not list
        or type(pair) is not list
        or len(pair) != 2
        or any(type(role) is not int for role in pair)
    ):
        raise ValueError("variable extent Compare carries no exact ordered subject")
    coordinate_tuple = tuple(coordinates)
    expected_source = tuple(
        direct_coordinates[coordinate["position"]] for coordinate in coordinate_tuple
    )
    expected_pair_subject = _pair_subject(coordinate_tuple, tuple(pair))
    applicability = _event(
        ledger,
        subject.get("applicability_result_reference", {}).get(
            "recorded_occurrence_reference"
        ),
        kind=COMPARE_APPLICABILITY_RESULT_KIND,
        message="variable extent Compare carries no exact Applicability result",
    )
    applicability_act = _require_yield(
        ledger,
        applicability,
        act_kind=COMPARE_APPLICABILITY_ACT_KIND,
        exact_act=COMPARE_APPLICABILITY_ACT,
        responsibility=COMPARE_RESPONSIBILITY,
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
        prior = get_recorded_variable_extent(
            ledger, prior_reference.get("recorded_occurrence_reference")
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
        == ({"role": pair[0]}, {"role": pair[1]})
        and all(
            type(item.get("relation_occurrence_reference")) is str
            and item["relation_occurrence_reference"]
            for item in participation
        )
        and participation[0]["relation_occurrence_reference"]
        != participation[1]["relation_occurrence_reference"]
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
        or finding.get("finding_reference")
        != _digest(
            "ordered-coordinate-set-compare",
            {"subject": expected_pair_subject, "result": expected_result},
        )
    ):
        raise ValueError("variable extent Compare result is not exact")
    return {**deepcopy(result.material), **deepcopy(result_coordinates)}


def _complete_pairs(length: int) -> tuple[tuple[int, int], ...]:
    # Established comparisons remain the exact prefix when the extent grows.
    # Only pairs introduced by the new final role are appended.
    return tuple(
        (first, second)
        for second in range(1, length)
        for first in range(second)
    )


def _record_extent_result(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    coordinates: tuple[dict[str, Any], ...],
    compare_results: tuple[Event, ...],
    newly_introduced_compare_results: tuple[Event, ...],
    prior_extent_result: Event | None,
) -> Event:
    readings = tuple(
        get_recorded_ordered_coordinate_set_compare(ledger, event.identity)
        for event in compare_results
    )
    pairs = tuple(tuple(reading["subject"]["ordered_role_pair"]) for reading in readings)
    if pairs != _complete_pairs(len(coordinates)):
        raise ValueError("extent result requires its complete internal Compare population")
    signature = [
        {
            "first_role": pair[0],
            "second_role": pair[1],
            "result": reading["finding"]["result"],
        }
        for pair, reading in zip(pairs, readings, strict=True)
    ]
    prior_reference = (
        _result_reference(prior_extent_result)
        if prior_extent_result is not None
        else None
    )
    payload = {
        "direct_position_result_occurrence": direct_result_event_identity,
        "coordinate_count": len(coordinates),
        "source_position_coordinates": deepcopy(list(coordinates)),
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
        act_kind=EXTENT_MEASUREMENT_ACT_KIND,
        result_kind=EXTENT_MEASUREMENT_RESULT_KIND,
        exact_act=EXTENT_MEASUREMENT_ACT,
        responsibility=EXTENT_MEASUREMENT_RESPONSIBILITY,
        book_reference="01.Source.D",
        occurrence_boundary=EXTENT_MEASUREMENT_BOUNDARY,
        locality_identity=coordinates[0]["locality_identity"],
        act_payload={"subject": deepcopy(payload)},
        result_payload=payload,
        identity_prefix="ordered_coordinate_set_measurement",
    )
    return result


def get_recorded_variable_extent(
    ledger: EventLedger, result_event_identity: str
) -> dict[str, Any]:
    result = _event(
        ledger,
        result_event_identity,
        kind=EXTENT_MEASUREMENT_RESULT_KIND,
        message="variable extent result is not exact",
    )
    act = _require_yield(
        ledger,
        result,
        act_kind=EXTENT_MEASUREMENT_ACT_KIND,
        exact_act=EXTENT_MEASUREMENT_ACT,
        responsibility=EXTENT_MEASUREMENT_RESPONSIBILITY,
        occurrence_boundary=EXTENT_MEASUREMENT_BOUNDARY,
    )
    material = _coordinates(result.material)
    direct_coordinates = _direct_coordinates(
        ledger, material.get("direct_position_result_occurrence")
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
        raise ValueError("variable extent result carries no exact population")
    start = coordinates[0].get("position")
    if (
        type(start) is not int
        or tuple(coordinates) != direct_coordinates[start : start + length]
        or tuple(coordinate["position"] for coordinate in coordinates)
        != tuple(range(start, start + length))
    ):
        raise ValueError("variable extent result carries no exact ordered coordinates")
    readings = []
    for reference in references:
        if type(reference) is not dict:
            raise ValueError("variable extent result carries no exact Compare reference")
        reading = get_recorded_ordered_coordinate_set_compare(
            ledger, reference.get("recorded_occurrence_reference")
        )
        if reference.get("result_reference") != reading["result_identity"]:
            raise ValueError("variable extent result carries no exact Compare reference")
        readings.append(reading)
    pairs = tuple(tuple(reading["subject"]["ordered_role_pair"]) for reading in readings)
    expected_surface = [
        {
            "first_role": pair[0],
            "second_role": pair[1],
            "result": reading["finding"]["result"],
        }
        for pair, reading in zip(pairs, readings, strict=True)
    ]
    prior_reference = material.get("prior_result_reference")
    if prior_reference is None:
        expected_new = references
        prior_material = None
    else:
        if type(prior_reference) is not dict:
            raise ValueError("variable extent result carries no exact prior result")
        prior_material = get_recorded_variable_extent(
            ledger, prior_reference.get("recorded_occurrence_reference")
        )
        if (
            prior_reference.get("result_reference") != prior_material["result_identity"]
            or prior_material["source_position_coordinates"] != coordinates[:-1]
            or prior_material["compare_result_references"]
            != references[: len(prior_material["compare_result_references"])]
        ):
            raise ValueError("variable extent result carries no exact prior result")
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
                "responsible_act_evidence_identity",
                "responsibility",
                "responsible_boundary",
                "evidence_of_yield_relation_identity",
            }
        }
    ):
        raise ValueError("variable extent result is not exact")
    return {**deepcopy(result.material), **deepcopy(material)}


def _extent_events_at_boundary(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    coordinate_count: int,
    boundary: EventLedgerBoundary,
    locality_identity: str,
) -> tuple[Event, ...]:
    events = []
    for event in ledger.list(through=boundary):
        if (
            event.kind == EXTENT_MEASUREMENT_RESULT_KIND
            and event.locality_identity == locality_identity
            and _coordinates(event.material).get(
                "direct_position_result_occurrence"
            )
            == direct_result_event_identity
            and _coordinates(event.material).get("coordinate_count") == coordinate_count
        ):
            get_recorded_variable_extent(ledger, event.identity)
            events.append(event)
    return tuple(events)


def _recurrence_groups(extents: tuple[Event, ...]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Event]] = {}
    surfaces: dict[str, list[dict[str, Any]]] = {}
    for event in extents:
        event_coordinates = _coordinates(event.material)
        surface = event_coordinates["complete_compare_findings"]
        key = _canonical(surface)
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
            "ordered-coordinate-result-set",
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
                    "ordered-coordinate-recurrence",
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
) -> Event:
    boundary = ledger.append_boundary()
    extents = _extent_events_at_boundary(
        ledger,
        direct_result_event_identity=direct_result_event_identity,
        coordinate_count=coordinate_count,
        boundary=boundary,
        locality_identity=locality_identity,
    )
    if not extents:
        raise ValueError("recurrence Measurement requires exact extent results")
    groups = _recurrence_groups(extents)
    payload = {
        "direct_position_result_occurrence": direct_result_event_identity,
        "coordinate_count": coordinate_count,
        "completeness_boundary_reference": boundary.identity,
        "ordered_coordinate_result_references": [_result_reference(event) for event in extents],
        "findings": groups,
    }
    _act, result = _record_yielded_result(
        ledger,
        act_kind=RECURRENCE_MEASUREMENT_ACT_KIND,
        result_kind=RECURRENCE_MEASUREMENT_RESULT_KIND,
        exact_act=RECURRENCE_MEASUREMENT_ACT,
        responsibility=RECURRENCE_MEASUREMENT_RESPONSIBILITY,
        book_reference="01.Source.D",
        occurrence_boundary=RECURRENCE_MEASUREMENT_BOUNDARY,
        locality_identity=locality_identity,
        act_payload={"subject": deepcopy(payload)},
        result_payload=payload,
        identity_prefix="ordered_coordinate_set_recurrence_measurement",
    )
    return result


def get_recorded_variable_extent_recurrence(
    ledger: EventLedger, result_event_identity: str
) -> dict[str, Any]:
    result = _event(
        ledger,
        result_event_identity,
        kind=RECURRENCE_MEASUREMENT_RESULT_KIND,
        message="variable extent recurrence result is not exact",
    )
    act = _require_yield(
        ledger,
        result,
        act_kind=RECURRENCE_MEASUREMENT_ACT_KIND,
        exact_act=RECURRENCE_MEASUREMENT_ACT,
        responsibility=RECURRENCE_MEASUREMENT_RESPONSIBILITY,
        occurrence_boundary=RECURRENCE_MEASUREMENT_BOUNDARY,
    )
    material = _coordinates(result.material)
    boundary_identity = material.get("completeness_boundary_reference")
    if type(boundary_identity) is not str or not boundary_identity:
        raise ValueError("recurrence result carries no exact completeness boundary")
    extents = _extent_events_at_boundary(
        ledger,
        direct_result_event_identity=material.get(
            "direct_position_result_occurrence"
        ),
        coordinate_count=material.get("coordinate_count"),
        boundary=EventLedgerBoundary(boundary_identity),
        locality_identity=result.locality_identity,
    )
    expected_payload = {
        "direct_position_result_occurrence": material[
            "direct_position_result_occurrence"
        ],
        "coordinate_count": material["coordinate_count"],
        "completeness_boundary_reference": boundary_identity,
        "ordered_coordinate_result_references": [_result_reference(event) for event in extents],
        "findings": _recurrence_groups(extents),
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
            "responsible_act_evidence_identity",
            "responsibility",
            "responsible_boundary",
            "evidence_of_yield_relation_identity",
        }
    }
    if (
        carried_payload != expected_payload
        or _coordinates(act.material).get("subject") != expected_payload
    ):
        raise ValueError("variable extent recurrence result is not exact")
    return {**deepcopy(result.material), **deepcopy(material)}


def _extend_recurrent_extents(
    ledger: EventLedger,
    *,
    recurrence_result: Event,
    direct_coordinates: tuple[dict[str, Any], ...],
) -> tuple[Event, ...]:
    recurrence = get_recorded_variable_extent_recurrence(
        ledger, recurrence_result.identity
    )
    extended = []
    for finding in recurrence["findings"]:
        if "recurrence" not in finding:
            continue
        for reference in finding["support_result_references"]:
            prior_event = _event(
                ledger,
                reference["recorded_occurrence_reference"],
                kind=EXTENT_MEASUREMENT_RESULT_KIND,
                message="recurrence carries no exact producing extent",
            )
            prior = get_recorded_variable_extent(ledger, prior_event.identity)
            if reference["result_reference"] != prior["result_identity"]:
                raise ValueError("recurrence carries no exact producing extent")
            prior_coordinates = tuple(prior["source_position_coordinates"])
            next_position = prior_coordinates[-1]["position"] + 1
            if next_position >= len(direct_coordinates):
                continue
            coordinates = (*prior_coordinates, direct_coordinates[next_position])
            prior_compare_events = tuple(
                _event(
                    ledger,
                    compare_reference["recorded_occurrence_reference"],
                    kind=COMPARE_RESULT_KIND,
                    message="prior extent carries no exact Compare result",
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
                    pair=(role, len(coordinates) - 1),
                    prior_result_reference=_result_reference(prior_event),
                )
                for role in range(len(coordinates) - 1)
            )
            extended.append(
                _record_extent_result(
                    ledger,
                    direct_result_event_identity=recurrence[
                        "direct_position_result_occurrence"
                    ],
                    coordinates=coordinates,
                    compare_results=(*prior_compare_events, *new_results),
                    newly_introduced_compare_results=new_results,
                    prior_extent_result=prior_event,
                )
            )
    return tuple(extended)


def _record_variable_extent_steps(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    extension_count: int,
) -> VariableExtentRun:
    """Record the minimal ordered extents and exact recurrence-led extensions."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("variable extent recording requires an EventLedger")
    if type(extension_count) is not int or extension_count < 0:
        raise ValueError("variable extent recording requires a nonnegative extension count")
    direct_coordinates = _direct_coordinates(ledger, direct_result_event_identity)
    locality_identity = direct_coordinates[0]["locality_identity"]
    standing = _require_current_measurement_subject(
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
            _record_extent_result(
                ledger,
                direct_result_event_identity=direct_result_event_identity,
                coordinates=coordinates,
                compare_results=(compare,),
                newly_introduced_compare_results=(compare,),
                prior_extent_result=None,
            )
        )
    recurrence = _record_recurrence_measurement(
        ledger,
        direct_result_event_identity=direct_result_event_identity,
        coordinate_count=2,
        locality_identity=locality_identity,
    )
    steps.append(
        VariableExtentStep(2, tuple(minimal), recurrence, len(ledger.list()) - before)
    )

    for _ in range(extension_count):
        before = len(ledger.list())
        extents = _extend_recurrent_extents(
            ledger,
            recurrence_result=recurrence,
            direct_coordinates=direct_coordinates,
        )
        if not extents:
            break
        coordinate_count = _coordinates(extents[0].material)["coordinate_count"]
        recurrence = _record_recurrence_measurement(
            ledger,
            direct_result_event_identity=direct_result_event_identity,
            coordinate_count=coordinate_count,
            locality_identity=locality_identity,
        )
        steps.append(
            VariableExtentStep(
                coordinate_count,
                extents,
                recurrence,
                len(ledger.list()) - before,
            )
        )
    new_events = tuple(ledger.list_locality(locality_identity)[locality_event_count:])
    return VariableExtentRun(
        direct_result_event_identity,
        tuple(steps),
        _carry_recorded_events(ledger, standing, new_events),
    )


def record_variable_extent_steps(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    extension_count: int,
) -> VariableExtentRun:
    """Record the exact proof road in a durable mechanics boundary."""

    with ledger.batched():
        return _record_variable_extent_steps(
            ledger,
            direct_result_event_identity=direct_result_event_identity,
            extension_count=extension_count,
        )


def _coordinate_findings(
    ledger: EventLedger, recurrence_group: dict[str, Any]
) -> list[dict[str, Any]]:
    productions = []
    for reference in recurrence_group["support_result_references"]:
        material = get_recorded_variable_extent(
            ledger, reference["recorded_occurrence_reference"]
        )
        if reference["result_reference"] != material["result_identity"]:
            raise ValueError("coordinate Measurement carries no exact production")
        productions.append((reference, material))
    coordinate_count = recurrence_group["subject"]["coordinate_count"]
    if any(production[1]["coordinate_count"] != coordinate_count for production in productions):
        raise ValueError("coordinate Measurement productions carry different extents")
    findings = []
    for role in range(coordinate_count):
        grouped: dict[int, list[dict[str, Any]]] = {}
        coordinates: dict[int, list[dict[str, Any]]] = {}
        for reference, production in productions:
            coordinate = production["source_position_coordinates"][role]
            value = coordinate["exact_material"][0]
            grouped.setdefault(value, []).append(deepcopy(reference))
            coordinates.setdefault(value, []).append(deepcopy(coordinate))
        for value in sorted(grouped):
            subject = {
                "recurrence_finding_reference": recurrence_group[
                    "finding_reference"
                ],
                "coordinate_role": role,
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
                "recurrence-ordered-coordinate-material-set",
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
                        "recurrence-ordered-coordinate-material-recurrence",
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
    locality_standing: dict[str, Any],
) -> CorrespondingCoordinateMeasurementRun:
    """Measure every recurrent group, coordinate role, and exact carried value."""

    recurrence_event = _event(
        ledger,
        recurrence_result_event_identity,
        kind=RECURRENCE_MEASUREMENT_RESULT_KIND,
        message="coordinate Measurement requires an exact recurrence result",
    )
    locality_identity = recurrence_event.locality_identity
    standing = _require_current_measurement_subject(
        ledger,
        locality_identity=locality_identity,
        measurement_result_event_identity=recurrence_result_event_identity,
        locality_standing=locality_standing,
    )
    locality_event_count = len(ledger.list_locality(locality_identity))
    recurrence = get_recorded_variable_extent_recurrence(
        ledger, recurrence_result_event_identity
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
            "support_result_references": deepcopy(
                group["support_result_references"]
            ),
            "completeness_boundary_reference": recurrence[
                "completeness_boundary_reference"
            ],
            "findings": _coordinate_findings(ledger, group),
        }
        _act, result = _record_yielded_result(
            ledger,
            act_kind=COORDINATE_MEASUREMENT_ACT_KIND,
            result_kind=COORDINATE_MEASUREMENT_RESULT_KIND,
            exact_act=COORDINATE_MEASUREMENT_ACT,
            responsibility=COORDINATE_MEASUREMENT_RESPONSIBILITY,
            book_reference="01.Source.D.1",
            occurrence_boundary=COORDINATE_MEASUREMENT_BOUNDARY,
            locality_identity=locality_identity,
            act_payload={"subject": deepcopy(payload)},
            result_payload=payload,
            identity_prefix="recurrence_ordered_coordinate_material_measurement",
        )
        recorded.append(
            CorrespondingCoordinateMeasurement(group["finding_reference"], result)
        )
    new_events = tuple(ledger.list_locality(locality_identity)[locality_event_count:])
    return CorrespondingCoordinateMeasurementRun(
        tuple(recorded),
        _carry_recorded_events(ledger, standing, new_events),
    )


def record_corresponding_coordinate_material_measurements(
    ledger: EventLedger,
    *,
    recurrence_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> CorrespondingCoordinateMeasurementRun:
    """Record the complete consumer population in a mechanics boundary."""

    with ledger.batched():
        return _record_corresponding_coordinate_material_measurements(
            ledger,
            recurrence_result_event_identity=recurrence_result_event_identity,
            locality_standing=locality_standing,
        )


def get_recorded_corresponding_coordinate_material_measurement(
    ledger: EventLedger, result_event_identity: str
) -> dict[str, Any]:
    result = _event(
        ledger,
        result_event_identity,
        kind=COORDINATE_MEASUREMENT_RESULT_KIND,
        message="corresponding-coordinate Measurement result is not exact",
    )
    act = _require_yield(
        ledger,
        result,
        act_kind=COORDINATE_MEASUREMENT_ACT_KIND,
        exact_act=COORDINATE_MEASUREMENT_ACT,
        responsibility=COORDINATE_MEASUREMENT_RESPONSIBILITY,
        occurrence_boundary=COORDINATE_MEASUREMENT_BOUNDARY,
    )
    material = _coordinates(result.material)
    source_reference = material.get("source_recurrence_result_reference")
    if type(source_reference) is not dict:
        raise ValueError("coordinate Measurement carries no exact recurrence result")
    recurrence = get_recorded_variable_extent_recurrence(
        ledger, source_reference.get("recorded_occurrence_reference")
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
        "findings": _coordinate_findings(ledger, group),
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
            "responsible_act_evidence_identity",
            "responsibility",
            "responsible_boundary",
            "evidence_of_yield_relation_identity",
        }
    }
    if carried_payload != payload or _coordinates(act.material).get("subject") != payload:
        raise ValueError("corresponding-coordinate Measurement result is not exact")
    return {**deepcopy(result.material), **deepcopy(material)}


def validate_variable_extent_event(
    ledger: EventLedger, event_identity: str
) -> Event:
    """Validate every occurrence exposed by the variable-extent proof road."""

    event = ledger.get(event_identity)
    if event is None or event.kind not in EVENT_KIND_RESPONSIBILITIES:
        raise ValueError("variable extent occurrence is not exact")
    if event.kind == COMPARE_RESULT_KIND:
        get_recorded_ordered_coordinate_set_compare(ledger, event.identity)
        return event
    if event.kind == EXTENT_MEASUREMENT_RESULT_KIND:
        get_recorded_variable_extent(ledger, event.identity)
        return event
    if event.kind == RECURRENCE_MEASUREMENT_RESULT_KIND:
        get_recorded_variable_extent_recurrence(ledger, event.identity)
        return event
    if event.kind == COORDINATE_MEASUREMENT_RESULT_KIND:
        get_recorded_corresponding_coordinate_material_measurement(
            ledger, event.identity
        )
        return event
    result_readings = {
        COMPARE_APPLICABILITY_RESULT_KIND: (
            COMPARE_APPLICABILITY_ACT_KIND,
            COMPARE_APPLICABILITY_ACT,
            COMPARE_RESPONSIBILITY,
            COMPARE_APPLICABILITY_BOUNDARY,
        ),
    }
    if event.kind in result_readings:
        act_kind, exact_act, responsibility, occurrence_boundary = result_readings[
            event.kind
        ]
        act = _require_yield(
            ledger,
            event,
            act_kind=act_kind,
            exact_act=exact_act,
            responsibility=responsibility,
            occurrence_boundary=occurrence_boundary,
        )
        coordinates = _coordinates(event.material)
        subject = coordinates.get("subject")
        if (
            type(subject) is not dict
            or coordinates.get("applicability") != "applicable"
            or _coordinates(act.material).get("subject") != subject
        ):
            raise ValueError("variable extent Applicability result is not exact")
        direct = _direct_coordinates(
            ledger, subject.get("direct_position_result_occurrence")
        )
        extent = subject.get("ordered_coordinates")
        pair = subject.get("ordered_role_pair")
        if (
            type(extent) is not list
            or type(pair) is not list
            or len(pair) != 2
            or tuple(extent)
            != tuple(direct[coordinate["position"]] for coordinate in extent)
            or subject.get("compare_subject")
            != _pair_subject(tuple(extent), tuple(pair))
        ):
            raise ValueError("variable extent Applicability result is not exact")
        return event
    act_readings = {
        COMPARE_APPLICABILITY_ACT_KIND: (
            COMPARE_APPLICABILITY_ACT,
            COMPARE_RESPONSIBILITY,
            "subject",
        ),
        COMPARE_ACT_KIND: (COMPARE_ACT, COMPARE_RESPONSIBILITY, "subject"),
        EXTENT_MEASUREMENT_ACT_KIND: (
            EXTENT_MEASUREMENT_ACT,
            EXTENT_MEASUREMENT_RESPONSIBILITY,
            "subject",
        ),
        RECURRENCE_MEASUREMENT_ACT_KIND: (
            RECURRENCE_MEASUREMENT_ACT,
            RECURRENCE_MEASUREMENT_RESPONSIBILITY,
            "subject",
        ),
        COORDINATE_MEASUREMENT_ACT_KIND: (
            COORDINATE_MEASUREMENT_ACT,
            COORDINATE_MEASUREMENT_RESPONSIBILITY,
            "subject",
        ),
    }
    exact_act, responsibility, required_coordinate = act_readings[event.kind]
    exact = _event(
        ledger,
        event.identity,
        kind=event.kind,
        message="variable extent Act occurrence is not exact",
    )
    _require_act_boundary(ledger, exact)
    if (
        exact.material.get("act") != exact_act
        or exact.material.get("responsibility") != responsibility
        or type(_coordinates(exact.material).get(required_coordinate)) is not dict
    ):
        raise ValueError("variable extent Act occurrence is not exact")
    return event


def iter_recurrent_coordinate_material_findings(
    ledger: EventLedger,
    measurements: tuple[CorrespondingCoordinateMeasurement, ...],
) -> Iterator[dict[str, Any]]:
    """Yield exact literal recurrence findings from the complete consumer output."""

    for measurement in measurements:
        material = get_recorded_corresponding_coordinate_material_measurement(
            ledger, measurement.result_occurrence.identity
        )
        for finding in material["findings"]:
            if "recurrence" in finding:
                yield deepcopy(finding)
